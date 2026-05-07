#!/usr/bin/env python
from pathlib import Path
import argparse
import pandas as pd

def browser_to_high_confidence(browser_df, symbol_map):
    out = browser_df.copy()
    out["gene_symbol"] = out["hgnc_symbol"]
    missing_symbol = out["gene_symbol"].fillna("").str.strip() == ""
    out.loc[missing_symbol, "gene_symbol"] = out.loc[missing_symbol, "ensembl_gene_id"].map(symbol_map).fillna("")
    out["evidence_channel"] = "browser_exomewide_ptv"
    out["evidence_basis"] = "browser PTV burden p_value <= 3.4e-7, odds_ratio > 1"
    out["variant_classes"] = "PTV"
    out["source_release"] = out["source_release"]
    out["publication_anchor"] = out["publication_anchor"]
    out["notes"] = (
        "ensembl_gene_id=" + out["ensembl_gene_id"].astype(str)
        + "; gene_description=" + out["gene_description"].astype(str)
        + "; p_value_raw=" + out["p_value_raw"].astype(str)
        + "; odds_ratio=" + out["odds_ratio"].astype(str)
        + "; case_count=" + out["case_count"].astype(str)
        + "; control_count=" + out["control_count"].astype(str)
    )
    return out[
        [
            "phenotype",
            "gene_symbol",
            "ensembl_gene_id",
            "evidence_channel",
            "evidence_basis",
            "variant_classes",
            "source_name",
            "source_tier",
            "source_type",
            "source_release",
            "publication_anchor",
            "notes",
        ]
    ]

def main():
    parser = argparse.ArgumentParser(description="Build Epi25 high-confidence gene sets by combining browser-derived and publication-anchored evidence channels.")
    parser.add_argument("--browser-core", default="/mnt/storage/gene_sets/epi25/2024/processed/epi25_2024_browser_exomewide_ptv.tsv")
    parser.add_argument("--publication-joint", default="data/metadata/epi25/epi25_2024_publication_joint_high_confidence.tsv")
    parser.add_argument("--symbol-map", default="data/metadata/epi25/epi25_2024_high_confidence_ensembl_symbol_map.tsv")
    parser.add_argument("--output-dir", default="/mnt/storage/gene_sets/epi25/2024/processed")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    browser_df = pd.read_csv(args.browser_core, sep="\t", dtype=str).fillna("")
    publication_df = pd.read_csv(args.publication_joint, sep="\t", dtype=str).fillna("")
    symbol_map_df = pd.read_csv(args.symbol_map, sep="\t", dtype=str).fillna("")
    symbol_map = dict(zip(symbol_map_df["ensembl_gene_id"], symbol_map_df["gene_symbol"]))

    browser_high = browser_to_high_confidence(browser_df, symbol_map)
    combined = pd.concat([browser_high, publication_df], ignore_index=True)

    if (combined["gene_symbol"].fillna("").str.strip() == "").any():
        missing = combined.loc[combined["gene_symbol"].fillna("").str.strip() == "", ["phenotype", "ensembl_gene_id", "evidence_channel"]]
        raise ValueError(f"Missing gene_symbol after mapping: {missing.to_dict(orient='records')}")

    combined = combined.sort_values(
        by=["phenotype", "gene_symbol", "evidence_channel"],
        ascending=[True, True, True]
    ).reset_index(drop=True)

    long_output = output_dir / "epi25_2024_high_confidence_long.tsv"
    combined.to_csv(long_output, sep="\t", index=False)

    summary_rows = []
    for phenotype, group in combined.groupby("phenotype"):
        genes = sorted(set(group["gene_symbol"]))
        phenotype_output = output_dir / f"epi25_2024_{phenotype.lower()}_high_confidence.tsv"
        phenotype_df = pd.DataFrame({
            "gene_symbol": genes,
            "phenotype": phenotype,
            "source_name": "Epi25",
            "source_tier": "gold",
            "evidence_class": "high_confidence",
        })
        phenotype_df.to_csv(phenotype_output, sep="\t", index=False)
        summary_rows.append({
            "phenotype": phenotype,
            "unique_genes": len(genes),
            "genes": "|".join(genes),
            "output_path": str(phenotype_output),
        })

    summary = pd.DataFrame(summary_rows).sort_values("phenotype")
    summary_path = output_dir / "epi25_2024_high_confidence_summary.tsv"
    summary.to_csv(summary_path, sep="\t", index=False)

    print(f"long_output={long_output}")
    print(f"summary_path={summary_path}")
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
