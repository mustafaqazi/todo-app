# Feature Specification: Phase IV – Complete Local Kubernetes Deployment of Todo AI Chatbot

**Feature Branch**: `5-k8s-deployment`
**Created**: 2026-01-20
**Status**: Draft
**Input**: Containerize and deploy the fully integrated Phase II + Phase III Todo AI Chatbot (premium Next.js frontend + FastAPI + Cohere-powered chatbot + Neon DB + Better Auth JWT) on a local Minikube Kubernetes cluster using AI-assisted tools (Gordon for Docker, kubectl-ai & Kagent for manifests/Helm/charts), with Helm packaging, secure secrets, and zero-downtime local demo readiness.

---

## User Scenarios & Testing

### User Story 1 – DevOps Engineer Sets Up Local Kubernetes Cluster and Deploys Todo App (Priority: P1)

A DevOps engineer or hackathon judge needs to demonstrate the Todo AI Chatbot application in a Kubernetes environment on their local machine. They should be able to go from a fresh checkout to a fully functioning demo with minimal manual steps, verifying that containerization and orchestration don't introduce any regressions.

**Why this priority**: This is the most critical path – without a working local Kubernetes demo, the entire Phase IV feature fails. The ability to reproduce deployment reliably is essential for judges and for validating that the Phase II–III application logic remains unchanged.

**Independent Test**: Can be fully tested by running a single demo sequence: `minikube start`, secret creation, `helm install` commands, and then verifying pods are running, frontend is accessible, and chatbot responds with Cohere. Delivers core value: reproducible, single-iteration demo with zero broken steps.

**Acceptance Scenarios**:

1. **Given** a fresh Minikube environment, **When** engineer runs setup commands in README order, **Then** all pods reach Running state within 60 seconds
2. **Given** pods are Running, **When** engineer accesses frontend via `minikube service todo-frontend`, **Then** login page loads without errors
3. **Given** authenticated user in frontend, **When** user creates a task and sends a chat message, **Then** task appears in DB and chatbot responds with Cohere-generated text
4. **Given** two different users logged in simultaneously, **When** each accesses their tasks/conversations, **Then** each sees only their own data (user isolation enforced)
5. **Given** a pod crashes, **When** Kubernetes health checks detect failure, **Then** pod is automatically restarted without manual intervention

---

### User Story 2 – Security Engineer Validates Secrets Management and Non-Root Containers (Priority: P1)

A security-conscious engineer or hackathon judge needs to verify that the Kubernetes deployment follows best practices: no hardcoded secrets, proper secret mounting, non-root containers, and resource limits. This prevents security regressions and demonstrates production-ready thinking.

**Why this priority**: Security is non-negotiable. Hardcoded secrets or root containers are instant disqualifiers. This user story ensures compliance with the constitution's security rules and demonstrates DevOps maturity to judges.

**Independent Test**: Can be fully tested by inspecting Dockerfile and Helm templates for non-root users, running `kubectl get secrets` to verify app-secrets exist and are mounted correctly, and confirming no plain-text secrets appear in manifests or ConfigMaps.

**Acceptance Scenarios**:

1. **Given** Dockerfiles for frontend and backend, **When** engineer inspects them, **Then** both use non-root user (UID 1000 or similar) for app processes
2. **Given** Helm chart deployment spec, **When** engineer reviews templates, **Then** no secrets appear as plain text; all reference external Kubernetes Secret objects
3. **Given** Kubernetes cluster with deployed app, **When** engineer runs `kubectl get secrets app-secrets -o yaml`, **Then** all three required secrets (DATABASE_URL, BETTER_AUTH_SECRET, COHERE_API_KEY) exist and are base64-encoded
4. **Given** deployed pods, **When** engineer runs `kubectl exec <pod> id`, **Then** container is running as non-root user (not UID 0)
5. **Given** Helm values.yaml, **When** engineer searches for DATABASE_URL, COHERE_API_KEY, or BETTER_AUTH_SECRET values, **Then** none appear; only references to secret names found

---

### User Story 3 – AI-Assisted DevOps Tools Demonstrate Spec-Driven Infrastructure Creation (Priority: P1)

A hackathon judge evaluating the development process wants to see that the team used AI-assisted DevOps tools (Gordon for Dockerfiles, kubectl-ai/Kagent for manifests and charts) to generate infrastructure code from specifications. Commit history should show AI prompts and outputs, demonstrating systematic, traceable infrastructure development.

