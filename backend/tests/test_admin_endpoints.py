#!/usr/bin/env python3
"""
Test admin endpoints with new language system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db, get_blog_posts

def test_admin_endpoint_compatibility():
    """Test that admin endpoints work with new language-specific structure"""
    print("🔧 Testing admin endpoint compatibility...")
    
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Test the function that admin endpoints use
        print("\n1️⃣ Testing get_blog_posts (used by /admin/blog/posts)...")
        posts = get_blog_posts(db, skip=0, limit=100, published_only=False)
        
        print(f"   Found {len(posts)} posts")
        
        # Test converting posts to admin format (like the endpoint does)
        result = []
        for post in posts:
            post_dict = {
                "id": post.id,
                "slug": post.slug,
                "title": post.title,  # Now single string instead of dict
                "excerpt": post.excerpt,  # Now single string instead of dict
                "featured_image": post.featured_image,
                "tags": post.tags,  # Now list instead of dict
                "language": post.language,  # New field
                "translation_id": post.translation_id,  # New field
                "is_published": post.is_published,
                "published_at": post.published_at,
                "created_at": post.created_at,
                "updated_at": post.updated_at
            }
            result.append(post_dict)
        
        print("   ✅ Successfully converted all posts to admin format")
        print("   Sample post:")
        if result:
            sample = result[0]
            print(f"     Title: {sample['title']}")
            print(f"     Language: {sample['language']}")
            print(f"     Tags: {sample['tags']}")
            print(f"     Translation ID: {sample['translation_id']}")
        
        # Check what the admin interface expects vs what we have
        print("\n2️⃣ Checking admin interface compatibility...")
        print("   ❌ Current admin interface expects:")
        print("     - title: {'en': '...', 'bg': '...'}")
        print("     - excerpt: {'en': '...', 'bg': '...'}")
        print("     - tags: {'en': [...], 'bg': [...]}")
        print("\n   ✅ New system provides:")
        print("     - title: 'Single language title'")
        print("     - excerpt: 'Single language excerpt'") 
        print("     - tags: ['tag1', 'tag2']")
        print("     - language: 'en' or 'bg'")
        print("     - translation_id: 'unique-id'")
        
        print("\n🔧 ADMIN INTERFACE NEEDS UPDATING")
        print("   The admin interface must be updated to handle:")
        print("   1. Single language fields instead of multilingual objects")
        print("   2. Language selection dropdown")
        print("   3. Translation linking functionality")
        print("   4. Language filtering in post list")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()

if __name__ == "__main__":
    test_admin_endpoint_compatibility()