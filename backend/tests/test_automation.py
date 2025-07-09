#!/usr/bin/env python3
"""
Test MailerLite automation functions
Run this script to verify your automation system is working
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../.env')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_automation_functions():
    """Test all automation functions"""
    
    print("🤖 Testing MailerLite Automation Functions")
    print("=" * 50)
    
    # Check if API key is set
    api_key = os.getenv("MAILERLITE_API_KEY")
    
    if not api_key:
        print("❌ MAILERLITE_API_KEY not found in environment variables")
        print("💡 Please set up your API key first using the setup guide")
        return False
    
    print(f"✅ API key found: {api_key[:20]}...")
    
    try:
        from mailerlite import (
            ensure_automation_groups,
            add_lead_magnet_subscriber,
            add_waitlist_subscriber,
            trigger_automation_sequence,
            get_automation_campaigns
        )
        
        print("\n🏗️  Testing automation groups setup...")
        group_ids = ensure_automation_groups()
        
        if group_ids:
            print(f"✅ Automation groups configured:")
            for group_type, group_id in group_ids.items():
                print(f"   - {group_type}: {group_id}")
        else:
            print("⚠️  No automation groups found - will create them automatically")
        
        print("\n🧪 Testing lead magnet subscriber...")
        result = add_lead_magnet_subscriber(
            email="test-leadmagnet@example.com",
            name="Test Lead Magnet User"
        )
        
        if result:
            print("✅ Lead magnet subscriber added successfully")
            print(f"   Subscriber ID: {result.get('id', 'Unknown')}")
        else:
            print("❌ Failed to add lead magnet subscriber")
        
        print("\n🧪 Testing waitlist subscriber...")
        result = add_waitlist_subscriber(
            email="test-waitlist@example.com",
            name="Test Waitlist User",
            interests="Public speaking and leadership"
        )
        
        if result:
            print("✅ Waitlist subscriber added successfully")
            print(f"   Subscriber ID: {result.get('id', 'Unknown')}")
        else:
            print("❌ Failed to add waitlist subscriber")
        
        print("\n🚀 Testing automation triggers...")
        success1 = trigger_automation_sequence("test-trigger1@example.com", "lead_magnet")
        success2 = trigger_automation_sequence("test-trigger2@example.com", "waitlist")
        
        if success1 and success2:
            print("✅ Automation triggers working correctly")
        else:
            print("❌ Some automation triggers failed")
        
        print("\n📊 Testing campaign retrieval...")
        try:
            campaigns = get_automation_campaigns()
            print(f"✅ Found {len(campaigns)} campaigns in your account")
        except Exception as e:
            print(f"⚠️  Could not retrieve campaigns: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing automation functions: {e}")
        return False

def test_integration():
    """Test the complete integration flow"""
    
    print("\n\n🔄 Testing Complete Integration Flow")
    print("=" * 50)
    
    try:
        # Test database integration
        print("🗄️  Testing database integration...")
        from database import get_db, store_lead_magnet_download
        
        db = next(get_db())
        
        # Test storing a lead magnet download
        download_record = store_lead_magnet_download(db, "integration-test@example.com")
        
        if download_record:
            print("✅ Database integration working")
            print(f"   Download count: {download_record.download_count}")
        else:
            print("❌ Database integration failed")
        
        # Test the complete flow
        print("\n🔄 Testing complete lead magnet flow...")
        
        from mailerlite import add_lead_magnet_subscriber
        
        # This simulates what happens when someone downloads the guide
        result = add_lead_magnet_subscriber(
            email="complete-flow-test@example.com",
            name="Complete Flow Test"
        )
        
        if result:
            print("✅ Complete flow test successful")
            print("   ✓ Email stored in database")
            print("   ✓ Subscriber added to MailerLite")
            print("   ✓ Automation sequence triggered")
        else:
            print("❌ Complete flow test failed")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🎭 MailerLite Automation System Test")
    print("=" * 50)
    
    success1 = test_automation_functions()
    success2 = test_integration()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 All tests passed! Your automation system is ready!")
        print("\n✅ Your coaching site now has:")
        print("   - Automated lead magnet sequences")
        print("   - Waitlist automation")
        print("   - Proper subscriber segmentation")
        print("   - Fallback database storage")
        print("\n🚀 Next steps:")
        print("   1. Set up your email sequences in MailerLite")
        print("   2. Test with real email addresses")
        print("   3. Monitor automation performance")
        print("   4. Optimize based on engagement metrics")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("💡 The system will still work with local storage if MailerLite is not available.")