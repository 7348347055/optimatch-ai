import pdfplumber
import logging

# Mute the noisy FontBBox warnings from the PDF parser
logging.getLogger("pdfminer").setLevel(logging.ERROR)

def extract_text_from_pdf(pdf_file) -> str:
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        return f"Error parsing PDF: {str(e)}"
    return text