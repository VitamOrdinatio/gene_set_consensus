#!/usr/bin/env python
from pathlib import Path
import argparse
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from gene_set_consensus.pipeline_runtime import resolve_execution_args
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
        default=None
    )

    parser.add_argument(
        "--release",
        default=None
    )

    parser.add_argument(
        "--identifier-map",
        default="data/example/identifier_map.tsv"
    )

    parser.add_argument(
        "--source-manifest",
        default=None
    )

    parser.add_argument(
        "--scoring-profile",
        default=None
    )

    args = parser.parse_args()

    resolved = resolve_execution_args(args)
    phenotype = resolved["phenotype"]
    phenotype_config = resolved["phenotype_config"]
    identifier_map = resolved["identifier_map"]
    source_manifest = resolved["source_manifest"]
    scoring_profile = resolved["scoring_profile"]
    release_id = resolved["release_id"]

    python = sys.executable
    run_id = generate_run_id()

    print(f"[GSC] run_id={run_id}")
    if release_id:
        print(f"[GSC] release_id={release_id}")
    print(f"[GSC] phenotype={phenotype}")
    print(f"[GSC] phenotype_config={phenotype_config}")
    if scoring_profile:
        print(f"[GSC] scoring_profile={scoring_profile}")
    if source_manifest:
        print(f"[GSC] source_manifest={source_manifest}")

    shared_args = [
        "--config",
        args.config,
        "--phenotype",
        phenotype,
        "--phenotype-config",
        phenotype_config,
        "--run-id",
        run_id,
    ]

    step_01 = [
        python,
        "scripts/step_01_validate_inputs.py",
        *shared_args,
    ]
    if source_manifest:
        step_01.extend(["--source-manifest", source_manifest])

    run_step(step_01, "step_01_validate_inputs")

    step_02 = [
        python,
        "scripts/step_02_normalize_genes.py",
        *shared_args,
        "--identifier-map",
        identifier_map,
    ]
    if source_manifest:
        step_02.extend(["--source-manifest", source_manifest])

    run_step(step_02, "step_02_normalize_genes")

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

    step_04 = [
        python,
        "scripts/step_04_score_consensus.py",
        *shared_args,
    ]
    if scoring_profile:
        step_04.extend(["--scoring-profile", scoring_profile])

    run_step(step_04, "step_04_score_consensus")

    step_05 = [
        python,
        "scripts/step_05_write_outputs.py",
        *shared_args,
    ]
    if source_manifest:
        step_05.extend(["--source-manifest", source_manifest])

    run_step(step_05, "step_05_write_outputs")

    run_step(
        [
            python,
            "scripts/step_06_validate_outputs.py",
            *shared_args,
        ],
        "step_06_validate_outputs",
    )

    print("[GSC] pipeline completed successfully")
    print(f"[GSC] final_run_id={run_id}")

if __name__ == "__main__":
    main()
