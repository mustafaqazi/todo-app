# Docker Multi-Stage Build Specification: Gordon AI Patterns

**Purpose**: Document Gordon AI usage for generating optimized multi-stage Dockerfiles.

**Status**: To be completed during Phase 2 (Foundational) & Phase 3 (User Story 1)

---

## Placeholder: Gordon AI Dockerfile Generation

This specification will document:
1. Multi-stage build patterns (build stage → final stage)
2. Layer caching optimization strategies
3. Security best practices (non-root user, minimal base images)
4. Image size targets: frontend <200MB, backend <400MB
5. Example Gordon AI prompts used for generation
6. Build time optimization (expected 1-2 minutes per image)

**To be filled in during T007, T011, T012, T055, T089-T092 (Foundational & User Story 1/3 implementation)**

---

## Key Optimization Goals

- **Frontend (Next.js 16+)**:
  - Base: Node 20-alpine for build, nginx:alpine for serving
  - Target size: <200MB
  - Multi-stage: Remove node_modules, build artifacts from final image
  - Health check: `/health` endpoint or static file verification

- **Backend (FastAPI)**:
  - Base: Python 3.12-slim for build, uvicorn for production
  - Target size: <400MB
  - Multi-stage: Leverage UV package manager for fast dependency resolution
  - Health check: `/health` endpoint returning 200 OK

---

## Multi-Stage Build Best Practices (T007: Research)

### Docker Layer Caching Strategy

1. **Dependency Layer Separation**: Place `package.json` COPY and install before code COPY
   - Reasoning: Dependencies change rarely; code changes frequently
   - Benefit: Reuse dependency layer across code iterations
   - Example: If only app code changes, npm/pip install layer cache is hit

2. **Multi-Stage Pattern**:
   ```
   Stage 1 (builder): Install build dependencies, compile assets
   Stage 2 (runtime): Copy only compiled artifacts, minimal runtime deps
   ```
   - Benefit: Final image excludes build tools, reducing size significantly
   - Example: Next.js build artifacts (.next/) copied; node_modules removed

3. **Base Image Selection**:
   - **Frontend**: `node:20-alpine` (build) → `nginx:alpine` (final)
     - Alpine: 30-40% smaller than full Debian
     - nginx: lightweight web server, high performance
   - **Backend**: `python:3.12-slim` (build) → `slim` (final)
     - slim: smaller than full Python image, includes essential build tools
     - Avoid `python:3.12-alpine` (missing glibc compatibility issues with some packages)

4. **Minimize Layers**:
   - Combine RUN commands with `&&` to reduce layers (e.g., `apt-get update && apt-get install`)
   - Each RUN creates a new layer; fewer layers = smaller image

5. **Security Scanning**:
   - Scan final image for vulnerabilities: `trivy image todo-frontend:latest`
   - Alpine and slim images have fewer CVEs than full images

### Image Size Targets

- **Frontend**: <200MB (Next.js + nginx + node_modules removed)
- **Backend**: <400MB (FastAPI + Python + dependencies)
- **Reasoning**: Smaller images = faster downloads, faster Minikube load, faster CI/CD

### Non-Root User Pattern

```dockerfile
# Best practice: Create user early, use throughout
RUN addgroup -g 1000 appuser && adduser -D -u 1000 -G appuser appuser
COPY --chown=appuser:appuser . /app
USER appuser
```

- Reasoning: Container escape risk mitigated; Kubernetes Pod Security Standards require non-root
- Benefit: Security-first design; judges validate this (US2)

---

## Gordon AI Usage Patterns (T009: Research & Documentation)

### Example Prompt 1: Frontend Dockerfile

```
Generate a production-ready multi-stage Dockerfile for a Next.js 16+ application:

Specifications:
- Build stage: node:20-alpine with npm install and npm run build
- Runtime stage: nginx:alpine serving compiled .next and public directories
- Non-root user: UID 1000 (appuser), created in runtime stage
- Target image size: <200MB
- Health check: nginx serving /health static file (30s interval, 3s timeout)
- Port: 80 (HTTP)
- Optimization: Minimize layers, cache dependency installs separately

Output should:
- Use multi-stage pattern to exclude build artifacts from final image
- Separate COPY package*.json from COPY . to leverage Docker layer cache
- Include security best practices (non-root, minimal base image)
- Include HEALTHCHECK directive
- Use .dockerignore patterns
```

**Expected Output Pattern**:
- BUILD stage: ~150MB (includes node_modules, build tools)
- FINAL stage: ~180MB (only runtime, compiled assets, nginx)

### Example Prompt 2: Backend Dockerfile

```
Generate a production-ready multi-stage Dockerfile for a FastAPI application:

Specifications:
- Build stage: python:3.12-slim with UV package manager
- Runtime stage: python:3.12-slim (slim, not alpine)
- Non-root user: UID 1000 (appuser), created in runtime stage
- Target image size: <400MB
- Health check: curl http://localhost:8000/health (30s interval, 3s timeout)
- Port: 8000 (HTTP/API)
- Entrypoint: uvicorn with 0.0.0.0:8000
- Optimization: Fast dependency resolution via UV, exclude dev dependencies

Output should:
- Use multi-stage pattern with UV in build stage for fast resolution
- Separate COPY pyproject.toml/uv.lock from COPY . to leverage cache
- Include security best practices (non-root, minimal base image)
- Include HEALTHCHECK directive
- Use .dockerignore patterns
- Set CMD to start uvicorn server
```

**Expected Output Pattern**:
- BUILD stage: ~600MB (includes build tools)
- FINAL stage: ~380MB (only runtime libraries, app code)

### Gordon AI Capabilities for T007-T009

Gordon AI will assist with:
- ✅ Generating initial multi-stage Dockerfile structure
- ✅ Optimizing layer ordering for cache efficiency
- ✅ Suggesting Alpine vs slim trade-offs
- ✅ Non-root user implementation patterns
- ✅ Health check endpoint implementation
- ✅ .dockerignore best practices
- ✅ Build time optimization recommendations

---

## References

- Feature Spec: `/specs/5-k8s-deployment/spec.md`
- Implementation Plan: `/specs/5-k8s-deployment/plan.md`
- Helm Charts: `/specs/infra/helm-charts.md`
- AI DevOps Tools: `/specs/infra/ai-devops.md`
