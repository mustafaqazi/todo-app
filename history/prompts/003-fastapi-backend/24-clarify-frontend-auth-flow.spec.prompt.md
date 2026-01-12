---
id: 24
title: Clarify frontend auth flow
stage: spec
date: 2026-01-09
surface: agent
model: claude-haiku-4-5-20251001
feature: 003-fastapi-backend
branch: 003-fastapi-backend
user: user
command: /sp.clarify
labels: ["authentication", "better-auth", "frontend", "clarification"]
links:
  spec: specs/003-fastapi-backend/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-fastapi-backend/spec.md
tests:
  - null
---

## Prompt

```
[API] [1/3] POST http://localhost:8000/auth/signup undefined
:8000/auth/signup:1  Failed to load resource: the server responded with a status of 404 (Not Found)Understand this error
forward-logs-shared.ts:95 [API] Response 404: Object
```

Understand this error by clarifying ambiguous requirements in the spec around Better Auth integration and frontend authentication flow.

## Response snapshot

Identified critical contradiction in spec between "Better Auth Integration Details" section (line 186) and "Root Cause Investigation" clarifications (line 120). The spec stated:
- Line 186: "Frontend calls backend endpoints with credentials and receives JWT token"
- Line 120: "Better Auth on frontend only. Frontend (Next.js) uses Better Auth for UI and token generation"

These conflicted. Clarification questions resolved:

**Q1: Where does signup/login occur?**
- Answer: Frontend only. Frontend (Next.js) uses Better Auth library directly. Backend does NOT have /api/auth/* endpoints.

**Q2: How does frontend get JWT token?**
- Answer: Frontend calls Better Auth library (not backend). Better Auth handles registration and login, generates JWT with `sub` claim. Frontend stores token in localStorage, includes it in `Authorization: Bearer <token>` header for backend API calls.

Updated spec sections:
- Added Session 2026-01-09 clarifications documenting both answers
- Fixed "Better Auth Integration Details" section to remove contradictory statement
- Clarified that backend has NO /api/auth/* endpoints
- Emphasized frontend-only Better Auth flow

## Outcome

- ✅ Impact: Resolved critical ambiguity that caused 404 error. Frontend should NOT call backend auth endpoints.
- 🧪 Tests: Acceptance criteria already reflect correct behavior; no test changes needed.
- 📁 Files: specs/003-fastapi-backend/spec.md (updated with clarifications and fixed contradiction)
- 🔁 Next prompts: Frontend code should be fixed to use Better Auth library directly instead of calling /auth/signup on backend. Then run integration tests.
- 🧠 Reflection: The 404 error on POST /auth/signup was a symptom of spec ambiguity. The spec had contradictory statements from earlier sessions that were never reconciled. Clarification workflow successfully identified and resolved this before planning/implementation continued.

## Evaluation notes (flywheel)

- Failure modes observed: Spec ambiguity led to incorrect frontend implementation trying to POST to backend auth endpoint that doesn't exist
- Graders run and results (PASS/FAIL): Spec now clear and unambiguous; contradiction removed
- Prompt variant (if applicable): null
- Next experiment: Verify frontend Better Auth integration is correct and test end-to-end authentication flow
