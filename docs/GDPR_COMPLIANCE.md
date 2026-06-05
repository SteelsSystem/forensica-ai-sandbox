# GDPR Compliance Architecture

## Data Controller
Your Czech s.r.o. is the GDPR data controller (Art. 4(7)).

## Data Residency — Full Request Path

| Layer | Provider | Location | Sovereignty |
|-------|----------|----------|--------------|
| Primary LLM | Mistral AI | Paris, France | EU-native, GDPR structural |
| Fallback LLM | Scaleway | Paris/Amsterdam | EU-native, EC Cloud III DPS |
| Database | Hetzner/OVHcloud | Germany/France | EU-native, no US parent |
| Cache | Redis (self-hosted) | EU server | You control |

> **Never route LLM calls to `api.openai.com`** from an EU-sovereign deployment.
> EU server location solves data residency but not sovereignty — inference calls send full context to US jurisdiction.

## Legal Bases

| Activity | Basis | Article |
|----------|-------|---------|
| Forensic audit | Legitimate interest / Contract | Art. 6(1)(b)(f) |
| AML screening | Legal obligation | Art. 6(1)(c) |
| Audit log retention | Legal obligation (EU AI Act Art. 12) | Art. 6(1)(c) |
| Authentication | Contract | Art. 6(1)(b) |

## Encryption
All PII encrypted at rest: **AES-256-GCM** with **PBKDF2** key derivation (600,000 iterations).
Satisfies GDPR Art. 32 (appropriate technical measures).

## Data Subject Rights

| Right | Endpoint (planned) | Article |
|-------|--------------------|---------|
| Access | `GET /api/v1/gdpr/export/{subject_id}` | Art. 15 |
| Erasure | `DELETE /api/v1/gdpr/delete/{subject_id}` | Art. 17 |
| Human review | `POST /api/v1/analyze/review/{case_id}` | Art. 22 |

## Audit Log Retention
Logs retained for **84 months** (7 years). EU AI Act Art. 12 requires minimum 6 months.

## EU AI Act Risk Classification

| Risk Tier | Condition | Obligation |
|-----------|-----------|------------|
| Unacceptable | Social scoring, real-time biometric | Prohibited |
| High-risk | Credit scoring, employment, border | Art. 9–15 + EU DB registration |
| Limited-risk | Chatbot, advisory AI | Transparency obligations only |
| Minimal risk | Spam filter, recommender | No mandatory obligations |

This system as research/advisory tool = **Limited Risk** (full applicability: 2 August 2026).
If deployed for automated credit decisions → reclassify to **High-Risk** before market entry.
