import os
import requests
from typing import Dict, Any, Optional

def add_subscriber_to_mailerlite(email: str, name: str, custom_fields: Optional[Dict[str, Any]] = None):
    """
    Add a subscriber to MailerLite
    
    Args:
        email: Subscriber's email address
        name: Subscriber's full name
        custom_fields: Optional dictionary of custom fields
    
    Returns:
        None
    
    Raises:
        Exception: If the API request fails
    """
    api_key = os.getenv("MAILERLITE_API_KEY")
    if not api_key:
        raise ValueError("MailerLite API key not found in environment variables")
    
    # MailerLite API endpoint for subscribers
    url = "https://api.mailerlite.com/api/v2/subscribers"
    
    # Prepare the data
    data = {
        "email": email,
        "name": name,
        "fields": custom_fields or {}
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