import subprocess
from pathlib import Path
import pandas as pd
import sys

def test_example_pipeline_runs_end_to_end():
    result = subprocess.run(
        [sys.executable, "run_pipeline.py", "--config", "config/config.yaml", "--phenotype", "example_phenotype"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, result.stderr
    consensus_path = Path("results/tables/example_phenotype/consensus_gene_set.tsv")
    assert consensus_path.exists()
    df = pd.read_csv(consensus_path, sep="\t")
    assert "sample_id" not in df.columns
    polg = df[df["gene_symbol"] == "POLG"].iloc[0]
    assert int(polg["source_count"]) == 3
    assert float(polg["consensus_score"]) == 8.0
