#!/usr/bin/env python3
"""
Add language column to existing blog posts
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from sqlalchemy import text

def add_language_column():
    """Add language column to existing blog posts table"""
    print("Adding language column to blog_posts table...")
    
    # Get database session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Add language column with default value 'en'
        db.execute(text("ALTER TABLE blog_posts ADD COLUMN language VARCHAR(5) DEFAULT 'en'"))
        
        # Update existing posts to have language 'en'
        db.execute(text("UPDATE blog_posts SET language = 'en' WHERE language IS NULL"))
        
        # Make the language column NOT NULL
        db.execute(text("UPDATE blog_posts SET language = 'en' WHERE language IS NULL"))
        
        db.commit()
        print("✓ Language column added successfully")
        print("✓ All existing posts set to English (en)")
        
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        db.rollback()
        
    finally:
        db.close()

if __name__ == "__main__":
    add_language_column()