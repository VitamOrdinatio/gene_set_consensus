import pandas as pd

SUPPORTED_CONSENSUS_FORMULAS = {"weighted_score"}

def score_consensus(frequency_df, scoring_config):
    formula = scoring_config.get("consensus_score_formula")
    if formula not in SUPPORTED_CONSENSUS_FORMULAS:
        raise ValueError(f"Unsupported consensus_score_formula: {formula}")
    df = frequency_df.copy()
    df["source_count"] = df["source_count"].astype(int)
    df["weighted_source_sum"] = df["weighted_source_sum"].astype(float)
    df["consensus_score"] = df["weighted_source_sum"]
    min_source_count = int(scoring_config.get("minimum_source_count", 1))
    include_single_source = bool(scoring_config.get("include_single_source_genes", True))
    if not include_single_source:
        min_source_count = max(min_source_count, 2)
    df = df[df["source_count"] >= min_source_count].copy()
    df = df.sort_values(
        by=["consensus_score", "source_count", "gene_symbol", "gene_id"],
        ascending=[False, False, True, True]
    ).reset_index(drop=True)
    return df
