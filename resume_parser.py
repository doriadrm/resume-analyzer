import pdfplumber
import docx

def extract_text_from_pdf(pdf_file):
<<<<<<< HEAD
=======
    """extracts text from a PDF file using pdfplumber."""
>>>>>>> 80630c1d5d0d8395d9d3adb2079403dc938ae778
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n"
<<<<<<< HEAD
    except Exception:
=======
    except Exception as e:
>>>>>>> 80630c1d5d0d8395d9d3adb2079403dc938ae778
        text = ""
    return text.strip()

def extract_text_from_docx(docx_file):
<<<<<<< HEAD
    try:
        doc = docx.Document(docx_file)
        return "\n".join([para.text for para in doc.paragraphs]).strip()
=======
    """extracts text from a DOCX file using python-docx."""
    try:
        doc = docx.Document(docx_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
>>>>>>> 80630c1d5d0d8395d9d3adb2079403dc938ae778
    except Exception:
        return ""
