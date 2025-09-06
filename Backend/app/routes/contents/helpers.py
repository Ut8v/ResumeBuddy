from fastapi import HTTPException
from typing import Literal
from io import BytesIO
import magic
from docx import Document
from pdfminer.high_level import extract_text as pdf_extract_text

# Only allow these types
ALLOWED: set[Literal[
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain"
]] = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
}

MAX_BYTES = 3 * 1024 * 1024  # 3mb


def detect_type(buffer: bytes) -> str:
    file_type = magic.from_buffer(buffer, mime=True)
    if not file_type:
        raise HTTPException(status_code=415, detail=f"Unsupported file type")
    return file_type


def extract_text_from_file(filename: str, data: bytes) -> str:
    if filename == "application/pdf":
        return pdf_extract_text(BytesIO(data)) or ""
    elif filename == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs)
    elif filename == "text/plain":
        return data.decode("utf-8", errors="replace")
    else:
        raise HTTPException(status_code=415, detail=f"Unsupported file type")
