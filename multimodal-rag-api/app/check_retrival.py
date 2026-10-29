from app.embeddings.text_embeddings import TextEmbeddingService
from app.vectorstore.pinecone import PineconeVectorStore
from app.services.retrival_service import RetrievalService

embedding_service = TextEmbeddingService()
vector_store = PineconeVectorStore()

retrieval_service = RetrievalService(
    embedding_service=embedding_service,
    vector_store=vector_store,
)

query = "What information is contained in the stored document?"
results = retrieval_service.retrieve(query, top_k=3)

print(f"\nQuery: {query}\n")

for i, result in enumerate(results, start=1):
    print(f"--- Result {i} ---")
    print(f"Score: {result['score']}")
    print(f"Source: {result['source']}")
    print(f"Chunk: {result['chunk_index']}")
    print(f"Text: {result['text']}\n")