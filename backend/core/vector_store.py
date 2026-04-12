# core/vector_store.py
# ChromaDB 0.4.x compatible version
# New API: PersistentClient replaces the old Settings-based Client

import chromadb
from typing import List, Dict
from config import CHROMA_PERSIST_DIR


# Singleton — one client instance for the app's lifetime
_client = None

def get_chroma_client() -> chromadb.PersistentClient:
    global _client
    if _client is None:
        # ✅ Correct API for chromadb 0.4.x
        _client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    return _client


def store_chunks(
    collection_name: str,
    chunks: List[Dict],
    embeddings: List[List[float]]
) -> None:
    client = get_chroma_client()

    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )

    collection.add(
        ids=[chunk["chunk_id"] for chunk in chunks],
        embeddings=embeddings,
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[
            {
                "doc_id": chunk["doc_id"],
                "chunk_index": chunk["chunk_index"]
            }
            for chunk in chunks
        ]
    )


def retrieve_chunks(
    collection_name: str,
    query_embedding: List[float],
    top_k: int = 5
) -> List[Dict]:
    client = get_chroma_client()

    try:
        collection = client.get_collection(collection_name)
    except Exception:
        raise ValueError(
            f"Collection '{collection_name}' not found. "
            "Document may not have been ingested yet."
        )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "distances", "metadatas"]
    )

    retrieved = []
    for i in range(len(results["documents"][0])):
        retrieved.append({
            "text": results["documents"][0][i],
            "score": 1 - results["distances"][0][i],
            "chunk_id": results["ids"][0][i],
            "metadata": results["metadatas"][0][i],
        })

    return retrieved


def delete_collection(collection_name: str) -> None:
    client = get_chroma_client()
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass