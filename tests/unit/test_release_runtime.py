from types import SimpleNamespace
import pytest

from gene_set_consensus.pipeline_runtime import resolve_execution_args


def test_release_resolves_epilepsy_runtime_inputs():
    args = SimpleNamespace(
        release="config/releases/epilepsy_semantic_gtr_experimental_v0.1.yaml",
        phenotype=None,
        identifier_map="data/example/identifier_map.tsv",
        source_manifest=None,
        scoring_profile=None,
    )

    resolved = resolve_execution_args(args)

    assert resolved["phenotype"] == "epilepsy"
    assert resolved["phenotype_id"] == "epilepsy"
    assert resolved["package_id"] == "epilepsy_semantic_gtr_experimental"

def test_release_resolves_mitochondrial_runtime_inputs():
    args = SimpleNamespace(
        release="config/releases/mitochondrial_semantic_gtr_experimental_v0.1.yaml",
        phenotype=None,
        identifier_map="data/example/identifier_map.tsv",
        source_manifest=None,
        scoring_profile=None,
    )

    resolved = resolve_execution_args(args)

    assert resolved["phenotype"] == "mitochondrial_disease"
    assert resolved["phenotype_id"] == "mitochondrial_disease"
    assert resolved["package_id"] == "mitochondrial_semantic_gtr_experimental"

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

    assert resolved["phenotype_id"] == "example_phenotype"
    assert resolved["package_id"] == "example_phenotype"
