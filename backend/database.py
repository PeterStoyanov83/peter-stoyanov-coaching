import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from models import Base, WaitlistRegistration, CorporateInquiry, LeadMagnetDownload, BlogPost

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

def store_lead_magnet_download(db: Session, email: str):
    """
    Store or update a lead magnet download record
    
    Args:
        db: Database session
        email: Email address of the downloader
    
    Returns:
        The created or updated LeadMagnetDownload record
    """
    from datetime import datetime
    
    # Check if email already exists
    existing_download = db.query(LeadMagnetDownload).filter(LeadMagnetDownload.email == email).first()
    
    if existing_download:
        # Update existing record
        existing_download.download_count += 1
        existing_download.last_downloaded_at = datetime.utcnow()
        db.commit()
        db.refresh(existing_download)
        return existing_download
    else:
        # Create new record
        new_download = LeadMagnetDownload(email=email)
        db.add(new_download)
        db.commit()
        db.refresh(new_download)
        return new_download

def get_lead_magnet_downloads(db: Session, skip: int = 0, limit: int = 100):
    """
    Get all lead magnet downloads
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List of lead magnet downloads
    """
    return db.query(LeadMagnetDownload).offset(skip).limit(limit).all()

def get_lead_magnet_download_by_email(db: Session, email: str):
    """
    Get a lead magnet download record by email
    
    Args:
        db: Database session
        email: Email address to search for
    
    Returns:
        LeadMagnetDownload object or None
    """
    return db.query(LeadMagnetDownload).filter(LeadMagnetDownload.email == email).first()

# Blog Post Database Functions

def create_blog_post(db: Session, post_data: dict):
    """
    Create a new blog post
    
    Args:
        db: Database session
        post_data: Dictionary containing blog post data
    
    Returns:
        The created BlogPost object
    """
    from datetime import datetime
    
    blog_post = BlogPost(**post_data)
    if blog_post.is_published and not blog_post.published_at:
        blog_post.published_at = datetime.utcnow()
    
    db.add(blog_post)
    db.commit()
    db.refresh(blog_post)
    return blog_post

def get_blog_posts(db: Session, skip: int = 0, limit: int = 100, published_only: bool = False):
    """
    Get blog posts with optional filtering
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        published_only: If True, only return published posts
    
    Returns:
        List of blog posts
    """
    import json
    
    query = db.query(BlogPost)
    if published_only:
        query = query.filter(BlogPost.is_published == True)
    
    posts = query.order_by(BlogPost.created_at.desc()).offset(skip).limit(limit).all()
    
    # Parse JSON fields
    for post in posts:
        if isinstance(post.title, str):
            post.title = json.loads(post.title)
        if isinstance(post.excerpt, str):
            post.excerpt = json.loads(post.excerpt)
        if isinstance(post.content, str):
            post.content = json.loads(post.content)
        if isinstance(post.tags, str):
            post.tags = json.loads(post.tags)
    
    return posts

def get_blog_post_by_id(db: Session, post_id: int):
    """
    Get a blog post by ID
    
    Args:
        db: Database session
        post_id: ID of the blog post
    
    Returns:
        BlogPost object or None
    """
    return db.query(BlogPost).filter(BlogPost.id == post_id).first()

def get_blog_post_by_slug(db: Session, slug: str, published_only: bool = False):
    """
    Get a blog post by slug
    
    Args:
        db: Database session
        slug: Slug of the blog post
        published_only: If True, only return if published
    
    Returns:
        BlogPost object or None
    """
    query = db.query(BlogPost).filter(BlogPost.slug == slug)
    if published_only:
        query = query.filter(BlogPost.is_published == True)
    
    return query.first()

def update_blog_post(db: Session, post_id: int, post_data: dict):
    """
    Update an existing blog post
    
    Args:
        db: Database session
        post_id: ID of the blog post to update
        post_data: Dictionary containing updated blog post data
    
    Returns:
        The updated BlogPost object or None if not found
    """
    from datetime import datetime
    
    blog_post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not blog_post:
        return None
    
    # Update fields
    for key, value in post_data.items():
        if hasattr(blog_post, key):
            setattr(blog_post, key, value)
    
    # Set published_at if publishing for the first time
    if blog_post.is_published and not blog_post.published_at:
        blog_post.published_at = datetime.utcnow()
    elif not blog_post.is_published:
        blog_post.published_at = None
    
    blog_post.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(blog_post)
    return blog_post

def delete_blog_post(db: Session, post_id: int):
    """
    Delete a blog post
    
    Args:
        db: Database session
        post_id: ID of the blog post to delete
    
    Returns:
        True if deleted, False if not found
    """
    blog_post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not blog_post:
        return False
    
    db.delete(blog_post)
    db.commit()
    return True

def search_blog_posts(db: Session, search_term: str = None, tags: list = None, published_only: bool = False):
    """
    Search blog posts by title, content, or tags
    
    Args:
        db: Database session
        search_term: Term to search in title and content
        tags: List of tags to filter by
        published_only: If True, only return published posts
    
    Returns:
        List of matching blog posts
    """
    query = db.query(BlogPost)
    
    if published_only:
        query = query.filter(BlogPost.is_published == True)
    
    if search_term:
        search_filter = f"%{search_term}%"
        query = query.filter(
            (BlogPost.title.ilike(search_filter)) |
            (BlogPost.content.ilike(search_filter)) |
            (BlogPost.excerpt.ilike(search_filter))
        )
    
    if tags:
        # For JSON column filtering (implementation may vary by database)
        for tag in tags:
            query = query.filter(BlogPost.tags.contains([tag]))
    
    return query.order_by(BlogPost.created_at.desc()).all()