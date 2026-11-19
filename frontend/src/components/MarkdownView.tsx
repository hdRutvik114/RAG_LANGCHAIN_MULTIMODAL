import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Check, Copy } from "lucide-react";
import { SourceItem } from "../services/api";

interface MarkdownViewProps {
  content: string;
  sources?: SourceItem[];
  onCitationClick?: (sourceId: string) => void;
}

export const MarkdownView: React.FC<MarkdownViewProps> = ({
  content,
  sources = [],
  onCitationClick,
}) => {
  return (
    <div className="prose prose-invert max-w-none text-zinc-300 leading-relaxed text-[13.5px] sm:text-[14.5px]">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          table: ({ children }) => (
            <div className="my-3 overflow-x-auto rounded-lg border border-zinc-800 bg-zinc-900/40">
              <table className="w-full text-left border-collapse text-xs">
                {children}
              </table>
            </div>
          ),
          thead: ({ children }) => (
            <thead className="bg-zinc-900/90 border-b border-zinc-800 text-zinc-300 font-medium text-[11px] uppercase tracking-wider">
              {children}
            </thead>
          ),
          tbody: ({ children }) => (
            <tbody className="divide-y divide-zinc-800/60">{children}</tbody>
          ),
          tr: ({ children }) => (
            <tr className="hover:bg-zinc-800/30 transition-colors">{children}</tr>
          ),
          th: ({ children }) => <th className="px-3 py-2 font-medium">{children}</th>,
          td: ({ children }) => <td className="px-3 py-2 text-zinc-300 font-mono text-[11px]">{children}</td>,
          code: ({ className, children, ...props }) => {
            const isInline = !className && typeof children === "string" && !children.includes("\n");
            if (isInline) {
              return (
                <code
                  className="rounded bg-zinc-900 px-1.5 py-0.5 text-xs font-mono text-zinc-200 border border-zinc-800"
                  {...props}
                >
                  {children}
                </code>
              );
            }
            return <CodeBlock>{String(children).replace(/\n$/, "")}</CodeBlock>;
          },
          p: ({ children }) => {
            return (
              <p className="mb-2.5 last:mb-0 leading-relaxed text-zinc-300">
                {renderWithInteractiveCitations(children, sources, onCitationClick)}
              </p>
            );
          },
          ul: ({ children }) => <ul className="my-2 space-y-1 list-disc list-inside text-zinc-300">{children}</ul>,
          ol: ({ children }) => <ol className="my-2 space-y-1 list-decimal list-inside text-zinc-300">{children}</ol>,
          li: ({ children }) => <li className="leading-relaxed">{children}</li>,
          strong: ({ children }) => <strong className="font-semibold text-zinc-100">{children}</strong>,
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
};

function CodeBlock({ children }: { children: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(children);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="group relative my-2.5 rounded-lg border border-zinc-800 bg-zinc-950 p-3 font-mono text-xs text-zinc-300">
      <button
        onClick={handleCopy}
        className="absolute right-2.5 top-2.5 rounded border border-zinc-800 bg-zinc-900 p-1 text-zinc-400 opacity-0 transition-all hover:bg-zinc-800 hover:text-zinc-100 group-hover:opacity-100"
        title="Copy code"
      >
        {copied ? <Check className="h-3 w-3 text-emerald-400" /> : <Copy className="h-3 w-3" />}
      </button>
      <pre className="overflow-x-auto">
        <code>{children}</code>
      </pre>
    </div>
  );
}

function renderWithInteractiveCitations(
  children: React.ReactNode,
  sources: SourceItem[],
  onCitationClick?: (sourceId: string) => void
): React.ReactNode {
  if (typeof children !== "string") {
    if (Array.isArray(children)) {
      return children.map((child, idx) => (
        <React.Fragment key={idx}>
          {renderWithInteractiveCitations(child, sources, onCitationClick)}
        </React.Fragment>
      ));
    }
    return children;
  }

  const regex = /\[(S\d+)\]/g;
  const parts: React.ReactNode[] = [];
  let lastIndex = 0;
  let match;

  while ((match = regex.exec(children)) !== null) {
    const citationId = match[1];
    const sourceObj = sources.find((s) => s.id === citationId);

    if (match.index > lastIndex) {
      parts.push(children.slice(lastIndex, match.index));
    }

    parts.push(
      <button
        key={`${citationId}-${match.index}`}
        onClick={() => onCitationClick?.(citationId)}
        className="mx-0.5 inline-flex items-center px-1.5 py-0.2 rounded text-[11px] font-mono font-medium text-zinc-400 hover:text-zinc-100 bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 transition-colors cursor-pointer align-baseline"
        title={sourceObj ? `${sourceObj.source} (Page ${sourceObj.page ?? "N/A"})` : `Source ${citationId}`}
      >
        [{citationId}]
      </button>
    );

    lastIndex = regex.lastIndex;
  }

  if (lastIndex < children.length) {
    parts.push(children.slice(lastIndex));
  }

  return parts;
}
