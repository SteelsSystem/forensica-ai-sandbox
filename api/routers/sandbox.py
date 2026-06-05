from fastapi import APIRouter
from models.schemas import SandboxClassifyInput, SandboxClassifyResponse
from sandbox.security_engine import SandboxSecurityEngine

router = APIRouter()

@router.post("/sandbox/classify", response_model=SandboxClassifyResponse)
async def sandbox_classify(req: SandboxClassifyInput):
    return await SandboxSecurityEngine().classify(req)
