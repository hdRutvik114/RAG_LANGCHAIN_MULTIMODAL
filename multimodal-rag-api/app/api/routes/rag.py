from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.api.dependencies import get_rag_service
from app.services.rag_service import RAGService

router = APIRouter()


class QueryRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=50)
    candidate_k: int = Field(default=20, ge=1, le=50)
    document_id: str | None = None


@router.post("/query")
def query_rag(
    request: QueryRequest,
    rag_service: RAGService = Depends(get_rag_service),
):
    """
    Execute hybrid retrieval (Pinecone dense + PostgreSQL BM25Okapi + RRF + CrossEncoder rerank)
    and generate grounded response using Gemini LLM.
    """
    try:
        return rag_service.answer(
            question=request.question,
            top_k=request.top_k,
            document_id=request.document_id,
            candidate_k=request.candidate_k,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
