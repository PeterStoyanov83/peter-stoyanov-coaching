from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict

Base = declarative_base()

# Database Models
class WaitlistRegistration(Base):
    __tablename__ = "waitlist_registrations"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    city_country = Column(String(100), nullable=False)
    occupation = Column(String(100), nullable=False)
    why_join = Column(Text, nullable=False)
    skills_to_improve = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Email sequence tracking
    welcome_sent = Column(Boolean, default=False)
    welcome_sent_at = Column(DateTime, nullable=True)
    sequence_started = Column(Boolean, default=False)
    current_email_index = Column(Integer, default=0)  # Which email in sequence they're on
    last_email_sent_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)  # Can unsubscribe
    
    # Relationships
    email_logs = relationship("EmailLog", back_populates="waitlist_registration", cascade="all, delete-orphan")

class CorporateInquiry(Base):
    __tablename__ = "corporate_inquiries"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(100), nullable=False)
    contact_person = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    phone = Column(String(20), nullable=True)
    team_size = Column(String(20), nullable=False)
    budget = Column(String(30), nullable=True)
    training_goals = Column(Text, nullable=False)
    preferred_dates = Column(Text, nullable=True)
    additional_info = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Email sequence tracking
    welcome_sent = Column(Boolean, default=False)
    welcome_sent_at = Column(DateTime, nullable=True)
    sequence_started = Column(Boolean, default=False)
    current_email_index = Column(Integer, default=0)
    last_email_sent_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    email_logs = relationship("EmailLog", back_populates="corporate_inquiry", cascade="all, delete-orphan")

class LeadMagnetDownload(Base):
    __tablename__ = "lead_magnet_downloads"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    download_count = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_downloaded_at = Column(DateTime, default=datetime.utcnow)
    
    # Email sequence tracking
    welcome_sent = Column(Boolean, default=False)
    welcome_sent_at = Column(DateTime, nullable=True)
    sequence_started = Column(Boolean, default=False)
    current_email_index = Column(Integer, default=0)
    last_email_sent_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    email_logs = relationship("EmailLog", back_populates="lead_magnet", cascade="all, delete-orphan")

class EmailSequence(Base):
    __tablename__ = "email_sequences"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    sequence_type = Column(String(50), nullable=False)  # "waitlist_magnet", "corporate"
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    emails = relationship("SequenceEmail", back_populates="sequence", cascade="all, delete-orphan")

class SequenceEmail(Base):
    __tablename__ = "sequence_emails"
    
    id = Column(Integer, primary_key=True, index=True)
    sequence_id = Column(Integer, ForeignKey("email_sequences.id"), nullable=False)
    email_index = Column(Integer, nullable=False)  # 0=welcome, 1=week1, 2=week2, etc.
    subject = Column(String(200), nullable=False)
    html_content = Column(Text, nullable=False)
    delay_days = Column(Integer, nullable=False, default=0)  # Days after previous email
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sequence = relationship("EmailSequence", back_populates="emails")

class EmailLog(Base):
    __tablename__ = "email_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    # Link to subscriber
    waitlist_id = Column(Integer, ForeignKey("waitlist_registrations.id"), nullable=True)
    corporate_id = Column(Integer, ForeignKey("corporate_inquiries.id"), nullable=True)
    lead_magnet_id = Column(Integer, ForeignKey("lead_magnet_downloads.id"), nullable=True)
    
    # Email details
    email_type = Column(String(50), nullable=False)  # "welcome", "sequence", "blog_notification", "manual"
    sequence_email_id = Column(Integer, ForeignKey("sequence_emails.id"), nullable=True)
    subject = Column(String(200), nullable=False)
    recipient_email = Column(String(100), nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    sendgrid_message_id = Column(String(100), nullable=True)
    
    # Status tracking
    status = Column(String(20), default="sent")  # sent, failed, bounced, opened, clicked
    error_message = Column(Text, nullable=True)
    
    # Relationships
    waitlist_registration = relationship("WaitlistRegistration", back_populates="email_logs")
    corporate_inquiry = relationship("CorporateInquiry", back_populates="email_logs")
    lead_magnet = relationship("LeadMagnetDownload", back_populates="email_logs")
    sequence_email = relationship("SequenceEmail")

# Blog post models (keeping existing)
class BlogPost(Base):
    __tablename__ = "blog_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(200), nullable=False, unique=True, index=True)
    title = Column(String(200), nullable=False)
    excerpt = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    featured_image = Column(String(500), nullable=True)
    tags = Column(JSON, nullable=True)
    language = Column(String(5), nullable=False, index=True)
    translation_id = Column(String(100), nullable=True, index=True)
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MultilingualBlogPost(Base):
    __tablename__ = "multilingual_blog_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    slug_en = Column(String(200), nullable=False, unique=True, index=True)
    slug_bg = Column(String(200), nullable=False, unique=True, index=True)
    title_en = Column(String(200), nullable=False)
    title_bg = Column(String(200), nullable=False)
    excerpt_en = Column(Text, nullable=False)
    excerpt_bg = Column(Text, nullable=False)
    content_en = Column(Text, nullable=False)
    content_bg = Column(Text, nullable=False)
    tags_en = Column(JSON, nullable=True)
    tags_bg = Column(JSON, nullable=True)
    featured_image = Column(String(500), nullable=True)
    is_published_en = Column(Boolean, default=False)
    is_published_bg = Column(Boolean, default=False)
    published_at_en = Column(DateTime, nullable=True)
    published_at_bg = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Pydantic Models for API
class WaitlistRegistrationRequest(BaseModel):
    full_name: str
    email: EmailStr
    city_country: str
    occupation: str
    why_join: str
    skills_to_improve: str

class WaitlistRegistrationResponse(BaseModel):
    id: int
    full_name: str
    email: str
    city_country: str
    occupation: str
    why_join: str
    skills_to_improve: str
    created_at: datetime
    welcome_sent: bool
    sequence_started: bool
    current_email_index: int
    is_active: bool
    
    class Config:
        from_attributes = True

class CorporateInquiryRequest(BaseModel):
    companyName: str
    contactPerson: str
    email: EmailStr
    phone: Optional[str] = None
    teamSize: Optional[str] = None
    budget: Optional[str] = None
    trainingGoals: str
    preferredDates: Optional[str] = None
    additionalInfo: Optional[str] = None

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
    welcome_sent: bool
    sequence_started: bool
    current_email_index: int
    is_active: bool
    
    class Config:
        from_attributes = True

class LeadMagnetRequest(BaseModel):
    email: EmailStr

class LeadMagnetResponse(BaseModel):
    id: int
    email: str
    download_count: int
    created_at: datetime
    welcome_sent: bool
    sequence_started: bool
    current_email_index: int
    is_active: bool
    
    class Config:
        from_attributes = True

class EmailLogResponse(BaseModel):
    id: int
    email_type: str
    subject: str
    recipient_email: str
    sent_at: datetime
    status: str
    
    class Config:
        from_attributes = True

class SequenceEmailResponse(BaseModel):
    id: int
    email_index: int
    subject: str
    delay_days: int
    is_active: bool
    
    class Config:
        from_attributes = True

class EmailSequenceResponse(BaseModel):
    id: int
    name: str
    sequence_type: str
    description: Optional[str]
    is_active: bool
    emails: List[SequenceEmailResponse]
    
    class Config:
        from_attributes = True

# Blog post response models (keeping existing)
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

class MultilingualBlogPostPublicResponse(BaseModel):
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