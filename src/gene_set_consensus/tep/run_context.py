from pathlib import Path
from typing import Any, Dict

import yaml


def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)

    if not isinstance(data, dict):
        raise ValueError(
            f"Expected YAML dictionary in finalized run manifest: {path}"
        )

    return data


def require_value(
    data: Dict[str, Any],
    key: str,
    source_path: Path,
) -> str:
    value = data.get(key)

    if value is None:
        raise ValueError(
            f"Finalized run manifest missing required key '{key}': "
            f"{source_path}"
        )

    value_text = str(value).strip()

    if not value_text:
        raise ValueError(
            f"Finalized run manifest has empty required key '{key}': "
            f"{source_path}"
        )

    return value_text


def load_finalized_run_context(
    final_run_manifest_path: str | Path,
) -> Dict[str, Any]:
    """Load and validate finalized GSC run context.

    Parameters
    ----------
    final_run_manifest_path:
        Path to results/runs/<run_id>/reports/<package_id>/final_run_manifest.yaml.

    Returns
    -------
    dict
        Normalized finalized run context used as the authoritative root for
        GSC-TEP construction.
    """
    manifest_path = Path(final_run_manifest_path)
    if not manifest_path.exists():
        raise FileNotFoundError(
            f"Missing finalized run manifest: {manifest_path}"
        )

    if not manifest_path.is_file():
        raise FileNotFoundError(
            f"Finalized run manifest is not a file: {manifest_path}"
        )

    manifest = load_yaml(manifest_path)

    run_status = require_value(
        manifest,
        "run_status",
        manifest_path,
    )

    validation_status = require_value(
        manifest,
        "validation_status",
        manifest_path,
    )

    if run_status != "COMPLETE":
        raise ValueError(
            f"Finalized run is not COMPLETE: "
            f"{manifest_path} has run_status={run_status}"
        )

    if validation_status != "PASS":
        raise ValueError(
            f"Finalized run did not PASS validation: "
            f"{manifest_path} has validation_status={validation_status}"
        )

    run_id = require_value(
        manifest,
        "run_id",
        manifest_path,
    )

    package_id = require_value(
        manifest,
        "package_id",
        manifest_path,
    )

    phenotype = require_value(
        manifest,
        "phenotype",
        manifest_path,
    )

    authoritative_run_directory = require_value(
        manifest,
        "authoritative_run_directory",
        manifest_path,
    )

    authoritative_run_path = Path(authoritative_run_directory)

    if not authoritative_run_path.exists():
        raise FileNotFoundError(
            f"Authoritative run directory does not exist: "
            f"{authoritative_run_path}"
        )

    if not authoritative_run_path.is_dir():
        raise FileNotFoundError(
            f"Authoritative run path is not a directory: "
            f"{authoritative_run_path}"
        )

    return {
        "final_run_manifest_path": manifest_path.as_posix(),
        "final_run_manifest": manifest,
        "run_id": run_id,
        "phenotype": phenotype,
        "package_id": package_id,
        "package_version": str(
            manifest.get("package_version", "")
        ).strip(),
        "release_id": str(
            manifest.get("release_id", "")
        ).strip(),
        "run_status": run_status,
        "validation_status": validation_status,
        "authoritative_run_directory": authoritative_run_path.as_posix(),
        "finalization_timestamp": str(
            manifest.get("finalization_timestamp", "")
        ).strip(),
    }