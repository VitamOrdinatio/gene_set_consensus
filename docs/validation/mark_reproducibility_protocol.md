# GSC MARK Reproducibility Protocol 

**Completed So Far**

## 0. Upload source files to MARK

Files were uploaded under:

`/root/Desktop/gsc/source_files/`

With this structure:

```text
/root/Desktop/gsc/source_files/
├── epi25/
│   ├── DEE_results_2026_05_06_16_21_39.csv
│   ├── EPI_results_2026_05_06_16_21_36.csv
│   ├── GGE_results_2026_05_06_16_21_42.csv
│   └── NAFE_results_2026_05_06_16_21_44.csv
├── genes4epilepsy/
│   └── genes4epilepsy.tsv
├── gtr/
│   └── gtr_ftp.xml.gz
└── mitocarta/
    ├── Human.MitoCarta3.0.xls
    └── mitocarta_human.tsv
```

## 1. MARK reconnaissance

Confirmed:

```text
Debian 12
Python 3.11.2
Git available
Make available
/data/storage writable
/mnt/storage reserved for VAP
256 GiB RAM
~2.2 TB free disk
```

Decision:

```text
Use /data/storage/gsc for GSC.
Do not touch /mnt/storage.
```

## 2. Create isolated GSC storage tree

```bash
mkdir -p /data/storage/gsc/gtr/raw
mkdir -p /data/storage/gsc/gtr/processed
mkdir -p /data/storage/gsc/gene_sets/epi25/2024/raw
mkdir -p /data/storage/gsc/gene_sets/epi25/2024/processed
mkdir -p /data/storage/gsc/gene_sets/genes4epilepsy
mkdir -p /data/storage/gsc/gene_sets/mitocarta/raw
mkdir -p /data/storage/gsc/gene_sets/mitocarta/processed
mkdir -p /data/storage/gsc/gene_sets/gtr_epilepsy/processed
mkdir -p /data/storage/gsc/gene_sets/gtr_mitochondria/processed
```

## 3. Copy uploaded source files into GSC storage

```bash
cp /root/Desktop/gsc/source_files/gtr/gtr_ftp.xml.gz /data/storage/gsc/gtr/raw/gtr_ftp.xml.gz

cp /root/Desktop/gsc/source_files/epi25/*.csv /data/storage/gsc/gene_sets/epi25/2024/raw/

cp /root/Desktop/gsc/source_files/genes4epilepsy/genes4epilepsy.tsv \
  /data/storage/gsc/gene_sets/genes4epilepsy/genes4epilepsy.tsv

cp /root/Desktop/gsc/source_files/mitocarta/Human.MitoCarta3.0.xls \
  /data/storage/gsc/gene_sets/mitocarta/raw/Human.MitoCarta3.0.xls

cp /root/Desktop/gsc/source_files/mitocarta/mitocarta_human.tsv \
  /data/storage/gsc/gene_sets/mitocarta/mitocarta_human.tsv

cp /root/Desktop/gsc/source_files/mitocarta/mitocarta_human.tsv \
  /data/storage/gsc/gene_sets/mitocarta/processed/mitocarta_human.tsv
```

## 4. Clone GSC on MARK

```bash
mkdir -p /root/dev/portfolio_projects
cd /root/dev/portfolio_projects
git clone git@github.com:VitamOrdinatio/gene_set_consensus.git
cd gene_set_consensus
```

### Inspect commit SHA:

```bash
git rev-parse HEAD
```

Result (commit SHA provenance):

```text
416645a551b4a7ac9af1aa8229ec6d817869e932
```

### Git Checkout

```bash
git checkout 416645a551b4a7ac9af1aa8229ec6d817869e932
```

---

## 5. Create GSC virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

```bash
which python
python --version
```

Result:

```text
/root/dev/portfolio_projects/gene_set_consensus/.venv/bin/python
Python 3.11.2
```

```bash
pip list
```

Result:

```text
Package           Version
----------------- -----------
anyio             4.13.0
biothings_client  0.5.0
certifi           2026.4.22
h11               0.16.0
httpcore          1.0.9
httpx             0.28.1
idna              3.14
iniconfig         2.3.0
mygene            3.2.2
numpy             2.4.4
packaging         26.2
pandas            3.0.3
pip               26.1.1
pluggy            1.6.0
Pygments          2.20.0
pytest            9.0.3
python-dateutil   2.9.0.post0
PyYAML            6.0.3
setuptools        66.1.1
six               1.17.0
typing_extensions 4.15.0
```

