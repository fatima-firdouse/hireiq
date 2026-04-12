# config.py
# Central place for all settings. 
# Every other module imports from here — never from os.environ directly.

import os
from dotenv import load_dotenv

load_dotenv()

# LLM
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"  # fast, free tier

# Embeddings
HF_API_KEY = os.getenv("HF_API_KEY")
HF_EMBEDDING_MODEL = os.getenv(
    "HF_EMBEDDING_MODEL", 
    "sentence-transformers/all-MiniLM-L6-v2"
)
EMBEDDING_DIM = 384  # MiniLM output dimension

# ChromaDB
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")

# Langfuse
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY", "")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY", "")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

# File validation
MAX_FILE_SIZE_BYTES = int(os.getenv("MAX_FILE_SIZE_MB", 5)) * 1024 * 1024

# Chunking settings
CHUNK_SIZE = 400        # characters per chunk
CHUNK_OVERLAP = 100      # overlap between chunks