#!/bin/bash

# Email Automation System - Docker Deployment Script

set -e

echo "🚀 Starting Email Automation System Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from template...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}📝 Please edit .env file with your configuration before continuing.${NC}"
    echo -e "${YELLOW}   Required: MAILERLITE_API_KEY, MAILERLITE_WEBHOOK_SECRET${NC}"
    read -p "Press Enter to continue after editing .env file..."
fi

# Load environment variables
source .env

# Check required environment variables
if [ -z "$MAILERLITE_API_KEY" ] || [ "$MAILERLITE_API_KEY" = "your_mailerlite_api_key_here" ]; then
    echo -e "${RED}❌ MAILERLITE_API_KEY is not set in .env file${NC}"
    exit 1
fi

# Create necessary directories
echo -e "${GREEN}📁 Creating necessary directories...${NC}"
mkdir -p backups
mkdir -p backend/data
mkdir -p backend/logs

# Set permissions
echo -e "${GREEN}🔐 Setting permissions...${NC}"
chmod 755 backups
chmod 755 backend/data
chmod 755 backend/logs

# Build and start services
echo -e "${GREEN}🏗️  Building and starting services...${NC}"

# Parse command line arguments
PROFILE=""
if [ "$1" = "--production" ]; then
    PROFILE="--profile production"
    echo -e "${GREEN}🏭 Running in production mode...${NC}"
fi

# Stop existing services
echo -e "${YELLOW}🛑 Stopping existing services...${NC}"
docker-compose down

# Build images
echo -e "${GREEN}🔨 Building Docker images...${NC}"
docker-compose build

# Start services
echo -e "${GREEN}🚀 Starting services...${NC}"
docker-compose up -d $PROFILE

# Wait for services to start
echo -e "${GREEN}⏳ Waiting for services to start...${NC}"
sleep 10

# Check service health
echo -e "${GREEN}🏥 Checking service health...${NC}"

# Check backend health
if curl -f http://localhost:8000/ &> /dev/null; then
    echo -e "${GREEN}✅ Backend is healthy${NC}"
else
    echo -e "${RED}❌ Backend health check failed${NC}"
    docker-compose logs backend
    exit 1
fi

# Check frontend health
if curl -f http://localhost:3000/ &> /dev/null; then
    echo -e "${GREEN}✅ Frontend is healthy${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend might still be starting...${NC}"
fi

# Check scheduler
if docker-compose ps email_scheduler | grep -q "Up"; then
    echo -e "${GREEN}✅ Email scheduler is running${NC}"
else
    echo -e "${RED}❌ Email scheduler is not running${NC}"
    docker-compose logs email_scheduler
fi

# Display service status
echo -e "\n${GREEN}📊 Service Status:${NC}"
docker-compose ps

# Display access URLs
echo -e "\n${GREEN}🌐 Access URLs:${NC}"
echo -e "  Frontend: http://localhost:3000"
echo -e "  Backend API: http://localhost:8000"
echo -e "  Admin Dashboard: http://localhost:8000/admin"
echo -e "  API Documentation: http://localhost:8000/docs"

# Display admin credentials
echo -e "\n${GREEN}🔑 Admin Credentials:${NC}"
echo -e "  Username: ${ADMIN_USERNAME:-admin}"
echo -e "  Password: ${ADMIN_PASSWORD:-admin123}"

# Display next steps
echo -e "\n${GREEN}🎯 Next Steps:${NC}"
echo -e "  1. Access admin dashboard and verify email sequences"
echo -e "  2. Configure MailerLite webhooks (see WEBHOOK_SETUP.md)"
echo -e "  3. Test email workflow (see TESTING_GUIDE.md)"
echo -e "  4. Start email scheduler in admin dashboard"

# Test system functionality
echo -e "\n${GREEN}🧪 Running basic system tests...${NC}"

# Test registration endpoint
echo -e "${YELLOW}Testing registration endpoint...${NC}"
TEST_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "http://localhost:8000/api/register" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test User",
    "email": "test@example.com",
    "city_country": "Test City",
    "occupation": "Developer",
    "why_join": "Testing",
    "skills_to_improve": "Testing skills"
  }')

if [ "$TEST_RESPONSE" = "200" ]; then
    echo -e "${GREEN}✅ Registration endpoint is working${NC}"
else
    echo -e "${YELLOW}⚠️  Registration endpoint returned: $TEST_RESPONSE${NC}"
fi

# Test admin login
echo -e "${YELLOW}Testing admin authentication...${NC}"
ADMIN_TOKEN=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=${ADMIN_USERNAME:-admin}&password=${ADMIN_PASSWORD:-admin123}" \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)

if [ ! -z "$ADMIN_TOKEN" ]; then
    echo -e "${GREEN}✅ Admin authentication is working${NC}"
else
    echo -e "${YELLOW}⚠️  Admin authentication test failed${NC}"
fi

echo -e "\n${GREEN}✨ Deployment completed successfully!${NC}"
echo -e "${GREEN}🎉 Your email automation system is now running!${NC}"

# Optional: Open browser
if command -v open &> /dev/null; then
    read -p "Open admin dashboard in browser? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open http://localhost:8000/admin
    fi
fi