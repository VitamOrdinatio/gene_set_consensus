#!/usr/bin/env python

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gene_set_consensus.config import load_phenotype_config, load_project_config
from gene_set_consensus.logging_utils import get_logger, setup_run_dirs
from gene_set_consensus.tep.builder import build_and_write_gsc_tep
from gene_set_consensus.tep.run_context import load_finalized_run_context


def main():
    parser = argparse.ArgumentParser(
        description="Build a GSC-TEP from a finalized GSC run."
    )
    parser.add_argument("--config", default="config/config.yaml")
    parser.add_argument("--phenotype", required=True)
    parser.add_argument("--phenotype-config", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--package-id", default=None)
    parser.add_argument("--validation-state", default="candidate")

    args = parser.parse_args()

    project_config = load_project_config(args.config)
    phenotype_config = load_phenotype_config(args.phenotype_config)

    package_id = (
        args.package_id
        if args.package_id
        else phenotype_config["package"]["package_id"]
    )

    run_dirs = setup_run_dirs(project_config, args.run_id)
    logger = get_logger(
        "step_08_build_tep",
        run_dirs["logs_dir"] / "step_08_build_tep.log",
    )

    results_root = Path(project_config["paths"]["results_dir"])

    final_run_manifest_path = (
        results_root
        / "runs"
        / args.run_id
        / "reports"
        / package_id
        / "final_run_manifest.yaml"
    )

    run_context = load_finalized_run_context(final_run_manifest_path)

    output_path = build_and_write_gsc_tep(
        final_run_manifest_path=final_run_manifest_path,
        validation_state=args.validation_state,
    )

    if not output_path.exists():
        raise FileNotFoundError(
            f"GSC-TEP output was not created: {output_path}"
        )

    logger.info(f"run_id={args.run_id}")
    logger.info(f"phenotype={args.phenotype}")
    logger.info(f"package_id={package_id}")
    logger.info(f"release_id={run_context['release_id']}")
    logger.info(f"final_run_manifest={final_run_manifest_path}")
    logger.info(f"gsc_tep_output={output_path}")
    logger.info("tep_construction_status=PASS")

    print("[GSC-TEP] build successful")
    print(f"[GSC-TEP] run_id: {args.run_id}")
    print(f"[GSC-TEP] package_id: {package_id}")
    print(f"[GSC-TEP] release_id: {run_context['release_id']}")
    print(f"[GSC-TEP] output: {output_path}")


if __name__ == "__main__":
    main()