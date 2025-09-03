import { test, expect } from '@playwright/test';
import { ChatPage } from '../utils/page-objects';
import { TestHelpers } from '../utils/test-helpers';

test.describe('Chat Scrolling Behavior', () => {
  let chatPage: ChatPage;
  let helpers: TestHelpers;

  test.beforeEach(async ({ page }) => {
    chatPage = new ChatPage(page);
    helpers = new TestHelpers(page);

    // Setup test environment
    await chatPage.setupTestEnvironment();

    // Navigate to chat page
    await page.goto('/chat/test-session-scrolling');
    await helpers.waitForPageLoad();
  });

  test('should auto-scroll to bottom when new messages arrive', async ({ page }) => {
    console.log('🧪 Testing auto-scroll on new messages...');

    // Mock API responses for multiple messages
    let messageCount = 0;
    await page.route('/api/chat', async route => {
      messageCount++;
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"text-start","id":"msg-${messageCount}"}
data: {"type":"text-delta","id":"msg-${messageCount}","delta":"Response ${messageCount} - This is a longer response to test scrolling behavior with more content."}
data: {"type":"text-end","id":"msg-${messageCount}"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Get initial scroll position
    const scrollContainer = page.locator('.flex-1.overflow-y-auto');
    const initialScrollTop = await scrollContainer.evaluate(el => el.scrollTop);
    const initialScrollHeight = await scrollContainer.evaluate(el => el.scrollHeight);

    console.log(`📊 Initial scroll: top=${initialScrollTop}, height=${initialScrollHeight}`);

    // Send first message
    await chatPage.sendMessage('First message for scrolling test');
    await helpers.waitForGenerationComplete();

    // Check that we auto-scrolled to bottom
    await page.waitForTimeout(500); // Wait for smooth scroll
    const afterFirstScrollTop = await scrollContainer.evaluate(el => el.scrollTop);
    const afterFirstScrollHeight = await scrollContainer.evaluate(el => el.scrollHeight);

    console.log(`📊 After first message: top=${afterFirstScrollTop}, height=${afterFirstScrollHeight}`);

    // Should be at or near bottom
    const isNearBottomAfterFirst = afterFirstScrollHeight - afterFirstScrollTop - (await scrollContainer.evaluate(el => el.clientHeight)) < 50;
    expect(isNearBottomAfterFirst).toBe(true);

    // Send second message
    await chatPage.sendMessage('Second message to test continued scrolling');
    await helpers.waitForGenerationComplete();

    // Check that we auto-scrolled again
    await page.waitForTimeout(500);
    const afterSecondScrollTop = await scrollContainer.evaluate(el => el.scrollTop);
    const afterSecondScrollHeight = await scrollContainer.evaluate(el => el.scrollHeight);

    console.log(`📊 After second message: top=${afterSecondScrollTop}, height=${afterSecondScrollHeight}`);

    // Should still be at or near bottom
    const isNearBottomAfterSecond = afterSecondScrollHeight - afterSecondScrollTop - (await scrollContainer.evaluate(el => el.clientHeight)) < 50;
    expect(isNearBottomAfterSecond).toBe(true);

    // Verify we have both message pairs
    await expect(chatPage.userMessages).toHaveCount(2);
    await expect(chatPage.assistantMessages).toHaveCount(2);

    console.log('✅ Auto-scroll test passed');
  });

  test('should not auto-scroll when user manually scrolls up', async ({ page }) => {
    console.log('🧪 Testing manual scroll preservation...');

    // Mock API responses
    let messageCount = 0;
    await page.route('/api/chat', async route => {
      messageCount++;
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"text-start","id":"msg-${messageCount}"}
data: {"type":"text-delta","id":"msg-${messageCount}","delta":"Response ${messageCount} - This is content that should not cause auto-scroll when user is reading above."}
data: {"type":"text-end","id":"msg-${messageCount}"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Send first message and wait for completion
    await chatPage.sendMessage('First message');
    await helpers.waitForGenerationComplete();

    // Wait for auto-scroll to complete
    await page.waitForTimeout(1000);

    // Manually scroll to top (away from bottom)
    const scrollContainer = page.locator('.flex-1.overflow-y-auto');
    await scrollContainer.evaluate(el => el.scrollTop = 0);

    // Verify we're not at bottom
    const scrollTopAfterManual = await scrollContainer.evaluate(el => el.scrollTop);
    const scrollHeight = await scrollContainer.evaluate(el => el.scrollHeight);
    const clientHeight = await scrollContainer.evaluate(el => el.clientHeight);

    console.log(`📊 After manual scroll up: top=${scrollTopAfterManual}, height=${scrollHeight}, client=${clientHeight}`);

    // Should NOT be at bottom
    const isAtBottomAfterManual = scrollHeight - scrollTopAfterManual - clientHeight < 50;
    expect(isAtBottomAfterManual).toBe(false);

    // Send second message
    await chatPage.sendMessage('Second message - should NOT auto-scroll');
    await helpers.waitForGenerationComplete();

    // Wait a bit for potential auto-scroll
    await page.waitForTimeout(1000);

    // Check scroll position - should still be near the top (not auto-scrolled)
    const scrollTopAfterSecond = await scrollContainer.evaluate(el => el.scrollTop);
    console.log(`📊 After second message: top=${scrollTopAfterSecond}`);

    // Should still be away from bottom (not auto-scrolled)
    const isAtBottomAfterSecond = scrollHeight - scrollTopAfterSecond - clientHeight < 50;
    expect(isAtBottomAfterSecond).toBe(false);

    // Should be close to where we manually scrolled
    expect(Math.abs(scrollTopAfterSecond - scrollTopAfterManual)).toBeLessThan(100);

    console.log('✅ Manual scroll preservation test passed');
  });

  test('should show scroll-to-bottom button when scrolled up', async ({ page }) => {
    console.log('🧪 Testing scroll-to-bottom button...');

    // Mock API response
    await page.route('/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"text-start","id":"test-msg"}
data: {"type":"text-delta","id":"test-msg","delta":"This is a test response for the scroll-to-bottom button test."}
data: {"type":"text-end","id":"test-msg"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Send message to create some content
    await chatPage.sendMessage('Test message for scroll button');
    await helpers.waitForGenerationComplete();

    // Wait for auto-scroll
    await page.waitForTimeout(1000);

    // Scroll to top manually
    const scrollContainer = page.locator('.flex-1.overflow-y-auto');
    await scrollContainer.evaluate(el => el.scrollTop = 0);

    // Wait for scroll-to-bottom button to appear
    await page.waitForTimeout(500);

    // Check if scroll-to-bottom button is visible
    const scrollButton = chatPage.scrollToBottomButton;
    await expect(scrollButton).toBeVisible();

    console.log('✅ Scroll-to-bottom button is visible when scrolled up');

    // Click the scroll-to-bottom button
    await scrollButton.click();

    // Wait for smooth scroll
    await page.waitForTimeout(1000);

    // Verify we're back at bottom
    const finalScrollTop = await scrollContainer.evaluate(el => el.scrollTop);
    const finalScrollHeight = await scrollContainer.evaluate(el => el.scrollHeight);
    const finalClientHeight = await scrollContainer.evaluate(el => el.clientHeight);

    const isAtBottomAfterClick = finalScrollHeight - finalScrollTop - finalClientHeight < 50;
    expect(isAtBottomAfterClick).toBe(true);

    console.log('✅ Scroll-to-bottom button works correctly');
  });

  test('should handle multiple message exchanges with proper scrolling', async ({ page }) => {
    console.log('🧪 Testing multiple message exchanges...');

    // Mock API responses for multiple exchanges
    let exchangeCount = 0;
    await page.route('/api/chat', async route => {
      exchangeCount++;
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"text-start","id":"exchange-${exchangeCount}"}
data: {"type":"text-delta","id":"exchange-${exchangeCount}","delta":"Exchange ${exchangeCount}: This is a response with enough content to test scrolling behavior across multiple conversational turns."}
data: {"type":"text-end","id":"exchange-${exchangeCount}"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    const scrollContainer = page.locator('.flex-1.overflow-y-auto');

    // Send multiple messages
    const messageCount = 4;
    for (let i = 1; i <= messageCount; i++) {
      console.log(`📤 Sending message ${i}/${messageCount}`);

      await chatPage.sendMessage(`Message ${i} in multi-turn conversation`);
      await helpers.waitForGenerationComplete();

      // Wait for auto-scroll
      await page.waitForTimeout(800);

      // Verify we're at bottom after each exchange
      const scrollTop = await scrollContainer.evaluate(el => el.scrollTop);
      const scrollHeight = await scrollContainer.evaluate(el => el.scrollHeight);
      const clientHeight = await scrollContainer.evaluate(el => el.clientHeight);

      const isAtBottom = scrollHeight - scrollTop - clientHeight < 50;
      expect(isAtBottom).toBe(true);

      console.log(`✅ After message ${i}: at bottom = ${isAtBottom}`);
    }

    // Verify final state
    await expect(chatPage.userMessages).toHaveCount(messageCount);
    await expect(chatPage.assistantMessages).toHaveCount(messageCount);

    console.log('✅ Multiple message exchanges test passed');
  });

  test('should auto-scroll during assistant response streaming', async ({ page }) => {
    console.log('🧪 Testing auto-scroll during streaming response...');

    // Mock a streaming response with multiple chunks
    await page.route('/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"text-start","id":"streaming-test"}
data: {"type":"text-delta","id":"streaming-test","delta":"This is the first part of a streaming response."}
data: {"type":"text-delta","id":"streaming-test","delta":" Here is the second part with more content."}
data: {"type":"text-delta","id":"streaming-test","delta":" And finally the third part to complete the response."}
data: {"type":"text-end","id":"streaming-test"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    const scrollContainer = page.locator('.flex-1.overflow-y-auto');

    // Send message
    await chatPage.sendMessage('Test streaming response scrolling');

    // Wait for response to start
    await page.waitForTimeout(500);

    // Check scroll position during streaming
    const scrollTopDuringStream = await scrollContainer.evaluate(el => el.scrollTop);
    const scrollHeightDuringStream = await scrollContainer.evaluate(el => el.scrollHeight);

    console.log(`📊 During streaming: top=${scrollTopDuringStream}, height=${scrollHeightDuringStream}`);

    // Wait for completion
    await helpers.waitForGenerationComplete();

    // Final check - should be at bottom
    await page.waitForTimeout(500);
    const finalScrollTop = await scrollContainer.evaluate(el => el.scrollTop);
    const finalScrollHeight = await scrollContainer.evaluate(el => el.scrollHeight);
    const finalClientHeight = await scrollContainer.evaluate(el => el.clientHeight);

    const isAtBottomFinal = finalScrollHeight - finalScrollTop - finalClientHeight < 50;
    expect(isAtBottomFinal).toBe(true);

    console.log('✅ Streaming response scrolling test passed');
  });
});
