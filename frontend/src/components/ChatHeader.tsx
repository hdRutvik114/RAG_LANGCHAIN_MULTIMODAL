import React from "react";
import { HealthStatus } from "../services/api";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { Sliders, Terminal, Plus, Sparkles, RefreshCw } from "lucide-react";
import { cn } from "../lib/utils";

interface ChatHeaderProps {
  health: HealthStatus;
  onOpenLogs: () => void;
  onOpenSettings: () => void;
  onResetChat: () => void;
  onCheckHealth: () => void;
}

export const ChatHeader: React.FC<ChatHeaderProps> = ({
  health,
  onOpenLogs,
  onOpenSettings,
  onResetChat,
  onCheckHealth,
}) => {
  return (
    <header className="sticky top-0 z-30 h-13 border-b border-zinc-800/80 bg-zinc-950/80 backdrop-blur-md px-4 sm:px-6 flex items-center justify-between">
      {/* Brand */}
      <div className="flex items-center gap-2.5">
        <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-zinc-900 border border-zinc-800 text-zinc-100">
          <Sparkles className="h-3.5 w-3.5" />
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs sm:text-sm font-semibold tracking-tight text-zinc-100">
            Multimodal RAG
          </span>
          <Badge variant="neutral" className="text-[10px] font-mono hidden sm:inline-flex">
            API v1.0
          </Badge>
        </div>
      </div>

      {/* Controls */}
      <div className="flex items-center gap-2">
        {/* Backend health status badge */}
        <button
          onClick={onCheckHealth}
          className="flex items-center gap-1.5 px-2 py-1 rounded-md text-[11px] font-mono text-zinc-400 hover:text-zinc-200 transition-colors border border-transparent hover:border-zinc-800"
          title="Click to ping backend health"
        >
          <span
            className={cn(
              "h-1.5 w-1.5 rounded-full",
              health.status === "healthy"
                ? "bg-emerald-400"
                : health.status === "checking"
                ? "bg-amber-400 animate-pulse"
                : "bg-red-400"
            )}
          />
          <span className="hidden sm:inline">
            {health.status === "healthy"
              ? `Backend ${health.latencyMs}ms`
              : health.status === "checking"
              ? "Checking..."
              : "Backend Offline"}
          </span>
        </button>

        <div className="h-4 w-[1px] bg-zinc-800 mx-1 hidden sm:block" />

        {/* Logs */}
        <Button
          variant="ghost"
          size="sm"
          onClick={onOpenLogs}
          className="text-zinc-400 hover:text-zinc-200 gap-1.5 h-7 px-2"
          title="View FastAPI server logs"
        >
          <Terminal className="h-3.5 w-3.5" />
          <span className="hidden sm:inline">Logs</span>
        </Button>

        {/* Settings */}
        <Button
          variant="ghost"
          size="sm"
          onClick={onOpenSettings}
          className="text-zinc-400 hover:text-zinc-200 gap-1.5 h-7 px-2"
          title="Configure retrieval parameters"
        >
          <Sliders className="h-3.5 w-3.5" />
          <span className="hidden sm:inline">Parameters</span>
        </Button>

        {/* New Chat */}
        <Button
          variant="outline"
          size="sm"
          onClick={onResetChat}
          className="h-7 px-2.5 text-zinc-300 gap-1"
          title="Start fresh conversation"
        >
          <Plus className="h-3.5 w-3.5" />
          <span className="hidden sm:inline">New Chat</span>
        </Button>
      </div>
    </header>
  );
};
