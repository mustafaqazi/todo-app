# Tasks: Ultimate Premium Professional & Visually Stunning Next.js 16+ Frontend

**Input**: Design documents from `/specs/002-premium-nextjs-frontend/` (spec.md, plan.md)
**Prerequisites**: plan.md (implementation roadmap), spec.md (6 user stories P1-P3)
**Status**: Ready for execution via `/sp.implement` or frontend-engineer agent

**Organization**: Tasks organized by user story priority (P1 → P2 → P3) enabling independent implementation and testing. Each user story is independently testable and deliverable as an MVP increment.

**Execution Strategy**:
- Phase 1: Setup (foundation)
- Phase 2: Foundational components (blocking prerequisites)
- Phases 3-8: User Stories 1-6 (P1, P1, P1, P2, P2, P3) in priority order
- Phase 9: Polish & verification

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependency configuration, and basic Next.js structure

**Estimated Duration**: 1-2 hours

- [ ] T001 Create Next.js project structure with App Router in `/frontend` directory per plan
- [ ] T002 Initialize `package.json` with dependencies: Next.js 16+, TypeScript, Tailwind CSS v4+, shadcn/ui, Better Auth, next-themes, Framer Motion, Lucide React
- [ ] T003 [P] Configure TypeScript strict mode in `/frontend/tsconfig.json` (noImplicitAny, strict all options)
- [ ] T004 [P] Setup Tailwind CSS v4+ configuration in `/frontend/tailwind.config.ts` with premium color palette (slate, emerald, indigo, rose)
- [ ] T005 [P] Initialize Next.js configuration in `/frontend/next.config.ts` (Image optimization, API routes, middleware)
- [ ] T006 Create `/frontend/app/layout.tsx` root layout structure (ready for providers and navbar)
- [ ] T007 Create `/frontend/styles/globals.css` with Tailwind imports and custom CSS properties for premium palette
- [ ] T008 [P] Create `/frontend/lib/constants.ts` with app-wide constants (API URLs, timeouts, animation timings)
- [ ] T009 [P] Create `/frontend/lib/types.ts` with shared TypeScript interfaces (Task, User, Toast, Theme types)

**Checkpoint**: Next.js project structure ready, all configurations in place, ready for foundational components

---

## Phase 2: Foundational Components (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST complete before ANY user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase completes

**Estimated Duration**: 2-3 hours

- [ ] T010 Create JWT-authenticated API client in `/frontend/lib/api.ts` with:
  - Centralized fetch wrapper with Authorization header injection
  - JWT token management (retrieval from cookies/storage)
  - Automatic 401/403 error handling with redirect to login
  - Error response normalization for toast notifications
  - Request/response logging (optional)

- [ ] T011 Create React Context providers in `/frontend/app/layout.tsx`:
  - ThemeProvider (next-themes with system preference detection)
  - ToastProvider (shadcn toast context)
  - AuthProvider (Better Auth integration)

- [ ] T012 [P] Setup Better Auth integration:
  - Configure Better Auth client in `/frontend/lib/auth.ts` with JWT enabled
  - Create authentication middleware in `/frontend/middleware.ts` to protect /tasks route
  - Setup secure token storage (HTTP-only cookies preferred, localStorage fallback)

- [ ] T013 [P] Create custom hooks directory `/frontend/lib/hooks/` with base hook implementations:
  - `useAuth.ts` — Hook for current auth state and logout function
  - `useTheme.ts` — Hook for theme toggle and system preference detection (via next-themes)
  - `useToast.ts` — Hook for triggering toast notifications (success/error with variants)
  - `useTasks.ts` (skeleton) — Hook for task state management (implement in Phase 3+)

- [ ] T014 [P] Initialize shadcn/ui components:
  - Run `npx shadcn-ui@latest init` to setup shadcn/ui in project
  - Install all required components: button, card, table, dialog, input, dropdown-menu, toast, skeleton, checkbox, badge, separator, avatar, sheet, tooltip
  - Verify all components import correctly in `/frontend/components/ui/`

- [ ] T015 [P] Create reusable form components in `/frontend/components/FormFields.tsx`:
  - Styled input fields with validation error display
  - Password input with show/hide toggle
  - Form label with required indicator
  - Inline error messages with soft red styling

- [ ] T016 Create comprehensive `Navbar.tsx` component in `/frontend/components/Navbar.tsx` with:
  - Fixed/sticky top navigation bar
  - Logo/branding on left
  - Theme toggle button (sun/moon icon) with Lucide
  - User avatar with dropdown menu (logout button)
  - Responsive design (hamburger menu stub for mobile)
  - Dark/light mode styling perfection

- [ ] T017 Create theme configuration styles in `/frontend/styles/animations.css`:
  - Define Framer Motion-compatible animation keyframes (if needed)
  - Tailwind animation customization for fade, scale transitions
  - Custom CSS variables for shadows, gradients, timing functions

- [ ] T018 Create error boundary component in `/frontend/components/ErrorBoundary.tsx`:
  - Catch React component errors
  - Display user-friendly error message
  - Include recovery button (e.g., reload page)

**Checkpoint**: Foundation complete — API client ready, auth setup done, all providers configured, shadcn/ui components available, Navbar component ready. User story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - New User Premium Onboarding Experience (Priority: P1) 🎯 MVP

**Goal**: Deliver breathtaking landing page and premium signup experience that establishes professional positioning and enables user account creation with JWT token handling.

