#!/usr/bin/env python
from pathlib import Path
import argparse
import sys
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gene_set_consensus.config import load_project_config
from gene_set_consensus.logging_utils import setup_run_dirs, get_logger
from gene_set_consensus.aggregation import build_gene_source_matrix, build_gene_frequency_table

def main():
    parser = argparse.ArgumentParser(description="Build GSC gene-source matrix and frequency table.")
    parser.add_argument("--config", default="config/config.yaml")
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    project_config = load_project_config(args.config)
    run_dirs = setup_run_dirs(project_config, args.run_id)
    logger = get_logger(
        "step_03_build_source_matrix",
        run_dirs["logs_dir"] / "step_03_build_source_matrix.log"
    )
    input_path = run_dirs["interim_dir"] / "normalized_source_records.tsv"
    if not input_path.exists():
        raise FileNotFoundError(f"Missing normalized input: {input_path}")
    normalized_df = pd.read_csv(input_path, sep="\t", dtype=str).fillna("")
    normalized_df["source_weight"] = normalized_df["source_weight"].astype(float)
    logger.info(f"run_id={args.run_id}")
    logger.info(f"input_path={input_path}")
    logger.info(f"normalized_rows={len(normalized_df)}")
    matrix_df = build_gene_source_matrix(normalized_df)
    frequency_df = build_gene_frequency_table(normalized_df, matrix_df)
    matrix_output = run_dirs["processed_dir"] / "gene_source_matrix.tsv"
    frequency_output = run_dirs["processed_dir"] / "gene_frequency_table.tsv"
    matrix_df.to_csv(matrix_output, sep="\t", index=False)
    frequency_df.to_csv(frequency_output, sep="\t", index=False)
    logger.info(f"matrix_rows={len(matrix_df)}")
    logger.info(f"frequency_rows={len(frequency_df)}")
    logger.info(f"matrix_output={matrix_output}")
    logger.info(f"frequency_output={frequency_output}")

if __name__ == "__main__":
    main()
