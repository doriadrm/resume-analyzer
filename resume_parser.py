import pdfplumber
import docx

def extract_text_from_pdf(pdf_file):
    """extracts text from a PDF file using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n"
    except Exception as e:
        text = ""
    return text.strip()

def extract_text_from_docx(docx_file):
    """extracts text from a DOCX file using python-docx."""
    try:
        doc = docx.Document(docx_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception:
        return ""