**Independent Test**:
- New user can visit landing page, click "Get Started", complete signup with valid credentials, see success toast, receive JWT token, and redirect to empty tasks dashboard
- Mobile and desktop layouts perfectly responsive with zero layout shift
- Dark and light modes render with perfect contrast and no flickering

### Implementation for User Story 1

- [ ] T019 Create beautiful landing page `/frontend/app/page.tsx` with:
  - Inspirational hero heading ("Transform Your Tasks Into Achievements")
  - Descriptive subtitle highlighting premium positioning
  - Clear CTA button ("Get Started") in emerald gradient
  - Responsive layout (mobile: full-width, desktop: two-column with accent)
  - Dark/light mode perfection with theme-aware gradients
  - Smooth fade-in entrance animation (Tailwind)

- [ ] T020 [P] Create premium login/signup page `/frontend/app/login/page.tsx` with:
  - Centered card layout (400px max, shadows for elevation)
  - Toggle between login and signup tabs (or separate views)
  - Animated form field entrances (Tailwind stagger or Framer Motion)
  - Email and password inputs with validation feedback
  - Show/hide password toggle
  - "Sign Up" button with gradient (emerald to teal)
  - Link to landing page ("Back to Home")
  - Dark/light mode with perfect contrast (7:1 WCAG AAA)

- [ ] T021 [P] Integrate Better Auth signup flow:
  - Configure signup endpoint in `/frontend/lib/auth.ts`
  - Handle form submission with email/password validation
  - Call Better Auth signup API, receive JWT token
  - Store JWT token securely (HTTP-only cookie or localStorage)
  - Attach JWT to all subsequent API requests via centralized client

- [ ] T022 Implement signup form validation in `/frontend/app/login/page.tsx`:
  - Email format validation (regex or HTML5)
  - Password strength validation (min 8 chars, uppercase, number, special char)
  - Real-time inline error messages with soft red styling
  - Disable submit button until valid
  - Show/hide password requirements as user types

- [ ] T023 Create signup success flow in `/frontend/app/login/page.tsx`:
  - On successful signup: Show green gradient success toast ("Account created! Redirecting...")
  - Redirect to `/tasks` dashboard after 1.5 second delay
  - Preserve JWT token across redirect
  - Handle token in AuthContext for subsequent requests

- [ ] T024 Create login form in `/frontend/app/login/page.tsx` (if separate from signup):
  - Email and password inputs
  - "Remember me" checkbox (optional, stores preference)
  - Login button with gradient
  - Call Better Auth login API, store JWT token
  - Redirect to `/tasks` on success

- [ ] T025 Implement responsive design for landing + auth:
  - Mobile (320px): Full-width layout, single column, touch-friendly buttons (48px+ height)
  - Desktop (1920px): Two-column hero, centered card with accent background
  - Tablet (768px): Intermediate layout with proper spacing
  - Test on Chrome DevTools: iPhone 12, Galaxy S21, iPad, Desktop

- [ ] T026 Implement dark/light mode for landing + auth pages:
  - Auto-detect system preference via next-themes
  - Toggle theme via navbar sun/moon icon
  - Persist choice to localStorage
  - Ensure 7:1 contrast ratio on all text (WCAG AAA)
  - Use slate, emerald, indigo, rose colors per design system

- [ ] T027 Create authentication guard middleware in `/frontend/middleware.ts`:
  - Protect `/tasks` route from unauthenticated users
  - Redirect to `/login` if JWT token missing or invalid
  - Allow `/login`, `/page` (landing) without auth
  - Handle 401 responses from API (redirect to login)

- [ ] T028 Handle JWT token expiration gracefully:
  - Detect 401 responses in API client
  - Show informative toast ("Session expired. Please log in again.")
  - Redirect to login page
  - Clear stored JWT token

**Checkpoint**: User Story 1 complete — Users can land, signup, and reach empty dashboard. Landing and auth pages are visually stunning with perfect responsive design and dark/light mode support.

---

## Phase 4: User Story 2 - Main Dashboard with Sophisticated Task List (Priority: P1)

**Goal**: Deliver breathtaking main dashboard that displays user's tasks in responsive layout (desktop table with zebra striping, mobile cards) with perfect alignment and smooth animations.

**Independent Test**:
- Authenticated user can view task list in professional table (desktop) or card stack (mobile)
- Layout perfectly responsive with zero CLS (cumulative layout shift)
- Dark and light modes render perfectly
- Empty state shows inspirational message

### Implementation for User Story 2

- [ ] T029 Create custom hook for task state management in `/frontend/lib/hooks/useTasks.ts`:
  - State for: tasks array, loading status, error state, filter (all/pending/completed)
  - Function to fetch tasks from API (`GET /api/tasks`)
  - Function to filter tasks client-side by status
  - Function to refetch tasks
  - Error handling with clear error messages
  - Loading skeleton display during fetch

- [ ] T030 [P] Create responsive TaskCard component for mobile in `/frontend/components/TaskCard.tsx`:
  - Card layout with rounded corners and subtle shadow (shadow-sm → shadow-md on hover)
  - Title (bold, text-lg)
  - Truncated description (2 lines max, "read more" expand button)
  - Created date badge (with Lucide calendar icon)
  - Checkbox status indicator (styled, clickable)
  - Edit icon button (pencil, clickable)
  - Delete icon button (trash, clickable)
  - Hover lift animation (Tailwind transform: hover:shadow-md)
  - Full-width on mobile, responsive padding (16px)

