"""DomainRegistry — hot-plug topic categories."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional

@dataclass
class Domain:
    id: str
    label: str
    description: str
    axiom_set: list[str]
    prompt_extra: str
    input_schema: Optional[Any] = None
    output_schema: Optional[Any] = None
    enabled: bool = True

FORENSIC_LEGAL = Domain(
    id="forensic-legal", label="Forensic / Legal",
    description="Lex Forensica v8.0. Axioms A1-A13. ECHR/CRPD mapping.",
    axiom_set=["A1","A2","A3","A4","A5","A6","A7","A8","A9","A10","A11","A12","A13"],
    prompt_extra="You are analysing a legal/institutional case under Lex Forensica v8.0. "
        "A1=Forensic Spoliation, A2=Semantic Neutralization, A3=Iatrogenic Attribution, "
        "A4=Epistemic Circularity, A5=Structural Bias, A6=Judicial Abandonment, "
        "A7=Temporal Manipulation, A8=Witness Suppression, A9=Diagnostic Shopping, "
        "A10=Resource Asymmetry, A11=Cultural Erasure, A12=Procedural Entrapment, "
        "A13=Systemic Gaslighting. Map all findings to ECHR articles and CRPD provisions.")

FINANCIAL = Domain(
    id="financial", label="Financial Forensics",
    description="AML, PSD2, MiCA, GDPR Art.15/22. Czech CNB Act 253/2008.",
    axiom_set=["A1","A2","A4","A5","A6","A10"],
    prompt_extra="You are a financial forensic analyst. Flag: account restrictions without "
        "documented evidence (A1), regulatory language without cited articles (A2), "
        "automated decisions without human review right (A5), denial of effective remedy (A6), "
        "resource asymmetry (A10). Map to PSD2, MiCA, GDPR Art.15/22, Czech AML Act 253/2008.")

SCIENCE = Domain(
    id="science", label="Scientific Data Analysis",
    description="Research integrity, reproducibility, statistical validity, peer review.",
    axiom_set=["A2","A3","A4","A5","A8"],
    prompt_extra="You are a scientific integrity analyst. Detect: semantic neutralization of "
        "contradictory results (A2), iatrogenic attribution (A3), epistemic circularity in "
        "experimental design (A4), structural publication bias (A5), suppression of dissenting "
        "findings (A8). Reference COPE Guidelines, ICMJE, statistical reproducibility norms.")

MEDICAL = Domain(
    id="medical", label="Medical / Psychiatric",
    description="Diagnostic integrity, informed consent, CRPD Art.12/17, iatrogenic harm.",
    axiom_set=["A3","A4","A5","A6","A9","A11","A13"],
    prompt_extra="You are a medical forensic analyst. Detect: iatrogenic attribution (A3), "
        "diagnostic shopping (A9), epistemic circularity in clinical notes (A4), systemic "
        "gaslighting of patient reports (A13), cultural erasure in assessment (A11). "
        "Map to CRPD Art.12/17 and informed consent law.")

IMMIGRATION = Domain(
    id="immigration", label="Immigration / Asylum",
    description="Credibility assessment, country-of-origin evidence, procedural fairness.",
    axiom_set=["A2","A4","A5","A6","A7","A11","A12"],
    prompt_extra="You are an immigration case analyst. Detect: credibility assessment circularity "
        "(A4), temporal manipulation (A7), procedural entrapment (A12), cultural erasure (A11), "
        "COI misrepresentation (A2), denial of effective remedy (A6). "
        "Reference UNHCR Handbook, ECHR Art.3/8/13.")

RAW_DATA = Domain(
    id="raw-data", label="Raw Data Inspection",
    description="Schema validation, anomaly detection, statistical profiling, PII scan.",
    axiom_set=[],
    prompt_extra="You are a data quality and forensic inspection engine. Identify: schema "
        "violations, null/missing value patterns, statistical outliers (Z-score >3), duplicate "
        "records, PII tokens (email, IBAN, passport, IP), temporal inconsistencies. "
        "Return structured JSON with field-level findings. Do NOT interpret meaning.")

COMPLIANCE = Domain(
    id="compliance", label="Regulatory Compliance",
    description="GDPR, EU AI Act, AML, MiFID II, MiCA, DORA gap analysis.",
    axiom_set=["A2","A4","A5","A6","A10","A12"],
    prompt_extra="You are a EU regulatory compliance analyst. Detect gaps against: GDPR "
        "(Art.5/6/13/15/17/22/32), EU AI Act risk tiers, AML/CFT (FATF, 6AMLD), MiFID II "
        "suitability, MiCA CASP obligations, DORA ICT risk. For each gap: cite specific "
        "article, observed violation, and required remediation action.")

CYBERSECURITY = Domain(
    id="cybersecurity", label="Cybersecurity / Incident",
    description="OWASP, ATT&CK, MITRE mapping, incident chain reconstruction.",
    axiom_set=["A1","A2","A5","A7"],
    prompt_extra="You are a cybersecurity incident analyst. Map to MITRE ATT&CK tactics. "
        "Reconstruct attack chains chronologically. Detect: evidence spoliation in log gaps (A1), "
        "semantic neutralization of severity (A2), temporal manipulation (A7). Flag OWASP "
        "Top-10 and OWASP LLM Top-10. Output: TTP list, timeline, IOC extraction, containment.")

CONTRACT = Domain(
    id="contract", label="Contract Analysis",
    description="Clause extraction, unfair terms (UCTD 93/13/EEC), obligation mapping.",
    axiom_set=["A2","A4","A5","A12"],
    prompt_extra="You are a contract forensic analyst. Extract: all obligations, termination, "
        "liability limits, penalties, jurisdiction. Flag unfair terms under EU Directive "
        "93/13/EEC, procedural entrapment (A12), asymmetric obligations (A5), circular "
        "definition traps (A4). Rate each clause: FAIR / QUESTIONABLE / UNFAIR.")

class DomainRegistry:
    _instance: 'DomainRegistry | None' = None
    def __new__(cls) -> 'DomainRegistry':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._domains: dict[str, Domain] = {}
            for d in [FORENSIC_LEGAL, FINANCIAL, SCIENCE, MEDICAL,
                      IMMIGRATION, RAW_DATA, COMPLIANCE, CYBERSECURITY, CONTRACT]:
                cls._instance._domains[d.id] = d
        return cls._instance
    def get(self, domain_id: str) -> 'Domain | None': return self._domains.get(domain_id)
    def all(self) -> list[Domain]: return [d for d in self._domains.values() if d.enabled]
    def register(self, domain: Domain) -> None: self._domains[domain.id] = domain
    def disable(self, domain_id: str) -> None:
        if domain_id in self._domains: self._domains[domain_id].enabled = False