---

## 6. Create MARK-local config overrides

MARK uses `/data/storage/gsc/` for GSC source data. The committed repository configs intentionally target the Sys76-local `/mnt/storage/` layout, so MARK requires local runtime overlays.

Do **not** commit `config/local_mark/` to Git. These files are machine-local execution overlays generated from tracked repository configs.

Instead, generate MARK-local overlays using the following helper script:

```bash
mkdir -p config/local_mark/phenotypes
mkdir -p config/local_mark/releases
mkdir -p config/local_mark/manifests

python - <<'PY'
from pathlib import Path

local_root = Path("config/local_mark")
(local_root / "phenotypes").mkdir(parents=True, exist_ok=True)
(local_root / "releases").mkdir(parents=True, exist_ok=True)
(local_root / "manifests").mkdir(parents=True, exist_ok=True)

files = [
    Path("config/phenotypes/epilepsy_semantic_gtr_experimental.yaml"),
    Path("config/phenotypes/dee_semantic_gtr_experimental.yaml"),
    Path("config/phenotypes/nafe_semantic_gtr_experimental.yaml"),
    Path("config/phenotypes/mitochondrial_semantic_gtr_experimental.yaml"),
    Path("config/releases/epilepsy_semantic_gtr_experimental_v0.1.yaml"),
    Path("config/releases/dee_semantic_gtr_experimental_v0.1.yaml"),
    Path("config/releases/nafe_semantic_gtr_experimental_v0.1.yaml"),
    Path("config/releases/mitochondrial_semantic_gtr_experimental_v0.1.yaml"),
    Path("manifests/sources/epilepsy_manifest.yaml"),
    Path("manifests/sources/mitochondrial_manifest.yaml"),
]

for src in files:
    text = src.read_text()
    text = text.replace("/mnt/storage/gene_sets", "/data/storage/gsc/gene_sets")
    text = text.replace("/mnt/storage/gtr", "/data/storage/gsc/gtr")

    if src.parts[0] == "config" and src.parts[1] == "phenotypes":
        out = local_root / "phenotypes" / src.name
    elif src.parts[0] == "config" and src.parts[1] == "releases":
        out = local_root / "releases" / src.name
        text = text.replace("config/phenotypes/", "config/local_mark/phenotypes/")
        text = text.replace("manifests/sources/", "config/local_mark/manifests/")
    elif src.parts[0] == "manifests":
        out = local_root / "manifests" / src.name
    else:
        raise RuntimeError(f"Unhandled path: {src}")

    out.write_text(text)
    print(f"wrote {out}")
PY
```

Expected overlay structure:

```text
config/local_mark/
├── phenotypes/
├── releases/
└── manifests/
```

Verify that local overlays point to `/data/storage/gsc/`:

```bash
grep -R "/data/storage/gsc" -n config/local_mark | head -n 40
grep -R "/mnt/storage" -n config/local_mark || true
```

Expected result:

```text
/data/storage/gsc paths are present.
No /mnt/storage paths remain in config/local_mark.
```

WARNING:

The committed repository manifests and release files intentionally target Sys76-local `/mnt/storage` paths and are expected to fail on MARK without local overlay replacement.

MARK execution MUST use:

`config/local_mark/`

for proper release, phenotype, and manifest overlays.


---

## 7. Validation strategy on MARK

This mostly worked, but make validate-all failed only because the committed source manifests intentionally target Sys76-local `/mnt/storage` paths rather than MARK-local `/data/storage/gsc` paths.

That is expected on MARK.

Conclusion:

```text
Use explicit MARK-local validation commands, not make validate-all, for path-aware MARK execution.
```

---

## 8. Epi25 multi-stage reconstruction pipeline — successful

Executed in three distinct stages:

| Stage | Function                              |
| ----- | ------------------------------------- |
| 1     | browser burden ingestion              |
| 2     | candidate gene set construction       |
| 3     | publication-anchored phenotype rollup |


