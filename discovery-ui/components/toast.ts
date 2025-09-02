export function toast({ type, description }: { type: string; description: string }) {
  console.log(`${type}: ${description}`);
}
