'use client';

import { useState } from 'react';
import type { VisibilityType } from '@/components/visibility-selector';

export function useChatVisibility({
  chatId,
  initialVisibilityType,
}: {
  chatId: string;
  initialVisibilityType: VisibilityType;
}) {
  const [visibilityType, setVisibilityType] = useState<VisibilityType>(initialVisibilityType);

  return {
    visibilityType,
    setVisibilityType,
  };
}
