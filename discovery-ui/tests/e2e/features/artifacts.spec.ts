import { test, expect } from '@playwright/test';
import { ChatPage, ArtifactPage } from '../utils/page-objects';

test.describe('Artifact Functionality', () => {
  let chatPage: ChatPage;
  let artifactPage: ArtifactPage;

  test.beforeEach(async ({ page }) => {
    chatPage = new ChatPage(page);
    artifactPage = new ArtifactPage(page);
    await chatPage.setupTestEnvironment();
  });

  test('should create text artifact when writing essay', async ({ page }) => {
    await chatPage.goto();

    // Mock the chat API to return artifact creation
    await page.route('/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"data-kind","data":"text"}
data: {"type":"data-id","data":"artifact-123"}
data: {"type":"data-title","data":"Essay about Silicon Valley"}
data: {"type":"data-clear"}
data: {"type":"text-start","id":"text-1"}
data: {"type":"text-delta","id":"text-1","delta":"# Silicon Valley: The Epicenter of Innovation\\n\\nSilicon Valley has become the world's most important economic region..."}
data: {"type":"text-end","id":"text-1"}
data: {"type":"data-finish"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Send message that should trigger artifact creation
    await chatPage.sendMessage('Help me write an essay about Silicon Valley');
    await chatPage.waitForGenerationComplete();

    // Check that artifact is visible
    await expect(artifactPage.artifact).toBeVisible();

    // Check artifact title
    expect(await artifactPage.getTitle()).toBe('Essay about Silicon Valley');

    // Check that assistant message indicates artifact creation
    const assistantMessage = await chatPage.getLastAssistantMessageContent();
    expect(assistantMessage).toContain('document was created');
  });

  test('should create code artifact when writing code', async ({ page }) => {
    await chatPage.goto();

    // Mock the chat API to return code artifact creation
    await page.route('/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"data-kind","data":"code"}
data: {"type":"data-id","data":"code-456"}
data: {"type":"data-title","data":"Python Calculator"}
data: {"type":"data-clear"}
data: {"type":"code-delta","data":"def add(a, b):\\n    return a + b\\n\\nprint(add(5, 3))"}
data: {"type":"data-finish"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Send message that should trigger code artifact creation
    await chatPage.sendMessage('Write a Python function to add two numbers');
    await chatPage.waitForGenerationComplete();

    // Check that artifact is visible
    await expect(artifactPage.artifact).toBeVisible();

    // Check artifact title
    expect(await artifactPage.getTitle()).toBe('Python Calculator');
  });

  test('should create sheet artifact for data analysis', async ({ page }) => {
    await chatPage.goto();

    // Mock the chat API to return sheet artifact creation
    await page.route('/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"data-kind","data":"sheet"}
data: {"type":"data-id","data":"sheet-789"}
data: {"type":"data-title","data":"Sales Data Analysis"}
data: {"type":"data-clear"}
data: {"type":"sheet-delta","data":"Month,Sales,Target\\nJan,10000,12000\\nFeb,15000,13000\\nMar,12000,14000"}
data: {"type":"data-finish"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Send message that should trigger sheet artifact creation
    await chatPage.sendMessage('Create a spreadsheet with sales data for Q1');
    await chatPage.waitForGenerationComplete();

    // Check that artifact is visible
    await expect(artifactPage.artifact).toBeVisible();

    // Check artifact title
    expect(await artifactPage.getTitle()).toBe('Sales Data Analysis');
  });

  test('should close artifact when close button is clicked', async ({ page }) => {
    await chatPage.goto();

    // Mock artifact creation
    await page.route('/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"data-kind","data":"text"}
data: {"type":"data-id","data":"close-test"}
data: {"type":"data-title","data":"Test Document"}
data: {"type":"data-clear"}
data: {"type":"text-delta","data":"Test content"}
data: {"type":"data-finish"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Create artifact
    await chatPage.sendMessage('Create a test document');
    await chatPage.waitForGenerationComplete();

    // Verify artifact is visible
    await expect(artifactPage.artifact).toBeVisible();

    // Close artifact
    await artifactPage.close();

    // Verify artifact is hidden
    await expect(artifactPage.artifact).not.toBeVisible();
  });

  test('should persist artifact content across page reloads', async ({ page }) => {
    await chatPage.goto();

    // Mock artifact creation
    await page.route('/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"data-kind","data":"text"}
data: {"type":"data-id","data":"persist-test"}
data: {"type":"data-title","data":"Persistent Document"}
data: {"type":"data-clear"}
data: {"type":"text-delta","data":"This content should persist"}
data: {"type":"data-finish"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Create artifact
    await chatPage.sendMessage('Create a persistent document');
    await chatPage.waitForGenerationComplete();

    // Verify artifact is visible and has content
    await expect(artifactPage.artifact).toBeVisible();
    expect(await artifactPage.getTitle()).toBe('Persistent Document');

    // Reload page
    await page.reload();

    // Artifact should still be visible (if the chat persists)
    // Note: This test assumes the chat URL is maintained
    const currentUrl = page.url();
    if (currentUrl.includes('/chat/')) {
      await expect(artifactPage.artifact).toBeVisible();
      expect(await artifactPage.getTitle()).toBe('Persistent Document');
    }
  });

  test('should handle multiple artifacts in conversation', async ({ page }) => {
    await chatPage.goto();

    // Mock first artifact creation
    await page.route('/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"data-kind","data":"text"}
data: {"type":"data-id","data":"first-doc"}
data: {"type":"data-title","data":"First Document"}
data: {"type":"data-clear"}
data: {"type":"text-delta","data":"First document content"}
data: {"type":"data-finish"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Create first artifact
    await chatPage.sendMessage('Create first document');
    await chatPage.waitForGenerationComplete();

    // Close first artifact
    await artifactPage.close();

    // Mock second artifact creation
    await page.route('/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"data-kind","data":"code"}
data: {"type":"data-id","data":"second-doc"}
data: {"type":"data-title","data":"Second Document"}
data: {"type":"data-clear"}
data: {"type":"code-delta","data":"print('Hello, World!')"}
data: {"type":"data-finish"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Create second artifact
    await chatPage.sendMessage('Create second document');
    await chatPage.waitForGenerationComplete();

    // Verify second artifact is visible
    await expect(artifactPage.artifact).toBeVisible();
    expect(await artifactPage.getTitle()).toBe('Second Document');
  });

  test('should show artifact loading state during creation', async ({ page }) => {
    await chatPage.goto();

    // Mock slow artifact creation
    await page.route('/api/chat', async route => {
      // Delay response to show loading state
      await new Promise(resolve => setTimeout(resolve, 2000));
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"data-kind","data":"text"}
data: {"type":"data-id","data":"loading-test"}
data: {"type":"data-title","data":"Loading Test"}
data: {"type":"data-clear"}
data: {"type":"text-delta","data":"Content loaded"}
data: {"type":"data-finish"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Send message
    await chatPage.sendMessage('Create loading test document');

    // Check that artifact appears during loading
    await expect(artifactPage.artifact).toBeVisible();

    // Wait for completion
    await chatPage.waitForGenerationComplete();

    // Verify final content
    expect(await artifactPage.getTitle()).toBe('Loading Test');
  });

  test('should handle artifact creation errors gracefully', async ({ page }) => {
    await chatPage.goto();

    // Mock failed artifact creation
    await page.route('/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"text-start","id":"error-test"}
data: {"type":"text-delta","id":"error-test","delta":"Sorry, I couldn't create the artifact due to an error."}
data: {"type":"text-end","id":"error-test"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Send message that should fail
    await chatPage.sendMessage('Create a document that will fail');
    await chatPage.waitForGenerationComplete();

    // Check that no artifact is created
    await expect(artifactPage.artifact).not.toBeVisible();

    // Check error message
    const assistantMessage = await chatPage.getLastAssistantMessageContent();
    expect(assistantMessage).toContain("couldn't create the artifact");
  });
});
