"""
Mailgun Webhook Handler for Email Analytics Events
Handles: delivered, opened, clicked, bounced, complained, unsubscribed
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


def verify_mailgun_signature(token: str, timestamp: str, signature: str, webhook_secret: str) -> bool:
    """Verify Mailgun webhook signature for security"""
    if not webhook_secret:
        logger.warning("No Mailgun webhook secret configured - skipping signature verification")
        return True
    
    # Create expected signature using Mailgun's format
    message = f"{timestamp}{token}"
    expected_signature = hmac.new(
        webhook_secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, signature)


def get_scheduled_email_by_message_id(db: Session, message_id: str) -> ScheduledEmail:
    """Find scheduled email by Mailgun message ID"""
    # Mailgun message IDs are stored in the mailerlite_campaign_id field for compatibility
    return db.query(ScheduledEmail).filter(
        ScheduledEmail.mailerlite_campaign_id == message_id
    ).first()


def handle_mailgun_delivered(event_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
    """Handle email delivered event from Mailgun"""
    try:
        message_id = event_data.get('message', {}).get('headers', {}).get('message-id', '')
        recipient_email = event_data.get('recipient', '')
        timestamp = datetime.fromtimestamp(event_data.get('timestamp', 0))
        
        logger.info(f"📧 Mailgun delivery event: {recipient_email} - {message_id}")
        
        # Find the scheduled email
        scheduled_email = get_scheduled_email_by_message_id(db, message_id)
        
        if not scheduled_email:
            logger.warning(f"No scheduled email found for message ID: {message_id}")
            return {"status": "ignored", "reason": "email_not_found"}
        
        # Update email analytics
        analytics = db.query(EmailAnalytics).filter(
            EmailAnalytics.scheduled_email_id == scheduled_email.id
        ).first()
        
        if not analytics:
            analytics = EmailAnalytics(
                scheduled_email_id=scheduled_email.id,
                campaign_id=message_id,
                delivered_at=timestamp
            )
            db.add(analytics)
        else:
            analytics.delivered_at = timestamp
        
        db.commit()
        logger.info(f"✅ Marked email as delivered: {scheduled_email.id}")
        
        return {"status": "success", "action": "delivered"}
        
    except Exception as e:
        logger.error(f"Error handling Mailgun delivered event: {e}")
        db.rollback()
        return {"status": "error", "message": str(e)}


def handle_mailgun_opened(event_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
    """Handle email opened event from Mailgun"""
    try:
        message_id = event_data.get('message', {}).get('headers', {}).get('message-id', '')
        recipient_email = event_data.get('recipient', '')
        timestamp = datetime.fromtimestamp(event_data.get('timestamp', 0))
        
        logger.info(f"👁️ Mailgun open event: {recipient_email} - {message_id}")
        
        # Find the scheduled email
        scheduled_email = get_scheduled_email_by_message_id(db, message_id)
        
        if not scheduled_email:
            logger.warning(f"No scheduled email found for message ID: {message_id}")
            return {"status": "ignored", "reason": "email_not_found"}
        
        # Update email analytics
        analytics = db.query(EmailAnalytics).filter(
            EmailAnalytics.scheduled_email_id == scheduled_email.id
        ).first()
        
        if not analytics:
            analytics = EmailAnalytics(
                scheduled_email_id=scheduled_email.id,
                campaign_id=message_id,
                opened_at=timestamp
            )
            db.add(analytics)
        else:
            analytics.opened_at = timestamp
        
        db.commit()
        logger.info(f"✅ Marked email as opened: {scheduled_email.id}")
        
        return {"status": "success", "action": "opened"}
        
    except Exception as e:
        logger.error(f"Error handling Mailgun opened event: {e}")
        db.rollback()
        return {"status": "error", "message": str(e)}


def handle_mailgun_clicked(event_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
    """Handle email clicked event from Mailgun"""
    try:
        message_id = event_data.get('message', {}).get('headers', {}).get('message-id', '')
        recipient_email = event_data.get('recipient', '')
        timestamp = datetime.fromtimestamp(event_data.get('timestamp', 0))
        url = event_data.get('url', '')
        
        logger.info(f"🔗 Mailgun click event: {recipient_email} - {url}")
        
        # Find the scheduled email
        scheduled_email = get_scheduled_email_by_message_id(db, message_id)
        
        if not scheduled_email:
            logger.warning(f"No scheduled email found for message ID: {message_id}")
            return {"status": "ignored", "reason": "email_not_found"}
        
        # Update email analytics
        analytics = db.query(EmailAnalytics).filter(
            EmailAnalytics.scheduled_email_id == scheduled_email.id
        ).first()
        
        if not analytics:
            analytics = EmailAnalytics(
                scheduled_email_id=scheduled_email.id,
                campaign_id=message_id,
                clicked_at=timestamp
            )
            db.add(analytics)
        else:
            analytics.clicked_at = timestamp
        
        db.commit()
        logger.info(f"✅ Marked email as clicked: {scheduled_email.id}")
        
        return {"status": "success", "action": "clicked", "url": url}
        
    except Exception as e:
        logger.error(f"Error handling Mailgun clicked event: {e}")
        db.rollback()
        return {"status": "error", "message": str(e)}


def handle_mailgun_bounced(event_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
    """Handle email bounced event from Mailgun"""
    try:
        message_id = event_data.get('message', {}).get('headers', {}).get('message-id', '')
        recipient_email = event_data.get('recipient', '')
        timestamp = datetime.fromtimestamp(event_data.get('timestamp', 0))
        reason = event_data.get('reason', '')
        
        logger.info(f"⚠️ Mailgun bounce event: {recipient_email} - {reason}")
        
        # Find the scheduled email
        scheduled_email = get_scheduled_email_by_message_id(db, message_id)
        
        if scheduled_email:
            # Update email analytics
            analytics = db.query(EmailAnalytics).filter(
                EmailAnalytics.scheduled_email_id == scheduled_email.id
            ).first()
            
            if not analytics:
                analytics = EmailAnalytics(
                    scheduled_email_id=scheduled_email.id,
                    campaign_id=message_id,
                    bounced_at=timestamp
                )
                db.add(analytics)
            else:
                analytics.bounced_at = timestamp
            
            db.commit()
        
        # Mark subscriber as bounced
        subscriber = db.query(EmailSubscriber).filter(
            EmailSubscriber.email == recipient_email
        ).first()
        
        if subscriber:
            subscriber.is_active = False
            db.commit()
            logger.info(f"🚫 Marked subscriber as inactive due to bounce: {recipient_email}")
        
        return {"status": "success", "action": "bounced", "reason": reason}
        
    except Exception as e:
        logger.error(f"Error handling Mailgun bounced event: {e}")
        db.rollback()
        return {"status": "error", "message": str(e)}


def handle_mailgun_complained(event_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
    """Handle email complained (spam) event from Mailgun"""
    try:
        recipient_email = event_data.get('recipient', '')
        timestamp = datetime.fromtimestamp(event_data.get('timestamp', 0))
        
        logger.info(f"🚨 Mailgun complaint event: {recipient_email}")
        
        # Mark subscriber as inactive
        subscriber = db.query(EmailSubscriber).filter(
            EmailSubscriber.email == recipient_email
        ).first()
        
        if subscriber:
            subscriber.is_active = False
            db.commit()
            logger.info(f"🚫 Marked subscriber as inactive due to complaint: {recipient_email}")
        
        return {"status": "success", "action": "complained"}
        
    except Exception as e:
        logger.error(f"Error handling Mailgun complained event: {e}")
        db.rollback()
        return {"status": "error", "message": str(e)}


def handle_mailgun_unsubscribed(event_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
    """Handle email unsubscribed event from Mailgun"""
    try:
        recipient_email = event_data.get('recipient', '')
        timestamp = datetime.fromtimestamp(event_data.get('timestamp', 0))
        
        logger.info(f"📤 Mailgun unsubscribe event: {recipient_email}")
        
        # Mark subscriber as inactive
        subscriber = db.query(EmailSubscriber).filter(
            EmailSubscriber.email == recipient_email
        ).first()
        
        if subscriber:
            subscriber.is_active = False
            db.commit()
            logger.info(f"🚫 Marked subscriber as inactive due to unsubscribe: {recipient_email}")
        
        return {"status": "success", "action": "unsubscribed"}
        
    except Exception as e:
        logger.error(f"Error handling Mailgun unsubscribed event: {e}")
        db.rollback()
        return {"status": "error", "message": str(e)}


def handle_mailgun_temporary_fail(event_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
    """Handle temporary failure event from Mailgun"""
    try:
        message_id = event_data.get('message', {}).get('headers', {}).get('message-id', '')
        recipient_email = event_data.get('recipient', '')
        timestamp = datetime.fromtimestamp(event_data.get('timestamp', 0))
        reason = event_data.get('reason', '')
        
        logger.info(f"⚠️ Mailgun temporary failure: {recipient_email} - {reason}")
        
        # Find the scheduled email and update retry info
        scheduled_email = get_scheduled_email_by_message_id(db, message_id)
        
        if scheduled_email:
            # Mark as failed but retryable
            scheduled_email.status = "failed"
            scheduled_email.error_message = f"Temporary failure: {reason}"
            scheduled_email.retry_count = scheduled_email.retry_count + 1 if scheduled_email.retry_count else 1
            
            db.commit()
            logger.info(f"🔄 Marked email for retry due to temporary failure: {scheduled_email.id}")
        
        return {"status": "success", "action": "temporary_fail", "reason": reason}
        
    except Exception as e:
        logger.error(f"Error handling Mailgun temporary failure event: {e}")
        db.rollback()
        return {"status": "error", "message": str(e)}


def handle_mailgun_permanent_fail(event_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
    """Handle permanent failure event from Mailgun"""
    try:
        message_id = event_data.get('message', {}).get('headers', {}).get('message-id', '')
        recipient_email = event_data.get('recipient', '')
        timestamp = datetime.fromtimestamp(event_data.get('timestamp', 0))
        reason = event_data.get('reason', '')
        
        logger.info(f"❌ Mailgun permanent failure: {recipient_email} - {reason}")
        
        # Find the scheduled email
        scheduled_email = get_scheduled_email_by_message_id(db, message_id)
        
        if scheduled_email:
            # Mark as permanently failed
            scheduled_email.status = "permanently_failed"
            scheduled_email.error_message = f"Permanent failure: {reason}"
            db.commit()
        
        # Mark subscriber as inactive for certain permanent failures
        if 'does not exist' in reason.lower() or 'invalid' in reason.lower():
            subscriber = db.query(EmailSubscriber).filter(
                EmailSubscriber.email == recipient_email
            ).first()
            
            if subscriber:
                subscriber.is_active = False
                db.commit()
                logger.info(f"🚫 Marked subscriber as inactive due to permanent failure: {recipient_email}")
        
        return {"status": "success", "action": "permanent_fail", "reason": reason}
        
    except Exception as e:
        logger.error(f"Error handling Mailgun permanent failure event: {e}")
        db.rollback()
        return {"status": "error", "message": str(e)}


def process_mailgun_webhook(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process Mailgun webhook event"""
    db = SessionLocal()
    try:
        event_type = event_data.get('event')
        
        if event_type == 'delivered':
            return handle_mailgun_delivered(event_data, db)
        elif event_type == 'opened':
            return handle_mailgun_opened(event_data, db)
        elif event_type == 'clicked':
            return handle_mailgun_clicked(event_data, db)
        elif event_type == 'bounced':
            return handle_mailgun_bounced(event_data, db)
        elif event_type == 'complained':
            return handle_mailgun_complained(event_data, db)
        elif event_type == 'unsubscribed':
            return handle_mailgun_unsubscribed(event_data, db)
        elif event_type == 'temporary_fail':
            return handle_mailgun_temporary_fail(event_data, db)
        elif event_type == 'permanent_fail':
            return handle_mailgun_permanent_fail(event_data, db)
        else:
            logger.warning(f"Unknown Mailgun event type: {event_type}")
            return {"status": "ignored", "reason": "unknown_event_type"}
            
    finally:
        db.close()