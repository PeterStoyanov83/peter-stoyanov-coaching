from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
import os
import shutil
from typing import List, Optional, Dict, Any
import markdown
import glob
from datetime import datetime, timedelta
from sqlalchemy import func, desc
import uuid

from models import WaitlistRegistration, CorporateInquiry, LeadMagnetDownload, BlogPost, BlogPostRequest, BlogPostResponse, BlogPostListResponse
from database import (get_db, store_waitlist_registration, store_corporate_inquiry, store_lead_magnet_download,
                     create_blog_post, get_blog_posts, get_blog_post_by_id, get_blog_post_by_slug, 
                     update_blog_post, delete_blog_post, search_blog_posts)
from mailerlite import add_subscriber_to_mailerlite, add_lead_magnet_subscriber, add_waitlist_subscriber
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
    
    # Try to add to MailerLite first
    mailer_success = False
    if os.getenv("MAILERLITE_API_KEY"):
        try:
            background_tasks.add_task(
                add_waitlist_subscriber,
                registration.email,
                registration.full_name,
                registration.skills_to_improve
            )
            mailer_success = True
        except Exception as e:
            print(f"MailerLite error: {e}")
            # Continue to SQLite fallback
    
    # Store in SQLite as fallback or if MailerLite failed
    if not mailer_success or not os.getenv("MAILERLITE_API_KEY"):
        store_waitlist_registration(db, reg_model)
    
    return {"status": "success", "message": "Registration successful"}

