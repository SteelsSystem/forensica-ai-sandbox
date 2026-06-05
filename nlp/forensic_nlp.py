from __future__ import annotations
import re
from typing import Any

PARAFRAME_TABLE = {
    "under review": "Decision has already been made; review is procedural cover.",
    "enhanced due diligence": "Heightened surveillance applied without cited evidence.",
    "this decision is final": "Appeal right is being pre-emptively denied.",
    "for compliance reasons": "Regulatory language invoked without specific article citation.",
    "cannot disclose": "Evidence is being withheld without legal basis.",
    "policy does not allow": "Internal policy asserted above legal obligation.",
    "in line with regulation": "Vague regulatory claim without article number.",
    "we take your concern seriously": "Acknowledgement substituting substantive response.",
    "our investigation found no wrongdoing": "Self-investigation cited as exculpatory.",
    "standard procedure": "Process presented as inherently legitimate.",
    "not within our remit": "Jurisdiction denial without supporting authority.",
    "subject to review": "Indefinite temporal suspension of rights.",
    "for security purposes": "Security invoked to justify undisclosed restriction.",
    "we are not in a position": "Capability denial masking policy choice.",
    "consistent with our obligations": "Obligations referenced but not cited.",
}

PII_PATTERNS = [
    (r'\b[A-Z]{2}\d{2}[ ]\d{4}[ ]\d{4}[ ]\d{4}[ ]\d{4}[ ]\d{4}[ ]\d{2}\b', "IBAN"),
    (r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', "CARD"),
    (r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', "EMAIL"),
    (r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', "PHONE"),
    (r'\b(\d{1,3}\.){3}\d{1,3}\b', "IP_ADDRESS"),
    (r'\b[A-Z]{2}\d{6,9}\b', "PASSPORT"),
]

CIRCULAR_PATTERNS = [
    (r'(because|since|as) .{3,80} (therefore|thus|hence) .{3,80} (because|since|as)', "Circular reasoning chain"),
    (r'(our investigation|our review) (found|concluded|determined) .{3,60} (our investigation|our review)', "Self-referential investigation"),
    (r'(in accordance with|pursuant to) (this|our|the) (policy|procedure|decision)', "Policy self-reference without external basis"),
]

class ForensicNLP:
    def redact_pii(self, text: str) -> tuple[str, bool]:
        hit = False
        for pattern, label in PII_PATTERNS:
            new = re.sub(pattern, f"[{label}_REDACTED]", text)
            if new != text: hit = True
            text = new
        return text, hit

    def decode_paraframe(self, text: str) -> list[dict[str, str]]:
        hits = []
        lower = text.lower()
        for phrase, decode in PARAFRAME_TABLE.items():
            if phrase in lower:
                hits.append({"phrase": phrase, "decoded": decode})
        return hits

    def detect_circular(self, text: str) -> list[str]:
        return [label for pattern, label in CIRCULAR_PATTERNS
                if re.search(pattern, text, re.IGNORECASE)]

    def loopcycle_verify(self, mind1: str, deep1: str, active_axioms: list[str]) -> dict[str, Any]:
        axioms_in_deep1 = list(set(re.findall(r'\b(A\d{1,2})\b', deep1)))
        activated = [a for a in axioms_in_deep1 if a in active_axioms]
        circular = self.detect_circular(deep1)
        paraframe_hits = self.decode_paraframe(mind1)
        return {
            "activated_axioms": activated,
            "axiom_coverage": f"{len(activated)}/{len(active_axioms)}" if active_axioms else "N/A",
            "circular_reasoning_detected": circular,
            "paraframe_phrases": paraframe_hits,
            "loopcycle_confidence": 0.9 if activated else 0.4,
            "pass": len(circular) == 0 and len(activated) >= (len(active_axioms) // 2 if active_axioms else 0),
        }

    def manipulation_score(self, phrases: list[dict]) -> float:
        return min(1.0, len(phrases) * 0.15)
