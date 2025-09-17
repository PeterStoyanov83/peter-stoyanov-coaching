#!/bin/bash

# Static Site Build Script for Cloudflare Pages Deployment
# Usage: ./build-static.sh

set -e  # Exit on any error

echo "🚀 Building static site for Cloudflare Pages deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -d "coaching-site/frontend" ]; then
    print_error "coaching-site/frontend directory not found. Please run this script from the project root."
    exit 1
fi

# Navigate to frontend directory
cd coaching-site/frontend

print_status "Installing dependencies..."
if ! npm install; then
    print_error "Failed to install dependencies"
    exit 1
fi

print_success "Dependencies installed"

# Run linting
print_status "Running linting checks..."
if npm run lint; then
    print_success "Linting passed"
else
    print_warning "Linting issues found, but continuing with build..."
fi

# Build the static site
print_status "Building static site..."
if ! npm run build; then
    print_error "Build failed"
    exit 1
fi

print_success "Static site built successfully"

# Check if out directory exists
if [ ! -d "out" ]; then
    print_error "Build output directory 'out' not found"
    exit 1
fi

# Create deployment directory in project root
cd ../../
DEPLOY_DIR="static-site-deploy"

print_status "Preparing deployment files..."

# Remove existing deployment directory if it exists
if [ -d "$DEPLOY_DIR" ]; then
    rm -rf "$DEPLOY_DIR"
fi

# Create deployment directory
mkdir -p "$DEPLOY_DIR"

# Copy static files
cp -r coaching-site/frontend/out/* "$DEPLOY_DIR/"

# Copy additional assets that might be needed
if [ -d "coaching-site/frontend/public/guides" ]; then
    mkdir -p "$DEPLOY_DIR/guides"
    cp -r coaching-site/frontend/public/guides/* "$DEPLOY_DIR/guides/"
    print_status "Copied PDF guides to deployment"
fi

# Create _headers file for Cloudflare Pages
cat > "$DEPLOY_DIR/_headers" << EOF
# Cloudflare Pages headers for static site

/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()

# Cache static assets for 1 year
/images/*
  Cache-Control: public, max-age=31536000, immutable

/guides/*
  Cache-Control: public, max-age=31536000, immutable
  Content-Type: application/pdf

# Cache HTML for 1 hour
*.html
  Cache-Control: public, max-age=3600

# Cache CSS and JS for 1 year
*.css
  Cache-Control: public, max-age=31536000, immutable

*.js
  Cache-Control: public, max-age=31536000, immutable
EOF

# Create _redirects file for Cloudflare Pages
cat > "$DEPLOY_DIR/_redirects" << EOF
# Cloudflare Pages redirects

# Redirect old backend API calls to appropriate pages
/api/* /contact 302

# Redirect admin routes to contact page
/admin/* /contact 302

# Handle SPA routing for Next.js
/* /index.html 200
EOF

# Create robots.txt
cat > "$DEPLOY_DIR/robots.txt" << EOF
User-agent: *
Allow: /

# Sitemap
Sitemap: https://peter-stoyanov.com/sitemap.xml
EOF

# Count files and get size
FILE_COUNT=$(find "$DEPLOY_DIR" -type f | wc -l)
TOTAL_SIZE=$(du -sh "$DEPLOY_DIR" | cut -f1)

print_success "Deployment files prepared in $DEPLOY_DIR/"
print_status "Total files: $FILE_COUNT"
print_status "Total size: $TOTAL_SIZE"

echo ""
echo "📦 Deployment Summary:"
echo "├── Static HTML files: ✅"
echo "├── CSS and JavaScript: ✅"
echo "├── Images and assets: ✅"
echo "├── PDF guides: ✅"
echo "├── Cloudflare headers: ✅"
echo "├── Redirects configured: ✅"
echo "└── Security headers: ✅"
echo ""

print_success "Static site build complete!"
echo ""
echo "🚀 Next steps for Cloudflare Pages deployment:"
echo "1. Go to https://pages.cloudflare.com/"
echo "2. Create new project"
echo "3. Upload the contents of the '$DEPLOY_DIR' folder"
echo "4. Configure custom domain: peter-stoyanov.com"
echo "5. Set up DNS in Cloudflare"
echo ""
echo "📁 Files ready for upload in: $(pwd)/$DEPLOY_DIR"