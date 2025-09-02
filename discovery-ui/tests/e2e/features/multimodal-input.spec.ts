import { test, expect } from '@playwright/test';
import { ChatPage, MultimodalInputPage } from '../utils/page-objects';

test.describe('Multimodal Input Functionality', () => {
  let chatPage: ChatPage;
  let inputPage: MultimodalInputPage;

  test.beforeEach(async ({ page }) => {
    chatPage = new ChatPage(page);
    inputPage = new MultimodalInputPage(page);
    await chatPage.setupTestEnvironment();
  });

  test('should attach image file and send with message', async ({ page }) => {
    await chatPage.goto();

    // Mock file upload API
    await page.route('/api/files/upload', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          url: 'https://example.com/uploaded-image.jpg',
          pathname: 'uploaded-image.jpg',
          contentType: 'image/jpeg',
        }),
      });
    });

    // Mock chat API
    await page.route('/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"text-start","id":"image-test"}
data: {"type":"text-delta","id":"image-test","delta":"I can see this is a beautiful landscape painting!"}
data: {"type":"text-end","id":"image-test"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Add image attachment
    await chatPage.addImageAttachment();

    // Check that attachment preview is visible
    await expect(chatPage.attachmentsPreview).toBeVisible();

    // Send message with attachment
    await chatPage.sendMessage('What do you see in this image?');
    await chatPage.waitForGenerationComplete();

    // Check that attachment is included in user message
    const userMessage = await chatPage.getLastUserMessageContent();
    expect(userMessage).toContain('What do you see in this image?');

    // Check assistant response
    const assistantMessage = await chatPage.getLastAssistantMessageContent();
    expect(assistantMessage).toContain('beautiful landscape painting');
  });

  test('should show attachment preview with correct file info', async ({ page }) => {
    await chatPage.goto();

    // Mock file upload API
    await page.route('/api/files/upload', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          url: 'https://example.com/test-image.jpg',
          pathname: 'test-image.jpg',
          contentType: 'image/jpeg',
        }),
      });
    });

    // Add image attachment
    await chatPage.addImageAttachment();

    // Check attachment preview elements
    await expect(chatPage.attachmentsPreview).toBeVisible();

    // Check that filename is displayed
    const previewText = await chatPage.attachmentsPreview.textContent();
    expect(previewText).toContain('test-image.jpg');
  });

  test('should handle multiple file attachments', async ({ page }) => {
    await chatPage.goto();

    // Mock file upload API for multiple files
    let uploadCount = 0;
    await page.route('/api/files/upload', async route => {
      uploadCount++;
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          url: `https://example.com/file-${uploadCount}.jpg`,
          pathname: `file-${uploadCount}.jpg`,
          contentType: 'image/jpeg',
        }),
      });
    });

    // Add multiple attachments
    await chatPage.addImageAttachment();
    await chatPage.addImageAttachment();

    // Check that both attachments are shown
    const attachmentElements = page.locator('[data-testid="input-attachment-preview"]');
    await expect(attachmentElements).toHaveCount(2);
  });

  test('should clear attachments after sending message', async ({ page }) => {
    await chatPage.goto();

    // Mock APIs
    await page.route('/api/files/upload', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          url: 'https://example.com/test.jpg',
          pathname: 'test.jpg',
          contentType: 'image/jpeg',
        }),
      });
    });

    await page.route('/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: {"type":"text-start","id":"clear-test"}
data: {"type":"text-delta","id":"clear-test","delta":"Attachment received"}
data: {"type":"text-end","id":"clear-test"}
data: {"type":"finish","finishReason":"stop"}
data: [DONE]`,
      });
    });

    // Add attachment
    await chatPage.addImageAttachment();
    await expect(chatPage.attachmentsPreview).toBeVisible();

    // Send message
    await chatPage.sendMessage('Test with attachment');
    await chatPage.waitForGenerationComplete();

    // Check that attachments are cleared
    await expect(chatPage.attachmentsPreview).not.toBeVisible();
  });

  test('should handle file upload errors gracefully', async ({ page }) => {
    await chatPage.goto();

    // Mock failed file upload
    await page.route('/api/files/upload', async route => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Upload failed' }),
      });
    });

    // Try to add attachment
    await chatPage.addImageAttachment();

    // Check that error is handled (attachment preview should not appear)
    await expect(chatPage.attachmentsPreview).not.toBeVisible();

    // Send button should still be disabled if no text
    await expect(chatPage.sendButton).toBeDisabled();
  });

  test('should support different file types', async ({ page }) => {
    await chatPage.goto();

    // Mock upload for different file types
    await page.route('/api/files/upload', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          url: 'https://example.com/document.pdf',
          pathname: 'document.pdf',
          contentType: 'application/pdf',
        }),
      });
    });

    // Add PDF attachment
    await page.setInputFiles('input[type="file"]', {
      name: 'document.pdf',
      mimeType: 'application/pdf',
      buffer: Buffer.from('fake-pdf-content'),
    });

    // Check that attachment is accepted
    await expect(chatPage.attachmentsPreview).toBeVisible();

    const previewText = await chatPage.attachmentsPreview.textContent();
    expect(previewText).toContain('document.pdf');
  });

  test('should maintain input text when adding attachments', async ({ page }) => {
    await chatPage.goto();

    // Type message first
    const testMessage = 'This is a test message with attachment';
    await chatPage.inputField.fill(testMessage);

    // Mock file upload
    await page.route('/api/files/upload', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          url: 'https://example.com/test.jpg',
          pathname: 'test.jpg',
          contentType: 'image/jpeg',
        }),
      });
    });

    // Add attachment
    await chatPage.addImageAttachment();

    // Check that text is still there
    await expect(chatPage.inputField).toHaveValue(testMessage);

    // Check that attachment is also there
    await expect(chatPage.attachmentsPreview).toBeVisible();
  });

  test('should disable send button while uploading files', async ({ page }) => {
    await chatPage.goto();

    // Mock slow file upload
    await page.route('/api/files/upload', async route => {
      // Delay upload
      await new Promise(resolve => setTimeout(resolve, 2000));
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          url: 'https://example.com/test.jpg',
          pathname: 'test.jpg',
          contentType: 'image/jpeg',
        }),
      });
    });

    // Start file upload
    await chatPage.addImageAttachment();

    // Send button should be disabled during upload
    await expect(chatPage.sendButton).toBeDisabled();

    // Wait for upload to complete
    await page.waitForTimeout(2500);

    // Send button should be enabled (since we have attachment)
    await expect(chatPage.sendButton).not.toBeDisabled();
  });

  test('should handle large file uploads', async ({ page }) => {
    await chatPage.goto();

    // Mock large file upload
    await page.route('/api/files/upload', async route => {
      await route.fulfill({
        status: 413,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'File too large' }),
      });
    });

    // Try to upload large file
    await page.setInputFiles('input[type="file"]', {
      name: 'large-file.jpg',
      mimeType: 'image/jpeg',
      buffer: Buffer.alloc(10 * 1024 * 1024), // 10MB file
    });

    // Check that error is handled gracefully
    await expect(chatPage.attachmentsPreview).not.toBeVisible();

    // Should be able to continue with text input
    await chatPage.inputField.fill('Test message');
    await expect(chatPage.sendButton).not.toBeDisabled();
  });

  test('should support drag and drop file upload', async ({ page }) => {
    await chatPage.goto();

    // Mock file upload
    await page.route('/api/files/upload', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          url: 'https://example.com/dropped-file.jpg',
          pathname: 'dropped-file.jpg',
          contentType: 'image/jpeg',
        }),
      });
    });

    // Simulate drag and drop
    const inputElement = page.locator('input[type="file"]');
    await inputElement.dispatchEvent('drop', {
      dataTransfer: {
        files: [
          new File(['dropped content'], 'dropped-file.jpg', {
            type: 'image/jpeg',
          }),
        ],
      },
    });

    // Check that file is uploaded
    await expect(chatPage.attachmentsPreview).toBeVisible();

    const previewText = await chatPage.attachmentsPreview.textContent();
    expect(previewText).toContain('dropped-file.jpg');
  });

  test('should show upload progress for large files', async ({ page }) => {
    await chatPage.goto();

    // Mock file upload with progress indication
    await page.route('/api/files/upload', async route => {
      // Simulate upload progress
      await page.waitForTimeout(1000);
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          url: 'https://example.com/progress-test.jpg',
          pathname: 'progress-test.jpg',
          contentType: 'image/jpeg',
        }),
      });
    });

    // Upload file
    await chatPage.addImageAttachment();

    // Check that loading indicator appears
    const loadingIndicator = page.locator('[data-testid="input-attachment-loader"]');
    await expect(loadingIndicator).toBeVisible();

    // Wait for upload to complete
    await page.waitForTimeout(1500);

    // Loading indicator should disappear
    await expect(loadingIndicator).not.toBeVisible();

    // Attachment should be visible
    await expect(chatPage.attachmentsPreview).toBeVisible();
  });
});
