# Nexus Multimodal RAG — Frontend UI

A sleek, modern developer-first chatbot UI for the **Multimodal RAG API**, built with **React**, **Vite**, **Tailwind CSS v4**, and **React Bits** design patterns.

---

## Features

- **React Bits Craftsmanship**:
  - `SpotlightCard`: Mouse-tracking dynamic radial lighting effects.
  - `ShinyText`: Sweeping gradient metallic shine on headers.
  - `DecryptedText`: Interactive hacker-style text scramble decryption effect on brand load.
  - Ultra-crisp glassmorphism (`backdrop-blur-xl`, subtle `white/10` borders, dark zinc aesthetic).
- **"Show Everything" Multimodal RAG Transparency**:
  - **Inline Citations**: Every claim in the LLM answer is tagged with interactive `[S1]`, `[S2]` pills displaying file name and page number.
  - **Grounding Cards**: Full breakdown of all sources, document IDs, and confidence/reranking scores.
  - **Retrieved Chunks Inspector**: Inspect individual chunks retrieved by the hybrid pipeline with their dense similarity, BM25 keyword score, and Cross-Encoder score.
  - **Table-Level Support**: Renders structured markdown tables with clean dark borders and headers.
  - **Image / Diagram Support**: Displays extracted figure diagrams and images directly inline.
  - **Raw LLM Context Viewer**: View the exact combined context string fed into Google Gemini.
- **Backend Connection & Telemetry**:
  - Live backend health indicator pinging `GET /health` with real-time round-trip latency.
  - **Server Logs Viewer**: Modal that tails live application logs from `GET /logs` with real-time text search and line count selector.
  - **Hyperparameter Tuner**: Adjust `top_k`, `candidate_k`, and document ID filtering.
  - Fallback simulation engine for instant preview even before backend routes are registered.

---

## Getting Started

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Start the Frontend Development Server
```bash
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## Connecting to Backend

The frontend is configured with a Vite proxy in `vite.config.ts`:
- Requests to `/api/*` are automatically forwarded to `http://localhost:8000/*`.
- When your FastAPI backend is running (`uvicorn app.main:app --reload`), the health badge will turn green: `Backend: Online (Xms)`.

### Optional: Wiring the RAG Query Endpoint in Backend
To connect your existing backend services directly to the chat endpoint without touching your core logic, you can add this route to your FastAPI application when ready:

```python
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.api.dependencies import get_rag_service
from app.services.rag_service import RAGService

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    top_k: int = 5
    candidate_k: int = 20
    document_id: str | None = None

@router.post("/rag/query")
def query_rag(req: QueryRequest, rag_service: RAGService = Depends(get_rag_service)):
    return rag_service.answer(
        question=req.question,
        top_k=req.top_k,
        candidate_k=req.candidate_k,
        document_id=req.document_id,
    )
```

