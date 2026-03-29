"""
Skill extraction using spaCy PhraseMatcher.
"""

import spacy
import subprocess
from spacy.matcher import PhraseMatcher
from typing import List, Dict
import logging

from config import SKILLS_DB, SKILL_CATEGORIES

logger = logging.getLogger(__name__)

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.info("Downloading en_core_web_sm...")
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
    nlp = spacy.load("en_core_web_sm")

def extract_skills(text: str) -> List[str]:
    """
    Extract skills from text using spaCy PhraseMatcher.

    Args:
        text: Input text to analyze

    Returns:
        List of unique skills found
    """
    try:
        doc = nlp(text.lower())
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        patterns = [nlp.make_doc(skill) for skill in SKILLS_DB]
        matcher.add("SKILLS", patterns)
        matches = matcher(doc)
        skills = list(set([doc[start:end].text.title() for match_id, start, end in matches]))
        logger.info(f"Extracted {len(skills)} skills")
        return skills
    except Exception as e:
        logger.error(f"Skill extraction failed: {e}")
        return []

def categorize_skills(skills: List[str]) -> Dict[str, List[str]]:
    """
    Categorize skills into predefined groups.

    Args:
        skills: List of skill names

    Returns:
        Dict mapping category names to lists of skills
    """
    categorized = {category: [] for category in SKILL_CATEGORIES.keys()}
    categorized["Other"] = []

    skill_lower = [skill.lower() for skill in skills]

    for skill, skill_lower in zip(skills, skill_lower):
        found = False
        for category, category_skills in SKILL_CATEGORIES.items():
            if skill_lower in category_skills:
                categorized[category].append(skill)
                found = True
                break
        if not found:
            categorized["Other"].append(skill)

    # Remove empty categories
    return {k: v for k, v in categorized.items() if v}
