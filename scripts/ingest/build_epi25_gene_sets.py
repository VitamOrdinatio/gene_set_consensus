#!/usr/bin/env python
from pathlib import Path
import argparse
import pandas as pd
import yaml

def load_rules(path):
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)

def apply_rule(df, rule):
    out = df.copy()

    if "variant_class" in rule:
        out = out[out["variant_class"] == rule["variant_class"]]

    if "p_value_lte" in rule:
        out = out[pd.to_numeric(out["p_value_numeric"], errors="coerce") <= float(rule["p_value_lte"])]

    if "odds_ratio_gt" in rule:
        out = out[pd.to_numeric(out["odds_ratio"], errors="coerce") > float(rule["odds_ratio_gt"])]

    if "case_count_gte" in rule:
        out = out[pd.to_numeric(out["case_count"], errors="coerce") >= float(rule["case_count_gte"])]

    return out.copy()

def main():
    parser = argparse.ArgumentParser(description="Build deterministic Epi25 browser-derived gene-set products from long burden evidence.")
    parser.add_argument("--input", default="/mnt/storage/gene_sets/epi25/2024/processed/epi25_2024_browser_burden_long.tsv")
    parser.add_argument("--rules", default="config/rules/epi25_rules.yaml")
    parser.add_argument("--output-dir", default="/mnt/storage/gene_sets/epi25/2024/processed")
    args = parser.parse_args()

    df = pd.read_csv(args.input, sep="\t", dtype=str).fillna("")
    rules = load_rules(args.rules)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    summary_rows = []

    for rule_name, rule in rules.items():
        subset = apply_rule(df, rule)
        subset = subset.sort_values(
            by=["phenotype", "variant_class", "p_value_numeric", "ensembl_gene_id"],
            ascending=[True, True, True, True],
            na_position="last"
        ).reset_index(drop=True)

        output_path = output_dir / f"{rule_name}.tsv"
        subset.to_csv(output_path, sep="\t", index=False)

        phenotype_counts = subset["phenotype"].value_counts().to_dict()
        unique_gene_count = subset["ensembl_gene_id"].nunique()

        summary_rows.append({
            "rule_name": rule_name,
            "rows": len(subset),
            "unique_genes": unique_gene_count,
            "EPI_rows": phenotype_counts.get("EPI", 0),
            "DEE_rows": phenotype_counts.get("DEE", 0),
            "GGE_rows": phenotype_counts.get("GGE", 0),
            "NAFE_rows": phenotype_counts.get("NAFE", 0),
            "output_path": str(output_path)
        })

    summary = pd.DataFrame(summary_rows)
    summary_path = output_dir / "epi25_2024_browser_gene_set_build_summary.tsv"
    summary.to_csv(summary_path, sep="\t", index=False)

    print(f"summary_path={summary_path}")
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
