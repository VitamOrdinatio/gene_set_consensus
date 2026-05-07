#!/usr/bin/env python
from pathlib import Path
import argparse
import yaml

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)

def main():
    parser = argparse.ArgumentParser(description="Validate a GSC release manifest.")
    parser.add_argument("--release", required=True)
    args = parser.parse_args()

    release_path = Path(args.release)
    release = load_yaml(release_path)

    errors = []

    execution = release.get("execution", {})
    phenotype_config_path = Path(execution.get("phenotype_config", ""))
    source_manifest_path = Path(execution.get("source_manifest", ""))
    identifier_map_path = Path(execution.get("identifier_map", ""))

    for label, path in [
        ("phenotype_config", phenotype_config_path),
        ("source_manifest", source_manifest_path),
        ("identifier_map", identifier_map_path),
    ]:
        if not path.exists():
            errors.append(f"Missing {label}: {path}")

    if phenotype_config_path.exists():
        phenotype_config = load_yaml(phenotype_config_path)
        config_sources = {
            src["source_id"]: src
            for src in phenotype_config.get("sources", [])
        }

        for source in release.get("sources", []):
            source_id = source.get("source_id")
            if source_id not in config_sources:
                errors.append(f"Release source_id not found in phenotype config: {source_id}")
                continue

            config_source = config_sources[source_id]

            if float(source.get("source_weight")) != float(config_source.get("source_weight")):
                errors.append(
                    f"Weight mismatch for {source_id}: "
                    f"release={source.get('source_weight')} config={config_source.get('source_weight')}"
                )

            if str(source.get("source_tier")) != str(config_source.get("weight_tier")):
                errors.append(
                    f"Tier mismatch for {source_id}: "
                    f"release={source.get('source_tier')} config={config_source.get('weight_tier')}"
                )

            source_path = Path(source.get("source_path", ""))
            if not source_path.exists():
                errors.append(f"Missing source_path for {source_id}: {source_path}")

    for rule in release.get("rules", []):
        rule_path = Path(rule)
        if not rule_path.exists():
            errors.append(f"Missing rule file: {rule_path}")

    if errors:
        print("RELEASE VALIDATION FAILED")
        for error in errors:
            print(f"ERROR\t{error}")
        raise SystemExit(1)

    print("RELEASE VALIDATION PASSED")
    print(f"release={release_path}")

if __name__ == "__main__":
    main()
