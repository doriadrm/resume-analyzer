from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def match_resume_to_job(resume_text, job_desc):
    embeddings = model.encode([resume_text, job_desc], convert_to_tensor=True)
    return float(util.cos_sim(embeddings[0], embeddings[1]).item())

def explain_match(resume_text, job_desc):
    resume_sents = [s.strip() for s in resume_text.split('.') if len(s.strip()) > 10]
    job_embedding = model.encode(job_desc, convert_to_tensor=True)

    scored = []
    for sent in resume_sents:
        sent_emb = model.encode(sent, convert_to_tensor=True)
        score = float(util.cos_sim(sent_emb, job_embedding).item())
        scored.append((sent, score))

    top_matches = sorted(scored, key=lambda x: x[1], reverse=True)[:5]
    return "\n\n".join([f"• {sent} ({score:.2f})" for sent, score in top_matches]) or "No strong semantic matches found."
