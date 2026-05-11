#!/usr/bin/env python
from pathlib import Path
import argparse
import sys
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gene_set_consensus.config import load_project_config, load_phenotype_config, resolve_phenotype_config_path
from gene_set_consensus.scoring_profiles import load_scoring_profile
from gene_set_consensus.logging_utils import setup_run_dirs, get_logger
from gene_set_consensus.scoring import score_consensus

def main():
    parser = argparse.ArgumentParser(description="Score GSC consensus gene evidence.")
    parser.add_argument("--config", default="config/config.yaml")
    parser.add_argument("--phenotype", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--scoring-profile", default=None)
    args = parser.parse_args()
    project_config = load_project_config(args.config)
    phenotype_path = resolve_phenotype_config_path(project_config, args.phenotype)
    phenotype_config = load_phenotype_config(phenotype_path)
    run_dirs = setup_run_dirs(project_config, args.run_id)
    logger = get_logger(
        "step_04_score_consensus",
        run_dirs["logs_dir"] / "step_04_score_consensus.log"
    )
    input_path = run_dirs["processed_dir"] / "gene_frequency_table.tsv"
    if not input_path.exists():
        raise FileNotFoundError(f"Missing gene frequency table: {input_path}")
    frequency_df = pd.read_csv(input_path, sep="\t", dtype=str).fillna("")
    logger.info(f"run_id={args.run_id}")
    logger.info(f"phenotype={args.phenotype}")
    logger.info(f"input_path={input_path}")
    logger.info(f"scoring_profile={args.scoring_profile if args.scoring_profile else ''}")
    logger.info(f"frequency_rows={len(frequency_df)}")
    scoring_config = phenotype_config["scoring"].copy()

    if args.scoring_profile:
        scoring_profile = load_scoring_profile(args.scoring_profile)
        scoring_config["active_score"] = scoring_profile["profile"]["active_score"]
        scoring_config["scoring_profile"] = scoring_profile["profile"]["profile_id"]

    scored_df = score_consensus(frequency_df, scoring_config)
    output_path = run_dirs["processed_dir"] / "scored_gene_evidence.tsv"
    scored_df.to_csv(output_path, sep="\t", index=False)
    logger.info(f"scored_rows={len(scored_df)}")
    logger.info(f"output_path={output_path}")

if __name__ == "__main__":
    main()
