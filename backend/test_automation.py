"""
Automated testing script for email automation
Tests with pre-authorized email addresses
"""

import requests
import os
from database import get_db
from sequence_automation import auto_enroll_subscriber
from email_scheduler import EmailScheduler

# Test emails for SendGrid
TEST_EMAILS = [
    "peterstoyanov83@gmail.com",  # Your primary email
    "p.stoyanov@craftgenie.ai",   # Your business email
    "test@peterstoyanov-pepe.com" # Add this if you have email forwarding
]

def test_full_automation(test_email: str, test_mode: bool = False):
    """
    Test the complete automation flow
    
    Args:
        test_email: Email to test with (should be in authorized recipients)
        test_mode: If True, converts days to minutes for fast testing
    """
    print(f"🧪 Testing automation with {test_email}")
    print(f"📅 Test mode: {test_mode}")
    
    # Step 1: Simulate form submission
    print("\n1️⃣ Simulating lead magnet subscription...")
    db = next(get_db())
    
    result = auto_enroll_subscriber(
        db,
        email=test_email,
        name="Test User",
        source="lead_magnet",
        language="en",
        custom_fields={
            "guide": "5_theater_secrets",
            "test_subscription": True
        },
        test_mode=test_mode
    )
    
    if result['success']:
        print(f"✅ Subscriber enrolled: ID {result['subscriber_id']}")
        print(f"✅ Enrollment created: ID {result['enrollment_id']}")
    else:
        print(f"❌ Enrollment failed: {result.get('error')}")
        return False
    
    # Step 2: Process scheduled emails
    print("\n2️⃣ Processing scheduled emails...")
    scheduler = EmailScheduler()
    
    try:
        scheduler.process_scheduled_emails()
        print("✅ Email scheduler completed")
    except Exception as e:
        print(f"❌ Email processing failed: {e}")
        return False
    
    print(f"\n🎉 Test completed for {test_email}")
    print("📧 Check your inbox for the welcome email!")
    
    if test_mode:
        print("⚡ Test mode enabled - emails will be sent every few minutes instead of weekly")
    
    return True

def check_sendgrid_setup():
    """Check SendGrid configuration"""
    print("📋 Testing with SendGrid API:")
    for email in TEST_EMAILS:
        print(f"   - {email}")
    
    api_key = os.getenv('SENDGRID_API_KEY')
    if api_key:
        print(f"✅ SendGrid API key configured: {api_key[:10]}...")
    else:
        print("❌ SendGrid API key not found in environment")
    
    domain = os.getenv('SENDGRID_DOMAIN', 'peterstoyanov-pepe.com')
    print(f"📧 Sending domain: {domain}")

def test_with_sendgrid():
    """Test automation with SendGrid"""
    test_email = TEST_EMAILS[0]  # peterstoyanov83@gmail.com
    print(f"🚀 Testing with SendGrid email: {test_email}")
    
    return test_full_automation(test_email, test_mode=True)

if __name__ == "__main__":
    print("🔧 SendGrid Email Automation Tester")
    print("=" * 50)
    
    # Check SendGrid setup
    check_sendgrid_setup()
    
    print("\n" + "=" * 50)
    choice = input("Run test with peterstoyanov83@gmail.com? (y/n): ")
    
    if choice.lower() == 'y':
        test_with_sendgrid()
    else:
        print("💡 Set SENDGRID_API_KEY environment variable first, then run:")
        print("   python test_automation.py")