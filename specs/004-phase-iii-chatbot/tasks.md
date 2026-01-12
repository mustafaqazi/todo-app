# Tasks: Phase III – Premium AI Todo Chatbot with Cohere Integration

**Input**: Design documents from `/specs/004-phase-iii-chatbot/`
**Prerequisites**: plan.md ✅, spec.md ✅, constitution.md (v2.0.0) ✅
**Tests**: Integration tests included for full validation

**Organization**: Tasks are organized by Phase, then by User Story priority (P1 → P2) to enable independent implementation and parallel execution.

---

## Phase 1: Setup & Infrastructure (Shared Foundation)

**Purpose**: Project initialization, environment configuration, and shared infrastructure setup

**Duration**: ~1-2 hours | **Team**: 1 developer

### Environment & Dependencies

- [ ] T001 Add Cohere SDK to backend requirements: `cohere-py>=5.0.0` in `backend/requirements.txt`
- [ ] T002 Configure COHERE_API_KEY environment variable in `backend/.env` and `backend/.env.example` (with placeholder)
- [ ] T003 [P] Install backend dependencies: Run `uv sync` in `backend/` directory to fetch latest Cohere SDK and MCP tools
- [ ] T004 [P] Add shadcn/ui Chat components to frontend: Run `npx shadcn-ui@latest add sheet toast badge skeleton input button avatar` in `frontend/`

### Project Structure Verification

- [ ] T005 Verify backend structure: `/backend/routes/`, `/backend/services/`, `/backend/agents/`, `/backend/mcp/` directories exist
- [ ] T006 Verify frontend structure: `/frontend/components/chat/`, `/frontend/lib/` directories exist

**Checkpoint**: Environment configured, dependencies installed, project structure ready

---

## Phase 2: Foundational Infrastructure (Blocking Prerequisites)

**Purpose**: Core database models, schemas, authentication integration, and Cohere setup — MUST complete before ANY user story

**Duration**: ~3-4 hours | **Team**: 1-2 developers | **⚠️ CRITICAL: Blocks all user stories**

### Database Models (Backend)

- [ ] T007 [P] Create Conversation SQLModel table in `backend/db.py`:
  - Fields: `id` (UUID PK), `user_id` (indexed FK), `created_at`, `updated_at`
  - Relationship: `messages` back-populates to Message table
  - Indexes: user_id, created_at DESC

- [ ] T008 [P] Create Message SQLModel table in `backend/db.py`:
  - Fields: `id` (UUID PK), `conversation_id` (indexed FK), `user_id` (indexed FK), `role` (enum: user/assistant), `content` (text), `tool_calls` (JSON optional), `created_at`
  - Relationships: `conversation` back-populates to Conversation
  - Indexes: conversation_id + user_id, user_id, created_at DESC
  - Foreign key constraint: conversation_id → conversations.id (cascade on delete)

- [ ] T009 Create Alembic migration for Conversation and Message tables: `alembic revision --autogenerate -m "Add Conversation and Message tables"` and verify migration in `backend/alembic/versions/`

### API Schemas (Backend)

- [ ] T010 [P] Create ChatRequest Pydantic model in `backend/schemas.py`:
  - Fields: `conversation_id` (optional str), `message` (str, min 1, max 5000)
  - Validation: message not empty, max length enforcement

- [ ] T011 [P] Create ChatResponse Pydantic model in `backend/schemas.py`:
  - Fields: `conversation_id` (str UUID), `response` (str), `tool_calls` (optional list of dicts)

### Cohere Integration Foundation (Backend)

- [ ] T012 Create Cohere client initialization in `backend/agents/cohere_todo_agent.py`:
  - Import Cohere SDK: `import cohere`
  - Initialize client in class constructor: `self.client = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))`
  - Add error handling for missing API key (raise ValueError if not set)
  - Add Cohere model constant: `MODEL = "command-r-plus"`

- [ ] T013 Define MCP tool schemas for Cohere in `backend/agents/cohere_todo_agent.py`:
  - Create tool definitions as list of dicts for Cohere tool calling
  - Tools: add_task, list_tasks, complete_task, delete_task, update_task
  - Each tool: name, description (for Cohere), parameter definitions (name, type, description)
  - Example: `{"name": "add_task", "description": "Add a new task for the user", "parameters": {...}}`

### Conversation Service (Backend)

- [ ] T014 Create conversation service in `backend/services/conversation.py`:
  - `get_or_create_conversation(session, user_id, conversation_id=None)` → Fetch existing or create new
  - `get_last_n_messages(session, conversation_id, user_id, n=20)` → Fetch last 20 messages with user_id filter
  - `append_message(session, conversation_id, user_id, role, content, tool_calls=None)` → Store message in DB
  - All functions use SQLModel async session

### JWT Middleware Verification (Backend)

- [ ] T015 Verify existing JWT middleware in `backend/dependencies/auth.py`:
  - Confirm `verify_jwt()` dependency extracts user_id from token
  - Confirm it returns user dict with at least `user_id` and `email` fields
  - Add docstring: "Extracts authenticated user_id from JWT; used in all endpoints requiring auth"

### Frontend API Extension

