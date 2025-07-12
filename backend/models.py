from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict

Base = declarative_base()

# SQLAlchemy models for database
class WaitlistRegistration(Base):
    __tablename__ = "waitlist_registrations"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    city_country = Column(String(100), nullable=False)
    occupation = Column(String(100), nullable=False)
    why_join = Column(Text, nullable=False)
    skills_to_improve = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Enhanced tracking fields
    status = Column(String(20), default="new")  # new, contacted, qualified, converted, not_interested, rejected
    notes = Column(Text, nullable=True)  # Admin notes
    priority = Column(String(10), default="medium")  # low, medium, high
    last_contacted = Column(DateTime, nullable=True)
    follow_up_date = Column(DateTime, nullable=True)
    conversion_source = Column(String(50), nullable=True)  # how they converted to subscriber
    updated_by = Column(String(100), nullable=True)  # admin who last updated
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    lead_score = Column(Integer, default=0)  # calculated lead score
    tags = Column(JSON, nullable=True)  # flexible tagging system
    
class CorporateInquiry(Base):
    __tablename__ = "corporate_inquiries"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(100), nullable=False)
    contact_person = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    team_size = Column(String(20), nullable=False)
    budget = Column(String(30), nullable=True)
    training_goals = Column(Text, nullable=False)
    preferred_dates = Column(Text, nullable=True)
    additional_info = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Enhanced tracking fields
    status = Column(String(20), default="new")  # new, qualified, proposal_sent, negotiation, closed_won, closed_lost, on_hold
    priority = Column(String(10), default="medium")  # low, medium, high, urgent
    estimated_value = Column(Integer, nullable=True)  # estimated deal value in euros
    proposal_sent_date = Column(DateTime, nullable=True)
    follow_up_date = Column(DateTime, nullable=True)
    expected_close_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)  # Admin notes
    assigned_to = Column(String(100), nullable=True)  # admin assigned to this inquiry
    last_contacted = Column(DateTime, nullable=True)
    updated_by = Column(String(100), nullable=True)  # admin who last updated
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    lead_score = Column(Integer, default=0)  # calculated lead score based on company size, budget, etc.
    tags = Column(JSON, nullable=True)  # flexible tagging system
    probability = Column(Integer, default=50)  # probability of closing (0-100%)
    lost_reason = Column(String(100), nullable=True)  # reason if status is closed_lost

class LeadMagnetDownload(Base):
    __tablename__ = "lead_magnet_downloads"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), nullable=False, index=True)
    download_count = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_downloaded_at = Column(DateTime, default=datetime.utcnow)

class Communication(Base):
    __tablename__ = "communications"
    
    id = Column(Integer, primary_key=True, index=True)
    contact_type = Column(String(20), nullable=False)  # waitlist, corporate, subscriber
    contact_id = Column(Integer, nullable=False)  # reference to waitlist/corporate/subscriber ID
    communication_type = Column(String(20), nullable=False)  # email, call, meeting, note
    subject = Column(String(200), nullable=True)
    content = Column(Text, nullable=True)
    sent_at = Column(DateTime, default=datetime.utcnow)
    sent_by = Column(String(100), nullable=False)  # admin name
    response_received = Column(Boolean, default=False)
    response_date = Column(DateTime, nullable=True)
    follow_up_required = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    task_type = Column(String(20), nullable=False)  # follow_up, call, email, meeting
    contact_type = Column(String(20), nullable=False)  # waitlist, corporate, subscriber
    contact_id = Column(Integer, nullable=False)
    assigned_to = Column(String(100), nullable=False)  # admin assigned
    due_date = Column(DateTime, nullable=False)
    status = Column(String(20), default="pending")  # pending, completed, overdue, cancelled
    priority = Column(String(10), default="medium")  # low, medium, high, urgent
    completed_at = Column(DateTime, nullable=True)
    completed_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BlogPost(Base):
    __tablename__ = "blog_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(200), nullable=False, unique=True, index=True)  # Language-specific slug
    title = Column(String(200), nullable=False)  # Single language title
    excerpt = Column(Text, nullable=False)  # Single language excerpt
    content = Column(Text, nullable=False)  # Single language content
    featured_image = Column(String(500), nullable=True)
    tags = Column(JSON, nullable=True)  # Array of tags for this language: ["tag1", "tag2"]
    language = Column(String(5), nullable=False, index=True)  # "en" or "bg"
    translation_id = Column(String(100), nullable=True, index=True)  # Links related translations
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MultilingualBlogPost(Base):
    __tablename__ = "multilingual_blog_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Separate slugs for SEO
    slug_en = Column(String(200), nullable=False, unique=True, index=True)
    slug_bg = Column(String(200), nullable=False, unique=True, index=True)
    
    # Multilingual content fields
    title_en = Column(String(200), nullable=False)
    title_bg = Column(String(200), nullable=False)
    excerpt_en = Column(Text, nullable=False)
    excerpt_bg = Column(Text, nullable=False)
    content_en = Column(Text, nullable=False)
    content_bg = Column(Text, nullable=False)
    
    # Multilingual tags
    tags_en = Column(JSON, nullable=True)  # ["tag1", "tag2"]
    tags_bg = Column(JSON, nullable=True)  # ["таг1", "таг2"]
    
    # Shared image
    featured_image = Column(String(500), nullable=True)
    
    # Per-language publish status
    is_published_en = Column(Boolean, default=False)
    is_published_bg = Column(Boolean, default=False)
    published_at_en = Column(DateTime, nullable=True)
    published_at_bg = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Email Sequence Automation Models
