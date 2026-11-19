import React, { useState, useEffect, useRef } from "react";
import { ChatHeader } from "./components/ChatHeader";
import { ChatMessage, MessageItem } from "./components/ChatMessage";
import { ChatInput } from "./components/ChatInput";
import { RetrievalSheet } from "./components/RetrievalSheet";
import { SettingsDialog } from "./components/SettingsDialog";
import { LogsDialog } from "./components/LogsDialog";
import { checkBackendHealth, sendQuery, HealthStatus, RAGResponse } from "./services/api";
import { Sparkles, FileText, Table as TableIcon, Image as ImageIcon } from "lucide-react";
import { FileText, Table as TableIcon, Image as ImageIcon } from "lucide-react";

export const App: React.FC = () => {
  const [messages, setMessages] = useState<MessageItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // Inspector & Dialogs
  const [sheetData, setSheetData] = useState<{
    isOpen: boolean;
    ragData: RAGResponse | null;
    sourceId: string | null;
  }>({
    isOpen: false,
    ragData: null,
    sourceId: null,
  });
  const [isLogsOpen, setIsLogsOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);

  // Hyperparameters
  const [topK, setTopK] = useState(5);
  const [candidateK, setCandidateK] = useState(20);
  const [documentId, setDocumentId] = useState("");

  // Health state
  const [health, setHealth] = useState<HealthStatus>({ status: "checking" });

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const checkHealth = async () => {
    setHealth({ status: "checking" });
    const res = await checkBackendHealth();
    setHealth(res);
  };

  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    const interval = setInterval(checkHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const handleSend = async (queryText: string) => {
    const userMsg: MessageItem = {
      id: `usr_${Date.now()}`,
      sender: "user",
      text: queryText,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const ragResponse = await sendQuery({
        question: queryText,
        top_k: topK,
        candidate_k: candidateK,
        document_id: documentId || undefined,
      });

      const assistantMsg: MessageItem = {
        id: `ast_${Date.now()}`,
        sender: "assistant",
        text: ragResponse.answer,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        ragData: ragResponse,
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      const errorMsg: MessageItem = {
        id: `err_${Date.now()}`,
        sender: "assistant",
        text: `Error retrieving answer: ${err.message}`,
        text: `**Backend Connection Error**: ${err.message}\n\nTo start the FastAPI backend on port 8000:\n\`\`\`bash\ncd multimodal-rag-api\nuvicorn app.main:app --reload\n\`\`\``,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleOpenInspector = (data: RAGResponse, sourceId?: string) => {
    setSheetData({
      isOpen: true,
      ragData: data,
      sourceId: sourceId || null,
    });
  };

  const starterPrompts = [
    {
      title: "Self-Attention Benefits",
      desc: "Why Transformer uses self-attention over recurrence",
      query: "Why does the Transformer use self-attention?",
      icon: FileText,
    },
    {
      title: "Table 1 Complexity",
      desc: "Layer complexity & sequential operation benchmark",
      query: "Compare layer complexity and sequential operations in Table 1.",
      icon: TableIcon,
    },
    {
      title: "Architecture Figure 1",
      desc: "Multi-head attention & encoder-decoder connections",
      query: "Explain the encoder-decoder attention connections in Figure 1.",
      icon: ImageIcon,
    },
  ];

  return (
    <div className="flex flex-col min-h-screen bg-zinc-950 text-zinc-100 selection:bg-zinc-800">
      {/* Minimal Header */}
      <ChatHeader
        health={health}
        onOpenLogs={() => setIsLogsOpen(true)}
        onOpenSettings={() => setIsSettingsOpen(true)}
        onResetChat={() => setMessages([])}
        onCheckHealth={checkHealth}
      />

      {/* Main Reading Canvas */}
      <main className="flex-1 flex flex-col max-w-3xl w-full mx-auto px-4 sm:px-6 pt-6 pb-28">
        {messages.length === 0 ? (
          /* Clean Minimal Empty State (Zero Clutter) */
          /* Clean Minimal Empty State */
          <div className="flex-1 flex flex-col items-center justify-center py-16 sm:py-24 text-center">
            <div className="space-y-2 mb-8 max-w-md">
              <h1 className="text-xl sm:text-2xl font-semibold tracking-tight text-zinc-100">
                Multimodal Document Intelligence
              </h1>
              <p className="text-xs sm:text-sm text-zinc-400 leading-relaxed">
                Retrieve and synthesize answers grounded in document text, structured tables, and architectural figures.
                Retrieve and synthesize answers directly from your PostgreSQL, Pinecone, and Gemini RAG pipeline.
              </p>
            </div>

            {/* Clean starter query buttons */}
            {/* Starter query buttons */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5 w-full max-w-2xl text-left">
              {starterPrompts.map((item, idx) => {
                const Icon = item.icon;
                return (
                  <button
                    key={idx}
                    onClick={() => handleSend(item.query)}
                    className="p-3.5 rounded-xl border border-zinc-800/80 bg-zinc-900/40 hover:bg-zinc-800/60 hover:border-zinc-700 transition-all text-xs group cursor-pointer"
                  >
                    <div className="flex items-center gap-2 mb-1.5 text-zinc-300 font-medium">
                      <Icon className="h-3.5 w-3.5 text-zinc-400 group-hover:text-zinc-200 transition-colors" />
                      <span>{item.title}</span>
                    </div>
                    <p className="text-[11px] text-zinc-500 leading-relaxed">
                      {item.desc}
                    </p>
                  </button>
                );
              })}
            </div>
          </div>
        ) : (
          /* Active Chat Feed */
          <div className="flex-1 divide-y divide-zinc-900 space-y-2">
            {messages.map((msg) => (
              <ChatMessage
                key={msg.id}
                message={msg}
                onInspect={(data, srcId) => handleOpenInspector(data, srcId)}
              />
            ))}

            {isLoading && (
              <div className="py-4 flex items-center gap-2 text-xs text-zinc-400 font-mono">
                <div className="h-3.5 w-3.5 border-2 border-zinc-400 border-t-transparent rounded-full animate-spin" />
                <span>Hybrid search & cross-encoder reranking...</span>
                <span>Running hybrid search & Cross-Encoder reranking on backend...</span>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        )}
      </main>

      {/* Clean Fixed Bottom Input */}
      <div className="fixed bottom-0 left-0 right-0 z-20 px-4 py-3 bg-gradient-to-t from-zinc-950 via-zinc-950/90 to-transparent">
        <ChatInput onSend={handleSend} isLoading={isLoading} topK={topK} />
      </div>

      {/* Right-Side Sliding Sheet for In-Depth Chunks Inspection */}
      <RetrievalSheet
        isOpen={sheetData.isOpen}
        onClose={() => setSheetData((prev) => ({ ...prev, isOpen: false }))}
        chunks={sheetData.ragData?.retrieved_chunks || []}
        rawContext={sheetData.ragData?.retrieval_context || []}
        sources={sheetData.ragData?.sources || []}
        highlightedSourceId={sheetData.sourceId}
      />

      {/* Settings Dialog */}
      <SettingsDialog
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        topK={topK}
        setTopK={setTopK}
        candidateK={candidateK}
        setCandidateK={setCandidateK}
        documentId={documentId}
        setDocumentId={setDocumentId}
      />

      {/* Logs Dialog */}
      <LogsDialog isOpen={isLogsOpen} onClose={() => setIsLogsOpen(false)} />
    </div>
  );
};

export default App;
