import pandas as pd
from gene_set_consensus.scoring import score_consensus

def test_consensus_score_equals_weighted_source_sum():
    df = pd.DataFrame([
        {"phenotype": "example", "gene_id": "G1", "gene_symbol": "AAA", "source_count": 2, "weighted_source_sum": 5.0, "source_list": "a|b", "weight_tier_summary": "gold", "mapping_status_summary": "resolved"},
        {"phenotype": "example", "gene_id": "G2", "gene_symbol": "BBB", "source_count": 1, "weighted_source_sum": 2.0, "source_list": "c", "weight_tier_summary": "silver", "mapping_status_summary": "resolved"},
    ])
    scored = score_consensus(df, {"consensus_score_formula": "weighted_score", "minimum_source_count": 1, "include_single_source_genes": True})
    assert float(scored.loc[0, "consensus_score"]) == 5.0
    assert float(scored.loc[1, "consensus_score"]) == 2.0
