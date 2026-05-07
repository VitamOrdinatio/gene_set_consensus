.PHONY: run-example validate-example reproduce test clean-runtime show-consensus show-tree

run-example:
	python run_pipeline.py \
		--config config/config.yaml \
		--phenotype example_phenotype \
		--source-manifest manifests/sources/example_source_manifest.yaml \
		--identifier-map data/example/identifier_map.tsv

validate-example:
	python scripts/step_06_validate_outputs.py \
		--config config/config.yaml \
		--phenotype example_phenotype \
		--run-id $$(ls -td data/processed/run_* | head -n 1 | xargs -n1 basename)

reproduce:
	python scripts/validation/validate_reproducibility.py \
		--config config/config.yaml \
		--phenotype example_phenotype \
		--source-manifest manifests/sources/example_source_manifest.yaml \
		--identifier-map data/example/identifier_map.tsv

test:
	pytest

show-consensus:
	column -t -s $$'\t' results/tables/example_phenotype/consensus_gene_set.tsv

show-tree:
	tree -L 4

clean-runtime:
	find logs -mindepth 1 ! -name README.md -exec rm -rf {} +
	find data/interim -mindepth 1 ! -name README.md -exec rm -rf {} +
	find data/processed -mindepth 1 ! -name README.md -exec rm -rf {} +
	find results/tables -mindepth 1 -exec rm -rf {} +
	find results/reports -mindepth 1 -exec rm -rf {} +


run-mito:
	@echo "Preparing mitochondrial disease execution target"
	@echo "Requires real source files under /mnt/storage"

run-epilepsy:
	@echo "Preparing epilepsy execution target"
	@echo "Requires real source files under /mnt/storage"


validate-releases:
	python scripts/validation/validate_release_manifest.py --release config/releases/epilepsy_gold_bronze_v0.1.yaml
	python scripts/validation/validate_release_manifest.py --release config/releases/mitocarta_only_v0.1.yaml
