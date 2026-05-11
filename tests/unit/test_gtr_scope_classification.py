from gene_set_consensus.gtr_scope import (
    classify_scope_from_gene_count,
    classify_scope_assignment_method,
)

def test_single_gene_is_targeted():
    assert classify_scope_from_gene_count(1) == "targeted_gene"

def test_small_panel_classification():
    assert classify_scope_from_gene_count(10) == "small_panel"

def test_medium_panel_classification():
    assert classify_scope_from_gene_count(50) == "medium_panel"

def test_large_panel_classification():
    assert classify_scope_from_gene_count(500) == "large_panel"

def test_targeted_upper_boundary():
    assert classify_scope_from_gene_count(5) == "targeted_gene"

def test_small_upper_boundary():
    assert classify_scope_from_gene_count(25) == "small_panel"

def test_medium_upper_boundary():
    assert classify_scope_from_gene_count(100) == "medium_panel"

def test_exome_assignment_method():
    assert classify_scope_assignment_method("exome") == "explicit_exome_genome"

def test_genome_assignment_method():
    assert classify_scope_assignment_method("genome") == "explicit_exome_genome"

def test_empirical_assignment_method():
    assert classify_scope_assignment_method("small_panel") == "empirical_gene_count"

def test_unsized_assignment_method():
    assert classify_scope_assignment_method("panel_unsized") == "text_category_heuristic"

def test_unknown_assignment_method():
    assert classify_scope_assignment_method("weird_scope") == "unknown"
