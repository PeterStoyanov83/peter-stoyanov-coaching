#!/usr/bin/env python3
"""
Email Content Management System
Allows editing email sequences through database
"""
import logging
from sqlalchemy.orm import Session
from models import EmailSequence, SequenceEmail
from database import SessionLocal

logger = logging.getLogger(__name__)

class EmailContentManager:
    def __init__(self):
        self.db = SessionLocal()
    
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()
    
    def initialize_sequences(self):
        """Initialize email sequences in database from hardcoded content"""
        try:
            # Check if sequences already exist
            existing = self.db.query(EmailSequence).filter(EmailSequence.sequence_type == "waitlist_magnet").first()
            if existing:
                logger.info("Email sequences already exist in database")
                return {"success": True, "message": "Sequences already initialized"}
            
            # Create waitlist/magnet sequence
            waitlist_sequence = EmailSequence(
                name="Waitlist & Lead Magnet Sequence",
                sequence_type="waitlist_magnet",
                description="10-week leadership development email sequence for waitlist subscribers and lead magnet downloads",
                is_active=True
            )
            self.db.add(waitlist_sequence)
            self.db.commit()
            self.db.refresh(waitlist_sequence)
            
            # Add the 10 sequence emails
            sequence_emails = [
                {
                    "email_index": 1,
                    "subject": "Week 1: The Foundation of Great Leadership",
                    "delay_days": 7,
                    "html_content": """
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
                {
                    "email_index": 2,
                    "subject": "Week 2: Communication That Inspires",
                    "delay_days": 7,
                    "html_content": """
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
                {
                    "email_index": 3,
                    "subject": "Week 3: Building Trust Through Vulnerability", 
                    "delay_days": 7,
                    "html_content": """
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
                {
                    "email_index": 4,
                    "subject": "Week 4: The Art of Decisive Leadership",
                    "delay_days": 7,
                    "html_content": """
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
                                <li><strong>Performance:</strong> Who will execute the decision?</li>
                                <li><strong>Input:</strong> Who provides information and expertise?</li>
                                <li><strong>Decide:</strong> Who makes the final call?</li>
                            </ol>
                            <p><strong>Action Step:</strong> Map your next major decision using this framework.</p>
                            <p>Leading with clarity,<br>Peter</p>
                        </div>
                    </div>
                    """
                },
                {
                    "email_index": 5,
                    "subject": "Week 5: Emotional Intelligence in Action",
                    "delay_days": 7,
                    "html_content": """
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
                {
                    "email_index": 6,
                    "subject": "Week 6: Delegation That Develops People",
                    "delay_days": 7,
                    "html_content": """
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
                {
                    "email_index": 7,
                    "subject": "Week 7: Creating a Vision That Inspires",
                    "delay_days": 7,
                    "html_content": """
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
                {
                    "email_index": 8,
                    "subject": "Week 8: Conflict Resolution as a Leadership Tool",
                    "delay_days": 7,
                    "html_content": """
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
                {
                    "email_index": 9,
                    "subject": "Week 9: Building High-Performance Teams",
                    "delay_days": 7,
                    "html_content": """
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
                {
                    "email_index": 10,
                    "subject": "Week 10: Leading Through Change and Uncertainty",
                    "delay_days": 7,
                    "html_content": """
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
            ]
            
            # Add each sequence email
            for email_data in sequence_emails:
                sequence_email = SequenceEmail(
                    sequence_id=waitlist_sequence.id,
                    email_index=email_data["email_index"],
                    subject=email_data["subject"],
                    html_content=email_data["html_content"],
                    delay_days=email_data["delay_days"],
                    is_active=True
                )
                self.db.add(sequence_email)
            
            self.db.commit()
            
            return {
                "success": True,
                "message": "Email sequences initialized successfully",
                "sequence_id": waitlist_sequence.id,
                "emails_added": len(sequence_emails)
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error initializing email sequences: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to initialize email sequences"
            }
    
    def get_sequence_email_from_db(self, sequence_type: str, email_index: int):
        """Get sequence email from database instead of hardcoded content"""
        try:
            sequence = self.db.query(EmailSequence).filter(
                EmailSequence.sequence_type == sequence_type,
                EmailSequence.is_active == True
            ).first()
            
            if not sequence:
                return None
            
            sequence_email = self.db.query(SequenceEmail).filter(
                SequenceEmail.sequence_id == sequence.id,
                SequenceEmail.email_index == email_index,
                SequenceEmail.is_active == True
            ).first()
            
            if not sequence_email:
                return None
            
            return {
                "subject": sequence_email.subject,
                "content": sequence_email.html_content
            }
            
        except Exception as e:
            logger.error(f"Error getting sequence email from database: {str(e)}")
            return None
    
    def update_sequence_email(self, sequence_type: str, email_index: int, subject: str, content: str):
        """Update a sequence email in the database"""
        try:
            sequence = self.db.query(EmailSequence).filter(
                EmailSequence.sequence_type == sequence_type,
                EmailSequence.is_active == True
            ).first()
            
            if not sequence:
                return {"success": False, "error": "Sequence not found"}
            
            sequence_email = self.db.query(SequenceEmail).filter(
                SequenceEmail.sequence_id == sequence.id,
                SequenceEmail.email_index == email_index
            ).first()
            
            if not sequence_email:
                return {"success": False, "error": "Email not found"}
            
            sequence_email.subject = subject
            sequence_email.html_content = content
            self.db.commit()
            
            return {
                "success": True,
                "message": f"Email {email_index} updated successfully"
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating sequence email: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update email"
            }
    
    def list_sequence_emails(self, sequence_type: str):
        """List all emails in a sequence"""
        try:
            sequence = self.db.query(EmailSequence).filter(
                EmailSequence.sequence_type == sequence_type,
                EmailSequence.is_active == True
            ).first()
            
            if not sequence:
                return {"success": False, "error": "Sequence not found"}
            
            emails = self.db.query(SequenceEmail).filter(
                SequenceEmail.sequence_id == sequence.id
            ).order_by(SequenceEmail.email_index).all()
            
            email_list = []
            for email in emails:
                email_list.append({
                    "index": email.email_index,
                    "subject": email.subject,
                    "delay_days": email.delay_days,
                    "is_active": email.is_active,
                    "content_preview": email.html_content[:200] + "..." if len(email.html_content) > 200 else email.html_content
                })
            
            return {
                "success": True,
                "sequence_name": sequence.name,
                "emails": email_list
            }
            
        except Exception as e:
            logger.error(f"Error listing sequence emails: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to list emails"
            }

def init_email_content():
    """Initialize email content in database"""
    manager = EmailContentManager()
    return manager.initialize_sequences()

if __name__ == "__main__":
    result = init_email_content()
    print(result)