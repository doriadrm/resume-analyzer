import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

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
