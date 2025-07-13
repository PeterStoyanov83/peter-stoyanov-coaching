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
            
            # Note: Corporate inquiries are handled manually, no automation
            
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
        try:
            # Try to get from database first
            from email_content_manager import EmailContentManager
            manager = EmailContentManager()
            db_content = manager.get_sequence_email_from_db(sequence_type, email_index)
            
            if db_content:
                return db_content
            
            # Fallback to hardcoded content
            logger.warning(f"No database content found for {sequence_type} email {email_index}, using fallback")
            if sequence_type == "waitlist_magnet":
                return self._get_waitlist_magnet_email(email_index)
            elif sequence_type == "corporate":
                return self._get_corporate_email(email_index)
            
        except Exception as e:
            logger.error(f"Error getting sequence email content: {str(e)}")
            # Fallback to hardcoded content
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
            },
            3: {
                "subject": "Week 3: Building Trust Through Vulnerability",
                "content": """
                <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center;">
                        <h1 style="color: #ffffff; margin: 0; font-size: 24px;">Week 3: Vulnerable Leadership</h1>
                    </div>
                    <div style="padding: 30px;">
                        <p>Hi {full_name},</p>
                        <p>This week, we explore one of the most counterintuitive leadership skills: strategic vulnerability.</p>
                        <h3>Why Vulnerability Creates Trust:</h3>
                        <ul>
                            <li><strong>Authenticity:</strong> People follow leaders they perceive as genuine</li>
                            <li><strong>Psychological Safety:</strong> When you model openness, others feel safe to contribute</li>
                            <li><strong>Connection:</strong> Shared struggles create deeper bonds than shared successes</li>
                        </ul>
                        <p><strong>This Week's Practice:</strong> Share one professional challenge you're working through with your team. Ask for their perspective.</p>
                        <p>Strength through openness,<br>Peter</p>
                    </div>
                </div>
                """
            },
            4: {
                "subject": "Week 4: The Art of Decisive Leadership",
                "content": """
                <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center;">
                        <h1 style="color: #ffffff; margin: 0; font-size: 24px;">Week 4: Decisive Leadership</h1>
                    </div>
                    <div style="padding: 30px;">
                        <p>Hi {full_name},</p>
                        <p>Great leaders make tough decisions with incomplete information. This week, we master the decision-making process.</p>
                        <h3>The RAPID Decision Framework:</h3>
                        <ol>
                            <li><strong>Recommend:</strong> Who suggests the course of action?</li>
                            <li><strong>Agree:</strong> Who must agree before moving forward?</li>
                            <li><strong>Perform:</strong> Who will execute the decision?</li>
                            <li><strong>Input:</strong> Who provides information and expertise?</li>
                            <li><strong>Decide:</strong> Who makes the final call?</li>
                        </ol>
                        <p><strong>Action Step:</strong> Map your next major decision using this framework.</p>
                        <p>Leading with clarity,<br>Peter</p>
                    </div>
                </div>
                """
            },
            5: {
                "subject": "Week 5: Emotional Intelligence in Action",
                "content": """
                <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center;">
                        <h1 style="color: #ffffff; margin: 0; font-size: 24px;">Week 5: Emotional Intelligence</h1>
                    </div>
                    <div style="padding: 30px;">
                        <p>Hi {full_name},</p>
                        <p>This week we dive deep into the skill that separates good leaders from exceptional ones: emotional intelligence.</p>
                        <h3>The 4 Domains of EQ:</h3>
                        <ul>
                            <li><strong>Self-Awareness:</strong> Understanding your emotions as they happen</li>
                            <li><strong>Self-Management:</strong> Controlling your emotional responses</li>
                            <li><strong>Social Awareness:</strong> Reading the emotions of others</li>
                            <li><strong>Relationship Management:</strong> Influencing positive emotional outcomes</li>
                        </ul>
                        <p><strong>This Week's Challenge:</strong> Before reacting to any frustrating situation, pause and name the emotion you're feeling.</p>
                        <p>Leading with wisdom,<br>Peter</p>
                    </div>
                </div>
                """
            },
            6: {
                "subject": "Week 6: Delegation That Develops People",
                "content": """
                <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center;">
                        <h1 style="color: #ffffff; margin: 0; font-size: 24px;">Week 6: Strategic Delegation</h1>
                    </div>
                    <div style="padding: 30px;">
                        <p>Hi {full_name},</p>
                        <p>True leadership isn't about doing everything yourself—it's about developing others to excel beyond what they thought possible.</p>
                        <h3>The GROW Model for Delegation:</h3>
                        <ol>
                            <li><strong>Goal:</strong> What specific outcome do you want?</li>
                            <li><strong>Reality:</strong> What skills does your team member currently have?</li>
                            <li><strong>Options:</strong> What support and resources can you provide?</li>
                            <li><strong>Will:</strong> What's their commitment level and timeline?</li>
                        </ol>
                        <p><strong>Action Item:</strong> Identify one task you can delegate using this framework this week.</p>
                        <p>Growing leaders,<br>Peter</p>
                    </div>
                </div>
                """
            },
            7: {
                "subject": "Week 7: Creating a Vision That Inspires",
                "content": """
                <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center;">
                        <h1 style="color: #ffffff; margin: 0; font-size: 24px;">Week 7: Visionary Leadership</h1>
                    </div>
                    <div style="padding: 30px;">
                        <p>Hi {full_name},</p>
                        <p>Great leaders paint a picture of the future so compelling that people can't help but want to be part of creating it.</p>
                        <h3>Elements of an Inspiring Vision:</h3>
                        <ul>
                            <li><strong>Clear Picture:</strong> People can visualize the future state</li>
                            <li><strong>Emotional Connection:</strong> It speaks to deeper values and purpose</li>
                            <li><strong>Achievable Stretch:</strong> Challenging but believable</li>
                            <li><strong>Personal Relevance:</strong> Everyone sees their role in achieving it</li>
                        </ul>
                        <p><strong>Vision Exercise:</strong> Write a one-paragraph description of where you want your team/organization to be in 3 years.</p>
                        <p>Painting the future,<br>Peter</p>
                    </div>
                </div>
                """
            },
            8: {
                "subject": "Week 8: Conflict Resolution as a Leadership Tool",
                "content": """
                <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center;">
                        <h1 style="color: #ffffff; margin: 0; font-size: 24px;">Week 8: Mastering Conflict</h1>
                    </div>
                    <div style="padding: 30px;">
                        <p>Hi {full_name},</p>
                        <p>Exceptional leaders don't avoid conflict—they transform it into opportunity for growth and innovation.</p>
                        <h3>The PEACE Method:</h3>
                        <ol>
                            <li><strong>Pause:</strong> Take time to understand all perspectives</li>
                            <li><strong>Empathize:</strong> Acknowledge everyone's feelings and concerns</li>
                            <li><strong>Ask:</strong> Focus on underlying interests, not positions</li>
                            <li><strong>Create:</strong> Brainstorm solutions together</li>
                            <li><strong>Execute:</strong> Agree on specific next steps</li>
                        </ol>
                        <p><strong>Challenge:</strong> Use this method in your next difficult conversation.</p>
                        <p>Turning tension into triumph,<br>Peter</p>
                    </div>
                </div>
                """
            },
            9: {
                "subject": "Week 9: Building High-Performance Teams",
                "content": """
                <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center;">
                        <h1 style="color: #ffffff; margin: 0; font-size: 24px;">Week 9: Team Excellence</h1>
                    </div>
                    <div style="padding: 30px;">
                        <p>Hi {full_name},</p>
                        <p>This week, we explore what transforms a group of individuals into a high-performing team that achieves extraordinary results.</p>
                        <h3>The 5 Characteristics of Elite Teams:</h3>
                        <ul>
                            <li><strong>Psychological Safety:</strong> Members feel safe to take risks and make mistakes</li>
                            <li><strong>Dependability:</strong> Everyone completes quality work on time</li>
                            <li><strong>Structure & Clarity:</strong> Clear goals, roles, and execution plans</li>
                            <li><strong>Meaning:</strong> Work has personal significance to each member</li>
                            <li><strong>Impact:</strong> The team believes their work matters</li>
                        </ul>
                        <p><strong>Team Assessment:</strong> Rate your team 1-10 on each characteristic. Focus on improving the lowest score.</p>
                        <p>Building excellence together,<br>Peter</p>
                    </div>
                </div>
                """
            },
            10: {
                "subject": "Week 10: Leading Through Change and Uncertainty",
                "content": """
                <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center;">
                        <h1 style="color: #ffffff; margin: 0; font-size: 24px;">Week 10: Leading Through Change</h1>
                    </div>
                    <div style="padding: 30px;">
                        <p>Hi {full_name},</p>
                        <p>Change is the only constant in leadership. This week, we master the art of guiding others through uncertainty with confidence and grace.</p>
                        <h3>The ADAPT Framework:</h3>
                        <ol>
                            <li><strong>Acknowledge:</strong> Recognize the reality of the situation openly</li>
                            <li><strong>Define:</strong> Clarify what you can and cannot control</li>
                            <li><strong>Assess:</strong> Evaluate options and potential outcomes</li>
                            <li><strong>Plan:</strong> Create flexible strategies with contingencies</li>
                            <li><strong>Take Action:</strong> Move forward with clear, decisive steps</li>
                        </ol>
                        <p><strong>Reflection:</strong> Think of a current change your team is facing. How can you apply this framework?</p>
                        <p>Navigating the unknown with certainty,<br>Peter</p>
                    </div>
                </div>
                """
            }
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
                'full_name': subscriber.full_name
            }
        elif isinstance(subscriber, CorporateInquiry):
            return {
                'contact_person': subscriber.contact_person,
                'company_name': subscriber.company_name
            }
        elif isinstance(subscriber, LeadMagnetDownload):
            return {
                'full_name': subscriber.email.split('@')[0].title()  # Fallback name from email
            }
        
        return {'full_name': 'Friend'}  # Default fallback
    
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