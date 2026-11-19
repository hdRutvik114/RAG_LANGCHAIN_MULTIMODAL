import React from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "./ui/dialog";
import { Button } from "./ui/button";

interface SettingsDialogProps {
  isOpen: boolean;
  onClose: () => void;
  topK: number;
  setTopK: (v: number) => void;
  candidateK: number;
  setCandidateK: (v: number) => void;
  documentId: string;
  setDocumentId: (v: string) => void;
}

export const SettingsDialog: React.FC<SettingsDialogProps> = ({
  isOpen,
  onClose,
  topK,
  setTopK,
  candidateK,
  setCandidateK,
  documentId,
  setDocumentId,
}) => {
  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Retrieval Hyperparameters</DialogTitle>
          <DialogDescription>
            Configure the hybrid search and cross-encoder reranking parameters.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4 py-2 text-xs">
          {/* Top-K */}
          <div className="space-y-1.5">
            <div className="flex justify-between font-medium">
              <span className="text-zinc-300">Top-K Context Chunks</span>
              <span className="font-mono text-zinc-400">{topK}</span>
            </div>
            <input
              type="range"
              min={1}
              max={15}
              value={topK}
              onChange={(e) => setTopK(Number(e.target.value))}
              className="w-full accent-zinc-200 cursor-pointer"
            />
            <p className="text-[11px] text-zinc-500">
              Number of reranked passages passed to the Gemini model.
            </p>
          </div>

          {/* Candidate-K */}
          <div className="space-y-1.5">
            <div className="flex justify-between font-medium">
              <span className="text-zinc-300">Candidate-K (RRF Fusion)</span>
              <span className="font-mono text-zinc-400">{candidateK}</span>
            </div>
            <input
              type="range"
              min={topK}
              max={50}
              value={candidateK}
              onChange={(e) => setCandidateK(Number(e.target.value))}
              className="w-full accent-zinc-200 cursor-pointer"
            />
            <p className="text-[11px] text-zinc-500">
              Initial candidates pulled by dense and sparse engines before fusion.
            </p>
          </div>

          {/* Document ID */}
          <div className="space-y-1.5">
            <label className="block font-medium text-zinc-300">
              Filter by Document ID (Optional)
            </label>
            <input
              type="text"
              value={documentId}
              onChange={(e) => setDocumentId(e.target.value)}
              placeholder="e.g. 91372821b401012093d6ef43a2bc6f87..."
              className="w-full rounded-md bg-zinc-900 border border-zinc-800 px-3 py-1.5 font-mono text-xs text-zinc-200 placeholder-zinc-600 focus:outline-none focus:border-zinc-600"
            />
            <div className="flex gap-2 pt-0.5">
              <Button
                variant="outline"
                size="xs"
                onClick={() =>
                  setDocumentId(
                    "91372821b401012093d6ef43a2bc6f87a1073fbcd4c2e64fb00217b3e1a0f052"
                  )
                }
                className="font-mono text-[10px]"
              >
                + attention.pdf ID
              </Button>
              {documentId && (
                <Button
                  variant="ghost"
                  size="xs"
                  onClick={() => setDocumentId("")}
                  className="text-zinc-500 text-[10px]"
                >
                  Clear
                </Button>
              )}
            </div>
          </div>
        </div>

        <div className="flex justify-end pt-2">
          <Button onClick={onClose} size="sm">
            Save Changes
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};

