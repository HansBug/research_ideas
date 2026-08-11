from __future__ import annotations

from paper_stm_conversion.normalization.plantuml import normalize_plantuml
from paper_stm_conversion.normalization.semantic_audit import audit_plantuml_semantic_preservation


def test_quoted_endpoint_alias_is_low_risk_and_preserves_label():
    raw = '@startuml\n[*] --> "Menu Created"\n"Menu Created" --> "Adding Items"\n@enduml\n'
    result = normalize_plantuml(raw)
    assert 'state "Menu Created" as ' in result.normalized_text
    assert '"Menu Created" -->' not in result.normalized_text
    assert result.low_risk_candidate is True
    assert result.main_eligibility_default is True
    assert set(result.rule_ids) == {"PUML.NORM.alias_quoted_endpoint"}


def test_multiword_endpoint_alias_is_low_risk():
    raw = "@startuml\n[*] --> Ready to Tag\nReady to Tag --> Processing New Item : New item added\n@enduml\n"
    result = normalize_plantuml(raw)
    assert 'state "Ready to Tag" as ' in result.normalized_text
    assert 'state "Processing New Item" as ' in result.normalized_text
    assert "Ready to Tag -->" not in result.normalized_text
    assert result.low_risk_candidate is True
    assert "PUML.NORM.alias_multiword_endpoint" in result.rule_ids


def test_embedded_pseudostate_marker_endpoint_is_high_risk():
    raw = "@startuml\nResolved --> Closed [*]\nSuggestRoutine --> Final [*]\n@enduml\n"
    result = normalize_plantuml(raw)
    assert 'state "Closed [*]" as ' in result.normalized_text
    assert 'state "Final [*]" as ' in result.normalized_text
    assert "PUML.NORM.alias_embedded_pseudostate_marker" in result.rule_ids
    assert result.has_high_risk_loss is True
    assert result.low_risk_candidate is False
    assert result.main_eligibility_default is False
    assert all(
        change.risk_tier == "high_risk"
        for change in result.changes
        if change.rule_id == "PUML.NORM.alias_embedded_pseudostate_marker"
    )


def test_ambiguous_arrow_patterns_are_not_collapsed_into_low_risk_aliases():
    raw = "@startuml\n[*] <--> [*]\nPreparingToShare --> [Error] --> SelectingPlatform\n@enduml\n"
    result = normalize_plantuml(raw)
    assert result.changes == []
    assert result.normalized_text == raw


def test_high_risk_action_and_dependency_are_excluded_from_main_eligibility():
    raw = "@startuml\nstate A {\n  entry/Start motor\n}\n[*] <.. A\n@enduml\n"
    result = normalize_plantuml(raw)
    assert "normalization-commented action" in result.normalized_text
    assert "normalization-commented dependency-like arrow" in result.normalized_text
    assert result.has_high_risk_loss is True
    assert result.low_risk_candidate is False
    assert result.main_eligibility_default is False
    assert "PUML.NORM.entry_do_exit_rewrite_or_loss" in result.rule_ids
    assert "PUML.NORM.comment_dependency_arrow" in result.rule_ids


def test_fork_join_sets_concurrency_degraded_and_excludes_main_eligibility():
    raw = "@startuml\nfork fork1\nA --> fork1\n@enduml\n"
    result = normalize_plantuml(raw)
    assert 'state "fork1" as fork1' in result.normalized_text
    assert result.concurrency_degraded is True
    assert result.main_eligibility_default is False
    assert any(c.rule_id == "PUML.NORM.fork_join_decl_to_state" and c.concurrency_degraded for c in result.changes)


def test_semantic_preservation_audit_accepts_alias_only_rewrite():
    raw = '@startuml\n[*] --> "Menu Created"\n"Menu Created" --> "Adding Items" : Add\n@enduml\n'
    result = normalize_plantuml(raw)
    audit = audit_plantuml_semantic_preservation(
        raw,
        result.normalized_text,
        introduced_alias_declarations=result.alias_declarations,
        rule_ids=result.rule_ids,
    )
    assert audit["pass"] is True
    assert audit["differences"]["transitions"]["missing_count"] == 0
    assert audit["differences"]["transitions"]["added_count"] == 0

