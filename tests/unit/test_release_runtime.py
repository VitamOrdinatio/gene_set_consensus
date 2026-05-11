from types import SimpleNamespace
import pytest

from gene_set_consensus.pipeline_runtime import (
    phenotype_from_config_path,
    resolve_execution_args,
)

def test_phenotype_from_config_path():
    assert (
        phenotype_from_config_path(
            "config/phenotypes/epilepsy_gold_bronze_gtr_experimental.yaml"
        )
        == "epilepsy_gold_bronze_gtr_experimental"
    )

def test_release_resolves_epilepsy_runtime_inputs():
    args = SimpleNamespace(
        release="config/releases/epilepsy_gold_bronze_gtr_experimental_v0.1.yaml",
        phenotype=None,
        identifier_map="data/example/identifier_map.tsv",
        source_manifest=None,
        scoring_profile=None,
    )

    resolved = resolve_execution_args(args)

    assert resolved["phenotype"] == "epilepsy_gold_bronze_gtr_experimental"
    assert resolved["identifier_map"] == "data/metadata/gene_identifier_maps/epilepsy_identifier_map.tsv"
    assert resolved["source_manifest"] == "manifests/sources/epilepsy_manifest.yaml"
    assert resolved["scoring_profile"] == "config/scoring_profiles/epilepsy_semantic_v0.1.yaml"
    assert resolved["release_id"] == "epilepsy_gold_bronze_gtr_experimental_v0.1"

def test_release_resolves_mitochondrial_runtime_inputs():
    args = SimpleNamespace(
        release="config/releases/mitocarta_gtr_experimental_v0.1.yaml",
        phenotype=None,
        identifier_map="data/example/identifier_map.tsv",
        source_manifest=None,
        scoring_profile=None,
    )

    resolved = resolve_execution_args(args)

    assert resolved["phenotype"] == "mitocarta_gtr_experimental"
    assert resolved["identifier_map"] == "data/example/identifier_map.tsv"
    assert resolved["source_manifest"] == "manifests/sources/mitochondrial_manifest.yaml"
    assert resolved["scoring_profile"] == "config/scoring_profiles/mitochondrial_semantic_v0.1.yaml"
    assert resolved["release_id"] == "mitocarta_gtr_experimental_v0.1"

def test_phenotype_mode_requires_phenotype():
    args = SimpleNamespace(
        release=None,
        phenotype=None,
        identifier_map="data/example/identifier_map.tsv",
        source_manifest=None,
        scoring_profile=None,
    )

    with pytest.raises(ValueError):
        resolve_execution_args(args)

def test_phenotype_mode_remains_backward_compatible():
    args = SimpleNamespace(
        release=None,
        phenotype="example_phenotype",
        identifier_map="data/example/identifier_map.tsv",
        source_manifest=None,
        scoring_profile=None,
    )

    resolved = resolve_execution_args(args)

    assert resolved["phenotype"] == "example_phenotype"
    assert resolved["identifier_map"] == "data/example/identifier_map.tsv"
    assert resolved["source_manifest"] is None
    assert resolved["scoring_profile"] is None
    assert resolved["release_id"] == ""
