from pathlib import Path

from gene_set_consensus.config import load_release_config

def phenotype_from_config_path(path):
    return Path(path).stem

def resolve_execution_args(args):
    if args.release:
        release_config = load_release_config(args.release)
        execution = release_config["execution"]
        phenotype = phenotype_from_config_path(execution["phenotype_config"])
        identifier_map = execution.get("identifier_map", args.identifier_map)
        source_manifest = execution.get("source_manifest", args.source_manifest)
        scoring_profile = execution.get("scoring_profile", args.scoring_profile)
        release_id = release_config["release"].get("release_id", "")
    else:
        if not args.phenotype:
            raise ValueError("Either --phenotype or --release is required")
        phenotype = args.phenotype
        identifier_map = args.identifier_map
        source_manifest = args.source_manifest
        scoring_profile = args.scoring_profile
        release_id = ""

    return {
        "phenotype": phenotype,
        "identifier_map": identifier_map,
        "source_manifest": source_manifest,
        "scoring_profile": scoring_profile,
        "release_id": release_id,
    }
