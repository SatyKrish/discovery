import { Page, Locator, expect } from '@playwright/test';
import { TestHelpers } from './test-helpers';

export class ChatPage {
  private helpers: TestHelpers;

  constructor(public page: Page) {
    this.helpers = new TestHelpers(page);
  }

  // Main elements
  get inputField(): Locator {
    return this.page.getByTestId('multimodal-input');
  }

  get sendButton(): Locator {
    return this.page.locator('button[type="submit"]').first();
  }

  get stopButton(): Locator {
    return this.page.locator('button').filter({ hasText: /stop/i }).first();
  }

  get suggestedActions(): Locator {
    return this.page.locator('.grid.grid-cols-2.gap-4').first();
  }

  get attachmentsPreview(): Locator {
    return this.page.getByTestId('attachments-preview');
  }

  get scrollToBottomButton(): Locator {
    return this.page.getByTestId('scroll-to-bottom-button');
  }

  // Header elements
  get themeToggle(): Locator {
    return this.page.getByTestId('theme-toggle');
  }

  get sidebarToggle(): Locator {
    return this.page.getByTestId('sidebar-toggle-button');
  }

  // Message elements
  get userMessages(): Locator {
    return this.page.getByTestId('message-user');
  }

  get assistantMessages(): Locator {
    return this.page.getByTestId('message-assistant');
  }

  get lastUserMessage(): Locator {
    return this.userMessages.last();
  }

  get lastAssistantMessage(): Locator {
    return this.assistantMessages.last();
  }

  // Actions
  async goto() {
    await this.page.goto('/');
    await this.helpers.waitForPageLoad();
  }

  async sendMessage(message: string) {
    await this.inputField.click();
    await this.inputField.fill(message);
    await this.sendButton.click();
  }

  async sendMessageFromSuggestion(index = 0) {
    const suggestions = this.page.locator('.grid.grid-cols-2.gap-4 button');
    await suggestions.nth(index).click();
  }

  async waitForGenerationComplete() {
    await this.helpers.waitForGenerationComplete();
  }

  async waitForUrlToContainChatId() {
    await this.helpers.waitForUrl(/^\/chat\/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/);
  }

  async hasChatIdInUrl(): Promise<boolean> {
    return this.helpers.hasChatIdInUrl();
  }

  async getChatIdFromUrl(): Promise<string | null> {
    return this.helpers.getChatIdFromUrl();
  }

  async getLastUserMessageContent(): Promise<string> {
    return await this.lastUserMessage.textContent() || '';
  }

  async getLastAssistantMessageContent(): Promise<string> {
    return await this.lastAssistantMessage.textContent() || '';
  }

  async toggleTheme() {
    await this.themeToggle.click();
  }

  async toggleSidebar() {
    await this.sidebarToggle.click();
  }

  async scrollToBottom() {
    await this.scrollToBottomButton.click();
  }

  async isScrolledToBottom(): Promise<boolean> {
    return await this.page.evaluate(() => {
      const scrollContainer = document.querySelector('.overflow-y-scroll');
      if (!scrollContainer) return false;
      const { scrollHeight, scrollTop, clientHeight } = scrollContainer as HTMLElement;
      return Math.abs(scrollHeight - scrollTop - clientHeight) < 1;
    });
  }

  async addImageAttachment() {
    // Mock file input for testing
    await this.page.setInputFiles('input[type="file"]', {
      name: 'test-image.jpg',
      mimeType: 'image/jpeg',
      buffer: Buffer.from('fake-image-content'),
    });
  }

  async setupTestEnvironment() {
    await this.helpers.setupTestEnvironment();
  }
}

export class SidebarPage {
  constructor(public page: Page) {}

  // Sidebar elements
  get sidebar(): Locator {
    return this.page.locator('[data-sidebar="sidebar"]');
  }

  get newChatButton(): Locator {
    return this.page.getByRole('button', { name: 'New Chat' });
  }

  get searchInput(): Locator {
    return this.page.getByPlaceholder('Search chats...');
  }

  get chatItems(): Locator {
    return this.page.locator('[data-sidebar="menu-item"]');
  }

  get filterButton(): Locator {
    return this.page.getByRole('button', { name: 'Filters' });
  }

  // Actions
  async createNewChat() {
    await this.newChatButton.click();
  }

  async searchChats(query: string) {
    await this.searchInput.fill(query);
  }

  async clickChatItem(index = 0) {
    await this.chatItems.nth(index).click();
  }

  async getChatTitles(): Promise<string[]> {
    return await this.chatItems.allTextContents();
  }

  async openFilters() {
    await this.filterButton.click();
  }

  async filterByDate(dateFilter: 'all' | 'today' | 'week' | 'month') {
    await this.openFilters();
    await this.page.locator('select').first().selectOption(dateFilter);
  }

  async filterByVisibility(visibility: 'all' | 'private' | 'public') {
    await this.openFilters();
    await this.page.locator('select').last().selectOption(visibility);
  }
}

export class ArtifactPage {
  constructor(private page: Page) {}

  // Artifact elements
  get artifact(): Locator {
    return this.page.getByTestId('artifact');
  }

  get artifactCloseButton(): Locator {
    return this.page.getByTestId('artifact-close-button');
  }

  get artifactTitle(): Locator {
    return this.page.locator('[data-testid="artifact"] h1');
  }

  // Actions
  async isVisible(): Promise<boolean> {
    return await this.artifact.isVisible();
  }

  async close() {
    await this.artifactCloseButton.click();
  }

  async getTitle(): Promise<string> {
    return await this.artifactTitle.textContent() || '';
  }
}

export class MultimodalInputPage {
  constructor(private page: Page) {}

  // Input elements
  get input(): Locator {
    return this.page.getByTestId('multimodal-input');
  }

  get attachmentsButton(): Locator {
    return this.page.getByTestId('attachments-button');
  }

  get sendButton(): Locator {
    return this.page.locator('button[type="submit"]').first();
  }

  get stopButton(): Locator {
    return this.page.locator('button').filter({ hasText: /stop/i }).first();
  }

  // Actions
  async typeMessage(message: string) {
    await this.input.fill(message);
  }

  async sendMessage() {
    await this.sendButton.click();
  }

  async stopGeneration() {
    await this.stopButton.click();
  }

  async attachFile() {
    await this.attachmentsButton.click();
  }

  async isSendButtonDisabled(): Promise<boolean> {
    return await this.sendButton.isDisabled();
  }

  async isStopButtonVisible(): Promise<boolean> {
    return await this.stopButton.isVisible();
  }
}
