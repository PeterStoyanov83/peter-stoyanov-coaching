import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from models import Base, WaitlistRegistration, CorporateInquiry, LeadMagnetDownload, BlogPost, MultilingualBlogPost

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://peterstoyanov@localhost:5432/coaching_site")

# Debug logging to see what DATABASE_URL is being used
print(f"🔍 DATABASE_URL: {DATABASE_URL}")

def get_db_url():
    """Get the database URL"""
    return DATABASE_URL

# Create SQLAlchemy engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # PostgreSQL configuration
    engine = create_engine(DATABASE_URL)

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

def _parse_blog_post_tags(post):
    """Helper function to parse tags field in blog posts"""
    import json
    
    try:
        if isinstance(post.tags, str) and post.tags:
            post.tags = json.loads(post.tags)
        elif not post.tags:
            post.tags = []
    except (json.JSONDecodeError, TypeError):
        post.tags = []
    
    # Ensure all attributes are properly accessible
    if hasattr(post, '_sa_instance_state'):
        # Force load all attributes to avoid lazy loading issues
        for attr in ['id', 'slug', 'title', 'excerpt', 'content', 'featured_image', 
                     'language', 'translation_id', 'is_published', 'published_at', 
                     'created_at', 'updated_at']:
            getattr(post, attr, None)
    
    return post

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
    import json
    
    # Convert tags list to JSON string for storage
    processed_data = post_data.copy()
    if isinstance(processed_data.get('tags'), list):
        processed_data['tags'] = json.dumps(processed_data['tags'])
    
    blog_post = BlogPost(**processed_data)
    if blog_post.is_published and not blog_post.published_at:
        blog_post.published_at = datetime.utcnow()
    
    db.add(blog_post)
    db.commit()
    db.refresh(blog_post)
    
    # Parse tags field back for response
    _parse_blog_post_tags(blog_post)
    return blog_post

def get_blog_posts(db: Session, skip: int = 0, limit: int = 100, published_only: bool = False, language: str = None):
    """
    Get blog posts with optional filtering
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        published_only: If True, only return published posts
        language: Filter by language ("en" or "bg")
    
    Returns:
        List of blog posts
    """
    query = db.query(BlogPost)
    if published_only:
        query = query.filter(BlogPost.is_published == True)
    if language:
        query = query.filter(BlogPost.language == language)
    
    posts = query.order_by(BlogPost.created_at.desc()).offset(skip).limit(limit).all()
    
    # Parse tags field
    for post in posts:
        _parse_blog_post_tags(post)
    
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
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if post:
        _parse_blog_post_tags(post)
    
    return post

def get_blog_post_by_slug(db: Session, slug: str, published_only: bool = False, language: str = None):
    """
    Get a blog post by slug
    
    Args:
        db: Database session
        slug: Slug of the blog post
        published_only: If True, only return if published
        language: Filter by language ("en" or "bg")
    
    Returns:
        BlogPost object or None
    """
    query = db.query(BlogPost).filter(BlogPost.slug == slug)
    if published_only:
        query = query.filter(BlogPost.is_published == True)
    if language:
        query = query.filter(BlogPost.language == language)
    
    post = query.first()
    if post:
        _parse_blog_post_tags(post)
    
    return post

def get_post_translations(db: Session, translation_id: str):
    """
    Get all translations of a blog post by translation_id
    
    Args:
        db: Database session
        translation_id: Common translation ID linking related posts
    
    Returns:
        List of BlogPost objects in different languages
    """
    posts = db.query(BlogPost).filter(
        BlogPost.translation_id == translation_id,
        BlogPost.is_published == True
    ).all()
    
    for post in posts:
        _parse_blog_post_tags(post)
    
    return posts

