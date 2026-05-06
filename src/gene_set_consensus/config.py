from pathlib import Path
import yaml

def load_yaml(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if data is None:
        raise ValueError(f"Config file is empty: {path}")
    if not isinstance(data, dict):
        raise ValueError(f"Config must parse to a dictionary: {path}")
    return data

def load_project_config(config_path):
    config = load_yaml(config_path)
    required_top_keys = ["project", "runtime", "paths", "identifier_normalization", "outputs"]
    missing = [key for key in required_top_keys if key not in config]
    if missing:
        raise ValueError(f"Project config missing required keys: {missing}")
    return config

def load_phenotype_config(phenotype_path):
    config = load_yaml(phenotype_path)
    if "phenotype" not in config:
        raise ValueError("Phenotype config missing required key: phenotype")
    if "sources" not in config:
        raise ValueError("Phenotype config missing required key: sources")
    if "scoring" not in config:
        raise ValueError("Phenotype config missing required key: scoring")
    if not config["sources"]:
        raise ValueError("Phenotype config must define at least one source")
    source_ids = [source.get("source_id") for source in config["sources"]]
    if len(source_ids) != len(set(source_ids)):
        raise ValueError(f"Duplicate source_id values detected: {source_ids}")
    return config

def resolve_phenotype_config_path(config, phenotype):
    return Path("config") / "phenotypes" / f"{phenotype}.yaml"
