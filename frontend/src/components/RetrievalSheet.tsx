import React, { useState } from "react";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
} from "./ui/sheet";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "./ui/tabs";
import { Badge } from "./ui/badge";
import { RetrievedChunk, SourceItem } from "../services/api";
import { FileText, Table as TableIcon, Image as ImageIcon, Database } from "lucide-react";
import { cn } from "../lib/utils";

interface RetrievalSheetProps {
  isOpen: boolean;
  onClose: () => void;
  chunks: RetrievedChunk[];
  rawContext: string[];
  sources: SourceItem[];
  highlightedSourceId?: string | null;
}

export const RetrievalSheet: React.FC<RetrievalSheetProps> = ({
  isOpen,
  onClose,
  chunks,
  rawContext,
  sources,
  highlightedSourceId,
}) => {
  const [activeTab, setActiveTab] = useState("chunks");

  return (
    <Sheet open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <SheetContent className="overflow-hidden flex flex-col p-0 sm:max-w-xl bg-zinc-950 border-zinc-800">
        <SheetHeader className="p-5 pb-3 border-b border-zinc-800/80">
          <div className="flex items-center gap-2">
            <Database className="h-4 w-4 text-zinc-400" />
            <SheetTitle>Retrieval & Grounding Context</SheetTitle>
          </div>
          <SheetDescription>
            {chunks.length} passages retrieved via Hybrid RRF & Cross-Encoder reranking
          </SheetDescription>

          <Tabs value={activeTab} onValueChange={setActiveTab} className="pt-2">
            <TabsList className="w-full grid grid-cols-2">
              <TabsTrigger value="chunks">Retrieved Chunks ({chunks.length})</TabsTrigger>
              <TabsTrigger value="context">LLM Prompt Context</TabsTrigger>
            </TabsList>
          </Tabs>
        </SheetHeader>

        {/* Scrollable Body */}
        <div className="flex-1 overflow-y-auto p-5 space-y-3.5">
          {activeTab === "chunks" && (
            <div className="space-y-3">
              {chunks.length === 0 ? (
                <div className="py-12 text-center text-xs text-zinc-500">
                  No retrieval context recorded for this turn.
                </div>
              ) : (
                chunks.map((chunk, idx) => {
                  const chunkType = chunk.chunk_type || "text";
                  const isHighlighted =
                    highlightedSourceId && chunk.text.includes(highlightedSourceId);

                  return (
                    <div
                      key={chunk.id || idx}
                      className={cn(
                        "rounded-lg border p-3.5 text-xs transition-colors space-y-2.5",
                        isHighlighted
                          ? "border-zinc-500 bg-zinc-900/80"
                          : "border-zinc-800/80 bg-zinc-900/30 hover:border-zinc-700/80"
                      )}
                    >
                      {/* Top meta row */}
                      <div className="flex items-center justify-between text-[11px]">
                        <div className="flex items-center gap-2">
                          <Badge
                            variant={
                              chunkType === "table"
                                ? "outline"
                                : chunkType === "image"
                                ? "secondary"
                                : "neutral"
                            }
                            className="font-mono text-[10px] uppercase gap-1"
                          >
                            {chunkType === "table" && <TableIcon className="h-2.5 w-2.5" />}
                            {chunkType === "image" && <ImageIcon className="h-2.5 w-2.5" />}
                            {chunkType === "text" && <FileText className="h-2.5 w-2.5" />}
                            {chunkType}
                          </Badge>
                          <span className="font-medium text-zinc-300">
                            {chunk.source}
                          </span>
                          {chunk.page && (
                            <span className="text-zinc-500">p. {chunk.page}</span>
                          )}
                        </div>

                        {/* Scores */}
                        <div className="flex items-center gap-1.5 font-mono text-[10px] text-zinc-400">
                          {chunk.rerank_score && (
                            <span className="text-zinc-300">
                              score: {chunk.rerank_score.toFixed(3)}
                            </span>
                          )}
                        </div>
                      </div>

                      {/* Special Table View */}
                      {chunkType === "table" && chunk.table_markdown && (
                        <div className="rounded border border-zinc-800 bg-zinc-950 p-2 font-mono text-[10px] text-zinc-300 overflow-x-auto whitespace-pre-wrap">
                          {chunk.table_markdown}
                        </div>
                      )}

                      {/* Special Image View */}
                      {chunkType === "image" && chunk.image_url && (
                        <div className="rounded border border-zinc-800 bg-zinc-950 p-2">
                          <img
                            src={chunk.image_url}
                            alt="Extracted Figure"
                            className="max-h-44 w-auto mx-auto rounded object-contain"
                          />
                        </div>
                      )}

                      {/* Content snippet */}
                      <p className="text-zinc-400 leading-relaxed text-xs">
                        {chunk.text}
                      </p>
                    </div>
                  );
                })
              )}
            </div>
          )}

          {activeTab === "context" && (
            <div className="space-y-2.5">
              <p className="text-[11px] text-zinc-500">
                Exact string injected into the Google Gemini prompt context:
              </p>
              {rawContext.map((c, i) => (
                <div
                  key={i}
                  className="rounded-lg border border-zinc-800/80 bg-zinc-900/40 p-3 font-mono text-xs text-zinc-300 leading-relaxed whitespace-pre-wrap"
                >
                  <span className="text-zinc-500 text-[10px] block mb-1">
                    Passage #{i + 1}
                  </span>
                  {c}
                </div>
              ))}
            </div>
          )}
        </div>
      </SheetContent>
    </Sheet>
  );
};

