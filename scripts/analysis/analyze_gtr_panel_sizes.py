#!/usr/bin/env python
from pathlib import Path
import argparse
import pandas as pd

def summarize_panel_sizes(df):
    if "gtr_accession" not in df.columns:
        raise ValueError("Missing gtr_accession column")

    if "gene_symbol" not in df.columns:
        raise ValueError("Missing gene_symbol column")

    grouped = (
        df.groupby("gtr_accession")["gene_symbol"]
        .nunique()
        .reset_index(name="genes_per_test")
    )

    print("\n=== PANEL SIZE SUMMARY ===\n")

    print(grouped["genes_per_test"].describe())

    quantiles = grouped["genes_per_test"].quantile(
        [0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
    )

    print("\n=== QUANTILES ===\n")
    print(quantiles)

    print("\n=== SMALLEST PANELS ===\n")
    print(
        grouped.sort_values("genes_per_test", ascending=True)
        .head(25)
        .to_string(index=False)
    )

    print("\n=== LARGEST PANELS ===\n")
    print(
        grouped.sort_values("genes_per_test", ascending=False)
        .head(25)
        .to_string(index=False)
    )

    return grouped

def classify_panel_size(n):
    if n <= 5:
        return "targeted_gene"
    elif n <= 25:
        return "small_panel"
    elif n <= 100:
        return "medium_panel"
    else:
        return "large_panel"

def main():
    parser = argparse.ArgumentParser(
        description="Analyze GTR panel size distributions."
    )

    parser.add_argument("--input", required=True)

    args = parser.parse_args()

    path = Path(args.input)

    df = pd.read_csv(path, sep="\t", dtype=str).fillna("")

    grouped = summarize_panel_sizes(df)

    grouped["panel_class"] = grouped["genes_per_test"].apply(
        classify_panel_size
    )

    print("\n=== PANEL CLASS COUNTS ===\n")

    print(
        grouped["panel_class"]
        .value_counts()
        .to_string()
    )

if __name__ == "__main__":
    main()