### 8.1 Browser Burden: Epi25

```bash
python scripts/ingest/ingest_epi25_browser_gene_burden.py \
  --raw-dir /data/storage/gsc/gene_sets/epi25/2024/raw \
  --processed-dir /data/storage/gsc/gene_sets/epi25/2024/processed
```

Generated:

```text
epi25_2024_browser_burden_long.tsv
epi25_2024_exomewide_ptv_core.tsv
epi25_2024_candidates_ranked.tsv
```

### 8.2 Candidate Gene Set Construction: Epi25

```bash
python scripts/ingest/build_epi25_gene_sets.py \
  --input /data/storage/gsc/gene_sets/epi25/2024/processed/epi25_2024_browser_burden_long.tsv \
  --rules config/rules/epi25_rules.yaml \
  --output-dir /data/storage/gsc/gene_sets/epi25/2024/processed
```

Generated:

```text
epi25_2024_browser_exomewide_ptv.tsv
epi25_2024_browser_strong_candidate.tsv
epi25_2024_browser_exploratory_candidate.tsv
epi25_2024_browser_gene_set_build_summary.tsv
```

### 8.3 Publication-Anchored Phenotype Rollup: Epi25

```bash
python scripts/ingest/build_epi25_high_confidence_sets.py \
  --browser-core /data/storage/gsc/gene_sets/epi25/2024/processed/epi25_2024_browser_exomewide_ptv.tsv \
  --publication-joint data/metadata/epi25/epi25_2024_publication_joint_high_confidence.tsv \
  --symbol-map data/metadata/epi25/epi25_2024_high_confidence_ensembl_symbol_map.tsv \
  --rollups config/rules/epi25_rollups.yaml \
  --output-dir /data/storage/gsc/gene_sets/epi25/2024/processed
```

Generated:

```text
epi25_2024_epi_high_confidence.tsv
epi25_2024_dee_high_confidence.tsv
epi25_2024_nafe_high_confidence.tsv
epi25_2024_high_confidence_long.tsv
epi25_2024_high_confidence_summary.tsv
```

## 9. Epi25 invariant validation — successful

MARK independently reconstructed the expected publication-grounded subtype partitioning:

DEE ∪ NAFE = EPI
DEE ∩ NAFE = ∅

This validates deterministic phenotype rollup behavior across independent systems.

Confirmed:

```text
EPI = 7 genes
DEE = 5 genes
NAFE = 2 genes
DEE ∪ NAFE = EPI
DEE ∩ NAFE = empty
GGE = no high-confidence release
```

This is the strongest reproducibility result so far.

## 10. Source integrity verification — successful

Source checksums captured on MARK:

```text
c598762369f4f59b661ff7c6a5615d02f2aaa79dc1cf6b57aa7cfc92d83b200a  /data/storage/gsc/gtr/raw/gtr_ftp.xml.gz
e458622b81026fd5cc22d0fae29c02d029835acf9c1940773c2cb61706ccd6ac  /data/storage/gsc/gene_sets/epi25/2024/raw/DEE_results_2026_05_06_16_21_39.csv
302027a1be652615a790c2bd8778576320d1e2aac16e904f09a03e24a150d891  /data/storage/gsc/gene_sets/epi25/2024/raw/EPI_results_2026_05_06_16_21_36.csv
4fea70e5a2f6f982cabf842fd826ee017ff4794abc7adb601732dc6198868615  /data/storage/gsc/gene_sets/epi25/2024/raw/GGE_results_2026_05_06_16_21_42.csv
8aa1213234ca4444690d7c99a9e3793539bd09a01b80b17f3eac6368dd2747d7  /data/storage/gsc/gene_sets/epi25/2024/raw/NAFE_results_2026_05_06_16_21_44.csv
6f75544797788c703d91e3272e2353c693d52c982caca969257a791eeaa4f3d0  /data/storage/gsc/gene_sets/genes4epilepsy/genes4epilepsy.tsv
4f3df76724a17ad214efa942482bf72e27ccdb5f5e39eb8a1b5f8c3c7b4f9d2c  /data/storage/gsc/gene_sets/mitocarta/mitocarta_human.tsv
```

GTR gzip integrity was also validated:

