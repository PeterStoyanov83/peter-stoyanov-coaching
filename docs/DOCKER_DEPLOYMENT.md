# Docker Deployment Guide

This guide covers deploying the email automation system using Docker and Docker Compose.

## Prerequisites

- Docker installed (version 20.10+)
- Docker Compose installed (version 2.0+)
- Your MailerLite API key and webhook secret

## Quick Start

### 1. Clone and Setup

```bash
# Navigate to project directory
cd coaching-site

# Copy environment file
cp .env.example .env

# Edit environment variables
nano .env
```

### 2. Configure Environment Variables

Edit `.env` file with your settings:

```bash
# MailerLite Configuration
MAILERLITE_API_KEY=your_actual_mailerlite_api_key
MAILERLITE_WEBHOOK_SECRET=your_webhook_secret

# Admin Authentication
JWT_SECRET_KEY=your_super_secret_jwt_key_here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password

# Frontend Configuration
NEXT_PUBLIC_SITE_URL=https://your-domain.com
NEXT_PUBLIC_API_URL=https://your-domain.com
```

### 3. Build and Run

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

### 4. Access Services

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Admin Dashboard**: http://localhost:8000/admin

## Services Overview

### Backend API (`coaching_backend`)
- **Purpose**: Main FastAPI application with email automation
- **Port**: 8000
- **Health Check**: Available at `/` endpoint
- **Features**:
  - Email sequence management
  - Automated subscriber enrollment
  - Webhook handling
  - Admin dashboard

### Frontend (`coaching_frontend`)
- **Purpose**: Next.js frontend application
- **Port**: 3000
- **Dependencies**: Backend API

### Email Scheduler (`coaching_scheduler`)
- **Purpose**: Background service for processing scheduled emails
- **Features**:
  - Processes emails every 5 minutes
  - Handles retry logic
  - Manages failed emails
- **No exposed ports** (internal service)

### Database Backup (`coaching_backup`)
- **Purpose**: Automated database backups
- **Schedule**: Every hour
- **Retention**: 7 days
- **Profile**: Production only

## Production Deployment

### 1. Production Environment

```bash
# Create production environment file
cp .env.example .env.production

# Edit with production values
nano .env.production
```

### 2. Production Configuration

```bash
# Production environment variables
MAILERLITE_API_KEY=your_production_api_key
MAILERLITE_WEBHOOK_SECRET=your_production_webhook_secret
JWT_SECRET_KEY=your_super_secure_production_key
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_very_secure_password
NEXT_PUBLIC_SITE_URL=https://your-domain.com
NEXT_PUBLIC_API_URL=https://your-domain.com
DATABASE_URL=sqlite:///./data/coaching_site.db
```

### 3. Run with Production Profile

```bash
# Start with backup service
docker-compose --profile production up -d

# Or with specific environment file
docker-compose --env-file .env.production up -d
```

## SSL/HTTPS Setup

For production, you'll need SSL certificates. Here's a basic Nginx configuration:

### 1. Create Nginx Configuration

```bash
mkdir -p nginx
```

Create `nginx/nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:3000;
    }

    server {
        listen 80;
        server_name your-domain.com;
        
        # Redirect to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Backend API
        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Admin Dashboard
        location /admin {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Webhooks
        location /webhooks/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

### 2. Add SSL Certificates

```bash
# Place your SSL certificates in
mkdir -p nginx/ssl
# Add cert.pem and key.pem to nginx/ssl/
```

### 3. Update Docker Compose for SSL

Add to `docker-compose.yml`:

```yaml
  nginx:
    image: nginx:alpine
    container_name: coaching_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped
    networks:
      - coaching-network
    profiles:
      - production
```

## Monitoring and Maintenance

### 1. View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f email_scheduler

# Last 100 lines
docker-compose logs --tail=100 backend
```

### 2. Health Checks

```bash
# Check service health
docker-compose ps

# Backend health
curl http://localhost:8000/admin/test/system-status

# Check email scheduler
docker-compose exec email_scheduler ps aux
```

### 3. Database Management

```bash
# Access database
docker-compose exec backend sqlite3 /app/data/coaching_site.db

# Backup database
docker-compose exec backend cp /app/data/coaching_site.db /app/backups/manual_backup.db

# Restore database
docker-compose exec backend cp /app/backups/backup_file.db /app/data/coaching_site.db
```

### 4. Scaling

```bash
# Scale specific services
docker-compose up -d --scale backend=2
docker-compose up -d --scale email_scheduler=2

# Update and restart
docker-compose build backend
docker-compose up -d backend
```

## Troubleshooting

### Common Issues

**1. Permission Errors**
```bash
# Fix volume permissions
sudo chown -R 1000:1000 backend/data
sudo chown -R 1000:1000 backend/logs
```

**2. Database Issues**
```bash
# Reset database
docker-compose down
docker volume rm coaching-site_backend_data
docker-compose up -d
```

**3. Email Scheduler Not Working**
```bash
# Check scheduler logs
docker-compose logs email_scheduler

# Restart scheduler
docker-compose restart email_scheduler
```

**4. Frontend Not Loading**
```bash
# Check frontend logs
docker-compose logs frontend

# Rebuild frontend
docker-compose build frontend
docker-compose up -d frontend
```

### Service URLs

- **Health Check**: `http://localhost:8000/`
- **System Status**: `http://localhost:8000/admin/test/system-status`
- **Test Webhook**: `http://localhost:8000/webhooks/mailerlite/verify`
- **Run Tests**: `http://localhost:8000/admin/test/email-workflow`

## Security Best Practices

### 1. Environment Variables
- Never commit `.env` files
- Use strong, unique passwords
- Rotate secrets regularly
- Use environment-specific configurations

### 2. Network Security
- Use Docker networks for service isolation
- Restrict port exposure
- Implement reverse proxy with SSL
- Use firewalls for additional protection

### 3. Data Protection
- Regular database backups
- Encrypt sensitive data
- Monitor access logs
- Implement proper authentication

### 4. Updates
- Keep Docker images updated
- Monitor for security vulnerabilities
- Test updates in staging first
- Have rollback procedures

## Performance Optimization

### 1. Resource Limits

Add to `docker-compose.yml`:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

### 2. Caching

```bash
# Add Redis for caching
  redis:
    image: redis:alpine
    container_name: coaching_redis
    restart: unless-stopped
    networks:
      - coaching-network
```

### 3. Load Balancing

```bash
# Scale backend services
docker-compose up -d --scale backend=3
```

## Backup Strategy

### 1. Database Backups
- Automated hourly backups (included in docker-compose)
- Manual backups before updates
- Off-site backup storage

### 2. File Backups
- Application code versioning
- Configuration file backups
- SSL certificate backups

### 3. Recovery Procedures
- Documented recovery steps
- Regular recovery testing
- Backup validation

This deployment setup provides a complete, production-ready email automation system with monitoring, backups, and security best practices.