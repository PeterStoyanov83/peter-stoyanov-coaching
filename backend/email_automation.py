#!/usr/bin/env python3
"""
Email Sequence Automation System
Handles sending scheduled email sequences to subscribers
"""
import os
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from database import SessionLocal
from models import (
    WaitlistRegistration, CorporateInquiry, LeadMagnetDownload, 
    EmailSequence, SequenceEmail, EmailLog
)
from email_service import sendgrid_service

logger = logging.getLogger(__name__)

class EmailSequenceAutomation:
    def __init__(self):
        self.db = SessionLocal()
    
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()
    
    def process_all_sequences(self):
        """Main method to process all email sequences"""
        logger.info("Starting email sequence processing...")
        
        try:
            # Process waitlist sequences
            self._process_waitlist_sequences()
            
            # Process lead magnet sequences  
            self._process_lead_magnet_sequences()
            
            # Process corporate sequences
            self._process_corporate_sequences()
            
            logger.info("Email sequence processing completed successfully")
            
        except Exception as e:
            logger.error(f"Error in email sequence processing: {str(e)}")
            raise
    
    def _process_waitlist_sequences(self):
        """Process email sequences for waitlist subscribers"""
        # Get waitlist subscribers ready for next email
        subscribers = self.db.query(WaitlistRegistration).filter(
            WaitlistRegistration.is_active == True,
            WaitlistRegistration.welcome_sent == True,
            WaitlistRegistration.sequence_started == True,
            WaitlistRegistration.current_email_index < 12  # 12-week sequence
        ).all()
        
        for subscriber in subscribers:
            if self._should_send_next_email(subscriber.last_email_sent_at, subscriber.current_email_index):
                self._send_sequence_email(subscriber, "waitlist_magnet")
    
    def _process_lead_magnet_sequences(self):
        """Process email sequences for lead magnet subscribers"""
        # Get lead magnet subscribers ready for next email
        subscribers = self.db.query(LeadMagnetDownload).filter(
            LeadMagnetDownload.is_active == True,
            LeadMagnetDownload.welcome_sent == True,
            LeadMagnetDownload.sequence_started == True,
            LeadMagnetDownload.current_email_index < 12  # 12-week sequence
        ).all()
        
        for subscriber in subscribers:
            if self._should_send_next_email(subscriber.last_email_sent_at, subscriber.current_email_index):
                self._send_sequence_email(subscriber, "waitlist_magnet")
    
    def _process_corporate_sequences(self):
        """Process email sequences for corporate inquiries"""
        # Get corporate subscribers ready for next email
        subscribers = self.db.query(CorporateInquiry).filter(
            CorporateInquiry.is_active == True,
            CorporateInquiry.welcome_sent == True,
            CorporateInquiry.sequence_started == True,
            CorporateInquiry.current_email_index < 12  # 12-week sequence
        ).all()
        
        for subscriber in subscribers:
            if self._should_send_next_email(subscriber.last_email_sent_at, subscriber.current_email_index):
                self._send_sequence_email(subscriber, "corporate")
    
    def _should_send_next_email(self, last_sent_at, current_index):
        """Determine if it's time to send the next email"""
        if last_sent_at is None:
            return True  # First sequence email
        
        # Send weekly (7 days apart)
        days_since_last = (datetime.utcnow() - last_sent_at).days
        return days_since_last >= 7
    
    def _send_sequence_email(self, subscriber, sequence_type: str):
        """Send the next email in the sequence"""
        try:
            # Get the sequence email content
            next_index = subscriber.current_email_index + 1
            sequence_email = self._get_sequence_email_content(sequence_type, next_index)
            
            if not sequence_email:
                logger.warning(f"No sequence email found for {sequence_type} index {next_index}")
                return
            
            # Prepare subscriber data for personalization
            subscriber_data = self._prepare_subscriber_data(subscriber)
            
            # Send the email
            email_result = sendgrid_service.send_sequence_email(
                to_email=subscriber.email,
                sequence_email_data={
                    'subject': sequence_email['subject'],
                    'html_content': self._personalize_email_content(sequence_email['content'], subscriber_data)
                }
            )
            
            if email_result.get('success'):
                # Update subscriber progress
                subscriber.current_email_index = next_index
                subscriber.last_email_sent_at = datetime.utcnow()
                
                if next_index == 1:  # First sequence email
                    subscriber.sequence_started = True
                
                self.db.commit()
                
                # Log the email
                self._log_sequence_email(subscriber, sequence_email, email_result)
                
                logger.info(f"Sent sequence email {next_index} to {subscriber.email}")
            else:
                logger.error(f"Failed to send sequence email to {subscriber.email}: {email_result.get('error')}")
                
        except Exception as e:
            logger.error(f"Error sending sequence email to {subscriber.email}: {str(e)}")
            self.db.rollback()
    
    def _get_sequence_email_content(self, sequence_type: str, email_index: int) -> Dict[str, str]:
        """Get email content for specific sequence and index"""
        # This could be from database or predefined content
        # For now, using predefined content structure
        
        if sequence_type == "waitlist_magnet":
            return self._get_waitlist_magnet_email(email_index)
        elif sequence_type == "corporate":
            return self._get_corporate_email(email_index)
        
        return None
    
    def _get_waitlist_magnet_email(self, index: int) -> Dict[str, str]:
        """Get waitlist/magnet sequence email content"""
        emails = {
            1: {
                "subject": "Week 1: The Foundation of Great Leadership",
                "content": """
                <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center;">
                        <h1 style="color: #ffffff; margin: 0; font-size: 24px;">Week 1: Leadership Foundation</h1>
                    </div>
                    <div style="padding: 30px;">
                        <p>Hi {full_name},</p>
                        <p>Welcome to your first week of leadership insights! This week, we're focusing on the fundamental principles that separate good leaders from great ones.</p>
                        <h3>This Week's Focus: Self-Awareness</h3>
                        <p>The best leaders start with understanding themselves. Here are 3 key areas to reflect on:</p>
                        <ul>
                            <li><strong>Your Leadership Style:</strong> How do you naturally approach challenges?</li>
                            <li><strong>Your Triggers:</strong> What situations cause you stress or frustration?</li>
                            <li><strong>Your Values:</strong> What principles guide your decisions?</li>
                        </ul>
                        <p><strong>Action Item:</strong> Spend 10 minutes this week writing down your answers to these questions.</p>
                        <p>Looking forward to your leadership journey!</p>
                        <p>Best,<br>Peter</p>
                    </div>
                </div>
                """
            },
            2: {
                "subject": "Week 2: Communication That Inspires",
                "content": """
                <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center;">
                        <h1 style="color: #ffffff; margin: 0; font-size: 24px;">Week 2: Inspiring Communication</h1>
                    </div>
                    <div style="padding: 30px;">
                        <p>Hi {full_name},</p>
                        <p>This week we're diving into the art of communication that truly connects and motivates your team.</p>
                        <h3>The 3 Pillars of Leadership Communication:</h3>
                        <ol>
                            <li><strong>Clarity:</strong> Your message should be crystal clear</li>
                            <li><strong>Empathy:</strong> Understand your audience's perspective</li>
                            <li><strong>Purpose:</strong> Connect every message to the bigger why</li>
                        </ol>
                        <p><strong>This Week's Challenge:</strong> Practice the "3-2-1 Rule" - Before any important conversation, take 3 deep breaths, identify 2 key points you want to make, and connect them to 1 overarching purpose.</p>
                        <p>Keep leading with intention!</p>
                        <p>Best,<br>Peter</p>
                    </div>
                </div>
                """
            }
            # Add more weeks as needed...
        }
        
        return emails.get(index)
    
    def _get_corporate_email(self, index: int) -> Dict[str, str]:
        """Get corporate sequence email content"""
        emails = {
            1: {
                "subject": "Week 1: Building High-Performance Teams",
                "content": """
                <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff;">
                    <div style="background: linear-gradient(135deg, #2c5282 0%, #2a4365 100%); padding: 40px 20px; text-align: center;">
                        <h1 style="color: #ffffff; margin: 0; font-size: 24px;">Week 1: High-Performance Teams</h1>
                    </div>
                    <div style="padding: 30px;">
                        <p>Hello {contact_person},</p>
                        <p>Thank you for your interest in corporate leadership development. This week, let's explore what makes teams truly high-performing.</p>
                        <h3>The 4 Characteristics of High-Performance Teams:</h3>
                        <ul>
                            <li><strong>Psychological Safety:</strong> Team members feel safe to take risks and make mistakes</li>
                            <li><strong>Clear Goals:</strong> Everyone understands what success looks like</li>
                            <li><strong>Mutual Accountability:</strong> Team members hold each other accountable</li>
                            <li><strong>Continuous Learning:</strong> The team actively seeks to improve and grow</li>
                        </ul>
                        <p><strong>For Your Team:</strong> Consider conducting a team assessment on these 4 areas. Where is your team strongest? Where is there room for growth?</p>
                        <p>I'd love to discuss how we can implement these principles at {company_name}.</p>
                        <p>Best regards,<br>Peter Stoyanov</p>
                    </div>
                </div>
                """
            },
            2: {
                "subject": "Week 2: Strategic Leadership in Corporate Settings",
                "content": """
                <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff;">
                    <div style="background: linear-gradient(135deg, #2c5282 0%, #2a4365 100%); padding: 40px 20px; text-align: center;">
                        <h1 style="color: #ffffff; margin: 0; font-size: 24px;">Week 2: Strategic Leadership</h1>
                    </div>
                    <div style="padding: 30px;">
                        <p>Hello {contact_person},</p>
                        <p>Strategic thinking is what separates good managers from exceptional leaders. This week, let's explore how to develop strategic leadership within your organization.</p>
                        <h3>Key Strategic Leadership Skills:</h3>
                        <ol>
                            <li><strong>Systems Thinking:</strong> Understanding how different parts of the organization connect</li>
                            <li><strong>Future Focus:</strong> Anticipating trends and preparing for change</li>
                            <li><strong>Decision Making:</strong> Making informed decisions with incomplete information</li>
                        </ol>
                        <p><strong>Corporate Application:</strong> Consider creating cross-functional projects that require your leaders to think beyond their immediate scope.</p>
                        <p>Would you like to explore a customized leadership development program for {company_name}?</p>
                        <p>Best regards,<br>Peter Stoyanov</p>
                    </div>
                </div>
                """
            }
            # Add more weeks as needed...
        }
        
        return emails.get(index)
    
    def _prepare_subscriber_data(self, subscriber) -> Dict[str, Any]:
        """Prepare subscriber data for email personalization"""
        if isinstance(subscriber, WaitlistRegistration):
            return {
                'full_name': subscriber.full_name,
                'email': subscriber.email,
                'occupation': subscriber.occupation,
                'city_country': subscriber.city_country
            }
        elif isinstance(subscriber, CorporateInquiry):
            return {
                'contact_person': subscriber.contact_person,
                'company_name': subscriber.company_name,
                'email': subscriber.email,
                'team_size': subscriber.team_size
            }
        elif isinstance(subscriber, LeadMagnetDownload):
            return {
                'email': subscriber.email,
                'full_name': subscriber.email.split('@')[0].title()  # Fallback name
            }
        
        return {}
    
    def _personalize_email_content(self, content: str, subscriber_data: Dict[str, Any]) -> str:
        """Personalize email content with subscriber data"""
        try:
            return content.format(**subscriber_data)
        except KeyError as e:
            logger.warning(f"Missing personalization data: {e}")
            return content
    
    def _log_sequence_email(self, subscriber, sequence_email, email_result):
        """Log the sent sequence email"""
        try:
            # Determine which table to link to
            if isinstance(subscriber, WaitlistRegistration):
                email_log = EmailLog(
                    waitlist_id=subscriber.id,
                    email_type="sequence",
                    subject=sequence_email['subject'],
                    recipient_email=subscriber.email,
                    sendgrid_message_id=email_result.get('message_id')
                )
            elif isinstance(subscriber, CorporateInquiry):
                email_log = EmailLog(
                    corporate_id=subscriber.id,
                    email_type="sequence",
                    subject=sequence_email['subject'],
                    recipient_email=subscriber.email,
                    sendgrid_message_id=email_result.get('message_id')
                )
            elif isinstance(subscriber, LeadMagnetDownload):
                email_log = EmailLog(
                    lead_magnet_id=subscriber.id,
                    email_type="sequence",
                    subject=sequence_email['subject'],
                    recipient_email=subscriber.email,
                    sendgrid_message_id=email_result.get('message_id')
                )
            
            self.db.add(email_log)
            self.db.commit()
            
        except Exception as e:
            logger.error(f"Error logging sequence email: {str(e)}")

def run_email_automation():
    """Main function to run email automation"""
    automation = EmailSequenceAutomation()
    automation.process_all_sequences()

if __name__ == "__main__":
    run_email_automation()