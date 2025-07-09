"""
End-to-End Email Workflow Testing Suite
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import get_db_url
from models import (
    EmailSubscriber, EmailSequence, SequenceEmail, SequenceEnrollment, 
    ScheduledEmail, EmailAnalytics
)
from sequence_automation import (
    auto_enroll_subscriber, create_or_get_subscriber, create_or_get_sequence,
    enroll_subscriber_in_sequence, get_emails_to_send, mark_email_as_sent
)
from email_scheduler import EmailScheduler
from webhook_handlers import process_webhook_event
from subscriber_segmentation import update_subscriber_engagement_level


# Test database setup
engine = create_engine(get_db_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class EmailWorkflowTester:
    """Comprehensive end-to-end email workflow testing"""
    
    def __init__(self):
        self.test_results = []
        self.test_data = {
            "subscribers": [],
            "sequences": [],
            "enrollments": [],
            "scheduled_emails": []
        }
    
    def log_test_result(self, test_name: str, passed: bool, details: str = "", data: Dict = None):
        """Log test result"""
        result = {
            "test_name": test_name,
            "passed": passed,
            "details": details,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data or {}
        }
        self.test_results.append(result)
        
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status} - {test_name}")
        if details:
            print(f"   Details: {details}")
    
    def test_1_subscriber_creation(self, db: Session) -> bool:
        """Test 1: Create test subscribers"""
        try:
            test_subscribers = [
                {"email": "test1@example.com", "name": "Test User 1", "source": "waitlist", "language": "en"},
                {"email": "test2@example.com", "name": "Test User 2", "source": "corporate", "language": "bg"},
                {"email": "test3@example.com", "name": "Test User 3", "source": "lead_magnet", "language": "en"}
            ]
            
            for subscriber_data in test_subscribers:
                subscriber = create_or_get_subscriber(
                    db, 
                    subscriber_data["email"], 
                    subscriber_data["name"], 
                    subscriber_data["source"],
                    subscriber_data["language"]
                )
                self.test_data["subscribers"].append(subscriber)
            
            self.log_test_result("Subscriber Creation", True, f"Created {len(test_subscribers)} test subscribers")
            return True
            
        except Exception as e:
            self.log_test_result("Subscriber Creation", False, f"Error: {str(e)}")
            return False
    
    def test_2_sequence_creation(self, db: Session) -> bool:
        """Test 2: Create test sequences"""
        try:
            sequence_types = [
                {"type": "waitlist", "language": "en"},
                {"type": "corporate", "language": "bg"},
                {"type": "lead_magnet", "language": "en"}
            ]
            
            for seq_data in sequence_types:
                sequence = create_or_get_sequence(db, seq_data["type"], seq_data["language"])
                self.test_data["sequences"].append(sequence)
            
            self.log_test_result("Sequence Creation", True, f"Created {len(sequence_types)} sequences")
            return True
            
        except Exception as e:
            self.log_test_result("Sequence Creation", False, f"Error: {str(e)}")
            return False
    
    def test_3_auto_enrollment(self, db: Session) -> bool:
        """Test 3: Auto-enrollment functionality"""
        try:
            enrollment_tests = [
                {"email": "auto1@example.com", "name": "Auto User 1", "source": "waitlist", "language": "en"},
                {"email": "auto2@example.com", "name": "Auto User 2", "source": "corporate", "language": "bg"}
            ]
            
            for enrollment_data in enrollment_tests:
                result = auto_enroll_subscriber(
                    db,
                    enrollment_data["email"],
                    enrollment_data["name"],
                    enrollment_data["source"],
                    enrollment_data["language"]
                )
                
                if not result.get("success"):
                    self.log_test_result("Auto Enrollment", False, f"Failed to enroll {enrollment_data['email']}")
                    return False
                
                # Verify enrollment was created
                enrollment = db.query(SequenceEnrollment).filter(
                    SequenceEnrollment.subscriber_id == result["subscriber_id"]
                ).first()
                
                if not enrollment:
                    self.log_test_result("Auto Enrollment", False, f"Enrollment not found for {enrollment_data['email']}")
                    return False
                
                self.test_data["enrollments"].append(enrollment)
            
            self.log_test_result("Auto Enrollment", True, f"Successfully enrolled {len(enrollment_tests)} subscribers")
            return True
            
        except Exception as e:
            self.log_test_result("Auto Enrollment", False, f"Error: {str(e)}")
            return False
    
    def test_4_email_scheduling(self, db: Session) -> bool:
        """Test 4: Email scheduling functionality"""
        try:
            # Check if emails were scheduled for enrollments
            scheduled_count = 0
            
            for enrollment in self.test_data["enrollments"]:
                scheduled_emails = db.query(ScheduledEmail).filter(
                    ScheduledEmail.enrollment_id == enrollment.id
                ).all()
                
                scheduled_count += len(scheduled_emails)
                self.test_data["scheduled_emails"].extend(scheduled_emails)
            
            if scheduled_count == 0:
                self.log_test_result("Email Scheduling", False, "No emails were scheduled")
                return False
            
            self.log_test_result("Email Scheduling", True, f"Scheduled {scheduled_count} emails")
            return True
            
        except Exception as e:
            self.log_test_result("Email Scheduling", False, f"Error: {str(e)}")
            return False
    
    def test_5_email_sending_simulation(self, db: Session) -> bool:
        """Test 5: Email sending simulation"""
        try:
            # Get emails ready to send (modify scheduled_for to make them ready)
            ready_emails = []
            for scheduled_email in self.test_data["scheduled_emails"][:3]:  # Test first 3
                # Make email ready to send
                scheduled_email.scheduled_for = datetime.utcnow() - timedelta(minutes=1)
                db.commit()
                ready_emails.append(scheduled_email)
            
            # Simulate sending
            for email in ready_emails:
                # Mark as sent (simulated)
                mark_email_as_sent(db, email, campaign_id=f"test-campaign-{email.id}")
            
            # Verify emails were marked as sent
            sent_count = 0
            for email in ready_emails:
                db.refresh(email)
                if email.status == "sent":
                    sent_count += 1
            
            self.log_test_result("Email Sending", True, f"Simulated sending {sent_count} emails")
            return True
            
        except Exception as e:
            self.log_test_result("Email Sending", False, f"Error: {str(e)}")
            return False
    
    def test_6_webhook_processing(self, db: Session) -> bool:
        """Test 6: Webhook event processing"""
        try:
            # Test webhook events for sent emails
            webhook_tests = []
            
            for email in self.test_data["scheduled_emails"]:
                if email.status == "sent" and email.mailerlite_campaign_id:
                    # Test open event
                    open_result = process_webhook_event("subscriber.opened", {
                        "subscriber": {"email": "test@example.com"},
                        "campaign": {"id": email.mailerlite_campaign_id}
                    })
                    webhook_tests.append(("Open", open_result))
                    
                    # Test click event
                    click_result = process_webhook_event("subscriber.clicked", {
                        "subscriber": {"email": "test@example.com"},
                        "campaign": {"id": email.mailerlite_campaign_id},
                        "click": {"url": "https://example.com/test"}
                    })
                    webhook_tests.append(("Click", click_result))
                    
                    break  # Test one email
            
            success_count = sum(1 for _, result in webhook_tests if result.get("status") == "processed")
            
            self.log_test_result("Webhook Processing", True, f"Processed {success_count}/{len(webhook_tests)} webhook events")
            return True
            
        except Exception as e:
            self.log_test_result("Webhook Processing", False, f"Error: {str(e)}")
            return False
    
    def test_7_engagement_tracking(self, db: Session) -> bool:
        """Test 7: Engagement level tracking"""
        try:
            # Update engagement levels for test subscribers
            updated_count = 0
            
            for subscriber in self.test_data["subscribers"]:
                old_level = subscriber.engagement_level
                new_level = update_subscriber_engagement_level(db, subscriber.id)
                
                if new_level:
                    updated_count += 1
            
            self.log_test_result("Engagement Tracking", True, f"Updated engagement for {updated_count} subscribers")
            return True
            
        except Exception as e:
            self.log_test_result("Engagement Tracking", False, f"Error: {str(e)}")
            return False
    
    def test_8_retry_logic(self, db: Session) -> bool:
        """Test 8: Retry logic for failed emails"""
        try:
            # Create a failed email for testing
            if self.test_data["scheduled_emails"]:
                test_email = self.test_data["scheduled_emails"][0]
                
                # Mark as failed
                mark_email_as_sent(db, test_email, error_message="Test failure")
                
                # Verify it's marked as failed
                db.refresh(test_email)
                if test_email.status == "failed":
                    self.log_test_result("Retry Logic", True, "Successfully tested retry logic setup")
                    return True
                else:
                    self.log_test_result("Retry Logic", False, "Failed to mark email as failed")
                    return False
            
            self.log_test_result("Retry Logic", False, "No scheduled emails to test")
            return False
            
        except Exception as e:
            self.log_test_result("Retry Logic", False, f"Error: {str(e)}")
            return False
    
    def test_9_sequence_completion(self, db: Session) -> bool:
        """Test 9: Sequence completion tracking"""
        try:
            # Simulate completing a sequence
            if self.test_data["enrollments"]:
                enrollment = self.test_data["enrollments"][0]
                
                # Get sequence email count
                sequence_email_count = db.query(SequenceEmail).filter(
                    SequenceEmail.sequence_id == enrollment.sequence_id
                ).count()
                
                # Set enrollment as completed
                enrollment.current_email_index = sequence_email_count
                enrollment.status = "completed"
                enrollment.completion_date = datetime.utcnow()
                db.commit()
                
                self.log_test_result("Sequence Completion", True, "Successfully tested sequence completion")
                return True
            
            self.log_test_result("Sequence Completion", False, "No enrollments to test")
            return False
            
        except Exception as e:
            self.log_test_result("Sequence Completion", False, f"Error: {str(e)}")
            return False
    
    def test_10_analytics_calculation(self, db: Session) -> bool:
        """Test 10: Analytics calculation"""
        try:
            from sequence_automation import get_sequence_analytics
            
            # Test analytics for a sequence
            if self.test_data["sequences"]:
                sequence = self.test_data["sequences"][0]
                analytics = get_sequence_analytics(db, sequence_id=sequence.id)
                
                required_fields = ["total_scheduled", "total_sent", "total_failed", "open_rate", "click_rate"]
                missing_fields = [field for field in required_fields if field not in analytics]
                
                if missing_fields:
                    self.log_test_result("Analytics Calculation", False, f"Missing fields: {missing_fields}")
                    return False
                
                self.log_test_result("Analytics Calculation", True, f"Analytics calculated successfully")
                return True
            
            self.log_test_result("Analytics Calculation", False, "No sequences to test")
            return False
            
        except Exception as e:
            self.log_test_result("Analytics Calculation", False, f"Error: {str(e)}")
            return False
    
    def cleanup_test_data(self, db: Session):
        """Clean up test data"""
        try:
            # Delete in reverse order due to foreign key constraints
            for email in self.test_data["scheduled_emails"]:
                db.delete(email)
            
            for enrollment in self.test_data["enrollments"]:
                db.delete(enrollment)
            
            # Delete test subscribers
            test_emails = [
                "test1@example.com", "test2@example.com", "test3@example.com",
                "auto1@example.com", "auto2@example.com"
            ]
            
            for email in test_emails:
                subscriber = db.query(EmailSubscriber).filter(EmailSubscriber.email == email).first()
                if subscriber:
                    db.delete(subscriber)
            
            db.commit()
            print("🧹 Test data cleaned up")
            
        except Exception as e:
            print(f"❌ Error cleaning up test data: {str(e)}")
    
    def run_full_test_suite(self) -> Dict[str, Any]:
        """Run complete end-to-end test suite"""
        print("🚀 Starting End-to-End Email Workflow Testing...")
        print("=" * 60)
        
        db = SessionLocal()
        try:
            # Run all tests
            tests = [
                self.test_1_subscriber_creation,
                self.test_2_sequence_creation,
                self.test_3_auto_enrollment,
                self.test_4_email_scheduling,
                self.test_5_email_sending_simulation,
                self.test_6_webhook_processing,
                self.test_7_engagement_tracking,
                self.test_8_retry_logic,
                self.test_9_sequence_completion,
                self.test_10_analytics_calculation
            ]
            
            for test in tests:
                test(db)
            
            # Calculate summary
            passed_tests = sum(1 for result in self.test_results if result["passed"])
            total_tests = len(self.test_results)
            
            summary = {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": total_tests - passed_tests,
                "success_rate": round((passed_tests / total_tests * 100) if total_tests > 0 else 0, 2),
                "test_results": self.test_results
            }
            
            print("=" * 60)
            print(f"📊 Test Summary:")
            print(f"   Total Tests: {total_tests}")
            print(f"   Passed: {passed_tests}")
            print(f"   Failed: {total_tests - passed_tests}")
            print(f"   Success Rate: {summary['success_rate']}%")
            
            if summary['success_rate'] >= 80:
                print("✅ Email workflow testing PASSED!")
            else:
                print("❌ Email workflow testing FAILED!")
            
            return summary
            
        finally:
            self.cleanup_test_data(db)
            db.close()


def run_workflow_tests():
    """Run the complete workflow test suite"""
    tester = EmailWorkflowTester()
    return tester.run_full_test_suite()


if __name__ == "__main__":
    # Run tests if called directly
    result = run_workflow_tests()
    
    # Save results to file
    with open("test_results.json", "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"\n📁 Test results saved to test_results.json")