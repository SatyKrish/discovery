# Discovery UI Test Suite

A comprehensive end-to-end test suite for the Discovery UI application using Playwright.

## Overview

This test suite covers all major functionality of the Discovery UI chat application, including:

- **Basic Chat Functionality**: Message sending, receiving, and conversation flow
- **UI Interactions**: Theme toggling, sidebar navigation, responsive design
- **Advanced Features**: Artifact creation, multimodal input, file uploads
- **Error Handling**: Network failures, invalid inputs, edge cases

## Test Structure

```
tests/
├── e2e/                          # End-to-end tests
│   ├── chat/                     # Basic chat functionality
│   │   └── basic-chat.spec.ts    # Core messaging tests
│   ├── ui/                       # UI interaction tests
│   │   ├── theme-toggle.spec.ts  # Theme switching
│   │   └── sidebar.spec.ts       # Sidebar navigation
│   ├── features/                 # Advanced feature tests
│   │   ├── artifacts.spec.ts     # Document/code artifact creation
│   │   └── multimodal-input.spec.ts # File upload and attachments
│   └── utils/                    # Test utilities and helpers
│       ├── page-objects.ts       # Page object models
│       ├── test-helpers.ts       # Common test utilities
│       ├── global-setup.ts       # Test suite setup
│       └── global-teardown.ts    # Test suite cleanup
└── README.md                     # This file
```

## Getting Started

### Prerequisites

- Node.js 18+
- npm or pnpm
- Discovery UI application running

### Installation

1. Install dependencies:
```bash
cd discovery-ui
npm install
```

2. Install Playwright browsers:
```bash
npx playwright install
```

### Running Tests

#### Run all tests
```bash
npm run test
```

#### Run specific test file
```bash
npx playwright test tests/e2e/chat/basic-chat.spec.ts
```

#### Run tests in specific browser
```bash
npx playwright test --project=e2e-firefox
```

#### Run tests in headed mode (visible browser)
```bash
npx playwright test --headed
```

#### Run tests with debugging
```bash
npx playwright test --debug
```

#### Generate test report
```bash
npx playwright show-report
```

### Test Configuration

The test suite is configured in `playwright.config.ts` with:

- **Multiple browsers**: Chrome, Firefox, Safari, Mobile Safari
- **Parallel execution**: Tests run in parallel for faster execution
- **Automatic retries**: Failed tests retry automatically
- **Screenshots and videos**: Captured on test failures
- **Trace collection**: For debugging failed tests

## Test Categories

### 1. Basic Chat Tests (`chat/basic-chat.spec.ts`)

Tests core chat functionality:
- ✅ Page loading and initial state
- ✅ Sending and receiving messages
- ✅ URL navigation and chat IDs
- ✅ Suggested actions interaction
- ✅ Send/stop button state management
- ✅ Multiple message conversations
- ✅ Input validation and button states

### 2. UI Interaction Tests (`ui/`)

#### Theme Toggle (`theme-toggle.spec.ts`)
- ✅ Light/dark theme switching
- ✅ Theme persistence in localStorage
- ✅ Theme application to all UI elements
- ✅ Theme persistence across page reloads
- ✅ Correct theme icon display

#### Sidebar (`sidebar.spec.ts`)
- ✅ Sidebar toggle visibility
- ✅ New chat creation
- ✅ Empty state handling
- ✅ Chat history display
- ✅ Navigation between chats
- ✅ Search functionality
- ✅ Date and visibility filtering

### 3. Advanced Features (`features/`)

#### Artifacts (`artifacts.spec.ts`)
- ✅ Text artifact creation (essays, documents)
- ✅ Code artifact creation (Python, JavaScript)
- ✅ Sheet artifact creation (spreadsheets)
- ✅ Artifact closing and persistence
- ✅ Multiple artifact handling
- ✅ Loading states and error handling

#### Multimodal Input (`multimodal-input.spec.ts`)
- ✅ Image file attachment and upload
- ✅ Multiple file attachments
- ✅ Attachment preview display
- ✅ File upload error handling
- ✅ Different file type support
- ✅ Drag and drop functionality
- ✅ Upload progress indication
- ✅ Large file handling

## Page Objects

The test suite uses the Page Object Model pattern for maintainable tests:

### ChatPage
Handles main chat interface interactions:
```typescript
const chatPage = new ChatPage(page);
await chatPage.sendMessage('Hello!');
await chatPage.waitForGenerationComplete();
```

### SidebarPage
Manages sidebar navigation and chat history:
```typescript
const sidebarPage = new SidebarPage(page);
await sidebarPage.createNewChat();
await sidebarPage.searchChats('React');
```

