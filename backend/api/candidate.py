# api/candidate.py

import os
import tempfile
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from config import MAX_FILE_SIZE_BYTES
from core.retriever import ingest_document
from intelligence.match_analyzer import analyze_match

router = APIRouter(prefix="/candidate", tags=["Candidate"])

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


class MatchRequest(BaseModel):
    collection_name: str
    job_description: str
    blind_mode: bool = False  # ← NEW field


@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and ingest a resume PDF or DOCX."""
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Invalid file type '{ext}'. Allowed: PDF, DOCX")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            413,
            f"File too large. Max: {MAX_FILE_SIZE_BYTES // (1024*1024)}MB"
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        collection_name = ingest_document(tmp_path)
    except (ValueError, RuntimeError) as e:
        raise HTTPException(422, str(e))
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    return JSONResponse({
        "status": "success",
        "collection_name": collection_name,
        "filename": file.filename,
    })


@router.post("/analyze-match")
async def analyze_match_endpoint(request: MatchRequest):
    """
    Compare uploaded resume against a job description.
    Supports blind_mode to strip PII before analysis.
    """
    if len(request.job_description.strip()) < 50:
        raise HTTPException(
            400,
            "Job description too short. Minimum 50 characters."
        )

    try:
        result = analyze_match(
            collection_name=request.collection_name,
            job_description=request.job_description,
            blind_mode=request.blind_mode
        )
    except ValueError as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, f"Analysis failed: {str(e)}")

    return JSONResponse({"status": "success", "data": result})