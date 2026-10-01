# frontend/components/utils.py

import os
import requests
import streamlit as st

try:
    API_BASE_URL = st.secrets.get("API_BASE_URL", os.getenv("API_URL", "https://hireiq-backend-s4tk.onrender.com"))
    if "13.49.78.118" in API_BASE_URL:
        API_BASE_URL = "https://hireiq-backend-s4tk.onrender.com"
except Exception:
    API_BASE_URL = os.getenv("API_URL", "https://hireiq-backend-s4tk.onrender.com")


def upload_resume(file) -> dict:
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(
            f"{API_BASE_URL}/candidate/upload-resume",
            files=files,
            timeout=60
        )
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {
                "success": False,
                "error": response.json().get("detail", "Unknown error")
            }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Cannot connect to backend. Make sure FastAPI is running on port 8000."
        }
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out. Try a smaller file."}
    except Exception as e:
        return {"success": False, "error": str(e)}


def analyze_match(
    collection_name: str,
    job_description: str,
    blind_mode: bool = False
) -> dict:
    try:
        response = requests.post(
            f"{API_BASE_URL}/candidate/analyze-match",
            json={
                "collection_name": collection_name,
                "job_description": job_description,
                "blind_mode": blind_mode
            },
            timeout=60
        )
        if response.status_code == 200:
            return {"success": True, "data": response.json()["data"]}
        else:
            return {
                "success": False,
                "error": response.json().get("detail")
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


def detect_bias(job_description: str) -> dict:
    try:
        response = requests.post(
            f"{API_BASE_URL}/recruiter/detect-bias",
            json={"job_description": job_description},
            timeout=60
        )
        if response.status_code == 200:
            return {"success": True, "data": response.json()["data"]}
        else:
            return {"success": False, "error": response.json().get("detail")}
    except Exception as e:
        return {"success": False, "error": str(e)}


def analyze_jd(job_description: str) -> dict:
    try:
        response = requests.post(
            f"{API_BASE_URL}/recruiter/analyze-jd",
            json={"job_description": job_description},
            timeout=60
        )
        if response.status_code == 200:
            return {"success": True, "data": response.json()["data"]}
        else:
            return {"success": False, "error": response.json().get("detail")}
    except Exception as e:
        return {"success": False, "error": str(e)}


def rewrite_jd(job_description: str) -> dict:
    try:
        response = requests.post(
            f"{API_BASE_URL}/recruiter/rewrite-jd",
            json={"job_description": job_description},
            timeout=120
        )
        if response.status_code == 200:
            return {"success": True, "data": response.json()["data"]}
        else:
            return {"success": False, "error": response.json().get("detail")}
    except Exception as e:
        return {"success": False, "error": str(e)}