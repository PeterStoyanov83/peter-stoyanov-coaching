from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
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

class LeadMagnetDownload(Base):
    __tablename__ = "lead_magnet_downloads"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), nullable=False, index=True)
    download_count = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_downloaded_at = Column(DateTime, default=datetime.utcnow)

class BlogPost(Base):
    __tablename__ = "blog_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(200), nullable=False, unique=True, index=True)  # Single slug for both languages
    title = Column(JSON, nullable=False)  # {"en": "English Title", "bg": "Bulgarian Title"}
    excerpt = Column(JSON, nullable=False)  # {"en": "English excerpt", "bg": "Bulgarian excerpt"}
    content = Column(JSON, nullable=False)  # {"en": "English content", "bg": "Bulgarian content"}
    featured_image = Column(String(500), nullable=True)
    tags = Column(JSON, nullable=True)  # {"en": ["tag1", "tag2"], "bg": ["таг1", "таг2"]}
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime, nullable=True)
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
    
    class Config:
        from_attributes = True

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
    title: Dict[str, str]  # {"en": "English Title", "bg": "Bulgarian Title"}
    excerpt: Dict[str, str]  # {"en": "English excerpt", "bg": "Bulgarian excerpt"}
    content: Dict[str, str]  # {"en": "English content", "bg": "Bulgarian content"}
    featured_image: Optional[str] = None
    tags: Optional[Dict[str, List[str]]] = {}  # {"en": ["tag1"], "bg": ["таг1"]}
    is_published: bool = False

class BlogPostResponse(BaseModel):
    id: int
    slug: str
    title: Dict[str, str]
    excerpt: Dict[str, str]
    content: Dict[str, str]
    featured_image: Optional[str]
    tags: Optional[Dict[str, List[str]]]
    is_published: bool
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class BlogPostListResponse(BaseModel):
    id: int
    slug: str
    title: Dict[str, str]
    excerpt: Dict[str, str]
    featured_image: Optional[str]
    tags: Optional[Dict[str, List[str]]]
    is_published: bool
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True