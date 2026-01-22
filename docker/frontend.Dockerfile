# Multi-stage Dockerfile for Next.js 16+ Frontend
# Generated via spec-driven development (T015)
# Based on docker-gordon.md best practices

# ============================================================================
# BUILD STAGE: Compile Next.js application
# ============================================================================
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependency files from frontend directory
COPY frontend/package*.json ./
COPY frontend/yarn.lock* frontend/pnpm-lock.yaml* ./

# Install dependencies
# Use npm install to ensure all dependencies are resolved
RUN npm install --legacy-peer-deps

# Copy application code from frontend directory
COPY frontend/ .

# Build Next.js application
# This generates .next directory with optimized artifacts
RUN npm run build

# ============================================================================
# RUNTIME STAGE: Serve compiled application with nginx
# ============================================================================
FROM nginx:alpine

# Security: Create non-root user (UID 1000)
# Required by Kubernetes Pod Security Standards and constitution
RUN addgroup -g 1000 appuser && adduser -D -u 1000 -G appuser appuser

WORKDIR /app

# Copy compiled Next.js artifacts from builder stage
COPY --from=builder /app/.next /usr/share/nginx/html/.next
COPY --from=builder /app/public /usr/share/nginx/html/public
COPY --from=builder /app/node_modules /usr/share/nginx/html/node_modules

# Copy nginx configuration (serve Next.js with SPA routing)
# This config ensures all routes are served by Next.js (SPA)
COPY <<'EOF' /etc/nginx/nginx.conf
worker_processes auto;
error_log /tmp/nginx_error.log warn;
pid /tmp/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Use /tmp for cache directories (writable by non-root)
    client_body_temp_path /tmp/client_temp;
    proxy_temp_path /tmp/proxy_temp;
    fastcgi_temp_path /tmp/fastcgi_temp;
    uwsgi_temp_path /tmp/uwsgi_temp;
    scgi_temp_path /tmp/scgi_temp;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /tmp/nginx_access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 20M;

    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript
               application/json application/javascript application/xml+rss
               application/rss+xml application/atom+xml image/svg+xml
               text/x-js text/x-component text/x-cross-domain-policy;

    server {
        listen 80;
        server_name _;

        root /usr/share/nginx/html;
        index index.html;

        # Health check endpoint (required for Kubernetes probes)
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }

        # SPA routing: serve index.html for all routes (Next.js handles routing)
        location / {
            try_files $uri $uri/ /index.html;
        }

        # Static assets: cache aggressively
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
            add_header Pragma "public";
        }

        # Deny access to hidden files
        location ~ /\. {
            deny all;
            access_log off;
            log_not_found off;
        }
    }
}
EOF

# Set permissions for nginx html directory (required for non-root user)
# Using /tmp for all writable directories (pid, logs, cache) so no extra setup needed
RUN chown -R appuser:appuser /usr/share/nginx/html

# Copy application files with correct ownership
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port 80 (HTTP)
EXPOSE 80

# Health check for Kubernetes
# Interval: 30s, Timeout: 3s, Retries: 3
# Ready if GET /health returns 200
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/health || exit 1

# Start nginx in foreground mode (required for Docker containers)
CMD ["nginx", "-g", "daemon off;"]

# ============================================================================
# Image Metadata
# ============================================================================
LABEL org.opencontainers.image.title="Todo Frontend"
LABEL org.opencontainers.image.description="Next.js 16+ frontend for Todo AI Chatbot"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.vendor="Todo Project"
