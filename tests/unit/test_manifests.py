from gene_set_consensus.manifests import build_manifest_source_lookup

def test_manifest_lookup():

    manifest = {
        "sources": [
            {
                "source_id": "s1",
                "source_name": "Source 1",
                "source_type": "curated_database",
                "adapter": "generic_gene_list",
                "biological_context": {},
                "provenance": {},
                "file_metadata": {},
            }
        ]
    }

    lookup = build_manifest_source_lookup(manifest)

    assert "s1" in lookup
    assert lookup["s1"]["source_name"] == "Source 1"
