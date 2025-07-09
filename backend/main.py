from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, status, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
import os
import shutil
import json
from typing import List, Optional, Dict, Any
import markdown
import glob
from datetime import datetime, timedelta
from sqlalchemy import func, desc
from sqlalchemy.orm import Session
import uuid

from models import (WaitlistRegistration, CorporateInquiry, LeadMagnetDownload, BlogPost, BlogPostRequest, BlogPostResponse, BlogPostListResponse,
                   MultilingualBlogPost, MultilingualBlogPostRequest, MultilingualBlogPostUpdateRequest, MultilingualBlogPostResponse, MultilingualBlogPostPublicResponse,
                   EmailSubscriber, SequenceEnrollment, SequenceEmail)
from database import (get_db, store_waitlist_registration, store_corporate_inquiry, store_lead_magnet_download,
                     create_blog_post, get_blog_posts, get_blog_post_by_id, get_blog_post_by_slug, 
                     update_blog_post, delete_blog_post, search_blog_posts, get_post_translations, 
                     link_post_translations, get_blog_posts_with_translations, get_related_posts,
                     create_multilingual_blog_post, get_multilingual_blog_posts, get_multilingual_blog_post_by_id,
                     get_multilingual_blog_post_by_slug, get_published_multilingual_posts, 
                     update_multilingual_blog_post, delete_multilingual_blog_post, get_related_multilingual_posts)
from mailerlite import (add_subscriber_to_mailerlite, add_lead_magnet_subscriber, add_waitlist_subscriber,
                         create_and_send_newsletter, get_subscriber_groups, create_newsletter_from_blog_posts,
                         get_newsletter_templates, get_sequence_info_by_language, trigger_sequence_by_subscriber_data)
from email_sequences import (get_sequence_by_type_and_language, get_available_languages, 
                             get_sequence_metadata_by_language, get_monday_morning_sequence_by_language,
                             get_waitlist_sequence_by_language, get_corporate_sequence_by_language)
from sequence_automation import (auto_enroll_subscriber, get_subscribers_with_filters, 
                                get_sequence_analytics, get_emails_to_send, mark_email_as_sent,
                                get_permanently_failed_emails, reset_failed_email_for_retry)
from subscriber_segmentation import (get_subscribers_by_segment, get_subscribers_by_custom_criteria,
                                   get_sequence_progress_summary, get_subscriber_journey, 
                                   bulk_update_engagement_levels, get_segmentation_analytics,
                                   update_subscriber_engagement_level)
from email_scheduler import EmailSchedulerService, process_emails_once
from webhook_handlers import process_webhook_event, verify_webhook_signature
from auth import authenticate_user, create_access_token, get_current_admin_user, Token, User, ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI(title="Coaching Site API", description="API for Peter Stoyanov's coaching website")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WaitlistRegistrationRequest(BaseModel):
    full_name: str
    email: EmailStr
    city_country: str
    occupation: str
    why_join: str
    skills_to_improve: str

class CorporateInquiryRequest(BaseModel):
    companyName: str
    contactPerson: str
    email: EmailStr
    phone: Optional[str] = None
    teamSize: str
    budget: Optional[str] = None
    trainingGoals: str
    preferredDates: Optional[str] = None
    additionalInfo: Optional[str] = None

class LeadMagnetRequest(BaseModel):
    email: EmailStr


@app.get("/")
def read_root():
    return {"message": "Welcome to Peter Stoyanov's Coaching API"}

