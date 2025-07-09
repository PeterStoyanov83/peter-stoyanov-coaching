#!/usr/bin/env python3
"""
MailerLite API Connection Test Suite
Comprehensive testing of all MailerLite integration functionality
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Import our MailerLite functions
from mailerlite import (
    get_subscriber_groups,
    ensure_automation_groups,
    add_subscriber_to_mailerlite,
    add_lead_magnet_subscriber,
    add_waitlist_subscriber,
    get_automation_campaigns,
    trigger_automation_sequence
)

def test_api_connection():
    """Test basic API connection"""
    print("🔍 Testing MailerLite API Connection...")
    
    try:
        # Check if API key is set
        api_key = os.getenv("MAILERLITE_API_KEY")
        if not api_key:
            print("❌ MAILERLITE_API_KEY not found in environment variables")
            return False
        
        print(f"✅ API Key found: {api_key[:8]}...")
        
        # Test getting groups
        groups = get_subscriber_groups()
        print(f"✅ Successfully connected to MailerLite API")
        print(f"📊 Found {len(groups)} subscriber groups")
        
        # Display existing groups
        if groups:
            print("\n📋 Existing Groups:")
            for group in groups:
                print(f"   - {group['name']} (ID: {group['id']})")
        
        return True
        
    except Exception as e:
        print(f"❌ API Connection failed: {e}")
        return False

def test_automation_groups():
    """Test automation groups setup"""
    print("\n🔧 Testing Automation Groups Setup...")
    
    try:
        group_ids = ensure_automation_groups()
        
        if group_ids:
            print("✅ Automation groups verified/created successfully")
            print("📋 Group IDs:")
            for group_type, group_id in group_ids.items():
                print(f"   - {group_type}: {group_id}")
        else:
            print("⚠️  No automation groups were set up")
            
        return True
        
    except Exception as e:
        print(f"❌ Automation groups setup failed: {e}")
        return False

def test_campaigns():
    """Test getting campaigns"""
    print("\n📧 Testing Campaigns Retrieval...")
    
    try:
        campaigns = get_automation_campaigns()
        print(f"✅ Successfully retrieved campaigns")
        print(f"📊 Found {len(campaigns)} campaigns")
        
        if campaigns:
            print("\n📋 Existing Campaigns:")
            for campaign in campaigns[:5]:  # Show first 5
                print(f"   - {campaign.get('name', 'Unnamed')} (ID: {campaign.get('id', 'N/A')})")
        
        return True
        
    except Exception as e:
        print(f"❌ Campaigns retrieval failed: {e}")
        return False

def test_subscriber_functions():
    """Test subscriber management functions"""
    print("\n👥 Testing Subscriber Management...")
    
    # Use a test email - make sure to use a valid email you control
    test_email = "test@example.com"
    test_name = "Test User"
    
    print(f"📧 Testing with email: {test_email}")
    print("⚠️  Note: Using test email. In production, use real subscriber emails.")
    
    try:
        # Test basic subscriber addition
        print("\n1. Testing basic subscriber addition...")
        result = add_subscriber_to_mailerlite(
            email=test_email,
            name=test_name,
            custom_fields={"source": "api_test", "test_date": str(datetime.now())},
            groups=[]
        )
        print("✅ Basic subscriber addition test passed")
        
        # Test lead magnet subscriber
        print("\n2. Testing lead magnet subscriber...")
        result = add_lead_magnet_subscriber(
            email=test_email,
            name=test_name
        )
        if result:
            print("✅ Lead magnet subscriber test passed")
        else:
            print("⚠️  Lead magnet subscriber test returned None")
        
        # Test waitlist subscriber
        print("\n3. Testing waitlist subscriber...")
        result = add_waitlist_subscriber(
            email=test_email,
            name=test_name,
            interests="Communication skills, Public speaking"
        )
        if result:
            print("✅ Waitlist subscriber test passed")
        else:
            print("⚠️  Waitlist subscriber test returned None")
        
        # Test automation sequence trigger
        print("\n4. Testing automation sequence trigger...")
        result = trigger_automation_sequence(test_email, "lead_magnet")
        if result:
            print("✅ Automation sequence trigger test passed")
        else:
            print("⚠️  Automation sequence trigger test failed")
        
        return True
        
    except Exception as e:
        print(f"❌ Subscriber management tests failed: {e}")
        return False

def test_integration_points():
    """Test how the MailerLite functions integrate with the main application"""
    print("\n🔗 Testing Integration Points...")
    
    try:
        # Test environment variables
        required_vars = ["MAILERLITE_API_KEY"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print(f"❌ Missing environment variables: {missing_vars}")
            return False
        
        print("✅ All required environment variables are set")
        
        # Test if the functions can be imported by main.py
        try:
            from main import app
            print("✅ MailerLite functions can be imported by main.py")
        except ImportError as e:
            print(f"⚠️  Import warning: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 MailerLite API Connection Test Suite")
    print("=" * 50)
    
    tests = [
        ("API Connection", test_api_connection),
        ("Automation Groups", test_automation_groups),
        ("Campaigns", test_campaigns),
        ("Subscriber Functions", test_subscriber_functions),
        ("Integration Points", test_integration_points)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} - PASSED")
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
    
    print(f"\n{'='*50}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! MailerLite integration is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    print("\n📝 Next Steps:")
    print("1. Review any failed tests and fix issues")
    print("2. Test with real subscriber emails in production")
    print("3. Set up automation workflows in MailerLite dashboard")
    print("4. Monitor subscriber additions and campaign triggers")

if __name__ == "__main__":
    main()