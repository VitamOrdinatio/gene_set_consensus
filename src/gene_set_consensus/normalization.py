from pathlib import Path
import pandas as pd
import hashlib

def load_identifier_map(identifier_map_path):
    df = pd.read_csv(identifier_map_path, sep="\t", dtype=str).fillna("")
    required_columns = [
        "input_gene_symbol",
        "normalized_gene_symbol",
        "gene_id",
        "gene_namespace",
        "mapping_status",
    ]
    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        raise ValueError(f"Identifier map missing required columns: {missing}")
    mapping = {}
    for _, row in df.iterrows():
        key = row["input_gene_symbol"].strip().upper()
        mapping[key] = row.to_dict()
    return mapping

def make_source_record_hash(source_id, source_row_number, normalized_gene_symbol):
    payload = f"{source_id}|{source_row_number}|{normalized_gene_symbol}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

def normalize_gene_symbol(raw_value):
    if raw_value is None:
        return ""
    return str(raw_value).strip().upper()

def normalize_source_dataframe(
    source_df,
    source_config,
    phenotype_id,
    identifier_map
):
    normalized_rows = []

    source_id = source_config["source_id"]
    source_name = source_config["source_name"]
    source_type = source_config["source_type"]
    source_weight = float(source_config["source_weight"])
    evidence_semantics = source_config.get("evidence_semantics", "unspecified")
    evidence_tier = source_config.get("evidence_tier", source_config.get("weight_tier", "unspecified"))
    semantic_channel = source_config.get("semantic_channel", evidence_semantics)
    scoring_rule_id = source_config.get("scoring_rule_id", "")
    weight_tier = source_config["weight_tier"]
    gene_column = source_config["gene_column"]
    source_gene_namespace = source_config.get(
        "source_gene_namespace",
        "unknown_namespace",
    )
    canonical_gene_namespace = source_config.get(
        "canonical_gene_namespace",
        "unknown_namespace",
    )

    for idx, row in source_df.iterrows():

        raw_gene = row.get(gene_column, "")
        normalized_input = normalize_gene_symbol(raw_gene)

        mapping_record = identifier_map.get(normalized_input)

        adapter_gene_id = str(row.get("gene_id", "")).strip()
        source_gene_id = adapter_gene_id

        if mapping_record:
            normalized_gene_symbol = mapping_record["normalized_gene_symbol"]
            gene_id = (
                mapping_record["gene_id"]
                if mapping_record["gene_id"]
                else adapter_gene_id
            )
            gene_namespace = (
                mapping_record.get("gene_namespace", "")
                or canonical_gene_namespace
                or "unknown_namespace"
            )
            mapping_status = mapping_record["mapping_status"]
        elif adapter_gene_id:
            normalized_gene_symbol = normalized_input
            gene_id = adapter_gene_id
            gene_namespace = source_gene_namespace
            mapping_status = "adapter_gene_id_resolved"
        else:
            normalized_gene_symbol = normalized_input
            gene_id = ""
            gene_namespace = "unknown_namespace"
            mapping_status = "unresolved"

        source_record_hash = make_source_record_hash(
            source_id=source_id,
            source_row_number=idx + 1,
            normalized_gene_symbol=normalized_gene_symbol
        )

        normalized_rows.append({
            "phenotype": phenotype_id,
            "source_id": source_id,
            "source_name": source_name,
            "source_type": source_type,
            "weight_tier": weight_tier,
            "source_weight": source_weight,
            "evidence_semantics": evidence_semantics,
            "evidence_tier": evidence_tier,
            "semantic_channel": semantic_channel,
            "scoring_rule_id": scoring_rule_id,
            "source_row_number": idx + 1,
            "input_gene_symbol": raw_gene,
            "source_gene_id": source_gene_id,
            "source_gene_namespace": source_gene_namespace,
            "normalized_gene_symbol": normalized_gene_symbol,
            "gene_id": gene_id,
            "gene_namespace": gene_namespace,
            "mapping_status": mapping_status,
            "evidence_label": row.get("evidence_label", ""),
            "notes": row.get("notes", ""),
            "source_record_hash": source_record_hash,
            "targeted_gene_count": row.get("targeted_gene_count", ""),
            "small_panel_count": row.get("small_panel_count", ""),
            "medium_panel_count": row.get("medium_panel_count", ""),
            "large_panel_count": row.get("large_panel_count", ""),
            "panel_unsized_count": row.get("panel_unsized_count", ""),
            "exome_or_genome_count": row.get("exome_or_genome_count", ""),
            "unknown_scope_count": row.get("unknown_scope_count", "")
        })

    return pd.DataFrame(normalized_rows)

def collapse_within_source_duplicates(df):
    dedup_columns = [
        "source_id",
        "normalized_gene_symbol"
    ]
    deduped = (
        df.sort_values(
            by=["source_id", "normalized_gene_symbol", "source_row_number"]
        )
        .drop_duplicates(
            subset=dedup_columns,
            keep="first"
        )
        .reset_index(drop=True)
    )
    return deduped
