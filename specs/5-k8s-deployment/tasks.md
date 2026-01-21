# Tasks: Phase IV – Complete Local Kubernetes Deployment of Todo AI Chatbot

**Input**: Design documents from `/specs/5-k8s-deployment/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)
**Status**: Ready for implementation

---

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic directory structure for Phase IV

- [x] T001 Create Phase IV directory structure: `/docker/`, `/k8s/helm-charts/`, `/k8s/manifests/`, `/k8s/secrets/`, `/specs/infra/`
- [x] T002 Create `.env.example` template documenting required env vars (DATABASE_URL, BETTER_AUTH_SECRET, COHERE_API_KEY, NEXT_PUBLIC_API_URL)
- [x] T003 [P] Create `/specs/infra/` placeholder files: minikube-deployment.md, helm-charts.md, docker-gordon.md, ai-devops.md

**Checkpoint**: Phase IV directory structure in place; env template ready ✅

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure and research that MUST complete before implementation

**⚠️ CRITICAL**: No implementation can begin until this phase is complete

- [x] T004 Create `specs/5-k8s-deployment/research.md` documenting 7 architectural decisions with rationale and tradeoff analysis
- [x] T005 Create `specs/5-k8s-deployment/data-model.md` defining Docker Image, Kubernetes Deployment, Helm Chart, Secret, Service entities
- [x] T006 Create `specs/5-k8s-deployment/quickstart.md` with quick reference for deployment flow
- [x] T007 [P] Research multi-stage Docker best practices (layer caching, security, image size optimization)
- [x] T008 [P] Research Helm chart structure patterns (values.yaml, templates, _helpers.tpl)
- [x] T009 [P] Document Gordon AI usage patterns for Dockerfile generation (example prompts in specs/infra/docker-gordon.md)
- [x] T010 [P] Document kubectl-ai/Kagent usage patterns for Helm chart generation (specs/infra/ai-devops.md)

**Checkpoint**: Research complete, all architectural decisions documented, best practices understood ✅

---

## Phase 3: User Story 1 – DevOps Engineer Sets Up Local Kubernetes Cluster and Deploys Todo App (Priority: P1) 🎯 MVP

**Goal**: Deliver reproducible, single-iteration Kubernetes demo with all pods running, frontend accessible, chatbot working

**Independent Test**: Execute demo sequence: `minikube start` → create secrets → `helm install` → verify pods Running → access frontend → login → create task → send chat → receive Cohere response

### Research & Specs for User Story 1

- [ ] T011 Use Gordon AI to research and document optimal multi-stage Dockerfile for Next.js frontend in specs/infra/docker-gordon.md (include example prompts)
- [ ] T012 Use Gordon AI to research and document optimal multi-stage Dockerfile for FastAPI backend in specs/infra/docker-gordon.md (include example prompts)
- [ ] T013 Create specs/infra/minikube-deployment.md: step-by-step startup and deployment flow with all commands
- [ ] T014 Create specs/infra/helm-charts.md: Helm chart structure design (Chart.yaml, values.yaml, templates/, probe configuration)

### Docker Implementation for User Story 1

- [ ] T015 [P] Generate frontend Dockerfile using Gordon AI: `docker/frontend.Dockerfile` (Node 20-alpine build → nginx:alpine, non-root UID 1000, < 200MB, port 80)
- [ ] T016 [P] Generate backend Dockerfile using Gordon AI: `docker/backend.Dockerfile` (Python 3.12-slim + UV → uvicorn, non-root UID 1000, < 400MB, port 8000)
- [ ] T017 Build frontend Docker image locally: `docker build -f docker/frontend.Dockerfile -t todo-frontend:latest .`
- [ ] T018 Build backend Docker image locally: `docker build -f docker/backend.Dockerfile -t todo-backend:latest .`
- [ ] T019 Verify frontend image size < 200MB: `docker images | grep todo-frontend`
- [ ] T020 Verify backend image size < 400MB: `docker images | grep todo-backend`
- [ ] T021 Smoke test frontend image: `docker run --rm todo-frontend:latest curl localhost/health`
- [ ] T022 Smoke test backend image: `docker run --rm todo-backend:latest curl localhost:8000/health`

### Secrets & Configuration for User Story 1

- [ ] T023 Create `k8s/secrets/app-secrets-template.yaml` (template with placeholder values, never commit real secrets)
- [ ] T024 Document secret creation procedure in k8s/DEMO.md: `kubectl create secret generic app-secrets --from-literal=...`
- [ ] T025 Verify secret mounting strategy in Helm templates: `envFrom: - secretRef: name: app-secrets`

### Helm Chart Generation for User Story 1

- [ ] T026 Use kubectl-ai to generate `k8s/helm-charts/todo-backend/Chart.yaml` (name, version, description, appVersion)
- [ ] T027 Use kubectl-ai to generate `k8s/helm-charts/todo-backend/values.yaml` (replicaCount, image, service type ClusterIP, port 8000, resources)
- [ ] T028 Use kubectl-ai to generate `k8s/helm-charts/todo-backend/templates/deployment.yaml` (Deployment with readiness/liveness probes, envFrom secret, port 8000)
- [ ] T029 Use kubectl-ai to generate `k8s/helm-charts/todo-backend/templates/service.yaml` (ClusterIP service, port 8000)
- [ ] T030 Use kubectl-ai to generate `k8s/helm-charts/todo-backend/templates/_helpers.tpl` (standard Helm helpers)
- [ ] T031 Use kubectl-ai to generate `k8s/helm-charts/todo-frontend/Chart.yaml` (name, version, description, appVersion)
- [ ] T032 Use kubectl-ai to generate `k8s/helm-charts/todo-frontend/values.yaml` (replicaCount, image, service type NodePort, port 80, resources)
- [ ] T033 Use kubectl-ai to generate `k8s/helm-charts/todo-frontend/templates/deployment.yaml` (Deployment with readiness/liveness probes, envFrom secret, port 80)
- [ ] T034 Use kubectl-ai to generate `k8s/helm-charts/todo-frontend/templates/service.yaml` (NodePort service, port 80, nodePort 30000)
- [ ] T035 Use kubectl-ai to generate `k8s/helm-charts/todo-frontend/templates/_helpers.tpl` (standard Helm helpers)

### Helm Chart Validation for User Story 1

- [ ] T036 [P] Lint backend chart: `helm lint k8s/helm-charts/todo-backend` (must pass with no warnings)
- [ ] T037 [P] Lint frontend chart: `helm lint k8s/helm-charts/todo-frontend` (must pass with no warnings)
- [ ] T038 [P] Template backend chart: `helm template todo-backend k8s/helm-charts/todo-backend > /tmp/backend-manifest.yaml` (validate YAML output)
- [ ] T039 [P] Template frontend chart: `helm template todo-frontend k8s/helm-charts/todo-frontend > /tmp/frontend-manifest.yaml` (validate YAML output)
- [ ] T040 [P] Dry-run backend install: `helm install --dry-run todo-backend k8s/helm-charts/todo-backend --set image.pullPolicy=Never`
- [ ] T041 [P] Dry-run frontend install: `helm install --dry-run todo-frontend k8s/helm-charts/todo-frontend --set image.pullPolicy=Never`

### Minikube Deployment for User Story 1

- [ ] T042 Start Minikube cluster: `minikube start --driver=docker --cpus=4 --memory=8192`
- [ ] T043 Verify cluster ready: `minikube status` (Running, Ready)
- [ ] T044 Load backend image into Minikube: `minikube image load todo-backend:latest`
- [ ] T045 Load frontend image into Minikube: `minikube image load todo-frontend:latest`
- [ ] T046 Verify images loaded: `minikube image ls | grep -E "todo-frontend|todo-backend"`
- [ ] T047 Create Kubernetes Secret (manual): `kubectl create secret generic app-secrets --from-literal=DATABASE_URL=... --from-literal=BETTER_AUTH_SECRET=... --from-literal=COHERE_API_KEY=...`
- [ ] T048 Deploy backend with Helm: `helm install todo-backend k8s/helm-charts/todo-backend --set image.pullPolicy=Never`
- [ ] T049 Deploy frontend with Helm: `helm install todo-frontend k8s/helm-charts/todo-frontend --set image.pullPolicy=Never`
- [ ] T050 Wait for backend pod Ready: `kubectl wait --for=condition=ready pod -l app=todo-backend --timeout=60s`
- [ ] T051 Wait for frontend pod Ready: `kubectl wait --for=condition=ready pod -l app=todo-frontend --timeout=60s`

### End-to-End Validation for User Story 1

- [ ] T052 Verify pods Running: `kubectl get pods` (both pods Running and Ready 1/1)
- [ ] T053 Verify services created: `kubectl get svc` (todo-frontend NodePort, todo-backend ClusterIP)
- [ ] T054 Check backend health: `kubectl port-forward svc/todo-backend 8000:8000 &` then `curl http://localhost:8000/health`
- [ ] T055 Access frontend via Minikube: `minikube service todo-frontend` (browser opens, login page loads)
- [ ] T056 [P] Login with test credentials (verify frontend → backend auth flow working)
- [ ] T057 [P] Create a test task in UI (verify frontend → backend → database flow)
- [ ] T058 [P] Send a chat message (verify Cohere API integration working, response appears)
- [ ] T059 [P] Verify task persisted in database (logout, login again, task still exists)
- [ ] T060 [P] Multi-user isolation test: Login as User B, verify User A's task not visible, create User B task, verify isolation

