import React, { useState, useRef, useEffect } from "react";
import { ArrowUp, CornerDownLeft } from "lucide-react";
import { cn } from "../lib/utils";

interface ChatInputProps {
  onSend: (text: string) => void;
  isLoading: boolean;
  topK: number;
}

export const ChatInput: React.FC<ChatInputProps> = ({ onSend, isLoading, topK }) => {
  const [input, setInput] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || isLoading) return;
    onSend(input.trim());
    setInput("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(
        textareaRef.current.scrollHeight,
        160
      )}px`;
    }
  }, [input]);

  return (
    <div className="w-full max-w-3xl mx-auto">
      <form
        onSubmit={handleSubmit}
        className="relative rounded-xl border border-zinc-800 bg-zinc-900/80 shadow-lg backdrop-blur-md focus-within:border-zinc-700 transition-colors p-2.5 sm:p-3"
      >
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about documents, tables, or diagrams..."
          rows={1}
          disabled={isLoading}
          className="w-full resize-none bg-transparent px-2 py-1 text-sm text-zinc-100 placeholder-zinc-500 focus:outline-none max-h-40 disabled:opacity-50"
        />

        {/* Action strip */}
        <div className="flex items-center justify-between pt-1.5 px-1 text-[11px] text-zinc-500">
          <div className="flex items-center gap-2 font-mono text-[10px]">
            <span>Hybrid (Pinecone + BM25)</span>
            <span>·</span>
            <span>k={topK}</span>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className={cn(
                "flex h-7 w-7 items-center justify-center rounded-lg transition-all",
                input.trim() && !isLoading
                  ? "bg-zinc-100 text-zinc-900 hover:bg-zinc-200 cursor-pointer shadow-sm"
                  : "bg-zinc-800 text-zinc-600 cursor-not-allowed"
              )}
            >
              {isLoading ? (
                <div className="h-3.5 w-3.5 border-2 border-zinc-900 border-t-transparent rounded-full animate-spin" />
              ) : (
                <ArrowUp className="h-3.5 w-3.5" />
              )}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};
