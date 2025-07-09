# MailerLite Webhook Integration Setup

This document explains how to configure MailerLite webhooks to track email analytics in real-time.

## Overview

The webhook integration allows the system to receive real-time notifications from MailerLite when subscribers:
- Open emails
- Click links in emails  
- Unsubscribe
- Have emails bounce
- Complete conversion goals

## Webhook Endpoints

The system provides these webhook endpoints:

- **Main webhook**: `POST /webhooks/mailerlite`
- **Verification**: `GET /webhooks/mailerlite/verify`
- **Analytics**: `GET /admin/webhook-analytics`

## MailerLite Configuration

### 1. Set Webhook Secret (Recommended)

Set an environment variable for webhook security:

```bash
export MAILERLITE_WEBHOOK_SECRET="your-secret-key-here"
```

### 2. Configure Webhooks in MailerLite Dashboard

1. Log into your MailerLite account
2. Go to **Integrations** → **Developer API** → **Webhooks**
3. Click **Add webhook**
4. Configure the following:

**Webhook URL**: `https://your-domain.com/webhooks/mailerlite`

**Events to subscribe to**:
- ✅ `subscriber.opened` - When subscriber opens an email
- ✅ `subscriber.clicked` - When subscriber clicks a link
- ✅ `subscriber.bounced` - When email bounces
- ✅ `subscriber.unsubscribed` - When subscriber unsubscribes  
- ✅ `subscriber.complained` - When subscriber marks as spam
- ✅ `conversion` - When conversion goal is met (optional)

**Secret**: Enter the same secret you set in the environment variable

### 3. Test Webhook Setup

1. Verify the endpoint is accessible:
   ```bash
   curl https://your-domain.com/webhooks/mailerlite/verify
   ```

2. Send a test webhook from MailerLite dashboard

3. Check the webhook analytics in the admin dashboard under **Sequence Analytics** → **Real-time Webhook Analytics**

## Supported Events

### Email Opened (`subscriber.opened`)
- Updates `EmailAnalytics.opened_at` 
- Increments `EmailAnalytics.open_count`

### Email Clicked (`subscriber.clicked`)  
- Updates `EmailAnalytics.clicked_at`
- Increments `EmailAnalytics.click_count`

### Email Bounced (`subscriber.bounced`)
- Updates `EmailAnalytics.bounced_at`
- If hard bounce, deactivates subscriber

### Subscriber Unsubscribed (`subscriber.unsubscribed`)
- Updates `EmailAnalytics.unsubscribed_at`
- Deactivates subscriber in the system

### Conversion Event (`conversion`)
- Updates `EmailAnalytics.converted_at`
- Tracks goal completions

## Security

The webhook handler includes signature verification using HMAC-SHA256:

1. MailerLite signs each webhook with your secret key
2. The system verifies the signature using the same key
3. Invalid signatures are rejected with 401 status

## Troubleshooting

### Webhook Not Receiving Events

1. **Check URL accessibility**: Ensure `https://your-domain.com/webhooks/mailerlite` is publicly accessible
2. **Verify SSL certificate**: MailerLite requires valid HTTPS
3. **Check logs**: Look for errors in application logs
4. **Test manually**: Send test webhook from MailerLite dashboard

### Signature Verification Failing

1. **Check secret key**: Ensure `MAILERLITE_WEBHOOK_SECRET` environment variable is set correctly
2. **Match secrets**: The secret in MailerLite must match your environment variable exactly
3. **Check headers**: Verify `X-MailerLite-Signature` header is being received

### Analytics Not Updating

1. **Check campaign mapping**: Ensure scheduled emails have `mailerlite_campaign_id` set
2. **Database connections**: Verify webhook handler can connect to database
3. **Error logs**: Check for processing errors in application logs

## Testing

### Manual Webhook Testing

You can test webhook processing manually:

```bash
curl -X POST https://your-domain.com/webhooks/mailerlite \
  -H "Content-Type: application/json" \
  -H "X-MailerLite-Signature: sha256=your-test-signature" \
  -d '{
    "type": "subscriber.opened",
    "data": {
      "subscriber": {"email": "test@example.com"},
      "campaign": {"id": "123456"}
    }
  }'
```

### Analytics Verification

Check webhook analytics through the admin dashboard:

1. Log into admin dashboard
2. Go to **Sequence Analytics** 
3. View **Real-time Webhook Analytics** section
4. Verify metrics are updating correctly

## Environment Variables

Required environment variables:

```bash
# Webhook security (recommended)
MAILERLITE_WEBHOOK_SECRET=your-secret-key-here

# Database URL (if different from default)
DATABASE_URL=sqlite:///./coaching_site.db
```

## Rate Limiting

The webhook endpoint has no built-in rate limiting. If you expect high volume:

1. Consider implementing rate limiting middleware
2. Use a queue system for webhook processing
3. Monitor webhook processing performance

## Monitoring

Monitor webhook health using:

1. **Webhook Analytics Dashboard**: Real-time metrics in admin interface
2. **Application Logs**: Error tracking and debugging
3. **MailerLite Logs**: Check delivery status in MailerLite dashboard
4. **Database Monitoring**: Track analytics table growth and performance