# Phase II–III–IV Todo Full-Stack Web Application + AI Chatbot + Kubernetes Constitution

> **Purpose**: Establish non-negotiable principles and standards for integrated Phase II (persistent multi-user TODO web app), Phase III (AI-powered conversational chatbot), and Phase IV (local Kubernetes deployment) development. All phases share backend infrastructure, containerization, orchestration, authentication, database, and API layers for seamless integration, demo reproducibility, and zero duplication.

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

All code is generated from specifications, never written manually. Specifications are the source of truth. Every feature, API endpoint, database table, UI component, MCP tool, and Cohere integration must have a dedicated spec file before implementation begins.

**Non-negotiable rules**:
- Every feature/API/database/UI/MCP/AI change requires a spec in `/specs/`
- No code generation without approved specification
- Specs are written before any implementation (TDD applies to specs too)
- All work is traceable: specification → plan → tasks → implementation → tests
- Hackathon judges review spec history as proof of systematic development
- Phase III specs extend Phase II patterns; no redundant specs for shared infrastructure

### II. Strict User Isolation (Security-Critical)

Each user sees and modifies ONLY their own tasks and conversations. No data leakage, no cross-user access.

**Non-negotiable rules**:
- Every database query MUST filter by `user_id` from authenticated JWT token
- No endpoint may return or modify another user's data (tasks, conversations, messages)
- All API responses filtered before transmission
- Tests MUST include cross-user attack scenarios
- Violation is a critical security breach; must be caught and fixed immediately
- Conversation and message tables include `user_id` indexed for efficient isolation

### III. JWT-Based Stateless Authentication

Authentication via JWT tokens with shared `BETTER_AUTH_SECRET` environment variable. No session storage; verification at every request. Applies to all endpoints: Phase II CRUD, Phase III chat, and MCP tools.

