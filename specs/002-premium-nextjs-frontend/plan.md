# Implementation Plan: Ultimate Premium Professional & Visually Stunning Next.js 16+ Frontend

**Branch**: `002-premium-nextjs-frontend` | **Date**: 2026-01-03 | **Spec**: [specs/002-premium-nextjs-frontend/spec.md](spec.md)
**Input**: Feature specification from `/specs/002-premium-nextjs-frontend/spec.md`

## Summary

Build a production-ready, premium-quality Next.js 16+ frontend for Phase II TODO app targeting hackathon judges with pixel-perfect design. Deliver 6 prioritized user stories (P1-P3) spanning landing page, premium auth flow, main dashboard with responsive task list (desktop table + mobile cards), advanced filtering, dark/light mode theme switching, and Phase 3 chatbot stub. Achieve visual excellence through minimalist design, subtle animations, perfect accessibility, and optimistic UI updates. Key technical approach: next-themes for dark/light mode auto-detection, Framer Motion for approved animations (checkbox spring toggle, modal scale-in), shadcn/ui components for consistency, JWT-authenticated centralized API client, and Server Components maximization for performance.

## Technical Context

**Language/Version**: TypeScript (strict mode), Node.js 18+ (via Next.js 16+)
**Primary Dependencies**: Next.js 16+ App Router, TypeScript strict, Tailwind CSS v4+, shadcn/ui components, Better Auth (JWT), optional Framer Motion for animations, next-themes for theme management
**Storage**: Backend API (FastAPI + PostgreSQL per Phase II constitution); frontend uses browser local storage for theme preference + secure HTTP-only cookies for JWT
**Testing**: Manual visual testing, Lighthouse scores, accessibility scanning (keyboard + screen reader), cross-browser (Chrome, Firefox, Safari), multi-device (mobile 320px, tablet 768px, desktop 1920px+)
**Target Platform**: Web (browser: Chromium-based, Safari 14+, Firefox 88+)
**Project Type**: Web application (Next.js frontend only; assumes Phase II backend exists per constitution)
**Performance Goals**: LCP <2.5s on 4G, CLS <0.1 (zero layout shift), animations 60fps, Lighthouse >95 (mobile), all interactions <300ms
**Constraints**: Exact file structure required (/app, /components, /lib), TypeScript strict mode mandatory, no extra dependencies beyond defined stack, <500KB gzipped bundle, single iteration perfection (no follow-up polish phase)
**Scale/Scope**: ~50 components (reusable), 7 pages/layouts, 20+ functional requirements, 13 measurable success criteria, 2025 premium design standards

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Compliance Analysis**:

✅ **Spec-Driven Development (I)**: Feature spec completed and approved before implementation begins. ✓

✅ **Strict User Isolation (II)**: Frontend enforces user isolation via JWT token verification; all API calls require valid token from Better Auth; cross-user data access prevented by backend filtering (frontend trust depends on backend implementation).

✅ **JWT-Based Stateless Authentication (III)**: Uses Better Auth with JWT tokens; centralized API client (`/lib/api.ts`) automatically attaches Authorization header; frontend handles token storage in secure HTTP-only cookies; 401/403 error handling implemented.

✅ **Technology Stack Fidelity (IV)**: Stack lock respected: Next.js 16+ App Router only, TypeScript strict, Tailwind CSS v4+, shadcn/ui, Better Auth (JWT), optional Framer Motion. No other dependencies permitted.

✅ **Modular Architecture & Monorepo (V)**: Frontend code organized in `/app` (pages), `/components` (reusable), `/lib` (utilities/API). Specs in `/specs/002-premium-nextjs-frontend/`. History/ADRs under `/history/`.

✅ **Testability & Quality Gates (VI)**: Manual visual testing aligned with success criteria. Accessibility testing (WCAG 2.1 AA). Performance testing (Lighthouse >95). Cross-browser and multi-device testing. No code merge without passing tests (enforced by development workflow).

✅ **API Design Standards (VII)**: Frontend consumes REST API with standard HTTP methods. All requests use JWT authorization. Error handling for 400/401/403/404/500 status codes.

⚠️ **Database Design & Normalization (VIII)**: Not applicable to frontend; backend responsibility. Frontend trust that backend enforces user_id filtering.

