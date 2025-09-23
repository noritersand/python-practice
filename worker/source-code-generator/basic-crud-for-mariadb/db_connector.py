"""
Database connection and metadata fetching module
"""
import re
import pymysql
from typing import List, Dict, Any, Optional

# Import database configuration
from db import DB_TYPE, DB_CONFIG


class DatabaseConnector:
    """Handle database connections and metadata fetching"""
    
    def __init__(self):
        # Note: type_mapping is used for simple DATA_TYPE matching
        # For more precise matching, use get_java_type_from_column_type
        self.type_mapping = {
            # Numeric types
            'int': 'java.lang.Integer',
            'integer': 'java.lang.Integer',
            'bigint': 'java.lang.Long',
            'smallint': 'java.lang.Integer',
            'tinyint': 'java.lang.Boolean',  # Changed to Boolean as per requirement
            'mediumint': 'java.lang.Integer',
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
            'enum': 'java.lang.String',
            'set': 'java.lang.String',
            
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
            'blob': 'java.lang.String',  # Changed to String as per requirement
            'tinyblob': 'java.lang.String',
            'mediumblob': 'java.lang.String',
            'longblob': 'java.lang.String',
            'binary': 'java.lang.String',
            'varbinary': 'java.lang.String',
        }
    
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
    
    def to_camel_case(self, snake_str: str, capitalize: bool = False) -> str:
        """Convert snake_case to camelCase or PascalCase"""
        components = snake_str.split('_')
        if capitalize:
            return ''.join(x.title() for x in components)
        else:
            return components[0] + ''.join(x.title() for x in components[1:])
    
    def get_java_type(self, db_type: str) -> str:
        """Map database types to Java types"""
        # Extract base type (remove size specification)
        base_type = re.sub(r'\([^)]*\)', '', db_type.lower()).strip()
        return self.type_mapping.get(base_type, 'java.lang.Object')
    
    def get_java_type_from_column_type(self, column_type: str) -> str:
        """Map database column types to Java types using COLUMN_TYPE for more precision"""
        column_type_lower = column_type.lower()
        
        # Check column types in order of specificity
        if column_type_lower.startswith('tinyint'):
            return 'java.lang.Boolean'
        elif column_type_lower.startswith('smallint'):
            return 'java.lang.Integer'
        elif column_type_lower.startswith('mediumint'):
            return 'java.lang.Integer'
        elif column_type_lower.startswith('bigint'):
            return 'java.lang.Long'
        elif column_type_lower.startswith('int'):
            return 'java.lang.Integer'
        elif column_type_lower.startswith('float'):
            return 'java.lang.Float'
        elif column_type_lower.startswith('double'):
            return 'java.lang.Double'
        elif column_type_lower.startswith('decimal'):
            return 'java.math.BigDecimal'
        elif column_type_lower.startswith('numeric'):
            return 'java.math.BigDecimal'
        elif column_type_lower.startswith('varchar'):
            return 'java.lang.String'
        elif column_type_lower.startswith('char'):
            return 'java.lang.String'
        elif column_type_lower.startswith('datetime'):
            return 'java.time.LocalDateTime'
        elif column_type_lower.startswith('date'):
            return 'java.time.LocalDate'
        elif column_type_lower.startswith('time'):
            return 'java.time.LocalTime'
        elif column_type_lower.startswith('timestamp'):
            return 'java.time.LocalDateTime'
        elif column_type_lower.startswith('longtext'):
            return 'java.lang.String'
        elif column_type_lower.startswith('mediumtext'):
            return 'java.lang.String'
        elif column_type_lower.startswith('tinytext'):
            return 'java.lang.String'
        elif column_type_lower.startswith('text'):
            return 'java.lang.String'
        elif column_type_lower.startswith('longblob'):
            return 'java.lang.String'
        elif column_type_lower.startswith('mediumblob'):
            return 'java.lang.String'
        elif column_type_lower.startswith('tinyblob'):
            return 'java.lang.String'
        elif column_type_lower.startswith('blob'):
            return 'java.lang.String'
        elif column_type_lower.startswith('binary'):
            return 'java.lang.String'
        elif column_type_lower.startswith('varbinary'):
            return 'java.lang.String'
        elif column_type_lower.startswith('enum'):
            return 'java.lang.String'
        elif column_type_lower.startswith('set'):
            return 'java.lang.String'
        elif column_type_lower.startswith('bool'):
            return 'java.lang.Boolean'
        elif column_type_lower.startswith('bit'):
            return 'java.lang.Boolean'
        else:
            return 'java.lang.Object'
    
    def validate_table(self, cursor, table_name: str) -> str:
        """Validate if table exists and return actual table name"""
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        available_tables = [table[0] for table in tables]
        
        # print(f"📋 Available tables in database: {', '.join(available_tables[:10])}")
        # if len(available_tables) > 10:
        #     print(f"   ... and {len(available_tables) - 10} more tables")
        
        # Check if the table exists (case-insensitive)
        matching_tables = [t for t in available_tables if t.lower() == table_name.lower()]
        if matching_tables:
            actual_table_name = matching_tables[0]  # Use the actual case from DB
            print(f"✅ Found table: {actual_table_name}")
            return actual_table_name
        elif not any(t == table_name for t in available_tables):
            print(f"❌ Table '{table_name}' not found!")
            print(f"💡 Did you mean one of these?")
            similar = [t for t in available_tables if table_name.lower() in t.lower() or t.lower() in table_name.lower()]
            if similar:
                for t in similar[:5]:
                    print(f"   - {t}")
            raise ValueError(f"Table '{table_name}' not found in database")
        
        return table_name
    
    def fetch_table_metadata(self, table_name: str) -> Dict[str, Any]:
        """Fetch table column information from MariaDB"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        columns = []
        primary_keys = []
        table_comment = ""
        
        try:
            # Validate table exists and get actual name
            actual_table_name = self.validate_table(cursor, table_name)
            
            # Get table comment
            cursor.execute("""
                SELECT TABLE_COMMENT
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = %s
            """, (actual_table_name,))
            
            table_result = cursor.fetchone()
            if table_result:
                table_comment = table_result[0] if table_result[0] else ""
            
            # MariaDB/MySQL query with column comments
            cursor.execute("""
                SELECT 
                    COLUMN_NAME,
                    DATA_TYPE,
                    IS_NULLABLE,
                    COLUMN_KEY,
                    COLUMN_DEFAULT,
                    EXTRA,
                    COLUMN_COMMENT,
                    COLUMN_TYPE
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = %s
                ORDER BY ORDINAL_POSITION
            """, (actual_table_name,))
            
            rows = cursor.fetchall()
            
            if not rows:
                raise ValueError(f"Table '{actual_table_name}' not found in database")
            
            for row in rows:
                column_name = row[0]
                data_type = row[1]
                is_nullable = row[2] == 'YES'
                is_primary = row[3] == 'PRI'
                extra = row[5]
                column_comment = row[6] if row[6] else ""
                column_type = row[7]
                
                # Skip syncTrigger column
                if column_name == 'syncTrigger':
                    continue
                
                # Check if it's auto_increment
                is_auto_increment = 'auto_increment' in extra.lower() if extra else False
                
                # Use column_type for more precise type mapping
                java_type = self.get_java_type_from_column_type(column_type)
                
                column_info = {
                    'db_name': column_name,
                    'java_name': self.to_camel_case(column_name),
                    'java_type': java_type,
                    'is_nullable': is_nullable,
                    'is_primary': is_primary,
                    'is_auto_increment': is_auto_increment,
                    'comment': column_comment,
                    'column_type': column_type
                }
                
                columns.append(column_info)
                
                # Collect all primary keys
                if is_primary:
                    primary_keys.append(column_info)
            
            # Print PK information
            if len(primary_keys) > 1:
                pk_names = [pk['db_name'] for pk in primary_keys]
                print(f"🔑 Composite Primary Key found: {', '.join(pk_names)}")
            elif len(primary_keys) == 1:
                print(f"🔑 Primary Key: {primary_keys[0]['db_name']}")
            else:
                print(f"⚠️  No Primary Key found for table {actual_table_name}")
                    
        finally:
            cursor.close()
            conn.close()
        
        return {
            'table_name': actual_table_name,
            'columns': columns,
            'primary_keys': primary_keys,
            'table_comment': table_comment
        }