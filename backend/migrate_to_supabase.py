#!/usr/bin/env python3
"""
Migrate data from exported JSON to Supabase database
"""
import json
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, WaitlistRegistration, CorporateInquiry, LeadMagnetDownload, EmailLog

def create_supabase_connection(supabase_url):
    """Create connection to Supabase database"""
    print(f"🔗 Connecting to Supabase database...")
    engine = create_engine(supabase_url)
    
    # Create all tables
    print("📋 Creating database schema...")
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def import_table_data(db, model_class, table_data, table_name):
    """Import data from JSON to Supabase table"""
    print(f"📥 Importing {len(table_data)} records to {table_name}...")
    
    imported = 0
    skipped = 0
    
    for record_data in table_data:
        try:
            # Convert datetime strings back to datetime objects
            for key, value in record_data.items():
                if value and isinstance(value, str) and 'T' in value and value.endswith('Z'):
                    try:
                        record_data[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    except:
                        pass
            
            # Create new record
            record = model_class(**record_data)
            db.add(record)
            imported += 1
            
        except Exception as e:
            print(f"  ⚠️  Skipped record {record_data.get('id', 'unknown')}: {e}")
            skipped += 1
            continue
    
    try:
        db.commit()
        print(f"  ✅ Imported {imported} records")
        if skipped > 0:
            print(f"  ⚠️  Skipped {skipped} records due to errors")
    except Exception as e:
        db.rollback()
        print(f"  ❌ Failed to commit {table_name}: {e}")
        raise

def main():
    print("🚀 Starting migration to Supabase...")
    
    # Get Supabase connection string
    supabase_url = input("\n🔗 Enter your Supabase connection string: ").strip()
    if not supabase_url:
        print("❌ No connection string provided")
        return
    
    # Get export file
    export_file = input("📄 Enter path to export JSON file: ").strip()
    if not os.path.exists(export_file):
        print(f"❌ File not found: {export_file}")
        return
    
    try:
        # Load export data
        print(f"📖 Loading export data from {export_file}...")
        with open(export_file, 'r') as f:
            export_data = json.load(f)
        
        print(f"📅 Export created: {export_data['export_timestamp']}")
        
        # Connect to Supabase
        db = create_supabase_connection(supabase_url)
        
        # Import each table
        table_imports = [
            (WaitlistRegistration, 'waitlist_registrations'),
            (CorporateInquiry, 'corporate_inquiries'),
            (LeadMagnetDownload, 'lead_magnet_downloads'), 
            (EmailLog, 'email_logs')
        ]
        
        for model_class, table_name in table_imports:
            if table_name in export_data['tables']:
                import_table_data(db, model_class, export_data['tables'][table_name], table_name)
            else:
                print(f"⚠️  No data found for {table_name}")
        
        print(f"\n🎉 Migration completed successfully!")
        print(f"🔗 Your Supabase database is ready at: {supabase_url}")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise
    finally:
        try:
            db.close()
        except:
            pass

if __name__ == "__main__":
    main()