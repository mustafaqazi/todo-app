# Implementation Plan: Phase IV – Complete Local Kubernetes Deployment

**Branch**: `5-k8s-deployment` | **Date**: 2026-01-20 | **Spec**: [specs/5-k8s-deployment/spec.md](./spec.md)

**Input**: Feature specification from `/specs/5-k8s-deployment/spec.md`

---

## Summary

Deploy the fully integrated Phase II (multi-user TODO web app) + Phase III (Cohere-powered AI Chatbot) on a local Kubernetes cluster using Minikube, Docker multi-stage builds, Helm charts, and AI-assisted DevOps tools (Gordon for Dockerfiles, kubectl-ai/Kagent for manifests and charts). The plan emphasizes reproducible, secure, single-iteration demo readiness with zero code rewrites – only containerization and orchestration layers added. Success requires orchestrating 7 phases: Containerization (Dockerfiles + Gordon), Minikube Setup, Secrets & Config, Helm Chart Generation (kubectl-ai/Kagent), Deployment, Verification & Debugging, and Polish & Demo.

---

## Technical Context

**Docker & Containerization**:
- Containerization Tool: Docker Desktop with multi-stage builds
- Frontend Image: Node.js 20-alpine (build stage) → nginx:alpine (final stage)
- Backend Image: Python 3.12-slim (build stage) → uvicorn/gunicorn (final stage)
- Image Registry: Local Minikube Docker daemon (loaded via `minikube image load`)
- Health Checks: HEALTHCHECK instruction in Dockerfile + readiness/liveness probes in Kubernetes manifests
- Non-root User: UID 1000 in both Dockerfiles for security compliance
- Image Size Targets: Frontend < 200MB, Backend < 400MB

**Kubernetes & Orchestration**:
- Local Cluster: Minikube with docker driver (preferred for Windows)
- Helm Version: 3.x
- Chart Structure: Separate helm charts for todo-frontend and todo-backend (modularity + independence)
- Deployment Model: Kubernetes Deployments with rolling updates, replicas=1–2, readiness/liveness probes
- Service Types: ClusterIP for backend (internal), NodePort for frontend (external access via `minikube service`)
- ConfigMaps: Optional; non-secret config via values.yaml
- Secrets: Kubernetes Secret object named `app-secrets` containing DATABASE_URL, BETTER_AUTH_SECRET, COHERE_API_KEY (mounted as env vars)

**Secrets & Configuration Management**:
- Secrets Approach: kubectl create secret generic (not Helm secrets, not sealed-secrets – simplicity for demo)
- Secret Name: `app-secrets` (single generic secret with 3 key-value pairs)
- Mounting Strategy: envFrom: secretRef in Deployment spec (all secrets as environment variables)
- No Hardcoding: Dockerfiles, manifests, and charts contain NO plain-text secrets
- .env Reference: `.env.example` documents all required env vars for local development

**Minikube Configuration**:
- Driver: `docker` (--driver=docker on Windows, native Docker integration)
- Resources: --cpus=4 --memory=8192 (8GB RAM recommended for smooth operation with both pods + system)
- Startup Command: `minikube start --driver=docker --cpus=4 --memory=8192`
- Image Loading: `minikube image load todo-frontend:latest` and `minikube image load todo-backend:latest`
- Service Access: `minikube service todo-frontend` (NodePort) or `minikube tunnel` (LoadBalancer, if used)
- Dashboard: `minikube dashboard` for visual inspection

**AI-Assisted DevOps Tools**:
- Gordon (Docker AI Agent): Generate and optimize Dockerfiles (multi-stage, layer efficiency, image size reduction)
- kubectl-ai: Generate Helm chart structure, deployment templates, and service definitions
- Kagent: Cluster health analysis, resource optimization, bottleneck identification
- Usage Strategy: Specs-first approach – write infra specs, AI generates artifacts, human review and refine
- Commit Traceability: Every commit using AI tools includes sanitized prompt/output excerpt in commit message

**Testing & Validation**:
- Docker Smoke Tests: Build success, image < 500MB, `docker run → curl /health`, env vars injected
- Minikube Tests: Startup success, image load success, pod creation via `kubectl run test --image=...`
- Helm Tests: `helm lint`, `helm template`, `helm install --dry-run`
- Kubernetes Tests: `kubectl get pods/services`, logs, describe failures, port-forward
- End-to-End Tests: Login via frontend, create task, use Cohere chatbot, verify Neon DB persistence, multi-user isolation
- Failure Simulation: Wrong secret → pod crash → debug with `kubectl logs` and `kubectl describe`
- Demo Readiness: Record steps (startup → helm install → browser access → chatbot demo)

**Code Reuse & Minimal Changes**:
- Phase II Frontend: No changes – same Next.js 16+, same API calls, same auth
- Phase III Backend: No changes – same FastAPI, same Cohere integration, same MCP tools
- Only New Artifacts: Dockerfiles, Helm charts, K8s manifests, deployment scripts

---

## Constitution Check

**GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.**

### Phase IV Constitution (v2.1.0) – Kubernetes Principles

**Principle XII: Cloud-Native Containerization & Orchestration**

✅ **Docker & Containerization Rules**:
- [x] Multi-stage builds mandatory ✓ (Planned: Node build → nginx for frontend; Python UV → uvicorn for backend)
- [x] Non-root user (UID 1000) ✓ (Both Dockerfiles will use non-root)
- [x] Image tags: `<app-name>:latest` or `:v1` ✓ (Planned: `todo-frontend:latest`, `todo-backend:latest`)
- [x] Health checks in K8s manifests (not Dockerfile) ✓ (Helm templates will include readiness/liveness probes)
- [x] Gordon AI for Dockerfile generation ✓ (Planned: Use Gordon to generate and optimize both Dockerfiles)

