from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
import logging
from datetime import datetime

from models import (
    WaitlistRegistration, CorporateInquiry, LeadMagnetDownload, EmailLog,
    WaitlistRegistrationRequest, CorporateInquiryRequest, LeadMagnetRequest,
    WaitlistRegistrationResponse, CorporateInquiryResponse, LeadMagnetResponse
)
from database import get_db
from email_service import sendgrid_service
from admin_routes import router as admin_router

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Peter Stoyanov Coaching API", description="Clean API for coaching website")

# Include admin routes
app.include_router(admin_router)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://peter-stoyanov.com",
        "https://www.peter-stoyanov.com", 
        "https://peter-stoyanov-coaching.onrender.com",
        "http://localhost:3000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Peter Stoyanov Coaching API", "status": "clean"}

# Admin web interface routes
@app.get("/admin", response_class=HTMLResponse)
async def admin_redirect():
    """Redirect /admin to /admin/login"""
    return HTMLResponse(content="""
        <script>
            window.location.href = '/admin/login';
        </script>
    """)

@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page():
    """Serve the admin login page"""
    try:
        with open("templates/login.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Login page not found</h1>", status_code=404)

@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard_page():
    """Serve the admin dashboard page"""
    try:
        with open("templates/dashboard.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Dashboard page not found</h1>", status_code=404)

# Form submission endpoints
@app.post("/api/register", response_model=dict)
async def register_waitlist(
    registration: WaitlistRegistrationRequest, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Handle waitlist registration with email automation"""
    try:
        # Store in database
        db_registration = WaitlistRegistration(
            full_name=registration.full_name,
            email=registration.email,
            city_country=registration.city_country,
            occupation=registration.occupation,
            why_join=registration.why_join,
            skills_to_improve=registration.skills_to_improve
        )
        db.add(db_registration)
        db.commit()
        db.refresh(db_registration)
        
        # Send welcome email
        registration_data = {
            "full_name": registration.full_name,
            "email": registration.email,
            "city_country": registration.city_country,
            "occupation": registration.occupation,
            "why_join": registration.why_join,
            "skills_to_improve": registration.skills_to_improve
        }
        
        email_result = sendgrid_service.send_welcome_email_waitlist(registration_data)
        
        if email_result["success"]:
            db_registration.welcome_sent = True
            db_registration.welcome_sent_at = datetime.utcnow()
            # Start email sequence after successful welcome email
            db_registration.sequence_started = True
            db_registration.last_email_sent_at = datetime.utcnow()
            db.commit()
            
            # Log email
            email_log = EmailLog(
                waitlist_id=db_registration.id,
                email_type="welcome",
                subject=f"Welcome to Peter Stoyanov Coaching, {registration.full_name}!",
                recipient_email=registration.email,
                sendgrid_message_id=email_result.get("message_id")
            )
            db.add(email_log)
            db.commit()
        
        # Send admin notification
        background_tasks.add_task(
            sendgrid_service.send_admin_notification, 
            "waitlist", 
            registration.email
        )
        
        logger.info(f"Waitlist registration successful: {registration.email}")
        
        return {
            "success": True,
            "message": "Registration successful! Check your email for welcome message.",
            "email": registration.email
        }
        
    except Exception as e:
        logger.error(f"Error processing waitlist registration: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Registration failed")

@app.post("/api/corporate-inquiry", response_model=dict)
async def submit_corporate_inquiry(
    inquiry: CorporateInquiryRequest, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Handle corporate inquiry with email automation"""
    try:
        # Store in database
        db_inquiry = CorporateInquiry(
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
        db.add(db_inquiry)
        db.commit()
        db.refresh(db_inquiry)
        
        # Send welcome email
        inquiry_data = {
            "company_name": inquiry.companyName,
            "contact_person": inquiry.contactPerson,
            "email": inquiry.email,
            "phone": inquiry.phone,
            "team_size": inquiry.teamSize,
            "budget": inquiry.budget,
            "training_goals": inquiry.trainingGoals,
            "preferred_dates": inquiry.preferredDates,
            "additional_info": inquiry.additionalInfo
        }
        
        email_result = sendgrid_service.send_welcome_email_corporate(inquiry_data)
        
        if email_result["success"]:
            db_inquiry.welcome_sent = True
            db_inquiry.welcome_sent_at = datetime.utcnow()
            # Start email sequence after successful welcome email
            db_inquiry.sequence_started = True
            db_inquiry.last_email_sent_at = datetime.utcnow()
            db.commit()
            
            # Log email
            email_log = EmailLog(
                corporate_id=db_inquiry.id,
                email_type="welcome",
                subject=f"Thank you for your corporate training inquiry, {inquiry.contactPerson}!",
                recipient_email=inquiry.email,
                sendgrid_message_id=email_result.get("message_id")
            )
            db.add(email_log)
            db.commit()
        
        # Send admin notification
        background_tasks.add_task(
            sendgrid_service.send_admin_notification, 
            "corporate", 
            inquiry.email
        )
        
        logger.info(f"Corporate inquiry successful: {inquiry.email} from {inquiry.companyName}")
        
        return {
            "success": True,
            "message": "Corporate inquiry received! We'll get back to you within 24 hours.",
            "email": inquiry.email,
            "company": inquiry.companyName
        }
        
    except Exception as e:
        logger.error(f"Error processing corporate inquiry: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Inquiry submission failed")

@app.post("/api/download-guide", response_model=dict)
async def download_guide(
    request: LeadMagnetRequest, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Handle lead magnet download with email automation"""
    try:
        # Store/update in database
        existing = db.query(LeadMagnetDownload).filter(LeadMagnetDownload.email == request.email).first()
        
        if existing:
            existing.download_count += 1
            existing.last_downloaded_at = datetime.utcnow()
            db.commit()
            db_download = existing
        else:
            db_download = LeadMagnetDownload(email=request.email)
            db.add(db_download)
            db.commit()
            db.refresh(db_download)
        
        # Send welcome email (only for new subscribers)
        if not existing or not existing.welcome_sent:
            email_result = sendgrid_service.send_welcome_email_lead_magnet(request.email)
            
            if email_result["success"]:
                db_download.welcome_sent = True
                db_download.welcome_sent_at = datetime.utcnow()
                # Start email sequence after successful welcome email
                db_download.sequence_started = True
                db_download.last_email_sent_at = datetime.utcnow()
                db.commit()
                
                # Log email
                email_log = EmailLog(
                    lead_magnet_id=db_download.id,
                    email_type="welcome",
                    subject="Your Leadership Guide is Ready + Welcome to the Community!",
                    recipient_email=request.email,
                    sendgrid_message_id=email_result.get("message_id")
                )
                db.add(email_log)
                db.commit()
                
                # Send admin notification for new subscribers only
                background_tasks.add_task(
                    sendgrid_service.send_admin_notification, 
                    "lead magnet", 
                    request.email
                )
        
        logger.info(f"Lead magnet download: {request.email}")
        
        return {
            "success": True,
            "message": "Download link sent! Check your email for the leadership guide.",
            "email": request.email
        }
        
    except Exception as e:
        logger.error(f"Error processing lead magnet download: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Download request failed")

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "clean", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
