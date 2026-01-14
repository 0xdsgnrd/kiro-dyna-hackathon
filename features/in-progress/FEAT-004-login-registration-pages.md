# [FEAT-004] Login and Registration Pages

## Goal
Create responsive login and registration pages with form handling and integration with the authentication system.

## Description
Build the user-facing authentication pages where users can create accounts and sign in. These pages use the authentication infrastructure from FEAT-003 and provide a clean, mobile-responsive interface.

---

## Requirements

- **Login Page**: Form with username and password fields at `/login`
- **Registration Page**: Form with email, username, and password fields at `/register`
- **Form Handling**: Submit forms and call authentication functions
- **Error Display**: Show error messages for failed authentication
- **Navigation**: Redirect to dashboard on successful auth
- **Responsive Design**: Mobile-first design using Tailwind CSS
- **Loading States**: Disable submit button during API calls

### Non-Goals
- Form validation (client-side)
- Password strength indicator
- "Remember me" checkbox
- Social authentication buttons
- Password visibility toggle

---

## Acceptance Criteria

- [ ] Login page accessible at `/login` with username and password fields
- [ ] Registration page accessible at `/register` with email, username, and password fields
- [ ] Successful login redirects to `/dashboard`
- [ ] Successful registration auto-logs in and redirects to `/dashboard`
- [ ] Failed login shows error message "Invalid credentials"
- [ ] Failed registration shows error message "Registration failed"
- [ ] Forms are responsive and functional on mobile (320px+) and desktop
- [ ] Submit buttons disabled during API request
- [ ] All form inputs have proper labels and placeholders
- [ ] Pages styled with Tailwind CSS matching design system

---

## Technical Context

- Pages in `frontend/app/login/page.tsx` and `frontend/app/register/page.tsx`
- Use `'use client'` directive (forms need client-side interactivity)
- Use `useAuth()` hook from AuthContext
- Use Next.js `useRouter()` for navigation
- Tailwind classes: centered card layout, blue-600 primary color
- Form inputs: `w-full px-4 py-2 border rounded-lg`

---

## Risks / Open Questions

- **Error Messages**: Generic messages may not help users debug issues
- **Validation**: No client-side validation, relies on backend errors

---

## Dependencies

- FEAT-003 (Frontend Auth Infrastructure) must be complete

---

## Design / Mockups

**Login Page**: 
- Centered white card on gray-50 background
- "Sign In" heading (text-3xl font-bold)
- Username input field
- Password input field
- Blue submit button (bg-blue-600 hover:bg-blue-700)

**Register Page**:
- Same layout as login
- "Create Account" heading
- Email, username, and password input fields
- Blue submit button

---

## Definition of Done

- All acceptance criteria met
- Pages render without console errors
- Forms submit successfully to backend
- Error states display properly
- Mobile responsive (tested at 320px, 768px, 1024px)
