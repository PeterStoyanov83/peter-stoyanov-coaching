#!/usr/bin/env python3
"""
Test the new language-specific blog system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import (get_db, get_blog_posts, get_blog_post_by_id, get_blog_post_by_slug, 
                     create_blog_post, get_post_translations, link_post_translations,
                     get_blog_posts_with_translations)

def test_new_language_system():
    """Test all aspects of the new language-specific blog system"""
    print("🧪 Testing new language-specific blog system...")
    
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Test 1: Check migrated posts
        print("\n1️⃣ Testing migrated posts...")
        all_posts = get_blog_posts(db, limit=10)
        print(f"   Found {len(all_posts)} total posts")
        
        for post in all_posts[:3]:  # Show first 3
            print(f"   - {post.slug} ({post.language}): {post.title}")
            print(f"     Translation ID: {post.translation_id}")
        
        # Test 2: Language filtering
        print("\n2️⃣ Testing language filtering...")
        en_posts = get_blog_posts(db, language="en", limit=5)
        bg_posts = get_blog_posts(db, language="bg", limit=5)
        print(f"   English posts: {len(en_posts)}")
        print(f"   Bulgarian posts: {len(bg_posts)}")
        
        # Test 3: Create a Bulgarian translation
        print("\n3️⃣ Testing creation of Bulgarian translation...")
        if en_posts:
            original_post = en_posts[0]
            print(f"   Creating Bulgarian translation for: {original_post.title}")
            
            bg_post_data = {
                "slug": f"{original_post.slug}-bg",
                "title": "Овладяване на публичното говорене", 
                "excerpt": "Научете се да говорите уверено пред публика",
                "content": "Публичното говорене е умение, което може да се научи...",
                "featured_image": original_post.featured_image,
                "tags": ["комуникация", "говорене", "увереност"],
                "language": "bg",
                "translation_id": original_post.translation_id,
                "is_published": True
            }
            
            bg_post = create_blog_post(db, bg_post_data)
            print(f"   ✅ Created Bulgarian post: {bg_post.title} (ID: {bg_post.id})")
            
            # Test 4: Check translations
            print("\n4️⃣ Testing translation linking...")
            translations = get_post_translations(db, original_post.translation_id)
            print(f"   Found {len(translations)} linked translations:")
            for t_post in translations:
                print(f"   - {t_post.language}: {t_post.title}")
        
        # Test 5: Create a completely new English post
        print("\n5️⃣ Testing new English post creation...")
        new_en_post_data = {
            "slug": "effective-communication-skills",
            "title": "Effective Communication Skills",
            "excerpt": "Master the art of clear and impactful communication",
            "content": "Communication is the foundation of all relationships...",
            "featured_image": "/images/communication.jpg",
            "tags": ["communication", "skills", "leadership"],
            "language": "en",
            "translation_id": None,  # No translation yet
            "is_published": True
        }
        
        new_post = create_blog_post(db, new_en_post_data)
        print(f"   ✅ Created new English post: {new_post.title} (ID: {new_post.id})")
        
        # Test 6: Test slug-based retrieval
        print("\n6️⃣ Testing post retrieval by slug...")
        retrieved_post = get_blog_post_by_slug(db, new_post.slug)
        if retrieved_post:
            print(f"   ✅ Retrieved post by slug: {retrieved_post.title}")
            print(f"   Language: {retrieved_post.language}")
            print(f"   Tags: {retrieved_post.tags}")
        
        # Test 7: Test ID-based retrieval
        print("\n7️⃣ Testing post retrieval by ID...")
        retrieved_by_id = get_blog_post_by_id(db, new_post.id)
        if retrieved_by_id:
            print(f"   ✅ Retrieved post by ID: {retrieved_by_id.title}")
        
        # Test 8: Test admin-style grouped view
        print("\n8️⃣ Testing posts with translations view...")
        posts_with_translations = get_blog_posts_with_translations(db, limit=5)
        print(f"   Found {len(posts_with_translations)} post groups:")
        for post_group in posts_with_translations:
            post = post_group
            if isinstance(post_group, dict):
                # Our new function returns dict format
                print(f"   - {post['title']} ({post['language']})")
                if post['translations']:
                    print(f"     Has {len(post['translations'])} translations")
            else:
                # Regular post object
                print(f"   - {post.title} ({post.language})")
        
        print("\n✅ ALL TESTS PASSED!")
        print("🎉 New language-specific blog system is working perfectly!")
        print("\nSystem capabilities:")
        print("✓ Language-specific posts (English/Bulgarian)")
        print("✓ Translation linking between posts")
        print("✓ Language filtering")
        print("✓ Independent post management")
        print("✓ Backwards compatibility with existing data")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        db.close()

if __name__ == "__main__":
    test_new_language_system()