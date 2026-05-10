import pandas as pd
from gene_set_consensus.scoring import score_consensus

def test_consensus_score_equals_weighted_source_sum():
    df = pd.DataFrame([
        {
            "phenotype": "example",
            "gene_id": "G1",
            "gene_symbol": "AAA",
            "source_count": 2,
            "weighted_source_sum": 5.0,
            "source_list": "a|b",
            "weight_tier_summary": "gold",
            "evidence_semantics_summary": "clinical_utilization|contextual_biology",
            "evidence_tier_summary": "gold|silver",
            "semantic_channel_summary": "clinical_utilization|contextual_biology",
            "mapping_status_summary": "resolved",
        },
        {
            "phenotype": "example",
            "gene_id": "G2",
            "gene_symbol": "BBB",
            "source_count": 1,
            "weighted_source_sum": 2.0,
            "source_list": "c",
            "weight_tier_summary": "silver",
            "evidence_semantics_summary": "clinical_utilization",
            "evidence_tier_summary": "silver",
            "semantic_channel_summary": "clinical_utilization",
            "mapping_status_summary": "resolved",
        },
    ])
    scored = score_consensus(df, {"consensus_score_formula": "weighted_score", "minimum_source_count": 1, "include_single_source_genes": True})
    assert float(scored.loc[0, "consensus_score"]) == 5.0
    assert float(scored.loc[1, "consensus_score"]) == 2.0

def test_semantic_channel_scores_are_emitted_without_replacing_legacy_score():
    df = pd.DataFrame([
        {
            "phenotype": "example",
            "gene_id": "G1",
            "gene_symbol": "POLG",
            "source_count": 2,
            "weighted_source_sum": 5.0,
            "source_list": "gtr|mitocarta",
            "weight_tier_summary": "gold|silver",
            "evidence_semantics_summary": "clinical_utilization|functional_localization",
            "evidence_tier_summary": "gold|silver",
            "semantic_channel_summary": "clinical_utilization|contextual_biology",
            "mapping_status_summary": "resolved",
        }
    ])
    scored = score_consensus(df, {"consensus_score_formula": "weighted_score", "minimum_source_count": 1, "include_single_source_genes": True})
    row = scored.iloc[0]
    assert float(row["consensus_score"]) == 5.0
    assert float(row["contextual_biology_score"]) == 2.0
    assert float(row["utilization_score"]) == 1.0
    assert float(row["semantic_consensus_score"]) == 3.0
    assert row["active_score"] == "weighted_source_sum"