✅ **Code Quality & Simplicity (IX)**: Minimum viable diff approach; no unrelated refactoring. Avoid premature abstractions. Type safety via TypeScript strict mode.

✅ **Traceability & Documentation (X)**: PHR created for specification phase. Plan (this document) created for planning phase. Tasks and implementation will create additional PHRs. Code references maintained.

**Gate Result**: ✅ PASS — No violations. Frontend spec complies with Phase II constitution. Backend API compliance assumed per constitution Phase II implementation.

## Project Structure

### Documentation (this feature)

```text
specs/002-premium-nextjs-frontend/
├── plan.md                          # This file (/sp.plan output)
├── spec.md                          # Approved feature specification
├── checklists/requirements.md       # Specification quality validation (PASSED)
├── research.md                      # Phase 0: Technology decisions & animation research
├── data-model.md                    # Phase 1: Component hierarchy & state management
├── design-system.md                 # Phase 1: Visual design tokens, colors, typography
├── contracts/                       # Phase 1: API client contracts
│   ├── api-client.ts                # JWT-authenticated API client interface
│   └── types.ts                     # Shared TypeScript types
├── quickstart.md                    # Phase 1: Developer quick start guide
└── tasks.md                         # Phase 2 output (/sp.tasks - NOT created by /sp.plan)
```

### Source Code (Next.js App Router)

```text
frontend/
├── app/
│   ├── layout.tsx                   # Root layout with providers, navbar, theme setup
│   ├── page.tsx                     # Landing page / hero
│   ├── login/page.tsx               # Premium login/signup page (Better Auth integration)
│   ├── tasks/
│   │   ├── page.tsx                 # Main dashboard (masterpiece: responsive list)
│   │   ├── layout.tsx               # Tasks section layout
│   │   └── error.tsx                # Error boundary
│   ├── error.tsx                    # Global error boundary
│   └── not-found.tsx                # 404 page
│
├── components/
│   ├── ui/                          # shadcn/ui components (auto-generated)
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── table.tsx
│   │   ├── dialog.tsx
│   │   ├── input.tsx
│   │   ├── dropdown-menu.tsx
│   │   ├── toast.tsx
│   │   ├── skeleton.tsx
│   │   ├── checkbox.tsx
│   │   ├── badge.tsx
│   │   ├── separator.tsx
│   │   ├── avatar.tsx
│   │   ├── sheet.tsx
│   │   └── toaster.tsx              # Toast provider
│   │
│   ├── TaskCard.tsx                 # Mobile task card component
│   ├── TaskTable.tsx                # Desktop task table component
│   ├── TaskFilters.tsx              # Filter dropdown (All/Pending/Completed)
│   ├── AddTaskDialog.tsx            # Modal for creating tasks
│   ├── EditTaskDialog.tsx           # Modal for editing tasks
│   ├── EmptyState.tsx               # Empty task list state
│   ├── Navbar.tsx                   # Top navigation bar (logo, theme toggle, logout)
│   ├── ChatbotStub.tsx              # Phase 3 chatbot placeholder (floating bubble)
│   ├── LoadingSkeletons.tsx         # Shimmer loading states
│   └── FormFields.tsx               # Reusable form input components with validation
│
├── lib/
│   ├── api.ts                       # JWT-authenticated API client with error handling
│   ├── types.ts                     # Shared TypeScript interfaces
│   ├── constants.ts                 # App constants (URLs, timeouts, animation timings)
│   ├── utils.ts                     # Utility functions (date formatting, validation)
│   └── hooks/
│       ├── useTasks.ts              # Custom hook for task state + CRUD operations
│       ├── useTheme.ts              # Theme switching hook (next-themes)
│       ├── useAuth.ts               # Authentication status hook (Better Auth)
│       └── useToast.ts              # Toast notification hook
│
├── styles/
│   ├── globals.css                  # Global Tailwind setup, custom properties
│   └── animations.css               # Tailwind animation definitions
│
├── middleware.ts                    # Authentication guard middleware
├── package.json                     # Dependencies (Next.js, shadcn/ui, Better Auth, Tailwind, etc.)
├── tsconfig.json                    # TypeScript strict mode configuration
├── next.config.ts                   # Next.js configuration
├── tailwind.config.ts               # Tailwind CSS v4+ configuration with premium palette
└── README.md                        # Setup and development guide
```

