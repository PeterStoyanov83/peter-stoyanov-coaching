#!/usr/bin/env python3
"""
Export data from current Render database before migration
"""
import json
import os
from datetime import datetime
from database import get_db
from models import WaitlistRegistration, CorporateInquiry, LeadMagnetDownload, EmailLog

def export_table_data(db, model_class, table_name):
    """Export data from a table to JSON"""
    print(f"Exporting {table_name}...")
    records = db.query(model_class).all()
    
    data = []
    for record in records:
        record_dict = {}
        for column in model_class.__table__.columns:
            value = getattr(record, column.name)
            # Convert datetime to string for JSON serialization
            if isinstance(value, datetime):
                value = value.isoformat()
            record_dict[column.name] = value
        data.append(record_dict)
    
    print(f"  Found {len(data)} records")
    return data

def main():
    print("🔄 Starting data export from Render database...")
    
    # Get database session
    db = next(get_db())
    
    try:
        # Export all tables
        export_data = {
            'export_timestamp': datetime.utcnow().isoformat(),
            'database_url': os.getenv('DATABASE_URL', 'Not found'),
            'tables': {}
        }
        
        # Export each table
        tables_to_export = [
            (WaitlistRegistration, 'waitlist_registrations'),
            (CorporateInquiry, 'corporate_inquiries'), 
            (LeadMagnetDownload, 'lead_magnet_downloads'),
            (EmailLog, 'email_logs')
        ]
        
        for model_class, table_name in tables_to_export:
            export_data['tables'][table_name] = export_table_data(db, model_class, table_name)
        
        # Save to JSON file
        filename = f"database_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"\n✅ Export completed successfully!")
        print(f"📄 Data saved to: {filename}")
        
        # Print summary
        print(f"\n📊 Export Summary:")
        for table_name, data in export_data['tables'].items():
            print(f"  {table_name}: {len(data)} records")
            
    except Exception as e:
        print(f"❌ Export failed: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()