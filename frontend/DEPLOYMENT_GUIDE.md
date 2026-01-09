# Deployment Guide - Premium TODO Frontend

## Overview

This guide covers deploying the premium Next.js 14+ TODO frontend to production environments (Vercel, self-hosted, or Docker).

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Configuration](#environment-configuration)
3. [Build & Deployment](#build--deployment)
4. [Post-Deployment Verification](#post-deployment-verification)
5. [Troubleshooting](#troubleshooting)
6. [Performance Optimization](#performance-optimization)

---

## Prerequisites

### Development Environment
- Node.js 18+ (check with `node --version`)
- npm 9+ or yarn/pnpm (check with `npm --version`)
- Git for version control

### Deployment Requirements
- **Vercel Account** (for Vercel deployment) or
- **Docker** (for containerized deployment) or
- **Linux server** with Node.js (for self-hosted)
- **Backend API** deployed and accessible (typically `https://api.youromain.com`)
- **SSL Certificate** (HTTPS required for production)

### Backend Dependencies
The frontend requires a working backend API with the following endpoints:

```
POST /auth/signup          - User account creation
POST /auth/login           - User authentication
GET  /api/tasks            - Fetch user's tasks
POST /api/tasks            - Create new task
PUT  /api/tasks/{id}       - Update task
PATCH /api/tasks/{id}      - Update task status
DELETE /api/tasks/{id}     - Delete task
```

All requests must include `Authorization: Bearer <JWT_TOKEN>` header.

---

## Environment Configuration

### 1. Local Development

Create `/frontend/.env.local`:

```env
# API Configuration (local backend)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Optional: Enable debug logging
NEXT_PUBLIC_DEBUG_MODE=false

# App configuration
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

Start development:
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000`

### 2. Staging Environment

Create `/frontend/.env.staging.local`:

```env
# API Configuration (staging backend)
NEXT_PUBLIC_API_URL=https://api.staging.yourdomain.com

# Enable some debugging
NEXT_PUBLIC_DEBUG_MODE=true

# App configuration
NEXT_PUBLIC_APP_URL=https://staging.yourdomain.com
```

### 3. Production Environment

Create `/frontend/.env.production.local`:

```env
# API Configuration (production backend) - MUST USE HTTPS
NEXT_PUBLIC_API_URL=https://api.yourdomain.com

# Disable debug logging
NEXT_PUBLIC_DEBUG_MODE=false

# App configuration
NEXT_PUBLIC_APP_URL=https://yourdomain.com
```

### Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | ✅ | Backend API base URL | `https://api.yourdomain.com` |
| `NEXT_PUBLIC_APP_URL` | ⚠️ | Frontend URL (for redirects) | `https://yourdomain.com` |
| `NEXT_PUBLIC_DEBUG_MODE` | ❌ | Enable console logging | `false` |

**Important**:
- Prefix with `NEXT_PUBLIC_` to expose to client
- Never commit `.env.local` files (use `.env.example`)
- Use HTTPS URLs in production
- Regenerate secrets/keys for production

---

## Build & Deployment

### Option 1: Vercel (Recommended for Next.js)

#### Setup

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Link Project**:
   ```bash
   cd frontend
   vercel link
   ```

#### Deploy to Production

```bash
# Deploy to production
vercel --prod

# Or use Git integration:
# Push to main branch → Vercel auto-deploys
```

#### Configure Environment Variables in Vercel Dashboard

1. Go to Project Settings → Environment Variables
2. Add variables for each environment:
   - **Production**: `NEXT_PUBLIC_API_URL=https://api.yourdomain.com`
   - **Preview**: `NEXT_PUBLIC_API_URL=https://api.staging.yourdomain.com`
   - **Development**: `NEXT_PUBLIC_API_URL=http://localhost:8000`

3. Save and redeploy

#### Vercel Project Configuration (Optional)

Create `vercel.json` in `/frontend`:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "env": {
    "NEXT_PUBLIC_API_URL": "@next_public_api_url"
  },
  "functions": {
    "api/**/*.ts": {
      "memory": 512,
      "maxDuration": 30
    }
  },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        }
      ]
    }
  ]
}
```

---

### Option 2: Docker (Self-Hosted)

#### Create Dockerfile

Create `/frontend/Dockerfile`:

```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --legacy-peer-deps

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