**Structure Decision**: Option 2 (Web application) — Next.js frontend using App Router. Source code organized by feature (app/ for pages, components/ for reusable pieces, lib/ for utilities and API client). This aligns with Phase II monorepo structure and Next.js 16+ best practices.

## Complexity Tracking

✅ **No Constitution Violations** — No complexity tracking needed. All design decisions comply with Phase II constitution.

---

## Phase 0: Research & Architectural Decisions

### Key Decision Resolutions

**Decision 1: Animation Library Choice**
- **Selected**: Framer Motion for checkbox toggle spring animation + modal scale-in ONLY; pure Tailwind transitions for everything else
- **Rationale**: Framer Motion provides expressive spring animations (premium feel) for 2 specific micro-interactions where it matters most (checkbox toggle, modal entrance). Everything else uses Tailwind's built-in transitions to minimize bundle impact. This balances premium quality with performance.
- **Tradeoff**: +25KB (Framer Motion minified) vs pure Tailwind, but justified by premium positioning. Alternative (pure Tailwind) would feel less polished for hackathon judges.
- **Implementation**: Install `framer-motion`, use `<motion.input />` for checkbox with `whileHover={{ scale: 1.05 }}` and spring animate on completion.

**Decision 2: Custom Checkbox Toggle Animation**
- **Selected**: Framer Motion spring animation (recommended) with Tailwind scale/transition as fallback
- **Rationale**: Spring animation (`spring: { type: "spring", damping: 12, stiffness: 100 }`) provides delightful micro-interaction that reinforces premium positioning. Feels snappier than basic CSS transition.
- **Implementation**: `motion.div` with custom spring config on checkbox state change.

**Decision 3: Empty State Illustration**
- **Selected**: shadcn/ui icons (Lucide React) + inspirational text only; NO placeholder SVG or Lottie
- **Rationale**: Minimalist design approach consistent with 2025 premium aesthetic. Text "No tasks yet – start your productive day!" is more impactful than generic illustration. Maintains simplicity and bundle size.
- **Implementation**: LucideIcon component (e.g., `<CheckCircle2 />`) + centered text with subtle animation (fade-in).

**Decision 4: Toast Variant Design**
- **Selected**: Custom gradient backgrounds (success: emerald gradient, error: rose/red gradient) built via Tailwind CSS classes; default shadcn toast component with custom styling
- **Rationale**: Custom gradients elevate premium feel without extra dependencies. Shadcn toast provides accessibility and consistent UX.
- **Implementation**: Create `success-toast` and `error-toast` CSS classes with gradient backgrounds; apply via toast component props.

**Decision 5: Modal Backdrop**
- **Selected**: Solid dark overlay with high opacity (not glassmorphism blur) for performance
- **Rationale**: Glassmorphism blur can impact performance on low-end devices (mobile). Solid overlay is faster, still premium-looking, and ensures text readability. 2025 aesthetic tolerates both; performance takes priority.
- **Implementation**: Dialog component with `bg-black/50` (dark mode: `bg-slate-950/50`) overlay.

**Decision 6: Navbar Design**
- **Selected**: Minimal top bar (fixed or static) with logo (left), theme toggle + user avatar with dropdown menu (right)
- **Rationale**: Clean minimal navbar (no sidebar) aligns with modern 2025 design and keeps focus on task content. Avatar dropdown provides quick access to logout and theme toggle without cluttering navbar.
- **Implementation**: Flexbox layout with logo, spacer, theme toggle icon, and Avatar component with DropdownMenu for logout.

### Technology Stack Validation

All decisions respect Phase II constitution:
- ✅ TypeScript strict mode confirmed
- ✅ Next.js 16+ App Router confirmed
- ✅ Tailwind CSS v4+ confirmed
- ✅ shadcn/ui for all UI components confirmed
- ✅ Better Auth for JWT confirmed
- ✅ Framer Motion for approved animations confirmed
- ✅ next-themes for theme management confirmed
- ✅ Lucide React for icons (included with shadcn/ui)

---

## Phase 1: Design & Architecture

### Component Hierarchy & State Management

**Client-Side State** (using React Context + custom hooks):
- `AuthContext`: Current user, JWT token status (from Better Auth)
- `ThemeContext`: Current theme (dark/light), system preference, toggle handler (via next-themes)
- `ToastContext`: Toast queue, add/remove toast (via shadcn toast provider)
- `TasksContext`: Task list, filters, loading state, optimistic updates (local state first, server confirmation)

