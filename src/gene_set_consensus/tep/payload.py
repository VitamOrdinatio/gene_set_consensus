import csv
from pathlib import Path
from typing import Any, Dict, List

from gene_set_consensus.tep.manifest import get_artifact_path


def _split_pipe_field(value: str | None) -> List[str]:
    if value is None:
        return []

    value = value.strip()

    if not value:
        return []

    return [item.strip() for item in value.split("|") if item.strip()]


def _nullify(value: str | None):
    if value is None:
        return None

    value = value.strip()

    if value == "":
        return None

    return value


def _to_float(value: str | None):
    value = _nullify(value)

    if value is None:
        return None

    try:
        return float(value)
    except ValueError:
        return None


def _to_int(value: str | None):
    value = _nullify(value)

    if value is None:
        return None

    try:
        return int(value)
    except ValueError:
        return None


def _infer_gene_namespace(
    gene_id: str | None,
) -> str:
    gene_id = _nullify(gene_id)

    if gene_id is None:
        return "unresolved"

    if gene_id.startswith("ENSG"):
        return "ensembl_gene"

    return "unknown_namespace"


def _has_multiple_gene_ids(
    gene_id: str | None,
) -> bool:
    gene_id = _nullify(gene_id)

    if gene_id is None:
        return False

    return "|" in gene_id


def build_semantic_prior(
    row: Dict[str, str],
    release_id: str,
    ) -> Dict[str, Any]:
    phenotype = row["phenotype"]
    gene_symbol = row["gene_symbol"]

    gene_id = _nullify(
        row.get("gene_id")
    )

    gene_namespace = (
        _nullify(
            row.get("gene_namespace")
        )
        or _infer_gene_namespace(
            gene_id
        )
    )

    multiple_gene_ids_present = _has_multiple_gene_ids(
        gene_id
    )

    semantic_prior_id = (
        f"{release_id}::"
        f"{phenotype}::"
        f"{gene_namespace}::"
        f"{gene_id}"
    )

    return {
        "semantic_prior_id": semantic_prior_id,
        "identity": {
            "gsc_release_id": release_id,
            "phenotype": row["phenotype"],
            "source_gene_symbol": row["gene_symbol"],
            "source_gene_id": gene_id,
            "source_gene_namespace": gene_namespace,            
            "gene_symbol": row["gene_symbol"],
            "gene_id": gene_id,
            "gene_namespace": gene_namespace,
            "mapping_status": _nullify(
                row.get("mapping_status_summary")
            ),
        },
        "scores": {
            "consensus_score": _to_float(
                row.get("consensus_score")
            ),
            "semantic_consensus_score": _to_float(
                row.get("semantic_consensus_score")
            ),
            "weighted_source_sum": _to_float(
                row.get("weighted_source_sum")
            ),
            "active_score": _nullify(
                row.get("active_score")
            ),
            "scoring_profile": _nullify(
                row.get("scoring_profile")
            ),
        },
        "semantic_channels": {
            "semantic_channel_summary": _split_pipe_field(
                row.get("semantic_channel_summary")
            ),
            "direct_disease_score": _to_float(
                row.get("direct_disease_score")
            ),
            "clinical_interpretation_score": _to_float(
                row.get("clinical_interpretation_score")
            ),
            "contextual_biology_score": _to_float(
                row.get("contextual_biology_score")
            ),
            "utilization_score": _to_float(
                row.get("utilization_score")
            ),
            "exploratory_score": _to_float(
                row.get("exploratory_score")
            ),
            "convergence_score": _to_float(
                row.get("convergence_score")
            ),
            "conflict_penalty": _to_float(
                row.get("conflict_penalty")
            ),
        },
        "source_attribution": {
            "source_count": _to_int(
                row.get("source_count")
            ),
            "source_list": _split_pipe_field(
                row.get("source_list")
            ),
            "evidence_semantics_summary": _split_pipe_field(
                row.get("evidence_semantics_summary")
            ),
            "evidence_tier_summary": _split_pipe_field(
                row.get("evidence_tier_summary")
            ),
            "weight_tier_summary": _split_pipe_field(
                row.get("weight_tier_summary")
            ),
        },
        "provenance": {
            "provenance_id": _nullify(
                row.get("provenance_id")
            ),
            "run_id": _nullify(
                row.get("run_id")
            ),
            "gsc_version": _nullify(
                row.get("gsc_version")
            ),
            "generated_at": _nullify(
                row.get("generated_at")
            ),
        },
        "uncertainty": {
            "mapping_status_summary": _nullify(
                row.get("mapping_status_summary")
            ),
            "mapping_uncertainty_present": multiple_gene_ids_present,
            "nullability_notes": (
                ["multiple_gene_ids_preserved"]
                if multiple_gene_ids_present
                else []
            ),
        },
    }


def build_payload(
    release_id: str,
    manifest: Dict[str, Any],
) -> Dict[str, Any]:
    consensus_path: Path = get_artifact_path(
        manifest,
        "consensus_gene_set",
    )

    semantic_priors: List[Dict[str, Any]] = []

    with consensus_path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:
        reader = csv.DictReader(
            handle,
            delimiter="\t",
        )

        for row in reader:
            semantic_priors.append(
                build_semantic_prior(
                    row,
                    release_id,
                )
            )


    phenotype = None

    if semantic_priors:
        first_prior = semantic_priors[0]
        identity = first_prior.get("identity", {})

        if isinstance(identity, dict):
            phenotype = identity.get("phenotype")


    return {
        "gsc_release_id": release_id,
        "phenotype": phenotype,
        "semantic_prior_count": len(
            semantic_priors
        ),
        "semantic_priors": semantic_priors,
        "source_summary": {},
        "channel_summary": {},
        "uncertainty_summary": {},
        "construction_notes": [
            (
                "Payload projected directly from "
                "consensus_gene_set.tsv"
            )
        ],
    }