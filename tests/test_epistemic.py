import hashlib

from nlp.epistemic import (
    build_input_provenance,
    evaluate_synthesis_gate,
    sha256_text,
)


def test_sha256_is_over_exact_utf8_input():
    value = "Důkaz / evidence"
    assert sha256_text(value) == hashlib.sha256(value.encode("utf-8")).hexdigest()


def test_provenance_never_claims_authenticity():
    record = build_input_provenance("institutional text", "subject text")
    assert record["input_a"]["authenticity"] == "UNVERIFIED"
    assert record["input_b"]["authenticity"] == "UNVERIFIED"
    assert any("does not establish" in item for item in record["limitations"])


def test_gate_requires_explicit_boolean_true():
    assert evaluate_synthesis_gate({"pass": True})["allowed"] is True
    assert evaluate_synthesis_gate({"pass": False})["allowed"] is False
    assert evaluate_synthesis_gate({})["allowed"] is False
    assert evaluate_synthesis_gate({"pass": "true"})["allowed"] is False


def test_allowed_synthesis_is_not_certification():
    result = evaluate_synthesis_gate({"pass": True})
    assert result["certification"] == "NOT_CERTIFIED"
