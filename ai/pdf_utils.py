import pdfplumber

def extract_text_from_pdf(pdf_file):
    """Extract text from an in-memory uploaded PDF file. No saving to disk."""
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        return None, f"PDF read error: {str(e)}"

    if not text.strip():
        return None, "PDF appears to be empty or image-based (no extractable text)."

    return text[:12000], None


def extract_text_from_study_file(study_file):
    """Extract study text from supported uploads."""
    name = study_file.name.lower()

    if name.endswith(".pdf"):
        return extract_text_from_pdf(study_file)

    if name.endswith((".txt", ".md")):
        try:
            raw = study_file.read()
            text = raw.decode("utf-8", errors="ignore")
        except Exception as e:
            return None, f"File read error: {str(e)}"

        if not text.strip():
            return None, "The uploaded file appears to be empty."

        return text[:12000], None

    return None, "Only PDF, TXT, and Markdown files are supported."
