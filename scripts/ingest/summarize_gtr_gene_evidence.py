#!/usr/bin/env python
from pathlib import Path
import argparse
import pandas as pd

EXCLUDED_TEST_SCOPES = {"exome", "genome"}

def explode_pipe_values(values):
    out = []
    for value in values:
        for token in str(value).split("|"):
            token = token.strip()
            if token and token.lower() != "nan":
                out.append(token)
    return out

def pipe_unique(values, limit=None):
    vals = sorted({str(v).strip() for v in values if str(v).strip() and str(v).strip().lower() != "nan"})
    if limit is not None:
        vals = vals[:limit]
    return "|".join(vals)

def pipe_unique_exploded(values, limit=None):
    vals = sorted(set(explode_pipe_values(values)))
    if limit is not None:
        vals = vals[:limit]
    return "|".join(vals)

def count_unique_exploded(values):
    return len(set(explode_pipe_values(values)))

def summarize(input_path, output_path, source_id, source_name, source_tier):
    df = pd.read_csv(input_path, sep="\t", dtype=str).fillna("")

    raw_rows = len(df)
    raw_unique_genes = df["gene_symbol"].nunique() if "gene_symbol" in df.columns else 0

    usable = df[~df["test_scope"].isin(EXCLUDED_TEST_SCOPES)].copy()
    usable = usable[usable["gene_symbol"].str.strip() != ""].copy()

    rows = []
    for gene_symbol, group in usable.groupby("gene_symbol", sort=True):
        gene_ids = [x for x in group["gene_id"].tolist() if x]
        gene_id = sorted(set(gene_ids))[0] if gene_ids else ""

        gtr_accessions = sorted(set(x for x in group["gtr_accession"].tolist() if x))
        lab_ids = sorted(set(x for x in group["lab_id"].tolist() if x))
        trait_ids = sorted(set(x for x in group["matched_trait_id"].tolist() if x))

        matched_keyword_count = count_unique_exploded(group["matched_keyword"])
        matched_trait_name_count = count_unique_exploded(group["matched_trait_name"])
        rows.append({
            "gene_symbol": gene_symbol,
            "gene_id": gene_id,
            "gtr_test_count": len(gtr_accessions),
            "independent_lab_count": len(lab_ids),
            "matched_trait_count": len(trait_ids),
            "unique_matched_keyword_count": matched_keyword_count,
            "matched_trait_name_count": matched_trait_name_count,
            "test_scope_summary": pipe_unique_exploded(group["test_scope"]),
            "matched_keywords": pipe_unique_exploded(group["matched_keyword"]),
            "matched_trait_names_capped": pipe_unique_exploded(group["matched_trait_name"], limit=25),
            "gtr_accessions_capped": pipe_unique(gtr_accessions, limit=50),
            "lab_ids_capped": pipe_unique(lab_ids, limit=50),
            "source_id": source_id,
            "source_name": source_name,
            "source_tier": source_tier,
            "evidence_label": "gtr_clinical_testing_utilization",
            "notes": (
                f"raw_rows={raw_rows}; "
                f"raw_unique_genes={raw_unique_genes}; "
                f"summary_policy=exclude_exome_genome_from_counts; "
                f"excluded_test_scopes={','.join(sorted(EXCLUDED_TEST_SCOPES))}"
            ),
        })

    out = pd.DataFrame(rows)
    if not out.empty:
        out = out.sort_values(
            ["independent_lab_count", "gtr_test_count", "matched_trait_count", "gene_symbol"],
            ascending=[False, False, False, True],
        )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, sep="\t", index=False, lineterminator="\n")

    print(f"input={input_path}")
    print(f"output={output_path}")
    print(f"raw_rows={raw_rows}")
    print(f"raw_unique_genes={raw_unique_genes}")
    print(f"summary_rows={len(out)}")
    if not out.empty:
        print(out[["gene_symbol", "gtr_test_count", "independent_lab_count", "matched_trait_count"]].head(20).to_string(index=False))

def main():
    parser = argparse.ArgumentParser(description="Summarize raw GTR gene-measure evidence into a GSC-ready gene-level source table.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--source-name", required=True)
    parser.add_argument("--source-tier", default="silver")
    args = parser.parse_args()

    summarize(
        input_path=args.input,
        output_path=args.output,
        source_id=args.source_id,
        source_name=args.source_name,
        source_tier=args.source_tier,
    )

if __name__ == "__main__":
    main()
