import pandas as pd
from gene_set_consensus.aggregation import build_gene_source_matrix

def test_source_count_deduplicated_source_records():
    df = pd.DataFrame([
        {"phenotype": "example", "gene_id": "G1", "normalized_gene_symbol": "POLG", "source_id": "a", "source_weight": 3.0},
        {"phenotype": "example", "gene_id": "G1", "normalized_gene_symbol": "POLG", "source_id": "a", "source_weight": 3.0},
        {"phenotype": "example", "gene_id": "G1", "normalized_gene_symbol": "POLG", "source_id": "b", "source_weight": 2.0},
    ])
    matrix = build_gene_source_matrix(df)
    assert int(matrix.loc[0, "source_count"]) == 2
    assert float(matrix.loc[0, "weighted_source_sum"]) == 5.0
