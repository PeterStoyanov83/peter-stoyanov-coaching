"""
Advanced Subscriber Segmentation and Tracking System
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from enum import Enum

from models import (
    EmailSubscriber, EmailSequence, SequenceEmail, SequenceEnrollment, 
    ScheduledEmail, EmailAnalytics
)


class EngagementLevel(Enum):
    """Subscriber engagement levels"""
    HOT = "hot"          # High engagement - opens and clicks regularly
    WARM = "warm"        # Medium engagement - opens occasionally
    COLD = "cold"        # Low engagement - rarely opens
    NEW = "new"          # New subscriber - no history yet
    INACTIVE = "inactive"  # No engagement for extended period


class SubscriberSegment(Enum):
    """Predefined subscriber segments"""
    LEAD_MAGNET = "lead_magnet"
    WAITLIST = "waitlist"
    CORPORATE = "corporate"
    HIGH_VALUE = "high_value"
    ENGAGED = "engaged"
    AT_RISK = "at_risk"
    CHURNED = "churned"


def calculate_engagement_score(db: Session, subscriber_id: int, days: int = 30) -> float:
    """Calculate engagement score for a subscriber based on recent activity"""
    since_date = datetime.utcnow() - timedelta(days=days)
    
    # Get subscriber's scheduled emails in the period
    scheduled_emails = db.query(ScheduledEmail).join(SequenceEnrollment).filter(
        and_(
            SequenceEnrollment.subscriber_id == subscriber_id,
            ScheduledEmail.sent_at >= since_date,
            ScheduledEmail.status == "sent"
        )
    ).all()
    
    if not scheduled_emails:
        return 0.0
    
    total_emails = len(scheduled_emails)
    total_opens = 0
    total_clicks = 0
    total_conversions = 0
    
    # Calculate engagement metrics
    for email in scheduled_emails:
        analytics = db.query(EmailAnalytics).filter(
            EmailAnalytics.scheduled_email_id == email.id
        ).first()
        
        if analytics:
            if analytics.opened_at:
                total_opens += 1
            if analytics.clicked_at:
                total_clicks += 1
            if analytics.converted_at:
                total_conversions += 1
    
    # Calculate weighted engagement score
    open_rate = total_opens / total_emails if total_emails > 0 else 0
    click_rate = total_clicks / total_emails if total_emails > 0 else 0
    conversion_rate = total_conversions / total_emails if total_emails > 0 else 0
    
    # Weighted score: opens (40%), clicks (40%), conversions (20%)
    engagement_score = (open_rate * 0.4) + (click_rate * 0.4) + (conversion_rate * 0.2)
    
    return round(engagement_score * 100, 2)  # Return as percentage


def update_subscriber_engagement_level(db: Session, subscriber_id: int) -> str:
    """Update subscriber's engagement level based on recent activity"""
    subscriber = db.query(EmailSubscriber).get(subscriber_id)
    if not subscriber:
        return "unknown"
    
    # Calculate engagement score
    engagement_score = calculate_engagement_score(db, subscriber_id)
    
    # Determine engagement level
    if engagement_score >= 70:
        new_level = EngagementLevel.HOT.value
    elif engagement_score >= 40:
        new_level = EngagementLevel.WARM.value
    elif engagement_score >= 15:
        new_level = EngagementLevel.COLD.value
    elif engagement_score > 0:
        new_level = EngagementLevel.INACTIVE.value
    else:
        # Check if subscriber is new (less than 7 days old)
        days_since_signup = (datetime.utcnow() - subscriber.signup_date).days
        if days_since_signup <= 7:
            new_level = EngagementLevel.NEW.value
        else:
            new_level = EngagementLevel.INACTIVE.value
    
    # Update subscriber
    subscriber.engagement_level = new_level
    subscriber.updated_at = datetime.utcnow()
    db.commit()
    
    return new_level