### ArtifactPage
Handles artifact creation and interaction:
```typescript
const artifactPage = new ArtifactPage(page);
await artifactPage.close();
expect(await artifactPage.getTitle()).toBe('My Document');
```

## Test Helpers

### TestHelpers Class
Provides common utilities for all tests:
```typescript
const helpers = new TestHelpers(page);
await helpers.mockChatAPI({ response: 'mock data' });
await helpers.waitForGenerationComplete();
```

### Mock APIs
Tests use mocked API responses for consistent testing:
- **Chat API**: Mocked responses for different scenarios
- **File Upload API**: Simulated file uploads
- **Document API**: Artifact creation and management

## Best Practices

### Writing Tests

1. **Use descriptive test names**:
```typescript
test('should send message and receive response', async () => {
  // Test implementation
});
```

2. **Group related tests**:
```typescript
test.describe('Chat Functionality', () => {
  test('should send message', () => { /* ... */ });
  test('should receive response', () => { /* ... */ });
});
```

3. **Use page objects**:
```typescript
const chatPage = new ChatPage(page);
await chatPage.sendMessage('test');
```

4. **Mock external dependencies**:
```typescript
await page.route('/api/chat', async route => {
  await route.fulfill({ status: 200, body: mockResponse });
});
```

### Test Data

- Use realistic test data that matches production scenarios
- Mock API responses to ensure consistent test results
- Test both success and error scenarios
- Include edge cases and boundary conditions

### Assertions

- Use specific assertions that clearly describe expected behavior
- Test both positive and negative scenarios
- Verify UI state changes, not just API responses
- Check accessibility attributes where relevant

## Debugging Tests

### Common Debugging Techniques

1. **Run tests in headed mode**:
```bash
npx playwright test --headed
```

2. **Use browser developer tools**:
```typescript
await page.pause(); // Pauses test execution
```

3. **Take screenshots on failure**:
```typescript
await page.screenshot({ path: 'debug.png' });
```

4. **Check test traces**:
```bash
npx playwright show-trace test-results/trace.zip
```

### Debugging Failed Tests

1. Check the HTML report for screenshots and videos
2. Use trace files to replay test execution
3. Add console logging to understand test flow
4. Use `page.pause()` to inspect the page state

## CI/CD Integration

The test suite is designed to work with CI/CD pipelines:

### GitHub Actions Example
```yaml
- name: Run Playwright tests
  run: npm run test
  env:
    CI: true
```

### Parallel Execution
Tests run in parallel by default for faster execution:
- **Local**: 4 workers
- **CI**: 2 workers with retries

### Test Results
- **HTML Report**: Generated automatically
- **Screenshots**: Captured on failures
- **Videos**: Recorded for failed tests
- **Traces**: Available for debugging

## Contributing

### Adding New Tests

1. Create test file in appropriate directory
2. Follow existing naming conventions
3. Use page objects and test helpers
4. Add proper test descriptions
5. Include both positive and negative test cases

### Test File Naming
- Use `.spec.ts` extension
- Use kebab-case for file names
- Group related tests in subdirectories

### Code Style
- Use TypeScript for type safety
- Follow existing code patterns
- Add JSDoc comments for complex functions
- Use descriptive variable names

## Troubleshooting

### Common Issues

1. **Tests timing out**:
   - Increase timeout in `playwright.config.ts`
   - Check for slow network requests
   - Use `page.waitForLoadState()` for page loads

2. **Flaky tests**:
   - Add proper wait conditions
   - Use `expect().toBeVisible()` instead of timeouts
   - Mock external dependencies

3. **Browser-specific failures**:
   - Test in multiple browsers
   - Use browser-specific test configurations
   - Check for browser compatibility issues

### Getting Help

- Check Playwright documentation: https://playwright.dev/
- Review existing test patterns in the codebase
- Use the HTML test report for debugging
- Check browser console for JavaScript errors

## Performance

### Test Execution Time
- **Parallel execution**: Tests run concurrently
- **Smart retries**: Only failed tests retry
- **Selective test runs**: Run only relevant tests

### Optimization Tips
- Use `test.describe.parallel()` for independent test groups
- Mock slow API calls
- Use `page.route()` to intercept and mock network requests
- Avoid unnecessary waits and sleeps

## Future Enhancements

### Planned Improvements
- [ ] Visual regression testing with Percy/Applitools
- [ ] Performance testing integration
- [ ] Accessibility testing with axe-playwright
- [ ] API testing integration
- [ ] Cross-browser visual comparison
- [ ] Mobile testing expansion
- [ ] Component testing with Storybook

### Test Coverage Goals
- [ ] 90%+ code coverage
- [ ] All critical user journeys tested
- [ ] Error scenarios and edge cases covered
- [ ] Accessibility compliance verified
- [ ] Performance benchmarks established
