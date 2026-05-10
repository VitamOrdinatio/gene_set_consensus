#!/usr/bin/env python
from pathlib import Path
import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser(
        description="Compare legacy and semantic GSC scoring modes."
    )
    parser.add_argument("--input", required=True)
    parser.add_argument("--top-n", type=int, default=25)
    args = parser.parse_args()

    df = pd.read_csv(args.input, sep="\t")

    legacy = (
        df.sort_values(
            by=["weighted_source_sum", "source_count"],
            ascending=[False, False]
        )
        .reset_index(drop=True)
    )

    semantic = (
        df.sort_values(
            by=["semantic_consensus_score", "source_count"],
            ascending=[False, False]
        )
        .reset_index(drop=True)
    )

    legacy["legacy_rank"] = legacy.index + 1
    semantic["semantic_rank"] = semantic.index + 1

    semantic_unique = (
        semantic[
            [
                "gene_id",
                "gene_symbol",
                "semantic_rank",
            ]
        ]
        .drop_duplicates(
            subset=["gene_id", "gene_symbol"]
        )
    )

    merged = legacy.merge(
        semantic_unique,
        on=["gene_id", "gene_symbol"],
        how="left"
    )

    merged["rank_shift"] = (
        merged["legacy_rank"] - merged["semantic_rank"]
    )

    columns = [
        "gene_symbol",
        "weighted_source_sum",
        "semantic_consensus_score",
        "legacy_rank",
        "semantic_rank",
        "rank_shift",
        "semantic_channel_summary",
        "score_explanation",
    ]

    print(
        merged[columns]
        .head(args.top_n)
        .to_string(index=False)
    )

if __name__ == "__main__":
    main()
