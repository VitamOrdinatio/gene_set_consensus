from pathlib import Path
import pandas as pd

REQUIRED_GTR_COLUMNS = [
    "condition_label",
    "condition_id",
    "test_name",
    "test_id",
    "panel_name",
    "gene_symbol",
    "gene_id",
]

def validate_gtr_dataframe(df):
    missing = [c for c in REQUIRED_GTR_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"GTR dataframe missing required columns: {missing}")

def load_gtr_panel(path):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"GTR panel file not found: {path}")

    df = pd.read_csv(path, sep="\t", dtype=str).fillna("")

    validate_gtr_dataframe(df)

    return df

def summarize_gtr_panel(df):
    summary = {
        "rows": len(df),
        "unique_conditions": int(df["condition_id"].nunique()),
        "unique_tests": int(df["test_id"].nunique()),
        "unique_panels": int(df["panel_name"].nunique()),
        "unique_genes": int(df["gene_symbol"].nunique()),
    }

    return summary
