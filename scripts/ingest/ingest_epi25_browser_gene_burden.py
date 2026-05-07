#!/usr/bin/env python
from pathlib import Path
import argparse
import math
import pandas as pd

PHENOTYPE_FILES = {
    "EPI": "EPI_results_*.csv",
    "DEE": "DEE_results_*.csv",
    "GGE": "GGE_results_*.csv",
    "NAFE": "NAFE_results_*.csv",
}

REQUIRED_COLUMNS = [
    "Gene",
    "Description",
    "Cases",
    "Controls",
    "PTV Case Count",
    "PTV Control Count",
    "PTV p-val",
    "PTV odds ratio",
    "Damaging Missense Case Count",
    "Damaging Missense Control Count",
    "Damaging Missense p-val",
    "Damaging Missense odds ratio",
]

VARIANT_CLASS_MAP = {
    "PTV": {
        "case_count": "PTV Case Count",
        "control_count": "PTV Control Count",
        "p_value": "PTV p-val",
        "odds_ratio": "PTV odds ratio",
    },
    "damaging_missense": {
        "case_count": "Damaging Missense Case Count",
        "control_count": "Damaging Missense Control Count",
        "p_value": "Damaging Missense p-val",
        "odds_ratio": "Damaging Missense odds ratio",
    },
}

def parse_float(value):
    value = str(value).strip()
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None

def neg_log10_p(p_value_numeric, p_value_zero_flag):
    if p_value_zero_flag:
        return -math.log10(1e-300)
    if p_value_numeric is None or p_value_numeric <= 0:
        return None
    return -math.log10(p_value_numeric)

def normalize_column_name(name):
    return (
        str(name)
        .replace("\u2010", "-")
        .replace("\u2011", "-")
        .replace("\u2012", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2212", "-")
        .strip()
    )

def load_epi25_file(path):
    df = pd.read_csv(path, dtype=str).fillna("")
    df.columns = [normalize_column_name(col) for col in df.columns]
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"{path} missing required columns: {missing}")
    return df

def wide_to_long(df, phenotype, browser_export_file):
    rows = []
    for _, row in df.iterrows():
        for variant_class, cols in VARIANT_CLASS_MAP.items():
            p_raw = str(row[cols["p_value"]]).strip()
            p_numeric = parse_float(p_raw)
            zero_flag = p_raw == "0"
            rows.append({
                "ensembl_gene_id": row["Gene"],
                "hgnc_symbol": "",
                "gene_description": row["Description"],
                "phenotype": phenotype,
                "variant_class": variant_class,
                "cases": row["Cases"],
                "controls": row["Controls"],
                "case_count": row[cols["case_count"]],
                "control_count": row[cols["control_count"]],
                "p_value_raw": p_raw,
                "p_value_numeric": p_numeric,
                "p_value_zero_flag": zero_flag,
                "p_value_for_neglog10": 1e-300 if zero_flag else p_numeric,
                "neg_log10_p": neg_log10_p(p_numeric, zero_flag),
                "odds_ratio": row[cols["odds_ratio"]],
                "source_name": "Epi25",
                "source_tier": "gold",
                "source_type": "consortium_wes_burden",
                "source_release": "browser_export_2026_05_06",
                "publication_anchor": "Epi25_2024",
                "browser_export_file": browser_export_file,
                "notes": "",
            })
    return pd.DataFrame(rows)

def classify_evidence(df):
    out = df.copy()
    out["case_count_numeric"] = pd.to_numeric(out["case_count"], errors="coerce")
    out["control_count_numeric"] = pd.to_numeric(out["control_count"], errors="coerce")
    out["odds_ratio_numeric"] = pd.to_numeric(out["odds_ratio"], errors="coerce")
    out["is_case_enriched"] = out["odds_ratio_numeric"] > 1
    out["is_exomewide_gene_ptv"] = (
        (out["variant_class"] == "PTV")
        & (out["p_value_numeric"].fillna(1.0) <= 3.4e-7)
        & (out["is_case_enriched"])
    )
    out["is_strong_candidate"] = (
        (out["p_value_numeric"].fillna(1.0) <= 1e-5)
        & (out["case_count_numeric"].fillna(0) >= 3)
        & (out["is_case_enriched"])
    )
    out["is_exploratory_candidate"] = (
        (out["p_value_numeric"].fillna(1.0) <= 1e-3)
        & (out["case_count_numeric"].fillna(0) >= 5)
        & (out["is_case_enriched"])
    )
    return out

def find_one_file(raw_dir, pattern):
    matches = sorted(raw_dir.glob(pattern))
    if len(matches) != 1:
        raise FileNotFoundError(f"Expected exactly one file for pattern {pattern}; found {len(matches)}")
    return matches[0]

def main():
    parser = argparse.ArgumentParser(description="Ingest Epi25 browser gene-burden CSVs into long GSC evidence tables.")
    parser.add_argument("--raw-dir", default="/mnt/storage/gene_sets/epi25/2024/raw")
    parser.add_argument("--processed-dir", default="/mnt/storage/gene_sets/epi25/2024/processed")
    args = parser.parse_args()

    raw_dir = Path(args.raw_dir)
    processed_dir = Path(args.processed_dir)
    processed_dir.mkdir(parents=True, exist_ok=True)

    long_tables = []
    for phenotype, pattern in PHENOTYPE_FILES.items():
        path = find_one_file(raw_dir, pattern)
        df = load_epi25_file(path)
        long_df = wide_to_long(df, phenotype, path.name)
        long_tables.append(long_df)

    burden_long = pd.concat(long_tables).reset_index(drop=True)
    burden_long = classify_evidence(burden_long)
    burden_long = burden_long.sort_values(
        by=["phenotype", "variant_class", "p_value_numeric", "ensembl_gene_id"],
        ascending=[True, True, True, True],
        na_position="last",
    ).reset_index(drop=True)

    long_output = processed_dir / "epi25_2024_browser_burden_long.tsv"
    core_output = processed_dir / "epi25_2024_exomewide_ptv_core.tsv"
    ranked_output = processed_dir / "epi25_2024_candidates_ranked.tsv"

    burden_long.to_csv(long_output, sep="\t", index=False)

    core = burden_long[burden_long["is_exomewide_gene_ptv"]].copy()
    core.to_csv(core_output, sep="\t", index=False)

    candidates = burden_long[
        burden_long["is_strong_candidate"] | burden_long["is_exploratory_candidate"]
    ].copy()
    candidates = candidates.sort_values(
        by=["is_exomewide_gene_ptv", "is_strong_candidate", "p_value_numeric", "phenotype", "variant_class"],
        ascending=[False, False, True, True, True],
        na_position="last",
    )
    candidates.to_csv(ranked_output, sep="\t", index=False)

    print(f"long_output={long_output}")
    print(f"long_rows={len(burden_long)}")
    print(f"core_output={core_output}")
    print(f"core_rows={len(core)}")
    print(f"ranked_output={ranked_output}")
    print(f"ranked_rows={len(candidates)}")

if __name__ == "__main__":
    main()