### Documentation & Commit for User Story 1

- [ ] T061 Create k8s/DEMO.md with step-by-step demo walkthrough (minikube start → helm install → browser access)
- [ ] T062 Document Dockerfile generation in commit message: "docker: Add multi-stage Dockerfiles (generated via Gordon AI)"
- [ ] T063 Document Helm chart generation in commit messages (include sanitized kubectl-ai prompts)
- [ ] T064 Commit Phase 1 work: "phase4: Complete Minikube deployment with Docker images and Helm charts"

**Checkpoint**: User Story 1 complete – Minikube demo fully functional, pods running, frontend accessible, chatbot working with Cohere, user isolation enforced

---

## Phase 4: User Story 2 – Security Engineer Validates Secrets Management and Non-Root Containers (Priority: P1)

**Goal**: Verify no hardcoded secrets, non-root containers, proper secret mounting, resource limits

**Independent Test**: Inspect Dockerfiles for UID 1000, verify no secrets in manifests, run `kubectl get secrets`, exec into pod and verify env vars mounted correctly

### Dockerfile Security Validation for User Story 2

- [ ] T065 Inspect frontend Dockerfile: Verify non-root user `USER appuser` with UID 1000 present
- [ ] T066 Inspect backend Dockerfile: Verify non-root user `USER appuser` with UID 1000 present
- [ ] T067 Verify no hardcoded secrets in frontend Dockerfile (search for DATABASE_URL, BETTER_AUTH_SECRET, COHERE_API_KEY – should be none)
- [ ] T068 Verify no hardcoded secrets in backend Dockerfile (same search)
- [ ] T069 Test frontend image runs as non-root: `docker run todo-frontend id` (should show UID 1000, not 0)
- [ ] T070 Test backend image runs as non-root: `docker run todo-backend id` (should show UID 1000, not 0)