✅ **Kubernetes & Helm Rules**:
- [x] One Helm chart per service ✓ (Planned: separate charts for frontend & backend)
- [x] values.yaml for configurable env vars, image tags, replicas ✓ (Planned: replicas 1–2, image tags, env vars in values)
- [x] Deployments: readiness/liveness probes, rolling update strategy ✓ (Helm templates will include all)
- [x] Services: ClusterIP (backend), NodePort/LoadBalancer (frontend) ✓ (Planned: ClusterIP for backend, NodePort for frontend)
- [x] kubectl-ai or Kagent for manifest generation ✓ (Planned: Use both for chart/manifest creation)

✅ **Secret & Configuration Management**:
- [x] NEVER hardcode secrets ✓ (All secrets in Kubernetes Secret object, mounted as env vars)
- [x] Kubernetes Secrets via kubectl create or Helm values ✓ (Planned: kubectl create secret generic app-secrets)
- [x] Secrets mounted as env vars (NOT ConfigMaps) ✓ (Helm deployment spec will use envFrom: secretRef)

✅ **Minikube & Local Deployment Flow**:
- [x] `minikube start --driver=docker` ✓ (Windows driver of choice)
- [x] Images loaded via `minikube image load` ✓ (Planned: both images loaded after build)
- [x] Secrets created before Helm install ✓ (kubectl create secret step mandatory)
- [x] Helm install succeeds, pods reach Running ✓ (Planned: both charts deployed, pods validated)
- [x] Frontend accessible via minikube service ✓ (NodePort access documented)

✅ **AI-Assisted DevOps**:
- [x] Gordon for Dockerfile creation/optimization ✓ (Planned: Primary AI tool for Dockerfile generation)
- [x] kubectl-ai for manifest generation ✓ (Planned: Used for Helm chart/template creation)
- [x] Kagent for cluster health analysis ✓ (Planned: Used for validation and optimization)
- [x] AI usage traceable in commit history ✓ (All commits will include AI tool names and prompts)

✅ **Security & Best Practices**:
- [x] No hardcoded secrets ✓ (All verified in constitution check)
- [x] Non-root containers ✓ (Both Dockerfiles)
- [x] Resource limits/requests in Deployments ✓ (Helm values will include resources: section)
- [x] Health checks passing ✓ (Readiness/liveness probes in templates)
- [x] User isolation enforced ✓ (Backend JWT verification, no changes needed)

**Constitution Check Result**: ✅ **PASS** – All Phase IV principles satisfied. Plan aligns with constitutional requirements.

### Core Principles (Phase II–III) – Preserved

✅ **Spec-Driven Development**: This plan is spec-driven; all work traced to specifications
✅ **User Isolation**: No changes to JWT or query filtering; enforcement preserved
✅ **Stateless Authentication**: JWT handling unchanged; secrets mounted as env vars
✅ **Technology Stack Fidelity**: No new dependencies; Docker, Kubernetes, Helm are infrastructure only
✅ **Modular Architecture**: Separate Helm charts; clear separation of concerns
✅ **Testability**: Plan includes layered testing (Docker, Minikube, Helm, K8s, E2E)
✅ **API Design Standards**: No API changes; Phase II CRUD and Phase III chat endpoints untouched
✅ **Database Design**: No schema changes; Neon access via external DATABASE_URL secret
✅ **Code Quality**: Only containerization layers added; no rewrites or refactoring
✅ **Traceability**: PHRs created for all decisions; ADRs suggested for architectural choices
✅ **AI & Agentic Workflow**: Gordon, kubectl-ai, Kagent usage documented and traceable

**Overall Constitution Check**: ✅ **FULL PASS** – Plan adheres to all Phase II–IV constitutional principles.

---

## Key Architectural Decisions

### Decision 1: Minikube Docker Driver (Windows)

**Choice**: `--driver=docker` (Docker Desktop integration)

**Rationale**:
- Native Docker integration on Windows (no VM overhead like Hyper-V or VirtualBox)
- Judges likely have Docker Desktop already installed
- Fastest startup and resource efficiency
- Simplest setup documentation ("if you have Docker Desktop, you're ready")

**Alternatives Considered**:
- Hyper-V driver: Requires Windows Pro/Enterprise; more complex VM management
- VirtualBox driver: Requires separate download; slower VM startup; legacy preference

**Tradeoffs**: Docker driver assumes Docker Desktop installed; if not available, falls back to Hyper-V (documented in README troubleshooting)

---

### Decision 2: Image Registry – Local Minikube Docker Daemon

**Choice**: `minikube image load` (local registry, no Docker Hub/external repo needed)

**Rationale**:
- Demo is 100% local; no external dependencies or network calls
- Fastest image loading (direct Docker daemon injection)
- Zero configuration; no registry credentials or authentication
- Images persist in Minikube cache across restarts

**Alternatives Considered**:
- Minikube registry addon (`minikube addons enable registry`): Requires additional addon; more complex
- Docker Hub: Requires credentials, network access, slower for judge's first-time demo
- Local Docker registry: Additional container to manage; complexity not justified for demo

**Tradeoffs**: Images must be rebuilt if Minikube is deleted; acceptable for hackathon scope

---

### Decision 3: Helm Chart Structure – Separate Charts (Frontend & Backend)

**Choice**: Two independent Helm charts: `todo-frontend/` and `todo-backend/`

**Rationale**:
- Modularity: Each service can be deployed/updated independently
- Clarity: Judges see separation of concerns (frontend != backend concerns)
- Best practice: Microservices architecture pattern; production-ready
- Flexibility: Can add more services later without umbrella chart complexity

**Alternatives Considered**:
- Single umbrella chart: Simpler initial setup but less modular; harder to explain separation
- Combined chart with many conditional blocks: Becomes unreadable; not production-ready