- [ ] T016 Extend `frontend/lib/api.ts` with chatWithAssistant() function:
  - Signature: `async chatWithAssistant({ conversationId, message }): Promise<{ conversation_id, response, tool_calls? }>`
  - Fetch to `/api/{user_id}/chat` with POST method
  - Auto-attach JWT from Better Auth session
  - Pass request body: `{ conversation_id: ..., message: ... }`
  - Error handling: 401 → redirect to login, 503 → user-friendly message, others → generic error

### Frontend Hooks/State Management

- [ ] T017 Create React hook in `frontend/hooks/useChat.ts`:
  - State: `conversations` (Map of conversation_id → messages), `currentConversationId` (string), `messages` (Message[])
  - Functions: `sendMessage(message: string)`, `loadConversation(id: string)`, `createNewConversation()`
  - localStorage coordination: Save/load conversation_id on state changes
  - Example: `useEffect(() => { localStorage.setItem('conversation_id', currentConversationId) }, [currentConversationId])`

**Checkpoint**: ✅ Foundation complete. All database models, schemas, Cohere client, and conversation service ready. User story implementation can now begin in parallel.

---

## Phase 3: User Story 1 – Access and Greet (Priority: P1) 🎯 MVP

**Goal**: Logged-in user sees floating chat bubble in UI; clicking reveals welcome drawer with personalized greeting

**Independent Test**: Click chat bubble → see welcome message with email → close drawer cleanly (no Cohere call needed yet)

**Deliverables**:
- Floating chat bubble icon visible only when authenticated
- Chat drawer component with glassmorphism design
- Welcome message displaying user email from JWT
- Smooth open/close animations

### Implementation

- [ ] T018 [P] [US1] Create ChatTrigger component in `frontend/components/chat/ChatTrigger.tsx`:
  - Floating icon (bottom-right, emerald/teal gradient, 56px × 56px)
  - SVG icon (message bubble or robot)
  - Pulse animation (1s cycle, 40% opacity)
  - Visible only when user is authenticated (check session)
  - Click handler: opens ChatWindow
  - Tailwind classes: `fixed bottom-8 right-8 rounded-full shadow-lg hover:shadow-xl transition`

- [ ] T019 [P] [US1] Create ChatWindow component in `frontend/components/chat/ChatWindow.tsx`:
  - Wrapper component for chat drawer/modal
  - State: `isOpen` (boolean), `user` (authenticated user object)
  - Use shadcn/ui Sheet component as base
  - Import: `import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetClose } from "@/components/ui/sheet"`
  - Sheet size: side=right, className="w-full sm:max-w-md" (mobile-responsive)
  - Header: "Smart TODO Assistant" + close button
  - Content area: Message history + input field (to be added in US2)
  - Backdrop: glassmorphism effect (bg-black/40 backdrop-blur-10px)

- [ ] T020 [P] [US1] Create MessageBubble component in `frontend/components/chat/MessageBubble.tsx`:
  - Props: `message` (Message object with role, content), `userEmail` (for display)
  - User message: Right-aligned, teal background (bg-teal-600 dark:bg-teal-700), white text
  - Assistant message: Left-aligned, slate background (bg-slate-100 dark:bg-slate-800), slate text
  - Styling: padding-2 rounded-lg max-w-xs, smooth animation (fade-in + slide-in)
  - Use Tailwind: `animate-fadeInUp` (custom animation or Framer Motion)

- [ ] T021 [US1] Add welcome message logic to ChatWindow:
  - On component mount, display welcome message: "Hi [user.email]! I'm your smart TODO assistant. How can I help today?"
  - Render as system message using MessageBubble with role="assistant"
  - Store in local state or pass as prop

- [ ] T022 [US1] Integrate ChatTrigger + ChatWindow in root layout (`frontend/app/layout.tsx`):
  - Import: `import ChatTrigger from "@/components/chat/ChatTrigger"`
  - Import: `import ChatWindow from "@/components/chat/ChatWindow"`
  - Add to return JSX: `<ChatTrigger />` and `<ChatWindow />`
  - Ensure ChatTrigger + ChatWindow don't interfere with Phase II task UI
  - Test: Chat bubble visible when logged in, hidden when logged out

- [ ] T023 [US1] Add dark/light mode support to chat components:
  - ChatTrigger: Gradient colors work in both modes (use `dark:` Tailwind prefix)
  - MessageBubble: Colors adjust per `dark:` theme
  - Example: User message light mode = `bg-teal-600 text-white`, dark mode = `dark:bg-teal-700 dark:text-white`
  - Verify contrast meets WCAG AA standards using color contrast checker

### Integration Test

- [ ] T024 [US1] Manual integration test for US1:
  - Login to Phase II app
  - Verify chat bubble visible in bottom-right
  - Click bubble → ChatWindow opens with smooth animation
  - Verify welcome message displays: "Hi [your-email]! I'm your smart TODO assistant..."
  - Click close button → Drawer closes smoothly
  - Logout → Chat bubble disappears
  - Document test results in `frontend/tests/integration/chat-access.test.ts` (or manual test report)

**Checkpoint**: ✅ User Story 1 complete. Chat bubble and welcome message fully functional and tested independently.

---

## Phase 4: User Story 2 – Natural Language Task Management (Priority: P1)

