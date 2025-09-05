import io
from fastapi import HTTPException


def _files_bytes(name="resume.pdf", data=b"%PDF-1.4\n..."):
    return {"file": (name, io.BytesIO(data), "application/pdf")}


def test_success_happy_path(client, monkeypatch):
    import app.main as main_mod

    monkeypatch.setattr(main_mod, "detect_type",
                        lambda _raw: "application/pdf")
    extracted = "A" * 2500
    monkeypatch.setattr(main_mod, "extract_text_from_file",
                        lambda _mt, _raw: extracted)
    monkeypatch.setattr(main_mod, "call_agent",
                        lambda text, jd: "# ATS Report\nOK")

    monkeypatch.setattr(main_mod, "ALLOWED", {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
    }, raising=True)

    files = _files_bytes()
    r = client.post(
        "/contents", params={"job_description": "React/Node role"}, files=files)

    assert r.status_code == 200, r.text
    body = r.json()
    assert body["filename"] == "resume.pdf"
    assert body["characters"] == len(extracted)
    assert body["content"] == extracted[:2000]
    assert body["truncated"] is True
    assert body["summery"].startswith("# ATS Report")


def test_missing_file_returns_422(client):
    r = client.post("/contents", params={"job_description": "JD text"})
    assert r.status_code == 422


def test_missing_job_description_returns_422(client):
    files = _files_bytes()
    r = client.post("/contents", files=files)
    assert r.status_code == 422


def test_empty_file_returns_400(client, monkeypatch):
    import app.main as main_mod
    files = {"file": ("resume.pdf", io.BytesIO(b""), "application/pdf")}
    r = client.post("/contents", params={"job_description": "JD"}, files=files)
    assert r.status_code == 400
    assert r.json()["detail"] == "Empty File"


def test_too_large_returns_413(client, monkeypatch):
    import app.main as main_mod
    monkeypatch.setattr(main_mod, "MAX_BYTES", 10, raising=True)
    big = b"X" * 11
    files = _files_bytes(data=big)
    r = client.post("/contents", params={"job_description": "JD"}, files=files)
    assert r.status_code == 413
    assert r.json()["detail"] == "File is too big to process"


def test_unsupported_type_returns_415(client, monkeypatch):
    import app.main as main_mod
    monkeypatch.setattr(main_mod, "detect_type", lambda _raw: "image/png")
    monkeypatch.setattr(main_mod, "ALLOWED", {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
    }, raising=True)

    files = _files_bytes()
    r = client.post("/contents", params={"job_description": "JD"}, files=files)
    assert r.status_code == 415
    assert r.json()["detail"] == "Only PDF, DOCX or TXT file allowed"


def test_extractor_http_exception_propagates(client, monkeypatch):
    import app.main as main_mod
    monkeypatch.setattr(main_mod, "detect_type",
                        lambda _raw: "application/pdf")

    def boom_http(_mt, _raw):
        raise HTTPException(status_code=422, detail="Cannot parse")
    monkeypatch.setattr(main_mod, "extract_text_from_file", boom_http)

    files = _files_bytes()
    r = client.post("/contents", params={"job_description": "JD"}, files=files)
    assert r.status_code == 422
    assert r.json()["detail"] == "Cannot parse"


def test_extractor_generic_exception_returns_500(client, monkeypatch):
    import app.main as main_mod
    monkeypatch.setattr(main_mod, "detect_type",
                        lambda _raw: "application/pdf")

    def boom_generic(_mt, _raw):
        raise Exception("unexpected failure")
    monkeypatch.setattr(main_mod, "extract_text_from_file", boom_generic)

    files = _files_bytes()
    r = client.post("/contents", params={"job_description": "JD"}, files=files)
    assert r.status_code == 500
    assert r.json()["detail"].startswith(
        "Failed to extract text: unexpected failure")