**Tradeoffs**: Two `helm install` commands instead of one; negligible complexity cost for significantly better architecture

---

### Decision 4: Secrets Management – kubectl create secret generic

**Choice**: `kubectl create secret generic app-secrets --from-literal=DATABASE_URL=... --from-literal=BETTER_AUTH_SECRET=... --from-literal=COHERE_API_KEY=...`

**Rationale**:
- Simple, direct, zero configuration
- No specialized tools (sealed-secrets, Vault, etc.) needed
- Easy to understand and document for judges
- Secrets are base64-encoded in etcd; sufficient for local demo

**Alternatives Considered**:
- Helm --set-string: Works, but requires sensitive values in command history
- Sealed-secrets: Overkill for local demo; requires additional controller
- Helm values with secrets: Risk of secrets in YAML; not recommended

**Tradeoffs**: Not production-grade (no encryption at rest); acceptable for local Minikube demo. Documentation emphasizes this is demo-only approach.

---

### Decision 5: Frontend Service Type – NodePort

**Choice**: `type: NodePort` (direct IP:port access via `minikube service todo-frontend`)

**Rationale**:
- Simple access model: `minikube service todo-frontend` opens browser automatically
- No tunnel complexity; judges see direct network access
- Works on Windows without additional setup
- Clear, understandable service pattern

**Alternatives Considered**:
- LoadBalancer with `minikube tunnel`: More complex; requires separate terminal; harder to explain
- Ingress controller: Overkill for demo; adds complexity

**Tradeoffs**: NodePort is less elegant than LoadBalancer; acceptable for demo context

---

### Decision 6: Resource Requests/Limits – Realistic (Not Minimal)

**Choice**: Conservative but realistic limits to prevent Minikube instability while allowing full app operation

**Frontend Deployment**:
```yaml
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 256Mi
```

**Backend Deployment**:
```yaml
resources:
  requests:
    cpu: 250m
    memory: 256Mi
  limits:
    cpu: 1000m
    memory: 512Mi
```

**Rationale**:
- Reflects realistic app behavior (not micro-optimization; not wasteful)
- Prevents Minikube OOM or CPU thrashing (8GB RAM, 4 CPUs available)
- Demonstrates production-ready thinking to judges
- Allows app to breathe; avoids artificial constraints causing demo failures

**Alternatives Considered**:
- Minimal limits (50m CPU, 64Mi RAM): Risk of pod eviction; breaks demo
- No limits: Wastes resources; unprofessional

**Tradeoffs**: Uses more Minikube resources; justified by demo reliability

---

### Decision 7: Health Check Endpoints – Use Existing /health if Available, Add Minimal Check if Missing

**Choice**: Backend checks for existing `/health` endpoint; if missing, add minimal check (no code rewrite)

**Rationale**:
- Kubernetes readiness/liveness probes require health checks
- If backend already has `/health` (likely for Phase III Cohere integration), use it
- If not, add minimal read-only check (e.g., `GET /health` returns `{"status": "ok"}`)
- Minimal change aligns with "strict code reuse" principle

**Alternatives Considered**:
- Skip health checks: Risky; pods may appear Running but be stuck
- Modify app logic for health check: Against principle; unnecessary code change

**Traceoffs**: May require minimal backend change; justified by reliability and constitutionally-required probes

---

## Project Structure

### Documentation (this feature)

```text
specs/5-k8s-deployment/
├── spec.md                           # Feature specification (this file)
├── plan.md                           # Implementation plan (generated by /sp.plan)
├── research.md                       # Phase 0 research findings (generated by /sp.plan)
├── data-model.md                     # Infrastructure model (generated by /sp.plan)
├── quickstart.md                     # Quick reference guide (generated by /sp.plan)
├── contracts/                        # Infrastructure contracts (generated by /sp.plan)
│   ├── dockerfile-contract.md
│   ├── helm-values-schema.md
│   └── kubernetes-manifest-schema.md
├── checklists/
│   └── requirements.md               # Specification quality checklist
└── tasks.md                          # Implementation tasks (generated by /sp.tasks)
```

### Infrastructure (new Phase IV directories)

```text
docker/
├── frontend.Dockerfile               # Multi-stage frontend image
└── backend.Dockerfile                # Multi-stage backend image

k8s/
├── helm-charts/
│   ├── todo-frontend/
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   └── templates/
│   │       ├── deployment.yaml
│   │       ├── service.yaml
│   │       └── _helpers.tpl
│   └── todo-backend/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── deployment.yaml
│           ├── service.yaml
│           ├── configmap.yaml (optional)
│           └── _helpers.tpl
├── manifests/                        # Optional raw YAML backups
│   ├── frontend-deploy.yaml
│   └── backend-deploy.yaml
└── secrets/
    └── app-secrets-template.yaml     # Template only (never commit real values)

specs/infra/                          # Infrastructure specs
├── minikube-deployment.md            # Step-by-step deployment guide
├── helm-charts.md                    # Helm chart design specification
├── docker-gordon.md                  # Dockerfile generation strategy & prompts
└── ai-devops.md                      # kubectl-ai and Kagent usage patterns
```

### No Changes to Existing Code

```text
frontend/                             # UNCHANGED from Phase II–III
└── [All files remain identical]

backend/                              # UNCHANGED from Phase II–III
└── [All files remain identical]

agents/                               # UNCHANGED from Phase III
└── [All files remain identical]

skills/                               # UNCHANGED from Phase III
└── [All files remain identical]
```

---

## Implementation Phases

### Phase 0: Outline & Research

**Objective**: Resolve architectural decisions and document research findings.

**Tasks**:
1. Create `specs/5-k8s-deployment/research.md` documenting:
   - Decision 1–7 choices with full rationale
   - Best practices for multi-stage Docker builds
   - Helm chart design patterns
   - Kubernetes probe configuration best practices
   - Gordon AI usage for Dockerfile optimization
   - kubectl-ai and Kagent typical workflows

