---
id: 1
title: Phase IV Kubernetes Deployment Specification
stage: spec
date: 2026-01-20
surface: agent
model: claude-haiku-4-5-20251001
feature: 5-k8s-deployment
branch: Phase3
user: user
command: /sp.specify
labels: ["kubernetes", "docker", "helm", "minikube", "phase-iv", "containerization", "infrastructure", "ai-devops"]
links:
  spec: specs/5-k8s-deployment/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/5-k8s-deployment/spec.md
  - specs/5-k8s-deployment/checklists/requirements.md
tests:
  - Specification quality validation (all checklist items pass)
  - No [NEEDS CLARIFICATION] markers
  - All functional requirements testable
  - All success criteria measurable
---

## Prompt

Phase IV – Complete Local Kubernetes Deployment of Todo AI Chatbot with Minikube, Helm, Gordon, kubectl-ai, and Kagent

Target audience: Hackathon judges evaluating cloud-native maturity, AI-assisted DevOps, security, and impressive local demo capability; DevOps reviewers expecting clean Helm charts, secure secrets handling, and reproducible deployment.

Focus: Containerize and deploy the fully integrated Phase II + Phase III Todo AI Chatbot (premium Next.js frontend + FastAPI + Cohere-powered chatbot + Neon DB + Better Auth JWT) on a local Minikube Kubernetes cluster using AI-assisted tools (Gordon for Docker, kubectl-ai & Kagent for manifests/Helm/charts), with Helm packaging, secure secrets, and zero-downtime local demo readiness.

Success criteria:
- **Docker Containerization**:
  - Frontend: Multi-stage Dockerfile (node build → nginx serve), image size < 200MB, non-root user, exposes port 80
  - Backend: Multi-stage Dockerfile (uv + python slim → uvicorn), image size < 400MB, non-root, exposes port 8000
  - Use Gordon (Docker AI Agent) to generate/optimize Dockerfiles where possible
  - Build success, smoke tests pass (health check, env vars injected, port reachable)

- **Helm Charts & Kubernetes Deployment**:
  - Two Helm charts: todo-frontend & todo-backend
  - Values.yaml configurable (replicas=1–2, image tag, env vars)
  - Deployments: readiness/liveness probes, rolling updates
  - Services: ClusterIP (backend), NodePort/LoadBalancer (frontend)
  - Secrets: app-secrets containing DATABASE_URL, BETTER_AUTH_SECRET, COHERE_API_KEY
  - Use kubectl-ai / Kagent to generate charts/manifests (show AI prompts in commit history)

- **Minikube & Local Demo Readiness**:
  - minikube start --driver=docker succeeds
  - Images loaded into Minikube (minikube image load)
  - helm install todo-backend ./k8s/helm-charts/todo-backend --set secrets=app-secrets
  - helm install todo-frontend ./k8s/helm-charts/todo-frontend
  - Frontend accessible via minikube service or tunnel
  - Full functionality: TODO CRUD + Cohere chatbot working, conversations persisted, user isolation enforced

- **Security & Best Practices**:
  - No hardcoded secrets – all via Kubernetes Secrets
  - Non-root containers
  - Resource limits/requests in Deployments
  - Health checks passing
  - No public exposure needed (local only)

- **AI-Assisted DevOps Excellence**:
  - Gordon used for Dockerfile creation/optimization
  - kubectl-ai used for manifest/Helm generation (e.g., "generate Helm chart for FastAPI backend")
  - Kagent used for cluster health check & optimization
  - Process traceable in commit history (prompts & AI outputs)

Constraints:
- Local only – Minikube + Docker Desktop (no cloud clusters)
- Reuse 100% of Phase II + III code (no rewrites)
- Secrets: DATABASE_URL, BETTER_AUTH_SECRET, COHERE_API_KEY from .env → Kubernetes Secret
- Helm charts: Simple, well-commented, values.yaml driven
- No Ingress (use NodePort + minikube tunnel for demo)
- Timeline: Single iteration perfection with @agents/docker-testing-agent + @agents/architecture-planner

Not building:
- Cloud deployment (EKS/GKE/etc.)
- Advanced monitoring (Prometheus/Grafana)
- CI/CD pipelines
- PersistentVolume for DB (use external Neon)
- Heavy custom Helm operators

