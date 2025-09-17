"""
Admin Dashboard API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

from database import get_db
from auth import admin_required, auth_service
from models import (
    WaitlistRegistration, CorporateInquiry, LeadMagnetDownload, EmailLog,
    WaitlistRegistrationResponse, CorporateInquiryResponse, LeadMagnetResponse,
    EmailLogResponse, BlogPost, MultilingualBlogPost, BlogPostResponse, 
    BlogPostListResponse, MultilingualBlogPostPublicResponse
)
from email_service import sendgrid_service

router = APIRouter(prefix="/admin", tags=["Admin"])

# Pydantic models for admin requests
class AdminLoginRequest(BaseModel):
    email: str
    password: str

class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class DashboardStats(BaseModel):
    total_waitlist: int
    total_corporate: int
    total_lead_magnet: int
    total_emails_sent: int
    new_this_week: int
    active_sequences: int

class SubscriberUpdate(BaseModel):
    is_active: Optional[bool] = None
    current_email_index: Optional[int] = None
    sequence_started: Optional[bool] = None

class ManualEmailRequest(BaseModel):
    subscriber_ids: List[int]
    subscriber_type: str  # "waitlist", "corporate", "lead_magnet"
    subject: str
    html_content: str

class BlogPostCreate(BaseModel):
    slug: str
    title: str
    excerpt: str
    content: str
    featured_image: Optional[str] = None
    tags: Optional[List[str]] = None
    language: str = "en"
    translation_id: Optional[str] = None
    is_published: bool = False

class BlogPostUpdate(BaseModel):
    slug: Optional[str] = None
    title: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    featured_image: Optional[str] = None
    tags: Optional[List[str]] = None
    is_published: Optional[bool] = None

class MultilingualBlogPostCreate(BaseModel):
    slug_en: str
    slug_bg: str
    title_en: str
    title_bg: str
    excerpt_en: str
    excerpt_bg: str
    content_en: str
    content_bg: str
    tags_en: Optional[List[str]] = None
    tags_bg: Optional[List[str]] = None
    featured_image: Optional[str] = None
    is_published_en: bool = False
    is_published_bg: bool = False

# Authentication endpoints
@router.post("/login", response_model=AdminLoginResponse)
async def admin_login(login_data: AdminLoginRequest):
    """Admin login endpoint"""
    if not auth_service.authenticate_admin(login_data.email, login_data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = auth_service.create_access_token(
        data={"sub": login_data.email, "type": "admin"}
    )
    
    return AdminLoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=1440  # 24 hours in minutes
    )

# Dashboard statistics
@router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics"""
    # Get current counts
    total_waitlist = db.query(WaitlistRegistration).count()
    total_corporate = db.query(CorporateInquiry).count()
    total_lead_magnet = db.query(LeadMagnetDownload).count()
    total_emails_sent = db.query(EmailLog).count()
    
    # Get new subscribers this week
    week_ago = datetime.utcnow() - timedelta(days=7)
    new_waitlist = db.query(WaitlistRegistration).filter(
        WaitlistRegistration.created_at >= week_ago
    ).count()
    new_corporate = db.query(CorporateInquiry).filter(
        CorporateInquiry.created_at >= week_ago
    ).count()
    new_lead_magnet = db.query(LeadMagnetDownload).filter(
        LeadMagnetDownload.created_at >= week_ago
    ).count()
    
    # Get active sequences count
    active_waitlist = db.query(WaitlistRegistration).filter(
        WaitlistRegistration.sequence_started == True,
        WaitlistRegistration.is_active == True,
        WaitlistRegistration.current_email_index < 12
    ).count()
    active_corporate = db.query(CorporateInquiry).filter(
        CorporateInquiry.sequence_started == True,
        CorporateInquiry.is_active == True,
        CorporateInquiry.current_email_index < 12
    ).count()
    active_lead_magnet = db.query(LeadMagnetDownload).filter(
        LeadMagnetDownload.sequence_started == True,
        LeadMagnetDownload.is_active == True,
        LeadMagnetDownload.current_email_index < 12
    ).count()
    
    return DashboardStats(
        total_waitlist=total_waitlist,
        total_corporate=total_corporate,
        total_lead_magnet=total_lead_magnet,
        total_emails_sent=total_emails_sent,
        new_this_week=new_waitlist + new_corporate + new_lead_magnet,
        active_sequences=active_waitlist + active_corporate + active_lead_magnet
    )

