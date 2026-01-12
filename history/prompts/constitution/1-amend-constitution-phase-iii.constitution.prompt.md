---
id: 1
title: "Amend Constitution to Phase II–III Integration"
stage: constitution
date: 2026-01-12
surface: agent
model: claude-haiku-4-5-20251001
feature: "none"
branch: "main"
user: "hackathon-assistant"
command: "/sp.constitution"
labels: ["phase-iii", "cohere-integration", "mcp-tools", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ".specify/memory/constitution.md"
tests: []
---

## Prompt

You are an expert full-stack system architect and spec-driven developer building the integrated Phase II + Phase III of a hackathon TODO application: a modern multi-user full-stack web app with persistent storage and an AI-powered Todo Chatbot seamlessly integrated into the existing backend.

Adhere strictly to this constitution for all specification writing, planning, code generation, and validation across the entire monorepo. This constitution ensures consistency, security, scalability, traceability, and excellence for hackathon judging, with zero compromises on integration quality.

## 1. Project Overview & Goals
- **Phases**: Integrated Phase II (Todo Full-Stack Web App) + Phase III (AI Todo Chatbot)
- **Objective**: Build a persistent, multi-user TODO web app (Phase II) and seamlessly integrate an AI-powered chatbot (Phase III) that handles all task operations via natural language, using the existing backend infrastructure. The chatbot must manage tasks (add, list, update, delete, mark complete) and provide user info (e.g., logged-in email).
- **Core Features**:
  - Phase II: 5 basic TODO operations (Add, List/View, Update, Delete, Mark Complete/Incomplete) via REST API and responsive UI.
  - Phase III: Conversational chatbot interface for the above features + user info queries, with stateless persistence.
- **Multi-User Requirement**: Strict user isolation – each user sees/modifies only their own tasks/conversations; enforced at DB and API levels.
- **Development Methodology**: 100% spec-driven using Claude Code + Spec-Kit Plus. No manual coding allowed. All work traceable via specs history. Use Agentic Dev Stack for agents/skills.
- **Integration Model**: Chatbot fully embedded in existing backend – no separate services; share DB, auth, and API routes. Frontend UI extends Phase II with chatbot component.
- **Future Compatibility**: Design for scalability (stateless), with easy extension for advanced AI features.
- **AI Adaptation**: Replace OpenAI Agents SDK with Cohere API integration – use Cohere's chat/completion APIs for natural language processing, tool calling, and agent-like behavior (simulate agents via Cohere's multi-step reasoning or custom chaining).

## 2. Technology Stack (Strict – No Deviations)
- **Frontend**: Next.js 16+ (App Router only), TypeScript, Tailwind CSS, shadcn/ui components; extend with Cohere SDK for chatbot UI if needed (or custom shadcn chat).
- **Backend**: Python FastAPI (latest).
- **ORM**: SQLModel (async).
- **Database**: Neon Serverless PostgreSQL.
- **Authentication**: Better Auth (frontend) with JWT plugin enabled; shared BETTER_AUTH_SECRET.
- **AI Framework**: Cohere API (via Cohere SDK) – use for natural language intent parsing, tool chaining, and responses. API Key: COHERE_API_KEY (env var).
- **MCP Server**: Official MCP SDK for task tools (stateless, integrated in FastAPI).
- **Project Management**: UV (backend), npm/pnpm (frontend).
- **Monorepo**: Single repository with /specs, /frontend, /backend, /agents, /skills.
- **No Additional External Dependencies** beyond the above; Cohere SDK for AI logic only.

## 3. Security & Authentication Rules (Non-Negotiable)
- All API endpoints (including /api/chat) require valid JWT in Authorization: Bearer <token> header.
- Shared secret: BETTER_AUTH_SECRET env var (same in frontend/backend).
- Backend must extract/verify JWT on every request; use Cohere API securely without exposing keys.
- Every database query MUST filter by authenticated user_id (e.g., Task.user_id == current_user_id).
- No endpoint/tool may return/modify another user's data/conversations.
- 401 Unauthorized for missing/invalid/expired token; 403 for ownership mismatch.
- Stateless JWT only – no DB sessions.
- Cohere API calls: Use secure env var (COHERE_API_KEY); rate-limit if possible; log anonymized usage.
- User table managed by Better Auth; tasks/conversations/messages have user_id FK.

## 4. Monorepo Structure & Spec-Kit Plus Conventions
- Root files: .spec-kit/config.yaml, CLAUDE.md, README.md, docker-compose.yml.
- /specs/ with subfolders: overview.md, architecture.md, features/, api/, database/, ui/, mcp-tools/.
- /frontend/ with CLAUDE.md and standard Next.js structure (extend with chatbot component).
- /backend/ with CLAUDE.md and modular FastAPI structure (main.py, db.py, models.py, schemas.py, dependencies/, routes/, mcp/, services/).
- /agents/ and /skills/ for agentic extensions (e.g., Cohere agent wrappers).
- All specifications in Markdown following Spec-Kit conventions; reference using @specs/path/to/file.md.

## 5. Specification Standards
- Every feature, API, DB change, UI component, MCP tool, or Cohere integration must have a dedicated spec file.
- Feature specs (/specs/features/): User stories, acceptance criteria, data requirements, edge cases, Cohere prompt examples.
- API specs (/specs/api/): Endpoints with method, path, auth, params, request/response schemas, errors (include /api/chat).
- Database specs (/specs/database/): Tables, fields, indexes, relationships (tasks + conversations + messages).
- UI specs (/specs/ui/): Pages, components, responsive behavior, auth guards, chatbot UI.
- MCP specs (/specs/mcp-tools/): Tools with params, returns, examples.
- Architecture spec (/specs/architecture.md): Diagrams, flows, Cohere integration points.

