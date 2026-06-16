import json
from pathlib import Path
from typing import Any, Dict

from gene_set_consensus.tep.envelope import build_envelope
from gene_set_consensus.tep.manifest import build_manifest
from gene_set_consensus.tep.payload import build_payload


def build_gsc_tep(
    release_id: str,
    results_dir: str | Path = "results",
    validation_state: str = "candidate",
) -> Dict[str, Any]:
    """Build a complete GSC-TEP object.

    Parameters
    ----------
    release_id:
        GSC release/package identifier.
    results_dir:
        Root GSC results directory.
    validation_state:
        Current validation state for the generated TEP.

    Returns
    -------
    dict
        JSON-serializable GSC-TEP object with envelope, manifest, and payload.
    """
    manifest = build_manifest(
        release_id=release_id,
        results_dir=results_dir,
    )

    envelope = build_envelope(
        release_id=release_id,
        validation_state=validation_state,
    )

    payload = build_payload(
        release_id=release_id,
        manifest=manifest,
    )

    return {
        "envelope": envelope,
        "manifest": manifest,
        "payload": payload,
    }


def default_output_path(
    release_id: str,
    results_dir: str | Path = "results",
) -> Path:
    """Return the default output path for a GSC-TEP JSON file."""
    return (
        Path(results_dir)
        / "teps"
        / "gsc"
        / release_id
        / "gsc_tep.json"
    )


def write_gsc_tep(
    tep: Dict[str, Any],
    output_path: str | Path,
) -> Path:
    """Write a GSC-TEP object to JSON."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as handle:
        json.dump(
            tep,
            handle,
            indent=2,
            sort_keys=True,
        )
        handle.write("\n")

    return path


def build_and_write_gsc_tep(
    release_id: str,
    results_dir: str | Path = "results",
    output_path: str | Path | None = None,
    validation_state: str = "candidate",
) -> Path:
    """Build and write a GSC-TEP JSON file."""
    tep = build_gsc_tep(
        release_id=release_id,
        results_dir=results_dir,
        validation_state=validation_state,
    )

    resolved_output_path = (
        Path(output_path)
        if output_path is not None
        else default_output_path(
            release_id=release_id,
            results_dir=results_dir,
        )
    )

    return write_gsc_tep(
        tep=tep,
        output_path=resolved_output_path,
    )