#!/usr/bin/env python
from pathlib import Path
import argparse
import sys
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gene_set_consensus.config import (
    load_project_config,
    load_phenotype_config,
    resolve_phenotype_config_path
)

from gene_set_consensus.logging_utils import (
    setup_run_dirs,
    get_logger
)
from gene_set_consensus.runtime import generate_run_id

from gene_set_consensus.normalization import (
    load_identifier_map,
    normalize_source_dataframe,
    collapse_within_source_duplicates
)

def detect_separator(path):
    suffix = Path(path).suffix.lower()
    if suffix == ".tsv":
        return "\t"
    if suffix == ".csv":
        return ","
    raise ValueError(f"Unsupported extension: {path}")

def main():

    parser = argparse.ArgumentParser(description="Normalize GSC source gene identifiers.")
    parser.add_argument("--config", default="config/config.yaml")
    parser.add_argument("--phenotype", required=True)
    parser.add_argument(
        "--identifier-map",
        default="data/example/identifier_map.tsv"
    )
    parser.add_argument("--run-id", default=None)

    args = parser.parse_args()

    project_config = load_project_config(args.config)

    phenotype_path = resolve_phenotype_config_path(
        project_config,
        args.phenotype
    )

    phenotype_config = load_phenotype_config(phenotype_path)

    phenotype_id = phenotype_config["phenotype"]["phenotype_id"]

    run_id = args.run_id if args.run_id else generate_run_id()

    run_dirs = setup_run_dirs(project_config, run_id)

    logger = get_logger(
        "step_02_normalize_genes",
        run_dirs["logs_dir"] / "step_02_normalize_genes.log"
    )

    logger.info(f"run_id={run_id}")
    logger.info(f"phenotype={phenotype_id}")

    identifier_map = load_identifier_map(args.identifier_map)

    all_normalized = []

    for source in phenotype_config["sources"]:

        source_path = Path(source["file_path"])

        logger.info(f"loading_source={source['source_id']}")
        logger.info(f"source_path={source_path}")

        sep = detect_separator(source_path)

        source_df = pd.read_csv(
            source_path,
            sep=sep,
            dtype=str
        ).fillna("")

        logger.info(f"source_rows={len(source_df)}")

        normalized_df = normalize_source_dataframe(
            source_df=source_df,
            source_config=source,
            phenotype_id=phenotype_id,
            identifier_map=identifier_map
        )

        before = len(normalized_df)

        normalized_df = collapse_within_source_duplicates(normalized_df)

        after = len(normalized_df)

        logger.info(f"duplicates_removed={before - after}")

        all_normalized.append(normalized_df)

    final_df = pd.concat(all_normalized).reset_index(drop=True)

    output_path = (
        run_dirs["interim_dir"] /
        "normalized_source_records.tsv"
    )

    final_df.to_csv(
        output_path,
        sep="\t",
        index=False
    )

    logger.info(f"normalized_rows={len(final_df)}")
    logger.info(f"output_path={output_path}")

    mapping_summary = (
        final_df["mapping_status"]
        .value_counts()
        .reset_index()
    )

    summary_path = (
        run_dirs["interim_dir"] /
        "mapping_summary.tsv"
    )

    mapping_summary.to_csv(
        summary_path,
        sep="\t",
        index=False
    )

    logger.info(f"mapping_summary_path={summary_path}")

if __name__ == "__main__":
    main()