**Why this priority**: Judges specifically evaluate "impressive AI-assisted DevOps" as a success criterion. Showing that Dockerfiles, Helm charts, and manifests were AI-generated from specs (with human review) demonstrates technical sophistication and proper use of AI tools in the development workflow.

**Independent Test**: Can be fully tested by reviewing commit history for AI tool usage (Gordon, kubectl-ai, Kagent prompts embedded in commit messages), examining infrastructure specs in `/specs/infra/`, and confirming that generated artifacts (Dockerfiles, Helm charts) match the specs exactly.

**Acceptance Scenarios**:

1. **Given** commit history, **When** engineer reviews messages, **Then** at least 3 commits mention "Gordon", "kubectl-ai", or "Kagent" with example prompts
2. **Given** `/specs/infra/` directory, **When** engineer reads specs, **Then** each spec (minikube-deployment.md, helm-charts.md, docker-gordon.md, ai-devops.md) references AI tool usage
3. **Given** Dockerfiles, **When** engineer compares them to docker-gordon.md spec, **Then** they match the spec's requirements (multi-stage, image sizes, ports, health checks)
4. **Given** Helm charts, **When** engineer compares them to helm-charts.md spec, **Then** they match the spec's structure (values.yaml format, deployment replicas, probe configuration)
5. **Given** a Helm chart revision, **When** engineer reviews commit message, **Then** it explains what AI tool generated it and includes sanitized prompt/output excerpt for traceability

---

### User Story 4 – Hackathon Judge Validates Multi-Stage Docker Builds for Image Optimization (Priority: P2)

A judge or DevOps reviewer wants to confirm that Docker images are optimized: multi-stage builds are used, image sizes are reasonable (frontend <200MB, backend <400MB), and build processes are efficient. This demonstrates production-ready containerization practices.

**Why this priority**: While less critical than core functionality, image size and build efficiency matter for demo performance and production readiness. Judges appreciate attention to detail in container optimization.

**Independent Test**: Can be fully tested by building both Dockerfiles locally, checking resulting image sizes with `docker images`, and inspecting Dockerfile structure for multi-stage patterns (FROM...AS builder, final FROM...COPY from builder).

**Acceptance Scenarios**:

1. **Given** frontend Dockerfile, **When** engineer builds it, **Then** resulting image is less than 200MB
2. **Given** backend Dockerfile, **When** engineer builds it, **Then** resulting image is less than 400MB
3. **Given** both Dockerfiles, **When** engineer inspects them, **Then** both use multi-stage build pattern (build stage with dependencies, final stage with only runtime essentials)
4. **Given** frontend image build, **When** build completes, **Then** build time is under 2 minutes (reasonable for CI/CD)
5. **Given** both images, **When** engineer inspects layers with `docker history`, **Then** each layer is < 100MB; no bloated dependency layers present

---

### User Story 5 – Infrastructure Maintainer Validates Helm Chart Configurability and Reusability (Priority: P2)

An infrastructure maintainer needs to verify that Helm charts are well-structured, reusable, and fully configurable via values.yaml. They should be able to modify deployment parameters (replicas, image tags, resource limits) without editing templates.

**Why this priority**: Helm chart quality matters for future maintenance and scaling. While not immediately critical for the demo, demonstrating good Helm practices shows production readiness.

**Independent Test**: Can be fully tested by deploying charts with custom values (`helm install --values override.yaml`), verifying that changes to values.yaml propagate correctly to deployed resources without template edits.

**Acceptance Scenarios**:

1. **Given** values.yaml, **When** engineer modifies `replicas: 2`, **When** charts are redeployed, **Then** deployments scale to 2 pods
2. **Given** values.yaml, **When** engineer changes `image.tag: v2`, **When** pods restart, **Then** new image version (v2) is deployed
3. **Given** a Helm chart, **When** engineer inspects templates/, **Then** no hardcoded config appears; all values reference `.Values.*` or ConfigMap/Secret references
4. **Given** Helm charts, **When** engineer runs `helm lint`, **Then** no warnings or errors reported
5. **Given** Helm values.yaml, **When** engineer documents parameters, **Then** each parameter has a comment explaining its purpose and valid values

