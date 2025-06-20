import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

<<<<<<< HEAD
SKILLS_DB = [
    "machine learning", "deep learning", "supervised learning", "unsupervised learning",
    "python", "r", "sql", "nosql", "tensorflow", "pytorch", "pandas", "numpy",
    "scikit-learn", "big data", "nlp", "bert", "gpt", "data science", "cloud computing",
    "aws", "azure", "gcp", "docker", "kubernetes", "java", "c#", "javascript", "react",
    "node.js", "html", "css", "linux", "git", "bash", "powerbi", "tableau", "mongodb",
    "postgresql", "hadoop", "spark", "airflow", "flask", "fastapi", "jira", "agile",
    "kibana", "elasticsearch", "snowflake", "databricks", "clickhouse"
]

def extract_skills(text):
    doc = nlp(text.lower())
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(skill) for skill in SKILLS_DB]
    matcher.add("SKILLS", patterns)
    matches = matcher(doc)
    return list(set([doc[start:end].text.title() for match_id, start, end in matches]))
=======
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
>>>>>>> 80630c1d5d0d8395d9d3adb2079403dc938ae778
