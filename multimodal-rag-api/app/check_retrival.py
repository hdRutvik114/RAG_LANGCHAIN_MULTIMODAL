from app.services.retrival_service import RetrievalService
from app.embeddings.text_embeddings import TextEmbeddingService
from app.vectorstore.pinecone import PineconeVectorStore

service = RetrievalService(
    embedding_service=TextEmbeddingService(),
    vector_store=PineconeVectorStore(),
)

PDF_DOCUMENT_ID = "91372821b401012093d6ef43a2bc6f87a1073fbcd4c2e64fb00217b3e1a0f052"

results = service.retrieve(
    query="Why does the Transformer use self-attention?",
    top_k=3,
    document_id=PDF_DOCUMENT_ID,
)

for index, result in enumerate(results, start=1):
    print(f"\n--- Result {index} ---")
    print(f"Source: {result['source']}")
    print(f"Page: {result['page']}")
    print(f"Score: {result['score']}")
    print(f"Text: {result['text']}")