## 6. Coding Standards
### Frontend (Next.js)
- App Router only; Server Components default; "use client" for interactivity.
- Centralized /lib/api.ts with JWT auto-attach; extend for /api/chat calls.
- Tailwind CSS + shadcn/ui; responsive, accessible, dark-mode.
- Chatbot UI: Cohere SDK for chat logic or custom shadcn (Drawer/Sheet + bubbles); persist conversation_id locally.
- TypeScript strict mode.

### Backend (FastAPI)
- Modular: main.py (app, lifespan), db.py (async engine/session), models.py (SQLModel tables), schemas.py (Pydantic), dependencies/ (auth.py), routes/ (tasks.py, chat.py), mcp/ (tools.py).
- Async everywhere possible.
- Dependency injection for session, current_user.
- Pydantic/SQLModel for validation/models.
- Cohere Integration: Use Cohere SDK for chat completions; simulate agent behavior with multi-turn prompts or tool-calling APIs.
- MCP Tools: Stateless wrappers around secure task operations.

## 7. API Design
- Base path: /api/tasks for Phase II CRUD.
- New /api/{user_id}/chat for Phase III (request: {conversation_id?, message}; response: {conversation_id, response, tool_calls}).
- All require JWT; Cohere calls internal – no direct exposure.
- JSON request/response bodies.

## 8. Database Schema Rules
- tasks: user_id (indexed), id, title, description, completed, created_at, updated_at.
- conversations: user_id (indexed), id, created_at, updated_at.
- messages: user_id (indexed), id, conversation_id (FK, indexed), role (user/assistant), content, tool_calls (JSON str), created_at.
- Proper constraints/indexes for performance/filtering.

## 9. AI & Agentic Workflow Rules
- Use Cohere API for all AI logic (chat completions, intent parsing, tool calling).
- Adapt OpenAI Agents SDK patterns to Cohere: Use Cohere's multi-step reasoning or custom prompt chaining for "agent" behavior.
- MCP Tools: 5 tools (add/list/complete/delete/update_task) – stateless, DB-backed.
- Agents/Skills: Use @agents/architecture-planner, @agents/chatbot-backend-engineer, etc.; skills in /skills/ call API/Cohere.
- Design API/Cohere for agents (clean JSON, no HTML).

## 10. General Principles
- Prioritize security, user isolation, and traceability.
- Keep specifications clear, testable, and complete.
- All generated code must be consistent with this constitution.
- Validate every implementation against specs and constitution.
- Favor simplicity, readability, and excellence while meeting requirements.
- Cohere API: Secure key management (env var); cost-efficient prompts; handle rate limits/errors.

When writing specifications, planning, generating code, or testing, always reference and enforce this constitution explicitly in your reasoning.

## Response snapshot

Constitution successfully updated from v1.0.0 (Phase II only) to v2.0.0 (Phase II + Phase III integrated).

**Key updates**:
1. **New Principle XI**: AI & Agentic Workflow Governance (Cohere API, MCP tools, agents, skills, prompt security)
2. **Modified all 10 existing principles** to incorporate Phase III scope, Cohere integration, MCP tools, agents, and skills
3. **Extended API Specifications** with Phase III chat endpoint schema
4. **Extended Database Schema** with Conversation and Message tables
5. **Extended Frontend Standards** with chatbot UI requirements
6. **Extended Backend Standards** with Cohere service layer, MCP tool implementation, async patterns
7. **Extended Testing Standards** with Cohere mocking and chatbot integration tests
8. **Updated Governance** with Cohere prompt quality compliance and hackathon checklist

**Version Strategy**: MAJOR bump (1.0.0 → 2.0.0) justified by:
- Fundamental architecture expansion (single-user → multi-user chatbot)
- New security concerns (Cohere API key management, rate limiting, prompt isolation)
- New component types (MCP tools, agents, skills)
- New database tables (conversations, messages)
- Extended frontend and backend with significant new sections

**Sync Impact Report included** documenting:
- All modified principles with change rationale
- New Principle XI
- Templates requiring updates (spec, plan, tasks, CLAUDE.md files)
- Follow-up TODOs (agents, skills, Cohere service layer, chatbot UI, schema extensions)

File written: `.specify/memory/constitution.md` (572 lines)

## Outcome

- ✅ Impact: Constitution v2.0.0 ratified; all 11 principles defined; Phase II + Phase III unified governance
- 🧪 Tests: PHR created documenting full amendment flow
- 📁 Files: `.specify/memory/constitution.md` (updated)
- 🔁 Next prompts: Spec templates update, Cohere service layer design, MCP tools implementation, agent orchestration
- 🧠 Reflection: Constitution now provides complete governance for integrated Phase II (persistent TODO web app) + Phase III (AI chatbot) with strict security, user isolation, Cohere API integration, MCP tools, and agentic workflow rules. Ready for spec-driven development.

## Evaluation notes (flywheel)

- Failure modes observed: None; constitution fully filled with concrete rules, no placeholder tokens remaining
- Graders run and results (PASS/FAIL): PASS (all sections complete, no ambiguity)
- Prompt variant (if applicable): Constitution amendment via `/sp.constitution` skill
- Next experiment: Validate constitution compliance by creating Phase III architecture spec and reviewing against new Principle XI

