# 📧 Email Automation & Follow-ups Guide

This guide shows you how to set up automated email sequences and follow-ups for your coaching site using MailerLite.

## 🎯 Email Automation Strategy

### Lead Magnet Funnel Sequence
```
Download PDF → Welcome Email → Value Email → Social Proof → Soft Pitch → Hard Pitch → Nurture
```

## 🚀 MailerLite Automation Setup

### 1. Create Subscriber Groups

**In MailerLite Dashboard:**
1. Go to **Subscribers** → **Groups**
2. Create these groups:
   - `Lead Magnet - Theater Secrets` (for PDF downloaders)
   - `Waitlist - Coaching Program` (for course waitlist)
   - `Corporate Prospects` (for corporate inquiries)

### 2. Set Up Automation Workflows

**Go to MailerLite → Automations → Create New**

#### 📥 Lead Magnet Welcome Series

**Trigger:** Subscriber joins "Lead Magnet - Theater Secrets" group

**Email Sequence:**

1. **Email 1: Immediate Welcome** (Send immediately)
   - Subject: "Your Theater Secrets Guide is Here! 🎭"
   - Content: PDF download link + personal welcome

2. **Email 2: Value Bomb** (Wait 2 days)
   - Subject: "The #1 mistake that kills stage presence"
   - Content: Additional tips + personal story

3. **Email 3: Social Proof** (Wait 3 days)
   - Subject: "How Maria transformed her presentations in 30 days"
   - Content: Student success story + testimonial

4. **Email 4: Soft Introduction** (Wait 4 days)
   - Subject: "What I learned from 20 years on stage"
   - Content: Your background + upcoming program hint

5. **Email 5: Program Announcement** (Wait 5 days)
   - Subject: "Ready to master confident communication?"
   - Content: Coaching program introduction + early bird offer

6. **Email 6: Final Call** (Wait 7 days)
   - Subject: "Last chance for early access"
   - Content: Urgency + final CTA

### 3. Advanced Segmentation

**Custom Fields to Track:**
- `lead_source` (lead_magnet, waitlist, corporate)
- `engagement_level` (high, medium, low)
- `purchase_intent` (hot, warm, cold)
- `communication_goals` (public_speaking, leadership, etc.)

## 🛠️ Technical Implementation

Let me create an enhanced backend system for automation triggers:
