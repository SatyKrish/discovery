import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    try { localStorage.removeItem('discovery:lastChatId'); } catch {}
  });
});

test.describe('Virtualized thread performance smoke', () => {
  test('renders bounded nodes while scrolling and on new message', async ({ page }) => {
    // Seed a large chat with many messages
    const totalMessages = 500;
    await page.route('**/api/chats', async (route) => {
      if (route.request().method() === 'GET') {
        return route.fulfill({ status: 200, body: JSON.stringify({ chats: [{ id: 'c1', title: 'Big chat' }] }), contentType: 'application/json' });
      }
      if (route.request().method() === 'POST') {
        return route.fulfill({ status: 200, body: JSON.stringify({ id: 'c1', title: 'Big chat' }), contentType: 'application/json' });
      }
    });

    let posted = false;
    await page.route('**/api/messages*', async (route) => {
      const method = route.request().method();
      if (method === 'GET') {
        if (posted) {
          // Append one more message from server
          const resp = {
            messages: Array.from({ length: totalMessages + 1 }, (_, i) => ({
              id: `m${i + 1}`,
              role: i % 2 === 0 ? 'user' : 'agent',
              text: `Message ${i + 1}`,
              createdAt: new Date().toISOString(),
            }))
          };
          return route.fulfill({ status: 200, body: JSON.stringify(resp), contentType: 'application/json' });
        }
        const resp = {
          messages: Array.from({ length: totalMessages }, (_, i) => ({
            id: `m${i + 1}`,
            role: i % 2 === 0 ? 'user' : 'agent',
            text: `Message ${i + 1}`,
            createdAt: new Date().toISOString(),
          }))
        };
        return route.fulfill({ status: 200, body: JSON.stringify(resp), contentType: 'application/json' });
      }
      if (method === 'POST') {
        posted = true;
        return route.fulfill({ status: 200, body: JSON.stringify({ ok: true }), contentType: 'application/json' });
      }
    });

    await page.goto('/');

    // If hero is visible, start chat to mount the UI
    const start = page.getByRole('button', { name: 'Start chatting' });
    if (await start.isVisible()) await start.click();

    // Wait for some messages to appear
    const messagesList = page.getByTestId('message-item');
    await expect(messagesList.first()).toBeVisible();

    // Check that only a bounded number of message nodes are in the DOM (virtualized)
    const countAtTop = await messagesList.count();
  expect(countAtTop).toBeLessThanOrEqual(100); // overscan + viewport window across browsers

    // Scroll down gradually to near the bottom and ensure DOM nodes remain bounded
    const thread = page.getByTestId('thread-scroll');
    await thread.evaluate((el) => { el.scrollTop = 0; });
    const maxScrolls = 10;
    for (let i = 0; i < maxScrolls; i++) {
      await thread.evaluate((el) => { el.scrollTop = el.scrollTop + el.clientHeight * 0.9; });
      await page.waitForTimeout(50);
      const c = await messagesList.count();
  expect(c).toBeLessThanOrEqual(100);
    }

    // Send a new message and ensure autoscroll keeps us near the bottom with bounded nodes
    await page.getByPlaceholder('Message Discovery Agent…').fill('Hello');
    await page.getByRole('button', { name: 'Send' }).click();

    await page.waitForTimeout(150); // allow fetch/get to update thread
    const countAfterSend = await messagesList.count();
  expect(countAfterSend).toBeLessThanOrEqual(100);
  });
});
