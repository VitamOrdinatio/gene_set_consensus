import pandas as pd

from gene_set_consensus.output_validation import validate_outputs

REQUIRED_CONSENSUS_COLUMNS = {
    "gene_symbol",
    "gene_id",
    "consensus_score",
    "semantic_consensus_score",
    "source_count",
    "source_list",
    "evidence_semantics_summary",
    "evidence_tier_summary",
    "semantic_channel_summary",
}

def build_valid_consensus_df():
    return pd.DataFrame([
        {
            "phenotype": "example",
            "gene_id": "ENSG00000144285",
            "gene_symbol": "SCN1A",
            "consensus_score": 3.0,
            "semantic_consensus_score": 4.0,
            "direct_disease_score": 4.0,
            "clinical_interpretation_score": 0.0,
            "contextual_biology_score": 0.0,
            "utilization_score": 0.0,
            "exploratory_score": 0.0,
            "convergence_score": 0.0,
            "conflict_penalty": 0.0,
            "source_count": 1,
            "weighted_source_sum": 3.0,
            "source_list": "epi25",
            "weight_tier_summary": "gold",
            "evidence_semantics_summary": "statistical_association",
            "evidence_tier_summary": "platinum",
            "semantic_channel_summary": "direct_disease",
            "mapping_status_summary": "resolved",
            "scoring_profile": "epilepsy_semantic_v0.1",
            "active_score": "weighted_source_sum",
            "score_explanation": "direct_disease_score=4",
            "provenance_id": "p1",
            "run_id": "run_x",
            "gsc_version": "0.1.0",
            "generated_at": "now",
        }
    ])

def build_valid_provenance_df():
    return pd.DataFrame([
        {
            "provenance_id": "p1",
            "phenotype": "example",
            "gene_id": "ENSG00000144285",
            "gene_symbol": "SCN1A",
            "source_id": "epi25",
            "source_name": "Epi25",
            "source_type": "consortium_wes_burden",
            "source_weight": 3.0,
            "weight_tier": "gold",
            "evidence_semantics": "statistical_association",
            "evidence_tier": "platinum",
            "semantic_channel": "direct_disease",
            "input_gene_symbol": "SCN1A",
            "mapping_status": "resolved",
            "evidence_label": "",
            "source_row_number": 1,
            "source_record_hash": "h1",
        }
    ])

def test_valid_outputs_pass():
    consensus = build_valid_consensus_df()
    provenance = build_valid_provenance_df()
    errors, warnings = validate_outputs(consensus, provenance)
    assert errors == []

def test_forbidden_column_fails():
    consensus = build_valid_consensus_df()
    provenance = build_valid_provenance_df()
    consensus["sample_id"] = "BAD"
    errors, warnings = validate_outputs(consensus, provenance)
    assert any("forbidden" in error for error in errors)

def test_invalid_semantic_channel_fails():
    consensus = build_valid_consensus_df()
    provenance = build_valid_provenance_df()
    consensus.loc[0, "semantic_channel_summary"] = "clinical_use"
    errors, warnings = validate_outputs(consensus, provenance)
    assert any("clinical_use" in error for error in errors)

def test_invalid_evidence_tier_fails():
    consensus = build_valid_consensus_df()
    provenance = build_valid_provenance_df()
    provenance.loc[0, "evidence_tier"] = "diamond"
    errors, warnings = validate_outputs(consensus, provenance)
    assert any("diamond" in error for error in errors)

def test_required_consensus_columns_exist():
    consensus = build_valid_consensus_df()
    missing = REQUIRED_CONSENSUS_COLUMNS - set(consensus.columns)
    assert missing == set()

def test_semantic_scores_are_numeric():
    consensus = build_valid_consensus_df()
    assert pd.api.types.is_numeric_dtype(consensus["consensus_score"])
    assert pd.api.types.is_numeric_dtype(consensus["semantic_consensus_score"])