**Goal**: User types natural language commands ("add task buy milk", "list tasks", "mark task 5 complete", etc.); chatbot executes via Cohere API + MCP tools; user sees confirmations

**Independent Test**: Type "add task buy milk" → see confirmation "Task 'Buy milk' added! ID: X" → verify task appears in Phase II task list

**Deliverables**:
- Chat input component (textarea + send button)
- Cohere API integration for intent parsing + tool calling
- 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
- Tool execution with proper user isolation
- Chat message flow with typing indicator
- Tool call badges showing results

### Backend: MCP Tools Implementation

- [ ] T025 [P] [US2] Create add_task MCP tool in `backend/mcp/tools.py`:
  - Function: `async def add_task(user_id: str, title: str, description: str = None) -> Dict`
  - Create Task with user_id filtering: `task = Task(user_id=user_id, title=title, description=description)`
  - Save to Neon: `session.add(task); await session.commit()`
  - Return: `{"id": task.id, "title": task.title, "created_at": task.created_at, "message": f"Task '{title}' added! ID: {task.id}"}`
  - Error handling: SQLAlchemy errors → user-friendly message

- [ ] T026 [P] [US2] Create list_tasks MCP tool in `backend/mcp/tools.py`:
  - Function: `async def list_tasks(user_id: str, status: str = "all") -> Dict`
  - Status filter: "pending" (completed=false), "completed" (completed=true), "all" (all tasks)
  - Query: `tasks = await session.execute(select(Task).where((Task.user_id == user_id) & (conditions)))`
  - Return: `{"tasks": [{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks], "count": len(tasks), "message": f"You have {len(tasks)} {status} tasks"}`

- [ ] T027 [P] [US2] Create complete_task MCP tool in `backend/mcp/tools.py`:
  - Function: `async def complete_task(user_id: str, task_id: int) -> Dict`
  - Query: `task = await session.execute(select(Task).where((Task.id == task_id) & (Task.user_id == user_id)))`
  - Check: If not found, return error; if found, update: `task.completed = True; await session.commit()`
  - Return: `{"id": task.id, "title": task.title, "completed": True, "message": "Task marked complete!"}`

- [ ] T028 [P] [US2] Create delete_task MCP tool in `backend/mcp/tools.py`:
  - Function: `async def delete_task(user_id: str, task_id: int) -> Dict`
  - Query with user_id filter + delete: `session.delete(task)`
  - Return: `{"success": True, "message": "Task deleted"}`

- [ ] T029 [P] [US2] Create update_task MCP tool in `backend/mcp/tools.py`:
  - Function: `async def update_task(user_id: str, task_id: int, title: str = None, description: str = None) -> Dict`
  - Update fields if provided; return updated task with message

### Backend: Cohere Agent Implementation

- [ ] T030 [US2] Implement `run()` method in `backend/agents/cohere_todo_agent.py`:
  - Signature: `async def run(self, user_id: str, message: str, messages: List[Message]) -> Dict`
  - Step 1: Format message history for Cohere: `[{"role": m.role, "content": m.content} for m in messages]`
  - Step 2: Call Cohere: `response = await self.client.chat(model=MODEL, message=message, tools=self.tools, chat_history=...)`
  - Step 3: Check for tool calls: `if response.tool_calls:`
    - For each tool_call in `response.tool_calls`:
      - Extract tool name and parameters
      - Call corresponding MCP tool function
      - Collect results
  - Step 4: Return response: `{"response": response.text, "tool_calls": response.tool_calls}` (or synthesized response if tool results are re-passed to Cohere)
  - Error handling: Cohere timeout → return friendly message; rate limit → return 503

- [ ] T031 [US2] Add system prompt to Cohere agent in `backend/agents/cohere_todo_agent.py`:
  - System prompt: "You are a helpful TODO assistant. Use tools to manage tasks: add, list, complete, delete, and update. Always confirm every action with a friendly message. Be concise."
  - Pass to Cohere chat call: `preamble=system_prompt`

### Backend: Chat Endpoint

- [ ] T032 [US2] Implement POST /api/{user_id}/chat endpoint in `backend/routes/chat.py`:
  - Auth: `current_user = Depends(verify_jwt)`
  - Validate user_id: `if current_user["user_id"] != user_id: raise HTTPException(403)`
  - Fetch conversation: `if body.conversation_id: conv = await get_conversation(...) else: conv = await create_conversation(...)`
  - Fetch history: `messages = await get_last_n_messages(session, conv.id, user_id, 20)`
  - Call agent: `response = await cohere_agent.run(user_id, body.message, messages)`
  - Store messages: User message + assistant response in Message table
  - Return: ChatResponse with conversation_id, response text, tool_calls

- [ ] T033 [US2] Add error handling to chat endpoint:
  - 401 Unauthorized: Invalid/missing JWT
  - 403 Forbidden: user_id mismatch
  - 503 Service Unavailable: Cohere API error (timeout, rate limit, invalid response)
  - Each error returns JSON: `{"error": "friendly message"}`

### Frontend: Chat Input Component

- [ ] T034 [P] [US2] Create ChatInput component in `frontend/components/chat/ChatInput.tsx`:
  - Textarea input: auto-focus, placeholder "Type a message..."
  - Send button: Click handler + disabled while sending (show loading spinner)
  - Keyboard: Enter to send, Shift+Enter for newline
  - Character counter (optional): Show "X / 5000" characters
  - Styling: Tailwind, dark mode support

