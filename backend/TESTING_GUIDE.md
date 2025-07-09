# Email Automation System - Testing Guide

This guide covers comprehensive testing of the automated email workflow system.

## Overview

The email automation system includes:
- ✅ Automated subscriber enrollment
- ✅ Email sequence scheduling
- ✅ Webhook analytics tracking
- ✅ Engagement level calculation
- ✅ Retry logic for failed emails
- ✅ Subscriber segmentation
- ✅ Admin dashboard management

## Testing Methods

### 1. Automated Test Suite

**Run via API:**
```bash
# Login to admin dashboard first to get auth token
curl -X POST "http://localhost:8000/admin/test/email-workflow" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

**Run via Command Line:**
```bash
cd backend
python test_email_workflow.py
```

This runs 10 comprehensive tests:
1. **Subscriber Creation** - Creates test subscribers
2. **Sequence Creation** - Verifies email sequences exist
3. **Auto Enrollment** - Tests automatic enrollment on signup
4. **Email Scheduling** - Validates emails are scheduled correctly
5. **Email Sending** - Simulates email delivery
6. **Webhook Processing** - Tests webhook event handling
7. **Engagement Tracking** - Verifies engagement level updates
8. **Retry Logic** - Tests failed email retry mechanism
9. **Sequence Completion** - Tests sequence completion tracking
10. **Analytics Calculation** - Validates analytics computation

### 2. Manual Registration Testing

**Test Waitlist Registration:**
```bash
curl -X POST "http://localhost:8000/api/register" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "email": "john@example.com",
    "city_country": "Sofia, Bulgaria",
    "occupation": "Developer",
    "why_join": "Learn leadership skills",
    "skills_to_improve": "Communication and team management"
  }'
```

**Test Corporate Inquiry:**
```bash
curl -X POST "http://localhost:8000/api/corporate-inquiry" \
  -H "Content-Type: application/json" \
  -d '{
    "companyName": "Tech Corp",
    "contactPerson": "Jane Smith",
    "email": "jane@techcorp.com",
    "phone": "+359888123456",
    "teamSize": "10-20",
    "budget": "5000-10000",
    "trainingGoals": "Leadership development for managers",
    "preferredDates": "Next month",
    "additionalInfo": "Remote training preferred"
  }'
```

**Test Lead Magnet Download:**
```bash
curl -X POST "http://localhost:8000/api/lead-magnet/download" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "subscriber@example.com"
  }'
```

### 3. Webhook Testing

**Test Webhook Events:**
```bash
# Test email opened event
curl -X POST "http://localhost:8000/webhooks/mailerlite/test?event_type=opened" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"

# Test email clicked event
curl -X POST "http://localhost:8000/webhooks/mailerlite/test?event_type=clicked" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"

# Test email bounced event
curl -X POST "http://localhost:8000/webhooks/mailerlite/test?event_type=bounced" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"

# Test unsubscribe event
curl -X POST "http://localhost:8000/webhooks/mailerlite/test?event_type=unsubscribed" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

### 4. System Status Monitoring

**Get System Health:**
```bash
curl -X GET "http://localhost:8000/admin/test/system-status" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

Expected response:
```json
{
  "status": "healthy",
  "health_score": 100,
  "scheduler_running": true,
  "recent_24h": {
    "new_subscribers": 5,
    "emails_sent": 12,
    "emails_failed": 0
  },
  "pending_emails": 3,
  "timestamp": "2024-01-15T10:30:00"
}
```

## Testing Scenarios

### Scenario 1: Complete User Journey

1. **User registers** → System creates subscriber
2. **Auto-enrollment** → User enrolled in appropriate sequence
3. **Email scheduling** → Emails scheduled based on sequence timing
4. **Scheduler processes** → Emails sent to MailerLite
5. **Webhook events** → Analytics updated in real-time
6. **Engagement tracking** → User engagement level calculated

### Scenario 2: Multilingual Support

1. **Bulgarian user registers** → Enrolled in Bulgarian sequence
2. **English user registers** → Enrolled in English sequence
3. **Verify language consistency** → All emails in correct language

### Scenario 3: Error Handling

1. **Email fails to send** → Marked as failed
2. **Retry logic activates** → Email rescheduled with backoff
3. **Permanent failure** → Email marked as permanently failed
4. **Analytics updated** → Failure rates calculated

### Scenario 4: High Volume Testing

1. **Multiple registrations** → System handles concurrent signups
2. **Bulk enrollment** → Large number of subscribers processed
3. **Scheduler performance** → Emails processed efficiently
4. **Database performance** → Queries remain fast

## Verification Steps

After running tests, verify:

### 1. Database State
```sql
-- Check subscribers were created
SELECT COUNT(*) FROM email_subscribers;

-- Check enrollments were created
SELECT COUNT(*) FROM sequence_enrollments;

-- Check emails were scheduled
SELECT COUNT(*) FROM scheduled_emails;

-- Check analytics were recorded
SELECT COUNT(*) FROM email_analytics;
```

### 2. Admin Dashboard
1. Login to `http://localhost:8000/admin`
2. Navigate to **Email Sequences** → **Sequence Analytics**
3. Verify metrics are populated
4. Check **Real-time Webhook Analytics**

### 3. Scheduler Status
1. Check scheduler is running: **Email Sequences** → **Scheduler Controls**
2. Verify email processing logs
3. Monitor failed emails section

## Performance Benchmarks

### Expected Performance:
- **Registration → Enrollment**: < 1 second
- **Email scheduling**: < 500ms per enrollment
- **Webhook processing**: < 200ms per event
- **Analytics calculation**: < 2 seconds
- **Bulk operations**: 1000+ subscribers/minute

### Memory Usage:
- **Baseline**: ~50MB
- **With 1000 subscribers**: ~100MB
- **With 10000 subscribers**: ~200MB

### Database Performance:
- **Subscriber queries**: < 100ms
- **Analytics queries**: < 500ms
- **Bulk operations**: < 5 seconds for 1000 records

## Troubleshooting

### Common Issues:

**1. Tests Failing:**
```bash
# Check database connection
python -c "from database import get_db; print('DB OK')"

# Check imports
python -c "from models import EmailSubscriber; print('Models OK')"

# Check scheduler
python -c "from email_scheduler import EmailScheduler; print('Scheduler OK')"
```

**2. No Emails Scheduled:**
- Verify sequences exist in database
- Check enrollment status is 'active'
- Confirm sequence_automation.py is working

**3. Webhook Events Not Processing:**
- Check webhook_handlers.py imports
- Verify database connections
- Check for error logs

**4. Analytics Not Updating:**
- Verify EmailAnalytics table exists
- Check webhook event processing
- Confirm analytics calculation logic

## Success Criteria

### System is ready for production when:
✅ **All automated tests pass** (>95% success rate)
✅ **Manual registration flows work** (all 3 types)
✅ **Emails are scheduled correctly** (proper timing)
✅ **Webhook events process** (analytics update)
✅ **Retry logic functions** (failed emails retry)
✅ **System health is good** (status endpoint returns healthy)
✅ **Admin dashboard loads** (all sections functional)
✅ **Performance meets benchmarks** (response times acceptable)

## Next Steps

After successful testing:
1. **Configure MailerLite API** (real API keys)
2. **Set up webhook endpoints** (production URLs)
3. **Configure monitoring** (logs, alerts)
4. **Deploy to production** (with proper SSL)
5. **Set up backup procedures** (database backup)

## Support

For issues during testing:
- Check application logs
- Review database state
- Verify configuration settings
- Run system status check
- Review webhook processing logs