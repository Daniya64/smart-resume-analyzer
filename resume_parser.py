
import pdfplumber


def extract_resume_text(pdf_file):
    text = ""

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    if not text.strip():
        raise ValueError(
            "No text found. Please upload a text-based PDF resume."
        )

    return text
