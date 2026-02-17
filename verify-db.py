"""
Script to verify database tables exist
Run with: python verify-db.py
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarmatch_project.settings')
django.setup()

from django.db import connection

def check_tables():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        print("=" * 50)
        print("Database Tables in PostgreSQL:")
        print("=" * 50)
        
        important_tables = [
            'users',  # Custom db_table name
            'user_profiles',  # Custom db_table name
            'scholarships',  # Custom db_table name
            'scholarship_applications',  # Custom db_table name
            'bookmarked_scholarships'  # Custom db_table name
        ]
        
        all_tables = [t[0] for t in tables]
        
        for table in important_tables:
            if table in all_tables:
                print(f"[OK] {table}")
            else:
                print(f"[MISSING] {table} - NOT FOUND")
        
        print("\nAll tables:")
        for table in all_tables:
            print(f"  - {table}")
        
        print(f"\nTotal: {len(all_tables)} tables")
        print("=" * 50)

if __name__ == "__main__":
    try:
        check_tables()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

