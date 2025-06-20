import streamlit as st
from resume_parser import extract_text_from_pdf, extract_text_from_docx
from matcher import match_resume_to_job
from skills import extract_skills

st.set_page_config(page_title="Resume Analyzer AI", page_icon="📄")

st.title("📄 Resume Analyzer with AI 🤖")
st.markdown("Upload your resume, paste a job description, and see how well your resume matches!")

# Upload resume file
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

    extracted_skills = extract_skills(resume_text)
    st.subheader("🎯 Extracted Skills")
    if extracted_skills:
        st.success(", ".join(sorted(extracted_skills)))
    else:
        st.warning("No relevant skills detected.")

    match_score = match_resume_to_job(resume_text, job_desc)
    st.subheader("✅ Resume Match Score")
    st.metric(label="Match Percentage", value=f"{match_score * 100:.2f}%")

    if match_score >= 0.7:
        st.success("Great match! Your resume fits well with this job.")
    elif match_score >= 0.4:
        st.warning("Decent match. You may need to tweak your resume.")
    else:
        st.error("Low match. Consider improving your resume for this role.")
else:
    st.info("Please upload your resume and paste a job description to get started.")
