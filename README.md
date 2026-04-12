# HireIQ — AI Hiring Intelligence System

> Production-grade AI system for smarter, fairer hiring decisions.

🔗 **Live Demo:** [hireiq-ai.streamlit.app](https://hireiq-ai.streamlit.app)  
🔧 **Backend API:** Deployed on AWS EC2  
📦 **Architecture:** RAG Pipeline + LLM Reasoning + Vector Search

---

## What It Does

### 🎯 Candidate Flow
Upload your resume (PDF/DOCX) and paste any job description to get:
- **Match Score** (0–100) — how well your resume fits the role
- **Skill Gap Analysis** — matched vs missing skills from the JD
- **Resume Improvement Suggestions** — specific, actionable fixes
- **STAR Interview Prep** — questions generated from your actual gaps

### 🏢 Recruiter Flow
Paste any job description to get:
- **Bias Detection** — context-aware, not keyword-based
- **JD Quality Analysis** — vague terms, missing info, requirement inflation score
- **AI Rewrite** — bias-free, inclusive, improved version with placeholders

---

## System Architecture

```
Frontend (Streamlit Cloud)
        ↓ HTTP
Backend (FastAPI on AWS EC2)
        ↓
RAG Pipeline:
  PDF/DOCX → pdfplumber / python-docx
  Text     → RecursiveCharacterTextSplitter (400 chars, 100 overlap)
  Chunks   → HuggingFace Inference API (all-MiniLM-L6-v2 embeddings)
  Vectors  → ChromaDB (PersistentClient, cosine similarity, HNSW index)
        ↓
Multi-Query Retrieval (3 focused queries → top 8 deduplicated chunks)
        ↓
LLM Reasoning → Groq API (LLaMA 3.1 8B Instant)
        ↓
Langfuse Observability (prompt + response + latency logged per call)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI + Uvicorn |
| RAG Pipeline | LangChain Text Splitters |
| Embeddings | HuggingFace Inference API — all-MiniLM-L6-v2 |
| Vector DB | ChromaDB |
| LLM | Groq — LLaMA 3.1 8B Instant |
| Observability | Langfuse |
| PDF Parsing | pdfplumber |
| DOCX Parsing | python-docx |
| Deployment | AWS EC2 (backend) + Streamlit Cloud (frontend) |

---

## Project Structure

```
hireiq/
├── backend/
│   ├── main.py                    # FastAPI entry point
│   ├── config.py                  # Centralized env vars
│   ├── requirements.txt
│   ├── api/
│   │   ├── candidate.py           # /candidate/* endpoints
│   │   └── recruiter.py           # /recruiter/* endpoints
│   ├── core/
│   │   ├── parser.py              # PDF/DOCX → raw text
│   │   ├── chunker.py             # Text → overlapping chunks
│   │   ├── embeddings.py          # Chunks → 384-dim vectors
│   │   ├── vector_store.py        # ChromaDB read/write
│   │   ├── retriever.py           # Full RAG orchestration
│   │   └── llm_client.py          # Groq API + Langfuse logging
│   ├── intelligence/
│   │   ├── match_analyzer.py      # Resume vs JD scoring
│   │   ├── bias_detector.py       # Context-aware bias detection
│   │   ├── jd_analyzer.py         # JD quality + inflation score
│   │   └── jd_rewriter.py         # Two-call AI JD rewrite
│   ├── prompts/
│   │   ├── match_analysis.py
│   │   ├── bias_detection.py
│   │   ├── jd_analysis.py
│   │   └── jd_rewrite.py
│   └── observability/
│       └── langfuse_logger.py
└── frontend/
    ├── app.py                     # Home page + role routing
    ├── requirements.txt
    ├── pages/
    │   ├── candidate.py           # 5-step candidate flow
    │   └── recruiter.py           # 3-step recruiter flow
    └── components/
        ├── styles.py              # All CSS (purple + black theme)
        ├── charts.py              # Plotly visualizations
        └── utils.py               # API call helpers
```

---

## Key Engineering Decisions

**Multi-query RAG retrieval** — instead of embedding the full JD as one diluted query, we run 3 focused queries (technical skills, experience, education) and merge top results. This improves chunk relevance from ~0.31 to ~0.55+.

**Evidence-based bias detection** — the LLM is instructed with JD START/END markers and told to only report phrases it can copy-paste verbatim from the text. Eliminates hallucinated bias flags.

**Two-call JD rewrite** — Call 1 generates the rewritten JD as plain text (no JSON, no truncation risk). Call 2 generates the changes summary as a small JSON. Solves the token truncation problem on Groq free tier.

**Requirement inflation scoring** — detects when nice-to-have skills are listed as required, and when experience requirements exceed the age of the technology.

**STAR interview framework** — questions include what a strong answer looks like + red flags to avoid, not just the question text.

**Langfuse tracing** — every LLM call is logged with trace name, prompt, response, latency in ms, and approximate token count. Graceful fallback if Langfuse is unavailable.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/candidate/upload-resume` | Upload PDF/DOCX → returns `collection_name` |
| POST | `/candidate/analyze-match` | Resume vs JD → score + gaps + STAR prep |
| POST | `/recruiter/detect-bias` | JD → bias report |
| POST | `/recruiter/analyze-jd` | JD → quality analysis |
| POST | `/recruiter/rewrite-jd` | JD → bias + quality + rewrite (3 LLM calls) |
| GET | `/health` | Health check |

---

## Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/fatima-firdouse/hireiq.git
cd hireiq

# 2. Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install chromadb --only-binary=:all:
pip install -r requirements.txt

# 3. Create .env
cp .env.example .env
# Fill in your API keys

# 4. Run backend
uvicorn main:app --reload --port 8000

# 5. Frontend (new terminal)
cd ../frontend
pip install -r requirements.txt
streamlit run app.py
```

---

## Environment Variables

```env
GROQ_API_KEY=gsk_...
HF_API_KEY=hf_...
HF_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHROMA_PERSIST_DIR=./chroma_db
MAX_FILE_SIZE_MB=5
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

---

## Requirements

**backend/requirements.txt**
```
fastapi==0.111.0
uvicorn==0.30.1
python-multipart==0.0.9
pdfplumber==0.11.0
python-docx==1.1.2
langchain-text-splitters==0.2.1
chromadb==1.5.5
groq==0.11.0
httpx==0.27.2
requests==2.32.3
python-dotenv==1.0.1
langfuse==2.36.1
packaging>=23.2,<24.0
pydantic==2.7.4
numpy>=1.24.0
```

**frontend/requirements.txt**
```
streamlit==1.35.0
plotly==5.22.0
requests==2.32.3
python-dotenv==1.0.1
```

---

## Deployment

| Service | Platform | Notes |
|---|---|---|
| Backend | AWS EC2 t2.micro (Ubuntu 22.04) | Port 8000, screen session |
| Frontend | Streamlit Cloud | Auto-deploys on GitHub push |
| Vector DB | ChromaDB on EC2 disk | Persisted to `./chroma_db` |
| LLM | Groq API | Free tier — 14,400 req/day |
| Embeddings | HuggingFace Inference API | Free tier |
| Observability | Langfuse Cloud | Free tier |

---

## Interview Questions This Project Covers

- What is RAG and why is it better than sending the full document to the LLM?
- Why chunk documents before embedding? What is chunk overlap?
- What is cosine similarity and why use it for text embeddings?
- What is mean pooling and why do sentence embedding models use it?
- What is HNSW and how does ChromaDB use it for fast retrieval?
- How do you prevent LLM hallucination in bias detection?
- Why use temperature 0.1 for structured JSON outputs?
- What is the singleton pattern and where did you use it?
- How does the two-call rewrite solve the token truncation problem?
- How does Langfuse observability work and what does it track?

---

## Built By

**Fatima Firdouse** — B.Tech Artificial Intelligence & Data Science  
Dr. VRK Women's College of Engineering & Technology, Hyderabad  
Graduating June 2026

📧 fatimafirdouse011@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/fatima-firdouse) · [GitHub](https://github.com/fatima-firdouse)

---

*Built in 3 days as a production-grade portfolio project demonstrating RAG pipeline architecture, LLM reasoning, prompt engineering, and full-stack AI deployment on AWS.*
