.PHONY: \
	test \
	compile \
	validate-releases \
	validate-scoring-profiles \
	validate-source-manifests \
	validate-all \
	run-example \
	run-epilepsy-semantic \
	run-mito-semantic \
	show-epilepsy-consensus \
	show-mito-consensus \
	show-tree \
	clean-runtime

test:
	pytest

compile:
	python -m py_compile $$(find src scripts tests -name "*.py" | tr '\n' ' ')

validate-releases:
	python scripts/validation/validate_release_manifest.py --release config/releases/epilepsy_semantic_gtr_experimental_v0.1.yaml
	python scripts/validation/validate_release_manifest.py --release config/releases/mitochondrial_semantic_gtr_experimental_v0.1.yaml

validate-scoring-profiles:
	python scripts/validation/validate_scoring_profile.py --profile config/scoring_profiles/epilepsy_semantic_v0.1.yaml
	python scripts/validation/validate_scoring_profile.py --profile config/scoring_profiles/mitochondrial_semantic_v0.1.yaml

validate-source-manifests:
	python scripts/validation/validate_source_manifest.py --manifest manifests/sources/epilepsy_manifest.yaml
	python scripts/validation/validate_source_manifest.py --manifest manifests/sources/mitochondrial_manifest.yaml

validate-all: compile validate-releases validate-scoring-profiles validate-source-manifests test

run-example:
	python run_pipeline.py \
		--config config/config.yaml \
		--phenotype example_phenotype \
		--identifier-map data/example/identifier_map.tsv

run-epilepsy-semantic:
	python run_pipeline.py \
		--release config/releases/epilepsy_semantic_gtr_experimental_v0.1.yaml

run-mito-semantic:
	python run_pipeline.py \
		--release config/releases/mitochondrial_semantic_gtr_experimental_v0.1.yaml

show-epilepsy-consensus:
	column -t -s $$'\t' results/tables/epilepsy_semantic_gtr_experimental/consensus_gene_set.tsv | head -n 25

show-mito-consensus:
	column -t -s $$'\t' results/tables/mitochondrial_semantic_gtr_experimental/consensus_gene_set.tsv | head -n 25

show-tree:
	tree -L 4

clean-runtime:
	find logs -mindepth 1 ! -name README.md -exec rm -rf {} +
	find data/interim -mindepth 1 ! -name README.md -exec rm -rf {} +
	find data/processed -mindepth 1 ! -name README.md -exec rm -rf {} +
	find results/tables -mindepth 1 -exec rm -rf {} +
	find results/reports -mindepth 1 -exec rm -rf {} +