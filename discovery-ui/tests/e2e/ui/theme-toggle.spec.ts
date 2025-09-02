import { test, expect } from '@playwright/test';
import { ChatPage } from '../utils/page-objects';

test.describe('Theme Toggle Functionality', () => {
  let chatPage: ChatPage;

  test.beforeEach(async ({ page }) => {
    chatPage = new ChatPage(page);
    await chatPage.setupTestEnvironment();
  });

  test('should toggle between light and dark themes', async ({ page }) => {
    await chatPage.goto();

    // Check initial theme (should be system by default)
    const html = page.locator('html');
    const initialClass = await html.getAttribute('class');

    // Click theme toggle
    await chatPage.toggleTheme();

    // Check that theme has changed
    const newClass = await html.getAttribute('class');
    expect(newClass).not.toBe(initialClass);

    // Click again to toggle back
    await chatPage.toggleTheme();

    // Should return to original theme
    const finalClass = await html.getAttribute('class');
    expect(finalClass).toBe(initialClass);
  });

  test('should persist theme preference in localStorage', async ({ page }) => {
    await chatPage.goto();

    // Click theme toggle
    await chatPage.toggleTheme();

    // Check localStorage
    const themePreference = await page.evaluate(() => {
      return localStorage.getItem('theme');
    });

    expect(themePreference).toBeDefined();
    expect(['light', 'dark', 'system']).toContain(themePreference);
  });

  test('should apply theme to all UI elements', async ({ page }) => {
    await chatPage.goto();

    // Get initial background color
    const body = page.locator('body');
    const initialBackground = await body.evaluate(el => {
      return window.getComputedStyle(el).backgroundColor;
    });

    // Toggle theme
    await chatPage.toggleTheme();

    // Wait for theme change
    await page.waitForTimeout(100);

    // Get new background color
    const newBackground = await body.evaluate(el => {
      return window.getComputedStyle(el).backgroundColor;
    });

    // Background should be different
    expect(newBackground).not.toBe(initialBackground);
  });

  test('should maintain theme across page reloads', async ({ page }) => {
    await chatPage.goto();

    // Toggle to dark theme
    await chatPage.toggleTheme();

    // Get current theme class
    const html = page.locator('html');
    const themeClass = await html.getAttribute('class');

    // Reload page
    await page.reload();

    // Check that theme is maintained
    const reloadedThemeClass = await html.getAttribute('class');
    expect(reloadedThemeClass).toBe(themeClass);
  });

  test('should show correct theme icon based on current theme', async ({ page }) => {
    await chatPage.goto();

    // Check initial icon (should be monitor for system theme)
    const themeButton = chatPage.themeToggle;
    const initialIcon = await themeButton.locator('svg').first();

    // Toggle theme
    await chatPage.toggleTheme();

    // Icon should change
    const newIcon = await themeButton.locator('svg').first();

    // The icon elements should be different
    const initialIconType = await initialIcon.getAttribute('data-testid') ||
                           await initialIcon.locator('path').first().getAttribute('d');
    const newIconType = await newIcon.getAttribute('data-testid') ||
                       await newIcon.locator('path').first().getAttribute('d');

    expect(newIconType).not.toBe(initialIconType);
  });
});
