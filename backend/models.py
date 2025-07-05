from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

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
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

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
        orm_mode = True

class CorporateInquiryResponse(BaseModel):
    id: int
    company_name: str
    contact_person: str
    email: str
    message: str
    created_at: datetime
    
    class Config:
        orm_mode = True