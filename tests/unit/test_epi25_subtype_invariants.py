from pathlib import Path
import pandas as pd

EPI = Path("/mnt/storage/gene_sets/epi25/2024/processed/epi25_2024_epi_high_confidence.tsv")
DEE = Path("/mnt/storage/gene_sets/epi25/2024/processed/epi25_2024_dee_high_confidence.tsv")
NAFE = Path("/mnt/storage/gene_sets/epi25/2024/processed/epi25_2024_nafe_high_confidence.tsv")

def read_genes(path):
    df = pd.read_csv(path, sep="\t", dtype=str).fillna("")
    return set(df["gene_symbol"])

def test_epi25_high_confidence_counts():
    assert len(read_genes(EPI)) == 7
    assert len(read_genes(DEE)) == 5
    assert len(read_genes(NAFE)) == 2

def test_epi25_dee_nafe_partition_reconstructs_epi():
    epi = read_genes(EPI)
    dee = read_genes(DEE)
    nafe = read_genes(NAFE)
    assert dee | nafe == epi
    assert dee & nafe == set()

def test_epi25_expected_subtype_gene_sets():
    assert read_genes(DEE) == {"NEXMIF", "SCN1A", "SYNGAP1", "STX1B", "WDR45"}
    assert read_genes(NAFE) == {"DEPDC5", "NPRL3"}