2. Create `specs/5-k8s-deployment/data-model.md` documenting:
   - Docker Image entity (tag, size, layers, registry)
   - Kubernetes Deployment entity (replicas, probes, resource requests)
   - Helm Chart entity (structure, values schema)
   - Secret entity (key-value pairs, mounting strategy)
   - Service entity (type, port, selector)

3. Create `specs/infra/` specifications:
   - `minikube-deployment.md`: Step-by-step startup and deployment flow
   - `helm-charts.md`: Chart design (values, templates, structure)
   - `docker-gordon.md`: Dockerfile generation strategy with example Gordon prompts
   - `ai-devops.md`: kubectl-ai and Kagent usage patterns

**Output**: research.md, data-model.md, quickstart.md, /contracts/, /specs/infra/ (4 specs)

---

### Phase 1: Containerization (Dockerfiles + AI Generation)

**Objective**: Generate optimized multi-stage Dockerfiles using Gordon AI.

**Tasks**:

1. **Generate Frontend Dockerfile** (using Gordon):
   - Multi-stage build: Node.js 20-alpine build stage → nginx:alpine final
   - Build stage: `npm install`, `npm run build` (Next.js static export or Vercel build)
   - Final stage: Copy build artifacts to nginx; expose port 80; non-root user (UID 1000)
   - HEALTHCHECK: HTTP GET /health (nginx status or custom)
   - Target size: < 200MB
   - Use @agents/docker-qa-validator to test build

2. **Generate Backend Dockerfile** (using Gordon):
   - Multi-stage build: Python 3.12-slim with UV package manager → uvicorn final stage
   - Build stage: UV install dependencies from pyproject.toml
   - Final stage: Copy app code, venv; expose port 8000; non-root user (UID 1000)
   - HEALTHCHECK: HTTP GET /health (FastAPI endpoint, create if missing)
   - Target size: < 400MB
   - Use @agents/docker-qa-validator to test build

3. **Build Images Locally** (no Minikube yet):
   ```bash
   docker build -f docker/frontend.Dockerfile -t todo-frontend:latest .
   docker build -f docker/backend.Dockerfile -t todo-backend:latest .
   ```

4. **Smoke Tests**:
   ```bash
   docker run --rm todo-frontend:latest curl localhost:80/health
   docker run --rm todo-backend:latest curl localhost:8000/health
   # Verify image sizes < targets
   docker images | grep todo-
   ```

**Output**: `docker/frontend.Dockerfile`, `docker/backend.Dockerfile`, tested images

**Artifacts**:
- Commit: "docker: Add multi-stage Dockerfiles (generated via Gordon AI)"
- Includes sanitized Gordon prompt and optimization notes

---

### Phase 2: Minikube Setup

**Objective**: Initialize local Kubernetes cluster and prepare for deployments.

**Tasks**:

1. **Start Minikube**:
   ```bash
   minikube start --driver=docker --cpus=4 --memory=8192
   minikube status
   ```

2. **Verify Cluster Ready**:
   ```bash
   kubectl cluster-info
   kubectl get nodes
   ```

3. **Load Images into Minikube**:
   ```bash
   minikube image load todo-frontend:latest
   minikube image load todo-backend:latest
   minikube image ls | grep todo-
   ```

4. **Verify Images Available**:
   ```bash
   minikube image ls | grep -E "todo-frontend|todo-backend"
   ```

**Output**: Running Minikube cluster with images loaded

**Artifacts**:
- None (setup-only phase)

---

### Phase 3: Secrets & Configuration

**Objective**: Create Kubernetes Secret with app configuration.

**Tasks**:

1. **Create Secret** (manual step, not automated):
   ```bash
   kubectl create secret generic app-secrets \
     --from-literal=DATABASE_URL="postgresql://user:pass@neon.tech/db" \
     --from-literal=BETTER_AUTH_SECRET="your-secret-key" \
     --from-literal=COHERE_API_KEY="your-cohere-api-key"
   ```

2. **Verify Secret Created**:
   ```bash
   kubectl get secrets
   kubectl describe secret app-secrets
   ```

3. **Create Template Documentation**:
   - `k8s/secrets/app-secrets-template.yaml` (template only, never commit real values)
   - Document which env vars map to which secrets

**Output**: `app-secrets` Kubernetes Secret in default namespace

**Artifacts**:
- `k8s/secrets/app-secrets-template.yaml` (template documentation)

---

### Phase 4: Helm Chart Generation & Validation

**Objective**: Create Helm charts for frontend and backend using kubectl-ai/Kagent.

**Tasks**:

1. **Generate Frontend Helm Chart** (using kubectl-ai):
   - Chart name: `todo-frontend`
   - Chart.yaml: name, version, description, appVersion
   - values.yaml:
     ```yaml
     replicaCount: 1
     image:
       repository: todo-frontend
       tag: latest
       pullPolicy: IfNotPresent
     service:
       type: NodePort
       port: 80
       nodePort: 30000
     resources:
       requests:
         cpu: 100m
         memory: 128Mi
       limits:
         cpu: 500m
         memory: 256Mi
     ```
   - templates/deployment.yaml: Deployment with readiness/liveness probes, env from secret
   - templates/service.yaml: NodePort service
   - templates/_helpers.tpl: Standard Helm helpers

2. **Generate Backend Helm Chart** (using kubectl-ai):
   - Chart name: `todo-backend`
   - Chart.yaml: name, version, description, appVersion
   - values.yaml:
     ```yaml
     replicaCount: 1
     image:
       repository: todo-backend
       tag: latest
       pullPolicy: IfNotPresent
     service:
       type: ClusterIP
       port: 8000
     resources:
       requests:
         cpu: 250m
         memory: 256Mi
       limits:
         cpu: 1000m
         memory: 512Mi
     ```
   - templates/deployment.yaml: Deployment with readiness/liveness probes, env from secret
   - templates/service.yaml: ClusterIP service
   - templates/_helpers.tpl: Standard Helm helpers

