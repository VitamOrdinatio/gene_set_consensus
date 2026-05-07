#!/usr/bin/env python
from pathlib import Path
import argparse
import gzip
import re
from xml.etree import ElementTree as ET

GENE_TERMS = [
    "POLG",
    "SCN1A",
    "DEPDC5",
    "NPRL3",
    "ALDH7A1",
    "SYNGAP1",
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

def summarize(elem):
    rows = []
    for child in elem.iter():
        tag = strip_ns(child.tag)
        attrs = ";".join(f"{k}={v}" for k, v in child.attrib.items())
        text = elem_text(child)
        if text or attrs:
            rows.append((tag, attrs, text[:500]))
    return rows

def write_example(outdir, term, idx, elem):
    xml_path = outdir / f"{term}_genetesting_example_{idx}.xml"
    summary_path = outdir / f"{term}_genetesting_example_{idx}_summary.tsv"

    xml_path.write_text(ET.tostring(elem, encoding="unicode"), encoding="utf-8")

    with summary_path.open("w", encoding="utf-8") as out:
        out.write("tag\tattributes\ttext\n")
        for tag, attrs, value in summarize(elem):
            attrs = attrs.replace("\t", " ").replace("\n", " ")
            value = value.replace("\t", " ").replace("\n", " ")
            out.write(f"{tag}\t{attrs}\t{value}\n")

    return xml_path, summary_path

def main():
    parser = argparse.ArgumentParser(description="Extract GeneTesting blocks matching target genes.")
    parser.add_argument("--xml", default="/mnt/storage/gtr/gtr_ftp.xml")
    parser.add_argument("--outdir", default="results/reports/gtr_schema_exploration/genetesting_examples")
    parser.add_argument("--max-per-gene", type=int, default=3)
    args = parser.parse_args()

    xml_path = Path(args.xml)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    counts = {gene: 0 for gene in GENE_TERMS}
    index_rows = []

    with open_text(xml_path) as handle:
        for _, elem in ET.iterparse(handle, events=("end",)):
            tag = strip_ns(elem.tag)

            if tag != "GeneTesting":
                elem.clear()
                continue

            text = elem_text(elem)

            for gene in GENE_TERMS:
                if counts[gene] >= args.max_per_gene:
                    continue

                if gene.lower() in text.lower():
                    counts[gene] += 1

                    xml_path_out, summary_path = write_example(
                        outdir,
                        gene,
                        counts[gene],
                        elem
                    )

                    index_rows.append({
                        "gene": gene,
                        "index": counts[gene],
                        "xml_path": str(xml_path_out),
                        "summary_path": str(summary_path),
                    })

            elem.clear()

            if all(v >= args.max_per_gene for v in counts.values()):
                break

    index_path = outdir / "genetesting_example_index.tsv"

    with index_path.open("w", encoding="utf-8") as out:
        out.write("gene\tindex\txml_path\tsummary_path\n")
        for row in index_rows:
            out.write(
                f"{row['gene']}\t{row['index']}\t"
                f"{row['xml_path']}\t{row['summary_path']}\n"
            )

    print(f"outdir={outdir}")
    print(f"index={index_path}")
    print(f"counts={counts}")

if __name__ == "__main__":
    main()
