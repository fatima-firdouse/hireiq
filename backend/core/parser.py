# core/parser.py

import pdfplumber
import docx
import os

def extract_text(file_path: str) -> str:
    """
    Extract raw text from PDF or DOCX file.
    
    Args:
        file_path: absolute or relative path to the uploaded file
    
    Returns:
        Extracted text as a single string
    
    Raises:
        ValueError: if file format is not supported
        RuntimeError: if extraction fails
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return _extract_from_pdf(file_path)
    elif ext == ".docx":
        return _extract_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}. Only PDF and DOCX are supported.")


def _extract_from_pdf(file_path: str) -> str:
    """
    Uses pdfplumber which handles:
    - multi-column layouts
    - tables (converts to readable text)
    - scanned PDFs (partially)
    """
    text_parts = []

    try:
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
                # If a page has a table, extract it separately
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        row_text = " | ".join(
                            cell if cell else "" for cell in row
                        )
                        text_parts.append(row_text)
    except Exception as e:
        raise RuntimeError(f"PDF extraction failed: {str(e)}")

    full_text = "\n".join(text_parts).strip()

    if not full_text:
        raise RuntimeError(
            "No text extracted from PDF. "
            "The file may be scanned/image-based. "
            "Please upload a text-based PDF."
        )

    return full_text


def _extract_from_docx(file_path: str) -> str:
    """
    Extracts from paragraphs + tables inside DOCX.
    """
    try:
        doc = docx.Document(file_path)
        text_parts = []

        # Extract paragraphs
        for para in doc.paragraphs:
            if para.text.strip():
                text_parts.append(para.text.strip())

        # Extract tables
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join(
                    cell.text.strip() for cell in row.cells
                )
                if row_text.strip():
                    text_parts.append(row_text)

    except Exception as e:
        raise RuntimeError(f"DOCX extraction failed: {str(e)}")

    full_text = "\n".join(text_parts).strip()

    if not full_text:
        raise RuntimeError("No text extracted from DOCX. File may be empty.")

    return full_text