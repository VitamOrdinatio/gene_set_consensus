import math
import pandas as pd

SUPPORTED_CONSENSUS_FORMULAS = {"weighted_score"}
SEMANTIC_SCORE_COLUMNS = {
    "direct_disease": "direct_disease_score",
    "clinical_interpretation": "clinical_interpretation_score",
    "contextual_biology": "contextual_biology_score",
    "clinical_utilization": "utilization_score",
    "exploratory_literature": "exploratory_score",
    "convergence": "convergence_score",
}

DEFAULT_CHANNEL_VALUES = {
    "direct_disease_score": 4.0,
    "clinical_interpretation_score": 3.0,
    "contextual_biology_score": 2.0,
    "utilization_score": 1.0,
    "exploratory_score": 0.75,
    "convergence_score": 1.5,
}

def _split_pipe(value):
    return [x.strip() for x in str(value).split("|") if x.strip()]

def _safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0

def calculate_gtr_utilization_score(row):
    weighted_panel_support = (
        _safe_float(row.get("targeted_gene_count", 0)) * 1.00
        + _safe_float(row.get("small_panel_count", 0)) * 0.75
        + _safe_float(row.get("medium_panel_count", 0)) * 0.50
        + _safe_float(row.get("large_panel_count", 0)) * 0.25
        + _safe_float(row.get("panel_unsized_count", 0)) * 0.10
        + _safe_float(row.get("unknown_scope_count", 0)) * 0.05
        + _safe_float(row.get("exome_or_genome_count", 0)) * 0.00
    )
    return min(1.0, math.log2(1.0 + weighted_panel_support))

def _semantic_scores_from_summary(row):
    scores = {column: 0.0 for column in DEFAULT_CHANNEL_VALUES}
    channels = _split_pipe(row.get("semantic_channel_summary", ""))
    for channel in channels:
        score_column = SEMANTIC_SCORE_COLUMNS.get(channel)
        if score_column:
            if channel == "clinical_utilization":
                scores[score_column] = calculate_gtr_utilization_score(row)
            else:
                scores[score_column] = DEFAULT_CHANNEL_VALUES[score_column]
    return scores

def _make_score_explanation(row):
    parts = []
    for column in DEFAULT_CHANNEL_VALUES:
        value = float(row.get(column, 0.0))
        if value > 0:
            parts.append(f"{column}={value:g}")
    if not parts:
        parts.append("no_semantic_score")
    return ";".join(parts)

def score_consensus(frequency_df, scoring_config):
    formula = scoring_config.get("consensus_score_formula")
    if formula not in SUPPORTED_CONSENSUS_FORMULAS:
        raise ValueError(f"Unsupported consensus_score_formula: {formula}")

    df = frequency_df.copy()
    df["source_count"] = df["source_count"].astype(int)
    df["weighted_source_sum"] = df["weighted_source_sum"].astype(float)

    for column in DEFAULT_CHANNEL_VALUES:
        df[column] = 0.0

    if "semantic_channel_summary" in df.columns:
        semantic_rows = df.apply(_semantic_scores_from_summary, axis=1)
        for idx, score_dict in semantic_rows.items():
            for column, value in score_dict.items():
                df.at[idx, column] = value

    df["conflict_penalty"] = 0.0
    df["semantic_consensus_score"] = (
        df["direct_disease_score"].astype(float)
        + df["clinical_interpretation_score"].astype(float)
        + df["contextual_biology_score"].astype(float)
        + df["utilization_score"].astype(float)
        + df["exploratory_score"].astype(float)
        + df["convergence_score"].astype(float)
        - df["conflict_penalty"].astype(float)
    ).clip(lower=0.0)

    active_score = scoring_config.get(
        "active_score",
        "weighted_source_sum"
    )

    if active_score not in {
        "weighted_source_sum",
        "semantic_consensus_score",
    }:
        raise ValueError(
            f"Unsupported active_score: {active_score}"
        )

    df["active_score"] = active_score
    df["scoring_profile"] = scoring_config.get("scoring_profile", "")

    if active_score == "semantic_consensus_score":
        df["consensus_score"] = df["semantic_consensus_score"]
    else:
        df["consensus_score"] = df["weighted_source_sum"]

    df["score_explanation"] = df.apply(_make_score_explanation, axis=1)

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