3. **Validate Charts**:
   ```bash
   helm lint k8s/helm-charts/todo-frontend
   helm lint k8s/helm-charts/todo-backend
   helm template todo-frontend k8s/helm-charts/todo-frontend
   helm template todo-backend k8s/helm-charts/todo-backend
   ```

4. **Dry-Run Install** (verify no errors):
   ```bash
   helm install --dry-run todo-backend k8s/helm-charts/todo-backend --set imagePullPolicy=Never
   helm install --dry-run todo-frontend k8s/helm-charts/todo-frontend --set imagePullPolicy=Never
   ```

**Output**: `k8s/helm-charts/todo-frontend/` and `k8s/helm-charts/todo-backend/` (fully validated)

**Artifacts**:
- Commit: "k8s: Add Helm charts for frontend and backend (generated via kubectl-ai)"
- Includes kubectl-ai prompt excerpt and validation output

---

### Phase 5: Deployment

**Objective**: Deploy both services to Minikube using Helm.

**Tasks**:

1. **Install Backend First** (frontend depends on backend service name):
   ```bash
   helm install todo-backend k8s/helm-charts/todo-backend \
     --set image.pullPolicy=Never \
     --set-string secrets=app-secrets
   ```

2. **Verify Backend Pods Running**:
   ```bash
   kubectl get pods -l app=todo-backend
   kubectl get svc todo-backend
   ```

3. **Install Frontend**:
   ```bash
   helm install todo-frontend k8s/helm-charts/todo-frontend \
     --set image.pullPolicy=Never \
     --set-string secrets=app-secrets
   ```

4. **Verify Frontend Pods Running**:
   ```bash
   kubectl get pods -l app=todo-frontend
   kubectl get svc todo-frontend
   ```

5. **Wait for Readiness** (< 60 seconds expected):
   ```bash
   kubectl wait --for=condition=ready pod -l app=todo-backend --timeout=60s
   kubectl wait --for=condition=ready pod -l app=todo-frontend --timeout=60s
   ```

**Output**: Both services running, pods in Ready state

**Artifacts**:
- None (deployment-only phase)

---

### Phase 6: Verification & Integration Testing

**Objective**: Validate end-to-end functionality and fix any issues.

**Tasks**:

1. **Pod Health Checks**:
   ```bash
   kubectl get pods -o wide
   kubectl describe pod <frontend-pod>
   kubectl describe pod <backend-pod>
   kubectl logs <frontend-pod>
   kubectl logs <backend-pod>
   ```

2. **Service Connectivity**:
   ```bash
   kubectl get svc
   kubectl port-forward svc/todo-backend 8000:8000 &
   curl http://localhost:8000/health
   ```

3. **Frontend Access**:
   ```bash
   minikube service todo-frontend
   # Browser opens; verify login page loads
   ```

4. **End-to-End Testing**:
   - Login with test credentials
   - Create a task
   - Verify task appears in UI
   - Send a chat message (Cohere integration test)
   - Verify chatbot response
   - Check database persistence (task saved to Neon)
   - Multi-user isolation test: login as different user, verify only own data visible

5. **Failure Simulation & Debugging**:
   - Delete a pod; verify Kubernetes restarts it automatically
   - Check pod restart count: `kubectl describe pod <pod-name>`
   - Simulate wrong secret: temporarily modify secret value, verify pod crashes, check `kubectl logs`

6. **Performance Baseline**:
   - Measure frontend load time: `minikube service todo-frontend` → browser open → time to interactive
   - Measure chat response latency: send message → measure time to response
   - Check pod CPU/memory usage: `kubectl top pods`

**Output**: All tests passing; any failures debugged and fixed

**Artifacts**:
- Test results/logs
- Screenshot of working frontend
- Console output showing pod health and service connectivity

---

### Phase 7: Polish & Documentation

**Objective**: Create final README with judge-ready demo scripts and traceability.

**Tasks**:

1. **Update Root README.md**:
   - Add Phase IV section: "Local Kubernetes Deployment"
   - Step-by-step Minikube setup instructions
   - Screenshot of working frontend
   - Troubleshooting section (common errors, solutions)
   - AI tool usage examples (Gordon prompts, kubectl-ai prompts, Kagent commands)
   - Demo walkthrough script

2. **Create Demo Script** (`k8s/DEMO.md`):
   ```bash
   # 1. Start Minikube
   minikube start --driver=docker --cpus=4 --memory=8192

   # 2. Create secrets
   kubectl create secret generic app-secrets \
     --from-literal=DATABASE_URL="..." \
     --from-literal=BETTER_AUTH_SECRET="..." \
     --from-literal=COHERE_API_KEY="..."

   # 3. Load images
   minikube image load todo-frontend:latest
   minikube image load todo-backend:latest

   # 4. Deploy with Helm
   helm install todo-backend k8s/helm-charts/todo-backend --set image.pullPolicy=Never
   helm install todo-frontend k8s/helm-charts/todo-frontend --set image.pullPolicy=Never

   # 5. Wait for pods
   kubectl wait --for=condition=ready pod -l app=todo-frontend --timeout=60s

   # 6. Access frontend
   minikube service todo-frontend
   ```

3. **Create Debugging Guide** (`k8s/TROUBLESHOOTING.md`):
   - Pod stuck in Pending: check `kubectl describe pod`
   - Pod in CrashLoopBackOff: check `kubectl logs`
   - Wrong secret mounting: verify `kubectl exec <pod> env | grep DATABASE`
   - Network connectivity: test with `kubectl port-forward` and `curl`

