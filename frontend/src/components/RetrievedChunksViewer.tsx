import React, { useState } from "react";
import { RetrievedChunk, SourceItem } from "../services/api";
import {
  FileText,
  Table as TableIcon,
  Image as ImageIcon,
  CheckCircle2,
  Layers,
  Code2,
  ExternalLink,
  Sparkles,
} from "lucide-react";
import { cn } from "../lib/utils";

interface RetrievedChunksViewerProps {
  chunks: RetrievedChunk[];
  rawContext: string[];
  sources: SourceItem[];
  highlightedSourceId?: string | null;
  onClose?: () => void;
}

export const RetrievedChunksViewer: React.FC<RetrievedChunksViewerProps> = ({
  chunks,
  rawContext,
  sources,
  highlightedSourceId,
}) => {
  const [activeTab, setActiveTab] = useState<"chunks" | "raw" | "stats">("chunks");
  const [filterType, setFilterType] = useState<"all" | "text" | "table" | "image">("all");

  const filteredChunks = chunks.filter((c) => {
    if (filterType === "all") return true;
    return (c.chunk_type || "text") === filterType;
  });

  return (
    <div className="rounded-2xl border border-white/10 bg-zinc-950/90 shadow-2xl overflow-hidden backdrop-blur-2xl">
      {/* Top Header & Tab Navigation */}
      <div className="flex flex-wrap items-center justify-between border-b border-white/10 px-4 py-3 bg-zinc-900/40 gap-3">
        <div className="flex items-center gap-2">
          <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
            <Layers className="h-4 w-4" />
          </div>
          <div>
            <h3 className="text-xs sm:text-sm font-semibold text-zinc-100 flex items-center gap-1.5">
              Retrieved Intelligence & Context Inspector
              <span className="rounded-full bg-emerald-500/20 px-2 py-0.5 text-[10px] text-emerald-300 font-mono">
                {chunks.length} chunks
              </span>
            </h3>
            <p className="text-[11px] text-zinc-400">
              Inspecting dense vectors, BM25 matches, RRF fusion, and Cross-Encoder reranking
            </p>
          </div>
        </div>

        {/* Tab switchers */}
        <div className="flex items-center rounded-xl bg-zinc-900 border border-white/10 p-1 text-xs">
          <button
            onClick={() => setActiveTab("chunks")}
            className={cn(
              "px-3 py-1 rounded-lg transition-all flex items-center gap-1.5 font-medium",
              activeTab === "chunks"
                ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 shadow-sm"
                : "text-zinc-400 hover:text-zinc-200"
            )}
          >
            <Layers className="h-3.5 w-3.5" />
            Chunks ({chunks.length})
          </button>
          <button
            onClick={() => setActiveTab("raw")}
            className={cn(
              "px-3 py-1 rounded-lg transition-all flex items-center gap-1.5 font-medium",
              activeTab === "raw"
                ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 shadow-sm"
                : "text-zinc-400 hover:text-zinc-200"
            )}
          >
            <Code2 className="h-3.5 w-3.5" />
            Raw LLM Context
          </button>
        </div>
      </div>

      {/* Filter by chunk type */}
      {activeTab === "chunks" && (
        <div className="flex items-center justify-between border-b border-white/5 px-4 py-2 bg-zinc-900/20 text-xs">
          <span className="text-zinc-500">Filter modality:</span>
          <div className="flex items-center gap-1.5">
            {(["all", "text", "table", "image"] as const).map((type) => (
              <button
                key={type}
                onClick={() => setFilterType(type)}
                className={cn(
                  "px-2.5 py-0.5 rounded-md text-[11px] uppercase tracking-wider font-semibold transition-all",
                  filterType === type
                    ? "bg-white/10 text-zinc-100 border border-white/20"
                    : "text-zinc-500 hover:text-zinc-300"
                )}
              >
                {type}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Main Content Area */}
      <div className="max-h-[460px] overflow-y-auto p-4 space-y-3">
        {activeTab === "chunks" && (
          <>
            {filteredChunks.length === 0 ? (
              <div className="py-8 text-center text-xs text-zinc-500">
                No chunks matching filter "{filterType}"
              </div>
            ) : (
              filteredChunks.map((chunk, idx) => {
                const chunkType = chunk.chunk_type || "text";
                const isSelected = highlightedSourceId && chunk.text.includes(highlightedSourceId);

                return (
                  <div
                    key={chunk.id || idx}
                    className={cn(
                      "rounded-xl border p-3.5 transition-all text-xs space-y-2.5",
                      isSelected
                        ? "border-emerald-500/60 bg-emerald-950/20 shadow-lg shadow-emerald-500/5"
                        : "border-white/10 bg-zinc-900/40 hover:border-white/20 hover:bg-zinc-900/60"
                    )}
                  >
                    {/* Header: Type, Page, Scores */}
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <div className="flex items-center gap-2">
                        {/* Type Badge */}
                        <span
                          className={cn(
                            "inline-flex items-center gap-1 px-2 py-0.5 rounded-full font-mono text-[10px] font-semibold border",
                            chunkType === "table"
                              ? "bg-amber-500/10 text-amber-300 border-amber-500/30"
                              : chunkType === "image"
                              ? "bg-purple-500/10 text-purple-300 border-purple-500/30"
                              : "bg-cyan-500/10 text-cyan-300 border-cyan-500/30"
                          )}
                        >
                          {chunkType === "table" && <TableIcon className="h-3 w-3" />}
                          {chunkType === "image" && <ImageIcon className="h-3 w-3" />}
                          {chunkType === "text" && <FileText className="h-3 w-3" />}
                          {chunkType.toUpperCase()}
                        </span>

                        <span className="text-zinc-300 font-medium">
                          {chunk.source || "Document"}
                        </span>
                        {chunk.page && (
                          <span className="text-zinc-500 font-mono">Page {chunk.page}</span>
                        )}
                      </div>

                      {/* Score metrics */}
                      <div className="flex items-center gap-2 font-mono text-[11px]">
                        {chunk.rerank_score && (
                          <span
                            className="text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-1.5 py-0.5 rounded"
                            title="Cross-Encoder Rerank Score"
                          >
                            Rerank: {chunk.rerank_score.toFixed(3)}
                          </span>
                        )}
                        {chunk.dense_score && (
                          <span
                            className="text-cyan-400 bg-cyan-500/10 border border-cyan-500/20 px-1.5 py-0.5 rounded"
                            title="Pinecone Cosine Similarity"
                          >
                            Dense: {chunk.dense_score.toFixed(3)}
                          </span>
                        )}
                        {chunk.bm25_score && (
                          <span
                            className="text-zinc-400 bg-zinc-800 border border-white/10 px-1.5 py-0.5 rounded"
                            title="BM25 Lexical Score"
                          >
                            BM25: {chunk.bm25_score.toFixed(1)}
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Table Special Preview */}
                    {chunkType === "table" && chunk.table_markdown && (
                      <div className="rounded-lg border border-amber-500/20 bg-amber-950/10 p-2.5">
                        <div className="text-[10px] uppercase font-mono text-amber-400 font-semibold mb-1 flex items-center gap-1">
                          <TableIcon className="h-3 w-3" /> Structured Table Representation
                        </div>
                        <pre className="font-mono text-[11px] text-zinc-300 whitespace-pre-wrap overflow-x-auto">
                          {chunk.table_markdown}
                        </pre>
                      </div>
                    )}

                    {/* Image Special Preview */}
                    {chunkType === "image" && chunk.image_url && (
                      <div className="rounded-lg border border-purple-500/20 bg-purple-950/10 p-2.5">
                        <div className="text-[10px] uppercase font-mono text-purple-400 font-semibold mb-2 flex items-center gap-1">
                          <ImageIcon className="h-3 w-3" /> Extracted Visual Diagram
                        </div>
                        <div className="relative rounded-lg overflow-hidden border border-white/10 bg-black/40 max-h-48 flex items-center justify-center">
                          <img
                            src={chunk.image_url}
                            alt="Extracted Figure"
                            className="object-contain max-h-48 w-full rounded"
                          />
                        </div>
                      </div>
                    )}

                    {/* Text Snippet */}
                    <p className="text-zinc-300 leading-relaxed font-sans text-xs">
                      {chunk.text}
                    </p>
                  </div>
                );
              })
            )}
          </>
        )}

        {/* Tab 2: Raw Context Passed to LLM */}
        {activeTab === "raw" && (
          <div className="space-y-3">
            <div className="rounded-xl border border-white/10 bg-zinc-900/60 p-3 text-xs text-zinc-400">
              The exact unified string injected into Gemini prompt under{" "}
              <code className="text-emerald-300">{"{context}"}</code>:
            </div>
            {rawContext.map((item, idx) => (
              <div
                key={idx}
                className="rounded-xl border border-white/5 bg-zinc-900/40 p-3 font-mono text-xs text-zinc-300 whitespace-pre-wrap leading-relaxed"
              >
                <div className="text-[10px] text-emerald-400 font-bold mb-1">
                  Context Block #{idx + 1}:
                </div>
                {item}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

