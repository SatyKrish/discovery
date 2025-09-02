'use client';

import { useState } from 'react';
import type { ArtifactKind, UIArtifact } from '@/components/artifact';

export const initialArtifactData: UIArtifact = {
  title: '',
  documentId: 'init',
  kind: 'text' as ArtifactKind,
  content: '',
  isVisible: false,
  status: 'idle',
  boundingBox: {
    top: 0,
    left: 0,
    width: 0,
    height: 0,
  },
};

export function useArtifact() {
  const [artifact, setArtifact] = useState<UIArtifact>(initialArtifactData);
  const [metadata, setMetadata] = useState<any>({});

  return {
    artifact,
    setArtifact,
    metadata,
    setMetadata,
  };
}

export function useArtifactSelector(selector: (state: UIArtifact) => any) {
  const { artifact } = useArtifact();
  return selector(artifact);
}
