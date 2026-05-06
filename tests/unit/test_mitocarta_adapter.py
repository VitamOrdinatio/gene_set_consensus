import pandas as pd
from gene_set_consensus.adapters.mitocarta import MitoCartaAdapter

def test_mitocarta_adapter_transforms_native_columns():
    df = pd.DataFrame([{
        "HumanGeneID": "1537",
        "Symbol": "CYC1",
        "Description": "cytochrome c1",
        "MitoCarta3.0_List": "MitoCarta3.0",
        "MitoCarta3.0_Evidence": "literature, MS/MS++",
        "MitoCarta3.0_SubMitoLocalization": "MIM",
        "MitoCarta3.0_MitoPathways": "OXPHOS > Complex III",
        "EnsemblGeneID_mapping_version_20200130": "ENSG00000179091",
    }])

    adapter = MitoCartaAdapter()
    adapter.validate(df)
    out = adapter.transform(df)

    assert out.loc[0, "gene_symbol"] == "CYC1"
    assert out.loc[0, "gene_id"] == "ENSG00000179091"
    assert "literature" in out.loc[0, "evidence_label"]
    assert "HumanGeneID=1537" in out.loc[0, "notes"]
    assert "OXPHOS" in out.loc[0, "notes"]
