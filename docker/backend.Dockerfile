# Multi-stage Dockerfile for FastAPI Backend
# Generated via spec-driven development (T016)
# Based on docker-gordon.md best practices

# ============================================================================
# BUILD STAGE: Install dependencies with UV package manager
# ============================================================================
FROM python:3.12-slim AS builder

WORKDIR /tmp

# Install UV package manager (fast Python dependency resolution)
RUN pip install --no-cache-dir uv

# Copy dependency files from backend directory
COPY backend/requirements.txt ./

# Install dependencies from requirements.txt
# This step can be cached separately from application code
RUN pip install --no-cache-dir -r requirements.txt

# ============================================================================
# RUNTIME STAGE: Minimal FastAPI runtime
# ============================================================================
FROM python:3.12-slim

# Security: Create non-root user (UID 1000)
# Required by Kubernetes Pod Security Standards and constitution
RUN groupadd -g 1000 appuser && useradd -u 1000 -g appuser -s /usr/sbin/nologin appuser

WORKDIR /app

# Copy installed dependencies from builder stage
# This keeps the final image minimal (no build tools)
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code from backend directory
# Place after dependencies to leverage cache (code changes more often)
COPY --chown=appuser:appuser backend/ .

# Set Python environment variables
# PYTHONUNBUFFERED: print logs immediately (important for Docker)
# PYTHONDONTWRITEBYTECODE: don't create __pycache__ directories
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/usr/local/bin:$PATH"

# Switch to non-root user
USER appuser

# Expose port 8000 (FastAPI default)
EXPOSE 8000

# Health check for Kubernetes
# Interval: 30s, Timeout: 3s, Retries: 3
# Ready if GET /health returns 200
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Start FastAPI with uvicorn
# 0.0.0.0: Listen on all interfaces (required for Kubernetes)
# --port 8000: Standard HTTP port
# --timeout-keep-alive 5: Shorter keepalive for Minikube
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# ============================================================================
# Image Metadata
# ============================================================================
LABEL org.opencontainers.image.title="Todo Backend"
LABEL org.opencontainers.image.description="FastAPI backend for Todo AI Chatbot with Cohere integration"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.vendor="Todo Project"
