"""
MyBatis Mapper XML and Java Interface generator
"""
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from db_connector import DatabaseConnector


class MapperGenerator:
    """Generate MyBatis Mapper XML and Java Interface files"""
    
    def __init__(self, table_name: str):
        self.db_connector = DatabaseConnector()
        self.table_name = table_name
        self.entity_name = self.db_connector.to_camel_case(table_name, capitalize=True)
        self.mapper_name = f"{self.entity_name}Mapper"
        self.columns = []
        self.primary_keys = []
        self.audit_columns = ['creator', 'createDt', 'updater', 'updateDt']
        
        # Fetch metadata on initialization
        self._load_metadata()
    
    def _load_metadata(self):
        """Load table metadata from database"""
        metadata = self.db_connector.fetch_table_metadata(self.table_name)
        self.table_name = metadata['table_name']  # Use actual table name from DB
        self.columns = metadata['columns']
        self.primary_keys = metadata['primary_keys']
        
        if not self.columns:
            raise ValueError(f"No columns found for table {self.table_name}")
    
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
    
    def generate(self):
        """Generate both XML and Java files"""
        xml_content = self.generate_mapper_xml()
        java_content = self.generate_mapper_interface()
        return self.save_to_file(xml_content, java_content)
