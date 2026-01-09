---
id: 2
title: Premium Frontend Implementation Planning
stage: plan
date: 2026-01-03
surface: agent
model: claude-haiku-4.5
feature: 002-premium-nextjs-frontend
branch: 002-premium-nextjs-frontend
user: architect
command: /sp.plan
labels: ["frontend","nextjs","plan","architecture","premium-design","phase-2"]
links:
  spec: specs/002-premium-nextjs-frontend/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-premium-nextjs-frontend/plan.md
tests:
  - Constitution Check: PASSED ✅
  - Architecture decisions documented: ✅
  - File generation order defined: ✅
  - Testing strategy complete: ✅
---

## Prompt

Create: detailed implementation roadmap, file-by-file generation order, component hierarchy diagram, visual design system plan, animation & polish strategy, responsive breakpoint plan, and final verification checklist.

Decisions needing documentation:

Animation library choice (Framer Motion vs pure Tailwind transitions) – tradeoffs: expressive spring animations vs zero-dependency lightweight approach
Custom checkbox toggle animation (Framer Motion spring vs Tailwind scale + transition) – tradeoffs: premium feel vs bundle size
Empty state illustration approach (shadcn icons + text vs placeholder SVG vs subtle Lottie) – tradeoffs: elegance vs no extra deps
Toast variant design (custom gradient backgrounds vs default shadcn) – tradeoffs: premium look vs simplicity
Modal backdrop (glassmorphism blur vs solid dark overlay) – tradeoffs: 2025 aesthetic vs performance on low-end devices
Navbar design (minimal top bar vs floating with avatar dropdown) – tradeoffs: clean space vs quick access to theme/logout

Testing strategy: rigorous manual visual and functional verification aligned with success criteria.

Multi-device testing: Chrome DevTools mobile (iPhone/Galaxy), tablet, desktop; dark/light mode on each
Visual perfection checks: alignment, spacing, hover states, focus rings, mobile touch targets (>48px)
Interaction flow: signup → login → dashboard → add task → filter → toggle → edit → delete → logout (two users in incognito)
Animation audit: all transitions smooth, no jank, subtle and tasteful only
Accessibility check: keyboard tab navigation, screen reader test (VoiceOver/NVDA), ARIA labels on interactive elements
Performance: Lighthouse score >95 (mobile), no layout shifts, instant interactions
Cross-browser: Chrome, Firefox, Safari (basic)

Technical details:

Strict adherence to constitution and /sp.specify visual excellence demands
Use Tailwind CSS v4+ with custom config for premium palette (slate base, emerald/teal accents, soft gradients)
shadcn/ui components: must run npx shadcn-ui@latest add for: button, card, table, dialog, input, dropdown-menu, toast, skeleton, checkbox, badge, separator, avatar, sheet, tooltip, tabs (for future)
Optional Framer Motion ONLY for checkbox toggle spring and modal scale-in (approved subtle animations)
Theme management: next-themes with system preference + manual toggle in navbar
Font: Geist Sans/Mono or Inter via next/font for crisp professional typography
Icons: Lucide React (included with shadcn) for all icons (check, plus, trash, edit, filter, moon/sun)
Responsive breakpoints: mobile-first (default), sm:640px, md:768px, lg:1024px, xl:1280px
File generation order (critical for incremental building):
Foundation → /lib/api.ts (JWT client), theme setup, root layout with navbar
Authentication → /app/login/page.tsx + Better Auth config
Landing → /app/page.tsx (hero)
Core Components → TaskCard, TaskTable, EmptyState, TaskFilters, AddTaskDialog, EditTaskDialog, Toast variants
Main Dashboard → /app/tasks/page.tsx (masterpiece integration)
Polish → ChatbotStub, micro-interactions, final animations
Verification → Manual checklist run

Organize implementation by phases:

