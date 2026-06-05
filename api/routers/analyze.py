from fastapi import APIRouter, HTTPException
from models.schemas import UniversalAnalysisInput, AnalysisResponse
from pipeline.engine import UniversalAnalysisEngine
from domains.registry import DomainRegistry

router = APIRouter()

@router.post("/analyze/", response_model=AnalysisResponse)
async def analyze(req: UniversalAnalysisInput):
    if not DomainRegistry().get(req.domain):
        raise HTTPException(400, f"Unknown domain: {req.domain}. GET /api/v1/domains/ for valid IDs.")
    try:
        return await UniversalAnalysisEngine().analyse(req)
    except Exception as e:
        raise HTTPException(500, f"Analysis failed: {str(e)}")