def get_related_posts(db: Session, post_id: int, language: str = None, limit: int = 3):
    """
    Get related blog posts based on shared tags
    
    Args:
        db: Database session
        post_id: ID of the current post
        language: Filter by language ("en" or "bg")
        limit: Maximum number of related posts to return
    
    Returns:
        List of related BlogPost objects
    """
    # Get the current post to find its tags
    current_post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not current_post:
        return []
    
    # Parse tags for the current post
    _parse_blog_post_tags(current_post)
    current_tags = current_post.tags or []
    
    if not current_tags:
        return []
    
    # Find other posts with similar tags
    query = db.query(BlogPost).filter(
        BlogPost.id != post_id,
        BlogPost.is_published == True
    )
    
    if language:
        query = query.filter(BlogPost.language == language)
    
    all_posts = query.all()
    
    # Score posts based on tag matches
    scored_posts = []
    for post in all_posts:
        _parse_blog_post_tags(post)
        post_tags = post.tags or []
        
        # Calculate similarity score (number of matching tags)
        matching_tags = set(current_tags) & set(post_tags)
        if matching_tags:
            score = len(matching_tags)
            scored_posts.append((post, score))
    
    # Sort by score (highest first) and limit results
    scored_posts.sort(key=lambda x: x[1], reverse=True)
    related_posts = [post for post, score in scored_posts[:limit]]
    
    return related_posts

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
    import json
    
    blog_post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not blog_post:
        return None
    
    # Check if slug is being updated and if it conflicts with existing posts
    if 'slug' in post_data and post_data['slug'] != blog_post.slug:
        existing_post = db.query(BlogPost).filter(
            BlogPost.slug == post_data['slug'],
            BlogPost.id != post_id  # Exclude the current post
        ).first()
        if existing_post:
            raise ValueError("A blog post with this slug already exists")
    
    # Process data - convert dict fields to JSON strings for storage
    processed_data = post_data.copy()
    if isinstance(processed_data.get('title'), dict):
        processed_data['title'] = json.dumps(processed_data['title'])
    if isinstance(processed_data.get('excerpt'), dict):
        processed_data['excerpt'] = json.dumps(processed_data['excerpt'])
    if isinstance(processed_data.get('content'), dict):
        processed_data['content'] = json.dumps(processed_data['content'])
    if isinstance(processed_data.get('tags'), dict):
        processed_data['tags'] = json.dumps(processed_data['tags'])
    
    # Update fields
    for key, value in processed_data.items():
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
    
    # Parse JSON fields back for response
    _parse_blog_post_tags(blog_post)
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

def get_blog_posts_with_translations(db: Session, skip: int = 0, limit: int = 100, published_only: bool = False):
    """
    Get blog posts with their translations grouped together
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        published_only: If True, only return published posts
    
    Returns:
        List of blog posts with their translations
    """
    query = db.query(BlogPost)
    if published_only:
        query = query.filter(BlogPost.is_published == True)
    
    posts = query.order_by(BlogPost.created_at.desc()).offset(skip).limit(limit).all()
    
    # Group posts by translation_id and add translations
    result = []
    processed_translation_ids = set()
    
    for post in posts:
        _parse_blog_post_tags(post)
        
        # Skip if we've already processed this translation group
        if post.translation_id and post.translation_id in processed_translation_ids:
            continue
            
        # Find all translations for this post
        translations = []
        if post.translation_id:
            translation_posts = db.query(BlogPost).filter(
                BlogPost.translation_id == post.translation_id,
                BlogPost.id != post.id
            ).all()
            
            for t_post in translation_posts:
                _parse_blog_post_tags(t_post)
                translations.append(t_post)
            
            processed_translation_ids.add(post.translation_id)
        
        # Create result with translations
        post_dict = {
            "id": post.id,
            "slug": post.slug,
            "title": post.title,
            "excerpt": post.excerpt,
            "content": post.content,
            "featured_image": post.featured_image,
            "tags": post.tags,
            "language": post.language,
            "translation_id": post.translation_id,
            "is_published": post.is_published,
            "published_at": post.published_at,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "translations": translations
        }
        result.append(post_dict)
    
    return result