# Waitlist management
@router.get("/waitlist", response_model=List[WaitlistRegistrationResponse])
async def get_waitlist_subscribers(
    skip: int = 0,
    limit: int = 50,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Get all waitlist subscribers"""
    subscribers = db.query(WaitlistRegistration).order_by(
        desc(WaitlistRegistration.created_at)
    ).offset(skip).limit(limit).all()
    
    return subscribers

@router.get("/waitlist/{subscriber_id}", response_model=WaitlistRegistrationResponse)
async def get_waitlist_subscriber(
    subscriber_id: int,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Get specific waitlist subscriber"""
    subscriber = db.query(WaitlistRegistration).filter(
        WaitlistRegistration.id == subscriber_id
    ).first()
    
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    
    return subscriber

@router.put("/waitlist/{subscriber_id}")
async def update_waitlist_subscriber(
    subscriber_id: int,
    update_data: SubscriberUpdate,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Update waitlist subscriber"""
    subscriber = db.query(WaitlistRegistration).filter(
        WaitlistRegistration.id == subscriber_id
    ).first()
    
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    
    # Update fields
    if update_data.is_active is not None:
        subscriber.is_active = update_data.is_active
    if update_data.current_email_index is not None:
        subscriber.current_email_index = update_data.current_email_index
    if update_data.sequence_started is not None:
        subscriber.sequence_started = update_data.sequence_started
    
    db.commit()
    return {"message": "Subscriber updated successfully"}

@router.delete("/waitlist/{subscriber_id}")
async def delete_waitlist_subscriber(
    subscriber_id: int,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Delete waitlist subscriber"""
    subscriber = db.query(WaitlistRegistration).filter(
        WaitlistRegistration.id == subscriber_id
    ).first()
    
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    
    db.delete(subscriber)
    db.commit()
    return {"message": "Subscriber deleted successfully"}

# Corporate inquiry management
@router.get("/corporate", response_model=List[CorporateInquiryResponse])
async def get_corporate_inquiries(
    skip: int = 0,
    limit: int = 50,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Get all corporate inquiries"""
    inquiries = db.query(CorporateInquiry).order_by(
        desc(CorporateInquiry.created_at)
    ).offset(skip).limit(limit).all()
    
    return inquiries

@router.get("/corporate/{inquiry_id}", response_model=CorporateInquiryResponse)
async def get_corporate_inquiry(
    inquiry_id: int,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Get specific corporate inquiry"""
    inquiry = db.query(CorporateInquiry).filter(
        CorporateInquiry.id == inquiry_id
    ).first()
    
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    
    return inquiry

@router.put("/corporate/{inquiry_id}")
async def update_corporate_inquiry(
    inquiry_id: int,
    update_data: SubscriberUpdate,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Update corporate inquiry"""
    inquiry = db.query(CorporateInquiry).filter(
        CorporateInquiry.id == inquiry_id
    ).first()
    
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    
    # Update fields
    if update_data.is_active is not None:
        inquiry.is_active = update_data.is_active
    if update_data.current_email_index is not None:
        inquiry.current_email_index = update_data.current_email_index
    if update_data.sequence_started is not None:
        inquiry.sequence_started = update_data.sequence_started
    
    db.commit()
    return {"message": "Inquiry updated successfully"}

@router.delete("/corporate/{inquiry_id}")
async def delete_corporate_inquiry(
    inquiry_id: int,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Delete corporate inquiry"""
    inquiry = db.query(CorporateInquiry).filter(
        CorporateInquiry.id == inquiry_id
    ).first()
    
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    
    db.delete(inquiry)
    db.commit()
    return {"message": "Inquiry deleted successfully"}

# Lead magnet management
@router.get("/lead-magnet", response_model=List[LeadMagnetResponse])
async def get_lead_magnet_downloads(
    skip: int = 0,
    limit: int = 50,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Get all lead magnet downloads"""
    downloads = db.query(LeadMagnetDownload).order_by(
        desc(LeadMagnetDownload.created_at)
    ).offset(skip).limit(limit).all()
    
    return downloads

@router.get("/lead-magnet/{download_id}", response_model=LeadMagnetResponse)
async def get_lead_magnet_download(
    download_id: int,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Get specific lead magnet download"""
    download = db.query(LeadMagnetDownload).filter(
        LeadMagnetDownload.id == download_id
    ).first()
    
    if not download:
        raise HTTPException(status_code=404, detail="Download not found")
    
    return download

@router.put("/lead-magnet/{download_id}")
async def update_lead_magnet_download(
    download_id: int,
    update_data: SubscriberUpdate,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Update lead magnet download"""
    download = db.query(LeadMagnetDownload).filter(
        LeadMagnetDownload.id == download_id
    ).first()
    
    if not download:
        raise HTTPException(status_code=404, detail="Download not found")
    
    # Update fields
    if update_data.is_active is not None:
        download.is_active = update_data.is_active
    if update_data.current_email_index is not None:
        download.current_email_index = update_data.current_email_index
    if update_data.sequence_started is not None:
        download.sequence_started = update_data.sequence_started
    
    db.commit()
    return {"message": "Download updated successfully"}

@router.delete("/lead-magnet/{download_id}")
async def delete_lead_magnet_download(
    download_id: int,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Delete lead magnet download"""
    download = db.query(LeadMagnetDownload).filter(
        LeadMagnetDownload.id == download_id
    ).first()
    
    if not download:
        raise HTTPException(status_code=404, detail="Download not found")
    
    db.delete(download)
    db.commit()
    return {"message": "Download deleted successfully"}

# Email logs
@router.get("/emails", response_model=List[EmailLogResponse])
async def get_email_logs(
    skip: int = 0,
    limit: int = 100,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Get email logs"""
    logs = db.query(EmailLog).order_by(
        desc(EmailLog.sent_at)
    ).offset(skip).limit(limit).all()
    
    return logs

# Email sequence management
@router.get("/sequences")
async def get_email_sequences(
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Get all email sequences with progress"""
    # Get sequence progress for all subscriber types
    waitlist_progress = db.query(
        WaitlistRegistration.current_email_index,
        func.count(WaitlistRegistration.id).label('count')
    ).filter(
        WaitlistRegistration.sequence_started == True,
        WaitlistRegistration.is_active == True
    ).group_by(WaitlistRegistration.current_email_index).all()
    
    corporate_progress = db.query(
        CorporateInquiry.current_email_index,
        func.count(CorporateInquiry.id).label('count')
    ).filter(
        CorporateInquiry.sequence_started == True,
        CorporateInquiry.is_active == True
    ).group_by(CorporateInquiry.current_email_index).all()
    
    lead_magnet_progress = db.query(
        LeadMagnetDownload.current_email_index,
        func.count(LeadMagnetDownload.id).label('count')
    ).filter(
        LeadMagnetDownload.sequence_started == True,
        LeadMagnetDownload.is_active == True
    ).group_by(LeadMagnetDownload.current_email_index).all()
    
    return {
        "waitlist_magnet_sequence": {
            "name": "12-Week Leadership Development",
            "type": "waitlist_magnet",
            "total_emails": 12,
            "progress": [{"email_index": p.current_email_index, "subscriber_count": p.count} for p in waitlist_progress]
        },
        "corporate_sequence": {
            "name": "12-Week Corporate Leadership",
            "type": "corporate", 
            "total_emails": 12,
            "progress": [{"email_index": p.current_email_index, "subscriber_count": p.count} for p in corporate_progress]
        },
        "lead_magnet_progress": {
            "name": "Lead Magnet Follow-up",
            "type": "lead_magnet",
            "total_emails": 12,
            "progress": [{"email_index": p.current_email_index, "subscriber_count": p.count} for p in lead_magnet_progress]
        }
    }

@router.post("/sequences/{sequence_type}/trigger")
async def trigger_sequence_for_subscriber(
    sequence_type: str,
    subscriber_id: int,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Manually trigger sequence for a specific subscriber"""
    if sequence_type == "waitlist":
        subscriber = db.query(WaitlistRegistration).filter(
            WaitlistRegistration.id == subscriber_id
        ).first()
    elif sequence_type == "corporate":
        subscriber = db.query(CorporateInquiry).filter(
            CorporateInquiry.id == subscriber_id
        ).first()
    elif sequence_type == "lead_magnet":
        subscriber = db.query(LeadMagnetDownload).filter(
            LeadMagnetDownload.id == subscriber_id
        ).first()
    else:
        raise HTTPException(status_code=400, detail="Invalid sequence type")
    
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    
    # Reset sequence for this subscriber
    subscriber.sequence_started = True
    subscriber.current_email_index = 0
    subscriber.last_email_sent_at = datetime.utcnow() - timedelta(days=8)  # Make them eligible for next email
    
    db.commit()
    
    return {"message": f"Sequence reset for subscriber {subscriber_id}"}

@router.post("/sequences/pause-all")
async def pause_all_sequences(
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Pause all email sequences (emergency stop)"""
    # Set all active subscribers to inactive
    db.query(WaitlistRegistration).filter(
        WaitlistRegistration.sequence_started == True
    ).update({"is_active": False})
    
    db.query(CorporateInquiry).filter(
        CorporateInquiry.sequence_started == True
    ).update({"is_active": False})
    
    db.query(LeadMagnetDownload).filter(
        LeadMagnetDownload.sequence_started == True
    ).update({"is_active": False})
    
    db.commit()
    
    return {"message": "All email sequences paused"}

@router.post("/sequences/resume-all")
async def resume_all_sequences(
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Resume all email sequences"""
    # Set all subscribers back to active
    db.query(WaitlistRegistration).filter(
        WaitlistRegistration.sequence_started == True
    ).update({"is_active": True})
    
    db.query(CorporateInquiry).filter(
        CorporateInquiry.sequence_started == True
    ).update({"is_active": True})
    
    db.query(LeadMagnetDownload).filter(
        LeadMagnetDownload.sequence_started == True
    ).update({"is_active": True})
    
    db.commit()
    
    return {"message": "All email sequences resumed"}

# Export data
@router.get("/export/subscribers")
async def export_subscribers(
    format: str = "csv",
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Export all subscriber data"""
    if format != "csv":
        raise HTTPException(status_code=400, detail="Only CSV format supported")
    
    import csv
    import io
    from fastapi.responses import StreamingResponse
    
    def generate_csv():
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow([
            "Type", "Email", "Name/Company", "Created", "Welcome Sent", 
            "Sequence Started", "Current Email Index", "Is Active"
        ])
        
        # Write waitlist data
        waitlist = db.query(WaitlistRegistration).all()
        for w in waitlist:
            writer.writerow([
                "Waitlist", w.email, w.full_name, w.created_at.isoformat(),
                w.welcome_sent, w.sequence_started, w.current_email_index, w.is_active
            ])
        
        # Write corporate data
        corporate = db.query(CorporateInquiry).all()
        for c in corporate:
            writer.writerow([
                "Corporate", c.email, f"{c.contact_person} ({c.company_name})", 
                c.created_at.isoformat(), c.welcome_sent, c.sequence_started, 
                c.current_email_index, c.is_active
            ])
        
        # Write lead magnet data
        lead_magnet = db.query(LeadMagnetDownload).all()
        for l in lead_magnet:
            writer.writerow([
                "Lead Magnet", l.email, l.email, l.created_at.isoformat(),
                l.welcome_sent, l.sequence_started, l.current_email_index, l.is_active
            ])
        
        output.seek(0)
        return output.read()
    
    csv_content = generate_csv()
    
    return StreamingResponse(
        io.StringIO(csv_content),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=subscribers.csv"}
    )

# Manual email sending
@router.post("/send-manual-email")
async def send_manual_email(
    email_request: ManualEmailRequest,
    background_tasks: BackgroundTasks,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Send manual email to selected subscribers"""
    
    def send_emails():
        for subscriber_id in email_request.subscriber_ids:
            try:
                # Get subscriber based on type
                if email_request.subscriber_type == "waitlist":
                    subscriber = db.query(WaitlistRegistration).filter(
                        WaitlistRegistration.id == subscriber_id
                    ).first()
                elif email_request.subscriber_type == "corporate":
                    subscriber = db.query(CorporateInquiry).filter(
                        CorporateInquiry.id == subscriber_id
                    ).first()
                elif email_request.subscriber_type == "lead_magnet":
                    subscriber = db.query(LeadMagnetDownload).filter(
                        LeadMagnetDownload.id == subscriber_id
                    ).first()
                else:
                    continue
                
                if subscriber:
                    # Send email
                    result = sendgrid_service.send_email(
                        to_email=subscriber.email,
                        subject=email_request.subject,
                        html_content=email_request.html_content
                    )
                    
                    # Log email
                    if result.get("success"):
                        email_log = EmailLog(
                            email_type="manual",
                            subject=email_request.subject,
                            recipient_email=subscriber.email,
                            sendgrid_message_id=result.get("message_id")
                        )
                        
                        # Link to appropriate subscriber
                        if email_request.subscriber_type == "waitlist":
                            email_log.waitlist_id = subscriber_id
                        elif email_request.subscriber_type == "corporate":
                            email_log.corporate_id = subscriber_id
                        elif email_request.subscriber_type == "lead_magnet":
                            email_log.lead_magnet_id = subscriber_id
                        
                        db.add(email_log)
                        db.commit()
                        
            except Exception as e:
                print(f"Error sending email to subscriber {subscriber_id}: {str(e)}")
    
    # Add to background tasks
    background_tasks.add_task(send_emails)
    
    return {
        "message": f"Manual email queued for {len(email_request.subscriber_ids)} subscribers",
        "recipient_count": len(email_request.subscriber_ids)
    }

# Blog Post Management
@router.get("/blog-posts", response_model=List[BlogPostListResponse])
async def get_blog_posts_admin(
    skip: int = 0,
    limit: int = 50,
    language: Optional[str] = None,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Get all blog posts for admin management"""
    query = db.query(BlogPost)
    
    if language:
        query = query.filter(BlogPost.language == language)
    
    posts = query.order_by(desc(BlogPost.created_at)).offset(skip).limit(limit).all()
    return posts

@router.get("/blog-posts/{post_id}", response_model=BlogPostResponse)
async def get_blog_post_admin(
    post_id: int,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Get specific blog post for editing"""
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return post

@router.post("/blog-posts", response_model=BlogPostResponse)
async def create_blog_post(
    post_data: BlogPostCreate,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Create new blog post"""
    # Check if slug already exists
    existing = db.query(BlogPost).filter(BlogPost.slug == post_data.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Slug already exists")
    
    blog_post = BlogPost(
        slug=post_data.slug,
        title=post_data.title,
        excerpt=post_data.excerpt,
        content=post_data.content,
        featured_image=post_data.featured_image,
        tags=post_data.tags,
        language=post_data.language,
        translation_id=post_data.translation_id,
        is_published=post_data.is_published,
        published_at=datetime.utcnow() if post_data.is_published else None
    )
    
    db.add(blog_post)
    db.commit()
    db.refresh(blog_post)
    
    return blog_post

@router.put("/blog-posts/{post_id}", response_model=BlogPostResponse)
async def update_blog_post(
    post_id: int,
    post_data: BlogPostUpdate,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Update blog post"""
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    # Check slug uniqueness if changing
    if post_data.slug and post_data.slug != post.slug:
        existing = db.query(BlogPost).filter(BlogPost.slug == post_data.slug).first()
        if existing:
            raise HTTPException(status_code=400, detail="Slug already exists")
    
    # Update fields
    for field, value in post_data.dict(exclude_unset=True).items():
        setattr(post, field, value)
    
    # Update published_at if publishing
    if post_data.is_published and not post.published_at:
        post.published_at = datetime.utcnow()
    elif post_data.is_published == False:
        post.published_at = None
    
    post.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(post)
    
    return post

@router.delete("/blog-posts/{post_id}")
async def delete_blog_post(
    post_id: int,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Delete blog post"""
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    db.delete(post)
    db.commit()
    
    return {"message": "Blog post deleted successfully"}

# Paired Blog Post Management (EN/BG together)
@router.get("/paired-blog-posts")
async def get_paired_blog_posts_admin(
    skip: int = 0,
    limit: int = 50,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Get all blog posts (both single language and multilingual) paired together"""
    # Get single language posts grouped by translation_id
    single_posts = db.query(BlogPost).order_by(desc(BlogPost.created_at)).all()
    
    # Get multilingual posts
    multilingual_posts = db.query(MultilingualBlogPost).order_by(
        desc(MultilingualBlogPost.created_at)
    ).all()
    
    paired_posts = []
    
    # Process multilingual posts (already paired)
    for post in multilingual_posts:
        paired_post = {
            "id": post.id,
            "type": "multilingual",
            "title_en": post.title_en,
            "title_bg": post.title_bg,
            "slug_en": post.slug_en,
            "slug_bg": post.slug_bg,
            "is_published_en": post.is_published_en,
            "is_published_bg": post.is_published_bg,
            "published_at_en": post.published_at_en,
            "published_at_bg": post.published_at_bg,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "featured_image": post.featured_image,
            "has_both_languages": True
        }
        paired_posts.append(paired_post)
    
    # Process single language posts - group by translation_id
    translation_groups = {}
    orphaned_posts = []
    
    for post in single_posts:
        if post.translation_id:
            if post.translation_id not in translation_groups:
                translation_groups[post.translation_id] = {}
            translation_groups[post.translation_id][post.language] = post
        else:
            orphaned_posts.append(post)
    
    # Create paired posts from translation groups
    for translation_id, posts_by_lang in translation_groups.items():
        en_post = posts_by_lang.get('en')
        bg_post = posts_by_lang.get('bg')
        
        # Use English as primary, fallback to Bulgarian
        primary_post = en_post if en_post else bg_post
        
        paired_post = {
            "id": f"paired_{translation_id}",
            "type": "paired_single",
            "translation_id": translation_id,
            "title_en": en_post.title if en_post else None,
            "title_bg": bg_post.title if bg_post else None,
            "slug_en": en_post.slug if en_post else None,
            "slug_bg": bg_post.slug if bg_post else None,
            "is_published_en": en_post.is_published if en_post else False,
            "is_published_bg": bg_post.is_published if bg_post else False,
            "published_at_en": en_post.published_at if en_post else None,
            "published_at_bg": bg_post.published_at if bg_post else None,
            "created_at": primary_post.created_at,
            "updated_at": primary_post.updated_at,
            "featured_image": primary_post.featured_image,
            "has_both_languages": en_post is not None and bg_post is not None,
            "en_post_id": en_post.id if en_post else None,
            "bg_post_id": bg_post.id if bg_post else None
        }
        paired_posts.append(paired_post)
    
    # Add orphaned single posts
    for post in orphaned_posts:
        paired_post = {
            "id": f"single_{post.id}",
            "type": "single",
            "post_id": post.id,
            "title_en": post.title if post.language == 'en' else None,
            "title_bg": post.title if post.language == 'bg' else None,
            "slug_en": post.slug if post.language == 'en' else None,
            "slug_bg": post.slug if post.language == 'bg' else None,
            "is_published_en": post.is_published if post.language == 'en' else False,
            "is_published_bg": post.is_published if post.language == 'bg' else False,
            "published_at_en": post.published_at if post.language == 'en' else None,
            "published_at_bg": post.published_at if post.language == 'bg' else None,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "featured_image": post.featured_image,
            "has_both_languages": False,
            "language": post.language
        }
        paired_posts.append(paired_post)
    
    # Sort by creation date
    paired_posts.sort(key=lambda x: x['created_at'], reverse=True)
    
    return paired_posts[skip:skip+limit]

# Get specific paired blog post for editing
@router.get("/paired-blog-posts/{post_identifier}")
async def get_paired_blog_post_admin(
    post_identifier: str,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Get specific paired blog post for editing"""
    
    if post_identifier.startswith("paired_"):
        # Translation group
        translation_id = post_identifier.replace("paired_", "")
        en_post = db.query(BlogPost).filter(
            BlogPost.translation_id == translation_id,
            BlogPost.language == 'en'
        ).first()
        bg_post = db.query(BlogPost).filter(
            BlogPost.translation_id == translation_id,
            BlogPost.language == 'bg'
        ).first()
        
        return {
            "type": "paired_single",
            "translation_id": translation_id,
            "en_post": en_post.__dict__ if en_post else None,
            "bg_post": bg_post.__dict__ if bg_post else None
        }
    
    elif post_identifier.startswith("single_"):
        # Single orphaned post
        post_id = int(post_identifier.replace("single_", ""))
        post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Blog post not found")
        
        return {
            "type": "single",
            "post": post.__dict__
        }
    
    else:
        # Multilingual post
        post_id = int(post_identifier)
        post = db.query(MultilingualBlogPost).filter(MultilingualBlogPost.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Blog post not found")
        
        return {
            "type": "multilingual",
            "post": {
                "id": post.id,
                "slug_en": post.slug_en,
                "slug_bg": post.slug_bg,
                "title_en": post.title_en,
                "title_bg": post.title_bg,
                "excerpt_en": post.excerpt_en,
                "excerpt_bg": post.excerpt_bg,
                "content_en": post.content_en,
                "content_bg": post.content_bg,
                "tags_en": post.tags_en,
                "tags_bg": post.tags_bg,
                "featured_image": post.featured_image,
                "is_published_en": post.is_published_en,
                "is_published_bg": post.is_published_bg,
                "published_at_en": post.published_at_en,
                "published_at_bg": post.published_at_bg,
                "created_at": post.created_at,
                "updated_at": post.updated_at
            }
        }

# Multilingual Blog Post Management
@router.get("/multilingual-blog-posts", response_model=List[MultilingualBlogPostPublicResponse])
async def get_multilingual_blog_posts_admin(
    skip: int = 0,
    limit: int = 50,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Get all multilingual blog posts for admin management"""
    posts = db.query(MultilingualBlogPost).order_by(
        desc(MultilingualBlogPost.created_at)
    ).offset(skip).limit(limit).all()
    
    # Convert to response format (showing English by default)
    response_posts = []
    for post in posts:
        available_languages = []
        if post.is_published_en or not post.is_published_bg:  # Show EN if available or as fallback
            available_languages.append("en")
        if post.is_published_bg:
            available_languages.append("bg")
        
        response_post = MultilingualBlogPostPublicResponse(
            id=post.id,
            slug=post.slug_en,
            title=post.title_en,
            excerpt=post.excerpt_en,
            content=post.content_en,
            featured_image=post.featured_image,
            tags=post.tags_en,
            language="en",
            available_languages=available_languages,
            is_published=post.is_published_en,
            published_at=post.published_at_en,
            created_at=post.created_at,
            updated_at=post.updated_at
        )
        response_posts.append(response_post)
    
    return response_posts

@router.get("/multilingual-blog-posts/{post_id}")
async def get_multilingual_blog_post_admin(
    post_id: int,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Get specific multilingual blog post for editing"""
    post = db.query(MultilingualBlogPost).filter(MultilingualBlogPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    return {
        "id": post.id,
        "slug_en": post.slug_en,
        "slug_bg": post.slug_bg,
        "title_en": post.title_en,
        "title_bg": post.title_bg,
        "excerpt_en": post.excerpt_en,
        "excerpt_bg": post.excerpt_bg,
        "content_en": post.content_en,
        "content_bg": post.content_bg,
        "tags_en": post.tags_en,
        "tags_bg": post.tags_bg,
        "featured_image": post.featured_image,
        "is_published_en": post.is_published_en,
        "is_published_bg": post.is_published_bg,
        "published_at_en": post.published_at_en,
        "published_at_bg": post.published_at_bg,
        "created_at": post.created_at,
        "updated_at": post.updated_at
    }

@router.post("/multilingual-blog-posts")
async def create_multilingual_blog_post(
    post_data: MultilingualBlogPostCreate,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Create new multilingual blog post"""
    # Check if slugs already exist
    existing_en = db.query(MultilingualBlogPost).filter(
        MultilingualBlogPost.slug_en == post_data.slug_en
    ).first()
    existing_bg = db.query(MultilingualBlogPost).filter(
        MultilingualBlogPost.slug_bg == post_data.slug_bg
    ).first()
    
    if existing_en:
        raise HTTPException(status_code=400, detail="English slug already exists")
    if existing_bg:
        raise HTTPException(status_code=400, detail="Bulgarian slug already exists")
    
    blog_post = MultilingualBlogPost(
        slug_en=post_data.slug_en,
        slug_bg=post_data.slug_bg,
        title_en=post_data.title_en,
        title_bg=post_data.title_bg,
        excerpt_en=post_data.excerpt_en,
        excerpt_bg=post_data.excerpt_bg,
        content_en=post_data.content_en,
        content_bg=post_data.content_bg,
        tags_en=post_data.tags_en,
        tags_bg=post_data.tags_bg,
        featured_image=post_data.featured_image,
        is_published_en=post_data.is_published_en,
        is_published_bg=post_data.is_published_bg,
        published_at_en=datetime.utcnow() if post_data.is_published_en else None,
        published_at_bg=datetime.utcnow() if post_data.is_published_bg else None
    )
    
    db.add(blog_post)
    db.commit()
    db.refresh(blog_post)
    
    return {"message": "Multilingual blog post created successfully", "id": blog_post.id}

@router.put("/multilingual-blog-posts/{post_id}")
async def update_multilingual_blog_post(
    post_id: int,
    post_data: dict,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Update multilingual blog post"""
    post = db.query(MultilingualBlogPost).filter(MultilingualBlogPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    # Update fields
    for field, value in post_data.items():
        if hasattr(post, field):
            setattr(post, field, value)
    
    # Update published_at fields
    if post_data.get('is_published_en') and not post.published_at_en:
        post.published_at_en = datetime.utcnow()
    elif post_data.get('is_published_en') == False:
        post.published_at_en = None
        
    if post_data.get('is_published_bg') and not post.published_at_bg:
        post.published_at_bg = datetime.utcnow()
    elif post_data.get('is_published_bg') == False:
        post.published_at_bg = None
    
    post.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(post)
    
    return {"message": "Multilingual blog post updated successfully"}

@router.delete("/multilingual-blog-posts/{post_id}")
async def delete_multilingual_blog_post(
    post_id: int,
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Delete multilingual blog post"""
    post = db.query(MultilingualBlogPost).filter(MultilingualBlogPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    db.delete(post)
    db.commit()
    
    return {"message": "Multilingual blog post deleted successfully"}

# Blog statistics
@router.get("/blog-stats")
async def get_blog_stats(
    current_admin: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    """Get blog statistics"""
    total_posts = db.query(BlogPost).count()
    published_posts = db.query(BlogPost).filter(BlogPost.is_published == True).count()
    draft_posts = total_posts - published_posts
    
    total_multilingual = db.query(MultilingualBlogPost).count()
    published_en = db.query(MultilingualBlogPost).filter(
        MultilingualBlogPost.is_published_en == True
    ).count()
    published_bg = db.query(MultilingualBlogPost).filter(
        MultilingualBlogPost.is_published_bg == True
    ).count()
    
    return {
        "single_language_posts": {
            "total": total_posts,
            "published": published_posts,
            "drafts": draft_posts
        },
        "multilingual_posts": {
            "total": total_multilingual,
            "published_en": published_en,
            "published_bg": published_bg
        }
    }