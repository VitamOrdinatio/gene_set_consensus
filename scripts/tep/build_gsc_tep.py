#!/usr/bin/env python3

"""
Build a GSC-TEP from an existing GSC release package.

Example
-------

python scripts/tep/build_gsc_tep.py \
    --release-id epilepsy_semantic_gtr_experimental

python scripts/tep/build_gsc_tep.py \
    --release-id mitochondrial_semantic_gtr_experimental
"""

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from gene_set_consensus.tep.builder import (  # noqa: E402
    build_and_write_gsc_tep,
    default_output_path,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a GSC-TEP from an existing GSC release package."
    )

    parser.add_argument(
        "--release-id",
        required=True,
        help=(
            "GSC release/package identifier "
            "(e.g. epilepsy_semantic_gtr_experimental)"
        ),
    )

    parser.add_argument(
        "--results-dir",
        default="results",
        help="Root GSC results directory.",
    )

    parser.add_argument(
        "--output-path",
        default=None,
        help=(
            "Optional explicit output path. "
            "Defaults to results/teps/gsc/<release_id>/gsc_tep.json"
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

    output_path = (
        Path(args.output_path)
        if args.output_path
        else default_output_path(
            release_id=args.release_id,
            results_dir=args.results_dir,
        )
    )

    written_path = build_and_write_gsc_tep(
        release_id=args.release_id,
        results_dir=args.results_dir,
        output_path=output_path,
        validation_state=args.validation_state,
    )

    print()
    print("[GSC-TEP] build successful")
    print(f"[GSC-TEP] release_id: {args.release_id}")
    print(f"[GSC-TEP] output: {written_path}")
    print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())