def get_post_translations(db: Session, translation_id: str):
    """
    Get all posts that share the same translation_id
    
    Args:
        db: Database session
        translation_id: The translation ID to search for
    
    Returns:
        List of related blog posts
    """
    if not translation_id:
        return []
        
    posts = db.query(BlogPost).filter(BlogPost.translation_id == translation_id).all()
    
    for post in posts:
        _parse_blog_post_tags(post)
    
    return posts

def link_post_translations(db: Session, post_ids: list, translation_id: str = None):
    """
    Link multiple posts as translations of each other
    
    Args:
        db: Database session
        post_ids: List of post IDs to link together
        translation_id: Optional custom translation ID, will generate one if not provided
    
    Returns:
        The translation_id used for linking
    """
    import uuid
    
    if not translation_id:
        translation_id = f"trans-{uuid.uuid4().hex[:12]}"
    
    # Update all posts with the same translation_id
    for post_id in post_ids:
        post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
        if post:
            post.translation_id = translation_id
    
    db.commit()
    return translation_id

# Multilingual Blog Post Database Functions

def create_multilingual_blog_post(db: Session, post_data: dict):
    """
    Create a new multilingual blog post
    
    Args:
        db: Database session
        post_data: Dictionary containing multilingual blog post data
    
    Returns:
        The created MultilingualBlogPost object
    """
    from datetime import datetime
    import json
    
    # Convert tags lists to JSON if needed
    processed_data = post_data.copy()
    if isinstance(processed_data.get('tags_en'), list):
        processed_data['tags_en'] = processed_data['tags_en']
    if isinstance(processed_data.get('tags_bg'), list):
        processed_data['tags_bg'] = processed_data['tags_bg']
    
    blog_post = MultilingualBlogPost(**processed_data)
    
    # Set published dates if publishing for the first time
    if blog_post.is_published_en and not blog_post.published_at_en:
        blog_post.published_at_en = datetime.utcnow()
    if blog_post.is_published_bg and not blog_post.published_at_bg:
        blog_post.published_at_bg = datetime.utcnow()
    
    db.add(blog_post)
    db.commit()
    db.refresh(blog_post)
    
    return blog_post

def get_multilingual_blog_posts(db: Session, skip: int = 0, limit: int = 100):
    """
    Get all multilingual blog posts
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List of multilingual blog posts
    """
    posts = db.query(MultilingualBlogPost).order_by(MultilingualBlogPost.created_at.desc()).offset(skip).limit(limit).all()
    return posts

def get_multilingual_blog_post_by_id(db: Session, post_id: int):
    """
    Get a multilingual blog post by ID
    
    Args:
        db: Database session
        post_id: ID of the blog post
    
    Returns:
        MultilingualBlogPost object or None
    """
    return db.query(MultilingualBlogPost).filter(MultilingualBlogPost.id == post_id).first()

def get_multilingual_blog_post_by_slug(db: Session, slug: str, language: str = "en"):
    """
    Get a multilingual blog post by slug and language
    
    Args:
        db: Database session
        slug: Slug of the blog post
        language: Language ("en" or "bg")
    
    Returns:
        MultilingualBlogPost object or None
    """
    if language == "en":
        return db.query(MultilingualBlogPost).filter(MultilingualBlogPost.slug_en == slug).first()
    else:
        return db.query(MultilingualBlogPost).filter(MultilingualBlogPost.slug_bg == slug).first()

def get_published_multilingual_posts(db: Session, language: str = "en", skip: int = 0, limit: int = 100):
    """
    Get published multilingual blog posts for a specific language
    
    Args:
        db: Database session
        language: Language ("en" or "bg")
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List of published posts for the specified language
    """
    if language == "en":
        posts = db.query(MultilingualBlogPost).filter(
            MultilingualBlogPost.is_published_en == True
        ).order_by(MultilingualBlogPost.published_at_en.desc()).offset(skip).limit(limit).all()
    else:
        posts = db.query(MultilingualBlogPost).filter(
            MultilingualBlogPost.is_published_bg == True
        ).order_by(MultilingualBlogPost.published_at_bg.desc()).offset(skip).limit(limit).all()
    
    return posts

