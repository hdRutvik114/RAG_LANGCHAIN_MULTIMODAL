import React from "react";
import { X, Sliders, Database, Eye, Sparkles } from "lucide-react";

interface SettingsDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  topK: number;
  setTopK: (val: number) => void;
  candidateK: number;
  setCandidateK: (val: number) => void;
  documentId: string;
  setDocumentId: (val: string) => void;
}

export const SettingsDrawer: React.FC<SettingsDrawerProps> = ({
  isOpen,
  onClose,
  topK,
  setTopK,
  candidateK,
  setCandidateK,
  documentId,
  setDocumentId,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="w-full max-w-md h-full bg-zinc-950 border-l border-white/10 shadow-2xl p-6 flex flex-col justify-between overflow-y-auto">
        <div className="space-y-6">
          {/* Header */}
          <div className="flex items-center justify-between pb-4 border-b border-white/10">
            <div className="flex items-center gap-2.5">
              <div className="p-2 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
                <Sliders className="h-5 w-5" />
              </div>
              <div>
                <h2 className="text-base font-semibold text-zinc-100">
                  RAG Pipeline Tuner
                </h2>
                <p className="text-xs text-zinc-400">
                  Retrieval, reranking & filtering hyperparameters
                </p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg border border-white/10 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-900 transition-all"
            >
              <X className="h-4 w-4" />
            </button>
          </div>

          {/* Top-K Setting */}
          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs font-medium">
              <span className="text-zinc-300">Final Top-K Chunks to LLM</span>
              <span className="font-mono text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded">
                {topK}
              </span>
            </div>
            <input
              type="range"
              min={1}
              max={15}
              value={topK}
              onChange={(e) => setTopK(Number(e.target.value))}
              className="w-full accent-emerald-500 cursor-pointer"
            />
            <p className="text-[11px] text-zinc-500">
              The number of reranked passages injected into Gemini's context window.
            </p>
          </div>

          {/* Candidate-K Setting */}
          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs font-medium">
              <span className="text-zinc-300">Candidate-K for RRF & Reranker</span>
              <span className="font-mono text-cyan-400 bg-cyan-500/10 border border-cyan-500/20 px-2 py-0.5 rounded">
                {candidateK}
              </span>
            </div>
            <input
              type="range"
              min={topK}
              max={50}
              value={candidateK}
              onChange={(e) => setCandidateK(Number(e.target.value))}
              className="w-full accent-cyan-500 cursor-pointer"
            />
            <p className="text-[11px] text-zinc-500">
              Passages retrieved by dense and sparse engines before Reciprocal Rank Fusion.
            </p>
          </div>

          {/* Document ID Filter */}
          <div className="space-y-2">
            <label className="block text-xs font-medium text-zinc-300">
              Target Document Filter (Optional)
            </label>
            <input
              type="text"
              value={documentId}
              onChange={(e) => setDocumentId(e.target.value)}
              placeholder="e.g. 91372821b401012093d6ef43a2bc6f87..."
              className="w-full rounded-xl bg-zinc-900 border border-white/10 px-3.5 py-2 text-xs font-mono text-zinc-200 placeholder-zinc-600 focus:outline-none focus:border-emerald-500/50"
            />
            <div className="flex gap-2 pt-1">
              <button
                type="button"
                onClick={() => setDocumentId("91372821b401012093d6ef43a2bc6f87a1073fbcd4c2e64fb00217b3e1a0f052")}
                className="text-[10px] text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-1 rounded-md hover:bg-emerald-500/20 transition-all font-mono"
              >
                + attention.pdf ID
              </button>
              {documentId && (
                <button
                  type="button"
                  onClick={() => setDocumentId("")}
                  className="text-[10px] text-zinc-400 bg-zinc-900 border border-white/10 px-2 py-1 rounded-md hover:text-zinc-200"
                >
                  Clear Filter
                </button>
              )}
            </div>
          </div>

          {/* Pipeline Details Card */}
          <div className="rounded-xl border border-white/10 bg-zinc-900/40 p-4 space-y-2.5 text-xs">
            <div className="text-zinc-200 font-semibold flex items-center gap-1.5">
              <Database className="h-4 w-4 text-emerald-400" /> Pipeline Architecture
            </div>
            <ul className="space-y-1 text-zinc-400 text-[11px] list-disc list-inside">
              <li>Vector Store: <strong className="text-zinc-300">Pinecone (384-dim)</strong></li>
              <li>Keyword Engine: <strong className="text-zinc-300">BM25Okapi</strong></li>
              <li>Fusion: <strong className="text-zinc-300">RRF (k=60)</strong></li>
              <li>Reranker: <strong className="text-zinc-300">ms-marco-MiniLM-L-6-v2</strong></li>
              <li>Synthesis: <strong className="text-zinc-300">Google Gemini</strong></li>
            </ul>
          </div>
        </div>

        {/* Footer */}
        <div className="pt-4 border-t border-white/10">
          <button
            onClick={onClose}
            className="w-full py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 text-zinc-950 font-semibold text-xs hover:opacity-95 transition-all shadow-lg shadow-emerald-500/10 cursor-pointer"
          >
            Apply & Close
          </button>
        </div>
      </div>
    </div>
  );
};