@app.post("/api/corporate-inquiry")
async def corporate_inquiry(
    inquiry: CorporateInquiryRequest,
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
    - Add to MailerLite if configured
    - Return download URL
    """
    
    # Store in database (tracks download count for returning users)
    download_record = store_lead_magnet_download(db, request.email)
    
    # Try to add to MailerLite for email marketing
    mailer_success = False
    if os.getenv("MAILERLITE_API_KEY"):
        try:
            # Add to MailerLite in background task using automation function
            background_tasks.add_task(
                add_lead_magnet_subscriber,
                request.email,
                ""  # Name not provided in lead magnet form
            )
            mailer_success = True
        except Exception as e:
            print(f"MailerLite error for lead magnet: {e}")
            # Continue anyway - email is stored in database
    
    # Return success response with download URL
    return {
        "success": True,
        "message": "Thank you! Your guide is ready for download.",
        "downloadUrl": "/guides/5-theater-secrets-guide.pdf",
        "isReturningUser": download_record.download_count > 1
    }

@app.get("/api/posts", response_model=List[BlogPostListResponse])
def api_get_blog_posts(published_only: bool = True, skip: int = 0, limit: int = 100, db = Depends(get_db)):
    """Get published blog posts for public consumption"""
    posts = get_blog_posts(db, skip=skip, limit=limit, published_only=published_only)
    return posts

@app.get("/api/posts/{slug}", response_model=BlogPostResponse)
def get_blog_post(slug: str, db = Depends(get_db)):
    """Get a specific blog post by slug"""
    post = get_blog_post_by_slug(db, slug, published_only=True)
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return post

# Authentication Endpoints
@app.post("/auth/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint for admin access"""
    user = authenticate_user(form_data.username, form_data.password)
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
@app.get("/admin/blog/posts", response_model=List[BlogPostListResponse])
def admin_get_blog_posts(skip: int = 0, limit: int = 100, published_only: Optional[bool] = None, 
                        db = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """Get all blog posts for admin management"""
    posts = get_blog_posts(db, skip=skip, limit=limit, published_only=published_only if published_only is not None else False)
    return posts

@app.get("/admin/blog/posts/{post_id}", response_model=BlogPostResponse)
def admin_get_blog_post(post_id: int, db = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """Get a specific blog post for editing"""
    post = get_blog_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return post

@app.post("/admin/blog/posts", response_model=BlogPostResponse)
def admin_create_blog_post(post: BlogPostRequest, db = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """Create a new blog post"""
    try:
        post_data = post.dict()
        blog_post = create_blog_post(db, post_data)
        return blog_post
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(status_code=400, detail="A blog post with this slug already exists")
        raise HTTPException(status_code=400, detail="Failed to create blog post")

@app.put("/admin/blog/posts/{post_id}", response_model=BlogPostResponse)
def admin_update_blog_post(post_id: int, post: BlogPostRequest, 
                          db = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """Update an existing blog post"""
    post_data = post.dict()
    updated_post = update_blog_post(db, post_id, post_data)
    if not updated_post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return updated_post

@app.delete("/admin/blog/posts/{post_id}")
def admin_delete_blog_post(post_id: int, db = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """Delete a blog post"""
    if not delete_blog_post(db, post_id):
        raise HTTPException(status_code=404, detail="Blog post not found")
    return {"message": "Blog post deleted successfully"}

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

@app.get("/admin/dashboard", response_class=HTMLResponse)
def admin_dashboard():
    """Admin dashboard with authentication"""
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Coaching Site Admin Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { background: #2563eb; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }
            .login-section { background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 400px; margin: 100px auto; }
            .login-form { display: flex; flex-direction: column; gap: 15px; }
            .form-group { display: flex; flex-direction: column; }
            .form-group label { margin-bottom: 5px; font-weight: bold; }
            .form-group input { padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
            .login-btn { background: #2563eb; color: white; padding: 12px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
            .login-btn:hover { background: #1d4ed8; }
            .logout-btn { background: #dc2626; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; }
            .logout-btn:hover { background: #b91c1c; }
            .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
            .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .stat-number { font-size: 2em; font-weight: bold; color: #2563eb; }
            .stat-label { color: #666; margin-top: 5px; }
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
            .form-group { margin-bottom: 15px; }
            .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
            .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
            .form-group textarea { height: 300px; }
            .form-actions { display: flex; gap: 10px; justify-content: flex-end; margin-top: 20px; }
            .btn-save { background: #2563eb; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
            .btn-cancel { background: #6b7280; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
            .status-badge { padding: 2px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }
            .status-published { background: #10b981; color: white; }
            .status-draft { background: #f59e0b; color: white; }
        </style>
    </head>
    <body>
        <!-- Login Section -->
        <div id="login-section" class="login-section">
            <h2>🎭 Admin Login</h2>
            <form class="login-form" onsubmit="login(event)">
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
        <div id="dashboard-section" class="container hidden">
            <div class="header">
                <div>
                    <h1>🎭 Coaching Site Admin Dashboard</h1>
                    <p>Real-time statistics and activity monitoring</p>
                </div>
                <div>
                    <span>Welcome, <span id="username-display"></span>!</span>
                    <button class="logout-btn" onclick="logout()">Logout</button>
                </div>
            </div>
            
            <div class="nav-tabs">
                <button class="nav-tab active" onclick="showTab('dashboard')">Dashboard</button>
                <button class="nav-tab" onclick="showTab('blog')">Blog Management</button>
            </div>
            
            <!-- Dashboard Tab -->
            <div id="dashboard-tab" class="tab-content">
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
            
            <div class="activity-section">
                <h2>Recent Activity <button class="refresh-btn" onclick="loadData()">Refresh</button></h2>
                <div id="recent-activity">Loading...</div>
            </div>
            </div>
            
            <!-- Blog Management Tab -->
            <div id="blog-tab" class="tab-content hidden">
                <div id="blog-list-view">
                    <button class="btn-new" onclick="showBlogEditor()">New Blog Post</button>
                    <div id="blog-posts-container">
                        <div class="blog-list" id="blog-list">
                            <!-- Blog posts will be loaded here -->
                        </div>
                    </div>
                </div>
                
                <div id="blog-editor-view" class="hidden">
                    <h3 id="editor-title">Create New Blog Post</h3>
                    <form id="blog-form">
                        <div class="form-group">
                            <label for="blog-slug">Slug (URL)</label>
                            <input type="text" id="blog-slug" name="slug" required placeholder="e.g., mastering-public-speaking">
                        </div>
                        
                        <h4>English Version</h4>
                        
                        <div class="form-group">
                            <label for="blog-title-en">Title (English)</label>
                            <input type="text" id="blog-title-en" name="title_en" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="blog-excerpt-en">Excerpt (English)</label>
                            <textarea id="blog-excerpt-en" name="excerpt_en" rows="3" placeholder="Brief description in English"></textarea>
                        </div>
                        
                        <div class="form-group">
                            <label for="blog-content-en">Content (English)</label>
                            <textarea id="blog-content-en" name="content_en" placeholder="Write your blog post content in English..."></textarea>
                        </div>
                        
                        <div class="form-group">
                            <label for="blog-tags-en">Tags (English, comma-separated)</label>
                            <input type="text" id="blog-tags-en" name="tags_en" placeholder="communication, public speaking, theater">
                        </div>
                        
                        <h4>Bulgarian Version</h4>
                        
                        <div class="form-group">
                            <label for="blog-title-bg">Title (Bulgarian)</label>
                            <input type="text" id="blog-title-bg" name="title_bg">
                        </div>
                        
                        <div class="form-group">
                            <label for="blog-excerpt-bg">Excerpt (Bulgarian)</label>
                            <textarea id="blog-excerpt-bg" name="excerpt_bg" rows="3" placeholder="Кратко описание на български"></textarea>
                        </div>
                        
                        <div class="form-group">
                            <label for="blog-content-bg">Content (Bulgarian)</label>
                            <textarea id="blog-content-bg" name="content_bg" placeholder="Напишете съдържанието на блог поста на български..."></textarea>
                        </div>
                        
                        <div class="form-group">
                            <label for="blog-tags-bg">Tags (Bulgarian, comma-separated)</label>
                            <input type="text" id="blog-tags-bg" name="tags_bg" placeholder="комуникация, публично говорене, театър">
                        </div>
                        
                        <div class="form-group">
                            <label for="blog-featured-image">Featured Image URL</label>
                            <input type="text" id="blog-featured-image" name="featured_image" placeholder="Upload or enter image URL">
                            <button type="button" onclick="uploadImage()" style="margin-top: 5px;">Upload Image</button>
                            <input type="file" id="image-upload" accept="image/*" style="display: none;" onchange="handleImageUpload(event)">
                        </div>
                        
                        
                        <div class="form-group">
                            <label for="blog-published">
                                <input type="checkbox" id="blog-published" name="is_published"> Published
                            </label>
                        </div>
                        
                        <div class="form-actions">
                            <button type="button" class="btn-cancel" onclick="closeBlogEditor()">Cancel</button>
                            <button type="submit" class="btn-save">Save Post</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        
        <script>
            let authToken = localStorage.getItem('adminToken');
            
            // Check if already logged in
            if (authToken) {
                checkAuth();
            }
            
            async function login(event) {
                event.preventDefault();
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;
                
                console.log('Attempting login with:', username);
                
                try {
                    const formData = new FormData();
                    formData.append('username', username);
                    formData.append('password', password);
                    
                    console.log('Sending login request...');
                    const response = await fetch('/auth/login', {
                        method: 'POST',
                        body: formData
                    });
                    
                    console.log('Response status:', response.status);
                    
                    if (response.ok) {
                        const data = await response.json();
                        console.log('Login successful, token received');
                        authToken = data.access_token;
                        localStorage.setItem('adminToken', authToken);
                        showDashboard(username);
                        hideError();
                    } else {
                        const errorData = await response.text();
                        console.log('Login failed:', errorData);
                        showError('Invalid username or password');
                    }
                } catch (error) {
                    console.error('Login error:', error);
                    showError('Login failed: ' + error.message);
                }
            }
            
            async function checkAuth() {
                try {
                    const response = await fetch('/auth/me', {
                        headers: {
                            'Authorization': `Bearer ${authToken}`
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
                        'Authorization': `Bearer ${authToken}`
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
                        
                        div.innerHTML = `
                            <span class="activity-type ${typeClass}">${item.type.replace('_', ' ').toUpperCase()}</span>
                            <strong>${item.email}</strong> ${item.name ? '(' + item.name + ')' : ''}
                            ${item.company ? '- ' + item.company : ''}
                            <div style="color: #666; font-size: 0.9em;">${item.details} - ${date}</div>
                        `;
                        
                        activityDiv.appendChild(div);
                    });
                    
                } catch (error) {
                    console.error('Error loading data:', error);
                }
            }
            
            // Blog Management Functions
            let currentEditingPost = null;
            
            function showTab(tabName) {
                // Update tab buttons
                document.querySelectorAll('.nav-tab').forEach(tab => tab.classList.remove('active'));
                event.target.classList.add('active');
                
                // Show/hide tab content
                document.querySelectorAll('.tab-content').forEach(content => content.classList.add('hidden'));
                document.getElementById(tabName + '-tab').classList.remove('hidden');
                
                // Load data for the specific tab
                if (tabName === 'blog') {
                    loadBlogPosts();
                } else if (tabName === 'dashboard') {
                    loadData();
                }
            }
            
            async function loadBlogPosts() {
                if (!authToken) return;
                
                try {
                    const response = await fetch('/admin/blog/posts', {
                        headers: { 'Authorization': `Bearer ${authToken}` }
                    });
                    
                    if (!response.ok) throw new Error('Failed to load blog posts');
                    
                    const posts = await response.json();
                    const blogList = document.getElementById('blog-list');
                    
                    blogList.innerHTML = '';
                    
                    if (posts.length === 0) {
                        blogList.innerHTML = '<p>No blog posts found. Create your first post!</p>';
                        return;
                    }
                    
                    posts.forEach(post => {
                        const postDiv = document.createElement('div');
                        postDiv.className = 'blog-item';
                        
                        const statusClass = post.is_published ? 'status-published' : 'status-draft';
                        const statusText = post.is_published ? 'Published' : 'Draft';
                        const publishedDate = post.published_at ? new Date(post.published_at).toLocaleDateString() : 'Not published';
                        const hasEnglish = post.title.en ? '🇺🇸' : '';
                        const hasBulgarian = post.title.bg ? '🇧🇬' : '';
                        const languages = [hasEnglish, hasBulgarian].filter(Boolean).join(' ');
                        
                        postDiv.innerHTML = `
                            <div class="blog-info">
                                <div class="blog-title">${languages} ${post.title.en || post.title.bg || 'Untitled'}</div>
                                <div class="blog-meta">
                                    <span class="status-badge ${statusClass}">${statusText}</span>
                                    Created: ${new Date(post.created_at).toLocaleDateString()}
                                    ${post.is_published ? `| Published: ${publishedDate}` : ''}
                                </div>
                            </div>
                            <div class="blog-actions">
                                <button class="btn-edit" onclick="editBlogPost(${post.id})">Edit</button>
                                <button class="btn-delete" onclick="deleteBlogPost(${post.id}, '${post.title.en || post.title.bg || 'Untitled'}')">Delete</button>
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
                document.getElementById('blog-list-view').classList.add('hidden');
                document.getElementById('blog-editor-view').classList.remove('hidden');
                
                if (postData) {
                    // Editing existing post
                    document.getElementById('editor-title').textContent = 'Edit Blog Post';
                    document.getElementById('blog-slug').value = postData.slug;
                    
                    // English fields
                    document.getElementById('blog-title-en').value = postData.title.en || '';
                    document.getElementById('blog-excerpt-en').value = postData.excerpt.en || '';
                    document.getElementById('blog-content-en').value = postData.content.en || '';
                    document.getElementById('blog-tags-en').value = postData.tags.en ? postData.tags.en.join(', ') : '';
                    
                    // Bulgarian fields
                    document.getElementById('blog-title-bg').value = postData.title.bg || '';
                    document.getElementById('blog-excerpt-bg').value = postData.excerpt.bg || '';
                    document.getElementById('blog-content-bg').value = postData.content.bg || '';
                    document.getElementById('blog-tags-bg').value = postData.tags.bg ? postData.tags.bg.join(', ') : '';
                    
                    document.getElementById('blog-featured-image').value = postData.featured_image || '';
                    document.getElementById('blog-published').checked = postData.is_published;
                    currentEditingPost = postData.id;
                } else {
                    // Creating new post
                    document.getElementById('editor-title').textContent = 'Create New Blog Post';
                    document.getElementById('blog-form').reset();
                    currentEditingPost = null;
                }
            }
            
            function closeBlogEditor() {
                document.getElementById('blog-editor-view').classList.add('hidden');
                document.getElementById('blog-list-view').classList.remove('hidden');
                document.getElementById('blog-form').reset();
                currentEditingPost = null;
            }
            
            async function editBlogPost(postId) {
                try {
                    const response = await fetch(`/admin/blog/posts/${postId}`, {
                        headers: { 'Authorization': `Bearer ${authToken}` }
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
                    const response = await fetch(`/admin/blog/posts/${postId}`, {
                        method: 'DELETE',
                        headers: { 'Authorization': `Bearer ${authToken}` }
                    });
                    
                    if (!response.ok) throw new Error('Failed to delete blog post');
                    
                    loadBlogPosts(); // Reload the list
                    
                } catch (error) {
                    console.error('Error deleting blog post:', error);
                    alert('Error deleting blog post');
                }
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
                        headers: { 'Authorization': `Bearer ${authToken}` },
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
            
            // Handle blog form submission
            document.getElementById('blog-form').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const formData = new FormData(e.target);
                const postData = {
                    slug: formData.get('slug'),
                    title: {
                        en: formData.get('title_en') || '',
                        bg: formData.get('title_bg') || ''
                    },
                    excerpt: {
                        en: formData.get('excerpt_en') || '',
                        bg: formData.get('excerpt_bg') || ''
                    },
                    content: {
                        en: formData.get('content_en') || '',
                        bg: formData.get('content_bg') || ''
                    },
                    featured_image: formData.get('featured_image') || null,
                    tags: {
                        en: formData.get('tags_en') ? formData.get('tags_en').split(',').map(tag => tag.trim()) : [],
                        bg: formData.get('tags_bg') ? formData.get('tags_bg').split(',').map(tag => tag.trim()) : []
                    },
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
                            'Authorization': `Bearer ${authToken}`,
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
            
            // Auto-generate slug from English title
            document.getElementById('blog-title-en').addEventListener('input', function(e) {
                const title = e.target.value;
                const slug = title
                    .toLowerCase()
                    .replace(/[^a-z0-9\s-]/g, '')
                    .replace(/\s+/g, '-')
                    .replace(/-+/g, '-')
                    .trim('-');
                document.getElementById('blog-slug').value = slug;
            });
        </script>
    </body>
    </html>
    """
    
    return html_content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)