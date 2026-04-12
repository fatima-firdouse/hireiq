# main.py — updated for Day 2

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.candidate import router as candidate_router
from api.recruiter import router as recruiter_router   # ← uncommented

app = FastAPI(
    title="AI Hiring Intelligence System",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(candidate_router)
app.include_router(recruiter_router)   # ← added

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "AI Hiring Intelligence API — visit /docs"}