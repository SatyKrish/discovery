import { type FullConfig } from '@playwright/test';
import fs from 'fs';
import path from 'path';

async function globalTeardown(config: FullConfig) {
  // Clean up test artifacts
  const cleanupDirs = [
    'playwright/.auth',
    'playwright/.sessions',
  ];

  cleanupDirs.forEach(dir => {
    const fullPath = path.join(process.cwd(), dir);
    if (fs.existsSync(fullPath)) {
      try {
        fs.rmSync(fullPath, { recursive: true, force: true });
        console.log(`🧹 Cleaned up ${dir}`);
      } catch (error) {
        console.warn(`Failed to clean up ${dir}:`, error);
      }
    }
  });

  console.log('✅ Global test teardown completed');
}

export default globalTeardown;
