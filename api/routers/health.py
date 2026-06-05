from fastapi import APIRouter
from models.schemas import HealthResponse
from domains.registry import DomainRegistry

router = APIRouter()

@router.get("/", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok", domains_loaded=len(DomainRegistry().all()))