4. **Create AI Tool Documentation** (`specs/infra/ai-devops.md`):
   - Gordon prompts used for Dockerfile generation
   - kubectl-ai prompts for Helm chart generation
   - Kagent analysis results
   - Key learnings and optimizations

5. **Git Commit Message**:
   ```
   docs: Add Phase IV Kubernetes deployment guide

   - Updated README.md with Minikube setup instructions
   - Added k8s/DEMO.md with step-by-step demo walkthrough
   - Added k8s/TROUBLESHOOTING.md with debugging tips
   - Documented Gordon/kubectl-ai/Kagent usage in specs/infra/

   Judges can now follow: minikube start → helm install → browser → full demo
   ```

**Output**: Complete documentation; ready for hackathon submission

**Artifacts**:
- Updated README.md with Phase IV section
- `k8s/DEMO.md` with demo walkthrough
- `k8s/TROUBLESHOOTING.md` with debugging guide
- `specs/infra/ai-devops.md` with AI tool usage

---

## Dependency & Secret Injection Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                   Minikube Cluster                          │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Kubernetes Secret: app-secrets                         │ │
│  │ ├─ DATABASE_URL (Neon connection)                     │ │
│  │ ├─ BETTER_AUTH_SECRET (JWT secret)                   │ │
│  │ └─ COHERE_API_KEY (Cohere API key)                   │ │
│  └────────────────────────────────────────────────────────┘ │
│                          ↓ mounted as env vars              │
│  ┌────────────────┐              ┌────────────────┐        │
│  │ Frontend Pod   │              │ Backend Pod    │        │
│  │ (todo-frontend)│              │ (todo-backend) │        │
│  │                │              │                │        │
│  │ Env: (none)    │              │ Env:           │        │
│  │                │              │  - DATABASE_URL│        │
│  │ Container:     │              │  - BETTER_AUTH │        │
│  │ nginx:alpine   │              │  - COHERE_KEY  │        │
│  │                │              │                │        │
│  │ Port: 80       │              │ Container:     │        │
│  │ (NodePort)     │◄────API Call─┤ uvicorn:8000   │        │
│  └────────────────┘    (backend) │ (ClusterIP)    │        │
│           ↓                       └────────────────┘        │
│        Service                             ↓                │
│     NodePort:30000                      Service             │
│          ↓                            ClusterIP:8000        │
│   ┌──────────────┐                                          │
│   │ Judge Browser│                                          │
│   │              │                                          │
│   └──────────────┘                                          │
│
│ External (outside Minikube):
│ ┌──────────────────────────────────────────┐              │
│ │ Neon PostgreSQL (DATABASE_URL)           │              │
│ │ Cohere API (COHERE_API_KEY)              │              │
│ └──────────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────────┘
```

---

## Minikube Startup & Deployment Flow

```
Step 1: Start Minikube
  Command: minikube start --driver=docker --cpus=4 --memory=8192
  Result: Local Kubernetes cluster running in Docker

Step 2: Build Docker Images (on Host)
  Command: docker build -f docker/frontend.Dockerfile -t todo-frontend:latest .
           docker build -f docker/backend.Dockerfile -t todo-backend:latest .
  Result: Images available in local Docker daemon

Step 3: Load Images into Minikube
  Command: minikube image load todo-frontend:latest
           minikube image load todo-backend:latest
  Result: Images available in Minikube's Docker daemon

Step 4: Create Kubernetes Secret
  Command: kubectl create secret generic app-secrets \
             --from-literal=DATABASE_URL=... \
             --from-literal=BETTER_AUTH_SECRET=... \
             --from-literal=COHERE_API_KEY=...
  Result: app-secrets object in default namespace

Step 5: Deploy Backend with Helm
  Command: helm install todo-backend k8s/helm-charts/todo-backend \
             --set image.pullPolicy=Never
  Result: Backend deployment, pods, service created

Step 6: Deploy Frontend with Helm
  Command: helm install todo-frontend k8s/helm-charts/todo-frontend \
             --set image.pullPolicy=Never
  Result: Frontend deployment, pods, service created

Step 7: Wait for Pods Ready
  Command: kubectl wait --for=condition=ready pod -l app=todo-frontend --timeout=60s
           kubectl wait --for=condition=ready pod -l app=todo-backend --timeout=60s
  Result: Both services running and accepting traffic

Step 8: Access Frontend
  Command: minikube service todo-frontend
  Result: Browser opens to http://<minikube-ip>:<nodeport>

Step 9: Verify Full Stack
  - Login with credentials → auth working
  - Add task → frontend → backend → Neon DB working
  - Send chat → backend → Cohere API working
  - Verify user isolation → JWT + query filtering working
