# Discovery UI — Tasks & Progress

This file tracks the current status, improvements, and pending functionality for `discovery-ui` with actionable checklists. Update it as features land to keep visibility high.

Last updated: 2025-08-28

## Status at a glance

- [x] Sidebar: search filtering with focus shortcut (Cmd/Ctrl+K)
- [x] Library navigation to a real route (`/library`, placeholder)
- [x] Keyboard shortcuts: New Chat (Cmd/Ctrl+N), Toggle sidebar (Cmd/Ctrl+/), Toggle artifacts (Cmd/Ctrl+Shift+A), Esc blur
- [x] Pin/Unpin wired in UI (optimistic); provider hook in place (no-op tolerated)
- [x] Chat create persistence flow (temp → POST → replace with server chat when available)
- [x] Delete chat end-to-end (UI confirm → optimistic remove → DELETE proxy)
- [x] Sidebar collapsed: hide chat sessions; keep footer aligned; stable icon order
- [x] Remove duplicate search trigger and chats empty-state banner
- [x] Header: hide fallback “New Chat” title when no chat is selected

## Current focus (high ROI next)

### 1) Attachments — end-to-end
- [x] Composer: file picker (hidden input + Paperclip button)
- [x] Show selected attachments as removable chips (filename, size)
- [x] Upload route: Next.js API proxy (`/api/uploads`) → backend; handle progress/errors
- [x] Provider: include uploaded attachment references/URIs in `sendMessage`
- [x] Artifact render: display `type: "file"` with download and preview affordances
- [x] Error handling: surface upload/send failures with retry and removal options
- [x] Restrict uploads to docs/spreadsheets/code; block audio/video
- [x] Tests: unit (attachment state), E2E (attach → send → artifact visible)

### 2) Library view (MVP)
- [x] Fetch pinned and recent artifacts (provider additions + API proxies)
- [x] UI: grid with filters (type, pinned, recent)
- [x] Actions: open in chat, unpin, copy link
- [x] Empty and loading states
- [x] E2E: navigate → filter → unpin reflects in chat

### 3) Virtualized thread
- [x] Integrate list virtualization (`@tanstack/react-virtual`) with fallback in tests
- [x] Maintain autoscroll to bottom on new messages; preserve position via element measurement
- [x] Tests: large thread smoke (performance sanity)

### 4) Responsive/mobile polish
- [ ] Collapsible sidebar UX on small screens (gesture, button)
- [ ] Composer layout: controls stacking, touch target sizes
- [ ] Header truncation and affordances (artifacts button placement)
- [ ] Viewport-safe areas (iOS safe-area insets)

### 5) Error/empty states
- [ ] Chats list: load error with retry
- [ ] Messages: empty chat prompt (helpful hints), load error with retry
- [ ] Artifacts: per-card load failures (table/file) with retry CTA

## Quality, testing, and accessibility

- [ ] Unit: `normalizeTable` cases (array, columns+rows, object, primitive)
- [ ] Unit: provider normalization for chats/messages
- [x] E2E: basic flow — start chat → send → artifact visible
- [ ] E2E: sidebar collapsed/expanded behavior and shortcuts
- [ ] A11y: ensure roles/labels for icon-only controls (Menu, Search, Theme)
- [ ] A11y: keyboard navigation through sidebar and composer

## Performance

- [ ] Bundle triage for `discovery-ui` (analyze + identify big deps)
- [ ] Lazy-load non-critical panels (artifacts, large tables)
- [ ] Memoize expensive renders (e.g., markdown) and artifact cards

## Developer experience

- [x] Add npm script for E2E (e.g., `test:e2e`) with Playwright
- [x] Playwright config: `webServer` (npm run build/start), multi-browser projects, trace/screenshot on failure
- [ ] Pre-commit: lint + typecheck (optional Husky hook)
- [ ] Document environment: `BACKEND_BASE_URL` for API proxies in `.env.local`

## Integration points (provider + API)

- [ ] Provider: `togglePin` implementation when backend supports it
- [ ] Provider: `createChat`/`deleteChat` error surfacing to UI
- [x] API: `/api/uploads` and any artifact retrieval proxies
- [ ] Consistent shapes for chats/messages/artifacts (normalize at provider boundary)

## Conventions and locators (testing helpers)

- Composer input: `getByPlaceholder('Message Discovery Agent…')`
- New chat: `getByRole('button', { name: 'New chat' })`
- Library: `getByRole('link', { name: 'Library' })`
- Search chats: `getByPlaceholder('Search chats')` (expanded) or `getByRole('button', { name: 'Search chats' })` (collapsed)
- Artifacts toggle: `getByRole('button', { name: 'Artifacts' })`
- Theme toggle: `getByRole('button', { name: /Switch to (dark|light)/ })`
- Local storage key to reset in tests: `discovery:lastChatId`

## Session log

| Date       | Summary                                                           | PR/Link |
|------------|-------------------------------------------------------------------|---------|
| 2025-08-28 | Collapsed sidebar polish, delete chat E2E, header title behavior  |         |

## Nice-to-haves / backlog

- [ ] Theming presets and contrast audit
- [ ] Inline artifact expanders (modal/gallery for images, full-screen table)
- [ ] Message editing and resend
- [ ] Chat renaming inline
- [ ] Offline/slow-network indicators for fetches
