#!/usr/bin/env python
from pathlib import Path
import argparse
import pandas as pd
import mygene

def collect_symbols(paths):
    symbols = set()
    for path in paths:
        path = Path(path)
        sep = "\t" if path.suffix.lower() == ".tsv" else ","
        df = pd.read_csv(path, sep=sep, dtype=str).fillna("")
        for col in ["gene_symbol", "Symbol"]:
            if col in df.columns:
                symbols.update(x.strip() for x in df[col].tolist() if x.strip())
    return sorted(symbols)

def _ensembl_gene(result):
    ensembl = result.get("ensembl", "")
    if isinstance(ensembl, list):
        return ensembl[0].get("gene", "") if ensembl else ""
    if isinstance(ensembl, dict):
        return ensembl.get("gene", "")
    return ""

def _aliases(result):
    aliases = result.get("alias", "")
    if isinstance(aliases, list):
        return "|".join(sorted(str(x) for x in aliases))
    return str(aliases) if aliases else ""

def choose_result(query, hits):
    if not hits:
        return None
    exact = [h for h in hits if str(h.get("symbol", "")).upper() == query.upper()]
    if len(exact) == 1:
        return exact[0]
    if len(exact) > 1:
        return sorted(exact, key=lambda h: float(h.get("_score", 0)), reverse=True)[0]
    return sorted(hits, key=lambda h: float(h.get("_score", 0)), reverse=True)[0]

def resolve_symbols(symbols):
    mg = mygene.MyGeneInfo()
    results = mg.querymany(
        symbols,
        scopes="symbol",
        fields="symbol,ensembl.gene,HGNC,entrezgene,alias",
        species="human",
        as_dataframe=False,
        returnall=False,
        verbose=False
    )

    by_query = {}
    for result in results:
        query = str(result.get("query", "")).strip()
        if query:
            by_query.setdefault(query, []).append(result)

    rows = []
    for query in symbols:
        hits = by_query.get(query, [])
        result = choose_result(query, hits)

        if result is None or result.get("notfound"):
            rows.append({
                "input_gene_symbol": query,
                "normalized_gene_symbol": query,
                "gene_id": "",
                "ensembl_gene_id": "",
                "hgnc_id": "",
                "entrezgene": "",
                "alias_symbol": "",
                "mapping_status": "unresolved",
                "mapping_source": "mygene.info",
                "mapping_version": "pinned_local_build"
            })
            continue

        ensembl_gene = _ensembl_gene(result)
        normalized_symbol = result.get("symbol", query)

        status = "resolved" if ensembl_gene and normalized_symbol.upper() == query.upper() else "symbol_resolved_nonexact"
        if not ensembl_gene:
            status = "symbol_only"

        rows.append({
            "input_gene_symbol": query,
            "normalized_gene_symbol": normalized_symbol,
            "gene_id": ensembl_gene,
            "ensembl_gene_id": ensembl_gene,
            "hgnc_id": result.get("HGNC", ""),
            "entrezgene": result.get("entrezgene", ""),
            "alias_symbol": _aliases(result),
            "mapping_status": status,
            "mapping_source": "mygene.info",
            "mapping_version": "pinned_local_build"
        })

    return pd.DataFrame(rows)

def main():
    parser = argparse.ArgumentParser(description="Build a pinned GSC gene identifier map using MyGene.info.")
    parser.add_argument("--inputs", nargs="+", required=True)
    parser.add_argument("--output", default="data/metadata/gene_identifier_maps/epilepsy_identifier_map.tsv")
    args = parser.parse_args()

    symbols = collect_symbols(args.inputs)
    if not symbols:
        raise ValueError("No gene symbols found in input files.")

    resolved = resolve_symbols(symbols)
    resolved = resolved.sort_values("input_gene_symbol").reset_index(drop=True)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    resolved.to_csv(output, sep="\t", index=False)

    print(f"symbols={len(symbols)}")
    print(f"output={output}")
    print(resolved["mapping_status"].value_counts().to_string())

if __name__ == "__main__":
    main()
