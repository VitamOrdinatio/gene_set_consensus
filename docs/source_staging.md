# Source Staging Guide

## Purpose

This guide defines where real GSC source files should live before pipeline execution.

GSC keeps code, configs, small examples, and tests in Git. Real biological source files live outside Git in the storage layer.

## sys76 Storage Targets

```text
/mnt/storage/gene_sets/mitocarta/
/mnt/storage/gene_sets/epi25/
/mnt/storage/gene_sets/mitochondrial_disease/
/mnt/storage/gene_sets/epilepsy/
/mnt/storage/gtr/
```

## MARK Storage Targets

```text
/data/storage/gene_sets/mitocarta/
/data/storage/gene_sets/epi25/
/data/storage/gene_sets/mitochondrial_disease/
/data/storage/gene_sets/epilepsy/
/data/storage/gtr/
```

## Recommended Source Filenames on sys76

```text
/mnt/storage/gene_sets/mitocarta/mitocarta_human.tsv
/mnt/storage/gtr/mitochondrial_disease_gtr_panel.tsv
/mnt/storage/gtr/epilepsy_gtr_panel.tsv
/mnt/storage/gene_sets/epi25/epi25_genes.tsv
/mnt/storage/gene_sets/epilepsy/user_curated_epilepsy_genes.tsv
```

## Recommended Source Filenames on MARK

```text
/data/storage/gene_sets/mitocarta/mitocarta_human.tsv
/data/storage/gtr/mitochondrial_disease_gtr_panel.tsv
/data/storage/gtr/epilepsy_gtr_panel.tsv
/data/storage/gene_sets/epi25/epi25_genes.tsv
/data/storage/gene_sets/epilepsy/user_curated_epilepsy_genes.tsv
```

## Minimal Source File Shape
Each source should be converted into a TSV with at least:
`gene_symbol`

Recommended columns:
- `gene_symbol`
- `gene_id`
- `evidence_label`
- `notes`

## Design Rule
Raw source files are not committed to Git unless they are tiny toy examples.
The repository stores:
    • source validators 
    • source adapters 
    • phenotype configs 
    • schema documentation 
    • reproducible output logic 
The storage layer stores:
    • downloaded source files 
    • exported clinical panels 
    • large external datasets

---