- [ ] T031 [P] Create sophisticated TaskTable component for desktop in `/frontend/components/TaskTable.tsx`:
  - shadcn/ui table with zebra striping (alternating slate-50/white rows)
  - Columns: Status checkbox, Title, Description (truncated), Created date, Actions (edit/delete)
  - Hover row highlighting (light emerald background)
  - Smooth row transitions (Tailwind transition-colors 300ms)
  - Responsive table with horizontal scroll fallback
  - Sort by created date (most recent first)
  - Click handlers for checkbox, edit, delete actions

- [ ] T032 [P] Create EmptyState component in `/frontend/components/EmptyState.tsx`:
  - Centered container (text-center)
  - Lucide icon (e.g., CheckCircle2, scale 48px)
  - Heading: "No tasks yet – start your productive day!"
  - Subtitle: "Click 'Add Task' to create your first task"
  - Subtle fade-in animation on mount
  - Responsive padding (mobile: 32px, desktop: 64px)
  - Dark/light mode styling perfection

- [ ] T033 Create main dashboard page `/frontend/app/tasks/page.tsx` with:
  - Protected route (only accessible to authenticated users)
  - Fetch user's tasks on page load via `useTasks` hook
  - Display loading state (skeleton cards or shimmer)
  - Conditional render: Empty state OR task list (based on task count)
  - Responsive container (max-w-6xl for desktop, full-width mobile)
  - Title: "My Tasks" with task count badge
  - Add Task button (mobile: FAB at bottom, desktop: prominent button in header)
  - Filter dropdown (connected to TaskFilters component)

- [ ] T034 [P] Create responsive layout logic in `/frontend/app/tasks/page.tsx`:
  - Detect viewport size (mobile-first approach)
  - Mobile (<768px): Render TaskCard component in vertical stack
  - Tablet (768px-1024px): Render TaskCard in 2-column grid
  - Desktop (>1024px): Render TaskTable component
  - Use Tailwind responsive classes (hidden md:block, etc.)
  - Ensure zero layout shift during responsive transitions

- [ ] T035 [P] Create AddTaskDialog component in `/frontend/components/AddTaskDialog.tsx`:
  - shadcn Dialog modal (centered, 600px max-width)
  - Smooth scale-in entrance animation (Framer Motion or Tailwind)
  - Form fields: Title (required), Description (optional, textarea)
  - Submit button: "Create Task" in emerald gradient
  - Cancel button: "Close" or ESC key to dismiss
  - Form validation (title required, max lengths)
  - Inline error messages on validation failure
  - Dark/light mode styling

- [ ] T036 Create add task flow in `/frontend/app/tasks/page.tsx`:
  - Dialog state management (open/close)
  - Add Task button toggles dialog open
  - On form submission: Call `useTasks` hook to add task
  - Send POST request to `/api/tasks` with title and description
  - On success: Close dialog, refresh task list, show success toast ("Task created!")
  - On error: Show error toast with retry option
  - Optimistic update: Add task to list immediately, confirm from server

- [ ] T037 Implement dark/light mode perfection for dashboard:
  - Table zebra striping: Adapt colors for dark mode (dark slate vs slate-100)
  - Card shadows: Ensure visible in both modes
  - Text contrast: 7:1 ratio minimum (WCAG AAA)
  - Badges and icons: Color-aware with emerald, indigo accents
  - Hover states: Clearly visible in both modes

- [ ] T038 Create responsive FAB (Floating Action Button) for mobile:
  - Fixed position at bottom-right (mobile: 16px from edges)
  - Circular button with emerald background
  - Plus icon (Lucide Plus)
  - Hidden on desktop (Tailwind md:hidden)
  - Click opens AddTaskDialog
  - Smooth scale-up entrance animation

- [ ] T039 Implement loading skeleton in `/frontend/components/LoadingSkeletons.tsx`:
  - Mobile task card skeleton (matching TaskCard layout)
  - Desktop table skeleton (3 rows, matching columns)
  - Shimmer animation (Tailwind or CSS animation)
  - Show during initial load and refetch
  - Replace with content as data arrives

**Checkpoint**: User Story 2 complete — Users can view their task list in professional responsive layout. Dashboard renders perfectly on all devices with zero layout shift. Empty state is inspirational. Add Task dialog ready for Phase 5.

---

## Phase 5: User Story 3 - Premium Task Management Interactions (Priority: P1)

**Goal**: Enable users to create, read, update (mark complete, edit), and delete tasks with beautiful optimistic UI, smooth animations, and instant visual feedback via toasts.

**Independent Test**:
- User can add task: Form submission → optimistic update → loading skeleton → server confirmation → success toast
- User can toggle complete: Checkbox click → Framer Motion spring animation → success toast
- User can edit task: Click edit → dialog pre-fills → edit → success toast
- User can delete task: Click delete → confirmation dialog → task disappears → success toast
- Network error reverts optimistic update and shows error toast with retry

### Implementation for User Story 3

- [ ] T040 [P] Create EditTaskDialog component in `/frontend/components/EditTaskDialog.tsx`:
  - shadcn Dialog modal (centered, 600px max-width)
  - Pre-fill form with current task values (title, description)
  - Form fields with validation
  - Submit button: "Save Changes" in emerald gradient
  - Cancel button to dismiss
  - Dark/light mode styling

