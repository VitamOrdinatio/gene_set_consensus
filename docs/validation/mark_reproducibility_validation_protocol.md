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

commit SHA (provenance):

`5c1b363dae7360226d4ea1284aeb981091c19970`

### Git Checkout

```bash
git checkout 5c1b363dae7360226d4ea1284aeb981091c19970
```

## 5. Create GSC virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 6. Create MARK-local config overrides

We generated local config copies under:

```text
config/local_mark/
├── phenotypes/
├── releases/
└── manifests/
```

These replace:

`/mnt/storage`

with:

`/data/storage/gsc`

This preserves committed repository portability and CI behavior while allowing MARK-specific storage path execution without modifying tracked configuration files.

## 7. Run CI-safe validation

This mostly worked, but make validate-all failed only because the committed source manifests intentionally target Sys76-local `/mnt/storage` paths rather than MARK-local `/data/storage/gsc` paths.

That is expected on MARK.

Conclusion:

```text
Use explicit MARK-local validation commands, not make validate-all, for path-aware MARK execution.
```
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

## Next Steps

Next Before Running Full GSC Releases

Before pipeline execution, we still need to validate/ingest the remaining source classes:

| Source            | Current state                     | Next action                              |
| ----------------- | --------------------------------- | ---------------------------------------- |
| Epi25             | fully rebuilt from raw CSVs       | done                                     |
| Genes4Epilepsy    | copied as TSV                     | inspect schema/path                      |
| MitoCarta         | copied as TSV + raw XLS preserved | inspect schema/path                      |
| GTR epilepsy phenotype extraction      | raw XML staged                    | parse XML → gene measures → gene summary |
| GTR mitochondrial phenotype extraction | raw XML staged                    | parse XML → gene measures → gene summary |

### Recommended task list:
1. inspect Genes4Epilepsy TSV
2. inspect MitoCarta TSV
3. parse GTR XML for epilepsy
4. parse GTR XML for mitochondrial disease
5. summarize both GTR outputs
6. validate local MARK release paths

### Once these steps are done, we can then run:

```bash
python run_pipeline.py --release config/local_mark/releases/epilepsy_semantic_gtr_experimental_v0.1.yaml
python run_pipeline.py --release config/local_mark/releases/dee_semantic_gtr_experimental_v0.1.yaml
python run_pipeline.py --release config/local_mark/releases/nafe_semantic_gtr_experimental_v0.1.yaml
python run_pipeline.py --release config/local_mark/releases/mitochondrial_semantic_gtr_experimental_v0.1.yaml
```

## Source Integrity Verification  (needs details)

```bash
sha256sum /data/storage/gsc/gtr/raw/gtr_ftp.xml.gz
```

## Cross-machine semantic release reproducibility

Get for sys76 and MARK:

- SHA256 outputs
- row counts
- deterministic output confirmation

From mark probe 02 log: 

```text
c598762369f4f59b661ff7c6a5615d02f2aaa79dc1cf6b57aa7cfc92d83b200a  /data/storage/gsc/gtr/raw/gtr_ftp.xml.gz
e458622b81026fd5cc22d0fae29c02d029835acf9c1940773c2cb61706ccd6ac  /data/storage/gsc/gene_sets/epi25/2024/raw/DEE_results_2026_05_06_16_21_39.csv
302027a1be652615a790c2bd8778576320d1e2aac16e904f09a03e24a150d891  /data/storage/gsc/gene_sets/epi25/2024/raw/EPI_results_2026_05_06_16_21_36.csv
4fea70e5a2f6f982cabf842fd826ee017ff4794abc7adb601732dc6198868615  /data/storage/gsc/gene_sets/epi25/2024/raw/GGE_results_2026_05_06_16_21_42.csv
8aa1213234ca4444690d7c99a9e3793539bd09a01b80b17f3eac6368dd2747d7  /data/storage/gsc/gene_sets/epi25/2024/raw/NAFE_results_2026_05_06_16_21_44.csv
6f75544797788c703d91e3272e2353c693d52c982caca969257a791eeaa4f3d0  /data/storage/gsc/gene_sets/genes4epilepsy/genes4epilepsy.tsv
4f3df76724a17ad214efa942482bf72e27ccdb5f5e39eb8a1b5f8c3c7b4f9d2c  /data/storage/gsc/gene_sets/mitocarta/mitocarta_human.tsv
```

---