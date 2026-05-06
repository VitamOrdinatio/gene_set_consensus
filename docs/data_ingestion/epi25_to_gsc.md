# Epi25-to-GSC Build Notes

**Purpose:** summarize how to use Epi25 consortium outputs to build deterministic epilepsy gene sets for the `gene_set_consensus` (GSC) repository.

**Prepared for:** GSC repo development  
**Date:** 2026-05-06  
**Primary source family:** Epi25 Collaborative WES studies and Epi25 WES browser exports

## Terminology:

- **EPI** (Epilepsy cohort): Broad epilepsy case cohort containing all epilepsy patients analyzed together, regardless of subtype classification.
- **DEE** (Developmental and Epileptic Encephalopathy): Severe early-onset epilepsy syndromes where seizures are associated with developmental delay, cognitive impairment, or neurological dysfunction.
- **GGE** (Genetic Generalized Epilepsy): Epilepsy syndromes characterized by generalized seizures thought to arise from widespread genetic network dysfunction rather than focal brain lesions.
- **NAFE** (Non-Acquired Focal Epilepsy): Focal epilepsy without an obvious acquired cause (such as trauma, stroke, or infection), often suspected to have an underlying genetic basis.
- **PTV** (Protein-Truncating Variant): A genetic variant predicted to severely disrupt protein production or generate a shortened, likely nonfunctional protein (e.g., nonsense, frameshift, essential splice-site mutations).

---

## 1. Executive conclusion

The four CSV files downloaded from the Epi25 WES browser are **directly useful for GSC** because they provide gene-level burden statistics for epilepsy case-control comparisons. They should not be treated as a hand-curated epilepsy gene list. Instead, they should be treated as **source evidence tables** from a Gold-tier consortium resource.

Recommended GSC treatment:

```text
gold / consortium source: Epi25
source release: browser export downloaded 2026-05-06
analysis type: gene-level ultra-rare variant burden
phenotype strata: EPI, DEE, GGE, NAFE
variant classes: PTV, damaging missense
```

These CSVs are useful for generating deterministic gene sets such as:

```text
epi25_2024_exomewide_ptv_core
epi25_2024_subthreshold_ptv_candidates
epi25_2024_damaging_missense_candidates
epi25_2024_dee_ptv
epi25_2024_nafe_gator1
epi25_2024_gge_candidate_signal
epi25_2024_any_epilepsy_signal
```

The key transformation is to convert the four wide browser-export files into a single normalized long-format evidence table with phenotype, variant class, counts, p-values, odds ratios, and gene identifiers.

---

## 2. Why Epi25 belongs in GSC Gold

Epi25 is not a typical individual-publication gene list. It is a large international consortium resource built from harmonized whole-exome sequencing, standardized phenotyping, large-scale case-control burden testing, and browser-released summary data.

Therefore, in the GSC provenance hierarchy:

```text
Gold   = consortium-scale resources and large coordinated genetic studies
Silver = individual publications / single-lab or narrower cohort studies
Bronze = mined sources, GTR-derived panels, text-mining, indirect aggregation
```

Epi25 should be classified as:

```text
source_tier = gold
source_type = consortium_wes_burden
source_name = Epi25 Collaborative
```

Important schema distinction:

```text
Gold/Silver/Bronze = provenance tier
core/extended/candidate = biological/evidence-confidence group within a source
```

Do not use “tier” ambiguously for both.

---

## 3. Papers and source relationship

### Epi25 2019 flagship paper

The 2019 Epi25 paper analyzed 9,170 epilepsy cases and 8,436 controls of European ancestry, including DEE, GGE, NAFE, and other epilepsy syndromes. It established that ultra-rare deleterious coding variants are enriched across epilepsy, especially in DEE, and showed strong pathway-level enrichment for GABAergic and ion-channel biology.

The 2019 paper explicitly states that primary gene-based test results and single-variant associations are available through the Epi25 WES browser.

