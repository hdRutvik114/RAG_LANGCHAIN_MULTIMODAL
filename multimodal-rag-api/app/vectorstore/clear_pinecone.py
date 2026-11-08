from app.vectorstore.pinecone import PineconeVectorStore

vector_store = PineconeVectorStore()
vector_store.delete_all_vectors()

print("All vectors deleted from Pinecone.")