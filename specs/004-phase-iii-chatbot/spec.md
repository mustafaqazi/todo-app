# Feature Specification: Phase III – Premium AI Todo Chatbot with Cohere Integration

**Feature Branch**: `004-phase-iii-chatbot`
**Created**: 2026-01-12
**Status**: Draft
**Target Audience**: Hackathon judges evaluating end-to-end AI integration, security, visual excellence, and modern stack mastery

---

## Feature Summary

Build and seamlessly integrate a stunning AI-powered chatbot into the existing Phase II full-stack TODO app using Cohere API for natural language understanding, intent parsing, and tool calling. The chatbot manages all task operations (add, list, update, delete, mark complete) via conversational interface while maintaining 100% user isolation, stateless architecture, and premium UI aesthetics. Frontend presents a floating chat bubble interface with glassmorphism design; backend exposes clean JSON chat endpoint backed by Cohere API with MCP tools for task execution.

---

## User Scenarios & Testing

### User Story 1 – Access and Greet (Priority: P1)

Logged-in user opens the app and discovers an elegant floating chat bubble in the interface. Clicking it reveals a premium conversation interface with a personalized welcome message showing their email address.

**Why this priority**: Foundation for entire chatbot feature; demonstrates authentication integration and UI polish. Users must see the bot is available and ready before using it.

**Independent Test**: Click chat bubble → see welcome message with user email → closes cleanly. Proves auth integration + UI rendering without needing chat functionality.

**Acceptance Scenarios**:

1. **Given** user is logged in with email "user@example.com", **When** user opens app dashboard, **Then** chat bubble icon is visible in bottom-right corner with subtle pulse animation
2. **Given** chat bubble is visible, **When** user clicks icon, **Then** full-height chat drawer opens with glassmorphism backdrop and message "Hi user@example.com! I'm your smart TODO assistant. How can I help today?"
3. **Given** chat drawer is open, **When** user clicks outside or presses Escape, **Then** drawer closes smoothly
4. **Given** user is NOT logged in, **When** user navigates to app, **Then** chat bubble is NOT visible

---

### User Story 2 – Natural Language Task Management (Priority: P1)

User types natural language commands ("add task buy milk", "show pending tasks", "mark task 3 complete") and the chatbot understands intent, executes via Cohere API, invokes appropriate MCP tools, and confirms action with human-friendly message.

**Why this priority**: Core value proposition of chatbot; all other features depend on this. Judges will immediately test "add task" and "list tasks" commands.

**Independent Test**: Type "add task buy milk" → see confirmation "Task 'Buy milk' added successfully! ID: X" → verify task appears in Phase II task list. Proves end-to-end Cohere + MCP integration.

**Acceptance Scenarios**:

1. **Given** chat is open, **When** user types "add task buy milk" and sends, **Then** system displays "Task 'Buy milk' added successfully! ID: [number]" and new task appears in Phase II task list
2. **Given** user has pending tasks, **When** user types "show pending tasks" or "list my tasks", **Then** chatbot lists all incomplete tasks with titles and IDs
3. **Given** chat shows task list, **When** user types "mark task 5 complete", **Then** system confirms "Task marked complete!" and task completion status updates in Phase II UI
4. **Given** completed tasks exist, **When** user types "show completed tasks", **Then** chatbot lists only completed tasks
5. **Given** task exists with ID 3, **When** user types "delete task 3", **Then** system confirms "Task deleted" and task is removed from Phase II UI
6. **Given** task exists, **When** user types "update task 2 to buy milk tomorrow", **Then** system updates task description and confirms change

---

### User Story 3 – User Identity Awareness (Priority: P1)

When user asks "who am I?" or "what email am I logged in as?", chatbot responds with their authenticated email address from JWT token, demonstrating secure backend context awareness.

**Why this priority**: Validates JWT auth integration and backend user context. Judges verify security/isolation via this interaction.

**Independent Test**: Type "who am I?" → see response "You're logged in as user@example.com". Proves JWT extraction and passing user context to Cohere.

**Acceptance Scenarios**:

1. **Given** user is authenticated with email "user@example.com", **When** user types "who am I?" or "what email am I logged in as?", **Then** chatbot responds "You're logged in as user@example.com"
2. **Given** different user logged in, **When** same query asked, **Then** response shows DIFFERENT email address (verifying user isolation)

---

### User Story 4 – Conversation Persistence & Recovery (Priority: P2)

