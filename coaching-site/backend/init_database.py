#!/usr/bin/env python3
"""
Database Initialization Script
Creates all tables for the clean system
"""
import os
from sqlalchemy import create_engine, text
from models import Base
from database import engine

def create_all_tables():
    """Create all database tables"""
    try:
        print("🗃️  Initializing database...")
        print("📋 Creating all tables...")
        
        # Create all tables defined in models
        Base.metadata.create_all(bind=engine)
        
        print("✅ All tables created successfully!")
        
        # Test database connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection test passed!")
        
        print("\n📊 Available tables:")
        with engine.connect() as conn:
            if engine.url.drivername.startswith('postgresql'):
                tables_query = text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name
                """)
            else:
                tables_query = text("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' 
                    ORDER BY name
                """)
            
            tables = conn.execute(tables_query).fetchall()
            for table in tables:
                print(f"   ✅ {table[0]}")
        
        print("\n🎉 Database initialization completed successfully!")
        print("🔗 You can now use the admin dashboard at /admin/dashboard")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        print("💡 Make sure DATABASE_URL is set correctly")
        raise

def test_database_operations():
    """Test basic database operations"""
    try:
        from database import SessionLocal
        from models import WaitlistRegistration
        
        print("\n🧪 Testing database operations...")
        
        db = SessionLocal()
        
        # Test query
        count = db.query(WaitlistRegistration).count()
        print(f"✅ Current waitlist subscribers: {count}")
        
        db.close()
        print("✅ Database operations test passed!")
        
    except Exception as e:
        print(f"❌ Database operations test failed: {e}")
        raise

if __name__ == "__main__":
    print("🚀 Starting database initialization...")
    print("=" * 50)
    
    create_all_tables()
    test_database_operations()
    
    print("\n" + "=" * 50)
    print("🎯 Database is ready for production!")
    print("🔗 Admin dashboard: https://your-app.onrender.com/admin/dashboard")
    print("🔑 Login: peterstoyanov83@gmail.com / admin123")