- [ ] T041 [P] Create DeleteConfirmation dialog component in `/frontend/components/DeleteConfirmation.tsx`:
  - Simple confirmation dialog: "Are you sure you want to delete this task?"
  - Show task title in confirmation message
  - Cancel button (dismisses)
  - Delete button in rose/red color (destructive action)
  - Dark/light mode styling

- [ ] T042 Create edit task flow in `/frontend/app/tasks/page.tsx`:
  - Edit icon click opens EditTaskDialog with task pre-filled
  - On form submission: Call useTasks to update task
  - Send PUT request to `/api/tasks/{id}` with updated title/description
  - Optimistic update: Update task in list immediately
  - On success: Close dialog, show success toast ("Task updated!")
  - On error: Revert change, show error toast

- [ ] T043 Create delete task flow in `/frontend/app/tasks/page.tsx`:
  - Delete icon click opens DeleteConfirmation dialog
  - On confirm: Call useTasks to delete task
  - Send DELETE request to `/api/tasks/{id}`
  - Optimistic update: Remove task from list immediately, fade-out animation
  - On success: Show success toast ("Task deleted!")
  - On error: Revert deletion, show error toast

- [ ] T044 Create animated checkbox toggle in `/frontend/components/TaskCheckbox.tsx`:
  - shadcn Checkbox component styled for premium feel
  - Framer Motion spring animation on toggle:
    - `animate={{ scale: [1, 1.2, 1] }}` with spring config
    - `transition={{ type: "spring", damping: 12, stiffness: 100 }}`
  - On click: Toggle task completion status
  - Send PATCH request to `/api/tasks/{id}/complete`
  - Optimistic update: Toggle checkbox immediately
  - Show success toast on completion
  - Dark/light mode styling

- [ ] T045 Implement optimistic UI updates throughout useTasks hook:
  - `addTask()`: Add to list immediately, send POST, revert on error
  - `updateTask()`: Update in list immediately, send PUT, revert on error
  - `deleteTask()`: Remove from list immediately (fade-out), send DELETE, revert on error
  - `toggleComplete()`: Toggle checkbox immediately, send PATCH, revert on error
  - Error handler: Revert state and show error toast with clear message

- [ ] T046 [P] Create custom toast notifications styling in `/frontend/lib/hooks/useToast.ts` and CSS:
  - Success variant: Emerald gradient background (linear-gradient 135deg emerald)
  - Error variant: Rose/red gradient background (linear-gradient 135deg rose)
  - Custom toast classes in `/frontend/styles/globals.css`
  - Apply via toast hook: `useToast().success()` / `.error()`
  - Auto-dismiss after 3 seconds

- [ ] T047 [P] Create custom loader/spinner component in `/frontend/components/LoadingSpinner.tsx`:
  - Small spinner for form submissions
  - Emerald color
  - Tailwind animation-spin
  - Display inside submit buttons during loading
  - Replace text with spinner, disable button

- [ ] T048 Create form submission handling for add/edit in dialogs:
  - Prevent form resubmission (disable button during request)
  - Show loading spinner inside submit button
  - Clear form on successful submit
  - Show error toast if validation or API failure
  - Focus back to input on error for accessibility

- [ ] T049 Implement network error handling in API client and components:
  - Detect network errors (timeout, no internet, etc.)
  - Show clear error toast: "Network error. Please try again."
  - Include retry button in toast (optional)
  - Log errors to console (development only)
  - Graceful degradation: Don't crash app on API error

- [ ] T050 Create task description "read more" expand in TaskCard:
  - Truncate description to 2 lines (CSS line-clamp-2)
  - Show "Read more" button if description longer
  - Click expands description to full height
  - Smooth height animation (Tailwind max-height transition)
  - "Show less" button to collapse

- [ ] T051 Create task metadata display (dates, icons) in TaskCard and TaskTable:
  - Created date formatted nicely (e.g., "Jan 3, 2025" or "2 hours ago")
  - Use date utility function in `/frontend/lib/utils.ts`
  - Lucide icons for status (CheckCircle2 for completed, Circle for pending)
  - Icons in subtle emerald/slate colors
  - Tooltip on hover showing full date/time

- [ ] T052 Implement success/error toast display patterns:
  - Success: "✓ Task created!" (green gradient)
  - Success: "✓ Task updated!" (green gradient)
  - Success: "✓ Task completed!" (green gradient)
  - Error: "Failed to create task. Please try again." (red gradient)
  - Error with retry: Include retry action button in toast

- [ ] T053 Test optimistic UI with network latency:
  - Simulate slow network (DevTools network throttle to Slow 3G)
  - Verify optimistic updates show immediately
  - Verify loading state appears while request in flight
  - Verify success/error toast appears on completion
  - Verify reverting on error works smoothly

**Checkpoint**: User Story 3 complete — All CRUD operations work with beautiful optimistic UI. Animations are smooth (Framer Motion for checkbox). Toasts provide clear feedback. Error handling is graceful with revert on failure.

---

## Phase 6: User Story 4 - Advanced Filtering with Elegant UX (Priority: P2)

**Goal**: Enable users to filter tasks by status (All, Pending, Completed) with elegant DropdownMenu control and smooth fade animations.

**Independent Test**:
- User can click filter dropdown and see All/Pending/Completed options
- Selecting filter instantly updates task list with fade animation
- Only correct tasks display (pending shows only incomplete, completed shows only complete)
- Reset to All shows full list
- No page reload, zero perceptible lag

### Implementation for User Story 4