```bash
gzip -t /data/storage/gsc/gtr/raw/gtr_ftp.xml.gz
```

Result:
`gzip_integrity_ok`

---

## 11. Curated source inspection — successful

### 11.1 Genes4Epilepsy

```text
path=/data/storage/gsc/gene_sets/genes4epilepsy/genes4epilepsy.tsv
rows=1078
columns=gene_id,gene_symbol
```

### 11.2 MitoCarta

```text
path=/data/storage/gsc/gene_sets/mitocarta/mitocarta_human.tsv
rows=1136
```

MitoCarta TSV preserved MitoCarta3.0 metadata, including human gene IDs, symbols, descriptions, MitoCarta evidence, submitochondrial localization, and MitoPathway annotations.

---

## 12. GTR XML parsing and summarization — successful

### 12.1 Epilepsy phenotype extraction

```bash
python scripts/ingest/parse_gtr_xml_gene_measures.py \
  --xml /data/storage/gsc/gtr/raw/gtr_ftp.xml.gz \
  --rules config/rules/gtr_epilepsy_terms.yaml \
  --output /data/storage/gsc/gene_sets/gtr_epilepsy/processed/gtr_epilepsy_gene_measures.tsv
```

Result:

```text
rows=201737
unique_genes=3325
runtime≈4m21s
```

Then summarized:

```bash
python scripts/ingest/summarize_gtr_gene_evidence.py \
  --input /data/storage/gsc/gene_sets/gtr_epilepsy/processed/gtr_epilepsy_gene_measures.tsv \
  --output /data/storage/gsc/gene_sets/gtr_epilepsy/processed/gtr_epilepsy_gene_summary.tsv \
  --source-id gtr_epilepsy_gene_summary \
  --source-name GTR_Epilepsy \
  --source-tier silver
```

Result:

```text
summary_rows=3320
```

### 12.2 Mitochondrial phenotype extraction

```bash
python scripts/ingest/parse_gtr_xml_gene_measures.py \
  --xml /data/storage/gsc/gtr/raw/gtr_ftp.xml.gz \
  --rules config/rules/gtr_mitochondrial_terms.yaml \
  --output /data/storage/gsc/gene_sets/gtr_mitochondria/processed/gtr_mitochondria_gene_measures.tsv
```

Result:

```text
rows=176394
unique_genes=2813
runtime≈4m54s
```

Then summarized:

```bash
python scripts/ingest/summarize_gtr_gene_evidence.py \
  --input /data/storage/gsc/gene_sets/gtr_mitochondria/processed/gtr_mitochondria_gene_measures.tsv \
  --output /data/storage/gsc/gene_sets/gtr_mitochondria/processed/gtr_mitochondria_gene_summary.tsv \
  --source-id gtr_mitochondrial_gene_summary \
  --source-name GTR_Mitochondria \
  --source-tier silver
```

Result:

```text
summary_rows=2749
```

## 13. MARK-local release validation — successful

Validated all MARK-local release manifests after Epi25, Genes4Epilepsy, MitoCarta, and GTR outputs exist:

```bash
python scripts/validation/validate_release_manifest.py \
  --release config/local_mark/releases/epilepsy_semantic_gtr_experimental_v0.1.yaml

python scripts/validation/validate_release_manifest.py \
  --release config/local_mark/releases/dee_semantic_gtr_experimental_v0.1.yaml

python scripts/validation/validate_release_manifest.py \
  --release config/local_mark/releases/nafe_semantic_gtr_experimental_v0.1.yaml

python scripts/validation/validate_release_manifest.py \
  --release config/local_mark/releases/mitochondrial_semantic_gtr_experimental_v0.1.yaml
```

Result:

```text
All passed
```

Validated MARK-local source manifests:

```bash
python scripts/validation/validate_source_manifest.py \
  --manifest config/local_mark/manifests/epilepsy_manifest.yaml

python scripts/validation/validate_source_manifest.py \
  --manifest config/local_mark/manifests/mitochondrial_manifest.yaml
```

Results:

```text
epilepsy sources=6
mitochondrial sources=4
```

Validated scoring profiles:

