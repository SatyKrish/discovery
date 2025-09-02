'use client';

import { useCallback, useEffect, useRef } from 'react';

export function useScrollToBottom() {
  const scrollRef = useRef<HTMLDivElement>(null);
  const isAtBottom = useRef(true);

  const scrollToBottom = useCallback(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, []);

  useEffect(() => {
    const handleScroll = () => {
      if (scrollRef.current) {
        const { scrollTop, scrollHeight, clientHeight } = scrollRef.current;
        isAtBottom.current = scrollTop + clientHeight >= scrollHeight - 10;
      }
    };

    const element = scrollRef.current;
    if (element) {
      element.addEventListener('scroll', handleScroll);
      return () => element.removeEventListener('scroll', handleScroll);
    }
  }, []);

  return {
    scrollRef,
    scrollToBottom,
    isAtBottom: isAtBottom.current,
  };
}