### Epi25 2024 flagship paper

The 2024 Epi25 paper expanded the resource to 20,979 epilepsy cases and 33,444 controls across multiple genetic ancestries. It performed ultra-rare variant burden testing across protein-coding genes and gene sets for all epilepsy combined and major epilepsy subtypes.

The 2024 paper explicitly states that summary-level variant and gene-level data are available in the Epi25 online browser and that full exome-wide burden results are available in Supplementary Data 1 and 4.

### Interpretation for the four CSVs

The four downloaded CSV files are browser exports of the 2024-style gene-level burden results for the following phenotype strata:

```text
EPI  = all epilepsy cases combined
DEE  = developmental and epileptic encephalopathy
GGE  = genetic generalized epilepsy
NAFE = non-acquired focal epilepsy
```

They correspond to the paper-described browser release of gene-level summary data and closely match the gene-burden analyses described in the 2024 paper.

---

## 4. Uploaded browser CSV inventory

| File | Phenotype stratum | Rows | Cases | Controls | Columns |
|---|---:|---:|---:|---:|---|
| `EPI_results_2026_05_06_16_21_36.csv` | EPI | 17544 | 20979 | 33444 | 12 |
| `DEE_results_2026_05_06_16_21_39.csv` | DEE | 17544 | 1938 | 33444 | 12 |
| `GGE_results_2026_05_06_16_21_42.csv` | GGE | 17544 | 5499 | 33444 | 12 |
| `NAFE_results_2026_05_06_16_21_44.csv` | NAFE | 17544 | 9219 | 33444 | 12 |


All four files have the same wide schema:

```text
Gene
Description
Cases
Controls
PTV Case Count
PTV Control Count
PTV p-val
PTV odds ratio
Damaging Missense Case Count
Damaging Missense Control Count
Damaging Missense p-val
Damaging Missense odds ratio
```

Important observation:

```text
Gene = Ensembl gene ID, not HGNC symbol
Description = gene description/name, not reliable as a canonical symbol field
```

Therefore, these files require gene-symbol normalization before final GSC gene-set output.

---

## 5. How the CSVs are useful to GSC

### 5.1 Primary use: evidence tables, not direct final gene sets

The CSVs should be stored as raw source evidence. They are too rich to flatten immediately. They encode:

- phenotype stratum
- variant class
- case/control counts
- burden p-values
- odds ratios
- gene-level identifiers

This supports deterministic filtering and re-filtering as GSC criteria mature.

### 5.2 Generating subtype-specific gene sets

The four files naturally support separate gene sets for:

```text
all epilepsy
DEE
GGE
NAFE
```

This is important because Epi25 shows that epilepsy genetics is subtype-structured. DEE has the strongest single-gene burden signals, NAFE is strongly shaped by GATOR1/mTOR biology, and GGE has more diffuse signals that often do not reach single-gene exome-wide significance.

### 5.3 Generating variant-class-aware gene sets

The CSVs separate:

```text
PTV = protein-truncating variant burden
Damaging Missense = damaging missense burden
```

This matters because different epilepsy genes show different risk architecture. Some genes are PTV/haploinsufficiency-dominant, whereas ion-channel genes often show important damaging missense enrichment.

### 5.4 Scoring and ranking candidate genes

The CSVs support deterministic ranking by:

```text
-p log10(p-value)
odds ratio
case carrier count
case-control enrichment
phenotype recurrence across files
variant-class recurrence
```

However, p-value alone should not be treated as final truth because some sparse events can produce unstable large odds ratios. Gene-set inclusion rules should require count and/or known context filters.

---

## 6. Required transformations

### Transformation 1 — Add source metadata

For every row, add:

```text
source_name = Epi25
source_tier = gold
source_type = consortium_wes_burden
source_release = browser_export_2026_05_06
publication_anchor = Epi25_2024_Nat_Neurosci
browser_export_file = original filename
```

