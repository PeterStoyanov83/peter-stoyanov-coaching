#!/usr/bin/env python3
"""
Production Scheduler Runner
Handles email automation scheduling for production deployment
"""
import os
import sys
import logging
import signal
import time
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/email_scheduler.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class EmailSchedulerService:
    def __init__(self):
        self.running = True
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
    
    def run_as_background_service(self):
        """Run scheduler as background service (for Docker/systemd)"""
        logger.info("Starting email scheduler as background service...")
        
        try:
            import schedule
            from email_automation import run_email_automation
            
            # Schedule email automation to run daily at 9 AM
            schedule.every().day.at("09:00").do(self._run_automation_job)
            
            # For testing/debugging, run every 30 minutes (comment out in production)
            # schedule.every(30).minutes.do(self._run_automation_job)
            
            logger.info("Email scheduler configured - running daily at 9:00 AM")
            
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except Exception as e:
            logger.error(f"Email scheduler service error: {str(e)}")
            raise
        
        logger.info("Email scheduler service stopped")
    
    def run_as_cron_job(self):
        """Run email automation once (for cron job execution)"""
        logger.info("Running email automation as cron job...")
        
        try:
            from email_automation import run_email_automation
            run_email_automation()
            logger.info("Email automation completed successfully")
            
        except Exception as e:
            logger.error(f"Email automation failed: {str(e)}")
            sys.exit(1)
    
    def _run_automation_job(self):
        """Internal method to run automation with error handling"""
        try:
            logger.info("Starting scheduled email automation job...")
            from email_automation import run_email_automation
            run_email_automation()
            logger.info("Scheduled email automation job completed successfully")
            
        except Exception as e:
            logger.error(f"Error in scheduled email automation job: {str(e)}")

def print_deployment_instructions():
    """Print deployment instructions for different environments"""
    print("""
🚀 EMAIL SCHEDULER DEPLOYMENT OPTIONS:

1. BACKGROUND SERVICE (Recommended for Docker/Render):
   python run_scheduler.py --service
   
   - Runs continuously in background
   - Automatically handles restarts
   - Good for containerized deployments

2. CRON JOB (Recommended for VPS/Traditional hosting):
   Add to crontab:
   0 9 * * * cd /path/to/backend && python run_scheduler.py --cron
   
   - More reliable (system manages scheduling)
   - Independent of main application
   - Standard Unix approach

3. SYSTEMD SERVICE (Recommended for Linux servers):
   Create /etc/systemd/system/email-scheduler.service:
   
   [Unit]
   Description=Email Automation Scheduler
   After=network.target
   
   [Service]
   Type=simple
   User=your-user
   WorkingDirectory=/path/to/backend
   ExecStart=/usr/bin/python3 run_scheduler.py --service
   Restart=always
   RestartSec=10
   
   [Install]
   WantedBy=multi-user.target
   
   Then: sudo systemctl enable email-scheduler && sudo systemctl start email-scheduler

4. DOCKER COMPOSE:
   Add to docker-compose.yml:
   
   scheduler:
     build: .
     command: python run_scheduler.py --service
     depends_on:
       - db
     environment:
       - SENDGRID_API_KEY=${SENDGRID_API_KEY}
       - DATABASE_URL=${DATABASE_URL}

📋 TESTING:
   Test the automation manually:
   python run_scheduler.py --test
   
   Test complete email sequence (11 emails in ~5 minutes):
   python run_scheduler.py --test-sequence your-email@example.com
   
   Check scheduler status:
   python run_scheduler.py --status
   
   API Testing (via curl/Postman):
   POST /admin/test-rapid-sequence?test_email=your-email@example.com
   POST /admin/test-single-sequence-email?test_email=your-email@example.com&week_number=1
""")

