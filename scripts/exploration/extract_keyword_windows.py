#!/usr/bin/env python
from pathlib import Path
import argparse
import gzip
import re
from collections import defaultdict

TERMS = {
    "epilepsy": [
        "epilepsy",
        "epileptic",
        "seizure",
        "seizures",
        "developmental epileptic encephalopathy",
        "infantile spasms",
        "generalized epilepsy",
        "focal epilepsy",
    ],
    "mitochondrial": [
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
    ],
}

def open_text(path):
    path = Path(path)
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8", errors="replace")
    return open(path, "r", encoding="utf-8", errors="replace")

def main():
    parser = argparse.ArgumentParser(description="Extract line windows around phenotype keyword hits in GTR XML.")
    parser.add_argument("--xml", default="/mnt/storage/gtr/gtr_ftp.xml")
    parser.add_argument("--outdir", default="results/reports/gtr_schema_exploration/keyword_windows")
    parser.add_argument("--window", type=int, default=40)
    parser.add_argument("--max-per-label", type=int, default=10)
    args = parser.parse_args()

    xml_path = Path(args.xml)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    lines = []
    hits = defaultdict(list)

    with open_text(xml_path) as handle:
        for line_number, line in enumerate(handle, start=1):
            lines.append(line.rstrip("\n"))
            lower = line.lower()
            for label, terms in TERMS.items():
                if len(hits[label]) >= args.max_per_label:
                    continue
                matched = [term for term in terms if term.lower() in lower]
                if matched:
                    hits[label].append((line_number, matched))

    index_path = outdir / "keyword_window_index.tsv"
    with index_path.open("w", encoding="utf-8") as index:
        index.write("label\tindex\tline_number\tmatched_terms\twindow_path\n")
        for label, label_hits in hits.items():
            for idx, (line_number, matched) in enumerate(label_hits, start=1):
                start = max(1, line_number - args.window)
                end = min(len(lines), line_number + args.window)
                window_path = outdir / f"{label}_window_{idx}_line_{line_number}.xml"
                with window_path.open("w", encoding="utf-8") as out:
                    for n in range(start, end + 1):
                        out.write(f"{n}: {lines[n-1]}\n")
                index.write(f"{label}\t{idx}\t{line_number}\t{'|'.join(matched)}\t{window_path}\n")

    print(f"outdir={outdir}")
    print(f"index={index_path}")
    for label in TERMS:
        print(f"{label}_windows={len(hits[label])}")

if __name__ == "__main__":
    main()
