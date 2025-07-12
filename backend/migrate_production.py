#!/usr/bin/env python3
"""
Production Database Migration Script
Drops old tables and recreates with new enhanced schema
"""
import os
from sqlalchemy import create_engine, text
from models import Base

def migrate_production_database():
    """Migrate production database to new schema"""
    try:
        # Get database URL
        DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://peterstoyanov@localhost:5432/coaching_site")
        engine = create_engine(DATABASE_URL)
        
        print("🗃️  Starting production database migration...")
        print("⚠️  This will drop existing tables and recreate them")
        
        with engine.connect() as conn:
            # First, drop all existing tables
            print("🗑️  Dropping existing tables...")
            
            drop_commands = [
                "DROP TABLE IF EXISTS email_logs CASCADE",
                "DROP TABLE IF EXISTS sequence_emails CASCADE", 
                "DROP TABLE IF EXISTS email_sequences CASCADE",
                "DROP TABLE IF EXISTS lead_magnet_downloads CASCADE",
                "DROP TABLE IF EXISTS corporate_inquiries CASCADE",
                "DROP TABLE IF EXISTS waitlist_registrations CASCADE",
                "DROP TABLE IF EXISTS blog_posts CASCADE",
                "DROP TABLE IF EXISTS multilingual_blog_posts CASCADE"
            ]
            
            for cmd in drop_commands:
                try:
                    conn.execute(text(cmd))
                    print(f"   ✅ {cmd}")
                except Exception as e:
                    print(f"   ⚠️  {cmd}: {str(e)[:100]}...")
            
            conn.commit()
            print("✅ All old tables dropped")
        
        # Now create all new tables
        print("📋 Creating new enhanced tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ All new tables created")
        
        # Verify tables exist
        print("🔍 Verifying new table structure...")
        with engine.connect() as conn:
            # Check waitlist_registrations has new columns
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'waitlist_registrations'
                ORDER BY column_name
            """))
            
            columns = [row[0] for row in result.fetchall()]
            print(f"   📋 waitlist_registrations columns: {len(columns)}")
            
            required_columns = ['welcome_sent', 'sequence_started', 'current_email_index', 'is_active']
            for col in required_columns:
                if col in columns:
                    print(f"   ✅ {col}")
                else:
                    print(f"   ❌ Missing: {col}")
        
        print("🎉 Production database migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    migrate_production_database()