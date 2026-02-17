"""
Quick script to test PostgreSQL database connection
Run this to verify your database setup before running Django migrations
"""
import psycopg2
import os

def test_connection():
    try:
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            database=os.environ.get('DB_NAME', 'scholarmatch_db'),
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASSWORD', 'postgres'),
            port=os.environ.get('DB_PORT', '5432')
        )
        print("✅ Database connection successful!")
        
        # Test query
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"✅ PostgreSQL version: {version[0]}")
        
        # Check if database exists
        cur.execute("SELECT datname FROM pg_database WHERE datname = 'scholarmatch_db';")
        db_exists = cur.fetchone()
        
        if db_exists:
            print("✅ Database 'scholarmatch_db' exists")
        else:
            print("⚠️  Database 'scholarmatch_db' does not exist. Please create it in pgAdmin 4.")
        
        cur.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure PostgreSQL is running")
        print("2. Verify credentials in .env file")
        print("3. Check if database 'scholarmatch_db' exists")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing PostgreSQL connection...")
    print("=" * 50)
    test_connection()
    print("=" * 50)