class EmailSubscriber(Base):
    __tablename__ = "email_subscribers"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    name = Column(String(100), nullable=True)
    source = Column(String(50), nullable=False)  # lead_magnet, waitlist, corporate
    language = Column(String(5), nullable=False, default="en")  # en, bg
    signup_date = Column(DateTime, default=datetime.utcnow)
    engagement_level = Column(String(20), default="new")  # new, warm, hot, cold
    is_active = Column(Boolean, default=True)
    mailerlite_id = Column(String(100), nullable=True)  # MailerLite subscriber ID
    custom_fields = Column(JSON, nullable=True)  # Additional subscriber data
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to sequence enrollments
    sequence_enrollments = relationship("SequenceEnrollment", back_populates="subscriber")

class EmailSequence(Base):
    __tablename__ = "email_sequences"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    sequence_type = Column(String(50), nullable=False)  # lead_magnet, waitlist, corporate
    language = Column(String(5), nullable=False)  # en, bg
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to emails and enrollments
    emails = relationship("SequenceEmail", back_populates="sequence")
    enrollments = relationship("SequenceEnrollment", back_populates="sequence")

class SequenceEmail(Base):
    __tablename__ = "sequence_emails"
    
    id = Column(Integer, primary_key=True, index=True)
    sequence_id = Column(Integer, ForeignKey("email_sequences.id"), nullable=False)
    email_index = Column(Integer, nullable=False)  # 0, 1, 2, etc.
    subject = Column(String(200), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    cta = Column(String(200), nullable=False)
    delay_days = Column(Integer, nullable=False, default=0)
    week_number = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sequence = relationship("EmailSequence", back_populates="emails")
    scheduled_sends = relationship("ScheduledEmail", back_populates="email")

class SequenceEnrollment(Base):
    __tablename__ = "sequence_enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    subscriber_id = Column(Integer, ForeignKey("email_subscribers.id"), nullable=False)
    sequence_id = Column(Integer, ForeignKey("email_sequences.id"), nullable=False)
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    current_email_index = Column(Integer, default=0)  # Next email to send
    status = Column(String(20), default="active")  # active, paused, completed, cancelled
    completion_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    subscriber = relationship("EmailSubscriber", back_populates="sequence_enrollments")
    sequence = relationship("EmailSequence", back_populates="enrollments")
    scheduled_emails = relationship("ScheduledEmail", back_populates="enrollment")

class ScheduledEmail(Base):
    __tablename__ = "scheduled_emails"
    
    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey("sequence_enrollments.id"), nullable=False)
    email_id = Column(Integer, ForeignKey("sequence_emails.id"), nullable=False)
    scheduled_for = Column(DateTime, nullable=False)
    sent_at = Column(DateTime, nullable=True)
    status = Column(String(20), default="scheduled")  # scheduled, sent, failed, cancelled, permanently_failed
    mailerlite_campaign_id = Column(String(100), nullable=True)
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    enrollment = relationship("SequenceEnrollment", back_populates="scheduled_emails")
    email = relationship("SequenceEmail", back_populates="scheduled_sends")

