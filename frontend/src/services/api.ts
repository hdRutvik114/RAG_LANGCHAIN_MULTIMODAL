export interface SourceItem {
  id: string; // e.g. "S1"
  source: string; // e.g. "attention.pdf"
  page?: number | null;
  document_id?: string;
  score?: number | null;
}

export interface RetrievedChunk {
  id: string;
  score: number;
  text: string;
  source: string;
  page?: number | null;
  document_id: string;
  content_hash?: string;
  chunk_index?: number;
  chunk_type?: "text" | "table" | "image";
  image_url?: string;
  table_markdown?: string;
  rerank_score?: number;
  bm25_score?: number;
  dense_score?: number;
}

export interface RAGResponse {
  question: string;
  answer: string;
  sources: SourceItem[];
  retrieval_context: string[];
  retrieved_chunks?: RetrievedChunk[];
  latency_ms?: number;
}

export interface HealthStatus {
  status: "healthy" | "offline" | "checking";
  environment?: string;
  latencyMs?: number;
  error?: string;
}

const API_BASE = "/api";

export async function checkBackendHealth(): Promise<HealthStatus> {
  const startTime = performance.now();
  try {
    const res = await fetch(`${API_BASE}/health`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });
    const latency = Math.round(performance.now() - startTime);

    if (res.ok) {
      const data = await res.json();
      return {
        status: "healthy",
        environment: data.environment || "development",
        latencyMs: latency,
      };
    }
    return {
      status: "offline",
      latencyMs: latency,
      error: `HTTP ${res.status}`,
    };
  } catch (err: any) {
    return {
      status: "offline",
      error: err.message || "Failed to reach backend",
    };
  }
}

export async function fetchServerLogs(lines: number = 100): Promise<string> {
  try {
    const res = await fetch(`${API_BASE}/logs?lines=${lines}`, {
      method: "GET",
    });
    if (res.ok) {
      return await res.text();
    }
    return `[Status ${res.status}] Log access unavailable or not development mode.`;
  } catch (err: any) {
    return `Error fetching server logs: ${err.message}`;
  }
}

export async function sendQuery(params: {
  question: string;
  top_k?: number;
  candidate_k?: number;
  document_id?: string;
}): Promise<RAGResponse> {
  const start = performance.now();
  const payload = {
    question: params.question,
    top_k: params.top_k || 5,
    candidate_k: params.candidate_k || 20,
    document_id: params.document_id || null,
  };

  const res = await fetch(`${API_BASE}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const latency = Math.round(performance.now() - start);

  if (!res.ok) {
    let errorDetail = `Backend HTTP error ${res.status}`;
    try {
      const errJson = await res.json();
      if (errJson.detail) {
        errorDetail = typeof errJson.detail === "string" ? errJson.detail : JSON.stringify(errJson.detail);
      }
    } catch {
      // ignore
    }
    throw new Error(errorDetail);
  }

  const data = await res.json();

  return {
    question: data.question || params.question,
    answer: data.answer || "No response received from RAG service.",
    sources: data.sources || [],
    retrieval_context: data.retrieval_context || [],
    retrieved_chunks: data.retrieved_chunks || [],
    latency_ms: latency,
  };
}
