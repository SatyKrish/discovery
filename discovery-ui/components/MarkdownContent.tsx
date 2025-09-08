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
      <div className={`prose prose-sm max-w-none text-sm leading-relaxed prose-headings:text-foreground prose-p:text-foreground prose-strong:text-foreground prose-code:text-foreground prose-pre:bg-muted prose-blockquote:text-muted-foreground prose-blockquote:border-border dark:prose-invert ${className}`}>
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
                  className="rounded-md text-xs overflow-x-auto !bg-muted"
                >
                  {String(children).replace(/\n$/, "")}
                </SyntaxHighlighter>
              ) : (
                <code className="bg-muted px-1.5 py-0.5 rounded text-xs font-mono text-foreground" {...props}>
                  {children}
                </code>
              );
            },
            pre({ children }: any) {
              return <div className="my-4 bg-muted rounded-md p-4 overflow-x-auto">{children}</div>;
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
                <blockquote className="border-l-4 border-border pl-4 italic text-muted-foreground my-4 bg-muted/50 py-2 px-4 rounded-r-md">
                  {children}
                </blockquote>
              );
            },
            ul({ children }: any) {
              return <ul className="list-disc list-inside my-2 space-y-1 text-foreground">{children}</ul>;
            },
            ol({ children }: any) {
              return <ol className="list-decimal list-inside my-2 space-y-1 text-foreground">{children}</ol>;
            },
            table({ children }: any) {
              return (
                <div className="overflow-x-auto my-4">
                  <table className="min-w-full border border-border rounded-md bg-card">{children}</table>
                </div>
              );
            },
            th({ children }: any) {
              return (
                <th className="border border-border px-4 py-2 bg-muted font-semibold text-left text-foreground">
                  {children}
                </th>
              );
            },
            td({ children }: any) {
              return (
                <td className="border border-border px-4 py-2 text-foreground">
                  {children}
                </td>
              );
            },
            h1({ children }: any) {
              return <h1 className="text-2xl font-bold text-foreground mb-4 mt-6 first:mt-0">{children}</h1>;
            },
            h2({ children }: any) {
              return <h2 className="text-xl font-bold text-foreground mb-3 mt-5">{children}</h2>;
            },
            h3({ children }: any) {
              return <h3 className="text-lg font-semibold text-foreground mb-2 mt-4">{children}</h3>;
            },
            p({ children }: any) {
              return <p className="text-foreground mb-4 last:mb-0 leading-relaxed">{children}</p>;
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
