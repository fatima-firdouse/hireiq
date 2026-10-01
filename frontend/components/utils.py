# frontend/components/utils.py

import os
import requests
import streamlit as st

try:
    API_BASE_URL = st.secrets.get("API_BASE_URL", os.getenv("API_URL", "https://hireiq-backend-6noy.onrender.com"))
    if any(old in API_BASE_URL for old in ["13.49.78.118", "s4tk", "f829"]):
        API_BASE_URL = "https://hireiq-backend-6noy.onrender.com"
except Exception:
    API_BASE_URL = os.getenv("API_URL", "https://hireiq-backend-6noy.onrender.com")


def _extract_error(response) -> str:
    try:
        data = response.json()
        if isinstance(data, dict):
            return data.get("detail", str(data))
        return str(data)
    except Exception:
        text = response.text.strip()
        if len(text) > 150:
            text = text[:150] + "..."
        return f"Server error {response.status_code}: {text} (URL: {response.url})"


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
                "error": _extract_error(response)
            }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": f"Cannot connect to backend at {API_BASE_URL}. Ensure the service is live on Render."
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
                "error": _extract_error(response)
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
            return {"success": False, "error": _extract_error(response)}
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
            return {"success": False, "error": _extract_error(response)}
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
            return {"success": False, "error": _extract_error(response)}
    except Exception as e:
        return {"success": False, "error": str(e)}