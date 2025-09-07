'use client';

import useSWR from 'swr';
export type ArtifactKind = 'text' | 'code' | 'image' | 'sheet';

export interface UIArtifact {
  title: string;
  documentId: string;
  kind: ArtifactKind;
  content: string;
  isVisible: boolean;
  status: 'idle' | 'streaming' | 'complete';
  boundingBox: {
    top: number;
    left: number;
    width: number;
    height: number;
  };
}
import { useCallback, useMemo } from 'react';

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
  const { data: localArtifact, mutate: setLocalArtifact } = useSWR<UIArtifact>(
    'artifact',
    null,
    {
      fallbackData: initialArtifactData,
    },
  );

  const artifact = useMemo(() => {
    if (!localArtifact) return initialArtifactData;
    return localArtifact;
  }, [localArtifact]);

  const setArtifact = useCallback(
    (updaterFn: UIArtifact | ((currentArtifact: UIArtifact) => UIArtifact)) => {
      setLocalArtifact((currentArtifact) => {
        const artifactToUpdate = currentArtifact || initialArtifactData;

        if (typeof updaterFn === 'function') {
          return updaterFn(artifactToUpdate);
        }

        return updaterFn;
      });
    },
    [setLocalArtifact],
  );

  const { data: localArtifactMetadata, mutate: setLocalArtifactMetadata } =
    useSWR<any>(
      () =>
        artifact.documentId ? `artifact-metadata-${artifact.documentId}` : null,
      null,
      {
        fallbackData: null,
      },
    );

  return useMemo(
    () => ({
      artifact,
      setArtifact,
      metadata: localArtifactMetadata,
      setMetadata: setLocalArtifactMetadata,
    }),
    [artifact, setArtifact, localArtifactMetadata, setLocalArtifactMetadata],
  );
}

export function useArtifactSelector(selector: (state: UIArtifact) => any) {
  const { artifact } = useArtifact();
  return selector(artifact);
}
