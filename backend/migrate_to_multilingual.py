#!/usr/bin/env python3
"""
Migrate existing blog posts to multilingual structure
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from sqlalchemy import text
import json

def migrate_to_multilingual():
    """Convert existing blog posts to multilingual JSON structure"""
    print("Migrating blog posts to multilingual structure...")
    
    # Get database session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # First, get all existing posts
        result = db.execute(text("SELECT id, title, excerpt, content, tags FROM blog_posts")).fetchall()
        
        if not result:
            print("No posts to migrate.")
            return
            
        print(f"Found {len(result)} posts to migrate.")
        
        # Drop the old table and recreate with new structure
        print("Recreating table with new structure...")
        
        # Create backup of data
        posts_backup = []
        for row in result:
            # Get the other fields
            other_data = db.execute(text("""
                SELECT slug, featured_image, is_published, published_at, created_at, updated_at 
                FROM blog_posts WHERE id = :id
            """), {"id": row[0]}).fetchone()
            
            posts_backup.append({
                'id': row[0],
                'title': row[1],
                'excerpt': row[2], 
                'content': row[3],
                'tags': row[4] if row[4] else [],
                'slug': other_data[0],
                'featured_image': other_data[1],
                'is_published': other_data[2],
                'published_at': other_data[3],
                'created_at': other_data[4],
                'updated_at': other_data[5]
            })
        
        # Drop and recreate table
        db.execute(text("DROP TABLE blog_posts"))
        
        # Create new table structure
        db.execute(text("""
            CREATE TABLE blog_posts (
                id INTEGER PRIMARY KEY,
                slug VARCHAR(200) NOT NULL UNIQUE,
                title JSON NOT NULL,
                excerpt JSON NOT NULL, 
                content JSON NOT NULL,
                featured_image VARCHAR(500),
                tags JSON,
                is_published BOOLEAN DEFAULT 0,
                published_at DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        # Insert migrated data
        for post in posts_backup:
            # Convert single-language data to multilingual JSON
            title_json = json.dumps({"en": post['title'], "bg": ""})
            excerpt_json = json.dumps({"en": post['excerpt'], "bg": ""})
            content_json = json.dumps({"en": post['content'], "bg": ""})
            
            # Handle tags - convert from array to multilingual object
            if isinstance(post['tags'], list) and post['tags']:
                tags_json = json.dumps({"en": post['tags'], "bg": []})
            else:
                tags_json = json.dumps({"en": [], "bg": []})
            
            db.execute(text("""
                INSERT INTO blog_posts 
                (slug, title, excerpt, content, featured_image, tags, is_published, published_at, created_at, updated_at)
                VALUES (:slug, :title, :excerpt, :content, :featured_image, :tags, :is_published, :published_at, :created_at, :updated_at)
            """), {
                'slug': post['slug'],
                'title': title_json,
                'excerpt': excerpt_json,
                'content': content_json,
                'featured_image': post['featured_image'],
                'tags': tags_json,
                'is_published': post['is_published'],
                'published_at': post['published_at'],
                'created_at': post['created_at'],
                'updated_at': post['updated_at']
            })
        
        db.commit()
        print(f"✓ Successfully migrated {len(posts_backup)} posts to multilingual structure")
        print("✓ All existing posts now have English content, Bulgarian fields are empty and ready for translation")
        
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        db.rollback()
        
    finally:
        db.close()

if __name__ == "__main__":
    migrate_to_multilingual()