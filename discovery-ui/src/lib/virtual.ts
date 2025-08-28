export type SimpleVirtualItem = {
  index: number;
  key: string;
  start: number;
  size: number;
  end: number;
  lane: number;
  measureElement: (el: Element | null) => void;
};

// Returns a simple fallback window of the last `keep` items when real virtualization isn't available
export function getFallbackVirtualItems(total: number, keep = 20): SimpleVirtualItem[] {
  if (total <= 0) return [];
  const startIndex = Math.max(0, total - keep);
  const result: SimpleVirtualItem[] = [];
  for (let i = startIndex; i < total; i++) {
    result.push({
      index: i,
      key: `fallback-${i}`,
      start: 0,
      size: 0,
      end: 0,
      lane: 0,
      measureElement: () => {},
    });
  }
  return result;
}
