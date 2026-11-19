import React, { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "./ui/dialog";
import { Button } from "./ui/button";
import { fetchServerLogs } from "../services/api";
import { RefreshCw, Copy, Check } from "lucide-react";

interface LogsDialogProps {
  isOpen: boolean;
  onClose: () => void;
}

export const LogsDialog: React.FC<LogsDialogProps> = ({ isOpen, onClose }) => {
  const [logs, setLogs] = useState("Fetching server logs...");
  const [copied, setCopied] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const loadLogs = async () => {
    setIsLoading(true);
    const text = await fetchServerLogs(100);
    setLogs(text);
    setIsLoading(false);
  };

  useEffect(() => {
    if (isOpen) {
      loadLogs();
    }
  }, [isOpen]);

  const handleCopy = () => {
    navigator.clipboard.writeText(logs);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-3xl max-h-[85vh] flex flex-col p-6">
        <DialogHeader className="pb-3 border-b border-zinc-800">
          <div className="flex items-center justify-between pr-6">
            <div>
              <DialogTitle>Server Telemetry & Logs</DialogTitle>
              <DialogDescription>
                Live tail from <code className="text-zinc-300">logs/app.log</code> via <code className="text-zinc-300">GET /logs</code>
              </DialogDescription>
            </div>
            <div className="flex items-center gap-1.5">
              <Button variant="outline" size="xs" onClick={handleCopy} className="gap-1">
                {copied ? <Check className="h-3 w-3 text-emerald-400" /> : <Copy className="h-3 w-3" />}
                <span>Copy</span>
              </Button>
              <Button
                variant="outline"
                size="xs"
                onClick={loadLogs}
                disabled={isLoading}
                className="gap-1"
              >
                <RefreshCw className={`h-3 w-3 ${isLoading ? "animate-spin" : ""}`} />
                <span>Refresh</span>
              </Button>
            </div>
          </div>
        </DialogHeader>

        <div className="flex-1 overflow-auto rounded-lg border border-zinc-800 bg-zinc-950 p-4 font-mono text-xs text-zinc-300 leading-relaxed my-2 max-h-[55vh]">
          <pre className="whitespace-pre-wrap">{logs}</pre>
        </div>
      </DialogContent>
    </Dialog>
  );
};

