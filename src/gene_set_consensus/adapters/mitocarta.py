import pandas as pd
from gene_set_consensus.adapters.base import SourceAdapter

class MitoCartaAdapter(SourceAdapter):

    REQUIRED_COLUMNS = [
        "HumanGeneID",
        "Symbol",
        "Description",
        "MitoCarta3.0_List",
        "MitoCarta3.0_Evidence",
        "MitoCarta3.0_SubMitoLocalization",
        "MitoCarta3.0_MitoPathways",
        "EnsemblGeneID_mapping_version_20200130",
    ]

    def load(self, path):
        return pd.read_csv(path, sep="\t", dtype=str).fillna("")

    def validate(self, df):
        missing = [c for c in self.REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            raise ValueError(f"MitoCarta file missing columns: {missing}")

    def transform(self, df):
        out = df.copy()

        out["gene_symbol"] = out["Symbol"]
        out["gene_id"] = out["EnsemblGeneID_mapping_version_20200130"]

        out["evidence_label"] = out["MitoCarta3.0_Evidence"]

        out["notes"] = (
            "HumanGeneID=" + out["HumanGeneID"].astype(str)
            + "; Description=" + out["Description"].astype(str)
            + "; SubMitoLocalization=" + out["MitoCarta3.0_SubMitoLocalization"].astype(str)
            + "; MitoPathways=" + out["MitoCarta3.0_MitoPathways"].astype(str)
            + "; MitoCarta3.0_List=" + out["MitoCarta3.0_List"].astype(str)
        )

        return out[
            [
                "gene_symbol",
                "gene_id",
                "evidence_label",
                "notes",
            ]
        ]