# Copy from builder
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/public ./public

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000', (r) => {if (r.statusCode !== 200) throw new Error(r.statusCode)})"

# Start application
ENTRYPOINT ["dumb-init", "--"]
CMD ["npm", "start"]
```

#### Create docker-compose.yml

Create `/frontend/docker-compose.yml`:

```yaml
version: '3.8'

services:
  frontend:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=https://api.yourdomain.com
      - NEXT_PUBLIC_APP_URL=https://yourdomain.com
      - NODE_ENV=production
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Optional: nginx reverse proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
    depends_on:
      - frontend
    restart: unless-stopped
```

#### Deploy with Docker

```bash
# Build image
docker build -t todo-frontend:latest .

# Run container
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=https://api.yourdomain.com \
  -e NEXT_PUBLIC_APP_URL=https://yourdomain.com \
  --restart unless-stopped \
  todo-frontend:latest

# Or use docker-compose
docker-compose up -d
```

---

### Option 3: Linux Server (PM2)

#### Installation

1. **SSH into server**:
   ```bash
   ssh user@server.ip
   ```

2. **Install Node.js** (if not installed):
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```

3. **Install PM2 globally**:
   ```bash
   sudo npm install -g pm2
   ```

#### Deploy Application

1. **Clone repository**:
   ```bash
   cd /var/www
   git clone <repository-url> todo-frontend
   cd todo-frontend/frontend
   ```

2. **Install dependencies**:
   ```bash
   npm ci --legacy-peer-deps
   ```

3. **Create `.env.production.local`**:
   ```bash
   cat > .env.production.local << 'EOF'
   NEXT_PUBLIC_API_URL=https://api.yourdomain.com
   NEXT_PUBLIC_APP_URL=https://yourdomain.com
   NEXT_PUBLIC_DEBUG_MODE=false
   EOF
   ```

4. **Build application**:
   ```bash
   npm run build
   ```

5. **Create PM2 Ecosystem Config** (`ecosystem.config.js`):

   ```javascript
   module.exports = {
     apps: [
       {
         name: 'todo-frontend',
         script: 'npm',
         args: 'start',
         env: {
           NODE_ENV: 'production',
           PORT: 3000,
         },
         instances: 'max',
         exec_mode: 'cluster',
         watch: false,
         ignore_watch: ['node_modules', '.next'],
         error_file: './logs/pm2-error.log',
         out_file: './logs/pm2-out.log',
         log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
       },
     ],
   };
   ```

6. **Start with PM2**:
   ```bash
   pm2 start ecosystem.config.js
   pm2 save
   sudo pm2 startup
   ```

7. **Setup Nginx Reverse Proxy**:

   Create `/etc/nginx/sites-available/todo`:

   ```nginx
   upstream todo_frontend {
     server localhost:3000;
   }

   server {
     listen 80;
     server_name yourdomain.com;
     return 301 https://$server_name$request_uri;
   }

   server {
     listen 443 ssl http2;
     server_name yourdomain.com;

     ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
     ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

     ssl_protocols TLSv1.2 TLSv1.3;
     ssl_ciphers HIGH:!aNULL:!MD5;
     ssl_prefer_server_ciphers on;

     client_max_body_size 10M;

     location / {
       proxy_pass http://todo_frontend;
       proxy_http_version 1.1;
       proxy_set_header Upgrade $http_upgrade;
       proxy_set_header Connection 'upgrade';
       proxy_set_header Host $host;
       proxy_cache_bypass $http_upgrade;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_set_header X-Forwarded-Proto $scheme;
     }
   }
   ```

8. **Enable Nginx config**:
   ```bash
   sudo ln -s /etc/nginx/sites-available/todo /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

---

## Post-Deployment Verification

### 1. Health Check

```bash
# Visit frontend
curl -I https://yourdomain.com
# Should return 200 OK

# Check API connectivity
curl -X GET https://yourdomain.com/api/health
# Or test login
curl -X POST https://yourdomain.com/login
```

### 2. Browser Testing

- [ ] Load homepage (http://yourdomain.com)
- [ ] Signup/login flow works
- [ ] Create, edit, delete tasks
- [ ] Theme toggle works
- [ ] Mobile responsive (test on iPhone)
- [ ] Dark mode renders correctly
- [ ] All animations smooth

### 3. Performance Check

```bash
# Lighthouse audit
# Open DevTools → Lighthouse → Generate report
# Target: >95 on mobile

