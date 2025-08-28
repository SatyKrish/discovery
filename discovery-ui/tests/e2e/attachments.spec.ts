import { test, expect } from '@playwright/test';

// Clear persisted chat selection to keep tests isolated
test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    try { localStorage.removeItem('discovery:lastChatId'); } catch {}
  });
});

// E2E: attach -> send -> artifact visible
// Stubs backend APIs via Next API proxy endpoints

test.describe('Attachments flow', () => {
  test('attach files, send, and see file artifact', async ({ page }) => {
    // Stub uploads
    await page.route('**/api/uploads', async (route) => {
      const json = [
        { id: 'f1', name: 'report.csv', url: 'https://example.com/report.csv', mimetype: 'text/csv', size: 2048 },
      ];
      await route.fulfill({ status: 200, body: JSON.stringify(json), contentType: 'application/json' });
    });

    // Stub chats list and messages before sending
    await page.route('**/api/chats', async (route) => {
      if (route.request().method() === 'GET') {
        return route.fulfill({ status: 200, body: JSON.stringify({ chats: [{ id: 'c1', title: 'Demo chat' }] }) });
      }
      if (route.request().method() === 'POST') {
        return route.fulfill({ status: 200, body: JSON.stringify({ id: 'c2', title: 'New chat' }) });
      }
    });

    let posted = false;
    await page.route('**/api/messages*', async (route) => {
      const method = route.request().method();
      if (method === 'GET') {
        if (posted) {
          const resp = {
            messages: [{
              id: 'm1', role: 'user', text: 'Here is the file.', createdAt: new Date().toISOString(),
              artifacts: [{ id: 'f1', type: 'file', title: 'report.csv', uri: 'https://example.com/report.csv' }]
            }]
          };
          return route.fulfill({ status: 200, body: JSON.stringify(resp), contentType: 'application/json' });
        }
        return route.fulfill({ status: 200, body: JSON.stringify({ messages: [] }), contentType: 'application/json' });
      }
      if (method === 'POST') {
        const body = JSON.parse(route.request().postData() || '{}');
        expect(body.attachments?.[0]?.uri).toContain('https://example.com/');
        posted = true;
        return route.fulfill({ status: 200, body: JSON.stringify({ ok: true }), contentType: 'application/json' });
      }
    });

    await page.goto('/');

    // If hero is visible, click Start chatting to bring the chat UI
    const startButton = page.getByRole('button', { name: 'Start chatting' });
    if (await startButton.isVisible()) {
      await startButton.click();
    }

    // New chat is created on entry; focus composer
    const composer = page.getByPlaceholder('Message Discovery Agent…');
    await composer.click();

    // Attach a file
    const [fileChooser] = await Promise.all([
      page.waitForEvent('filechooser'),
      page.getByRole('button', { name: 'Attach file' }).click(),
    ]);
    await fileChooser.setFiles({ name: 'report.csv', mimeType: 'text/csv', buffer: Buffer.from('a,b\n1,2\n') });

    // Chips should show the selected file
    await expect(page.getByText('report.csv')).toBeVisible();

    // Type a message and send
    await composer.fill('Here is the file.');
    await page.getByRole('button', { name: 'Send' }).click();

  // The artifact panel should show a file card with Download
    await page.getByRole('button', { name: 'Artifacts' }).click();
  await expect(page.getByRole('link', { name: /Download/ }).first()).toBeVisible();
  });
});
