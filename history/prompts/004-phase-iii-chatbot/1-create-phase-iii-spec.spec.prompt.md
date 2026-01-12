---
id: 1
title: "Create Phase III AI Chatbot Specification"
stage: spec
date: 2026-01-12
surface: agent
model: claude-haiku-4-5-20251001
feature: "004-phase-iii-chatbot"
branch: "004-phase-iii-chatbot"
user: "hackathon-assistant"
command: "/sp.specify"
labels: ["phase-iii", "chatbot", "cohere-integration", "mcp-tools", "user-isolation", "ai-feature"]
links:
  spec: "specs/004-phase-iii-chatbot/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/004-phase-iii-chatbot/spec.md"
  - "specs/004-phase-iii-chatbot/checklists/requirements.md"
tests: []
---

## Prompt

/sp.specify Phase III – Premium AI Todo Chatbot with Cohere Integration (Full Backend + Frontend Seamless Extension)

Target audience: Hackathon judges evaluating end-to-end AI integration, security, visual excellence, and modern stack mastery; users expecting a luxurious, natural-language-powered TODO experience.

Focus: Build and perfectly integrate a stunning AI-powered chatbot into the existing Phase II full-stack TODO app (Next.js + FastAPI + Neon DB + Better Auth), replacing OpenAI Agents SDK with Cohere API for natural language understanding, tool calling, and task management — while maintaining 100% user isolation, stateless architecture, and premium Phase II UI aesthetics.

Success criteria:
- **Chatbot UI Excellence** (Frontend):
  - Floating chat bubble icon (bottom-right, emerald/teal gradient, subtle pulse animation) in Phase II navbar or dashboard
  - Opens elegant full-height Drawer/Sheet with glassmorphism backdrop, dark/light mode perfection
  - Message bubbles: User (right, teal), Assistant (left, slate), typing indicator, tool call badges ("Task added!", "Listed pending tasks")
  - Input: Auto-focus textarea + send button; Enter to send, Shift+Enter newline
  - Conversation persistence: conversation_id stored in localStorage; auto-resumes last chat
  - Empty state: "Hi [User Email]! I'm your smart TODO assistant. How can I help today?"
  - Micro-interactions: Fade-in messages, spring checkbox toggle (if shown), smooth open/close
  - Responsive & accessible: Mobile keyboard handling, ARIA labels, keyboard nav

- **Backend Integration & Cohere Power**:
  - Extend existing FastAPI backend with POST /api/{user_id}/chat (stateless)
  - Use Cohere API (COHERE_API_KEY from env) instead of OpenAI Agents SDK
  - Adapt Cohere chat/completion for agent-like behavior: multi-turn conversation, intent parsing, tool calling via structured output or function calling
  - Expose 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) via Cohere tool calling
  - Persist conversation + messages in Neon DB (Conversation & Message tables)
  - Strict JWT auth + user_id validation (path vs token match)
  - Return clean JSON: {conversation_id, response, tool_calls}

- **AI Behavior & Cohere Usage**:
  - Natural language commands understood perfectly (add/list/update/delete/mark + user info queries)
  - Confirmation messages: "Task 'Buy milk' added successfully! ID: 5"
  - Error handling: Graceful responses ("Sorry, I couldn't find that task", "Please login first")
  - User awareness: "You're logged in as mustafa@example.com" when asked
  - Tool chaining: e.g., "delete the meeting task" → list → confirm ID → delete

- **Security & Integration Perfection**:
  - Zero data leakage – every operation filtered by authenticated user_id
  - Cohere key never exposed client-side; all calls from backend
  - Seamless Phase II connection: Same JWT, same DB, same /lib/api.ts pattern
  - No breaking changes to Phase II UI/API

Constraints:
- **Frontend**: Next.js 16+ App Router, TypeScript strict, Tailwind v4+, shadcn/ui (add sheet, toast, badge, skeleton, input, button, avatar)
- **Backend**: FastAPI, SQLModel async, Cohere SDK (cohere-py) for chat/tool calling
- **Environment**:
  - COHERE_API_KEY (env var – never hardcode)
  - Reuse BETTER_AUTH_SECRET, DATABASE_URL from Phase II
- **Chatbot Placement**: Floating trigger + Drawer/Sheet (not full page takeover)
- **No Extra Deps**: Only Cohere SDK in backend; no new frontend libs beyond shadcn
- **Timeline**: Single iteration perfection with @agents/frontend-chatbot-engineer + @agents/chatbot-backend-engineer

