#!/usr/bin/env python
from pathlib import Path
import argparse
import subprocess
import sys
import hashlib
import pandas as pd

DETERMINISTIC_TABLES = [
    "gene_source_matrix.tsv",
    "gene_frequency_table.tsv",
    "gene_provenance.tsv",
]

CONSENSUS_TABLE = "consensus_gene_set.tsv"
NONDETERMINISTIC_CONSENSUS_COLUMNS = ["run_id", "generated_at"]

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def latest_run_id():
    run_dirs = sorted(Path("data/processed").glob("run_*"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not run_dirs:
        raise RuntimeError("No processed run directories found")
    return run_dirs[0].name

def normalized_consensus_hash(path):
    df = pd.read_csv(path, sep="\t", dtype=str).fillna("")
    keep_cols = [c for c in df.columns if c not in NONDETERMINISTIC_CONSENSUS_COLUMNS]
    df = df[keep_cols]
    payload = df.to_csv(sep="\t", index=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def run_pipeline(config, phenotype, source_manifest, identifier_map):
    cmd = [
        sys.executable,
        "run_pipeline.py",
        "--config",
        config,
        "--phenotype",
        phenotype,
        "--source-manifest",
        source_manifest,
        "--identifier-map",
        identifier_map,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError("Pipeline run failed during reproducibility validation")
    return latest_run_id()

def collect_hashes(phenotype):
    table_dir = Path("results") / "tables" / phenotype
    hashes = {}
    for filename in DETERMINISTIC_TABLES:
        path = table_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing deterministic table: {path}")
        hashes[filename] = sha256_file(path)
    consensus_path = table_dir / CONSENSUS_TABLE
    if not consensus_path.exists():
        raise FileNotFoundError(f"Missing consensus table: {consensus_path}")
    hashes[CONSENSUS_TABLE] = normalized_consensus_hash(consensus_path)
    return hashes

def main():
    parser = argparse.ArgumentParser(description="Validate GSC reproducibility by running the example pipeline twice.")
    parser.add_argument("--config", default="config/config.yaml")
    parser.add_argument("--phenotype", default="example_phenotype")
    parser.add_argument("--source-manifest", default="manifests/sources/example_source_manifest.yaml")
    parser.add_argument("--identifier-map", default="data/example/identifier_map.tsv")
    args = parser.parse_args()

    run_1 = run_pipeline(args.config, args.phenotype, args.source_manifest, args.identifier_map)
    hashes_1 = collect_hashes(args.phenotype)

    run_2 = run_pipeline(args.config, args.phenotype, args.source_manifest, args.identifier_map)
    hashes_2 = collect_hashes(args.phenotype)

    output_path = Path("results") / "reports" / args.phenotype / "reproducibility_validation.tsv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    errors = []
    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("artifact\trun_1_hash\trun_2_hash\tstatus\n")
        for artifact in sorted(hashes_1):
            status = "PASS" if hashes_1[artifact] == hashes_2[artifact] else "FAIL"
            handle.write(f"{artifact}\t{hashes_1[artifact]}\t{hashes_2[artifact]}\t{status}\n")
            if status == "FAIL":
                errors.append(artifact)

    print(f"run_1={run_1}")
    print(f"run_2={run_2}")
    print(f"reproducibility_report={output_path}")

    if errors:
        raise SystemExit(f"Reproducibility validation failed for: {errors}")

    print("Reproducibility validation passed")

if __name__ == "__main__":
    main()