### Transformation 2 — Add phenotype stratum from filename

Map files to phenotype labels:

```text
EPI_results_*.csv  -> phenotype = EPI
DEE_results_*.csv  -> phenotype = DEE
GGE_results_*.csv  -> phenotype = GGE
NAFE_results_*.csv -> phenotype = NAFE
```

### Transformation 3 — Convert wide to long format

Convert each row from this wide structure:

```text
PTV p-val / PTV odds ratio / PTV counts
Damaging Missense p-val / Damaging Missense odds ratio / Damaging Missense counts
```

into two rows:

```text
variant_class = PTV
variant_class = damaging_missense
```

Recommended long-format columns:

```text
ensembl_gene_id
hgnc_symbol
gene_description
phenotype
variant_class
cases
controls
case_count
control_count
p_value
odds_ratio
neg_log10_p
source_name
source_tier
source_release
browser_export_file
notes
```

### Transformation 4 — Normalize gene identifiers

The browser exports use Ensembl IDs in `Gene`. GSC should ultimately expose HGNC symbols as the primary human-readable gene field while preserving Ensembl IDs.

Required mapping:

```text
ENSG -> HGNC approved symbol
ENSG -> Entrez ID, optional
ENSG -> chromosome/location, optional
```

Do not use `Description` as a substitute for HGNC symbol. For example, the CSV description `DEP domain containing 5, GATOR1 subcomplex subunit` corresponds to **DEPDC5**, but the description itself is not the symbol.

### Transformation 5 — Clean p-values

Some browser exports use `0` where the true value is below display/precision range. Convert cautiously:

```text
p_value_raw = original string
p_value_numeric = parsed value when possible
p_value_zero_flag = true if raw value == "0"
```

For ranking, set zero values to a conservative floor only in derived fields, e.g.:

```text
p_value_for_neglog10 = max(parsed_p_value, 1e-300)
```

But preserve the raw value.

### Transformation 6 — Apply deterministic inclusion rules

Recommended first-pass rules:

```text
exomewide_gene_ptv:
    variant_class == PTV
    p_value <= 3.4e-7

strong_candidate_gene:
    p_value <= 1e-5
    case_count >= 3
    odds_ratio > 1

exploratory_candidate_gene:
    p_value <= 1e-3
    case_count >= 5
    odds_ratio > 1
```

Use these labels as evidence classes, not as GSC provenance tiers.

---

## 7. Initial top signals visible in uploaded CSVs

These are browser-export top signals and should be reprocessed after Ensembl-to-HGNC mapping.

### EPI

**PTV top browser rows by p-value:**

| Ensembl ID | Description | Case count | Control count | p-value | Odds ratio |
|---|---|---:|---:|---:|---:|
| ENSG00000100150 | DEP domain containing 5, GATOR1 subcomplex subunit | 66 | 11 | 3.4417e-15 | 8.4971 |
| ENSG00000050030 | neurite extension and migration factor | 22 | 0 | 6.2791e-9 | 63.228 |
| ENSG00000144285 | sodium voltage-gated channel alpha subunit 1 | 27 | 2 | 3.4869e-8 | 14.406 |
| ENSG00000103148 | NPR3 like, GATOR1 complex subunit | 18 | 2 | 0.0000092939 | 11.423 |
| ENSG00000169071 | receptor tyrosine kinase like orphan receptor 2 | 11 | 0 | 0.000081625 | 31.54 |
| ENSG00000005483 | lysine methyltransferase 2E (inactive) | 25 | 10 | 0.000088556 | 4.0767 |

**Damaging Missense top browser rows by p-value:**

