#!/usr/bin/env python
from pathlib import Path
import argparse
import gzip
import re
import yaml
import pandas as pd
from xml.etree import ElementTree as ET

def open_text(path):
    path = Path(path)
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8", errors="replace")
    return open(path, "r", encoding="utf-8", errors="replace")

def strip_ns(tag):
    return tag.split("}", 1)[-1] if "}" in tag else tag

def clean(text):
    return re.sub(r"\s+", " ", text or "").strip()

def child_text(elem, tag_name):
    for child in elem:
        if strip_ns(child.tag) == tag_name:
            return clean(" ".join(t for t in child.itertext() if t))
    return ""

def all_child_texts(elem, tag_name):
    vals = []
    for child in elem:
        if strip_ns(child.tag) == tag_name:
            txt = clean(" ".join(t for t in child.itertext() if t))
            if txt:
                vals.append(txt)
    return vals

def load_rule(path):
    with open(path, "r", encoding="utf-8") as handle:
        rule = yaml.safe_load(handle)
    rule["terms"] = [str(t).lower() for t in rule.get("terms", [])]
    return rule

def match_terms(text, terms):
    lower = text.lower()
    return sorted({term for term in terms if term in lower})

def get_lab_name(gtrlab):
    org = next((c for c in gtrlab if strip_ns(c.tag) == "Organization"), None)
    if org is None:
        return ""
    for child in org:
        if strip_ns(child.tag) == "Name":
            return clean(" ".join(t for t in child.itertext() if t))
    return ""

def get_test_categories(test):
    vals = []
    for node in test.iter():
        if strip_ns(node.tag) == "Category":
            value = node.attrib.get("Value", "")
            score = node.attrib.get("Score", "")
            if value:
                vals.append(f"{value}:{score}" if score else value)
    return "|".join(sorted(set(vals)))

def classify_test_scope(test_name, test_categories):
    text = f"{test_name} {test_categories}".lower()
    if any(term in text for term in ["whole genome", "wgs", "genome sequencing"]):
        return "genome"
    if any(term in text for term in ["whole exome", "wes", "exome sequencing"]):
        return "exome"
    if "panel" in text:
        return "panel_unsized"
    if any(term in text for term in ["single gene", "deletion test", "duplication test"]):
        return "targeted_gene"
    return "unknown"

def extract_trait_records(assertion):
    traits = []
    for node in assertion.iter():
        if strip_ns(node.tag) != "Trait":
            continue
        trait_id = node.attrib.get("ID", "")
        trait_type = node.attrib.get("Type", "")
        names = []
        symbols = []
        xrefs = []
        for child in node:
            tag = strip_ns(child.tag)
            if tag == "Name":
                txt = clean(" ".join(t for t in child.itertext() if t))
                typ = child.attrib.get("Type", "")
                if txt:
                    names.append(f"{typ}:{txt}" if typ else txt)
            elif tag == "Symbol":
                txt = clean(" ".join(t for t in child.itertext() if t))
                typ = child.attrib.get("Type", "")
                if txt:
                    symbols.append(f"{typ}:{txt}" if typ else txt)
            elif tag == "XRef":
                db = child.attrib.get("DB", "")
                xid = child.attrib.get("ID", "")
                xtype = child.attrib.get("Type", "")
                if db or xid:
                    xrefs.append(":".join(x for x in [db, xtype, xid] if x))
        trait_text = " ".join(names + symbols + xrefs)
        traits.append({
            "trait_id": trait_id,
            "trait_type": trait_type,
            "trait_names": "|".join(names),
            "trait_symbols": "|".join(symbols),
            "trait_xrefs": "|".join(xrefs),
            "trait_text": trait_text,
        })
    return traits

def extract_gene_measures(assertion, measure_types_included):
    measures = []
    for node in assertion.iter():
        if strip_ns(node.tag) != "Measure":
            continue
        measure_type = node.attrib.get("Type", "")
        if measure_type not in measure_types_included:
            continue
        measure_id = node.attrib.get("ID", "")
        gene_symbol = ""
        gene_id = ""
        omim_gene_id = ""
        locations = []
        names = []
        for child in node:
            tag = strip_ns(child.tag)
            if tag == "Symbol" and child.attrib.get("Type", "") == "Preferred":
                gene_symbol = clean(" ".join(t for t in child.itertext() if t))
            elif tag == "Name":
                txt = clean(" ".join(t for t in child.itertext() if t))
                typ = child.attrib.get("Type", "")
                if txt:
                    names.append(f"{typ}:{txt}" if typ else txt)
            elif tag == "XRef":
                db = child.attrib.get("DB", "")
                xid = child.attrib.get("ID", "")
                xtype = child.attrib.get("Type", "")
                if db == "Gene":
                    gene_id = xid
                elif db == "OMIM":
                    omim_gene_id = xid
            elif tag == "Location":
                assembly = child.attrib.get("assembly", "")
                chr_ = child.attrib.get("Chr", "")
                loc_type = child.attrib.get("Type", "")
                txt = clean(" ".join(t for t in child.itertext() if t))
                locations.append(f"{loc_type}:{assembly}:chr{chr_}:{txt}")
        if gene_symbol:
            measures.append({
                "gene_symbol": gene_symbol,
                "gene_id": gene_id,
                "omim_gene_id": omim_gene_id,
                "measure_id": measure_id,
                "measure_type": measure_type,
                "measure_names": "|".join(names),
                "measure_locations": "|".join(locations),
            })
    return measures