**Server Components** (default):
- Root layout, landing page, error boundaries
- Data fetching for initial task list load (if needed for SSR)

**Client Components** (`use client`):
- Pages: login, tasks (interactive)
- Components: TaskCard, TaskTable, TaskFilters, dialogs, Navbar, chatbot stub
- Hooks: useTasks, useTheme, useAuth, useToast

### Visual Design System

**Color Palette** (Tailwind CSS custom properties):
- **Neutral Base**: `slate-50` (light bg), `slate-900` (dark bg), `slate-700` (dark text on light), `slate-200` (light text on dark)
- **Primary Accent**: `emerald-500` (success, primary actions), `emerald-600` (hover), `emerald-400` (light mode accents)
- **Secondary Accent**: `indigo-500` (secondary actions), `indigo-600` (hover)
- **Error**: `rose-500` (errors, destructive), `rose-100` (light error bg)
- **Gradients**:
  - Success toast: `linear-gradient(135deg, #10b981 0%, #059669 100%)`
  - Primary CTA: `linear-gradient(135deg, #10b981 0%, #0891b2 100%)`

**Typography**:
- **Font Stack**: `font-sans` (Geist Sans via next/font or system stack: `-apple-system, BlinkMacSystemFont, "Segoe UI"`)
- **Headlines**: `font-bold`, sizes from `2xl` (h1) to `lg` (h3)
- **Body**: `font-normal`, `text-base`
- **Code**: `font-mono`, `text-sm`

**Spacing**:
- 8px grid system: `p-2` (4px), `p-3` (12px), `p-4` (16px), `p-6` (24px), `p-8` (32px)
- Generous whitespace: Minimum 16px padding around content areas
- Desktop max-width: `max-w-6xl` container

**Shadows & Effects**:
- Card shadows: `shadow-sm` (small), `shadow-md` (medium for hover)
- No heavy shadows; prefer subtle elevation
- Rounded corners: `rounded-lg` (cards, buttons), `rounded-full` (avatars)

**Responsive Breakpoints** (mobile-first):
- Default (mobile <640px): Single column, vertical stacks, full width
- `sm:640px`: Large mobile, small tablets
- `md:768px`: Tablet portrait
- `lg:1024px`: Tablet landscape / small desktop
- `xl:1280px`: Desktop

### Responsive Layout Strategy

**Landing Page**:
- Mobile: Full-width hero with centered text, single CTA button
- Desktop: Two-column layout (left text + CTA, right illustration/accent)

**Login/Signup**:
- Mobile: Centered card (400px max), full viewport height, keyboard-aware
- Desktop: Same centered card, but with background gradient/pattern

**Tasks Dashboard**:
- Mobile: Vertical stack of cards (100% width - padding), FAB at bottom
- Tablet: Cards in 2-column grid
- Desktop: Table with full row hover, sidebar space reserved for future

**Task Modals**:
- Mobile: Full-screen or bottom sheet (90vh max)
- Desktop: Centered modal (600px max)

### Optimistic UI & State Management Strategy

**Optimistic Updates** (all CRUD operations):
1. User triggers action (e.g., add task, toggle complete)
2. UI updates IMMEDIATELY with optimistic data (no loading state for simple toggles)
3. API call sends in background
4. On success: Server confirms, no UI change needed
5. On error: Revert UI to previous state, show error toast with retry

**Implementation**:
- `useTasks` hook manages local task list state
- `addTask()` adds to local state instantly, sends POST in background
- `toggleComplete()` flips checkbox immediately, sends PATCH in background
- Error handler reverts state on failure

**Loading States**:
- Simple toggles (checkbox): No skeleton, immediate visual feedback
- Form submissions: Loading spinner inside button
- List loading: Skeleton cards matching final layout
- Transitions: Fade-in for new items, fade-out for deleted items

---

## Phase 2: Implementation Roadmap

### File Generation Order (Critical)

**Foundation Phase** (1-2 hours):
1. `package.json` + `tsconfig.json` — Dependencies, TypeScript strict config
2. `next.config.ts` + `tailwind.config.ts` — Premium palette config
3. `/lib/constants.ts` — App-wide constants
4. `/lib/types.ts` — Shared TypeScript interfaces
5. `/lib/api.ts` — JWT-authenticated API client
6. `/styles/globals.css` — Tailwind setup + custom properties
7. `/app/layout.tsx` — Root layout with providers (Theme, Toast, Auth)
8. `Navbar.tsx` — Header bar component

