# Resume Analyzer with AI

A professional Streamlit web application that leverages advanced NLP techniques to analyze resume-job description compatibility, providing actionable insights for career optimization.

## Features

- **Multi-format Resume Parsing**: Supports PDF and DOCX file formats for comprehensive text extraction
- **Advanced Skill Extraction**: Utilizes spaCy NLP models to identify and categorize technical and soft skills
- **Semantic Matching**: Employs Sentence Transformers for accurate similarity scoring between resumes and job descriptions
- **Interactive Visualizations**: Features Plotly charts for intuitive display of skill matching results
- **AI-Powered Feedback**: Generates personalized improvement suggestions using Hugging Face transformer models
- **Real-time Processing**: Provides instant analysis with efficient caching mechanisms

## Architecture

The application is built with:
- **Frontend**: Streamlit for responsive web interface
- **NLP Engine**: spaCy for text processing and entity recognition
- **Embedding Models**: Sentence Transformers for semantic similarity
- **AI Models**: Hugging Face Transformers for text generation
- **Visualization**: Plotly for interactive charts

## Deployment

### Hugging Face Spaces (Recommended)

1. Create a new Space on Hugging Face
2. Set the Space to use Docker
3. Upload the `Dockerfile` and all project files
4. The Space will automatically build and deploy using the provided Dockerfile

### Local Development

```bash
# Clone the repository
git clone https://github.com/doriadrm/resume-analyzer.git
cd resume-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run the application
streamlit run app.py
```

## Usage

1. Upload your resume (PDF or DOCX format)
2. Paste the job description
3. Click "Analyze Resume" to get:
   - Match score
   - Skill analysis
   - Improvement suggestions

## Dependencies

- Python 3.11+
- Streamlit
- spaCy with en_core_web_sm model
- Sentence Transformers
- Hugging Face Transformers
- Plotly for visualizations

## Contributing

Contributions are welcome! Please ensure code quality and add tests for new features.

## License

MIT License