### Helm Chart Security Validation for User Story 2

- [ ] T071 Inspect frontend deployment template: Verify no plain-text secrets in `spec.template.spec.env` (should only reference secretRef)
- [ ] T072 Inspect backend deployment template: Verify no plain-text secrets (same)
- [ ] T073 Inspect frontend values.yaml: Verify DATABASE_URL, BETTER_AUTH_SECRET, COHERE_API_KEY not present as values (only `secrets: app-secrets` reference)
- [ ] T074 Inspect backend values.yaml: Verify no hardcoded secrets
- [ ] T075 Search all Helm templates for literal secret values: `grep -r "DATABASE_URL\|BETTER_AUTH_SECRET\|COHERE_API_KEY" k8s/` (should return only comments/documentation, no values)

### Kubernetes Secret Validation for User Story 2

- [ ] T076 Verify Kubernetes Secret exists: `kubectl get secrets app-secrets -o yaml` (should show 3 keys, all base64-encoded)
- [ ] T077 Verify all 3 required secrets mounted: `kubectl exec <backend-pod> env | grep -E "DATABASE_URL|BETTER_AUTH_SECRET|COHERE_API_KEY"` (all 3 should appear)
- [ ] T078 Verify env var values are populated (not empty): Check that each env var has a non-empty value
- [ ] T079 Verify no secrets in ConfigMaps: `kubectl get configmaps` (should not contain DATABASE_URL, BETTER_AUTH_SECRET, COHERE_API_KEY)

