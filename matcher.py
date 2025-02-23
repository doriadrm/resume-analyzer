from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_resume_to_job(resume_text, job_desc):
    """Compare resume with job description using TF-IDF"""
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_desc])
    
    similarity_score = cosine_similarity(vectors)[0, 1]
    return similarity_score
