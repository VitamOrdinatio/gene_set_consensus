from datetime import datetime, timezone
from typing import Dict


TEP_TYPE = "gsc_tep"
TEP_SCHEMA_VERSION = "0.1"
TEP_SLEEVE_VERSION = "gsc_tep_sleeve_v0.1"
SOURCE_REPOSITORY = "gene_set_consensus"
SOURCE_IDENTITY_SCOPE = "gsc_release_id + phenotype + gene identity"


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
    )


def build_tep_id(release_id: str) -> str:
    """Build a deterministic readable TEP identifier for a GSC release."""
    normalized_release_id = normalize_release_id_for_tep_id(release_id)
    return f"gsc_tep_{normalized_release_id}_v0_1"


def build_envelope(
    release_id: str,
    validation_state: str = "candidate",
) -> Dict[str, object]:
    """Build the GSC-TEP transport envelope.

    Parameters
    ----------
    release_id:
        GSC release/package identifier.
    validation_state:
        Current validation state for the TEP candidate.

    Returns
    -------
    dict
        JSON-serializable envelope object.
    """
    if not release_id or not release_id.strip():
        raise ValueError("release_id is required for GSC-TEP envelope construction")

    if not validation_state or not validation_state.strip():
        raise ValueError("validation_state is required for GSC-TEP envelope construction")

    return {
        "tep_id": build_tep_id(release_id),
        "tep_type": TEP_TYPE,
        "tep_schema_version": TEP_SCHEMA_VERSION,
        "tep_sleeve_version": TEP_SLEEVE_VERSION,
        "source_repository": SOURCE_REPOSITORY,
        "source_package_id": release_id,
        "source_identity_scope": SOURCE_IDENTITY_SCOPE,
        "creation_timestamp": utc_timestamp(),
        "validation_state": validation_state,
        "provenance": {
            "producer": SOURCE_REPOSITORY,
            "construction_mode": "producer_side_projection",
            "source_artifacts_authoritative": True,
        },
    }