### Resource Limits Validation for User Story 2

- [ ] T080 Verify frontend deployment has resource requests: `kubectl get deployment todo-frontend -o yaml | grep -A5 "resources:"`
- [ ] T081 Verify backend deployment has resource requests: `kubectl get deployment todo-backend -o yaml | grep -A5 "resources:"`
- [ ] T082 Verify resource limits prevent OOM: Frontend limits < 256Mi, backend limits < 512Mi (reasonable for Minikube)

### Documentation & Commit for User Story 2

- [ ] T083 Document security validation results in k8s/TROUBLESHOOTING.md
- [ ] T084 Commit security validation: "k8s: Verify non-root containers, secret mounting, no hardcoded secrets"

**Checkpoint**: User Story 2 complete – All security best practices validated, no hardcoded secrets, non-root containers confirmed

---

## Phase 5: User Story 3 – AI-Assisted DevOps Tools Demonstrate Spec-Driven Infrastructure Creation (Priority: P1)

**Goal**: Show AI tool usage traceability in commits and specs, demonstrate spec-driven infrastructure generation

**Independent Test**: Review commit history for Gordon/kubectl-ai/Kagent mentions, examine `/specs/infra/` specs, verify generated artifacts match specs

### Infrastructure Specifications for User Story 3

- [ ] T085 Complete `specs/infra/minikube-deployment.md`: Full step-by-step deployment guide with all Minikube commands
- [ ] T086 Complete `specs/infra/helm-charts.md`: Helm chart design specification (Chart structure, values.yaml format, probe configuration)
- [ ] T087 Complete `specs/infra/docker-gordon.md`: Document Gordon AI usage patterns with example prompts for multi-stage Dockerfile generation
- [ ] T088 Complete `specs/infra/ai-devops.md`: Document kubectl-ai and Kagent usage patterns with example prompts and cluster analysis output

### AI Tool Usage Documentation for User Story 3

- [ ] T089 Add commit message for Dockerfiles: Include Gordon AI tool name and sanitized prompt excerpt
- [ ] T090 Add commit message for Helm charts: Include kubectl-ai tool name and sanitized prompt excerpt
- [ ] T091 Add commit message for validation: Include Kagent cluster health analysis results
- [ ] T092 Create specs/infra/PROMPTS.md documenting all AI tool prompts used (sanitized versions)

### Traceability Validation for User Story 3

- [ ] T093 Review commit history: Verify at least 3 commits mention "Gordon", "kubectl-ai", or "Kagent"
- [ ] T094 Verify Dockerfiles match docker-gordon.md spec: Multi-stage, image sizes < targets, ports correct, health checks present
- [ ] T095 Verify Helm charts match helm-charts.md spec: Chart structure correct, values.yaml configurable, probes present
- [ ] T096 Cross-reference specs/infra/minikube-deployment.md with actual deployment commands used
- [ ] T097 Cross-reference generated artifacts with their specification requirements

### Documentation & Commit for User Story 3

- [ ] T098 Create README.md Phase IV section: "AI-Assisted DevOps Excellence" documenting Gordon, kubectl-ai, Kagent usage
- [ ] T099 Commit AI tool documentation: "docs: Document AI-assisted DevOps process (Gordon, kubectl-ai, Kagent)"

**Checkpoint**: User Story 3 complete – AI tool usage fully traceable, specs-first approach demonstrated, commit history shows systematic development

---

## Phase 6: User Story 4 – Multi-Stage Docker Builds for Image Optimization (Priority: P2)

**Goal**: Verify multi-stage builds, image sizes optimized, build efficiency reasonable

**Independent Test**: Build both images, verify < 200MB (frontend) and < 400MB (backend), inspect layers for efficiency

### Dockerfile Optimization Analysis for User Story 4