```bash
python scripts/validation/validate_scoring_profile.py \
  --profile config/scoring_profiles/epilepsy_semantic_v0.1.yaml

python scripts/validation/validate_scoring_profile.py \
  --profile config/scoring_profiles/mitochondrial_semantic_v0.1.yaml
```

Results:

```text
Both passed.
```

---

## 14. Runtime Portability Refactor

Initial MARK release execution exposed a runtime portability issue: release manifests carried explicit `phenotype_config` paths, but `run_pipeline.py` propagated only the phenotype ID to downstream steps. The step scripts then reconstructed phenotype config paths under `config/phenotypes/`, which broke MARK-local execution.

The fix was implemented on Sys76 and pushed to GitHub:

```text
release → explicit phenotype_config path → propagated through run_pipeline.py → honored by step scripts
```

This refactor decoupled phenotype identity from phenotype config file location.

After the patch, MARK correctly used:

```text
config/local_mark/phenotypes/...
```

rather than:

```text
config/phenotypes/...
```

## 14.1 Pull runtime portability refactor onto MARK

After the runtime portability refactor was implemented and pushed from Sys76, MARK synchronized to the updated repository state:

```bash
cd /root/dev/portfolio_projects/gene_set_consensus
git pull --ff-only
```

Post-pull commit provenance:

```bash
git rev-parse HEAD
```

Result (commit SHA provenance):

```text
416645a551b4a7ac9af1aa8229ec6d817869e932
```

This updated MARK to the portability-enabled release runtime architecture.

The portability refactor modified:

```text
src/gene_set_consensus/pipeline_runtime.py
run_pipeline.py
scripts/step_01_validate_inputs.py
scripts/step_02_normalize_genes.py
scripts/step_04_score_consensus.py
scripts/step_05_write_outputs.py
scripts/step_06_validate_outputs.py
```

---

## 15. Full semantic release execution on MARK — successful

After pulling the runtime portability refactor on MARK, all four semantic releases executed successfully.

Final semantic outputs were written under:

```text
results/tables/
results/reports/
```

Important note regarding EPI, DEE and NAFE phenotypes:

> Although DEE and NAFE use smaller direct-disease anchor sets, all epilepsy-family releases operate over the same normalized candidate universe derived from integrated semantic evidence sources. The subtype-specific releases alter semantic weighting and provenance layering rather than restricting the candidate gene universe itself.

### 15.1 Epilepsy semantic release

```bash
python run_pipeline.py \
  --release config/local_mark/releases/epilepsy_semantic_gtr_experimental_v0.1.yaml
```

Result:

```text
phenotype_config=config/local_mark/phenotypes/epilepsy_semantic_gtr_experimental.yaml
normalized_rows=4405
matrix_rows=3543
frequency_rows=3543
scored_rows=3543
runtime_seconds=8
output_contract_validation=PASS
```

### 15.2 DEE semantic release

```bash
python run_pipeline.py \
  --release config/local_mark/releases/dee_semantic_gtr_experimental_v0.1.yaml
```

Result:

```text
phenotype_config=config/local_mark/phenotypes/dee_semantic_gtr_experimental.yaml
normalized_rows=4403
matrix_rows=3543
frequency_rows=3543
scored_rows=3543
runtime_seconds=9
output_contract_validation=PASS
```

### 15.3 NAFE semantic release

```bash
python run_pipeline.py \
  --release config/local_mark/releases/nafe_semantic_gtr_experimental_v0.1.yaml
```

Result:

```text
phenotype_config=config/local_mark/phenotypes/nafe_semantic_gtr_experimental.yaml
normalized_rows=4400
matrix_rows=3543
frequency_rows=3543
scored_rows=3543
runtime_seconds=8
output_contract_validation=PASS
```

### 15.4 Mitochondrial semantic release

```bash
python run_pipeline.py \
  --release config/local_mark/releases/mitochondrial_semantic_gtr_experimental_v0.1.yaml
```

Result:

```text
phenotype_config=config/local_mark/phenotypes/mitochondrial_semantic_gtr_experimental.yaml
normalized_rows=3885
matrix_rows=3881
frequency_rows=3881
scored_rows=3881
runtime_seconds=9
output_contract_validation=PASS
```

---

## 16. Final consensus output row counts

