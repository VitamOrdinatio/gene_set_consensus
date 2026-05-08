#!/usr/bin/env python
from pathlib import Path
import argparse
import sys
import yaml

VALID_ACTIVE_SCORES = {"weighted_source_sum", "semantic_consensus_score"}
REQUIRED_TIERS = {"platinum", "gold", "silver", "bronze", "annotation_only"}
REQUIRED_CHANNEL_SCORE_COLUMNS = {
    "direct_disease_score",
    "clinical_interpretation_score",
    "contextual_biology_score",
    "utilization_score",
    "exploratory_score",
    "convergence_score",
}

def load_yaml(path):
    with Path(path).open() as handle:
        return yaml.safe_load(handle)

def is_number(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False

def validate_profile(data):
    errors = []

    profile = data.get("profile", {})
    for key in ["profile_id", "phenotype_family", "version", "active_score", "emit_legacy_scores", "emit_semantic_scores", "strict_semantic_validation"]:
        if key not in profile:
            errors.append(f"profile missing required field: {key}")

    if profile.get("active_score") not in VALID_ACTIVE_SCORES:
        errors.append(f"invalid active_score: {profile.get('active_score')}")

    tier_weights = data.get("tier_weights", {})
    missing_tiers = sorted(REQUIRED_TIERS - set(tier_weights))
    if missing_tiers:
        errors.append(f"tier_weights missing tiers: {missing_tiers}")
    for tier, weight in tier_weights.items():
        if not is_number(weight):
            errors.append(f"tier_weights.{tier} is non-numeric: {weight}")

    channel_caps = data.get("channel_caps", {})
    missing_caps = sorted(REQUIRED_CHANNEL_SCORE_COLUMNS - set(channel_caps))
    if missing_caps:
        errors.append(f"channel_caps missing score columns: {missing_caps}")
    for channel, cap in channel_caps.items():
        if not is_number(cap):
            errors.append(f"channel_caps.{channel} is non-numeric: {cap}")

    semantic_channel_map = data.get("semantic_channel_map", {})
    for semantic_channel, score_column in semantic_channel_map.items():
        if score_column not in channel_caps:
            errors.append(f"semantic_channel_map.{semantic_channel} maps to unknown score column: {score_column}")

    modifier_defaults = data.get("modifier_defaults", {})
    for key in ["source_quality_modifier", "phenotype_match_modifier", "independence_modifier"]:
        if key not in modifier_defaults:
            errors.append(f"modifier_defaults missing field: {key}")
        elif not is_number(modifier_defaults[key]):
            errors.append(f"modifier_defaults.{key} is non-numeric: {modifier_defaults[key]}")

    unknown_policy = data.get("unknown_policy", {})
    for key in ["unknown_semantic_channel", "unknown_evidence_tier", "missing_scoring_rule"]:
        if key not in unknown_policy:
            errors.append(f"unknown_policy missing field: {key}")

    for idx, rule in enumerate(data.get("source_rules", []), start=1):
        for key in ["source_id", "semantic_channel", "evidence_tier", "scoring_rule_id"]:
            if key not in rule:
                errors.append(f"source_rules[{idx}] missing field: {key}")
        if rule.get("semantic_channel") not in semantic_channel_map:
            errors.append(f"source_rules[{idx}] unknown semantic_channel: {rule.get('semantic_channel')}")
        if rule.get("evidence_tier") not in tier_weights:
            errors.append(f"source_rules[{idx}] unknown evidence_tier: {rule.get('evidence_tier')}")

    return errors

def main():
    parser = argparse.ArgumentParser(description="Validate a GSC semantic scoring profile.")
    parser.add_argument("--profile", required=True)
    args = parser.parse_args()

    data = load_yaml(args.profile)
    errors = validate_profile(data)

    if errors:
        print("SCORING PROFILE VALIDATION FAILED")
        for error in errors:
            print(f"ERROR   {error}")
        sys.exit(1)

    print("SCORING PROFILE VALIDATION PASSED")
    print(f"profile={args.profile}")
    print(f"profile_id={data['profile']['profile_id']}")
    print(f"active_score={data['profile']['active_score']}")
    print(f"source_rules={len(data.get('source_rules', []))}")

if __name__ == "__main__":
    main()
