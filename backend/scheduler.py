#!/usr/bin/env python3
"""
Email Sequence Scheduler
Runs email automation on a schedule
"""
import schedule
import time
import logging
from email_automation import run_email_automation

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def scheduled_email_job():
    """Job that runs the email automation"""
    try:
        logger.info("Starting scheduled email automation job...")
        run_email_automation()
        logger.info("Scheduled email automation job completed successfully")
    except Exception as e:
        logger.error(f"Error in scheduled email automation job: {str(e)}")

def start_scheduler():
    """Start the email scheduler"""
    logger.info("Starting email sequence scheduler...")
    
    # Schedule email automation to run daily at 9 AM
    schedule.every().day.at("09:00").do(scheduled_email_job)
    
    # For testing, also run every 30 minutes (remove in production)
    # schedule.every(30).minutes.do(scheduled_email_job)
    
    logger.info("Email scheduler configured:")
    logger.info("- Daily at 9:00 AM")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    start_scheduler()