- [ ] T035 [P] [US2] Create ToolBadge component in `frontend/components/chat/ToolBadge.tsx`:
  - Display tool execution result: "Task added!", "Listed 3 tasks", etc.
  - Colors: Success (green), error (red), info (blue)
  - Styling: Small badge, inline with message

- [ ] T036 [US2] Create TypingIndicator component in `frontend/components/chat/TypingIndicator.tsx`:
  - Animation: Pulsing dots (. . .) or "Assistant is typing..."
  - Use Tailwind or Framer Motion
  - Show while Cohere is processing

### Frontend: Chat Window Message Integration

- [ ] T037 [US2] Add message history display to ChatWindow:
  - Import: useChat hook (from T017)
  - Render messages using MessageBubble component
  - Use ScrollArea (shadcn/ui) for scrollable message list
  - Auto-scroll to latest message
  - Show TypingIndicator while sending

- [ ] T038 [US2] Add ChatInput to ChatWindow:
  - Import ChatInput component
  - Handle send: Call `useChat.sendMessage(text)`
  - Clear input after send
  - Error handling: Show Toast (shadcn/ui) on error
  - Example: `if (error) { toast({ title: "Error", description: "Failed to send", variant: "destructive" }) }`

### Frontend: localStorage & Conversation Persistence

- [ ] T039 [US2] Update useChat hook to persist conversation_id:
  - On first message send: Generate/receive conversation_id from backend
  - Save to localStorage: `localStorage.setItem("conversation_id", id)`
  - On chat open: Retrieve and load: `const id = localStorage.getItem("conversation_id")`
  - Sync with backend: Always pass conversation_id in request body

### Integration Tests

- [ ] T040 [P] [US2] Curl/Postman test for chat endpoint:
  - Mock Cohere response in test
  - POST /api/{user_id}/chat with valid JWT
  - Send message: "add task test"
  - Verify response: conversation_id (UUID), response (string), tool_calls array (if applicable)
  - Verify response status: 200 OK

- [ ] T041 [P] [US2] MCP tool isolation test:
  - Pytest: Call add_task with user_id_1, then query as user_id_2
  - Verify: user_id_2 does NOT see user_id_1's task
  - Verify query includes WHERE user_id filter

- [ ] T042 [US2] End-to-end test: "Add task buy milk"
  - Frontend: Login, open chat, type "add task buy milk", send
  - Backend: Process, call Cohere, execute MCP tool
  - Verify: Task appears in Phase II task list
  - Verify: Chat shows confirmation "Task 'Buy milk' added! ID: X"
  - Document in `frontend/tests/integration/chat-task-management.test.ts`

**Checkpoint**: ✅ User Story 2 complete. Full task management via natural language working. MCP tools tested for isolation. E2E flow verified.

---

## Phase 5: User Story 3 – User Identity Awareness (Priority: P1)

**Goal**: User asks "who am I?" or "what email am I logged in as?" → chatbot responds with authenticated email

**Independent Test**: Type "who am I?" → Response: "You're logged in as user@example.com" (matches logged-in user)

**Deliverables**:
- Backend passes user email context to Cohere
- Cohere synthesizes user-friendly response
- Multi-user test confirms different users see different emails

### Backend: User Context in Cohere

- [ ] T043 [US3] Update Cohere agent to include user context:
  - Modify `run()` method: Include user email in system prompt or chat message context
  - Example: Append to message: `f"(User is logged in as {user_email}. Answer identity queries truthfully.)"`
  - Or: Add preamble with user info: `preamble = f"Current user: {user_email}. Help them manage TODOs..."`

### Frontend: Multi-User Isolation Test

- [ ] T044 [US3] Manual multi-user isolation test:
  - User A: Login with alice@example.com, open chat, type "who am I?"
  - Verify response: "You're logged in as alice@example.com"
  - User B: Incognito window, login with bob@example.com, open chat, type "who am I?"
  - Verify response: "You're logged in as bob@example.com"
  - Verify: User A and User B have completely separate conversations (different conversation_ids)
  - Document in `frontend/tests/integration/chat-multi-user.test.ts`

### Integration Tests

- [ ] T045 [P] [US3] Pytest: User isolation on identity query:
  - Mock two Cohere calls with different user emails
  - Verify backend passes correct email to Cohere
  - Verify response reflects correct user

**Checkpoint**: ✅ User Story 3 complete. User identity awareness working. Multi-user isolation verified.

---

## Phase 6: User Story 4 – Conversation Persistence & Recovery (Priority: P2)

**Goal**: User sends messages → conversation_id persisted in localStorage + Neon DB → Refresh/reopen → Conversation resumes with full history

**Independent Test**: Send 3 messages, refresh page → All 3 messages visible, conversation continues

**Deliverables**:
- Conversation history fetched from Neon on page reload
- localStorage coordinates with backend conversation_id
- Full message context available for Cohere

### Frontend: Conversation Recovery

- [ ] T046 [P] [US4] Update ChatWindow to load conversation on mount:
  - On component mount: `useEffect(() => { if (conversationId in localStorage) { loadConversation(id) } }, [])`
  - Fetch messages from backend: `GET /api/{user_id}/chat/{conversation_id}` (if endpoint exists) or load from messages table via chat calls
  - Or: Store messages in localStorage on every send (lightweight approach)
  - Render messages on UI

