import { describe, it, expect } from 'vitest';
import { normalizeUploadItem } from '@/lib/provider';

describe('normalizeUploadItem', () => {
  it('handles array item with common fields', () => {
    const input = { id: '1', name: 'a.txt', url: 'https://x/a.txt', mimetype: 'text/plain', size: 10 };
    const out = normalizeUploadItem(input)!;
    expect(out).toEqual({ id: '1', title: 'a.txt', uri: 'https://x/a.txt', mime: 'text/plain', size: 10 });
  });

  it('falls back across alternative keys', () => {
    const input: Record<string, unknown> = { uuid: 'u1', filename: 'file.pdf', path: '/f.pdf' };
    const out = normalizeUploadItem(input)!;
    expect(out.id).toBeDefined();
    expect(out.title).toBe('file.pdf');
    expect(out.uri).toBe('/f.pdf');
  });

  it('returns null when no uri exists', () => {
    expect(normalizeUploadItem({ id: 'x', name: 'b' })).toBeNull();
  });
});
