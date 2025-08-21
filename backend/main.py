from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
from sqlalchemy.orm import Session
from typing import List
import logging
from datetime import datetime

from models import (
    WaitlistRegistration, CorporateInquiry, LeadMagnetDownload, EmailLog,
    WaitlistRegistrationRequest, CorporateInquiryRequest, LeadMagnetRequest,
    WaitlistRegistrationResponse, CorporateInquiryResponse, LeadMagnetResponse
)
from database_supabase import get_db
from email_service import sendgrid_service
from admin_routes import router as admin_router

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Peter Stoyanov Coaching API", description="Clean API for coaching website")

# Include admin routes
app.include_router(admin_router)

# Serve static files (frontend) if available
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    try:
        from models import Base
        from database_supabase import engine
        
        # Create all tables if they don't exist
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        # Don't fail startup, just log the error

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://peter-stoyanov.com",
        "https://www.peter-stoyanov.com", 
        "https://peter-stoyanov-coaching.onrender.com",
        "https://*.railway.app",
        "https://*.fly.dev",
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
        
        # Send welcome email with lead magnet
        registration_data = {
            "full_name": registration.full_name,
            "email": registration.email,
            "city_country": registration.city_country,
            "occupation": registration.occupation,
            "why_join": registration.why_join,
            "skills_to_improve": registration.skills_to_improve
        }
        
        email_result = sendgrid_service.send_welcome_email_waitlist(registration_data)
        
        # Also create lead magnet entry for guide access
        lead_magnet_entry = LeadMagnetDownload(email=registration.email)
        db.add(lead_magnet_entry)
        db.commit()
        
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
        
        # Check if it's a duplicate email error
        if "duplicate key" in str(e) or "UNIQUE constraint failed" in str(e):
            raise HTTPException(status_code=409, detail="This email is already registered. Please use a different email.")
        else:
            raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

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
            "training_goals": inquiry.trainingGoals,
            "preferred_dates": inquiry.preferredDates,
            "additional_info": inquiry.additionalInfo
        }
        
        email_result = sendgrid_service.send_welcome_email_corporate(inquiry_data)
        
        if email_result["success"]:
            db_inquiry.welcome_sent = True
            db_inquiry.welcome_sent_at = datetime.utcnow()
            # Note: Corporate inquiries are handled manually, no automated sequence
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
        
        # Provide direct download URL for immediate download
        download_url = "https://peter-stoyanov.com/guides/exersises-for-breathing-voice-and-speaking.pdf"
        
        return {
            "success": True,
            "message": "Download link sent! Check your email for the leadership guide.",
            "email": request.email,
            "downloadUrl": download_url
        }
        
    except Exception as e:
        logger.error(f"Error processing lead magnet download: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Download request failed")

# Database migration endpoint  
@app.post("/admin/migrate-database")
async def migrate_database():
    """Migrate database to new schema - drops and recreates tables"""
    try:
        from sqlalchemy import text
        from models import Base
        from database_supabase import engine
        
        with engine.connect() as conn:
            # Drop existing tables
            drop_commands = [
                "DROP TABLE IF EXISTS email_logs CASCADE",
                "DROP TABLE IF EXISTS sequence_emails CASCADE", 
                "DROP TABLE IF EXISTS email_sequences CASCADE",
                "DROP TABLE IF EXISTS lead_magnet_downloads CASCADE",
                "DROP TABLE IF EXISTS corporate_inquiries CASCADE",
                "DROP TABLE IF EXISTS waitlist_registrations CASCADE"
            ]
            
            for cmd in drop_commands:
                try:
                    conn.execute(text(cmd))
                except Exception:
                    pass  # Ignore errors if table doesn't exist
            
            conn.commit()
        
        # Create all new tables
        Base.metadata.create_all(bind=engine)
        
        # Test the new structure
        from database_supabase import SessionLocal
        from models import WaitlistRegistration
        
        db = SessionLocal()
        count = db.query(WaitlistRegistration).count()
        db.close()
        
        return {
            "success": True,
            "message": "Database migrated successfully",
            "waitlist_count": count
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Database migration failed"
        }

