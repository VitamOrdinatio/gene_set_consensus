.PHONY: run-example validate-example test clean-runtime

run-example:
	python run_pipeline.py --config config/config.yaml --phenotype example_phenotype

validate-example:
	python scripts/step_06_validate_outputs.py --config config/config.yaml --phenotype example_phenotype --run-id $$(ls -td data/processed/run_* | head -n 1 | xargs -n1 basename)

test:
	pytest

clean-runtime:
	find logs -mindepth 1 ! -name README.md -exec rm -rf {} +
	find data/interim -mindepth 1 ! -name README.md -exec rm -rf {} +
	find data/processed -mindepth 1 ! -name README.md -exec rm -rf {} +
	find results/tables -mindepth 1 -exec rm -rf {} +
	find results/reports -mindepth 1 -exec rm -rf {} +
