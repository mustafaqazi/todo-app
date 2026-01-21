# Research & Architectural Decisions: Phase IV Kubernetes Deployment

**Purpose**: Document 7 key architectural decisions with rationale, alternatives, and tradeoff analysis for Phase IV implementation.

**Status**: Foundational Research (T004)

---

## Architecture Decision 1: Local Minikube vs Cloud Kubernetes

### Decision
Use **local Minikube cluster** (docker driver on Windows) instead of cloud Kubernetes (GKE, EKS, AKS).

### Rationale
- **Reproducibility**: Judges can reproduce demo on their machines without cloud account
- **Zero cost**: No cloud credits or billing concerns
- **Simplicity**: Docker driver is lightweight; minimal setup (minikube start)
- **Speed**: Local cluster faster than cloud for iteration
- **Hackathon context**: Perfect for demo purposes

### Alternatives Considered
1. **Cloud Kubernetes (GKE/EKS/AKS)**: Better for production; harder to reproduce locally; involves costs; judge friction
2. **Docker Compose**: Simpler; lacks Kubernetes abstractions (no pod orchestration, no liveness probes, no Helm)
3. **Kind (Kubernetes in Docker)**: Similar to Minikube; both viable; Minikube more user-friendly

### Tradeoffs
- **Pros**: Local, zero cost, reproducible, simple
- **Cons**: Not production-like; Minikube has resource limits (4 CPUs, 8GB RAM); no persistent storage by default

### Impact
- All Phase IV specs assume Minikube
- Documentation must highlight local-only scope
- Production deployment would use cloud provider (out of scope per spec)

---

## Architecture Decision 2: Multi-Stage Docker Builds vs Single-Stage

### Decision
**Multi-stage builds** for both frontend (Node → nginx) and backend (Python + UV → uvicorn).

### Rationale
- **Image size optimization**: Build stage includes dev dependencies; final stage only runtime deps
- **Frontend target <200MB**: Node build artifacts removed from final image
- **Backend target <400MB**: Pip/UV cache not included in final image
- **Build cache efficiency**: Changes in app code don't invalidate dependency layers
- **Security**: Final image smaller surface area for vulnerabilities

### Alternatives Considered
1. **Single-stage build**: Simpler Dockerfiles; larger images (500MB+); includes build tools in production
2. **Distroless base images**: Smallest possible images; requires manual dependency management; harder to debug
3. **Pre-built images from Docker Hub**: Easier; less control; potential security gaps

### Tradeoffs
- **Pros**: Optimized image size, build efficiency, security
- **Cons**: Slightly more complex Dockerfile syntax; requires understanding multi-stage pattern

### Impact
- Frontend Dockerfile: Node 20-alpine build stage → nginx:alpine final stage
- Backend Dockerfile: Python 3.12-slim + UV build stage → slim final stage
- Image size targets: <200MB (frontend), <400MB (backend)

---

## Architecture Decision 3: Helm Charts vs Raw Kubernetes YAML

### Decision
**Helm charts** for templating and deployment (todo-frontend, todo-backend charts).

### Rationale
- **Parameterization**: values.yaml drives all configuration (image, replicas, resources)
- **Reusability**: Same chart deployable to different namespaces, environments, with different values
- **Standards**: Helm is Kubernetes package manager standard
- **Traceability**: values.yaml shows all configurable parameters in one place
- **Judge perspective**: Helm install command is cleaner than kubectl apply multiple files

### Alternatives Considered
1. **Raw YAML manifests**: Simpler for one-off deployments; harder to parameterize; copy-paste error-prone
2. **Kustomize**: Lightweight; good for variations; less mature than Helm
3. **Manual kubectl commands**: Ad-hoc; not reproducible; no version control

### Tradeoffs
- **Pros**: Reusable, parameterizable, industry standard, clean deployment
- **Cons**: Extra layer of indirection; requires Helm knowledge; adds templates/values.yaml files

### Impact
- Two Helm charts: `k8s/helm-charts/todo-frontend/` and `k8s/helm-charts/todo-backend/`
- Each chart includes: Chart.yaml, values.yaml, templates/(deployment.yaml, service.yaml, _helpers.tpl)
- Deployment: `helm install todo-frontend k8s/helm-charts/todo-frontend`

---

## Architecture Decision 4: Kubernetes Secrets vs ConfigMaps for Sensitive Data

### Decision
**Kubernetes Secrets** for all sensitive environment variables (DATABASE_URL, BETTER_AUTH_SECRET, COHERE_API_KEY).

### Rationale
- **Security intent**: Secrets signal "sensitive data" to Kubernetes RBAC and audit systems
- **Encryption ready**: Secrets can be encrypted at rest (etcd encryption plugin)
- **Separation of concerns**: Non-sensitive config (image tags, replicas) in ConfigMaps; secrets elsewhere
- **Constitution requirement**: Constitution explicitly forbids hardcoded secrets
- **Deployment safety**: Secrets created out-of-band (kubectl create secret), never committed

### Alternatives Considered
1. **ConfigMaps**: Works technically; semantically wrong; signals "not sensitive"
2. **Hardcoded in values.yaml**: Violates security principle; judge red flag
3. **Environment file in image**: Violates security principle; image is not secure
4. **External secret store (Vault, AWS Secrets Manager)**: Over-engineered for local Minikube