- [ ] T054 Create TaskFilters component in `/frontend/components/TaskFilters.tsx`:
  - shadcn DropdownMenu button (centered in header)
  - Trigger button with Lucide filter icon and label "All Tasks"
  - Menu items: "All Tasks", "Pending", "Completed" (each with icon)
  - Current filter indicator (checkmark or highlight)
  - Dark/light mode styling

- [ ] T055 Implement filter state in `useTasks` hook:
  - Add `filter` state (all/pending/completed)
  - Add `setFilter()` function to update filter
  - Add `filteredTasks()` computed value (filters array based on status)
  - Persist filter to component state (not localStorage, resets on reload)

- [ ] T056 Integrate TaskFilters into dashboard in `/frontend/app/tasks/page.tsx`:
  - Render TaskFilters component in header
  - Connect to `useTasks` filter state
  - Pass `setFilter()` callback to TaskFilters
  - Conditional render: Show filtered tasks when filter active
  - Display filter badge "Showing: Pending (3)" in header

- [ ] T057 Implement filter fade animation:
  - When filter changes: Fade out task list (opacity 0.5) over 200ms
  - Filter tasks in background
  - Fade in new list (opacity 1) over 200ms
  - Use Tailwind transition-opacity or Framer Motion for smooth transition
  - No layout shift, smooth visual transition

- [ ] T058 Implement responsive TaskFilters for mobile:
  - Mobile: Filter dropdown button full-width or bottom-tab
  - Desktop: Filter dropdown button in header right-side
  - Use Tailwind responsive classes (md:inline-block, etc.)
  - Ensure 48px+ touch target on mobile

- [ ] T059 Create filter label display in TaskFilters button:
  - Show current filter name dynamically ("All Tasks", "Pending", "Completed")
  - Update button label when filter changes
  - Add subtle down-arrow icon (Lucide ChevronDown)

- [ ] T060 Test filter with edge cases:
  - Filter to "Pending" with no pending tasks → Show empty state
  - Filter to "Completed" with some completed tasks → Show only completed
  - Add new task while "Pending" filter active → New task appears in list
  - Delete last pending task while "Pending" filter active → Switch to empty state

**Checkpoint**: User Story 4 complete — Users can filter tasks by status with smooth fade animations. Filter state is clear. Empty state shows when no tasks match filter.

---

## Phase 7: User Story 5 - Theme Switching and Dark/Light Mode Excellence (Priority: P2)

**Goal**: Enable seamless dark/light mode with auto-detection of system preference, instant toggle without flicker, and perfect contrast in both modes.

**Independent Test**:
- System dark mode preference automatically applies on first visit
- Theme toggle button (sun/moon icon) switches modes instantly with no flicker
- All pages (landing, login, dashboard) render perfectly in both modes
- Contrast ratio 7:1 minimum (WCAG AAA) on all text
- Theme preference persists across sessions

### Implementation for User Story 5

- [ ] T061 Setup next-themes integration in `/frontend/app/layout.tsx`:
  - Import ThemeProvider from next-themes
  - Wrap app content with ThemeProvider
  - Configure system preference detection
  - Set default theme to "system"
  - Enable localStorage persistence

- [ ] T062 Create theme toggle in Navbar component `/frontend/components/Navbar.tsx`:
  - Button with sun icon (light mode) / moon icon (dark mode)
  - Click toggles theme via next-themes `setTheme()`
  - Show current theme via icon change
  - Smooth transition between icons (fade)
  - Tooltip on hover: "Toggle dark mode"

- [ ] T063 Verify dark/light mode colors in design system:
  - Light mode background: slate-50 (off-white)
  - Dark mode background: slate-900 (dark slate)
  - Text light mode: slate-700 (dark slate)
  - Text dark mode: slate-200 (light gray)
  - Accents: emerald-500 (both modes), indigo-500 (both modes)
  - Contrast check: All text meets 7:1 ratio (WCAG AAA)

- [ ] T064 Apply dark mode styling to all components:
  - Landing page: Background, text, button colors for dark
  - Login page: Card background, form inputs, button for dark
  - Dashboard: Table/card backgrounds, text for dark
  - Cards: Use dark: prefix in Tailwind classes
  - Shadows: Adjust shadow colors for dark mode (darker shadows less visible)

- [ ] T065 Apply dark mode styling to shadcn/ui components:
  - Verify button component dark mode styling
  - Verify card component dark mode styling
  - Verify table component dark mode styling
  - Verify dialog/modal component dark mode styling
  - Verify input component dark mode styling
  - Test each component renders correctly in dark/light

- [ ] T066 Test theme toggle no-flicker behavior:
  - Click theme toggle button
  - Verify instant theme switch (no delay)
  - Verify no white flash during transition
  - Verify all text remains readable
  - Test on Chrome, Firefox, Safari

- [ ] T067 Test theme persistence:
  - Set theme to dark, refresh page → Dark mode persists
  - Set theme to light, refresh page → Light mode persists
  - Clear localStorage → System preference applies
  - Test on incognito window → System preference applies

- [ ] T068 Create custom CSS for dark mode gradients:
  - Success toast gradient in dark: Adapt emerald (darker shade)
  - Button gradients in dark: Adjust opacity/shades
  - Background patterns in dark: Subtle grid or texture
  - Ensure premium feel in both modes
  - No harsh contrasts, maintain elegance