| Ensembl ID | Description | Case count | Control count | p-value | Odds ratio |
|---|---|---:|---:|---:|---:|
| ENSG00000166206 | gamma-aminobutyric acid type A receptor subunit beta3 | 32 | 12 | 0.0000068436 | 4.3866 |
| ENSG00000113327 | gamma-aminobutyric acid type A receptor subunit gamma2 | 33 | 13 | 0.000027895 | 3.7104 |
| ENSG00000157103 | solute carrier family 6 member 1 | 30 | 11 | 0.000094924 | 3.6537 |
| ENSG00000144285 | sodium voltage-gated channel alpha subunit 1 | 49 | 37 | 0.00016047 | 2.3513 |
| ENSG00000117394 | solute carrier family 2 member 1 | 38 | 20 | 0.00020775 | 2.5532 |
| ENSG00000122641 | inhibin subunit beta A | 8 | 0 | 0.00031449 | 31.027 |

### DEE

**PTV top browser rows by p-value:**

| Ensembl ID | Description | Case count | Control count | p-value | Odds ratio |
|---|---|---:|---:|---:|---:|
| ENSG00000050030 | neurite extension and migration factor | 15 | 0 | 0 | 774.74 |
| ENSG00000144285 | sodium voltage-gated channel alpha subunit 1 | 9 | 2 | 6.3195e-9 | 62.738 |
| ENSG00000197283 | synaptic Ras GTPase activating protein 1 | 7 | 1 | 5.9462e-8 | 65.103 |
| ENSG00000099365 | syntaxin 1B | 5 | 0 | 2.2855e-7 | 92.809 |
| ENSG00000196998 | WD repeat domain 45 | 5 | 0 | 2.3762e-7 | 249.53 |
| ENSG00000167522 | ankyrin repeat domain containing 11 | 5 | 2 | 0.0000011956 | 50.799 |

**Damaging Missense top browser rows by p-value:**

| Ensembl ID | Description | Case count | Control count | p-value | Odds ratio |
|---|---|---:|---:|---:|---:|
| ENSG00000127663 | lysine demethylase 4B | 9 | 18 | 0.0000066397 | 9.9512 |
| ENSG00000144285 | sodium voltage-gated channel alpha subunit 1 | 11 | 37 | 0.000014439 | 6.5616 |
| ENSG00000073464 | chloride voltage-gated channel 4 | 6 | 14 | 0.000018207 | 12.885 |
| ENSG00000008086 | cyclin dependent kinase like 5 | 6 | 7 | 0.000052751 | 15.498 |
| ENSG00000177565 | TBL1X/Y related 1 | 5 | 2 | 0.000074407 | 22.67 |
| ENSG00000136854 | syntaxin binding protein 1 | 8 | 21 | 0.00008429 | 7.6951 |

### GGE

**PTV top browser rows by p-value:**

| Ensembl ID | Description | Case count | Control count | p-value | Odds ratio |
|---|---|---:|---:|---:|---:|
| ENSG00000139718 | SET domain containing 1B, histone lysine methyltransferase | 5 | 0 | 0.0000061394 | 92.631 |
| ENSG00000112110 | mitochondrial ribosomal protein L18 | 6 | 1 | 0.0000063619 | 34.338 |
| ENSG00000198626 | ryanodine receptor 2 | 14 | 14 | 0.0000086024 | 5.9189 |
| ENSG00000084676 | nuclear receptor coactivator 1 | 7 | 3 | 0.000027515 | 15.408 |
| ENSG00000169071 | receptor tyrosine kinase like orphan receptor 2 | 4 | 0 | 0.000072607 | 64.526 |
| ENSG00000130477 | unc-13 homolog A | 4 | 0 | 0.000096005 | 61.657 |

**Damaging Missense top browser rows by p-value:**

| Ensembl ID | Description | Case count | Control count | p-value | Odds ratio |
|---|---|---:|---:|---:|---:|
| ENSG00000157103 | solute carrier family 6 member 1 | 15 | 11 | 0.0000030095 | 6.6157 |
| ENSG00000117394 | solute carrier family 2 member 1 | 16 | 20 | 0.000056406 | 3.6407 |
| ENSG00000100884 | copine 6 | 3 | 0 | 0.00093091 | 44.5 |
| ENSG00000188582 | progestin and adipoQ receptor family member 9 | 13 | 20 | 0.00094705 | 3.5229 |
| ENSG00000181472 | zinc finger and BTB domain containing 2 | 4 | 1 | 0.0010715 | 18.204 |
| ENSG00000101940 | WD repeat domain 13 | 5 | 3 | 0.0011208 | 11.216 |

