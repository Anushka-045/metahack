import pdfplumber

def extract_text(file_path: str) -> str:
    """Reads a PDF and returns its text as a single string."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text