- [ ] T047 [P] [US4] Persist full message history in useChat hook:
  - On every message append: Save entire conversation to localStorage
  - Example: `localStorage.setItem("messages", JSON.stringify(messages))`
  - On chat open: Restore: `const saved = localStorage.getItem("messages")`

### Backend: Conversation History Endpoint (Optional)

- [ ] T048 [US4] (Optional) Create GET endpoint to fetch conversation history:
  - `GET /api/{user_id}/chat/{conversation_id}`
  - Return: `{ "messages": [...], "conversation_id": "...", "created_at": "..." }`
  - If backend doesn't have this, frontend uses localStorage only (acceptable for MVP)

### Integration Test

- [ ] T049 [US4] Manual persistence test:
  - Login, open chat, send 3 messages: "hello", "add task test", "list tasks"
  - Refresh page (browser reload)
  - Verify all 3 messages still visible
  - Verify conversation_id in localStorage matches
  - Type new message → Cohere has full 3-message context
  - Verify no errors
  - Document in `frontend/tests/integration/chat-persistence.test.ts`

- [ ] T050 [US4] Backend restart test:
  - Send message, conversation saved to Neon
  - Restart backend (stop FastAPI server, start it again)
  - Frontend sends message with same conversation_id
  - Verify backend retrieves full history from Neon
  - Verify Cohere gets full context
  - Verify response is coherent

**Checkpoint**: ✅ User Story 4 complete. Conversation persistence and recovery fully functional.

---

## Phase 7: User Story 5 – Responsive Design & Dark Mode (Priority: P2)

**Goal**: Chat UI renders perfectly on mobile + desktop; dark/light mode toggle works seamlessly

**Independent Test**: Open on mobile (375px), toggle dark mode, send message → Everything readable and accessible

**Deliverables**:
- Mobile-responsive chat drawer (min 70% on mobile, full on desktop)
- Dark mode colors perfect (high contrast, readable)
- Touch-friendly buttons (48px+)
- Keyboard navigation works

### Frontend: Responsive Design