Manual Verification Checklist (must pass 100%):
- [ ] Docker images build successfully (frontend & backend)
- [ ] Smoke tests pass (docker run → curl health/port)
- [ ] minikube start & tunnel working
- [ ] Secrets created & mounted correctly
- [ ] helm install succeeds for both charts
- [ ] kubectl get pods → Running & Ready
- [ ] Frontend accessible via Minikube IP/port
- [ ] Chatbot responds with Cohere, tasks saved to Neon DB
- [ ] Multi-user isolation works in Kubernetes pods
- [ ] Judges can follow README steps and see everything live

This spec demands absolute deployment perfection – the most impressive local Kubernetes demo in the hackathon, showcasing AI-assisted DevOps (Gordon + kubectl-ai + Kagent) and seamless integration with the premium Phase II + III app.

## Response snapshot

Comprehensive Phase IV Kubernetes deployment specification created:

**User Scenarios (5 stories)**:
- P1: DevOps setup & local demo (core functionality)
- P1: Security validation (secrets, non-root, best practices)
- P1: AI-assisted DevOps traceability (Gordon, kubectl-ai, Kagent usage)
- P2: Multi-stage Docker image optimization
- P2: Helm chart configurability & reusability

**Functional Requirements (40 total)**:
- Docker requirements (FR-001 through FR-009): Multi-stage builds, non-root users, image sizes, ports, health checks
- Kubernetes requirements (FR-010 through FR-018): Helm charts, deployments, probes, services
- Secrets management (FR-019 through FR-023): No hardcoding, Kubernetes Secret mounting
- Minikube deployment (FR-024 through FR-029): Docker driver, image loading, secret creation, Helm install
- Validation (FR-030 through FR-035): Pods running, logs, health checks, user isolation, Cohere integration
- AI-assisted DevOps (FR-036 through FR-040): Gordon/kubectl-ai usage, specs, README documentation

**Success Criteria (14 measurable outcomes)**:
- SC-001–SC-014 cover build success, deployment startup (<60s), frontend accessibility (<30s), chat latency (<10s), user isolation verification, health checks, pod recovery, demo walkthrough, AI tool traceability

**Edge Cases (7 documented)**: Network unavailable, missing secrets, OOM, Cohere downtime, port mismatch, user isolation breach, pod restart recovery

**Quality Checklist**: ✅ All items pass – no [NEEDS CLARIFICATION] markers, all requirements testable/measurable, scope clearly bounded

## Outcome

- ✅ Impact: Phase IV specification complete and ready for planning. Covers all success criteria from user input (Docker containerization, Helm charts, Minikube deployment, security best practices, AI-assisted DevOps excellence). Specification is technology-agnostic, measurable, and testable.
- 🧪 Tests: Quality checklist passed 100% – all mandatory sections present, no ambiguities, edge cases identified, assumptions documented, out-of-scope items defined.
- 📁 Files: `specs/5-k8s-deployment/spec.md` (comprehensive feature specification), `specs/5-k8s-deployment/checklists/requirements.md` (quality validation checklist)
- 🔁 Next prompts: Execute `/sp.plan` to generate implementation plan with architecture decisions, task breakdown, and deployment sequencing.
- 🧠 Reflection: Specification emphasizes zero-downtime demo reliability (pods running <60s, frontend accessible <30s), security non-negotiables (no hardcoded secrets, non-root containers, user isolation enforcement), AI tool traceability (Gordon, kubectl-ai, Kagent prompts embedded in commits), and production-ready practices (multi-stage Docker, Helm configurability, health checks, resource limits). Foundation laid for judges to evaluate cloud-native maturity and AI-assisted DevOps sophistication.

## Evaluation notes (flywheel)

- Failure modes observed: None – specification is well-formed, comprehensive, and aligned with Phase IV constitution (v2.1.0) and user success criteria.
- Graders run and results (PASS/FAIL): PASS – All functional requirements are testable, all success criteria are measurable, edge cases documented, assumptions clear, scope bounded, no implementation details.
- Prompt variant (if applicable): Standard feature specification workflow (describe feature → create user scenarios → derive requirements → define success criteria → validate).
- Next experiment (smallest change to try): Proceed to `/sp.plan` to generate implementation plan with architecture decisions (Dockerfile structure, Helm chart layout, secret mounting strategy, Minikube networking).