- [ ] T069 Test dark mode on all viewport sizes:
  - Mobile dark mode: Text, buttons, cards readable
  - Tablet dark mode: Table rows visible, hover states clear
  - Desktop dark mode: Full layout renders correctly
  - Dark mode with light mode toggle: Instant switch works

- [ ] T070 Ensure animations work in dark mode:
  - Framer Motion checkbox spring visible in dark
  - Modal scale-in visible in dark
  - Filter fade animation works in dark
  - Toast animations visible in dark mode

**Checkpoint**: User Story 5 complete — Dark/light mode toggles instantly with no flicker. System preference auto-detected. All components render with 7:1+ contrast in both modes. Theme persists across sessions.

---

## Phase 8: User Story 6 - Phase 3 Ready: Chatbot Integration Stub (Priority: P3)

**Goal**: Create elegant ChatbotUI component stub ready for Phase 3 agent integration. Component floats at bottom-right, displays sample messages, shows "coming soon", and doesn't interfere with app functionality.

**Independent Test**:
- Chatbot stub renders without errors
- Floating bubble/drawer appears at bottom-right
- Click opens drawer with sample message bubbles
- "Coming soon" message displays
- Close button works, no layout shift
- Doesn't interfere with task list scrolling or interactions

### Implementation for User Story 6

- [ ] T071 Create ChatbotStub component in `/frontend/components/ChatbotStub.tsx`:
  - Fixed position at bottom-right (16px from edges)
  - Circular floating bubble button with text "Chat" or icon (Lucide MessageCircle)
  - Emerald background color
  - Click toggles drawer open/close
  - Smooth scale and fade animations

- [ ] T072 Create chatbot drawer/panel in ChatbotStub:
  - Slide-in drawer from bottom-right (or modal)
  - Width: 400px on desktop, full-width on mobile
  - Height: 500px max (scrollable content)
  - Message bubbles in conversation style
  - Sample messages: "Hello! I'm your task assistant.", "Coming soon: Intelligent task suggestions and chat support."

- [ ] T073 Style message bubbles in chatbot:
  - User message: Emerald background, right-aligned
  - Assistant message: Slate background, left-aligned
  - Rounded corners (rounded-lg)
  - Padding and margins per design system (8px grid)
  - Clean typography (text-sm)
  - Dark/light mode styling

- [ ] T074 Create close button for chatbot drawer:
  - X icon (Lucide X) at top-right of drawer
  - Click closes drawer smoothly
  - Escape key also closes drawer (accessibility)
  - Keyboard focus management (focus trap inside drawer)

- [ ] T075 Implement chatbot animations:
  - Bubble entrance: Scale-up from 0 to 1 (Framer Motion)
  - Drawer entrance: Slide-in from right or fade-in
  - Message fade-in (Tailwind fade-in animation)
  - Close smooth fade-out
  - All animations <300ms, smooth 60fps

- [ ] T076 Ensure chatbot doesn't interfere with task list:
  - Bubble z-index high enough (z-50) but below modals (z-100)
  - Drawer scrolls independently from page
  - No clicks on bubble propagate to task list behind
  - No layout shift when drawer opens
  - Test with long task lists, scrolling still works

- [ ] T077 Responsive chatbot design:
  - Mobile: Full-width drawer (safer for 320px screens)
  - Tablet: 400px drawer at bottom-right
  - Desktop: Same 400px drawer
  - Test on iPhone 12, iPad, Desktop 1920px

- [ ] T078 Dark/light mode for chatbot:
  - Bubble colors adaptive (emerald in both modes)
  - Drawer background: slate-50 (light), slate-900 (dark)
  - Text: slate-700 (light), slate-200 (dark)
  - Message bubbles: Clear distinction in both modes
  - No text readability issues

- [ ] T079 Add "coming soon" message and placeholder state:
  - Show clear "Chat Support Coming Soon" message
  - Explain: "In Phase 3, we'll add intelligent task suggestions and chat support"
  - Button or CTA: "Notify me" (or similar, no-op for now)
  - Professional, non-intrusive messaging

- [ ] T080 Test chatbot with various task list states:
  - Empty dashboard: Chatbot visible and functional
  - Long task list: Chatbot floats above, list scrollable independently
  - Modals open (add task, edit task): Chatbot behind modal (z-index correct)
  - Filter active: Chatbot visible and functional
  - Mobile landscape: Chatbot positioned correctly

**Checkpoint**: User Story 6 complete — Chatbot stub renders elegantly, floats non-intrusively, ready for Phase 3 agent integration. No interference with core functionality.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final visual polish, accessibility compliance, performance optimization, and verification against success criteria

**Estimated Duration**: 2-4 hours

### Accessibility & Keyboard Navigation

- [ ] T081 [P] Implement keyboard navigation throughout app:
  - Tab key navigates through all interactive elements
  - Enter/Space activate buttons
  - Escape closes modals and dropdown menus
  - Focus visible (outline or ring) on all focused elements
  - Focus trap in modals (Tab cycles within modal)

- [ ] T082 [P] Add ARIA labels to interactive elements:
  - Buttons: aria-label (e.g., "Add task", "Delete task")
  - Form fields: aria-label or associated labels
  - Icons: aria-label if not self-explanatory
  - Dialogs: aria-label, aria-modal="true"
  - Menu buttons: aria-expanded, aria-haspopup

- [ ] T083 [P] Test with screen readers:
  - Test on Windows with NVDA screen reader
  - Test on macOS with VoiceOver
  - Test on iPhone with VoiceOver
  - Verify: Page structure readable, form fields labeled, buttons announced, error messages heard
  - Ensure semantic HTML (use <button>, <form>, <label>, etc.)