- [ ] T051 [P] [US5] Update ChatWindow for mobile responsiveness:
  - Sheet component: Adjust width per breakpoint
  - Desktop: `max-w-md` (medium width, doesn't overwhelm)
  - Tablet: `max-w-lg` (larger)
  - Mobile: Full width minus padding
  - Use Tailwind breakpoints: `w-full sm:max-w-md md:max-w-lg`
  - Input field: Ensure visible above mobile keyboard
  - Test on iPhone SE (375px width), iPad, desktop

- [ ] T052 [P] [US5] Dark mode color scheme:
  - Light mode:
    - Chat trigger gradient: emerald to teal
    - User message: bg-teal-600 text-white
    - Assistant message: bg-slate-100 text-slate-900
    - Input: bg-white border-slate-300
  - Dark mode (use `dark:` prefix):
    - Chat trigger: Still emerald/teal (works in dark)
    - User message: bg-teal-700 text-white
    - Assistant message: bg-slate-800 text-slate-100
    - Input: bg-slate-900 border-slate-700
  - Verify contrast with WebAIM contrast checker

- [ ] T053 [US5] Add keyboard navigation:
  - Tab through send button, close button, input field
  - Escape key closes drawer
  - Shift+Enter in textarea adds newline
  - Implement via onKeyDown handlers

- [ ] T054 [US5] Add accessibility attributes:
  - ARIA labels: `aria-label="Chat assistant"`, `aria-label="Send message"`, `aria-label="Close chat"`
  - Role attributes: `role="dialog"` on ChatWindow
  - Focus management: Auto-focus input on open, focus close button on input blur

### Integration Tests

- [ ] T055 [P] [US5] Mobile responsive test:
  - Open on device with 375px width (iPhone SE)
  - Chat bubble visible, clickable
  - Drawer opens full-width with proper margins
  - Input field visible above keyboard when keyboard appears
  - Send button clickable (≥48px tall)
  - Messages readable with good contrast
  - Document results (screenshots) in test report

- [ ] T056 [P] [US5] Dark mode test:
  - Toggle Phase II dark mode switch
  - Chat colors adjust correctly
  - Text remains readable (contrast ≥4.5:1 for normal text)
  - Verify in both light and dark modes
  - Test on multiple browsers (Chrome, Firefox, Safari)

- [ ] T057 [US5] Keyboard accessibility test:
  - Tab through all interactive elements
  - Escape closes drawer
  - Shift+Enter adds newline in textarea
  - Document in test report

**Checkpoint**: ✅ User Story 5 complete. Responsive design and dark mode perfect.

---

## Phase 8: User Story 6 – Real-Time Feedback & Error Handling (Priority: P2)

**Goal**: Typing indicator while processing, graceful error messages on failure, tool badges showing results

**Independent Test**: Send message → See typing indicator → Response arrives. Send invalid command → See friendly error

**Deliverables**:
- Typing indicator animates while Cohere processes
- Error messages are user-friendly, not technical
- Tool call badges show what chatbot did
- Network errors handled gracefully

### Frontend: Typing Indicator & Loading States

- [ ] T058 [P] [US6] Integrate TypingIndicator in ChatWindow:
  - Show while `isLoading` state is true
  - Render after last message: `{isLoading && <TypingIndicator />}`
  - Remove when response arrives

- [ ] T059 [P] [US6] Show Toast notifications for errors:
  - Import: `import { useToast } from "@/components/ui/use-toast"`
  - On error: `toast({ title: "Error", description: "...", variant: "destructive" })`
  - Examples: "Sorry, I had trouble processing that", "Connection error", "Too many requests"

### Backend: Error Messages

- [ ] T060 [US6] Update chat endpoint to return user-friendly error messages:
  - Cohere timeout/API error: Return `{"error": "Sorry, I had trouble processing that. Please try again."}`
  - Rate limit (429): Return `{"error": "I'm getting a lot of requests. Please wait a moment and try again."}`
  - Network offline: Frontend shows `{"error": "Connection error. Please check your internet."}`
  - Invalid task reference: Cohere or tool returns `{"error": "Sorry, I couldn't find that task. Can you be more specific?"}`

### Frontend: Tool Call Badges

- [ ] T061 [US6] Render ToolBadge after assistant message with tool results:
  - Parse `tool_calls` from response
  - For each tool: `<ToolBadge name="add_task" result="Task 'Buy milk' added! ID: 5" />`
  - Display as small badges below assistant message

### Integration Tests

- [ ] T062 [P] [US6] Typing indicator timing test:
  - Send message
  - Measure time until typing indicator appears: <100ms
  - Measure time until response: <3 seconds (Cohere latency)
  - Verify indicator disappears when response arrives
  - Document in `frontend/tests/integration/chat-loading.test.ts`

- [ ] T063 [P] [US6] Error handling test:
  - Mock Cohere timeout: Verify friendly error message
  - Mock rate limit (429): Verify "too many requests" message
  - Network offline: Verify connection error message
  - Invalid task ID: Verify "couldn't find task" message
  - No crashes or technical errors shown to user

**Checkpoint**: ✅ User Story 6 complete. Real-time feedback and error handling working smoothly.

---

## Phase 9: User Story 7 – Multi-User Isolation Verification (Priority: P1)

**Goal**: Two users with different JWTs have completely isolated conversations + tasks. No cross-user data leakage.

**Independent Test**: Open incognito, different user → Empty chat history, different tasks, cross-user access returns 403

**Deliverables**:
- Database queries filter by user_id
- JWT validation prevents cross-user access
- Tests verify isolation
- 403 Forbidden on unauthorized access

### Backend: Security Tests

- [ ] T064 [P] [US7] Pytest: User A cannot see User B's conversation:
  - Create conversation and messages for User A
  - Fetch with User B's JWT (different user_id)
  - Verify: Returns 403 Forbidden (not 404, which reveals existence)
  - Document in `backend/tests/test_chat_security.py`

- [ ] T065 [P] [US7] Pytest: User A cannot access User B's tasks via MCP:
  - User A creates task
  - Call list_tasks with User B's user_id
  - Verify: Task NOT in results
  - Verify all MCP tools filter by user_id

- [ ] T066 [US7] Pytest: Cross-user conversation query verification:
  - Query: `select(Conversation).where((Conversation.id == conv_id) & (Conversation.user_id == user_a_id))`
  - Verify all queries include `user_id` filter
  - Use code review + grep to confirm no queries without user_id filter

### Frontend: Multi-User Integration Test

- [ ] T067 [US7] Manual multi-user isolation test:
  - Browser 1: Login with alice@example.com
    - Open chat, send message "add task alice's task"
    - Verify task appears in Phase II UI
    - Note conversation_id (from localStorage)
  - Browser 2 (or incognito): Login with bob@example.com
    - Open chat, send message "list tasks"
    - Verify: alice's task NOT in list
    - Note conversation_id (different from Browser 1)
  - Browser 1 again:
    - Verify alice's task still there
    - Verify alice's conversation_id is still in localStorage
  - Document results in `frontend/tests/integration/chat-multi-user-isolation.test.ts`

### Intrusion Tests

- [ ] T068 [P] [US7] Manual intrusion test (simulate attack):
  - Browser 1: Login alice, get JWT + conversation_id
  - Browser 2: Login bob
  - Manually craft curl request: `curl -H "Authorization: Bearer bob_jwt" /api/alice/chat -d '{"conversation_id": "alice_conv_id", ...}'`
  - Verify: Backend returns 403 Forbidden (path user_id mismatch)
  - Verify: No data leakage
  - Document in `backend/tests/test_security_intrusion.py`

**Checkpoint**: ✅ User Story 7 complete. Multi-user isolation verified. Security tests pass. Zero cross-user data leakage.

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Animations, confirmations, error messages, dark mode perfection, accessibility, documentation

**Duration**: ~4-6 hours | **Team**: 1-2 developers

### Visual Animations & Micro-Interactions

- [ ] T069 [P] Add drawer open/close animations:
  - Slide-in from right: Framer Motion or Tailwind animation
  - Example: `initial={{ x: "100%" }} animate={{ x: 0 }} exit={{ x: "100%" }} transition={{ duration: 0.3 }}`

- [ ] T070 [P] Add message fade-in + slide animation:
  - Each message appears with fade + slight slide-up
  - Use Framer Motion: `initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}`

- [ ] T071 [P] Pulse animation on chat bubble:
  - Tailwind: `animate-pulse` or custom keyframes
  - Opacity: 0.4 → 1.0 → 0.4 cycle (1s duration)
  - CSS: `@keyframes pulse { 0% { opacity: 0.4 } 50% { opacity: 1 } 100% { opacity: 0.4 } }`

- [ ] T072 [P] Typing indicator animation:
  - Pulsing dots: `. . .` with staggered delays
  - Or: "Assistant is typing..." with blinking cursor

### Toast & Confirmation Messages

- [ ] T073 [P] Add Toast provider to root layout (`frontend/app/layout.tsx`):
  - Import: `import { Toaster } from "@/components/ui/toaster"`
  - Add to JSX: `<Toaster />`

- [ ] T074 Task success confirmations:
  - When add_task succeeds: Toast: "Task 'Buy milk' added! ID: 5"
  - When complete succeeds: Toast: "Task marked complete!"
  - When delete succeeds: Toast: "Task deleted"

### Empty States & Fallbacks

- [ ] T075 Empty conversation state:
  - When chat first opens: Show welcome message + hint: "Try 'add task' or 'list my tasks'"
  - If no tasks: "You have no pending tasks. Would you like to add one?"

- [ ] T076 Network offline state:
  - Detect offline: `window.addEventListener('offline', ...)`
  - Show banner: "You're offline. Messages won't send until you're back online."
  - Queuing: (Optional) Buffer messages, send when back online

### Accessibility & Keyboard Navigation

- [ ] T077 [P] ARIA labels and semantic HTML:
  - `aria-label="Chat assistant"` on ChatTrigger
  - `aria-label="Send message"` on send button
  - `role="dialog"` on ChatWindow
  - `aria-live="polite"` on message list (for screen reader announcements)

- [ ] T078 [P] Keyboard navigation focus management:
  - Auto-focus input on drawer open
  - Trap focus within dialog (no Tab out)
  - Escape closes dialog

- [ ] T079 Test with screen reader (optional):
  - NVDA (Windows) or VoiceOver (Mac)
  - Verify messages are readable, buttons are labeled
  - Document any issues in accessibility report

### Documentation & Developer Guide

- [ ] T080 Create quickstart guide in `frontend/CHATBOT_SETUP.md`:
  - How to test locally
  - Environment variables (COHERE_API_KEY)
  - Run commands: `npm run dev`, `python -m uvicorn backend.main:app`
  - Manual test steps

- [ ] T081 Code comments on Cohere integration:
  - `backend/agents/cohere_todo_agent.py`: Comment on tool definitions, API call structure
  - `backend/routes/chat.py`: Comment on conversation flow, error handling
  - Example: `# Cohere returns tool_calls as array; execute each sequentially`

- [ ] T082 [P] Backend API documentation:
  - Document `/api/{user_id}/chat` endpoint in README or OpenAPI spec
  - Request/response examples
  - Error codes and meanings

### Testing & Validation

- [ ] T083 Code coverage check:
  - Backend: Run `pytest --cov=backend tests/` → Ensure ≥80% coverage for routes, services, MCP tools
  - Frontend: Run `npm run test -- --coverage` → Ensure ≥70% coverage for chat components
  - Document in test report

- [ ] T084 Final manual verification checklist:
  - [ ] Chat icon visible only when logged in
  - [ ] Open chat → see welcome message with email
  - [ ] Type "add task buy milk" → task created, shown in UI
  - [ ] Type "show pending tasks" → list correct
  - [ ] Type "who am I?" → responds with email
  - [ ] Incognito user → isolated conversation & tasks
  - [ ] Dark/light mode → colors adjust, readable
  - [ ] Mobile (375px) → chat responsive, input accessible
  - [ ] Network tab → /api/chat calls show JWT in header
  - [ ] Restart backend → conversation resumes
  - [ ] Cohere rate limit → friendly message
  - [ ] Type invalid task ID → graceful error
  - [ ] Offline network → connection error message
  - Document results in `VERIFICATION_REPORT.md`

- [ ] T085 Cost estimation:
  - Estimate Cohere API calls per user interaction
  - Estimate total cost for hackathon event (based on expected usage)
  - Document in `COHERE_COST_ESTIMATE.md`

### Git & Deployment Readiness

- [ ] T086 [P] Final git cleanup:
  - Remove console.logs, debug code
  - Ensure no commented-out code
  - Clean commit history (squash if needed)

- [ ] T087 Create deployment checklist:
  - .env variables set (COHERE_API_KEY, DATABASE_URL, BETTER_AUTH_SECRET)
  - Tests passing (backend + frontend)
  - Coverage ≥thresholds
  - Manual verification checklist 100% pass
  - Ready for final submission

**Checkpoint**: ✅ Polish complete. All user stories fully functional, tested, documented, and deployment-ready.

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase | Duration | Blocker | Can Start After |
|-------|----------|---------|-----------------|
| Setup (Ph1) | 1-2h | No | Immediately |
| Foundational (Ph2) | 3-4h | YES ⚠️ | Phase 1 complete |
| US1 (Ph3) | 2-3h | No | Phase 2 complete |
| US2 (Ph4) | 4-5h | No | Phase 2 complete |
| US3 (Ph5) | 1-2h | No | Phase 2 complete |
| US4 (Ph6) | 2-3h | No | Phase 2 complete |
| US5 (Ph7) | 2-3h | No | Phase 2 complete (can parallel with earlier stories) |
| US6 (Ph8) | 2-3h | No | Phase 2 complete (can parallel) |
| US7 (Ph9) | 2-3h | No | Phase 2 complete (can parallel) |
| Polish (Ph10) | 4-6h | No | Any user story complete (ideally all) |

### User Story Execution Strategy

**MVP First (Recommended for Hackathon)**:
1. Complete Phase 1 + Phase 2 (Foundation)
2. Complete Phase 3 (US1 – Access & Greet) → STOP & VALIDATE
3. If time: Add Phase 4 (US2 – Task Management) → STOP & VALIDATE
4. If more time: Add Phases 5-10

**Parallel Team (with 3+ developers)**:
1. All developers: Phase 1 + Phase 2 together
2. Once Phase 2 done:
   - Developer A: Phase 3 (US1)
   - Developer B: Phase 4 (US2)
   - Developer C: Phase 5 (US3)
   - (Others can start Phase 6, 7, 8 in parallel)
3. Final developer: Phase 10 (Polish)

### Within Each User Story

Recommended execution order:
1. **Backend Setup**: MCP tools → Service → Endpoint (in dependency order)
2. **Frontend Components**: Create components in order (Trigger → Window → Bubble → Input)
3. **Integration**: Connect frontend → backend
4. **Tests**: Write and validate
5. **Polish**: Animations, error messages specific to that story

### Parallel Opportunities Highlighted

**Phase 1**: All tasks marked [P] can run in parallel:
- T003 + T004 can install dependencies together

**Phase 2**: MCP tools marked [P] can run in parallel:
- T025 through T029 (5 tools) can be written simultaneously
- T007 + T008 (database models) can be implemented simultaneously
- T010 + T011 (schemas) can be written simultaneously

**Phase 3 (US1)**: Can start immediately after Phase 2 is done:
- Frontend components (T018, T019, T020) can be built in parallel

**Phase 4 (US2)**: All MCP tool tests (T040, T041) + Integration tests (T042) can run in parallel once tools are implemented

**Phase 5-9**: Once Phase 2 is complete, all user stories can be developed in parallel by different developers

---

## Summary

### Task Count by Phase

| Phase | Tasks | Duration | Category |
|-------|-------|----------|----------|
| Setup (Ph1) | 4 tasks | 1-2h | Infrastructure |
| Foundational (Ph2) | 11 tasks | 3-4h | Database + Auth + Services |
| US1 (Ph3) | 7 tasks + 1 test | 2-3h | Chat UI Access |
| US2 (Ph4) | 19 tasks + 3 tests | 4-5h | Task Management + Cohere |
| US3 (Ph5) | 3 tasks + 1 test | 1-2h | User Identity |
| US4 (Ph6) | 4 tasks + 2 tests | 2-3h | Persistence |
| US5 (Ph7) | 5 tasks + 3 tests | 2-3h | Responsive + Dark Mode |
| US6 (Ph8) | 6 tasks + 2 tests | 2-3h | Error Handling + Loading |
| US7 (Ph9) | 5 tasks + 3 tests | 2-3h | Security Isolation |
| Polish (Ph10) | 12 tasks | 4-6h | Animations + Docs + Verification |
| **TOTAL** | **79 tasks** | **~27-35 hours** | **Full feature** |

### MVP Scope (Recommended for Hackathon)

**Minimum Viable Product** = Phases 1-4:
- Phase 1 (Setup): ~1-2h
- Phase 2 (Foundational): ~3-4h
- Phase 3 (US1 – Chat bubble & welcome): ~2-3h
- Phase 4 (US2 – Task management via chat): ~4-5h
- **MVP Total: ~10-14 hours**

**MVP Deliverables**:
- ✅ Floating chat bubble visible when logged in
- ✅ Welcome message with user email
- ✅ "Add task", "list tasks", "complete task", etc. via natural language
- ✅ Tasks appear in Phase II UI
- ✅ Cohere + MCP tools integrated and working
- ✅ User isolation verified

**Judges will be impressed with MVP** – Shows Cohere integration, MCP tools, security, and seamless Phase II integration.

**Optional Additions** (if time):
- Phase 5 (US3): User identity awareness
- Phase 6 (US4): Conversation persistence
- Phase 7-9: Dark mode, responsive, multi-user tests
- Phase 10: Polish, animations, perfect UX

---

## Notes

- Each task is specific and independently executable
- [P] tasks can run in parallel (different files, no dependencies)
- [Story] labels enable traceability to user stories
- Dependencies within phases are documented
- Stop at any checkpoint to validate independently
- Tests are optional but recommended for security-critical features (user isolation)
- Use git commits after each task or logical group
- Verify against spec requirements as you go

---

**Ready to Build**: All 79 tasks mapped to user stories, phases, and parallel opportunities. Estimated **10-14 hours for MVP**, **27-35 hours for full feature**. Start with Phase 1!