def main():
    parser = argparse.ArgumentParser(description="Parse pinned GTR XML into phenotype-scoped gene-measure evidence.")
    parser.add_argument("--xml", default="/mnt/storage/gtr/gtr_ftp.xml")
    parser.add_argument("--rules", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    rule = load_rule(args.rules)
    measure_types_included = set(rule.get("measure_types_included", ["Gene"]))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    current_lab = None
    lab_id = ""
    lab_name = ""

    with open_text(args.xml) as handle:
        for event, elem in ET.iterparse(handle, events=("start", "end")):
            tag = strip_ns(elem.tag)

            if event == "start" and tag == "GTRLab":
                current_lab = elem
                lab_id = elem.attrib.get("id", "")

            if event == "end" and tag == "GTRLab":
                elem.clear()
                current_lab = None
                lab_id = ""
                lab_name = ""

            if event == "end" and tag == "GTRLabTest":
                if current_lab is not None and not lab_name:
                    lab_name = get_lab_name(current_lab)

                test_id = elem.attrib.get("id", "")
                gtr_accession = elem.attrib.get("GTRAccession", "")
                test_version = elem.attrib.get("Version", "")
                last_update = elem.attrib.get("LastUpdate", "")
                last_touched = elem.attrib.get("LastTouched", "")
                test_name = child_text(elem, "TestName")
                test_categories = get_test_categories(elem)
                test_scope = classify_test_scope(test_name, test_categories)

                for assertion in elem.iter():
                    if strip_ns(assertion.tag) != "ClinVarAssertion":
                        continue

                    traits = extract_trait_records(assertion)
                    gene_measures = extract_gene_measures(assertion, measure_types_included)

                    if not traits or not gene_measures:
                        continue

                    for trait in traits:
                        matched = match_terms(trait["trait_text"], rule["terms"])
                        if not matched:
                            continue

                        for measure in gene_measures:
                            rows.append({
                                "phenotype_id": rule.get("phenotype_id", ""),
                                "gene_symbol": measure["gene_symbol"],
                                "gene_id": measure["gene_id"],
                                "omim_gene_id": measure["omim_gene_id"],
                                "matched_trait_name": trait["trait_names"],
                                "matched_trait_id": trait["trait_id"],
                                "matched_trait_type": trait["trait_type"],
                                "matched_trait_symbols": trait["trait_symbols"],
                                "matched_trait_xrefs": trait["trait_xrefs"],
                                "matched_keyword": "|".join(matched),
                                "measure_id": measure["measure_id"],
                                "measure_type": measure["measure_type"],
                                "measure_names": measure["measure_names"],
                                "measure_locations": measure["measure_locations"],
                                "gtr_accession": gtr_accession,
                                "gtr_test_id": test_id,
                                "test_name": test_name,
                                "test_version": test_version,
                                "test_categories": test_categories,
                                "test_scope": test_scope,
                                "broad_test_policy": rule.get("broad_test_policy", ""),
                                "match_scope": rule.get("match_scope", ""),
                                "ontology_expansion": str(rule.get("ontology_expansion", False)),
                                "lab_id": lab_id,
                                "lab_name": lab_name,
                                "last_update": last_update,
                                "last_touched": last_touched,
                                "source_snapshot": rule.get("source_snapshot", ""),
                                "parser_version": rule.get("parser_version", ""),
                                "extraction_rule_version": rule.get("extraction_rule_version", ""),
                            })

                elem.clear()

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.drop_duplicates().sort_values(
            ["gene_symbol", "gtr_accession", "matched_trait_id", "measure_id"]
        )

    # Raw evidence table: preserve row-level GTR evidence.
    # This file is intentionally not the collapsed GSC-ready summary.
    df.to_csv(output, sep="\t", index=False, lineterminator="\n")

    print(f"output={output}")
    print(f"rows={len(df)}")
    if not df.empty:
        print(f"unique_genes={df['gene_symbol'].nunique()}")
        print(df["gene_symbol"].value_counts().head(20).to_string())

if __name__ == "__main__":
    main()
