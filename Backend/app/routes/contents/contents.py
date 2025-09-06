from fastapi import APIRouter
from fastapi import UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from app.LLM.llm import call_agent
from .helpers import extract_text_from_file, MAX_BYTES, ALLOWED, detect_type
contentsRouter = APIRouter(
    prefix="/api/v1",
    tags=["Contents"]
)


@contentsRouter.post('/contents')
async def postContents(job_description: str = Form(...), file: UploadFile = File(...)):

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
