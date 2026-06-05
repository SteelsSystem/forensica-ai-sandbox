from __future__ import annotations
import json, logging, re
from core.llm_provider import ProviderRegistry, PipelinePhase
from domains.registry import DomainRegistry, Domain
from pipeline.prompts import BASE_SYSTEM_MIND1, BASE_SYSTEM_DEEP1, BASE_SYSTEM_DEFENSE
from nlp.forensic_nlp import ForensicNLP
from models.schemas import UniversalAnalysisInput, AnalysisResponse, AnalysisPhaseResult

logger = logging.getLogger(__name__)

def _build_sys(template: str, domain: Domain) -> str:
    return template.format(domain_extra=domain.prompt_extra)

def _extract_axioms(text: str) -> list[str]:
    return list(set(re.findall(r'\b(A\d{1,2})\b', text)))

def _risk_score(axioms: list[str]) -> float:
    weights = {"A1":0.9,"A2":0.7,"A3":0.8,"A4":0.75,"A5":0.8,"A6":0.9,"A7":0.65,
               "A8":0.7,"A9":0.75,"A10":0.6,"A11":0.55,"A12":0.8,"A13":0.85}
    if not axioms: return 0.0
    return min(1.0, sum(weights.get(a, 0.5) for a in axioms) / len(axioms))

class UniversalAnalysisEngine:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._llm = ProviderRegistry()
            cls._instance._domains = DomainRegistry()
            cls._instance._nlp = ForensicNLP()
        return cls._instance

    async def analyse(self, req: UniversalAnalysisInput) -> AnalysisResponse:
        domain = self._domains.get(req.domain) or self._domains.get("forensic-legal")
        pii_hit = False
        a = req.input_a; b = req.input_b
        if req.enable_pii_redaction:
            a, hit_a = self._nlp.redact_pii(a)
            b, hit_b = self._nlp.redact_pii(b)
            pii_hit = hit_a or hit_b

        mind1_out = await self._llm.complete([
            {"role":"system","content":_build_sys(BASE_SYSTEM_MIND1, domain)},
            {"role":"user","content":f"INPUT_A (institutional):\n{a}\n\nINPUT_B (subject):\n{b}"}
        ], PipelinePhase.MIND1)
        mind1 = AnalysisPhaseResult(phase="MIND1", raw_output=mind1_out,
            axioms_triggered=[], findings=[mind1_out[:500]], confidence=0.8)

        deep1_out = await self._llm.complete([
            {"role":"system","content":_build_sys(BASE_SYSTEM_DEEP1, domain)},
            {"role":"user","content":f"FRAMES FROM MIND1:\n{mind1_out}\n\nACTIVE AXIOMS: {domain.axiom_set}"}
        ], PipelinePhase.DEEP1)
        d1_axioms = _extract_axioms(deep1_out)
        deep1 = AnalysisPhaseResult(phase="DEEP1", raw_output=deep1_out,
            axioms_triggered=d1_axioms, findings=[deep1_out[:500]], confidence=0.85)

        loop = self._nlp.loopcycle_verify(mind1_out, deep1_out, domain.axiom_set)

        defense_out = await self._llm.complete([
            {"role":"system","content":_build_sys(BASE_SYSTEM_DEFENSE, domain)},
            {"role":"user","content":f"DEEP1 FINDINGS:\n{deep1_out}\n\nLOOPCYCLE:\n{json.dumps(loop)}"}
        ], PipelinePhase.DEFENSE)
        defense = AnalysisPhaseResult(phase="DEFENSE", raw_output=defense_out,
            axioms_triggered=_extract_axioms(defense_out),
            findings=[defense_out[:500]], confidence=0.82)

        all_axioms = list(set(d1_axioms + defense.axioms_triggered))
        return AnalysisResponse(
            case_id=req.case_id, domain=req.domain,
            mind1=mind1, deep1=deep1, loopcycle=loop, defense=defense,
            risk_score=_risk_score(all_axioms), flagged_axioms=all_axioms,
            pii_redacted=pii_hit)
