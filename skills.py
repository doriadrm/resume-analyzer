import spacy
import re

nlp = spacy.load("en_core_web_sm")

# Sample skill set
SKILLS_DB = {
    "Machine Learning", "Deep Learning", "Python", "SQL", "TensorFlow", "Pandas",
    "Scikit-learn", "Big Data", "NLP", "Data Science", "Cloud Computing", "AWS",
    "Azure", "Docker", "Kubernetes", "Java", "C#", "React", "Node.js"
}

def extract_skills(text):
    """Extracts skills from resume text using NLP"""
    extracted_skills = set()
    
    doc = nlp(text)
    
    for token in doc:
        word = token.text.lower()
        for skill in SKILLS_DB:
            if re.search(rf"\b{skill.lower()}\b", word):
                extracted_skills.add(skill)

    return list(extracted_skills)
