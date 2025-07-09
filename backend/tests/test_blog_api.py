#!/usr/bin/env python3
"""
Test blog API functions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db, get_blog_posts

def test_blog_functions():
    """Test that blog functions work correctly"""
    print("Testing blog functions...")
    
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Test get_blog_posts
        posts = get_blog_posts(db, limit=2)
        
        print(f"Retrieved {len(posts)} posts")
        
        for post in posts:
            print(f"\nPost: {post.slug}")
            print(f"Title type: {type(post.title)}")
            print(f"Title: {post.title}")
            print(f"Excerpt type: {type(post.excerpt)}")
            print(f"Tags type: {type(post.tags)}")
            print(f"Tags: {post.tags}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()

if __name__ == "__main__":
    test_blog_functions()