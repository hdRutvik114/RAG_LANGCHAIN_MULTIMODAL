from app.services.retrival_service import RetrievalService
from app.services.generation_service import GenerationService



class RAGService:
    def __init__(self,retrieval_service: RetrievalService, generation_service: GenerationService):
        self.retrieval_service = retrieval_service
        self.generation_service = generation_service
        
        
    def answer(
        self,
        question: str,
        top_k: int = 5,
        document_id: str | None = None,
    ) -> dict:

        retrieved_chunks = self.retrieval_service.retrieve(
            query=question,
            top_k=top_k,
            document_id=document_id,
        )

        if not retrieved_chunks:
            return {
                "question": question,
                "answer": "I couldn't find relevant information in the provided documents.",
                "sources": [],
            }

        context_parts = []
        sources = []

        for chunk in retrieved_chunks:
            page = chunk.get("page")

            context_parts.append(
                f"[Page {page}]\n{chunk['text']}"
            )

            sources.append({
                "source": chunk.get("source"),
                "page": page,
                "score": chunk.get("score"),
            })

        context = "\n\n".join(context_parts)

        answer = self.generation_service.generate(
            question=question,
            context=context,
        )

        return {
            "question": question,
            "answer": answer,
            "sources": sources,
        }
        
        