```text
results/tables/epilepsy_semantic_gtr_experimental/consensus_gene_set.tsv       rows=3543
results/tables/dee_semantic_gtr_experimental/consensus_gene_set.tsv            rows=3543
results/tables/nafe_semantic_gtr_experimental/consensus_gene_set.tsv           rows=3543
results/tables/mitochondrial_semantic_gtr_experimental/consensus_gene_set.tsv  rows=3881
```

---

## 17. Biological spot checks

### 17.1 Epilepsy release

Selected genes showed expected semantic layering:

```text
DEPDC5   source_count=3  weighted_source_sum=6.0  direct_disease_score=4  utilization_score=1  exploratory_score=0.75
NPRL3    source_count=3  weighted_source_sum=6.0  direct_disease_score=4  utilization_score=1  exploratory_score=0.75
SCN1A    source_count=3  weighted_source_sum=6.0  direct_disease_score=4  utilization_score=1  exploratory_score=0.75
SYNGAP1  source_count=3  weighted_source_sum=6.0  direct_disease_score=4  utilization_score=1  exploratory_score=0.75
POLG     source_count=2  weighted_source_sum=3.0  utilization_score=1  exploratory_score=0.75
```

### 17.2 DEE release

DEE anchor genes were preserved:

```text
NEXMIF
SCN1A
STX1B
SYNGAP1
WDR45
```

Each showed:

```text
source_count=3
weighted_source_sum=6.0
direct_disease_score=4
utilization_score=1
exploratory_score=0.75
```

### 17.3 NAFE release

NAFE anchor genes were preserved:

```text
DEPDC5
NPRL3
```

Each showed:

```text
source_count=3
weighted_source_sum=6.0
direct_disease_score=4
utilization_score=1
exploratory_score=0.75
```

### 17.4 Mitochondrial release

Selected mitochondrial genes showed expected contextual biology and clinical utilization layering:

```text
POLG  source_count=2  weighted_source_sum=5.0  contextual_biology_score=2  utilization_score=1
TWNK  source_count=2  weighted_source_sum=5.0  contextual_biology_score=2  utilization_score=1
CYC1  source_count=1  weighted_source_sum=3.0  contextual_biology_score=2
TFAM  source_count=1  weighted_source_sum=3.0  contextual_biology_score=2
```

---

## 18. MARK output checksums

Representative final MARK output hashes:

```text
5f8806591382f32bb8e8f4c2c3c91fc2508cc0a6edd81105ab02301810669427  results/tables/epilepsy_semantic_gtr_experimental/consensus_gene_set.tsv
0514a5a85338160f507a992e4b8b4333ee0d0c6511a6cbd59614099a3e4e819e  results/tables/dee_semantic_gtr_experimental/consensus_gene_set.tsv
0b4a408afd6bdefa939098d04c1b11fd404f823148a308363ba161b727cd8db0  results/tables/nafe_semantic_gtr_experimental/consensus_gene_set.tsv
e08797e269de86ab9b8aa27f02870cfb4d743ace7950c5304ad1fb1bfbf9e0c6  results/tables/mitochondrial_semantic_gtr_experimental/consensus_gene_set.tsv
```

Note: final output hashes include generated timestamps and run IDs, so byte-identical hashes are not expected across independent runs unless timestamp/run-id normalization is introduced. Row counts, source-specific gene anchors, semantic scores, and output contract validation are the primary reproducibility criteria at this stage.

---

## 19. Runtime Durations Disclaimer

Runtime durations are approximate and hardware-dependent but are included to provide rough operational expectations.

---

## 20. Final validation conclusion

MARK validation demonstrated that GSC can be reconstructed and executed on independent infrastructure using:

- fresh repository clone
- pinned Git commit
- fresh virtual environment
- remapped external storage
- raw Epi25 browser exports
- raw GTR XML
- curated Genes4Epilepsy and MitoCarta source files
- MARK-local release/phenotype/source-manifest overlays
- portable release runtime execution

The validation confirms:

- Epi25 subtype reconstruction is deterministic.
- GTR XML parsing and summarization are reproducible.
- Semantic release execution is portable across systems.
- EPI, DEE, NAFE, and mitochondrial releases produce valid output contracts.
- Subtype-specific semantic anchors are preserved through final scoring outputs.

---