# api/recruiter.py

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from intelligence.bias_detector import detect_bias
from intelligence.jd_analyzer import analyze_jd
from intelligence.jd_rewriter import rewrite_jd

router = APIRouter(prefix="/recruiter", tags=["Recruiter"])


class JDRequest(BaseModel):
    job_description: str


# --- Endpoint 1: Bias Detection ---
@router.post("/detect-bias")
async def detect_bias_endpoint(request: JDRequest):
    """Detect biased language in a job description."""
    try:
        result = detect_bias(request.job_description)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, f"Bias detection failed: {str(e)}")

    return JSONResponse({"status": "success", "data": result})


# --- Endpoint 2: JD Quality Analysis ---
@router.post("/analyze-jd")
async def analyze_jd_endpoint(request: JDRequest):
    """Analyze job description for quality issues."""
    try:
        result = analyze_jd(request.job_description)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, f"JD analysis failed: {str(e)}")

    return JSONResponse({"status": "success", "data": result})


# --- Endpoint 3: JD Rewrite ---
@router.post("/rewrite-jd")
async def rewrite_jd_endpoint(request: JDRequest):
    """
    Full pipeline: detect bias + analyze quality + rewrite JD.
    This is the most expensive endpoint (3 LLM calls).
    """
    try:
        result = rewrite_jd(request.job_description)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, f"JD rewrite failed: {str(e)}")

    return JSONResponse({"status": "success", "data": result})