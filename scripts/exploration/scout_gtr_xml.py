#!/usr/bin/env python
from pathlib import Path
import argparse
import gzip
import re
from collections import Counter, defaultdict
from xml.etree import ElementTree as ET

EPILEPSY_TERMS = [
    "epilepsy",
    "epileptic",
    "seizure",
    "seizures",
    "developmental and epileptic encephalopathy",
    "dee",
    "infantile spasms",
    "generalized epilepsy",
    "focal epilepsy",
]

MITO_TERMS = [
    "mitochondrial",
    "mitochondria",
    "mitochondrion",
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

def get_text(elem, max_len=500):
    text = " ".join(t.strip() for t in elem.itertext() if t and t.strip())
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_len]

def tag_frequency(path, max_events):
    counts = Counter()
    parent_child = Counter()
    stack = []
    events = 0

    with open_text(path) as handle:
        for event, elem in ET.iterparse(handle, events=("start", "end")):
            tag = strip_ns(elem.tag)
            if event == "start":
                counts[tag] += 1
                if stack:
                    parent_child[(stack[-1], tag)] += 1
                stack.append(tag)
                events += 1
                if events >= max_events:
                    break
            elif event == "end":
                if stack:
                    stack.pop()
                elem.clear()

    return counts, parent_child

def keyword_scan(path, terms, max_hits_per_term):
    hits = defaultdict(list)
    line_no = 0

    with open_text(path) as handle:
        for line in handle:
            line_no += 1
            lower = line.lower()
            for term in terms:
                if term.lower() in lower and len(hits[term]) < max_hits_per_term:
                    snippet = re.sub(r"\s+", " ", line.strip())
                    hits[term].append((line_no, snippet[:500]))

    return hits

def find_candidate_records(path, terms, candidate_tags, max_records):
    records = []
    lower_terms = [t.lower() for t in terms]

    with open_text(path) as handle:
        context = ET.iterparse(handle, events=("end",))
        for _, elem in context:
            tag = strip_ns(elem.tag)
            if tag not in candidate_tags:
                elem.clear()
                continue

            text = get_text(elem, max_len=3000)
            lower_text = text.lower()
            matched = [t for t in lower_terms if t in lower_text]
            if matched:
                records.append({
                    "tag": tag,
                    "matched_terms": "|".join(sorted(set(matched))),
                    "text": text,
                })
                if len(records) >= max_records:
                    elem.clear()
                    break
            elem.clear()

    return records

def write_tag_reports(outdir, counts, parent_child):
    tag_path = outdir / "tag_frequency.tsv"
    with tag_path.open("w", encoding="utf-8") as out:
        out.write("tag\tcount\n")
        for tag, count in counts.most_common():
            out.write(f"{tag}\t{count}\n")

    pc_path = outdir / "parent_child_frequency.tsv"
    with pc_path.open("w", encoding="utf-8") as out:
        out.write("parent\tchild\tcount\n")
        for (parent, child), count in parent_child.most_common():
            out.write(f"{parent}\t{child}\t{count}\n")

def write_keyword_hits(outdir, label, hits):
    path = outdir / f"{label}_keyword_line_hits.tsv"
    with path.open("w", encoding="utf-8") as out:
        out.write("term\tline_number\tsnippet\n")
        for term in sorted(hits):
            for line_no, snippet in hits[term]:
                out.write(f"{term}\t{line_no}\t{snippet}\n")

def write_records(outdir, label, records):
    path = outdir / f"{label}_candidate_records.tsv"
    with path.open("w", encoding="utf-8") as out:
        out.write("record_index\ttag\tmatched_terms\ttext\n")
        for idx, record in enumerate(records, start=1):
            text = record["text"].replace("\t", " ").replace("\n", " ")
            out.write(f"{idx}\t{record['tag']}\t{record['matched_terms']}\t{text}\n")

def write_summary(outdir, xml_path, counts, epilepsy_hits, mito_hits, epilepsy_records, mito_records):
    path = outdir / "gtr_xml_scout_summary.md"
    with path.open("w", encoding="utf-8") as out:
        out.write("# GTR XML Scout Summary\n\n")
        out.write(f"Input XML: `{xml_path}`\n\n")
        out.write("## Top Tags\n\n")
        out.write("| Tag | Count |\n|---|---:|\n")
        for tag, count in counts.most_common(25):
            out.write(f"| `{tag}` | {count} |\n")
        out.write("\n## Keyword Hit Summary\n\n")
        out.write("| Phenotype family | Terms with hits | Candidate records |\n|---|---:|---:|\n")
        out.write(f"| epilepsy | {sum(1 for v in epilepsy_hits.values() if v)} | {len(epilepsy_records)} |\n")
        out.write(f"| mitochondrial | {sum(1 for v in mito_hits.values() if v)} | {len(mito_records)} |\n")
        out.write("\n## Interpretation Notes\n\n")
        out.write("- This script is exploratory and does not define final GTR extraction rules.\n")
        out.write("- Keyword hits are used only for schema reconnaissance.\n")
        out.write("- Candidate records should be inspected before production parser design.\n")
        out.write("- Future production extraction should remain pinned to source snapshot, parser version, and extraction rule version.\n")

def main():
    parser = argparse.ArgumentParser(description="Scout a pinned GTR XML dump for schema and phenotype-relevant records.")
    parser.add_argument("--xml", default="/mnt/storage/gtr/gtr_ftp.xml")
    parser.add_argument("--outdir", default="results/reports/gtr_schema_exploration")
    parser.add_argument("--max-events", type=int, default=250000)
    parser.add_argument("--max-hits-per-term", type=int, default=50)
    parser.add_argument("--max-records", type=int, default=25)
    parser.add_argument("--candidate-tags", nargs="+", default=[
        "GTRLabTest",
        "GTRTest",
        "Test",
        "ClinicalTest",
        "GeneTest",
        "Panel",
        "Condition",
        "GTRCondition",
        "Disorder",
        "Trait",
    ])
    args = parser.parse_args()

    xml_path = Path(args.xml)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    if not xml_path.exists():
        raise FileNotFoundError(f"XML file not found: {xml_path}")

    counts, parent_child = tag_frequency(xml_path, args.max_events)
    write_tag_reports(outdir, counts, parent_child)

    epilepsy_hits = keyword_scan(xml_path, EPILEPSY_TERMS, args.max_hits_per_term)
    mito_hits = keyword_scan(xml_path, MITO_TERMS, args.max_hits_per_term)
    write_keyword_hits(outdir, "epilepsy", epilepsy_hits)
    write_keyword_hits(outdir, "mitochondrial", mito_hits)

    epilepsy_records = find_candidate_records(xml_path, EPILEPSY_TERMS, set(args.candidate_tags), args.max_records)
    mito_records = find_candidate_records(xml_path, MITO_TERMS, set(args.candidate_tags), args.max_records)
    write_records(outdir, "epilepsy", epilepsy_records)
    write_records(outdir, "mitochondrial", mito_records)

    write_summary(outdir, xml_path, counts, epilepsy_hits, mito_hits, epilepsy_records, mito_records)

    print(f"outdir={outdir}")
    print(f"tag_report={outdir / 'tag_frequency.tsv'}")
    print(f"epilepsy_hits={outdir / 'epilepsy_keyword_line_hits.tsv'}")
    print(f"mitochondrial_hits={outdir / 'mitochondrial_keyword_line_hits.tsv'}")
    print(f"summary={outdir / 'gtr_xml_scout_summary.md'}")

if __name__ == "__main__":
    main()
