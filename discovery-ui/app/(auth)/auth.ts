export async function auth() {
  // Simple auth stub for now
  return {
    user: {
      id: 'guest',
      email: 'guest@example.com',
      name: 'Guest User',
    },
    expires: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(), // 24 hours from now
  };
}
