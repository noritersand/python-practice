import re
import sys
from pathlib import Path
from datetime import datetime
import pymysql  # pymysql works perfectly with MariaDB

# Import database configuration
from db import DB_TYPE, DB_CONFIG


class MapperGenerator:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.entity_name = self._to_camel_case(table_name, capitalize=True)
        self.mapper_name = f"{self.entity_name}Mapper"
        self.columns = []
        self.primary_keys = []  # Changed from primary_key to primary_keys (list)
        self.audit_columns = ['creator', 'createDt', 'updater', 'updateDt']
        
    def _to_camel_case(self, snake_str: str, capitalize: bool = False) -> str:
        """Convert snake_case to camelCase or PascalCase"""
        components = snake_str.split('_')
        if capitalize:
            return ''.join(x.title() for x in components)
        else:
            return components[0] + ''.join(x.title() for x in components[1:])
    
    def _get_java_type(self, db_type: str) -> str:
        """Map database types to Java types"""
        type_mapping = {
            # Numeric types
            'int': 'java.lang.Integer',
            'integer': 'java.lang.Integer',
            'bigint': 'java.lang.Long',
            'smallint': 'java.lang.Integer',
            'tinyint': 'java.lang.Integer',
            'decimal': 'java.math.BigDecimal',
            'numeric': 'java.math.BigDecimal',
            'float': 'java.lang.Float',
            'double': 'java.lang.Double',
            'real': 'java.lang.Float',
            
            # String types
            'varchar': 'java.lang.String',
            'char': 'java.lang.String',
            'text': 'java.lang.String',
            'longtext': 'java.lang.String',
            'mediumtext': 'java.lang.String',
            'tinytext': 'java.lang.String',
            
            # Date/Time types
            'date': 'java.time.LocalDate',
            'datetime': 'java.time.LocalDateTime',
            'timestamp': 'java.time.LocalDateTime',
            'time': 'java.time.LocalTime',
            
            # Boolean
            'boolean': 'java.lang.Boolean',
            'bit': 'java.lang.Boolean',
            'bool': 'java.lang.Boolean',
            
            # Binary
            'blob': 'byte[]',
            'binary': 'byte[]',
            'varbinary': 'byte[]',
        }
        
        # Extract base type (remove size specification)
        base_type = re.sub(r'\([^)]*\)', '', db_type.lower()).strip()
        return type_mapping.get(base_type, 'java.lang.Object')
    
    def get_connection(self):
        """Get MariaDB connection"""
        config = DB_CONFIG.get(DB_TYPE)
        
        if not config:
            raise ValueError(f"Database configuration not found")
        
        try:
            connection = pymysql.connect(
                host=config['host'],
                port=config['port'],
                user=config['user'],
                password=config['password'],
                database=config['database'],
                charset=config.get('charset', 'utf8mb4'),
                cursorclass=pymysql.cursors.Cursor
            )
            print(f"✅ Connected to MariaDB database: {config['database']}")
            return connection
            
        except Exception as e:
            print(f"❌ Failed to connect to database: {e}")
            raise
    
    def fetch_table_metadata(self):
        """Fetch table column information from MariaDB"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # First, check if table exists and show available tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            available_tables = [table[0] for table in tables]
            
            print(f"📋 Available tables in database: {', '.join(available_tables[:10])}")
            if len(available_tables) > 10:
                print(f"   ... and {len(available_tables) - 10} more tables")
            
            # Check if the table exists (case-insensitive)
            matching_tables = [t for t in available_tables if t.lower() == self.table_name.lower()]
            if matching_tables:
                self.table_name = matching_tables[0]  # Use the actual case from DB
                print(f"✅ Found table: {self.table_name}")
            elif not any(t == self.table_name for t in available_tables):
                print(f"❌ Table '{self.table_name}' not found!")
                print(f"💡 Did you mean one of these?")
                similar = [t for t in available_tables if self.table_name.lower() in t.lower() or t.lower() in self.table_name.lower()]
                if similar:
                    for t in similar[:5]:
                        print(f"   - {t}")
                raise ValueError(f"Table '{self.table_name}' not found in database")
            
            # MariaDB/MySQL query
            cursor.execute("""
                SELECT 
                    COLUMN_NAME,
                    DATA_TYPE,
                    IS_NULLABLE,
                    COLUMN_KEY,
                    COLUMN_DEFAULT,
                    EXTRA
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = %s
                ORDER BY ORDINAL_POSITION
            """, (self.table_name,))
            
            rows = cursor.fetchall()
            
            if not rows:
                raise ValueError(f"Table '{self.table_name}' not found in database")
            
            for row in rows:
                column_name = row[0]
                data_type = row[1]
                is_nullable = row[2] == 'YES'
                is_primary = row[3] == 'PRI'
                extra = row[5]
                
                # Check if it's auto_increment
                is_auto_increment = 'auto_increment' in extra.lower()
                
                column_info = {
                    'db_name': column_name,
                    'java_name': self._to_camel_case(column_name),
                    'java_type': self._get_java_type(data_type),
                    'is_nullable': is_nullable,
                    'is_primary': is_primary,
                    'is_auto_increment': is_auto_increment
                }
                
                self.columns.append(column_info)
                
                # Collect all primary keys
                if is_primary:
                    self.primary_keys.append(column_info)
            
            # Print PK information
            if len(self.primary_keys) > 1:
                pk_names = [pk['db_name'] for pk in self.primary_keys]
                print(f"🔑 Composite Primary Key found: {', '.join(pk_names)}")
            elif len(self.primary_keys) == 1:
                print(f"🔑 Primary Key: {self.primary_keys[0]['db_name']}")
                    
        finally:
            cursor.close()
            conn.close()
    
    def has_update_columns(self) -> bool:
        """Check if table has updater and updateDt columns"""
        column_names = [col['db_name'] for col in self.columns]
        return 'updater' in column_names and 'updateDt' in column_names
    
    def generate_insert(self) -> str:
        """Generate INSERT statement"""
        # Filter out auto-increment primary key and auto-generated timestamps
        insert_columns = [col for col in self.columns 
                         if not (col.get('is_auto_increment', False))
                         and col['db_name'] not in ['createDt', 'updateDt']]
        
        column_list = ',\n            '.join([col['db_name'] for col in insert_columns])
        value_list = ',\n            '.join([f"#{{{col['java_name']}}}" for col in insert_columns])
        
        return f"""    <insert id="insert{self.entity_name}">
        /*{self.mapper_name}.insert{self.entity_name}*/
        insert into {self.table_name} (
            {column_list}
        ) values (
            {value_list}
        )
    </insert>"""
    
    def generate_update(self) -> str:
        """Generate UPDATE statement"""
        # Check if table has update columns
        if not self.has_update_columns():
            return f"    <!-- Table {self.table_name} does not have updater/updateDt columns - UPDATE not needed -->"
        
        if not self.primary_keys:
            return f"    <!-- No primary key found for table {self.table_name} -->"
        
        # Filter out primary keys and audit columns from update fields
        pk_names = [pk['db_name'] for pk in self.primary_keys]
        update_columns = [col for col in self.columns 
                         if col['db_name'] not in pk_names 
                         and col['db_name'] not in ['creator', 'createDt']]
        
        set_clauses = []
        for col in update_columns:
            if col['db_name'] in ['updater', 'updateDt']:
                continue  # Handle these separately
            set_clauses.append(
                f'            <if test="{col["java_name"]} != null">{col["db_name"]} = #{{{col["java_name"]}}},</if>'
            )
        
        set_clause_str = '\n'.join(set_clauses)
        
        # Add updater and updateDt
        update_fields = ""
        if any(col['db_name'] == 'updater' for col in self.columns):
            update_fields += "            updater = #{updater},"
        if any(col['db_name'] == 'updateDt' for col in self.columns):
            update_fields += " updateDt = now()"
        else:
            update_fields = update_fields.rstrip(',')
        
        # Build WHERE clause with all primary keys
        where_conditions = []
        for pk in self.primary_keys:
            where_conditions.append(f"{pk['db_name']} = #{{{pk['java_name']}}}")
        where_clause = '\n        and '.join(where_conditions)
        
        return f"""    <update id="update{self.entity_name}">
        /*{self.mapper_name}.update{self.entity_name}*/
        update {self.table_name}
        <set>
{set_clause_str}
{update_fields}
        </set>
        where {where_clause}
    </update>"""
    
    def generate_delete(self) -> str:
        """Generate DELETE statement"""
        if not self.primary_keys:
            return f"    <!-- No primary key found for table {self.table_name} -->"
        
        # Build WHERE clause with all primary keys
        where_conditions = []
        for pk in self.primary_keys:
            where_conditions.append(f"{pk['db_name']} = #{{{pk['java_name']}}}")
        where_clause = '\n        and '.join(where_conditions)
        
        return f"""    <delete id="delete{self.entity_name}">
        /*{self.mapper_name}.delete{self.entity_name}*/
        delete from {self.table_name}
        where {where_clause}
    </delete>"""
    
    def generate_select(self) -> str:
        """Generate SELECT statement"""
        if not self.primary_keys:
            return f"    <!-- No primary key found for table {self.table_name} -->"
        
        column_list = []
        for i, col in enumerate(self.columns):
            if i % 4 == 0 and i > 0:
                column_list.append('\n            ')
            column_list.append(col['db_name'])
            if i < len(self.columns) - 1:
                column_list.append(', ')
        
        columns_str = ''.join(column_list)
        
        # Build WHERE clause with all primary keys
        where_conditions = []
        for pk in self.primary_keys:
            where_conditions.append(f"{pk['db_name']} = #{{{pk['java_name']}}}")
        where_clause = '\n        and '.join(where_conditions)
        
        # Use FILL_THIS_VALUE for resultType
        result_type = "FILL_THIS_VALUE"
        
        return f"""    <select id="get{self.entity_name}" resultType="{result_type}">
        /*{self.mapper_name}.get{self.entity_name}*/
        select
            {columns_str}
        from {self.table_name}
        where {where_clause}
    </select>"""
    
    def generate_mapper_xml(self) -> str:
        """Generate complete Mapper XML file"""
        self.fetch_table_metadata()
        
        if not self.columns:
            raise ValueError(f"No columns found for table {self.table_name}")
        
        # Check if UPDATE is needed
        has_update = self.has_update_columns()
        
        if has_update:
            xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="FILL_THIS_VALUE">

{self.generate_insert()}

{self.generate_update()}

{self.generate_delete()}

{self.generate_select()}

</mapper>"""
        else:
            # No UPDATE for tables without updater/updateDt
            print(f"ℹ️  Table {self.table_name} does not have updater/updateDt columns - skipping UPDATE generation")
            xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="FILL_THIS_VALUE">