- [ ] T084 [P] Verify color contrast ratios:
  - Use Chrome DevTools Lighthouse audit
  - Target: 7:1 contrast (WCAG AAA) for all text
  - Test on light and dark mode
  - Especially important: Form labels, button text, toast messages, error messages

### Performance Optimization

- [ ] T085 [P] Optimize bundle size:
  - Run `npm run build` and check output
  - Target: <500KB gzipped total
  - Analyze bundle with `next/bundle-analyzer` if needed
  - Remove unused dependencies
  - Tree-shake CSS with Tailwind

- [ ] T086 [P] Optimize images and assets:
  - Use Next.js Image component for all task-related images (if any)
  - Lazy-load images below fold
  - Use proper image formats (WebP with fallback)
  - Optimize favicon and logo

- [ ] T087 [P] Implement Server Components maximization:
  - Root layout: Server Component
  - Landing page: Server Component
  - Tasks page: Mix of Server + Client (interactive parts only)
  - Minimize Client component count and bundle impact

- [ ] T088 [P] Test performance with Lighthouse:
  - Run Lighthouse audit (mobile and desktop)
  - Target: >95 score on mobile
  - Metrics: LCP <2.5s, FID <100ms, CLS <0.1
  - Fix any Critical issues

- [ ] T089 [P] Optimize API calls and data fetching:
  - Fetch tasks on initial dashboard load (SSR or client?)
  - Implement caching strategy (next.js caching)
  - Avoid redundant API calls
  - Use React Query or SWR if data refetch needed

### Visual Polish & Micro-Interactions

- [ ] T090 [P] Refine hover states on all interactive elements:
  - Buttons: Scale 1.05 or shadow elevation
  - Cards: Shadow lift (shadow-sm → shadow-md)
  - Links: Underline or color change (emerald)
  - Checkboxes: Scale or color change
  - All transitions <300ms

- [ ] T091 [P] Verify focus rings on all interactive elements:
  - Focus ring style: 2-3px, emerald or indigo
  - Visible on buttons, inputs, links
  - Test with keyboard Tab navigation
  - Ensure keyboard-only users can navigate

- [ ] T092 [P] Verify animations smooth and no jank:
  - Checkbox spring toggle: Smooth spring motion
  - Modal scale-in: Smooth scale and fade
  - Filter fade: Smooth opacity transition
  - Toast entrance/exit: Smooth slide or fade
  - Test at 60fps (DevTools Performance tab)

- [ ] T093 [P] Verify touch target sizes on mobile:
  - All buttons: minimum 48x48px (44x44px iOS)
  - Form inputs: at least 44px height
  - Checkbox size: At least 24x24px (preferably 40px+)
  - Test on actual mobile device if possible

- [ ] T094 [P] Fine-tune spacing and alignment:
  - Review all padding/margins (8px grid)
  - Verify component alignment (use DevTools ruler)
  - Check for inconsistent spacing
  - Test on multiple viewports
  - Look for visual "breathing room" (generous whitespace)

- [ ] T095 [P] Verify typography hierarchy:
  - Page headings: Bold, 28-32px
  - Section headings: Bold, 20-24px
  - Body text: Regular, 16px
  - Small text (metadata): Regular, 12-14px
  - Line-height: 1.5 for body, 1.3 for headings

- [ ] T096 [P] Verify color consistency:
  - Emerald accent: #10b981 (500) and #059669 (600)
  - Indigo accent: #6366f1 (500)
  - Rose error: #f43f5e (500)
  - Slate neutral: 50, 200, 700, 900
  - Gradients: Correct direction and colors

### Error Handling & Edge Cases

- [ ] T097 [P] Test JWT token expiration:
  - Set token expiration to 5 minutes
  - Wait >5 minutes, make API request
  - Verify 401 response triggers redirect to login
  - Verify graceful error message shown

- [ ] T098 [P] Test network error handling:
  - Disconnect internet, try to add task
  - Verify error toast shows ("Network error...")
  - Verify optimistic update reverts
  - Verify retry button works (if included)

- [ ] T099 [P] Test form validation edge cases:
  - Empty title: Error "Title required"
  - Title too long (>256 chars): Error "Title too long"
  - Description >1000 chars: Truncate or error
  - Invalid email: Error "Invalid email format"
  - Weak password: Error "Password must contain..."

- [ ] T100 [P] Test rapid interactions:
  - Click "Add Task" button multiple times
  - Verify only one request sent (debounce or disable)
  - Click delete on task, then immediately click add
  - Verify state consistency

- [ ] T101 Test responsive design on extreme viewports:
  - Very narrow (320px): Single column, full-width buttons
  - Very wide (2560px): Max-width respected, no stretched layout
  - Height-constrained (500px): Scrollable, no overlapping elements
  - Landscape mobile: Appropriate layout adjustments

- [ ] T102 Test on multiple browsers:
  - Chrome 120+: All features work
  - Firefox 121+: All features work
  - Safari 17+ (macOS + iOS): All features work, including WebKit quirks

### Documentation & Knowledge Transfer

- [ ] T103 [P] Create `/frontend/README.md` with:
  - Project overview and goals
  - Tech stack (Next.js 16, TypeScript, Tailwind, shadcn/ui)
  - Setup instructions (npm install, env variables)
  - Development workflow (npm run dev, build, test)
  - Folder structure explanation
  - Component documentation (what each component does)
  - API client usage examples
  - Common patterns (hooks, optimistic updates)

