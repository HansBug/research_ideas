"""The fabrication detector has to be checked, or "0 fabricated" means nothing.

`detect_fabrications.py` is what scores a new run, so a silent failure in it reads
as a clean result.  Two parts can fail silently:

  * `_parse_call` -- a predicate call it cannot parse is skipped, not reported
  * `_default_entry_of` -- brace-depth scanning that returns None for a composite
    that does have an unconditional entry would clear a real fabrication

Both are checked against the real corpus, where the answers are known
independently: pair 0029's `HighwayMode` and `UrbanMode` each carry a synthetic
`[*] -> UnspecifiedInitial` beside a token-guarded authored entry, and pair 0006's
`UAVSwarmStateMachine` carries an authored `[*] -> Searching` and no synthetic one.

The end-to-end arm re-creates the old refs behaviour rather than reverting the fix,
because the detector's job is to catch a *recurrence*.

Run:
    PYTHONPATH=<repo root> pytest project_1_llm_state_machine_modeling/eval/discover_matrix
"""

from __future__ import annotations

import pathlib
import sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import detect_fabrications as detect  # noqa: E402

R0029 = "llms_emp_feedback_final_0029"
R0006 = "llms_emp_feedback_final_0006"
MODEL_DIR = detect.REPORT / "fcstm"


def _model(case: str) -> str:
    return (MODEL_DIR / f"llms_emp_feedback_final_{case}.fcstm").read_text()


@pytest.mark.parametrize(
    "expression, predicate, bindings",
    [
        (
            'initial_target(composite="A.B", child="A.B.C") is True',
            "initial_target",
            {"composite": "A.B", "child": "A.B.C"},
        ),
        (
            'occupancy_after(source="A.X", trigger="A.e", target="A.Y", within_cycles=2) is True',
            "occupancy_after",
            {"source": "A.X", "trigger": "A.e", "target": "A.Y", "within_cycles": "2"},
        ),
        # Single quotes and extra whitespace occur in real scripts.
        (
            "containment( parent='A.P' , child='A.P.Q' )  is  True",
            "containment",
            {"parent": "A.P", "child": "A.P.Q"},
        ),
    ],
)
def test_the_call_parser_reads_the_shapes_real_scripts_use(expression, predicate, bindings):
    parsed = detect._parse_call(expression)
    assert parsed is not None, expression
    assert parsed == (predicate, bindings)


def test_the_call_parser_reports_failure_instead_of_a_wrong_parse():
    """A skipped call is a missed fabrication, so the failure has to be visible."""

    assert detect._parse_call("not a call at all") is None
    assert detect._parse_call("") is None


def test_the_default_entry_scan_finds_the_synthetic_entry_on_the_real_corpus():
    """These two are exactly the composites matrix-v16 fabricated findings about."""

    model = _model("0029")
    assert (
        detect._default_entry_of(model, f"{R0029}.HighwayMode")
        == f"{R0029}.HighwayMode.UnspecifiedInitial"
    )
    assert (
        detect._default_entry_of(model, f"{R0029}.UrbanMode")
        == f"{R0029}.UrbanMode.UnspecifiedInitial"
    )


def test_the_default_entry_scan_does_not_invent_one():
    """A composite whose only entry is authored must not be reported as synthetic."""

    model = _model("0006")
    entry = detect._default_entry_of(model, f"{R0006}.UAVSwarmStateMachine")
    assert entry == f"{R0006}.UAVSwarmStateMachine.Searching", entry
    # A composite that does not exist has no entry, rather than a wrong one.
    assert detect._default_entry_of(model, f"{R0006}.NoSuchComposite") is None


def _audit_bundle(tmp_path, cell, pair, requirement_id, expression):
    """A one-issue audit record, in the shape `build_gist.py` writes."""

    import json

    record = {
        "pair": pair,
        "terminal": "completed",
        "assertions": [{"assertion_id": "AST-1", "expression": expression}],
        "terminal_artifact": {
            "issues": [
                {
                    "requirement_id": requirement_id,
                    "title": "probe",
                    "assertion_ids": ["AST-1"],
                }
            ]
        },
    }
    (tmp_path / f"{cell}-audit.json").write_text(json.dumps(record))
    return tmp_path


def test_a_false_resting_on_a_converter_owned_element_is_reported(tmp_path):
    """The class matrix-v16 published twice, now decided by matching exclusions.

    `initial_target(HighwayMode, enter_hwy)` is False because the converter's
    synthetic unconditional entry targets `UnspecifiedInitial`, which the pair's
    `attribution_exclusions` list -- so the finding is representation debt and must
    not be a confirmed issue.  The refs fix is what makes the match possible; before
    it, the failing call named neither the entry nor the token.
    """

    bundle = _audit_bundle(
        tmp_path, "0029-claude-opus-4-7", "0029", "REQ-006",
        f'initial_target(composite="{R0029}.HighwayMode", '
        f'child="{R0029}.HighwayMode.enter_hwy") is True',
    )
    found = detect.scan(bundle)
    assert len(found) == 1, found
    assert found[0]["defect_class"] == "false-rests-on-converter-owned-element"
    assert "UnspecifiedInitial" in found[0]["evidence"]


def test_an_issue_whose_assertion_no_longer_fails_is_reported(tmp_path):
    """The horizon guard turns yesterday's fabrication into a refusal.

    Pair 0006's `Searching --detected--> Intercepted --(completion)--> Adjusting`
    was published as a defect over one cycle; the predicate now refuses that
    horizon, so an issue resting on it no longer stands.
    """

    bundle = _audit_bundle(
        tmp_path, "0006-claude-opus-4-7", "0006", "REQ-003",
        f'occupancy_after(source="{R0006}.UAVSwarmStateMachine.Searching", '
        f'trigger="{R0006}.Interception_Detected", '
        f'target="{R0006}.UAVSwarmStateMachine.FormationAdjustment", '
        f'within_cycles=1) is True',
    )
    found = detect.scan(bundle)
    assert len(found) == 1, found
    assert found[0]["defect_class"].startswith("published-issue-no-longer-false")


def test_a_genuine_defect_is_left_alone(tmp_path):
    """Otherwise the gate would reject the run for finding what it should find."""

    bundle = _audit_bundle(
        tmp_path, "0029-claude-opus-4-7", "0029", "REQ-012",
        f'occupancy_after(source="{R0029}.HighwayMode.cruise", '
        f'trigger="{R0029}.dist_to_exit_2", '
        f'target="{R0029}.HighwayMode.exit_hwy", within_cycles=1) is True',
    )
    assert detect.scan(bundle) == []


def test_an_unparseable_assertion_is_reported_rather_than_skipped(tmp_path):
    """A skipped issue would read as a clean one."""

    bundle = _audit_bundle(
        tmp_path, "0029-claude-opus-4-7", "0029", "REQ-999", "this is not a call"
    )
    found = detect.scan(bundle)
    assert len(found) == 1, found
    assert found[0]["defect_class"] == "unparseable-assertion"
