from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging_config import AppLogger
from app.api.routes.health import router as health_router
from app.api.routes.logs import router as logs_router
from app.api.routes.rag import router as rag_router


# configure logging early so other imports log correctly
AppLogger.configure(settings.log_file)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)

# Enable CORS for the frontend Vite server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(logs_router)
app.include_router(rag_router)
