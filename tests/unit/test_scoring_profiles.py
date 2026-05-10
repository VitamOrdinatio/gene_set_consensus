from pathlib import Path
from gene_set_consensus.scoring_profiles import (
    load_scoring_profile,
    get_active_score_column,
)

def test_load_scoring_profile():
    profile = load_scoring_profile(
        "config/scoring_profiles/epilepsy_semantic_v0.1.yaml"
    )

    assert profile["profile"]["profile_id"] == "epilepsy_semantic_v0.1"

def test_active_score_column():
    profile = load_scoring_profile(
        "config/scoring_profiles/epilepsy_semantic_v0.1.yaml"
    )

    active = get_active_score_column(profile)

    assert active == "weighted_source_sum"
