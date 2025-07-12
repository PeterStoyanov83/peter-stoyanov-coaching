#!/usr/bin/env python3
"""
Comprehensive Test Data Population Script
Creates realistic test data for waitlist, corporate inquiries, communications, and tasks
"""
import os
import sys
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import random
import json

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import (
    WaitlistRegistration, CorporateInquiry, LeadMagnetDownload,
    EmailSubscriber, Communication, Task, Base
)

def get_database_url():
    """Get database URL from environment or use default"""
    return os.getenv('DATABASE_URL', 'postgresql://peterstoyanov@localhost:5432/coaching_site')

def create_test_data():
    """Create comprehensive test data"""
    database_url = get_database_url()
    print(f"🗃️  Connecting to database: {database_url.split('@')[0] if '@' in database_url else database_url}")
    
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    with SessionLocal() as db:
        print("🚀 Creating comprehensive test data...")
        
        # Sample data pools
        first_names = [
            "Alexander", "Maria", "James", "Sofia", "David", "Elena", "Michael", "Anna",
            "Robert", "Viktoria", "John", "Petya", "Daniel", "Irina", "Peter", "Katya",
            "Thomas", "Nadya", "Richard", "Svetlana", "Christopher", "Mariya", "Paul", "Galya"
        ]
        
        last_names = [
            "Petrov", "Johnson", "Smith", "Ivanova", "Williams", "Dimitrov", "Brown", "Stoycheva",
            "Jones", "Nikolova", "Garcia", "Georgiev", "Miller", "Popova", "Davis", "Marinov",
            "Rodriguez", "Ilieva", "Wilson", "Yankov", "Martinez", "Kostova", "Anderson", "Hristov"
        ]
        
        cities = [
            "Sofia, Bulgaria", "London, UK", "New York, USA", "Berlin, Germany", "Paris, France",
            "Amsterdam, Netherlands", "Vienna, Austria", "Prague, Czech Republic", "Warsaw, Poland",
            "Budapest, Hungary", "Bucharest, Romania", "Athens, Greece", "Madrid, Spain",
            "Stockholm, Sweden", "Oslo, Norway", "Copenhagen, Denmark", "Helsinki, Finland",
            "Dublin, Ireland", "Brussels, Belgium", "Zurich, Switzerland"
        ]
        
        occupations = [
            "Marketing Manager", "Software Engineer", "Project Manager", "Sales Director",
            "HR Manager", "Data Analyst", "Product Manager", "Business Analyst",
            "Operations Manager", "Team Lead", "Consultant", "Entrepreneur",
            "CEO", "CTO", "VP Sales", "Director", "Senior Manager", "Department Head"
        ]
        
        company_names = [
            "TechCorp Solutions", "Global Dynamics", "InnovateLab", "FutureWorks Inc",
            "Digital Horizons", "SmartTech Ltd", "NextGen Systems", "ProActive Solutions",
            "Excellence Consulting", "Strategic Partners", "Growth Ventures", "Prime Technologies",
            "Elite Services", "Quantum Solutions", "Alpha Industries", "Beta Innovations",
            "Gamma Enterprises", "Delta Corp", "Epsilon Holdings", "Zeta Group"
        ]
        
        skills_to_improve = [
            "leadership and team management",
            "communication and presentation skills",
            "strategic thinking and planning",
            "conflict resolution and negotiation",
            "time management and productivity",
            "emotional intelligence and empathy",
            "decision making under pressure",
            "delegation and empowerment",
            "change management and adaptability",
            "cross-cultural communication"
        ]
        
        why_join_reasons = [
            "I want to advance my career and become a better leader for my team",
            "Looking to improve my management skills and drive better results",
            "Need to develop stronger communication skills for executive presentations",
            "Want to build confidence in leading organizational change initiatives",
            "Seeking to enhance my strategic thinking and long-term planning abilities",
            "Looking to improve team dynamics and employee engagement",
            "Need help with work-life balance and stress management",
            "Want to develop better negotiation and conflict resolution skills",
            "Seeking to improve my emotional intelligence and people skills",
            "Looking to transition into a senior leadership role"
        ]
        
        training_goals = [
            "Develop leadership skills for our growing management team",
            "Improve communication and collaboration across departments",
            "Build a stronger company culture and employee engagement",
            "Enhance strategic planning and execution capabilities",
            "Develop change management skills for digital transformation",
            "Improve customer service and client relationship management",
            "Build high-performing teams and reduce turnover",
            "Develop innovation and creative thinking capabilities",
            "Improve sales and business development skills",
            "Build resilience and stress management capabilities"
        ]
        
        # 1. Create Waitlist Registrations (50 entries)
        print("📝 Creating waitlist registrations...")
        waitlist_statuses = ["new", "contacted", "qualified", "converted", "not_interested", "rejected"]
        priorities = ["low", "medium", "high", "urgent"]
        
        for i in range(50):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            full_name = f"{first_name} {last_name}"
            email = f"{first_name.lower()}.{last_name.lower()}.{i+1}@example.com"
            
            # Create realistic dates
            created_days_ago = random.randint(1, 90)
            created_at = datetime.utcnow() - timedelta(days=created_days_ago)
            
            status = random.choice(waitlist_statuses)
            priority = random.choice(priorities)
            
            # Determine follow-up date based on status
            follow_up_date = None
            last_contacted = None
            if status in ["contacted", "qualified"]:
                last_contacted = created_at + timedelta(days=random.randint(1, 5))
                follow_up_date = datetime.utcnow() + timedelta(days=random.randint(-5, 15))
            elif status == "new" and random.random() < 0.3:
                follow_up_date = datetime.utcnow() + timedelta(days=random.randint(1, 7))
            
            # Generate lead score
            base_score = 30
            if "manager" in random.choice(occupations).lower():
                base_score += 20
            if "leadership" in random.choice(skills_to_improve):
                base_score += 15
            lead_score = min(base_score + random.randint(-10, 25), 100)
            
            # Create notes based on status
            notes = None
            if status != "new":
                note_options = [
                    "Very interested in leadership development program",
                    "Has budget constraints, following up next quarter",
                    "Wants to discuss group coaching options",
                    "Prefers online sessions due to travel schedule",
                    "Looking for executive coaching specifically",
                    "Needs approval from HR department",
                    "Interested in both individual and team coaching"
                ]
                notes = random.choice(note_options)
            
            waitlist_entry = WaitlistRegistration(
                full_name=full_name,
                email=email,
                city_country=random.choice(cities),
                occupation=random.choice(occupations),
                why_join=random.choice(why_join_reasons),
                skills_to_improve=random.choice(skills_to_improve),
                created_at=created_at,
                status=status,
                notes=notes,
                priority=priority,
                last_contacted=last_contacted,
                follow_up_date=follow_up_date,
                lead_score=lead_score,
                tags=random.sample(["leadership", "management", "communication", "strategy"], k=random.randint(1, 3)),
                updated_by="admin" if status != "new" else None,
                updated_at=last_contacted or created_at
            )
            
            db.add(waitlist_entry)
        
        print("✅ Created 50 waitlist registrations")
        
        # 2. Create Corporate Inquiries (30 entries)
        print("🏢 Creating corporate inquiries...")
        corporate_statuses = ["new", "qualified", "proposal_sent", "negotiation", "closed_won", "closed_lost", "on_hold"]
        team_sizes = ["1-5", "5-10", "10-20", "20-50", "50-100", "100+"]
        budgets = ["€1,000-5,000", "€5,000-10,000", "€10,000-20,000", "€20,000-50,000", "€50,000+"]
        
        for i in range(30):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            contact_person = f"{first_name} {last_name}"
            email = f"{first_name.lower()}.{last_name.lower()}.corp{i+1}@{random.choice(company_names).lower().replace(' ', '').replace('inc', '').replace('ltd', '').replace('corp', '')}.com"
            
            created_days_ago = random.randint(1, 120)
            created_at = datetime.utcnow() - timedelta(days=created_days_ago)
            
            status = random.choice(corporate_statuses)
            priority = random.choice(priorities)
            team_size = random.choice(team_sizes)
            budget = random.choice(budgets)
            
            # Determine estimated value based on team size and budget
            estimated_value = None
            if team_size in ["50-100", "100+"]:
                estimated_value = random.randint(15000, 75000)
            elif team_size in ["20-50"]:
                estimated_value = random.randint(8000, 35000)
            elif team_size in ["10-20"]:
                estimated_value = random.randint(5000, 20000)
            else:
                estimated_value = random.randint(2000, 10000)
            
            # Determine probability based on status
            probability_map = {
                "new": random.randint(20, 40),
                "qualified": random.randint(40, 60),
                "proposal_sent": random.randint(60, 80),
                "negotiation": random.randint(70, 90),
                "closed_won": 100,
                "closed_lost": 0,
                "on_hold": random.randint(30, 50)
            }
            probability = probability_map[status]
            
            # Determine follow-up and other dates
            follow_up_date = None
            proposal_sent_date = None
            expected_close_date = None
            last_contacted = None
            
            if status in ["qualified", "proposal_sent", "negotiation", "on_hold"]:
                last_contacted = created_at + timedelta(days=random.randint(1, 7))
                follow_up_date = datetime.utcnow() + timedelta(days=random.randint(-3, 10))
                
            if status in ["proposal_sent", "negotiation", "closed_won", "closed_lost"]:
                proposal_sent_date = created_at + timedelta(days=random.randint(5, 20))
                expected_close_date = datetime.utcnow() + timedelta(days=random.randint(5, 45))
            
            # Generate lead score for corporate
            base_score = 40
            if team_size in ["50-100", "100+"]:
                base_score += 30
            elif team_size in ["20-50"]:
                base_score += 20
            if estimated_value and estimated_value > 20000:
                base_score += 20
            lead_score = min(base_score + random.randint(-15, 20), 100)
            
            # Create notes
            notes = None
            if status != "new":
                note_options = [
                    "Decision maker very engaged, high probability",
                    "Need to address budget concerns in next meeting",
                    "Competing with 2 other providers",
                    "Great cultural fit, they love our approach",
                    "Waiting for Q1 budget approval",
                    "CEO wants to see ROI projections",
                    "HR director is our champion in the process",
                    "They want to start with pilot program",
                    "Need customized proposal for their industry",
                    "Timeline pushed to next quarter due to restructuring"
                ]
                notes = random.choice(note_options)
            
            # Lost reason for closed_lost
            lost_reason = None
            if status == "closed_lost":
                lost_reasons = ["Budget constraints", "Chose competitor", "Internal solution", "Timeline mismatch", "No decision made"]
                lost_reason = random.choice(lost_reasons)
            
            corporate_inquiry = CorporateInquiry(
                company_name=random.choice(company_names),
                contact_person=contact_person,
                email=email,
                phone=f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                team_size=team_size,
                budget=budget,
                training_goals=random.choice(training_goals),
                preferred_dates=f"Q{random.randint(1, 4)} 202{random.randint(4, 5)}",
                additional_info="Looking for comprehensive leadership development program",
                created_at=created_at,
                status=status,
                priority=priority,
                estimated_value=estimated_value,
                proposal_sent_date=proposal_sent_date,
                follow_up_date=follow_up_date,
                expected_close_date=expected_close_date,
                notes=notes,
                assigned_to="admin" if status != "new" else None,
                last_contacted=last_contacted,
                updated_by="admin" if status != "new" else None,
                updated_at=last_contacted or created_at,
                lead_score=lead_score,
                tags=random.sample(["enterprise", "leadership", "team-building", "strategic"], k=random.randint(1, 3)),
                probability=probability,
                lost_reason=lost_reason
            )
            
            db.add(corporate_inquiry)
        
        print("✅ Created 30 corporate inquiries")
        
        # 3. Create Lead Magnet Downloads (40 entries)
        print("🧲 Creating lead magnet downloads...")
        for i in range(40):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@example.com"
            
            created_days_ago = random.randint(1, 60)
            created_at = datetime.utcnow() - timedelta(days=created_days_ago)
            
            download_count = random.randint(1, 3)
            last_downloaded = created_at + timedelta(days=random.randint(0, 30)) if download_count > 1 else created_at
            
            lead_download = LeadMagnetDownload(
                email=email,
                download_count=download_count,
                created_at=created_at,
                last_downloaded_at=last_downloaded
            )
            
            db.add(lead_download)
        
        print("✅ Created 40 lead magnet downloads")
        
        # 4. Create Email Subscribers (25 entries)
        print("👥 Creating email subscribers...")
        sources = ["lead_magnet", "waitlist", "corporate"]
        languages = ["en", "bg"]
        engagement_levels = ["new", "warm", "hot", "cold"]
        
        for i in range(25):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = f"{first_name.lower()}.{last_name.lower()}.sub{i+1}@example.com"
            
            created_days_ago = random.randint(1, 180)
            created_at = datetime.utcnow() - timedelta(days=created_days_ago)
            
            subscriber = EmailSubscriber(
                email=email,
                name=f"{first_name} {last_name}",
                source=random.choice(sources),
                language=random.choice(languages),
                signup_date=created_at,
                engagement_level=random.choice(engagement_levels),
                is_active=random.choice([True, True, True, False]),  # 75% active
                custom_fields={"interests": random.sample(["leadership", "management", "coaching"], k=random.randint(1, 2))},
                created_at=created_at,
                updated_at=created_at
            )
            
            db.add(subscriber)
        
        print("✅ Created 25 email subscribers")
        
        # Commit all the basic records first
        db.commit()
        print("💾 Committed basic records to database")
        
        # 5. Create Communications (80 entries)
        print("📞 Creating communications...")
        communication_types = ["email", "call", "meeting", "note"]
        
        # Get some records to attach communications to
        waitlist_ids = [w.id for w in db.query(WaitlistRegistration).limit(20).all()]
        corporate_ids = [c.id for c in db.query(CorporateInquiry).limit(15).all()]
        
        communication_subjects = {
            "email": [
                "Follow-up on coaching inquiry",
                "Proposal for leadership development program",
                "Thank you for your interest",
                "Next steps in our coaching process",
                "Scheduling initial consultation"
            ],
            "call": [
                "Discovery call completed",
                "Follow-up call scheduled",
                "Needs assessment discussion",
                "Budget and timeline discussion",
                "Decision maker identified"
            ],
            "meeting": [
                "Initial consultation meeting",
                "Proposal presentation",
                "Contract negotiation meeting",
                "Stakeholder introduction meeting",
                "Program kick-off planning"
            ],
            "note": [
                "Client research completed",
                "Internal team discussion",
                "Pricing strategy notes",
                "Competitor analysis",
                "Follow-up reminder set"
            ]
        }
        
        for i in range(80):
            contact_type = random.choice(["waitlist", "corporate"])
            if contact_type == "waitlist" and waitlist_ids:
                contact_id = random.choice(waitlist_ids)
            elif contact_type == "corporate" and corporate_ids:
                contact_id = random.choice(corporate_ids)
            else:
                continue
            
            comm_type = random.choice(communication_types)
            created_days_ago = random.randint(1, 30)
            sent_at = datetime.utcnow() - timedelta(days=created_days_ago)
            
            subject = random.choice(communication_subjects[comm_type])
            
            content_options = [
                "Discussed client needs and coaching objectives. Very positive response.",
                "Sent detailed proposal with pricing and timeline. Awaiting feedback.",
                "Great conversation about their leadership challenges. High interest level.",
                "Clarified program structure and deliverables. Moving to next stage.",
                "Addressed budget questions and provided flexible payment options.",
                "Introduced our methodology and success stories. Client very engaged.",
                "Scheduled follow-up meeting with decision makers next week.",
                "Received positive feedback on proposal. Minor revisions requested."
            ]
            
            communication = Communication(
                contact_type=contact_type,
                contact_id=contact_id,
                communication_type=comm_type,
                subject=subject,
                content=random.choice(content_options),
                sent_at=sent_at,
                sent_by="admin",
                response_received=random.choice([True, False]),
                response_date=sent_at + timedelta(hours=random.randint(2, 48)) if random.random() < 0.6 else None,
                follow_up_required=random.choice([True, False]),
                created_at=sent_at,
                updated_at=sent_at
            )
            
            db.add(communication)
        
        print("✅ Created 80 communications")
        
        # 6. Create Tasks (50 entries)
        print("📋 Creating tasks...")
        task_types = ["follow_up", "call", "email", "meeting"]
        task_statuses = ["pending", "completed", "overdue"]
        
        task_titles = {
            "follow_up": [
                "Follow up on coaching proposal",
                "Check in on decision timeline",
                "Send additional resources",
                "Schedule next conversation",
                "Confirm meeting attendance"
            ],
            "call": [
                "Discovery call with stakeholder",
                "Budget discussion call",
                "Reference check call",
                "Contract negotiation call",
                "Project kick-off call"
            ],
            "email": [
                "Send welcome email sequence",
                "Share case studies and testimonials",
                "Provide pricing information",
                "Send contract for signature",
                "Share onboarding materials"
            ],
            "meeting": [
                "Initial consultation meeting",
                "Proposal presentation meeting",
                "Stakeholder alignment meeting",
                "Contract signing meeting",
                "Program planning session"
            ]
        }
        
        for i in range(50):
            contact_type = random.choice(["waitlist", "corporate"])
            if contact_type == "waitlist" and waitlist_ids:
                contact_id = random.choice(waitlist_ids)
            elif contact_type == "corporate" and corporate_ids:
                contact_id = random.choice(corporate_ids)
            else:
                continue
            
            task_type = random.choice(task_types)
            status = random.choice(task_statuses)
            priority = random.choice(priorities)
            
            # Create realistic due dates
            if status == "overdue":
                due_date = datetime.utcnow() - timedelta(days=random.randint(1, 10))
            elif status == "completed":
                due_date = datetime.utcnow() - timedelta(days=random.randint(1, 30))
            else:  # pending
                due_date = datetime.utcnow() + timedelta(days=random.randint(1, 14))
            
            created_at = due_date - timedelta(days=random.randint(1, 7))
            
            title = random.choice(task_titles[task_type])
            
            completed_at = None
            completed_by = None
            if status == "completed":
                completed_at = due_date + timedelta(hours=random.randint(-12, 12))
                completed_by = "admin"
            
            task = Task(
                title=title,
                description=f"Important {task_type} task for {contact_type} contact. Requires immediate attention.",
                task_type=task_type,
                contact_type=contact_type,
                contact_id=contact_id,
                assigned_to="admin",
                due_date=due_date,
                status=status,
                priority=priority,
                completed_at=completed_at,
                completed_by=completed_by,
                created_at=created_at,
                updated_at=completed_at or created_at
            )
            
            db.add(task)
        
        print("✅ Created 50 tasks")
        
        # Final commit
        db.commit()
        print("\n🎉 Successfully created comprehensive test data!")
        
        # Print summary
        summary = f"""
        📊 TEST DATA SUMMARY:
        ═══════════════════════════════════════
        📝 Waitlist Registrations: 50
           - Statuses: new, contacted, qualified, converted, not_interested, rejected
           - Priorities: low, medium, high, urgent
           - Lead scores: 15-100 range
           - Follow-up dates and notes included
        
        🏢 Corporate Inquiries: 30  
           - Statuses: new → closed_won/lost pipeline
           - Deal values: €2,000 - €75,000
           - Probabilities: 0-100% based on stage
           - Pipeline and timeline tracking
        
        🧲 Lead Magnet Downloads: 40
           - Multiple downloads per email
           - Realistic date ranges
        
        👥 Email Subscribers: 25
           - Multiple sources and languages
           - Engagement level tracking
        
        📞 Communications: 80
           - Emails, calls, meetings, notes
           - Linked to waitlist and corporate contacts
           - Response tracking included
        
        📋 Tasks: 50
           - Follow-ups, calls, emails, meetings  
           - Pending, completed, and overdue statuses
           - Priority levels and assignments
        
        ✅ Ready for comprehensive testing of:
           • Dashboard analytics and widgets
           • CRUD operations with status management
           • Pipeline tracking and lead scoring
           • Follow-up reminders and task management
           • Communication history and tracking
        """
        
        print(summary)
        return True

if __name__ == "__main__":
    try:
        success = create_test_data()
        if success:
            print("\n🚀 Test data population completed successfully!")
            print("🌐 You can now test all features in the admin dashboard")
        else:
            print("\n❌ Test data population failed")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error during test data population: {str(e)}")
        sys.exit(1)