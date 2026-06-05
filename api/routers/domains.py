from fastapi import APIRouter, HTTPException
from domains.registry import DomainRegistry

router = APIRouter()

@router.get("/domains/")
async def list_domains():
    return [{"id":d.id,"label":d.label,"description":d.description,
             "axiom_set":d.axiom_set,"enabled":d.enabled}
            for d in DomainRegistry().all()]

@router.get("/domains/{domain_id}")
async def get_domain(domain_id: str):
    d = DomainRegistry().get(domain_id)
    if not d: raise HTTPException(404, f"Domain not found: {domain_id}")
    return {"id":d.id,"label":d.label,"description":d.description,
            "axiom_set":d.axiom_set,"prompt_extra":d.prompt_extra,"enabled":d.enabled}