def test_semantic_preservation_audit_documents_source_signature_not_strict_equivalence():
    raw = '''@startuml
state "Original" as A_B_afaff9
[*] --> A-B
A-B --> Done
@enduml
'''
    result = normalize_plantuml(raw)
    audit = audit_plantuml_semantic_preservation(
        raw,
        result.normalized_text,
        introduced_alias_declarations=result.alias_declarations,
        rule_ids=result.rule_ids,
    )
    assert result.low_risk_candidate is True
    assert audit["pass"] is True
    assert "source-level" in audit["scope"]
    assert any("not a theorem-level semantic equivalence proof" in item for item in audit["limitations"])


def test_code_rules_match_documented_plantuml_rules_registry():
    import json
    from pathlib import Path

    from paper_stm_conversion.normalization.plantuml import RULES

    root = Path(__file__).resolve().parents[1]
    registry = json.loads((root / "normalization" / "plantuml_rules.json").read_text(encoding="utf-8"))
    documented = {row["rule_id"]: row for row in registry["rules"]}
    assert set(RULES) == set(documented)
    for rule_id, code_row in RULES.items():
        doc_row = documented[rule_id]
        assert code_row["semantic_risk"] == doc_row["semantic_risk"]
        assert code_row["risk_tier"] == doc_row["risk_tier"]
        assert code_row["main_eligibility_default"] == doc_row["main_eligibility_default"]
    assert documented["PUML.NORM.fork_join_decl_to_state"]["concurrency_degraded"] is True


def test_when_transition_label_is_normalized_without_dropping_guard_cue():
    raw = "@startuml\nchoice2 --> Join1 when : sunny=true\n@enduml\n"
    result = normalize_plantuml(raw)
    assert "choice2 --> Join1 : when sunny=true" in result.normalized_text
    assert "choice2 --> Join1 when : sunny=true" not in result.normalized_text
    assert "PUML.NORM.transition_when_label" in result.rule_ids
    assert result.low_risk_candidate is True
    change = next(c for c in result.changes if c.rule_id == "PUML.NORM.transition_when_label")
    assert change.span == "transition_label"
    assert "guard-like cue" in change.rationale


def test_empty_transition_label_colon_is_removed_as_low_risk_syntax_cleanup():
    raw = "@startuml\nchoice1 --> choice3:\nFlash --> Terminate:\n@enduml\n"
    result = normalize_plantuml(raw)
    assert "choice1 --> choice3\n" in result.normalized_text
    assert "Flash --> Terminate\n" in result.normalized_text
    assert "choice1 --> choice3:" not in result.normalized_text
    assert result.rule_ids == ["PUML.NORM.remove_empty_transition_label"]
    assert result.low_risk_candidate is True
    assert all(c.kind == "remove_empty_transition_label" for c in result.changes)


def test_non_star_bracket_endpoint_alias_preserves_star_pseudostate():
    raw = "@startuml\n[FrontendCollision] -down-> [BrakingControl] : Brake Signal Received\n[BrakingControl] --> [*] : Collision Avoided\n@enduml\n"
    result = normalize_plantuml(raw)
    assert 'state "FrontendCollision" as ' in result.normalized_text
    assert 'state "BrakingControl" as ' in result.normalized_text
    assert "--> [*] : Collision Avoided" in result.normalized_text
    assert "PUML.NORM.alias_bracket_endpoint" in result.rule_ids
    assert "PUML.NORM.alias_embedded_pseudostate_marker" not in result.rule_ids
    assert result.low_risk_candidate is True


def test_r5_5_2_blocked_patterns_are_low_risk_normalized_together():
    raw = """@startuml
stm CameraSystem
[*] --> TurnOn
TurnOn --> fork1: after 2s
choice1 --> choice3:
choice2 --> Join1 when : sunny=true
[FrontendCollision] -down-> [BrakingControl] : Brake Signal Received
[BrakingControl] --> [*] : Collision Avoided
@enduml
"""
    result = normalize_plantuml(raw)
    assert "normalization removed non-PlantUML stm heading" in result.normalized_text
    assert "choice1 --> choice3\n" in result.normalized_text
    assert "choice2 --> Join1 : when sunny=true" in result.normalized_text
    assert "--> [*] : Collision Avoided" in result.normalized_text
    assert {
        "PUML.NORM.remove_stm_heading",
        "PUML.NORM.remove_empty_transition_label",
        "PUML.NORM.transition_when_label",
        "PUML.NORM.alias_bracket_endpoint",
    }.issubset(set(result.rule_ids))
    assert result.has_high_risk_loss is False
    assert result.main_eligibility_default is True
