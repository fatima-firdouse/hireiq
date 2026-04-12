# core/retriever.py
# Orchestrates the full RAG pipeline:
# text → chunks → embeddings → store  (ingestion)
# query → embedding → retrieve         (retrieval)

import uuid
from typing import List, Dict

from core.parser import extract_text
from core.chunker import chunk_text
from core.embeddings import get_embeddings, get_single_embedding
from core.vector_store import store_chunks, retrieve_chunks, delete_collection


def ingest_document(file_path: str) -> str:
    """
    Full ingestion pipeline for a single document.
    
    Steps:
      1. Extract text from PDF/DOCX
      2. Chunk the text
      3. Generate embeddings for all chunks
      4. Store in ChromaDB
    
    Returns:
        collection_name — pass this to retrieve() later
    """
    # Generate a unique collection name for this document
    doc_id = str(uuid.uuid4()).replace("-", "")[:12]
    collection_name = f"doc_{doc_id}"

    # Step 1: Parse
    raw_text = extract_text(file_path)

    # Step 2: Chunk
    chunks = chunk_text(raw_text, doc_id)

    if not chunks:
        raise RuntimeError("Document produced zero chunks after processing.")

    # Step 3: Embed — batch all chunk texts together
    chunk_texts = [chunk["text"] for chunk in chunks]
    embeddings = get_embeddings(chunk_texts)

    # Step 4: Store
    store_chunks(collection_name, chunks, embeddings)

    return collection_name


def retrieve(
    collection_name: str,
    query: str,
    top_k: int = 5
) -> List[Dict]:
    """
    Retrieve relevant chunks for a query from an ingested document.
    
    Args:
        collection_name: returned by ingest_document()
        query:           job description or any query text
        top_k:           number of chunks to retrieve
    
    Returns:
        List of relevant chunk dicts (text + similarity score)
    """
    query_embedding = get_single_embedding(query)
    results = retrieve_chunks(collection_name, query_embedding, top_k)
    return results


def get_context_string(retrieved_chunks: List[Dict]) -> str:
    """
    Format retrieved chunks into a single context string for the LLM.
    Chunks are sorted by score (highest first).
    """
    sorted_chunks = sorted(retrieved_chunks, key=lambda x: x["score"], reverse=True)
    context_parts = []

    for i, chunk in enumerate(sorted_chunks):
        context_parts.append(
            f"[Chunk {i+1} | Relevance: {chunk['score']:.2f}]\n{chunk['text']}"
        )

    return "\n\n---\n\n".join(context_parts)