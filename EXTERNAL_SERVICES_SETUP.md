# 🔗 External Services Setup Guide

This guide walks you through setting up all external services needed for the static site migration.

## 📋 Overview

The static site replaces the backend with these external services:
- **Typeform** → Form collection
- **Google Sheets** → Data storage
- **Zapier** → Automation & notifications
- **SendGrid** → Email automation
- **Cloudflare Pages** → Hosting

---

## 1. 📝 Typeform Setup

### Current Forms (Keep These)
- **Waitlist Form ID**: `C9yyuMrs`
- **Corporate Form ID**: `YRsIpOvV`

### New Lead Magnet Form (Create)

1. **Create New Typeform**:
   - Go to [typeform.com](https://typeform.com)
   - Click "Create a typeform"
   - Choose "Lead generation" template

2. **Form Fields**:
   ```
   Welcome Screen: "Get Your Free Theater Secrets Guide"

   Field 1: What's your first name? (Short text, required)
   Field 2: What's your email address? (Email, required)
   Field 3: What's your biggest communication challenge? (Multiple choice)
   - Speaking up in meetings
   - Presentation anxiety
   - Executive presence
   - Camera confidence
   - Other

   Field 4: What's your role? (Dropdown)
   - Executive/Manager
   - Entrepreneur
   - Sales Professional
   - Consultant
   - Other

   Thank You Screen: "Check your email! Your guide is on the way."
   ```

3. **Get Form ID**:
   - In Typeform admin, go to Share → Embed
   - Copy the form ID from the URL

4. **Update Frontend**:
   - Replace `formId="PZopArKb"` in `pages/index.js` with your new form ID

---

## 2. 📊 Google Sheets Setup

### Create Data Collection Sheets

1. **Create New Google Sheet**: "Coaching Site Leads"

2. **Create 3 Tabs**:
   - **Waitlist** (for waitlist form)
   - **Corporate** (for corporate form)
   - **Lead Magnet** (for new lead magnet form)

3. **Column Headers** (same for all tabs):
   ```
   A: Timestamp
   B: First Name
   C: Email
   D: Challenge/Goals
   E: Role/Company
   F: Additional Info
   G: Source (waitlist/corporate/lead_magnet)
   ```

### Connect Typeform to Google Sheets

1. **In Typeform**:
   - Go to Connect → Google Sheets
   - Authorize Google account
   - Select your "Coaching Site Leads" sheet
   - Map fields to appropriate columns
   - Test the connection

2. **Repeat for all 3 forms**:
   - Map each form to its respective tab
   - Ensure all forms write to the same sheet

---

## 3. ⚡ Zapier Automation Setup

### Zap 1: Immediate Email Notifications

1. **Create New Zap**:
   - Trigger: Google Sheets "New Spreadsheet Row"
   - Select your "Coaching Site Leads" sheet

2. **Action: Send Email**:
   ```
   To: your-email@domain.com
   Subject: New {{Source}} Lead: {{First Name}}
   Body:
   New lead from {{Source}} form:

   Name: {{First Name}}
   Email: {{Email}}
   Challenge: {{Challenge}}
   Role: {{Role}}
   Time: {{Timestamp}}

   View sheet: [link to Google Sheet]
   ```

3. **Test & Activate**

### Zap 2: SendGrid Integration

1. **Create New Zap**:
   - Trigger: Google Sheets "New Spreadsheet Row"
   - Filter: Only when Source = "waitlist" OR "lead_magnet"

2. **Action: SendGrid "Add Contact"**:
   - Add to appropriate list
   - Map first name and email
   - Set custom fields for source tracking

3. **Test & Activate**

---

## 4. 📧 SendGrid Configuration

### Setup Email Lists

1. **Go to SendGrid Dashboard**:
   - Marketing → Contacts → Lists

2. **Create Lists**:
   - "Waitlist Subscribers"
   - "Lead Magnet Downloads"
   - "Corporate Prospects"

### Import Email Templates

1. **Go to Marketing → Email Templates**

2. **Create 5 Templates** using HTML from `/email-templates/`:
   - "01 Welcome Email"
   - "02 Thirty Second Technique"
   - "03 Sarah Transformation"
   - "04 Confidence Builder"
   - "05 Consultation Offer"

3. **Upload HTML**:
   - Copy content from each `.html` file
   - Replace placeholder links with actual URLs
   - Test templates in SendGrid preview

### Setup Automation Workflows

1. **Go to Marketing → Automations**

2. **Create "Waitlist Nurture" Automation**:
   ```
   Trigger: Contact added to "Waitlist Subscribers" list

   Email 1: Welcome Email (immediate)
   Wait: 3 days
   Email 2: Thirty Second Technique
   Wait: 4 days (total 1 week)
   Email 3: Sarah Transformation
   Wait: 1 week (total 2 weeks)
   Email 4: Confidence Builder
   Wait: 1 week (total 3 weeks)
   Email 5: Consultation Offer
   ```

3. **Create "Lead Magnet" Automation**:
   ```
   Trigger: Contact added to "Lead Magnet Downloads" list

   Email 1: Welcome + Download Link (immediate)
   Wait: 2 days
   Email 2: Additional Value
   Wait: 5 days (total 1 week)
   Email 3: Join main nurture sequence
   ```

4. **Test Automations**:
   - Add test email to lists
   - Verify timing and content
   - Check unsubscribe links work

---

## 5. ☁️ Cloudflare Pages Deployment

### Domain Setup

1. **Transfer Domain to Cloudflare**:
   - Go to Cloudflare Dashboard
   - Add site: peter-stoyanov.com
   - Update nameservers at current registrar
   - Wait for DNS propagation (24-48 hours)

### Pages Deployment

1. **Build Static Site**:
   ```bash
   ./build-static.sh
   ```

2. **Upload to Cloudflare Pages**:
   - Go to Cloudflare → Pages
   - Create new project
   - Upload contents of `static-site-deploy` folder
   - Set custom domain to peter-stoyanov.com

3. **Configure Settings**:
   - Build command: `npm run build` (if using Git integration)
   - Output directory: `out`
   - Environment variables: (none needed for static site)

### DNS Configuration

1. **A Records**:
   ```
   @ → 192.0.2.1 (Cloudflare Pages IP)
   www → 192.0.2.1
   ```

2. **CNAME Records**:
   ```
   www → peter-stoyanov.com
   ```

3. **Email Routing** (if needed):
   - Set up email forwarding in Cloudflare
   - Configure MX records for custom email

---

## 6. 🧪 Testing & Validation

### End-to-End Testing

1. **Form Submission Test**:
   - Fill out each form on the live site
   - Verify data appears in Google Sheets
   - Check immediate email notification received
   - Confirm contact added to SendGrid lists

2. **Email Automation Test**:
   - Monitor SendGrid automation triggers
   - Verify email sequence timing
   - Test unsubscribe functionality
   - Check email rendering across clients

3. **Performance Testing**:
   - Test site speed with tools like PageSpeed Insights
   - Verify Cloudflare caching is working
   - Check mobile responsiveness
   - Test PDF download functionality

### Monitoring Setup

1. **Google Analytics** (optional):
   - Add tracking code to site
   - Monitor form conversion rates
   - Track PDF downloads

2. **SendGrid Analytics**:
   - Monitor email open rates
   - Track click-through rates
   - Watch unsubscribe rates

3. **Cloudflare Analytics**:
   - Monitor site traffic
   - Check performance metrics
   - Review security events

---

## 7. 🔧 Maintenance & Updates

### Regular Tasks

1. **Weekly**:
   - Check Google Sheets for new leads
   - Review SendGrid email performance
   - Monitor Cloudflare analytics

2. **Monthly**:
   - Update email templates if needed
   - Review automation performance
   - Check for broken links or issues

3. **Quarterly**:
   - Review and optimize conversion rates
   - Update PDF guides if needed
   - Assess overall system performance

### Backup & Security

1. **Data Backup**:
   - Export Google Sheets regularly
   - Backup SendGrid contact lists
   - Keep local copies of email templates

2. **Security**:
   - Review Cloudflare security settings
   - Monitor for spam in form submissions
   - Keep email lists clean and compliant

---

## 🎯 Success Metrics

Track these KPIs to measure success:

### Conversion Metrics
- Form submission rates
- Email sequence completion rates
- Consultation booking rates
- PDF download completion rates

### Performance Metrics
- Site load speed (target: <2 seconds)
- Email deliverability rates (target: >95%)
- Uptime (target: 99.9%+)

### Cost Comparison
- **Old system**: $60-120/month (server + database)
- **New system**: $26/month (Zapier + Google Workspace)
- **Savings**: ~$400-1000/year

---

## 📞 Support Resources

- **Typeform Support**: help.typeform.com
- **Google Sheets Help**: support.google.com/docs
- **Zapier Help Center**: help.zapier.com
- **SendGrid Support**: support.sendgrid.com
- **Cloudflare Support**: support.cloudflare.com

---

## ✅ Quick Setup Checklist

- [ ] Create lead magnet Typeform
- [ ] Set up Google Sheets with 3 tabs
- [ ] Connect all Typeforms to Google Sheets
- [ ] Create Zapier automations for notifications
- [ ] Upload email templates to SendGrid
- [ ] Set up SendGrid automation workflows
- [ ] Build static site with `./build-static.sh`
- [ ] Deploy to Cloudflare Pages
- [ ] Configure custom domain
- [ ] Test entire flow end-to-end
- [ ] Set up monitoring and analytics

---

**🎉 Once complete, you'll have a high-performance, low-maintenance static site with automated lead capture and email nurturing!**