Not building:
- Separate Cohere frontend SDK calls (all via backend proxy)
- Heavy animations or Lottie
- New auth system (reuse Better Auth)
- Pagination or advanced filtering in chatbot (keep simple)

Cohere Integration Requirements:
- Use Cohere chat endpoint with tool calling (structured output for tool invocation)
- Adapt existing OpenAI-style agent code to Cohere:
  - Replace Model.generate with co.chat(model="command-r-plus", message=..., tools=...)
  - Handle tool calls via Cohere response.tool_calls
  - Chain multi-turn if needed (loop until no more tool calls)
- Example prompt adaptation:
  "You are a helpful TODO assistant. Use tools to manage tasks. Confirm every action."

Frontend /lib/api.ts Extension (must include):
chatWithAssistant({ conversationId?: number, message: string }) → Promise<{conversation_id, response, tool_calls}>

Manual Verification Checklist (must pass 100%):
- [ ] Chat icon visible only when logged in
- [ ] Open chat → see welcome message with email
- [ ] Type "add task buy milk" → task created, shown in UI
- [ ] Type "show pending tasks" → lists correctly
- [ ] Type "who am I" → responds with email
- [ ] Incognito user → isolated conversation & tasks
- [ ] Dark/light mode, mobile responsive, no visual bugs
- [ ] Network tab shows /api/chat calls with JWT
- [ ] Restart backend → conversation resumes

This spec demands absolute visual & functional perfection – the most beautiful, secure, and intelligently integrated AI chatbot in the hackathon.

## Response snapshot

**Specification Created Successfully**

Created comprehensive Phase III AI Chatbot specification at `specs/004-phase-iii-chatbot/spec.md` (37 functional requirements, 10 success criteria, 7 prioritized user stories, 35+ acceptance scenarios, 8 edge cases).

**Specification Highlights**:
- 7 user stories (P1: Access/Greet, Task Mgmt, User Identity, Multi-User Isolation; P2: Persistence, Responsive Design, Error Handling)
- 37 functional requirements organized by domain (Frontend UI, Backend, Database, Security, API)
- 10 measurable success criteria (3s response time, 100% task success, conversation persistence, multi-user isolation, dark mode, error handling)
- 4 key entities (Conversation, Message, MCP Tool, Cohere API Request/Response)
- 8 edge cases (empty messages, rate limiting, localStorage unavailability, message truncation, task not found, auth expiry, mobile keyboard)
- 15-item manual verification checklist for judges
- Complete constraints, assumptions, and out-of-scope guidance

**Quality Validation**: Specification passed all quality checks:
- ✅ No implementation details (feature-agnostic requirements)
- ✅ No [NEEDS CLARIFICATION] markers (all aspects fully specified)
- ✅ All requirements testable and unambiguous
- ✅ Success criteria measurable and technology-agnostic
- ✅ Edge cases identified
- ✅ Scope clearly bounded (7 out-of-scope items listed)

**Files Created**:
1. `specs/004-phase-iii-chatbot/spec.md` — Complete feature specification (600+ lines)
2. `specs/004-phase-iii-chatbot/checklists/requirements.md` — Quality validation checklist

**Branch**: `004-phase-iii-chatbot` (created and checked out)

**Readiness**: Specification is READY FOR PLANNING. Next step: `/sp.plan` to detail architecture, Cohere integration points, MCP tool design, and implementation tasks.

## Outcome

- ✅ Impact: Specification complete and validated; clear user value + measurable outcomes for hackathon judges
- 🧪 Tests: Manual verification checklist (15 items) documents validation path
- 📁 Files: spec.md (600+ lines), requirements.md (checklist)
- 🔁 Next prompts: `/sp.plan` (architecture & task breakdown), `/sp.tasks` (detailed implementation tasks)
- 🧠 Reflection: Specification captures premium UI/UX vision (glassmorphism, animations, dark mode), security-critical requirements (user isolation, JWT, Cohere key safety), backend integration (Cohere API, MCP tools, Neon DB), and frontend seamlessness (localStorage persistence, responsive design). Zero ambiguity; ready for planning and implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None; specification fully specified with no placeholder tokens
- Graders run and results (PASS/FAIL): PASS (content quality, requirement completeness, feature readiness all validated)
- Prompt variant (if applicable): `/sp.specify` skill with detailed Phase III description
- Next experiment: Validate specification compliance by creating planning artifacts and task breakdown with `/sp.plan` command

