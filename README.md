# 📝 AI-Powered Resume Analyzer

## 🚀 Project Overview
This project is an **AI-powered Resume Analyzer** that extracts key information from resumes using **Natural Language Processing (NLP)**. It processes PDF resumes, identifies important details like **name, skills, experience, and education**, and presents them in a structured format.

## 🎯 Features
✅ Upload a PDF resume
✅ Extract text using PyPDF2
✅ Identify key sections: Name, Skills, Experience, Education
✅ Simple web UI using **Streamlit**
✅ Easily expandable for job matching, ranking, etc.

## 🛠 Tech Stack
- **Python** (Pandas, NLTK, Spacy)
- **PyPDF2** (Extract text from PDFs)
- **Streamlit** (Web UI)
- **GitHub Actions** (Optional for CI/CD)

## 📂 Project Structure
```
resume-analyzer/
│── main.py              # Main script (Streamlit app)
│── resume_parser.py     # Extract & process text from PDF
│── requirements.txt     # Dependencies
│── README.md            # Project documentation
```

## 🚀 Installation & Usage
```bash
# Clone the repository
git clone https://github.com/doriadrm/resume-analyzer.git
cd resume-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run main.py
```

## 🌟 Future Enhancements
- 📌 Add AI-based job matching
- 📌 Support more file formats (DOCX, TXT)
- 📌 Integrate with databases for resume storage

## 🤝 Contributing
Pull requests are welcome! Feel free to **fork** the repo and make improvements. 🚀

---
✨ **Built with ❤️ by Doria** ✨
