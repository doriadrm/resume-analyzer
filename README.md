# Resume Analyzer with AI 

A smart and interactive Streamlit web app that helps you evaluate how well your resume matches a specific job description using NLP and AI-powered suggestions.

## Features

- Extracts text from PDF and DOCX resumes  
- Identifies relevant skills from your resume and the job description using NLP  
- Calculates a semantic similarity match score using Sentence Transformers  
- Visualizes matched vs missing skills using bar and pie charts  
- Generates tailored resume improvement suggestions using a Hugging Face summarization model

## Try It Live

[Click here to test the app directly on Hugging Face Spaces](https://huggingface.co/spaces/doriadrm/resume-analyzer)

## Local Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/resume-analyzer.git
cd resume-analyzer

# Install dependencies
pip install -r requirements.txt

# Download required spaCy model
python -m spacy download en_core_web_sm

# Run the Streamlit app
streamlit run app.py