**Authentication Phase** (1-2 hours):
9. `/app/login/page.tsx` — Premium auth page (Better Auth integration)
10. `middleware.ts` — Authentication guard

**Landing Phase** (30 minutes):
11. `/app/page.tsx` — Landing page hero

**Components Core** (2-3 hours):
12. shadcn/ui components init (`button`, `card`, `table`, `dialog`, `input`, `dropdown-menu`, `toast`, `skeleton`, `checkbox`, `badge`, `separator`, `avatar`, `sheet`)
13. `TaskCard.tsx` — Mobile task card
14. `TaskTable.tsx` — Desktop task table
15. `EmptyState.tsx` — Empty state component
16. `TaskFilters.tsx` — Filter dropdown
17. `AddTaskDialog.tsx` — Add task modal
18. `EditTaskDialog.tsx` — Edit task modal
19. `LoadingSkeletons.tsx` — Skeleton loaders

**Hooks & State** (1 hour):
20. `/lib/hooks/useTasks.ts` — Task CRUD state + optimistic updates
21. `/lib/hooks/useTheme.ts` — Theme switching (next-themes)
22. `/lib/hooks/useAuth.ts` — Auth status
23. `/lib/hooks/useToast.ts` — Toast notifications

**Main Dashboard** (2-3 hours):
24. `/app/tasks/page.tsx` — Main dashboard (masterpiece: responsive layout, filters, FAB, empty state)
25. `/app/tasks/layout.tsx` — Tasks section layout

**Polish & Phase 3** (1-2 hours):
26. `ChatbotStub.tsx` — Chatbot component stub
27. `/styles/animations.css` — Custom animation definitions
28. Error boundaries + 404 page
29. Final visual polish (spacing, colors, micro-interactions)

**Testing & Verification** (2-3 hours):
30. Manual visual testing across devices/browsers
31. Accessibility testing (keyboard, screen reader)
32. Performance audit (Lighthouse)
33. Screenshot capture for judges

### Implementation Phases

**Phase 1: Setup & Foundation** (est. 1-2 hours)
- Initialize Next.js project structure
- Install and configure Tailwind CSS v4+, shadcn/ui, Better Auth, next-themes, Framer Motion
- Create TypeScript types and constants
- Build JWT-authenticated API client (`/lib/api.ts`)
- Setup theme provider and dark/light mode system
- Create root layout with Navbar

**Phase 2: Authentication Excellence** (est. 1-2 hours)
- Integrate Better Auth
- Build premium login/signup page with animated form fields
- Implement authentication middleware
- Add JWT token storage and automatic attach to requests

**Phase 3: Component Library** (est. 2-3 hours)
- Add all shadcn/ui components
- Build reusable components: TaskCard, TaskTable, TaskFilters, dialogs, empty state
- Implement custom hook state management (useTasks, useTheme, useAuth)
- Build loading skeleton components with shimmer effect

**Phase 4: Dashboard Masterpiece** (est. 2-3 hours)
- Build main tasks dashboard with responsive logic
- Implement task list display (desktop table vs mobile cards)
- Add filter controls with smooth animations
- Implement add/edit/delete dialogs with smooth entrances
- Build empty state with inspirational message
- Ensure zero layout shift and perfect alignment

**Phase 5: Interactions & Feedback** (est. 1-2 hours)
- Implement optimistic UI updates for all CRUD operations
- Build beautiful success/error toasts with custom gradients
- Add loading states and shimmer skeletons
- Implement Framer Motion animations (checkbox spring toggle, modal scale-in)
- Add micro-interactions (hover effects, press animations, focus rings)

**Phase 6: Polish & Optimization** (est. 1-2 hours)
- Dark/light mode perfection (contrast checks, color calibration)
- Responsive design refinement (mobile 320px, tablet, desktop)
- Accessibility compliance (ARIA, keyboard navigation, screen reader)
- Performance optimization (bundle size, lazy loading, Server Components)
- ChatbotStub component ready for Phase 3

**Phase 7: Final Verification** (est. 2-3 hours)
- Multi-device testing (mobile, tablet, desktop)
- Cross-browser testing (Chrome, Firefox, Safari)
- Lighthouse audit (target >95 mobile)
- Accessibility audit (keyboard nav, VoiceOver/NVDA)
- Screenshot capture and judge-ready presentation

