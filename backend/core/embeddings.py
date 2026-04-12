# core/embeddings.py
# Stable embeddings using Hugging Face InferenceClient (no router issues)

from typing import List
import numpy as np
from huggingface_hub import InferenceClient
from config import HF_API_KEY, HF_EMBEDDING_MODEL


# ✅ Initialize HF client
client = InferenceClient(
    model=HF_EMBEDDING_MODEL,
    token=HF_API_KEY
)


def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of texts using HF Inference API.
    Reliable and avoids router/pipeline issues.
    """

    if not texts:
        return []

    embeddings = []

    for text in texts:
        emb = client.feature_extraction(text)

        # Normalize output shape
        emb_array = np.array(emb)

        if emb_array.ndim == 2:
            # [seq_len, hidden_dim] → mean pooling
            emb_array = emb_array.mean(axis=0)

        elif emb_array.ndim != 1:
            raise ValueError(f"Unexpected embedding shape: {emb_array.shape}")

        embeddings.append(emb_array.tolist())

    return embeddings


def get_single_embedding(text: str) -> List[float]:
    """
    Generate embedding for a single text.
    """
    return get_embeddings([text])[0]