import pytest
from domains.registry import DomainRegistry, Domain

def test_all_domains_loaded():
    reg = DomainRegistry()
    ids = [d.id for d in reg.all()]
    for expected in ["forensic-legal","financial","science","medical","immigration",
                     "raw-data","compliance","cybersecurity","contract"]:
        assert expected in ids, f"Missing domain: {expected}"

def test_get_domain():
    d = DomainRegistry().get("financial")
    assert d is not None
    assert "A1" in d.axiom_set
    assert "PSD2" in d.prompt_extra

def test_runtime_register():
    reg = DomainRegistry()
    reg.register(Domain(id="test-env", label="Test Environmental",
        description="Test domain", axiom_set=["A1","A2"], prompt_extra="Test."))
    d = reg.get("test-env")
    assert d is not None
    assert d.label == "Test Environmental"

def test_registry_singleton():
    assert DomainRegistry() is DomainRegistry()

def test_raw_data_no_axioms():
    assert DomainRegistry().get("raw-data").axiom_set == []

def test_science_axioms():
    d = DomainRegistry().get("science")
    assert "A2" in d.axiom_set and "A8" in d.axiom_set

def test_disable_domain():
    reg = DomainRegistry()
    reg.register(Domain(id="temp-domain", label="Temp", description="", axiom_set=[], prompt_extra=""))
    reg.disable("temp-domain")
    assert "temp-domain" not in [d.id for d in reg.all()]