{self.generate_insert()}

{self.generate_delete()}

{self.generate_select()}

</mapper>"""
        
        return xml_content
    
    def generate_mapper_interface(self) -> str:
        """Generate Java Mapper Interface"""
        # Check if UPDATE is needed
        has_update = self.has_update_columns()
        
        # Generate update method only if needed
        update_method = ""
        if has_update:
            update_method = f"""
    /**
     * {self.table_name} 기본 update 메서드
     * 
     * @param entity 입력값
     * @return 처리 개수
     */
    int update{self.entity_name}({self.entity_name}Entity entity);
"""
        
        interface_content = f"""/**
 * {self.table_name} 테이블용 마이바티스 쿼리 매퍼
 */
public interface {self.mapper_name} {{
    /**
     * {self.table_name} 기본 insert 메서드
     *
     * @param entity 입력값 
     * @return 처리 개수
     */
    int insert{self.entity_name}({self.entity_name}Entity entity);
{update_method}
    /**
     * {self.table_name} 기본 delete 메서드
     *
     * @param params 검색 조건
     * @return 처리 개수
     */
    int delete{self.entity_name}(FILL_THIS_TYPE params);

    /**
     * {self.table_name} 기본 단 건 select 메서드
     *
     * @param params 검색 조건
     * @return 조회 결과
     */
    {self.entity_name}Entity get{self.entity_name}(FILL_THIS_TYPE params);

}}"""
        
        return interface_content
    
    def save_to_file(self, xml_content: str, java_content: str):
        """Save generated XML and Java files"""
        # Create result directory if it doesn't exist
        output_dir = Path("result")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save XML file
        xml_filename = f"{self.mapper_name}_{timestamp}.xml"
        xml_filepath = output_dir / xml_filename
        with open(xml_filepath, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        # Save Java interface file
        java_filename = f"{self.mapper_name}_{timestamp}.java"
        java_filepath = output_dir / java_filename
        with open(java_filepath, 'w', encoding='utf-8') as f:
            f.write(java_content)
        
        print(f"✅ Files generated successfully!")
        print(f"📁 XML file: {xml_filepath}")
        print(f"📁 Java file: {java_filepath}")
        return xml_filepath, java_filepath


def main():
    """Main function"""
    # Check command line arguments
    if len(sys.argv) != 2:
        print("❌ Usage: python main.py <table_name>")
        print("Example: python main.py app_push")
        sys.exit(1)
    
    table_name = sys.argv[1].strip()
    
    print("=" * 50)
    print(f"MyBatis Mapper Generator")
    print(f"Table: {table_name}")
    print("=" * 50)
    
    try:
        # Generate mapper
        generator = MapperGenerator(table_name)
        xml_content = generator.generate_mapper_xml()
        java_content = generator.generate_mapper_interface()
        
        # Save to files
        xml_path, java_path = generator.save_to_file(xml_content, java_content)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()