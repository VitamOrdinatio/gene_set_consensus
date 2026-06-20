#!/usr/bin/env python

import argparse
import shutil
import sys
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gene_set_consensus.config import load_project_config, load_phenotype_config, resolve_phenotype_config_path
from gene_set_consensus.logging_utils import setup_run_dirs, get_logger
from gene_set_consensus.provenance import (
    build_gene_provenance,
    attach_provenance_ids,
    make_provenance_id,
)
from gene_set_consensus.reporting import write_run_manifest, write_validation_report

def main():
    parser = argparse.ArgumentParser(description="Write final GSC outputs.")
    parser.add_argument("--config", default="config/config.yaml")
    parser.add_argument("--phenotype", required=True)
    parser.add_argument("--phenotype-config", default=None)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--source-manifest", default=None)
    parser.add_argument("--package-id", default=None)
    args = parser.parse_args()
    project_config = load_project_config(args.config)
    phenotype_path = (
        Path(args.phenotype_config)
        if args.phenotype_config
        else resolve_phenotype_config_path(project_config, args.phenotype)
    )
    phenotype_config = load_phenotype_config(phenotype_path)

    phenotype_id = (
        phenotype_config["phenotype"]["phenotype_id"]
    )

    package_id = (
        args.package_id
        if args.package_id
        else phenotype_config["package"]["package_id"]
    )    
    gsc_version = project_config["project"]["version"]
    run_dirs = setup_run_dirs(project_config, args.run_id)
    logger = get_logger(
        "step_05_write_outputs",
        run_dirs["logs_dir"] / "step_05_write_outputs.log"
    )
    normalized_path = run_dirs["interim_dir"] / "normalized_source_records.tsv"
    scored_path = run_dirs["processed_dir"] / "scored_gene_evidence.tsv"
    matrix_path = run_dirs["processed_dir"] / "gene_source_matrix.tsv"
    frequency_path = run_dirs["processed_dir"] / "gene_frequency_table.tsv"
    for path in [normalized_path, scored_path, matrix_path, frequency_path]:
        if not path.exists():
            raise FileNotFoundError(f"Missing required input: {path}")
    normalized_df = pd.read_csv(normalized_path, sep="\t", dtype=str).fillna("")
    scored_df = pd.read_csv(scored_path, sep="\t", dtype=str).fillna("")
    provenance_df = build_gene_provenance(normalized_df)
    source_contributions_df = normalized_df.copy()
    source_contributions_df["gene_id"] = (
        source_contributions_df["gene_id"].fillna("")
    )
    source_contributions_df["normalized_gene_symbol"] = (
        source_contributions_df["normalized_gene_symbol"].fillna("")
    )
    source_contributions_df["provenance_id"] = source_contributions_df.apply(
        lambda row: make_provenance_id(
            row["phenotype"],
            row["gene_id"],
            row["normalized_gene_symbol"],
        ),
        axis=1,
    )

    source_contributions_df = source_contributions_df[
        [
            "provenance_id",
            "phenotype",
            "gene_id",
            "normalized_gene_symbol",
            "source_id",
            "source_name",
            "source_type",
            "source_weight",
            "weight_tier",
            "evidence_semantics",
            "evidence_tier",
            "semantic_channel",
            "scoring_rule_id",
            "input_gene_symbol",
            "mapping_status",
            "evidence_label",
            "source_row_number",
            "source_record_hash",
        ]
    ].rename(
        columns={
            "normalized_gene_symbol": "gene_symbol",
        }
    )

    source_contributions_df = source_contributions_df.sort_values(
        by=[
            "phenotype",
            "gene_symbol",
            "source_id",
            "source_row_number",
        ],
        ascending=[True, True, True, True],
    ).reset_index(drop=True)    
    consensus_df = attach_provenance_ids(scored_df)
    consensus_df["run_id"] = args.run_id
    consensus_df["gsc_version"] = gsc_version
    consensus_df["generated_at"] = pd.Timestamp.now().isoformat(timespec="seconds")
    consensus_df = consensus_df[
        [
            "phenotype",
            "gene_id",
            "gene_symbol",
            "consensus_score",
            "semantic_consensus_score",
            "direct_disease_score",
            "clinical_interpretation_score",
            "contextual_biology_score",
            "utilization_score",
            "exploratory_score",
            "convergence_score",
            "conflict_penalty",
            "source_count",
            "weighted_source_sum",
            "source_list",
            "weight_tier_summary",
            "evidence_semantics_summary",
            "evidence_tier_summary",
            "semantic_channel_summary",
            "mapping_status_summary",
            "scoring_profile",
            "active_score",
            "score_explanation",
            "provenance_id",
            "run_id",
            "gsc_version",
            "generated_at"
        ]
    ]

    results_root = Path(project_config["paths"]["results_dir"])

    run_results_dir = (
        results_root
        / "runs"
        / args.run_id
    )

    run_tables_dir = (
        run_results_dir
        / "tables"
        / package_id
    )

    run_reports_dir = (
        run_results_dir
        / "reports"
        / package_id
    )

    run_tables_dir.mkdir(parents=True, exist_ok=True)
    run_reports_dir.mkdir(parents=True, exist_ok=True)

    tables_dir = results_root / "tables" / package_id
    reports_dir = results_root / "reports" / package_id

    tables_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    tables_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    run_consensus_output = (
        run_tables_dir / "consensus_gene_set.tsv"
    )

    run_provenance_output = (
        run_tables_dir / "gene_provenance.tsv"
    )

    run_source_contributions_output = (
        run_tables_dir / "source_contributions.tsv"
    )

    run_matrix_output = (
        run_tables_dir / "gene_source_matrix.tsv"
    )

    run_frequency_output = (
        run_tables_dir / "gene_frequency_table.tsv"
    )

    run_manifest_output = (
        run_reports_dir / "run_manifest.yaml"
    )

    run_validation_output = (
        run_reports_dir / "validation_report.md"
    )

    matrix_output = tables_dir / "gene_source_matrix.tsv"
    frequency_output = tables_dir / "gene_frequency_table.tsv"
    manifest_output = reports_dir / "run_manifest.yaml"
    validation_output = reports_dir / "validation_report.md"

    consensus_df.to_csv(
        run_consensus_output,
        sep="\t",
        index=False,
    )

    provenance_df.to_csv(
        run_provenance_output,
        sep="\t",
        index=False,
    )

    source_contributions_df.to_csv(
        run_source_contributions_output,
        sep="\t",
        index=False,
    )

    pd.read_csv(
        matrix_path,
        sep="\t",
        dtype=str,
    ).to_csv(
        run_matrix_output,
        sep="\t",
        index=False,
    )

    pd.read_csv(
        frequency_path,
        sep="\t",
        dtype=str,
    ).to_csv(
        run_frequency_output,
        sep="\t",
        index=False,
    )

    write_validation_report(
        run_validation_output,
        phenotype_id,
        consensus_df,
        provenance_df,
    )

    write_run_manifest(
        path=run_manifest_output,
        run_id=args.run_id,
        phenotype=phenotype_id,
        config_file=Path(args.config),
        phenotype_config_file=phenotype_path,
        input_files=[normalized_path, scored_path, matrix_path, frequency_path],
        output_files=[
            run_consensus_output,
            run_provenance_output,
            run_source_contributions_output,
            run_matrix_output,
            run_frequency_output,
            run_validation_output,
        ],        
        status="PASS",
        source_manifest_file=Path(args.source_manifest) if args.source_manifest else None
    )
    
    # Mirror to Latest Layer
    consensus_output = (
        tables_dir / "consensus_gene_set.tsv"
    )

    provenance_output = (
        tables_dir / "gene_provenance.tsv"
    )

    source_contributions_output = (
        tables_dir / "source_contributions.tsv"
    )

    matrix_output = (
        tables_dir / "gene_source_matrix.tsv"
    )

    frequency_output = (
        tables_dir / "gene_frequency_table.tsv"
    )

    manifest_output = (
        reports_dir / "run_manifest.yaml"
    )

    validation_output = (
        reports_dir / "validation_report.md"
    )

    shutil.copy2(
        run_consensus_output,
        consensus_output,
    )

    shutil.copy2(
        run_provenance_output,
        provenance_output,
    )

    shutil.copy2(
        run_source_contributions_output,
        source_contributions_output,
    )

    shutil.copy2(
        run_matrix_output,
        matrix_output,
    )

    shutil.copy2(
        run_frequency_output,
        frequency_output,
    )

    shutil.copy2(
        run_manifest_output,
        manifest_output,
    )

    shutil.copy2(
        run_validation_output,
        validation_output,
    )    
    
    # Log Activity
    logger.info(f"run_id={args.run_id}")
    logger.info(f"phenotype={phenotype_id}")
    logger.info(f"package_id={package_id}")
    logger.info(f"consensus_output={consensus_output}")
    logger.info(f"provenance_output={provenance_output}")
    logger.info(f"source_contributions_output={source_contributions_output}")
    logger.info(f"manifest_output={manifest_output}")
    logger.info(f"validation_output={validation_output}")

if __name__ == "__main__":
    main()
