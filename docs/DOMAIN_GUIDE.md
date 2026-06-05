# Domain Guide

## Built-in Domains

### forensic-legal
Full Lex Forensica v8.0. All 13 axioms. ECHR/CRPD mapping.
Use for: institutional abuse, judicial bias, systemic procedural failures.

### financial
AML, PSD2, MiCA, CNB Czech Act 253/2008. Axioms: A1,A2,A4,A5,A6,A10.
Use for: account restrictions, GDPR Art.15 violations, automated AML decisions.

### science
Research integrity, reproducibility, peer review. Axioms: A2,A3,A4,A5,A8.
Use for: retraction investigations, data withholding, p-hacking detection.

### medical
Diagnostic integrity, iatrogenic harm, CRPD. Axioms: A3,A4,A5,A6,A9,A11,A13.
Use for: psychiatric misdiagnosis, forced treatment, consent violations.

### immigration
Credibility assessment, asylum claims. Axioms: A2,A4,A5,A6,A7,A11,A12.
Use for: asylum refusals, visa denials, COI misrepresentation.

### raw-data
Schema validation, anomaly detection, PII scan. No axioms (structural only).
Use for: database exports, log files, CSV anomalies.

### compliance
GDPR, EU AI Act, AML, MiFID II, DORA gap analysis. Axioms: A2,A4,A5,A6,A10,A12.
Use for: regulatory gap assessment, audit preparation.

### cybersecurity
MITRE ATT&CK, OWASP, incident reconstruction. Axioms: A1,A2,A5,A7.
Use for: incident reports, log analysis, breach investigation.

### contract
Unfair terms (UCTD 93/13/EEC), clause extraction. Axioms: A2,A4,A5,A12.
Use for: consumer contracts, SaaS ToS, B2B clause review.

## Adding a Custom Domain (no restart)

```http
POST /api/v1/admin/domains/register
{
  "id": "environmental-law",
  "label": "Environmental Law",
  "description": "EU ETS, Aarhus Convention, CSRD, ESG violations.",
  "axiom_set": ["A1","A2","A5","A6","A12"],
  "prompt_extra": "You are an environmental law analyst. Map to Aarhus Convention, EU ETS, CSRD, ECHR Art.8."
}
```

To persist across restarts: add to `domains/registry.py` in `DomainRegistry.__new__()`.
