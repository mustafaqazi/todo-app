---
id: 1
title: Phase IV Infrastructure Constitution
stage: constitution
date: 2026-01-20
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: Phase3
user: user
command: /sp.constitution
labels: ["kubernetes", "docker", "helm", "infrastructure", "phase-iv", "minikube", "ai-devops"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - Constitution validation (no unresolved placeholders)
  - Version bump rationale (MINOR 2.0.0 → 2.1.0)
  - Backward compatibility verification
---

## Prompt

You are an expert cloud-native architect, DevOps engineer, and spec-driven developer building Phase IV of the hackathon Todo AI Chatbot project: local Kubernetes deployment of the complete Phase II + Phase III application using Minikube, Helm Charts, Docker (with Gordon AI assistance), kubectl-ai, and Kagent.

Adhere strictly to this constitution for all specification writing, planning, Dockerfiles, Helm chart generation, Kubernetes manifests, deployment automation, and validation across the entire monorepo. This constitution ensures consistency, security, reproducibility, zero-downtime local demo capability, and outstanding hackathon judging quality.

## 1. Project Overview & Goals
- Phase IV Objective: Containerize and deploy the fully integrated Phase II (multi-user TODO web app) + Phase III (Cohere-powered AI Chatbot) on a local Kubernetes cluster using Minikube.
- Key Deliverables:
  - Docker images for frontend (Next.js) and backend (FastAPI + Cohere)
  - Helm charts for both services (frontend + backend)
  - Use Gordon (Docker AI) for Dockerfile generation/optimization where possible
  - Use kubectl-ai and Kagent for AI-assisted manifest/chart creation and debugging
  - Deploy on Minikube with external Neon DB access via secrets
  - Demonstrate full functionality: TODO CRUD, Cohere chatbot, user isolation, conversation persistence
- Integration Rule: Reuse 100% of Phase II + III code — no rewrites; only add Kubernetes/Docker layers
- Judging Focus: Spec-driven infra process (prompts, iterations, AI tools usage), clean Helm charts, secure secrets handling, easy local demo steps, impressive AI-assisted DevOps

## 2. Technology Stack (Strict – No Deviations)
- Containerization: Docker Desktop + Gordon (Docker AI Agent)
- Local Kubernetes: Minikube (docker driver preferred on Windows)
- Package Manager: Helm 3+
- AI DevOps Tools: kubectl-ai, Kagent
- Frontend: Existing Phase II Next.js 16+ App Router
- Backend: Existing Phase II + III FastAPI + Cohere SDK + SQLModel async
- Database: External Neon PostgreSQL (via DATABASE_URL secret)
- Authentication: Better Auth JWT (BETTER_AUTH_SECRET secret)
- AI: Cohere API (COHERE_API_KEY secret)
- No cloud providers — everything local via Minikube

## 3. Security & Secret Management Rules (Non-Negotiable)
- NEVER hardcode secrets (BETTER_AUTH_SECRET, DATABASE_URL, COHERE_API_KEY)
- Use Kubernetes Secrets for all sensitive env vars
- Create secrets via `kubectl create secret generic` or Helm values
- Mount secrets as environment variables in Deployments (not ConfigMaps)
- Enforce user_id isolation remains in backend code (JWT verification)
- Minikube runs locally — no public exposure required
- Use HTTPS internally if LoadBalancer (Minikube tunnel)
- No root containers; use non-root users in Dockerfiles

## 4. Monorepo Structure Additions for Phase IV
- /docker/
  - frontend.Dockerfile
  - backend.Dockerfile
- /k8s/
  - /helm-charts/
    - todo-frontend/
      - Chart.yaml
      - values.yaml
      - templates/deployment.yaml, service.yaml, ingress.yaml (optional)
    - todo-backend/
      - (same structure)
  - /manifests/ (optional raw YAML if Helm not used)
  - /secrets/ (templates only – never commit real values)
- /specs/infra/
  - minikube-deployment.md
  - helm-charts.md
  - docker-gordon.md
  - ai-devops.md

## 5. Docker & Containerization Rules
- Multi-stage builds mandatory for small images
- Frontend Dockerfile: node:20-alpine build → nginx:alpine serve
- Backend Dockerfile: python:3.12-slim → uv install → uvicorn/gunicorn
- Use Gordon AI for generating/optimizing Dockerfiles when possible
- Image tags: <app-name>:latest or :v1
- Build & load directly into Minikube: `minikube image load` or use local registry
- Health checks: readiness & liveness probes in k8s manifests

## 6. Helm Chart & Kubernetes Rules
- One Helm chart per service (frontend & backend separate)
- Use values.yaml for configurable env vars, image tags, replicas (default 1–2)
- Deployments: replicas, rollingUpdate strategy, probes
- Services: ClusterIP for backend, NodePort/LoadBalancer for frontend
- Secrets: Reference from Helm values or existing k8s secrets
- Prefer AI generation: kubectl-ai "generate Helm chart for FastAPI backend with 2 replicas" or kagent "create deployment chart for Next.js frontend"

## 7. AI-Assisted DevOps Rules
- Use Gordon for: Dockerfile creation, optimization, troubleshooting
- Use kubectl-ai for: manifest generation, scaling, debugging ("why pod failing?")
- Use Kagent for: cluster health analysis, resource optimization
- Spec-driven infra: Write infra specs first → generate YAML/Helm → apply
- Show AI usage in commit history (prompts & outputs)

## 8. Deployment & Demo Rules
- Minikube start command: `minikube start --driver=docker`
- Tunnel external access: `minikube tunnel` for LoadBalancer
- Secrets creation example:
  kubectl create secret generic app-secrets \
    --from-literal=DATABASE_URL=... \
    --from-literal=BETTER_AUTH_SECRET=... \
    --from-literal=COHERE_API_KEY=...
- Access frontend: `minikube service todo-frontend`
- Demo flow: Show minikube dashboard, kubectl get pods, chat working with Cohere

## 9. General Principles
- Prioritize demo reliability: app must work after simple minikube start + helm install
- Keep manifests/Helm charts simple, readable, well-commented for judges
- Document everything in README.md: step-by-step setup, Gordon/kubectl-ai examples
- Validate: pods running, frontend accessible via Minikube IP, chatbot responds with Cohere, DB connected, no crashes
- Favor AI-generated infra (show process) while maintaining security & simplicity

When generating Dockerfiles, Helm charts, manifests, plans, or deployment steps, always reference and enforce this constitution explicitly in your reasoning.

## Response snapshot

Constitution updated from v2.0.0 to v2.1.0. Added principle XII: Cloud-Native Containerization & Orchestration governing Docker, Kubernetes, Helm, Minikube, secret management, and AI-assisted DevOps (Gordon, kubectl-ai, Kagent). Updated monorepo structure section to include `/docker/` and `/k8s/` directories. Comprehensive Sync Impact Report added documenting:
- MINOR version bump rationale (additive, no breaking changes)
- Modified and new principles
- Templates requiring updates
- Follow-up TODOs (13 items for infrastructure specs, Dockerfiles, Helm charts, README)
- Backward compatibility verification (Phase II–III code untouched)

## Outcome

- ✅ Impact: Constitution now governs Phase IV Kubernetes/Docker/Helm deployment with strict security, demo reliability, and AI-assisted DevOps principles. Zero rewrites of Phase II–III code; purely additive infrastructure layer.
- 🧪 Tests: Constitution file validated—no unresolved placeholders, version numbering consistent, dates ISO format, principles declarative and testable.
- 📁 Files: `.specify/memory/constitution.md` (v2.1.0) updated with 250+ lines of Phase IV infrastructure governance.
- 🔁 Next prompts: Execute `/sp.specify` to create infrastructure specifications (minikube-deployment.md, helm-charts.md, docker-gordon.md, ai-devops.md); then proceed to planning and task generation for Phase IV implementation.
- 🧠 Reflection: Phase IV constitution emphasizes spec-driven infrastructure (write specs first, generate YAML/Helm via AI tools), demo reproducibility (single-command Minikube startup + Helm install), security (secrets management via Kubernetes, no hardcoding), and AI-assisted DevOps workflow (Gordon for Dockerfiles, kubectl-ai for manifests, Kagent for cluster analysis). Foundation laid for judges to see systematic, traceable infra development using AI tools.

## Evaluation notes (flywheel)

- Failure modes observed: None—constitution is well-formed, consistent with Phases II–III, and adds new governance without breaking existing patterns.
- Graders run and results (PASS/FAIL): PASS — Constitution syntax valid, version bump justified, backward compatibility confirmed, all sections coherent.
- Prompt variant (if applicable): Standard constitution amendment workflow.
- Next experiment (smallest change to try): Create first infrastructure spec (minikube-deployment.md) to validate specification templates are adequate for Phase IV infra work.

