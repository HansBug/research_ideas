"""A filtered compiler variable must not disqualify the evidence that filtered it.

Pair 0006's expected defect (`EXP-0006-EA-001`) is that the model declares no
UAV-count decrement after `Attack_Complete`.  The only effect on that transition
is the converter's own route-control variable:

    AttackingTarget -> [*] : /Attack_Complete effect { R45RouteToken = 7; };

`effect_deltas` drops `R45RouteToken` (it is in the frozen source exclusions) and
correctly returns `[]`, so the assertion is False -- the defect is detected.  But
the reference collector then reported `route_control:R45RouteToken` as an element
the evidence *touched*, `bind_attribution` matched it against
`compiler:route_control:R45RouteToken`, and the finding was filed as
`representation_debt` in both models.

The query was disqualified for looking at the very thing it filtered out.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.assertions import (  # noqa: E402
    AssertionChecker,
    build_eval_environment,
)
from paper_stm_feedback_loop.discover.nodes import (  # noqa: E402
    _reference_matches_observed,
)

# Same shape as pair 0006: the only effect on the event-bearing transition is a
# compiler route-control variable, and there is no semantic quantity at all.
MODEL = """def int R45RouteToken = 0;

state Root {
    event done;
    event go;
    state Working {
        state Busy;
        [*] -> Busy;
        Busy -> [*] : /done effect { R45RouteToken = 7; };
    }
    state Idle;
    [*] -> Idle;
    Idle -> Working : /go;
    Working -> Idle : if [R45RouteToken == 7] effect { R45RouteToken = 0; };
}
"""

EXCLUSIONS = ["compiler:route_control:R45RouteToken"]


def _checker() -> AssertionChecker:
    return AssertionChecker(
        environment=build_eval_environment(
            model_text=MODEL,
            source_mappings=[],
            source_exclusions=EXCLUSIONS,
            timeout_seconds=10,
        )
    )


def _refs(expression: str, families: tuple[str, ...]) -> set[str]:
    result = _checker().check(
        f'assert {expression}, "[REQ-001][AST-001] probe"',
        "probe",
        required_function_families=families,
    )
    return {
        ref
        for call in result.to_json().get("function_call_trace") or []
        for ref in call.get("model_refs") or []
    }


def test_effect_query_still_detects_the_missing_quantity() -> None:
    result = _checker().check(
        'assert any(d < 0 for _, d in effect_deltas(source="Root.Working.Busy", '
        'event="Root.done")), "[REQ-001][AST-001] no decrement"',
        "probe",
        required_function_families=("effect",),
    )
    assert result.outcome == "sealed_false"
    assert result.value is False


def test_effect_query_does_not_report_the_variable_it_filtered_as_touched() -> None:
    refs = _refs(
        'any(d < 0 for _, d in effect_deltas(source="Root.Working.Busy", event="Root.done"))',
        ("effect",),
    )
    assert "route_control:R45RouteToken" not in refs
    # The audit trail survives under a kind attribution does not read as debt.
    assert "filtered_route_control:R45RouteToken" in refs


def test_filtered_marker_does_not_match_the_compiler_exclusion() -> None:
    observed = {"filtered_route_control:R45RouteToken", "Root.Working.Busy"}
    assert not _reference_matches_observed(EXCLUSIONS[0], observed)
    # The unfiltered form must still match, or lowering detection would break.
    assert _reference_matches_observed(
        EXCLUSIONS[0], {"route_control:R45RouteToken"}
    )


def test_relation_queries_still_signal_converter_lowering() -> None:
    """A relation False caused by lowering must keep reporting debt.

    The route token is how the converter splits a composite exit, so its
    presence in a *relation* match is genuine representation evidence and must
    not be softened by this change.
    """

    refs = _refs(
        'transition_exists(source="Root.Working", target="Root.Idle")',
        ("relation",),
    )
    assert "route_control:R45RouteToken" in refs
    assert "filtered_route_control:R45RouteToken" not in refs