def main():
    if len(sys.argv) < 2:
        print_deployment_instructions()
        return
    
    command = sys.argv[1]
    service = EmailSchedulerService()
    
    if command == "--service":
        service.run_as_background_service()
    elif command == "--cron":
        service.run_as_cron_job()
    elif command == "--test":
        logger.info("Running test email automation...")
        try:
            from email_automation import run_email_automation
            run_email_automation()
            print("✅ Email automation test completed successfully")
        except Exception as e:
            print(f"❌ Email automation test failed: {str(e)}")
            sys.exit(1)
    elif command == "--test-sequence":
        if len(sys.argv) < 3:
            print("Usage: python run_scheduler.py --test-sequence your-email@example.com")
            sys.exit(1)
        
        test_email = sys.argv[2]
        logger.info(f"Running full sequence test to {test_email}...")
        
        try:
            import time
            from email_automation import EmailSequenceAutomation
            from email_service import sendgrid_service
            
            # Test data
            test_data = {
                "full_name": "Test User",
                "email": test_email,
                "occupation": "Test Manager", 
                "city_country": "Test City, Test Country"
            }
            
            automation = EmailSequenceAutomation()
            results = []
            
            print(f"🚀 Starting full sequence test to {test_email}")
            print("📧 Sending welcome email...")
            
            # Send welcome email
            welcome_result = sendgrid_service.send_welcome_email_waitlist(test_data)
            results.append(("Welcome", welcome_result.get("success", False)))
            
            time.sleep(5)  # Wait 5 seconds
            
            # Send all 10 sequence emails with 30 second intervals
            for i in range(1, 11):
                print(f"📧 Sending Week {i} email...")
                
                sequence_email = automation._get_sequence_email_content("waitlist_magnet", i)
                
                if sequence_email:
                    personalized_content = automation._personalize_email_content(
                        sequence_email['content'], test_data
                    )
                    
                    result = sendgrid_service.send_email(
                        to_email=test_email,
                        subject=f"[TEST SEQUENCE {i}/10] {sequence_email['subject']}",
                        html_content=personalized_content
                    )
                    
                    results.append((f"Week {i}", result.get("success", False)))
                    
                    if i < 10:  # Don't wait after the last email
                        print(f"⏰ Waiting 30 seconds before next email...")
                        time.sleep(30)
                else:
                    results.append((f"Week {i}", False))
                    print(f"❌ No content found for Week {i}")
            
            # Print summary
            successful = sum(1 for _, success in results if success)
            total = len(results)
            
            print(f"\n📊 SEQUENCE TEST COMPLETE!")
            print(f"✅ Emails sent: {successful}/{total}")
            print(f"📧 Check {test_email} for all emails")
            
            if successful < total:
                print(f"❌ {total - successful} emails failed to send")
                sys.exit(1)
            
        except Exception as e:
            print(f"❌ Full sequence test failed: {str(e)}")
            sys.exit(1)
    elif command == "--status":
        try:
            from database import SessionLocal
            from models import WaitlistRegistration, EmailLog
            from datetime import timedelta
            
            db = SessionLocal()
            
            # Get basic stats
            total_subscribers = db.query(WaitlistRegistration).count()
            active_subscribers = db.query(WaitlistRegistration).filter(WaitlistRegistration.is_active == True).count()
            
            # Get recent email activity
            last_24h = datetime.utcnow() - timedelta(hours=24)
            emails_sent_24h = db.query(EmailLog).filter(EmailLog.sent_at >= last_24h).count()
            
            db.close()
            
            print(f"""
📊 EMAIL AUTOMATION STATUS:

Subscribers:
  - Total: {total_subscribers}
  - Active: {active_subscribers}

Recent Activity:
  - Emails sent (last 24h): {emails_sent_24h}

Scheduler Status: Check logs for current status
Log file: /tmp/email_scheduler.log

Environment:
  - SENDGRID_API_KEY: {'✅ Set' if os.getenv('SENDGRID_API_KEY') else '❌ Missing'}
  - DATABASE_URL: {'✅ Set' if os.getenv('DATABASE_URL') else '❌ Missing'}
""")
            
        except Exception as e:
            print(f"❌ Error checking status: {str(e)}")
            sys.exit(1)
    else:
        print_deployment_instructions()

if __name__ == "__main__":
    main()