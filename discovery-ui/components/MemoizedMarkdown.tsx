import { memo, useMemo } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const MemoizedMarkdownBlock = memo(
  ({ content }: { content: string }) => {
    const components = {
      table: ({ node, ...props }: any) => (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 my-4" {...props} />
        </div>
      ),
      thead: ({ node, ...props }: any) => (
        <thead className="bg-gray-50" {...props} />
      ),
      th: ({ node, ...props }: any) => (
        <th
          className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border border-gray-200"
          {...props}
        />
      ),
      td: ({ node, ...props }: any) => (
        <td
          className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 border border-gray-200"
          {...props}
        />
      ),
      tr: ({ node, ...props }: any) => (
        <tr className="odd:bg-white even:bg-gray-50" {...props} />
      ),
    };

    return <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>{content}</ReactMarkdown>;
  },
  (prevProps, nextProps) => {
    if (prevProps.content !== nextProps.content) return false;
    return true;
  },
);

MemoizedMarkdownBlock.displayName = 'MemoizedMarkdownBlock';

export const MemoizedMarkdown = memo(({ content, id }: { content: string; id: string }) => {
  return <MemoizedMarkdownBlock content={content} key={id} />;
});

MemoizedMarkdown.displayName = 'MemoizedMarkdown';