```

---

## Testing Strategy

### Layer 1: Docker Build & Image Validation

**Tests**:
1. Frontend Dockerfile builds without errors
   - No BuildKit warnings
   - Multi-stage structure correct
   - Non-root user UID 1000 present
2. Backend Dockerfile builds without errors
   - Same checks as frontend
3. Image sizes verified:
   - Frontend < 200MB
   - Backend < 400MB
4. Smoke test: Images run locally
   - `docker run todo-frontend curl localhost/health` → 200 OK
   - `docker run todo-backend curl localhost:8000/health` → 200 OK

**Tool**: @agents/docker-qa-validator

---

### Layer 2: Minikube Cluster Validation

**Tests**:
1. Minikube cluster starts
   - `minikube start --driver=docker` succeeds
   - `minikube status` shows "Running"
2. Images load successfully
   - `minikube image load` completes
   - `minikube image ls | grep todo-` shows both images
3. Pods can be created
   - `kubectl run test --image=busybox` succeeds
   - Pod reaches Running state

**Tool**: kubectl commands

---

### Layer 3: Helm Chart Validation

**Tests**:
1. Charts pass linting
   - `helm lint k8s/helm-charts/todo-frontend` → no warnings
   - `helm lint k8s/helm-charts/todo-backend` → no warnings
2. Templates render correctly
   - `helm template todo-frontend k8s/helm-charts/todo-frontend` outputs valid YAML
   - `helm template todo-backend k8s/helm-charts/todo-backend` outputs valid YAML
3. Dry-run install succeeds
   - `helm install --dry-run todo-frontend ...` succeeds
   - `helm install --dry-run todo-backend ...` succeeds

**Tool**: Helm CLI

---

### Layer 4: Kubernetes Deployment Validation

**Tests**:
1. Pods reach Running state
   - `kubectl get pods` shows both pods Running and Ready (1/1)
   - Pods reach Ready within 60 seconds
2. Services created and accessible
   - `kubectl get svc` shows todo-frontend (NodePort) and todo-backend (ClusterIP)
   - `kubectl get endpoints` shows both services have endpoints
3. Health checks passing
   - `kubectl describe pod <frontend-pod>` shows Readiness probe passing
   - `kubectl describe pod <backend-pod>` shows Readiness probe passing
4. Logs clean (no errors)
   - `kubectl logs <frontend-pod>` shows nginx startup logs, no errors
   - `kubectl logs <backend-pod>` shows uvicorn startup logs, no errors

**Tool**: kubectl CLI

---

### Layer 5: End-to-End Integration Testing

**Tests**:
1. Frontend accessibility
   - `minikube service todo-frontend` opens browser
   - Login page loads (Minikube IP + NodePort)
   - Page is interactive (can type in forms)

2. Authentication & Authorization
   - Signup/login with test credentials works
   - JWT token obtained and stored in localStorage
   - Logout clears token and redirects to home

3. Task CRUD Operations
   - Create task: form submit → API call → task appears in list
   - Edit task: update title → API call → list reflects changes
   - Delete task: confirmation → API call → task removed from list
   - Mark complete: checkbox toggle → API call → UI reflects status

4. Cohere Chatbot Integration
   - Send chat message → backend receives message
   - Backend calls Cohere API → response returned
   - Response appears in UI with chatbot name
   - Conversation persists in Neon database

5. Multi-User Isolation
   - Login as User A, create task T1
   - Logout; login as User B
   - Verify User B doesn't see T1
   - Create task T2 as User B
   - Verify only User B sees T2
   - Logout; login as User A
   - Verify User A still doesn't see T2; still sees T1

6. Database Persistence
   - Create task, logout
   - Login again
   - Task still exists (persisted to Neon)

7. Pod Auto-Recovery
   - Delete a pod: `kubectl delete pod <pod-name>`
   - Kubernetes restarts pod automatically
   - Pod reaches Ready again (< 10 seconds)
   - App functionality restored

**Tool**: Browser automation or manual walkthrough

---

### Layer 6: Failure Simulation & Debugging

**Tests**:
1. Wrong secret value
   - Modify DATABASE_URL to invalid string
   - Re-deploy pod
   - Pod crashes (CrashLoopBackOff)
   - `kubectl logs` shows database connection error
   - Fix secret, pod recovers

2. Missing environment variable
   - Misconfigure Helm chart to not mount secret
   - Pod starts but application fails
   - `kubectl describe pod` shows env vars missing
   - Fix Helm values, re-deploy

3. Port mismatch
   - Change service port to wrong value
   - Frontend cannot reach backend
   - `kubectl port-forward` test shows connection timeout
   - Fix service port, connectivity restored

**Tool**: kubectl debugging commands

---

### Layer 7: Demo Readiness

**Test**:
- Follow `/k8s/DEMO.md` from start to finish
- All steps complete successfully
- Frontend accessible and responsive
- Chatbot demo (send message → get Cohere response)
- Task demo (create, edit, delete, mark complete)
- Judge can perform all above without errors

**Success Criteria**: Demo takes < 5 minutes total; all functionality working

---

## Rollback & Debugging Checklist

### Rollback Procedures

**If deployment fails**:
1. Uninstall Helm charts:
   ```bash
   helm uninstall todo-frontend
   helm uninstall todo-backend
   ```
2. Delete secret (if needed):
   ```bash
   kubectl delete secret app-secrets
   ```
3. Restart Minikube (if cluster is corrupted):
   ```bash
   minikube stop
   minikube delete
   minikube start --driver=docker --cpus=4 --memory=8192
   ```
4. Rebuild images and retry deployment

---

### Debugging Checklist

**Pod not starting (Pending state)**:
- [ ] Check `kubectl describe pod <pod-name>` for error events
- [ ] Verify image available: `minikube image ls | grep todo-`
- [ ] Check resource availability: `kubectl top nodes` (is node under OOM?)
- [ ] Inspect imagePullPolicy: should be `IfNotPresent` (local images)

**Pod in CrashLoopBackOff**:
- [ ] Check logs: `kubectl logs <pod-name>` (what error on startup?)
- [ ] Verify environment variables: `kubectl exec <pod-name> env | grep DATABASE`
- [ ] Test secret mounting: `kubectl exec <pod-name> env | grep -E "DATABASE|BETTER_AUTH|COHERE"`
- [ ] If database error: verify DATABASE_URL is correct
- [ ] If missing env vars: check Helm deployment template for `envFrom` block

**Service not accessible**:
- [ ] Check service exists: `kubectl get svc`
- [ ] Check endpoints: `kubectl get endpoints` (should show pod IPs)
- [ ] Test port-forward: `kubectl port-forward svc/todo-frontend 8000:80` then `curl localhost:8000`
- [ ] Verify NodePort value: `kubectl get svc todo-frontend -o jsonpath='{.spec.ports[0].nodePort}'`

**Frontend can't reach backend**:
- [ ] Verify backend service name: `kubectl get svc todo-backend`
- [ ] Check frontend pod environment: does it know backend service name?
- [ ] Test connectivity: `kubectl exec <frontend-pod> curl http://todo-backend:8000/health`
- [ ] If DNS resolution fails: check pod DNS settings with `kubectl exec <pod> cat /etc/resolv.conf`

