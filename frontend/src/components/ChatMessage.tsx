import React from "react";
import { RAGResponse } from "../services/api";
import { MarkdownView } from "./MarkdownView";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { Sparkles, Layers, FileText } from "lucide-react";
import { cn } from "../lib/utils";

export interface MessageItem {
  id: string;
  sender: "user" | "assistant";
  text: string;
  timestamp: string;
  ragData?: RAGResponse;
}

interface ChatMessageProps {
  message: MessageItem;
  onInspect: (data: RAGResponse, sourceId?: string) => void;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message, onInspect }) => {
  const isUser = message.sender === "user";

  return (
    <div className={cn("py-4 sm:py-5 flex gap-3 sm:gap-4", isUser && "justify-end")}>
      {/* Bot Icon */}
      {!isUser && (
        <div className="flex-shrink-0 pt-0.5">
          <div className="flex h-7 w-7 items-center justify-center rounded-md border border-zinc-800 bg-zinc-900 text-zinc-300">
            <Sparkles className="h-3.5 w-3.5 text-zinc-400" />
          </div>
        </div>
      )}

      {/* Message Content */}
      <div className={cn("space-y-2.5 max-w-3xl", isUser ? "max-w-2xl text-right" : "flex-1")}>
        {isUser ? (
          <div className="inline-block rounded-2xl bg-zinc-800/90 text-zinc-100 px-4 py-2.5 text-[14px] leading-relaxed text-left border border-zinc-700/50 shadow-sm">
            {message.text}
          </div>
        ) : (
          <div className="space-y-3">
            <MarkdownView
              content={message.text}
              sources={message.ragData?.sources}
              onCitationClick={(id) => message.ragData && onInspect(message.ragData, id)}
            />

            {/* Quiet Sources Strip (Production-grade, zero clutter) */}
            {message.ragData?.sources && message.ragData.sources.length > 0 && (
              <div className="pt-2 flex flex-wrap items-center gap-1.5 text-xs">
                <span className="text-zinc-500 text-[11px] font-medium mr-1">Sources:</span>
                {message.ragData.sources.map((s) => (
                  <button
                    key={s.id}
                    onClick={() => message.ragData && onInspect(message.ragData, s.id)}
                    className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded border border-zinc-800 bg-zinc-900/60 hover:bg-zinc-800 hover:border-zinc-700 text-zinc-400 hover:text-zinc-200 transition-colors text-[11px] cursor-pointer"
                  >
                    <FileText className="h-3 w-3 text-zinc-500" />
                    <span>{s.source}</span>
                    {s.page && <span className="text-zinc-500">· p.{s.page}</span>}
                  </button>
                ))}

                {/* Inspect button */}
                {message.ragData.retrieved_chunks && message.ragData.retrieved_chunks.length > 0 && (
                  <Button
                    variant="ghost"
                    size="xs"
                    onClick={() => message.ragData && onInspect(message.ragData)}
                    className="text-zinc-400 hover:text-zinc-200 ml-1 gap-1 text-[11px]"
                  >
                    <Layers className="h-3 w-3" />
                    <span>Inspect ({message.ragData.retrieved_chunks.length})</span>
                  </Button>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
