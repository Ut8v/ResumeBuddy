from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Literal
from io import BytesIO
import magic
from docx import Document
from pdfminer.high_level import extract_text as pdf_extract_text
from fastapi.middleware.cors import CORSMiddleware
from app.LLM.llm import call_agent

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    print(filename)
    if filename == "application/pdf":
        return pdf_extract_text(BytesIO(data)) or ""
    elif filename == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs)
    elif filename == "text/plain":
        return data.decode("utf-8", errors="replace")
    else:
        raise HTTPException(status_code=415, detail=f"Unsupported file type")


@app.get('/')
def getCheck():
    return {"OK": True}


@app.post('/contents')
async def postContents(job_description: str, file: UploadFile = File(...)):

    if not file or not file.filename:
        raise HTTPException(
            status_code=400, detail="A resume file is required")

    raw_file = await file.read()

    if len(raw_file) == 0:
        raise HTTPException(status_code=400, detail="Empty File")

    if len(raw_file) > MAX_BYTES:
        raise HTTPException(
            status_code=413, detail="File is too big to process")

    processed_file = detect_type(raw_file)
    print('processed file: ', processed_file)

    if processed_file not in ALLOWED:
        raise HTTPException(
            status_code=415, detail="Only PDF, DOCX or TXT file allowed")

    # Extract the text
    try:
        text = extract_text_from_file(processed_file, raw_file)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to extract text: {str(e)}")

    preview = text[:2000]

    summery = call_agent(text, job_description)

    return JSONResponse({
        "filename": file.filename,
        "characters": len(text),
        "content": preview,
        "truncated": len(text) > len(preview),
        "summery": summery
    })
