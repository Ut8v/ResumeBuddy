from app.main import app
import os
import pytest
from fastapi.testclient import TestClient
from app.configs.config import settings

os.environ.setdefault("OPENAI_API_KEY", "test")
os.environ.setdefault("OPENAI_MODEL", "gpt-4.1-mini")
os.environ.setdefault("MAX_OPENAI_TOKENS", "800")
os.environ.setdefault("MAX_FILE_MB", "3")


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
