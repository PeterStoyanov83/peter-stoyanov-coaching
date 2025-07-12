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
    EmailLogResponse
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