from fastapi import FastAPI

from app.core.config import settings
from app.core.logging_config import configure_logging
from app.api.routes.health import router as health_router
from app.api.routes.logs import router as logs_router


# configure logging early so other imports log correctly
configure_logging(settings.log_file)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)

app.include_router(health_router)
app.include_router(logs_router)