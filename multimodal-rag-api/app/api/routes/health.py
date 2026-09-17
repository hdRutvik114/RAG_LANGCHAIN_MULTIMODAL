from fastapi import APIRouter, Depends

from app.api.dependencies import get_settings
from app.core.config import Settings


router = APIRouter()


@router.get("/health")
def health_check(config: Settings = Depends(get_settings)):
    return {
        "status": "healthy",
        "environment": config.environment,
    }