class EmailAnalytics(Base):
    __tablename__ = "email_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    scheduled_email_id = Column(Integer, ForeignKey("scheduled_emails.id"), nullable=False)
    opened_at = Column(DateTime, nullable=True)
    clicked_at = Column(DateTime, nullable=True)
    converted_at = Column(DateTime, nullable=True)
    bounced_at = Column(DateTime, nullable=True)
    unsubscribed_at = Column(DateTime, nullable=True)
    open_count = Column(Integer, default=0)
    click_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Pydantic models for response
class WaitlistRegistrationResponse(BaseModel):
    id: int
    full_name: str
    email: str
    city_country: str
    occupation: str
    why_join: str
    skills_to_improve: str
    created_at: datetime
    status: str
    notes: Optional[str]
    priority: str
    last_contacted: Optional[datetime]
    follow_up_date: Optional[datetime]
    conversion_source: Optional[str]
    updated_by: Optional[str]
    updated_at: datetime
    lead_score: int
    tags: Optional[List[str]]
    
    class Config:
        from_attributes = True

class WaitlistUpdateRequest(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
    priority: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    conversion_source: Optional[str] = None
    lead_score: Optional[int] = None
    tags: Optional[List[str]] = None

class CorporateInquiryResponse(BaseModel):
    id: int
    company_name: str
    contact_person: str
    email: str
    phone: Optional[str]
    team_size: str
    budget: Optional[str]
    training_goals: str
    preferred_dates: Optional[str]
    additional_info: Optional[str]
    created_at: datetime
    status: str
    priority: str
    estimated_value: Optional[int]
    proposal_sent_date: Optional[datetime]
    follow_up_date: Optional[datetime]
    expected_close_date: Optional[datetime]
    notes: Optional[str]
    assigned_to: Optional[str]
    last_contacted: Optional[datetime]
    updated_by: Optional[str]
    updated_at: datetime
    lead_score: int
    tags: Optional[List[str]]
    probability: int
    lost_reason: Optional[str]
    
    class Config:
        from_attributes = True

class CorporateUpdateRequest(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    estimated_value: Optional[int] = None
    proposal_sent_date: Optional[datetime] = None
    follow_up_date: Optional[datetime] = None
    expected_close_date: Optional[datetime] = None
    notes: Optional[str] = None
    assigned_to: Optional[str] = None
    lead_score: Optional[int] = None
    tags: Optional[List[str]] = None
    probability: Optional[int] = None
    lost_reason: Optional[str] = None

class CommunicationRequest(BaseModel):
    contact_type: str  # waitlist, corporate, subscriber
    contact_id: int
    communication_type: str  # email, call, meeting, note
    subject: Optional[str] = None
    content: Optional[str] = None
    follow_up_required: bool = False

class CommunicationResponse(BaseModel):
    id: int
    contact_type: str
    contact_id: int
    communication_type: str
    subject: Optional[str]
    content: Optional[str]
    sent_at: datetime
    sent_by: str
    response_received: bool
    response_date: Optional[datetime]
    follow_up_required: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TaskRequest(BaseModel):
    title: str
    description: Optional[str] = None
    task_type: str  # follow_up, call, email, meeting
    contact_type: str  # waitlist, corporate, subscriber
    contact_id: int
    assigned_to: str
    due_date: datetime
    priority: str = "medium"

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    task_type: str
    contact_type: str
    contact_id: int
    assigned_to: str
    due_date: datetime
    status: str
    priority: str
    completed_at: Optional[datetime]
    completed_by: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class LeadMagnetDownloadResponse(BaseModel):
    id: int
    email: str
    download_count: int
    created_at: datetime
    last_downloaded_at: datetime
    
    class Config:
        from_attributes = True

class BlogPostRequest(BaseModel):
    slug: str
    title: str
    excerpt: str
    content: str
    featured_image: Optional[str] = None
    tags: Optional[List[str]] = []  # ["tag1", "tag2"]
    language: str  # "en" or "bg"
    translation_id: Optional[str] = None  # Links related translations
    is_published: bool = False

class MultilingualBlogPostRequest(BaseModel):
    slug_en: str
    slug_bg: str
    title_en: str
    title_bg: str
    excerpt_en: str
    excerpt_bg: str
    content_en: str
    content_bg: str
    tags_en: Optional[List[str]] = []
    tags_bg: Optional[List[str]] = []
    featured_image: Optional[str] = None
    is_published_en: bool = False
    is_published_bg: bool = False

class MultilingualBlogPostUpdateRequest(BaseModel):
    slug_en: Optional[str] = None
    slug_bg: Optional[str] = None
    title_en: Optional[str] = None
    title_bg: Optional[str] = None
    excerpt_en: Optional[str] = None
    excerpt_bg: Optional[str] = None
    content_en: Optional[str] = None
    content_bg: Optional[str] = None
    tags_en: Optional[List[str]] = None
    tags_bg: Optional[List[str]] = None
    featured_image: Optional[str] = None
    is_published_en: Optional[bool] = None
    is_published_bg: Optional[bool] = None

class BlogPostResponse(BaseModel):
    id: int
    slug: str
    title: str
    excerpt: str
    content: str
    featured_image: Optional[str]
    tags: Optional[List[str]]
    language: str
    translation_id: Optional[str]
    is_published: bool
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class BlogPostListResponse(BaseModel):
    id: int
    slug: str
    title: str
    excerpt: str
    featured_image: Optional[str]
    tags: Optional[List[str]]
    language: str
    translation_id: Optional[str]
    is_published: bool
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class BlogPostWithTranslations(BaseModel):
    """Blog post with its available translations"""
    id: int
    slug: str
    title: str
    excerpt: str
    content: str
    featured_image: Optional[str]
    tags: Optional[List[str]]
    language: str
    translation_id: Optional[str]
    is_published: bool
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    translations: List[BlogPostResponse] = []  # Available translations
    
    class Config:
        from_attributes = True

class MultilingualBlogPostResponse(BaseModel):
    """Full multilingual blog post response for admin"""
    id: int
    slug_en: str
    slug_bg: str
    title_en: str
    title_bg: str
    excerpt_en: str
    excerpt_bg: str
    content_en: str
    content_bg: str
    tags_en: Optional[List[str]]
    tags_bg: Optional[List[str]]
    featured_image: Optional[str]
    is_published_en: bool
    is_published_bg: bool
    published_at_en: Optional[datetime]
    published_at_bg: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class MultilingualBlogPostPublicResponse(BaseModel):
    """Single language response for public API"""
    id: int
    slug: str
    title: str
    excerpt: str
    content: str
    featured_image: Optional[str]
    tags: Optional[List[str]]
    language: str
    available_languages: List[str]
    is_published: bool
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Email Sequence Pydantic Models
class EmailSubscriberRequest(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    source: str  # lead_magnet, waitlist, corporate
    language: str = "en"
    custom_fields: Optional[Dict] = None

class EmailSubscriberResponse(BaseModel):
    id: int
    email: str
    name: Optional[str]
    source: str
    language: str
    signup_date: datetime
    engagement_level: str
    is_active: bool
    mailerlite_id: Optional[str]
    custom_fields: Optional[Dict]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class SequenceEnrollmentRequest(BaseModel):
    subscriber_id: int
    sequence_type: str
    language: str = "en"

class SequenceEnrollmentResponse(BaseModel):
    id: int
    subscriber_id: int
    sequence_id: int
    enrollment_date: datetime
    current_email_index: int
    status: str
    completion_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ScheduledEmailResponse(BaseModel):
    id: int
    enrollment_id: int
    email_id: int
    scheduled_for: datetime
    sent_at: Optional[datetime]
    status: str
    mailerlite_campaign_id: Optional[str]
    error_message: Optional[str]
    retry_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class EmailAnalyticsResponse(BaseModel):
    id: int
    scheduled_email_id: int
    opened_at: Optional[datetime]
    clicked_at: Optional[datetime]
    converted_at: Optional[datetime]
    bounced_at: Optional[datetime]
    unsubscribed_at: Optional[datetime]
    open_count: int
    click_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True