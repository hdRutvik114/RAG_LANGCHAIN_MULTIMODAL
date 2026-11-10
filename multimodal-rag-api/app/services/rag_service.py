
from app.services.retrival_service import RetrievalService
from app.services.generation_service import GenerationService


class RAGService:
    def __init__(
        self,
        retrieval_service: RetrievalService,
        generation_service: GenerationService,
    ):
        self.retrieval_service = retrieval_service
        self.generation_service = generation_service

    def answer(
        self,
        question: str,
        top_k: int = 5,
        document_id: str | None = None,
        candidate_k: int = 20,
    ) -> dict:

        # Retrieve candidates using hybrid search + reranking
        retrieved_chunks = self.retrieval_service.retrieve_hybrid_reranked(
            query=question,
            top_k=top_k,
            candidate_k=candidate_k,
            document_id=document_id,
        )

        if not retrieved_chunks:
            return {
                "question": question,
                "answer": "I couldn't find relevant information in the provided documents.",
                "sources": [],
                "retrieval_context": [],
            }

        context_parts = []
        retrieval_context = []
        sources = []
        source_ids = {}

        for chunk in retrieved_chunks:
            source = chunk.get("source", "unknown")
            page = chunk.get("page")
            doc_id = chunk.get("document_id", "")
            chunk_text = chunk["text"]

            source_key = (doc_id, source, page)

            if source_key not in source_ids:
                source_id = f"S{len(source_ids) + 1}"
                source_ids[source_key] = source_id

                sources.append({
                    "id": source_id,
                    "source": source,
                    "page": page,
                    "document_id": doc_id,
                    "score": chunk.get("score"),
                })

            source_id = source_ids[source_key]

            context_parts.append(
                f"[{source_id}] Source: {source} | Page: {page}\n"
                f"{chunk_text}"
            )

            # Keep raw retrieved text for evaluation
            retrieval_context.append(chunk_text)

        context = "\n".join(context_parts)

        answer = self.generation_service.generate(
            question=question,
            context=context,
        )

        return {
            "question": question,
            "answer": answer,
            "sources": sources,
            "retrieval_context": retrieval_context,
        }
