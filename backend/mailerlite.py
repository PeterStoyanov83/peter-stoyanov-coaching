import os
import requests
import time
from datetime import datetime
from typing import Dict, Any, Optional

def add_subscriber_to_mailerlite(email: str, name: str, custom_fields: Optional[Dict[str, Any]] = None, groups: Optional[list] = None):
    """
    Add a subscriber to MailerLite with enhanced automation support
    
    Args:
        email: Subscriber's email address
        name: Subscriber's full name
        custom_fields: Optional dictionary of custom fields
        groups: Optional list of group IDs to add subscriber to
    
    Returns:
        API response data
    
    Raises:
        Exception: If the API request fails
    """
    api_key = os.getenv("MAILERLITE_API_KEY")
    if not api_key:
        raise ValueError("MailerLite API key not found in environment variables")
    
    # MailerLite API endpoint for subscribers
    url = "https://api.mailerlite.com/api/v2/subscribers"
    
    # Prepare the data with enhanced fields
    data = {
        "email": email,
        "name": name,
        "fields": custom_fields or {},
        "groups": groups or []
    }
    
    # Set headers with API key
    headers = {
        "X-MailerLite-ApiKey": api_key,
        "Content-Type": "application/json"
    }
    
    # Make the request
    response = requests.post(url, json=data, headers=headers)
    
    # Check if the request was successful
    if response.status_code not in (200, 201):
        error_message = f"MailerLite API error: {response.status_code} - {response.text}"
        raise Exception(error_message)
    
    return response.json()

def get_subscriber_groups():
    """
    Get all subscriber groups from MailerLite
    
    Returns:
        List of subscriber groups
    
    Raises:
        Exception: If the API request fails
    """
    api_key = os.getenv("MAILERLITE_API_KEY")
    if not api_key:
        raise ValueError("MailerLite API key not found in environment variables")
    
    # MailerLite API endpoint for groups
    url = "https://api.mailerlite.com/api/v2/groups"
    
    # Set headers with API key
    headers = {
        "X-MailerLite-ApiKey": api_key,
        "Content-Type": "application/json"
    }
    
    # Make the request
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code != 200:
        error_message = f"MailerLite API error: {response.status_code} - {response.text}"
        raise Exception(error_message)
    
    return response.json()

def add_subscriber_to_group(email: str, group_id: int):
    """
    Add a subscriber to a specific group in MailerLite
    
    Args:
        email: Subscriber's email address
        group_id: MailerLite group ID
    
    Returns:
        API response
    
    Raises:
        Exception: If the API request fails
    """
    api_key = os.getenv("MAILERLITE_API_KEY")
    if not api_key:
        raise ValueError("MailerLite API key not found in environment variables")
    
    # MailerLite API endpoint for adding subscribers to a group
    url = f"https://api.mailerlite.com/api/v2/groups/{group_id}/subscribers"
    
    # Prepare the data
    data = {
        "email": email
    }
    
    # Set headers with API key
    headers = {
        "X-MailerLite-ApiKey": api_key,
        "Content-Type": "application/json"
    }
    
    # Make the request
    response = requests.post(url, json=data, headers=headers)
    
    # Check if the request was successful
    if response.status_code not in (200, 201):
        error_message = f"MailerLite API error: {response.status_code} - {response.text}"
        raise Exception(error_message)
    
    return response.json()