Setup & Foundation → Tailwind config, theme provider, shadcn init, /lib/api.ts, root layout with premium navbar
Authentication Excellence → Stunning login/signup page with animated fields and gradient accents
Component Library → Build all reusable components with premium styling (cards with subtle glass/shadow, animated checkbox, custom toast variants)
Dashboard Masterpiece → Assemble /app/tasks/page.tsx with responsive logic (mobile cards vs desktop table), filters, FAB/modal, empty state
Interactions & Feedback → Optimistic updates, beautiful toasts, loading shimmer skeletons
Polish & Micro-Interactions → Hover effects, focus states, subtle animations, dark mode perfection
Phase 3 Readiness → Add elegant ChatbotStub component
Final Verification → Run full manual test suite, capture screenshots for judges, confirm "wow" factor

## Response snapshot

**Comprehensive Implementation Plan Created — Branch `002-premium-nextjs-frontend`**

Plan includes:

**Technical Context**: TypeScript strict, Node.js 18+, Next.js 16+, Tailwind v4+, shadcn/ui, Better Auth (JWT), optional Framer Motion, next-themes. Performance goals: LCP <2.5s, CLS <0.1, animations 60fps, Lighthouse >95 (mobile), all interactions <300ms. Scale: ~50 components, 7 pages/layouts.

**Constitution Check**: ✅ PASSED all 10 principles. No violations. Frontend spec complies with Phase II constitution.

**Project Structure**: Next.js App Router with /app (pages), /components (reusable), /lib (utilities/API), /styles (CSS). Exact folder structure defined.

**6 Resolved Architectural Decisions**:
1. **Animation Library**: Framer Motion for 2 animations (checkbox spring, modal scale-in) + Tailwind for rest. Rationale: Premium feel with minimal bundle impact (+25KB). Alternative pure Tailwind would feel less polished.
2. **Checkbox Animation**: Framer Motion spring with custom damping/stiffness. Delightful premium micro-interaction.
3. **Empty State**: Lucide icons + inspirational text only. Minimalist 2025 aesthetic. No SVG/Lottie.
4. **Toast Variants**: Custom Tailwind gradient backgrounds (emerald success, rose error). Premium look without extra deps.
5. **Modal Backdrop**: Solid dark overlay (not glassmorphism blur). Performance on low-end devices prioritized.
6. **Navbar**: Minimal top bar with logo (left), theme toggle + avatar dropdown (right). Clean focus on content.

**Component Hierarchy**:
- **Client-Side State**: AuthContext, ThemeContext (next-themes), ToastContext, TasksContext (optimistic updates)
- **Server Components**: Root layout, landing, error boundaries
- **Client Components**: Login, tasks pages; TaskCard, TaskTable, TaskFilters, dialogs, Navbar, chatbot stub
- **Custom Hooks**: useTasks (CRUD + optimistic), useTheme (dark/light), useAuth (status), useToast (notifications)

**Visual Design System**:
- **Color Palette**: slate neutral base, emerald/indigo accents, rose for errors. Gradients for success toast and CTAs.
- **Typography**: Geist Sans/Inter via next/font, crisp professional. Headlines bold, body normal, code mono.
- **Spacing**: 8px grid (p-2 to p-8), generous whitespace, min 16px padding around content, max-w-6xl desktop.
- **Shadows/Effects**: sm/md shadows only, no heavy elevation. rounded-lg for cards/buttons, rounded-full for avatars.
- **Responsive Breakpoints**: Mobile-first, sm:640px, md:768px, lg:1024px, xl:1280px.

**Responsive Layout Strategy**:
- Landing: Full-width hero mobile, two-column desktop
- Auth: Centered card (400px max), keyboard-aware
- Dashboard: Vertical cards mobile, 2-col grid tablet, table desktop
- Modals: Full-screen/bottom sheet mobile, centered (600px) desktop

**Optimistic UI Strategy**:
1. User triggers action
2. UI updates IMMEDIATELY with optimistic data
3. API call in background
4. On success: No UI change needed (already updated)
5. On error: Revert + show error toast with retry

Simple toggles (checkbox): No skeleton, immediate visual feedback
Form submissions: Loading spinner inside button
List loading: Skeleton cards
Transitions: Fade-in new items, fade-out deleted items

