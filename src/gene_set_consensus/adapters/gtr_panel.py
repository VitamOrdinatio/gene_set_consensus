import pandas as pd

from gene_set_consensus.adapters.base import SourceAdapter

class GTRPanelAdapter(SourceAdapter):

    REQUIRED_COLUMNS = [
        "condition_label",
        "condition_id",
        "test_name",
        "test_id",
        "panel_name",
        "gene_symbol",
    ]

    def load(self, path):

        return pd.read_csv(
            path,
            sep="\t",
            dtype=str
        ).fillna("")

    def validate(self, df):

        missing = [
            c for c in self.REQUIRED_COLUMNS
            if c not in df.columns
        ]

        if missing:
            raise ValueError(
                f"GTR panel missing columns: {missing}"
            )

    def transform(self, df):

        out = df.copy()

        if "gene_id" not in out.columns:
            out["gene_id"] = ""

        out["evidence_label"] = (
            out["panel_name"]
            .fillna("")
            .astype(str)
        )

        out["notes"] = (
            "condition_id=" +
            out["condition_id"].astype(str)
        )

        return out[
            [
                "gene_symbol",
                "gene_id",
                "evidence_label",
                "notes"
            ]
        ]
