from io import BytesIO
from pypdf import PdfReader
from docx import Document

def parse_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)

    return "\n".join(pages)

def parse_docx(file_bytes: bytes) -> str:
    doc = Document(BytesIO(file_bytes))
    paragraphs = []

    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(paragraph.text)

    return "\n".join(paragraphs)

def extract_text(file_name: str, content_type: str, file_bytes: bytes) -> str:
    if content_type == "application/pdf":
        return parse_pdf(file_bytes)
    
    if content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return parse_docx(file_bytes)
    
    raise ValueError(f"Unsupported file type: {content_type}")