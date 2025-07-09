"""
Email Sequence Automation Database Operations
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import uuid

from models import (
    EmailSubscriber, EmailSequence, SequenceEmail, SequenceEnrollment, 
    ScheduledEmail, EmailAnalytics
)
from email_sequences import (
    get_sequence_by_type_and_language, get_sequence_metadata_by_language,
    get_available_languages
)


def create_or_get_subscriber(db: Session, email: str, name: str = None, source: str = "lead_magnet", 
                           language: str = "en", custom_fields: Dict = None) -> EmailSubscriber:
    """Create or get existing subscriber"""
    subscriber = db.query(EmailSubscriber).filter(EmailSubscriber.email == email).first()
    
    if not subscriber:
        subscriber = EmailSubscriber(
            email=email,
            name=name,
            source=source,
            language=language,
            custom_fields=custom_fields or {}
        )
        db.add(subscriber)
        db.commit()
        db.refresh(subscriber)
    else:
        # Update existing subscriber if needed
        if name and not subscriber.name:
            subscriber.name = name
        if custom_fields:
            subscriber.custom_fields = {**(subscriber.custom_fields or {}), **custom_fields}
        subscriber.updated_at = datetime.utcnow()
        db.commit()
    
    return subscriber


def create_or_get_sequence(db: Session, sequence_type: str, language: str = "en") -> EmailSequence:
    """Create or get existing email sequence"""
    sequence = db.query(EmailSequence).filter(
        and_(
            EmailSequence.sequence_type == sequence_type,
            EmailSequence.language == language
        )
    ).first()
    
    if not sequence:
        # Get sequence metadata
        metadata = get_sequence_metadata_by_language(language)
        sequence_info = metadata.get(sequence_type, {})
        
        sequence = EmailSequence(
            name=sequence_info.get('name', f'{sequence_type} sequence'),
            sequence_type=sequence_type,
            language=language,
            description=sequence_info.get('description', '')
        )
        db.add(sequence)
        db.commit()
        db.refresh(sequence)
        
        # Create sequence emails
        emails = get_sequence_by_type_and_language(sequence_type, language)
        for index, email_data in enumerate(emails):
            sequence_email = SequenceEmail(
                sequence_id=sequence.id,
                email_index=index,
                subject=email_data['subject'],
                title=email_data['title'],
                content=email_data['content'],
                cta=email_data['cta'],
                delay_days=email_data['delay_days'],
                week_number=email_data.get('week', index + 1)
            )
            db.add(sequence_email)
        
        db.commit()
    
    return sequence


def enroll_subscriber_in_sequence(db: Session, subscriber: EmailSubscriber, 
                                 sequence_type: str, language: str = None) -> SequenceEnrollment:
    """Enroll subscriber in an email sequence"""
    if language is None:
        language = subscriber.language
    
    # Check if already enrolled
    sequence = create_or_get_sequence(db, sequence_type, language)
    existing_enrollment = db.query(SequenceEnrollment).filter(
        and_(
            SequenceEnrollment.subscriber_id == subscriber.id,
            SequenceEnrollment.sequence_id == sequence.id,
            SequenceEnrollment.status == "active"
        )
    ).first()
    
    if existing_enrollment:
        return existing_enrollment
    
    # Create new enrollment
    enrollment = SequenceEnrollment(
        subscriber_id=subscriber.id,
        sequence_id=sequence.id,
        enrollment_date=datetime.utcnow(),
        current_email_index=0,
        status="active"
    )
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    
    # Schedule all emails for this enrollment
    schedule_sequence_emails(db, enrollment)
    
    return enrollment


def schedule_sequence_emails(db: Session, enrollment: SequenceEnrollment):
    """Schedule all emails for a sequence enrollment"""
    # Get sequence emails
    sequence_emails = db.query(SequenceEmail).filter(
        SequenceEmail.sequence_id == enrollment.sequence_id
    ).order_by(SequenceEmail.email_index).all()
    
    base_date = enrollment.enrollment_date
    
    for email in sequence_emails:
        # Calculate when this email should be sent
        send_date = base_date + timedelta(days=email.delay_days)
        
        # Create scheduled email
        scheduled_email = ScheduledEmail(
            enrollment_id=enrollment.id,
            email_id=email.id,
            scheduled_for=send_date,
            status="scheduled"
        )
        db.add(scheduled_email)
    
    db.commit()


def get_emails_to_send(db: Session, limit: int = 100) -> List[ScheduledEmail]:
    """Get emails that are ready to be sent"""
    now = datetime.utcnow()
    
    emails = db.query(ScheduledEmail).filter(
        and_(
            ScheduledEmail.status == "scheduled",
            ScheduledEmail.scheduled_for <= now
        )
    ).join(SequenceEnrollment).filter(
        SequenceEnrollment.status == "active"
    ).limit(limit).all()
    
    return emails


def mark_email_as_sent(db: Session, scheduled_email: ScheduledEmail, 
                      campaign_id: str = None, error_message: str = None):
    """Mark an email as sent or failed"""
    scheduled_email.sent_at = datetime.utcnow()
    scheduled_email.mailerlite_campaign_id = campaign_id
    scheduled_email.updated_at = datetime.utcnow()
    
    if error_message:
        scheduled_email.status = "failed"
        scheduled_email.error_message = error_message
        scheduled_email.retry_count += 1
    else:
        scheduled_email.status = "sent"
        
        # Update enrollment progress
        enrollment = db.query(SequenceEnrollment).get(scheduled_email.enrollment_id)
        if enrollment:
            enrollment.current_email_index += 1
            enrollment.updated_at = datetime.utcnow()
            
            # Check if sequence is complete
            total_emails = db.query(func.count(SequenceEmail.id)).filter(
                SequenceEmail.sequence_id == enrollment.sequence_id
            ).scalar()
            
            if enrollment.current_email_index >= total_emails:
                enrollment.status = "completed"
                enrollment.completion_date = datetime.utcnow()
    
    db.commit()


def get_failed_emails_for_retry(db: Session, max_retries: int = 5) -> List[ScheduledEmail]:
    """Get failed emails that can be retried (excludes permanently failed)"""
    failed_emails = db.query(ScheduledEmail).filter(
        and_(
            ScheduledEmail.status == "failed",
            ScheduledEmail.retry_count < max_retries
        )
    ).join(SequenceEnrollment).filter(
        SequenceEnrollment.status == "active"
    ).all()
    
    return failed_emails


def get_permanently_failed_emails(db: Session, days: int = 30) -> List[ScheduledEmail]:
    """Get permanently failed emails for reporting"""
    from datetime import datetime, timedelta
    
    since_date = datetime.utcnow() - timedelta(days=days)
    
    failed_emails = db.query(ScheduledEmail).filter(
        and_(
            ScheduledEmail.status == "permanently_failed",
            ScheduledEmail.updated_at >= since_date
        )
    ).all()
    
    return failed_emails


def reset_failed_email_for_retry(db: Session, scheduled_email_id: int) -> bool:
    """Reset a failed/permanently failed email for manual retry"""
    scheduled_email = db.query(ScheduledEmail).get(scheduled_email_id)
    
    if not scheduled_email:
        return False
    
    if scheduled_email.status in ["failed", "permanently_failed"]:
        scheduled_email.status = "scheduled"
        scheduled_email.retry_count = 0
        scheduled_email.error_message = None
        scheduled_email.updated_at = datetime.utcnow()
        db.commit()
        return True
    
    return False


def get_subscriber_enrollments(db: Session, subscriber_id: int) -> List[SequenceEnrollment]:
    """Get all enrollments for a subscriber"""
    enrollments = db.query(SequenceEnrollment).filter(
        SequenceEnrollment.subscriber_id == subscriber_id
    ).all()
    
    return enrollments


def get_sequence_analytics(db: Session, sequence_id: int = None, 
                         language: str = None, days: int = 30) -> Dict[str, Any]:
    """Get analytics for email sequences"""
    base_query = db.query(ScheduledEmail).join(SequenceEnrollment).join(EmailSequence)
    
    # Apply filters
    if sequence_id:
        base_query = base_query.filter(EmailSequence.id == sequence_id)
    if language:
        base_query = base_query.filter(EmailSequence.language == language)
    
    # Date filter
    since_date = datetime.utcnow() - timedelta(days=days)
    base_query = base_query.filter(ScheduledEmail.created_at >= since_date)
    
    # Get basic metrics
    total_scheduled = base_query.count()
    total_sent = base_query.filter(ScheduledEmail.status == "sent").count()
    total_failed = base_query.filter(ScheduledEmail.status == "failed").count()
    total_permanently_failed = base_query.filter(ScheduledEmail.status == "permanently_failed").count()
    
    # Get analytics data
    analytics_query = db.query(EmailAnalytics).join(ScheduledEmail).join(SequenceEnrollment).join(EmailSequence)
    
    if sequence_id:
        analytics_query = analytics_query.filter(EmailSequence.id == sequence_id)
    if language:
        analytics_query = analytics_query.filter(EmailSequence.language == language)
    
    analytics_query = analytics_query.filter(ScheduledEmail.created_at >= since_date)
    
    total_opens = analytics_query.filter(EmailAnalytics.opened_at.isnot(None)).count()
    total_clicks = analytics_query.filter(EmailAnalytics.clicked_at.isnot(None)).count()
    total_conversions = analytics_query.filter(EmailAnalytics.converted_at.isnot(None)).count()
    
    # Calculate rates
    open_rate = (total_opens / total_sent * 100) if total_sent > 0 else 0
    click_rate = (total_clicks / total_sent * 100) if total_sent > 0 else 0
    conversion_rate = (total_conversions / total_sent * 100) if total_sent > 0 else 0
    
    return {
        "total_scheduled": total_scheduled,
        "total_sent": total_sent,
        "total_failed": total_failed,
        "total_permanently_failed": total_permanently_failed,
        "total_opens": total_opens,
        "total_clicks": total_clicks,
        "total_conversions": total_conversions,
        "open_rate": round(open_rate, 2),
        "click_rate": round(click_rate, 2),
        "conversion_rate": round(conversion_rate, 2),
        "success_rate": round((total_sent / total_scheduled * 100) if total_scheduled > 0 else 0, 2),
        "failure_rate": round(((total_failed + total_permanently_failed) / total_scheduled * 100) if total_scheduled > 0 else 0, 2),
        "period_days": days
    }


def get_subscribers_with_filters(db: Session, language: str = None, 
                               source: str = None, limit: int = 100) -> List[EmailSubscriber]:
    """Get subscribers with filtering options"""
    query = db.query(EmailSubscriber)
    
    if language:
        query = query.filter(EmailSubscriber.language == language)
    if source:
        query = query.filter(EmailSubscriber.source == source)
    
    query = query.filter(EmailSubscriber.is_active == True)
    query = query.order_by(EmailSubscriber.created_at.desc())
    
    return query.limit(limit).all()


def pause_enrollment(db: Session, enrollment_id: int):
    """Pause an active enrollment"""
    enrollment = db.query(SequenceEnrollment).get(enrollment_id)
    if enrollment and enrollment.status == "active":
        enrollment.status = "paused"
        enrollment.updated_at = datetime.utcnow()
        
        # Cancel scheduled emails
        scheduled_emails = db.query(ScheduledEmail).filter(
            and_(
                ScheduledEmail.enrollment_id == enrollment_id,
                ScheduledEmail.status == "scheduled"
            )
        ).all()
        
        for email in scheduled_emails:
            email.status = "cancelled"
            email.updated_at = datetime.utcnow()
        
        db.commit()


def resume_enrollment(db: Session, enrollment_id: int):
    """Resume a paused enrollment"""
    enrollment = db.query(SequenceEnrollment).get(enrollment_id)
    if enrollment and enrollment.status == "paused":
        enrollment.status = "active"
        enrollment.updated_at = datetime.utcnow()
        
        # Reschedule remaining emails
        schedule_remaining_emails(db, enrollment)
        
        db.commit()


def schedule_remaining_emails(db: Session, enrollment: SequenceEnrollment):
    """Schedule remaining emails for a resumed enrollment"""
    # Get remaining emails
    remaining_emails = db.query(SequenceEmail).filter(
        and_(
            SequenceEmail.sequence_id == enrollment.sequence_id,
            SequenceEmail.email_index >= enrollment.current_email_index
        )
    ).order_by(SequenceEmail.email_index).all()
    
    # Cancel existing scheduled emails
    existing_scheduled = db.query(ScheduledEmail).filter(
        and_(
            ScheduledEmail.enrollment_id == enrollment.id,
            ScheduledEmail.status == "cancelled"
        )
    ).all()
    
    for email in existing_scheduled:
        db.delete(email)
    
    # Schedule new emails
    base_date = datetime.utcnow()
    
    for email in remaining_emails:
        # Calculate delay from current time
        delay_from_now = email.delay_days - (enrollment.current_email_index * 7)  # Assuming weekly emails
        if delay_from_now < 0:
            delay_from_now = 0
        
        send_date = base_date + timedelta(days=delay_from_now)
        
        scheduled_email = ScheduledEmail(
            enrollment_id=enrollment.id,
            email_id=email.id,
            scheduled_for=send_date,
            status="scheduled"
        )
        db.add(scheduled_email)
    
    db.commit()


def auto_enroll_subscriber(db: Session, email: str, name: str = None, 
                         source: str = "lead_magnet", language: str = "en", 
                         custom_fields: Dict = None) -> Dict[str, Any]:
    """Automatically enroll subscriber in appropriate sequence"""
    try:
        # Create or get subscriber
        subscriber = create_or_get_subscriber(
            db, email, name, source, language, custom_fields
        )
        
        # Enroll in appropriate sequence
        enrollment = enroll_subscriber_in_sequence(db, subscriber, source, language)
        
        return {
            "success": True,
            "subscriber_id": subscriber.id,
            "enrollment_id": enrollment.id,
            "sequence_type": source,
            "language": language,
            "message": f"Subscriber {email} enrolled in {source} sequence"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }