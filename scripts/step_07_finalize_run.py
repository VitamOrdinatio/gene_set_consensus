#!/usr/bin/env python

import argparse
import hashlib
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gene_set_consensus.config import load_phenotype_config, load_project_config
from gene_set_consensus.logging_utils import get_logger, setup_run_dirs


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)

    if not isinstance(data, dict):
        raise ValueError(f"YAML file did not contain a dictionary: {path}")

    return data


def write_yaml(path: Path, data: dict) -> None:
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(
            data,
            handle,
            sort_keys=False,
        )


def parse_validation_status(validation_path: Path) -> str:
    validation_df = pd.read_csv(
        validation_path,
        sep="\t",
        dtype=str,
    ).fillna("")

    if "level" not in validation_df.columns:
        raise ValueError(
            f"Validation artifact missing required column 'level': "
            f"{validation_path}"
        )

    levels = {
        value.strip().lower()
        for value in validation_df["level"].tolist()
    }

    if "error" in levels:
        return "FAIL"

    return "PASS"


def iter_manifest_referenced_paths(manifest: dict):
    for section in ("input_files", "output_files"):
        entries = manifest.get(section, {})

        if not isinstance(entries, dict):
            raise ValueError(
                f"Manifest section must be a dictionary: {section}"
            )

        for path_text in entries:
            yield Path(path_text)


def assert_manifest_paths_exist(manifest: dict) -> None:
    missing_paths = [
        path
        for path in iter_manifest_referenced_paths(manifest)
        if not path.exists()
    ]

    if missing_paths:
        missing_text = "\n".join(str(path) for path in missing_paths)
        raise FileNotFoundError(
            "Manifest-referenced artifacts are missing:\n"
            f"{missing_text}"
        )


def build_final_manifest(
    execution_manifest: dict,
    execution_manifest_path: Path,
    validation_artifact_path: Path,
    package_id: str,
    package_version: str,
    release_id: str,
    run_results_dir: Path,
) -> dict:
    validation_status = parse_validation_status(validation_artifact_path)

    if validation_status != "PASS":
        raise RuntimeError(
            f"Cannot finalize run with validation_status={validation_status}"
        )

    finalization_timestamp = datetime.now(
        timezone.utc
    ).isoformat(timespec="seconds")

    execution_files = {
        str(execution_manifest_path): sha256_file(execution_manifest_path)
    }

    validation_files = {
        str(validation_artifact_path): sha256_file(validation_artifact_path)
    }

    return {
        "run_id": execution_manifest.get("run_id", ""),
        "phenotype": execution_manifest.get("phenotype", ""),
        "package_id": package_id,
        "package_version": package_version,
        "release_id": release_id,
        "run_status": "COMPLETE",
        "validation_status": validation_status,
        "authoritative_run_directory": str(run_results_dir),
        "execution_manifest": str(execution_manifest_path),
        "validation_artifact": str(validation_artifact_path),
        "execution_generated_at": execution_manifest.get("generated_at", ""),
        "finalization_timestamp": finalization_timestamp,
        "config_file": execution_manifest.get("config_file", ""),
        "phenotype_config_file": execution_manifest.get(
            "phenotype_config_file",
            "",
        ),
        "source_manifest_file": execution_manifest.get(
            "source_manifest_file",
            "",
        ),
        "source_manifest_hash": execution_manifest.get(
            "source_manifest_hash",
            "",
        ),
        "input_files": execution_manifest.get("input_files", {}),
        "output_files": execution_manifest.get("output_files", {}),
        "execution_files": execution_files,
        "validation_files": validation_files,
        "software_versions": execution_manifest.get(
            "software_versions",
            {},
        ),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Finalize a completed GSC run."
    )
    parser.add_argument("--config", default="config/config.yaml")
    parser.add_argument("--phenotype", required=True)
    parser.add_argument("--phenotype-config", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--package-id", default=None)
    parser.add_argument("--release-id", default="")

    args = parser.parse_args()

    project_config = load_project_config(args.config)
    phenotype_config = load_phenotype_config(args.phenotype_config)

    package_id = (
        args.package_id
        if args.package_id
        else phenotype_config["package"]["package_id"]
    )

    package_version = phenotype_config["package"].get("version", "")

    run_dirs = setup_run_dirs(project_config, args.run_id)
    logger = get_logger(
        "step_07_finalize_run",
        run_dirs["logs_dir"] / "step_07_finalize_run.log",
    )

    results_root = Path(project_config["paths"]["results_dir"])

    run_results_dir = (
        results_root
        / "runs"
        / args.run_id
    )

    run_reports_dir = (
        run_results_dir
        / "reports"
        / package_id
    )

    latest_reports_dir = (
        results_root
        / "reports"
        / package_id
    )

    run_reports_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    latest_reports_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    execution_manifest_path = (
        run_reports_dir
        / "run_manifest.yaml"
    )

    validation_artifact_path = (
        run_reports_dir
        / "output_contract_validation.tsv"
    )

    final_manifest_path = (
        run_reports_dir
        / "final_run_manifest.yaml"
    )

    latest_final_manifest_path = (
        latest_reports_dir
        / "final_run_manifest.yaml"
    )

    if not execution_manifest_path.exists():
        raise FileNotFoundError(
            f"Missing execution manifest: {execution_manifest_path}"
        )

    if not validation_artifact_path.exists():
        raise FileNotFoundError(
            f"Missing validation artifact: {validation_artifact_path}"
        )

    execution_manifest = load_yaml(execution_manifest_path)

    assert_manifest_paths_exist(execution_manifest)

    final_manifest = build_final_manifest(
        execution_manifest=execution_manifest,
        execution_manifest_path=execution_manifest_path,
        validation_artifact_path=validation_artifact_path,
        package_id=package_id,
        package_version=package_version,
        release_id=args.release_id,
        run_results_dir=run_results_dir,
    )

    write_yaml(
        final_manifest_path,
        final_manifest,
    )

    shutil.copy2(
        final_manifest_path,
        latest_final_manifest_path,
    )

    logger.info(f"run_id={args.run_id}")
    logger.info(f"phenotype={args.phenotype}")
    logger.info(f"package_id={package_id}")
    logger.info(f"execution_manifest={execution_manifest_path}")
    logger.info(f"validation_artifact={validation_artifact_path}")
    logger.info(f"final_manifest={final_manifest_path}")
    logger.info("run_status=COMPLETE")
    logger.info("validation_status=PASS")

    print("[GSC] finalized run")
    print(f"[GSC] run_id={args.run_id}")
    print(f"[GSC] package_id={package_id}")
    print(f"[GSC] final_manifest={final_manifest_path}")


if __name__ == "__main__":
    main()