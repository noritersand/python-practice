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
        self.type_mapping = {
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
    
    def validate_table(self, cursor, table_name: str) -> str:
        """Validate if table exists and return actual table name"""
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        available_tables = [table[0] for table in tables]
        
        print(f"📋 Available tables in database: {', '.join(available_tables[:10])}")
        if len(available_tables) > 10:
            print(f"   ... and {len(available_tables) - 10} more tables")
        
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
        
        try:
            # Validate table exists and get actual name
            actual_table_name = self.validate_table(cursor, table_name)
            
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
                
                # Check if it's auto_increment
                is_auto_increment = 'auto_increment' in extra.lower() if extra else False
                
                column_info = {
                    'db_name': column_name,
                    'java_name': self.to_camel_case(column_name),
                    'java_type': self.get_java_type(data_type),
                    'is_nullable': is_nullable,
                    'is_primary': is_primary,
                    'is_auto_increment': is_auto_increment
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
            'primary_keys': primary_keys
        }
