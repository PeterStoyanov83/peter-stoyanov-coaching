import os
import logging
from datetime import datetime
from sendgrid.sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class SendGridService:
    def __init__(self):
        self.api_key = os.getenv('SENDGRID_API_KEY')
        if not self.api_key:
            logger.warning("SENDGRID_API_KEY not found in environment variables")
            self.client = None
        else:
            self.client = SendGridAPIClient(api_key=self.api_key)
        
        self.from_email = "peterstoyanov83@gmail.com"
        self.admin_email = "peterstoyanov83@gmail.com"

    def send_email(self, to_email: str, subject: str, html_content: str, from_name: str = "Peter Stoyanov Coaching") -> Dict[str, Any]:
        """Send an email via SendGrid"""
        if not self.client:
            logger.error("SendGrid client not initialized")
            return {"success": False, "error": "SendGrid not configured"}
        
        try:
            mail = Mail(
                from_email=(self.from_email, from_name),
                to_emails=to_email,
                subject=subject,
                html_content=html_content
            )
            
            response = self.client.send(mail)
            
            return {
                "success": True,
                "message_id": response.headers.get('X-Message-Id'),
                "status_code": response.status_code
            }
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return {"success": False, "error": str(e)}

    def send_welcome_email_waitlist(self, registration_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send welcome email to waitlist subscriber"""
        subject = f"Welcome to Peter Stoyanov Coaching, {registration_data['full_name']}!"
        
        html_content = self._create_waitlist_welcome_template(registration_data)
        
        return self.send_email(
            to_email=registration_data['email'],
            subject=subject,
            html_content=html_content
        )

    def send_welcome_email_corporate(self, inquiry_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send welcome email to corporate inquirer"""
        subject = f"Thank you for your corporate training inquiry, {inquiry_data['contact_person']}!"
        
        html_content = self._create_corporate_welcome_template(inquiry_data)
        
        return self.send_email(
            to_email=inquiry_data['email'],
            subject=subject,
            html_content=html_content
        )

    def send_welcome_email_lead_magnet(self, email: str) -> Dict[str, Any]:
        """Send welcome email to lead magnet subscriber"""
        subject = "Your Leadership Guide is Ready + Welcome to the Community!"
        
        html_content = self._create_lead_magnet_welcome_template(email)
        
        return self.send_email(
            to_email=email,
            subject=subject,
            html_content=html_content
        )

    def send_admin_notification(self, subscriber_type: str, email: str) -> Dict[str, Any]:
        """Send notification to admin about new subscriber"""
        subject = f"🎉 New {subscriber_type.title()} Subscriber!"
        
        html_content = f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2c5282;">New Subscriber Alert</h2>
            <p>You have a new <strong>{subscriber_type}</strong> subscriber!</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Time:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
            <p>Check your admin dashboard for full details.</p>
        </div>
        """
        
        return self.send_email(
            to_email=self.admin_email,
            subject=subject,
            html_content=html_content
        )

    def send_sequence_email(self, to_email: str, sequence_email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send a sequence email"""
        return self.send_email(
            to_email=to_email,
            subject=sequence_email_data['subject'],
            html_content=sequence_email_data['html_content']
        )

    def send_blog_notification(self, to_email: str, blog_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send blog post notification"""
        subject = f"New Post: {blog_data['title']}"
        
        html_content = self._create_blog_notification_template(blog_data)
        
        return self.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content
        )

    def _create_waitlist_welcome_template(self, data: Dict[str, Any]) -> str:
        """Create HTML template for waitlist welcome email"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome to Peter Stoyanov Coaching</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f8fafc;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                
                <!-- Header -->
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center;">
                    <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 600;">Welcome, {data['full_name']}!</h1>
                    <p style="color: #e2e8f0; margin: 10px 0 0 0; font-size: 16px;">You're now part of the leadership development community</p>
                </div>
                
                <!-- Content -->
                <div style="padding: 40px 30px;">
                    <p style="color: #2d3748; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                        Thank you for joining the waitlist for my leadership coaching program! I'm excited to help you develop your skills in <strong>{data['skills_to_improve']}</strong> and achieve your goal of <em>"{data['why_join']}"</em>.
                    </p>
                    
                    <p style="color: #2d3748; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                        As a <strong>{data['occupation']}</strong> in {data['city_country']}, you bring unique perspectives that I look forward to working with.
                    </p>
                    
                    <div style="background-color: #f0fff4; border: 2px solid #38a169; padding: 25px; border-radius: 8px; margin: 30px 0; text-align: center;">
                        <h3 style="color: #2f855a; margin: 0 0 15px 0; font-size: 20px;">🎁 Welcome Gift: Leadership Guide</h3>
                        <p style="color: #2d3748; margin: 0 0 20px 0;">As a thank you for joining, here's your exclusive leadership development guide!</p>
                        <a href="https://peter-stoyanov.com/guides/5-theater-secrets-guide.pdf" style="display: inline-block; background: linear-gradient(135deg, #38a169 0%, #2f855a 100%); color: #ffffff; padding: 15px 30px; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 16px;">Download Your Free Guide</a>
                    </div>
                    
                    <div style="background-color: #edf2f7; padding: 20px; border-radius: 8px; margin: 30px 0;">
                        <h3 style="color: #2c5282; margin: 0 0 10px 0; font-size: 18px;">What's Next?</h3>
                        <ul style="color: #2d3748; margin: 0; padding-left: 20px;">
                            <li style="margin-bottom: 8px;">You'll receive weekly insights on leadership development</li>
                            <li style="margin-bottom: 8px;">Get early access to new programs and resources</li>
                            <li style="margin-bottom: 8px;">I'll personally reach out when spots open up</li>
                        </ul>
                    </div>
                    
                    <p style="color: #2d3748; font-size: 16px; line-height: 1.6; margin: 0 0 30px 0;">
                        In the meantime, feel free to explore my latest insights on <a href="https://peter-stoyanov.com" style="color: #667eea; text-decoration: none;">peter-stoyanov.com</a>.
                    </p>
                    
                    <div style="text-align: center;">
                        <a href="https://peter-stoyanov.com" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: 600;">Visit My Website</a>
                    </div>
                </div>
                
                <!-- Footer -->
                <div style="background-color: #f7fafc; padding: 30px; text-align: center; border-top: 1px solid #e2e8f0;">
                    <p style="color: #718096; font-size: 14px; margin: 0 0 10px 0;">
                        Best regards,<br>
                        <strong>Peter Stoyanov</strong><br>
                        Leadership & Executive Coach
                    </p>
                    <p style="color: #a0aec0; font-size: 12px; margin: 0;">
                        You're receiving this because you signed up for coaching updates. 
                        <a href="#" style="color: #667eea;">Unsubscribe</a> if you no longer wish to receive these emails.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

    def _create_corporate_welcome_template(self, data: Dict[str, Any]) -> str:
        """Create HTML template for corporate welcome email"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Corporate Training Inquiry - Peter Stoyanov Coaching</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f8fafc;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                
                <!-- Header -->
                <div style="background: linear-gradient(135deg, #2c5282 0%, #2a4365 100%); padding: 40px 20px; text-align: center;">
                    <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 600;">Thank you, {data['contact_person']}!</h1>
                    <p style="color: #e2e8f0; margin: 10px 0 0 0; font-size: 16px;">Your corporate training inquiry has been received</p>
                </div>
                
                <!-- Content -->
                <div style="padding: 40px 30px;">
                    <p style="color: #2d3748; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                        Thank you for considering Peter Stoyanov Coaching for <strong>{data['company_name']}</strong>'s leadership development needs.
                    </p>
                    
                    <div style="background-color: #edf2f7; padding: 20px; border-radius: 8px; margin: 30px 0;">
                        <h3 style="color: #2c5282; margin: 0 0 15px 0; font-size: 18px;">Your Inquiry Details:</h3>
                        <div style="color: #2d3748; font-size: 14px;">
                            <p style="margin: 5px 0;"><strong>Team Size:</strong> {data['team_size']}</p>
                            {f'<p style="margin: 5px 0;"><strong>Budget:</strong> {data["budget"]}</p>' if data.get('budget') else ''}
                            <p style="margin: 5px 0;"><strong>Training Goals:</strong> {data['training_goals']}</p>
                            {f'<p style="margin: 5px 0;"><strong>Preferred Timeline:</strong> {data["preferred_dates"]}</p>' if data.get('preferred_dates') else ''}
                        </div>
                    </div>
                    
                    <p style="color: #2d3748; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                        I'll personally review your requirements and get back to you within 24 hours with a customized proposal that addresses your specific leadership development needs.
                    </p>
                    
                    <div style="background-color: #f0fff4; border-left: 4px solid #38a169; padding: 20px; margin: 30px 0;">
                        <h4 style="color: #2f855a; margin: 0 0 10px 0; font-size: 16px;">What happens next?</h4>
                        <ul style="color: #2d3748; margin: 0; padding-left: 20px; font-size: 14px;">
                            <li style="margin-bottom: 8px;">I'll prepare a tailored training proposal</li>
                            <li style="margin-bottom: 8px;">Schedule a discovery call to discuss your specific needs</li>
                            <li style="margin-bottom: 8px;">Provide case studies from similar organizations</li>
                        </ul>
                    </div>
                    
                    <p style="color: #2d3748; font-size: 16px; line-height: 1.6; margin: 0 0 30px 0;">
                        In the meantime, you can learn more about my corporate training approach at <a href="https://peter-stoyanov.com" style="color: #2c5282; text-decoration: none;">peter-stoyanov.com</a>.
                    </p>
                    
                    <div style="text-align: center;">
                        <a href="https://peter-stoyanov.com" style="display: inline-block; background: linear-gradient(135deg, #2c5282 0%, #2a4365 100%); color: #ffffff; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: 600;">Learn More About Corporate Training</a>
                    </div>
                </div>
                
                <!-- Footer -->
                <div style="background-color: #f7fafc; padding: 30px; text-align: center; border-top: 1px solid #e2e8f0;">
                    <p style="color: #718096; font-size: 14px; margin: 0 0 10px 0;">
                        Best regards,<br>
                        <strong>Peter Stoyanov</strong><br>
                        Leadership & Executive Coach<br>
                        <a href="mailto:peterstoyanov83@gmail.com" style="color: #2c5282;">peterstoyanov83@gmail.com</a>
                    </p>
                    <p style="color: #a0aec0; font-size: 12px; margin: 0;">
                        You're receiving this because you inquired about corporate training. 
                        <a href="#" style="color: #2c5282;">Unsubscribe</a> if you no longer wish to receive these emails.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

    def _create_lead_magnet_welcome_template(self, email: str) -> str:
        """Create HTML template for lead magnet welcome email"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Your Leadership Guide - Peter Stoyanov Coaching</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f8fafc;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                
                <!-- Header -->
                <div style="background: linear-gradient(135deg, #38a169 0%, #2f855a 100%); padding: 40px 20px; text-align: center;">
                    <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 600;">Your Guide is Ready! 📚</h1>
                    <p style="color: #e2e8f0; margin: 10px 0 0 0; font-size: 16px;">Plus, welcome to the leadership community</p>
                </div>
                
                <!-- Content -->
                <div style="padding: 40px 30px;">
                    <p style="color: #2d3748; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                        Thank you for downloading the leadership guide! You now have access to proven strategies that will help you become a more effective leader.
                    </p>
                    
                    <div style="background-color: #f0fff4; border: 2px solid #38a169; padding: 25px; border-radius: 8px; margin: 30px 0; text-align: center;">
                        <h3 style="color: #2f855a; margin: 0 0 15px 0; font-size: 20px;">📥 Download Your Guide</h3>
                        <a href="#" style="display: inline-block; background: linear-gradient(135deg, #38a169 0%, #2f855a 100%); color: #ffffff; padding: 15px 30px; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 16px;">Get Your Leadership Guide</a>
                    </div>
                    
                    <p style="color: #2d3748; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                        As a bonus, you're now part of my exclusive leadership community. Every week, you'll receive:
                    </p>
                    
                    <div style="background-color: #edf2f7; padding: 20px; border-radius: 8px; margin: 30px 0;">
                        <ul style="color: #2d3748; margin: 0; padding-left: 20px;">
                            <li style="margin-bottom: 10px;"><strong>Weekly Leadership Insights</strong> - Practical tips you can use immediately</li>
                            <li style="margin-bottom: 10px;"><strong>Case Studies</strong> - Real examples from successful leaders</li>
                            <li style="margin-bottom: 10px;"><strong>Exclusive Resources</strong> - Tools and templates for leadership development</li>
                            <li style="margin-bottom: 10px;"><strong>Early Access</strong> - First to know about new programs and opportunities</li>
                        </ul>
                    </div>
                    
                    <p style="color: #2d3748; font-size: 16px; line-height: 1.6; margin: 0 0 30px 0;">
                        Start exploring more leadership resources at <a href="https://peter-stoyanov.com" style="color: #38a169; text-decoration: none;">peter-stoyanov.com</a>.
                    </p>
                    
                    <div style="text-align: center;">
                        <a href="https://peter-stoyanov.com" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: 600;">Explore More Resources</a>
                    </div>
                </div>
                
                <!-- Footer -->
                <div style="background-color: #f7fafc; padding: 30px; text-align: center; border-top: 1px solid #e2e8f0;">
                    <p style="color: #718096; font-size: 14px; margin: 0 0 10px 0;">
                        Best regards,<br>
                        <strong>Peter Stoyanov</strong><br>
                        Leadership & Executive Coach
                    </p>
                    <p style="color: #a0aec0; font-size: 12px; margin: 0;">
                        You're receiving this because you downloaded our leadership guide. 
                        <a href="#" style="color: #38a169;">Unsubscribe</a> if you no longer wish to receive these emails.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

    def _create_blog_notification_template(self, blog_data: Dict[str, Any]) -> str:
        """Create HTML template for blog post notification"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>New Post: {blog_data['title']}</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f8fafc;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                
                <!-- Header -->
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center;">
                    <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 600;">New Leadership Insight</h1>
                    <p style="color: #e2e8f0; margin: 10px 0 0 0; font-size: 16px;">Fresh from Peter Stoyanov Coaching</p>
                </div>
                
                <!-- Content -->
                <div style="padding: 40px 30px;">
                    {f'<img src="{blog_data["featured_image"]}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px; margin-bottom: 20px;" alt="Featured image">' if blog_data.get('featured_image') else ''}
                    
                    <h2 style="color: #2d3748; margin: 0 0 15px 0; font-size: 24px; line-height: 1.3;">{blog_data['title']}</h2>
                    
                    <p style="color: #4a5568; font-size: 16px; line-height: 1.6; margin: 0 0 30px 0;">
                        {blog_data['excerpt']}
                    </p>
                    
                    <div style="text-align: center; margin: 40px 0;">
                        <a href="https://peter-stoyanov.com/blog/{blog_data['slug']}" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; padding: 15px 30px; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 16px;">Read Full Article</a>
                    </div>
                    
                    {f'<div style="margin-top: 30px;"><p style="color: #718096; font-size: 14px; margin: 0;"><strong>Tags:</strong> {", ".join(blog_data["tags"])}</p></div>' if blog_data.get('tags') else ''}
                </div>
                
                <!-- Footer -->
                <div style="background-color: #f7fafc; padding: 30px; text-align: center; border-top: 1px solid #e2e8f0;">
                    <p style="color: #718096; font-size: 14px; margin: 0 0 10px 0;">
                        <strong>Peter Stoyanov</strong><br>
                        Leadership & Executive Coach
                    </p>
                    <p style="color: #a0aec0; font-size: 12px; margin: 0;">
                        You're receiving this because you're subscribed to leadership updates. 
                        <a href="#" style="color: #667eea;">Unsubscribe</a> | <a href="https://peter-stoyanov.com" style="color: #667eea;">Visit Website</a>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

# Create singleton instance
sendgrid_service = SendGridService()