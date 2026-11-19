import React, { useState, useEffect } from "react";
import { fetchServerLogs } from "../services/api";
import { X, RefreshCw, Terminal, Search, Copy, Check } from "lucide-react";

interface LogsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const LogsModal: React.FC<LogsModalProps> = ({ isOpen, onClose }) => {
  const [logs, setLogs] = useState<string>("Loading backend logs...");
  const [filter, setFilter] = useState("");
  const [lines, setLines] = useState(150);
  const [isLoading, setIsLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const loadLogs = async () => {
    setIsLoading(true);
    const data = await fetchServerLogs(lines);
    setLogs(data);
    setIsLoading(false);
  };

  useEffect(() => {
    if (isOpen) {
      loadLogs();
    }
  }, [isOpen, lines]);

  if (!isOpen) return null;

  const filteredLogs = logs
    .split("\n")
    .filter((line) => line.toLowerCase().includes(filter.toLowerCase()))
    .join("\n");

  const handleCopy = () => {
    navigator.clipboard.writeText(logs);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-md animate-in fade-in duration-200">
      <div className="relative w-full max-w-4xl rounded-2xl border border-white/10 bg-zinc-950 shadow-2xl overflow-hidden flex flex-col max-h-[85vh]">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-white/10 px-5 py-3.5 bg-zinc-900/50">
          <div className="flex items-center gap-2.5">
            <div className="p-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
              <Terminal className="h-4 w-4" />
            </div>
            <div>
              <h2 className="text-sm font-semibold text-zinc-100 flex items-center gap-2">
                FastAPI Server Logs
                <span className="text-[10px] font-mono rounded bg-zinc-800 px-1.5 py-0.5 text-zinc-400">
                  GET /logs
                </span>
              </h2>
              <p className="text-[11px] text-zinc-500">
                Live tail from <code className="text-zinc-400">logs/app.log</code>
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="p-1.5 rounded-lg border border-white/10 bg-zinc-900 text-zinc-400 hover:text-zinc-200 text-xs flex items-center gap-1 transition-all"
              title="Copy All Logs"
            >
              {copied ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
            </button>
            <button
              onClick={loadLogs}
              disabled={isLoading}
              className="p-1.5 rounded-lg border border-white/10 bg-zinc-900 text-zinc-400 hover:text-zinc-200 text-xs flex items-center gap-1 transition-all"
              title="Refresh Logs"
            >
              <RefreshCw className={`h-3.5 w-3.5 ${isLoading ? "animate-spin text-emerald-400" : ""}`} />
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg border border-white/10 bg-zinc-900 text-zinc-400 hover:text-zinc-200 transition-all"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* Filter bar */}
        <div className="flex items-center justify-between border-b border-white/5 px-4 py-2 bg-zinc-900/20 gap-3 text-xs">
          <div className="relative flex-1 max-w-sm">
            <Search className="absolute left-2.5 top-2 h-3.5 w-3.5 text-zinc-500" />
            <input
              type="text"
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              placeholder="Search log messages..."
              className="w-full rounded-lg bg-zinc-900/80 border border-white/10 pl-8 pr-3 py-1 text-xs text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-emerald-500/50"
            />
          </div>

          <div className="flex items-center gap-2 text-zinc-400 text-xs">
            <span>Lines:</span>
            <select
              value={lines}
              onChange={(e) => setLines(Number(e.target.value))}
              className="rounded-lg bg-zinc-900 border border-white/10 px-2 py-1 text-xs text-zinc-300 focus:outline-none"
            >
              <option value={50}>50</option>
              <option value={100}>100</option>
              <option value={200}>200</option>
              <option value={500}>500</option>
            </select>
          </div>
        </div>

        {/* Log Viewer Content */}
        <div className="flex-1 overflow-auto p-4 bg-zinc-950 font-mono text-xs text-zinc-300 leading-relaxed selection:bg-emerald-500/20">
          <pre className="whitespace-pre-wrap">
            {filteredLogs || "[No matching log lines]"}
          </pre>
        </div>
      </div>
    </div>
  );
};

