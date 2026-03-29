import streamlit as st
from resume_parser import extract_text_from_pdf, extract_text_from_docx, get_resume_metadata
from matcher import match_resume_to_job, explain_match, get_match_breakdown
from skills import extract_skills, categorize_skills
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import base64
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import logging
from typing import Optional, Tuple

from config import (
    APP_NAME, APP_DESCRIPTION, BART_MODEL_NAME, GOOD_MATCH, MODERATE_MATCH,
    COLOR_PALETTE, MAX_FILE_SIZE_MB
)
from utils import (
    sanitize_text, truncate_for_model, validate_file_size, validate_job_description,
    get_match_color, format_percentage
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title=APP_NAME,
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load BART model (cached)
@st.cache_resource
def load_bart_model():
    """Load BART model for feedback generation."""
    try:
        tokenizer = AutoTokenizer.from_pretrained(BART_MODEL_NAME)
        model = AutoModelForSeq2SeqLM.from_pretrained(BART_MODEL_NAME)
        return tokenizer, model
    except Exception as e:
        logger.error(f"Failed to load BART model: {e}")
        return None, None

tokenizer, bart_model = load_bart_model()

# Custom CSS
st.markdown("""
<style>
.hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-card {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    text-align: center;
}
.gauge-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 300px;
}
.error-message {
    background: #fee;
    border: 1px solid #fcc;
    color: #c33;
    padding: 1rem;
    border-radius: 5px;
    margin: 1rem 0;
}
.success-message {
    background: #efe;
    border: 1px solid #cfc;
    color: #363;
    padding: 1rem;
    border-radius: 5px;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

def create_hero_section():
    """Create styled hero section."""
    st.markdown(f"""
    <div class="hero-section">
        <h1>{APP_NAME}</h1>
        <p>{APP_DESCRIPTION}</p>
    </div>
    """, unsafe_allow_html=True)

def create_sidebar():
    """Create sidebar with app info and settings."""
    with st.sidebar:
        st.header("Settings")

        # Settings toggles
        st.session_state.show_raw_text = st.checkbox("Show raw resume text", value=False)
        st.session_state.feedback_depth = st.selectbox(
            "Feedback depth",
            ["Quick", "Detailed"],
            index=0
        )

        st.header("How it works")
        st.markdown("""
        1. Upload your resume (PDF/DOCX)
        2. Paste job description
        3. Analyze for skill matches & semantic similarity
        4. Get AI feedback for improvements
        5. Download detailed report
        """)

        st.header("About")
        st.info(f"Version 2.0.0 | Built with Streamlit & AI models")

def generate_ai_feedback(resume: str, job: str, depth: str = "Quick") -> str:
    """Generate AI feedback using BART model."""
    if not tokenizer or not bart_model:
        return "⚠️ AI model not available. Please check model loading."

    try:
        max_length = 150 if depth == "Quick" else 300
        prompt = f"How can I improve this resume to better match this job?\n\nResume: {truncate_for_model(resume, 300)}\n\nJob Description: {truncate_for_model(job, 200)}"

        inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = bart_model.generate(
            inputs,
            max_length=max_length,
            min_length=50,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )
        feedback = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return feedback
    except Exception as e:
        logger.error(f"AI feedback generation failed: {e}")
        return f"⚠️ Error generating AI feedback: {str(e)}"

def create_gauge_chart(score: float) -> go.Figure:
    """Create circular gauge chart for match score."""
    color = get_match_color(score)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Match Score", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, MODERATE_MATCH * 100], 'color': COLOR_PALETTE["danger"]},
                {'range': [MODERATE_MATCH * 100, GOOD_MATCH * 100], 'color': COLOR_PALETTE["warning"]},
                {'range': [GOOD_MATCH * 100, 100], 'color': COLOR_PALETTE["success"]}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))

    fig.update_layout(
        font={'color': "darkblue", 'family': "Arial"},
        height=300
    )

    return fig

def create_skills_charts(resume_skills: list, job_skills: list, categorized_skills: dict):
    """Create skills visualization charts."""
    # Pie chart for matched vs missing
    matched = set(s.lower() for s in resume_skills) & set(s.lower() for s in job_skills)
    missing = set(s.lower() for s in job_skills) - matched

    pie_data = pd.DataFrame({
        "Type": ["Matched", "Missing"],
        "Count": [len(matched), len(missing)]
    })

    pie_fig = px.pie(
        pie_data,
        names="Type",
        values="Count",
        color="Type",
        color_discrete_map={"Matched": COLOR_PALETTE["success"], "Missing": COLOR_PALETTE["danger"]},
        title="Skill Match Overview"
    )

    # Horizontal bar chart for matched skills by relevance
    if matched:
        # Simple relevance based on frequency (can be improved)
        matched_list = list(matched)
        relevance_scores = [1.0] * len(matched_list)  # Placeholder

        bar_data = pd.DataFrame({
            "Skill": matched_list,
            "Relevance": relevance_scores
        }).sort_values("Relevance", ascending=True)

        bar_fig = px.bar(
            bar_data,
            x="Relevance",
            y="Skill",
            orientation='h',
            title="Matched Skills by Relevance",
            color="Relevance",
            color_continuous_scale="Blues"
        )
    else:
        bar_fig = None

    return pie_fig, bar_fig

def generate_html_report(match_data: dict, skills_data: dict) -> str:
    """Generate styled HTML report."""
    score = match_data["overall_score"]
    color = get_match_color(score)

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; }}
            .score-badge {{ background: {color}; color: white; padding: 10px 20px; border-radius: 20px; font-size: 24px; display: inline-block; margin: 10px 0; }}
            .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
            .skills-table {{ width: 100%; border-collapse: collapse; }}
            .skills-table th, .skills-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Resume Analysis Report</h1>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>

        <div class="section">
            <h2>Match Score</h2>
            <div class="score-badge">{format_percentage(score)}</div>
        </div>

        <div class="section">
            <h2>Skills Analysis</h2>
            <p><strong>Resume Skills:</strong> {', '.join(skills_data['resume_skills'])}</p>
            <p><strong>Job Skills:</strong> {', '.join(skills_data['job_skills'])}</p>
            <p><strong>Matched:</strong> {len(skills_data['matched'])} | <strong>Missing:</strong> {len(skills_data['missing'])}</p>
        </div>

        <div class="section">
            <h2>Semantic Match</h2>
            <p><strong>Keyword Overlap:</strong> {match_data['keyword_overlap_ratio']:.2%}</p>
            <p><strong>Semantic Density:</strong> {match_data['semantic_density']:.3f}</p>
        </div>

        <div class="section">
            <h2>AI Feedback</h2>
            <p>{match_data.get('ai_feedback', 'Not generated')}</p>
        </div>
    </body>
    </html>
    """

    return html

def main():
    """Main application logic."""
    create_hero_section()
    create_sidebar()

    # File upload and job description
    col1, col2 = st.columns([1, 2])

    with col1:
        uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

    with col2:
        job_desc = st.text_area("Job Description", height=100)

    # Validation
    validation_error = None
    if uploaded_file:
        if not validate_file_size(len(uploaded_file.getvalue())):
            validation_error = f"File size exceeds {MAX_FILE_SIZE_MB}MB limit."
        else:
            validation_error = validate_job_description(job_desc)

    if validation_error:
        st.markdown(f'<div class="error-message">❌ {validation_error}</div>', unsafe_allow_html=True)
        return

    if not uploaded_file or not job_desc:
        st.info("Please upload your resume and paste a job description to begin.")
        return

    # Processing with progress
    with st.status("Processing resume...", expanded=True) as status:
        st.write("Extracting text from resume...")

        # Extract text
        try:
            if uploaded_file.name.endswith(".pdf"):
                resume_text = extract_text_from_pdf(uploaded_file)
                metadata = get_resume_metadata(uploaded_file)
            elif uploaded_file.name.endswith(".docx"):
                resume_text = extract_text_from_docx(uploaded_file)
                metadata = {"page_count": 1, "word_count": len(resume_text.split()), "char_count": len(resume_text), "estimated_read_time": 1}
            else:
                st.markdown('<div class="error-message">❌ Unsupported file format</div>', unsafe_allow_html=True)
                return
        except Exception as e:
            st.markdown(f'<div class="error-message">❌ Error extracting text: {e}</div>', unsafe_allow_html=True)
            logger.error(f"Text extraction failed: {e}")
            return

        if not resume_text:
            st.markdown('<div class="error-message">❌ Could not extract text from the uploaded file.</div>', unsafe_allow_html=True)
            return

        st.write("Text extracted successfully!")
        status.update(label="Processing resume... Done!", state="complete")

    # Skills extraction
    with st.status("Analyzing skills...", expanded=True) as status:
        st.write("Extracting skills from resume and job description...")

        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_desc)
        categorized_skills = categorize_skills(resume_skills)

        st.write("Skills extracted!")
        status.update(label="Analyzing skills... Done!", state="complete")

    # Semantic matching
    with st.status("Calculating match score...", expanded=True) as status:
        st.write("Computing semantic similarity...")

        match_score = match_resume_to_job(resume_text, job_desc)
        match_breakdown = get_match_breakdown(resume_text, job_desc)

        st.write("Match calculated!")
        status.update(label="Calculating match score... Done!", state="complete")

    # AI Feedback
    with st.status("Generating AI feedback...", expanded=True) as status:
        st.write("Crafting personalized suggestions...")

        ai_feedback = generate_ai_feedback(resume_text, job_desc, st.session_state.feedback_depth)

        st.write("Feedback generated!")
        status.update(label="Generating AI feedback... Done!", state="complete")

    # Create tabs
    tab_overview, tab_skills, tab_semantic, tab_feedback, tab_report = st.tabs(
        ["Overview", "Skills", "Semantic Match", "AI Feedback", "Report"]
    )

    # Overview Tab
    with tab_overview:
        st.header("Analysis Overview")

        # Summary cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Match Score", format_percentage(match_score))

        with col2:
            matched_count = len(set(s.lower() for s in resume_skills) & set(s.lower() for s in job_skills))
            st.metric("Matched Skills", matched_count)

        with col3:
            missing_count = len(set(s.lower() for s in job_skills) - set(s.lower() for s in resume_skills))
            st.metric("Missing Skills", missing_count)

        with col4:
            st.metric("Resume Words", metadata["word_count"])

        # Gauge chart
        st.plotly_chart(create_gauge_chart(match_score), use_container_width=True)

        # Match interpretation
        if match_score >= GOOD_MATCH:
            st.markdown('<div class="success-message">Excellent match! Your resume is a strong fit.</div>', unsafe_allow_html=True)
        elif match_score >= MODERATE_MATCH:
            st.warning("Moderate match. Consider tailoring your resume further.")
        else:
            st.markdown('<div class="error-message">Low match. Significant improvements needed.</div>', unsafe_allow_html=True)

    # Skills Tab
    with tab_skills:
        st.header("Skills Analysis")

        # Charts
        pie_fig, bar_fig = create_skills_charts(resume_skills, job_skills, categorized_skills)

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(pie_fig, use_container_width=True)

        with col2:
            if bar_fig:
                st.plotly_chart(bar_fig, use_container_width=True)
            else:
                st.info("No matched skills to display.")

        # Categorized skills table
        st.subheader("Categorized Skills")
        if categorized_skills:
            # Create a dataframe for better display
            skill_rows = []
            for category, skills_list in categorized_skills.items():
                for skill in skills_list:
                    skill_rows.append({"Category": category, "Skill": skill})

            if skill_rows:
                skills_df = pd.DataFrame(skill_rows)
                st.dataframe(
                    skills_df,
                    column_config={
                        "Category": st.column_config.TextColumn("Category", width="medium"),
                        "Skill": st.column_config.TextColumn("Skill", width="large")
                    },
                    hide_index=True,
                    use_container_width=True
                )
        else:
            st.info("No skills detected.")

    # Semantic Match Tab
    with tab_semantic:
        st.header("Semantic Match Details")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Keyword Overlap", f"{match_breakdown['keyword_overlap_ratio']:.1%}")
        with col2:
            st.metric("Semantic Density", f"{match_breakdown['semantic_density']:.3f}")

        st.subheader("Top Matching Sentences")
        explanation = explain_match(resume_text, job_desc)
        st.markdown(explanation)

    # AI Feedback Tab
    with tab_feedback:
        st.header("AI-Powered Feedback")

        if st.session_state.feedback_depth == "Detailed":
            st.info("📝 Detailed feedback mode - more comprehensive suggestions")

        st.markdown(ai_feedback)

    # Report Tab
    with tab_report:
        st.header("Download Report")

        # Prepare report data
        report_data = {
            "overall_score": match_score,
            "keyword_overlap_ratio": match_breakdown["keyword_overlap_ratio"],
            "semantic_density": match_breakdown["semantic_density"],
            "ai_feedback": ai_feedback
        }

        skills_report_data = {
            "resume_skills": resume_skills,
            "job_skills": job_skills,
            "matched": list(set(s.lower() for s in resume_skills) & set(s.lower() for s in job_skills)),
            "missing": list(set(s.lower() for s in job_skills) - set(s.lower() for s in resume_skills))
        }

        html_report = generate_html_report(report_data, skills_report_data)

        # Download button
        st.download_button(
            label="Download HTML Report",
            data=html_report,
            file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
            mime="text/html"
        )

    # Optional raw text display
    if st.session_state.show_raw_text:
        with st.expander("Raw Resume Text"):
            st.text_area("Extracted Text", resume_text, height=200, disabled=True)

if __name__ == "__main__":
    main()
