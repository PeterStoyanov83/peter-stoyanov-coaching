#!/usr/bin/env python3
"""
Test MailerLite API connectivity
Run this script to verify your MailerLite API key is working
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../.env')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_mailerlite_connection():
    """Test MailerLite API connection"""
    
    print("🧪 Testing MailerLite API Connection")
    print("=" * 40)
    
    # Check if API key is set
    api_key = os.getenv("MAILERLITE_API_KEY")
    
    if not api_key:
        print("❌ MAILERLITE_API_KEY not found in environment variables")
        print("💡 Make sure to:")
        print("   1. Create a .env file in the project root")
        print("   2. Add: MAILERLITE_API_KEY=your_actual_api_key")
        return False
    
    if api_key == "your_mailerlite_api_key_here":
        print("❌ Please replace the placeholder API key with your actual MailerLite API key")
        return False
    
    print(f"✅ API key found: {api_key[:20]}...")
    
    # Test API connection
    try:
        from mailerlite import get_subscriber_groups
        
        print("\n🔗 Testing API connection...")
        groups = get_subscriber_groups()
        
        print("✅ Successfully connected to MailerLite!")
        print(f"📊 Found {len(groups)} subscriber groups:")
        
        for group in groups[:3]:  # Show first 3 groups
            print(f"   - {group.get('name', 'Unnamed Group')} (ID: {group.get('id')})")
        
        if len(groups) > 3:
            print(f"   ... and {len(groups) - 3} more groups")
            
        return True
        
    except Exception as e:
        print(f"❌ MailerLite API Error: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Verify your API key is correct")
        print("   2. Check your internet connection")
        print("   3. Make sure your MailerLite account is active")
        return False

def test_add_subscriber():
    """Test adding a subscriber"""
    
    print("\n🧪 Testing Add Subscriber Functionality")
    print("=" * 40)
    
    try:
        from mailerlite import add_subscriber_to_mailerlite
        
        # Test with a dummy email
        test_email = "test-subscriber@example.com"
        print(f"🔍 Testing with email: {test_email}")
        
        result = add_subscriber_to_mailerlite(
            email=test_email,
            name="Test Subscriber",
            custom_fields={"source": "api_test", "test": "true"}
        )
        
        print("✅ Successfully added test subscriber!")
        print(f"📧 Subscriber ID: {result.get('id')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error adding subscriber: {e}")
        return False

if __name__ == "__main__":
    success = test_mailerlite_connection()
    
    if success:
        test_add_subscriber()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 MailerLite is ready to use!")
        print("✅ Your lead magnet will now automatically add emails to MailerLite")
    else:
        print("⚠️  Please fix the issues above before using MailerLite integration")
        print("💡 The system will still work - emails will be stored in the local database")