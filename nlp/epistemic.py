"""Deterministic epistemic controls.

Hashes bind records to the bytes observed by this process. They do not prove
source authenticity, authorship, completeness, or the truth of a claim.
"""
from __future__ import annotations

import hashlib
from typing import Any


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def build_input_provenance(input_a: str, input_b: str) -> dict[str, Any]:
    return {
        "algorithm": "sha256",
        "scope": "exact UTF-8 input strings received by the API",
        "input_a": {
            "channel": "institutional_or_dataset_a",
            "sha256": sha256_text(input_a),
            "byte_length": len(input_a.encode("utf-8")),
            "authenticity": "UNVERIFIED",
        },
        "input_b": {
            "channel": "subject_or_dataset_b",
            "sha256": sha256_text(input_b),
            "byte_length": len(input_b.encode("utf-8")),
            "authenticity": "UNVERIFIED",
        },
        "limitations": [
            "A digest detects later byte changes only when compared with a trusted digest.",
            "A digest does not establish authorship, authenticity, completeness, or factual truth.",
            "Channel labels describe API field assignment, not independently verified source identity.",
        ],
    }


def evaluate_synthesis_gate(loop_result: dict[str, Any]) -> dict[str, Any]:
    """Permit draft synthesis only after an explicit successful verifier result."""
    passed = loop_result.get("pass") is True
    if passed:
        return {
            "decision": "ALLOW_PROVISIONAL_SYNTHESIS",
            "allowed": True,
            "certification": "NOT_CERTIFIED",
            "reason": "Deterministic LOOPCYCLE result explicitly passed; factual claims remain unverified.",
        }
    return {
        "decision": "BLOCK_UNRESOLVED",
        "allowed": False,
        "certification": "NOT_CERTIFIED",
        "reason": "LOOPCYCLE did not explicitly pass; defense synthesis is blocked.",
    }
