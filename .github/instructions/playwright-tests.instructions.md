---
applyTo: "**/tests/*.spec.ts"
---

## Playwright test requirements

When writing Playwright tests, please follow these guidelines to ensure consistency and maintainability:
```
1. **Use stable locators** - Prefer `getByRole()`, `getByText()`, and `getByTestId()` over CSS selectors or XPath
1. **Write isolated tests** - Each test should be independent and not rely on other tests' state
1. **Follow naming conventions** - Use descriptive test names and `*.spec.ts` file naming
1. **Implement proper assertions** - Use Playwright's `expect()` with specific matchers like `toHaveText()`, `toBeVisible()`
1. **Leverage auto-wait** - Avoid manual `setTimeout()` and rely on Playwright's built-in waiting mechanisms
1. **Configure cross-browser testing** - Test across Chromium, Firefox, and WebKit browsers
1. **Use Page Object Model** - Organize selectors and actions into reusable page classes for maintainability
1. **Handle dynamic content** - Properly wait for elements to load and handle loading states
1. **Set up proper test data** - Use beforeEach/afterEach hooks for test setup and cleanup
1. **Configure CI/CD integration** - Set up headless mode, screenshots on failure, and parallel execution
```

### Discovery-specific guidance
- Location and runner
	- UI lives in `discovery-ui/`. Run tests from that folder with npm: `npm run test` or `npx playwright test`.
	- Prefer a `webServer` in Playwright config to boot Next.js (dev or prod) before tests.
- Base routes and APIs to cover or stub
	- Pages: `/` (chat), `/library` (library view)
	- Next API proxies: `/api/chats`, `/api/messages`, and `/api/chats/[id]`
	- In tests, stub these with `page.route()` to avoid hitting real backends; assert request payloads.
- Stable locators in this UI (examples)
	- New chat: `page.getByRole('button', { name: 'New chat' })`
	- Library: `page.getByRole('link', { name: 'Library' })`
	- Search chats: `page.getByRole('button', { name: 'Search chats' })` (collapsed sidebar) or `page.getByPlaceholder('Search chats')`
	- Artifacts toggle: `page.getByRole('button', { name: 'Artifacts' })`
	- Theme toggle: `page.getByRole('button', { name: /Switch to (dark|light)/ })`
	- Composer: `page.getByPlaceholder('Message Discovery Agent…')`
	- Delete chat button: `page.getByRole('button', { name: /Delete chat / })`
- State isolation
	- Clear local storage key `discovery:lastChatId` between tests.
	- Avoid relying on persisted sessions; use `test.use({ storageState: 'empty' })` or per-test cleanup.
- Cross-browser and CI
	- Configure projects for Chromium, Firefox, WebKit in `playwright.config.ts`.
	- Run headless in CI with trace on, screenshots and videos on failure.
	- Use npm scripts (e.g., `npm run build && npm start`) with `webServer` to serve the app for E2E tests.
