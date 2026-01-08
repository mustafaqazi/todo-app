---
id: 1
title: Establish Phase II constitution
stage: constitution
date: 2026-01-03
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: main
user: hackathon-participant
command: /sp.constitution
labels: ["architecture", "governance", "security", "authentication", "api-design"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests: []
---

## Prompt

You are an expert full-stack system architect and spec-driven developer building Phase II of a hackathon TODO application: a modern multi-user web application evolving from a Phase I console app.

Adhere strictly to this constitution for all specification writing, planning, code generation, and validation across the entire monorepo. This constitution ensures consistency, security, scalability, and traceability for hackathon judging.

## 1. Project Overview & Goals
- **Phase**: Phase II – Todo Full-Stack Web Application (Basic Level)
- **Objective**: Transform Phase I in-memory console TODO app into a persistent, multi-user web app with authentication.
- **Core Features**: Implement all 5 basic TODO operations (Add, List/View, Update, Delete, Mark Complete/Incomplete) as a responsive web application.
- **Multi-User Requirement**: Strict user isolation – each user sees and modifies only their own tasks.
- **Development Methodology**: 100% spec-driven using Claude Code + Spec-Kit Plus. No manual coding allowed. All work traceable via specs history.
- **Future Compatibility**: Design to be Phase 3 ready (AI chatbot with agents and skills).

## 2. Technology Stack (Strict – No Deviations)
- **Frontend**: Next.js 16+ (App Router only), TypeScript, Tailwind CSS, shadcn/ui components
- **Backend**: Python FastAPI (latest)
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth (frontend) with JWT plugin enabled
- **JWT Verification**: FastAPI middleware using shared BETTER_AUTH_SECRET
- **Project Management**: UV (backend), npm/pnpm (frontend)
- **Monorepo**: Single repository with organized /specs, /frontend, /backend, /agents, /skills
- **No Additional External Dependencies** beyond the above stack for Phase II.

## 3. Security & Authentication Rules (Non-Negotiable)
- All API endpoints require valid JWT in Authorization: Bearer <token> header
- Shared secret: BETTER_AUTH_SECRET environment variable (same value in frontend and backend)
- Backend must extract and verify JWT on every request
- Every database query MUST filter by authenticated user_id (Task.user_id == current_user["user_id"])
- No endpoint may return or modify another user's data
- 401 Unauthorized for missing/invalid/expired token
- No session storage in database – stateless JWT only
- User table managed by Better Auth; tasks table has user_id foreign key

## 4. Monorepo Structure & Spec-Kit Plus Conventions
- Root files: .spec-kit/config.yaml, CLAUDE.md, README.md, docker-compose.yml
- /specs/ with subfolders: overview.md, architecture.md, features/, api/, database/, ui/
- /frontend/ with CLAUDE.md and standard Next.js App Router structure
- /backend/ with CLAUDE.md and modular FastAPI structure
- /agents/ and /skills/ for agentic extensions (Phase 3 ready)
- All specifications written in Markdown following Spec-Kit conventions
- Reference specs using @specs/path/to/file.md

## 5. Specification Standards
- Every feature, API, database change, and UI page must have a dedicated spec file
- Feature specs (/specs/features/): User stories, acceptance criteria, data requirements, edge cases
- API specs (/specs/api/): Endpoints with method, path, auth, parameters, request/response schemas, errors
- Database specs (/specs/database/): Tables, fields, indexes, relationships
- UI specs (/specs/ui/): Pages, components, responsive behavior, auth guards
- Architecture spec (/specs/architecture.md): System diagrams, data flows, decisions

## 6. Coding Standards
### Frontend (Next.js)
- App Router only (no Pages Router)
- Server Components by default; "use client" only when necessary
- Centralized API client in /lib/api.ts with automatic JWT attachment
- Tailwind CSS + shadcn/ui components
- Responsive, accessible, dark-mode ready
- TypeScript strict mode

### Backend (FastAPI)
- Modular structure: main.py, db.py, models.py, schemas.py, dependencies/auth.py, routes/
- Async where possible
- Dependency injection for session and current_user
- Pydantic/SQLModel for validation and models
- HTTPException for errors
- Proper status codes and messages

## 7. API Design
- Base path: /api/tasks (no {user_id} in path – user_id from JWT)
- Endpoints:
  - GET /api/tasks
  - POST /api/tasks
  - GET /api/tasks/{id}
  - PUT /api/tasks/{id}
  - DELETE /api/tasks/{id}
  - PATCH /api/tasks/{id}/complete
- Query params for filtering/sorting (status, sort)
- JSON request/response bodies

## 8. Database Schema Rules
- tasks table must include: user_id (indexed), title, description, completed, created_at, updated_at
- Proper constraints and indexes for performance and filtering

## 9. Agentic Workflow Rules
- Use @agents/architecture-planner, @agents/frontend-engineer, @agents/backend-engineer, @agents/integration-tester
- Future skills in /skills/ may call API endpoints
- Design API to be consumable by agents (clean JSON, no HTML)

## 10. General Principles
- Prioritize security, user isolation, and traceability
- Keep specifications clear, testable, and complete
- All generated code must be consistent with this constitution
- Validate every implementation against relevant specs and this constitution
- Favor simplicity and readability while meeting requirements

When writing specifications, planning, generating code, or testing, always reference and enforce this constitution explicitly in your reasoning.

## Response snapshot

### Constitution Established ✅

Created comprehensive Phase II constitution document at `.specify/memory/constitution.md` with:

**10 Core Principles**:
1. Spec-Driven Development (NON-NEGOTIABLE)
2. Strict User Isolation (Security-Critical)
3. JWT-Based Stateless Authentication
4. Technology Stack Fidelity (No Deviations)
5. Modular Architecture & Monorepo Structure
6. Testability & Quality Gates
7. API Design Standards
8. Database Design & Normalization
9. Code Quality & Simplicity (YAGNI)
10. Traceability & Documentation

**Foundation Sections**:
- Security & Authentication: JWT token flow, data isolation enforcement, error handling
- API Specifications: Task CRUD endpoints with complete request/response schemas
- Frontend Standards: Next.js App Router patterns, required features, responsive design
- Backend Standards: FastAPI + SQLModel structure, async patterns, error handling
- Testing Standards: Unit, integration, E2E, and security testing requirements
- Development Workflow: Spec → Plan → Implement → Test flow
- Governance: Amendment process, version numbering, compliance review, hackathon checklist

**Version**: 1.0.0 (Ratified: 2026-01-03)

## Outcome

- ✅ Impact: Foundation established for 100% spec-driven Phase II development with non-negotiable security (user isolation, JWT auth) and technology stack constraints
- 🧪 Tests: Hackathon submission checklist provided (11-item verification list)
- 📁 Files: `.specify/memory/constitution.md` (421 lines, complete)
- 🔁 Next prompts: (1) Create spec templates aligned with constitution; (2) Initialize specs for auth, task CRUD, database; (3) Create frontend/backend CLAUDE.md files
- 🧠 Reflection: Constitution balances strict governance (security, tech stack, user isolation) with practical flexibility (simplicity, YAGNI, TDD). Ready to enforce during phase II implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution syntax validated; all placeholders replaced; version numbering applied correctly
- Prompt variant (if applicable): null
- Next experiment: Create spec templates for features/api/database/ui domains to operationalize constitution

