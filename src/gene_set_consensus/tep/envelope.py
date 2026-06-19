from datetime import datetime, timezone
from typing import Any, Dict


TEP_TYPE = "gsc_tep"
TEP_SCHEMA_VERSION = "0.1"
TEP_SLEEVE_VERSION = "gsc_tep_sleeve_v0.1"
SOURCE_REPOSITORY = "gene_set_consensus"
SOURCE_IDENTITY_SCOPE = ("finalized_gsc_run + package + release + phenotype + gene identity")


def utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp for TEP construction."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalize_release_id_for_tep_id(release_id: str) -> str:
    """Normalize release IDs for deterministic, readable TEP IDs."""
    return (
        release_id.strip()
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("-", "_")
        .replace(".", "_")
    )


def build_tep_id(release_id: str) -> str:
    """Build a deterministic readable TEP identifier for a GSC release."""
    normalized_release_id = normalize_release_id_for_tep_id(release_id)
    return f"gsc_tep_{normalized_release_id}"


def build_envelope(
    run_context: Dict[str, Any],
    validation_state: str = "candidate",
) -> Dict[str, object]:
    """Build the GSC-TEP transport envelope.

    Parameters
    ----------
    run_context:
        Finalized run context loaded from final_run_manifest.yaml.
    validation_state:
        Current validation state for the TEP candidate.

    Returns
    -------
    dict
        JSON-serializable envelope object.
    """
    release_id = str(run_context.get("release_id", "")).strip()
    package_id = str(run_context.get("package_id", "")).strip()
    run_id = str(run_context.get("run_id", "")).strip()

    if not release_id:
        raise ValueError("release_id is required for GSC-TEP envelope construction")

    if not package_id:
        raise ValueError("package_id is required for GSC-TEP envelope construction")

    if not run_id:
        raise ValueError("run_id is required for GSC-TEP envelope construction")

    if not validation_state or not validation_state.strip():
        raise ValueError("validation_state is required for GSC-TEP envelope construction")

    return {
        "tep_id": build_tep_id(release_id),
        "tep_type": TEP_TYPE,
        "tep_schema_version": TEP_SCHEMA_VERSION,
        "tep_sleeve_version": TEP_SLEEVE_VERSION,
        "source_repository": SOURCE_REPOSITORY,
        "source_package_id": package_id,
        "source_package_version": run_context.get("package_version", ""),
        "source_release_id": release_id,
        "source_run_id": run_id,
        "source_phenotype": run_context.get("phenotype", ""),
        "source_identity_scope": SOURCE_IDENTITY_SCOPE,
        "source_final_run_manifest": run_context.get(
            "final_run_manifest_path",
            "",
        ),
        "source_authoritative_run_directory": run_context.get(
            "authoritative_run_directory",
            "",
        ),
        "source_run_status": run_context.get("run_status", ""),
        "source_validation_status": run_context.get("validation_status", ""),
        "source_finalization_timestamp": run_context.get(
            "finalization_timestamp",
            "",
        ),
        "creation_timestamp": utc_timestamp(),
        "validation_state": validation_state,
        "provenance": {
            "producer": SOURCE_REPOSITORY,
            "construction_mode": "producer_side_projection",
            "source_artifacts_authoritative": True,
            "source_state": "finalized_run",
        },
    }