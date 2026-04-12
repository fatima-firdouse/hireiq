
```markdown
# 🧠 HireIQ — AI Hiring Intelligence System

🔗 Live Demo: https://hireiq-ai.streamlit.app  
🔧 Backend API: FastAPI on AWS EC2  
📦 Architecture: RAG Pipeline + Vector Search + LLM Reasoning

---

## 🚀 Overview

HireIQ is an AI-powered hiring intelligence system that helps both candidates and recruiters make smarter, fairer hiring decisions using LLMs and Retrieval-Augmented Generation (RAG).

---

## 👤 Candidate Features

- 📊 Resume vs Job Description Match Score (0–100)
- 🧩 Skill Gap Analysis (matched vs missing skills)
- 🛠️ Resume Improvement Suggestions
- 🎯 STAR Interview Question Generation

---

## 🏢 Recruiter Features

- 🚨 Bias Detection in Job Descriptions
- 🧾 JD Quality Analysis (clarity, inflation, missing info)
- ✍️ AI-powered JD Rewrite (clean + inclusive version)

---

## 🧠 System Architecture

Streamlit Frontend  
↓  
FastAPI Backend (AWS EC2)  
↓  
RAG Pipeline:

- PDF/DOCX Parsing (pdfplumber, python-docx)
- Text Chunking (LangChain RecursiveCharacterTextSplitter)
- Embeddings (HuggingFace MiniLM-L6-v2)
- Vector DB (ChromaDB)
- Multi-query retrieval (top relevant chunks)
↓  
LLM Reasoning (Groq — LLaMA 3.1 8B Instant)
↓  
Final structured response

---

## 🛠️ Tech Stack

| Layer | Technology |
|------|------------|
| Frontend | Streamlit |
| Backend | FastAPI + Uvicorn |
| LLM | Groq (LLaMA 3.1 8B Instant) |
| Embeddings | HuggingFace MiniLM |
| Vector DB | ChromaDB |
| Parsing | pdfplumber, python-docx |
| Observability | Langfuse |
| Deployment | AWS EC2 + Streamlit Cloud |

---

## 📁 Project Structure

```

hireiq/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── api/
│   │   ├── candidate.py
│   │   └── recruiter.py
│   ├── core/
│   │   ├── parser.py
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   ├── retriever.py
│   │   └── llm_client.py
│   ├── intelligence/
│   │   ├── match_analyzer.py
│   │   ├── bias_detector.py
│   │   ├── jd_analyzer.py
│   │   └── jd_rewriter.py
│   ├── prompts/
│   ├── observability/
│
├── frontend/
│   ├── app.py
│   ├── pages/
│   │   ├── candidate.py
│   │   └── recruiter.py
│   └── components/
│       ├── styles.py
│       ├── charts.py
│       └── utils.py

```

---

## ⚡ Key Highlights

- 🔍 Multi-query RAG retrieval for better accuracy
- 🧠 Evidence-based bias detection (no hallucinated flags)
- 📈 STAR interview generation system
- ⚖️ Requirement inflation detection in job descriptions
- 📊 Full observability using Langfuse tracing

---

## 🔌 API Endpoints

```

POST /candidate/upload-resume
POST /candidate/analyze-match
POST /recruiter/detect-bias
POST /recruiter/analyze-jd
POST /recruiter/rewrite-jd
GET  /health

````

---

## 💻 Local Setup

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
````

### Frontend

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

---

## 🔐 Environment Variables

```env
GROQ_API_KEY=your_key
HF_API_KEY=your_key
HF_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHROMA_PERSIST_DIR=./chroma_db
LANGFUSE_PUBLIC_KEY=your_key
LANGFUSE_SECRET_KEY=your_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

---

## 👩‍💻 Author

**Fatima Firdouse**
B.Tech AI & Data Science (2026)
📍 Hyderabad, India

GitHub: [https://github.com/fatima-firdouse](https://github.com/fatima-firdouse)
LinkedIn: [https://linkedin.com/in/fatima-firdouse](https://linkedin.com/in/fatima-firdouse)

---

## 🧾 Note

Built as a production-grade portfolio project demonstrating:

* RAG pipeline design
* LLM reasoning workflows
* Full-stack AI system deployment

```

---

If you want next level improvement (and this is where your project becomes **“wow” for recruiters”**), I can help you add:
- 🔥 badges (Streamlit, FastAPI, AWS)
- 🖼️ architecture diagram
- 🎥 GIF demo section
- 💥 2-line “impact summary” that makes it sound like a startup product

Just say 👍
```
