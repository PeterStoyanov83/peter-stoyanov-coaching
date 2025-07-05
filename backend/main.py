from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
import os
from typing import List, Optional, Dict, Any
import markdown
import glob
from datetime import datetime, timedelta
from sqlalchemy import func, desc

from models import WaitlistRegistration, CorporateInquiry, LeadMagnetDownload
from database import get_db, store_waitlist_registration, store_corporate_inquiry, store_lead_magnet_download
from mailerlite import add_subscriber_to_mailerlite, add_lead_magnet_subscriber, add_waitlist_subscriber
from auth import authenticate_user, create_access_token, get_current_admin_user, Token, User, ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI(title="Coaching Site API", description="API for Petar Stoyanov's coaching website")

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
    company_name: str
    contact_person: str
    email: EmailStr
    message: str

class LeadMagnetRequest(BaseModel):
    email: EmailStr

class BlogPost(BaseModel):
    slug: str
    title: str
    content: str
    excerpt: str
    date: str
    tags: List[str] = []

@app.get("/")
def read_root():
    return {"message": "Welcome to Petar Stoyanov's Coaching API"}

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

@app.post("/api/contact-corporate")
async def contact_corporate(
    inquiry: CorporateInquiryRequest,
    db = Depends(get_db)
):
    # Create model instance
    inq_model = CorporateInquiry(
        company_name=inquiry.company_name,
        contact_person=inquiry.contact_person,
        email=inquiry.email,
        message=inquiry.message
    )
    
    # Store in database
    store_corporate_inquiry(db, inq_model)
    
    return {"status": "success", "message": "Inquiry submitted successfully"}

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

@app.get("/api/posts", response_model=List[BlogPost])
def get_blog_posts(tag: Optional[str] = None):
    posts = []
    
    # Get all markdown files from the blog directory
    blog_files = glob.glob("../blog/*.md")
    
    for file_path in blog_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Extract metadata and content
        # This is a simple implementation - in a real app, you might want to use frontmatter
        lines = content.split("\n")
        title = lines[0].replace("# ", "")
        date = ""
        tags_list = []
        
        # Look for metadata in the first few lines
        for i, line in enumerate(lines[1:5]):
            if line.startswith("Date: "):
                date = line.replace("Date: ", "")
            elif line.startswith("Tags: "):
                tags_text = line.replace("Tags: ", "")
                tags_list = [tag.strip() for tag in tags_text.split(",")]
        
        # Generate excerpt from first paragraph
        excerpt = ""
        for line in lines:
            if line and not line.startswith("#") and not line.startswith("Date:") and not line.startswith("Tags:"):
                excerpt = line[:150] + "..." if len(line) > 150 else line
                break
        
        # Convert markdown to HTML
        html_content = markdown.markdown(content)
        
        # Get slug from filename
        slug = os.path.basename(file_path).replace(".md", "")
        
        # Filter by tag if specified
        if tag and tag not in tags_list:
            continue
            
        posts.append(BlogPost(
            slug=slug,
            title=title,
            content=html_content,
            excerpt=excerpt,
            date=date,
            tags=tags_list
        ))
    
    # Sort by date (newest first)
    posts.sort(key=lambda x: x.date, reverse=True)
    
    return posts

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
        </script>
    </body>
    </html>
    """
    
    return html_content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)