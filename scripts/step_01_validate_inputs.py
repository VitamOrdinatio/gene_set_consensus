#!/usr/bin/env python
from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gene_set_consensus.config import load_project_config, load_phenotype_config, resolve_phenotype_config_path
from gene_set_consensus.logging_utils import setup_run_dirs, get_logger
from gene_set_consensus.runtime import generate_run_id
from gene_set_consensus.validation import validate_project_paths, validate_sources

def main():
    parser = argparse.ArgumentParser(description="Validate GSC project and phenotype inputs.")
    parser.add_argument("--config", default="config/config.yaml")
    parser.add_argument("--phenotype", required=True)
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    project_config = load_project_config(args.config)
    phenotype_path = resolve_phenotype_config_path(project_config, args.phenotype)
    phenotype_config = load_phenotype_config(phenotype_path)
    run_id = args.run_id if args.run_id else generate_run_id()
    run_dirs = setup_run_dirs(project_config, run_id)
    logger = get_logger("step_01_validate_inputs", run_dirs["logs_dir"] / "step_01_validate_inputs.log")
    logger.info(f"run_id={run_id}")
    logger.info(f"project_config={args.config}")
    logger.info(f"phenotype_config={phenotype_path}")
    errors = []
    warnings = []
    errors.extend(validate_project_paths(project_config))
    source_errors, source_warnings = validate_sources(phenotype_config)
    errors.extend(source_errors)
    warnings.extend(source_warnings)
    summary_path = run_dirs["interim_dir"] / "input_validation_summary.tsv"
    with summary_path.open("w", encoding="utf-8") as handle:
        handle.write("level\tmessage\n")
        for warning in warnings:
            handle.write(f"warning\t{warning}\n")
        for error in errors:
            handle.write(f"error\t{error}\n")
        if not warnings and not errors:
            handle.write("info\tinput validation passed\n")
    if errors:
        for error in errors:
            logger.error(error)
        raise SystemExit(1)
    logger.info("Input validation passed")
    logger.info(f"summary_path={summary_path}")

if __name__ == "__main__":
    main()
