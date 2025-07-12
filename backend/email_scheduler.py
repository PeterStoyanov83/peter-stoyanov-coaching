"""
Email Scheduler Service for Automated Email Sequences
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import get_db_url
from models import ScheduledEmail, SequenceEnrollment, SequenceEmail, EmailSubscriber
from sequence_automation import get_emails_to_send, mark_email_as_sent, get_failed_emails_for_retry
from sendgrid_service import create_and_send_newsletter, send_individual_email
from email_sequences import get_sequence_by_type_and_language

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
engine = create_engine(get_db_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class EmailScheduler:
    """Service for scheduling and sending automated emails"""
    
    def __init__(self, check_interval: int = 300):  # 5 minutes
        self.check_interval = check_interval
        self.is_running = False
        
    async def start(self):
        """Start the scheduler service"""
        self.is_running = True
        logger.info("Email scheduler started")
        
        while self.is_running:
            try:
                self.process_scheduled_emails()
                self.retry_failed_emails()
                await asyncio.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                await asyncio.sleep(60)  # Wait before retrying
    
    def stop(self):
        """Stop the scheduler service"""
        self.is_running = False
        logger.info("Email scheduler stopped")
    
    def process_scheduled_emails(self):
        """Process emails that are ready to be sent"""
        db = SessionLocal()
        try:
            # Get emails ready to send
            emails_to_send = get_emails_to_send(db, limit=50)
            
            if not emails_to_send:
                logger.debug("No emails to send")
                return
            
            logger.info(f"Processing {len(emails_to_send)} scheduled emails")
            
            for scheduled_email in emails_to_send:
                try:
                    self.send_scheduled_email(db, scheduled_email)
                except Exception as e:
                    logger.error(f"Error sending email {scheduled_email.id}: {e}")
                    # Mark as failed
                    mark_email_as_sent(
                        db, scheduled_email, 
                        error_message=str(e)
                    )
        
        finally:
            db.close()
    
    def send_scheduled_email(self, db: Session, scheduled_email: ScheduledEmail):
        """Send a single scheduled email"""
        try:
            # Get enrollment and subscriber info
            enrollment = db.query(SequenceEnrollment).get(scheduled_email.enrollment_id)
            if not enrollment or enrollment.status != "active":
                logger.warning(f"Skipping email {scheduled_email.id} - enrollment not active")
                return
            
            subscriber = db.query(EmailSubscriber).get(enrollment.subscriber_id)
            if not subscriber or not subscriber.is_active:
                logger.warning(f"Skipping email {scheduled_email.id} - subscriber not active")
                return
            
            # Get email content
            sequence_email = db.query(SequenceEmail).get(scheduled_email.email_id)
            if not sequence_email:
                logger.error(f"Email content not found for scheduled email {scheduled_email.id}")
                return
            
            # Personalize content
            personalized_content = self.personalize_email_content(
                sequence_email.content, 
                subscriber.name or "Friend",
                subscriber.custom_fields or {}
            )
            
            # Send individual email via Mailgun
            result = send_individual_email(
                to_email=subscriber.email,
                subject=sequence_email.subject,
                content=personalized_content,
                from_name="Peter Stoyanov"
            )
            
            if result.get("success"):
                message_id = result.get("message_id", result.get("campaign_id", ""))
                mark_email_as_sent(db, scheduled_email, campaign_id=str(message_id))
                logger.info(f"Email sent successfully: {scheduled_email.id}")
            else:
                error_msg = result.get("error", "Unknown error")
                mark_email_as_sent(db, scheduled_email, error_message=error_msg)
                logger.error(f"Failed to send email {scheduled_email.id}: {error_msg}")
                
        except Exception as e:
            logger.error(f"Error sending scheduled email {scheduled_email.id}: {e}")
            mark_email_as_sent(db, scheduled_email, error_message=str(e))
    
    def personalize_email_content(self, content: str, name: str, custom_fields: dict) -> str:
        """Personalize email content with subscriber data"""
        # Replace name placeholder
        personalized = content.replace("{{name}}", name)
        
        # Replace custom field placeholders
        for field, value in custom_fields.items():
            placeholder = f"{{{{{field}}}}}"
            personalized = personalized.replace(placeholder, str(value))
        
        return personalized
    
    def retry_failed_emails(self):
        """Retry failed emails with enhanced exponential backoff and categorized error handling"""
        db = SessionLocal()
        try:
            # Get failed emails with different retry configurations based on error type
            failed_emails = get_failed_emails_for_retry(db, max_retries=5)
            
            if not failed_emails:
                logger.debug("No failed emails to retry")
                return
            
            logger.info(f"Retrying {len(failed_emails)} failed emails")
            
            for failed_email in failed_emails:
                try:
                    # Enhanced exponential backoff with jitter
                    retry_delay = self.calculate_retry_delay(failed_email)
                    time_since_last_attempt = (datetime.utcnow() - failed_email.updated_at).total_seconds()
                    
                    if time_since_last_attempt >= retry_delay:
                        # Check if error is retryable
                        if not self.is_retryable_error(failed_email.error_message):
                            logger.warning(f"Marking email {failed_email.id} as permanently failed - non-retryable error")
                            failed_email.status = "permanently_failed"
                            failed_email.updated_at = datetime.utcnow()
                            db.commit()
                            continue
                        
                        # Reset status to scheduled for retry
                        failed_email.status = "scheduled"
                        failed_email.updated_at = datetime.utcnow()
                        db.commit()
                        
                        logger.info(f"Retrying email {failed_email.id} (attempt {failed_email.retry_count + 1})")
                        self.send_scheduled_email(db, failed_email)
                        
                    else:
                        retry_in = int(retry_delay - time_since_last_attempt)
                        logger.debug(f"Email {failed_email.id} not ready for retry - waiting {retry_in}s")
                        
                except Exception as e:
                    logger.error(f"Error retrying failed email {failed_email.id}: {e}")
                    # Mark as permanently failed if retry logic itself fails
                    failed_email.status = "permanently_failed"
                    failed_email.error_message = f"Retry failed: {str(e)}"
                    failed_email.updated_at = datetime.utcnow()
                    db.commit()
        
        finally:
            db.close()
    
    def calculate_retry_delay(self, failed_email: ScheduledEmail) -> int:
        """Calculate retry delay with exponential backoff and jitter"""
        import random
        
        # Base delay with exponential backoff: 2^retry_count minutes
        base_delay = (2 ** failed_email.retry_count) * 60
        
        # Add jitter to prevent thundering herd (±25% randomization)
        jitter = random.uniform(0.75, 1.25)
        
        # Cap maximum delay at 4 hours
        max_delay = 4 * 60 * 60  # 4 hours in seconds
        
        return min(int(base_delay * jitter), max_delay)
    
    def is_retryable_error(self, error_message: str) -> bool:
        """Determine if an error is retryable based on error message"""
        if not error_message:
            return True
        
        error_lower = error_message.lower()
        
        # Non-retryable errors (permanent failures)
        non_retryable_patterns = [
            "invalid email address",
            "invalid api key",
            "unauthorized", 
            "forbidden",
            "email address is invalid",
            "malformed email",
            "subscriber not found",
            "hard bounce",
            "blacklisted",
            "suppressed",
            "unsubscribed",
            "invalid recipient"
        ]
        
        for pattern in non_retryable_patterns:
            if pattern in error_lower:
                return False
        
        # Retryable errors (temporary failures)
        retryable_patterns = [
            "rate limit",
            "timeout",
            "connection",
            "network",
            "temporary",
            "service unavailable",
            "internal server error",
            "bad gateway",
            "gateway timeout",
            "too many requests"
        ]
        
        for pattern in retryable_patterns:
            if pattern in error_lower:
                return True
        
        # Default to retryable for unknown errors
        return True


class EmailSchedulerService:
    """Singleton service for managing the email scheduler"""
    
    _instance = None
    _scheduler = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmailSchedulerService, cls).__new__(cls)
        return cls._instance
    
    def start_scheduler(self, check_interval: int = 300):
        """Start the email scheduler"""
        if self._scheduler is None:
            self._scheduler = EmailScheduler(check_interval)
            asyncio.create_task(self._scheduler.start())
            logger.info("Email scheduler service started")
    
    def stop_scheduler(self):
        """Stop the email scheduler"""
        if self._scheduler:
            self._scheduler.stop()
            self._scheduler = None
            logger.info("Email scheduler service stopped")
    
    def is_running(self):
        """Check if scheduler is running"""
        return self._scheduler is not None and self._scheduler.is_running


# Manual email processing function for testing
async def process_emails_once():
    """Process emails once (for testing or manual triggers)"""
    scheduler = EmailScheduler()
    scheduler.process_scheduled_emails()
    scheduler.retry_failed_emails()


# CLI interface for running the scheduler
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Email Scheduler Service")
    parser.add_argument("--interval", type=int, default=300, help="Check interval in seconds")
    parser.add_argument("--once", action="store_true", help="Process emails once and exit")
    
    args = parser.parse_args()
    
    if args.once:
        asyncio.run(process_emails_once())
    else:
        scheduler = EmailScheduler(args.interval)
        try:
            asyncio.run(scheduler.start())
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")