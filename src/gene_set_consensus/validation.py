from pathlib import Path
import csv

SUPPORTED_EXTENSIONS = {".tsv", ".csv"}

def detect_delimiter(path):
    suffix = Path(path).suffix.lower()
    if suffix == ".tsv":
        return "\t"
    if suffix == ".csv":
        return ","
    raise ValueError(f"Unsupported file extension for source file: {path}")

def read_header(path):
    delimiter = detect_delimiter(path)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, delimiter=delimiter)
        try:
            return next(reader)
        except StopIteration:
            raise ValueError(f"Source file is empty: {path}")

def count_data_rows(path):
    delimiter = detect_delimiter(path)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, delimiter=delimiter)
        next(reader, None)
        return sum(1 for _ in reader)

def validate_sources(phenotype_config):
    errors = []
    warnings = []
    sources = phenotype_config["sources"]
    for source in sources:
        for key in ["source_id", "source_name", "source_type", "file_path", "gene_column", "weight_tier", "source_weight"]:
            if key not in source or source[key] in [None, ""]:
                errors.append(f"{source.get('source_id', '<unknown>')} missing required field: {key}")
        if "source_weight" in source:
            try:
                float(source["source_weight"])
            except (TypeError, ValueError):
                errors.append(f"{source.get('source_id', '<unknown>')} has non-numeric source_weight: {source.get('source_weight')}")
        file_path = Path(source.get("file_path", ""))
        if not file_path.exists():
            errors.append(f"{source.get('source_id', '<unknown>')} source file not found: {file_path}")
            continue
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            errors.append(f"{source.get('source_id', '<unknown>')} unsupported file extension: {file_path}")
            continue
        header = read_header(file_path)
        gene_column = source.get("gene_column")
        if gene_column not in header:
            errors.append(f"{source.get('source_id', '<unknown>')} missing configured gene_column '{gene_column}' in {file_path}")
        rows = count_data_rows(file_path)
        if rows == 0:
            errors.append(f"{source.get('source_id', '<unknown>')} source file contains no data rows: {file_path}")
        if "gene_id" not in header and gene_column not in header:
            errors.append(f"{source.get('source_id', '<unknown>')} must provide gene_id or configured gene_column")
    return errors, warnings

def validate_project_paths(project_config):
    errors = []
    for key in ["interim_dir", "processed_dir", "results_dir", "logs_dir"]:
        if key not in project_config["paths"]:
            errors.append(f"Project config missing paths.{key}")
    return errors
