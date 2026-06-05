# Contributing

## Adding a New Domain

The fastest way to add a new topic category is the runtime API — no code changes needed:

```http
POST /api/v1/admin/domains/register
{
  "id": "your-domain-id",
  "label": "Human Readable Name",
  "description": "One-line description.",
  "axiom_set": ["A1", "A5"],
  "prompt_extra": "You are a [role] analyst. Detect [patterns]. Map to [legal refs]."
}
```

To persist across restarts, add to `domains/registry.py` in `DomainRegistry.__new__()`.

## Prompt Engineering Guidelines

`prompt_extra` is injected into all three LLM phases (MIND1, DEEP1, DEFENSE). Write it to work as both a tokenisation instruction and an analysis lens.

## Running Tests

```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```

## Code Style

- Python 3.12+, type hints everywhere
- Pydantic v2 for all data contracts
- Singletons for all stateful components
- No hardcoded secrets — all config via `config/settings.py` from `.env`
