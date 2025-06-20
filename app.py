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

# Load a better lightweight summarization model for CPU use
model_name = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def gpt_feedback(resume, job):
    try:
        prompt = f"How can I improve this resume to better match this job?\nResume: {resume}\nJob Description: {job}"
        inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(inputs, max_length=256, min_length=60, length_penalty=2.0, num_beams=4, early_stopping=True)
        return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    except Exception as e:
        return f"⚠️ HuggingFace model error: {e}"

st.set_page_config(page_title="Resume Analyzer AI", page_icon="📄")

st.title("📄 Resume Analyzer with AI 🤖")
st.markdown("Upload your resume, paste a job description, and see how well your resume matches!")

uploaded_file = st.file_uploader("📁 Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
job_desc = st.text_area("📝 Paste the job description here:")

if uploaded_file and job_desc:
    st.subheader("📌 Extracting Resume Data...")

    try:
        if uploaded_file.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".docx"):
            resume_text = extract_text_from_docx(uploaded_file)
        else:
            st.error("Unsupported file format.")
            st.stop()
    except Exception as e:
        st.error(f"Error extracting text: {e}")
        st.stop()

    with st.expander("🔍 View Extracted Resume Text"):
        st.write(resume_text or "No text found.")

    extracted_resume_skills = extract_skills(resume_text)
    extracted_job_skills = extract_skills(job_desc)

    st.subheader("🎯 Extracted Skills from Resume")
    if extracted_resume_skills:
        st.success(", ".join(sorted(extracted_resume_skills)))
    else:
        st.warning("No relevant skills detected in the resume.")

    st.subheader("🧾 Extracted Skills from Job Description")
    if extracted_job_skills:
        st.info(", ".join(sorted(extracted_job_skills)))
    else:
        st.warning("No relevant skills detected in the job description.")

    def show_skill_charts(resume_skills, job_skills):
        matched = set(skill.lower() for skill in resume_skills) & set(skill.lower() for skill in job_skills)
        missing = set(skill.lower() for skill in job_skills) - matched

        match_data = pd.DataFrame({
            "Type": ["Matched", "Missing"],
            "Count": [len(matched), len(missing)]
        })
        fig1 = px.bar(match_data, x="Type", y="Count", color="Type", title="Skill Match Overview",
                      color_discrete_map={"Matched": "green", "Missing": "red"})
        st.plotly_chart(fig1)

        if matched:
            matched_df = pd.DataFrame({"Skill": sorted(matched), "Status": ["Matched"] * len(matched)})
        else:
            matched_df = pd.DataFrame(columns=["Skill", "Status"])

        if missing:
            missing_df = pd.DataFrame({"Skill": sorted(missing), "Status": ["Missing"] * len(missing)})
        else:
            missing_df = pd.DataFrame(columns=["Skill", "Status"])

        full_df = pd.concat([matched_df, missing_df])

        if not full_df.empty:
            fig2 = px.pie(full_df, names="Skill", title="Matched vs Missing Skills Breakdown", color="Status",
                          color_discrete_map={"Matched": "green", "Missing": "red"})
            st.plotly_chart(fig2)

    st.subheader("📊 Skills Match Overview")
    show_skill_charts(extracted_resume_skills, extracted_job_skills)

    match_score = match_resume_to_job(resume_text, job_desc)
    st.subheader("✅ Resume Match Score")
    st.metric(label="Match Percentage", value=f"{match_score * 100:.2f}%")

    explanation = explain_match(resume_text, job_desc)
    with st.expander("🧠 Contextual Match Insights"):
        st.write(explanation)

    feedback = gpt_feedback(resume_text, job_desc)
    with st.expander("💡 Smart Suggestions (AI)"):
        st.write(feedback)

    if match_score >= 0.7:
        st.success("Great match! Your resume fits well with this job.")
    elif match_score >= 0.4:
        st.warning("Decent match. You may need to tweak your resume.")
    else:
        st.error("Low match. Consider improving your resume for this role.")

    if st.button("📄 Download Report"):
        report = f"""
        Resume Match Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        ------------------------------------------------------------
        Match Score: {match_score * 100:.2f}%
        Extracted Resume Skills: {', '.join(extracted_resume_skills)}
        Extracted Job Skills: {', '.join(extracted_job_skills)}

        Contextual Match:
        {explanation}

        Suggestions:
        {feedback}
        """
        b64 = base64.b64encode(report.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="resume_report.txt">📥 Click to download your report</a>'
        st.markdown(href, unsafe_allow_html=True)

else:
    st.info("Please upload your resume and paste a job description to get started.")
