import spacy
import re

nlp = spacy.load("en_core_web_sm")

# Expanded skills DB (you can add more)
SKILLS_DB = {
    "machine learning", "deep learning", "python", "sql", "tensorflow", "pandas",
    "scikit-learn", "big data", "nlp", "data science", "cloud computing", "aws",
    "azure", "docker", "kubernetes", "java", "c#", "react", "node.js", "fastapi",
    "flask", "linux", "git", "bash", "powerbi", "tableau"
}

def extract_skills(text):
    """Extracts skills from resume text using spaCy and regex."""
    extracted = set()
    text = text.lower()
    doc = nlp(text)

    tokens = [token.text for token in doc]
    full_text = " ".join(tokens)

    for skill in SKILLS_DB:
        pattern = rf"\b{re.escape(skill.lower())}\b"
        if re.search(pattern, full_text):
            extracted.add(skill.title())

    return list(extracted)
