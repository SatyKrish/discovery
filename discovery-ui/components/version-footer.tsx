'use client';

import { memo } from 'react';
import type { Document } from '@/lib/db/schema';

function PureVersionFooter({
  currentVersionIndex,
  documents,
  handleVersionChange,
}: {
  currentVersionIndex: number;
  documents: Document[] | undefined;
  handleVersionChange: (type: 'next' | 'prev' | 'toggle' | 'latest') => void;
}) {
  if (!documents || documents.length <= 1) return null;

  return (
    <div className="flex items-center justify-between p-2 border-t">
      <button
        onClick={() => handleVersionChange('prev')}
        disabled={currentVersionIndex === 0}
        className="px-3 py-1 text-sm border rounded disabled:opacity-50"
      >
        Previous
      </button>
      <span className="text-sm text-gray-500">
        Version {currentVersionIndex + 1} of {documents.length}
      </span>
      <button
        onClick={() => handleVersionChange('next')}
        disabled={currentVersionIndex === documents.length - 1}
        className="px-3 py-1 text-sm border rounded disabled:opacity-50"
      >
        Next
      </button>
    </div>
  );
}

export const VersionFooter = memo(PureVersionFooter);