### NAFE

**PTV top browser rows by p-value:**

| Ensembl ID | Description | Case count | Control count | p-value | Odds ratio |
|---|---|---:|---:|---:|---:|
| ENSG00000100150 | DEP domain containing 5, GATOR1 subcomplex subunit | 47 | 11 | 0 | 13.209 |
| ENSG00000103148 | NPR3 like, GATOR1 complex subunit | 12 | 2 | 0.0000013519 | 18.262 |
| ENSG00000108231 | leucine rich glioma inactivated 1 | 9 | 1 | 0.000013712 | 21.4 |
| ENSG00000114388 | NPR2 like, GATOR1 complex subunit | 8 | 1 | 0.000036181 | 16.043 |
| ENSG00000171431 | keratin 20 | 0 | 22 | 0.00020717 | 0.038702 |
| ENSG00000108509 | calmodulin binding transcription activator 2 | 11 | 8 | 0.00053076 | 5.2785 |

**Damaging Missense top browser rows by p-value:**

| Ensembl ID | Description | Case count | Control count | p-value | Odds ratio |
|---|---|---:|---:|---:|---:|
| ENSG00000166206 | gamma-aminobutyric acid type A receptor subunit beta3 | 17 | 12 | 0.000041527 | 5.1755 |
| ENSG00000111262 | potassium voltage-gated channel subfamily A member 1 | 15 | 14 | 0.00010731 | 4.5822 |
| ENSG00000196535 | myosin XVIIIA | 0 | 31 | 0.00021468 | 0.042699 |
| ENSG00000174437 | ATPase sarcoplasmic/endoplasmic reticulum Ca2+ transporting 2 | 19 | 19 | 0.00045937 | 3.346 |
| ENSG00000223865 | major histocompatibility complex, class II, DP beta 1 | 3 | 1 | 0.00053374 | 76.946 |
| ENSG00000131473 | ATP citrate lyase | 11 | 9 | 0.00089918 | 4.5958 |



Interpretation caution: these tables are useful for pipeline testing and ranking, but final GSC gene symbols should be generated only after proper Ensembl-to-HGNC mapping.

---

## 8. High-confidence Epi25 2024 gene anchors

The 2024 paper reports exome-wide significant protein-truncating URV burden in:

```text
DEE:  NEXMIF, SCN1A, SYNGAP1, STX1B, WDR45
NAFE: DEPDC5
EPI:  DEPDC5, NEXMIF, SCN1A
```

It also highlights GATOR1 biology:

```text
DEPDC5
NPRL3
NPRL2
```

and damaging missense/channel biology including:

```text
SLC6A1
GABRB3
GABRA1 / GABRB2 / GABRG2-related GABAA receptor biology
SCN2A / SCN8A-related sodium channel biology
```

Recommended GSC products:

```text
epi25_2024_exomewide_ptv_core.tsv
epi25_2024_gator1.tsv
epi25_2024_gabaa_missense_support.tsv
epi25_2024_ion_channel_support.tsv
epi25_2024_all_browser_burden_long.tsv
```

---

## 9. Proposed GSC directory placement

