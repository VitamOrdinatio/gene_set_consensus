from pathlib import Path
import yaml

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)

def load_source_registry(manifest_path):
    manifest = load_yaml(manifest_path)
    return {
        source["source_id"]: source
        for source in manifest.get("sources", [])
    }

def hydrate_sources(phenotype_sources, manifest_path):
    registry = load_source_registry(manifest_path)

    hydrated = []

    for source in phenotype_sources:

        # legacy fully-expanded config still supported
        if "adapter" in source and "file_path" in source:

            source_id = source.get("source_id")
            registry_source = registry.get(source_id, {})

            hydrated_source = {
                **source,
                "source_gene_namespace": source.get(
                    "source_gene_namespace",
                    registry_source.get(
                        "source_gene_namespace",
                        "unknown_namespace",
                    ),
                ),
                "canonical_gene_namespace": source.get(
                    "canonical_gene_namespace",
                    registry_source.get(
                        "canonical_gene_namespace",
                        "unknown_namespace",
                    ),
                ),
            }

            hydrated.append(hydrated_source)
            continue

        source_id = source.get("source_id")

        if source_id not in registry:
            raise ValueError(f"source_id not found in registry: {source_id}")

        registry_source = registry[source_id]

        hydrated_source = {
            "source_id": source_id,
            "source_name": registry_source["source_name"],
            "source_type": registry_source["source_type"],
            "adapter": registry_source["adapter"],
            "file_path": registry_source["file_metadata"]["path"],
            "gene_column": source.get("gene_column", registry_source.get("gene_column", "gene_symbol")),
            "source_gene_namespace": source.get(
                "source_gene_namespace",
                registry_source.get(
                    "source_gene_namespace",
                    "unknown_namespace",
                ),
            ),
            "canonical_gene_namespace": source.get(
                "canonical_gene_namespace",
                registry_source.get(
                    "canonical_gene_namespace",
                    "unknown_namespace",
                ),
            ),
            "weight_tier": source.get("weight_tier", registry_source.get("weight_tier", registry_source.get("source_tier", ""))),
            "source_weight": source["source_weight"],
        }

        hydrated.append(hydrated_source)

    return hydrated