# Check bundle size
# DevTools → Network → JS files
# Target: <500KB gzipped

# Check Core Web Vitals
# Google PageSpeed Insights
# LCP <2.5s, CLS <0.1, FID <100ms
```

### 4. Security Check

- [ ] HTTPS enabled (check padlock)
- [ ] No console errors (F12 → Console)
- [ ] No XSS vulnerabilities
- [ ] CORS headers correct (if applicable)
- [ ] No secrets in client code (check Network tab)

---

## Troubleshooting

### Build Fails: Dependency Conflicts

**Error**: `npm ERR! peer dep missing`

**Solution**:
```bash
npm ci --legacy-peer-deps
```

### Application Won't Start

**Check logs**:
```bash
# Vercel
vercel logs frontend.vercel.app

# PM2
pm2 logs todo-frontend

# Docker
docker logs <container-id>
```

### API Connection Fails

**Check environment variables**:
```bash
# Vercel Dashboard → Settings → Environment Variables
# Should show: NEXT_PUBLIC_API_URL=https://api.yourdomain.com

# Docker
docker exec <container> env | grep NEXT_PUBLIC_API_URL

# Local
echo $NEXT_PUBLIC_API_URL
```

### Dark Mode Doesn't Work

**Fix**: Ensure `dark` class is applied to `<html>` element
```bash
# Check in DevTools
# <html class="dark" ...>
```

### Authentication Fails (401 Errors)

1. **Check backend is running**: `curl https://api.yourdomain.com/health`
2. **Verify CORS headers**: Browser Console → Network → Response Headers
3. **Check token storage**: DevTools → Application → LocalStorage → `todo_auth_token`
4. **Verify API endpoint**: Check `lib/api.ts` has correct URL

### Performance Issues

1. **Run Lighthouse audit** (DevTools → Lighthouse)
2. **Check bundle size**: `npm run build` → analyze `.next/static`
3. **Enable compression**: Nginx/server should gzip responses
4. **Optimize images**: Use Next.js Image component

---

## Performance Optimization

### 1. Enable Compression

**Nginx**:
```nginx
gzip on;
gzip_types text/plain text/css text/javascript application/json;
gzip_min_length 1000;
```

**Vercel**: Automatic

### 2. Enable Caching

**Nginx**:
```nginx
# Cache static files 1 week
location ~* \.(?:jpg|jpeg|gif|png|ico|css|js|svg)$ {
  expires 1w;
  add_header Cache-Control "public, immutable";
}
```

### 3. CDN Configuration

Use Cloudflare or similar for:
- Global CDN distribution
- DDoS protection
- Automatic compression
- Cache purging

### 4. Database Optimization

If using Next.js API routes (not applicable here, backend is separate):
- Implement connection pooling
- Add caching headers (`Cache-Control`, `ETag`)

---

## Monitoring & Maintenance

### Uptime Monitoring

Use services like:
- Pingdom
- Uptime Robot
- New Relic
- DataDog

### Error Tracking

Setup Sentry for error monitoring:

```bash
npm install @sentry/nextjs
```

Initialize in `app/layout.tsx`:
```typescript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0,
});
```

### Log Aggregation

- **Vercel**: Built-in logging
- **Self-hosted**: Use ELK stack or Loki
- **Docker**: Use centralized logging (e.g., splunk)

### Regular Updates

```bash
# Check for outdated packages
npm outdated

# Update packages
npm update

# Update major versions (carefully)
npm upgrade
```

---

## Rollback Procedure

### Vercel
```bash
# Go to Deployments → select previous → redeploy
# Or use CLI
vercel rollback
```

### Docker
```bash
# Revert to previous image
docker run -p 3000:3000 todo-frontend:previous-tag

# Or keep multiple versions tagged
docker images
```

### PM2
```bash
# View running version
pm2 show todo-frontend

# Revert codebase
git checkout <previous-commit>

# Rebuild and restart
npm run build
pm2 restart todo-frontend
```

---

## Support & Help

- **Documentation**: See `/frontend/README.md`
- **Issues**: Check logs in Vercel/PM2/Docker
- **Backend**: Verify backend API is running and accessible
- **Frontend**: Open DevTools (F12) → Console for errors

---

**Last Updated**: January 3, 2026
**Status**: Production-Ready
**Next**: Monitor deployment and gather metrics
