#!/usr/bin/env python3
"""
Production Database Cleanup Script
Clears all email automation and lead magnet records from PRODUCTION database
"""

import os
import requests
from database import get_db
from models import (
    EmailSubscriber, EmailSequence, SequenceEmail, SequenceEnrollment,
    ScheduledEmail, EmailAnalytics, LeadMagnetDownload, 
    WaitlistRegistration, CorporateInquiry
)

def get_admin_token():
    """Get admin access token for API calls"""
    login_url = "https://peter-stoyanov-backend.onrender.com/auth/login"
    
    response = requests.post(
        login_url,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data="username=peterstoyanov&password=admin123"
    )
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data["access_token"]
    else:
        print(f"❌ Failed to get admin token: {response.status_code}")
        return None

def cleanup_via_api():
    """Clean database via API calls (if cleanup endpoint exists)"""
    token = get_admin_token()
    if not token:
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Check current stats
    stats_url = "https://peter-stoyanov-backend.onrender.com/admin/stats"
    response = requests.get(stats_url, headers=headers)
    
    if response.status_code == 200:
        stats = response.json()
        print("📊 Current database stats:")
        print(f"  - Lead Magnet Downloads: {stats['lead_magnet']['total']}")
        print(f"  - Waitlist Registrations: {stats['waitlist']['total']}")
        print(f"  - Corporate Inquiries: {stats['corporate']['total']}")
        
        if stats['lead_magnet']['total'] == 0 and stats['waitlist']['total'] == 0 and stats['corporate']['total'] == 0:
            print("✅ Database is already clean!")
            return True
        
        print("\n⚠️  Need to clean database manually...")
        return False
    else:
        print(f"❌ Failed to get stats: {response.status_code}")
        return False

def cleanup_production_database():
    """Clean production database directly"""
    # Check if we're connecting to production database
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ No DATABASE_URL found - cannot clean production database")
        return False
    
    print(f"🗄️  Database URL: {db_url[:50]}...")
    
    db = next(get_db())
    
    try:
        print("🧹 Starting PRODUCTION database cleanup...")
        
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
        print(f"\n🎉 PRODUCTION database cleanup completed! Total records deleted: {total_deleted}")
        print("📊 Production database is now clean and ready for fresh testing")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during production cleanup: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def verify_cleanup():
    """Verify the cleanup worked by checking admin stats"""
    token = get_admin_token()
    if not token:
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    stats_url = "https://peter-stoyanov-backend.onrender.com/admin/stats"
    
    response = requests.get(stats_url, headers=headers)
    if response.status_code == 200:
        stats = response.json()
        print("\n📊 Post-cleanup verification:")
        print(f"  - Lead Magnet Downloads: {stats['lead_magnet']['total']}")
        print(f"  - Waitlist Registrations: {stats['waitlist']['total']}")
        print(f"  - Corporate Inquiries: {stats['corporate']['total']}")
        
        if stats['lead_magnet']['total'] == 0 and stats['waitlist']['total'] == 0 and stats['corporate']['total'] == 0:
            print("✅ Production database is confirmed clean!")
            return True
        else:
            print("⚠️  Some records may still exist")
            return False
    else:
        print(f"❌ Failed to verify cleanup: {response.status_code}")
        return False

if __name__ == "__main__":
    print("🗃️  PRODUCTION Database Cleanup Tool")
    print("=" * 60)
    print("⚠️  WARNING: This will clean the PRODUCTION database!")
    print("⚠️  This affects the live website at www.peter-stoyanov.com")
    print("=" * 60)
    
    # First try API approach
    print("🔍 Checking current database state...")
    if cleanup_via_api():
        exit(0)
    
    # If API doesn't work, do direct database cleanup
    print("\n💥 Proceeding with direct database cleanup...")
    print("⚠️  This will delete ALL production data! Press Ctrl+C to cancel...")
    
    import time
    for i in range(3, 0, -1):
        print(f"Starting in {i}...")
        time.sleep(1)
    
    if cleanup_production_database():
        verify_cleanup()
    else:
        print("❌ Production cleanup failed")