**File Generation Order** (30 files, 7 phases, est. 12-18 hours):
1. Foundation (package.json, config, API client, root layout, navbar) — 1-2 hours
2. Authentication (Better Auth integration, login page, middleware) — 1-2 hours
3. Landing page — 30 min
4. shadcn/ui components init + reusable components (TaskCard, TaskTable, dialogs, etc.) — 2-3 hours
5. Custom hooks (useTasks with optimistic updates, useTheme, useAuth, useToast) — 1 hour
6. Main dashboard (/app/tasks/page.tsx) — 2-3 hours
7. Polish, animations, ChatbotStub, error boundaries — 1-2 hours
8. Testing & verification (manual visual, accessibility, performance, screenshots) — 2-3 hours

**Implementation Phases** (7 phases):
1. Setup & Foundation (Tailwind config, theme provider, shadcn init, JWT client, navbar)
2. Authentication Excellence (Better Auth, premium login/signup, token management)
3. Component Library (All shadcn/ui, reusable premium components, custom hooks)
4. Dashboard Masterpiece (Responsive task list, filters, dialogs, empty state)
5. Interactions & Feedback (Optimistic updates, toasts, loading states, Framer Motion animations)
6. Polish & Optimization (Dark mode perfection, accessibility, performance, ChatbotStub)
7. Final Verification (Multi-device testing, cross-browser, Lighthouse, screenshots)

**Testing & Verification Checklist** (60+ items):
- Multi-device: iPhone 12/14 Max, iPad, iPad Pro, Desktop 1920px
- Cross-browser: Chrome 120+, Firefox 121+, Safari 17+
- Visual quality: Alignment, spacing, animations (60fps), hover/focus states, touch targets (48px+), dark/light contrast (7:1)
- Interaction flows: Signup → login → dashboard → add → filter → toggle → edit → delete → logout
- Animation audit: Spring toggle smooth, modal entrance smooth, filter fade smooth, <300ms, no 3D effects
- Accessibility: Keyboard nav, VoiceOver/NVDA, ARIA labels, form labels, error announcement, color + icons
- Performance: Lighthouse >95, LCP <2.5s, CLS <0.1, FID <100ms, interactions <300ms, <500KB bundle
- API: All CRUD works, 401/403 redirect, network errors handled, optimistic revert on error

**Architectural Decisions Summary Table**: Documents 9 key decisions (animation library, checkbox animation, empty state, toast variants, modal backdrop, navbar, state management, dark mode, API client) with choice, rationale, and tradeoff for each.

**Gate Re-evaluation Plan**: After Phase 1 (data-model.md + design-system.md complete), re-check Constitution. Ready for Phase 2 implementation via `/sp.tasks`.

## Outcome

- ✅ Impact: Comprehensive implementation plan ready for execution. All 6 architectural decisions documented with clear rationales and tradeoffs. File generation order defined for incremental building. Visual design system specified. Testing strategy aligned with 13 success criteria. Ready for `/sp.tasks` phase.
- 🧪 Tests: Constitution Check PASSED (10/10 principles), Architecture decisions documented (6/6), File generation order defined (30 files), Testing checklist (60+ items)
- 📁 Files: specs/002-premium-nextjs-frontend/plan.md (500+ lines, complete implementation roadmap)
- 🔁 Next prompts: Run `/sp.tasks` to generate actionable task list with dependencies; execute Phase 1 setup via frontend-engineer agent; manual testing post-implementation
- 🧠 Reflection: Plan balances premium positioning (Framer Motion for selective animations, custom gradients) with performance (Tailwind-first approach, Server Components, <500KB bundle). All architectural decisions justified with clear tradeoffs. Responsive design strategy comprehensive (mobile-first, 5 breakpoints, 3-column dashboard layout options). Testing strategy rigorous (manual visual, accessibility, performance). Ready for systematic implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None—planning phase complete without blockers
- Graders run and results (PASS/FAIL): Constitution Check PASSED (10/10)
- Prompt variant (if applicable): User-provided decisions on 6 key areas incorporated directly
- Next experiment: Proceed to `/sp.tasks` for task generation, then frontend-engineer agent for code generation