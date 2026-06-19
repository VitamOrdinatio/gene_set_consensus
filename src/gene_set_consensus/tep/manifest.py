from pathlib import Path
from typing import Dict, List


REQUIRED_TABLE_ARTIFACTS = {
    "consensus_gene_set": {
        "filename": "consensus_gene_set.tsv",
        "artifact_type": "tsv",
        "semantic_role": "primary_semantic_prior_table",
    },
    "gene_frequency_table": {
        "filename": "gene_frequency_table.tsv",
        "artifact_type": "tsv",
        "semantic_role": "aggregation_support_table",
    },
    "gene_provenance": {
        "filename": "gene_provenance.tsv",
        "artifact_type": "tsv",
        "semantic_role": "source_provenance_table",
    },
    "gene_source_matrix": {
        "filename": "gene_source_matrix.tsv",
        "artifact_type": "tsv",
        "semantic_role": "source_gene_relationship_table",
    },
}


REQUIRED_REPORT_ARTIFACTS = {
    "final_run_manifest": {
        "filename": "final_run_manifest.yaml",
        "artifact_type": "yaml",
        "semantic_role": "authoritative_finalized_run_context",
    },
    "output_contract_validation": {
        "filename": "output_contract_validation.tsv",
        "artifact_type": "tsv",
        "semantic_role": "output_contract_validation",
    },
    "validation_report": {
        "filename": "validation_report.md",
        "artifact_type": "md",
        "semantic_role": "human_readable_validation_report",
    },
}


def _artifact_record(
    artifact_id: str,
    artifact_type: str,
    artifact_path: Path,
    semantic_role: str,
) -> Dict[str, str]:
    return {
        "artifact_id": artifact_id,
        "artifact_type": artifact_type,
        "artifact_path": artifact_path.as_posix(),
        "semantic_role": semantic_role,
        "producer_ownership": "gene_set_consensus",
    }


def _require_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing required GSC-TEP source artifact: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"GSC-TEP source artifact is not a file: {path}")


def build_manifest(
    run_context: Dict[str, object],
) -> Dict[str, object]:
    """Build the source artifact manifest for a GSC-TEP.

    Parameters
    ----------
    run_context:
        Finalized run context loaded from
        final_run_manifest.yaml.

    Returns
    -------
    dict
        JSON-serializable manifest object.
    """

    authoritative_run_directory = Path(
        str(run_context["authoritative_run_directory"])
    )

    package_id = str(
        run_context["package_id"]
    )

    tables_dir = (
        authoritative_run_directory
        / "tables"
        / package_id
    )

    reports_dir = (
        authoritative_run_directory
        / "reports"
        / package_id
    )

    if not tables_dir.exists():
        raise FileNotFoundError(f"Missing GSC tables directory: {tables_dir}")
    if not reports_dir.exists():
        raise FileNotFoundError(f"Missing GSC reports directory: {reports_dir}")

    artifacts: List[Dict[str, str]] = []

    for artifact_id, spec in REQUIRED_TABLE_ARTIFACTS.items():
        artifact_path = tables_dir / spec["filename"]
        _require_file(artifact_path)
        artifacts.append(
            _artifact_record(
                artifact_id=artifact_id,
                artifact_type=spec["artifact_type"],
                artifact_path=artifact_path,
                semantic_role=spec["semantic_role"],
            )
        )

    for artifact_id, spec in REQUIRED_REPORT_ARTIFACTS.items():
        artifact_path = reports_dir / spec["filename"]
        _require_file(artifact_path)
        artifacts.append(
            _artifact_record(
                artifact_id=artifact_id,
                artifact_type=spec["artifact_type"],
                artifact_path=artifact_path,
                semantic_role=spec["semantic_role"],
            )
        )

    return {
        "run_id": run_context["run_id"],
        "release_id": run_context["release_id"],
        "source_package_id": package_id,
        "authoritative_run_directory": (
            authoritative_run_directory.as_posix()
        ),
        "tables_dir": tables_dir.as_posix(),
        "reports_dir": reports_dir.as_posix(),
        "checksum_authority": {
            "authority_artifact": "final_run_manifest",
            "authority_path": (
                reports_dir / "final_run_manifest.yaml"
            ).as_posix(),
            "hash_algorithm": "sha256",
        },
        "artifacts": artifacts,
    }

def get_artifact_path(manifest: Dict[str, object], artifact_id: str) -> Path:
    """Return an artifact path from a manifest by artifact ID."""
    artifacts = manifest.get("artifacts", [])
    if not isinstance(artifacts, list):
        raise ValueError("Manifest artifacts field is not a list")

    for artifact in artifacts:
        if artifact.get("artifact_id") == artifact_id:
            return Path(str(artifact["artifact_path"]))

    raise KeyError(f"Artifact not found in manifest: {artifact_id}")