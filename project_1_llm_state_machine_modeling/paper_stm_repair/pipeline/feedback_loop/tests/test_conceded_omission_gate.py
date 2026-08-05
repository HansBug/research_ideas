"""A concession filed in `limitations` cannot come back False, so it is not a finding.

Pair 0050's specification says takeover happens `in (auto final)`. The model declares no such
substate. On `v5run1` the splitter saw that and wrote it down:

    REQ-M005a.limitations[1] =
        「auto final 是 NL 提及的名称;模型未声明此名的子状态,声明的是 FinalWaittr_0005」

-- exactly step 4's trigger condition, stated correctly -- and then bound the behavioural claim
to `SubState1/2/3`, three substates that do exist. All eleven released assertions came back True,
`coverage_status` was `full`, and the cell published nothing.

That is the second way a rule kept in prose fails. The familiar way is that it does not fire.
This way it fires, the model reaches the right conclusion, and the conclusion lands somewhere
with no consequences. It is harder to spot because the trace looks correct.

The check here is on the model's own output, not on the NL: concede that a name the NL used is
undeclared, and something in the batch has to claim it -- a binding the model never declared,
which can therefore fail. Feasibility over all 15 rounds before this shipped: rejects `v5run1`,
passes `v5run3`, zero rejections on `0029-claude` and `0006-claude`, 43 rejections corpus-wide.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover.capability import (  # noqa: E402
    conceded_omission_findings,
)

NS = "llms_emp_feedback_final_0050"
DECLARED = (
    NS,
    f"{NS}.AutonomousMode",
    f"{NS}.AutonomousMode.SubState1",
    f"{NS}.AutonomousMode.SubState2",
    f"{NS}.AutonomousMode.SubState3",
    f"{NS}.AutonomousMode.FinalWaittr_0005",
    f"{NS}.HumanDrivingMode",
    f"{NS}.Power_Off",
)


class _Req:
    def __init__(
        self,
        requirement_id: str,
        predicate: str,
        bindings: dict[str, str],
        limitations: tuple[str, ...] = (),
    ):
        self.requirement_id = requirement_id
        self.predicate = predicate
        self.predicate_bindings = bindings
        self.limitations = limitations


#: The round that lost the cell: a correct concession, and a behavioural claim on a sibling.
CONCEDED = _Req(
    "REQ-M005a",
    "occupancy_after",
    {"source": f"{NS}.AutonomousMode.SubState1", "target": f"{NS}.HumanDrivingMode"},
    ("auto final 是 NL 提及的名称;模型未声明此名的子状态,声明的是 FinalWaittr_0005",),
)
#: The round that hit: the same concession plus an assertion that can fail.
PROPOSAL = _Req(
    "REQ-M005b",
    "state_declared",
    {"state": f"{NS}.AutonomousMode.auto_final", "kind": "any"},
    ("模型未声明名为 'auto final' 的状态",),
)


def _findings(*requirements: _Req) -> tuple[str, ...]:
    return conceded_omission_findings(requirements, DECLARED)


def test_a_concession_with_no_claim_is_refused() -> None:
    findings = _findings(CONCEDED)
    assert len(findings) == 1
    assert "REQ-M005a" in findings[0]
    assert "auto final" in findings[0]


def test_the_finding_names_the_legal_move() -> None:
    """A refusal with no way forward is how a gate turns a cell into a no-progress kill."""
    findings = _findings(CONCEDED)
    assert "Step 4" in findings[0]
    assert "propose" in findings[0]


def test_a_claim_elsewhere_in_the_batch_satisfies_it() -> None:
    """`v5run3`: same concession, plus `state_declared(auto_final)`. Must not be disturbed."""
    assert _findings(CONCEDED, PROPOSAL) == ()


def test_a_claim_carried_by_a_behavioural_binding_also_counts() -> None:
    """Pair 0006 proposes `MissionComplete` through `persists_until(release=...)`.

    Reading only the `*_declared` predicates called that a bare concession on three rounds.
    """
    conceded = _Req(
        "REQ-001",
        "persists_until",
        {
            "scope": f"{NS}.AutonomousMode",
            "release": f'active("{NS}.MissionComplete")',
        },
        ("模型未声明表示『任务完成』的状态或事件;按第 4 步提议 MissionComplete",),
    )
    assert conceded_omission_findings((conceded,), DECLARED) == ()


def test_a_concession_naming_nothing_extractable_is_left_alone() -> None:
    """115 of the corpus's 246 concessions are like this. Missing beats refusing blind."""
    vague = _Req(
        "REQ-X",
        "occupancy_after",
        {"source": f"{NS}.AutonomousMode", "target": f"{NS}.HumanDrivingMode"},
        ("模型未声明足以区分这三个条件的独立事件,按合并事件绑定",),
    )
    assert conceded_omission_findings((vague,), DECLARED) == ()


def test_the_four_step_procedure_is_not_read_as_the_missing_name() -> None:
    """`step 4` / `步骤 4` are cited constantly; reading one as a name refuses a real proposal."""
    conceded = _Req(
        "REQ-006",
        "variable_declared",
        {"variable": f"{NS}.uav_count"},
        ("模型未声明表示无人机数量的作者变量；uav_count 由 NL 措辞提出（step 4）",),
    )
    assert conceded_omission_findings((conceded,), DECLARED) == ()


def test_a_compiler_owned_name_is_not_read_as_the_missing_name() -> None:
    """A concession routinely rules out the compiler's own names as substitutes."""
    conceded = _Req(
        "REQ-005",
        "variable_declared",
        {"variable": f"{NS}.uav_count"},
        ("模型未声明任何作者自定义变量(R45RouteToken 为编译器所有),因此按 step 4 提出 uav_count",),
    )
    assert conceded_omission_findings((conceded,), DECLARED) == ()


def test_a_requirement_with_no_concession_is_not_examined() -> None:
    plain = _Req(
        "REQ-M001",
        "state_declared",
        {"state": f"{NS}.HumanDrivingMode", "kind": "leaf"},
        ("NL 将三个条件作为联合触发保留;模型以一个复合事件名表示",),
    )
    assert conceded_omission_findings((plain,), DECLARED) == ()


def test_the_declared_substitute_named_in_the_same_breath_is_not_the_missing_name() -> None:
    """The concession names `FinalWaittr_0005`, which IS declared -- it is the substitute."""
    findings = _findings(CONCEDED)
    assert "FinalWaittr_0005" not in findings[0]


def test_no_declared_paths_disables_the_gate() -> None:
    """Without the model's vocabulary there is nothing to call undeclared."""
    assert conceded_omission_findings((CONCEDED,), ()) == ()


def test_every_offending_requirement_gets_its_own_finding() -> None:
    second = _Req(
        "REQ-M006",
        "reaches",
        {"source": f"{NS}.AutonomousMode.SubState2", "target": f"{NS}.HumanDrivingMode"},
        ("模型未声明名为 'auto final' 的状态",),
    )
    assert len(_findings(CONCEDED, second)) == 2
