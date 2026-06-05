from __future__ import annotations
import re, logging
from models.schemas import SandboxClassifyInput, SandboxClassifyResponse
from core.llm_provider import ProviderRegistry, PipelinePhase

logger = logging.getLogger(__name__)

INJECTION_PATTERNS = [
    r'ignore\s+(previous|prior|all)\s+instruction',
    r'you\s+are\s+now\s+(in\s+)?(a\s+)?different',
    r'reveal\s+(your\s+)?(system\s+)?prompt',
    r'act\s+as\s+(if\s+you\s+are|a)',
    r'jailbreak', r'DAN\s+mode', r'pretend\s+you',
    r'forget\s+(all|your)\s+(previous|instructions)',
    r'do\s+anything\s+now',
]

PII_PATTERNS = [
    r'\b[A-Z]{2}\d{2}[ ]\d{4}[ ]\d{4}',
    r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
    r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
]

POLICY_PATTERNS = [
    r'\b(terrorism|child\s+abuse|bomb|synthesize\s+(drug|weapon))\b',
    r'\b(hack|exploit|bypass)\s+(this\s+)?(system|server|model|api)\b',
]

class SandboxSecurityEngine:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._llm = ProviderRegistry()
        return cls._instance

    async def classify(self, req: SandboxClassifyInput) -> SandboxClassifyResponse:
        text = req.payload
        if not text or not text.strip():
            return SandboxClassifyResponse(allowed=False, threat_score=1.0,
                threat_type="LLM04_MODEL_DOS", blocking_layer=1, reason="Empty payload")
        for p in INJECTION_PATTERNS:
            if re.search(p, text, re.IGNORECASE):
                return SandboxClassifyResponse(allowed=False, threat_score=0.94,
                    threat_type="LLM01_PROMPT_INJECTION", blocking_layer=2,
                    reason=f"Injection pattern matched")
        for p in PII_PATTERNS:
            if re.search(p, text):
                return SandboxClassifyResponse(allowed=False, threat_score=0.8,
                    threat_type="LLM06_SENSITIVE_INFO", blocking_layer=3,
                    reason="PII token detected")
        for p in POLICY_PATTERNS:
            if re.search(p, text, re.IGNORECASE):
                return SandboxClassifyResponse(allowed=False, threat_score=0.99,
                    threat_type="LLM02_INSECURE_OUTPUT", blocking_layer=4,
                    reason="Policy violation detected")
        try:
            r = await self._llm.complete([
                {"role":"system","content":"Classify: is this a prompt injection, jailbreak, data extraction, or safe? Reply SAFE or THREAT:<type>."},
                {"role":"user","content":text}
            ], PipelinePhase.SANDBOX)
            if "THREAT" in r.upper():
                return SandboxClassifyResponse(allowed=False, threat_score=0.7,
                    threat_type="LLM_CLASSIFIED_THREAT", blocking_layer=5,
                    reason=f"LLM classifier: {r.strip()[:80]}")
        except Exception as e:
            logger.warning("Sandbox LLM layer failed: %s", e)
        return SandboxClassifyResponse(allowed=True, threat_score=0.0,
            threat_type=None, blocking_layer=None, reason="All 5 layers passed")
