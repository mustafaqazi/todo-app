---
id: 17
title: Clarify Better Auth Root Cause
stage: spec
date: 2026-01-08
surface: agent
model: claude-haiku-4-5-20251001
feature: 003-fastapi-backend
branch: 003-fastapi-backend
user: user
command: /sp.clarify
labels: ["better-auth", "authentication", "root-cause", "architecture"]
links:
  spec: /specs/003-fastapi-backend/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /specs/003-fastapi-backend/spec.md
tests:
  - No tests run (clarification-only session)
---

## Prompt

I am unable to signup, signin using better-auth, frontend is already implemented, backend services are also starting, but i cannot see user table in neondb for authentication

## Response snapshot

Identified and resolved 5 critical ambiguities through structured questioning:

1. **Better Auth Not Initialized**: Backend lacks Better Auth library integration entirely (no imports, no endpoints, no user tables).
2. **Missing Dependency**: `better-auth` Python package not installed in backend requirements.
3. **Database**: PostgreSQL (Neon) correctly configured with `postgresql+asyncpg://...`
4. **Architecture Decision**: Better Auth should integrate on frontend only (Next.js). Backend validates JWT tokens using shared secret.
5. **JWT Claim Correction**: Standard `sub` claim (not custom `user_id`). Corrects earlier spec misstatement.

Spec updated with accurate clarifications and corrected JWT claim references throughout.

## Outcome

- ✅ Impact: High - Root cause identified; architecture clarified; spec corrected. Unblocks backend implementation.
- 🧪 Tests: N/A (clarification session; no code changes)
- 📁 Files: 1 modified (spec.md with clarifications section and corrected JWT references)
- 🔁 Next prompts: `/sp.plan` for implementation planning; backend-engineer agent to add JWT validation and user endpoints
- 🧠 Reflection: User's issue stemmed from architectural misalignment. Early clarification prevented building incorrect backend auth system. Better Auth frontend-only approach simplifies backend logic significantly.

## Evaluation notes (flywheel)

- Failure modes observed: Better Auth referenced in spec but never integrated in code; user table missing because Better Auth initialization never occurred.
- Graders run and results: N/A (spec clarification, not code)
- Prompt variant: Sequential questioning (5 of max 5 questions); early termination not triggered
- Next experiment: Implement JWT validation in backend routes; add User model for token mapping; test auth flow end-to-end

---

## Session Details

**Questions Asked & Answered:**

| # | Question | Answer | Impact |
|---|----------|--------|--------|
| 1 | Is Better Auth initialized in backend? | No - not initialized yet (option A) | Root cause identified |
| 2 | Is better-auth package installed? | No - needs to be added (option A) | Dependency gap confirmed |
| 3 | Database type? | PostgreSQL Neon (option A) | Architecture validated |
| 4 | Better Auth integration approach? | Frontend only; FastAPI validates JWT (option A) | Architecture clarified |
| 5 | JWT claim for user ID? | Standard `sub` claim, not custom (option A) | Spec corrected |

**Coverage Summary:**

| Category | Status | Resolution |
|----------|--------|------------|
| Functional Scope & Behavior | Clear | User isolation, CRUD ops well-defined |
| Domain & Data Model | Resolved | Task model OK; User model clarified (Better Auth managed) |
| Interaction & UX Flow | Resolved | Frontend handles auth UI; backend validates tokens |
| Non-Functional Quality | Clear | Performance targets, concurrency goals specified |
| Integration & External Dependencies | Resolved | Better Auth frontend integration pattern clarified |
| Edge Cases & Failure Handling | Clear | 401/404/422 cases defined |
| Constraints & Tradeoffs | Resolved | Frontend-only auth simplifies backend; clarified |
| Terminology & Consistency | Resolved | `sub` claim standardized throughout (corrected from `user_id`) |
| Completion Signals | Clear | Acceptance checklist present |

**No outstanding ambiguities remain.** Spec is now ready for `/sp.plan` phase.