- [ ] T100 Analyze frontend Dockerfile structure: Verify multi-stage pattern (FROM...AS builder, final FROM with COPY from builder)
- [ ] T101 Analyze backend Dockerfile structure: Verify multi-stage pattern
- [ ] T102 Inspect frontend image layers: `docker history todo-frontend:latest | head -20` (verify no bloated layers > 100MB)
- [ ] T103 Inspect backend image layers: `docker history todo-backend:latest | head -20` (verify efficient layering)

### Image Size Validation for User Story 4

- [ ] T104 [P] Build frontend image and measure: `docker build -f docker/frontend.Dockerfile -t todo-frontend:test .` → verify < 200MB
- [ ] T105 [P] Build backend image and measure: `docker build -f docker/backend.Dockerfile -t todo-backend:test .` → verify < 400MB
- [ ] T106 [P] Verify build times: Frontend build < 2 minutes, backend build < 2 minutes (reasonable for CI/CD)

### Layer Efficiency Validation for User Story 4

- [ ] T107 Confirm no redundant layers: `docker history todo-frontend:latest | wc -l` (reasonable layer count, no duplicates)
- [ ] T108 Confirm no redundant layers in backend image
- [ ] T109 Verify build cache efficiency: Rebuild images, confirm cached layers reused (second build faster than first)

### Documentation & Commit for User Story 4

- [ ] T110 Document image optimization results in k8s/TROUBLESHOOTING.md: Size, layer count, build times
- [ ] T111 Commit optimization results: "docker: Verify multi-stage builds, image sizes < targets, build efficiency"

**Checkpoint**: User Story 4 complete – Multi-stage builds verified, image sizes optimized, layer efficiency confirmed

---

## Phase 7: User Story 5 – Helm Chart Configurability and Reusability (Priority: P2)

**Goal**: Verify Helm charts fully configurable, values.yaml drives all parameters, charts are reusable

**Independent Test**: Deploy charts with custom values (replicas, image tags, resource limits), verify changes propagate without template edits

### Helm Chart Configurability Validation for User Story 5

- [ ] T112 Test frontend chart parameter configurability: Modify values.yaml `replicaCount: 2`, redeploy, verify 2 pods (instead of 1)
- [ ] T113 Test backend chart parameter configurability: Modify `replicaCount: 2`, redeploy, verify 2 pods
- [ ] T114 Test image tag override: Modify `image.tag: v2`, redeploy, verify pods restart with new image tag
- [ ] T115 Test resource limit override: Modify `resources.limits.memory`, redeploy, verify deployment reflects new limits

### Helm Template Best Practices Validation for User Story 5

- [ ] T116 Inspect frontend templates: Verify no hardcoded config in deployment.yaml (all values reference `.Values.*`)
- [ ] T117 Inspect backend templates: Verify no hardcoded config (all parameterized via values)
- [ ] T118 Verify _helpers.tpl usage: Confirm template helpers reduce duplication (labels, selectors, resource blocks)
- [ ] T119 Verify Helm linting passes: `helm lint k8s/helm-charts/todo-frontend` and `helm lint k8s/helm-charts/todo-backend` (no errors or warnings)

### Values Documentation for User Story 5

- [ ] T120 Add comments to frontend values.yaml: Each parameter documented with purpose and valid values
- [ ] T121 Add comments to backend values.yaml: Document all configurable parameters
- [ ] T122 Create k8s/VALUES-REFERENCE.md: Detailed reference for all Helm chart parameters

### Chart Reusability Validation for User Story 5

- [ ] T123 Verify frontend chart can be installed to different namespace: `helm install todo-frontend-test k8s/helm-charts/todo-frontend -n test-ns`
- [ ] T124 Verify backend chart can be installed multiple times with different names: `helm install todo-backend-prod k8s/helm-charts/todo-backend`
- [ ] T125 Test chart values override from CLI: `helm install todo-frontend --values custom-values.yaml k8s/helm-charts/todo-frontend`

### Documentation & Commit for User Story 5

- [ ] T126 Document Helm configurability patterns in k8s/HELM-GUIDE.md
- [ ] T127 Commit chart documentation: "k8s: Document Helm chart configurability and reusability patterns"

**Checkpoint**: User Story 5 complete – Helm charts fully configurable, reusable, well-documented

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final documentation, debugging guides, demo readiness, cross-cutting validation

