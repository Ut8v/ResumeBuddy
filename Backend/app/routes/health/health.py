from fastapi import APIRouter
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
import time
from app.configs.config import settings

healthRouter = APIRouter(
    prefix="/api/v1", tags=["Health"]
)

_started = time.monotonic()


@healthRouter.get("/health")
async def health():
    return JSONResponse(
        {
            "status": "OK",
            "time_utc": datetime.now(timezone.utc).isoformat(),
            "uptime_seconds": round(time.monotonic() - _started, 2),
        }
    )


@healthRouter.get("/health/ready")
async def ready():
    checks = {"config_openai_key": bool(
        getattr(settings, "OPENAI_API_KEY", ""))}
    failing = {k: v for k, v in checks.items() if not v}
    ok = not failing
    body = {"status": "ok" if ok else "degraded"}
    if not ok:
        body["checks"] = failing
    return JSONResponse(body, status_code=200 if ok else 503)
