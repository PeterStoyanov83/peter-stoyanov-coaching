"""
MailerLite Webhook Handler for Email Analytics Events
"""

import hashlib
import hmac
import logging
from datetime import datetime
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from typing import Dict, Any

from models import EmailAnalytics, ScheduledEmail, EmailSubscriber
from database import get_db_url
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup for webhook handlers
engine = create_engine(get_db_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def verify_webhook_signature(payload: bytes, signature: str, webhook_secret: str) -> bool:
    """Verify MailerLite webhook signature for security"""
    if not webhook_secret:
        logger.warning("No webhook secret configured - skipping signature verification")
        return True
    
    # Create expected signature
    expected_signature = hmac.new(
        webhook_secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    # Compare signatures
    return hmac.compare_digest(f"sha256={expected_signature}", signature)


def get_scheduled_email_by_campaign_id(db: Session, campaign_id: str) -> ScheduledEmail:
    """Find scheduled email by MailerLite campaign ID"""
    return db.query(ScheduledEmail).filter(
        ScheduledEmail.mailerlite_campaign_id == campaign_id
    ).first()


def get_or_create_analytics(db: Session, scheduled_email_id: int) -> EmailAnalytics:
    """Get existing analytics record or create new one"""
    analytics = db.query(EmailAnalytics).filter(
        EmailAnalytics.scheduled_email_id == scheduled_email_id
    ).first()
    
    if not analytics:
        analytics = EmailAnalytics(scheduled_email_id=scheduled_email_id)
        db.add(analytics)
        db.commit()
        db.refresh(analytics)
    
    return analytics


def handle_email_opened(db: Session, event_data: Dict[str, Any]) -> Dict[str, str]:
    """Handle email opened event"""
    try:
        campaign_id = event_data.get('campaign', {}).get('id')
        subscriber_email = event_data.get('subscriber', {}).get('email')
        
        if not campaign_id:
            return {"status": "ignored", "reason": "No campaign ID provided"}
        
        # Find the scheduled email
        scheduled_email = get_scheduled_email_by_campaign_id(db, str(campaign_id))
        if not scheduled_email:
            return {"status": "ignored", "reason": f"Scheduled email not found for campaign {campaign_id}"}
        
        # Get or create analytics record
        analytics = get_or_create_analytics(db, scheduled_email.id)
        
        # Update analytics
        if not analytics.opened_at:
            analytics.opened_at = datetime.utcnow()
        analytics.open_count += 1
        analytics.updated_at = datetime.utcnow()
        
        db.commit()
        
        logger.info(f"Email opened: Campaign {campaign_id}, Subscriber {subscriber_email}")
        return {"status": "processed", "event": "email_opened"}
        
    except Exception as e:
        logger.error(f"Error handling email opened event: {e}")
        return {"status": "error", "error": str(e)}


def handle_email_clicked(db: Session, event_data: Dict[str, Any]) -> Dict[str, str]:
    """Handle email clicked event"""
    try:
        campaign_id = event_data.get('campaign', {}).get('id')
        subscriber_email = event_data.get('subscriber', {}).get('email')
        click_url = event_data.get('click', {}).get('url')
        
        if not campaign_id:
            return {"status": "ignored", "reason": "No campaign ID provided"}
        
        # Find the scheduled email
        scheduled_email = get_scheduled_email_by_campaign_id(db, str(campaign_id))
        if not scheduled_email:
            return {"status": "ignored", "reason": f"Scheduled email not found for campaign {campaign_id}"}
        
        # Get or create analytics record
        analytics = get_or_create_analytics(db, scheduled_email.id)
        
        # Update analytics
        if not analytics.clicked_at:
            analytics.clicked_at = datetime.utcnow()
        analytics.click_count += 1
        analytics.updated_at = datetime.utcnow()
        
        db.commit()
        
        logger.info(f"Email clicked: Campaign {campaign_id}, Subscriber {subscriber_email}, URL {click_url}")
        return {"status": "processed", "event": "email_clicked"}
        
    except Exception as e:
        logger.error(f"Error handling email clicked event: {e}")
        return {"status": "error", "error": str(e)}


def handle_email_bounced(db: Session, event_data: Dict[str, Any]) -> Dict[str, str]:
    """Handle email bounced event"""
    try:
        campaign_id = event_data.get('campaign', {}).get('id')
        subscriber_email = event_data.get('subscriber', {}).get('email')
        bounce_type = event_data.get('bounce', {}).get('type')
        
        if not campaign_id:
            return {"status": "ignored", "reason": "No campaign ID provided"}
        
        # Find the scheduled email
        scheduled_email = get_scheduled_email_by_campaign_id(db, str(campaign_id))
        if not scheduled_email:
            return {"status": "ignored", "reason": f"Scheduled email not found for campaign {campaign_id}"}
        
        # Get or create analytics record
        analytics = get_or_create_analytics(db, scheduled_email.id)
        
        # Update analytics
        analytics.bounced_at = datetime.utcnow()
        analytics.updated_at = datetime.utcnow()
        
        # If hard bounce, deactivate subscriber
        if bounce_type == 'hard':
            subscriber = db.query(EmailSubscriber).filter(
                EmailSubscriber.email == subscriber_email
            ).first()
            if subscriber:
                subscriber.is_active = False
                subscriber.updated_at = datetime.utcnow()
        
        db.commit()
        
        logger.info(f"Email bounced: Campaign {campaign_id}, Subscriber {subscriber_email}, Type {bounce_type}")
        return {"status": "processed", "event": "email_bounced"}
        
    except Exception as e:
        logger.error(f"Error handling email bounced event: {e}")
        return {"status": "error", "error": str(e)}


def handle_subscriber_unsubscribed(db: Session, event_data: Dict[str, Any]) -> Dict[str, str]:
    """Handle subscriber unsubscribed event"""
    try:
        campaign_id = event_data.get('campaign', {}).get('id')
        subscriber_email = event_data.get('subscriber', {}).get('email')
        
        # Find and deactivate subscriber
        subscriber = db.query(EmailSubscriber).filter(
            EmailSubscriber.email == subscriber_email
        ).first()
        
        if subscriber:
            subscriber.is_active = False
            subscriber.updated_at = datetime.utcnow()
        
        # Update analytics if campaign ID is available
        if campaign_id:
            scheduled_email = get_scheduled_email_by_campaign_id(db, str(campaign_id))
            if scheduled_email:
                analytics = get_or_create_analytics(db, scheduled_email.id)
                analytics.unsubscribed_at = datetime.utcnow()
                analytics.updated_at = datetime.utcnow()
        
        db.commit()
        
        logger.info(f"Subscriber unsubscribed: {subscriber_email}")
        return {"status": "processed", "event": "subscriber_unsubscribed"}
        
    except Exception as e:
        logger.error(f"Error handling unsubscribe event: {e}")
        return {"status": "error", "error": str(e)}


def handle_conversion_event(db: Session, event_data: Dict[str, Any]) -> Dict[str, str]:
    """Handle conversion/goal achievement event"""
    try:
        campaign_id = event_data.get('campaign', {}).get('id')
        subscriber_email = event_data.get('subscriber', {}).get('email')
        conversion_value = event_data.get('conversion', {}).get('value', 0)
        
        if not campaign_id:
            return {"status": "ignored", "reason": "No campaign ID provided"}
        
        # Find the scheduled email
        scheduled_email = get_scheduled_email_by_campaign_id(db, str(campaign_id))
        if not scheduled_email:
            return {"status": "ignored", "reason": f"Scheduled email not found for campaign {campaign_id}"}
        
        # Get or create analytics record
        analytics = get_or_create_analytics(db, scheduled_email.id)
        
        # Update analytics
        analytics.converted_at = datetime.utcnow()
        analytics.updated_at = datetime.utcnow()
        
        db.commit()
        
        logger.info(f"Conversion tracked: Campaign {campaign_id}, Subscriber {subscriber_email}, Value {conversion_value}")
        return {"status": "processed", "event": "conversion"}
        
    except Exception as e:
        logger.error(f"Error handling conversion event: {e}")
        return {"status": "error", "error": str(e)}


# Event handler mapping
WEBHOOK_HANDLERS = {
    'campaign.sent': lambda db, data: {"status": "ignored", "reason": "Campaign sent events not processed"},
    'subscriber.opened': handle_email_opened,
    'subscriber.clicked': handle_email_clicked,
    'subscriber.bounced': handle_email_bounced,
    'subscriber.unsubscribed': handle_subscriber_unsubscribed,
    'subscriber.complained': handle_subscriber_unsubscribed,  # Treat complaints as unsubscribes
    'conversion': handle_conversion_event,
}


def process_webhook_event(event_type: str, event_data: Dict[str, Any]) -> Dict[str, str]:
    """Process incoming webhook event"""
    db = SessionLocal()
    try:
        handler = WEBHOOK_HANDLERS.get(event_type)
        if not handler:
            logger.warning(f"No handler for event type: {event_type}")
            return {"status": "ignored", "reason": f"No handler for event type {event_type}"}
        
        return handler(db, event_data)
        
    finally:
        db.close()