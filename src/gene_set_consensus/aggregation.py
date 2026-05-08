import pandas as pd

def _gene_key_columns(df):
    if "gene_id" in df.columns and df["gene_id"].fillna("").ne("").any():
        return ["gene_id", "normalized_gene_symbol"]
    return ["normalized_gene_symbol"]

def build_gene_source_matrix(normalized_df):
    df = normalized_df.copy()
    df["gene_id"] = df["gene_id"].fillna("")
    df["normalized_gene_symbol"] = df["normalized_gene_symbol"].fillna("")
    df["presence"] = 1
    key_cols = ["phenotype", "gene_id", "normalized_gene_symbol"]
    source_order = sorted(df["source_id"].unique().tolist())
    matrix = (
        df.pivot_table(
            index=key_cols,
            columns="source_id",
            values="presence",
            aggfunc="max",
            fill_value=0
        )
        .reset_index()
    )
    for source_id in source_order:
        if source_id not in matrix.columns:
            matrix[source_id] = 0
    matrix = matrix[key_cols + source_order]
    matrix["source_count"] = matrix[source_order].sum(axis=1).astype(int)
    weight_map = df[["source_id", "source_weight"]].drop_duplicates().set_index("source_id")["source_weight"].astype(float).to_dict()
    matrix["weighted_source_sum"] = 0.0
    for source_id in source_order:
        matrix["weighted_source_sum"] += matrix[source_id].astype(float) * float(weight_map[source_id])
    matrix = matrix.sort_values(
        by=["source_count", "weighted_source_sum", "normalized_gene_symbol"],
        ascending=[False, False, True]
    ).reset_index(drop=True)
    return matrix

def build_gene_frequency_table(normalized_df, gene_source_matrix):
    df = normalized_df.copy()
    df["gene_id"] = df["gene_id"].fillna("")
    df["normalized_gene_symbol"] = df["normalized_gene_symbol"].fillna("")
    grouped = (
        df.groupby(["phenotype", "gene_id", "normalized_gene_symbol"], dropna=False)
        .agg(
            source_list=("source_id", lambda x: "|".join(sorted(set(x)))),
            mapping_status_summary=("mapping_status", lambda x: "|".join(sorted(set(x)))),
            weight_tier_summary=("weight_tier", lambda x: "|".join(sorted(set(x)))),
            evidence_semantics_summary=("evidence_semantics", lambda x: "|".join(sorted(set(x)))),
            evidence_tier_summary=("evidence_tier", lambda x: "|".join(sorted(set(x)))),
            semantic_channel_summary=("semantic_channel", lambda x: "|".join(sorted(set(x))))
        )
        .reset_index()
    )
    frequency = gene_source_matrix.merge(
        grouped,
        on=["phenotype", "gene_id", "normalized_gene_symbol"],
        how="left"
    )
    frequency = frequency.rename(columns={"normalized_gene_symbol": "gene_symbol"})
    frequency = frequency[
        [
            "phenotype",
            "gene_id",
            "gene_symbol",
            "source_count",
            "weighted_source_sum",
            "source_list",
            "weight_tier_summary",
            "evidence_semantics_summary",
            "evidence_tier_summary",
            "semantic_channel_summary",
            "mapping_status_summary"
        ]
    ]
    frequency = frequency.sort_values(
        by=["source_count", "weighted_source_sum", "gene_symbol"],
        ascending=[False, False, True]
    ).reset_index(drop=True)
    return frequency
