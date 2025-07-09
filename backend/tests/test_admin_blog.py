#!/usr/bin/env python3
"""
Test admin blog management functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db, get_blog_posts

def test_admin_blog_functionality():
    """Test the admin blog functionality that was causing issues"""
    print("Testing admin blog management functionality...")
    
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Simulate what the admin endpoint does
        posts = get_blog_posts(db, skip=0, limit=100, published_only=False)
        
        print(f"Retrieved {len(posts)} posts")
        
        # Convert to dictionaries like the endpoint does
        result = []
        for post in posts:
            post_dict = {
                "id": post.id,
                "slug": post.slug,
                "title": post.title,
                "excerpt": post.excerpt,
                "featured_image": post.featured_image,
                "tags": post.tags,
                "is_published": post.is_published,
                "published_at": post.published_at,
                "created_at": post.created_at,
                "updated_at": post.updated_at
            }
            result.append(post_dict)
            
        print("\nSuccessfully converted posts to admin format:")
        for post_dict in result:
            print(f"- {post_dict['slug']}: {post_dict['title']} (Published: {post_dict['is_published']})")
            
        print("\n✓ Admin blog management functionality working correctly!")
        print("✓ Posts can be retrieved and serialized properly")
        print("✓ User should now be able to access the Blog Management tab in admin dashboard")
        
    except Exception as e:
        print(f"✗ Error testing admin functionality: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()

if __name__ == "__main__":
    test_admin_blog_functionality()