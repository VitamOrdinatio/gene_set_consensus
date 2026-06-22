import hashlib
import pandas as pd

def make_provenance_id(phenotype, gene_id, gene_symbol):
    payload = f"{phenotype}|{gene_id}|{gene_symbol}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

def build_gene_provenance(normalized_df):
    df = normalized_df.copy()
    df["gene_id"] = df["gene_id"].fillna("")
    df["normalized_gene_symbol"] = df["normalized_gene_symbol"].fillna("")
    df["provenance_id"] = df.apply(
        lambda row: make_provenance_id(
            row["phenotype"],
            row["gene_id"],
            row["normalized_gene_symbol"]
        ),
        axis=1
    )
    keep_cols = [
        "provenance_id",
        "phenotype",

        "source_gene_id",
        "source_gene_namespace",

        "gene_id",
        "gene_namespace",

        "normalized_gene_symbol",

        "source_id",
        "source_name",
        "source_type",
        "source_weight",
        "weight_tier",
        "input_gene_symbol",
        "mapping_status",
        "evidence_label",
        "source_row_number",
        "source_record_hash",
    ]
    out = df[keep_cols].rename(columns={"normalized_gene_symbol": "gene_symbol"})
    out = out.sort_values(
        by=["phenotype", "gene_symbol", "source_id", "source_row_number"],
        ascending=[True, True, True, True]
    ).reset_index(drop=True)
    return out

def attach_provenance_ids(scored_df):
    df = scored_df.copy()
    df["gene_id"] = df["gene_id"].fillna("")
    df["gene_symbol"] = df["gene_symbol"].fillna("")
    df["provenance_id"] = df.apply(
        lambda row: make_provenance_id(
            row["phenotype"],
            row["gene_id"],
            row["gene_symbol"]
        ),
        axis=1
    )
    return df