---

### Edge Cases

- **What happens when Minikube network is unavailable?** Deployment should fail gracefully with clear error message; docs should document network prerequisites.
- **What happens when secrets are missing when Helm install runs?** Installation should fail with clear error indicating which secrets are missing; docs should clarify `kubectl create secret` step is mandatory.
- **What happens when a pod runs out of memory?** Kubernetes should evict the pod; liveness probe should detect and restart it. If pod repeatedly crashes, Helm deployment should show CrashLoopBackOff status; docs should explain how to increase resource limits.
- **What happens when Cohere API is down during demo?** Chat endpoint should return 503 Service Unavailable with clear message; frontend should show friendly error; other features (task CRUD) should continue working.
- **What happens when frontend tries to access backend on wrong port?** Connection should fail; browser console should show CORS or network error; logs should help diagnose port mismatch.
- **What happens when a user in pod A tries to access data belonging to user in pod B?** JWT verification should fail; API should return 403 Forbidden; user isolation should be enforced regardless of which pod processes the request.

---

## Requirements

### Functional Requirements

#### Docker Containerization

- **FR-001**: Frontend Dockerfile MUST use multi-stage build (node:20-alpine build stage → nginx:alpine final stage)
- **FR-002**: Frontend Dockerfile MUST expose port 80 and serve static Next.js build
- **FR-003**: Frontend Dockerfile MUST use non-root user for app processes (UID 1000)
- **FR-004**: Frontend image build MUST result in image < 200MB
- **FR-005**: Backend Dockerfile MUST use multi-stage build (python:3.12-slim with UV package manager → final stage with uvicorn)
- **FR-006**: Backend Dockerfile MUST expose port 8000 and run uvicorn/gunicorn server
- **FR-007**: Backend Dockerfile MUST use non-root user for app processes (UID 1000)
- **FR-008**: Backend image build MUST result in image < 400MB
- **FR-009**: Both Dockerfiles MUST include health check endpoint (e.g., ENV HEALTHCHECK CMD or readiness probe in Kubernetes)

#### Kubernetes & Helm Charts

- **FR-010**: System MUST provide separate Helm chart for frontend (todo-frontend) with Chart.yaml, values.yaml, and templates/ directory
- **FR-011**: System MUST provide separate Helm chart for backend (todo-backend) with same structure
- **FR-012**: Frontend chart MUST allow configuration of replicas (default 1–2), image tag, and service port via values.yaml
- **FR-013**: Backend chart MUST allow configuration of replicas, image tag, and service port via values.yaml
- **FR-014**: Frontend chart MUST deploy as Kubernetes Deployment with readiness and liveness probes
- **FR-015**: Backend chart MUST deploy as Kubernetes Deployment with readiness and liveness probes (HTTP GET /health or equivalent)
- **FR-016**: Frontend service MUST be NodePort or LoadBalancer (allow external access from Minikube host)
- **FR-017**: Backend service MUST be ClusterIP (internal only; frontend talks to it via service name)
- **FR-018**: Both deployments MUST support rolling update strategy with 1 replica as minimum during update

#### Secrets & Configuration Management

- **FR-019**: System MUST NOT hardcode DATABASE_URL, BETTER_AUTH_SECRET, or COHERE_API_KEY in Dockerfiles, manifests, or charts
- **FR-020**: System MUST accept these three secrets as Kubernetes Secret object named `app-secrets`
- **FR-021**: Helm charts MUST reference `app-secrets` by name; assume secret exists before deployment
- **FR-022**: Both deployments MUST mount secrets as environment variables (envFrom: secretRef)
- **FR-023**: `.env.example` file MUST document all required environment variables for local development reference

#### Minikube & Local Deployment

- **FR-024**: System MUST support `minikube start --driver=docker` command on Windows with Docker Desktop
- **FR-025**: Docker images MUST be loadable into Minikube with `minikube image load` command
- **FR-026**: System MUST support `kubectl create secret generic app-secrets --from-literal=...` for secret creation
- **FR-027**: System MUST support `helm install todo-frontend ./k8s/helm-charts/todo-frontend` and similar for backend
- **FR-028**: Frontend MUST be accessible via `minikube service todo-frontend` command (NodePort access)
- **FR-029**: Deployed pods MUST reach Running state and pass readiness checks within 60 seconds

