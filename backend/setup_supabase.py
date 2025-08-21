#!/usr/bin/env python3
"""
Set up Supabase database schema and migrate data
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Base, WaitlistRegistration, CorporateInquiry, LeadMagnetDownload, EmailLog

# Supabase connection string
SUPABASE_URL = "postgresql://postgres:Peterko123!@db.alltdwjhpdtcrsweotgh.supabase.co:5432/postgres"

def setup_supabase_schema():
    """Create all tables in Supabase database"""
    print("🔗 Connecting to Supabase database...")
    
    try:
        # Create engine and connect
        engine = create_engine(SUPABASE_URL)
        
        print("📋 Creating database schema...")
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Connected successfully!")
            print(f"   Database version: {version}")
        
        # Create session for testing
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Test table creation
        print("🧪 Testing table access...")
        waitlist_count = db.query(WaitlistRegistration).count()
        corporate_count = db.query(CorporateInquiry).count() 
        lead_magnet_count = db.query(LeadMagnetDownload).count()
        email_log_count = db.query(EmailLog).count()
        
        print(f"📊 Current data counts:")
        print(f"   Waitlist registrations: {waitlist_count}")
        print(f"   Corporate inquiries: {corporate_count}")
        print(f"   Lead magnet downloads: {lead_magnet_count}")
        print(f"   Email logs: {email_log_count}")
        
        db.close()
        
        print("\n🎉 Supabase database setup completed successfully!")
        print(f"🔗 Database URL: {SUPABASE_URL.split('@')[1]}")  # Hide password in output
        
        return True
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False

if __name__ == "__main__":
    setup_supabase_schema()