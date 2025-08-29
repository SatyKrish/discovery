import { test, expect } from '@playwright/test';

// Clear persisted chat selection to keep tests isolated
test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    try { localStorage.removeItem('discovery:lastChatId'); } catch {}
  });
});

test.describe('Composer keyboard shortcuts', () => {
  test('Shift+Enter creates newline without sending', async ({ page }) => {
    await page.route('**/api/chats', async (route) => {
      if (route.request().method() === 'GET') {
        return route.fulfill({ status: 200, body: JSON.stringify({ chats: [{ id: 'c1', title: 'Demo chat' }] }), contentType: 'application/json' });
      }
      if (route.request().method() === 'POST') {
        return route.fulfill({ status: 200, body: JSON.stringify({ id: 'c2', title: 'New chat' }), contentType: 'application/json' });
      }
    });
    await page.route('**/api/messages*', async (route) => {
      const method = route.request().method();
      if (method === 'GET') {
        return route.fulfill({ status: 200, body: JSON.stringify({ messages: [] }), contentType: 'application/json' });
      }
      if (method === 'POST') {
        return route.fulfill({ status: 200, body: JSON.stringify({ ok: true }), contentType: 'application/json' });
      }
    });

    await page.goto('/');
    const start = page.getByRole('button', { name: 'Start chatting' });
    if (await start.isVisible()) await start.click();

    const composer = page.getByPlaceholder('Message Discovery Agent…');
    await composer.click();
    await composer.type('Hello');
    await composer.press('Shift+Enter');
    await composer.type('World');
    await expect(composer).toHaveValue('Hello\nWorld');
    await expect(page.getByTestId('message-item')).toHaveCount(0);
  });

  test('Ctrl+Enter sends message', async ({ page }) => {
    await page.route('**/api/chats', async (route) => {
      if (route.request().method() === 'GET') {
        return route.fulfill({ status: 200, body: JSON.stringify({ chats: [{ id: 'c1', title: 'Demo chat' }] }), contentType: 'application/json' });
      }
      if (route.request().method() === 'POST') {
        return route.fulfill({ status: 200, body: JSON.stringify({ id: 'c2', title: 'New chat' }), contentType: 'application/json' });
      }
    });
    let posted = false;
    await page.route('**/api/messages*', async (route) => {
      const method = route.request().method();
      if (method === 'GET') {
        if (posted) {
          const resp = { messages: [{ id: 'm1', role: 'user', text: 'Hello', createdAt: new Date().toISOString() }] };
          return route.fulfill({ status: 200, body: JSON.stringify(resp), contentType: 'application/json' });
        }
        return route.fulfill({ status: 200, body: JSON.stringify({ messages: [] }), contentType: 'application/json' });
      }
      if (method === 'POST') {
        posted = true;
        return route.fulfill({ status: 200, body: JSON.stringify({ ok: true }), contentType: 'application/json' });
      }
    });

    await page.goto('/');
    const start = page.getByRole('button', { name: 'Start chatting' });
    if (await start.isVisible()) await start.click();
    const composer = page.getByPlaceholder('Message Discovery Agent…');
    await composer.fill('Hello');
    await composer.press('Control+Enter');
    await expect(page.getByTestId('message-item')).toHaveCount(1);
  });

  test('Meta+Enter sends message', async ({ page }) => {
    await page.route('**/api/chats', async (route) => {
      if (route.request().method() === 'GET') {
        return route.fulfill({ status: 200, body: JSON.stringify({ chats: [{ id: 'c1', title: 'Demo chat' }] }), contentType: 'application/json' });
      }
      if (route.request().method() === 'POST') {
        return route.fulfill({ status: 200, body: JSON.stringify({ id: 'c2', title: 'New chat' }), contentType: 'application/json' });
      }
    });
    let posted = false;
    await page.route('**/api/messages*', async (route) => {
      const method = route.request().method();
      if (method === 'GET') {
        if (posted) {
          const resp = { messages: [{ id: 'm1', role: 'user', text: 'Hello', createdAt: new Date().toISOString() }] };
          return route.fulfill({ status: 200, body: JSON.stringify(resp), contentType: 'application/json' });
        }
        return route.fulfill({ status: 200, body: JSON.stringify({ messages: [] }), contentType: 'application/json' });
      }
      if (method === 'POST') {
        posted = true;
        return route.fulfill({ status: 200, body: JSON.stringify({ ok: true }), contentType: 'application/json' });
      }
    });

    await page.goto('/');
    const start = page.getByRole('button', { name: 'Start chatting' });
    if (await start.isVisible()) await start.click();
    const composer = page.getByPlaceholder('Message Discovery Agent…');
    await composer.fill('Hello');
    await composer.press('Meta+Enter');
    await expect(page.getByTestId('message-item')).toHaveCount(1);
  });
});