#### Validation & Testing

- **FR-030**: System MUST support `kubectl get pods` to verify all pods are Running and Ready (1/1)
- **FR-031**: System MUST support `kubectl logs <pod-name>` to inspect container logs for debugging
- **FR-032**: Backend health endpoint MUST return 200 OK (e.g., GET /health)
- **FR-033**: System MUST enforce user isolation: attempt to access another user's tasks/conversations MUST return 403 Forbidden
- **FR-034**: Chat endpoint MUST work inside Kubernetes pods, calling external Cohere API and receiving responses
- **FR-035**: Database connections from pods MUST work (verify Neon PostgreSQL accessible via DATABASE_URL)

#### AI-Assisted DevOps & Documentation

- **FR-036**: Dockerfiles SHOULD be generated or optimized using Gordon AI; commit messages MUST reference this
- **FR-037**: Helm charts MAY be generated using kubectl-ai or Kagent; commit messages SHOULD reference this
- **FR-038**: Infrastructure specifications in `/specs/infra/` MUST document all AI tool usage (Gordon, kubectl-ai, Kagent)
- **FR-039**: README.md MUST include step-by-step Minikube setup and Helm deployment instructions
- **FR-040**: README.md MUST show example Gordon/kubectl-ai prompts used in development

### Key Entities

- **Docker Image**: A containerized version of frontend or backend; tagged with app name and version (e.g., `todo-frontend:latest`). Stored locally on host or in Minikube registry.
- **Kubernetes Pod**: Smallest deployable unit; runs one or more containers. Managed by Deployment for scaling, rolling updates, health checks.
- **Kubernetes Deployment**: Desired state for frontend or backend; specifies replicas, image, ports, probes, secret mounts, and update strategy.
- **Kubernetes Service**: Exposes pods internally (ClusterIP) or externally (NodePort/LoadBalancer). Frontend service allows external access; backend service is internal.
- **Kubernetes Secret**: Stores sensitive data (DATABASE_URL, BETTER_AUTH_SECRET, COHERE_API_KEY) in base64 encoding; mounted as env vars in pods.
- **Helm Chart**: Templated Kubernetes manifests (Chart.yaml, values.yaml, templates/). Parameterized for reusability across environments.
- **Minikube Cluster**: Local single-node Kubernetes cluster running inside Docker Desktop. Provides full Kubernetes API for local testing.

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: Docker images build successfully without errors; frontend < 200MB, backend < 400MB
- **SC-002**: `minikube start --driver=docker` succeeds and cluster is ready for deployments
- **SC-003**: `kubectl create secret generic app-secrets --from-literal=...` creates and stores three secrets without errors
- **SC-004**: `helm install` commands for both charts complete successfully; pods reach Running state within 60 seconds
- **SC-005**: Frontend is accessible and responsive via `minikube service todo-frontend` within 30 seconds of pods reaching Running
- **SC-006**: Authenticated user can create a task, see it in UI, and verify it persists in Neon database
- **SC-007**: Authenticated user can send a chat message in frontend; backend receives it, calls Cohere API, returns response within 10 seconds
- **SC-008**: Two different users logged in simultaneously each see only their own tasks and conversations (user isolation confirmed)
- **SC-009**: Health checks pass: `curl http://<backend-pod-ip>:8000/health` returns 200 OK
- **SC-010**: Kubernetes correctly enforces user isolation: attempt to access another user's task returns 403 Forbidden from pod
- **SC-011**: Helm lint reports no warnings or errors for both charts
- **SC-012**: Pod restart/recovery works: terminate a pod, observe Kubernetes restarts it automatically; app functionality resumes
- **SC-013**: Judges can follow README steps in order and see full app demo working without errors or manual interventions
- **SC-014**: Commit history shows AI tool usage (Gordon, kubectl-ai, Kagent) with example prompts and outputs embedded

### Acceptance Criteria

