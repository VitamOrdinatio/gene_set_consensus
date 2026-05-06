#!/usr/bin/env python
from pathlib import Path
import argparse
import subprocess
import sys
import time

def run_step(command, step_name):
    print(f"[GSC] starting {step_name}")
    result = subprocess.run(command)
    if result.returncode != 0:
        raise RuntimeError(f"{step_name} failed with exit code {result.returncode}")
    print(f"[GSC] completed {step_name}")

def latest_run_id_from_interim():
    run_dirs = sorted(Path("data/interim").glob("run_*"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not run_dirs:
        raise RuntimeError("No run directory found in data/interim after validation/normalization.")
    return run_dirs[0].name

def main():
    parser = argparse.ArgumentParser(description="Run the GSC pipeline end-to-end.")
    parser.add_argument("--config", default="config/config.yaml")
    parser.add_argument("--phenotype", required=True)
    parser.add_argument("--identifier-map", default="data/example/identifier_map.tsv")
    args = parser.parse_args()

    python = sys.executable

    run_step(
        [
            python,
            "scripts/step_01_validate_inputs.py",
            "--config",
            args.config,
            "--phenotype",
            args.phenotype,
        ],
        "step_01_validate_inputs",
    )

    # Step 02 currently creates the run directory used by downstream steps.
    # Step 01 has its own validation-only run directory. This will be refined later
    # when shared run-id propagation is added.
    run_step(
        [
            python,
            "scripts/step_02_normalize_genes.py",
            "--config",
            args.config,
            "--phenotype",
            args.phenotype,
            "--identifier-map",
            args.identifier_map,
        ],
        "step_02_normalize_genes",
    )

    # Small guard to avoid edge cases on filesystems with coarse mtimes.
    time.sleep(0.2)
    run_id = latest_run_id_from_interim()
    print(f"[GSC] downstream run_id={run_id}")

    run_step(
        [
            python,
            "scripts/step_03_build_source_matrix.py",
            "--config",
            args.config,
            "--run-id",
            run_id,
        ],
        "step_03_build_source_matrix",
    )

    run_step(
        [
            python,
            "scripts/step_04_score_consensus.py",
            "--config",
            args.config,
            "--phenotype",
            args.phenotype,
            "--run-id",
            run_id,
        ],
        "step_04_score_consensus",
    )

    run_step(
        [
            python,
            "scripts/step_05_write_outputs.py",
            "--config",
            args.config,
            "--phenotype",
            args.phenotype,
            "--run-id",
            run_id,
        ],
        "step_05_write_outputs",
    )

    run_step(
        [
            python,
            "scripts/step_06_validate_outputs.py",
            "--config",
            args.config,
            "--phenotype",
            args.phenotype,
            "--run-id",
            run_id,
        ],
        "step_06_validate_outputs",
    )

    print("[GSC] pipeline completed successfully")
    print(f"[GSC] final run_id={run_id}")
    print(f"[GSC] consensus=results/tables/{args.phenotype}/consensus_gene_set.tsv")
    print(f"[GSC] report=results/reports/{args.phenotype}/validation_report.md")

if __name__ == "__main__":
    main()
