#!/usr/bin/env python3
"""
Debug script to check what's in the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from sqlalchemy import text

def debug_database():
    """Check what's actually in the database"""
    print("Debugging database content...")
    
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Get raw data from database
        result = db.execute(text("SELECT id, slug, title, excerpt, content, tags FROM blog_posts LIMIT 2")).fetchall()
        
        for row in result:
            print(f"\nPost ID: {row[0]}")
            print(f"Slug: {row[1]}")
            print(f"Title type: {type(row[2])}, Value: {row[2]}")
            print(f"Excerpt type: {type(row[3])}, Value: {row[3][:100]}...")
            print(f"Tags type: {type(row[5])}, Value: {row[5]}")
            
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        db.close()

if __name__ == "__main__":
    debug_database()