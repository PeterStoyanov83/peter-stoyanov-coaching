#!/usr/bin/env python3
"""
Database Cleanup Script
Clears all email automation and lead magnet records for fresh testing
"""

from database import get_db
from models import (
    EmailSubscriber, EmailSequence, SequenceEmail, SequenceEnrollment,
    ScheduledEmail, EmailAnalytics, LeadMagnetDownload, 
    WaitlistRegistration, CorporateInquiry
)

def cleanup_all_records():
    """Clean up all email automation and form submission records"""
    db = next(get_db())
    
    try:
        print("🧹 Starting database cleanup...")
        
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
        
        for table_name, model_class in tables_to_clean:
            count = db.query(model_class).count()
            if count > 0:
                deleted = db.query(model_class).delete()
                print(f"  ✅ Deleted {deleted} records from {table_name}")
                total_deleted += deleted
            else:
                print(f"  ⭕ No records found in {table_name}")
        
        # Commit all deletions
        db.commit()
        print(f"\n🎉 Database cleanup completed! Total records deleted: {total_deleted}")
        print("📊 Database is now clean and ready for fresh testing")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def cleanup_email_automation_only():
    """Clean up only email automation records, keep form submissions"""
    db = next(get_db())
    
    try:
        print("🧹 Starting email automation cleanup...")
        
        # Delete only email automation tables
        tables_to_clean = [
            ("EmailAnalytics", EmailAnalytics),
            ("ScheduledEmail", ScheduledEmail),
            ("SequenceEnrollment", SequenceEnrollment),
            ("SequenceEmail", SequenceEmail),
            ("EmailSequence", EmailSequence),
            ("EmailSubscriber", EmailSubscriber)
        ]
        
        total_deleted = 0
        
        for table_name, model_class in tables_to_clean:
            count = db.query(model_class).count()
            if count > 0:
                deleted = db.query(model_class).delete()
                print(f"  ✅ Deleted {deleted} records from {table_name}")
                total_deleted += deleted
            else:
                print(f"  ⭕ No records found in {table_name}")
        
        # Commit all deletions
        db.commit()
        print(f"\n🎉 Email automation cleanup completed! Total records deleted: {total_deleted}")
        print("📊 Email automation tables are now clean")
        print("📝 Form submissions (LeadMagnetDownload, WaitlistRegistration, CorporateInquiry) preserved")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    
    print("🗃️  Database Cleanup Tool")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--email-only":
        print("🎯 Cleaning up email automation records only...")
        cleanup_email_automation_only()
    else:
        print("💥 Cleaning up ALL records (email automation + form submissions)...")
        print("⚠️  This will delete all data! Press Ctrl+C to cancel...")
        
        import time
        for i in range(3, 0, -1):
            print(f"Starting in {i}...")
            time.sleep(1)
        
        cleanup_all_records()