import chromadb

# Create a persistent database
client = chromadb.PersistentClient(path="./chroma_store")

# Create or get a collection
collection = client.get_or_create_collection(name="helpdesk_docs")

def add_chunks(chunks: list[str], embeddings: list[list[float]], source: str):
    ids = [f"{source}--{i}" for i in range(len(chunks))]

    metadatas = [
        {"source": source, "chunk_index": i}
        for i in range(len(chunks))
    ]
   
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )


def search_chunks(query_embedding: list[float], top_k: int = 5):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )
    
    return results