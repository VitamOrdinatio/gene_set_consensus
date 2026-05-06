from pathlib import Path
import yaml

REQUIRED_SOURCE_MANIFEST_FIELDS = [
    "source_id",
    "source_name",
    "source_type",
    "adapter",
    "biological_context",
    "provenance",
    "file_metadata",
]

def load_source_manifest(path):

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Source manifest not found: {path}"
        )

    with open(path, "r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)

    if "sources" not in data:
        raise ValueError(
            "Manifest missing top-level 'sources'"
        )

    for source in data["sources"]:

        missing = [
            field
            for field in REQUIRED_SOURCE_MANIFEST_FIELDS
            if field not in source
        ]

        if missing:
            raise ValueError(
                f"Manifest source missing fields: {missing}"
            )

    return data

def build_manifest_source_lookup(manifest):

    lookup = {}

    for source in manifest["sources"]:

        lookup[source["source_id"]] = source

    return lookup
