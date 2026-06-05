# Architecture

## Pipeline: MIND1 → DEEP1 → LOOPCYCLE → DEFENSE

```
                 ┌─────────────────────────────────────────────┐
                 │           UniversalAnalysisEngine            │
                 │                                              │
input_a ──┬       │  ┌──────┐   ┌──────┐   ┌──────────┐  ┌─────────┐
           ├────►│  │MIND1 │──►│DEEP1 │──►│LOOPCYCLE │─►│ DEFENSE  │
input_b ──┘       │  │(fast)│   │(deep)│   │(NLP,prog)│  │ (deep)   │
                 │  └──────┘   └──────┘   └──────────┘  └─────────┘
domain ─────────►│              ↑                ↑                     │
                 │        domain.axiom_set  domain.prompt_extra        │
                 └─────────────────────────────────────────────┘
```

## Singleton Init Order

```
S1: ProviderRegistry        ← Mistral (primary) + Scaleway (fallback)
S2: DomainRegistry          ← 9 built-in domains + runtime registration
S3: UniversalAnalysisEngine ← depends on S1 + S2
S4: SandboxSecurityEngine   ← depends on S1 (layer 5)
S5: ForensicNLP             ← stateless, safe to lazy-init
```

## O-Gate Security Pipeline

```
Input → [L1: Empty?] → [L2: Injection regex] → [L3: PII detector]
       → [L4: Policy/toxic regex] → [L5: LLM classifier] → ALLOW/BLOCK
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/v1/analyze/ | Universal analysis (all domains) |
| GET  | /api/v1/domains/ | List all registered domains |
| GET  | /api/v1/domains/{id} | Domain detail + prompt_extra |
| POST | /api/v1/sandbox/classify | O-Gate OWASP LLM Top-10 check |
| POST | /api/v1/paraframe/decode | PARAFRAME institutional phrase decode |
| POST | /api/v1/admin/domains/register | Register new domain at runtime |
| GET  | /health/ | Health + domain count |
