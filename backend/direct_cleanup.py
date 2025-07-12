#!/usr/bin/env python3
"""
Direct Database Cleanup Script
Uses the existing database connection to clean all records
"""
import os
import sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import (
    EmailSubscriber, EmailSequence, SequenceEmail, SequenceEnrollment,
    ScheduledEmail, EmailAnalytics, LeadMagnetDownload,
    WaitlistRegistration, CorporateInquiry
)

def get_database_url():
    """Get database URL from environment or use default local"""
    return os.getenv('DATABASE_URL', 'sqlite:///coaching_site.db')

def cleanup_database():
    """Clean all records from database"""
    try:
        database_url = get_database_url()
        print(f"🗃️  Connecting to database: {database_url.split('@')[0] if '@' in database_url else database_url}")
        
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        with SessionLocal() as db:
            # Delete in correct order to avoid foreign key conflicts
            tables_to_clean = [
                ("EmailAnalytics", EmailAnalytics),
                ("ScheduledEmail", ScheduledEmail),
                ("SequenceEnrollment", SequenceEnrollment),
                ("SequenceEmail", SequenceEmail),
                ("EmailSequence", EmailSequence),
                ("EmailSubscriber", EmailSubscriber),
                ("LeadMagnetDownload", LeadMagnetDownload),
                ("WaitlistRegistration", WaitlistRegistration),
                ("CorporateInquiry", CorporateInquiry)
            ]
            
            total_deleted = 0
            
            print("💥 Starting database cleanup...")
            print("=" * 50)
            
            for table_name, model_class in tables_to_clean:
                try:
                    count = db.query(model_class).count()
                    if count > 0:
                        deleted = db.query(model_class).delete()
                        total_deleted += deleted
                        print(f"✅ {table_name}: {deleted} records deleted")
                    else:
                        print(f"⭕ {table_name}: 0 records (already empty)")
                except Exception as e:
                    print(f"❌ {table_name}: Error - {str(e)}")
            
            # Commit all deletions
            db.commit()
            
            print("=" * 50)
            print(f"🎉 Database cleanup completed!")
            print(f"📊 Total records deleted: {total_deleted}")
            
            if total_deleted == 0:
                print("ℹ️  Database was already empty")
            
            return True
            
    except Exception as e:
        print(f"💥 Database cleanup failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = cleanup_database()
    sys.exit(0 if success else 1)