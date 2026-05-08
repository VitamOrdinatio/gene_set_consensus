FORBIDDEN_GSC_COLUMNS = {
    "sample_id",
    "variant_id",
    "zygosity",
    "chrom",
    "pos",
    "ref",
    "alt",
    "rdgp_score",
}

REQUIRED_CONSENSUS_COLUMNS = [
    "phenotype",
    "gene_id",
    "gene_symbol",
    "consensus_score",
    "source_count",
    "weighted_source_sum",
    "source_list",
    "weight_tier_summary",
    "evidence_semantics_summary",
    "evidence_tier_summary",
    "semantic_channel_summary",
    "mapping_status_summary",
    "provenance_id",
    "run_id",
    "gsc_version",
    "generated_at",
]

REQUIRED_PROVENANCE_COLUMNS = [
    "provenance_id",
    "phenotype",
    "gene_id",
    "gene_symbol",
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

def validate_required_columns(df, required_columns, table_name):
    errors = []
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        errors.append(f"{table_name} missing required columns: {missing}")
    return errors

def validate_forbidden_columns(df, table_name):
    errors = []
    forbidden = sorted(FORBIDDEN_GSC_COLUMNS.intersection(set(df.columns)))
    if forbidden:
        errors.append(f"{table_name} contains forbidden GSC columns: {forbidden}")
    return errors

def validate_consensus_identity(consensus_df):
    errors = []
    with_gene_id = consensus_df[consensus_df["gene_id"].fillna("") != ""]
    duplicates = with_gene_id.duplicated(subset=["phenotype", "gene_id"], keep=False)
    if duplicates.any():
        dup_records = with_gene_id.loc[duplicates, ["phenotype", "gene_id", "gene_symbol"]].to_dict("records")
        errors.append(f"Duplicate (phenotype, gene_id) records detected: {dup_records}")
    return errors

def validate_provenance_join(consensus_df, provenance_df):
    errors = []
    consensus_ids = set(consensus_df["provenance_id"].dropna().astype(str))
    provenance_ids = set(provenance_df["provenance_id"].dropna().astype(str))
    missing = sorted(consensus_ids - provenance_ids)
    if missing:
        errors.append(f"Consensus provenance_id values missing from provenance table: {missing}")
    return errors

def validate_score_consistency(consensus_df):
    errors = []
    for _, row in consensus_df.iterrows():
        try:
            consensus_score = float(row["consensus_score"])
            weighted_source_sum = float(row["weighted_source_sum"])
        except ValueError:
            errors.append(f"Non-numeric score detected for gene {row.get('gene_symbol')}")
            continue
        if abs(consensus_score - weighted_source_sum) > 1e-9:
            errors.append(
                f"Score mismatch for {row.get('gene_symbol')}: "
                f"consensus_score={consensus_score}, weighted_source_sum={weighted_source_sum}"
            )
    return errors

def validate_outputs(consensus_df, provenance_df):
    errors = []
    warnings = []
    errors.extend(validate_required_columns(consensus_df, REQUIRED_CONSENSUS_COLUMNS, "consensus_gene_set"))
    errors.extend(validate_required_columns(provenance_df, REQUIRED_PROVENANCE_COLUMNS, "gene_provenance"))
    errors.extend(validate_forbidden_columns(consensus_df, "consensus_gene_set"))
    errors.extend(validate_forbidden_columns(provenance_df, "gene_provenance"))
    if not errors:
        errors.extend(validate_consensus_identity(consensus_df))
        errors.extend(validate_provenance_join(consensus_df, provenance_df))
        errors.extend(validate_score_consistency(consensus_df))
    unresolved = consensus_df["mapping_status_summary"].fillna("").str.contains("unresolved").sum() if "mapping_status_summary" in consensus_df.columns else 0
    ambiguous = consensus_df["mapping_status_summary"].fillna("").str.contains("ambiguous").sum() if "mapping_status_summary" in consensus_df.columns else 0
    if unresolved:
        warnings.append(f"Unresolved mappings present: {int(unresolved)}")
    if ambiguous:
        warnings.append(f"Ambiguous mappings present: {int(ambiguous)}")
    return errors, warnings