# Database initialization endpoint
@app.post("/admin/init-database")
async def init_database():
    """Initialize database tables - run this once after deployment"""
    try:
        from models import Base
        from database_supabase import engine
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Test connection
        from database_supabase import SessionLocal
        db = SessionLocal()
        
        # Check if tables exist by trying a simple query
        from models import WaitlistRegistration
        count = db.query(WaitlistRegistration).count()
        db.close()
        
        return {
            "success": True,
            "message": "Database initialized successfully",
            "waitlist_count": count
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Database initialization failed"
        }

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "clean", "timestamp": datetime.utcnow().isoformat()}

# Test endpoints for production verification
@app.post("/admin/test-email-flow")
async def test_email_flow(db: Session = Depends(get_db)):
    """Test the complete email automation flow"""
    test_email = "test@peter-stoyanov.com"
    
    try:
        # 1. Test database connection
        test_count = db.query(WaitlistRegistration).count()
        
        # 2. Test email service
        test_result = sendgrid_service.send_email(
            to_email=test_email,
            subject="Email Flow Test",
            html_content="<p>This is a test email from your automation system.</p>"
        )
        
        # 3. Test sequence email generation
        from email_automation import EmailSequenceAutomation
        automation = EmailSequenceAutomation()
        test_sequence = automation._get_waitlist_magnet_email(1)
        
        return {
            "success": True,
            "database_connection": "OK",
            "waitlist_count": test_count,
            "email_service": "OK" if test_result.get("success") else f"ERROR: {test_result.get('error')}",
            "sequence_generation": "OK" if test_sequence else "ERROR: No sequence content",
            "test_email_sent": test_result.get("success", False),
            "message_id": test_result.get("message_id")
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Email flow test failed"
        }

@app.post("/admin/test-sequence-email")
async def test_sequence_email(email: str, sequence_index: int = 1, db: Session = Depends(get_db)):
    """Send a test sequence email to verify content and formatting"""
    try:
        from email_automation import EmailSequenceAutomation
        automation = EmailSequenceAutomation()
        
        # Get sequence email content
        sequence_email = automation._get_waitlist_magnet_email(sequence_index)
        if not sequence_email:
            return {"success": False, "error": f"No sequence email found for index {sequence_index}"}
        
        # Personalize with test data
        test_data = {
            "full_name": "Test User",
            "email": email,
            "occupation": "Test Occupation",
            "city_country": "Test City, Test Country"
        }
        
        personalized_content = automation._personalize_email_content(sequence_email['content'], test_data)
        
        # Send test email
        result = sendgrid_service.send_email(
            to_email=email,
            subject=f"[TEST] {sequence_email['subject']}",
            html_content=personalized_content
        )
        
        return {
            "success": result.get("success", False),
            "sequence_index": sequence_index,
            "subject": sequence_email['subject'],
            "message_id": result.get("message_id"),
            "error": result.get("error")
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Sequence email test failed"
        }

