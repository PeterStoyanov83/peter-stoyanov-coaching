# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Static Site Development
```bash
cd coaching-site/frontend
npm install        # Install dependencies
npm run dev        # Development server (localhost:3000)
npm run build      # Static export build
npm run static     # Build and serve locally
npm run lint       # ESLint checks
```

### Static Site Deployment
```bash
./build-static.sh  # Build complete static site for deployment
./test-static.sh   # Test static site locally on port 5000
./log_progress.sh  # Log development progress
```

## Architecture Overview

This is a high-performance static coaching website with external service integrations:

### Core Components
- **Frontend**: Next.js static export with TailwindCSS and next-i18next
- **Forms**: Typeform integration for data collection
- **Data Storage**: Google Sheets via Typeform
- **Notifications**: Zapier automation for immediate alerts
- **Email Automation**: SendGrid with professional HTML templates
- **Hosting**: Cloudflare Pages with global CDN

### Key Services
1. **Lead Collection**: Typeform → Google Sheets → Zapier → Email notifications
2. **Email Nurturing**: 5-email automated sequence via SendGrid
3. **Lead Magnet**: PDF download with email capture
4. **Performance**: Cloudflare CDN for sub-second load times

### Form Collection Points
- **Waitlist Form** (`C9yyuMrs`): Main coaching program signup
- **Corporate Form** (`YRsIpOvV`): Business training inquiries
- **Lead Magnet Form**: PDF guide download with email capture

### Email Automation Sequences
- **Waitlist Nurture**: 5 emails (immediate, 3 days, 1 week, 2 weeks, 3 weeks)
- **Lead Magnet**: 6 emails with immediate PDF delivery
- **Corporate**: Immediate notification for manual follow-up

## Project Structure

```
coaching-site/
├── frontend/
│   ├── pages/               # Next.js pages (static export)
│   ├── components/          # React components
│   │   ├── TypeformModal.js # Existing forms
│   │   └── LeadMagnetModal.js # New lead magnet form
│   ├── public/
│   │   └── guides/          # PDF downloads
│   └── public/locales/      # Translation files (bg/en)
├── email-templates/         # HTML email templates for SendGrid
│   ├── 01-welcome-email.html
│   ├── 02-thirty-second-technique.html
│   ├── 03-sarah-transformation.html
│   ├── 04-confidence-builder-exercise.html
│   └── 05-consultation-offer.html
├── static-site-deploy/      # Generated deployment files
├── build-static.sh          # Build script for Cloudflare Pages
├── test-static.sh           # Local testing script
└── EXTERNAL_SERVICES_SETUP.md # Complete setup guide
```

## External Services Configuration

### Required Services
- **Typeform**: Form collection and data capture
- **Google Sheets**: Data storage and organization
- **Zapier**: Automation and immediate notifications
- **SendGrid**: Email automation and template management
- **Cloudflare Pages**: Static hosting with CDN

### Setup Documentation
- Complete setup guide: `EXTERNAL_SERVICES_SETUP.md`
- Email templates ready for SendGrid import
- Form IDs and integration points documented

## Development Workflow

### Local Development
1. `cd coaching-site/frontend && npm run dev` - Development server
2. `./test-static.sh` - Test static build locally
3. `./build-static.sh` - Generate deployment files
4. `./log_progress.sh "your progress notes"` - Log session progress

### Deployment Process
1. Run `./build-static.sh` to generate `static-site-deploy/`
2. Upload contents to Cloudflare Pages
3. Configure custom domain and DNS
4. Test external service integrations

## Key Features

### Performance Optimizations
- Static files served via Cloudflare CDN
- Optimized images and assets
- Security headers and caching rules
- Sub-second global load times

### Lead Generation
- Professional PDF guide: "The Complete Theater Secrets Guide"
- Multi-step email nurturing sequences
- Automatic notifications for new leads
- Segmented lists for different lead sources

### Internationalization
- Bulgarian and English language support
- Maintained from original full-stack version
- Static export preserves i18n functionality

## Migration Notes

This site was migrated from a full-stack FastAPI + Next.js application to a static site with external services. Benefits include:

- **Performance**: 50%+ faster load times
- **Reliability**: 99.9%+ uptime with Cloudflare
- **Cost**: 70%+ reduction in hosting costs
- **Maintenance**: Minimal technical maintenance required
- **Scalability**: Automatic scaling for traffic spikes

The migration maintains all original functionality while significantly improving performance and reducing complexity.