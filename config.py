"""
Configuration constants for the Resume Analyzer application.
"""

# Model configurations
BART_MODEL_NAME = "facebook/bart-large-cnn"
SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"
SPACY_MODEL = "en_core_web_sm"

# Score thresholds
GOOD_MATCH = 0.7
MODERATE_MATCH = 0.4

# UI constants
MAX_FILE_SIZE_MB = 5
MIN_JOB_DESC_LENGTH = 50

# Color palette
COLOR_PALETTE = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "success": "#2ca02c",
    "warning": "#ffbb78",
    "danger": "#d62728",
    "info": "#17becf",
    "light": "#f8f9fa",
    "dark": "#343a40"
}

# App metadata
APP_NAME = "Resume Analyzer AI"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "Advanced AI-powered resume analysis tool for job matching"

# Skills database (expanded)
SKILLS_DB = [
    "machine learning", "deep learning", "supervised learning", "unsupervised learning",
    "python", "r", "sql", "nosql", "tensorflow", "pytorch", "pandas", "numpy",
    "scikit-learn", "big data", "nlp", "bert", "gpt", "data science", "cloud computing",
    "aws", "azure", "gcp", "docker", "kubernetes", "java", "c#", "javascript", "react",
    "node.js", "html", "css", "linux", "git", "bash", "powerbi", "tableau", "mongodb",
    "postgresql", "hadoop", "spark", "airflow", "flask", "fastapi", "jira", "agile",
    "kibana", "elasticsearch", "snowflake", "databricks", "clickhouse",
    # New additions
    "langchain", "llm", "hugging face", "transformers", "openai", "fine-tuning",
    "rag", "vector database", "pinecone", "weaviate", "dbt", "mlflow", "wandb",
    "github actions", "ci/cd", "terraform", "redis", "kafka", "graphql", "rust"
]

# Skill categories
SKILL_CATEGORIES = {
    "AI/ML": ["machine learning", "deep learning", "supervised learning", "unsupervised learning",
              "tensorflow", "pytorch", "scikit-learn", "nlp", "bert", "gpt", "langchain",
              "llm", "hugging face", "transformers", "openai", "fine-tuning", "rag"],
    "Data": ["python", "r", "sql", "nosql", "pandas", "numpy", "big data", "data science",
             "mongodb", "postgresql", "hadoop", "spark", "snowflake", "databricks", "clickhouse",
             "dbt", "vector database", "pinecone", "weaviate"],
    "Cloud": ["aws", "azure", "gcp", "cloud computing"],
    "DevOps": ["docker", "kubernetes", "github actions", "ci/cd", "terraform", "linux", "bash"],
    "Web": ["javascript", "react", "node.js", "html", "css", "flask", "fastapi", "graphql"],
    "Other": ["java", "c#", "git", "airflow", "jira", "agile", "kibana", "elasticsearch",
              "powerbi", "tableau", "mlflow", "wandb", "redis", "kafka", "rust"]
}