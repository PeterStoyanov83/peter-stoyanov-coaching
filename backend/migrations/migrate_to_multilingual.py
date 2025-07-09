#!/usr/bin/env python3

"""
Migration script to convert existing separate language blog posts 
to the new multilingual blog post structure.
"""

import os
import sys
from datetime import datetime
from database import SessionLocal, engine
from models import Base, BlogPost, MultilingualBlogPost
import json

def migrate_to_multilingual():
    """Migrate existing blog posts to multilingual structure"""
    
    # Create new table
    Base.metadata.create_all(bind=engine)
    
    # Create database session
    db = SessionLocal()
    
    try:
        print("Starting migration to multilingual blog posts...")
        
        # Get all English posts with translation_id
        english_posts = db.query(BlogPost).filter(
            BlogPost.language == "en",
            BlogPost.translation_id.isnot(None)
        ).all()
        
        print(f"Found {len(english_posts)} English posts with translation_id")
        
        migrated_count = 0
        
        for en_post in english_posts:
            # Find the corresponding Bulgarian post
            bg_post = db.query(BlogPost).filter(
                BlogPost.language == "bg",
                BlogPost.translation_id == en_post.translation_id
            ).first()
            
            if not bg_post:
                print(f"Warning: No Bulgarian translation found for '{en_post.title}' (translation_id: {en_post.translation_id})")
                continue
            
            # Check if this multilingual post already exists
            existing = db.query(MultilingualBlogPost).filter(
                MultilingualBlogPost.slug_en == en_post.slug
            ).first()
            
            if existing:
                print(f"Skipping '{en_post.title}' - already migrated")
                continue
            
            # Parse tags if they're JSON strings
            en_tags = en_post.tags if isinstance(en_post.tags, list) else []
            bg_tags = bg_post.tags if isinstance(bg_post.tags, list) else []
            
            if isinstance(en_post.tags, str):
                try:
                    en_tags = json.loads(en_post.tags)
                except:
                    en_tags = []
            
            if isinstance(bg_post.tags, str):
                try:
                    bg_tags = json.loads(bg_post.tags)
                except:
                    bg_tags = []
            
            # Create new multilingual blog post
            multilingual_post = MultilingualBlogPost(
                slug_en=en_post.slug,
                slug_bg=bg_post.slug,
                title_en=en_post.title,
                title_bg=bg_post.title,
                excerpt_en=en_post.excerpt,
                excerpt_bg=bg_post.excerpt,
                content_en=en_post.content,
                content_bg=bg_post.content,
                tags_en=en_tags,
                tags_bg=bg_tags,
                featured_image=en_post.featured_image or bg_post.featured_image,  # Use whichever has an image
                is_published_en=en_post.is_published,
                is_published_bg=bg_post.is_published,
                published_at_en=en_post.published_at,
                published_at_bg=bg_post.published_at,
                created_at=min(en_post.created_at, bg_post.created_at),  # Use earliest creation date
                updated_at=max(en_post.updated_at, bg_post.updated_at)   # Use latest update date
            )
            
            db.add(multilingual_post)
            print(f"Migrated: '{en_post.title}' / '{bg_post.title}'")
            migrated_count += 1
        
        # Handle posts without translation_id (standalone posts)
        standalone_posts = db.query(BlogPost).filter(
            BlogPost.translation_id.is_(None)
        ).all()
        
        print(f"Found {len(standalone_posts)} standalone posts without translation_id")
        
        for post in standalone_posts:
            # Check if this post already exists in multilingual table
            if post.language == "en":
                existing = db.query(MultilingualBlogPost).filter(
                    MultilingualBlogPost.slug_en == post.slug
                ).first()
            else:
                existing = db.query(MultilingualBlogPost).filter(
                    MultilingualBlogPost.slug_bg == post.slug
                ).first()
            
            if existing:
                print(f"Skipping standalone '{post.title}' - already exists in multilingual table")
                continue
            
            # Parse tags
            tags = post.tags if isinstance(post.tags, list) else []
            if isinstance(post.tags, str):
                try:
                    tags = json.loads(post.tags)
                except:
                    tags = []
            
            # Create multilingual post with empty fields for missing language
            if post.language == "en":
                multilingual_post = MultilingualBlogPost(
                    slug_en=post.slug,
                    slug_bg=f"{post.slug}-bg",  # Generate BG slug
                    title_en=post.title,
                    title_bg="",  # Empty until translated
                    excerpt_en=post.excerpt,
                    excerpt_bg="",  # Empty until translated
                    content_en=post.content,
                    content_bg="",  # Empty until translated
                    tags_en=tags,
                    tags_bg=[],
                    featured_image=post.featured_image,
                    is_published_en=post.is_published,
                    is_published_bg=False,  # Not published until translated
                    published_at_en=post.published_at,
                    published_at_bg=None,
                    created_at=post.created_at,
                    updated_at=post.updated_at
                )
            else:  # Bulgarian
                multilingual_post = MultilingualBlogPost(
                    slug_en=f"{post.slug}-en",  # Generate EN slug
                    slug_bg=post.slug,
                    title_en="",  # Empty until translated
                    title_bg=post.title,
                    excerpt_en="",  # Empty until translated
                    excerpt_bg=post.excerpt,
                    content_en="",  # Empty until translated
                    content_bg=post.content,
                    tags_en=[],
                    tags_bg=tags,
                    featured_image=post.featured_image,
                    is_published_en=False,  # Not published until translated
                    is_published_bg=post.is_published,
                    published_at_en=None,
                    published_at_bg=post.published_at,
                    created_at=post.created_at,
                    updated_at=post.updated_at
                )
            
            db.add(multilingual_post)
            print(f"Migrated standalone: '{post.title}' ({post.language})")
            migrated_count += 1
        
        db.commit()
        print(f"Successfully migrated {migrated_count} posts to multilingual structure.")
        
        # Verify the migration
        total_multilingual = db.query(MultilingualBlogPost).count()
        print(f"Total multilingual posts in database: {total_multilingual}")
        
        # Show some examples
        print("\nSample migrated posts:")
        sample_posts = db.query(MultilingualBlogPost).limit(3).all()
        for post in sample_posts:
            print(f"  - EN: '{post.title_en}' ({post.slug_en})")
            print(f"    BG: '{post.title_bg}' ({post.slug_bg})")
            print(f"    Image: {post.featured_image}")
            print(f"    Published: EN={post.is_published_en}, BG={post.is_published_bg}")
            print()
        
    except Exception as e:
        db.rollback()
        print(f"Error during migration: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting multilingual blog post migration...")
    migrate_to_multilingual()
    print("Migration completed successfully!")