```text
gene_set_consensus/
└── data/
    └── disease/
        └── epilepsy/
            └── gold/
                └── epi25/
                    ├── 2019/
                    │   ├── raw/
                    │   ├── processed/
                    │   └── metadata/
                    └── 2024/
                        ├── raw/
                        │   ├── EPI_results_2026_05_06_16_21_36.csv
                        │   ├── DEE_results_2026_05_06_16_21_39.csv
                        │   ├── GGE_results_2026_05_06_16_21_42.csv
                        │   └── NAFE_results_2026_05_06_16_21_44.csv
                        ├── processed/
                        │   ├── epi25_2024_browser_burden_long.tsv
                        │   ├── epi25_2024_exomewide_ptv_core.tsv
                        │   ├── epi25_2024_gator1.tsv
                        │   ├── epi25_2024_gabaa_missense_support.tsv
                        │   └── epi25_2024_candidates_ranked.tsv
                        └── metadata/
                            ├── source_metadata.yaml
                            ├── transform_notes.md
                            └── column_dictionary.md
```

---

## 10. Deterministic build strategy

### Step 1 — Preserve raw exports

Never edit the raw CSVs. Store them with original filenames and checksums.

### Step 2 — Build long burden table

Use a parser to stack the four files and convert PTV/damaging missense columns into variant-class rows.

### Step 3 — Map gene IDs

Add HGNC symbols using a pinned gene annotation file. Store the annotation source and version.

### Step 4 — Generate evidence classes

Add derived flags:

```text
is_exomewide_gene_ptv
is_strong_candidate
is_exploratory_candidate
is_case_enriched
has_zero_browser_pvalue
```

### Step 5 — Emit gene-set products

Each final gene-set TSV should contain at minimum:

```text
hgnc_symbol
ensembl_gene_id
gene_set_name
disease_context
phenotype
variant_class
evidence_class
source_tier
source_name
source_release
p_value
odds_ratio
case_count
control_count
notes
```

### Step 6 — Add validation checks

Required checks:

```text
No missing Ensembl IDs
No duplicated gene-symbol/phenotype/variant-class rows after normalization
All source files represented
All phenotype labels valid: EPI, DEE, GGE, NAFE
All p-values parse or retain raw parse-failure flag
All final HGNC symbols are approved symbols or explicitly marked alias/unmapped
```

---

## 11. Key design principle for GSC

Do not collapse Epi25 into a single undifferentiated epilepsy gene list.

Instead, GSC should preserve these orthogonal axes:

```text
provenance tier: gold
phenotype: EPI / DEE / GGE / NAFE
variant class: PTV / damaging missense / CNV / GWAS later
evidence class: exomewide / strong_candidate / exploratory
biological module: GATOR1 / GABAA / ion channel / constrained / NDD overlap
```

This design allows downstream repositories such as VAP, RSP, and RDGP to query Epi25-derived gene sets at the appropriate granularity.

---

## 12. Immediate next implementation target for DEX-GSC

Ask DEX-GSC to build:

```text
scripts/ingest/ingest_epi25_browser_gene_burden.py
```

Inputs:

```text
raw EPI/DEE/GGE/NAFE browser CSVs
pinned Ensembl-to-HGNC mapping TSV
source metadata YAML
```

Outputs:

```text
data/disease/epilepsy/gold/epi25/2024/processed/epi25_2024_browser_burden_long.tsv
data/disease/epilepsy/gold/epi25/2024/processed/epi25_2024_exomewide_ptv_core.tsv
data/disease/epilepsy/gold/epi25/2024/processed/epi25_2024_candidates_ranked.tsv
```

Minimum deterministic behavior:

```text
- input file order does not affect output
- output rows are sorted by phenotype, variant_class, p_value, ensembl_gene_id
- raw p-values are preserved as strings
- derived numeric p-values are separate fields
- all thresholds are specified in config, not hardcoded
```

---

## 13. Bottom line

The four browser CSVs are highly useful because they provide deterministic, re-runnable source evidence for Epi25-derived epilepsy gene sets. They require transformation, but not reinterpretation. The safest GSC strategy is to preserve them as Gold raw evidence, normalize them into a long-format burden table, map Ensembl IDs to HGNC symbols, and generate multiple explicit gene-set products rather than one flattened epilepsy list.