- [ ] T128 [P] Create k8s/TROUBLESHOOTING.md with comprehensive debugging guide (pod failures, network issues, secrets mounting)
- [ ] T129 [P] Create k8s/ROLLBACK.md with rollback procedures and recovery strategies
- [ ] T130 [P] Update root README.md with Phase IV section: Setup instructions, demo walkthrough, screenshot
- [ ] T131 Update `.specify/memory/constitution.md` to reference all Phase IV artifacts
- [ ] T132 Create .env.example with all required Phase IV variables documented
- [ ] T133 Verify all infrastructure specs complete and accurate (specs/infra/*.md)
- [ ] T134 Validate all Phase IV files exist and are readable: docker/*, k8s/*, specs/5-k8s-deployment/*
- [ ] T135 [P] Run full E2E demo walkthrough following k8s/DEMO.md (from `minikube start` to working app in < 5 minutes)
- [ ] T136 [P] Verify all acceptance criteria from spec.md met (pods running, frontend accessible, chatbot working, user isolation enforced)
- [ ] T137 Test clean Minikube deletion and re-deployment: `minikube delete` → redeploy entire stack → verify full functionality
- [ ] T138 [P] Create GitHub issues or commit tags for all Phase IV-related work for judges
- [ ] T139 Final validation: Review all commits, verify AI tool usage documented, spec-driven approach demonstrated
- [ ] T140 Create k8s/JUDGE-DEMO.md: Judge-specific walkthrough (emphasizing AI-assisted DevOps, cloud-native patterns, security best practices)

**Checkpoint**: Phase IV complete – All artifacts polished, documentation comprehensive, ready for hackathon submission

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies – can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion – **BLOCKS all user stories**
- **User Stories (Phases 3–7)**: All depend on Foundational phase completion
  - **US1, US2, US3** (P1): Can proceed sequentially or in parallel after Foundational
  - **US4, US5** (P2): Can proceed in parallel after US1–US3 or after Foundational
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1 – MVP)**: Can start after Foundational – No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational – Independent security validation; can run in parallel with US1
- **User Story 3 (P1)**: Can start after Foundational – Independent documentation; can run in parallel with US1 & US2
- **User Story 4 (P2)**: Can start after Foundational – Independent optimization; can run in parallel with US5
- **User Story 5 (P2)**: Can start after Foundational – Independent validation; can run in parallel with US4

### Within Each User Story

- Research/specs first, then implementation
- Docker/Helm generation before deployment
- Validation before E2E testing
- Documentation after implementation

### Parallel Opportunities

**After Foundational (Phase 2) Complete**:

```bash
# All these can run in parallel:
- User Story 1: Dockerfiles → Helm → Deployment → Validation
- User Story 2: Security validation (inspects artifacts from US1)
- User Story 3: Documentation (uses artifacts from US1 & US2)

# After US1–US3 complete:
- User Story 4: Image optimization analysis (parallel)
- User Story 5: Helm chart validation (parallel)

# Finally:
- Phase 8: Polish & Cross-Cutting (depends on all stories)
```

---

## Parallel Example: User Story 1 Docker Generation & Validation

```bash
# These can run in parallel (different files):
T015: Generate frontend Dockerfile (docker/frontend.Dockerfile)
T016: Generate backend Dockerfile (docker/backend.Dockerfile)

# After both images built, these can run in parallel:
T019: Verify frontend size < 200MB
T020: Verify backend size < 400MB
T021: Smoke test frontend health
T022: Smoke test backend health
```

---

## Implementation Strategy

### MVP First (User Stories 1, 2, 3)

1. Complete Phase 1: Setup ✓
2. Complete Phase 2: Foundational ✓
3. Complete Phase 3: User Story 1 (Core Deployment)
4. Complete Phase 4: User Story 2 (Security)
5. Complete Phase 5: User Story 3 (AI Traceability)
6. **STOP and VALIDATE**: Full demo working, security validated, AI usage documented
7. Deploy for hackathon demo

### Full Delivery (All User Stories)

After MVP demo works:

6. Complete Phase 6: User Story 4 (Image Optimization)
7. Complete Phase 7: User Story 5 (Helm Configurability)
8. Complete Phase 8: Polish & Cross-Cutting
9. Final validation: All acceptance criteria met
10. Submit for hackathon

### Parallel Team Strategy (With Multiple Developers)

1. **Team completes Phase 1 + 2 together** (Setup + Foundational = 2–3 hours)
2. **Once Foundational done**:
   - Developer A: User Story 1 (Deployment) – 4–5 hours
   - Developer B: User Story 2 (Security) – 2–3 hours (can start after US1 artifacts available)
   - Developer C: User Story 3 (AI Docs) – 2–3 hours (can start after US1 & US2)
3. **Stories complete and integrate** (US1–US3 in parallel = 8–12 hours vs sequential = 12–16 hours)
4. **Optional – optimize** (US4 & US5 in parallel = 3–4 hours)
5. **Polish** (Phase 8 = 2–3 hours)

---

## Implementation Notes

- **[P] tasks**: Different files, no interdependencies – execute in parallel
- **[Story] label**: Maps task to specific user story for traceability and independence
- **Each user story**: Independently completable, testable, and deployable
- **Commit after**: Each major task or logical group (e.g., after all Dockerfiles built and tested)
- **Stop at checkpoints**: Validate story independently before moving to next
- **Avoid**: Vague tasks, same-file conflicts, cross-story dependencies that break independence
- **AI tool usage**: Every commit involving AI generation must mention the tool (Gordon, kubectl-ai, Kagent)

---

## Success Criteria

### Per User Story

| Story | Success Criteria |
|-------|------------------|
| **US1** | Pods running in < 60s; frontend accessible < 30s; chatbot responds < 10s; user isolation enforced; all SM acceptance scenarios pass |
| **US2** | No hardcoded secrets; non-root containers confirmed; all 3 secrets mounted; resources configured; all acceptance scenarios pass |
| **US3** | ≥3 commits mention Gordon/kubectl-ai/Kagent; specs/infra/ complete; artifacts match specs; traceability clear |
| **US4** | Frontend < 200MB; backend < 400MB; multi-stage builds verified; layers efficient; build time < 2 min |
| **US5** | Charts lint clean; parameters configurable via values.yaml; deployment scales correctly; reusable across namespaces |

### Overall

- All 5 user stories complete and passing
- All 140 tasks checked off
- Full E2E demo works in < 5 minutes
- Judges can reproduce without errors
- AI-assisted DevOps traceability clear
- Phase II–III code unchanged, fully functional

---

## Time Estimates (For Planning)

| Phase | Duration | Notes |
|-------|----------|-------|
| **Phase 1** | 30 min | Setup directories, templates |
| **Phase 2** | 2–3 hours | Research, best practices, docs |
| **Phase 3 (US1)** | 4–5 hours | Dockerfiles, Helm, deployment – **CRITICAL PATH** |
| **Phase 4 (US2)** | 2–3 hours | Security validation (can parallel with Phase 3) |
| **Phase 5 (US3)** | 2–3 hours | Documentation (can parallel with Phase 3 & 4) |
| **Phase 6 (US4)** | 1–2 hours | Image optimization (after US1) |
| **Phase 7 (US5)** | 1–2 hours | Helm validation (after US1) |
| **Phase 8** | 2–3 hours | Polish, final demo, submission |
| **TOTAL** | **8–12 hours (sequential)** or **8–9 hours (parallel)** | Parallel execution with team = faster |

---

## Next Steps

1. **Assign tasks** to team members or execute sequentially
2. **Complete Phase 1 & 2** (Setup + Foundational) together
3. **Execute Phase 3** (US1 – MVP) to get working demo
4. **Validate independently** at each checkpoint
5. **Continue with US2–US5** for full feature set
6. **Phase 8 Polish** for hackathon submission
7. **Final validation** before demo/submission

---

## References

- Feature Spec: `/specs/5-k8s-deployment/spec.md`
- Implementation Plan: `/specs/5-k8s-deployment/plan.md`
- Research & Decisions: `/specs/5-k8s-deployment/research.md` (to be generated)
- Docker Patterns: `/specs/infra/docker-gordon.md` (to be generated)
- Helm Patterns: `/specs/infra/helm-charts.md` (to be generated)
- Deployment Guide: `/specs/infra/minikube-deployment.md` (to be generated)
- AI Tool Usage: `/specs/infra/ai-devops.md` (to be generated)