def get_subscribers_by_segment(db: Session, segment: str, limit: int = 100) -> List[EmailSubscriber]:
    """Get subscribers by predefined segment"""
    
    if segment == SubscriberSegment.LEAD_MAGNET.value:
        return db.query(EmailSubscriber).filter(
            EmailSubscriber.source == "lead_magnet"
        ).limit(limit).all()
    
    elif segment == SubscriberSegment.WAITLIST.value:
        return db.query(EmailSubscriber).filter(
            EmailSubscriber.source == "waitlist"
        ).limit(limit).all()
    
    elif segment == SubscriberSegment.CORPORATE.value:
        return db.query(EmailSubscriber).filter(
            EmailSubscriber.source == "corporate"
        ).limit(limit).all()
    
    elif segment == SubscriberSegment.ENGAGED.value:
        return db.query(EmailSubscriber).filter(
            EmailSubscriber.engagement_level.in_(["hot", "warm"])
        ).limit(limit).all()
    
    elif segment == SubscriberSegment.AT_RISK.value:
        return db.query(EmailSubscriber).filter(
            EmailSubscriber.engagement_level == "cold"
        ).limit(limit).all()
    
    elif segment == SubscriberSegment.CHURNED.value:
        return db.query(EmailSubscriber).filter(
            EmailSubscriber.engagement_level == "inactive"
        ).limit(limit).all()
    
    else:
        return []


def get_subscribers_by_custom_criteria(db: Session, criteria: Dict[str, Any]) -> List[EmailSubscriber]:
    """Get subscribers using custom filtering criteria"""
    query = db.query(EmailSubscriber)
    
    # Apply filters
    if criteria.get("language"):
        query = query.filter(EmailSubscriber.language == criteria["language"])
    
    if criteria.get("source"):
        query = query.filter(EmailSubscriber.source == criteria["source"])
    
    if criteria.get("engagement_level"):
        query = query.filter(EmailSubscriber.engagement_level == criteria["engagement_level"])
    
    if criteria.get("is_active") is not None:
        query = query.filter(EmailSubscriber.is_active == criteria["is_active"])
    
    if criteria.get("signup_date_from"):
        query = query.filter(EmailSubscriber.signup_date >= criteria["signup_date_from"])
    
    if criteria.get("signup_date_to"):
        query = query.filter(EmailSubscriber.signup_date <= criteria["signup_date_to"])
    
    if criteria.get("custom_field_key") and criteria.get("custom_field_value"):
        # JSON field filtering (implementation depends on database)
        key = criteria["custom_field_key"]
        value = criteria["custom_field_value"]
        query = query.filter(EmailSubscriber.custom_fields.op('->>')(key) == value)
    
    # Apply ordering
    order_by = criteria.get("order_by", "signup_date")
    order_dir = criteria.get("order_dir", "desc")
    
    if order_by == "signup_date":
        query = query.order_by(desc(EmailSubscriber.signup_date) if order_dir == "desc" else asc(EmailSubscriber.signup_date))
    elif order_by == "engagement_level":
        query = query.order_by(desc(EmailSubscriber.engagement_level) if order_dir == "desc" else asc(EmailSubscriber.engagement_level))
    
    limit = criteria.get("limit", 100)
    return query.limit(limit).all()


