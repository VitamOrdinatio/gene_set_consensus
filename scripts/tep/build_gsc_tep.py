#!/usr/bin/env python3

"""
Build a GSC-TEP from an existing GSC release package.

Example
-------

python scripts/tep/build_gsc_tep.py \
    --final-run-manifest \
    results/runs/run_2026_06_17_213318/reports/epilepsy_semantic_gtr_experimental/final_run_manifest.yaml
"""

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from gene_set_consensus.tep.builder import (
    build_and_write_gsc_tep,
    default_output_path,
)

from gene_set_consensus.tep.run_context import load_finalized_run_context

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a GSC-TEP from a finalized GSC run."
    )

    parser.add_argument(
        "--final-run-manifest",
        required=True,
        help=(
            "Path to finalized GSC run manifest "
            "(final_run_manifest.yaml)."
        ),
    )

    parser.add_argument(
        "--output-path",
        default=None,
        help=(
            "Optional explicit output path. "
            "Defaults to results/teps/gsc/<package_id>/gsc_tep.json"
        ),
    )

    parser.add_argument(
        "--validation-state",
        default="candidate",
        help="Validation state to embed in the TEP envelope.",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    run_context = load_finalized_run_context(
        args.final_run_manifest
    )

    output_path = (
        Path(args.output_path)
        if args.output_path
        else default_output_path(
            run_context=run_context,
        )
    )

    written_path = build_and_write_gsc_tep(
        final_run_manifest_path=args.final_run_manifest,
        output_path=output_path,
        validation_state=args.validation_state,
    )

    print()
    print("[GSC-TEP] build successful")

    print(
        "[GSC-TEP] release_id: "
        f"{run_context['release_id']}"
    )

    print(
        "[GSC-TEP] run_id: "
        f"{run_context['run_id']}"
    )

    print(f"[GSC-TEP] output: {written_path}")
    print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())