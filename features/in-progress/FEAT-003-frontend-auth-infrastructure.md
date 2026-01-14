# [FEAT-003] Frontend Authentication Infrastructure

## Goal
Build the frontend authentication infrastructure including API client, authentication context, and token management.

## Description
Create the foundational frontend code for handling authentication without building UI pages yet. This includes the API client for backend communication, React Context for auth state, and token storage logic.

---

## Requirements

- **API Client**: TypeScript module for making authenticated requests to backend
- **Authentication Context**: React Context provider for global auth state
- **Token Management**: Store/retrieve/clear JWT tokens in localStorage
- **TypeScript Types**: Interfaces for User, LoginCredentials, RegisterData, Token
- **Error Handling**: Graceful handling of network errors and auth failures

### Non-Goals
- UI pages (login, register, dashboard)
- Form validation
- Loading states or UI feedback
- Token refresh logic

---

## Acceptance Criteria

- [ ] API client module exports functions for `register()` and `login()`
- [ ] API client uses `NEXT_PUBLIC_API_URL` environment variable
- [ ] AuthContext provides `user`, `token`, `login()`, `register()`, `logout()`, `isLoading`
- [ ] Login function stores token in localStorage on success
- [ ] Logout function clears token from localStorage
- [ ] AuthContext loads token from localStorage on mount
- [ ] All TypeScript types properly defined with no `any` types
- [ ] Root layout wrapped with AuthProvider
- [ ] Frontend linting and type checking passes

---

## Technical Context

- API client in `frontend/lib/api.ts`
- Auth context in `frontend/contexts/AuthContext.tsx`
- Use native Fetch API (no axios dependency)
- OAuth2 password flow requires `application/x-www-form-urlencoded` for login
- JSON format for registration
- Client components must use `'use client'` directive

---

## Risks / Open Questions

- **localStorage Security**: Consider httpOnly cookies for production
- **Token Expiration**: No automatic refresh, user must re-login after 30 minutes

---

## Dependencies

- FEAT-001 (Project Setup) must be complete
- FEAT-002 (Backend Auth Service) must be complete

---

## Definition of Done

- All acceptance criteria met
- TypeScript compilation passes with no errors
- ESLint passes with no warnings
- AuthContext can be imported and used in components
