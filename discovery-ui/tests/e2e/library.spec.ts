import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    try { localStorage.removeItem('discovery:lastChatId'); } catch {}
  });
});

// E2E: Library — navigate → filter → unpin → reflects in chat
// Stubs backend via Next API proxies

test.describe('Library view', () => {
  test('pinned filter, unpin an artifact, and see it unpinned in chat', async ({ page }) => {
    const chatId = 'c1';
    const artifactId = 'a1';
    let pinned = true;

    // Stub artifacts list
    await page.route('**/api/artifacts**', async (route) => {
      if (route.request().method() !== 'GET') return route.continue();
      const url = new URL(route.request().url());
      const isPinned = url.searchParams.has('pinned');
      const type = url.searchParams.get('type');
      const list = [
        { id: artifactId, title: 'Quarterly Report', type: 'file', uri: 'https://example.com/q1.pdf', pinned, chatId },
      ].filter((a) => (isPinned ? a.pinned : true) && (!type || a.type === type));
      return route.fulfill({ status: 200, body: JSON.stringify({ artifacts: list }) });
    });

    // Stub toggle pin
    await page.route('**/api/artifacts/toggle-pin', async (route) => {
      const body = JSON.parse(route.request().postData() || '{}');
      expect(body.chatId).toBe(chatId);
      expect(body.artifactId).toBe(artifactId);
      pinned = !pinned;
      return route.fulfill({ status: 200, body: JSON.stringify({ ok: true }) });
    });

    // Stub chats and messages
    await page.route('**/api/chats', async (route) => {
      if (route.request().method() === 'GET') {
        return route.fulfill({ status: 200, body: JSON.stringify({ chats: [{ id: chatId, title: 'Demo chat' }] }) });
      }
      return route.continue();
    });

    await page.route('**/api/messages*', async (route) => {
      if (route.request().method() !== 'GET') return route.continue();
      const url = new URL(route.request().url());
      const cid = url.searchParams.get('chatId');
      if (cid !== chatId) return route.fulfill({ status: 200, body: JSON.stringify({ messages: [] }) });
      const resp = {
        messages: [
          {
            id: 'm1', role: 'agent', text: 'Here is your file.', createdAt: new Date().toISOString(),
            artifacts: [{ id: artifactId, type: 'file', title: 'Quarterly Report', uri: 'https://example.com/q1.pdf', pinned }],
          },
        ],
      };
      return route.fulfill({ status: 200, body: JSON.stringify(resp) });
    });

    // Go to Library
    await page.goto('/library');

    // Filters: default is Pinned; select type File to narrow (optional)
    await page.getByRole('button', { name: 'file' }).click();

    // See the artifact card
    await expect(page.getByText('Quarterly Report').first()).toBeVisible();
    await expect(page.getByRole('button', { name: 'Unpin' })).toBeVisible();

    // Unpin it
  await page.getByRole('button', { name: /^Unpin$/ }).click();
  // Optimistic toggle should flip to Pin (exact match)
  await expect(page.getByRole('button', { name: /^Pin$/ })).toBeVisible();

    // Open in chat
  await page.getByRole('button', { name: /^Open in chat$/ }).click();

    // Chat loads for the selected chat; open artifacts panel
    await page.getByRole('button', { name: 'Artifacts' }).click();

    // Ensure the card exists and is now unpinned (button shows Pin)
    await expect(page.getByText('Quarterly Report').first()).toBeVisible();
    // No Unpin button should be present for this card anymore
  await expect(page.getByRole('button', { name: /^Unpin$/ })).toHaveCount(0);
  });
});
