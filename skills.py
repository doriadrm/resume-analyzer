import spacy
from spacy.matcher import PhraseMatcher


#check if en_core_web_sm is installed, if not, download it
try:
    spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
finally:
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
