"""
Utility functions for text processing and validation.
"""

import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def sanitize_text(text: str) -> str:
    """Clean and normalize extracted text by removing extra whitespace and normalizing quotes."""
    if not text:
        return ""

    # Remove extra whitespace and normalize line breaks
    text = re.sub(r'\s+', ' ', text.strip())

    # Normalize quotes
    text = text.replace('"', '"').replace('"', '"').replace(''', "'").replace(''', "'")

    return text

def truncate_for_model(text: str, max_words: int = 400) -> str:
    """Truncate text to a maximum number of words for safe model inference."""
    if not text:
        return ""

    words = text.split()
    if len(words) <= max_words:
        return text

    truncated = ' '.join(words[:max_words])
    logger.warning(f"Text truncated from {len(words)} to {max_words} words")
    return truncated + "..."

def validate_file_size(file_size: int) -> bool:
    """Check if file size is within acceptable limits."""
    from config import MAX_FILE_SIZE_MB
    max_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
    return file_size <= max_size_bytes

def validate_job_description(job_desc: str) -> Optional[str]:
    """Validate job description length and return error message if invalid."""
    from config import MIN_JOB_DESC_LENGTH
    if len(job_desc.strip()) < MIN_JOB_DESC_LENGTH:
        return f"Job description must be at least {MIN_JOB_DESC_LENGTH} characters long."
    return None

def get_match_color(score: float) -> str:
    """Get color based on match score."""
    from config import GOOD_MATCH, MODERATE_MATCH, COLOR_PALETTE
    if score >= GOOD_MATCH:
        return COLOR_PALETTE["success"]
    elif score >= MODERATE_MATCH:
        return COLOR_PALETTE["warning"]
    else:
        return COLOR_PALETTE["danger"]

def format_percentage(score: float) -> str:
    """Format score as percentage string."""
    return f"{score * 100:.1f}%"