@app.get("/admin/automation-status")
async def automation_status(db: Session = Depends(get_db)):
    """Get status of email automation system"""
    try:
        # Count subscribers by type and status
        waitlist_total = db.query(WaitlistRegistration).count()
        waitlist_active = db.query(WaitlistRegistration).filter(WaitlistRegistration.is_active == True).count()
        waitlist_sequences_started = db.query(WaitlistRegistration).filter(WaitlistRegistration.sequence_started == True).count()
        
        lead_magnet_total = db.query(LeadMagnetDownload).count()
        lead_magnet_active = db.query(LeadMagnetDownload).filter(LeadMagnetDownload.is_active == True).count()
        
        corporate_total = db.query(CorporateInquiry).count()
        corporate_active = db.query(CorporateInquiry).filter(CorporateInquiry.is_active == True).count()
        
        # Count recent emails
        from datetime import timedelta
        last_24h = datetime.utcnow() - timedelta(hours=24)
        emails_sent_24h = db.query(EmailLog).filter(EmailLog.sent_at >= last_24h).count()
        
        return {
            "database_status": "connected",
            "subscribers": {
                "waitlist": {"total": waitlist_total, "active": waitlist_active, "sequences_started": waitlist_sequences_started},
                "lead_magnet": {"total": lead_magnet_total, "active": lead_magnet_active},
                "corporate": {"total": corporate_total, "active": corporate_active}
            },
            "email_activity": {
                "emails_sent_last_24h": emails_sent_24h
            },
            "sendgrid_configured": bool(sendgrid_service.api_key),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        return {
            "database_status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

# Email content management endpoints
@app.post("/admin/init-email-content")
async def init_email_content():
    """Initialize email sequences in database"""
    try:
        from email_content_manager import EmailContentManager
        manager = EmailContentManager()
        result = manager.initialize_sequences()
        return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to initialize email content"
        }

@app.get("/admin/list-sequence-emails/{sequence_type}")
async def list_sequence_emails(sequence_type: str):
    """List all emails in a sequence"""
    try:
        from email_content_manager import EmailContentManager
        manager = EmailContentManager()
        result = manager.list_sequence_emails(sequence_type)
        return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to list sequence emails"
        }

@app.put("/admin/update-sequence-email/{sequence_type}/{email_index}")
async def update_sequence_email(sequence_type: str, email_index: int, subject: str, content: str):
    """Update a sequence email"""
    try:
        from email_content_manager import EmailContentManager
        manager = EmailContentManager()
        result = manager.update_sequence_email(sequence_type, email_index, subject, content)
        return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to update sequence email"
        }


@app.post("/admin/test-single-sequence-email")
async def test_single_sequence_email(test_email: str, week_number: int, db: Session = Depends(get_db)):
    """Test a single email from the sequence"""
    try:
        from email_automation import EmailSequenceAutomation
        
        if week_number < 1 or week_number > 10:
            return {"success": False, "error": "Week number must be between 1 and 10"}
        
        automation = EmailSequenceAutomation()
        sequence_email = automation._get_sequence_email_content("waitlist_magnet", week_number)
        
        if not sequence_email:
            return {"success": False, "error": f"No content found for week {week_number}"}
        
        # Test subscriber data
        test_data = {
            "full_name": "Test User"
        }
        
        # Personalize and send
        personalized_content = automation._personalize_email_content(
            sequence_email['content'], 
            test_data
        )
        
        result = sendgrid_service.send_email(
            to_email=test_email,
            subject=f"[TEST WEEK {week_number}] {sequence_email['subject']}",
            html_content=personalized_content
        )
        
        return {
            "success": result.get("success", False),
            "week_number": week_number,
            "subject": sequence_email['subject'],
            "message_id": result.get("message_id"),
            "error": result.get("error"),
            "message": f"Week {week_number} email sent to {test_email}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to send week {week_number} email"
        }

@app.delete("/admin/delete-subscriber")
async def delete_subscriber_for_testing(email: str, db: Session = Depends(get_db)):
    """Delete subscriber from all tables for testing purposes"""
    try:
        # Delete from waitlist registrations
        waitlist_deleted = db.query(WaitlistRegistration).filter(WaitlistRegistration.email == email).delete()
        
        # Delete from lead magnet downloads
        lead_magnet_deleted = db.query(LeadMagnetDownload).filter(LeadMagnetDownload.email == email).delete()
        
        # Delete from corporate inquiries
        corporate_deleted = db.query(CorporateInquiry).filter(CorporateInquiry.email == email).delete()
        
        # Delete related email logs
        email_logs_deleted = db.query(EmailLog).filter(EmailLog.recipient_email == email).delete()
        
        db.commit()
        
        return {
            "success": True,
            "message": f"Subscriber {email} deleted from all tables",
            "deleted_counts": {
                "waitlist_registrations": waitlist_deleted,
                "lead_magnet_downloads": lead_magnet_deleted,
                "corporate_inquiries": corporate_deleted,
                "email_logs": email_logs_deleted
            }
        }
        
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to delete subscriber {email}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
