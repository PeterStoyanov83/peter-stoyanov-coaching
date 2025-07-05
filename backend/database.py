import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from models import Base, WaitlistRegistration, CorporateInquiry

# Get database URL from environment variable or use default SQLite URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./coaching_site.db")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the database
Base.metadata.create_all(bind=engine)

def get_db():
    """
    Dependency to get the database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def store_waitlist_registration(db: Session, registration: WaitlistRegistration):
    """
    Store a waitlist registration in the database
    
    Args:
        db: Database session
        registration: WaitlistRegistration object
    
    Returns:
        The created registration
    """
    db.add(registration)
    db.commit()
    db.refresh(registration)
    return registration

def store_corporate_inquiry(db: Session, inquiry: CorporateInquiry):
    """
    Store a corporate inquiry in the database
    
    Args:
        db: Database session
        inquiry: CorporateInquiry object
    
    Returns:
        The created inquiry
    """
    db.add(inquiry)
    db.commit()
    db.refresh(inquiry)
    return inquiry

def get_waitlist_registrations(db: Session, skip: int = 0, limit: int = 100):
    """
    Get all waitlist registrations
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List of waitlist registrations
    """
    return db.query(WaitlistRegistration).offset(skip).limit(limit).all()

def get_corporate_inquiries(db: Session, skip: int = 0, limit: int = 100):
    """
    Get all corporate inquiries
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List of corporate inquiries
    """
    return db.query(CorporateInquiry).offset(skip).limit(limit).all()

def get_waitlist_registration_by_email(db: Session, email: str):
    """
    Get a waitlist registration by email
    
    Args:
        db: Database session
        email: Email address to search for
    
    Returns:
        WaitlistRegistration object or None
    """
    return db.query(WaitlistRegistration).filter(WaitlistRegistration.email == email).first()

def get_corporate_inquiry_by_email(db: Session, email: str):
    """
    Get a corporate inquiry by email
    
    Args:
        db: Database session
        email: Email address to search for
    
    Returns:
        CorporateInquiry object or None
    """
    return db.query(CorporateInquiry).filter(CorporateInquiry.email == email).first()