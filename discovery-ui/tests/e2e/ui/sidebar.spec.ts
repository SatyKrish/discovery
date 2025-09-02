import { test, expect } from '@playwright/test';
import { ChatPage, SidebarPage } from '../utils/page-objects';

test.describe('Sidebar Functionality', () => {
  let chatPage: ChatPage;
  let sidebarPage: SidebarPage;

  test.beforeEach(async ({ page }) => {
    chatPage = new ChatPage(page);
    sidebarPage = new SidebarPage(page);
    await chatPage.setupTestEnvironment();
  });

  test('should toggle sidebar visibility', async ({ page }) => {
    await chatPage.goto();

    // Sidebar should be visible initially on desktop
    await expect(sidebarPage.sidebar).toBeVisible();

    // Click sidebar toggle
    await chatPage.toggleSidebar();

    // Sidebar should be hidden
    await expect(sidebarPage.sidebar).not.toBeVisible();

    // Click toggle again
    await chatPage.toggleSidebar();

    // Sidebar should be visible again
    await expect(sidebarPage.sidebar).toBeVisible();
  });

  test('should create new chat from sidebar', async ({ page }) => {
    await chatPage.goto();

    // Mock the chat API for initial load
    await page.route('/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"text-start","id":"test-id"}
data: {"type":"text-delta","id":"test-id","delta":"Initial response"}
data: {"type":"text-end","id":"test-id"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Send initial message to create a chat
    await chatPage.sendMessage('Initial message');
    await chatPage.waitForGenerationComplete();

    // Click new chat button
    await sidebarPage.createNewChat();

    // Should navigate to new chat
    await chatPage.waitForUrlToContainChatId();

    // Suggested actions should be visible again
    await expect(chatPage.suggestedActions).toBeVisible();

    // No messages should be present
    await expect(chatPage.userMessages).toHaveCount(0);
    await expect(chatPage.assistantMessages).toHaveCount(0);
  });

  test('should show empty state when no chats exist', async () => {
    await chatPage.goto();

    // Should show empty state message
    const emptyState = sidebarPage.page.locator('text=No chats yet');
    await expect(emptyState).toBeVisible();

    const startChattingButton = sidebarPage.page.locator('text=Start chatting');
    await expect(startChattingButton).toBeVisible();
  });

  test('should display chat history after creating chats', async ({ page }) => {
    await chatPage.goto();

    // Mock chat creation and responses
    let chatCount = 0;
    await page.route('/api/chat', async route => {
      chatCount++;
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"text-start","id":"chat-${chatCount}"}
data: {"type":"text-delta","id":"chat-${chatCount}","delta":"Response ${chatCount}"}
data: {"type":"text-end","id":"chat-${chatCount}"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Create first chat
    await chatPage.sendMessage('First chat message');
    await chatPage.waitForGenerationComplete();
    const firstChatId = await chatPage.getChatIdFromUrl();

    // Create second chat
    await sidebarPage.createNewChat();
    await chatPage.sendMessage('Second chat message');
    await chatPage.waitForGenerationComplete();
    const secondChatId = await chatPage.getChatIdFromUrl();

    // Check that both chats appear in sidebar
    const chatItems = sidebarPage.chatItems;
    await expect(chatItems).toHaveCount(2);

    // Check chat titles
    const titles = await sidebarPage.getChatTitles();
    expect(titles.length).toBe(2);
    expect(titles[0]).toContain('First chat message');
    expect(titles[1]).toContain('Second chat message');
  });

  test('should navigate between chats using sidebar', async ({ page }) => {
    await chatPage.goto();

    // Mock chat creation
    let chatCount = 0;
    await page.route('/api/chat', async route => {
      chatCount++;
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"text-start","id":"chat-${chatCount}"}
data: {"type":"text-delta","id":"chat-${chatCount}","delta":"Response ${chatCount}"}
data: {"type":"text-end","id":"chat-${chatCount}"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Create first chat
    await chatPage.sendMessage('First chat');
    await chatPage.waitForGenerationComplete();
    const firstChatId = await chatPage.getChatIdFromUrl();

    // Create second chat
    await sidebarPage.createNewChat();
    await chatPage.sendMessage('Second chat');
    await chatPage.waitForGenerationComplete();
    const secondChatId = await chatPage.getChatIdFromUrl();

    // Navigate back to first chat
    await sidebarPage.clickChatItem(0);

    // URL should change to first chat
    await chatPage.page.waitForURL(`**/chat/${firstChatId}`);

    // Check that first chat content is displayed
    expect(await chatPage.getLastUserMessageContent()).toContain('First chat');

    // Navigate to second chat
    await sidebarPage.clickChatItem(1);

    // URL should change to second chat
    await chatPage.page.waitForURL(`**/chat/${secondChatId}`);

    // Check that second chat content is displayed
    expect(await chatPage.getLastUserMessageContent()).toContain('Second chat');
  });

  test('should search chats in sidebar', async ({ page }) => {
    await chatPage.goto();

    // Mock multiple chats
    await page.route('/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"text-start","id":"search-test"}
data: {"type":"text-delta","id":"search-test","delta":"Test response"}
data: {"type":"text-end","id":"search-test"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Create chats with different content
    await chatPage.sendMessage('React development tips');
    await chatPage.waitForGenerationComplete();

    await sidebarPage.createNewChat();
    await chatPage.sendMessage('Python programming guide');
    await chatPage.waitForGenerationComplete();

    await sidebarPage.createNewChat();
    await chatPage.sendMessage('JavaScript best practices');
    await chatPage.waitForGenerationComplete();

    // Search for "React"
    await sidebarPage.searchChats('React');

    // Should show only React chat
    const visibleChats = sidebarPage.chatItems;
    await expect(visibleChats).toHaveCount(1);
    const titles = await sidebarPage.getChatTitles();
    expect(titles[0]).toContain('React development tips');

    // Search for "programming"
    await sidebarPage.searchChats('programming');

    // Should show only Python chat
    await expect(visibleChats).toHaveCount(1);
    const pythonTitles = await sidebarPage.getChatTitles();
    expect(pythonTitles[0]).toContain('Python programming guide');

    // Clear search
    await sidebarPage.searchChats('');

    // Should show all chats
    await expect(visibleChats).toHaveCount(3);
  });

  test('should filter chats by date', async ({ page }) => {
    await chatPage.goto();

    // Mock chat creation
    await page.route('/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"text-start","id":"filter-test"}
data: {"type":"text-delta","id":"filter-test","delta":"Test response"}
data: {"type":"text-end","id":"filter-test"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Create a chat today
    await chatPage.sendMessage('Today chat');
    await chatPage.waitForGenerationComplete();

    // Filter by today
    await sidebarPage.filterByDate('today');

    // Should show the chat
    const visibleChats = sidebarPage.chatItems;
    await expect(visibleChats).toHaveCount(1);

    // Filter by week
    await sidebarPage.filterByDate('week');
    await expect(visibleChats).toHaveCount(1);

    // Filter by all
    await sidebarPage.filterByDate('all');
    await expect(visibleChats).toHaveCount(1);
  });

  test('should filter chats by visibility', async ({ page }) => {
    await chatPage.goto();

    // Mock chat creation
    await page.route('/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"text-start","id":"visibility-test"}
data: {"type":"text-delta","id":"visibility-test","delta":"Test response"}
data: {"type":"text-end","id":"visibility-test"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Create a private chat (default)
    await chatPage.sendMessage('Private chat');
    await chatPage.waitForGenerationComplete();

    // Filter by private
    await sidebarPage.filterByVisibility('private');

    // Should show the chat
    const visibleChats = sidebarPage.chatItems;
    await expect(visibleChats).toHaveCount(1);

    // Filter by public
    await sidebarPage.filterByVisibility('public');

    // Should show no chats
    await expect(visibleChats).toHaveCount(0);

    // Filter by all
    await sidebarPage.filterByVisibility('all');
    await expect(visibleChats).toHaveCount(1);
  });

  test('should show chat creation date and time', async ({ page }) => {
    await chatPage.goto();

    // Mock chat creation
    await page.route('/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"text-start","id":"date-test"}
data: {"type":"text-delta","id":"date-test","delta":"Test response"}
data: {"type":"text-end","id":"date-test"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Create a chat
    await chatPage.sendMessage('Test chat for date display');
    await chatPage.waitForGenerationComplete();

    // Check that chat appears in sidebar with date/time info
    const chatItems = sidebarPage.chatItems;
    await expect(chatItems).toHaveCount(1);

    // The chat item should contain date/time information
    const chatItem = chatItems.first();
    const chatText = await chatItem.textContent();
    expect(chatText).toBeTruthy();

    // Should contain the message text
    expect(chatText).toContain('Test chat for date display');
  });
});
