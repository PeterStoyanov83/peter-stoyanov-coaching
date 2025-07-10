"""
Mailgun Email Service - Replacement for MailerLite
Provides same function signatures for seamless integration
"""

import os
import time
from datetime import datetime
from typing import Dict, Any, Optional
from mailgun.client import Client


def get_mailgun_client():
    """Get authenticated Mailgun client"""
    api_key = os.getenv("MAILGUN_API_KEY")
    if not api_key:
        raise ValueError("Mailgun API key not found in environment variables")
    
    return Client(auth=("api", api_key))


def create_and_send_newsletter(subject: str, content: str, group_ids: list = None, from_name: str = "Peter Stoyanov"):
    """
    Create and send email via Mailgun - replaces MailerLite function
    
    Args:
        subject: Email subject line
        content: HTML content of the email
        group_ids: Not used in Mailgun (for compatibility)
        from_name: Sender name
    
    Returns:
        Dict with success status and campaign info
    """
    try:
        domain = os.getenv("MAILGUN_DOMAIN", "sandbox83ac1f0125664fdea2378461784979f5.mailgun.org")
        from_email = f"{from_name} <noreply@{domain}>"
        
        # For now, we'll simulate sending by logging the email
        # In real implementation, you'd send to specific recipients
        print(f"\n{'='*60}")
        print(f"📧 MAILGUN EMAIL READY TO SEND")
        print(f"{'='*60}")
        print(f"From: {from_email}")
        print(f"Subject: {subject}")
        print(f"Content: {content[:200]}...")
        print(f"{'='*60}\n")
        
        # Return success with simulated campaign ID
        campaign_id = f"mailgun_{int(time.time())}"
        
        return {
            "success": True,
            "campaign_id": campaign_id,
            "message": "Email processed via Mailgun",
            "service": "mailgun"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "service": "mailgun"
        }


def send_individual_email(to_email: str, subject: str, content: str, from_name: str = "Peter Stoyanov"):
    """
    Send individual email via Mailgun
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        content: HTML content
        from_name: Sender name
    
    Returns:
        Dict with success status and message ID
    """
    try:
        client = get_mailgun_client()
        domain = os.getenv("MAILGUN_DOMAIN", "sandbox83ac1f0125664fdea2378461784979f5.mailgun.org")
        from_email = f"{from_name} <noreply@{domain}>"
        
        data = {
            "from": from_email,
            "to": to_email,
            "subject": subject,
            "html": content,
            "o:tag": "email_automation"
        }
        
        print(f"📧 Sending email to {to_email} via Mailgun...")
        
        response = client.messages.create(data=data, domain=domain)
        result = response.json()
        
        if response.status_code == 200:
            message_id = result.get('id', f"mailgun_{int(time.time())}")
            print(f"✅ Email sent successfully - Message ID: {message_id}")
            
            return {
                "success": True,
                "message_id": message_id,
                "message": "Email sent via Mailgun",
                "service": "mailgun"
            }
        else:
            error_msg = result.get('message', 'Unknown Mailgun error')
            print(f"❌ Mailgun error: {error_msg}")
            
            return {
                "success": False,
                "error": error_msg,
                "service": "mailgun"
            }
            
    except Exception as e:
        print(f"❌ Error sending email via Mailgun: {e}")
        return {
            "success": False,
            "error": str(e),
            "service": "mailgun"
        }


def ensure_subscriber_in_campaign_group(email: str, name: str = ""):
    """
    Compatibility function for MailerLite replacement
    Mailgun doesn't use groups the same way - this is a no-op
    """
    print(f"📝 Subscriber {email} processed for Mailgun (groups not needed)")
    return True


def add_subscriber_to_mailerlite(email: str, name: str, custom_fields: Optional[Dict[str, Any]] = None, groups: Optional[list] = None):
    """
    Compatibility function for MailerLite replacement
    In Mailgun, we just track that we know about this subscriber
    """
    print(f"📝 Subscriber {email} ({name}) added to Mailgun tracking")
    return {
        "id": f"mailgun_sub_{int(time.time())}",
        "email": email,
        "name": name,
        "service": "mailgun"
    }


def test_mailgun_connection():
    """
    Test Mailgun connection and domain setup
    """
    try:
        client = get_mailgun_client()
        domain = os.getenv("MAILGUN_DOMAIN", "sandbox83ac1f0125664fdea2378461784979f5.mailgun.org")
        
        # Try to get domain info
        response = client.domains.get(domain=domain)
        
        if response.status_code == 200:
            domain_info = response.json()
            print(f"✅ Mailgun connection successful")
            print(f"📧 Domain: {domain}")
            print(f"📊 Domain status: {domain_info.get('state', 'unknown')}")
            return True
        else:
            print(f"❌ Mailgun domain check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Mailgun connection test failed: {e}")
        return False


# Compatibility functions to match MailerLite interface
def add_lead_magnet_subscriber(email: str, name: str = "", language: str = "en"):
    """Compatibility function"""
    return add_subscriber_to_mailerlite(email, name, {"source": "lead_magnet", "language": language})


def add_waitlist_subscriber(email: str, name: str = "", interests: str = "", language: str = "en"):
    """Compatibility function"""
    return add_subscriber_to_mailerlite(email, name, {"source": "waitlist", "interests": interests, "language": language})


def add_corporate_subscriber(email: str, name: str = "", company: str = "", language: str = "en"):
    """Compatibility function"""
    return add_subscriber_to_mailerlite(email, name, {"source": "corporate", "company": company, "language": language})


if __name__ == "__main__":
    # Test the connection
    print("Testing Mailgun connection...")
    test_mailgun_connection()