"use client";
import Link from "next/link";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export default function LibraryPage() {
  return (
    <main className="min-h-dvh p-6">
      <div className="mx-auto max-w-5xl">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-semibold">Library</h1>
          <Link href="/" className={cn(buttonVariants({ variant: "outline" }))}>Back to chat</Link>
        </div>
        <div className="rounded-xl border bg-background p-6 text-sm text-muted-foreground">
          This is a placeholder for your Library. Next steps:
          <ul className="list-disc ml-4 mt-2 space-y-1">
            <li>Render pinned artifacts and recent outputs.</li>
            <li>Add filters (type, chat, date) and a grid/list toggle.</li>
          </ul>
        </div>
      </div>
    </main>
  );
}