User sends multiple messages in a conversation; conversation_id is persisted in localStorage on frontend and database on backend. When user refreshes page or closes/reopens browser, conversation resumes automatically with full history visible.

**Why this priority**: Stateless architecture requirement; demonstrates Neon DB integration and localStorage coordination. Judges verify "restart backend → conversation resumes" from manual checklist.

**Independent Test**: Open chat, send 3 messages, refresh page → see all 3 messages + conversation continues. Proves DB persistence + localStorage coordination.

**Acceptance Scenarios**:

1. **Given** chat is open, **When** user sends message "add task A", **Then** conversation_id is generated and stored in localStorage
2. **Given** conversation in progress, **When** user sends 5 messages total, **Then** all 5 messages visible in chat history
3. **Given** conversation with 5 messages, **When** user refreshes page, **Then** all 5 messages remain visible and conversation_id is reused
4. **Given** chat is closed, **When** user reopens chat, **Then** previous conversation is auto-loaded (same conversation_id)
5. **Given** backend is restarted, **When** frontend sends message with existing conversation_id, **Then** backend retrieves full history from Neon and continues conversation

---

### User Story 5 – Responsive Design & Dark Mode (Priority: P2)

Chatbot UI renders perfectly on mobile and desktop. Dark/light mode toggle applies seamlessly to chat bubbles, input field, and backdrop. All text is readable, buttons are touch-friendly (48px+), keyboard navigation works.

**Why this priority**: Judges evaluate "visual excellence" and "modern stack mastery". Hackathon UI quality is critical differentiator.

**Independent Test**: Open on mobile device, toggle dark mode, send message → chat renders correctly, input is accessible, colors adjust properly.

**Acceptance Scenarios**:

1. **Given** app in light mode, **When** chat drawer opens, **Then** message bubbles are rendered with appropriate contrast (user: teal bg, assistant: slate bg, text readable)
2. **Given** app in dark mode, **When** chat drawer opens, **Then** colors invert appropriately and text remains readable
3. **Given** mobile device (375px width), **When** chat drawer opens, **Then** message input and send button are touch-friendly (≥48px tall)
4. **Given** keyboard focus in message input, **When** user presses Tab, **Then** focus cycles through send button and close button
5. **Given** message input has text, **When** user presses Shift+Enter, **Then** newline is added (not sent)

---

### User Story 6 – Real-Time Feedback & Error Handling (Priority: P2)

While Cohere API is processing, user sees typing indicator. If API times out or errors occur, user sees graceful error message ("Sorry, I had trouble processing that. Please try again.") instead of silent failure or crash. Tool calls that fail display specific feedback ("Task not found" vs generic error).

**Why this priority**: Professional UX; demonstrates backend error handling and user awareness of async operations.

**Independent Test**: Send message → see typing indicator for 1-2 seconds → response arrives. Send invalid command → see appropriate error message.

**Acceptance Scenarios**:

1. **Given** message is sent, **When** Cohere API is processing (0.5-2 seconds), **Then** typing indicator ("Assistant is typing...") appears
2. **Given** Cohere API returns error (timeout, rate limit, invalid response), **When** error is handled, **Then** user sees "Sorry, I had trouble processing that. Please try again."
3. **Given** MCP tool execution fails (e.g., task ID not found), **When** error is caught, **Then** chatbot says "Sorry, I couldn't find that task. Can you be more specific?"
4. **Given** user sends message while network is offline, **When** request fails, **Then** user sees "Connection error. Please check your internet."

---

### User Story 7 – Multi-User Isolation Verification (Priority: P1)

Two users logged into different accounts chat with the bot simultaneously. Each user's conversations, task operations, and messages are completely isolated. User A cannot see User B's chat history or perform operations on User B's tasks.

**Why this priority**: Security-critical; constitution mandates "zero data leakage". Judges will test with incognito windows or multiple browser sessions.

**Independent Test**: Open two browsers, log in as different users, send different messages in each → verify chat histories are completely separate and tasks created by User A don't appear in User B's task list.

**Acceptance Scenarios**:

1. **Given** User A is logged in (email: "alice@example.com"), **When** User A chats and creates tasks, **Then** conversation_id is unique to User A
2. **Given** User B is logged in separately (email: "bob@example.com"), **When** User B opens chat, **Then** User B sees EMPTY chat history (not User A's messages)
3. **Given** User A created Task X, **When** User B opens task list via "show all tasks", **Then** User B does NOT see Task X
4. **Given** User A's conversation is in Neon DB, **When** User B sends JWT with different user_id, **Then** backend returns 403 Forbidden (access denial, not 404 which would reveal task exists)

---

### Edge Cases

- What happens when user sends an empty message? → System ignores or prompts "Please type something"
- What happens when Cohere API rate limit (e.g., 10 calls/minute) is exceeded? → Backend returns 503 Service Unavailable with friendly message "I'm getting a lot of requests. Please wait a moment and try again."
- What happens when localStorage is disabled? → Conversation persistence uses session storage as fallback; no hard failure
- What happens when user sends very long message (>5000 chars)? → Backend truncates to 5000 chars and processes; user sees confirmation of what was processed
- What happens when Cohere tool call references non-existent task? → Cohere retries with list_tasks context, or system returns "That task doesn't exist. Would you like me to show you your tasks?"
- What happens when user is logged out mid-conversation? → JWT expires; next request returns 401 Unauthorized; frontend redirects to login
- What happens on mobile when chat drawer is open and keyboard appears? → Drawer scrolls up; input stays visible above keyboard; messages scroll to show latest

---

## Requirements

### Functional Requirements

**Frontend – Chat UI & Integration**:

- **FR-001**: System MUST render a floating chat bubble icon (emerald/teal gradient, 56px × 56px) in bottom-right corner of Phase II dashboard, only visible when user is authenticated
- **FR-002**: Chat bubble MUST display subtle pulse animation (1s cycle) to indicate interactivity without being distracting
- **FR-003**: Clicking chat bubble MUST open a full-height chat drawer (min 70% viewport height on mobile, full height on desktop) with glassmorphism backdrop (40% opacity, blur 10px)
- **FR-004**: Chat drawer MUST display welcome message: "Hi [user-email]! I'm your smart TODO assistant. How can I help today?" using authenticated user's email from JWT
- **FR-005**: Chat messages MUST display in bubbles: user messages right-aligned (teal background), assistant messages left-aligned (slate background), with appropriate padding and border radius (8px)
- **FR-006**: System MUST show typing indicator ("Assistant is typing...") while awaiting Cohere response (display duration: until response received)
- **FR-007**: Chat input MUST be a textarea with auto-focus, character counter optional, and Enter-to-send, Shift+Enter-for-newline behavior
- **FR-008**: Send button MUST be clearly visible, disabled while sending, show loading spinner during Cohere processing
- **FR-009**: Message history MUST auto-scroll to latest message; user can scroll up to view earlier messages
- **FR-010**: Conversation MUST be persisted in browser localStorage with key `chatbot_conversation_id`; on next visit, conversation_id is retrieved and conversation resumed
- **FR-011**: Dark/light mode toggle MUST apply colors correctly: light mode (user: teal-600 bg, white text), dark mode (user: teal-700 bg, white text; assistant: slate-800 bg, slate-100 text)
- **FR-012**: Mobile-responsive design MUST ensure input field ≥48px height, buttons ≥48px × 48px touch targets, drawer scrollable on narrow viewports

**Backend – Chat Endpoint & Cohere Integration**:

- **FR-013**: Backend MUST expose `POST /api/{user_id}/chat` endpoint requiring JWT in `Authorization: Bearer <token>` header
- **FR-014**: Endpoint MUST validate path `user_id` matches JWT `user_id`; return 403 Forbidden if mismatch
- **FR-015**: Request body MUST accept `{ "conversation_id": "string (optional)", "message": "string (required)" }` and validate message non-empty, ≤5000 chars
- **FR-016**: Endpoint MUST retrieve conversation from Neon DB (if conversation_id provided); fetch all messages for context (limit last 10 messages to avoid token bloat)
- **FR-017**: Endpoint MUST call Cohere API with `co.chat()` using model "command-r-plus" (or latest available), passing system prompt + conversation context + user message
- **FR-018**: System prompt MUST define assistant as "You are a helpful TODO assistant. Use tools to manage tasks: add, list, complete, delete, and update. Always confirm every action. Be concise."
- **FR-019**: Endpoint MUST expose 5 MCP tools to Cohere: `add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`, each filtered by authenticated `user_id`
- **FR-020**: If Cohere response includes tool calls, backend MUST execute each tool via MPC SDK, collect results, and optionally pass back to Cohere for synthesis (one retry round max)
- **FR-021**: Endpoint MUST store user message in Neon `messages` table with `role='user'`, store assistant response with `role='assistant'`, include `conversation_id`, `user_id`, timestamps
- **FR-022**: Response MUST return `{ "conversation_id": "uuid", "response": "string", "tool_calls": "[optional array of executed tools]" }` and HTTP 200
- **FR-023**: Endpoint MUST handle Cohere API errors (timeout, rate limit, invalid response) gracefully: log error, return 503 Service Unavailable, respond to user "Sorry, I had trouble processing that. Please try again."
- **FR-024**: Backend MUST rate-limit Cohere calls per user (e.g., 10 calls/minute); exceeding limit returns 503 with message "I'm getting a lot of requests. Please wait a moment and try again."
- **FR-025**: System MUST NOT expose COHERE_API_KEY to frontend; all Cohere calls must be backend-only
- **FR-026**: MCP tools MUST filter all operations by authenticated `user_id`; no cross-user access permitted

**Database – Conversation & Message Persistence**:

- **FR-027**: Neon DB MUST have `conversations` table with columns: `id` (UUID PK), `user_id` (indexed FK), `created_at`, `updated_at`
- **FR-028**: Neon DB MUST have `messages` table with columns: `id` (UUID PK), `conversation_id` (indexed FK), `user_id` (indexed FK), `role` (enum: 'user'/'assistant'), `content` (text), `tool_calls` (JSON optional), `created_at`
- **FR-029**: All DB queries MUST filter by authenticated `user_id`; foreign key constraints enforce referential integrity

**Authentication & Security**:

- **FR-030**: Chat endpoint MUST require valid JWT token; invalid/expired token returns 401 Unauthorized
- **FR-031**: JWT MUST be extracted from `Authorization: Bearer <token>` header; decoded using shared `BETTER_AUTH_SECRET`
- **FR-032**: Extracted `user_id` from JWT MUST match path parameter; mismatch returns 403 Forbidden
- **FR-033**: All Cohere API calls MUST use server-side API key from `COHERE_API_KEY` environment variable; key MUST NOT be embedded in frontend code or logs
- **FR-034**: Error messages returned to client MUST be generic (e.g., "Error processing request") and NOT expose internal system details, API keys, or user data

**API Integration**:

- **FR-035**: Frontend `lib/api.ts` MUST include new function `chatWithAssistant({ conversationId?: string, message: string }): Promise<{ conversation_id: string, response: string, tool_calls?: any[] }>`
- **FR-036**: Function MUST automatically attach JWT from Better Auth to request header
- **FR-037**: Function MUST pass conversationId in request body; if not provided, endpoint creates new conversation

### Key Entities

- **Conversation**: Represents a single chat session; belongs to one user; has multiple messages; persisted in Neon DB and localStorage (conversation_id)
- **Message**: Represents a single exchange (user or assistant); belongs to a conversation; stores role, content, optional tool calls; persisted in Neon DB
- **MCP Tool (add_task, list_tasks, complete_task, delete_task, update_task)**: Stateless, user-isolated task operations; invoked by Cohere API; execute against Phase II tasks table filtered by user_id
- **Cohere API Request/Response**: Chat endpoint marshals user context + conversation history into Cohere request; handles tool calls; synthesizes response back to user

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can open chat, see welcome message with email, and close drawer in under 3 seconds (measures UI responsiveness and instant load)
- **SC-002**: Users can add, list, update, delete, and mark tasks complete via natural language commands with 100% success rate (measures chatbot intent understanding and MCP tool execution)
- **SC-003**: Cohere response latency ≤3 seconds for 95% of requests (measures backend performance and Cohere API reliability)
- **SC-004**: Conversation persistence test: User sends 5 messages, refreshes page, all 5 messages remain visible (measures stateless architecture and DB persistence)
- **SC-005**: Multi-user isolation test: Two users create tasks with same title; each user sees only their own tasks; cross-user access attempts return 403 (measures security compliance)
- **SC-006**: Chat UI renders correctly in dark mode and light mode; all text readable (WCAG AA contrast minimum); mobile viewport responsive at 375px width (measures accessibility and responsive design)
- **SC-007**: Typing indicator appears within 100ms of message send; resolved within 3s of Cohere response (measures perceived responsiveness)
- **SC-008**: Error scenarios (network timeout, API rate limit, invalid task ID) display user-friendly messages; no crashes or silent failures (measures error handling robustness)
- **SC-009**: Chat icon hidden when user is NOT authenticated; visible immediately after login (measures auth integration)
- **SC-010**: Full end-to-end flow (login → add task via chat → mark complete via chat → see updated task in Phase II UI) takes under 10 seconds (measures integration seamlessness)

---

## Constraints & Assumptions

### Constraints

- Frontend: Next.js 16+ (App Router only), TypeScript strict mode, Tailwind v4+, shadcn/ui components (sheet, toast, badge, skeleton, input, button, avatar)
- Backend: FastAPI, SQLModel async, Cohere SDK (cohere-py) for chat/tool calling
- Chat placement: Floating trigger + Drawer/Sheet (not full page takeover)
- No new frontend dependencies beyond shadcn/ui components
- Only Cohere SDK in backend; no other AI SDKs
- Single iteration to perfection; no phased rollout

### Assumptions

- Cohere API key is available in `COHERE_API_KEY` environment variable (not hardcoded)
- Phase II JWT authentication and Better Auth integration are already functional
- Phase II task CRUD endpoints (`/api/tasks`) are already working and user-isolated
- Neon PostgreSQL connection is active and accessible
- MCP tool SDK is available and integrated in FastAPI
- localStorage is available in browser (graceful fallback to session storage if disabled)
- Cohere chat endpoint response includes tool_calls in a structured format (to be verified during implementation)
- Users have basic familiarity with typing commands; no voice input required

### Out of Scope

- Separate Cohere frontend SDK calls; all Cohere is backend-proxy
- Heavy animations or Lottie libraries
- New authentication system; reuse Better Auth
- Pagination or advanced filtering in chat history
- Multi-language support
- Voice input/output
- File upload in chat

---

## Manual Verification Checklist

This checklist MUST pass 100% before feature is considered complete:

- [ ] Chat icon visible only when logged in
- [ ] Click chat icon → drawer opens with welcome message including logged-in email
- [ ] Type "add task buy milk" → task created, shown in Phase II task list, chatbot confirms "Task 'Buy milk' added successfully! ID: [X]"
- [ ] Type "show pending tasks" or "list my tasks" → chatbot lists all pending tasks correctly
- [ ] Type "mark task [ID] complete" → task marked complete, confirmation shown, Phase II UI updates
- [ ] Type "who am I?" → responds with email address
- [ ] Open incognito window, log in as different user → chat shows empty history, tasks are completely different (zero cross-user data leakage)
- [ ] Dark mode toggle → chat colors invert correctly, text readable
- [ ] Mobile device (375px width) → chat drawer opens, input field is usable, send button clickable
- [ ] Network tab shows `/api/chat` POST requests with JWT in Authorization header
- [ ] Type invalid task ID → graceful error message ("Task not found"), no crash
- [ ] Network offline → connection error message, no silent failure
- [ ] Restart backend → refresh frontend, conversation resumes with all previous messages
- [ ] Cohere rate limit exceeded → friendly message "I'm getting a lot of requests..."
- [ ] Send very long message (5000+ chars) → truncated and processed gracefully
- [ ] Close chat drawer, reopen → previous messages visible (conversation resumed)
- [ ] Test typing indicator appears while Cohere is processing
- [ ] Test Shift+Enter adds newline; Enter sends message
- [ ] Test mobile keyboard handling; input stays visible when keyboard opens

---

## Notes for Planning Phase

**Key Integration Points**:
1. Extend existing FastAPI `/api/tasks` to include `/api/{user_id}/chat`
2. Create Conversation and Message SQLModel tables in Neon DB
3. Implement Cohere chat service layer with tool orchestration
4. Implement MCP tools: add_task, list_tasks, complete_task, delete_task, update_task
5. Create chatbot UI component in Next.js using shadcn/ui Sheet + message bubbles
6. Extend `/lib/api.ts` with `chatWithAssistant()` function

**Critical Decisions to Document**:
- Cohere model choice (command-r-plus vs command-r)
- One-round vs multi-round tool calling (recommend one-round for simplicity)
- Message history context window (recommend last 10 messages)
- Rate limiting strategy (recommend per-user Cohere call throttle)

**Testing Strategy**:
- Mock Cohere API in unit tests to avoid real API calls
- Integration tests: full chat flow with mocked Cohere
- Manual verification: follow checklist above
- Cross-user isolation tests: pytest with two different user JWTs

