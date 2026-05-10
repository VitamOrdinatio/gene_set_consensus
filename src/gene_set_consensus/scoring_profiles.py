from pathlib import Path
import yaml

REQUIRED_PROFILE_FIELDS = {
    "profile_id",
    "phenotype_family",
    "version",
    "active_score",
}

VALID_ACTIVE_SCORES = {
    "weighted_source_sum",
    "semantic_consensus_score",
}

def load_scoring_profile(profile_path):
    path = Path(profile_path)

    if not path.exists():
        raise FileNotFoundError(f"Missing scoring profile: {profile_path}")

    with path.open() as handle:
        data = yaml.safe_load(handle)

    profile = data.get("profile", {})

    missing = REQUIRED_PROFILE_FIELDS - set(profile.keys())
    if missing:
        raise ValueError(
            f"Scoring profile missing required fields: {sorted(missing)}"
        )

    active_score = profile.get("active_score")

    if active_score not in VALID_ACTIVE_SCORES:
        raise ValueError(
            f"Unsupported active_score: {active_score}"
        )

    return data

def get_active_score_column(profile):
    return profile["profile"]["active_score"]
