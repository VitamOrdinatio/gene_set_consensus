ALLOWED_EVIDENCE_TIERS = {
    "platinum",
    "gold",
    "silver",
    "bronze",
    "annotation_only",
    "unspecified",
}

ALLOWED_SEMANTIC_CHANNELS = {
    "direct_disease",
    "clinical_interpretation",
    "contextual_biology",
    "clinical_utilization",
    "exploratory_literature",
    "convergence",
    "unspecified",
}

ALLOWED_EVIDENCE_SEMANTICS = {
    "statistical_association",
    "functional_localization",
    "clinical_utilization",
    "clinical_interpretation",
    "exploratory_literature",
    "network_convergence",
    "biochemical_phenotype",
    "unspecified",
}

def split_pipe_values(value):
    return [token.strip() for token in str(value).split("|") if token.strip()]

def validate_pipe_values(value, allowed_values, field_name):
    errors = []
    for token in split_pipe_values(value):
        if token not in allowed_values:
            errors.append(f"Unknown {field_name}: {token}")
    return errors

def validate_semantic_record(record):
    errors = []
    errors.extend(
        validate_pipe_values(
            record.get("evidence_tier", record.get("evidence_tier_summary", "")),
            ALLOWED_EVIDENCE_TIERS,
            "evidence_tier",
        )
    )
    errors.extend(
        validate_pipe_values(
            record.get("semantic_channel", record.get("semantic_channel_summary", "")),
            ALLOWED_SEMANTIC_CHANNELS,
            "semantic_channel",
        )
    )
    errors.extend(
        validate_pipe_values(
            record.get("evidence_semantics", record.get("evidence_semantics_summary", "")),
            ALLOWED_EVIDENCE_SEMANTICS,
            "evidence_semantics",
        )
    )
    return errors