**Chat not working (Cohere API)**:
- [ ] Verify COHERE_API_KEY is mounted: `kubectl exec <backend-pod> env | grep COHERE`
- [ ] Check backend logs: `kubectl logs <backend-pod> | grep -i cohere` (rate limit? timeout?)
- [ ] Test Cohere connectivity: can backend reach external API? Check firewall/proxy
- [ ] Rate limit issue: wait and retry, or check Cohere dashboard for limits

**Database persistence not working**:
- [ ] Verify DATABASE_URL is correct: `kubectl exec <backend-pod> env | grep DATABASE`
- [ ] Test DB connection: `kubectl exec <backend-pod> python -c "import sqlalchemy; sqlalchemy.create_engine(os.getenv('DATABASE_URL')).connect()"`
- [ ] Check Neon account: is database accessible? Sufficient connection limit?
- [ ] Verify schema exists: did database migrations run? Check backend logs for migration errors

**Multi-user isolation broken**:
- [ ] Check JWT token: does it include `user_id`? (decode token: `jwt.decode(token, ...)`)
- [ ] Verify backend code: does every route filter by `user_id` from JWT?
- [ ] Test manually: login as User A, create task T1; login as User B, try to fetch T1 (should 403)
- [ ] Check if JWT verification middleware is working: wrong token should return 401

---

## Summary: Implementation Roadmap

| Phase | Objective | Key Deliverable | Duration | Risk |
|-------|-----------|-----------------|----------|------|
| **0** | Research & Design | research.md, data-model.md, specs/infra/ | 1–2 hours | Low (mostly planning) |
| **1** | Dockerfiles + Gordon | docker/frontend.Dockerfile, docker/backend.Dockerfile | 2–3 hours | Medium (Gordon AI usage; test Docker builds) |
| **2** | Minikube Setup | Running cluster, images loaded | 30 minutes | Low (standard Minikube startup) |
| **3** | Secrets & Config | app-secrets Kubernetes Secret | 15 minutes | Low (simple kubectl command) |
| **4** | Helm Charts + kubectl-ai | k8s/helm-charts/, validated charts | 2–3 hours | Medium (AI tool usage; Helm complexity) |
| **5** | Deployment | Both services running in Minikube | 30 minutes | Medium (pods must reach Ready; may need debugging) |
| **6** | Verification & Testing | All tests passing; full E2E demo works | 1–2 hours | High (E2E testing; integration issues) |
| **7** | Polish & Docs | Updated README, demo script, AI docs | 1 hour | Low (documentation) |
| **TOTAL** | | All artifacts ready for hackathon submission | **8–12 hours** | Medium–High (Docker + Kubernetes integration) |

---

## Success Criteria

### Mandatory Pass Gates

1. **Docker images build and run** ✓
   - Both Dockerfiles build without errors
   - Images < 500MB (preferably < 200MB frontend, < 400MB backend)
   - Smoke tests pass: health checks respond with 200 OK

2. **Minikube cluster operational** ✓
   - `minikube start --driver=docker` succeeds
   - Cluster status shows "Running"
   - Images loaded successfully

3. **Helm charts valid** ✓
   - `helm lint` passes for both charts
   - `helm template` produces valid YAML
   - `helm install --dry-run` completes without errors

4. **Deployment successful** ✓
   - Both pods reach Running state (1/1 Ready)
   - Startup time < 60 seconds
   - Services created and accessible

5. **E2E functionality working** ✓
   - Frontend accessible via `minikube service`
   - Login/auth flow works
   - Task CRUD operations work (create, read, update, delete)
   - Chat endpoint responds (Cohere integration)
   - Multi-user isolation enforced
   - Database persistence verified

6. **Security & best practices met** ✓
   - No hardcoded secrets
   - Non-root containers
   - Health checks passing
   - Resource limits/requests defined
   - User isolation enforced

7. **AI-assisted DevOps traceable** ✓
   - Gordon used for Dockerfile generation
   - kubectl-ai used for Helm chart generation
   - Kagent used for cluster analysis
   - All usage documented in commits and specs/infra/

8. **Documentation complete** ✓
   - README.md updated with Phase IV section
   - Step-by-step demo walkthrough (README or k8s/DEMO.md)
   - Debugging guide (k8s/TROUBLESHOOTING.md)
   - AI tool prompts documented

---

## Next Steps

1. **Execute Phase 0**: Run research workflow; create research.md, data-model.md, specs/infra/
2. **Execute Phase 1**: Generate Dockerfiles using Gordon; test with docker-qa-validator
3. **Execute Phases 2–7**: Follow deployment roadmap; leverage agents for Docker QA and architecture validation
4. **Execute `/sp.tasks`**: Generate task breakdown for implementation team
5. **Begin development**: Follow tasks in order; track progress with Git commits and PHRs

---

## References & Dependencies

- **Phase IV Constitution** (v2.1.0): Governing principles for Kubernetes, Docker, Helm, AI-assisted DevOps
- **Feature Specification**: specs/5-k8s-deployment/spec.md (requirements, user stories, success criteria)
- **Phase II Code**: frontend/, backend/ (unchanged from Phase II–III)
- **Minikube Documentation**: https://minikube.sigs.k8s.io/docs/
- **Helm Documentation**: https://helm.sh/docs/
- **Docker Best Practices**: https://docs.docker.com/develop/dev-best-practices/
- **Gordon AI**: Docker containerization optimization
- **kubectl-ai**: Kubernetes manifest and Helm chart generation
- **Kagent**: Cluster health and optimization analysis
