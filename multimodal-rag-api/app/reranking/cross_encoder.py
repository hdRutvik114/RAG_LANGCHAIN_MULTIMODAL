from sentence_transformers import CrossEncoder


class CrossEncoderReranker:
    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
    ):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        documents: list[dict],
        top_k: int = 5,
    ) -> list[dict]:

        if not documents:
            return []

        pairs = [
            (query, document["text"])
            for document in documents
        ]

        scores = self.model.predict(pairs)

        ranked_documents = []

        for document, score in zip(documents, scores):
            ranked_documents.append({
                **document,
                "rerank_score": float(score),
            })

        ranked_documents.sort(
            key=lambda item: item["rerank_score"],
            reverse=True,
        )

        return ranked_documents[:top_k]