- [ ] T104 [P] Create `/frontend/.env.example` with:
  - NEXT_PUBLIC_API_URL=http://localhost:8000
  - BETTER_AUTH_SECRET=your_secret_here
  - Any other environment variables needed

- [ ] T105 [P] Add inline code comments for complex logic:
  - Optimistic update pattern in useTasks hook
  - Spring animation configuration in TaskCheckbox
  - Theme detection logic in next-themes setup
  - API error handling in api.ts
  - Keep comments minimal (code should be self-documenting)

### Final Verification & Testing

- [ ] T106 Multi-device visual testing:
  - iPhone 12 (375px): Landing, login, dashboard in light and dark
  - iPhone 14 Max (428px): Same as above
  - iPad (768px): Tablet layout with task cards/table
  - iPad Pro (1024px): Larger tablet layout
  - Desktop 1920px: Full layout, all features

- [ ] T107 [P] Cross-browser testing:
  - Chrome 120+ (mobile & desktop): All features
  - Firefox 121+ (mobile & desktop): All features
  - Safari 17+ (iPhone, iPad, macOS): All features

- [ ] T108 Complete interaction flow test:
  - New user signup from landing page (mobile + desktop)
  - Login with existing credentials
  - Add first task via FAB (mobile) / button (desktop)
  - Edit task with markdown in description
  - Toggle task complete (checkbox spring animation)
  - Filter to pending, then completed
  - Delete task with confirmation
  - Toggle dark/light mode (instant, no flicker)
  - Logout and verify redirect to login
  - Verify JWT token handling (cookie storage)

- [ ] T109 [P] Accessibility audit:
  - Run Lighthouse accessibility audit
  - Target: 100 (or >95)
  - Test keyboard navigation (Tab through all elements)
  - Test with NVDA (Windows) and VoiceOver (macOS/iOS)
  - Verify no automatic focus traps
  - Verify error messages announced

- [ ] T110 [P] Performance audit:
  - Run Lighthouse performance audit (mobile)
  - LCP: <2.5s (green)
  - CLS: <0.1 (green)
  - FID/INP: <100ms (green)
  - Target: >95 score
  - Check bundle size: <500KB gzipped

- [ ] T111 Capture final screenshots for judges:
  - Landing page (light mode)
  - Landing page (dark mode)
  - Signup form with animation
  - Empty dashboard with FAB
  - Task list with 5-10 tasks (desktop table)
  - Task list (mobile cards)
  - Add task dialog
  - Filter dropdown open
  - Edit task dialog
  - Dark mode toggle active
  - Chatbot stub visible

- [ ] T112 Create feature completion summary:
  - Verify all 6 user stories implemented
  - Verify all 20 functional requirements met
  - Verify all 13 success criteria achievable
  - Verify visual design matches 2025 premium standards
  - Verify zero layout shift and perfect responsiveness
  - Verify accessibility (WCAG 2.1 AA)
  - Verify performance (Lighthouse >95)
  - Ready for hackathon submission

**Checkpoint**: Polish phase complete. App is visually stunning, fully accessible, highly performant, and ready for judges. All requirements met, all edge cases handled.

---

## Summary & Task Statistics

**Total Tasks**: 112
- Phase 1 (Setup): 9 tasks
- Phase 2 (Foundational): 9 tasks
- Phase 3 (US1 Onboarding): 10 tasks
- Phase 4 (US2 Dashboard): 11 tasks
- Phase 5 (US3 CRUD): 14 tasks
- Phase 6 (US4 Filtering): 7 tasks
- Phase 7 (US5 Theme): 10 tasks
- Phase 8 (US6 Chatbot): 10 tasks
- Phase 9 (Polish): 32 tasks

**Parallelizable Tasks** (marked with [P]): 45+ tasks can run in parallel within their phase

**MVP Scope** (Minimum Viable Product): Complete Phase 1 + 2 + Phase 3 (User Story 1) → Delivers landing page, signup, basic auth
**Full Feature** (Recommended MVP+): Phases 1-7 (add User Stories 2-5) → Delivers complete task management
**Production Ready**: All phases 1-9 → Deliver premium, fully polished app with perfect UX

**Dependency Graph**:
- Phase 1 → Phase 2 (blocked)
- Phase 2 → Phases 3-8 (all stories can run in parallel after Phase 2)
- Phases 3-8 can execute in parallel or sequentially (minimal cross-story dependencies)
- Phase 9 depends on completion of Phases 1-8

**Estimated Effort**:
- Phase 1: 1-2 hours
- Phase 2: 2-3 hours
- Phases 3-8: ~8-10 hours total (2-3 per story, some parallelization)
- Phase 9: 2-4 hours
- **Total: ~15-20 hours for production-ready frontend**

**Success Criteria Alignment**:
- ✅ All 13 success criteria have corresponding tasks
- ✅ All 20 functional requirements have implementation tasks
- ✅ All 6 user stories have complete task coverage
- ✅ Accessibility, performance, testing integrated throughout

---

## Next Steps

1. **Run `/sp.implement`** to begin execution via frontend-engineer agent, or
2. **Execute tasks manually** in phase order (1 → 2 → 3+ in parallel)
3. **Use task checkboxes** to track completion
4. **Create PHR** for implementation phase
5. **Run final verification** (Phase 9) before submission