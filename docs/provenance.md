# GSC Provenance and Scientific Revision Framework

## Purpose

Gene Set Consensus (GSC) is designed to support reproducible, versioned, and auditable scientific interpretation of gene-set evidence.

GSC outputs are not treated as immutable biological truths. Instead, each output represents a time-stamped computational interpretation generated from specific source releases, processing rules, identifier harmonization layers, and evidence-weighting policies.

This design supports:
- scientific revision
- longitudinal reproducibility
- clinical auditability
- computational provenance
- deterministic regeneration of historical outputs

---

# Core Provenance Philosophy

## Scientific Knowledge Evolves

Gene-disease associations change over time.

A gene set considered high-confidence in:
- 2026

may differ substantially from:
- 2036

due to:
- new consortium data
- larger cohorts
- improved statistical methods
- revised phenotype definitions
- updated curation standards
- new publications

Therefore, GSC stores:
- source release versions
- acquisition dates
- publication anchors
- processing timestamps
- evidence channels
- rule definitions
- identifier mapping provenance

rather than treating outputs as permanent truth.

---

# Provenance Layers

## 1. Source Provenance

Each source should preserve:

- source_name
- source_release
- source_publication_year
- source_download_date
- source_accession
- source_url
- source_checksum
- source_type
- source_tier

Examples:
- Epi25_2024
- MitoCarta3.0
- Genes4Epilepsy_v1

---

## 2. Evidence Provenance

GSC preserves evidence channels independently.

Example:
- browser-derived SNV/indel burden evidence
- publication-derived joint CNV + SNV evidence

These channels are not flattened into a single opaque source.

This allows future users to distinguish:
- direct statistical burden evidence
vs
- publication-level interpretive assertions

---

## 3. Identifier Provenance

Gene identifiers evolve across database releases.

GSC therefore:
- separates live identifier resolution from pipeline execution
- uses pinned identifier maps
- preserves mapping provenance
- avoids unsafe implicit merges

Identifier maps should preserve:
- input_gene_symbol
- normalized_gene_symbol
- Ensembl gene ID
- HGNC ID
- Entrez ID
- alias symbols
- mapping source
- mapping timestamp
- mapping version

---

## 4. Computational Provenance

Each GSC run should preserve:
- run_id
- GSC version
- phenotype configuration
- source manifest
- identifier map
- rule set
- processing timestamp
- output checksums

This allows deterministic regeneration of historical outputs.

---

# Scientific Revision Policy

GSC is designed to support scientific revision rather than resist it.

Future updates may:
- add genes
- remove genes
- alter evidence weights
- redefine phenotype rollups
- revise source tiers
- replace identifier mappings

Such changes should occur through:
- new source releases
- new configuration versions
- explicit commit history
- documented provenance updates

rather than silent mutation of historical outputs.

---

# Tier Semantics

Evidence tiers reflect:
- curation philosophy
- scale of evidence
- confidence of interpretation

not absolute biological truth.

Current tier philosophy:

- gold
  - flagship consortium-scale evidence
  - highly curated canonical resources
  - examples: Epi25, MitoCarta

- silver
  - systematic aggregation
  - clinical data mining
  - examples: GTR-derived aggregation

- bronze
  - literature-derived lists
  - smaller curated publications
  - examples: Genes4Epilepsy

---

# Phenotype Rollup Philosophy

Some phenotypes represent umbrella clinical concepts.

Example:
- EPI may incorporate subtype evidence from:
  - DEE
  - NAFE

Rollup behavior should be:
- explicit
- versioned
- documented
- reproducible

rather than implicit.

---

# Deterministic Execution

Live external APIs should not alter deterministic pipeline execution.

External services such as:
- MyGene.info

may be used to construct:
- pinned identifier maps

However:
- production GSC runs should consume pinned local resources
- not live network queries

This preserves reproducibility.

