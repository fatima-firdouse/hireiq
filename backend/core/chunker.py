# core/chunker.py
# Why chunk? LLMs and embedding models have token limits.
# Chunking breaks large documents into retrievable pieces.

from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP
from typing import List


def chunk_text(text: str, doc_id: str) -> List[dict]:
    """
    Split text into overlapping chunks with metadata attached.
    
    Args:
        text:   raw extracted text
        doc_id: unique identifier for this document (used in ChromaDB)
    
    Returns:
        List of dicts: [{"chunk_id": str, "text": str, "doc_id": str}, ...]
    
    Why RecursiveCharacterTextSplitter?
    It tries to split on: paragraphs → sentences → words → characters.
    This preserves semantic boundaries better than fixed-size splitting.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    raw_chunks = splitter.split_text(text)

    chunks = []
    for idx, chunk_text in enumerate(raw_chunks):
        chunks.append({
            "chunk_id": f"{doc_id}_chunk_{idx}",
            "text": chunk_text.strip(),
            "doc_id": doc_id,
            "chunk_index": idx,
        })

    return chunks