def get_sequence_progress_summary(db: Session, sequence_id: int) -> Dict[str, Any]:
    """Get detailed progress summary for a sequence"""
    sequence = db.query(EmailSequence).get(sequence_id)
    if not sequence:
        return {}
    
    # Get all enrollments for this sequence
    enrollments = db.query(SequenceEnrollment).filter(
        SequenceEnrollment.sequence_id == sequence_id
    ).all()
    
    # Get sequence emails count
    total_emails = db.query(func.count(SequenceEmail.id)).filter(
        SequenceEmail.sequence_id == sequence_id
    ).scalar()
    
    # Calculate progress metrics
    total_enrolled = len(enrollments)
    active_enrollments = [e for e in enrollments if e.status == "active"]
    completed_enrollments = [e for e in enrollments if e.status == "completed"]
    paused_enrollments = [e for e in enrollments if e.status == "paused"]
    
    # Calculate average progress
    if active_enrollments:
        avg_progress = sum(e.current_email_index for e in active_enrollments) / len(active_enrollments)
        avg_completion = (avg_progress / total_emails * 100) if total_emails > 0 else 0
    else:
        avg_progress = 0
        avg_completion = 0
    
    # Get email-by-email stats
    email_stats = []
    sequence_emails = db.query(SequenceEmail).filter(
        SequenceEmail.sequence_id == sequence_id
    ).order_by(SequenceEmail.email_index).all()
    
    for email in sequence_emails:
        sent_count = db.query(ScheduledEmail).filter(
            and_(
                ScheduledEmail.email_id == email.id,
                ScheduledEmail.status == "sent"
            )
        ).count()
        
        failed_count = db.query(ScheduledEmail).filter(
            and_(
                ScheduledEmail.email_id == email.id,
                ScheduledEmail.status.in_(["failed", "permanently_failed"])
            )
        ).count()
        
        # Get engagement metrics
        analytics = db.query(EmailAnalytics).join(ScheduledEmail).filter(
            ScheduledEmail.email_id == email.id
        ).all()
        
        opens = sum(1 for a in analytics if a.opened_at)
        clicks = sum(1 for a in analytics if a.clicked_at)
        
        email_stats.append({
            "email_index": email.email_index,
            "subject": email.subject,
            "sent_count": sent_count,
            "failed_count": failed_count,
            "opens": opens,
            "clicks": clicks,
            "open_rate": round((opens / sent_count * 100) if sent_count > 0 else 0, 2),
            "click_rate": round((clicks / sent_count * 100) if sent_count > 0 else 0, 2)
        })
    
    return {
        "sequence_id": sequence_id,
        "sequence_name": sequence.name,
        "sequence_type": sequence.sequence_type,
        "language": sequence.language,
        "total_emails": total_emails,
        "total_enrolled": total_enrolled,
        "active_enrollments": len(active_enrollments),
        "completed_enrollments": len(completed_enrollments),
        "paused_enrollments": len(paused_enrollments),
        "completion_rate": round((len(completed_enrollments) / total_enrolled * 100) if total_enrolled > 0 else 0, 2),
        "average_progress": round(avg_progress, 2),
        "average_completion": round(avg_completion, 2),
        "email_stats": email_stats
    }


def get_subscriber_journey(db: Session, subscriber_id: int) -> Dict[str, Any]:
    """Get complete journey/history for a subscriber"""
    subscriber = db.query(EmailSubscriber).get(subscriber_id)
    if not subscriber:
        return {}
    
    # Get all enrollments
    enrollments = db.query(SequenceEnrollment).filter(
        SequenceEnrollment.subscriber_id == subscriber_id
    ).all()
    
    journey_data = []
    
    for enrollment in enrollments:
        sequence = db.query(EmailSequence).get(enrollment.sequence_id)
        
        # Get emails sent for this enrollment
        scheduled_emails = db.query(ScheduledEmail).filter(
            ScheduledEmail.enrollment_id == enrollment.id
        ).order_by(ScheduledEmail.scheduled_for).all()
        
        email_history = []
        for email in scheduled_emails:
            sequence_email = db.query(SequenceEmail).get(email.email_id)
            analytics = db.query(EmailAnalytics).filter(
                EmailAnalytics.scheduled_email_id == email.id
            ).first()
            
            email_history.append({
                "subject": sequence_email.subject if sequence_email else "Unknown",
                "scheduled_for": email.scheduled_for.isoformat(),
                "sent_at": email.sent_at.isoformat() if email.sent_at else None,
                "status": email.status,
                "opened": bool(analytics and analytics.opened_at),
                "clicked": bool(analytics and analytics.clicked_at),
                "converted": bool(analytics and analytics.converted_at)
            })
        
        journey_data.append({
            "sequence_name": sequence.name if sequence else "Unknown",
            "sequence_type": sequence.sequence_type if sequence else "Unknown",
            "enrollment_date": enrollment.enrollment_date.isoformat(),
            "status": enrollment.status,
            "current_email_index": enrollment.current_email_index,
            "completion_date": enrollment.completion_date.isoformat() if enrollment.completion_date else None,
            "email_history": email_history
        })
    
    return {
        "subscriber_id": subscriber_id,
        "email": subscriber.email,
        "name": subscriber.name,
        "source": subscriber.source,
        "language": subscriber.language,
        "engagement_level": subscriber.engagement_level,
        "signup_date": subscriber.signup_date.isoformat(),
        "is_active": subscriber.is_active,
        "custom_fields": subscriber.custom_fields,
        "journey": journey_data
    }


