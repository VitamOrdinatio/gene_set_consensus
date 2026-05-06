#!/usr/bin/env python
from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from gene_set_consensus.gtr import load_gtr_panel, summarize_gtr_panel

def main():

    parser = argparse.ArgumentParser(description="Validate GTR-derived source file.")
    parser.add_argument("--input", required=True)

    args = parser.parse_args()

    df = load_gtr_panel(args.input)

    summary = summarize_gtr_panel(df)

    print("GTR VALIDATION SUMMARY")
    print("----------------------")

    for key, value in summary.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
