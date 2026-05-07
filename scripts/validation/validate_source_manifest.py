#!/usr/bin/env python
from pathlib import Path
import argparse
import yaml

REQUIRED_TOP_LEVEL = [
    "source_id",
    "source_name",
    "source_type",
    "adapter",
]

REQUIRED_PROVENANCE = [
    "provider",
    "acquisition_method",
    "acquisition_date",
    "source_release",
]

REQUIRED_FILE_METADATA = [
    "path",
    "file_format",
]

VALID_ADAPTERS = {
    "generic_gene_list",
    "gtr_panel",
    "mitocarta",
}

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)

def main():
    parser = argparse.ArgumentParser(description="Validate a GSC source manifest.")
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()

    manifest_path = Path(args.manifest)

    if not manifest_path.exists():
        raise SystemExit(f"Manifest not found: {manifest_path}")

    manifest = load_yaml(manifest_path)

    errors = []
    seen_source_ids = set()

    sources = manifest.get("sources", [])

    if not sources:
        errors.append("Manifest contains no sources.")

    for idx, source in enumerate(sources, start=1):
        context = f"source[{idx}]"

        for field in REQUIRED_TOP_LEVEL:
            if field not in source:
                errors.append(f"{context} missing required field: {field}")

        source_id = source.get("source_id")

        if source_id:
            if source_id in seen_source_ids:
                errors.append(f"Duplicate source_id: {source_id}")
            seen_source_ids.add(source_id)

        adapter = source.get("adapter")
        if adapter and adapter not in VALID_ADAPTERS:
            errors.append(f"{context} invalid adapter: {adapter}")

        provenance = source.get("provenance", {})
        for field in REQUIRED_PROVENANCE:
            if field not in provenance:
                errors.append(f"{context} provenance missing field: {field}")

        file_metadata = source.get("file_metadata", {})
        for field in REQUIRED_FILE_METADATA:
            if field not in file_metadata:
                errors.append(f"{context} file_metadata missing field: {field}")

        status = source.get("status", "active")

        source_path = file_metadata.get("path")
        if source_path:
            if not Path(source_path).exists() and status != "planned":
                errors.append(f"{context} source path does not exist: {source_path}")

    if errors:
        print("SOURCE MANIFEST VALIDATION FAILED")
        for error in errors:
            print(f"ERROR\t{error}")
        raise SystemExit(1)

    print("SOURCE MANIFEST VALIDATION PASSED")
    print(f"manifest={manifest_path}")
    print(f"sources={len(sources)}")

if __name__ == "__main__":
    main()
