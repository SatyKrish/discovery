import { Page, expect } from '@playwright/test';
import { generateUUID } from '@/lib/utils';

export class TestHelpers {
  constructor(private page: Page) {}

  /**
   * Generate a unique chat ID for testing
   */
  static generateChatId(): string {
    return `chat-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Wait for the page to be fully loaded
   */
  async waitForPageLoad() {
    await this.page.waitForLoadState('networkidle');
  }

  /**
   * Wait for chat generation to complete
   */
  async waitForGenerationComplete() {
    await this.page.waitForResponse((response) =>
      response.url().includes('/api/chat') && response.status() === 200
    );
  }

  /**
   * Get the current URL path
   */
  getCurrentPath(): string {
    return new URL(this.page.url()).pathname;
  }

  /**
   * Check if URL contains chat ID
   */
  hasChatIdInUrl(): boolean {
    const path = this.getCurrentPath();
    return /^\/chat\/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/.test(path);
  }

  /**
   * Extract chat ID from URL
   */
  getChatIdFromUrl(): string | null {
    const path = this.getCurrentPath();
    const match = path.match(/^\/chat\/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$/);
    return match ? match[1] : null;
  }

  /**
   * Mock API responses for testing
   */
  async mockChatAPI(response: any) {
    await this.page.route('/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: `data: ${JSON.stringify(response)}\n\ndata: [DONE]`,
      });
    });
  }

  /**
   * Mock file upload API
   */
  async mockFileUploadAPI() {
    await this.page.route('/api/files/upload', async route => {
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
  }

  /**
   * Take a screenshot for debugging
   */
  async takeScreenshot(name: string) {
    await this.page.screenshot({ path: `test-results/${name}.png` });
  }

  /**
   * Wait for element to be visible with timeout
   */
  async waitForElement(selector: string, timeout = 5000) {
    await this.page.waitForSelector(selector, { timeout, state: 'visible' });
  }

  /**
   * Check if element exists
   */
  async elementExists(selector: string): Promise<boolean> {
    try {
      await this.page.waitForSelector(selector, { timeout: 1000 });
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Get element text content
   */
  async getElementText(selector: string): Promise<string> {
    return await this.page.locator(selector).textContent() || '';
  }

  /**
   * Click element and wait for navigation
   */
  async clickAndWaitForNavigation(selector: string) {
    await Promise.all([
      this.page.waitForLoadState('networkidle'),
      this.page.click(selector),
    ]);
  }

  /**
   * Fill input and wait for value
   */
  async fillInput(selector: string, value: string) {
    await this.page.fill(selector, value);
    await expect(this.page.locator(selector)).toHaveValue(value);
  }

  /**
   * Wait for URL to match pattern
   */
  async waitForUrl(pattern: RegExp | string) {
    await this.page.waitForURL(pattern);
  }

  /**
   * Mock console errors for cleaner test output
   */
  async suppressConsoleErrors() {
    await this.page.addScriptTag({
      content: `
        console.error = () => {};
        console.warn = () => {};
      `,
    });
  }

  /**
   * Clear local storage (disabled due to security restrictions)
   */
  async clearLocalStorage() {
    // Disabled due to security restrictions in test environment
    // localStorage access is blocked in Playwright tests
    console.log('Skipping localStorage clear due to security restrictions');
  }

  /**
   * Set up test environment
   */
  async setupTestEnvironment() {
    await this.clearLocalStorage();
    await this.suppressConsoleErrors();
    await this.page.setViewportSize({ width: 1280, height: 720 });
  }
}
