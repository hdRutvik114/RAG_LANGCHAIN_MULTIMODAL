from app.vectorstore.pinecone import PineconeVectorStore

store = PineconeVectorStore()

stats = store.index.describe_index_stats()

print(stats)