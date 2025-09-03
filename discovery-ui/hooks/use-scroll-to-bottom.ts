'use client';

import { useCallback, useEffect, useRef, useState } from 'react';

export function useScrollToBottom(externalRef?: React.RefObject<HTMLDivElement>) {
  const internalRef = useRef<HTMLDivElement>(null);
  const scrollRef = externalRef || internalRef;
  const [isAtBottom, setIsAtBottom] = useState(true);

  const scrollToBottom = useCallback(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [scrollRef]);

  useEffect(() => {
    const handleScroll = () => {
      if (scrollRef.current) {
        const { scrollTop, scrollHeight, clientHeight } = scrollRef.current;
        const atBottom = scrollTop + clientHeight >= scrollHeight - 10;
        setIsAtBottom(atBottom);
      }
    };

    const element = scrollRef.current;
    if (element) {
      element.addEventListener('scroll', handleScroll);
      // Initial check
      handleScroll();
      return () => element.removeEventListener('scroll', handleScroll);
    }
  }, [scrollRef]);

  return {
    scrollRef,
    scrollToBottom,
    isAtBottom,
  };
}
