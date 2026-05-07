#!/usr/bin/env python
from pathlib import Path
import argparse
import gzip
import re
from xml.etree import ElementTree as ET

EPILEPSY_TERMS = [
    "epilepsy",
    "epileptic",
    "seizure",
    "seizures",
    "developmental epileptic encephalopathy",
    "infantile spasms",
    "generalized epilepsy",
    "focal epilepsy",
]

MITO_TERMS = [
    "mitochondrial",
    "mitochondria",
    "mitochondrial disease",
    "mitochondrial disorder",
    "mitochondrial depletion",
    "oxidative phosphorylation",
    "oxphos",
    "respiratory chain",
    "leigh syndrome",
    "polg",
]

def open_text(path):
    path = Path(path)
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8", errors="replace")
    return open(path, "r", encoding="utf-8", errors="replace")

def strip_ns(tag):
    return tag.split("}", 1)[-1] if "}" in tag else tag

def clean(text):
    return re.sub(r"\s+", " ", text or "").strip()

def elem_text(elem):
    return clean(" ".join(t for t in elem.itertext() if t))

def matched_terms(text, terms):
    lower = text.lower()
    return [term for term in terms if term.lower() in lower]

def summarize_block(elem):
    rows = []
    for child in elem.iter():
        tag = strip_ns(child.tag)
        text = elem_text(child)
        attrs = ";".join(f"{k}={v}" for k, v in child.attrib.items())
        if text or attrs:
            rows.append((tag, attrs, text[:500]))
    return rows

def write_example(outdir, label, idx, elem, terms):
    xml_path = outdir / f"{label}_clinvarset_example_{idx}.xml"
    summary_path = outdir / f"{label}_clinvarset_example_{idx}_summary.tsv"

    xml_path.write_text(ET.tostring(elem, encoding="unicode"), encoding="utf-8")

    text = elem_text(elem)
    matches = matched_terms(text, terms)

    with summary_path.open("w", encoding="utf-8") as out:
        out.write("tag\tattributes\ttext\n")
        for tag, attrs, value in summarize_block(elem):
            attrs = attrs.replace("\t", " ").replace("\n", " ")
            value = value.replace("\t", " ").replace("\n", " ")
            out.write(f"{tag}\t{attrs}\t{value}\n")

    return {
        "label": label,
        "index": idx,
        "matched_terms": "|".join(matches),
        "xml_path": str(xml_path),
        "summary_path": str(summary_path),
    }

def main():
    parser = argparse.ArgumentParser(description="Extract phenotype-matching ClinVarSet blocks from pinned GTR XML.")
    parser.add_argument("--xml", default="/mnt/storage/gtr/gtr_ftp.xml")
    parser.add_argument("--outdir", default="results/reports/gtr_schema_exploration/clinvarset_examples")
    parser.add_argument("--max-per-label", type=int, default=5)
    args = parser.parse_args()

    xml_path = Path(args.xml)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    found = {"epilepsy": 0, "mitochondrial": 0, "control": 0}
    index_rows = []

    with open_text(xml_path) as handle:
        for _, elem in ET.iterparse(handle, events=("end",)):
            tag = strip_ns(elem.tag)
            if tag != "ClinVarSet":
                elem.clear()
                continue

            text = elem_text(elem)
            epilepsy_match = matched_terms(text, EPILEPSY_TERMS)
            mito_match = matched_terms(text, MITO_TERMS)

            label = None
            terms = []

            if epilepsy_match and found["epilepsy"] < args.max_per_label:
                label = "epilepsy"
                terms = EPILEPSY_TERMS
            elif mito_match and found["mitochondrial"] < args.max_per_label:
                label = "mitochondrial"
                terms = MITO_TERMS
            elif not epilepsy_match and not mito_match and found["control"] < args.max_per_label:
                label = "control"
                terms = []

            if label:
                found[label] += 1
                index_rows.append(write_example(outdir, label, found[label], elem, terms))

            elem.clear()

            if all(v >= args.max_per_label for v in found.values()):
                break

    index_path = outdir / "clinvarset_example_index.tsv"
    with index_path.open("w", encoding="utf-8") as out:
        out.write("label\tindex\tmatched_terms\txml_path\tsummary_path\n")
        for row in index_rows:
            out.write(f"{row['label']}\t{row['index']}\t{row['matched_terms']}\t{row['xml_path']}\t{row['summary_path']}\n")

    print(f"outdir={outdir}")
    print(f"index={index_path}")
    print(f"counts={found}")

if __name__ == "__main__":
    main()
