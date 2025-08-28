import { describe, it, expect } from 'vitest';
import { getFallbackVirtualItems } from '@/lib/virtual';

describe('getFallbackVirtualItems', () => {
  it('returns empty for 0 total', () => {
    expect(getFallbackVirtualItems(0)).toEqual([]);
  });

  it('returns last N indices when total > keep', () => {
    const items = getFallbackVirtualItems(100, 20);
    expect(items.length).toBe(20);
    expect(items[0].index).toBe(80);
    expect(items[19].index).toBe(99);
  });

  it('returns all when total <= keep', () => {
    const items = getFallbackVirtualItems(5, 20);
    expect(items.map(i => i.index)).toEqual([0,1,2,3,4]);
  });
});
