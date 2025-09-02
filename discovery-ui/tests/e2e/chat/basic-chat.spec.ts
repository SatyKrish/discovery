import { test, expect } from '@playwright/test';
import { ChatPage, MultimodalInputPage } from '../utils/page-objects';

test.describe('Basic Chat Functionality', () => {
  let chatPage: ChatPage;
  let inputPage: MultimodalInputPage;

  test.beforeEach(async ({ page }) => {
    chatPage = new ChatPage(page);
    inputPage = new MultimodalInputPage(page);
    await chatPage.setupTestEnvironment();
  });

  test('should load the chat page successfully', async ({ page }) => {
    // Navigate directly to a chat URL since the app redirects from root
    const chatId = `chat-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    await page.goto(`/chat/${chatId}`);

    // Check that main elements are present
    await expect(chatPage.inputField).toBeVisible();
    await expect(chatPage.sendButton).toBeVisible();
    await expect(chatPage.suggestedActions).toBeVisible();
  });

  test('should send a user message and receive response', async ({ page }) => {
    // Navigate directly to a chat URL since the app redirects from root
    const chatId = `chat-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    await page.goto(`/chat/${chatId}`);

    // Mock the chat API response
    await page.route('/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"text-start","id":"test-id"}
data: {"type":"text-delta","id":"test-id","delta":"Hello! This is a test response."}
data: {"type":"text-end","id":"test-id"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Send a message
    await chatPage.sendMessage('Hello, how are you?');

    // Wait for generation to complete
    await chatPage.waitForGenerationComplete();

    // Check that user message appears
    await expect(chatPage.userMessages).toHaveCount(1);
    expect(await chatPage.getLastUserMessageContent()).toContain('Hello, how are you?');

    // Check that assistant message appears
    await expect(chatPage.assistantMessages).toHaveCount(1);
    expect(await chatPage.getLastAssistantMessageContent()).toContain('Hello! This is a test response.');
  });

  test('should redirect to chat URL after sending message', async ({ page }) => {
    // Navigate directly to a chat URL since the app redirects from root
    const chatId = `chat-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    await page.goto(`/chat/${chatId}`);

    // Mock the chat API
    await page.route('/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"text-start","id":"test-id"}
data: {"type":"text-delta","id":"test-id","delta":"Test response"}
data: {"type":"text-end","id":"test-id"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    await chatPage.sendMessage('Test message');
    await chatPage.waitForGenerationComplete();

    // Check URL contains chat ID
    expect(await chatPage.hasChatIdInUrl()).toBe(true);
  });

  test('should show suggested actions on initial load', async () => {
    // Navigate directly to a chat URL since the app redirects from root
    const chatId = `chat-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    await chatPage.page.goto(`/chat/${chatId}`);

    await expect(chatPage.suggestedActions).toBeVisible();

    // Check that there are multiple suggested actions
    const suggestedButtons = chatPage.page.locator('[data-testid="suggested-actions"] button');
    await expect(suggestedButtons).toHaveCount(6); // Based on the suggested actions in the component
  });

  test('should send message from suggested action', async ({ page }) => {
    // Navigate directly to a chat URL since the app redirects from root
    const chatId = `chat-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    await page.goto(`/chat/${chatId}`);

    // Mock the chat API
    await page.route('/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"text-start","id":"test-id"}
data: {"type":"text-delta","id":"test-id","delta":"Great question about Next.js!"}
data: {"type":"text-end","id":"test-id"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Click on first suggested action
    await chatPage.sendMessageFromSuggestion(0);
    await chatPage.waitForGenerationComplete();

    // Check that suggested actions are hidden after sending message
    await expect(chatPage.suggestedActions).not.toBeVisible();

    // Check that user message contains expected content
    expect(await chatPage.getLastUserMessageContent()).toContain('advantages of using Next.js');
  });

  test('should hide suggested actions after sending message', async ({ page }) => {
    // Navigate directly to a chat URL since the app redirects from root
    const chatId = `chat-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    await page.goto(`/chat/${chatId}`);

    // Verify suggested actions are visible initially
    await expect(chatPage.suggestedActions).toBeVisible();

    // Mock the chat API
    await page.route('/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"text-start","id":"test-id"}
data: {"type":"text-delta","id":"test-id","delta":"Response"}
data: {"type":"text-end","id":"test-id"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Send a message
    await chatPage.sendMessage('Test message');
    await chatPage.waitForGenerationComplete();

    // Check that suggested actions are hidden
    await expect(chatPage.suggestedActions).not.toBeVisible();
  });

  test('should disable send button when input is empty', async () => {
    // Navigate directly to a chat URL since the app redirects from root
    const chatId = `chat-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    await chatPage.page.goto(`/chat/${chatId}`);

    // Send button should be disabled initially
    await expect(chatPage.sendButton).toBeDisabled();

    // Type something
    await chatPage.inputField.fill('Test message');

    // Send button should be enabled
    await expect(chatPage.sendButton).not.toBeDisabled();

    // Clear input
    await chatPage.inputField.clear();

    // Send button should be disabled again
    await expect(chatPage.sendButton).toBeDisabled();
  });

  test('should show stop button during generation and send button after completion', async ({ page }) => {
    // Navigate directly to a chat URL since the app redirects from root
    const chatId = `chat-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    await page.goto(`/chat/${chatId}`);

    // Mock a slow response to test the stop button
    await page.route('/api/chat', async route => {
      // Delay the response
      await new Promise(resolve => setTimeout(resolve, 1000));
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"text-start","id":"test-id"}
data: {"type":"text-delta","id":"test-id","delta":"Slow response"}
data: {"type":"text-end","id":"test-id"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Send message
    await chatPage.sendMessage('Test message');

    // Stop button should be visible during generation
    await expect(chatPage.stopButton).toBeVisible();
    await expect(chatPage.sendButton).not.toBeVisible();

    // Wait for completion
    await chatPage.waitForGenerationComplete();

    // Send button should be visible again
    await expect(chatPage.sendButton).toBeVisible();
    await expect(chatPage.stopButton).not.toBeVisible();
  });

  test('should handle multiple messages in conversation', async ({ page }) => {
    // Navigate directly to a chat URL since the app redirects from root
    const chatId = `chat-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    await page.goto(`/chat/${chatId}`);

    // Mock responses for multiple messages
    let messageCount = 0;
    await page.route('/api/chat', async route => {
      messageCount++;
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"text-start","id":"msg-${messageCount}"}
data: {"type":"text-delta","id":"msg-${messageCount}","delta":"Response ${messageCount}"}
data: {"type":"text-end","id":"msg-${messageCount}"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Send first message
    await chatPage.sendMessage('First message');
    await chatPage.waitForGenerationComplete();

    // Send second message
    await chatPage.sendMessage('Second message');
    await chatPage.waitForGenerationComplete();

    // Check that we have 2 user messages and 2 assistant messages
    await expect(chatPage.userMessages).toHaveCount(2);
    await expect(chatPage.assistantMessages).toHaveCount(2);

    // Check message contents
    const userMessages = await chatPage.userMessages.allTextContents();
    expect(userMessages[0]).toContain('First message');
    expect(userMessages[1]).toContain('Second message');

    const assistantMessages = await chatPage.assistantMessages.allTextContents();
    expect(assistantMessages[0]).toContain('Response 1');
    expect(assistantMessages[1]).toContain('Response 2');
  });
});