def bulk_update_engagement_levels(db: Session, limit: int = 1000) -> Dict[str, int]:
    """Bulk update engagement levels for all subscribers"""
    subscribers = db.query(EmailSubscriber).filter(
        EmailSubscriber.is_active == True
    ).limit(limit).all()
    
    updated_counts = {
        "hot": 0,
        "warm": 0,
        "cold": 0,
        "new": 0,
        "inactive": 0
    }
    
    for subscriber in subscribers:
        old_level = subscriber.engagement_level
        new_level = update_subscriber_engagement_level(db, subscriber.id)
        
        if new_level in updated_counts:
            updated_counts[new_level] += 1
    
    return {
        "total_processed": len(subscribers),
        "engagement_distribution": updated_counts
    }


def get_segmentation_analytics(db: Session) -> Dict[str, Any]:
    """Get overall segmentation analytics"""
    
    # Get subscriber counts by source
    source_counts = db.query(
        EmailSubscriber.source,
        func.count(EmailSubscriber.id).label('count')
    ).filter(
        EmailSubscriber.is_active == True
    ).group_by(EmailSubscriber.source).all()
    
    # Get subscriber counts by engagement level
    engagement_counts = db.query(
        EmailSubscriber.engagement_level,
        func.count(EmailSubscriber.id).label('count')
    ).filter(
        EmailSubscriber.is_active == True
    ).group_by(EmailSubscriber.engagement_level).all()
    
    # Get subscriber counts by language
    language_counts = db.query(
        EmailSubscriber.language,
        func.count(EmailSubscriber.id).label('count')
    ).filter(
        EmailSubscriber.is_active == True
    ).group_by(EmailSubscriber.language).all()
    
    # Get recent signups (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_signups = db.query(func.count(EmailSubscriber.id)).filter(
        and_(
            EmailSubscriber.is_active == True,
            EmailSubscriber.signup_date >= thirty_days_ago
        )
    ).scalar()
    
    return {
        "total_active_subscribers": db.query(func.count(EmailSubscriber.id)).filter(
            EmailSubscriber.is_active == True
        ).scalar(),
        "source_distribution": {source: count for source, count in source_counts},
        "engagement_distribution": {level: count for level, count in engagement_counts},
        "language_distribution": {lang: count for lang, count in language_counts},
        "recent_signups_30d": recent_signups,
        "segments": {
            "engaged": db.query(func.count(EmailSubscriber.id)).filter(
                and_(
                    EmailSubscriber.is_active == True,
                    EmailSubscriber.engagement_level.in_(["hot", "warm"])
                )
            ).scalar(),
            "at_risk": db.query(func.count(EmailSubscriber.id)).filter(
                and_(
                    EmailSubscriber.is_active == True,
                    EmailSubscriber.engagement_level == "cold"
                )
            ).scalar(),
            "churned": db.query(func.count(EmailSubscriber.id)).filter(
                and_(
                    EmailSubscriber.is_active == True,
                    EmailSubscriber.engagement_level == "inactive"
                )
            ).scalar()
        }
    }