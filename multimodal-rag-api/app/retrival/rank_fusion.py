from collections import defaultdict


def reciprocal_rank_fusion(
    ranked_lists: list[list[dict]],
    top_k: int = 10,
    rrf_k: int = 60,
) -> list[dict]:

    if not 1 <= top_k <= 50:
        raise ValueError("top_k must be between 1 and 50")

    scores = defaultdict(float)
    documents = {}

    for ranked_list in ranked_lists:
        for rank, document in enumerate(ranked_list, start=1):
            document_id = document["id"]

            scores[document_id] += 1 / (rrf_k + rank)

            if document_id not in documents:
                documents[document_id] = document.copy()

    fused_results = []

    for document_id, score in scores.items():
        result = documents[document_id].copy()
        result["score"] = score
        result["rrf_score"] = score
        fused_results.append(result)

    fused_results.sort(
        key=lambda document: document["rrf_score"],
        reverse=True,
    )

    return fused_results[:top_k]