**Non-negotiable rules**:
- All API endpoints require `Authorization: Bearer <token>` header
- Backend extracts `user_id` from JWT and uses for all query filtering
- Frontend attaches JWT automatically via centralized API client (`/lib/api.ts`)
- 401 Unauthorized for missing/invalid/expired tokens
- 403 Forbidden for valid token but insufficient permissions (e.g., accessing another user's data)
- Better Auth manages user table; backend does NOT manage users
- Shared secret identical on frontend and backend
- Cohere API calls are backend-only; user never sees API keys or credentials

### IV. Technology Stack Fidelity (No Deviations)

Stack is fixed and non-negotiable. Adding dependencies requires explicit constitutional amendment.

**Frontend**:
- Next.js 16+ (App Router only, no Pages Router)
- TypeScript (strict mode)
- Tailwind CSS + shadcn/ui
- Better Auth (for JWT support)
- Cohere SDK (optional; if used for chatbot UI)

**Backend**:
- Python FastAPI (latest)
- SQLModel (ORM, async)
- Neon Serverless PostgreSQL
- Cohere SDK (for chat completions, intent parsing, tool calling)
- Official MCP SDK (Model Context Protocol for task tools)

**Package Management**:
- Backend: UV
- Frontend: npm/pnpm

**No additional external dependencies beyond the above.**

### V. Modular Architecture & Monorepo Structure

Single repository with organized subdirectories ensures scalability and clarity. Phase II and Phase III share backend; frontend UI extends Phase II with chatbot component. Phase IV adds containerization and orchestration layers without modifying Phase II–III code.

**Structure**:
- `/specs/` — All specifications (overview, architecture, features, api, database, ui, mcp-tools, infra)
- `/frontend/` — Next.js application extending Phase II with chatbot component (unchanged by Phase IV)
- `/backend/` — FastAPI application serving both Phase II tasks and Phase III chat (unchanged by Phase IV)
- `/agents/` — Agentic orchestrators (chatbot-orchestrator, conversation-manager, mcp-tool-executor, user-info-provider, etc.)
- `/skills/` — Stateful skill modules wrapping API/MCP calls for agents
- `/docker/` — Container definitions (frontend.Dockerfile, backend.Dockerfile) ⭐ Phase IV
- `/k8s/` — Kubernetes/Helm charts and manifests (helm-charts/, manifests/, secrets/) ⭐ Phase IV
- `/.specify/` — Spec-Kit Plus templates, scripts, and memory
- `/history/prompts/` — Prompt History Records (PHR)
- `/history/adr/` — Architecture Decision Records (ADR)

### VI. Testability & Quality Gates

All code must be testable and tested. Integration tests verify full flows including authentication, user isolation, and chatbot workflows.

**Non-negotiable rules**:
- Backend: Unit tests for models and routes; integration tests for API contracts (Phase II CRUD + Phase III chat)
- Frontend: Component tests; end-to-end tests for auth flows and task CRUD
- Chatbot integration: Test intent parsing, tool invocation, conversation persistence
- Cross-user security tests: Attempt to access another user's tasks/conversations; must fail with 401/403
- No code merge without passing tests
- Code coverage expectations: Backend routes ≥80%, frontend components ≥70%

### VII. API Design Standards

RESTful API for Phase II tasks; stateless JSON endpoint for Phase III chat. Both require JWT authentication and filter by user ownership.

**Non-negotiable rules**:
- **Phase II (Task CRUD)**: Base path `/api/tasks` (no `{user_id}` in URL; derived from JWT)
  - Standard HTTP methods: GET (read), POST (create), PUT (update), PATCH (partial), DELETE (remove)
  - Example: `GET /api/tasks`, `POST /api/tasks`, `PUT /api/tasks/{id}`, `DELETE /api/tasks/{id}`
- **Phase III (Chat)**: Path `/api/{user_id}/chat`
  - Single POST endpoint: `POST /api/{user_id}/chat`
  - Request: `{ "conversation_id": "string (optional)", "message": "string" }`
  - Response: `{ "conversation_id": "string", "response": "string", "tool_calls": "[...optional]" }`
- All responses in JSON; no HTML
- Status codes: 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error
- Request/response schemas documented and validated via Pydantic
- Query parameters for filtering/sorting Phase II tasks (e.g., `?status=pending&sort=created_at`)

### VIII. Database Design & Normalization

Proper schema design with indexes, constraints, and relationships for performance and correctness. Phase II tasks + Phase III conversations/messages coexist in shared Neon PostgreSQL.

**Non-negotiable rules**:
- **Tasks** (`tasks` table): `id`, `user_id` (indexed, FK), `title`, `description`, `completed`, `created_at`, `updated_at`
- **Conversations** (`conversations` table): `id`, `user_id` (indexed, FK), `created_at`, `updated_at`
- **Messages** (`messages` table): `id`, `user_id` (indexed, FK), `conversation_id` (indexed, FK), `role` (user/assistant), `content`, `tool_calls` (JSON string, optional), `created_at`
- Foreign key constraints: all `user_id` reference Better Auth user table; `conversation_id` → `conversations`
- Indexes on: `user_id`, `created_at`, `completed` (Phase II); `user_id`, `conversation_id` (Phase III)
- Timestamps: `created_at` (immutable), `updated_at` (on insert and update)
- No NULL titles (Phase II); no NULL content (Phase III); default `completed=false` (Phase II)

### IX. Code Quality & Simplicity (YAGNI)

Keep solutions simple, focused, and maintainable. Avoid over-engineering. Apply equally to Phase II CRUD and Phase III AI workflows.

**Non-negotiable rules**:
- Minimum viable diff: only code required for the feature
- No unrelated refactoring in the same commit
- No premature abstractions; DRY applies after 3+ uses
- Type safety: all functions have type hints (Python, TypeScript)
- Comments only for non-obvious logic (e.g., Cohere API quirks, MCP tool semantics)
- Clear error messages; avoid cryptic codes
- Prompt engineering: Cohere system prompts concise and focused; no bloat

### X. Traceability & Documentation

All decisions, code, and tests are traceable for hackathon judging and future reference. Phase III specs inherit and extend Phase II traceability patterns.

**Non-negotiable rules**:
- Prompt History Records (PHR) created for every significant user input
- Architecture Decision Records (ADR) for major decisions (e.g., Cohere vs OpenAI choice, stateless chat design)
- Code references in documentation (e.g., `backend/routes/chat.py:42`)
- Commit messages reference spec/ADR/PHR when applicable
- Final submission includes complete `/history/` for audit trail
- PHR routing: constitution → `history/prompts/constitution/`, feature-specific → `history/prompts/<feature>/`, general → `history/prompts/general/`

### XI. AI & Agentic Workflow Governance (Phase III)

Phase III integrates Cohere API for natural language understanding and tool orchestration. All AI logic is backend-only; frontend is UI only. MCP tools are stateless wrappers around secure task operations.

**Non-negotiable rules**:
- **Cohere API**: Use for chat completions, intent parsing, and simulated agent behavior (multi-step reasoning or custom chaining)
- **MCP Tools**: 5 stateless tools—`add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`—DB-backed, user-isolated
- **Agents**: Orchestrate tool calls and Cohere responses; live in `/agents/` (chatbot-orchestrator, conversation-manager, mcp-tool-executor, user-info-provider)
- **Skills**: Stateful wrappers in `/skills/` calling API or Cohere; reusable across agents
- **Prompt Security**: API keys (COHERE_API_KEY) stored in `.env`; never exposed to frontend; rate-limit Cohere calls if possible; log anonymized usage
- **Conversation Persistence**: All chat history stored in Neon `conversations`/`messages` tables; conversation_id persisted locally on frontend
- **Stateless Design**: Each `/api/{user_id}/chat` request includes full conversation history (retrieved from DB); Cohere receives only necessary context
- **Tool Calling**: Cohere API responses include tool calls; backend executes via MCP tools; results returned to Cohere for synthesis into final response
- **Error Handling**: Cohere timeouts/rate limits → 503 Service Unavailable; API errors logged anonymously; user sees generic friendly message

### XII. Cloud-Native Containerization & Orchestration (Phase IV)

Phase IV deploys Phase II + III application to local Kubernetes (Minikube) using Docker containers, Helm charts, and AI-assisted infrastructure tooling. Zero rewrites; 100% code reuse from Phases II–III.

**Non-negotiable rules**:

**Docker & Containerization**:
- Frontend Dockerfile: Node.js 20-alpine build stage → nginx:alpine serve stage (multi-stage mandatory)
- Backend Dockerfile: Python 3.12-slim → UV package manager → uvicorn/gunicorn server (multi-stage mandatory)
- No root users in containers; use non-root UID (e.g., 1000 for app user)
- Health checks: readiness & liveness probes defined in Kubernetes manifests (not Dockerfiles)
- Image tags: `<app-name>:latest` or `:v1` for local Minikube use
- Build & load: Use `minikube image load` for local registry or Docker Desktop integration
- Gordon AI used for Dockerfile generation/optimization wherever possible; show AI prompts in commit history

**Kubernetes & Helm Charts**:
- Local cluster: Minikube (docker driver on Windows, preferred for simplicity)
- One Helm chart per service (frontend & backend separate charts)
- Chart structure: `Chart.yaml`, `values.yaml`, `templates/` (deployment.yaml, service.yaml, optional ingress.yaml)
- Deployments: configurable replicas (default 1–2), rollingUpdate strategy, resource requests/limits
- Services: ClusterIP for backend, NodePort or LoadBalancer for frontend access
- Probes: readinessProbe (HTTP GET /health or equiv, 10s timeout), livenessProbe (same, 30s timeout)
- Values: all configurable env vars, image tags, replicas, resources defined in `values.yaml`
- kubectl-ai or Kagent used for manifest generation, debugging, and cluster health analysis

**Secret & Configuration Management**:
- NEVER hardcode secrets (DATABASE_URL, BETTER_AUTH_SECRET, COHERE_API_KEY) in charts or manifests
- Kubernetes Secrets created via `kubectl create secret generic` or Helm `--set-string` at deployment time
- Secrets mounted as environment variables in Deployment spec (NOT ConfigMaps)
- `.env` files (local) and `.env.example` (committed) for development reference
- Helm values can reference pre-created secrets by name; charts assume secrets exist before deployment

**Local Minikube Deployment Flow**:
1. `minikube start --driver=docker` to initialize cluster
2. Create Kubernetes Secrets: `kubectl create secret generic app-secrets --from-literal=DATABASE_URL=... --from-literal=BETTER_AUTH_SECRET=... --from-literal=COHERE_API_KEY=...`
3. Build and load Docker images: `docker build -f docker/frontend.Dockerfile -t todo-frontend:latest .` → `minikube image load todo-frontend:latest`
4. Helm install: `helm install todo-frontend ./k8s/helm-charts/todo-frontend --values values-override.yaml` and `helm install todo-backend ./k8s/helm-charts/todo-backend --values values-override.yaml`
5. Access frontend: `minikube service todo-frontend` (opens browser with NodePort URL)
6. Validate: `kubectl get pods`, `kubectl logs`, `minikube dashboard` for visual inspection

**AI-Assisted DevOps Workflow**:
- **Gordon AI**: Use for Dockerfile optimization, multi-stage design, image size reduction
- **kubectl-ai**: Use for manifest generation ("generate Helm chart for FastAPI backend with 2 replicas"), debugging ("why is pod failing?"), scaling decisions
- **Kagent**: Use for cluster health analysis, resource optimization, bottleneck identification
- Spec-driven infra: Write infrastructure specs first → AI generates YAML/Helm → validate → apply
- Show AI usage: Commit messages include AI tool names and prompts (e.g., "infra: Add Helm chart (generated via kubectl-ai prompt)")

**Monorepo Structure Addition for Phase IV**:
```
/docker/
  ├── frontend.Dockerfile     # Multi-stage Next.js build
  └── backend.Dockerfile      # Multi-stage FastAPI build

/k8s/
  ├── helm-charts/
  │   ├── todo-frontend/
  │   │   ├── Chart.yaml
  │   │   ├── values.yaml
  │   │   └── templates/
  │   │       ├── deployment.yaml
  │   │       ├── service.yaml
  │   │       └── hpa.yaml (optional auto-scaling)
  │   └── todo-backend/
  │       ├── Chart.yaml
  │       ├── values.yaml
  │       └── templates/
  │           ├── deployment.yaml
  │           ├── service.yaml
  │           └── configmap.yaml (non-secret config)
  ├── manifests/               # Optional raw YAML if Helm not used
  └── secrets/                 # Templates only; never commit real values

/specs/infra/
  ├── minikube-deployment.md   # Step-by-step local deployment guide
  ├── helm-charts.md           # Helm chart design and configuration
  ├── docker-gordon.md         # Dockerfile generation strategy (Gordon prompts)
  └── ai-devops.md             # kubectl-ai and Kagent usage patterns
```

**Validation & Testing**:
- Pods reach Running state and pass readiness probes
- Frontend accessible via `minikube service` (NodePort URL works)
- Backend health endpoint `/health` returns 200 OK
- Chat endpoint responds with Cohere reply (verify COHERE_API_KEY secret mounted)
- Database queries work (verify DATABASE_URL secret mounted and Neon accessible)
- No pod crashes; logs clean (check `kubectl logs`)
- User isolation enforced (attempt cross-user access → 403 Forbidden)

**Demo Reliability**:
- App fully functional after: `minikube start` → `kubectl create secret ...` → `helm install ...`
- No manual configuration beyond secret creation
- Single-command demo startup (document in README)
- Dashboard view shows pods running, services healthy
- Judges see: Minikube dashboard, kubectl output, app working end-to-end

## Security & Authentication (Foundation)

### JWT Token Flow

1. **Frontend (Better Auth)**:
   - User signs up/logs in via Better Auth UI
   - Better Auth generates JWT token and stores in secure storage
   - Centralized API client (`/lib/api.ts`) automatically attaches token to all requests

2. **Backend (FastAPI)**:
   - Dependency injection extracts JWT from `Authorization: Bearer <token>` header
   - Shared secret (`BETTER_AUTH_SECRET`) verifies signature
   - Extract `user_id` and user claims; inject into route handlers
   - All database queries filtered by `user_id`
   - Cohere API calls are backend-only; user_id is context for tools, never exposed to Cohere

### Authentication Errors

- **401 Unauthorized**: Missing/invalid/expired token
- **403 Forbidden**: Valid token but data does not belong to authenticated user

### Data Isolation Enforcement

Every route handler (Phase II and Phase III) receives `current_user` dependency containing verified `user_id`. Before returning any data, verify ownership:

```python
# Example: Get task (must belong to current user)
@router.get("/tasks/{id}")
async def get_task(id: int, current_user = Depends(verify_jwt)):
    task = db.query(Task).filter(Task.id == id, Task.user_id == current_user["user_id"]).first()
    if not task:
        raise HTTPException(404)  # Hides whether task exists or belongs to another user
    return task

# Example: Chat endpoint (Phase III)
@router.post("/api/{user_id}/chat")
async def chat(user_id: str, body: ChatRequest, current_user = Depends(verify_jwt)):
    if current_user["user_id"] != user_id:
        raise HTTPException(403)  # User mismatch
    # Fetch conversation (if exists) and messages filtered by user_id
    # Call Cohere with message; fetch MCP tools results; synthesize response
    # Save message exchange to DB; return response
```

### No Session Storage

All state is in JWT. No user sessions in database. Eliminates logout-but-still-valid token race conditions.

### Cohere API Security

- API key stored in `COHERE_API_KEY` environment variable
- Never expose key to frontend or logs
- Cohere calls are backend-only
- User identity communicated to tools via `user_id` parameter, not to Cohere directly
- Rate-limit Cohere calls per user to prevent abuse

## API Specifications (Phase II + Phase III)

### Phase II: Task CRUD Endpoints

| Method | Path | Description | Auth | Filtering |
|--------|------|-------------|------|-----------|
| `GET` | `/api/tasks` | List all user's tasks | JWT | `?status=pending/completed&sort=created_at` |
| `POST` | `/api/tasks` | Create new task | JWT | N/A |
| `GET` | `/api/tasks/{id}` | Get specific task | JWT | Verifies ownership |
| `PUT` | `/api/tasks/{id}` | Update task (full) | JWT | Verifies ownership |
| `PATCH` | `/api/tasks/{id}/complete` | Toggle completion | JWT | Verifies ownership |
| `DELETE` | `/api/tasks/{id}` | Delete task | JWT | Verifies ownership |

### Phase III: Chat Endpoint

| Method | Path | Description | Auth | Input |
|--------|------|-------------|------|-------|
| `POST` | `/api/{user_id}/chat` | Send message, get response | JWT | `{ "conversation_id": "string?", "message": "string" }` |

**Response**:
```json
{
  "conversation_id": "string (UUID)",
  "response": "string (assistant reply)",
  "tool_calls": "[{\"tool\": \"string\", \"args\": {...}}]"
}
```

### Request/Response Schemas

**Create Task** (`POST /api/tasks`):
```json
Request: { "title": "string (required)", "description": "string (optional)" }
Response (201): { "id": int, "user_id": string, "title": string, "description": string, "completed": false, "created_at": "ISO8601", "updated_at": "ISO8601" }
```

**List Tasks** (`GET /api/tasks`):
```json
Response (200): [{ task object }, ...]
```

**Update Task** (`PUT /api/tasks/{id}`):
```json
Request: { "title": "string", "description": "string" }
Response (200): { task object }
```

**Toggle Completion** (`PATCH /api/tasks/{id}/complete`):
```json
Response (200): { task object with updated completed status }
```

**Chat** (`POST /api/{user_id}/chat`):
```json
Request: { "conversation_id": "string (optional)", "message": "string" }
Response (200): {
  "conversation_id": "string",
  "response": "string (assistant reply, may include tool results)",
  "tool_calls": "[optional array of executed tools]"
}
```

## Frontend Standards (Next.js 16+ App Router + Chatbot)

### Architecture

- **Server Components** (default): Fetch data server-side; render HTML
- **Client Components** (`use client`): Only for interactive elements (forms, real-time updates, chatbot UI)
- **Centralized API Client** (`/lib/api.ts`): All HTTP requests go through single client; JWT attached automatically; extended for `/api/chat` calls
- **Layout & Pages**: Organize by feature (e.g., `/app/tasks/page.tsx`, `/app/tasks/[id]/page.tsx`, `/app/chat/page.tsx`)
- **Components**: Reusable shadcn/ui components; minimal custom CSS

### Required Features

**Phase II (Task Management)**:
1. **Auth Guard**: Redirect unauthenticated users to login (Better Auth handles UI)
2. **Task List Page** (`/app/tasks`): Display all user tasks with completion status
3. **Add Task Form**: Create new task (title, optional description)
4. **Edit Task Modal/Form**: Update existing task
5. **Delete Confirmation**: Confirm before deletion
6. **Mark Complete**: Toggle completion status (button or checkbox)

**Phase III (Chatbot)**:
1. **Chat Page** (`/app/chat`): Conversation interface
2. **Message Display**: User messages + assistant responses with markdown/formatting
3. **Message Input**: Text input field with submit button
4. **Conversation Persistence**: Store `conversation_id` in localStorage; fetch history on load
5. **Loading States**: Typing indicator, skeleton loaders while awaiting Cohere response
6. **Error Handling**: Display friendly error messages if chat fails

### Responsive Design

- Mobile-first: Tailwind responsive classes
- Desktop: Full layout with sidebar/navigation
- Dark mode ready: shadcn/ui theme support
- Chat UI: Drawer or full-width panel; message bubbles with author identification

## Backend Standards (FastAPI + SQLModel + Cohere)

### Project Structure

```
backend/
├── main.py                 # FastAPI app, CORS, middleware, lifespan, routes
├── db.py                   # Database connection, session management
├── models.py               # SQLModel tables (Task, Conversation, Message, User via Better Auth)
├── schemas.py              # Pydantic schemas for request/response validation
├── dependencies/
│   └── auth.py             # JWT verification, current_user injection
├── routes/
│   ├── tasks.py            # Task CRUD endpoints (Phase II)
│   └── chat.py             # Chat endpoint (Phase III) with Cohere integration
├── mcp/
│   └── tools.py            # MCP tool implementations (add_task, list_tasks, etc.)
├── services/
│   └── cohere_service.py   # Cohere API wrapper, intent parsing, tool orchestration
├── pyproject.toml          # UV dependencies
└── .env.example            # Environment variable template
```

### Async Patterns

- All route handlers are `async def`
- Database operations use SQLModel async sessions
- Cohere API calls use async HTTP client
- No blocking I/O; use appropriate async libraries

### Error Handling

- Custom `HTTPException` with clear messages
- Proper status codes (400, 401, 403, 404, 503)
- Stack traces logged; generic messages returned to client
- Cohere API errors: log full error, return 503 to frontend

### Cohere Integration

- **Service Layer** (`services/cohere_service.py`): Wrap Cohere SDK calls; handle rate limits, retries, timeouts
- **Chat Endpoint** (`routes/chat.py`): Receive message, fetch conversation history, call Cohere, execute MCP tools, synthesize response
- **Tool Orchestration**: Cohere API responses include tool calls; execute via MCP tools; pass results back to Cohere for final synthesis
- **Prompt Engineering**: System prompts in service layer; concise, focused; include MCP tool descriptions for Cohere context
- **Rate Limiting**: Per-user limits on Cohere calls (e.g., 10 calls/minute) to prevent abuse

### MCP Tool Implementation

- **Stateless**: Tools take `user_id` + parameters; return results
- **Secure**: All operations filtered by `user_id`; no cross-user access
- **Documented**: Tool descriptions provided to Cohere for context
- **Example** (`add_task` MCP tool):
  ```python
  @mcp_tool
  async def add_task(user_id: str, title: str, description: str = None):
      task = Task(user_id=user_id, title=title, description=description)
      db.session.add(task)
      await db.session.commit()
      return {"id": task.id, "title": task.title, "created_at": task.created_at}
  ```

## Testing Standards

### Backend Tests

- **Unit**: Model creation, schema validation, utility functions, Cohere prompt formatting
- **Integration**: Full request/response cycle (Phase II CRUD, Phase III chat), authentication, authorization
- **MCP Tools**: Test each tool with valid/invalid inputs; verify user isolation
- **Cohere Mocking**: Mock Cohere API in tests to avoid real calls and costs
- **Security**: Cross-user access attempts must fail with 401/403

### Frontend Tests

- **Component**: Render, user interaction, async data loading
- **Integration**: Full auth flow, task CRUD workflow, chatbot message exchange
- **E2E**: Login → Create task → Edit → Mark complete → Delete → Open chat → Send message → Receive response

### Coverage & CI/CD

- Backend: 80%+ coverage for routes and models
- Frontend: 70%+ coverage for critical paths
- CI/CD pipeline runs tests on every PR; must pass before merge

## Development Workflow

### Specification Phase

1. Write spec for feature/API/database/UI/MCP/Cohere change
2. User approves spec
3. Plan phase begins

### Planning Phase

1. Architect solution given spec
2. Identify tasks and dependencies
3. Document decisions (ADRs for significant ones)
4. User approves plan

### Implementation Phase

1. Execute tasks in dependency order
2. Generate code from plan using specialized agents
3. Tests written alongside code
4. All changes reference spec/plan/task
5. Commit with traceability information

### Testing Phase

1. All tests pass locally (including Cohere mocks)
2. Code review verifies compliance with constitution
3. Cross-user security tests executed
4. Integration tests verify full flows (Phase II + Phase III)
5. Chatbot workflows verified (intent parsing, tool execution, response synthesis)

### Deployment Readiness

- All specs in `/specs/`
- All decisions in `/history/adr/`
- All prompts in `/history/prompts/`
- All tests passing
- Code coverage ≥ thresholds
- Commit history clean and traceable
- `.env.example` complete with all required variables (BETTER_AUTH_SECRET, COHERE_API_KEY, DATABASE_URL, etc.)

## Governance

### Constitution Authority

This constitution supersedes all other guidance. When conflicts arise, this document is authoritative. Every pull request must verify compliance before merge.

### Amendment Process

1. **Identification**: Current principle/section identified as inadequate
2. **Proposal**: Detailed amendment with rationale and impact on existing code
3. **Approval**: User consent required
4. **Migration**: Changes to dependent code/specs documented
5. **Version Bump**: Semantic versioning applied
6. **Documentation**: Changelog updated; team notified

### Version Numbering

- **MAJOR**: Backward-incompatible principle changes or removals (e.g., Phase II → Phase II+III integration, AI framework swap)
- **MINOR**: New principles or significant expansions (e.g., adding MCP tools, Cohere integration)
- **PATCH**: Clarifications, wording, non-semantic refinements

### Compliance Review

- All specs verified against constitution before approval
- All code generation validated against stack/architecture rules
- Security principles (user isolation, auth, Cohere API safety) verified on every implementation
- Code reviews check: traceability, compliance, tests, simplicity, Cohere prompt quality

### Runtime Guidance

Detailed development guidance in `CLAUDE.md` files at each level:
- Root: `/CLAUDE.md` (constitutional context, spec-driven workflow)
- Frontend: `/frontend/CLAUDE.md` (Next.js patterns, chatbot UI)
- Backend: `/backend/CLAUDE.md` (FastAPI patterns, Cohere integration, MCP tools)

These files evolve with constitution but never contradict it.

### Hackathon Submission Checklist

Before final submission:

- [ ] All Phase II features functional and tested
- [ ] All Phase III chatbot features functional and tested
- [ ] User isolation verified: attempts to access other users' tasks/conversations fail
- [ ] Authentication: all endpoints require valid JWT
- [ ] Cohere API: secure key management; calls backend-only; no exposure to frontend
- [ ] Specs complete: `/specs/` organized and comprehensive (Phase II + Phase III + MCP + Cohere)
- [ ] Architecture decisions documented: `/history/adr/` (including Cohere choice rationale)
- [ ] Prompt history complete: `/history/prompts/` with all major interactions
- [ ] Code references correct: all citations match actual line numbers
- [ ] Tests passing: backend ≥80%, frontend ≥70% coverage
- [ ] Monorepo clean: no stray files, proper structure
- [ ] Documentation: README updated for Phase II + Phase III; setup instructions clear; Cohere API key setup documented
- [ ] Commit history traceable: messages reference specs/decisions
- [ ] Agents/skills functional: chatbot-orchestrator, conversation-manager, mcp-tool-executor, user-info-provider tested
- [ ] Cohere prompts evaluated: system prompts concise, tool descriptions clear, response quality validated

## Sync Impact Report

<!-- Generated: 2026-01-20 -->

### Version Change
- **Old**: 2.0.0 (Phase II + Phase III integration)
- **New**: 2.1.0 (Phase II + Phase III + Phase IV Kubernetes deployment)

### Rationale for MINOR Version Bump
- Phase IV (Kubernetes/Docker/Helm orchestration) is **additive to existing Phases II–III** without breaking changes
- New infrastructure principles govern containerization and local Minikube deployment
- Zero rewrites of Phase II–III code; only new `/docker/` and `/k8s/` directories added
- AI-assisted DevOps principles (Gordon, kubectl-ai, Kagent) introduce new tooling governance
- Monorepo structure expanded to include infrastructure specifications and manifests
- Version bump type: MINOR (new principles/sections, no removed principles, backward compatible)

### Modified Principles

| Old Title | New Title | Changes |
|-----------|-----------|---------|
| V. Monorepo Structure | V. Modular Architecture & Monorepo Structure | Added `/docker/` and `/k8s/` directories; emphasized Phase IV non-invasiveness |

### New Principles & Sections

| Principle | Content | Scope |
|-----------|---------|-------|
| XII. Cloud-Native Containerization & Orchestration | Docker multi-stage builds, Kubernetes/Helm charts, Minikube deployment, secrets management, AI-assisted DevOps (Gordon, kubectl-ai, Kagent) | Phase IV infrastructure |

### Added Sections

- XII. Cloud-Native Containerization & Orchestration (Docker, Kubernetes, Helm, Minikube, secret management, AI DevOps, validation)
- Updated monorepo structure with `/docker/` and `/k8s/` directories and `/specs/infra/` specifications

### Removed Sections

- None (purely additive to Phases II–III foundation)

### Templates Requiring Updates

| Template | Status | Notes |
|----------|--------|-------|
| `.specify/templates/spec-template.md` | ⚠ Pending | Add Phase IV infrastructure spec sections (Dockerfile design, Helm chart structure, Minikube config) |
| `.specify/templates/plan-template.md` | ⚠ Pending | Add infrastructure planning section; Docker/Helm/Minikube design decisions |
| `.specify/templates/tasks-template.md` | ⚠ Pending | Add task types for Dockerfile creation, Helm chart implementation, k8s manifest generation, validation |
| `/README.md` (root) | ⚠ Pending | Add Phase IV overview, Minikube setup instructions, demo walkthrough, Gordon/kubectl-ai usage examples |
| `/frontend/CLAUDE.md` | ✅ No change | Phase IV uses existing Next.js code; no frontend-specific guidance needed |
| `/backend/CLAUDE.md` | ✅ No change | Phase IV uses existing FastAPI code; no backend-specific guidance needed |

### Follow-Up TODOs

- [ ] Create `specs/infra/minikube-deployment.md` — step-by-step local deployment guide with all secrets, image build, Helm install commands
- [ ] Create `specs/infra/helm-charts.md` — design document for frontend & backend Helm charts (structure, values, templates)
- [ ] Create `specs/infra/docker-gordon.md` — Dockerfile generation strategy using Gordon AI (prompts, optimization patterns)
- [ ] Create `specs/infra/ai-devops.md` — kubectl-ai and Kagent usage patterns (manifest generation, debugging, cluster health)
- [ ] Create `/docker/frontend.Dockerfile` — multi-stage Node 20-alpine → nginx build
- [ ] Create `/docker/backend.Dockerfile` — multi-stage Python 3.12-slim → uvicorn build
- [ ] Create `/k8s/helm-charts/todo-frontend/` — full Helm chart structure and templates
- [ ] Create `/k8s/helm-charts/todo-backend/` — full Helm chart structure and templates
- [ ] Create `/k8s/secrets/` — secret templates (never commit real values)
- [ ] Update `/README.md` — add Phase IV section with Minikube + Helm demo steps
- [ ] Create `.env.example` updates — ensure DOCKER_* and K8S_* variables documented
- [ ] Validate deployment: pods running, frontend accessible, chatbot working, DB connected
- [ ] Demonstrate AI tool usage: show Gordon Dockerfile prompts, kubectl-ai manifest generation, Kagent cluster analysis in commit history

### Backward Compatibility

- **✅ No breaking changes**: Phase II–III code untouched; Phase IV is purely additive infrastructure
- **✅ Development workflow unchanged**: Developers can still `npm run dev` and `python -m uvicorn` locally without Kubernetes
- **✅ Specs remain the same**: Existing Phase II–III specs in `/specs/` apply without modification
- **✅ Database unchanged**: Neon PostgreSQL connection via `DATABASE_URL` secret in Kubernetes; same as local `.env`
- **✅ Authentication unchanged**: JWT via Better Auth; same `BETTER_AUTH_SECRET` used by local and Kubernetes deployments
- **✅ API endpoints unchanged**: Phase II CRUD and Phase III chat endpoints work identically

---

**Version**: 2.1.0 | **Ratified**: 2026-01-12 | **Last Amended**: 2026-01-20