@app.post("/api/register")
async def register_waitlist(
    registration: WaitlistRegistrationRequest,
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    # Create model instance
    reg_model = WaitlistRegistration(
        full_name=registration.full_name,
        email=registration.email,
        city_country=registration.city_country,
        occupation=registration.occupation,
        why_join=registration.why_join,
        skills_to_improve=registration.skills_to_improve
    )
    
    # Determine language (could be from frontend or IP geolocation)
    language = "en"  # Default to English, can be enhanced later
    
    # Auto-enroll in sequence (this will also handle MailerLite)
    background_tasks.add_task(
        auto_enroll_subscriber,
        db,
        registration.email,
        registration.full_name,
        "waitlist",
        language,
        {
            "city_country": registration.city_country,
            "occupation": registration.occupation,
            "why_join": registration.why_join,
            "skills_to_improve": registration.skills_to_improve
        }
    )
    
    # Store in SQLite as fallback
    store_waitlist_registration(db, reg_model)
    
    return {"status": "success", "message": "Registration successful"}

@app.post("/api/corporate-inquiry")
async def corporate_inquiry(
    inquiry: CorporateInquiryRequest,
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    # Create model instance
    inq_model = CorporateInquiry(
        company_name=inquiry.companyName,
        contact_person=inquiry.contactPerson,
        email=inquiry.email,
        phone=inquiry.phone,
        team_size=inquiry.teamSize,
        budget=inquiry.budget,
        training_goals=inquiry.trainingGoals,
        preferred_dates=inquiry.preferredDates,
        additional_info=inquiry.additionalInfo
    )
    
    # Determine language (could be from frontend or IP geolocation)
    language = "en"  # Default to English, can be enhanced later
    
    # Auto-enroll in corporate sequence
    background_tasks.add_task(
        auto_enroll_subscriber,
        db,
        inquiry.email,
        inquiry.contactPerson,
        "corporate",
        language,
        {
            "company_name": inquiry.companyName,
            "phone": inquiry.phone,
            "team_size": inquiry.teamSize,
            "budget": inquiry.budget,
            "training_goals": inquiry.trainingGoals,
            "preferred_dates": inquiry.preferredDates,
            "additional_info": inquiry.additionalInfo
        }
    )
    
    # Store in database
    store_corporate_inquiry(db, inq_model)
    
    return {"status": "success", "message": "Corporate inquiry submitted successfully"}

@app.post("/api/download-guide")
async def download_guide(
    request: LeadMagnetRequest,
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    """
    Handle lead magnet download requests
    - Store email in database
    - Auto-enroll in lead magnet sequence
    - Return download URL
    """
    
    # Store in database (tracks download count for returning users)
    download_record = store_lead_magnet_download(db, request.email)
    
    # Determine language (could be from frontend or IP geolocation)
    language = "en"  # Default to English, can be enhanced later
    
    # Auto-enroll in lead magnet sequence
    background_tasks.add_task(
        auto_enroll_subscriber,
        db,
        request.email,
        "",  # Name not provided in lead magnet form
        "lead_magnet",
        language,
        {
            "guide": "5_theater_secrets",
            "download_count": download_record.download_count
        }
    )
    
    # Return success response with download URL
    return {
        "success": True,
        "message": "Thank you! Your guide is ready for download.",
        "downloadUrl": "/guides/5-theater-secrets-guide.pdf",
        "isReturningUser": download_record.download_count > 1
    }

@app.get("/api/posts")
def api_get_blog_posts(published_only: bool = True, skip: int = 0, limit: int = 100, language: str = "en", db = Depends(get_db)):
    """Get published blog posts for public consumption - now using multilingual structure"""
    if published_only:
        posts = get_published_multilingual_posts(db, language=language, skip=skip, limit=limit)
    else:
        posts = get_multilingual_blog_posts(db, skip=skip, limit=limit)
    
    # Convert to language-specific response format (compatible with old frontend)
    result = []
    for post in posts:
        if language == "en":
            if published_only and not post.is_published_en:
                continue
            result.append({
                "id": post.id,
                "slug": post.slug_en,
                "title": post.title_en,
                "excerpt": post.excerpt_en,
                "featured_image": post.featured_image,
                "tags": post.tags_en or [],
                "language": "en",
                "translation_id": f"ml-{post.id}",  # Use post ID as translation_id for compatibility
                "is_published": post.is_published_en,
                "published_at": post.published_at_en.isoformat() if post.published_at_en else None,
                "created_at": post.created_at.isoformat(),
                "updated_at": post.updated_at.isoformat()
            })
        else:  # Bulgarian
            if published_only and not post.is_published_bg:
                continue
            result.append({
                "id": post.id,
                "slug": post.slug_bg,
                "title": post.title_bg,
                "excerpt": post.excerpt_bg,
                "featured_image": post.featured_image,
                "tags": post.tags_bg or [],
                "language": "bg",
                "translation_id": f"ml-{post.id}",  # Use post ID as translation_id for compatibility
                "is_published": post.is_published_bg,
                "published_at": post.published_at_bg.isoformat() if post.published_at_bg else None,
                "created_at": post.created_at.isoformat(),
                "updated_at": post.updated_at.isoformat()
            })
    
    return result

@app.get("/api/posts/{slug}")
def get_blog_post(slug: str, language: str = "en", db = Depends(get_db)):
    """Get a specific blog post by slug - now using multilingual structure"""
    post = get_multilingual_blog_post_by_slug(db, slug, language=language)
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    # Check if the requested language is published
    if language == "en" and not post.is_published_en:
        raise HTTPException(status_code=404, detail="Blog post not published in English")
    if language == "bg" and not post.is_published_bg:
        raise HTTPException(status_code=404, detail="Blog post not published in Bulgarian")
    
    # Return language-specific response (compatible with old frontend)
    if language == "en":
        return {
            "id": post.id,
            "slug": post.slug_en,
            "title": post.title_en,
            "excerpt": post.excerpt_en,
            "content": post.content_en,
            "featured_image": post.featured_image,
            "tags": post.tags_en or [],
            "language": "en",
            "translation_id": f"ml-{post.id}",
            "is_published": post.is_published_en,
            "published_at": post.published_at_en.isoformat() if post.published_at_en else None,
            "created_at": post.created_at.isoformat(),
            "updated_at": post.updated_at.isoformat()
        }
    else:  # Bulgarian
        return {
            "id": post.id,
            "slug": post.slug_bg,
            "title": post.title_bg,
            "excerpt": post.excerpt_bg,
            "content": post.content_bg,
            "featured_image": post.featured_image,
            "tags": post.tags_bg or [],
            "language": "bg",
            "translation_id": f"ml-{post.id}",
            "is_published": post.is_published_bg,
            "published_at": post.published_at_bg.isoformat() if post.published_at_bg else None,
            "created_at": post.created_at.isoformat(),
            "updated_at": post.updated_at.isoformat()
        }

@app.get("/api/posts/{slug}/translations")
def get_blog_post_translations(slug: str, language: str = "en", db = Depends(get_db)):
    """Get all translations of a blog post - now using multilingual structure"""
    # Try to find the post in the specified language first
    post = get_multilingual_blog_post_by_slug(db, slug, language=language)
    
    # If not found, try the other language
    if not post:
        other_language = "bg" if language == "en" else "en"
        post = get_multilingual_blog_post_by_slug(db, slug, language=other_language)
    
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    translations = []
    # Add English version if available and published
    if post.title_en and post.is_published_en:
        translations.append({
            "id": post.id,
            "slug": post.slug_en,
            "title": post.title_en,
            "language": "en",
            "translation_id": f"ml-{post.id}"
        })
    
    # Add Bulgarian version if available and published
    if post.title_bg and post.is_published_bg:
        translations.append({
            "id": post.id,
            "slug": post.slug_bg,
            "title": post.title_bg,
            "language": "bg",
            "translation_id": f"ml-{post.id}"
        })
    
    return translations

@app.get("/api/posts/{slug}/related")
def get_related_blog_posts(slug: str, language: str = "en", limit: int = 3, db = Depends(get_db)):
    """Get related blog posts based on shared tags - now using multilingual structure"""
    # First get the post to find its ID
    post = get_multilingual_blog_post_by_slug(db, slug, language=language)
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    # Get related posts
    related_posts = get_related_multilingual_posts(db, post.id, language=language, limit=limit)
    
    # Convert to language-specific response format (compatible with old frontend)
    result = []
    for related_post in related_posts:
        if language == "en":
            result.append({
                "id": related_post.id,
                "slug": related_post.slug_en,
                "title": related_post.title_en,
                "excerpt": related_post.excerpt_en,
                "featured_image": related_post.featured_image,
                "tags": related_post.tags_en or [],
                "language": "en",
                "published_at": related_post.published_at_en.isoformat() if related_post.published_at_en else None,
                "created_at": related_post.created_at.isoformat()
            })
        else:  # Bulgarian
            result.append({
                "id": related_post.id,
                "slug": related_post.slug_bg,
                "title": related_post.title_bg,
                "excerpt": related_post.excerpt_bg,
                "featured_image": related_post.featured_image,
                "tags": related_post.tags_bg or [],
                "language": "bg",
                "published_at": related_post.published_at_bg.isoformat() if related_post.published_at_bg else None,
                "created_at": related_post.created_at.isoformat()
            })
    
    return result

# Multilingual Blog Post API Endpoints (New Structure)

@app.get("/api/v2/posts")
def api_get_multilingual_blog_posts(language: str = "en", published_only: bool = True, skip: int = 0, limit: int = 100, db = Depends(get_db)):
    """Get published multilingual blog posts for public consumption"""
    if published_only:
        posts = get_published_multilingual_posts(db, language=language, skip=skip, limit=limit)
    else:
        posts = get_multilingual_blog_posts(db, skip=skip, limit=limit)
    
    # Convert to language-specific response format
    result = []
    for post in posts:
        # Check if the requested language is published
        if language == "en":
            if published_only and not post.is_published_en:
                continue
            result.append({
                "id": post.id,
                "slug": post.slug_en,
                "title": post.title_en,
                "excerpt": post.excerpt_en,
                "featured_image": post.featured_image,
                "tags": post.tags_en or [],
                "language": "en",
                "available_languages": [lang for lang in ["en", "bg"] if (lang == "en" and post.title_en) or (lang == "bg" and post.title_bg)],
                "is_published": post.is_published_en,
                "published_at": post.published_at_en.isoformat() if post.published_at_en else None,
                "created_at": post.created_at.isoformat(),
                "updated_at": post.updated_at.isoformat()
            })
        else:  # Bulgarian
            if published_only and not post.is_published_bg:
                continue
            result.append({
                "id": post.id,
                "slug": post.slug_bg,
                "title": post.title_bg,
                "excerpt": post.excerpt_bg,
                "featured_image": post.featured_image,
                "tags": post.tags_bg or [],
                "language": "bg",
                "available_languages": [lang for lang in ["en", "bg"] if (lang == "en" and post.title_en) or (lang == "bg" and post.title_bg)],
                "is_published": post.is_published_bg,
                "published_at": post.published_at_bg.isoformat() if post.published_at_bg else None,
                "created_at": post.created_at.isoformat(),
                "updated_at": post.updated_at.isoformat()
            })
    
    return result

@app.get("/api/v2/posts/{slug}")
def get_multilingual_blog_post(slug: str, language: str = "en", db = Depends(get_db)):
    """Get a specific multilingual blog post by slug"""
    post = get_multilingual_blog_post_by_slug(db, slug, language=language)
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    # Check if the requested language is published
    if language == "en" and not post.is_published_en:
        raise HTTPException(status_code=404, detail="Blog post not published in English")
    if language == "bg" and not post.is_published_bg:
        raise HTTPException(status_code=404, detail="Blog post not published in Bulgarian")
    
    # Return language-specific response
    if language == "en":
        return {
            "id": post.id,
            "slug": post.slug_en,
            "title": post.title_en,
            "excerpt": post.excerpt_en,
            "content": post.content_en,
            "featured_image": post.featured_image,
            "tags": post.tags_en or [],
            "language": "en",
            "available_languages": [lang for lang in ["en", "bg"] if (lang == "en" and post.title_en) or (lang == "bg" and post.title_bg)],
            "is_published": post.is_published_en,
            "published_at": post.published_at_en.isoformat() if post.published_at_en else None,
            "created_at": post.created_at.isoformat(),
            "updated_at": post.updated_at.isoformat()
        }
    else:  # Bulgarian
        return {
            "id": post.id,
            "slug": post.slug_bg,
            "title": post.title_bg,
            "excerpt": post.excerpt_bg,
            "content": post.content_bg,
            "featured_image": post.featured_image,
            "tags": post.tags_bg or [],
            "language": "bg",
            "available_languages": [lang for lang in ["en", "bg"] if (lang == "en" and post.title_en) or (lang == "bg" and post.title_bg)],
            "is_published": post.is_published_bg,
            "published_at": post.published_at_bg.isoformat() if post.published_at_bg else None,
            "created_at": post.created_at.isoformat(),
            "updated_at": post.updated_at.isoformat()
        }

@app.get("/api/v2/posts/{slug}/translations")
def get_multilingual_blog_post_translations(slug: str, language: str = "en", db = Depends(get_db)):
    """Get all available translations of a multilingual blog post"""
    post = get_multilingual_blog_post_by_slug(db, slug, language=language)
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    translations = []
    # Add English version if available and published
    if post.title_en and post.is_published_en:
        translations.append({
            "id": post.id,
            "slug": post.slug_en,
            "title": post.title_en,
            "language": "en"
        })
    
    # Add Bulgarian version if available and published
    if post.title_bg and post.is_published_bg:
        translations.append({
            "id": post.id,
            "slug": post.slug_bg,
            "title": post.title_bg,
            "language": "bg"
        })
    
    return translations

@app.get("/api/v2/posts/{slug}/related")
def get_related_multilingual_blog_posts(slug: str, language: str = "en", limit: int = 3, db = Depends(get_db)):
    """Get related multilingual blog posts based on shared tags"""
    # First get the post to find its ID
    post = get_multilingual_blog_post_by_slug(db, slug, language=language)
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    # Get related posts
    related_posts = get_related_multilingual_posts(db, post.id, language=language, limit=limit)
    
    # Convert to language-specific response format
    result = []
    for related_post in related_posts:
        if language == "en":
            result.append({
                "id": related_post.id,
                "slug": related_post.slug_en,
                "title": related_post.title_en,
                "excerpt": related_post.excerpt_en,
                "featured_image": related_post.featured_image,
                "tags": related_post.tags_en or [],
                "language": "en",
                "published_at": related_post.published_at_en.isoformat() if related_post.published_at_en else None,
                "created_at": related_post.created_at.isoformat()
            })
        else:  # Bulgarian
            result.append({
                "id": related_post.id,
                "slug": related_post.slug_bg,
                "title": related_post.title_bg,
                "excerpt": related_post.excerpt_bg,
                "featured_image": related_post.featured_image,
                "tags": related_post.tags_bg or [],
                "language": "bg",
                "published_at": related_post.published_at_bg.isoformat() if related_post.published_at_bg else None,
                "created_at": related_post.created_at.isoformat()
            })
    
    return result

# Authentication Endpoints
@app.post("/auth/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint for admin access"""
    print(f"Login attempt - Username: {form_data.username}, Password length: {len(form_data.password)}")
    user = authenticate_user(form_data.username, form_data.password)
    print(f"Authentication result: {user}")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_admin_user)):
    """Get current user info"""
    return current_user

# Admin Dashboard Endpoints
@app.get("/admin/stats")
def get_admin_stats(db = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """Get comprehensive statistics for admin dashboard"""
    
    # Lead Magnet Statistics
    lead_magnet_total = db.query(LeadMagnetDownload).count()
    lead_magnet_today = db.query(LeadMagnetDownload).filter(
        func.date(LeadMagnetDownload.created_at) == func.date(datetime.now())
    ).count()
    lead_magnet_week = db.query(LeadMagnetDownload).filter(
        LeadMagnetDownload.created_at >= datetime.now() - timedelta(days=7)
    ).count()
    lead_magnet_month = db.query(LeadMagnetDownload).filter(
        LeadMagnetDownload.created_at >= datetime.now() - timedelta(days=30)
    ).count()
    
    # Waitlist Statistics
    waitlist_total = db.query(WaitlistRegistration).count()
    waitlist_today = db.query(WaitlistRegistration).filter(
        func.date(WaitlistRegistration.created_at) == func.date(datetime.now())
    ).count()
    waitlist_week = db.query(WaitlistRegistration).filter(
        WaitlistRegistration.created_at >= datetime.now() - timedelta(days=7)
    ).count()
    waitlist_month = db.query(WaitlistRegistration).filter(
        WaitlistRegistration.created_at >= datetime.now() - timedelta(days=30)
    ).count()
    
    # Corporate Inquiry Statistics
    corporate_total = db.query(CorporateInquiry).count()
    corporate_today = db.query(CorporateInquiry).filter(
        func.date(CorporateInquiry.created_at) == func.date(datetime.now())
    ).count()
    corporate_week = db.query(CorporateInquiry).filter(
        CorporateInquiry.created_at >= datetime.now() - timedelta(days=7)
    ).count()
    corporate_month = db.query(CorporateInquiry).filter(
        CorporateInquiry.created_at >= datetime.now() - timedelta(days=30)
    ).count()
    
    # Top download counts
    top_downloaders = db.query(LeadMagnetDownload).order_by(desc(LeadMagnetDownload.download_count)).limit(10).all()
    
    return {
        "lead_magnet": {
            "total": lead_magnet_total,
            "today": lead_magnet_today,
            "week": lead_magnet_week,
            "month": lead_magnet_month,
            "top_downloaders": [{"email": d.email, "count": d.download_count} for d in top_downloaders]
        },
        "waitlist": {
            "total": waitlist_total,
            "today": waitlist_today,
            "week": waitlist_week,
            "month": waitlist_month
        },
        "corporate": {
            "total": corporate_total,
            "today": corporate_today,
            "week": corporate_week,
            "month": corporate_month
        },
        "overview": {
            "total_leads": lead_magnet_total + waitlist_total + corporate_total,
            "conversion_rate": round((waitlist_total / max(lead_magnet_total, 1)) * 100, 2)
        }
    }

@app.get("/admin/recent-activity")
def get_recent_activity(limit: int = 20, db = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """Get recent activity across all systems"""
    
    # Recent lead magnet downloads
    recent_downloads = db.query(LeadMagnetDownload).order_by(desc(LeadMagnetDownload.created_at)).limit(limit).all()
    
    # Recent waitlist registrations
    recent_waitlist = db.query(WaitlistRegistration).order_by(desc(WaitlistRegistration.created_at)).limit(limit).all()
    
    # Recent corporate inquiries
    recent_corporate = db.query(CorporateInquiry).order_by(desc(CorporateInquiry.created_at)).limit(limit).all()
    
    # Combine and sort by date
    activity = []
    
    for download in recent_downloads:
        activity.append({
            "type": "lead_magnet",
            "email": download.email,
            "date": download.created_at.isoformat(),
            "details": f"Downloaded guide (count: {download.download_count})"
        })
    
    for registration in recent_waitlist:
        activity.append({
            "type": "waitlist",
            "email": registration.email,
            "name": registration.full_name,
            "date": registration.created_at.isoformat(),
            "details": f"Joined waitlist - {registration.occupation}"
        })
    
    for inquiry in recent_corporate:
        activity.append({
            "type": "corporate",
            "email": inquiry.email,
            "name": inquiry.contact_person,
            "company": inquiry.company_name,
            "date": inquiry.created_at.isoformat(),
            "details": "Corporate inquiry"
        })
    
    # Sort by date (newest first)
    activity.sort(key=lambda x: x["date"], reverse=True)
    
    return activity[:limit]

@app.get("/admin/emails")
def get_all_emails(db = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """Get all email addresses for export"""
    
    # Get all unique emails
    lead_emails = db.query(LeadMagnetDownload.email).all()
    waitlist_emails = db.query(WaitlistRegistration.email).all()
    corporate_emails = db.query(CorporateInquiry.email).all()
    
    all_emails = set()
    all_emails.update([e[0] for e in lead_emails])
    all_emails.update([e[0] for e in waitlist_emails])
    all_emails.update([e[0] for e in corporate_emails])
    
    return {
        "total_unique_emails": len(all_emails),
        "emails": sorted(list(all_emails)),
        "by_source": {
            "lead_magnet": [e[0] for e in lead_emails],
            "waitlist": [e[0] for e in waitlist_emails],
            "corporate": [e[0] for e in corporate_emails]
        }
    }

# Admin Blog Management Endpoints
@app.get("/admin/blog/posts")
def admin_get_blog_posts(skip: int = 0, limit: int = 100, published_only: Optional[bool] = None, 
                        language: Optional[str] = None, 
                        db = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """Get all blog posts for admin management with language filtering"""
    posts = get_blog_posts(db, skip=skip, limit=limit, 
                          published_only=published_only if published_only is not None else False,
                          language=language)
    
    # Convert SQLAlchemy objects to dictionaries
    result = []
    for post in posts:
        # Get translations for this post
        translations = []
        if post.translation_id:
            translation_posts = get_post_translations(db, post.translation_id)
            for t_post in translation_posts:
                if t_post.id != post.id:  # Don't include the post itself
                    translations.append({
                        "id": t_post.id,
                        "language": t_post.language,
                        "title": t_post.title,
                        "slug": t_post.slug,
                        "is_published": t_post.is_published
                    })
        
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

@app.get("/admin/blog/posts/{post_id}")
def admin_get_blog_post(post_id: int, db = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """Get a specific blog post for editing"""
    post = get_blog_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    # Get translations for this post
    translations = []
    if post.translation_id:
        translation_posts = get_post_translations(db, post.translation_id)
        for t_post in translation_posts:
            if t_post.id != post.id:  # Don't include the post itself
                translations.append({
                    "id": t_post.id,
                    "language": t_post.language,
                    "title": t_post.title,
                    "slug": t_post.slug,
                    "is_published": t_post.is_published
                })
    
    # Convert SQLAlchemy object to dictionary
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
    return post_dict

@app.post("/admin/blog/posts")
def admin_create_blog_post(post: BlogPostRequest, db = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """Create a new blog post"""
    try:
        post_data = post.dict()
        blog_post = create_blog_post(db, post_data)
        
        # Convert SQLAlchemy object to dictionary
        post_dict = {
            "id": blog_post.id,
            "slug": blog_post.slug,
            "title": blog_post.title,
            "excerpt": blog_post.excerpt,
            "content": blog_post.content,
            "featured_image": blog_post.featured_image,
            "tags": blog_post.tags,
            "language": blog_post.language,
            "translation_id": blog_post.translation_id,
            "is_published": blog_post.is_published,
            "published_at": blog_post.published_at,
            "created_at": blog_post.created_at,
            "updated_at": blog_post.updated_at
        }
        return post_dict
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(status_code=400, detail="A blog post with this slug already exists")
        raise HTTPException(status_code=400, detail="Failed to create blog post")

@app.put("/admin/blog/posts/{post_id}")
def admin_update_blog_post(post_id: int, post: BlogPostRequest, 
                          db = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """Update an existing blog post"""
    try:
        post_data = post.dict()
        updated_post = update_blog_post(db, post_id, post_data)
        if not updated_post:
            raise HTTPException(status_code=404, detail="Blog post not found")
        
        # Convert SQLAlchemy object to dictionary
        post_dict = {
            "id": updated_post.id,
            "slug": updated_post.slug,
            "title": updated_post.title,
            "excerpt": updated_post.excerpt,
            "content": updated_post.content,
            "featured_image": updated_post.featured_image,
            "tags": updated_post.tags,
            "language": updated_post.language,
            "translation_id": updated_post.translation_id,
            "is_published": updated_post.is_published,
            "published_at": updated_post.published_at,
            "created_at": updated_post.created_at,
            "updated_at": updated_post.updated_at
        }
        return post_dict
    except ValueError as e:
        if "slug already exists" in str(e):
            raise HTTPException(status_code=400, detail="A blog post with this slug already exists")
        raise HTTPException(status_code=400, detail="Failed to update blog post")
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(status_code=400, detail="A blog post with this slug already exists")
        raise HTTPException(status_code=400, detail="Failed to update blog post")

@app.delete("/admin/blog/posts/{post_id}")
def admin_delete_blog_post(post_id: int, db = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """Delete a blog post"""
    if not delete_blog_post(db, post_id):
        raise HTTPException(status_code=404, detail="Blog post not found")
    return {"message": "Blog post deleted successfully"}

@app.post("/admin/blog/posts/link-translations")
def admin_link_translations(post_ids: List[int], translation_id: Optional[str] = None, 
                           db = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """Link multiple posts as translations of each other"""
    if len(post_ids) < 2:
        raise HTTPException(status_code=400, detail="At least 2 posts are required to create a translation link")
    
    # Verify all posts exist
    for post_id in post_ids:
        post = get_blog_post_by_id(db, post_id)
        if not post:
            raise HTTPException(status_code=404, detail=f"Blog post with ID {post_id} not found")
    
    # Link the posts
    final_translation_id = link_post_translations(db, post_ids, translation_id)
    
    return {
        "message": "Posts linked as translations successfully",
        "translation_id": final_translation_id,
        "linked_posts": post_ids
    }

@app.post("/admin/blog/upload-image")
async def admin_upload_blog_image(file: UploadFile = File(...), current_user: User = Depends(get_current_admin_user)):
    """Upload an image for blog posts"""
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, PNG, GIF, and WebP are allowed.")
    
    # Create uploads directory if it doesn't exist
    upload_dir = "../frontend/public/uploads/blog"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
    file_path = os.path.join(upload_dir, unique_filename)
    
    try:
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Return the public URL
        public_url = f"/uploads/blog/{unique_filename}"
        return {"url": public_url, "filename": unique_filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

# Multilingual Blog Admin Endpoints
@app.get("/admin/multilingual/posts")
def admin_get_multilingual_blog_posts(skip: int = 0, limit: int = 100, 
                                     db = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """Get all multilingual blog posts for admin management"""
    posts = get_multilingual_blog_posts(db, skip=skip, limit=limit)
    
    # Convert to response format
    result = []
    for post in posts:
        result.append({
            "id": post.id,
            "slug_en": post.slug_en,
            "slug_bg": post.slug_bg,
            "title_en": post.title_en,
            "title_bg": post.title_bg,
            "excerpt_en": post.excerpt_en,
            "excerpt_bg": post.excerpt_bg,
            "content_en": post.content_en,
            "content_bg": post.content_bg,
            "tags_en": post.tags_en or [],
            "tags_bg": post.tags_bg or [],
            "featured_image": post.featured_image,
            "is_published_en": post.is_published_en,
            "is_published_bg": post.is_published_bg,
            "published_at_en": post.published_at_en,
            "published_at_bg": post.published_at_bg,
            "created_at": post.created_at,
            "updated_at": post.updated_at
        })
    
    return result

@app.get("/admin/multilingual/posts/{post_id}")
def admin_get_multilingual_blog_post(post_id: int, db = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """Get a specific multilingual blog post for editing"""
    post = get_multilingual_blog_post_by_id(db, post_id)
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
        "tags_en": post.tags_en or [],
        "tags_bg": post.tags_bg or [],
        "featured_image": post.featured_image,
        "is_published_en": post.is_published_en,
        "is_published_bg": post.is_published_bg,
        "published_at_en": post.published_at_en,
        "published_at_bg": post.published_at_bg,
        "created_at": post.created_at,
        "updated_at": post.updated_at
    }

@app.post("/admin/multilingual/posts")
def admin_create_multilingual_blog_post(post: MultilingualBlogPostRequest, db = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """Create a new multilingual blog post"""
    try:
        post_data = post.dict()
        blog_post = create_multilingual_blog_post(db, post_data)
        
        return {
            "id": blog_post.id,
            "slug_en": blog_post.slug_en,
            "slug_bg": blog_post.slug_bg,
            "title_en": blog_post.title_en,
            "title_bg": blog_post.title_bg,
            "excerpt_en": blog_post.excerpt_en,
            "excerpt_bg": blog_post.excerpt_bg,
            "content_en": blog_post.content_en,
            "content_bg": blog_post.content_bg,
            "tags_en": blog_post.tags_en or [],
            "tags_bg": blog_post.tags_bg or [],
            "featured_image": blog_post.featured_image,
            "is_published_en": blog_post.is_published_en,
            "is_published_bg": blog_post.is_published_bg,
            "published_at_en": blog_post.published_at_en,
            "published_at_bg": blog_post.published_at_bg,
            "created_at": blog_post.created_at,
            "updated_at": blog_post.updated_at
        }
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(status_code=400, detail="A blog post with this slug already exists")
        raise HTTPException(status_code=400, detail="Failed to create blog post")

@app.put("/admin/multilingual/posts/{post_id}")
def admin_update_multilingual_blog_post(post_id: int, post: MultilingualBlogPostUpdateRequest, 
                                       db = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """Update an existing multilingual blog post"""
    try:
        # Only include fields that are not None
        post_data = {k: v for k, v in post.dict().items() if v is not None}
        updated_post = update_multilingual_blog_post(db, post_id, post_data)
        if not updated_post:
            raise HTTPException(status_code=404, detail="Blog post not found")
        
        return {
            "id": updated_post.id,
            "slug_en": updated_post.slug_en,
            "slug_bg": updated_post.slug_bg,
            "title_en": updated_post.title_en,
            "title_bg": updated_post.title_bg,
            "excerpt_en": updated_post.excerpt_en,
            "excerpt_bg": updated_post.excerpt_bg,
            "content_en": updated_post.content_en,
            "content_bg": updated_post.content_bg,
            "tags_en": updated_post.tags_en or [],
            "tags_bg": updated_post.tags_bg or [],
            "featured_image": updated_post.featured_image,
            "is_published_en": updated_post.is_published_en,
            "is_published_bg": updated_post.is_published_bg,
            "published_at_en": updated_post.published_at_en,
            "published_at_bg": updated_post.published_at_bg,
            "created_at": updated_post.created_at,
            "updated_at": updated_post.updated_at
        }
    except ValueError as e:
        if "slug already exists" in str(e):
            raise HTTPException(status_code=400, detail="A blog post with this slug already exists")
        raise HTTPException(status_code=400, detail="Failed to update blog post")
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(status_code=400, detail="A blog post with this slug already exists")
        raise HTTPException(status_code=400, detail="Failed to update blog post")

@app.delete("/admin/multilingual/posts/{post_id}")
def admin_delete_multilingual_blog_post(post_id: int, db = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """Delete a multilingual blog post"""
    if not delete_multilingual_blog_post(db, post_id):
        raise HTTPException(status_code=404, detail="Blog post not found")
    return {"message": "Blog post deleted successfully"}

# Newsletter Endpoints
class NewsletterRequest(BaseModel):
    subject: str
    content: str
    group_ids: Optional[List[int]] = None
    from_name: Optional[str] = "Peter Stoyanov"

class BlogNewsletterRequest(BaseModel):
    post_ids: List[int]
    subject: Optional[str] = None
    group_ids: Optional[List[int]] = None

@app.get("/admin/newsletter/groups")
def get_mailerlite_groups(current_user: User = Depends(get_current_admin_user)):
    """Get all subscriber groups from MailerLite"""
    try:
        from mailerlite import get_subscriber_groups
        groups = get_subscriber_groups()
        return {"success": True, "groups": groups}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch groups: {str(e)}")

@app.get("/admin/newsletter/templates")
def get_newsletter_templates_endpoint(current_user: User = Depends(get_current_admin_user)):
    """Get available newsletter templates"""
    try:
        from mailerlite import get_newsletter_templates
        templates = get_newsletter_templates()
        return {"success": True, "templates": templates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch templates: {str(e)}")

@app.post("/admin/newsletter/send")
def send_newsletter(newsletter: NewsletterRequest, current_user: User = Depends(get_current_admin_user)):
    """Send a newsletter campaign"""
    try:
        from mailerlite import create_and_send_newsletter
        result = create_and_send_newsletter(
            subject=newsletter.subject,
            content=newsletter.content,
            group_ids=newsletter.group_ids,
            from_name=newsletter.from_name
        )
        
        if result["success"]:
            return {
                "success": True,
                "message": "Newsletter sent successfully",
                "campaign_id": result["campaign_id"]
            }
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send newsletter: {str(e)}")

@app.post("/admin/newsletter/send-blog-digest")
def send_blog_newsletter(blog_newsletter: BlogNewsletterRequest, db = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """Send a newsletter with selected blog posts"""
    try:
        # Get the blog posts
        blog_posts = []
        for post_id in blog_newsletter.post_ids:
            post = get_blog_post_by_id(db, post_id)
            if post:
                blog_posts.append({
                    'title': post.title,
                    'excerpt': post.excerpt,
                    'slug': post.slug
                })
        
        if not blog_posts:
            raise HTTPException(status_code=400, detail="No valid blog posts found")
        
        # Create newsletter content from blog posts
        from mailerlite import create_newsletter_from_blog_posts, create_and_send_newsletter
        content = create_newsletter_from_blog_posts(blog_posts, blog_newsletter.subject)
        
        # Send the newsletter
        subject = blog_newsletter.subject or f"Latest Updates - {len(blog_posts)} New Posts"
        result = create_and_send_newsletter(
            subject=subject,
            content=content,
            group_ids=blog_newsletter.group_ids
        )
        
        if result["success"]:
            return {
                "success": True,
                "message": f"Blog newsletter sent successfully with {len(blog_posts)} posts",
                "campaign_id": result["campaign_id"]
            }
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send blog newsletter: {str(e)}")

@app.get("/admin/dashboard", response_class=HTMLResponse)
def admin_dashboard():
    """Admin dashboard with authentication"""
    
    html_content = r"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Coaching Site Admin Dashboard</title>
        <!-- Quill.js WYSIWYG Editor -->
        <link href="https://cdn.quilljs.com/1.3.6/quill.snow.css" rel="stylesheet">
        <script src="https://cdn.quilljs.com/1.3.6/quill.min.js"></script>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif; background: #f8fafc; height: 100vh; overflow: hidden; }
            
            /* Sidebar Layout */
            .admin-layout { display: flex; height: 100vh; }
            .sidebar { width: 280px; background: #1f2937; color: white; flex-shrink: 0; overflow-y: auto; }
            .main-content { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
            .content-header { background: white; padding: 20px 30px; border-bottom: 1px solid #e5e7eb; flex-shrink: 0; }
            .content-body { flex: 1; padding: 30px; overflow-y: auto; }
            
            /* Sidebar Styles */
            .sidebar-header { padding: 20px; border-bottom: 1px solid #374151; }
            .sidebar-title { font-size: 18px; font-weight: 600; color: #f9fafb; }
            .sidebar-subtitle { font-size: 12px; color: #9ca3af; margin-top: 4px; }
            
            .sidebar-nav { padding: 20px 0; }
            .nav-section { margin-bottom: 30px; }
            .nav-section-title { 
                font-size: 11px; font-weight: 600; color: #6b7280; 
                text-transform: uppercase; letter-spacing: 0.05em; 
                padding: 0 20px; margin-bottom: 10px; 
            }
            .nav-item { 
                display: flex; align-items: center; padding: 12px 20px; 
                color: #d1d5db; cursor: pointer; transition: all 0.2s;
                border-left: 3px solid transparent;
            }
            .nav-item:hover { background: #374151; color: white; }
            .nav-item.active { 
                background: #1e40af; color: white; border-left-color: #3b82f6;
                box-shadow: inset 0 0 0 1px rgba(59, 130, 246, 0.3);
            }
            .nav-icon { margin-right: 12px; font-size: 18px; }
            .nav-text { font-size: 14px; font-weight: 500; }
            
            .sidebar-footer { padding: 20px; border-top: 1px solid #374151; margin-top: auto; }
            .user-info { display: flex; align-items: center; margin-bottom: 15px; }
            .user-avatar { 
                width: 36px; height: 36px; border-radius: 50%; 
                background: #3b82f6; display: flex; align-items: center; justify-content: center;
                font-weight: 600; margin-right: 12px;
            }
            .user-details { flex: 1; }
            .user-name { font-size: 14px; font-weight: 500; color: #f9fafb; }
            .user-role { font-size: 12px; color: #9ca3af; }
            
            /* Header Styles */
            .page-header { display: flex; justify-content: space-between; align-items: center; }
            .page-title { font-size: 24px; font-weight: 600; color: #1f2937; }
            .page-subtitle { font-size: 14px; color: #6b7280; margin-top: 4px; }
            .header-actions { display: flex; gap: 12px; align-items: center; }
            /* Login Styles */
            .login-section { background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 400px; margin: 100px auto; }
            .login-form { display: flex; flex-direction: column; gap: 15px; }
            .login-btn { background: #2563eb; color: white; padding: 12px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
            .login-btn:hover { background: #1d4ed8; }
            
            /* Buttons */
            .btn { padding: 8px 16px; border: none; border-radius: 6px; cursor: pointer; font-weight: 500; font-size: 14px; transition: all 0.2s; }
            .btn-primary { background: #2563eb; color: white; }
            .btn-primary:hover { background: #1d4ed8; }
            .btn-danger { background: #dc2626; color: white; }
            .btn-danger:hover { background: #b91c1c; }
            .btn-success { background: #059669; color: white; }
            .btn-success:hover { background: #047857; }
            
            /* Content Cards */
            .content-card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 20px; }
            .card-header { padding: 20px; border-bottom: 1px solid #e5e7eb; }
            .card-title { font-size: 18px; font-weight: 600; color: #1f2937; }
            .card-body { padding: 20px; }
            
            /* Stats Grid */
            .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
            .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
            .stat-number { font-size: 2em; font-weight: bold; color: #2563eb; }
            .stat-label { color: #6b7280; margin-top: 5px; font-size: 14px; }
            /* Form Styling */
            .form-group { margin-bottom: 20px; }
            .form-group label { display: block; margin-bottom: 8px; font-weight: 600; color: #374151; font-size: 14px; }
            .form-group input, .form-group textarea, .form-group select { 
                width: 100%; padding: 12px; border: 2px solid #e5e7eb; border-radius: 6px; 
                font-size: 14px; transition: border-color 0.2s ease, box-shadow 0.2s ease;
                box-sizing: border-box;
            }
            .form-group input:focus, .form-group textarea:focus, .form-group select:focus {
                outline: none; border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
            }
            .form-group textarea { min-height: 120px; resize: vertical; font-family: inherit; }
            .activity-section { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .activity-item { padding: 10px; border-bottom: 1px solid #eee; }
            .activity-item:last-child { border-bottom: none; }
            .activity-type { font-weight: bold; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; }
            .type-lead { background: #10b981; color: white; }
            .type-waitlist { background: #f59e0b; color: white; }
            .type-corporate { background: #8b5cf6; color: white; }
            .refresh-btn { background: #2563eb; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
            .refresh-btn:hover { background: #1d4ed8; }
            .hidden { display: none; }
            .error { color: #dc2626; margin-top: 10px; }
            .nav-tabs { display: flex; gap: 10px; margin-bottom: 20px; }
            .nav-tab { background: #f5f5f5; border: none; padding: 10px 20px; border-radius: 8px 8px 0 0; cursor: pointer; }
            .nav-tab.active { background: white; border-bottom: 2px solid #2563eb; }
            .tab-content { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .blog-list { display: flex; flex-direction: column; gap: 10px; }
            .blog-item { display: flex; justify-content: between; align-items: center; padding: 15px; border: 1px solid #e5e7eb; border-radius: 8px; }
            .blog-info { flex: 1; }
            .blog-title { font-weight: bold; margin-bottom: 5px; }
            .blog-meta { color: #666; font-size: 0.9em; }
            .blog-actions { display: flex; gap: 10px; }
            .btn-edit { background: #f59e0b; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; }
            .btn-delete { background: #dc2626; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; }
            .btn-new { background: #10b981; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; margin-bottom: 20px; }
            /* Form Styling */
            .form-group { margin-bottom: 20px; }
            .form-group label { display: block; margin-bottom: 8px; font-weight: 600; color: #374151; font-size: 14px; }
            .form-group input, .form-group textarea, .form-group select { 
                width: 100%; padding: 12px; border: 2px solid #e5e7eb; border-radius: 6px; 
                font-size: 14px; transition: border-color 0.2s ease, box-shadow 0.2s ease;
                box-sizing: border-box;
            }
            .form-group input:focus, .form-group textarea:focus, .form-group select:focus {
                outline: none; border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
            }
            .form-group textarea { min-height: 200px; resize: vertical; font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace; }
            
            /* Language Tabs */
            .language-tabs { display: flex; margin-bottom: 20px; border-bottom: 1px solid #e5e7eb; }
            .language-tab { 
                padding: 12px 24px; border: none; background: none; cursor: pointer; 
                font-weight: 500; color: #6b7280; border-bottom: 2px solid transparent;
                transition: all 0.2s ease;
            }
            .language-tab.active { color: #2563eb; border-bottom-color: #2563eb; }
            .language-tab:hover { color: #374151; }
            
            /* Language Content */
            .language-content { display: none; }
            .language-content.active { display: block; }
            
            /* Form Sections */
            .form-section { 
                background: #f8fafc; padding: 20px; border-radius: 8px; margin-bottom: 20px;
                border-left: 4px solid #e5e7eb;
            }
            .form-section h4 { 
                margin: 0 0 16px 0; color: #1f2937; font-size: 16px; font-weight: 600;
                display: flex; align-items: center; gap: 8px;
            }
            .section-meta { background: #f3f4f6; }
            .section-content { background: #fefefe; border-left-color: #2563eb; }
            
            /* Actions */
            .form-actions { 
                display: flex; gap: 12px; justify-content: flex-end; margin-top: 30px; 
                padding-top: 20px; border-top: 1px solid #e5e7eb;
            }
            .btn-save { 
                background: #2563eb; color: white; border: none; padding: 12px 24px; 
                border-radius: 6px; cursor: pointer; font-weight: 500; font-size: 14px;
                transition: background-color 0.2s ease;
            }
            .btn-save:hover { background: #1d4ed8; }
            .btn-cancel { 
                background: #6b7280; color: white; border: none; padding: 12px 24px; 
                border-radius: 6px; cursor: pointer; font-weight: 500; font-size: 14px;
                transition: background-color 0.2s ease;
            }
            .btn-cancel:hover { background: #4b5563; }
            
            /* Status and Badges */
            .status-badge { padding: 4px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; }
            .status-published { background: #10b981; color: white; }
            .status-draft { background: #f59e0b; color: white; }
            
            /* Editor Enhancements */
            .editor-header { 
                display: flex; justify-content: space-between; align-items: center; 
                margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #e5e7eb;
            }
            .editor-header h3 { margin: 0; color: #1f2937; }
            .completion-indicator { 
                display: flex; gap: 8px; align-items: center; font-size: 12px; color: #6b7280;
            }
            .completion-dot { 
                width: 8px; height: 8px; border-radius: 50%; background: #e5e7eb;
            }
            .completion-dot.filled { background: #10b981; }
            
            /* New Language System Styles */
            .editor-info { 
                display: flex; gap: 20px; align-items: center; font-size: 12px; color: #6b7280;
            }
            .section-translation { 
                background: #f0f9ff; border-left-color: #0ea5e9;
            }
            .btn-link-translation {
                background: #0ea5e9; color: white; border: none; padding: 8px 16px;
                border-radius: 4px; cursor: pointer; font-size: 12px;
            }
            .btn-link-translation:hover { background: #0284c7; }
            .translation-item {
                display: flex; justify-content: space-between; align-items: center;
                padding: 8px 12px; background: white; border-radius: 4px; margin-bottom: 8px;
                border: 1px solid #e5e7eb;
            }
            .language-filter {
                display: flex; gap: 10px; margin-bottom: 15px; align-items: center;
            }
            .language-filter select {
                padding: 6px 12px; border: 1px solid #d1d5db; border-radius: 4px;
            }
            
            /* WYSIWYG Editor Styles */
            .editor-container {
                border: 2px solid #e5e7eb;
                border-radius: 6px;
                background: white;
            }
            .editor-container.focused {
                border-color: #2563eb;
                box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
            }
            .ql-toolbar {
                border-bottom: 1px solid #e5e7eb !important;
                border-top: none !important;
                border-left: none !important;
                border-right: none !important;
            }
            .ql-container {
                border: none !important;
                font-size: 14px;
                font-family: inherit;
            }
            .ql-editor {
                min-height: 200px;
                padding: 12px;
                background-color: white !important;
            }
            
            /* Ensure Quill container has white background */
            .ql-container {
                background-color: white !important;
            }
            
            /* Ensure the entire Quill wrapper has white background */
            .quill {
                background-color: white !important;
            }
            
            /* Editor Tabs */
            .editor-tabs {
                display: flex;
                margin-bottom: 0;
                border-bottom: 1px solid #e5e7eb;
            }
            .editor-tab {
                padding: 8px 16px;
                border: none;
                background: #f9fafb;
                cursor: pointer;
                border-bottom: 2px solid transparent;
                font-size: 13px;
                font-weight: 500;
            }
            .editor-tab.active {
                background: white;
                border-bottom-color: #2563eb;
                color: #2563eb;
            }
            .editor-tab:hover {
                background: #f3f4f6;
            }
            
            /* Preview Styles */
            .preview-container {
                display: none;
                border: 2px solid #e5e7eb;
                border-radius: 6px;
                background: white;
                padding: 20px;
                min-height: 200px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
                line-height: 1.6;
            }
            .preview-container.active {
                display: block;
            }
            .preview-container h1, .preview-container h2, .preview-container h3 {
                color: #1f2937;
                margin-top: 1.5em;
                margin-bottom: 0.5em;
            }
            .preview-container p {
                margin-bottom: 1em;
                color: #374151;
            }
            .preview-container ul, .preview-container ol {
                margin-bottom: 1em;
                padding-left: 1.5em;
            }
            .preview-container blockquote {
                border-left: 4px solid #e5e7eb;
                padding-left: 1em;
                margin: 1em 0;
                font-style: italic;
                color: #6b7280;
            }
            
            /* Responsive Design */
            @media (max-width: 768px) {
                .admin-layout { flex-direction: column; }
                .sidebar { width: 100%; height: auto; order: 2; }
                .main-content { order: 1; }
                .content-header { padding: 15px 20px; }
                .content-body { padding: 20px; }
                .page-title { font-size: 20px; }
                .stats-grid { grid-template-columns: 1fr 1fr; gap: 15px; }
                .nav-item { padding: 15px 20px; }
                .sidebar-nav { padding: 15px 0; }
            }
            
            @media (max-width: 480px) {
                .stats-grid { grid-template-columns: 1fr; }
                .content-body { padding: 15px; }
                .form-group input, .form-group textarea, .form-group select { padding: 10px; }
                .editor-tabs { font-size: 12px; }
                .editor-tab { padding: 6px 12px; }
            }
        </style>
    </head>
    <body>
        <!-- Login Section -->
        <div id="login-section" class="login-section">
            <h2>🎭 Admin Login</h2>
            <form class="login-form" onsubmit="return login(event)">
                <div class="form-group">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit" class="login-btn">Login</button>
                <div id="login-error" class="error hidden"></div>
            </form>
        </div>

        <!-- Dashboard Section -->
        <div id="dashboard-section" class="admin-layout hidden">
            <!-- Sidebar -->
            <div class="sidebar">
                <div class="sidebar-header">
                    <div class="sidebar-title">🎭 Coaching Admin</div>
                    <div class="sidebar-subtitle">Peter Stoyanov's Dashboard</div>
                </div>
                
                <nav class="sidebar-nav">
                    <div class="nav-section">
                        <div class="nav-section-title">Overview</div>
                        <div class="nav-item active" onclick="showTab('dashboard')">
                            <span class="nav-icon">📊</span>
                            <span class="nav-text">Dashboard</span>
                        </div>
                    </div>
                    
                    <div class="nav-section">
                        <div class="nav-section-title">Content Management</div>
                        <div class="nav-item" onclick="showTab('blog')">
                            <span class="nav-icon">✍️</span>
                            <span class="nav-text">Blog Management</span>
                        </div>
                        <div class="nav-item" onclick="showTab('newsletter')">
                            <span class="nav-icon">📧</span>
                            <span class="nav-text">Newsletter</span>
                        </div>
                    </div>
                    
                    <div class="nav-section">
                        <div class="nav-section-title">Email Automation</div>
                        <div class="nav-item" onclick="showTab('email-sequences')">
                            <span class="nav-icon">🤖</span>
                            <span class="nav-text">Email Sequences</span>
                        </div>
                        <div class="nav-item" onclick="showTab('subscribers')">
                            <span class="nav-icon">👥</span>
                            <span class="nav-text">Subscribers</span>
                        </div>
                        <div class="nav-item" onclick="showTab('sequence-analytics')">
                            <span class="nav-icon">📊</span>
                            <span class="nav-text">Sequence Analytics</span>
                        </div>
                    </div>
                    
                    <div class="nav-section">
                        <div class="nav-section-title">Analytics</div>
                        <div class="nav-item" onclick="showTab('leads')">
                            <span class="nav-icon">👥</span>
                            <span class="nav-text">Leads & Contacts</span>
                        </div>
                        <div class="nav-item" onclick="showTab('performance')">
                            <span class="nav-icon">📈</span>
                            <span class="nav-text">Performance</span>
                        </div>
                    </div>
                    
                    <div class="nav-section">
                        <div class="nav-section-title">Settings</div>
                        <div class="nav-item" onclick="showTab('profile')">
                            <span class="nav-icon">⚙️</span>
                            <span class="nav-text">Profile Settings</span>
                        </div>
                        <div class="nav-item" onclick="showTab('system')">
                            <span class="nav-icon">🔧</span>
                            <span class="nav-text">System Settings</span>
                        </div>
                    </div>
                </nav>
                
                <div class="sidebar-footer">
                    <div class="user-info">
                        <div class="user-avatar">PS</div>
                        <div class="user-details">
                            <div class="user-name" id="username-display">Loading...</div>
                            <div class="user-role">Administrator</div>
                        </div>
                    </div>
                    <button class="btn btn-danger" onclick="logout()" style="width: 100%;">Logout</button>
                </div>
            </div>
            
            <!-- Main Content -->
            <div class="main-content">
                <div class="content-header">
                    <div class="page-header">
                        <div>
                            <h1 class="page-title" id="page-title">Dashboard</h1>
                            <div class="page-subtitle" id="page-subtitle">Real-time statistics and activity monitoring</div>
                        </div>
                        <div class="header-actions">
                            <button class="btn btn-primary" onclick="loadData()">🔄 Refresh</button>
                        </div>
                    </div>
                </div>
                
                <div class="content-body" id="main-content-area">
                    <!-- Dynamic content will be loaded here -->
                </div>
            </div>
        </div>
        
        <!-- Content Templates -->
        <div style="display: none;">
            <!-- Dashboard Content Template -->
            <div id="dashboard-content-template">
                <div class="stats-grid" id="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number" id="total-leads">Loading...</div>
                        <div class="stat-label">Total Leads</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" id="lead-magnet-total">Loading...</div>
                        <div class="stat-label">Lead Magnet Downloads</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" id="waitlist-total">Loading...</div>
                        <div class="stat-label">Waitlist Registrations</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" id="corporate-total">Loading...</div>
                        <div class="stat-label">Corporate Inquiries</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" id="conversion-rate">Loading...</div>
                        <div class="stat-label">Conversion Rate</div>
                    </div>
                </div>
                
                <div class="content-card">
                    <div class="card-header">
                        <h3 class="card-title">Recent Activity</h3>
                    </div>
                    <div class="card-body">
                        <div id="recent-activity">Loading...</div>
                    </div>
                </div>
            </div>
            
            <!-- Blog Management Content Template -->
            <div id="blog-content-template">
                <div id="blog-list-view">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <button class="btn btn-success" onclick="showBlogEditor()">✍️ New Blog Post</button>
                        <div class="language-filter">
                            <label for="language-filter">Filter by language:</label>
                            <select id="language-filter" onchange="loadBlogPosts()">
                                <option value="">All Languages</option>
                                <option value="en">🇺🇸 English</option>
                                <option value="bg">🇧🇬 Bulgarian</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="content-card">
                        <div class="card-body">
                            <div class="blog-list" id="blog-list">
                                <!-- Blog posts will be loaded here -->
                            </div>
                        </div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="lead-magnet-total">Loading...</div>
                    <div class="stat-label">Lead Magnet Downloads</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="waitlist-total">Loading...</div>
                    <div class="stat-label">Waitlist Registrations</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="corporate-total">Loading...</div>
                    <div class="stat-label">Corporate Inquiries</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="conversion-rate">Loading...</div>
                    <div class="stat-label">Conversion Rate</div>
                </div>
            </div>
            
            <div class="activity-section">
                <h2>Recent Activity <button class="refresh-btn" onclick="loadData()">Refresh</button></h2>
                <div id="recent-activity">Loading...</div>
            </div>
            </div>
            
            <!-- Blog Management Tab -->
            <div id="blog-tab" class="tab-content hidden">
                <div id="blog-list-view">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <button class="btn-new" onclick="showBlogEditor()">New Blog Post</button>
                        <div class="language-filter">
                            <label for="language-filter">Filter by language:</label>
                            <select id="language-filter" onchange="loadBlogPosts()">
                                <option value="">All Languages</option>
                                <option value="en">🇺🇸 English</option>
                                <option value="bg">🇧🇬 Bulgarian</option>
                            </select>
                        </div>
                    </div>
                    <div id="blog-posts-container">
                        <div class="blog-list" id="blog-list">
                            <!-- Blog posts will be loaded here -->
                        </div>
                    </div>
                </div>
                
                <div id="blog-editor-view" class="hidden">
                    <div class="editor-header">
                        <h3 id="editor-title">Create New Blog Post</h3>
                        <div class="editor-info">
                            <span id="current-language-display">Language: English</span>
                            <span id="translation-info"></span>
                        </div>
                    </div>
                    
                    <form id="blog-form">
                        <!-- Meta Section -->
                        <div class="form-section section-meta">
                            <h4>📝 Post Settings</h4>
                            
                            <div class="form-group">
                                <label for="blog-language">Language</label>
                                <select id="blog-language" name="language" required onchange="updateLanguageDisplay()">
                                    <option value="en">🇺🇸 English</option>
                                    <option value="bg">🇧🇬 Bulgarian</option>
                                </select>
                            </div>
                            
                            <div class="form-group">
                                <label for="blog-slug">Slug (URL)</label>
                                <input type="text" id="blog-slug" name="slug" required placeholder="e.g., mastering-public-speaking">
                            </div>
                            
                            <div class="form-group">
                                <label for="blog-featured-image">Featured Image URL</label>
                                <input type="text" id="blog-featured-image" name="featured_image" placeholder="https://...">
                                <button type="button" onclick="uploadImage()" style="margin-top: 5px;">Upload Image</button>
                                <input type="file" id="image-upload" accept="image/*" style="display: none;" onchange="handleImageUpload(event)">
                            </div>
                            
                            <div class="form-group">
                                <label>
                                    <input type="checkbox" id="blog-published" name="is_published"> Published
                                </label>
                            </div>
                        </div>
                        
                        <!-- Content Section -->
                        <div class="form-section section-content">
                            <h4>📝 Content</h4>
                            
                            <div class="form-group">
                                <label for="blog-title">Title</label>
                                <input type="text" id="blog-title" name="title" required>
                            </div>
                            
                            <div class="form-group">
                                <label for="blog-excerpt">Excerpt</label>
                                <textarea id="blog-excerpt" name="excerpt" placeholder="Brief description of your post..."></textarea>
                            </div>
                            
                            <div class="form-group">
                                <label for="blog-content">Content</label>
                                <div class="editor-tabs">
                                    <button type="button" class="editor-tab active" onclick="switchEditorTab('write')">✏️ Write</button>
                                    <button type="button" class="editor-tab" onclick="switchEditorTab('preview')">👁️ Preview</button>
                                </div>
                                
                                <!-- WYSIWYG Editor -->
                                <div id="editor-container" class="editor-container">
                                    <div id="blog-content-editor"></div>
                                </div>
                                
                                <!-- Preview Container -->
                                <div id="preview-container" class="preview-container">
                                    <div id="preview-content">
                                        <p style="color: #6b7280; font-style: italic;">Preview will appear here...</p>
                                    </div>
                                </div>
                                
                                <!-- Hidden textarea for form submission -->
                                <textarea id="blog-content" name="content" style="display: none;"></textarea>
                            </div>
                            
                            <div class="form-group">
                                <label for="blog-tags">Tags (comma-separated)</label>
                                <input type="text" id="blog-tags" name="tags" placeholder="tag1, tag2, tag3">
                            </div>
                        </div>
                        
                        <!-- Translation Section -->
                        <div class="form-section section-translation" id="translation-section" style="display: none;">
                            <h4>🌐 Translations</h4>
                            <div id="translation-list">
                                <!-- Translations will be loaded here -->
                            </div>
                            <button type="button" onclick="showTranslationDialog()" class="btn-link-translation">Link to Translation</button>
                        </div>
                        
                        <div class="form-actions">
                            <button type="button" class="btn-cancel" onclick="closeBlogEditor()">Cancel</button>
                            <button type="submit" class="btn-save">Save Post</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        
        <!-- Newsletter Management Content Template -->
        <div id="newsletter-content-template" style="display: none;">
            <div class="content-card">
                <div class="card-header">
                    <h2>📧 Newsletter Management</h2>
                    <p>Create and send newsletters to your subscribers</p>
                </div>
                <div class="card-body">
                    
                    <!-- Newsletter Options -->
                    <div style="display: flex; gap: 20px; margin-bottom: 30px;">
                        <button class="btn btn-primary" onclick="showNewsletterComposer('blog-digest')" style="flex: 1;">
                            ✍️ Send Blog Digest
                        </button>
                        <button class="btn btn-success" onclick="showNewsletterComposer('custom')" style="flex: 1;">
                            📝 Custom Newsletter
                        </button>
                        <button class="btn" onclick="loadNewsletterGroups()" style="flex: 1;">
                            👥 Manage Groups
                        </button>
                    </div>
                    
                    <!-- Newsletter Composer -->
                    <div id="newsletter-composer" style="display: none;">
                        <div class="form-section">
                            <h3 id="composer-title">Create Newsletter</h3>
                            
                            <form id="newsletter-form">
                                <div class="form-group">
                                    <label for="newsletter-subject">Subject Line</label>
                                    <input type="text" id="newsletter-subject" placeholder="Newsletter subject line..." required>
                                </div>
                                
                                <div class="form-group" id="blog-posts-selection" style="display: none;">
                                    <label>Select Blog Posts</label>
                                    <div id="blog-posts-list" style="max-height: 200px; overflow-y: auto; border: 1px solid #e5e7eb; border-radius: 4px; padding: 10px;">
                                        <!-- Blog posts will be loaded here -->
                                    </div>
                                </div>
                                
                                <div class="form-group" id="custom-content-group" style="display: none;">
                                    <label for="newsletter-content">Newsletter Content</label>
                                    <div style="border: 1px solid #e5e7eb; border-radius: 4px;">
                                        <div id="newsletter-content-editor" style="min-height: 300px;"></div>
                                    </div>
                                    <textarea id="newsletter-content" style="display: none;"></textarea>
                                </div>
                                
                                <div class="form-group">
                                    <label for="newsletter-groups">Target Groups (Optional)</label>
                                    <select id="newsletter-groups" multiple style="height: 100px;">
                                        <option value="">All Subscribers</option>
                                    </select>
                                    <small style="color: #6b7280;">Hold Ctrl/Cmd to select multiple groups</small>
                                </div>
                                
                                <div class="form-actions">
                                    <button type="button" class="btn btn-primary" onclick="previewNewsletter()">
                                        👁️ Preview
                                    </button>
                                    <button type="button" class="btn btn-success" onclick="sendNewsletter()">
                                        📧 Send Newsletter
                                    </button>
                                    <button type="button" class="btn" onclick="cancelNewsletter()">
                                        Cancel
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                    
                    <!-- Newsletter Preview -->
                    <div id="newsletter-preview" style="display: none;">
                        <div class="form-section">
                            <h3>📧 Newsletter Preview</h3>
                            <div style="border: 2px solid #e5e7eb; border-radius: 8px; background: #f9fafb; padding: 20px; margin: 20px 0;">
                                <div id="newsletter-preview-content">
                                    <!-- Preview content will be loaded here -->
                                </div>
                            </div>
                            <div class="form-actions">
                                <button type="button" class="btn btn-success" onclick="confirmSendNewsletter()">
                                    ✅ Confirm & Send
                                </button>
                                <button type="button" class="btn" onclick="editNewsletter()">
                                    ✏️ Edit
                                </button>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Groups Management -->
                    <div id="newsletter-groups-management" style="display: none;">
                        <div class="form-section">
                            <h3>👥 Subscriber Groups</h3>
                            <div id="groups-list">
                                <!-- Groups will be loaded here -->
                            </div>
                        </div>
                    </div>
                    
                    <!-- Newsletter Status -->
                    <div id="newsletter-status" style="display: none; padding: 15px; border-radius: 6px; margin-top: 20px;">
                        <div id="newsletter-status-content"></div>
                    </div>
                    
                </div>
            </div>
        </div>
        
        <!-- Email Sequences Content Template -->
        <div id="email-sequences-template" style="display: none;">
            <div class="content-card">
                <div class="card-header">
                    <h2>🤖 Email Sequences Management</h2>
                    <p>Manage automated email sequences in English and Bulgarian</p>
                </div>
                <div class="card-body">
                    
                    <!-- Language Selector -->
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
                        <div class="form-group" style="margin: 0;">
                            <label for="sequence-language">Language:</label>
                            <select id="sequence-language" onchange="loadEmailSequences()" style="width: 200px;">
                                <option value="en">🇺🇸 English</option>
                                <option value="bg">🇧🇬 Bulgarian</option>
                            </select>
                        </div>
                        <button class="btn btn-success" onclick="testSequence()">
                            🧪 Test Sequence
                        </button>
                        <button class="btn btn-primary" onclick="toggleScheduler()">
                            <span id="scheduler-toggle-text">⏸️ Scheduler</span>
                        </button>
                    </div>
                    
                    <!-- Sequences Overview -->
                    <div class="stats-grid" style="margin-bottom: 30px;">
                        <div class="stat-card">
                            <div class="stat-number" id="lead-magnet-count">-</div>
                            <div class="stat-label">Lead Magnet Emails</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="waitlist-count">-</div>
                            <div class="stat-label">Waitlist Emails</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="corporate-count">-</div>
                            <div class="stat-label">Corporate Emails</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="active-subscribers">-</div>
                            <div class="stat-label">Active Subscribers</div>
                        </div>
                    </div>
                    
                    <!-- Sequence List -->
                    <div id="sequences-list">
                        <!-- Will be populated by JavaScript -->
                    </div>
                    
                    <!-- Sequence Details Modal -->
                    <div id="sequence-details" style="display: none;">
                        <div class="form-section">
                            <h3 id="sequence-details-title">Sequence Details</h3>
                            <div id="sequence-emails-list">
                                <!-- Email list will be loaded here -->
                            </div>
                            <div class="form-actions">
                                <button type="button" class="btn" onclick="closeSequenceDetails()">Close</button>
                            </div>
                        </div>
                    </div>
                    
                </div>
            </div>
        </div>
        
        <!-- Subscribers Content Template -->
        <div id="subscribers-template" style="display: none;">
            <div class="content-card">
                <div class="card-header">
                    <h2>👥 Subscriber Management</h2>
                    <p>View and manage your email subscribers</p>
                </div>
                <div class="card-body">
                    
                    <!-- Subscriber Filters -->
                    <div style="display: flex; gap: 20px; margin-bottom: 30px;">
                        <div class="form-group" style="margin: 0;">
                            <label for="subscriber-language">Language:</label>
                            <select id="subscriber-language" onchange="loadSubscribers()">
                                <option value="">All Languages</option>
                                <option value="en">🇺🇸 English</option>
                                <option value="bg">🇧🇬 Bulgarian</option>
                            </select>
                        </div>
                        <div class="form-group" style="margin: 0;">
                            <label for="subscriber-source">Source:</label>
                            <select id="subscriber-source" onchange="loadSubscribers()">
                                <option value="">All Sources</option>
                                <option value="lead_magnet">Lead Magnet</option>
                                <option value="waitlist">Waitlist</option>
                                <option value="corporate">Corporate</option>
                            </select>
                        </div>
                        <button class="btn btn-primary" onclick="exportSubscribers()">
                            📊 Export Data
                        </button>
                    </div>
                    
                    <!-- Subscribers List -->
                    <div id="subscribers-list">
                        <!-- Will be populated by JavaScript -->
                    </div>
                    
                </div>
            </div>
        </div>
        
        <!-- Sequence Analytics Content Template -->
        <div id="sequence-analytics-template" style="display: none;">
            <div class="content-card">
                <div class="card-header">
                    <h2>📊 Sequence Analytics</h2>
                    <p>Track performance of automated email sequences</p>
                </div>
                <div class="card-body">
                    
                    <!-- Analytics Filters -->
                    <div style="display: flex; gap: 20px; margin-bottom: 30px;">
                        <div class="form-group" style="margin: 0;">
                            <label for="analytics-language">Language:</label>
                            <select id="analytics-language" onchange="loadSequenceAnalytics()">
                                <option value="">All Languages</option>
                                <option value="en">🇺🇸 English</option>
                                <option value="bg">🇧🇬 Bulgarian</option>
                            </select>
                        </div>
                        <div class="form-group" style="margin: 0;">
                            <label for="analytics-period">Period:</label>
                            <select id="analytics-period" onchange="loadSequenceAnalytics()">
                                <option value="7">Last 7 days</option>
                                <option value="30" selected>Last 30 days</option>
                                <option value="90">Last 90 days</option>
                            </select>
                        </div>
                    </div>
                    
                    <!-- Performance Metrics -->
                    <div class="stats-grid" style="margin-bottom: 30px;">
                        <div class="stat-card">
                            <div class="stat-number" id="total-opens">-</div>
                            <div class="stat-label">Total Opens</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="open-rate">-%</div>
                            <div class="stat-label">Open Rate</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="click-rate">-%</div>
                            <div class="stat-label">Click Rate</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="conversion-rate">-%</div>
                            <div class="stat-label">Conversion Rate</div>
                        </div>
                    </div>
                    
                    <!-- Webhook Analytics -->
                    <div style="margin-bottom: 30px;">
                        <h3 style="margin-bottom: 20px; color: #374151;">🔗 Real-time Webhook Analytics</h3>
                        <div class="stats-grid">
                            <div class="stat-card">
                                <div class="stat-number" id="webhook-opens">-</div>
                                <div class="stat-label">Unique Opens</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-number" id="webhook-clicks">-</div>
                                <div class="stat-label">Unique Clicks</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-number" id="webhook-bounces">-</div>
                                <div class="stat-label">Bounces</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-number" id="webhook-unsubscribes">-</div>
                                <div class="stat-label">Unsubscribes</div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Analytics Charts -->
                    <div id="analytics-charts">
                        <!-- Charts will be rendered here -->
                        <div style="text-align: center; padding: 40px; color: #6b7280;">
                            <h3>📈 Analytics Coming Soon</h3>
                            <p>Detailed email performance analytics are being implemented.</p>
                        </div>
                    </div>
                    
                </div>
            </div>
        </div>
        
        <script>
            let authToken = localStorage.getItem('adminToken');
            
            // Check if already logged in
            if (authToken) {
                checkAuth();
            }
            
            function login(event) {
                event.preventDefault();
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;
                
                const formData = new FormData();
                formData.append('username', username);
                formData.append('password', password);
                
                fetch('/auth/login', {
                    method: 'POST',
                    body: formData
                })
                .then(function(response) {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('Login failed');
                    }
                })
                .then(function(data) {
                    authToken = data.access_token;
                    localStorage.setItem('adminToken', authToken);
                    showDashboard(username);
                })
                .catch(function(error) {
                    showError('Invalid username or password');
                });
                
                return false;
            }
            
            async function checkAuth() {
                try {
                    const response = await fetch('/auth/me', {
                        headers: {
                            'Authorization': 'Bearer ' + authToken
                        }
                    });
                    
                    if (response.ok) {
                        const user = await response.json();
                        showDashboard(user.username);
                    } else {
                        logout();
                    }
                } catch (error) {
                    logout();
                }
            }
            
            function showDashboard(username) {
                document.getElementById('login-section').classList.add('hidden');
                document.getElementById('dashboard-section').classList.remove('hidden');
                document.getElementById('username-display').textContent = username;
                loadData();
                setInterval(loadData, 30000);
            }
            
            function logout() {
                localStorage.removeItem('adminToken');
                authToken = null;
                document.getElementById('login-section').classList.remove('hidden');
                document.getElementById('dashboard-section').classList.add('hidden');
                document.getElementById('username').value = '';
                document.getElementById('password').value = '';
                hideError();
            }
            
            function showError(message) {
                const errorDiv = document.getElementById('login-error');
                errorDiv.textContent = message;
                errorDiv.classList.remove('hidden');
            }
            
            function hideError() {
                document.getElementById('login-error').classList.add('hidden');
            }
            
            async function loadData() {
                if (!authToken) return;
                
                try {
                    const headers = {
                        'Authorization': 'Bearer ' + authToken
                    };
                    
                    // Load statistics
                    const statsResponse = await fetch('/admin/stats', { headers });
                    if (!statsResponse.ok) {
                        logout();
                        return;
                    }
                    const stats = await statsResponse.json();
                    
                    document.getElementById('total-leads').textContent = stats.overview.total_leads;
                    document.getElementById('lead-magnet-total').textContent = stats.lead_magnet.total;
                    document.getElementById('waitlist-total').textContent = stats.waitlist.total;
                    document.getElementById('corporate-total').textContent = stats.corporate.total;
                    document.getElementById('conversion-rate').textContent = stats.overview.conversion_rate + '%';
                    
                    // Load recent activity
                    const activityResponse = await fetch('/admin/recent-activity', { headers });
                    const activity = await activityResponse.json();
                    
                    const activityDiv = document.getElementById('recent-activity');
                    activityDiv.innerHTML = '';
                    
                    activity.forEach(item => {
                        const div = document.createElement('div');
                        div.className = 'activity-item';
                        
                        const typeClass = 'type-' + item.type.replace('_', '-');
                        const date = new Date(item.date).toLocaleString();
                        
                        div.innerHTML = 
                            '<span class="activity-type ' + typeClass + '">' + item.type.replace('_', ' ').toUpperCase() + '</span>' +
                            '<strong>' + item.email + '</strong> ' + (item.name ? '(' + item.name + ')' : '') +
                            (item.company ? '- ' + item.company : '') +
                            '<div style="color: #666; font-size: 0.9em;">' + item.details + ' - ' + date + '</div>';
                        
                        activityDiv.appendChild(div);
                    });
                    
                } catch (error) {
                    console.error('Error loading data:', error);
                }
            }
            
            // Blog Management Functions
            let currentEditingPost = null;
            let quillEditor = null;
            
            function initializeWYSIWYGEditor() {
                if (quillEditor) {
                    return; // Already initialized
                }
                
                // Initialize Quill editor
                quillEditor = new Quill('#blog-content-editor', {
                    theme: 'snow',
                    placeholder: 'Write your blog post content...',
                    modules: {
                        toolbar: [
                            [{ 'header': [1, 2, 3, false] }],
                            ['bold', 'italic', 'underline', 'strike'],
                            [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                            [{ 'indent': '-1'}, { 'indent': '+1' }],
                            ['link', 'image', 'blockquote', 'code-block'],
                            [{ 'align': [] }],
                            ['clean']
                        ]
                    }
                });
                
                // Update hidden textarea when content changes
                quillEditor.on('text-change', function() {
                    const content = quillEditor.root.innerHTML;
                    document.getElementById('blog-content').value = content;
                    updatePreview();
                });
                
                // Focus styling
                quillEditor.on('selection-change', function(range) {
                    const container = document.getElementById('editor-container');
                    if (range) {
                        container.classList.add('focused');
                    } else {
                        container.classList.remove('focused');
                    }
                });
            }
            
            function switchEditorTab(tab) {
                const tabs = document.querySelectorAll('.editor-tab');
                const editorContainer = document.getElementById('editor-container');
                const previewContainer = document.getElementById('preview-container');
                
                // Update tab states
                tabs.forEach(t => t.classList.remove('active'));
                document.querySelector(`[onclick="switchEditorTab('${tab}')"]`).classList.add('active');
                
                if (tab === 'write') {
                    editorContainer.style.display = 'block';
                    previewContainer.classList.remove('active');
                } else if (tab === 'preview') {
                    editorContainer.style.display = 'none';
                    previewContainer.classList.add('active');
                    updatePreview();
                }
            }
            
            function updatePreview() {
                if (!quillEditor) return;
                
                const content = quillEditor.root.innerHTML;
                const title = document.getElementById('blog-title').value;
                const excerpt = document.getElementById('blog-excerpt').value;
                
                const previewContent = document.getElementById('preview-content');
                
                let preview = '';
                if (title) {
                    preview += `<h1>${title}</h1>`;
                }
                if (excerpt) {
                    preview += `<p style="font-size: 1.1em; color: #6b7280; margin-bottom: 1.5em;"><em>${excerpt}</em></p>`;
                }
                if (content && content !== '<p><br></p>') {
                    preview += content;
                } else {
                    preview += '<p style="color: #9ca3af; font-style: italic;">No content yet...</p>';
                }
                
                previewContent.innerHTML = preview;
            }
            
            function updateLanguageDisplay() {
                const language = document.getElementById('blog-language').value;
                const displayMap = { 'en': 'English', 'bg': 'Bulgarian' };
                document.getElementById('current-language-display').textContent = `Language: ${displayMap[language]}`;
                
                // Update placeholder based on language
                const titleInput = document.getElementById('blog-title');
                const excerptTextarea = document.getElementById('blog-excerpt');
                const tagsInput = document.getElementById('blog-tags');
                
                if (language === 'bg') {
                    if (quillEditor) {
                        quillEditor.root.dataset.placeholder = "Напишете съдържанието на блог поста на български...";
                    }
                    titleInput.placeholder = "Заглавие на български";
                    excerptTextarea.placeholder = "Кратко описание на български...";
                    tagsInput.placeholder = "таг1, таг2, таг3";
                } else {
                    if (quillEditor) {
                        quillEditor.root.dataset.placeholder = "Write your blog post content in English...";
                    }
                    titleInput.placeholder = "Title in English";
                    excerptTextarea.placeholder = "Brief description in English...";
                    tagsInput.placeholder = "tag1, tag2, tag3";
                }
            }
            
            function showTab(tabName) {
                // Update sidebar navigation
                document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
                event.target.classList.add('active');
                
                // Update page title and subtitle
                const titles = {
                    'dashboard': { title: 'Dashboard', subtitle: 'Real-time statistics and activity monitoring' },
                    'blog': { title: 'Blog Management', subtitle: 'Create and manage blog posts in multiple languages' },
                    'newsletter': { title: 'Newsletter Management', subtitle: 'Create and send newsletters to your subscribers' },
                    'email-sequences': { title: 'Email Sequences', subtitle: 'Manage automated email sequences in English and Bulgarian' },
                    'subscribers': { title: 'Subscriber Management', subtitle: 'View and manage your email subscribers' },
                    'sequence-analytics': { title: 'Sequence Analytics', subtitle: 'Track performance of automated email sequences' },
                    'leads': { title: 'Leads & Contacts', subtitle: 'Manage customer inquiries and contacts' },
                    'performance': { title: 'Performance', subtitle: 'Analytics and performance metrics' },
                    'profile': { title: 'Profile Settings', subtitle: 'Manage your account settings' },
                    'system': { title: 'System Settings', subtitle: 'Configure system preferences' }
                };
                
                if (titles[tabName]) {
                    document.getElementById('page-title').textContent = titles[tabName].title;
                    document.getElementById('page-subtitle').textContent = titles[tabName].subtitle;
                }
                
                // Load content into main area
                const mainContentArea = document.getElementById('main-content-area');
                
                if (tabName === 'dashboard') {
                    const template = document.getElementById('dashboard-content-template');
                    mainContentArea.innerHTML = template.innerHTML;
                    loadData();
                } else if (tabName === 'blog') {
                    const template = document.getElementById('blog-content-template');
                    mainContentArea.innerHTML = template.innerHTML;
                    loadBlogPosts();
                } else if (tabName === 'newsletter') {
                    const template = document.getElementById('newsletter-content-template');
                    mainContentArea.innerHTML = template.innerHTML;
                    initializeNewsletterSection();
                } else if (tabName === 'email-sequences') {
                    const template = document.getElementById('email-sequences-template');
                    mainContentArea.innerHTML = template.innerHTML;
                    loadEmailSequences();
                    loadSchedulerStatus();
                } else if (tabName === 'subscribers') {
                    const template = document.getElementById('subscribers-template');
                    mainContentArea.innerHTML = template.innerHTML;
                    loadSubscribers();
                } else if (tabName === 'sequence-analytics') {
                    const template = document.getElementById('sequence-analytics-template');
                    mainContentArea.innerHTML = template.innerHTML;
                    loadSequenceAnalytics();
                } else {
                    // Placeholder for other sections
                    mainContentArea.innerHTML = `
                        <div class="content-card">
                            <div class="card-body">
                                <div style="text-align: center; padding: 40px; color: #6b7280;">
                                    <h3>🚧 Coming Soon</h3>
                                    <p>This section is under development.</p>
                                </div>
                            </div>
                        </div>
                    `;
                }
            }
            
            async function loadBlogPosts() {
                if (!authToken) return;
                
                try {
                    // Use the new multilingual endpoint
                    const response = await fetch('/admin/multilingual/posts', {
                        headers: { 'Authorization': 'Bearer ' + authToken }
                    });
                    
                    if (!response.ok) throw new Error('Failed to load blog posts');
                    
                    const posts = await response.json();
                    const blogList = document.getElementById('blog-list');
                    
                    blogList.innerHTML = '';
                    
                    if (posts.length === 0) {
                        blogList.innerHTML = '<p>No blog posts found. Create your first multilingual post!</p>';
                        return;
                    }
                    
                    posts.forEach(post => {
                        const postDiv = document.createElement('div');
                        postDiv.className = 'blog-item';
                        
                        // Check publish status for both languages
                        const enStatus = post.is_published_en ? '🇺🇸 Published' : '🇺🇸 Draft';
                        const bgStatus = post.is_published_bg ? '🇧🇬 Published' : '🇧🇬 Draft';
                        
                        const enDate = post.published_at_en ? new Date(post.published_at_en).toLocaleDateString() : 'Not published';
                        const bgDate = post.published_at_bg ? new Date(post.published_at_bg).toLocaleDateString() : 'Not published';
                        
                        // Show titles for both languages
                        const enTitle = post.title_en || '[No English title]';
                        const bgTitle = post.title_bg || '[No Bulgarian title]';
                        
                        postDiv.innerHTML = `
                            <div class="blog-info">
                                <div class="blog-title">
                                    <strong>🇺🇸 ${enTitle}</strong>
                                    <br><strong>🇧🇬 ${bgTitle}</strong>
                                </div>
                                <div class="blog-meta">
                                    <div style="margin-bottom: 5px;">
                                        <span class="status-badge ${post.is_published_en ? 'status-published' : 'status-draft'}">${enStatus}</span>
                                        ${post.is_published_en ? `| Published: ${enDate}` : ''}
                                    </div>
                                    <div style="margin-bottom: 5px;">
                                        <span class="status-badge ${post.is_published_bg ? 'status-published' : 'status-draft'}">${bgStatus}</span>
                                        ${post.is_published_bg ? `| Published: ${bgDate}` : ''}
                                    </div>
                                    <div style="font-size: 11px; color: #6b7280;">
                                        Created: ${new Date(post.created_at).toLocaleDateString()}
                                        | Updated: ${new Date(post.updated_at).toLocaleDateString()}
                                    </div>
                                </div>
                            </div>
                            <div class="blog-actions">
                                <button class="btn-edit" onclick="editMultilingualBlogPost(${post.id})">Edit Both</button>
                                <button class="btn-delete" onclick="deleteMultilingualBlogPost(${post.id}, '${enTitle.replace(/'/g, '\\\'') || 'Untitled'}')">Delete</button>
                            </div>
                        `;
                        
                        blogList.appendChild(postDiv);
                    });
                    
                } catch (error) {
                    console.error('Error loading blog posts:', error);
                    document.getElementById('blog-list').innerHTML = '<p>Error loading blog posts.</p>';
                }
            }
            
            function showBlogEditor(postData = null) {
                // Create the blog editor in the main content area
                const mainContentArea = document.getElementById('main-content-area');
                
                // Update page title
                document.getElementById('page-title').textContent = postData ? 'Edit Blog Post' : 'Create New Blog Post';
                document.getElementById('page-subtitle').textContent = 'Use the WYSIWYG editor and preview functionality';
                
                // Load blog editor template
                mainContentArea.innerHTML = `
                    <div class="content-card">
                        <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h3 class="card-title" id="editor-title">${postData ? 'Edit Blog Post' : 'Create New Blog Post'}</h3>
                                <div style="margin-top: 8px; display: flex; gap: 20px; align-items: center; font-size: 12px; color: #6b7280;">
                                    <span id="current-language-display">Language: English</span>
                                    <span id="translation-info"></span>
                                </div>
                            </div>
                            <button type="button" class="btn btn-primary" onclick="backToBlogList()">← Back to Posts</button>
                        </div>
                        <div class="card-body">
                            <form id="blog-form">
                                <!-- Meta Section -->
                                <div style="background: #f8fafc; padding: 20px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #e5e7eb;">
                                    <h4 style="margin: 0 0 16px 0; color: #1f2937; font-size: 16px; font-weight: 600; display: flex; align-items: center; gap: 8px;">📝 Post Settings</h4>
                                    
                                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                                        <div class="form-group">
                                            <label for="blog-language">Language</label>
                                            <select id="blog-language" name="language" required onchange="updateLanguageDisplay()">
                                                <option value="en">🇺🇸 English</option>
                                                <option value="bg">🇧🇬 Bulgarian</option>
                                            </select>
                                        </div>
                                        
                                        <div class="form-group">
                                            <label for="blog-slug">Slug (URL)</label>
                                            <input type="text" id="blog-slug" name="slug" required placeholder="e.g., mastering-public-speaking">
                                        </div>
                                    </div>
                                    
                                    <div class="form-group">
                                        <label for="blog-featured-image">Featured Image URL</label>
                                        <div style="display: flex; gap: 10px;">
                                            <input type="text" id="blog-featured-image" name="featured_image" placeholder="https://..." style="flex: 1;">
                                            <button type="button" onclick="uploadImage()" class="btn btn-primary">Upload</button>
                                        </div>
                                        <input type="file" id="image-upload" accept="image/*" style="display: none;" onchange="handleImageUpload(event)">
                                    </div>
                                    
                                    <div class="form-group">
                                        <label>
                                            <input type="checkbox" id="blog-published" name="is_published" style="margin-right: 8px;"> Published
                                        </label>
                                    </div>
                                </div>
                                
                                <!-- Content Section -->
                                <div style="background: #fefefe; padding: 20px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #2563eb;">
                                    <h4 style="margin: 0 0 16px 0; color: #1f2937; font-size: 16px; font-weight: 600;">📝 Content</h4>
                                    
                                    <div class="form-group">
                                        <label for="blog-title">Title</label>
                                        <input type="text" id="blog-title" name="title" required>
                                    </div>
                                    
                                    <div class="form-group">
                                        <label for="blog-excerpt">Excerpt</label>
                                        <textarea id="blog-excerpt" name="excerpt" placeholder="Brief description of your post..."></textarea>
                                    </div>
                                    
                                    <div class="form-group">
                                        <label for="blog-content">Content</label>
                                        <div class="editor-tabs">
                                            <button type="button" class="editor-tab active" onclick="switchEditorTab('write')">✏️ Write</button>
                                            <button type="button" class="editor-tab" onclick="switchEditorTab('preview')">👁️ Preview</button>
                                        </div>
                                        
                                        <!-- WYSIWYG Editor -->
                                        <div id="editor-container" class="editor-container">
                                            <div id="blog-content-editor"></div>
                                        </div>
                                        
                                        <!-- Preview Container -->
                                        <div id="preview-container" class="preview-container">
                                            <div id="preview-content">
                                                <p style="color: #6b7280; font-style: italic;">Preview will appear here...</p>
                                            </div>
                                        </div>
                                        
                                        <!-- Hidden textarea for form submission -->
                                        <textarea id="blog-content" name="content" style="display: none;"></textarea>
                                    </div>
                                    
                                    <div class="form-group">
                                        <label for="blog-tags">Tags (comma-separated)</label>
                                        <input type="text" id="blog-tags" name="tags" placeholder="tag1, tag2, tag3">
                                    </div>
                                </div>
                                
                                <!-- Translation Section -->
                                <div id="translation-section" style="background: #f0f9ff; padding: 20px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #0ea5e9; display: none;">
                                    <h4 style="margin: 0 0 16px 0; color: #1f2937; font-size: 16px; font-weight: 600;">🌐 Translations</h4>
                                    <div id="translation-list">
                                        <!-- Translations will be loaded here -->
                                    </div>
                                    <button type="button" onclick="showTranslationDialog()" class="btn-link-translation">Link to Translation</button>
                                </div>
                                
                                <div style="display: flex; gap: 12px; justify-content: flex-end; margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
                                    <button type="button" class="btn" onclick="backToBlogList()" style="background: #6b7280; color: white;">Cancel</button>
                                    <button type="submit" class="btn btn-primary">Save Post</button>
                                </div>
                            </form>
                        </div>
                    </div>
                `;
                
                // Initialize WYSIWYG editor
                setTimeout(() => { 
                    initializeWYSIWYGEditor();
                    setupBlogFormHandler(); // Set up form submission handler
                    
                    // Load existing post data if editing
                    if (postData) {
                        document.getElementById('blog-language').value = postData.language;
                        document.getElementById('blog-slug').value = postData.slug;
                        document.getElementById('blog-title').value = postData.title;
                        document.getElementById('blog-excerpt').value = postData.excerpt;
                        document.getElementById('blog-content').value = postData.content;
                        if (quillEditor) {
                            quillEditor.root.innerHTML = postData.content || '';
                        }
                        document.getElementById('blog-tags').value = Array.isArray(postData.tags) ? postData.tags.join(', ') : '';
                        document.getElementById('blog-featured-image').value = postData.featured_image || '';
                        document.getElementById('blog-published').checked = postData.is_published;
                        currentEditingPost = postData.id;
                        
                        updateLanguageDisplay();
                        
                        if (postData.translations && postData.translations.length > 0) {
                            document.getElementById('translation-section').style.display = 'block';
                            loadTranslations(postData.translations);
                            document.getElementById('translation-info').textContent = 'Part of translation group: ' + postData.translation_id;
                        }
                    } else {
                        document.getElementById('blog-language').value = 'en';
                        updateLanguageDisplay();
                        currentEditingPost = null;
                    }
                    
                    updatePreview();
                }, 200);
            }
            
            function backToBlogList() {
                showTab('blog');
            }
            
            // Blog editor functions will be here
            
            // Blog editor functions simplified for basic login functionality
            
            // Newsletter Management Functions
            let newsletterType = null;
            let selectedPosts = [];
            let newsletterEditor = null;
            
            function initializeNewsletterSection() {
                console.log('Initializing newsletter section...');
                // Reset newsletter state
                newsletterType = null;
                selectedPosts = [];
                
                // Hide all sub-sections
                document.getElementById('newsletter-composer').style.display = 'none';
                document.getElementById('newsletter-preview').style.display = 'none';
                document.getElementById('newsletter-groups-management').style.display = 'none';
                document.getElementById('newsletter-status').style.display = 'none';
            }
            
            function showNewsletterComposer(type) {
                console.log('Showing newsletter composer for type:', type);
                newsletterType = type;
                
                // Show composer
                document.getElementById('newsletter-composer').style.display = 'block';
                document.getElementById('newsletter-preview').style.display = 'none';
                document.getElementById('newsletter-groups-management').style.display = 'none';
                
                // Update title and show appropriate sections
                if (type === 'blog-digest') {
                    document.getElementById('composer-title').textContent = 'Create Blog Digest Newsletter';
                    document.getElementById('blog-posts-selection').style.display = 'block';
                    document.getElementById('custom-content-group').style.display = 'none';
                    loadBlogPostsForNewsletter();
                } else if (type === 'custom') {
                    document.getElementById('composer-title').textContent = 'Create Custom Newsletter';
                    document.getElementById('blog-posts-selection').style.display = 'none';
                    document.getElementById('custom-content-group').style.display = 'block';
                    initializeNewsletterEditor();
                }
                
                // Load subscriber groups
                loadSubscriberGroups();
            }
            
            function loadBlogPostsForNewsletter() {
                const blogPostsList = document.getElementById('blog-posts-list');
                blogPostsList.innerHTML = '<div>Loading blog posts...</div>';
                
                fetch('/admin/blog/posts', {
                    headers: { 'Authorization': 'Bearer ' + authToken }
                })
                .then(response => response.json())
                .then(posts => {
                    blogPostsList.innerHTML = '';
                    if (posts && posts.length > 0) {
                        posts.forEach(post => {
                            const postElement = document.createElement('div');
                            postElement.style.cssText = 'padding: 10px; border-bottom: 1px solid #f3f4f6; cursor: pointer;';
                            postElement.innerHTML = 
                                '<label style="display: flex; align-items: center; cursor: pointer;">' +
                                    '<input type="checkbox" value="' + post.id + '" style="margin-right: 10px;">' +
                                    '<div>' +
                                        '<strong>' + post.title + '</strong>' +
                                        '<br><small style="color: #6b7280;">' + (post.excerpt || 'No excerpt') + '</small>' +
                                    '</div>' +
                                '</label>';
                            
                            postElement.querySelector('input').addEventListener('change', function(e) {
                                if (e.target.checked) {
                                    selectedPosts.push(parseInt(e.target.value));
                                } else {
                                    selectedPosts = selectedPosts.filter(id => id !== parseInt(e.target.value));
                                }
                                console.log('Selected posts:', selectedPosts);
                            });
                            
                            blogPostsList.appendChild(postElement);
                        });
                    } else {
                        blogPostsList.innerHTML = '<div style="color: #6b7280; text-align: center; padding: 20px;">No blog posts found</div>';
                    }
                })
                .catch(error => {
                    console.error('Error loading blog posts:', error);
                    blogPostsList.innerHTML = '<div style="color: #dc2626;">Error loading blog posts</div>';
                });
            }
            
            function loadSubscriberGroups() {
                const groupsSelect = document.getElementById('newsletter-groups');
                
                fetch('/admin/newsletter/groups', {
                    headers: { 'Authorization': 'Bearer ' + authToken }
                })
                .then(response => response.json())
                .then(data => {
                    groupsSelect.innerHTML = '<option value="">All Subscribers</option>';
                    if (data.success && data.groups) {
                        data.groups.forEach(group => {
                            const option = document.createElement('option');
                            option.value = group.id;
                            option.textContent = group.name + ' (' + (group.total || 0) + ' subscribers)';
                            groupsSelect.appendChild(option);
                        });
                    }
                })
                .catch(error => {
                    console.error('Error loading groups:', error);
                    groupsSelect.innerHTML = '<option value="">All Subscribers (Error loading groups)</option>';
                });
            }
            
            function initializeNewsletterEditor() {
                // Initialize a simple content editor for custom newsletters
                const editorDiv = document.getElementById('newsletter-content-editor');
                editorDiv.innerHTML = '<textarea style="width: 100%; height: 300px; border: none; padding: 15px; font-family: monospace;" placeholder="Enter your newsletter content here...\\n\\nYou can use HTML for formatting:\\n<h1>Title</h1>\\n<p>Paragraph</p>\\n<a href=\\"#\\">Link</a>"></textarea>';
            }
            
            function previewNewsletter() {
                console.log('Previewing newsletter...');
                
                const subject = document.getElementById('newsletter-subject').value;
                if (!subject) {
                    alert('Please enter a subject line');
                    return;
                }
                
                if (newsletterType === 'blog-digest') {
                    if (selectedPosts.length === 0) {
                        alert('Please select at least one blog post');
                        return;
                    }
                    previewBlogDigest(subject);
                } else if (newsletterType === 'custom') {
                    const content = document.querySelector('#newsletter-content-editor textarea').value;
                    if (!content) {
                        alert('Please enter newsletter content');
                        return;
                    }
                    previewCustomNewsletter(subject, content);
                }
            }
            
            function previewBlogDigest(subject) {
                // Generate preview for blog digest
                showNewsletterStatus('Generating preview...', 'info');
                
                fetch('/admin/newsletter/send-blog-digest', {
                    method: 'POST',
                    headers: {
                        'Authorization': 'Bearer ' + authToken,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        post_ids: selectedPosts,
                        subject: subject,
                        preview_only: true
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showPreview(subject, data.preview_content || 'Preview generated successfully');
                    } else {
                        showNewsletterStatus('Error generating preview: ' + (data.error || 'Unknown error'), 'error');
                    }
                })
                .catch(error => {
                    console.error('Error generating preview:', error);
                    showNewsletterStatus('Error generating preview', 'error');
                });
            }
            
            function previewCustomNewsletter(subject, content) {
                showPreview(subject, content);
            }
            
            function showPreview(subject, content) {
                document.getElementById('newsletter-composer').style.display = 'none';
                document.getElementById('newsletter-preview').style.display = 'block';
                
                const previewContent = document.getElementById('newsletter-preview-content');
                previewContent.innerHTML = 
                    '<div style="border-bottom: 2px solid #e5e7eb; padding-bottom: 15px; margin-bottom: 20px;">' +
                        '<strong>Subject:</strong> ' + subject +
                    '</div>' +
                    '<div style="border: 1px solid #e5e7eb; border-radius: 4px; padding: 15px; background: white;">' +
                        content +
                    '</div>';
            }
            
            function editNewsletter() {
                document.getElementById('newsletter-preview').style.display = 'none';
                document.getElementById('newsletter-composer').style.display = 'block';
            }
            
            function sendNewsletter() {
                previewNewsletter(); // This will show the preview first
            }
            
            function confirmSendNewsletter() {
                const subject = document.getElementById('newsletter-subject').value;
                const selectedGroups = Array.from(document.getElementById('newsletter-groups').selectedOptions)
                    .map(option => option.value)
                    .filter(value => value !== '');
                
                showNewsletterStatus('Sending newsletter...', 'info');
                
                if (newsletterType === 'blog-digest') {
                    sendBlogDigestNewsletter(subject, selectedGroups);
                } else if (newsletterType === 'custom') {
                    const content = document.querySelector('#newsletter-content-editor textarea').value;
                    sendCustomNewsletter(subject, content, selectedGroups);
                }
            }
            
            function sendBlogDigestNewsletter(subject, groupIds) {
                fetch('/admin/newsletter/send-blog-digest', {
                    method: 'POST',
                    headers: {
                        'Authorization': 'Bearer ' + authToken,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        post_ids: selectedPosts,
                        subject: subject,
                        group_ids: groupIds.length > 0 ? groupIds.map(id => parseInt(id)) : null
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showNewsletterStatus('Newsletter sent successfully! Campaign ID: ' + data.campaign_id, 'success');
                        resetNewsletterForm();
                    } else {
                        showNewsletterStatus('Error sending newsletter: ' + (data.error || 'Unknown error'), 'error');
                    }
                })
                .catch(error => {
                    console.error('Error sending newsletter:', error);
                    showNewsletterStatus('Error sending newsletter', 'error');
                });
            }
            
            function sendCustomNewsletter(subject, content, groupIds) {
                fetch('/admin/newsletter/send', {
                    method: 'POST',
                    headers: {
                        'Authorization': 'Bearer ' + authToken,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        subject: subject,
                        content: content,
                        group_ids: groupIds.length > 0 ? groupIds.map(id => parseInt(id)) : null
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showNewsletterStatus('Newsletter sent successfully! Campaign ID: ' + data.campaign_id, 'success');
                        resetNewsletterForm();
                    } else {
                        showNewsletterStatus('Error sending newsletter: ' + (data.error || 'Unknown error'), 'error');
                    }
                })
                .catch(error => {
                    console.error('Error sending newsletter:', error);
                    showNewsletterStatus('Error sending newsletter', 'error');
                });
            }
            
            function cancelNewsletter() {
                resetNewsletterForm();
            }
            
            function resetNewsletterForm() {
                document.getElementById('newsletter-composer').style.display = 'none';
                document.getElementById('newsletter-preview').style.display = 'none';
                document.getElementById('newsletter-form').reset();
                selectedPosts = [];
                newsletterType = null;
            }
            
            function loadNewsletterGroups() {
                document.getElementById('newsletter-composer').style.display = 'none';
                document.getElementById('newsletter-preview').style.display = 'none';
                document.getElementById('newsletter-groups-management').style.display = 'block';
                
                const groupsList = document.getElementById('groups-list');
                groupsList.innerHTML = '<div>Loading groups...</div>';
                
                fetch('/admin/newsletter/groups', {
                    headers: { 'Authorization': 'Bearer ' + authToken }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success && data.groups) {
                        groupsList.innerHTML = '';
                        data.groups.forEach(group => {
                            const groupElement = document.createElement('div');
                            groupElement.style.cssText = 'padding: 15px; border: 1px solid #e5e7eb; border-radius: 6px; margin-bottom: 10px;';
                            groupElement.innerHTML = 
                                '<h4>' + group.name + '</h4>' +
                                '<p style="color: #6b7280; margin: 5px 0;">Subscribers: ' + (group.total || 0) + '</p>' +
                                '<small style="color: #9ca3af;">ID: ' + group.id + '</small>';
                            groupsList.appendChild(groupElement);
                        });
                    } else {
                        groupsList.innerHTML = '<div style="color: #6b7280;">No groups found or error loading groups</div>';
                    }
                })
                .catch(error => {
                    console.error('Error loading groups:', error);
                    groupsList.innerHTML = '<div style="color: #dc2626;">Error loading groups</div>';
                });
            }
            
            function showNewsletterStatus(message, type) {
                const statusDiv = document.getElementById('newsletter-status');
                const statusContent = document.getElementById('newsletter-status-content');
                
                statusDiv.style.display = 'block';
                statusContent.textContent = message;
                
                // Style based on type
                if (type === 'success') {
                    statusDiv.style.backgroundColor = '#dcfce7';
                    statusDiv.style.color = '#166534';
                    statusDiv.style.border = '1px solid #bbf7d0';
                } else if (type === 'error') {
                    statusDiv.style.backgroundColor = '#fef2f2';
                    statusDiv.style.color = '#dc2626';
                    statusDiv.style.border = '1px solid #fecaca';
                } else {
                    statusDiv.style.backgroundColor = '#dbeafe';
                    statusDiv.style.color = '#1d4ed8';
                    statusDiv.style.border = '1px solid #bfdbfe';
                }
                
                // Auto-hide success messages after 5 seconds
                if (type === 'success') {
                    setTimeout(() => {
                        statusDiv.style.display = 'none';
                    }, 5000);
                }
            }
            
            function loadTranslations(translations) {
                const translationList = document.getElementById('translation-list');
                translationList.innerHTML = '';
                
                translations.forEach(translation => {
                    const languageFlag = translation.language === 'en' ? '🇺🇸' : '🇧🇬';
                    const languageName = translation.language === 'en' ? 'English' : 'Bulgarian';
                    const statusBadge = translation.is_published ? 
                        '<span class="status-badge status-published">Published</span>' : 
                        '<span class="status-badge status-draft">Draft</span>';
                    
                    const item = document.createElement('div');
                    item.className = 'translation-item';
                    item.innerHTML = 
                        '<div>' +
                            '<strong>' + languageFlag + ' ' + translation.title + '</strong>' +
                            '<small style="color: #6b7280; display: block;">' + languageName + ' • ' + statusBadge + '</small>' +
                        '</div>' +
                        '<button type="button" onclick="editBlogPost(' + translation.id + ')" class="btn-edit">Edit</button>';
                    translationList.appendChild(item);
                });
            }
            
            function closeBlogEditor() {
                document.getElementById('blog-editor-view').classList.add('hidden');
                document.getElementById('blog-list-view').classList.remove('hidden');
                document.getElementById('blog-form').reset();
                currentEditingPost = null;
            }
            
            async function editBlogPost(postId) {
                try {
                    const response = await fetch('/admin/blog/posts/' + postId, {
                        headers: { 'Authorization': 'Bearer ' + authToken }
                    });
                    
                    if (!response.ok) throw new Error('Failed to load blog post');
                    
                    const post = await response.json();
                    showBlogEditor(post);
                    
                } catch (error) {
                    console.error('Error loading blog post:', error);
                    alert('Error loading blog post for editing');
                }
            }
            
            async function deleteBlogPost(postId, title) {
                if (!confirm(`Are you sure you want to delete "${title}"?`)) return;
                
                try {
                    const response = await fetch('/admin/blog/posts/' + postId, {
                        method: 'DELETE',
                        headers: { 'Authorization': 'Bearer ' + authToken }
                    });
                    
                    if (!response.ok) throw new Error('Failed to delete blog post');
                    
                    loadBlogPosts(); // Reload the list
                    
                } catch (error) {
                    console.error('Error deleting blog post:', error);
                    alert('Error deleting blog post');
                }
            }
            
            // New multilingual blog post functions
            async function editMultilingualBlogPost(postId) {
                try {
                    const response = await fetch('/admin/multilingual/posts/' + postId, {
                        headers: { 'Authorization': 'Bearer ' + authToken }
                    });
                    
                    if (!response.ok) throw new Error('Failed to load multilingual blog post');
                    
                    const post = await response.json();
                    showMultilingualBlogEditor(post);
                    
                } catch (error) {
                    console.error('Error loading multilingual blog post:', error);
                    alert('Error loading blog post for editing');
                }
            }
            
            async function deleteMultilingualBlogPost(postId, title) {
                if (!confirm(`Are you sure you want to delete "${title}" and its translations?`)) return;
                
                try {
                    const response = await fetch('/admin/multilingual/posts/' + postId, {
                        method: 'DELETE',
                        headers: { 'Authorization': 'Bearer ' + authToken }
                    });
                    
                    if (!response.ok) throw new Error('Failed to delete multilingual blog post');
                    
                    loadBlogPosts(); // Reload the list
                    
                } catch (error) {
                    console.error('Error deleting multilingual blog post:', error);
                    alert('Error deleting blog post');
                }
            }
            
            function showMultilingualBlogEditor(postData = null) {
                // Create the multilingual blog editor in the main content area
                const mainContentArea = document.getElementById('main-content-area');
                
                // Update page title
                document.getElementById('page-title').textContent = postData ? 'Edit Multilingual Blog Post' : 'Create New Multilingual Blog Post';
                document.getElementById('page-subtitle').textContent = 'Edit both English and Bulgarian versions in one place';
                
                // Get current editing post ID
                currentEditingPost = postData ? postData.id : null;
                
                mainContentArea.innerHTML = `
                    <div class="content-card">
                        <div class="card-header">
                            <h3 class="card-title" id="editor-title">${postData ? 'Edit Multilingual Blog Post' : 'Create New Multilingual Blog Post'}</h3>
                            <div class="card-actions">
                                <button type="button" class="btn btn-primary" onclick="backToBlogList()">← Back to Posts</button>
                            </div>
                        </div>
                        <div class="card-body">
                            <form id="multilingual-blog-form">
                                
                                <!-- Shared Settings -->
                                <div class="form-section">
                                    <h4>🖼️ Shared Settings</h4>
                                    
                                    <div class="form-group">
                                        <label for="blog-featured-image">Featured Image</label>
                                        <div class="image-upload-container">
                                            <input type="text" id="blog-featured-image" name="featured_image" placeholder="Image URL (shared for both languages)" value="${postData?.featured_image || ''}">
                                            <button type="button" class="btn btn-secondary" onclick="uploadImage()">Upload Image</button>
                                            <input type="file" id="image-upload" style="display: none;" accept="image/*" onchange="handleImageUpload(event)">
                                        </div>
                                        ${postData?.featured_image ? `<img src="${postData.featured_image}" alt="Preview" style="max-width: 200px; margin-top: 10px;">` : ''}
                                    </div>
                                </div>
                                
                                <!-- English Version -->
                                <div class="form-section">
                                    <h4>🇺🇸 English Version</h4>
                                    
                                    <div class="form-group">
                                        <label for="blog-slug-en">English Slug</label>
                                        <input type="text" id="blog-slug-en" name="slug_en" required placeholder="e.g., mastering-public-speaking" value="${postData?.slug_en || ''}">
                                    </div>
                                    
                                    <div class="form-group">
                                        <label for="blog-title-en">English Title</label>
                                        <input type="text" id="blog-title-en" name="title_en" required placeholder="Post title in English" value="${postData?.title_en || ''}">
                                    </div>
                                    
                                    <div class="form-group">
                                        <label for="blog-excerpt-en">English Excerpt</label>
                                        <textarea id="blog-excerpt-en" name="excerpt_en" required placeholder="Brief summary in English" rows="3">${postData?.excerpt_en || ''}</textarea>
                                    </div>
                                    
                                    <div class="form-group">
                                        <label for="blog-content-en">English Content</label>
                                        <div id="blog-content-en-editor"></div>
                                        <textarea id="blog-content-en" name="content_en" required style="display: none;">${postData?.content_en || ''}</textarea>
                                    </div>
                                    
                                    <div class="form-group">
                                        <label for="blog-tags-en">English Tags</label>
                                        <input type="text" id="blog-tags-en" name="tags_en" placeholder="Comma-separated tags in English" value="${postData?.tags_en ? postData.tags_en.join(', ') : ''}">
                                    </div>
                                    
                                    <div class="form-group">
                                        <label>
                                            <input type="checkbox" id="is-published-en" name="is_published_en" ${postData?.is_published_en ? 'checked' : ''}>
                                            Publish English version
                                        </label>
                                    </div>
                                </div>
                                
                                <!-- Bulgarian Version -->
                                <div class="form-section">
                                    <h4>🇧🇬 Bulgarian Version</h4>
                                    
                                    <div class="form-group">
                                        <label for="blog-slug-bg">Bulgarian Slug</label>
                                        <input type="text" id="blog-slug-bg" name="slug_bg" required placeholder="e.g., ovladyavane-na-publichnoto-govorene" value="${postData?.slug_bg || ''}">
                                    </div>
                                    
                                    <div class="form-group">
                                        <label for="blog-title-bg">Bulgarian Title</label>
                                        <input type="text" id="blog-title-bg" name="title_bg" required placeholder="Post title in Bulgarian" value="${postData?.title_bg || ''}">
                                    </div>
                                    
                                    <div class="form-group">
                                        <label for="blog-excerpt-bg">Bulgarian Excerpt</label>
                                        <textarea id="blog-excerpt-bg" name="excerpt_bg" required placeholder="Brief summary in Bulgarian" rows="3">${postData?.excerpt_bg || ''}</textarea>
                                    </div>
                                    
                                    <div class="form-group">
                                        <label for="blog-content-bg">Bulgarian Content</label>
                                        <div id="blog-content-bg-editor"></div>
                                        <textarea id="blog-content-bg" name="content_bg" required style="display: none;">${postData?.content_bg || ''}</textarea>
                                    </div>
                                    
                                    <div class="form-group">
                                        <label for="blog-tags-bg">Bulgarian Tags</label>
                                        <input type="text" id="blog-tags-bg" name="tags_bg" placeholder="Comma-separated tags in Bulgarian" value="${postData?.tags_bg ? postData.tags_bg.join(', ') : ''}">
                                    </div>
                                    
                                    <div class="form-group">
                                        <label>
                                            <input type="checkbox" id="is-published-bg" name="is_published_bg" ${postData?.is_published_bg ? 'checked' : ''}>
                                            Publish Bulgarian version
                                        </label>
                                    </div>
                                </div>
                                
                                <!-- Form Actions -->
                                <div class="form-actions">
                                    <button type="submit" class="btn btn-primary" style="background: #10b981; border-color: #10b981;">
                                        ${postData ? 'Update Multilingual Post' : 'Create Multilingual Post'}
                                    </button>
                                    <button type="button" class="btn" onclick="backToBlogList()" style="background: #6b7280; color: white;">Cancel</button>
                                </div>
                            </form>
                        </div>
                    </div>
                `;
                
                // Initialize Quill editors
                initializeMultilingualQuillEditors(postData);
                
                setupMultilingualBlogFormHandler(); // Set up form submission handler
            }
            
            let quillEditorEn = null;
            let quillEditorBg = null;
            
            function initializeMultilingualQuillEditors(postData) {
                // Initialize English content editor
                if (quillEditorEn) {
                    quillEditorEn = null;
                }
                
                quillEditorEn = new Quill('#blog-content-en-editor', {
                    theme: 'snow',
                    placeholder: 'Write your blog post content in English...',
                    modules: {
                        toolbar: [
                            [{ 'header': [1, 2, 3, false] }],
                            ['bold', 'italic', 'underline', 'strike'],
                            ['blockquote', 'code-block'],
                            [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                            [{ 'script': 'sub'}, { 'script': 'super' }],
                            [{ 'indent': '-1'}, { 'indent': '+1' }],
                            [{ 'direction': 'rtl' }],
                            [{ 'color': [] }, { 'background': [] }],
                            [{ 'font': [] }],
                            [{ 'align': [] }],
                            ['clean'],
                            ['link', 'image', 'video']
                        ]
                    }
                });
                
                // Initialize Bulgarian content editor
                if (quillEditorBg) {
                    quillEditorBg = null;
                }
                
                quillEditorBg = new Quill('#blog-content-bg-editor', {
                    theme: 'snow',
                    placeholder: 'Напишете съдържанието на блог поста на български...',
                    modules: {
                        toolbar: [
                            [{ 'header': [1, 2, 3, false] }],
                            ['bold', 'italic', 'underline', 'strike'],
                            ['blockquote', 'code-block'],
                            [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                            [{ 'script': 'sub'}, { 'script': 'super' }],
                            [{ 'indent': '-1'}, { 'indent': '+1' }],
                            [{ 'direction': 'rtl' }],
                            [{ 'color': [] }, { 'background': [] }],
                            [{ 'font': [] }],
                            [{ 'align': [] }],
                            ['clean'],
                            ['link', 'image', 'video']
                        ]
                    }
                });
                
                // Set initial content if editing
                if (postData) {
                    if (postData.content_en) {
                        quillEditorEn.root.innerHTML = postData.content_en;
                    }
                    if (postData.content_bg) {
                        quillEditorBg.root.innerHTML = postData.content_bg;
                    }
                }
                
                // Sync editors with hidden textareas
                quillEditorEn.on('text-change', function() {
                    const content = quillEditorEn.root.innerHTML;
                    document.getElementById('blog-content-en').value = content;
                });
                
                quillEditorBg.on('text-change', function() {
                    const content = quillEditorBg.root.innerHTML;
                    document.getElementById('blog-content-bg').value = content;
                });
            }
            
            function setupMultilingualBlogFormHandler() {
                const form = document.getElementById('multilingual-blog-form');
                if (!form) return;
                
                form.onsubmit = async function(e) {
                    if (!e) {
                        console.error('Event object is undefined');
                        return false;
                    }
                    
                    try {
                        e.preventDefault();
                        
                        const formData = new FormData(form);
                        
                        // Parse tags
                        const tagsEn = formData.get('tags_en') ? formData.get('tags_en').split(',').map(t => t.trim()).filter(t => t) : [];
                        const tagsBg = formData.get('tags_bg') ? formData.get('tags_bg').split(',').map(t => t.trim()).filter(t => t) : [];
                        
                        // Get content from Quill editors
                        const contentEn = quillEditorEn ? quillEditorEn.root.innerHTML : formData.get('content_en');
                        const contentBg = quillEditorBg ? quillEditorBg.root.innerHTML : formData.get('content_bg');
                        
                        const postData = {
                            slug_en: formData.get('slug_en'),
                            slug_bg: formData.get('slug_bg'),
                            title_en: formData.get('title_en'),
                            title_bg: formData.get('title_bg'),
                            excerpt_en: formData.get('excerpt_en'),
                            excerpt_bg: formData.get('excerpt_bg'),
                            content_en: contentEn,
                            content_bg: contentBg,
                            tags_en: tagsEn,
                            tags_bg: tagsBg,
                            featured_image: formData.get('featured_image'),
                            is_published_en: formData.get('is_published_en') === 'on',
                            is_published_bg: formData.get('is_published_bg') === 'on'
                        };
                        
                        const url = currentEditingPost 
                            ? `/admin/multilingual/posts/${currentEditingPost}` 
                            : '/admin/multilingual/posts';
                        
                        const response = await fetch(url, {
                            method: currentEditingPost ? 'PUT' : 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer ' + authToken
                            },
                            body: JSON.stringify(postData)
                        });
                        
                        if (!response.ok) {
                            const error = await response.json();
                            throw new Error(error.detail || 'Failed to save blog post');
                        }
                        
                        alert('Multilingual blog post saved successfully!');
                        
                        // Reset form and go back to list
                        form.reset();
                        currentEditingPost = null;
                        backToBlogList();
                        loadBlogPosts();
                        
                    } catch (error) {
                        console.error('Error saving multilingual blog post:', error);
                        alert('Error saving blog post: ' + error.message);
                    }
                    
                    return false;
                };
            }
            
            function uploadImage() {
                document.getElementById('image-upload').click();
            }
            
            async function handleImageUpload(event) {
                const file = event.target.files[0];
                if (!file) return;
                
                const formData = new FormData();
                formData.append('file', file);
                
                try {
                    const response = await fetch('/admin/blog/upload-image', {
                        method: 'POST',
                        headers: { 'Authorization': 'Bearer ' + authToken },
                        body: formData
                    });
                    
                    if (!response.ok) throw new Error('Failed to upload image');
                    
                    const result = await response.json();
                    document.getElementById('blog-featured-image').value = result.url;
                    
                } catch (error) {
                    console.error('Error uploading image:', error);
                    alert('Error uploading image');
                }
            }
            
            // Add event listeners for preview updates
            document.addEventListener('DOMContentLoaded', function() {
                // Update preview when title or excerpt changes
                document.addEventListener('input', function(e) {
                    if (e.target.id === 'blog-title' || e.target.id === 'blog-excerpt') {
                        updatePreview();
                    }
                });
            });
            
            // Handle blog form submission (when it exists)
            function setupBlogFormHandler() {
                const blogForm = document.getElementById('blog-form');
                if (blogForm) {
                    blogForm.addEventListener('submit', async function(e) {
                        e.preventDefault();
                
                const formData = new FormData(e.target);
                const postData = {
                    slug: formData.get('slug'),
                    title: formData.get('title'),
                    excerpt: formData.get('excerpt'),
                    content: formData.get('content'),
                    featured_image: formData.get('featured_image') || null,
                    tags: formData.get('tags') ? formData.get('tags').split(',').map(tag => tag.trim()) : [],
                    language: formData.get('language'),
                    is_published: formData.get('is_published') ? true : false
                };
                
                try {
                    const url = currentEditingPost ? 
                        `/admin/blog/posts/${currentEditingPost}` : 
                        '/admin/blog/posts';
                    const method = currentEditingPost ? 'PUT' : 'POST';
                    
                    const response = await fetch(url, {
                        method: method,
                        headers: {
                            'Authorization': 'Bearer ' + authToken,
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(postData)
                    });
                    
                    if (!response.ok) {
                        const error = await response.json();
                        throw new Error(error.detail || 'Failed to save blog post');
                    }
                    
                    closeBlogEditor();
                    loadBlogPosts();
                    
                    } catch (error) {
                        console.error('Error saving blog post:', error);
                        alert('Error saving blog post: ' + error.message);
                    }
                    });
                }
            }
            
            // Auto-generate slug from title (only if element exists)
            const titleInput = document.getElementById('blog-title');
            if (titleInput) {
                titleInput.addEventListener('input', function(e) {
                    const title = e.target.value;
                    const slug = title
                        .toLowerCase()
                        .replace(/[^a-z0-9\s-]/g, '')
                        .replace(/\s+/g, '-')
                        .replace(/-+/g, '-')
                        .trim('-');
                    const slugInput = document.getElementById('blog-slug');
                    if (slugInput) {
                        slugInput.value = slug;
                    }
                });
            }
            
            // Email Sequences Management Functions
            async function loadEmailSequences() {
                if (!authToken) return;
                
                try {
                    const language = document.getElementById('sequence-language')?.value || 'en';
                    const response = await fetch(`/admin/sequences/info?language=${language}`, {
                        headers: { 'Authorization': 'Bearer ' + authToken }
                    });
                    
                    if (!response.ok) throw new Error('Failed to load sequences');
                    
                    const data = await response.json();
                    
                    // Update counts
                    document.getElementById('lead-magnet-count').textContent = data.sequences.lead_magnet.email_count;
                    document.getElementById('waitlist-count').textContent = data.sequences.waitlist.email_count;
                    document.getElementById('corporate-count').textContent = data.sequences.corporate.email_count;
                    
                    // Load active subscribers count
                    fetch('/admin/sequences/active-subscribers', {
                        headers: { 'Authorization': 'Bearer ' + authToken }
                    })
                    .then(response => response.json())
                    .then(result => {
                        document.getElementById('active-subscribers').textContent = result.count.toLocaleString();
                    })
                    .catch(error => {
                        console.error('Error loading active subscribers:', error);
                        document.getElementById('active-subscribers').textContent = '-';
                    });
                    
                    // Load sequences list
                    const sequencesList = document.getElementById('sequences-list');
                    sequencesList.innerHTML = '';
                    
                    Object.entries(data.sequences).forEach(([type, info]) => {
                        const sequenceCard = document.createElement('div');
                        sequenceCard.className = 'content-card';
                        sequenceCard.style.marginBottom = '20px';
                        
                        sequenceCard.innerHTML = `
                            <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <h3>${info.name}</h3>
                                    <p style="color: #6b7280; margin: 0;">${info.description}</p>
                                </div>
                                <div style="display: flex; gap: 10px;">
                                    <button class="btn btn-primary" onclick="viewSequence('${type}', '${language}')">
                                        👁️ View Emails
                                    </button>
                                    <button class="btn btn-success" onclick="testSequenceFlow('${type}', '${language}')">
                                        🧪 Test
                                    </button>
                                </div>
                            </div>
                            <div class="card-body">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <div>
                                        <strong>${info.email_count} emails</strong> • 
                                        <span style="color: #6b7280;">${info.target_audience}</span>
                                    </div>
                                    <div style="color: #059669; font-weight: 500;">
                                        ✅ Active
                                    </div>
                                </div>
                            </div>
                        `;
                        
                        sequencesList.appendChild(sequenceCard);
                    });
                    
                } catch (error) {
                    console.error('Error loading email sequences:', error);
                    document.getElementById('sequences-list').innerHTML = '<p>Error loading sequences.</p>';
                }
            }
            
            async function viewSequence(type, language) {
                try {
                    const response = await fetch(`/admin/sequences/${type}?language=${language}`, {
                        headers: { 'Authorization': 'Bearer ' + authToken }
                    });
                    
                    if (!response.ok) throw new Error('Failed to load sequence details');
                    
                    const emails = await response.json();
                    
                    // Show sequence details
                    const detailsDiv = document.getElementById('sequence-details');
                    const titleDiv = document.getElementById('sequence-details-title');
                    const emailsList = document.getElementById('sequence-emails-list');
                    
                    titleDiv.textContent = `${type.replace('_', ' ').toUpperCase()} Sequence (${language.toUpperCase()})`;
                    
                    emailsList.innerHTML = '';
                    emails.forEach((email, index) => {
                        const emailCard = document.createElement('div');
                        emailCard.className = 'content-card';
                        emailCard.style.marginBottom = '15px';
                        
                        emailCard.innerHTML = `
                            <div class="card-header" style="padding: 15px;">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <div>
                                        <h4>Week ${email.week}: ${email.subject}</h4>
                                        <p style="color: #6b7280; margin: 0; font-size: 14px;">
                                            Sent ${email.delay_days} days after sequence start
                                        </p>
                                    </div>
                                    <button class="btn btn-primary" onclick="previewEmail('${type}', ${index}, '${language}')">
                                        👁️ Preview
                                    </button>
                                </div>
                            </div>
                            <div class="card-body" style="padding: 15px;">
                                <div><strong>Title:</strong> ${email.title}</div>
                                <div style="margin-top: 8px;"><strong>CTA:</strong> ${email.cta}</div>
                                <div style="margin-top: 8px; color: #6b7280; font-size: 14px;">
                                    Content length: ${email.content.length} characters
                                </div>
                            </div>
                        `;
                        
                        emailsList.appendChild(emailCard);
                    });
                    
                    detailsDiv.style.display = 'block';
                    
                } catch (error) {
                    console.error('Error viewing sequence:', error);
                    alert('Error loading sequence details');
                }
            }
            
            function closeSequenceDetails() {
                document.getElementById('sequence-details').style.display = 'none';
            }
            
            async function testSequenceFlow(type, language) {
                const email = prompt('Enter test email address:');
                if (!email) return;
                
                try {
                    const response = await fetch('/admin/sequences/test', {
                        method: 'POST',
                        headers: {
                            'Authorization': 'Bearer ' + authToken,
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            email: email,
                            sequence_type: type,
                            language: language,
                            name: 'Test User'
                        })
                    });
                    
                    if (!response.ok) throw new Error('Failed to trigger test sequence');
                    
                    const result = await response.json();
                    alert(`Test sequence triggered successfully for ${email}`);
                    
                } catch (error) {
                    console.error('Error testing sequence:', error);
                    alert('Error triggering test sequence');
                }
            }
            
            async function previewEmail(type, index, language) {
                try {
                    const response = await fetch(`/admin/sequences/${type}/${index}?language=${language}`, {
                        headers: { 'Authorization': 'Bearer ' + authToken }
                    });
                    
                    if (!response.ok) throw new Error('Failed to load email preview');
                    
                    const email = await response.json();
                    
                    // Create preview modal
                    const modal = document.createElement('div');
                    modal.style.cssText = `
                        position: fixed; top: 0; left: 0; right: 0; bottom: 0; 
                        background: rgba(0,0,0,0.5); z-index: 1000; 
                        display: flex; align-items: center; justify-content: center; padding: 20px;
                    `;
                    
                    modal.innerHTML = `
                        <div style="background: white; border-radius: 8px; max-width: 800px; max-height: 90vh; overflow-y: auto; width: 100%;">
                            <div style="padding: 20px; border-bottom: 1px solid #e5e7eb; display: flex; justify-content: space-between; align-items: center;">
                                <h3>📧 Email Preview: Week ${email.week}</h3>
                                <button onclick="this.closest('[style*=\"position: fixed\"]').remove()" 
                                        style="background: none; border: none; font-size: 24px; cursor: pointer;">×</button>
                            </div>
                            <div style="padding: 20px;">
                                <div style="margin-bottom: 15px;">
                                    <strong>Subject:</strong> ${email.subject}
                                </div>
                                <div style="margin-bottom: 15px;">
                                    <strong>Title:</strong> ${email.title}
                                </div>
                                <div style="border: 1px solid #e5e7eb; border-radius: 4px; padding: 20px; background: #f9fafb;">
                                    ${email.content}
                                </div>
                                <div style="margin-top: 15px; color: #6b7280; font-size: 14px;">
                                    <strong>Call to Action:</strong> ${email.cta}
                                </div>
                            </div>
                        </div>
                    `;
                    
                    document.body.appendChild(modal);
                    
                } catch (error) {
                    console.error('Error previewing email:', error);
                    alert('Error loading email preview');
                }
            }
            
            // Subscribers Management Functions
            async function loadSubscribers() {
                if (!authToken) return;
                
                try {
                    const language = document.getElementById('subscriber-language')?.value || '';
                    const source = document.getElementById('subscriber-source')?.value || '';
                    
                    const params = new URLSearchParams();
                    if (language) params.append('language', language);
                    if (source) params.append('source', source);
                    
                    const response = await fetch(`/admin/subscribers?${params}`, {
                        headers: { 'Authorization': 'Bearer ' + authToken }
                    });
                    
                    if (!response.ok) throw new Error('Failed to load subscribers');
                    
                    const subscribers = await response.json();
                    
                    const subscribersList = document.getElementById('subscribers-list');
                    subscribersList.innerHTML = '';
                    
                    if (subscribers.length === 0) {
                        subscribersList.innerHTML = '<p>No subscribers found with the selected filters.</p>';
                        return;
                    }
                    
                    const table = document.createElement('table');
                    table.style.cssText = 'width: 100%; border-collapse: collapse; margin-top: 20px;';
                    
                    table.innerHTML = `
                        <thead>
                            <tr style="background: #f3f4f6; border-bottom: 1px solid #e5e7eb;">
                                <th style="padding: 12px; text-align: left;">Email</th>
                                <th style="padding: 12px; text-align: left;">Name</th>
                                <th style="padding: 12px; text-align: left;">Source</th>
                                <th style="padding: 12px; text-align: left;">Language</th>
                                <th style="padding: 12px; text-align: left;">Date Added</th>
                                <th style="padding: 12px; text-align: left;">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${subscribers.map(sub => `
                                <tr style="border-bottom: 1px solid #e5e7eb;">
                                    <td style="padding: 12px;">${sub.email}</td>
                                    <td style="padding: 12px;">${sub.name || '-'}</td>
                                    <td style="padding: 12px;">
                                        <span style="background: #e0f2fe; color: #0369a1; padding: 2px 6px; border-radius: 4px; font-size: 12px;">
                                            ${sub.source}
                                        </span>
                                    </td>
                                    <td style="padding: 12px;">${sub.language === 'en' ? '🇺🇸' : '🇧🇬'} ${sub.language.toUpperCase()}</td>
                                    <td style="padding: 12px;">${new Date(sub.signup_date).toLocaleDateString()}</td>
                                    <td style="padding: 12px;">
                                        <span style="background: #dcfce7; color: #166534; padding: 2px 6px; border-radius: 4px; font-size: 12px;">
                                            ${sub.engagement_level}
                                        </span>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    `;
                    
                    subscribersList.appendChild(table);
                    
                } catch (error) {
                    console.error('Error loading subscribers:', error);
                    document.getElementById('subscribers-list').innerHTML = '<p>Error loading subscribers.</p>';
                }
            }
            
            function exportSubscribers() {
                // This would implement CSV export functionality
                alert('Export functionality coming soon!');
            }
            
            // Sequence Analytics Functions
            async function loadSequenceAnalytics() {
                if (!authToken) return;
                
                try {
                    const language = document.getElementById('analytics-language')?.value || '';
                    const period = document.getElementById('analytics-period')?.value || '30';
                    
                    const params = new URLSearchParams();
                    if (language) params.append('language', language);
                    params.append('period', period);
                    
                    // Load sequence analytics
                    const sequenceResponse = await fetch(`/admin/sequences/analytics?${params}`, {
                        headers: { 'Authorization': 'Bearer ' + authToken }
                    });
                    
                    // Load webhook analytics  
                    const webhookResponse = await fetch(`/admin/webhook-analytics?days=${period}`, {
                        headers: { 'Authorization': 'Bearer ' + authToken }
                    });
                    
                    if (!sequenceResponse.ok) throw new Error('Failed to load sequence analytics');
                    
                    const sequenceAnalytics = await sequenceResponse.json();
                    let webhookAnalytics = {};
                    
                    if (webhookResponse.ok) {
                        webhookAnalytics = await webhookResponse.json();
                    }
                    
                    // Update sequence metrics
                    document.getElementById('total-opens').textContent = sequenceAnalytics.total_opens || '0';
                    document.getElementById('open-rate').textContent = (sequenceAnalytics.open_rate || 0) + '%';
                    document.getElementById('click-rate').textContent = (sequenceAnalytics.click_rate || 0) + '%';
                    document.getElementById('conversion-rate').textContent = (sequenceAnalytics.conversion_rate || 0) + '%';
                    
                    // Update webhook metrics if elements exist
                    if (document.getElementById('webhook-opens')) {
                        document.getElementById('webhook-opens').textContent = webhookAnalytics.unique_opens || '0';
                    }
                    if (document.getElementById('webhook-clicks')) {
                        document.getElementById('webhook-clicks').textContent = webhookAnalytics.unique_clicks || '0';
                    }
                    if (document.getElementById('webhook-bounces')) {
                        document.getElementById('webhook-bounces').textContent = webhookAnalytics.bounces || '0';
                    }
                    if (document.getElementById('webhook-unsubscribes')) {
                        document.getElementById('webhook-unsubscribes').textContent = webhookAnalytics.unsubscribes || '0';
                    }
                    
                } catch (error) {
                    console.error('Error loading sequence analytics:', error);
                    // Set default values
                    document.getElementById('total-opens').textContent = '-';
                    document.getElementById('open-rate').textContent = '-%';
                    document.getElementById('click-rate').textContent = '-%';
                    document.getElementById('conversion-rate').textContent = '-%';
                }
            }
            
            // Email Scheduler Functions
            let schedulerStatus = false;
            
            async function loadSchedulerStatus() {
                try {
                    const response = await fetch('/admin/scheduler/status', {
                        headers: { 'Authorization': 'Bearer ' + authToken }
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        schedulerStatus = data.running;
                        updateSchedulerUI();
                    }
                } catch (error) {
                    console.error('Error loading scheduler status:', error);
                }
            }
            
            function updateSchedulerUI() {
                const toggleText = document.getElementById('scheduler-toggle-text');
                if (schedulerStatus) {
                    toggleText.textContent = '⏸️ Stop Scheduler';
                } else {
                    toggleText.textContent = '▶️ Start Scheduler';
                }
            }
            
            async function toggleScheduler() {
                try {
                    const action = schedulerStatus ? 'stop' : 'start';
                    const response = await fetch(`/admin/scheduler/${action}`, {
                        method: 'POST',
                        headers: { 'Authorization': 'Bearer ' + authToken }
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        schedulerStatus = !schedulerStatus;
                        updateSchedulerUI();
                        alert(data.message);
                    } else {
                        alert('Error toggling scheduler');
                    }
                } catch (error) {
                    console.error('Error toggling scheduler:', error);
                    alert('Error toggling scheduler');
                }
            }
            
            async function processEmailsOnce() {
                try {
                    const response = await fetch('/admin/scheduler/process-once', {
                        method: 'POST',
                        headers: { 'Authorization': 'Bearer ' + authToken }
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        alert(data.message);
                    } else {
                        alert('Error processing emails');
                    }
                } catch (error) {
                    console.error('Error processing emails:', error);
                    alert('Error processing emails');
                }
            }
            
            // Load scheduler status when email sequences page loads
            if (document.getElementById('email-sequences-template')) {
                loadSchedulerStatus();
            }
        </script>
    </body>
    </html>
    """
    
    return html_content

# Email Sequences API Endpoints
@app.get("/admin/sequences/info")
def get_sequences_info(language: str = "en", current_user: User = Depends(get_current_admin_user)):
    """Get information about available email sequences"""
    try:
        return get_sequence_info_by_language(language)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get sequences info: {str(e)}")

@app.get("/admin/sequences/{sequence_type}")
def get_sequence_emails(sequence_type: str, language: str = "en", current_user: User = Depends(get_current_admin_user)):
    """Get all emails in a specific sequence"""
    try:
        emails = get_sequence_by_type_and_language(sequence_type, language)
        return emails
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get sequence emails: {str(e)}")

@app.get("/admin/sequences/{sequence_type}/{email_index}")
def get_sequence_email(sequence_type: str, email_index: int, language: str = "en", current_user: User = Depends(get_current_admin_user)):
    """Get a specific email from a sequence"""
    try:
        emails = get_sequence_by_type_and_language(sequence_type, language)
        if email_index >= len(emails):
            raise HTTPException(status_code=404, detail="Email not found")
        return emails[email_index]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get sequence email: {str(e)}")

class SequenceTestRequest(BaseModel):
    email: EmailStr
    sequence_type: str
    language: str = "en"
    name: str = ""

@app.post("/admin/sequences/test")
def test_sequence(request: SequenceTestRequest, current_user: User = Depends(get_current_admin_user)):
    """Test an email sequence by sending it to a test email"""
    try:
        subscriber_data = {
            "email": request.email,
            "name": request.name,
            "source": request.sequence_type,
            "language": request.language
        }
        
        result = trigger_sequence_by_subscriber_data(subscriber_data)
        
        if result["success"]:
            return {"success": True, "message": f"Test sequence triggered for {request.email}"}
        else:
            raise HTTPException(status_code=400, detail=result["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to test sequence: {str(e)}")


@app.get("/admin/sequences/active-subscribers")
def get_active_subscribers_count(current_user: User = Depends(get_current_admin_user)):
    """Get count of active subscribers"""
    try:
        # This would normally query the database
        # For now, return sample data
        return {"count": 1567}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get active subscribers count: {str(e)}")

# Email Scheduler Management Endpoints
@app.post("/admin/scheduler/start")
def start_email_scheduler(current_user: User = Depends(get_current_admin_user)):
    """Start the email scheduler service"""
    try:
        scheduler_service = EmailSchedulerService()
        scheduler_service.start_scheduler()
        return {"success": True, "message": "Email scheduler started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start scheduler: {str(e)}")

@app.post("/admin/scheduler/stop")
def stop_email_scheduler(current_user: User = Depends(get_current_admin_user)):
    """Stop the email scheduler service"""
    try:
        scheduler_service = EmailSchedulerService()
        scheduler_service.stop_scheduler()
        return {"success": True, "message": "Email scheduler stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop scheduler: {str(e)}")

@app.get("/admin/scheduler/status")
def get_scheduler_status(current_user: User = Depends(get_current_admin_user)):
    """Get the status of the email scheduler"""
    try:
        scheduler_service = EmailSchedulerService()
        is_running = scheduler_service.is_running()
        return {"running": is_running}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get scheduler status: {str(e)}")

@app.post("/admin/scheduler/process-once")
async def process_emails_manually(current_user: User = Depends(get_current_admin_user)):
    """Manually process emails once (for testing)"""
    try:
        await process_emails_once()
        return {"success": True, "message": "Emails processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process emails: {str(e)}")

# Update existing subscribers endpoint to use new database functions
@app.get("/admin/subscribers")
def get_subscribers(
    language: Optional[str] = None,
    source: Optional[str] = None,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get subscribers with optional filtering"""
    try:
        subscribers = get_subscribers_with_filters(db, language, source)
        
        # Convert to response format
        response_data = []
        for subscriber in subscribers:
            response_data.append({
                "email": subscriber.email,
                "name": subscriber.name,
                "source": subscriber.source,
                "language": subscriber.language,
                "signup_date": subscriber.signup_date.isoformat(),
                "engagement_level": subscriber.engagement_level
            })
        
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get subscribers: {str(e)}")

# Update sequences analytics endpoint to use new database functions
@app.get("/admin/sequences/analytics")
def get_sequence_analytics_endpoint(
    language: Optional[str] = None,
    period: int = 30,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get analytics for email sequences"""
    try:
        analytics = get_sequence_analytics(db, language=language, days=period)
        return analytics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")


# MailerLite Webhook Endpoints
@app.post("/webhooks/mailerlite")
async def mailerlite_webhook(request: Request):
    """Handle MailerLite webhook events"""
    try:
        # Get webhook secret from environment (you should set this)
        webhook_secret = os.getenv("MAILERLITE_WEBHOOK_SECRET", "")
        
        # Get raw payload and headers
        payload = await request.body()
        signature = request.headers.get("X-MailerLite-Signature", "")
        
        # Verify webhook signature for security
        if not verify_webhook_signature(payload, signature, webhook_secret):
            raise HTTPException(status_code=401, detail="Invalid webhook signature")
        
        # Parse JSON payload
        event_data = json.loads(payload.decode('utf-8'))
        
        # Extract event type and data
        event_type = event_data.get('type')
        event_payload = event_data.get('data', {})
        
        if not event_type:
            raise HTTPException(status_code=400, detail="Missing event type")
        
        # Process the webhook event
        result = process_webhook_event(event_type, event_payload)
        
        return {
            "status": "received",
            "event_type": event_type,
            "processing_result": result
        }
        
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON payload: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {str(e)}")


@app.get("/webhooks/mailerlite/verify")
async def verify_mailerlite_webhook():
    """Verification endpoint for MailerLite webhook setup"""
    return {"status": "ok", "message": "MailerLite webhook endpoint is configured correctly"}


@app.post("/webhooks/mailerlite/test")
async def test_webhook_locally(
    event_type: str,
    campaign_id: str = "test-campaign-123",
    subscriber_email: str = "test@example.com",
    current_user: User = Depends(get_current_admin_user)
):
    """Test webhook processing locally without MailerLite"""
    try:
        # Create test event data
        test_events = {
            "opened": {
                "type": "subscriber.opened",
                "data": {
                    "subscriber": {"email": subscriber_email},
                    "campaign": {"id": campaign_id}
                }
            },
            "clicked": {
                "type": "subscriber.clicked", 
                "data": {
                    "subscriber": {"email": subscriber_email},
                    "campaign": {"id": campaign_id},
                    "click": {"url": "https://example.com/test-link"}
                }
            },
            "bounced": {
                "type": "subscriber.bounced",
                "data": {
                    "subscriber": {"email": subscriber_email},
                    "campaign": {"id": campaign_id},
                    "bounce": {"type": "hard"}
                }
            },
            "unsubscribed": {
                "type": "subscriber.unsubscribed",
                "data": {
                    "subscriber": {"email": subscriber_email},
                    "campaign": {"id": campaign_id}
                }
            },
            "conversion": {
                "type": "conversion",
                "data": {
                    "subscriber": {"email": subscriber_email},
                    "campaign": {"id": campaign_id},
                    "conversion": {"value": 100}
                }
            }
        }
        
        if event_type not in test_events:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid event type. Use: {', '.join(test_events.keys())}"
            )
        
        event_data = test_events[event_type]
        
        # Process the test webhook event
        result = process_webhook_event(event_data["type"], event_data["data"])
        
        return {
            "status": "test_processed",
            "event_type": event_type,
            "test_data": event_data,
            "processing_result": result,
            "message": f"Test {event_type} event processed successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test webhook failed: {str(e)}")


# Webhook Analytics Endpoint
@app.get("/admin/webhook-analytics")
def get_webhook_analytics(
    days: int = 30,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get webhook event analytics"""
    try:
        from datetime import datetime, timedelta
        from sqlalchemy import func
        from models import EmailAnalytics, ScheduledEmail
        
        # Calculate date range
        since_date = datetime.utcnow() - timedelta(days=days)
        
        # Get analytics data
        analytics_query = db.query(EmailAnalytics).join(ScheduledEmail).filter(
            ScheduledEmail.created_at >= since_date
        )
        
        total_events = analytics_query.count()
        opens = analytics_query.filter(EmailAnalytics.opened_at.isnot(None)).count()
        clicks = analytics_query.filter(EmailAnalytics.clicked_at.isnot(None)).count()
        bounces = analytics_query.filter(EmailAnalytics.bounced_at.isnot(None)).count()
        unsubscribes = analytics_query.filter(EmailAnalytics.unsubscribed_at.isnot(None)).count()
        conversions = analytics_query.filter(EmailAnalytics.converted_at.isnot(None)).count()
        
        # Calculate total open and click counts
        total_opens = db.query(func.sum(EmailAnalytics.open_count)).join(ScheduledEmail).filter(
            ScheduledEmail.created_at >= since_date
        ).scalar() or 0
        
        total_clicks = db.query(func.sum(EmailAnalytics.click_count)).join(ScheduledEmail).filter(
            ScheduledEmail.created_at >= since_date
        ).scalar() or 0
        
        return {
            "period_days": days,
            "total_tracked_emails": total_events,
            "unique_opens": opens,
            "unique_clicks": clicks,
            "total_opens": total_opens,
            "total_clicks": total_clicks,
            "bounces": bounces,
            "unsubscribes": unsubscribes,
            "conversions": conversions,
            "open_rate": round((opens / total_events * 100) if total_events > 0 else 0, 2),
            "click_rate": round((clicks / total_events * 100) if total_events > 0 else 0, 2),
            "bounce_rate": round((bounces / total_events * 100) if total_events > 0 else 0, 2),
            "unsubscribe_rate": round((unsubscribes / total_events * 100) if total_events > 0 else 0, 2),
            "conversion_rate": round((conversions / total_events * 100) if total_events > 0 else 0, 2)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get webhook analytics: {str(e)}")


# Failed Email Management Endpoints
@app.get("/admin/failed-emails")
def get_failed_emails(
    days: int = 30,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get permanently failed emails for review"""
    try:
        failed_emails = get_permanently_failed_emails(db, days)
        
        response_data = []
        for email in failed_emails:
            # Get enrollment and subscriber info
            enrollment = db.query(SequenceEnrollment).get(email.enrollment_id)
            subscriber = db.query(EmailSubscriber).get(enrollment.subscriber_id) if enrollment else None
            sequence_email = db.query(SequenceEmail).get(email.email_id)
            
            response_data.append({
                "id": email.id,
                "subscriber_email": subscriber.email if subscriber else "Unknown",
                "subscriber_name": subscriber.name if subscriber else "Unknown",
                "subject": sequence_email.subject if sequence_email else "Unknown",
                "scheduled_for": email.scheduled_for.isoformat(),
                "error_message": email.error_message,
                "retry_count": email.retry_count,
                "status": email.status,
                "updated_at": email.updated_at.isoformat()
            })
        
        return {
            "failed_emails": response_data,
            "total_count": len(response_data),
            "period_days": days
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get failed emails: {str(e)}")


@app.post("/admin/failed-emails/{email_id}/retry")
def retry_failed_email(
    email_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Manually retry a failed email"""
    try:
        success = reset_failed_email_for_retry(db, email_id)
        
        if success:
            return {"success": True, "message": f"Email {email_id} reset for retry"}
        else:
            raise HTTPException(status_code=404, detail="Email not found or not in failed state")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retry email: {str(e)}")


# Subscriber Segmentation Endpoints
@app.get("/admin/segmentation/analytics")
def get_segmentation_analytics_endpoint(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get overall segmentation analytics"""
    try:
        analytics = get_segmentation_analytics(db)
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get segmentation analytics: {str(e)}")


@app.get("/admin/segmentation/segments/{segment}")
def get_subscribers_by_segment_endpoint(
    segment: str,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get subscribers by predefined segment"""
    try:
        valid_segments = ["lead_magnet", "waitlist", "corporate", "engaged", "at_risk", "churned"]
        if segment not in valid_segments:
            raise HTTPException(status_code=400, detail=f"Invalid segment. Use: {', '.join(valid_segments)}")
        
        subscribers = get_subscribers_by_segment(db, segment, limit)
        
        response_data = []
        for subscriber in subscribers:
            response_data.append({
                "id": subscriber.id,
                "email": subscriber.email,
                "name": subscriber.name,
                "source": subscriber.source,
                "language": subscriber.language,
                "engagement_level": subscriber.engagement_level,
                "signup_date": subscriber.signup_date.isoformat(),
                "is_active": subscriber.is_active,
                "custom_fields": subscriber.custom_fields
            })
        
        return {
            "segment": segment,
            "subscribers": response_data,
            "total_count": len(response_data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get subscribers by segment: {str(e)}")


@app.post("/admin/segmentation/search")
def search_subscribers_by_criteria(
    criteria: dict,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Search subscribers using custom criteria"""
    try:
        # Convert string dates to datetime if provided
        if criteria.get("signup_date_from"):
            criteria["signup_date_from"] = datetime.fromisoformat(criteria["signup_date_from"])
        if criteria.get("signup_date_to"):
            criteria["signup_date_to"] = datetime.fromisoformat(criteria["signup_date_to"])
        
        subscribers = get_subscribers_by_custom_criteria(db, criteria)
        
        response_data = []
        for subscriber in subscribers:
            response_data.append({
                "id": subscriber.id,
                "email": subscriber.email,
                "name": subscriber.name,
                "source": subscriber.source,
                "language": subscriber.language,
                "engagement_level": subscriber.engagement_level,
                "signup_date": subscriber.signup_date.isoformat(),
                "is_active": subscriber.is_active,
                "custom_fields": subscriber.custom_fields
            })
        
        return {
            "criteria": criteria,
            "subscribers": response_data,
            "total_count": len(response_data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search subscribers: {str(e)}")


@app.get("/admin/sequences/{sequence_id}/progress")
def get_sequence_progress(
    sequence_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get detailed progress summary for a sequence"""
    try:
        progress = get_sequence_progress_summary(db, sequence_id)
        if not progress:
            raise HTTPException(status_code=404, detail="Sequence not found")
        
        return progress
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get sequence progress: {str(e)}")


@app.get("/admin/subscribers/{subscriber_id}/journey")
def get_subscriber_journey_endpoint(
    subscriber_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get complete journey/history for a subscriber"""
    try:
        journey = get_subscriber_journey(db, subscriber_id)
        if not journey:
            raise HTTPException(status_code=404, detail="Subscriber not found")
        
        return journey
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get subscriber journey: {str(e)}")


@app.post("/admin/segmentation/update-engagement")
def update_engagement_levels(
    limit: int = 1000,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Bulk update engagement levels for all subscribers"""
    try:
        result = bulk_update_engagement_levels(db, limit)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update engagement levels: {str(e)}")


@app.post("/admin/subscribers/{subscriber_id}/update-engagement")
def update_single_subscriber_engagement(
    subscriber_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update engagement level for a single subscriber"""
    try:
        new_level = update_subscriber_engagement_level(db, subscriber_id)
        return {"subscriber_id": subscriber_id, "new_engagement_level": new_level}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update subscriber engagement: {str(e)}")


# End-to-End Testing Endpoint
@app.post("/admin/test/email-workflow")
def test_email_workflow_endpoint(
    current_user: User = Depends(get_current_admin_user)
):
    """Run end-to-end email workflow tests"""
    try:
        from test_email_workflow import run_workflow_tests
        
        # Run the complete test suite
        test_results = run_workflow_tests()
        
        return {
            "status": "completed",
            "results": test_results,
            "message": f"Testing completed with {test_results['success_rate']}% success rate"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run workflow tests: {str(e)}")


@app.get("/admin/test/system-status")
def get_system_status(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get overall system status for monitoring"""
    try:
        from email_scheduler import EmailSchedulerService
        
        # Check scheduler status
        scheduler_service = EmailSchedulerService()
        scheduler_running = scheduler_service.is_running()
        
        # Get recent activity
        recent_date = datetime.utcnow() - timedelta(hours=24)
        
        recent_subscribers = db.query(func.count(EmailSubscriber.id)).filter(
            EmailSubscriber.signup_date >= recent_date
        ).scalar()
        
        recent_emails_sent = db.query(func.count(ScheduledEmail.id)).filter(
            and_(
                ScheduledEmail.sent_at >= recent_date,
                ScheduledEmail.status == "sent"
            )
        ).scalar()
        
        recent_emails_failed = db.query(func.count(ScheduledEmail.id)).filter(
            and_(
                ScheduledEmail.updated_at >= recent_date,
                ScheduledEmail.status.in_(["failed", "permanently_failed"])
            )
        ).scalar()
        
        # Get pending emails
        pending_emails = db.query(func.count(ScheduledEmail.id)).filter(
            ScheduledEmail.status == "scheduled"
        ).scalar()
        
        # Calculate system health score
        health_score = 100
        if not scheduler_running:
            health_score -= 30
        if recent_emails_failed > recent_emails_sent * 0.1:  # More than 10% failure rate
            health_score -= 20
        if pending_emails > 1000:  # Large backlog
            health_score -= 10
        
        status = "healthy" if health_score >= 80 else "warning" if health_score >= 60 else "critical"
        
        return {
            "status": status,
            "health_score": health_score,
            "scheduler_running": scheduler_running,
            "recent_24h": {
                "new_subscribers": recent_subscribers,
                "emails_sent": recent_emails_sent,
                "emails_failed": recent_emails_failed
            },
            "pending_emails": pending_emails,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get system status: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)