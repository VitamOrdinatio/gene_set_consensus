from gene_set_consensus.semantic_ontology import (
    ALLOWED_EVIDENCE_TIERS,
    ALLOWED_SEMANTIC_CHANNELS,
    ALLOWED_EVIDENCE_SEMANTICS,
    validate_semantic_record,
)

def test_expected_semantic_namespaces_are_allowed():
    assert "platinum" in ALLOWED_EVIDENCE_TIERS
    assert "direct_disease" in ALLOWED_SEMANTIC_CHANNELS
    assert "clinical_utilization" in ALLOWED_SEMANTIC_CHANNELS
    assert "statistical_association" in ALLOWED_EVIDENCE_SEMANTICS
    assert "functional_localization" in ALLOWED_EVIDENCE_SEMANTICS

def test_valid_semantic_record_passes():
    record = {
        "evidence_tier_summary": "platinum|silver",
        "semantic_channel_summary": "direct_disease|clinical_utilization",
        "evidence_semantics_summary": "statistical_association|clinical_utilization",
    }
    assert validate_semantic_record(record) == []

def test_unknown_semantic_channel_fails():
    record = {
        "evidence_tier_summary": "silver",
        "semantic_channel_summary": "clinical_use",
        "evidence_semantics_summary": "clinical_utilization",
    }
    errors = validate_semantic_record(record)
    assert any("clinical_use" in error for error in errors)

def test_unknown_evidence_tier_fails():
    record = {
        "evidence_tier_summary": "diamond",
        "semantic_channel_summary": "direct_disease",
        "evidence_semantics_summary": "statistical_association",
    }
    errors = validate_semantic_record(record)
    assert any("diamond" in error for error in errors)
