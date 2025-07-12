#!/usr/bin/env python3
"""
Database Migration Script
Adds new columns to existing tables for enhanced management features
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def get_database_url():
    """Get database URL from environment or use default"""
    return os.getenv('DATABASE_URL', 'postgresql://peterstoyanov@localhost:5432/coaching_site')

def migrate_database():
    """Add new columns to existing tables"""
    database_url = get_database_url()
    print(f"🗃️  Connecting to database: {database_url.split('@')[0] if '@' in database_url else database_url}")
    
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        print("🔄 Starting database migration...")
        
        try:
            # Migrate waitlist_registrations table
            print("📝 Migrating waitlist_registrations table...")
            
            waitlist_migrations = [
                "ALTER TABLE waitlist_registrations ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'new'",
                "ALTER TABLE waitlist_registrations ADD COLUMN IF NOT EXISTS notes TEXT",
                "ALTER TABLE waitlist_registrations ADD COLUMN IF NOT EXISTS priority VARCHAR(10) DEFAULT 'medium'",
                "ALTER TABLE waitlist_registrations ADD COLUMN IF NOT EXISTS last_contacted TIMESTAMP",
                "ALTER TABLE waitlist_registrations ADD COLUMN IF NOT EXISTS follow_up_date TIMESTAMP",
                "ALTER TABLE waitlist_registrations ADD COLUMN IF NOT EXISTS conversion_source VARCHAR(50)",
                "ALTER TABLE waitlist_registrations ADD COLUMN IF NOT EXISTS updated_by VARCHAR(100)",
                "ALTER TABLE waitlist_registrations ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                "ALTER TABLE waitlist_registrations ADD COLUMN IF NOT EXISTS lead_score INTEGER DEFAULT 0",
                "ALTER TABLE waitlist_registrations ADD COLUMN IF NOT EXISTS tags JSON"
            ]
            
            for migration in waitlist_migrations:
                try:
                    conn.execute(text(migration))
                    print(f"✅ {migration.split('ADD COLUMN IF NOT EXISTS')[1].split()[0] if 'ADD COLUMN' in migration else 'Migration'}")
                except Exception as e:
                    print(f"⚠️  {migration}: {str(e)}")
            
            # Migrate corporate_inquiries table
            print("🏢 Migrating corporate_inquiries table...")
            
            corporate_migrations = [
                "ALTER TABLE corporate_inquiries ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'new'",
                "ALTER TABLE corporate_inquiries ADD COLUMN IF NOT EXISTS priority VARCHAR(10) DEFAULT 'medium'",
                "ALTER TABLE corporate_inquiries ADD COLUMN IF NOT EXISTS estimated_value INTEGER",
                "ALTER TABLE corporate_inquiries ADD COLUMN IF NOT EXISTS proposal_sent_date TIMESTAMP",
                "ALTER TABLE corporate_inquiries ADD COLUMN IF NOT EXISTS follow_up_date TIMESTAMP",
                "ALTER TABLE corporate_inquiries ADD COLUMN IF NOT EXISTS expected_close_date TIMESTAMP",
                "ALTER TABLE corporate_inquiries ADD COLUMN IF NOT EXISTS notes TEXT",
                "ALTER TABLE corporate_inquiries ADD COLUMN IF NOT EXISTS assigned_to VARCHAR(100)",
                "ALTER TABLE corporate_inquiries ADD COLUMN IF NOT EXISTS last_contacted TIMESTAMP",
                "ALTER TABLE corporate_inquiries ADD COLUMN IF NOT EXISTS updated_by VARCHAR(100)",
                "ALTER TABLE corporate_inquiries ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                "ALTER TABLE corporate_inquiries ADD COLUMN IF NOT EXISTS lead_score INTEGER DEFAULT 0",
                "ALTER TABLE corporate_inquiries ADD COLUMN IF NOT EXISTS tags JSON",
                "ALTER TABLE corporate_inquiries ADD COLUMN IF NOT EXISTS probability INTEGER DEFAULT 50",
                "ALTER TABLE corporate_inquiries ADD COLUMN IF NOT EXISTS lost_reason VARCHAR(100)"
            ]
            
            for migration in corporate_migrations:
                try:
                    conn.execute(text(migration))
                    print(f"✅ {migration.split('ADD COLUMN IF NOT EXISTS')[1].split()[0] if 'ADD COLUMN' in migration else 'Migration'}")
                except Exception as e:
                    print(f"⚠️  {migration}: {str(e)}")
            
            # Create new tables
            print("📋 Creating new tables...")
            
            # Create communications table
            create_communications = """
            CREATE TABLE IF NOT EXISTS communications (
                id SERIAL PRIMARY KEY,
                contact_type VARCHAR(20) NOT NULL,
                contact_id INTEGER NOT NULL,
                communication_type VARCHAR(20) NOT NULL,
                subject VARCHAR(200),
                content TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                sent_by VARCHAR(100) NOT NULL,
                response_received BOOLEAN DEFAULT FALSE,
                response_date TIMESTAMP,
                follow_up_required BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            conn.execute(text(create_communications))
            print("✅ Created communications table")
            
            # Create tasks table
            create_tasks = """
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                description TEXT,
                task_type VARCHAR(20) NOT NULL,
                contact_type VARCHAR(20) NOT NULL,
                contact_id INTEGER NOT NULL,
                assigned_to VARCHAR(100) NOT NULL,
                due_date TIMESTAMP NOT NULL,
                status VARCHAR(20) DEFAULT 'pending',
                priority VARCHAR(10) DEFAULT 'medium',
                completed_at TIMESTAMP,
                completed_by VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            conn.execute(text(create_tasks))
            print("✅ Created tasks table")
            
            # Commit all changes
            conn.commit()
            print("💾 All migrations committed successfully!")
            
            print("""
            🎉 Database migration completed successfully!
            
            ✅ Added new columns to waitlist_registrations:
               - status, notes, priority, follow_up_date
               - lead_score, tags, updated_by, etc.
            
            ✅ Added new columns to corporate_inquiries:
               - status, priority, estimated_value, probability
               - follow_up_date, notes, assigned_to, etc.
            
            ✅ Created new tables:
               - communications (for tracking all interactions)
               - tasks (for follow-up and task management)
            
            🚀 Ready to populate test data!
            """)
            
            return True
            
        except Exception as e:
            print(f"💥 Migration failed: {str(e)}")
            conn.rollback()
            return False

if __name__ == "__main__":
    try:
        success = migrate_database()
        if success:
            print("✅ Database migration completed successfully!")
        else:
            print("❌ Database migration failed")
            sys.exit(1)
    except Exception as e:
        print(f"💥 Error during migration: {str(e)}")
        sys.exit(1)