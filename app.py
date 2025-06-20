import streamlit as st
from resume_parser import extract_text_from_pdf, extract_text_from_docx
from matcher import match_resume_to_job, explain_match
from skills import extract_skills
import plotly.express as px
import pandas as pd
import base64
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import time

#load summarization model (cached)
@st.cache_resource
def load_model():
    model_name = "facebook/bart-large-cnn"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

def gpt_feedback(resume, job):
    try:
        prompt = f"How can I improve this resume to better match this job?\nResume: {resume}\nJob Description: {job}"
        inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(inputs, max_length=256, min_length=60, length_penalty=2.0, num_beams=4, early_stopping=True)
        return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    except Exception as e:
        return f"⚠️ HuggingFace model error: {e}"

#Page configuration
st.set_page_config(page_title="Resume Analyzer AI", page_icon="📄", layout="wide")

#Custom CSS styling
st.markdown("""
<style>
body, .stApp {
    background-color: #f5f7fa;
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3 {
    color: #333;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
.report-container {
    background: #ffffff;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.metric-label {
    font-weight: bold;
    color: #444;
}
</style>
""", unsafe_allow_html=True)

#Title and Description
st.title("📄 Resume Analyzer with AI")
st.markdown("This tool analyzes your resume against any job description and offers smart, contextual feedback. No fluff — just actionable insights.")

#upload and Job Description Input
col1, col2 = st.columns([1, 2])
with col1:
    uploaded_file = st.file_uploader("📁 Upload Resume", type=["pdf", "docx"])
with col2:
    job_desc = st.text_area("📝 Paste Job Description")

if uploaded_file and job_desc:
    with st.spinner("🔍 Reading resume..."):
        try:
            if uploaded_file.name.endswith(".pdf"):
                resume_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.name.endswith(".docx"):
                resume_text = extract_text_from_docx(uploaded_file)
        except Exception as e:
            st.error(f"❌ Error extracting text: {e}")
            st.stop()

    st.success("✅ Resume parsed successfully!")

    #Extracted skills
    extracted_resume_skills = extract_skills(resume_text)
    extracted_job_skills = extract_skills(job_desc)

    def show_skill_charts(resume_skills, job_skills):
        matched = set(s.lower() for s in resume_skills) & set(s.lower() for s in job_skills)
        missing = set(s.lower() for s in job_skills) - matched

        match_df = pd.DataFrame({
            "Type": ["Matched", "Missing"],
            "Count": [len(matched), len(missing)]
        })
        st.plotly_chart(px.bar(match_df, x="Type", y="Count", color="Type",
                               color_discrete_map={"Matched": "green", "Missing": "red"},
                               title="Skill Match Overview"), use_container_width=True)

        if matched or missing:
            full_df = pd.DataFrame({
                "Skill": list(matched) + list(missing),
                "Status": ["Matched"] * len(matched) + ["Missing"] * len(missing)
            })
            st.plotly_chart(px.pie(full_df, names="Skill", color="Status", title="Matched vs Missing Skills",
                                   color_discrete_map={"Matched": "green", "Missing": "red"}), use_container_width=True)

    st.markdown("---")
    st.subheader("🎯 Skills Extraction")

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**From Resume:**")
        st.success(", ".join(sorted(extracted_resume_skills)) if extracted_resume_skills else "No skills detected.")
    with col4:
        st.markdown("**From Job Description:**")
        st.info(", ".join(sorted(extracted_job_skills)) if extracted_job_skills else "No skills detected.")

    show_skill_charts(extracted_resume_skills, extracted_job_skills)

    #Resume match score
    st.markdown("---")
    st.subheader("📈 Resume Match Score")
    with st.spinner("🔎 Calculating similarity..."):
        match_score = match_resume_to_job(resume_text, job_desc)
        time.sleep(1.5)
    st.metric(label="Match Percentage", value=f"{match_score * 100:.2f}%")

    #contextual sentence match
    with st.expander("🧠 Top Matching Sentences"):
        explanation = explain_match(resume_text, job_desc)
        st.markdown(explanation)

    #smart suggestions
    if st.button("💡 Generate Smart AI Suggestions"):
        with st.spinner("✍️ Crafting personalized feedback..."):
            feedback = gpt_feedback(resume_text, job_desc)
        st.markdown("#### 💡 Smart Suggestions")
        st.markdown(feedback)

    #final message
    st.markdown("---")
    if match_score >= 0.7:
        st.success("✅ Excellent match! Your resume is a strong fit.")
    elif match_score >= 0.4:
        st.warning("⚠️ Moderate match. Consider tailoring your resume further.")
    else:
        st.error("❌ Low match. You should definitely revise your resume.")

    #report download
    if st.button("📄 Download Report"):
        report = f"""
Resume Match Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
------------------------------------------------------------
Match Score: {match_score * 100:.2f}%
Resume Skills: {', '.join(extracted_resume_skills)}
Job Skills: {', '.join(extracted_job_skills)}

Top Matching Sentences:
{explanation}

AI Suggestions:
{feedback if 'feedback' in locals() else 'Not generated yet.'}
"""
        b64 = base64.b64encode(report.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="resume_report.txt">📥 Download Full Report</a>'
        st.markdown(href, unsafe_allow_html=True)

else:
    st.info("👆 Please upload your resume and paste a job description to begin.")
