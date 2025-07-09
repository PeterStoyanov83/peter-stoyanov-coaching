#!/usr/bin/env python3
"""
Migrate from JSON multilingual posts to separate language-specific posts
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db
from sqlalchemy import text
import json
import uuid

def migrate_to_separate_languages():
    """Convert existing multilingual JSON posts to separate language-specific posts"""
    print("Migrating to separate language-specific posts...")
    
    # Get database session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # First, get all existing posts with their multilingual data
        result = db.execute(text("SELECT id, slug, title, excerpt, content, tags, featured_image, is_published, published_at, created_at, updated_at FROM blog_posts")).fetchall()
        
        if not result:
            print("No posts to migrate.")
            return
            
        print(f"Found {len(result)} posts to migrate.")
        
        # Backup existing data
        posts_backup = []
        for row in result:
            posts_backup.append({
                'id': row[0],
                'slug': row[1],
                'title': row[2],
                'excerpt': row[3],
                'content': row[4],
                'tags': row[5],
                'featured_image': row[6],
                'is_published': row[7],
                'published_at': row[8],
                'created_at': row[9],
                'updated_at': row[10]
            })
        
        # Drop and recreate table with new structure
        print("Recreating table with new structure...")
        db.execute(text("DROP TABLE blog_posts"))
        
        # Create new table structure
        db.execute(text("""
            CREATE TABLE blog_posts (
                id INTEGER PRIMARY KEY,
                slug VARCHAR(200) NOT NULL UNIQUE,
                title VARCHAR(200) NOT NULL,
                excerpt TEXT NOT NULL,
                content TEXT NOT NULL,
                featured_image VARCHAR(500),
                tags JSON,
                language VARCHAR(5) NOT NULL,
                translation_id VARCHAR(100),
                is_published BOOLEAN DEFAULT 0,
                published_at DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        # Create indexes
        db.execute(text("CREATE INDEX idx_blog_posts_slug ON blog_posts(slug)"))
        db.execute(text("CREATE INDEX idx_blog_posts_language ON blog_posts(language)"))
        db.execute(text("CREATE INDEX idx_blog_posts_translation_id ON blog_posts(translation_id)"))
        
        # Process each old post and create separate language versions
        new_id_counter = 1
        
        for old_post in posts_backup:
            # Generate a unique translation_id for linking posts
            translation_id = f"post-{old_post['slug']}-{uuid.uuid4().hex[:8]}"
            
            # Parse JSON fields (handle both string and dict cases)
            try:
                if isinstance(old_post['title'], str):
                    title_data = json.loads(old_post['title'])
                else:
                    title_data = old_post['title']
            except (json.JSONDecodeError, TypeError):
                title_data = {"en": old_post['title'] or "", "bg": ""}
                
            try:
                if isinstance(old_post['excerpt'], str):
                    excerpt_data = json.loads(old_post['excerpt'])
                else:
                    excerpt_data = old_post['excerpt']
            except (json.JSONDecodeError, TypeError):
                excerpt_data = {"en": old_post['excerpt'] or "", "bg": ""}
                
            try:
                if isinstance(old_post['content'], str):
                    content_data = json.loads(old_post['content'])
                else:
                    content_data = old_post['content']
            except (json.JSONDecodeError, TypeError):
                content_data = {"en": old_post['content'] or "", "bg": ""}
                
            try:
                if isinstance(old_post['tags'], str):
                    tags_data = json.loads(old_post['tags'])
                else:
                    tags_data = old_post['tags']
            except (json.JSONDecodeError, TypeError):
                tags_data = {"en": [], "bg": []}
            
            # Create English version if it exists
            if title_data.get('en') and content_data.get('en'):
                en_slug = old_post['slug']  # Keep original slug for English
                en_tags = json.dumps(tags_data.get('en', []))
                
                db.execute(text("""
                    INSERT INTO blog_posts 
                    (slug, title, excerpt, content, featured_image, tags, language, translation_id, is_published, published_at, created_at, updated_at)
                    VALUES (:slug, :title, :excerpt, :content, :featured_image, :tags, :language, :translation_id, :is_published, :published_at, :created_at, :updated_at)
                """), {
                    'slug': en_slug,
                    'title': title_data['en'],
                    'excerpt': excerpt_data.get('en', ''),
                    'content': content_data['en'],
                    'featured_image': old_post['featured_image'],
                    'tags': en_tags,
                    'language': 'en',
                    'translation_id': translation_id,
                    'is_published': old_post['is_published'],
                    'published_at': old_post['published_at'],
                    'created_at': old_post['created_at'],
                    'updated_at': old_post['updated_at']
                })
                print(f"  ✓ Created English version: {en_slug}")
                new_id_counter += 1
            
            # Create Bulgarian version if it exists
            if title_data.get('bg') and content_data.get('bg'):
                # Generate Bulgarian slug based on title or use a transliterated version
                bg_title = title_data['bg']
                bg_slug = f"{old_post['slug']}-bg"  # Simple approach: add -bg suffix
                bg_tags = json.dumps(tags_data.get('bg', []))
                
                try:
                    db.execute(text("""
                        INSERT INTO blog_posts 
                        (slug, title, excerpt, content, featured_image, tags, language, translation_id, is_published, published_at, created_at, updated_at)
                        VALUES (:slug, :title, :excerpt, :content, :featured_image, :tags, :language, :translation_id, :is_published, :published_at, :created_at, :updated_at)
                    """), {
                        'slug': bg_slug,
                        'title': bg_title,
                        'excerpt': excerpt_data.get('bg', ''),
                        'content': content_data['bg'],
                        'featured_image': old_post['featured_image'],
                        'tags': bg_tags,
                        'language': 'bg',
                        'translation_id': translation_id,
                        'is_published': old_post['is_published'],
                        'published_at': old_post['published_at'],
                        'created_at': old_post['created_at'],
                        'updated_at': old_post['updated_at']
                    })
                    print(f"  ✓ Created Bulgarian version: {bg_slug}")
                    new_id_counter += 1
                except Exception as e:
                    print(f"  ⚠ Could not create Bulgarian version for {old_post['slug']}: {e}")
        
        db.commit()
        
        # Show summary
        final_count = db.execute(text("SELECT COUNT(*) FROM blog_posts")).fetchone()[0]
        en_count = db.execute(text("SELECT COUNT(*) FROM blog_posts WHERE language = 'en'")).fetchone()[0]
        bg_count = db.execute(text("SELECT COUNT(*) FROM blog_posts WHERE language = 'bg'")).fetchone()[0]
        
        print(f"\n✓ Migration completed successfully!")
        print(f"✓ Original posts: {len(posts_backup)}")
        print(f"✓ New language-specific posts: {final_count}")
        print(f"  - English posts: {en_count}")
        print(f"  - Bulgarian posts: {bg_count}")
        print(f"✓ Posts are now independent and can be managed separately")
        print(f"✓ Translation linking is maintained via translation_id field")
        
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()

if __name__ == "__main__":
    migrate_to_separate_languages()