---

## Testing & Verification Strategy

### Manual Visual Testing Checklist

**Multi-Device Testing**:
- [ ] iPhone 12 (375px): All pages, dark/light mode, rotations
- [ ] iPhone 14 Max (428px): Same as above
- [ ] iPad (768px): Responsive layout, keyboard support
- [ ] iPad Pro (1024px): Sidebar space awareness
- [ ] Desktop 1920px: Full layout, spacing, alignment

**Cross-Browser**:
- [ ] Chrome 120+ (mobile, desktop)
- [ ] Firefox 121+ (mobile, desktop)
- [ ] Safari 17+ (iPhone, iPad, macOS)

**Visual Quality Checks**:
- [ ] No horizontal scroll on any viewport
- [ ] Perfect alignment (8px grid visible)
- [ ] Consistent spacing (no inconsistent margins/paddings)
- [ ] Smooth animations (60fps, no jank)
- [ ] Hover states visible and consistent
- [ ] Focus rings clear and WCAG-compliant (min 3px, high contrast)
- [ ] Mobile touch targets ≥48px
- [ ] Dark/light mode contrast ≥7:1 (WCAG AAA)

**Interaction Flows**:
- [ ] Signup → login → view empty dashboard → add task → toggle complete → edit → delete → logout
- [ ] Open/close modals with smooth animations
- [ ] Filter tasks (All/Pending/Completed) with fade animations
- [ ] Theme toggle instant with no flicker
- [ ] Toast notifications appear and dismiss
- [ ] Keyboard navigation (Tab, Enter, Escape) works on all interactive elements

**Animation Audit**:
- [ ] Checkbox spring toggle smooth
- [ ] Modal entrance scale smooth
- [ ] Filter fade smooth
- [ ] No 3D effects or heavy animations
- [ ] All animations <300ms
- [ ] Framer Motion optimized (prefers-reduced-motion respected)

**Accessibility**:
- [ ] Keyboard-only navigation through all interactive elements
- [ ] VoiceOver (macOS/iOS) reads labels and roles correctly
- [ ] NVDA (Windows) reads properly
- [ ] ARIA labels on buttons and interactive elements
- [ ] Form fields have associated labels
- [ ] Error messages announced to screen readers
- [ ] Color not sole indicator (icons + text)

**Performance**:
- [ ] Lighthouse score >95 (mobile)
- [ ] LCP <2.5s on 4G
- [ ] CLS <0.1 (zero layout shift)
- [ ] FID <100ms
- [ ] All interactions <300ms
- [ ] Bundle size <500KB gzipped

**API Integration**:
- [ ] All task operations work without visual bugs
- [ ] 401/403 errors handled gracefully with redirect to login
- [ ] Network errors show appropriate error toast
- [ ] Optimistic updates revert on error
- [ ] Loading states appear and disappear appropriately

---

## Architectural Decisions Summary

| Decision | Choice | Rationale | Tradeoff |
|----------|--------|-----------|----------|
| Animation Library | Framer Motion (2 animations) + Tailwind (rest) | Premium spring animations for checkbox/modal; minimal bundle impact | +25KB for Framer Motion |
| Checkbox Animation | Framer Motion spring | Delightful micro-interaction | N/A |
| Empty State | Icons + Text | Minimalist, 2025 aesthetic | No illustration |
| Toast Variants | Tailwind gradients | Custom premium gradients without extra deps | Requires CSS classes |
| Modal Backdrop | Solid overlay | Performance on low-end devices | No glassmorphism blur |
| Navbar Design | Minimal top bar | Clean focus on content | No sidebar (reserved for future) |
| State Management | React Context + custom hooks | Simplicity, no Redux overhead | Prop drilling for deep nesting |
| Dark Mode | next-themes | Auto system detection + toggle | Extra dependency |
| API Client | Centralized (`/lib/api.ts`) | JWT auto-attach, error handling | Single point of failure |

---

## Gate Re-evaluation (Post-Phase 1)

After data-model.md and design-system.md are complete, re-run Constitution Check:
- ✅ All Phase 1 decisions documented
- ✅ No new violations introduced
- ✅ Ready for Phase 2 implementation via `/sp.tasks`
