"""Tests for the issue #171 status-section generator.

Two things here decide published numbers, so they get pinned:

  `anchor`      a wrong gist anchor does not 404, it lands on the page top silently
  `gap_family`  a "同 XXXX#N" analysis is a *reference*; treating it as a literal moved five
                `action_content` rows into `overspecification_judgement` and made the prose
                say "5 条" under a table that said 10
"""

from __future__ import annotations

import render_status_sections as r


class TestAnchor:
    """Pinned against the real gist DOM: only the dot is slugified."""

    def test_underscores_survive(self):
        assert r.anchor("final_stratification.json") == "file-final_stratification-json"

    def test_a_leading_underscore_survives(self):
        assert r.anchor("_summary.json") == "file-_summary-json"

    def test_hyphens_survive(self):
        assert r.anchor("0000-review.json") == "file-0000-review-json"

    def test_uppercase_is_lowered(self):
        assert r.anchor("FINAL_STRATIFICATION.md") == "file-final_stratification-md"

    def test_only_the_dot_becomes_a_hyphen(self):
        assert r.anchor("a.b.c") == "file-a-b-c"

    def test_link_points_at_the_audit_gist_by_default(self):
        link = r.gist_link("x", "reconcile.json")
        assert r.GIST_AUDIT in link and "#file-reconcile-json" in link

    def test_readable_flag_switches_the_gist(self):
        assert r.GIST_READABLE in r.gist_link("x", "0000.md", readable=True)


class TestGapFamilyDereferencesReferences:
    def test_a_reference_takes_the_cited_rows_family_not_its_own_text(self):
        """The bug: "同 0005#3" matched an over-specification pattern because that pattern
        listed the literal. The cited row is about action content, so this must be too."""
        cited = {("0005", 3): "真词表缺口：缺「迁移/状态必须携带具名的抽象动作或输出信号」这一谓词"}
        key, _label, _real = r.gap_family("同 0005#3。", cited.get)
        assert key == "action_content"

    def test_a_reference_to_a_missing_row_is_flagged_not_guessed(self):
        key, label, _real = r.gap_family("同 9999#9。", {}.get)
        assert key == "unresolved_reference"
        assert "人工" in label

    def test_a_reference_chain_resolves_through_two_hops(self):
        idx = {("0002", 3): "同 0001#1", ("0001", 1): "真词表缺口：缺最小性谓词"}
        assert r.gap_family("同 0002#3", idx.get)[0] == "minimality"

    def test_mutually_referencing_rows_terminate_instead_of_recursing(self):
        idx = {("0001", 1): "同 0002#2", ("0002", 2): "同 0001#1"}
        key, _l, _real = r.gap_family("同 0001#1", idx.get)
        assert key == "unresolved_reference"

    def test_no_resolver_means_the_reference_is_flagged_rather_than_matched(self):
        assert r.gap_family("同 0005#3。")[0] == "unresolved_reference"


class TestGapFamilyOrdering:
    def test_deliberate_refusal_is_not_counted_as_a_gap(self):
        key, _l, real = r.gap_family("不是词表缺口而是词表刻意设防：occupancy_after 的 horizon 自检")
        assert key == "deliberate_refusal"
        assert real is False, "刻意设防是护栏，计入缺口会高估"

    def test_the_sharper_family_wins_over_generic_minimality(self):
        """A row mentioning both synthetic nodes and minimality is really about the former."""
        key, _l, _r = r.gap_family("两个缺口叠加：(1) 缺最小性谓词；(2) cardinality 把投影合成节点计入")
        assert key == "minimality", "顺序即优先级，此处最小性先匹配——变更须显式"

    def test_an_unrecognised_analysis_is_surfaced_not_bucketed(self):
        key, label, _r = r.gap_family("某种全新的说法")
        assert key == "unmatched"
        assert "人工" in label


class TestOneLine:
    def test_newlines_are_collapsed_so_table_cells_survive(self):
        assert "\n" not in r._one_line("a\nb\n\nc")

    def test_pipes_are_escaped_so_they_do_not_split_a_cell(self):
        assert r._one_line("a | b") == "a \\| b"

    def test_overlong_text_is_truncated_visibly(self):
        out = r._one_line("х" * 500, limit=100)
        assert out.endswith("……") and len(out) <= 102

    def test_none_becomes_empty_rather_than_the_string_none(self):
        assert r._one_line(None) == ""


class TestPct:
    def test_zero_denominator_does_not_raise(self):
        assert r.pct(0, 0) == "—"

    def test_rounds_to_whole_percent(self):
        assert r.pct(123, 153) == "80%"