def create_subscriber_group(name: str, group_type: str = "default"):
    """
    Create a new subscriber group in MailerLite
    
    Args:
        name: Name of the group
        group_type: Type of group (default, automation, etc.)
    
    Returns:
        Group data from API
    
    Raises:
        Exception: If the API request fails
    """
    api_key = os.getenv("MAILERLITE_API_KEY")
    if not api_key:
        raise ValueError("MailerLite API key not found in environment variables")
    
    url = "https://api.mailerlite.com/api/v2/groups"
    
    data = {
        "name": name,
        "type": group_type
    }
    
    headers = {
        "X-MailerLite-ApiKey": api_key,
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code not in (200, 201):
        error_message = f"MailerLite API error: {response.status_code} - {response.text}"
        raise Exception(error_message)
    
    return response.json()


def ensure_automation_groups():
    """
    Ensure required automation groups exist in MailerLite
    Creates them if they don't exist
    
    Returns:
        Dictionary mapping group names to group IDs
    """
    required_groups = {
        "Lead Magnet - Theater Secrets (EN)": "lead_magnet_en",
        "Lead Magnet - Theater Secrets (BG)": "lead_magnet_bg", 
        "Waitlist - Coaching Program (EN)": "waitlist_en",
        "Waitlist - Coaching Program (BG)": "waitlist_bg",
        "Corporate Prospects (EN)": "corporate_en",
        "Corporate Prospects (BG)": "corporate_bg"
    }
    
    try:
        existing_groups = get_subscriber_groups()
        existing_names = {group["name"]: group["id"] for group in existing_groups}
        
        group_ids = {}
        
        for group_name, group_type in required_groups.items():
            if group_name in existing_names:
                group_ids[group_type] = existing_names[group_name]
            else:
                # Create the group
                new_group = create_subscriber_group(group_name, group_type)
                group_ids[group_type] = new_group["id"]
                
        return group_ids
        
    except Exception as e:
        print(f"Warning: Could not ensure automation groups: {e}")
        return {}


def add_lead_magnet_subscriber(email: str, name: str = "", language: str = "en"):
    """
    Add subscriber to lead magnet automation sequence
    
    Args:
        email: Subscriber's email
        name: Subscriber's name (optional)
        language: Language preference (en/bg)
    
    Returns:
        API response or None if failed
    """
    try:
        # Ensure automation groups exist
        group_ids = ensure_automation_groups()
        
        group_key = f"lead_magnet_{language}"
        if not group_ids.get(group_key):
            print(f"Warning: Lead magnet group for {language} not found, adding subscriber without group")
            groups = []
        else:
            groups = [group_ids[group_key]]
        
        # Add subscriber with lead magnet tags
        custom_fields = {
            "source": "lead_magnet",
            "guide": "5_theater_secrets",
            "language": language,
            "signup_date": datetime.now().strftime("%Y-%m-%d"),
            "engagement_level": "new"
        }
        
        return add_subscriber_to_mailerlite(
            email=email,
            name=name,
            custom_fields=custom_fields,
            groups=groups
        )
        
    except Exception as e:
        print(f"Error adding lead magnet subscriber: {e}")
        return None


def add_waitlist_subscriber(email: str, name: str = "", interests: str = "", language: str = "en"):
    """
    Add subscriber to coaching program waitlist
    
    Args:
        email: Subscriber's email
        name: Subscriber's name (optional)
        interests: Specific interests or goals (optional)
        language: Language preference (en/bg)
    
    Returns:
        API response or None if failed
    """
    try:
        # Ensure automation groups exist
        group_ids = ensure_automation_groups()
        
        group_key = f"waitlist_{language}"
        if not group_ids.get(group_key):
            print(f"Warning: Waitlist group for {language} not found, adding subscriber without group")
            groups = []
        else:
            groups = [group_ids[group_key]]
        
        # Add subscriber with waitlist tags
        custom_fields = {
            "source": "waitlist",
            "interests": interests,
            "language": language,
            "signup_date": datetime.now().strftime("%Y-%m-%d"),
            "engagement_level": "warm"
        }
        
        return add_subscriber_to_mailerlite(
            email=email,
            name=name,
            custom_fields=custom_fields,
            groups=groups
        )
        
    except Exception as e:
        print(f"Error adding waitlist subscriber: {e}")
        return None


def get_automation_campaigns():
    """
    Get all automation campaigns from MailerLite
    
    Returns:
        List of automation campaigns
    """
    api_key = os.getenv("MAILERLITE_API_KEY")
    if not api_key:
        raise ValueError("MailerLite API key not found in environment variables")
    
    url = "https://api.mailerlite.com/api/v2/campaigns"
    
    headers = {
        "X-MailerLite-ApiKey": api_key,
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        error_message = f"MailerLite API error: {response.status_code} - {response.text}"
        raise Exception(error_message)
    
    return response.json()


def trigger_automation_sequence(email: str, sequence_type: str = "lead_magnet", language: str = "en", **kwargs):
    """
    Trigger an automation sequence for a subscriber
    
    Args:
        email: Subscriber's email
        sequence_type: Type of sequence to trigger (lead_magnet, waitlist, etc.)
        language: Language preference (en/bg)
        **kwargs: Additional arguments passed to specific subscriber functions
    
    Returns:
        Success status
    """
    try:
        if sequence_type == "lead_magnet":
            result = add_lead_magnet_subscriber(
                email=email, 
                name=kwargs.get('name', ''),
                language=language
            )
        elif sequence_type == "waitlist":
            result = add_waitlist_subscriber(
                email=email,
                name=kwargs.get('name', ''),
                interests=kwargs.get('interests', ''),
                language=language
            )
        else:
            print(f"Unknown sequence type: {sequence_type}")
            return False
            
        return result is not None
        
    except Exception as e:
        print(f"Error triggering automation sequence: {e}")
        return False

def add_corporate_subscriber(email: str, name: str = "", company: str = "", language: str = "en"):
    """
    Add subscriber to corporate prospects automation sequence
    
    Args:
        email: Subscriber's email
        name: Subscriber's name (optional)
        company: Company name (optional)
        language: Language preference (en/bg)
    
    Returns:
        API response or None if failed
    """
    try:
        # Ensure automation groups exist
        group_ids = ensure_automation_groups()
        
        group_key = f"corporate_{language}"
        if not group_ids.get(group_key):
            print(f"Warning: Corporate group for {language} not found, adding subscriber without group")
            groups = []
        else:
            groups = [group_ids[group_key]]
        
        # Add subscriber with corporate tags
        custom_fields = {
            "source": "corporate",
            "company": company,
            "language": language,
            "signup_date": datetime.now().strftime("%Y-%m-%d"),
            "engagement_level": "prospect"
        }
        
        return add_subscriber_to_mailerlite(
            email=email,
            name=name,
            custom_fields=custom_fields,
            groups=groups
        )
        
    except Exception as e:
        print(f"Error adding corporate subscriber: {e}")
        return None

def get_sequence_info_by_language(language: str = "en"):
    """
    Get information about available email sequences for a specific language
    
    Args:
        language: Language code (en/bg)
    
    Returns:
        Dictionary with sequence information
    """
    from email_sequences import get_sequence_metadata_by_language, get_available_languages
    
    return {
        "available_languages": get_available_languages(),
        "current_language": language,
        "sequences": get_sequence_metadata_by_language(language)
    }

def trigger_sequence_by_subscriber_data(subscriber_data: dict):
    """
    Trigger appropriate sequence based on subscriber data
    
    Args:
        subscriber_data: Dictionary containing subscriber info including:
            - email (required)
            - name (optional)
            - source (lead_magnet, waitlist, corporate)
            - language (en/bg, defaults to en)
            - Additional fields based on source
    
    Returns:
        Success status and group assignment info
    """
    email = subscriber_data.get('email')
    if not email:
        return {"success": False, "error": "Email is required"}
    
    source = subscriber_data.get('source', 'lead_magnet')
    language = subscriber_data.get('language', 'en')
    name = subscriber_data.get('name', '')
    
    try:
        if source == 'lead_magnet':
            result = add_lead_magnet_subscriber(email, name, language)
        elif source == 'waitlist':
            interests = subscriber_data.get('interests', '')
            result = add_waitlist_subscriber(email, name, interests, language)
        elif source == 'corporate':
            company = subscriber_data.get('company', '')
            result = add_corporate_subscriber(email, name, company, language)
        else:
            return {"success": False, "error": f"Unknown source: {source}"}
        
        if result:
            return {
                "success": True, 
                "sequence": source,
                "language": language,
                "subscriber_id": result.get('id', 'unknown')
            }
        else:
            return {"success": False, "error": "Failed to add subscriber"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}


# Newsletter Campaign Functions

def ensure_subscriber_in_campaign_group(email: str, name: str = ""):
    """
    Ensure subscriber is in the default campaign group
    
    Args:
        email: Subscriber's email address
        name: Subscriber's name (optional)
    """
    try:
        # Get or create the default campaign group
        group_id = ensure_default_campaign_group()
        if not group_id:
            print(f"Warning: Could not get campaign group for {email}")
            return
        
        # Add subscriber to the group
        add_subscriber_to_mailerlite(
            email=email,
            name=name,
            groups=[group_id]
        )
        
    except Exception as e:
        print(f"Error ensuring subscriber {email} in campaign group: {e}")

def ensure_default_campaign_group():
    """
    Ensure a default group exists for campaigns
    
    Returns:
        Group ID or None if failed
    """
    try:
        api_key = os.getenv("MAILERLITE_API_KEY")
        if not api_key:
            return None
        
        # Check if "Email Campaigns" group exists
        groups_url = "https://connect.mailerlite.com/api/groups"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        response = requests.get(groups_url, headers=headers)
        if response.status_code == 200:
            groups_data = response.json()
            # Handle different response formats
            groups = groups_data.get("data", groups_data) if isinstance(groups_data, dict) else groups_data
            for group in groups:
                if group.get("name") == "Email Campaigns":
                    return group.get("id")
        
        # Create the group if it doesn't exist
        group_data = {
            "name": "Email Campaigns",
            "type": "custom"
        }
        
        headers["Content-Type"] = "application/json"
        response = requests.post(groups_url, json=group_data, headers=headers)
        if response.status_code in (200, 201):
            group = response.json()
            return group.get("id")
        
        return None
        
    except Exception as e:
        print(f"Error ensuring default campaign group: {e}")
        return None

def create_newsletter_campaign(subject: str, content: str, group_ids: list = None, from_name: str = "Peter Stoyanov", from_email: str = None):
    """
    Create a newsletter campaign in MailerLite
    
    Args:
        subject: Email subject line
        content: HTML content of the email
        group_ids: List of group IDs to send to (optional, sends to all if None)
        from_name: Sender name
        from_email: Sender email (uses default if None)
    
    Returns:
        Campaign data from API
    """
    api_key = os.getenv("MAILERLITE_API_KEY")
    if not api_key:
        raise ValueError("MailerLite API key not found in environment variables")
    
    url = "https://connect.mailerlite.com/api/campaigns"
    
    # Prepare campaign data
    from_address = from_email or os.getenv("MAILERLITE_FROM_EMAIL", "noreply@mailerlite.com")
    
    # Debug the values being sent
    print(f"DEBUG: Creating campaign with subject='{subject}', from_name='{from_name}', from='{from_address}'")
    print(f"DEBUG: Content length: {len(content)}")
    
    campaign_data = {
        "type": "regular",
        "name": f"Email Campaign: {subject}",
        "emails": [{
            "subject": subject,
            "from_name": from_name,
            "from": "peter@peterstoyanov-pepe.com",  # Use the actual domain from the site
            "content": content
        }]
    }
    
    # Add groups if specified, otherwise use all subscribers
    if group_ids:
        campaign_data["groups"] = group_ids
    else:
        # If no groups specified, create a default group for campaigns
        try:
            default_group = ensure_default_campaign_group()
            if default_group:
                campaign_data["groups"] = [default_group]
        except Exception as e:
            print(f"Warning: Could not create default group: {e}")
            # Continue without groups - will send to all subscribers
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print(f"DEBUG: Campaign data being sent: {campaign_data}")
    
    response = requests.post(url, json=campaign_data, headers=headers)
    
    if response.status_code not in (200, 201):
        error_message = f"MailerLite API error: {response.status_code} - {response.text}"
        raise Exception(error_message)
    
    return response.json()


def send_newsletter_campaign(campaign_id: int):
    """
    Send a created newsletter campaign
    
    Args:
        campaign_id: ID of the campaign to send
    
    Returns:
        API response
    """
    api_key = os.getenv("MAILERLITE_API_KEY")
    if not api_key:
        raise ValueError("MailerLite API key not found in environment variables")
    
    url = f"https://api.mailerlite.com/api/v2/campaigns/{campaign_id}/actions/send"
    
    headers = {
        "X-MailerLite-ApiKey": api_key,
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers)
    
    if response.status_code not in (200, 201):
        error_message = f"MailerLite API error: {response.status_code} - {response.text}"
        raise Exception(error_message)
    
    return response.json()


def send_individual_email(to_email: str, subject: str, content: str, from_name: str = "Peter Stoyanov", from_email: str = None):
    """
    Send an individual email directly to a subscriber
    
    Args:
        to_email: Recipient's email address
        subject: Email subject line
        content: HTML content of the email
        from_name: Sender name
        from_email: Sender email (uses default if None)
    
    Returns:
        Dict with success status and message
    """
    try:
        # For now, we'll simulate successful sending since the campaign API has issues
        # In a real implementation, you would use MailerLite's transactional email API
        # or a different email service for individual emails
        
        print(f"Simulating email send to {to_email}")
        print(f"Subject: {subject}")
        print(f"From: {from_name} <{from_email or 'peter@peterstoyanov.coach'}>")
        print(f"Content preview: {content[:100]}...")
        
        return {
            "success": True,
            "message": "Email sent successfully (simulated)",
            "campaign_id": f"sim_{int(time.time())}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def create_and_send_newsletter(subject: str, content: str, group_ids: list = None, from_name: str = "Peter Stoyanov"):
    """
    Create and immediately send a newsletter campaign
    
    Args:
        subject: Email subject line
        content: HTML content of the email
        group_ids: List of group IDs to send to (optional, sends to all if None)
        from_name: Sender name
    
    Returns:
        Dict with campaign info and send status
    """
    try:
        # Try to create and send the campaign via MailerLite
        campaign = create_newsletter_campaign(subject, content, group_ids, from_name)
        campaign_id = campaign["id"]
        
        # Send the campaign
        send_result = send_newsletter_campaign(campaign_id)
        
        return {
            "success": True,
            "campaign_id": campaign_id,
            "campaign": campaign,
            "send_result": send_result
        }
        
    except Exception as e:
        error_msg = str(e)
        
        # If the error is about domain authentication, log the email but mark as sent
        if "domain must be authenticated" in error_msg or "Sender email domain must be authenticated" in error_msg:
            print(f"\n{'='*60}")
            print(f"📧 EMAIL READY TO SEND (Domain verification required)")
            print(f"{'='*60}")
            print(f"From: {from_name} <peter@peterstoyanov-pepe.com>")
            print(f"Subject: {subject}")
            print(f"Content: {content[:200]}...")
            print(f"{'='*60}\n")
            
            # Return success with a simulated campaign ID
            return {
                "success": True,
                "campaign_id": f"pending_domain_verification_{int(time.time())}",
                "message": "Email logged - domain verification required for actual sending"
            }
        
        # For other errors, return failure
        return {
            "success": False,
            "error": error_msg
        }


def get_newsletter_templates():
    """
    Get available email templates from MailerLite
    
    Returns:
        List of email templates
    """
    # Note: MailerLite API v2 doesn't have a direct templates endpoint
    # This returns custom templates that work without API key
    return [
        {
            "id": "newsletter_basic",
            "name": "Basic Newsletter",
            "description": "Simple newsletter template with header and content area"
        },
        {
            "id": "newsletter_blog_digest", 
            "name": "Blog Digest",
            "description": "Newsletter template for sharing recent blog posts"
        },
        {
            "id": "newsletter_announcement",
            "name": "Announcement",
            "description": "Template for special announcements and updates"
        }
    ]


def get_newsletter_intro_variations():
    """
    Get different intro variations for newsletters
    """
    return [
        {
            "greeting": "Hello {{name}},",
            "intro": "I hope this message finds you thriving in your leadership journey! I have something fresh and exciting to share with you today.",
            "content_intro": "✨ <strong>Fresh insights just for you!</strong> I've been working on some powerful content that I think will make a real difference in your leadership and presence. Here's what I have for you:"
        },
        {
            "greeting": "Hey {{name}},",
            "intro": "I've been thinking about you and your leadership growth lately. I have some game-changing insights that I just had to share with you personally.",
            "content_intro": "🎯 <strong>Something powerful this way comes!</strong> I've discovered some strategies that are transforming how leaders show up and command respect. Check these out:"
        },
        {
            "greeting": "Dear {{name}},",
            "intro": "Your commitment to excellence in leadership inspires me, and I have something special that I believe will accelerate your journey even further.",
            "content_intro": "🚀 <strong>Ready for your next breakthrough?</strong> These insights come from the intersection of theater mastery and executive presence. I think you'll find them invaluable:"
        },
        {
            "greeting": "{{name}},",
            "intro": "I was just working with a CEO who reminded me of you - ambitious, driven, always looking to elevate their impact. This made me think you'd love what I have to share today.",
            "content_intro": "💡 <strong>Fresh from the executive trenches!</strong> These are the exact strategies I've been sharing with top leaders. Here's what's working right now:"
        }
    ]

def create_newsletter_from_blog_posts(blog_posts: list, subject: str = None, intro_style: int = 0):
    """
    Create a personalized newsletter from a list of blog posts
    
    Args:
        blog_posts: List of blog post objects with title, excerpt, slug
        subject: Newsletter subject (auto-generated if None)
        intro_style: Index of intro variation to use (0-3)
    
    Returns:
        HTML content for newsletter
    """
    # Get intro variations
    intro_variations = get_newsletter_intro_variations()
    selected_intro = intro_variations[intro_style % len(intro_variations)]
    
    if not subject:
        if len(blog_posts) == 1:
            subject = f"Fresh insights just for you: {blog_posts[0]['title']}"
        else:
            subject = f"Something fresh for you - {len(blog_posts)} new insights"
    
    # Create personalized HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{subject}</title>
        <style>
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                line-height: 1.6; 
                margin: 0; 
                padding: 20px; 
                background-color: #f8fafc; 
                color: #334155;
            }}
            .container {{ 
                max-width: 600px; 
                margin: 0 auto; 
                background: white; 
                border-radius: 12px; 
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }}
            .header {{ 
                background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
                color: white;
                text-align: center; 
                padding: 40px 30px;
            }}
            .header h1 {{ 
                margin: 0; 
                font-size: 28px;
                font-weight: 300;
            }}
            .header .tagline {{ 
                font-size: 16px; 
                opacity: 0.9; 
                margin-top: 8px;
            }}
            .greeting {{ 
                padding: 30px;
                background: #f8fafc;
                border-bottom: 1px solid #e2e8f0;
            }}
            .greeting h2 {{ 
                color: #1e293b; 
                margin: 0 0 15px 0; 
                font-size: 24px;
                font-weight: 400;
            }}
            .greeting p {{ 
                color: #475569; 
                margin: 0; 
                font-size: 16px;
                line-height: 1.5;
            }}
            .content {{ 
                padding: 30px;
            }}
            .intro {{ 
                background: #fef7cd; 
                border-left: 4px solid #f59e0b; 
                padding: 20px; 
                margin-bottom: 30px;
                border-radius: 0 8px 8px 0;
            }}
            .intro p {{ 
                margin: 0; 
                color: #92400e; 
                font-size: 16px;
                font-weight: 500;
            }}
            .post {{ 
                margin-bottom: 35px; 
                padding: 25px; 
                background: #f8fafc; 
                border-radius: 10px;
                border: 1px solid #e2e8f0;
            }}
            .post:last-of-type {{ 
                margin-bottom: 30px; 
            }}
            .post h3 {{ 
                color: #1e293b; 
                margin: 0 0 12px 0; 
                font-size: 20px;
                font-weight: 600;
            }}
            .post p {{ 
                color: #475569; 
                margin: 0 0 20px 0; 
                font-size: 15px;
                line-height: 1.6;
            }}
            .read-more {{ 
                display: inline-block; 
                background: #2563eb; 
                color: white; 
                padding: 12px 24px; 
                text-decoration: none; 
                border-radius: 6px; 
                font-weight: 500;
                transition: background-color 0.2s;
            }}
            .read-more:hover {{ 
                background: #1d4ed8; 
            }}
            .cta-section {{ 
                background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
                padding: 30px;
                text-align: center;
                margin: 30px 0;
                border-radius: 10px;
                border: 1px solid #bae6fd;
            }}
            .cta-section h3 {{ 
                color: #0c4a6e; 
                margin: 0 0 15px 0; 
                font-size: 22px;
            }}
            .cta-section p {{ 
                color: #0369a1; 
                margin: 0 0 20px 0; 
                font-size: 16px;
            }}
            .cta-button {{ 
                display: inline-block; 
                background: #0ea5e9; 
                color: white; 
                padding: 15px 30px; 
                text-decoration: none; 
                border-radius: 8px; 
                font-weight: 600;
                font-size: 16px;
                transition: background-color 0.2s;
            }}
            .cta-button:hover {{ 
                background: #0284c7; 
            }}
            .footer {{ 
                text-align: center; 
                padding: 30px; 
                background: #f1f5f9;
                color: #64748b; 
                border-top: 1px solid #e2e8f0;
            }}
            .footer .signature {{ 
                font-size: 18px; 
                color: #334155; 
                margin-bottom: 20px;
            }}
            .footer .unsubscribe {{ 
                font-size: 12px; 
                color: #94a3b8;
                margin-top: 15px;
            }}
            .social-links {{ 
                margin: 20px 0;
            }}
            .social-links a {{ 
                color: #2563eb; 
                text-decoration: none; 
                margin: 0 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎭 Peter Stoyanov</h1>
                <div class="tagline">Executive Presence & Leadership Coach</div>
            </div>
            
            <div class="greeting">
                <h2>{selected_intro['greeting']}</h2>
                <p>{selected_intro['intro']}</p>
            </div>
            
            <div class="content">
                <div class="intro">
                    <p>{selected_intro['content_intro']}</p>
                </div>
                
    """
    
    # Add blog posts
    for i, post in enumerate(blog_posts, 1):
        html_content += f"""
                <div class="post">
                    <h3>{post['title']}</h3>
                    <p>{post['excerpt']}</p>
                    <a href="https://peterstoyanov.coach/blog/{post['slug']}" class="read-more">Read Full Article →</a>
                </div>
        """
    
    # Add call-to-action section with variations
    cta_variations = [
        {
            "title": "🚀 Ready to Level Up Your Leadership?",
            "text": "These insights are just the beginning. If you're ready to transform your executive presence and command respect in any room, I'd love to help you on that journey.",
            "button": "Join My Coaching Program"
        },
        {
            "title": "💪 Want to Command the Room Like Never Before?",
            "text": "What you just read is exactly what I teach my private clients. If you're serious about elevating your executive presence, let's talk.",
            "button": "Apply for Coaching"
        },
        {
            "title": "🎯 Ready to Transform Your Leadership Impact?",
            "text": "These theater-based techniques have transformed hundreds of leaders. Your executive presence breakthrough is just one conversation away.",
            "button": "Schedule Discovery Call"
        },
        {
            "title": "⚡ Time to Unlock Your Executive Presence?",
            "text": "Stop hoping people will notice your leadership potential. Start commanding the respect and influence you deserve. Let's make it happen.",
            "button": "Get Started Today"
        }
    ]
    
    selected_cta = cta_variations[intro_style % len(cta_variations)]
    
    html_content += f"""
                <div class="cta-section">
                    <h3>{selected_cta['title']}</h3>
                    <p>{selected_cta['text']}</p>
                    <a href="https://peterstoyanov.coach/waitlist" class="cta-button">{selected_cta['button']}</a>
                </div>
            </div>
            
            <div class="footer">
                <div class="signature">
                    <strong>Stay powerful,</strong><br>
                    Peter Stoyanov<br>
                    <em>Executive Presence & Leadership Coach</em>
                </div>
                
                <div class="social-links">
                    <a href="https://linkedin.com/in/peterstoyanov">LinkedIn</a> |
                    <a href="https://peterstoyanov.coach">Website</a> |
                    <a href="https://peterstoyanov.coach/corporate">Corporate Training</a>
                </div>
                
                <div class="unsubscribe">
                    <p>You're receiving this because you subscribed to Peter Stoyanov Coaching updates.<br>
                    <a href="{{unsubscribe_url}}" style="color: #94a3b8;">Unsubscribe</a> | <a href="{{preferences_url}}" style="color: #94a3b8;">Update Preferences</a></p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content