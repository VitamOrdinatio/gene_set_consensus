def classify_scope_from_gene_count(genes_per_test):
    if genes_per_test <= 5:
        return "targeted_gene"
    if genes_per_test <= 25:
        return "small_panel"
    if genes_per_test <= 100:
        return "medium_panel"
    return "large_panel"

def classify_scope_assignment_method(test_scope):
    if test_scope in {"genome", "exome"}:
        return "explicit_exome_genome"
    if test_scope in {
        "targeted_gene",
        "small_panel",
        "medium_panel",
        "large_panel",
    }:
        return "empirical_gene_count"
    if test_scope == "panel_unsized":
        return "text_category_heuristic"
    return "unknown"
