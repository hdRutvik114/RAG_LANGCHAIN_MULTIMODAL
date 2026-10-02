from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse
from pathlib import Path
from typing import Optional

from app.api.dependencies import get_settings
from app.core.config import Settings


router = APIRouter()


@router.get("/logs", response_class=PlainTextResponse)
def get_logs(lines: int = Query(200, ge=1, le=10000), config: Settings = Depends(get_settings)):
    """Return the last `lines` lines from the application log file.

    Only allowed when `environment` is `development` to avoid exposing logs in production.
    """
    if config.environment.lower() != "development":
        raise HTTPException(status_code=403, detail="Log access is disabled in this environment")

    log_path = Path(config.log_file)
    if not log_path.exists():
        raise HTTPException(status_code=404, detail="Log file not found")

    # read last N lines efficiently
    def tail(path: Path, n: int):
        avg_line_size = 150
        to_read = n * avg_line_size
        with path.open("rb") as f:
            try:
                f.seek(-to_read, 2)
            except OSError:
                f.seek(0)
            data = f.read().decode("utf-8", errors="replace")
        lines = data.splitlines()
        return "\n".join(lines[-n:])

    content = tail(log_path, lines)
    return PlainTextResponse(content)