### Tradeoffs
- **Pros**: Secure, standards-compliant, audit-friendly
- **Cons**: Extra step (kubectl create secret) before helm install; not baked into image

### Impact
- Minikube deployment: `kubectl create secret generic app-secrets --from-literal=...` before helm install
- Helm templates reference `secretRef: name: app-secrets`
- Documentation must emphasize secret creation is prerequisite
- k8s/secrets/app-secrets-template.yaml documents structure (never commit real values)

---

## Architecture Decision 5: Non-Root Container User (UID 1000) vs Root

### Decision
**Non-root user (UID 1000, appuser)** for both frontend and backend containers.

### Rationale
- **Security best practice**: Root inside container can become root on host (container escape)
- **Constitution requirement**: Constitution explicitly requires non-root
- **Judge validation**: Security engineer story (US2) explicitly checks for non-root
- **Minimal overhead**: Simple Dockerfile directive: `USER appuser`, `RUN useradd -u 1000 appuser`
- **Compliance**: Kubernetes Pod Security Standards recommend non-root

### Alternatives Considered
1. **Root user (UID 0)**: Simpler Dockerfile; massive security risk; violates constitution
2. **Custom numeric UID**: Works; less readable than named user

### Tradeoffs
- **Pros**: Secure, standards-compliant, required by constitution
- **Cons**: Minimal; must ensure file permissions set before USER directive

### Impact
- Dockerfile for both services: Add `RUN useradd -u 1000 appuser` and `USER appuser`
- Validation task (US2) confirms: `docker run <image> id` shows UID 1000
- Helm deployment verification: `kubectl exec <pod> id` shows UID 1000

---

## Architecture Decision 6: ImagePullPolicy = Never vs IfNotPresent

### Decision
**ImagePullPolicy = Never** for Minikube local deployment (use `minikube image load`).

### Rationale
- **Local-first**: Images built locally, loaded into Minikube; no registry needed
- **Offline capability**: Works without Docker registry or internet (after image load)
- **Speed**: Minikube image load is instant; registry pull would be slower
- **Judge experience**: Zero friction; images already in Minikube; no registry setup needed

### Alternatives Considered
1. **ImagePullPolicy = IfNotPresent**: Checks Minikube first, then pulls from registry if missing; adds latency
2. **Push to Docker Hub**: Requires credentials, internet, registry account
3. **Local Docker registry in Minikube**: Extra complexity; requires registry setup

### Tradeoffs
- **Pros**: Simple, offline-capable, fast
- **Cons**: Requires pre-loading images; wouldn't work for cloud deployment (production uses registry pull)

### Impact
- Deployment steps: Build images → `minikube image load` → Helm install with `--set image.pullPolicy=Never`
- Documentation must emphasize: Images must be loaded before deployment
- Production deployment would use `IfNotPresent` or `Always` with registry

---

## Architecture Decision 7: Health Checks (Readiness + Liveness Probes) vs No Probes

### Decision
**Both readiness and liveness probes** for all deployments.

### Rationale
- **Readiness probe**: Ensures traffic only sent to healthy pods; prevents 503 errors during startup
- **Liveness probe**: Restarts pods that become unresponsive; automatically recovers from crashes
- **Judge validation**: Spec explicitly requires health checks; acceptance criteria verify pod Ready state
- **Best practice**: Kubernetes best practice for production-ready deployments
- **User story validation**: US1 (MVP) requires pods to reach Running + Ready within 60s

### Alternatives Considered
1. **No probes**: Pods marked Running immediately; may receive traffic before app ready; no restart on hang
2. **Readiness only**: Prevents traffic to unready pods; no auto-recovery from crashes
3. **Liveness only**: Auto-recovers from crashes; may send traffic to pods still starting up

### Tradeoffs
- **Pros**: Robust, self-healing, production-ready
- **Cons**: Requires app to expose health endpoint (/health or similar); adds deployment complexity

### Impact
- Helm templates: `readinessProbe` (HTTP GET /health, 10s timeout) and `livenessProbe` (same, 30s timeout)
- Backend must expose `/health` endpoint (typically already done in FastAPI)
- Frontend must expose /health (nginx can serve static file or use script)
- Minikube deployment: `kubectl wait --for=condition=ready pod` validates probes working

---

## Summary Table

| Decision | Choice | Key Benefit | Tradeoff |
|----------|--------|------------|----------|
| 1. Cluster | Minikube (local) | Reproducible, zero cost | Not production-like |
| 2. Docker | Multi-stage builds | Optimized images <200/400MB | Slightly more complex |
| 3. Packaging | Helm charts | Reusable, parameterizable | Extra configuration layer |
| 4. Secrets | Kubernetes Secrets | Secure, standards-compliant | Separate creation step |
| 5. User | Non-root UID 1000 | Security best practice | Minimal overhead |
| 6. Image Pull | Never (local load) | Fast, offline-capable | Requires pre-loading |
| 7. Health | Readiness + Liveness | Robust, self-healing | Requires /health endpoint |

---

## References

- Feature Spec: `/specs/5-k8s-deployment/spec.md`
- Implementation Plan: `/specs/5-k8s-deployment/plan.md`
- Constitution: `.specify/memory/constitution.md` (Principle XII: Cloud-Native Containerization)