def update_multilingual_blog_post(db: Session, post_id: int, post_data: dict):
    """
    Update an existing multilingual blog post
    
    Args:
        db: Database session
        post_id: ID of the blog post to update
        post_data: Dictionary containing updated blog post data
    
    Returns:
        The updated MultilingualBlogPost object or None if not found
    """
    from datetime import datetime
    
    blog_post = db.query(MultilingualBlogPost).filter(MultilingualBlogPost.id == post_id).first()
    if not blog_post:
        return None
    
    # Check for slug conflicts
    if 'slug_en' in post_data and post_data['slug_en'] != blog_post.slug_en:
        existing_post = db.query(MultilingualBlogPost).filter(
            MultilingualBlogPost.slug_en == post_data['slug_en'],
            MultilingualBlogPost.id != post_id
        ).first()
        if existing_post:
            raise ValueError("A blog post with this English slug already exists")
    
    if 'slug_bg' in post_data and post_data['slug_bg'] != blog_post.slug_bg:
        existing_post = db.query(MultilingualBlogPost).filter(
            MultilingualBlogPost.slug_bg == post_data['slug_bg'],
            MultilingualBlogPost.id != post_id
        ).first()
        if existing_post:
            raise ValueError("A blog post with this Bulgarian slug already exists")
    
    # Update fields
    for key, value in post_data.items():
        if hasattr(blog_post, key):
            setattr(blog_post, key, value)
    
    # Set published dates if publishing for the first time
    if blog_post.is_published_en and not blog_post.published_at_en:
        blog_post.published_at_en = datetime.utcnow()
    elif not blog_post.is_published_en:
        blog_post.published_at_en = None
    
    if blog_post.is_published_bg and not blog_post.published_at_bg:
        blog_post.published_at_bg = datetime.utcnow()
    elif not blog_post.is_published_bg:
        blog_post.published_at_bg = None
    
    blog_post.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(blog_post)
    
    return blog_post

def delete_multilingual_blog_post(db: Session, post_id: int):
    """
    Delete a multilingual blog post
    
    Args:
        db: Database session
        post_id: ID of the blog post to delete
    
    Returns:
        True if deleted, False if not found
    """
    blog_post = db.query(MultilingualBlogPost).filter(MultilingualBlogPost.id == post_id).first()
    if not blog_post:
        return False
    
    db.delete(blog_post)
    db.commit()
    return True

def get_related_multilingual_posts(db: Session, post_id: int, language: str = "en", limit: int = 3):
    """
    Get related multilingual blog posts based on shared tags
    
    Args:
        db: Database session
        post_id: ID of the current post
        language: Filter by language ("en" or "bg")
        limit: Maximum number of related posts to return
    
    Returns:
        List of related MultilingualBlogPost objects
    """
    # Get the current post to find its tags
    current_post = db.query(MultilingualBlogPost).filter(MultilingualBlogPost.id == post_id).first()
    if not current_post:
        return []
    
    # Get tags for the specified language
    if language == "en":
        current_tags = current_post.tags_en or []
        published_filter = MultilingualBlogPost.is_published_en == True
    else:
        current_tags = current_post.tags_bg or []
        published_filter = MultilingualBlogPost.is_published_bg == True
    
    if not current_tags:
        return []
    
    # Find other published posts
    query = db.query(MultilingualBlogPost).filter(
        MultilingualBlogPost.id != post_id,
        published_filter
    )
    
    all_posts = query.all()
    
    # Score posts based on tag matches
    scored_posts = []
    for post in all_posts:
        if language == "en":
            post_tags = post.tags_en or []
        else:
            post_tags = post.tags_bg or []
        
        # Calculate similarity score (number of matching tags)
        matching_tags = set(current_tags) & set(post_tags)
        if matching_tags:
            score = len(matching_tags)
            scored_posts.append((post, score))
    
    # Sort by score (highest first) and limit results
    scored_posts.sort(key=lambda x: x[1], reverse=True)
    related_posts = [post for post, score in scored_posts[:limit]]
    
    return related_posts