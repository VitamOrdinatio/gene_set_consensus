import pandas as pd
from gene_set_consensus.normalization import normalize_source_dataframe, collapse_within_source_duplicates

def test_deprecated_symbol_maps_to_current_symbol():
    source_df = pd.DataFrame([{"gene_symbol": "C10orf2", "evidence_label": "x", "notes": ""}])
    source_config = {"source_id": "s1", "source_name": "Source 1", "source_type": "curated", "source_weight": 3.0, "weight_tier": "gold", "gene_column": "gene_symbol"}
    identifier_map = {"C10ORF2": {"normalized_gene_symbol": "TWNK", "gene_id": "ENSG00000107815", "mapping_status": "deprecated_symbol_resolved"}}
    out = normalize_source_dataframe(source_df, source_config, "example", identifier_map)
    assert out.loc[0, "normalized_gene_symbol"] == "TWNK"
    assert out.loc[0, "mapping_status"] == "deprecated_symbol_resolved"

def test_collapse_within_source_duplicates():
    df = pd.DataFrame([
        {"source_id": "s1", "normalized_gene_symbol": "POLG", "source_row_number": 1},
        {"source_id": "s1", "normalized_gene_symbol": "POLG", "source_row_number": 2},
    ])
    out = collapse_within_source_duplicates(df)
    assert len(out) == 1
