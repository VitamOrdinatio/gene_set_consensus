from gene_set_consensus.gtr import summarize_gtr_panel
import pandas as pd

def test_gtr_summary_counts():

    df = pd.DataFrame([
        {
            "condition_label": "A",
            "condition_id": "C1",
            "test_name": "T1",
            "test_id": "TID1",
            "panel_name": "P1",
            "gene_symbol": "POLG",
            "gene_id": "G1",
        },
        {
            "condition_label": "A",
            "condition_id": "C1",
            "test_name": "T1",
            "test_id": "TID1",
            "panel_name": "P1",
            "gene_symbol": "TWNK",
            "gene_id": "G2",
        },
    ])

    summary = summarize_gtr_panel(df)

    assert summary["rows"] == 2
    assert summary["unique_conditions"] == 1
    assert summary["unique_tests"] == 1
    assert summary["unique_panels"] == 1
    assert summary["unique_genes"] == 2
