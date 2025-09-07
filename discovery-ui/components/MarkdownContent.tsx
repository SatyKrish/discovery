"use client";

import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

interface MarkdownContentProps {
  content: string;
  className?: string;
}

export const MarkdownContent = React.memo<MarkdownContentProps>(
  ({ content, className = "" }) => {
    return (
      <div className={`prose prose-sm max-w-none text-sm leading-relaxed ${className}`}>
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            code({ node, inline, className, children, ...props }: any) {
              const match = /language-(\w+)/.exec(className || "");
              return !inline && match ? (
                <SyntaxHighlighter
                  style={oneDark as any}
                  language={match[1]}
                  PreTag="div"
                  className="rounded-md text-xs overflow-x-auto"
                >
                  {String(children).replace(/\n$/, "")}
                </SyntaxHighlighter>
              ) : (
                <code className="bg-muted px-1.5 py-0.5 rounded text-xs font-mono" {...props}>
                  {children}
                </code>
              );
            },
            pre({ children }: any) {
              return <div className="my-4">{children}</div>;
            },
            a({ href, children }: any) {
              return (
                <a
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-primary hover:underline"
                >
                  {children}
                </a>
              );
            },
            blockquote({ children }: any) {
              return (
                <blockquote className="border-l-4 border-border pl-4 italic text-muted-foreground my-4">
                  {children}
                </blockquote>
              );
            },
            ul({ children }: any) {
              return <ul className="list-disc list-inside my-2 space-y-1">{children}</ul>;
            },
            ol({ children }: any) {
              return <ol className="list-decimal list-inside my-2 space-y-1">{children}</ol>;
            },
            table({ children }: any) {
              return (
                <div className="overflow-x-auto my-4">
                  <table className="min-w-full border border-border rounded-md">{children}</table>
                </div>
              );
            },
            th({ children }: any) {
              return (
                <th className="border border-border px-4 py-2 bg-muted font-semibold text-left">
                  {children}
                </th>
              );
            },
            td({ children }: any) {
              return (
                <td className="border border-border px-4 py-2">
                  {children}
                </td>
              );
            },
          }}
        >
          {content}
        </ReactMarkdown>
      </div>
    );
  },
);

MarkdownContent.displayName = "MarkdownContent";
