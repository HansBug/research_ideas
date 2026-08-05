"""A behavioural claim anchored at a projection artefact asks about the compiler, not the model.

Pair 0050's specification says takeover happens `in (auto final)`. The model declares no such
substate; what it does have is `AutonomousMode.FinalWaittr_0005`, injected by the R4.5
projection as a completion hold and listed in `attribution_exclusions`. On `v4run2` the
splitter bound that node as the `source` of a behavioural claim:

    REQ-M005C  reaches(source=…AutonomousMode.FinalWaittr_0005, target=…HumanDrivingMode,
                       within_cycles=3)   → True

It is True -- the projection really does route `FinalWaittr_0005` onward -- so the cell
published nothing at all. The defect the specification points at (a named substate the model
lacks) went unreported, and pair 0050 dropped from three-for-three to two-for-three.

The prompt already forbids this exact binding, by name: "`FinalWaittr_0005` and 'auto final'
are not the same state merely because both are substates of the autonomous mode". Prose fired
on two of three rounds. Across four generations the same pattern holds every time -- a rule
in prose fires at a rate, a rule in a gate fires always -- so this one moves to a gate,
shaped like `root_anchored_findings` and `initialization_anchored_findings` before it.

Scope: behavioural predicates only, and only `source`/`scope`. A *declarative* claim about a
projection artefact is legitimate -- `state_declared(FinalWaittr_0005)` is a true statement
about what the projection produced, and `_omission_placeholder_only` already handles the case
where such an element is the evidence of an omission. What cannot be asked is "what does a run
starting here do", because the run starts somewhere the author never wrote.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover.capability import (  # noqa: E402
    projection_anchored_findings,
)

NS = "llms_emp_feedback_final_0050"
#: What pair 0050's working contract actually lists. `FinalWaittr_0005` is a completion hold
#: the projection adds for a nested PlantUML final state; `R45RouteToken` is the routing
#: variable it adds to every projected model.
EXCLUSIONS = (
    f"compiler:state:{NS}.AutonomousMode.FinalWaittr_0005",
    "compiler:route_control:R45RouteToken",
)


class _Req:
    def __init__(self, requirement_id: str, predicate: str, bindings: dict[str, str]):
        self.requirement_id = requirement_id
        self.predicate = predicate
        self.predicate_bindings = bindings


def _findings(*requirements: _Req) -> tuple[str, ...]:
    return projection_anchored_findings(requirements, EXCLUSIONS)


def test_a_behavioural_source_on_a_projection_artefact_is_refused() -> None:
    """The exact binding that cost pair 0050 a round."""
    findings = _findings(
        _Req(
            "REQ-M005C",
            "reaches",
            {
                "source": f"{NS}.AutonomousMode.FinalWaittr_0005",
                "target": f"{NS}.HumanDrivingMode",
                "within_cycles": "3",
            },
        )
    )
    assert len(findings) == 1
    assert "REQ-M005C" in findings[0]
    assert "FinalWaittr_0005" in findings[0]


def test_the_finding_says_what_to_do_instead() -> None:
    """A refusal with no legal move is how the no-progress gate turns into a dead cell.

    That is not hypothetical here: the substituted-binding gate added one generation earlier
    killed a cell within two rounds for exactly this reason.
    """
    findings = _findings(
        _Req(
            "REQ-M005C",
            "reaches",
            {"source": f"{NS}.AutonomousMode.FinalWaittr_0005", "target": f"{NS}.HumanDrivingMode"},
        )
    )
    assert "the author wrote" in findings[0] or "作者" in findings[0] or "declared" in findings[0]


def test_a_behavioural_scope_is_refused_too() -> None:
    """`terminates` names its subject `scope`; the question it asks is the same one."""
    findings = _findings(
        _Req(
            "REQ-M006",
            "terminates",
            {"scope": f"{NS}.AutonomousMode.FinalWaittr_0005", "trigger": f"{NS}.Power_Off"},
        )
    )
    assert len(findings) == 1
    assert "scope" in findings[0]


def test_a_declarative_claim_about_the_artefact_is_allowed() -> None:
    """`state_declared(FinalWaittr_0005)` is a true statement about what the projection made.

    Refusing it would also refuse the omission-placeholder evidence the attribution layer was
    taught to accept one generation earlier -- the two rules have to agree.
    """
    findings = _findings(
        _Req(
            "REQ-M002",
            "state_declared",
            {"state": f"{NS}.AutonomousMode.FinalWaittr_0005", "kind": "any"},
        )
    )
    assert findings == ()


def test_a_declared_state_is_not_refused() -> None:
    findings = _findings(
        _Req(
            "REQ-M005",
            "reaches",
            {"source": f"{NS}.AutonomousMode", "target": f"{NS}.HumanDrivingMode"},
        )
    )
    assert findings == ()


def test_a_non_source_binding_on_the_artefact_is_not_refused() -> None:
    """Only the subject of the run matters. Reaching *into* a projected node is observable.

    A claim that the machine ends up at a completion hold is about the machine's behaviour,
    not about a run the author never authored -- and refusing it would block legitimate work.
    """
    findings = _findings(
        _Req(
            "REQ-M005D",
            "reaches",
            {
                "source": f"{NS}.AutonomousMode",
                "target": f"{NS}.AutonomousMode.FinalWaittr_0005",
            },
        )
    )
    assert findings == ()


def test_the_route_control_token_is_covered_too() -> None:
    """`R45RouteToken` is added to every projected model; a run anchored on it is meaningless."""
    findings = _findings(
        _Req("REQ-X", "stays_in", {"source": "R45RouteToken", "trigger": f"{NS}.Power_Off"})
    )
    assert len(findings) == 1


def test_no_exclusions_means_no_gate() -> None:
    """A pair whose contract lists nothing must not have every binding refused."""
    assert (
        projection_anchored_findings(
            (
                _Req(
                    "REQ-M005C",
                    "reaches",
                    {"source": f"{NS}.AutonomousMode.FinalWaittr_0005"},
                ),
            ),
            (),
        )
        == ()
    )


def test_every_offending_requirement_gets_its_own_finding() -> None:
    findings = _findings(
        _Req("REQ-A", "reaches", {"source": f"{NS}.AutonomousMode.FinalWaittr_0005"}),
        _Req("REQ-B", "stays_in", {"source": f"{NS}.AutonomousMode.FinalWaittr_0005"}),
    )
    assert len(findings) == 2


def test_the_model_root_is_not_treated_as_a_projection_artefact() -> None:
    """`compiler:root:<ns>` is on the exclusion list, but the author wrote the root.

    `root_anchored_findings` already refuses a behavioural claim anchored there, and it carries
    the exemptions that decision needs -- `containment`, `initial_target` and `cardinality` ask
    what the model declares about itself, so the root is their legitimate subject. Folding the
    root in here would refuse `terminates(scope=<root>)` for a sentence that really is about the
    whole system shutting down. The corpus has three such requirements, all in v1's gpt cells: two `terminates(scope=root)`
    and one `occupancy_after(source=root)`.
    """
    exclusions = (*EXCLUSIONS, f"compiler:root:{NS}")
    findings = projection_anchored_findings(
        (_Req("REQ-M006", "terminates", {"scope": NS, "trigger": f"{NS}.Power_Off"}),),
        exclusions,
    )
    assert findings == ()


def test_a_real_artefact_is_still_refused_when_the_root_is_listed() -> None:
    """Excluding the root must not disable the gate for everything else on the list."""
    exclusions = (*EXCLUSIONS, f"compiler:root:{NS}")
    findings = projection_anchored_findings(
        (
            _Req(
                "REQ-M005C",
                "reaches",
                {"source": f"{NS}.AutonomousMode.FinalWaittr_0005", "target": f"{NS}.HumanDrivingMode"},
            ),
        ),
        exclusions,
    )
    assert len(findings) == 1
