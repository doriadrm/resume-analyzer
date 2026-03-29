"""
Resume text extraction utilities.
"""

import pdfplumber
import docx
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract text from PDF file using pdfplumber, with PyMuPDF fallback.

    Args:
        pdf_file: File-like object or path to PDF

    Returns:
        Extracted text as string
    """
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n"
    except Exception as e:
        logger.warning(f"pdfplumber failed: {e}, trying PyMuPDF fallback")
        text = _extract_pdf_fallback(pdf_file)

    return text.strip()

def _extract_pdf_fallback(pdf_file) -> str:
    """Fallback PDF extraction using PyMuPDF (fitz)."""
    try:
        import fitz  # PyMuPDF
        text = ""
        with fitz.open(pdf_file) as doc:
            for page in doc:
                text += page.get_text() + "\n"
        return text.strip()
    except ImportError:
        logger.error("PyMuPDF not available for fallback")
        return ""
    except Exception as e:
        logger.error(f"PyMuPDF extraction failed: {e}")
        return ""

def extract_text_from_docx(docx_file) -> str:
    """
    Extract text from DOCX file.

    Args:
        docx_file: File-like object or path to DOCX

    Returns:
        Extracted text as string
    """
    try:
        doc = docx.Document(docx_file)
        return "\n".join([para.text for para in doc.paragraphs]).strip()
    except Exception as e:
        logger.error(f"DOCX extraction failed: {e}")
        return ""

def get_resume_metadata(pdf_file) -> Dict[str, int]:
    """
    Extract metadata from PDF resume.

    Args:
        pdf_file: File-like object or path to PDF

    Returns:
        Dict with page_count, word_count, char_count, estimated_read_time
    """
    try:
        text = extract_text_from_pdf(pdf_file)
        if not text:
            return {"page_count": 0, "word_count": 0, "char_count": 0, "estimated_read_time": 0}

        words = text.split()
        chars = len(text)
        pages = 1  # Approximate, could be improved

        # Estimate read time (200 words per minute average)
        read_time_minutes = len(words) / 200

        return {
            "page_count": pages,
            "word_count": len(words),
            "char_count": chars,
            "estimated_read_time": int(read_time_minutes)
        }
    except Exception as e:
        logger.error(f"Metadata extraction failed: {e}")
        return {"page_count": 0, "word_count": 0, "char_count": 0, "estimated_read_time": 0}
