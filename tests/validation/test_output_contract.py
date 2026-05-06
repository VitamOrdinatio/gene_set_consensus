import pandas as pd
from gene_set_consensus.output_validation import validate_outputs

def test_forbidden_sample_id_column_fails():
    consensus = pd.DataFrame([{
        "phenotype": "example", "gene_id": "G1", "gene_symbol": "POLG", "consensus_score": "3.0",
        "source_count": "1", "weighted_source_sum": "3.0", "source_list": "a", "weight_tier_summary": "gold",
        "mapping_status_summary": "resolved", "provenance_id": "p1", "run_id": "run_x", "gsc_version": "0.1.0",
        "generated_at": "now", "sample_id": "S1"
    }])
    provenance = pd.DataFrame([{
        "provenance_id": "p1", "phenotype": "example", "gene_id": "G1", "gene_symbol": "POLG",
        "source_id": "a", "source_name": "A", "source_type": "curated", "source_weight": "3.0",
        "weight_tier": "gold", "input_gene_symbol": "POLG", "mapping_status": "resolved",
        "evidence_label": "", "source_row_number": "1", "source_record_hash": "h1"
    }])
    errors, warnings = validate_outputs(consensus, provenance)
    assert any("forbidden" in error for error in errors)
