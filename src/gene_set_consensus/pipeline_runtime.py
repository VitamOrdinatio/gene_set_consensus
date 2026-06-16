from pathlib import Path

from gene_set_consensus.config import (
    load_phenotype_config,
    load_release_config,
)


def phenotype_config_path_from_name(phenotype: str) -> str:
    return str(
        Path("config")
        / "phenotypes"
        / f"{phenotype}.yaml"
    )


def resolve_identity_from_phenotype_config(phenotype_config_path: str) -> dict:
    phenotype_config = load_phenotype_config(phenotype_config_path)

    phenotype_id = phenotype_config["phenotype"]["phenotype_id"]
    package_id = phenotype_config["package"]["package_id"]

    return {
        "phenotype_id": phenotype_id,
        "package_id": package_id,
    }


def resolve_execution_args(args):
    if args.release:
        release_config = load_release_config(args.release)
        execution = release_config["execution"]

        phenotype_config = execution["phenotype_config"]
        identity = resolve_identity_from_phenotype_config(
            phenotype_config
        )

        identifier_map = execution.get(
            "identifier_map",
            args.identifier_map,
        )

        source_manifest = execution.get(
            "source_manifest",
            args.source_manifest,
        )

        scoring_profile = execution.get(
            "scoring_profile",
            args.scoring_profile,
        )

        release_id = release_config["release"].get(
            "release_id",
            "",
        )

    else:
        if not args.phenotype:
            raise ValueError(
                "Either --phenotype or --release is required"
            )

        phenotype_config = phenotype_config_path_from_name(
            args.phenotype
        )

        identity = resolve_identity_from_phenotype_config(
            phenotype_config
        )

        identifier_map = args.identifier_map
        source_manifest = args.source_manifest
        scoring_profile = args.scoring_profile
        release_id = ""

    return {
        "phenotype": identity["phenotype_id"],
        "phenotype_id": identity["phenotype_id"],
        "package_id": identity["package_id"],
        "phenotype_config": phenotype_config,
        "identifier_map": identifier_map,
        "source_manifest": source_manifest,
        "scoring_profile": scoring_profile,
        "release_id": release_id,
    }