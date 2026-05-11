import pandas as pd
from gene_set_consensus.scoring import (
    calculate_gtr_utilization_score,
    score_consensus,
)

def test_gtr_utilization_score_caps_at_one():
    row = {
        "targeted_gene_count": 1000,
        "small_panel_count": 1000,
        "medium_panel_count": 1000,
        "large_panel_count": 1000,
        "panel_unsized_count": 1000,
        "unknown_scope_count": 1000,
        "exome_or_genome_count": 1000,
    }
    assert calculate_gtr_utilization_score(row) == 1.0

def test_exome_or_genome_count_does_not_increase_utilization_score():
    exome_only = {
        "targeted_gene_count": 0,
        "small_panel_count": 0,
        "medium_panel_count": 0,
        "large_panel_count": 0,
        "panel_unsized_count": 0,
        "unknown_scope_count": 0,
        "exome_or_genome_count": 1000,
    }
    assert calculate_gtr_utilization_score(exome_only) == 0.0

def test_targeted_gene_support_exceeds_unknown_scope_support():
    targeted = {
        "targeted_gene_count": 1,
        "small_panel_count": 0,
        "medium_panel_count": 0,
        "large_panel_count": 0,
        "panel_unsized_count": 0,
        "unknown_scope_count": 0,
        "exome_or_genome_count": 0,
    }
    unknown = {
        "targeted_gene_count": 0,
        "small_panel_count": 0,
        "medium_panel_count": 0,
        "large_panel_count": 0,
        "panel_unsized_count": 0,
        "unknown_scope_count": 1,
        "exome_or_genome_count": 0,
    }
    assert calculate_gtr_utilization_score(targeted) > calculate_gtr_utilization_score(unknown)

def test_direct_disease_outranks_utilization_plus_exploratory():
    df = pd.DataFrame([
        {
            "phenotype": "epilepsy",
            "gene_id": "G1",
            "gene_symbol": "SCN1A",
            "source_count": 1,
            "weighted_source_sum": 3.0,
            "source_list": "epi25",
            "weight_tier_summary": "gold",
            "evidence_semantics_summary": "statistical_association",
            "evidence_tier_summary": "platinum",
            "semantic_channel_summary": "direct_disease",
            "mapping_status_summary": "resolved",
            "targeted_gene_count": 0,
            "small_panel_count": 0,
            "medium_panel_count": 0,
            "large_panel_count": 0,
            "panel_unsized_count": 0,
            "exome_or_genome_count": 0,
            "unknown_scope_count": 0,
        },
        {
            "phenotype": "epilepsy",
            "gene_id": "G2",
            "gene_symbol": "POLG",
            "source_count": 2,
            "weighted_source_sum": 3.0,
            "source_list": "gtr|genes4epilepsy",
            "weight_tier_summary": "silver|bronze",
            "evidence_semantics_summary": "clinical_utilization|exploratory_literature",
            "evidence_tier_summary": "silver|bronze",
            "semantic_channel_summary": "clinical_utilization|exploratory_literature",
            "mapping_status_summary": "resolved",
            "targeted_gene_count": 100,
            "small_panel_count": 100,
            "medium_panel_count": 100,
            "large_panel_count": 100,
            "panel_unsized_count": 100,
            "exome_or_genome_count": 100,
            "unknown_scope_count": 100,
        },
    ])

    scored = score_consensus(
        df,
        {
            "consensus_score_formula": "weighted_score",
            "minimum_source_count": 1,
            "include_single_source_genes": True,
        },
    )

    direct = scored[scored["gene_symbol"] == "SCN1A"].iloc[0]
    indirect = scored[scored["gene_symbol"] == "POLG"].iloc[0]

    assert float(direct["semantic_consensus_score"]) == 4.0
    assert float(indirect["semantic_consensus_score"]) == 1.75
    assert float(direct["semantic_consensus_score"]) > float(indirect["semantic_consensus_score"])
