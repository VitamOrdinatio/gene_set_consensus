#!/usr/bin/env python
from pathlib import Path
import argparse
import sys
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gene_set_consensus.config import load_project_config
from gene_set_consensus.logging_utils import setup_run_dirs, get_logger
from gene_set_consensus.output_validation import validate_outputs

def main():
    parser = argparse.ArgumentParser(description="Validate final GSC outputs.")
    parser.add_argument("--config", default="config/config.yaml")
    parser.add_argument("--phenotype", required=True)
    parser.add_argument("--phenotype-config", default=None)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    project_config = load_project_config(args.config)
    run_dirs = setup_run_dirs(project_config, args.run_id)
    logger = get_logger(
        "step_06_validate_outputs",
        run_dirs["logs_dir"] / "step_06_validate_outputs.log"
    )
    tables_dir = Path(project_config["paths"]["results_dir"]) / "tables" / args.phenotype
    reports_dir = Path(project_config["paths"]["results_dir"]) / "reports" / args.phenotype
    reports_dir.mkdir(parents=True, exist_ok=True)
    consensus_path = tables_dir / "consensus_gene_set.tsv"
    provenance_path = tables_dir / "gene_provenance.tsv"
    if not consensus_path.exists():
        raise FileNotFoundError(f"Missing consensus output: {consensus_path}")
    if not provenance_path.exists():
        raise FileNotFoundError(f"Missing provenance output: {provenance_path}")
    consensus_df = pd.read_csv(consensus_path, sep="\t", dtype=str).fillna("")
    provenance_df = pd.read_csv(provenance_path, sep="\t", dtype=str).fillna("")
    errors, warnings = validate_outputs(consensus_df, provenance_df)
    validation_path = reports_dir / "output_contract_validation.tsv"
    with validation_path.open("w", encoding="utf-8") as handle:
        handle.write("level\tmessage\n")
        for warning in warnings:
            handle.write(f"warning\t{warning}\n")
        for error in errors:
            handle.write(f"error\t{error}\n")
        if not errors and not warnings:
            handle.write("info\toutput contract validation passed\n")
        elif not errors:
            handle.write("info\toutput contract validation passed with warnings\n")
    logger.info(f"run_id={args.run_id}")
    logger.info(f"phenotype={args.phenotype}")
    logger.info(f"consensus_path={consensus_path}")
    logger.info(f"provenance_path={provenance_path}")
    logger.info(f"validation_path={validation_path}")
    for warning in warnings:
        logger.warning(warning)
    if errors:
        for error in errors:
            logger.error(error)
        raise SystemExit(1)
    logger.info("Output contract validation passed")

if __name__ == "__main__":
    main()
