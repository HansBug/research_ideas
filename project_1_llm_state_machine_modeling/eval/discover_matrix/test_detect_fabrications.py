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


def test_it_catches_a_recurrence_of_the_refs_omission(monkeypatch):
    """Re-creates the pre-fix refs, since a recurrence is what it must catch.

    Reverting the fix would test the fix; suppressing just the one `_note` call
    tests the detector.
    """

    from paper_stm_feedback_loop.assertions.predicate_api import PredicateAPI

    original = PredicateAPI._note

    def note_without_the_entry(self, *refs):
        return original(self, *(r for r in refs if "UnspecifiedInitial" not in str(r)))

    monkeypatch.setattr(PredicateAPI, "_note", note_without_the_entry)

    env, model, exclusions = detect._environment("0029")
    verdict = detect._check_initial_target(
        env,
        model,
        exclusions,
        {"composite": f"{R0029}.HighwayMode", "child": f"{R0029}.HighwayMode.enter_hwy"},
    )
    assert verdict is not None
    assert verdict["defect_class"] == "initial-target-omits-deciding-entry-from-refs"
    assert "UnspecifiedInitial" in verdict["evidence"]


def test_it_clears_the_finding_once_the_entry_is_declared():
    """With the fix in place the same call is not reported, so the gate can pass."""

    env, model, exclusions = detect._environment("0029")
    assert (
        detect._check_initial_target(
            env,
            model,
            exclusions,
            {"composite": f"{R0029}.HighwayMode", "child": f"{R0029}.HighwayMode.enter_hwy"},
        )
        is None
    )
