# [FEAT-005] Protected Dashboard and Landing Page

## Goal
Create a protected dashboard for authenticated users and a public landing page with navigation.

## Description
Build the main user interface: a landing page that introduces the platform and a protected dashboard that only authenticated users can access. The dashboard should redirect unauthenticated users to login.

---

## Requirements

- **Landing Page**: Hero section with product description and CTAs at `/`
- **Dashboard Page**: Protected page at `/dashboard` for authenticated users
- **Route Protection**: Redirect to `/login` if accessing dashboard without token
- **Navigation**: Header with logo and auth-aware navigation links
- **Logout Functionality**: Logout button in dashboard that clears session
- **Responsive Design**: Both pages work on mobile and desktop

### Non-Goals
- Dashboard content or widgets
- User profile display
- Settings page
- Content aggregation features

---

## Acceptance Criteria

- [ ] Landing page accessible at `/` with hero section and navigation
- [ ] Landing page has "Get Started" and "Sign In" buttons
- [ ] "Get Started" button links to `/register`
- [ ] "Sign In" button links to `/login`
- [ ] Dashboard accessible at `/dashboard` only when authenticated
- [ ] Unauthenticated access to `/dashboard` redirects to `/login`
- [ ] Dashboard displays welcome message and user interface
- [ ] Dashboard has logout button that clears token and redirects to `/`
- [ ] Both pages are responsive (320px+ mobile, desktop)
- [ ] Navigation is consistent and functional

---

## Technical Context

- Landing page in `frontend/app/page.tsx` (server component, no auth needed)
- Dashboard in `frontend/app/dashboard/page.tsx` (client component, uses auth)
- Use `useEffect` to check token and redirect if missing
- Use `useRouter()` for programmatic navigation
- Tailwind gradient background: `bg-gradient-to-b from-blue-50 to-white`
- Dashboard navigation: white background with shadow

---

## Risks / Open Questions

- **Flash of Content**: Dashboard may briefly show before redirect (acceptable for MVP)

---

## Dependencies

- FEAT-003 (Frontend Auth Infrastructure) must be complete
- FEAT-004 (Login/Registration Pages) must be complete

---

## Design / Mockups

**Landing Page**:
- Top navigation: Logo left, "Sign In" and "Get Started" buttons right
- Hero section: Large heading "Aggregate Content from Anywhere"
- Subheading: "Collect, organize, and manage all your content in one place"
- Primary CTA button: "Start Free Trial"

**Dashboard**:
- Top navigation: Logo left, "Logout" button right (red bg)
- Main content: "Welcome to your Dashboard" heading
- Placeholder text: "Content aggregation features coming soon..."

---

## Definition of Done

- All acceptance criteria met
- Route protection works correctly
- Logout clears token and redirects
- Both pages responsive and styled
- No console errors or warnings
