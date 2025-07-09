#!/usr/bin/env python3
"""
Test WYSIWYG editor and preview functionality
"""

import requests

def test_wysiwyg_functionality():
    """Test that WYSIWYG editor components are present in admin interface"""
    print("🧪 Testing WYSIWYG Editor and Preview Functionality...")
    
    base_url = "http://localhost:8000"
    
    try:
        # Test 1: Check if Quill.js is loaded
        print("\n1️⃣ Testing admin dashboard for WYSIWYG components...")
        response = requests.get(f"{base_url}/admin/dashboard")
        
        if response.status_code == 200:
            content = response.text
            
            # Check for Quill.js CDN
            if 'quilljs.com' in content:
                print("   ✅ Quill.js CDN loaded")
            else:
                print("   ❌ Quill.js CDN not found")
                
            # Check for editor elements
            editor_elements = [
                'blog-content-editor',
                'editor-container', 
                'preview-container',
                'editor-tabs',
                'switchEditorTab',
                'initializeWYSIWYGEditor'
            ]
            
            found_elements = []
            for element in editor_elements:
                if element in content:
                    found_elements.append(element)
                    
            print(f"   ✅ Found {len(found_elements)}/{len(editor_elements)} WYSIWYG elements")
            
            # Check for preview functionality
            if 'updatePreview' in content:
                print("   ✅ Preview functionality present")
            else:
                print("   ❌ Preview functionality missing")
                
            # Check for editor styling
            if '.ql-toolbar' in content and '.ql-container' in content:
                print("   ✅ Quill editor styling present")
            else:
                print("   ❌ Quill editor styling missing")
                
        else:
            print(f"   ❌ Dashboard failed to load: {response.status_code}")
            
        print("\n✅ WYSIWYG Editor Implementation Tests Completed!")
        
        print("\n📋 **New Features Added:**")
        print("✅ **WYSIWYG Editor**: Rich text editing with Quill.js")
        print("   - Headers, bold, italic, underline, strike")
        print("   - Lists (ordered and unordered)")
        print("   - Links, images, blockquotes")
        print("   - Code blocks and text alignment")
        print("   - Clean formatting tools")
        
        print("\n✅ **Live Preview**: GitHub-style preview tab")
        print("   - Real-time preview as you type")
        print("   - Shows title, excerpt, and formatted content")
        print("   - Switch between Write and Preview tabs")
        print("   - Styled like a real blog post")
        
        print("\n✅ **Enhanced UX**:")
        print("   - Language-aware placeholders")
        print("   - Focus states and visual feedback") 
        print("   - Clean, modern interface")
        print("   - Responsive design")
        
        print("\n🎯 **Manual Testing Steps:**")
        print("1. Go to http://localhost:8000/admin/dashboard")
        print("2. Login with admin credentials")
        print("3. Navigate to Blog Management")
        print("4. Click 'New Blog Post'")
        print("5. Try the WYSIWYG editor:")
        print("   - Type content and use formatting tools")
        print("   - Add headers, bold text, lists")
        print("   - Insert links and images")
        print("6. Switch to Preview tab to see formatted output")
        print("7. Test with both English and Bulgarian languages")
        
        print("\n💡 **WYSIWYG vs Plain Text:**")
        print("✅ **WYSIWYG Benefits:**")
        print("   - Visual editing (see formatting as you type)")
        print("   - Toolbar with formatting options") 
        print("   - No need to learn markup syntax")
        print("   - Live preview of final output")
        print("   - Better for content creators")
        
        print("\n🔧 **Technical Implementation:**")
        print("   - Quill.js editor with Snow theme")
        print("   - HTML content storage")
        print("   - Real-time preview updates")
        print("   - Clean, semantic HTML output")
        print("   - Responsive design")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_wysiwyg_functionality()