#!/usr/bin/env python3

"""
Migration script to transfer all data from SQLite to PostgreSQL.
This script reads from the existing SQLite database and writes to PostgreSQL.
"""

import os
import sys
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import (
    Base, BlogPost, MultilingualBlogPost, WaitlistRegistration, 
    CorporateInquiry, LeadMagnetDownload, EmailSubscriber, 
    SequenceEnrollment, SequenceEmail
)

def migrate_sqlite_to_postgres():
    """Migrate all data from SQLite to PostgreSQL"""
    
    # SQLite connection (source)
    sqlite_db_path = os.path.join(os.path.dirname(__file__), "coaching_site.db")
    sqlite_url = f"sqlite:///{sqlite_db_path}"
    sqlite_engine = create_engine(sqlite_url)
    SqliteSession = sessionmaker(bind=sqlite_engine)
    
    # PostgreSQL connection (destination) - use environment variable
    postgres_url = os.getenv("DATABASE_URL", "postgresql://peterstoyanov@localhost:5432/coaching_site")
    postgres_engine = create_engine(postgres_url)
    PostgresSession = sessionmaker(bind=postgres_engine)
    
    print(f"📊 Starting migration from SQLite to PostgreSQL...")
    print(f"   Source: {sqlite_url}")
    print(f"   Destination: {postgres_url}")
    
    # Create tables in PostgreSQL
    print("🔨 Creating tables in PostgreSQL...")
    Base.metadata.create_all(bind=postgres_engine)
    
    # Create sessions
    sqlite_session = SqliteSession()
    postgres_session = PostgresSession()
    
    try:
        # Check if SQLite database exists
        if not os.path.exists(sqlite_db_path):
            print(f"❌ SQLite database not found at: {sqlite_db_path}")
            return
        
        # Get list of tables to migrate
        tables_to_migrate = [
            (BlogPost, "blog_posts"),
            (MultilingualBlogPost, "multilingual_blog_posts"),
            (WaitlistRegistration, "waitlist_registrations"),
            (CorporateInquiry, "corporate_inquiries"),
            (LeadMagnetDownload, "lead_magnet_downloads"),
            (EmailSubscriber, "email_subscribers"),
            (SequenceEnrollment, "sequence_enrollments"),
            (SequenceEmail, "sequence_emails")
        ]
        
        total_migrated = 0
        
        for model_class, table_name in tables_to_migrate:
            try:
                print(f"\n📋 Migrating {table_name}...")
                
                # Check if table exists in SQLite
                try:
                    sqlite_count = sqlite_session.query(model_class).count()
                    print(f"   Found {sqlite_count} records in SQLite")
                except Exception as e:
                    print(f"   ⚠️  Table {table_name} doesn't exist in SQLite: {e}")
                    continue
                
                if sqlite_count == 0:
                    print(f"   ✅ No data to migrate for {table_name}")
                    continue
                
                # Check current PostgreSQL count
                postgres_count = postgres_session.query(model_class).count()
                print(f"   Current PostgreSQL records: {postgres_count}")
                
                # Get all records from SQLite
                sqlite_records = sqlite_session.query(model_class).all()
                
                # Clear existing PostgreSQL data for this table
                if postgres_count > 0:
                    print(f"   🗑️  Clearing existing PostgreSQL data...")
                    postgres_session.query(model_class).delete()
                    postgres_session.commit()
                
                # Migrate each record
                migrated_count = 0
                for record in sqlite_records:
                    # Create a new instance with the same data
                    record_dict = {}
                    for column in model_class.__table__.columns:
                        value = getattr(record, column.name)
                        record_dict[column.name] = value
                    
                    new_record = model_class(**record_dict)
                    postgres_session.add(new_record)
                    migrated_count += 1
                
                postgres_session.commit()
                print(f"   ✅ Migrated {migrated_count} records to PostgreSQL")
                total_migrated += migrated_count
                
                # Verify migration
                final_count = postgres_session.query(model_class).count()
                print(f"   ✅ Verification: {final_count} records in PostgreSQL")
                
            except Exception as e:
                print(f"   ❌ Error migrating {table_name}: {e}")
                postgres_session.rollback()
                continue
        
        print(f"\n🎉 Migration completed successfully!")
        print(f"   Total records migrated: {total_migrated}")
        
        # Show summary
        print(f"\n📊 Final PostgreSQL database summary:")
        for model_class, table_name in tables_to_migrate:
            try:
                count = postgres_session.query(model_class).count()
                print(f"   {table_name}: {count} records")
            except:
                print(f"   {table_name}: Error counting records")
        
        # Show some sample blog posts
        print(f"\n📝 Sample migrated blog posts:")
        sample_posts = postgres_session.query(BlogPost).limit(3).all()
        for post in sample_posts:
            print(f"   - {post.title} (ID: {post.id})")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        postgres_session.rollback()
        raise
    finally:
        sqlite_session.close()
        postgres_session.close()

if __name__ == "__main__":
    print("🚀 Starting SQLite to PostgreSQL migration...")
    migrate_sqlite_to_postgres()
    print("✨ Migration script completed!")