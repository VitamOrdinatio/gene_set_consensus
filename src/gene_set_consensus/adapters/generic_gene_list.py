from pathlib import Path
import pandas as pd

from gene_set_consensus.adapters.base import SourceAdapter

class GenericGeneListAdapter(SourceAdapter):

    REQUIRED_COLUMNS = ["gene_symbol"]

    def load(self, path):

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(
                f"Source file not found: {path}"
            )

        suffix = path.suffix.lower()

        if suffix == ".tsv":
            sep = "\t"
        elif suffix == ".csv":
            sep = ","
        else:
            raise ValueError(
                f"Unsupported extension: {path}"
            )

        return pd.read_csv(
            path,
            sep=sep,
            dtype=str
        ).fillna("")

    def validate(self, df):

        missing = [
            c for c in self.REQUIRED_COLUMNS
            if c not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Generic gene list missing columns: {missing}"
            )

    def transform(self, df):

        out = df.copy()

        optional_columns = [
            "gene_id",
            "evidence_label",
            "notes"
        ]

        for col in optional_columns:
            if col not in out.columns:
                out[col] = ""

        return out[
            [
                "gene_symbol",
                "gene_id",
                "evidence_label",
                "notes"
            ]
        ]
