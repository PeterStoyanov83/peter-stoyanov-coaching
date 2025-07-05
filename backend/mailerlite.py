import os
import requests
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
        "Lead Magnet - Theater Secrets": "lead_magnet",
        "Waitlist - Coaching Program": "waitlist",
        "Corporate Prospects": "corporate"
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


def add_lead_magnet_subscriber(email: str, name: str = ""):
    """
    Add subscriber to lead magnet automation sequence
    
    Args:
        email: Subscriber's email
        name: Subscriber's name (optional)
    
    Returns:
        API response or None if failed
    """
    try:
        # Ensure automation groups exist
        group_ids = ensure_automation_groups()
        
        if not group_ids.get("lead_magnet"):
            print("Warning: Lead magnet group not found, adding subscriber without group")
            groups = []
        else:
            groups = [group_ids["lead_magnet"]]
        
        # Add subscriber with lead magnet tags
        custom_fields = {
            "source": "lead_magnet",
            "guide": "5_theater_secrets",
            "signup_date": "2024-01-01",  # You can make this dynamic
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


def add_waitlist_subscriber(email: str, name: str = "", interests: str = ""):
    """
    Add subscriber to coaching program waitlist
    
    Args:
        email: Subscriber's email
        name: Subscriber's name (optional)
        interests: Specific interests or goals (optional)
    
    Returns:
        API response or None if failed
    """
    try:
        # Ensure automation groups exist
        group_ids = ensure_automation_groups()
        
        if not group_ids.get("waitlist"):
            print("Warning: Waitlist group not found, adding subscriber without group")
            groups = []
        else:
            groups = [group_ids["waitlist"]]
        
        # Add subscriber with waitlist tags
        custom_fields = {
            "source": "waitlist",
            "interests": interests,
            "signup_date": "2024-01-01",  # You can make this dynamic
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


def trigger_automation_sequence(email: str, sequence_type: str = "lead_magnet"):
    """
    Trigger an automation sequence for a subscriber
    
    Args:
        email: Subscriber's email
        sequence_type: Type of sequence to trigger (lead_magnet, waitlist, etc.)
    
    Returns:
        Success status
    """
    try:
        if sequence_type == "lead_magnet":
            result = add_lead_magnet_subscriber(email)
        elif sequence_type == "waitlist":
            result = add_waitlist_subscriber(email)
        else:
            print(f"Unknown sequence type: {sequence_type}")
            return False
            
        return result is not None
        
    except Exception as e:
        print(f"Error triggering automation sequence: {e}")
        return False