- **All Docker requirements (FR-001 through FR-009) met**: Multi-stage builds, non-root users, image sizes, ports correct
- **All Kubernetes requirements (FR-010 through FR-018) met**: Helm charts created, deployments configured, services set up
- **All secrets requirements (FR-019 through FR-023) met**: No hardcoded secrets, app-secrets mounted correctly, .env.example complete
- **All Minikube requirements (FR-024 through FR-029) met**: Docker driver, image loading, secret creation, Helm install, 60-second startup
- **All validation requirements (FR-030 through FR-035) met**: Pods running, logs accessible, health checks passing, user isolation enforced
- **All AI-Assisted DevOps requirements (FR-036 through FR-040) met**: Specs written, AI tools used, commit history traceable, README complete
- **All edge cases handled**: Missing secrets fail gracefully, network issues produce clear errors, resource limits work, Cohere downtime doesn't break task CRUD
- **Manual verification checklist 100% pass**: All 10 items in spec description pass (images build, smoke tests pass, minikube works, secrets mounted, helm install succeeds, pods running, frontend accessible, chatbot works, isolation enforced, judges can demo)

---

## Assumptions

- Judges and developers have Docker Desktop and Minikube installed locally
- Neon PostgreSQL connection string (DATABASE_URL) is available and accessible from local network
- Cohere API key (COHERE_API_KEY) is available and valid
- Better Auth secret (BETTER_AUTH_SECRET) is already configured and known
- Phase II–III application code (frontend Next.js, backend FastAPI) compiles and runs correctly without modification
- Phase II–III tests pass before containerization (no new bugs introduced by Docker/Kubernetes layers)
- Judges have `kubectl` and `helm` CLI tools installed
- Windows environment has Docker Desktop with WSL2 backend configured

---

## Out of Scope

- Cloud deployment (EKS, GKE, AKS) – local Minikube only
- Advanced monitoring (Prometheus, Grafana, ELK stack) – basic `kubectl logs` and `kubectl get pods` sufficient
- CI/CD pipelines – manual `docker build` and `helm install` sufficient for hackathon
- Persistent volumes for database – use external Neon, not local PV
- Ingress controllers – use NodePort + minikube tunnel for demo access
- Network policies – local demo doesn't need advanced networking
- Istio or service mesh – overkill for single-machine demo
- Helm dependency management (umbrella charts) – separate simple charts only
- Multi-namespace deployments – default namespace sufficient

---

## Constraints

- Reuse 100% of Phase II–III code – no rewrites, only containerization layers
- Local development only – no cloud resources
- Single-iteration perfection – must work on first demo attempt
- No breaking changes to existing APIs or authentication
- Helm charts must be simple and readable (judges should understand them quickly)
- Resource limits must be reasonable for local development (not micro, not excessive)

---

## Next Steps

1. **Create infrastructure specifications** (via `/sp.clarify` if needed, then proceed to specs)
   - `specs/infra/minikube-deployment.md` – step-by-step local deployment guide
   - `specs/infra/helm-charts.md` – Helm chart design and configuration
   - `specs/infra/docker-gordon.md` – Dockerfile generation strategy
   - `specs/infra/ai-devops.md` – kubectl-ai and Kagent usage patterns

2. **Generate Dockerfiles using Gordon AI** (Docker AI Agent)
   - Frontend: node:20-alpine → nginx:alpine multi-stage
   - Backend: python:3.12-slim → uvicorn multi-stage

3. **Generate Helm charts using kubectl-ai/Kagent**
   - todo-frontend chart with values, deployment, service templates
   - todo-backend chart with same structure

4. **Create Kubernetes manifests and test locally**
   - Build images, load into Minikube, deploy with Helm
   - Verify pods running, services accessible, app functional

5. **Validate end-to-end** against manual verification checklist
   - All acceptance criteria passing
   - All edge cases handled
   - Ready for hackathon demo

---

## References & Dependencies

- **Phase II Constitution** (v2.0.0): Established security, authentication, and API design principles
- **Phase III Constitution** (v2.0.0): Added Cohere, MCP tools, conversation persistence
- **Phase IV Constitution** (v2.1.0): Added Kubernetes, Docker, Helm, AI-assisted DevOps principles
- **Frontend Code**: `/frontend/` (Next.js 16+, TypeScript, Tailwind, shadcn/ui)
- **Backend Code**: `/backend/` (FastAPI, SQLModel, async, Cohere SDK)
- **Database**: Neon PostgreSQL (external, accessed via DATABASE_URL secret)
- **Authentication**: Better Auth (JWT tokens, BETTER_AUTH_SECRET)
- **AI**: Cohere API (chat completions, tool calling, COHERE_API_KEY)
