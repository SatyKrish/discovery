import { test, expect } from '@playwright/test';

async function stubBasicChat(page: any) {
  await page.route('**/api/chats', async (route: any) => {
    if (route.request().method() === 'GET') {
      return route.fulfill({ status: 200, body: JSON.stringify({ chats: [{ id: 'c1', title: 'Demo chat' }] }), contentType: 'application/json' });
    }
    return route.continue();
  });
  await page.route('**/api/messages*', async (route: any) => {
    if (route.request().method() === 'GET') {
      return route.fulfill({ status: 200, body: JSON.stringify({ messages: [] }), contentType: 'application/json' });
    }
    return route.continue();
  });
}

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    try { localStorage.removeItem('discovery:lastChatId'); } catch {}
  });
  await stubBasicChat(page);
});

test.describe('responsive layout', () => {
  test('phone uses sheets for side panels', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto('/');

    const start = page.getByRole('button', { name: 'Start chatting' });
    if (await start.isVisible()) await start.click();

    await expect(page.getByText('Chats', { exact: true })).toHaveCount(0);

    await page.getByLabel('Open sidebar').click();
    await expect(page.getByText('Chats', { exact: true })).toBeVisible();
    await page.keyboard.press('Escape');

    await page.getByRole('button', { name: 'Artifacts' }).click();
    await expect(page.getByText('No artifacts yet')).toBeVisible();
    await page.keyboard.press('Escape');
  });

  test('tablet collapses columns', async ({ page }) => {
    await page.setViewportSize({ width: 800, height: 1000 });
    await page.goto('/');

    const start = page.getByRole('button', { name: 'Start chatting' });
    if (await start.isVisible()) await start.click();

    await expect(page.getByText('Chats', { exact: true })).toHaveCount(0);

    await page.getByRole('button', { name: 'Artifacts' }).click();
    await expect(page.getByText('No artifacts yet')).toBeVisible();
    await page.keyboard.press('Escape');
  });

  test('desktop shows inline panels', async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto('/');

    const start = page.getByRole('button', { name: 'Start chatting' });
    if (await start.isVisible()) await start.click();

    await expect(page.getByText('Chats', { exact: true })).toBeVisible();

    await page.getByRole('button', { name: 'Artifacts' }).click();
    await expect(page.getByText('No artifacts yet')).toBeVisible();
  });
});

