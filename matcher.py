"""
Semantic matching utilities using Sentence Transformers.
"""

import re
from sentence_transformers import SentenceTransformer, util
from typing import Dict, List, Tuple
import logging

from utils import sanitize_text

logger = logging.getLogger(__name__)

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

def match_resume_to_job(resume_text: str, job_desc: str) -> float:
    """
    Calculate semantic similarity between resume and job description.

    Args:
        resume_text: Resume content
        job_desc: Job description content

    Returns:
        Similarity score between 0 and 1
    """
    try:
        embeddings = model.encode([sanitize_text(resume_text), sanitize_text(job_desc)], convert_to_tensor=True)
        score = float(util.cos_sim(embeddings[0], embeddings[1]).item())
        logger.info(f"Calculated match score: {score:.3f}")
        return score
    except Exception as e:
        logger.error(f"Similarity calculation failed: {e}")
        return 0.0

def explain_match(resume_text: str, job_desc: str) -> str:
    """
    Find top matching sentences from resume to job description.

    Args:
        resume_text: Resume content
        job_desc: Job description content

    Returns:
        Formatted string of top 5 matching sentences with scores
    """
    try:
        # Improved sentence splitting using regex
        resume_sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', resume_text) if len(s.strip()) > 10]

        if not resume_sents:
            return "No suitable sentences found in resume for analysis."

        job_embedding = model.encode(sanitize_text(job_desc), convert_to_tensor=True)

        scored = []
        for sent in resume_sents[:50]:  # Limit to first 50 sentences for performance
            sent_emb = model.encode(sanitize_text(sent), convert_to_tensor=True)
            score = float(util.cos_sim(sent_emb, job_embedding).item())
            scored.append((sent, score))

        top_matches = sorted(scored, key=lambda x: x[1], reverse=True)[:5]
        result = "\n\n".join([f"• {sent} ({score:.2f})" for sent, score in top_matches])
        return result or "No strong semantic matches found."
    except Exception as e:
        logger.error(f"Match explanation failed: {e}")
        return "Error generating match explanation."

def get_match_breakdown(resume_text: str, job_desc: str) -> Dict:
    """
    Provide detailed breakdown of resume-job match.

    Args:
        resume_text: Resume content
        job_desc: Job description content

    Returns:
        Dict with overall_score, top_5_sentences, keyword_overlap_ratio, semantic_density
    """
    try:
        overall_score = match_resume_to_job(resume_text, job_desc)

        # Top 5 sentences
        resume_sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', resume_text) if len(s.strip()) > 10]
        job_embedding = model.encode(sanitize_text(job_desc), convert_to_tensor=True)

        scored_sentences = []
        similarities = []

        for sent in resume_sents[:50]:
            sent_emb = model.encode(sanitize_text(sent), convert_to_tensor=True)
            score = float(util.cos_sim(sent_emb, job_embedding).item())
            scored_sentences.append((sent, score))
            similarities.append(score)

        top_5_sentences = sorted(scored_sentences, key=lambda x: x[1], reverse=True)[:5]

        # Keyword overlap (simple word-based)
        resume_words = set(sanitize_text(resume_text).lower().split())
        job_words = set(sanitize_text(job_desc).lower().split())
        overlap = len(resume_words & job_words)
        total_unique = len(resume_words | job_words)
        keyword_overlap_ratio = overlap / total_unique if total_unique > 0 else 0

        # Semantic density
        semantic_density = sum(similarities) / len(similarities) if similarities else 0

        return {
            "overall_score": overall_score,
            "top_5_sentences": top_5_sentences,
            "keyword_overlap_ratio": keyword_overlap_ratio,
            "semantic_density": semantic_density
        }
    except Exception as e:
        logger.error(f"Match breakdown failed: {e}")
        return {
            "overall_score": 0.0,
            "top_5_sentences": [],
            "keyword_overlap_ratio": 0.0,
            "semantic_density": 0.0
        }
