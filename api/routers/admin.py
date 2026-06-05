from fastapi import APIRouter, HTTPException
from models.schemas import DomainRegisterInput
from domains.registry import DomainRegistry, Domain

router = APIRouter()

@router.post("/domains/register")
async def register_domain(req: DomainRegisterInput):
    existing = DomainRegistry().get(req.id)
    if existing:
        raise HTTPException(409, f"Domain '{req.id}' already exists.")
    domain = Domain(id=req.id, label=req.label, description=req.description,
                    axiom_set=req.axiom_set, prompt_extra=req.prompt_extra)
    DomainRegistry().register(domain)
    return {"status": "registered", "id": req.id, "label": req.label,
            "message": "Domain live immediately. No restart needed."}
