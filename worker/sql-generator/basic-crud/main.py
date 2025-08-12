#!/usr/bin/env python3
"""
Main entry point for MyBatis Mapper Generator
"""
import sys
from mapper_generator import MapperGenerator


def print_banner():
    """Print application banner"""
    print("=" * 50)
    print("MyBatis Mapper Generator")
    print("=" * 50)


def print_usage():
    """Print usage information"""
    print("❌ Usage: python main.py <table_name>")
    print("Example: python main.py app_push")
    print("\nThis tool generates:")
    print("  - MyBatis Mapper XML file")
    print("  - Java Mapper Interface file")
    print("  - Java Entity Class file")
    print("\nGenerated files will be saved in 'result/<table_name>/' directory")


def main():
    """Main function"""
    # Check command line arguments
    if len(sys.argv) != 2:
        print_usage()
        sys.exit(1)
    
    table_name = sys.argv[1].strip()
    
    if not table_name:
        print("❌ Table name cannot be empty")
        print_usage()
        sys.exit(1)
    
    print_banner()
    print(f"Table: {table_name}")
    print("=" * 50)
    
    try:
        # Generate mapper files
        generator = MapperGenerator(table_name)
        xml_path, java_path, entity_path = generator.generate()
        
        print("\n" + "=" * 50)
        print("✨ Generation completed successfully!")
        print("=" * 50)
        
    except ValueError as e:
        print(f"\n❌ Validation Error: {e}")
        print("\n💡 Tips:")
        print("  - Check if the table name is correct")
        print("  - Ensure you have proper database connection")
        print("  - Verify your db.py configuration")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        print("\n💡 Please check:")
        print("  - Database connection settings in db.py")
        print("  - Network connectivity to database server")
        print("  - Database user permissions")
        sys.exit(1)


if __name__ == "__main__":
    main()