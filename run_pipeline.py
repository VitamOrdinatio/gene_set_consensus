#!/usr/bin/env python
from pathlib import Path
import argparse
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from gene_set_consensus.runtime import generate_run_id

def run_step(command, step_name):

    print(f"[GSC] starting {step_name}")

    result = subprocess.run(command)

    if result.returncode != 0:
        raise RuntimeError(
            f"{step_name} failed with exit code {result.returncode}"
        )

    print(f"[GSC] completed {step_name}")

def main():

    parser = argparse.ArgumentParser(
        description="Run the GSC pipeline end-to-end."
    )

    parser.add_argument(
        "--config",
        default="config/config.yaml"
    )

    parser.add_argument(
        "--phenotype",
        required=True
    )

    parser.add_argument(
        "--identifier-map",
        default="data/example/identifier_map.tsv"
    )

    args = parser.parse_args()

    python = sys.executable

    run_id = generate_run_id()

    print(f"[GSC] run_id={run_id}")

    shared_args = [
        "--config",
        args.config,
        "--phenotype",
        args.phenotype,
        "--run-id",
        run_id,
    ]

    run_step(
        [
            python,
            "scripts/step_01_validate_inputs.py",
            *shared_args,
        ],
        "step_01_validate_inputs",
    )

    run_step(
        [
            python,
            "scripts/step_02_normalize_genes.py",
            *shared_args,
            "--identifier-map",
            args.identifier_map,
        ],
        "step_02_normalize_genes",
    )

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
            *shared_args,
        ],
        "step_04_score_consensus",
    )

    run_step(
        [
            python,
            "scripts/step_05_write_outputs.py",
            *shared_args,
        ],
        "step_05_write_outputs",
    )

    run_step(
        [
            python,
            "scripts/step_06_validate_outputs.py",
            *shared_args,
        ],
        "step_06_validate_outputs",
    )

    print("[GSC] pipeline completed successfully")
    print(f"[GSC] final run_id={run_id}")

if __name__ == "__main__":
    main()
