# Email Templates for SendGrid Automation

This folder contains professionally styled HTML email templates for the 5-email nurturing sequence.

## Email Sequence Overview

### 1. Welcome Email (`01-welcome-email.html`)
- **Subject:** Welcome to the journey - Your speaking confidence starts here
- **Timing:** Immediate (upon waitlist signup)
- **Purpose:** Welcome, set expectations, introduce Peter's background
- **Design:** Blue gradient theme, confidence-focused messaging

### 2. Value Email #1 (`02-thirty-second-technique.html`)
- **Subject:** The 30-second technique that transforms speaking anxiety
- **Timing:** 3 days after signup
- **Purpose:** Provide actionable technique (Stand and State)
- **Design:** Green/teal theme, step-by-step instructions, theater story

### 3. Value Email #2 (`03-sarah-transformation.html`)
- **Subject:** How Sarah went from silent in meetings to leading presentations
- **Timing:** 1 week after signup
- **Purpose:** Social proof through detailed case study
- **Design:** Red/orange theme, transformation story, client results

### 4. Value Email #3 (`04-confidence-builder-exercise.html`)
- **Subject:** Try this 5-minute confidence builder (works anywhere)
- **Timing:** 2 weeks after signup
- **Purpose:** Practical exercise they can do immediately
- **Design:** Purple theme, step-by-step choreography exercise

### 5. Soft Pitch (`05-consultation-offer.html`)
- **Subject:** Ready to unlock your confident speaker? Let's talk.
- **Timing:** 3 weeks after signup
- **Purpose:** Consultation offer, transition to sales conversation
- **Design:** Professional dark theme with gold accents, clear CTA

## Design Features

All templates include:
- **Mobile-responsive design** with media queries
- **Consistent branding** with gradient headers and Peter's coaching theme
- **Professional typography** using system fonts for maximum compatibility
- **Clear call-to-actions** where appropriate
- **Unsubscribe links** and compliance footer
- **Personalization placeholders** ({{first_name}}, {{unsubscribe_url}}, etc.)

## SendGrid Integration

To use these templates in SendGrid:
1. Copy the HTML content from each file
2. Create new email templates in SendGrid
3. Set up automation workflows with proper timing
4. Configure personalization variables
5. Test templates across different email clients

## Variable Placeholders

Each template uses these SendGrid merge tags:
- `{{first_name}}` - Subscriber's first name
- `{{unsubscribe_url}}` - SendGrid unsubscribe link
- `{{preferences_url}}` - SendGrid preference center link

## Color Themes by Email

1. **Welcome:** Blue gradients (#475569, #1e40af, #3730a3)
2. **Technique:** Green/teal (#059669, #0891b2, #3730a3)
3. **Case Study:** Red/orange (#dc2626, #ea580c, #d97706)
4. **Exercise:** Purple (#7c3aed, #c026d3, #e11d48)
5. **Consultation:** Dark professional (#0f172a, #1e293b, #334155)

Each email maintains Peter's professional coaching brand while having its own visual identity to keep the sequence engaging.

## Testing Recommendations

Before deploying:
1. Test in multiple email clients (Gmail, Outlook, Apple Mail)
2. Check mobile responsiveness
3. Verify all links work correctly
4. Test personalization variables
5. Review spam score and deliverability