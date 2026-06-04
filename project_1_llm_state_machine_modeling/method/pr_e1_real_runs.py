"""PR-E1 real agent-loop run exploration and reporting helpers.

PR-E1 is not a new runtime.  It is a thin, auditable runner around the
canonical ``method.loop.run_agent_loop(nl, LoopConfig(...))`` entry so that the
umbrella PR can compare real Path1/Path2 NL runs under a small set of explicit
budget/config conditions.

The module deliberately keeps three boundaries clear:

* ``default`` uses the unmodified ``full_staged_v1`` default and may be eligible
  for Path1/Path2 main-result status if the record itself succeeds.
* all budget/retry/review variants are explicit non-default conditions; even if
  they succeed, they are exploratory evidence rather than main-result rows.
* every run writes a single ``AgentLoopRunRecord`` plus lightweight derived
  artifacts (``final.fcstm``, ``summary.json``, ``report.md``, ``checks.json``)
  under a per-run directory.
"""

from __future__ import annotations

import argparse
import contextlib
import difflib
import hashlib
import gzip
import json
import os
import re
import subprocess
import time
import uuid
from urllib.parse import urlparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import MISSING, asdict, dataclass, field, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

from method.gpt_client import (
    DEFAULT_SDK_MAX_RETRIES,
    get_progress_log_enabled,
    get_request_timeout_seconds,
    get_stream_enabled,
    get_stream_include_usage_enabled,
)
from method.loop import LoopConfig, run_agent_loop
from method.pr_d_representative import (
    PATH1_CARA_NL,
    PATH2_LNG_EMS_NL,
    assert_pr_d_provider_env,
    missing_provider_env,
    representative_cases,
)
from method.run_record import is_path_result_eligible, read_agent_loop_run_record
from method.schema import AgentLoopResult, AgentLoopRunRecord, experiment_default_condition

RunAgentLoopFn = Callable[[str, LoopConfig], AgentLoopResult]

REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = REPO_ROOT / "project_1_llm_state_machine_modeling"

PR_E1_FULL_STAGED_REQUIRED_STAGE_IDS = [
    "SC-0",
    "SL-1",
    "SD-2",
    "SD-3",
    "SD-4",
    "SL-5",
    "SD-5A",
    "SC-5F",
    "SD-6",
    "SL-7",
    "SC-12",
    "SC-13",
]

PR_E1_REPAIR_STAGE_IDS = ["SD-8", "SL-9", "SL-10", "SC-11"]


PATH1_ABS_NL = """The paper implements the single-wheel ABS hydraulic regulator as a three-state FSM coupled with a PID-based slip controller. Wheel speed and vehicle speed are used to compute the slip ratio, and the PID output drives the Stateflow supervisor instead of sending commands directly to the hydraulic valves.

The FSM contains the states `increase`, `hold`, and `decrease`, where `increase` sets `k1=1, k2=0, n=0`, `hold` neutralizes both valves with `k1=0, k2=0, n=0`, and `decrease` sets `k1=0, k2=1, n=500` to release pressure.

The transition guards split the slip-error space into four bands: `increase -> hold` when `slp <= 0.01`, `hold -> increase` when `slp > 0.01`, `hold -> decrease` when `slp < -0.01`, and `decrease -> hold` when `slp >= -0.01`.

This gives a concrete discrete supervisor that maps slip-error thresholds to inlet-valve, return-valve, and pump actions while the continuous wheel-slip dynamics remain in the plant model."""


PATH1_ABS_NL_ZH = """论文把单轮 ABS 液压调节器实现为一个三状态 FSM，并与基于滑移率的 PID 控制器耦合。轮速与车速用于计算滑移率，PID 输出驱动 Stateflow 监督器，而不是直接发送液压阀命令。

FSM 包含 `increase`、`hold`、`decrease` 三个状态：`increase` 设置 `k1=1, k2=0, n=0`，`hold` 设置 `k1=0, k2=0, n=0`，`decrease` 设置 `k1=0, k2=1, n=500` 以释放压力。

转移 guard 把滑移误差空间分成四个区间：`increase -> hold` 当 `slp <= 0.01`，`hold -> increase` 当 `slp > 0.01`，`hold -> decrease` 当 `slp < -0.01`，`decrease -> hold` 当 `slp >= -0.01`。

这给出了一个具体的离散监督器，把滑移误差阈值映射为进油阀、回油阀与泵动作，而连续轮胎滑移动力学仍留在被控对象模型中。"""


PATH1_ELEVATOR_NL = """The automatic elevator controller is built as a finite-state machine whose state space combines floor states `F1`, `F2`, and `F3` with motion states `MU2`, `MU3`, `MD1`, and `MD2` for upward and downward travel.

In the normal workflow, the system starts from an ideal state on floor 1, chooses either the up or down branch according to floor requests, stops at the requested floor, and then immediately checks the next destination before deciding whether to continue moving.

The controller uses `PS1/PS2/PS3` as floor-request inputs and `S1/S2/S3` as sensing inputs for arrival. From `F1`, `PS2` triggers `MU2` and `PS3` triggers `MU3`. From `F2`, `PS3` triggers `MU3` and `PS1` triggers `MD1`. From `F3`, `PS1` triggers `MD1` and `PS2` triggers `MD2`. Arrival sensors complete motion transitions: `MU2 + S2 -> F2`, `MU3 + S3 -> F3`, `MD1 + S1 -> F1`, and `MD2 + S2 -> F2`.

The `hbrg` output distinguishes upward drive, downward drive, and stop conditions. A reset signal forces the controller back to floor 1 regardless of the outstanding request context."""


PATH1_ELEVATOR_NL_ZH = """自动电梯控制器被构建为有限状态机，其状态空间由楼层状态 `F1`、`F2`、`F3` 与上/下行运动状态 `MU2`、`MU3`、`MD1`、`MD2` 组合而成。

正常流程中，系统从 1 楼理想状态开始，根据楼层请求选择上行或下行分支，在请求楼层停止，然后立即检查下一目的地以决定是否继续移动。

控制器使用 `PS1/PS2/PS3` 作为楼层请求输入，使用 `S1/S2/S3` 作为到位传感输入。从 `F1`，`PS2` 触发 `MU2`，`PS3` 触发 `MU3`；从 `F2`，`PS3` 触发 `MU3`，`PS1` 触发 `MD1`；从 `F3`，`PS1` 触发 `MD1`，`PS2` 触发 `MD2`。到位传感器完成运动转移：`MU2 + S2 -> F2`，`MU3 + S3 -> F3`，`MD1 + S1 -> F1`，`MD2 + S2 -> F2`。

`hbrg` 输出区分上行驱动、下行驱动和停止状态。复位信号会无视当前请求上下文，强制控制器回到 1 楼。"""


PATH1_CARA_NL_ZH = """运行时，CARA 围绕一台向患者输液的输液泵协调 Caregiver Interface、Blood Pressure Monitor、Algorithm 与 Pump Monitors，传感器读数会写入共享缓冲区供软件访问。泵具有手动和自动控制两种模式。手动模式下，泵速由内置开关设置，护理人员直接在泵上设置默认流量；自动控制模式下，泵速由外部控制电压设置。Algorithm 组件控制输液速率并记录输液相关日志；患者血压用于计算输液速率，血压越高流量越低。Caregiver Interface 允许护理人员修改目标血压，并启动或终止算法泵控制，同时显示和发出错误消息。在 Mode_Control_Algorithm 层次中，CARA 具有手动与自动控制相关的模式控制状态以及 Ask_StartAC 子模式；在 Ask_StartAC 中可以修改设定点，按下 StartAC 会进入 AutocontrolInit。正常自动控制期间，只有没有泵操作并发症时 CARA 才控制流量。如果出现输液管堵塞等泵故障，泵会激活报警信号，护理人员排除故障；当 CARA 正在控制泵时，软件会释放控制。作为跨组件回退，CA_backManual 或 CB_backManual、CP_backManual、CC_backManual 中任一事件都会使 CA_mode 变为 Manual，使手动操作成为共享恢复目标。"""


PATH2_LNG_EMS_NL_ZH = """LNG 船 EMS 管理一个包含光伏、波浪能、柴油机、LNG、电池和随时间变化船舶负载的船舶能源系统，并向发电单元与负载发出切入/切出命令。它在变化的时段和运行条件下控制发电单元与负载需求之间的功率调度，随着资源和需求变化动态切换状态以保持功率平衡。FSM 读取负载需求 PL、可再生贡献 Ppv 和 Pw、电池荷电状态 SoC，以及 eng3_Pmax 等发动机容量边界，然后返回请求的发电机功率、电池放电或充电功率以及备用功率。十二个有限状态由需求、发电、容量和 SoC 上的逻辑转移条件选择。当 Ppv + Pw 覆盖 PL 时，EMS 用 RES 满足全部船舶需求，并在 SoC 低于 0.95 时给电池充电，或在 SoC 至少为 0.95 时把剩余可再生功率视为备用功率。当 Ppv + Pw 低于 PL 时，调度遵循优先级：RES 优先，SoC 合适时使用电池，LNG 先于柴油机，DG1/DG2 只作为最后优先级。低 SoC 分支加入明确充电裕量，包括 LNG 覆盖场景中的 Pgmax/5，以及后续柴油发电机场景中的 Pd1max/10。当 PL = 0 时，RES 产出根据 SoC 阈值送往电池充电或备用功率。过载完成状态是非法状态：若极端需求超过全部 RES 与热力资源，EMS 会激活全部热发电单元并用电池放电弥补缺口，该状态实践中不应发生。"""


@dataclass(frozen=True)
class PrE1Case:
    """One NL input used by PR-E1 real-run exploration."""

    case_key: str
    path: str
    case_id: str
    title: str
    nl: str
    nl_zh: str
    source_url: str
    source_note: str = "issue #14 / PR-D representative NL"
    source_path: str | None = None
    paper_path: str | None = None
    selection_rationale: str = ""
    variable_participation_note: str = ""


@dataclass(frozen=True)
class ConditionSpec:
    """One explicit PR-E1 config condition."""

    config_id: str
    label: str
    max_iterations: int = 5
    llm_max_retries: int = 2
    scenario_max_retries: int = 2
    model_review_mode: str = "blocking_major_only"
    repair_review_mode: str = "blocking_major_only"
    exploratory: bool = False
    changed_factors: tuple[str, ...] = field(default_factory=tuple)
    academic_question: str = ""
    recommendation_role: str = "baseline"


@dataclass(frozen=True)
class PrE1RunSummary:
    """Compact, secret-safe summary of one PR-E1 run."""

    case_key: str
    path: str
    case_id: str
    config_id: str
    condition_id: str | None
    run_id: str
    result_status: str
    record_status: str
    verdict: str | None
    verdict_reason: str | None
    verdict_source_stage_id: str | None
    main_result_eligible: bool
    oracle_weak: bool
    schema_valid: bool
    schema_error: str | None
    secret_redacted: bool
    redaction_report_count: int
    provider_mode: str | None
    provider_model_redacted: str | None
    real_llm_provider_api: bool | None
    provider_config_read: bool | None
    git_commit: str | None
    git_dirty: bool | None
    git_diff_hash: str | None
    prompt_snapshot_hash: str | None
    reproducibility_path: str
    clean_commit_bound: bool
    elapsed_seconds: float
    token_usage: dict[str, Any]
    stage_count: int
    executed_stage_ids: list[str]
    missing_required_stage_ids: list[str]
    llm_stage_ids: list[str]
    iteration_count: int
    repair_count: int
    accepted_repair_count: int
    scenario_history_count: int
    final_dsl_length: int
    final_dsl_hash: str | None
    run_record_path: str
    report_path: str
    summary_path: str
    final_dsl_path: str
    checks_path: str
    stdout_path: str
    stderr_path: str
    primary_failure_class: str
    fix_log_next_actions: list[str] = field(default_factory=list)
    iteration_exit_reasons: list[str] = field(default_factory=list)
    final_dsl_source: dict[str, object] = field(default_factory=dict)


REQUIRED_ENV_KEYS = ("LLM_ENDPOINT", "LLM_API_KEY", "LLM_MODEL")


def pr_e1_cases(case_set: str = "mandatory", case_keys: Sequence[str] | None = None) -> list[PrE1Case]:
    """Return PR-E1 case list.

    ``mandatory`` intentionally contains only the two representative cases that
    PR-D already used, so before/after and config comparisons are interpretable.
    The CLI keeps the ``case-set`` switch because PR-E1 may later add screened
    extension cases without changing the runner interface.
    """

    cases = [
        PrE1Case(
            case_key="path1_abs",
            path="path1",
            case_id="abs-fsm-brake-control",
            title="Path1 ABS three-state brake supervisor",
            nl=PATH1_ABS_NL,
            nl_zh=PATH1_ABS_NL_ZH,
            source_url="project_1_llm_state_machine_modeling/eval/data/sources/abs-fsm-brake-control/nl.md",
            source_note="PR-E2 aligned Path1 sample / sources STM extracted NL",
            source_path="project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control",
            paper_path="project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control/paper.pdf",
            selection_rationale="三态、guard、state action 均明确，适合检验 parse/semantic/design/sim 是否能走到后段。",
            variable_participation_note="`slp` 是 guard 变量；`k1/k2/n` 是状态动作输出，变量不是纯吉祥物。",
        ),
        PrE1Case(
            case_key="path1_elevator",
            path="path1",
            case_id="automatic-elevator-controller",
            title="Path1 automatic elevator controller",
            nl=PATH1_ELEVATOR_NL,
            nl_zh=PATH1_ELEVATOR_NL_ZH,
            source_url="project_1_llm_state_machine_modeling/eval/data/sources/automatic-elevator-controller/nl.md",
            source_note="PR-E2 aligned Path1 sample / sources STM extracted NL",
            source_path="project_1_llm_state_machine_modeling/sources/automatic-elevator-controller",
            paper_path="project_1_llm_state_machine_modeling/sources/automatic-elevator-controller/paper.pdf",
            selection_rationale="楼层态、运动态、请求事件、到位传感事件与 reset 都明确，适合检验事件建模和 forced fallback。",
            variable_participation_note="`PS*`/`S*`/`reset` 更适合按事件建模；`hbrg` 是输出动作，变量压力低于 Path2 EFSM。",
        ),
        PrE1Case(
            case_key="path1_cara",
            path="path1",
            case_id="cara-infusion-pump-formal-spec__01",
            title="Path1 CARA representative NL",
            nl=PATH1_CARA_NL,
            nl_zh=PATH1_CARA_NL_ZH,
            source_url="https://github.com/HansBug/research_ideas/issues/14#issuecomment-4598890685",
            source_path="project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec",
            paper_path="project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf",
            selection_rationale="issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。",
            variable_participation_note="变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。",
        ),
        PrE1Case(
            case_key="path2_lng_ems",
            path="path2",
            case_id="state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship",
            title="Path2 LNG-ship EMS representative NL",
            nl=PATH2_LNG_EMS_NL,
            nl_zh=PATH2_LNG_EMS_NL_ZH,
            source_url="https://github.com/HansBug/research_ideas/issues/14#issuecomment-4598890799",
            source_path="project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship",
            paper_path="project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/paper.pdf",
            selection_rationale="issue #14 / PR-D 代表性 Path2 EFSM，变量、guard、12 个状态和非法状态都明确。",
            variable_participation_note="`PL/Ppv/Pw/SoC/eng*_Pmax` 是环境输入/容量边界，适合暴露 SD-4 对外部输入变量的处理能力。",
        ),
    ]
    if case_set == "mandatory":
        selected = [case for case in cases if case.case_key in {"path1_cara", "path2_lng_ems"}]
    elif case_set in {"all", "e2-aligned", "mandatory+screening"}:
        selected = cases
    else:
        selected = []
    if case_keys:
        allowed = {case.case_key for case in cases}
        unknown = [key for key in case_keys if key not in allowed]
        if unknown:
            raise ValueError(f"unknown case key(s): {', '.join(unknown)}; allowed: {', '.join(sorted(allowed))}")
        selected = [case for case in selected if case.case_key in set(case_keys)]
    if selected:
        return selected
    allowed = ", ".join(["mandatory", "all", "e2-aligned", "mandatory+screening"])
    raise ValueError(f"unknown case-set {case_set!r}; allowed: {allowed}")


def condition_specs() -> dict[str, ConditionSpec]:
    """Return the PR-E1 condition matrix.

    Only ``default`` keeps ``condition_id=full_staged_v1``.  Budget/retry/review
    variants are explicit non-default conditions and must be interpreted as
    exploratory evidence even when they run against the real provider.
    """

    return {
        "default": ConditionSpec(
            config_id="default",
            label="Default full_staged_v1 budget",
            recommendation_role="recommended baseline candidate",
        ),
        "iter3": ConditionSpec(
            config_id="iter3",
            label="Low-budget max_iterations=3 exploration",
            max_iterations=3,
            exploratory=True,
            changed_factors=("max_iterations=3",),
            academic_question="PR-E1 explores whether a lower iteration budget is enough for representative real NL cases.",
            recommendation_role="lower-cost diagnostic",
        ),
        "iter8": ConditionSpec(
            config_id="iter8",
            label="Higher-budget max_iterations=8 exploration",
            max_iterations=8,
            exploratory=True,
            changed_factors=("max_iterations=8",),
            academic_question="PR-E1 explores whether a higher iteration budget materially improves representative real NL cases.",
            recommendation_role="enhanced-budget diagnostic",
        ),
        "iter10": ConditionSpec(
            config_id="iter10",
            label="High-budget max_iterations=10 diagnostic",
            max_iterations=10,
            exploratory=True,
            changed_factors=("max_iterations=10",),
            academic_question="PR-E1 diagnostic-only high budget for hard non-convergence cases.",
            recommendation_role="diagnostic-only",
        ),
        "scenario0": ConditionSpec(
            config_id="scenario0",
            label="No scenario retry diagnostic",
            scenario_max_retries=0,
            exploratory=True,
            changed_factors=("scenario_max_retries=0",),
            academic_question="PR-E1 explores whether scenario retry is necessary or merely cost overhead.",
            recommendation_role="diagnostic-only",
        ),
        "retry3": ConditionSpec(
            config_id="retry3",
            label="LLM retry=3 diagnostic",
            llm_max_retries=3,
            exploratory=True,
            changed_factors=("llm_max_retries=3",),
            academic_question="PR-E1 explores whether one extra LLM retry helps provider/schema instability.",
            recommendation_role="diagnostic-only",
        ),
    }


def parse_csv_selection(raw: str, *, allowed: Iterable[str], kind: str) -> list[str]:
    allowed_set = set(allowed)
    values = [item.strip() for item in raw.split(",") if item.strip()]
    unknown = [item for item in values if item not in allowed_set]
    if unknown:
        raise ValueError(f"unknown {kind}: {', '.join(unknown)}; allowed: {', '.join(sorted(allowed_set))}")
    return values


def make_pr_e1_config(spec: ConditionSpec, *, output_dir: str | Path, run_id: str) -> LoopConfig:
    """Build a LoopConfig for one PR-E1 run."""

    if not spec.exploratory:
        return LoopConfig(output_dir=str(output_dir), run_id=run_id)

    defaults = experiment_default_condition()
    budget_policy = dict(defaults.budget_policy)
    budget_policy.update(
        {
            "max_iterations": spec.max_iterations,
            "llm_max_retries": spec.llm_max_retries,
            "scenario_max_retries": spec.scenario_max_retries,
        }
    )
    llm_policy = dict(defaults.llm_policy)
    condition_id = f"pr_e1_{spec.config_id}_v1"
    changed = tuple(spec.changed_factors) or (
        f"max_iterations={spec.max_iterations}",
        f"llm_max_retries={spec.llm_max_retries}",
        f"scenario_max_retries={spec.scenario_max_retries}",
    )
    return LoopConfig(
        condition_id=condition_id,
        condition_family="pr_e1_real_run_exploration",
        base_condition_id="full_staged_v1",
        changed_factors=list(changed),
        policy_profile="pr_e1_exploratory",
        max_iterations=spec.max_iterations,
        llm_max_retries=spec.llm_max_retries,
        scenario_max_retries=spec.scenario_max_retries,
        budget_policy=budget_policy,
        llm_policy=llm_policy,
        academic_question=spec.academic_question,
        model_review_mode=spec.model_review_mode,
        delta_review_mode=spec.repair_review_mode,
        output_dir=str(output_dir),
        run_id=run_id,
    )


def build_run_id(case: PrE1Case, spec: ConditionSpec, *, run_tag: str | None = None) -> str:
    tag = run_tag or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"pr-e1-{case.case_key}-{spec.config_id}-{tag}-{uuid.uuid4().hex[:8]}"


def _run_command(args: Sequence[str]) -> str:
    try:
        return subprocess.check_output(list(args), cwd=REPO_ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def _status_path(line: str) -> str:
    value = line[3:] if len(line) > 3 else ""
    if " -> " in value:
        value = value.rsplit(" -> ", 1)[-1]
    return value.strip().strip('"')


def _is_under(path_text: str, root_text: str) -> bool:
    path_text = path_text.strip("/")
    root_text = root_text.strip("/")
    return path_text == root_text or path_text.startswith(root_text + "/")


def _git_dirty(*, exclude_paths: Sequence[str | Path] = ()) -> bool | None:
    try:
        status = _run_command(["git", "status", "--porcelain"])
    except Exception:
        return None
    excludes = [(_as_repo_relative(path) if isinstance(path, Path) else str(path)).strip("/") for path in exclude_paths]
    for line in status.splitlines():
        path_text = _status_path(line)
        if excludes and any(_is_under(path_text, root) for root in excludes):
            continue
        return True
    return False


def _hash_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _hash_text(text: str) -> str:
    return _hash_bytes(text.encode("utf-8"))


def _short_hash_text(text: str) -> str:
    return _hash_text(text)[:19]


def _git_diff_hash(*, exclude_paths: Sequence[str | Path] = ()) -> str | None:
    pathspec = ["."]
    for path in exclude_paths:
        rel = _as_repo_relative(path) if isinstance(path, Path) else str(path)
        pathspec.append(f":(exclude){rel.strip('/')}")
    try:
        diff = subprocess.check_output(["git", "diff", "--binary", "--", *pathspec], cwd=REPO_ROOT, stderr=subprocess.DEVNULL)
        staged = subprocess.check_output(["git", "diff", "--cached", "--binary", "--", *pathspec], cwd=REPO_ROOT, stderr=subprocess.DEVNULL)
    except Exception:
        return None
    return _hash_bytes(diff + b"\n--cached--\n" + staged)


def _file_hash(path: Path) -> str | None:
    try:
        return _hash_bytes(path.read_bytes())
    except Exception:
        return None


def _prompt_snapshot() -> dict[str, object]:
    paths = [
        PROJECT_ROOT / "method" / "prompts" / "_pyfcstm_grammar.md",
        PROJECT_ROOT / "method" / "prompts" / "modeler.txt",
        PROJECT_ROOT / "method" / "stages" / "sl_initial_modeling_prompt.py",
        PROJECT_ROOT / "method" / "stages" / "sl_repair_prompt.py",
        PROJECT_ROOT / "method" / "stages" / "sl_scenario_generation_prompt.py",
        PROJECT_ROOT / "method" / "stages" / "sl_model_review_prompt.py",
        PROJECT_ROOT / "method" / "stages" / "sl10_repair_review_prompt.py",
        PROJECT_ROOT / "method" / "stages" / "sl_delta_review_prompt.py",
    ]
    files = []
    for path in paths:
        files.append({"path": _as_repo_relative(path), "sha256": _file_hash(path)})
    digest = _hash_text(json.dumps(files, ensure_ascii=False, sort_keys=True))
    return {"digest": digest, "files": files}


def _as_repo_relative(path: str | Path) -> str:
    p = Path(path)
    try:
        return p.resolve().relative_to(REPO_ROOT).as_posix()
    except Exception:
        return p.as_posix()


def _hash_env_value(value: str | None, *, prefix: int = 16) -> str | None:
    if value is None:
        return None
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:prefix]


def _redacted_endpoint_snapshot(endpoint: str | None) -> dict[str, object]:
    if not endpoint:
        return {"present": False}
    parsed = urlparse(endpoint)
    return {
        "present": True,
        "scheme": parsed.scheme or "<unknown>",
        "host": parsed.hostname or "<unknown>",
        "port": parsed.port,
        "path_hash": _hash_env_value(parsed.path or "/"),
        "endpoint_sha256_prefix": _hash_env_value(endpoint),
    }


def _provider_runtime_snapshot() -> dict[str, object]:
    timeout = get_request_timeout_seconds()
    endpoint = os.environ.get("LLM_ENDPOINT")
    api_key = os.environ.get("LLM_API_KEY")
    return {
        "required_env_present": {key: bool(os.environ.get(key)) for key in REQUIRED_ENV_KEYS},
        "model_redacted": os.environ.get("LLM_MODEL") or "<env:LLM_MODEL>",
        "endpoint": _redacted_endpoint_snapshot(endpoint),
        "api_key_sha256_prefix": _hash_env_value(api_key),
        "llm_stream": get_stream_enabled(),
        "llm_stream_include_usage": get_stream_include_usage_enabled(),
        "llm_request_timeout_seconds": timeout if timeout is not None else "none",
        "sdk_max_retries": DEFAULT_SDK_MAX_RETRIES,
        "progress_log_enabled": get_progress_log_enabled(),
        "snapshot_note": "Secret-safe provider/runtime snapshot for distinguishing OpenAI-compatible endpoints and stream policy; raw endpoint path/API key are never stored.",
    }


def build_reproducibility_payload(
    *,
    case: PrE1Case,
    spec: ConditionSpec,
    cfg: LoopConfig,
    run_id: str,
    output_root: Path,
    started_at: str,
) -> dict[str, object]:
    prompt_snapshot = _prompt_snapshot()
    output_rel = _as_repo_relative(output_root)
    return {
        "schema_version": "pr-e1-reproducibility.v1",
        "started_at": started_at,
        "run_id": run_id,
        "case": {
            "case_key": case.case_key,
            "path": case.path,
            "case_id": case.case_id,
            "title": case.title,
            "source_url": case.source_url,
            "source_note": case.source_note,
            "source_path": case.source_path,
            "paper_path": case.paper_path,
            "selection_rationale": case.selection_rationale,
            "variable_participation_note": case.variable_participation_note,
            "nl_hash": _hash_text(case.nl),
            "nl_zh_hash": _hash_text(case.nl_zh),
        },
        "condition": asdict(spec),
        "command": {
            "module": "method.pr_e1_real_runs",
            "canonical_example": (
                "PYTHONPATH=project_1_llm_state_machine_modeling "
                f"python -m method.pr_e1_real_runs --case-set e2-aligned "
                f"--case-keys {case.case_key} --condition-set {spec.config_id} "
                f"--output-dir {_as_repo_relative(output_root)} --run-tag <same-tag>"
            ),
        },
        "resolved_loop_config": cfg.resolved_config(),
        "git": {
            "commit": _run_command(["git", "rev-parse", "HEAD"]) or None,
            "branch": _run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"]) or None,
            "dirty": _git_dirty(exclude_paths=[output_rel]),
            "dirty_scope": f"outside_output_dir:{output_rel}",
            "diff_hash": _git_diff_hash(exclude_paths=[output_rel]),
        },
        "prompt_snapshot": prompt_snapshot,
        "provider": {
            **_provider_runtime_snapshot(),
            "model_redacted": os.environ.get("LLM_MODEL") or cfg.llm_model or "<env:LLM_MODEL>",
        },
    }


def write_reproducibility_payload(run_dir: Path, payload: dict[str, object]) -> Path:
    path = run_dir / "reproducibility.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _repro_digest(payload: dict[str, object]) -> tuple[bool | None, str | None, str | None]:
    git_info = payload.get("git") if isinstance(payload.get("git"), dict) else {}
    prompt = payload.get("prompt_snapshot") if isinstance(payload.get("prompt_snapshot"), dict) else {}
    dirty = git_info.get("dirty") if isinstance(git_info, dict) else None
    diff_hash = git_info.get("diff_hash") if isinstance(git_info, dict) else None
    prompt_hash = prompt.get("digest") if isinstance(prompt, dict) else None
    return (
        bool(dirty) if dirty is not None else None,
        str(diff_hash) if diff_hash is not None else None,
        str(prompt_hash) if prompt_hash is not None else None,
    )


def run_pr_e1_matrix(
    *,
    output_dir: str | Path = "runs/pr_e1_real_agent_loop",
    case_set: str = "mandatory",
    case_keys: Sequence[str] | None = None,
    condition_set: Sequence[str] = ("default", "iter3", "iter8"),
    run_agent_loop_fn: RunAgentLoopFn = run_agent_loop,
    require_provider_env: bool = True,
    run_tag: str | None = None,
    workers: int = 1,
) -> list[PrE1RunSummary]:
    """Run the selected PR-E1 matrix and write derived reports.

    ``workers`` defaults to 1 to avoid provider rate-limit surprises.  Values
    above 1 are allowed because each case/config pair gets an independent
    ``run_id`` and output directory.
    """

    if require_provider_env:
        assert_pr_d_provider_env()
    if workers < 1:
        raise ValueError("workers must be >= 1")
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    specs = condition_specs()
    selected_specs = [specs[key] for key in condition_set]
    jobs = [(case, spec) for case in pr_e1_cases(case_set, case_keys=case_keys) for spec in selected_specs]
    summaries: list[PrE1RunSummary] = []
    if workers == 1:
        for case, spec in jobs:
            summaries.append(
                run_one_pr_e1_case(
                    case,
                    spec,
                    output_root=out,
                    run_agent_loop_fn=run_agent_loop_fn,
                    run_tag=run_tag,
                )
            )
            write_matrix_summary(summaries, out)
    else:
        if run_agent_loop_fn is not run_agent_loop:
            raise ValueError("workers>1 only supports the default run_agent_loop_fn because fake test callables are not process-safe")
        with ProcessPoolExecutor(max_workers=workers) as executor:
            future_to_job = {
                executor.submit(_run_one_pr_e1_case_process, case, spec, out, run_tag): (case, spec)
                for case, spec in jobs
            }
            for future in as_completed(future_to_job):
                summaries.append(future.result())
                summaries.sort(key=lambda item: (item.case_key, item.config_id, item.run_id))
                write_matrix_summary(summaries, out)
    write_matrix_summary(summaries, out)
    return summaries


def _run_one_pr_e1_case_process(
    case: PrE1Case,
    spec: ConditionSpec,
    output_root: str | Path,
    run_tag: str | None,
) -> PrE1RunSummary:
    """Process-pool worker for real PR-E1 runs.

    A process pool is intentionally used instead of threads because
    ``run_one_pr_e1_case`` captures stdout/stderr via process-global streams.
    In separate processes each run keeps independent logs without cross-talk.
    """

    return run_one_pr_e1_case(case, spec, output_root=output_root, run_tag=run_tag)


def run_one_pr_e1_case(
    case: PrE1Case,
    spec: ConditionSpec,
    *,
    output_root: str | Path,
    run_agent_loop_fn: RunAgentLoopFn = run_agent_loop,
    run_tag: str | None = None,
) -> PrE1RunSummary:
    """Run one case/config pair and render all per-run artifacts."""

    output_root = Path(output_root)
    run_id = build_run_id(case, spec, run_tag=run_tag)
    run_dir = output_root / run_id
    logs_dir = run_dir / "run_logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = logs_dir / "stdout.txt"
    stderr_path = logs_dir / "stderr.txt"
    cfg = make_pr_e1_config(spec, output_dir=run_dir, run_id=run_id)
    repro_payload = build_reproducibility_payload(
        case=case,
        spec=spec,
        cfg=cfg,
        run_id=run_id,
        output_root=output_root,
        started_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    )
    repro_path = write_reproducibility_payload(run_dir, repro_payload)
    started = time.monotonic()
    result: AgentLoopResult | None = None
    raised: Exception | None = None
    with stdout_path.open("w", encoding="utf-8") as stdout_f, stderr_path.open("w", encoding="utf-8") as stderr_f:
        with contextlib.redirect_stdout(stdout_f), contextlib.redirect_stderr(stderr_f):
            try:
                result = run_agent_loop_fn(case.nl, cfg)
            except Exception as exc:  # pragma: no cover - exercised only by real-provider failure modes
                raised = exc
                print(f"PR-E1 run raised {type(exc).__name__}: {exc}", file=stderr_f)
    elapsed = time.monotonic() - started
    if raised is not None:
        return _write_exception_artifacts(case, spec, cfg, run_id, run_dir, stdout_path, stderr_path, repro_payload, repro_path, elapsed, raised)
    assert result is not None
    if not result.run_record_path:
        return _write_missing_record_artifacts(case, spec, cfg, result, run_id, run_dir, stdout_path, stderr_path, repro_payload, repro_path, elapsed)

    record = read_agent_loop_run_record(result.run_record_path)
    summary = summarize_pr_e1_run(
        case=case,
        spec=spec,
        result=result,
        record=record,
        elapsed_seconds=elapsed,
        run_dir=run_dir,
        stdout_path=stdout_path,
        stderr_path=stderr_path,
        reproducibility_payload=repro_payload,
        reproducibility_path=repro_path,
    )
    _write_per_run_artifacts(case, spec, result, record, summary, run_dir)
    return summary


def summarize_pr_e1_run(
    *,
    case: PrE1Case,
    spec: ConditionSpec,
    result: AgentLoopResult,
    record: AgentLoopRunRecord,
    elapsed_seconds: float,
    run_dir: Path,
    stdout_path: Path,
    stderr_path: Path,
    reproducibility_payload: dict[str, object] | None = None,
    reproducibility_path: Path | None = None,
) -> PrE1RunSummary:
    final = record.final_artifacts
    environment = record.environment
    resolved = environment.get("resolved_config") if isinstance(environment.get("resolved_config"), dict) else {}
    executed_stage_ids = _executed_stage_ids(record)
    required_stage_ids = _required_stage_ids_for_record(record)
    missing_required = [stage_id for stage_id in required_stage_ids if stage_id not in set(executed_stage_ids)]
    final_dsl = str(final.get("final_dsl") or result.final_dsl or "")
    public_payload = _record_public_text(record)
    checks = run_record_checks(record, public_payload)
    repro_dirty, repro_diff_hash, prompt_hash = _repro_digest(reproducibility_payload or {})
    repro_path = reproducibility_path or (run_dir / "reproducibility.json")
    final_dsl_hash = _optional_str(final.get("final_dsl_hash"))
    return PrE1RunSummary(
        case_key=case.case_key,
        path=case.path,
        case_id=case.case_id,
        config_id=spec.config_id,
        condition_id=_optional_str(resolved.get("condition_id") or record.run_config.get("condition_id")),
        run_id=record.run_id,
        result_status=result.status,
        record_status=record.status,
        verdict=_optional_str(final.get("verdict")),
        verdict_reason=_optional_str(final.get("verdict_reason")),
        verdict_source_stage_id=_optional_str(final.get("verdict_source_stage_id")),
        main_result_eligible=bool(final.get("main_result_eligible")) and is_path_result_eligible(record),
        oracle_weak=bool(final.get("oracle_weak")),
        schema_valid=checks["schema_valid"],
        schema_error=checks["schema_error"],
        secret_redacted=checks["secret_redacted"],
        redaction_report_count=len(record.redaction_report),
        provider_mode=_optional_str(environment.get("provider_mode")),
        provider_model_redacted=_optional_str(environment.get("provider_model_redacted")),
        real_llm_provider_api=_optional_bool(environment.get("real_llm_provider_api")),
        provider_config_read=_optional_bool(environment.get("provider_config_read")),
        git_commit=_optional_str(environment.get("git_commit")),
        git_dirty=repro_dirty,
        git_diff_hash=repro_diff_hash,
        prompt_snapshot_hash=prompt_hash,
        reproducibility_path=_as_posix(repro_path),
        clean_commit_bound=(repro_dirty is False),
        elapsed_seconds=round(elapsed_seconds, 3),
        token_usage=_token_usage(record),
        stage_count=len(record.stage_records),
        executed_stage_ids=executed_stage_ids,
        missing_required_stage_ids=missing_required,
        llm_stage_ids=_llm_stage_ids(record),
        iteration_count=len(record.iteration_records),
        repair_count=len(record.repair_history),
        accepted_repair_count=sum(1 for item in record.repair_history if isinstance(item, dict) and item.get("accepted") is True),
        scenario_history_count=len(record.scenario_history),
        final_dsl_length=len(final_dsl),
        final_dsl_hash=final_dsl_hash,
        run_record_path=_as_posix(result.run_record_path),
        report_path=_as_posix(run_dir / "report.md"),
        summary_path=_as_posix(run_dir / "summary.json"),
        final_dsl_path=_as_posix(run_dir / "final.fcstm"),
        checks_path=_as_posix(run_dir / "checks.json"),
        stdout_path=_as_posix(stdout_path),
        stderr_path=_as_posix(stderr_path),
        primary_failure_class=classify_primary_failure(record),
        fix_log_next_actions=_fix_log_next_actions(record),
        iteration_exit_reasons=_iteration_exit_reasons(record),
        final_dsl_source=_final_dsl_source(record, final_dsl_hash),
    )


def run_record_checks(record: AgentLoopRunRecord, public_payload: str | None = None) -> dict[str, object]:
    schema_error: str | None = None
    try:
        AgentLoopRunRecord(**asdict(record))
    except (TypeError, ValueError) as exc:
        schema_error = str(exc)
    payload = public_payload if public_payload is not None else _record_public_text(record)
    return {
        "schema_valid": schema_error is None,
        "schema_error": schema_error,
        "secret_redacted": not _contains_obvious_secret(payload),
        "redaction_report_count": len(record.redaction_report),
        "main_result_eligible_by_helper": is_path_result_eligible(record),
    }


def _required_stage_ids_for_record(record: AgentLoopRunRecord) -> list[str]:
    """Return PR-E1 required stages without treating legacy stages as missing.

    PR-D's helper still counted legacy ``SD-10`` / ``SL-10B`` as required.  In
    PR-E1 the default repair path is ``SL-10`` with local checks as evidence,
    while ``SD-8/SL-9/SC-11`` are required only when a repair block actually
    occurs.  Reporting legacy stages as "missing" on a success run confuses
    reviewers and can falsely imply incomplete execution.
    """

    stage_ids = {str(item.get("stage_id")) for item in record.stage_records if isinstance(item, dict)}
    required = list(PR_E1_FULL_STAGED_REQUIRED_STAGE_IDS)
    if any(stage_id in stage_ids for stage_id in PR_E1_REPAIR_STAGE_IDS):
        for stage_id in PR_E1_REPAIR_STAGE_IDS:
            if stage_id not in required:
                required.append(stage_id)
    return required


def _required_stage_ids_for_summary(summary: PrE1RunSummary) -> list[str]:
    required = list(PR_E1_FULL_STAGED_REQUIRED_STAGE_IDS)
    if any(stage_id in set(summary.executed_stage_ids) for stage_id in PR_E1_REPAIR_STAGE_IDS):
        for stage_id in PR_E1_REPAIR_STAGE_IDS:
            if stage_id not in required:
                required.append(stage_id)
    return required


def _fix_log_next_actions(record: AgentLoopRunRecord) -> list[str]:
    actions: list[str] = []
    for entry in record.fix_log if isinstance(record.fix_log, list) else []:
        if isinstance(entry, dict) and entry.get("next_action") is not None:
            actions.append(str(entry["next_action"]))
    return actions


def _iteration_exit_reasons(record: AgentLoopRunRecord) -> list[str]:
    reasons: list[str] = []
    for entry in record.iteration_records if isinstance(record.iteration_records, list) else []:
        if isinstance(entry, dict) and entry.get("exit_reason") is not None:
            reasons.append(str(entry["exit_reason"]))
    return reasons


def _final_dsl_source(record: AgentLoopRunRecord, final_dsl_hash: str | None = None) -> dict[str, object]:
    """Locate which accepted repair, if any, produced ``final.fcstm``."""

    wanted = final_dsl_hash or _optional_str(record.final_artifacts.get("final_dsl_hash"))
    source: dict[str, object] = {
        "final_dsl_hash": wanted,
        "source_kind": "initial_or_unrepaired",
    }
    if not wanted:
        return source
    for index, item in enumerate(record.repair_history if isinstance(record.repair_history, list) else []):
        if not isinstance(item, dict):
            continue
        if item.get("candidate_dsl_hash") == wanted:
            source.update(
                {
                    "source_kind": "repair_candidate",
                    "repair_history_index": index,
                    "iteration": item.get("iteration"),
                    "accepted": item.get("accepted"),
                    "sl10_decision": (item.get("sl10_repair_review") or {}).get("decision") if isinstance(item.get("sl10_repair_review"), dict) else None,
                    "selected_source_stage": (item.get("selected_feedback") or {}).get("source_stage") if isinstance(item.get("selected_feedback"), dict) else None,
                }
            )
            break
    rejected: list[dict[str, object]] = []
    for index, item in enumerate(record.repair_history if isinstance(record.repair_history, list) else []):
        if not isinstance(item, dict) or item.get("accepted") is True:
            continue
        sl10 = item.get("sl10_repair_review") if isinstance(item.get("sl10_repair_review"), dict) else {}
        rejected.append(
            {
                "repair_history_index": index,
                "iteration": item.get("iteration"),
                "candidate_dsl_hash": item.get("candidate_dsl_hash"),
                "sl10_decision": sl10.get("decision") if isinstance(sl10, dict) else None,
                "rework_instructions": sl10.get("rework_instructions") if isinstance(sl10, dict) else None,
            }
        )
    if rejected:
        source["last_rejected_candidate"] = rejected[-1]
    return source


def _last_repair(record: AgentLoopRunRecord) -> dict[str, Any]:
    for item in reversed(record.repair_history if isinstance(record.repair_history, list) else []):
        if isinstance(item, dict):
            return item
    return {}


def _last_selected_feedback(record: AgentLoopRunRecord) -> dict[str, Any]:
    for item in reversed(record.iteration_records if isinstance(record.iteration_records, list) else []):
        if isinstance(item, dict) and isinstance(item.get("selected_feedback"), dict):
            return item["selected_feedback"]
    repair = _last_repair(record)
    selected = repair.get("selected_feedback")
    return selected if isinstance(selected, dict) else {}


def classify_primary_failure(record: AgentLoopRunRecord) -> str:
    """Classify the main stop reason for PR-E1 reviewer triage."""

    final = record.final_artifacts
    verdict = str(final.get("verdict") or "")
    reason = str(final.get("verdict_reason") or final.get("error_message") or "").lower()
    if verdict == "success":
        if final.get("main_result_eligible") is not True:
            if final.get("oracle_weak") is True or "oracle" in str(final.get("exclusion_reason") or "").lower():
                return "success_but_weak_oracle_ineligible"
            return "success_but_main_ineligible"
        return "success"
    if verdict == "provider_error" or "provider" in reason or "retry exhausted" in reason:
        return "provider_or_retry"
    selected = _last_selected_feedback(record)
    selected_stage = str(selected.get("source_stage") or "")
    selected_source = str(selected.get("source") or "")
    last_repair = _last_repair(record)
    sl10 = last_repair.get("sl10_repair_review") if isinstance(last_repair.get("sl10_repair_review"), dict) else {}
    if selected_stage == "SD-6" or selected_source == "sim":
        if isinstance(sl10, dict) and sl10.get("decision") == "rework":
            return "repair_review_rework_budget"
        return "scenario_or_sim_oracle"
    if selected_stage == "SL-7" or selected_source == "model_review":
        return "model_review_or_quality"
    if isinstance(sl10, dict) and sl10.get("decision") == "rework":
        return "repair_review_rework_budget"
    if "parse" in reason or "syntax" in reason:
        return "dsl_parse_or_grammar"
    if "semantic" in reason or "dangling" in reason or "forced_transition" in reason:
        return "semantic_or_topology"
    if "design" in reason or "unwritten" in reason or "guard" in reason:
        return "design_or_variable_dynamics"
    if "grounding" in reason:
        return "grounding_or_required_element_loss"
    if "scenario" in reason or "oracle" in reason or "sim" in reason:
        return "scenario_or_sim_oracle"
    if record.status == "budget_exhausted":
        return "budget"
    if record.status in {"invalid", "error"}:
        return "record_or_schema"
    return "model_quality_or_unclassified"


def _write_per_run_artifacts(
    case: PrE1Case,
    spec: ConditionSpec,
    result: AgentLoopResult,
    record: AgentLoopRunRecord,
    summary: PrE1RunSummary,
    run_dir: Path,
) -> None:
    final_dsl = str(record.final_artifacts.get("final_dsl") or result.final_dsl or "")
    (run_dir / "final.fcstm").write_text(final_dsl, encoding="utf-8")
    (run_dir / "summary.json").write_text(json.dumps(asdict(summary), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (run_dir / "checks.json").write_text(
        json.dumps(run_record_checks(record), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (run_dir / "flow_log.json").write_text(json.dumps(record.logs, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (run_dir / "fix_log.json").write_text(json.dumps(record.fix_log, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (run_dir / "report.md").write_text(render_run_report(case, spec, record, summary), encoding="utf-8")


def _write_exception_artifacts(
    case: PrE1Case,
    spec: ConditionSpec,
    cfg: LoopConfig,
    run_id: str,
    run_dir: Path,
    stdout_path: Path,
    stderr_path: Path,
    reproducibility_payload: dict[str, object],
    reproducibility_path: Path,
    elapsed: float,
    exc: Exception,
) -> PrE1RunSummary:
    repro_dirty, repro_diff_hash, prompt_hash = _repro_digest(reproducibility_payload)
    summary = PrE1RunSummary(
        case_key=case.case_key,
        path=case.path,
        case_id=case.case_id,
        config_id=spec.config_id,
        condition_id=cfg.condition_id,
        run_id=run_id,
        result_status="api_failed" if missing_provider_env() else "spec_failed",
        record_status="error",
        verdict="provider_error" if missing_provider_env() else "invalid",
        verdict_reason=f"runner_exception: {type(exc).__name__}: {str(exc)[:300]}",
        verdict_source_stage_id=None,
        main_result_eligible=False,
        oracle_weak=False,
        schema_valid=False,
        schema_error="no run record produced",
        secret_redacted=True,
        redaction_report_count=0,
        provider_mode=cfg.llm_provider_mode,
        provider_model_redacted=cfg.llm_model,
        real_llm_provider_api=cfg.llm_provider_mode == "real_env",
        provider_config_read=not missing_provider_env(),
        git_commit=_optional_str((reproducibility_payload.get("git") or {}).get("commit") if isinstance(reproducibility_payload.get("git"), dict) else None),
        git_dirty=repro_dirty,
        git_diff_hash=repro_diff_hash,
        prompt_snapshot_hash=prompt_hash,
        reproducibility_path=_as_posix(reproducibility_path),
        clean_commit_bound=(repro_dirty is False),
        elapsed_seconds=round(elapsed, 3),
        token_usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "n_calls": 0},
        stage_count=0,
        executed_stage_ids=[],
        missing_required_stage_ids=list(PR_E1_FULL_STAGED_REQUIRED_STAGE_IDS),
        llm_stage_ids=[],
        iteration_count=0,
        repair_count=0,
        accepted_repair_count=0,
        scenario_history_count=0,
        final_dsl_length=0,
        final_dsl_hash=None,
        run_record_path="",
        report_path=_as_posix(run_dir / "report.md"),
        summary_path=_as_posix(run_dir / "summary.json"),
        final_dsl_path=_as_posix(run_dir / "final.fcstm"),
        checks_path=_as_posix(run_dir / "checks.json"),
        stdout_path=_as_posix(stdout_path),
        stderr_path=_as_posix(stderr_path),
        primary_failure_class="provider_or_retry" if missing_provider_env() else "record_or_schema",
        fix_log_next_actions=[],
        iteration_exit_reasons=[],
        final_dsl_source={},
    )
    (run_dir / "final.fcstm").write_text("", encoding="utf-8")
    (run_dir / "summary.json").write_text(json.dumps(asdict(summary), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (run_dir / "checks.json").write_text(json.dumps({"schema_valid": False, "schema_error": "no run record produced", "secret_redacted": True}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (run_dir / "flow_log.json").write_text("[]\n", encoding="utf-8")
    (run_dir / "fix_log.json").write_text("[]\n", encoding="utf-8")
    (run_dir / "report.md").write_text(render_exception_report(case, spec, summary), encoding="utf-8")
    return summary


def _write_missing_record_artifacts(
    case: PrE1Case,
    spec: ConditionSpec,
    cfg: LoopConfig,
    result: AgentLoopResult,
    run_id: str,
    run_dir: Path,
    stdout_path: Path,
    stderr_path: Path,
    reproducibility_payload: dict[str, object],
    reproducibility_path: Path,
    elapsed: float,
) -> PrE1RunSummary:
    exc = RuntimeError(f"run_agent_loop returned no run_record_path: {result.error_message}")
    return _write_exception_artifacts(case, spec, cfg, run_id, run_dir, stdout_path, stderr_path, reproducibility_payload, reproducibility_path, elapsed, exc)


def render_run_report(case: PrE1Case, spec: ConditionSpec, record: AgentLoopRunRecord, summary: PrE1RunSummary) -> str:
    final_dsl = str(record.final_artifacts.get("final_dsl") or "")
    boundary = "否；本次使用真实默认入口/显式 PR-E1 探索条件，没有 fake、fixture、hot-start 或 replay。"
    if spec.exploratory:
        boundary = "否；本次使用真实 provider，但配置是显式 non-default PR-E1 探索条件，不可计入主结果。"
    lines = [
        f"## {case.path} / {case.case_id} / {spec.config_id} 真实运行结果：{case.title}",
        "",
        "### 0. 准确边界与结论",
        "",
        f"- 运行入口：`method.loop.run_agent_loop(nl, LoopConfig(...))`。",
        f"- 是否使用 fake / fixture / hot-start / replay：{boundary}",
        f"- final verdict：`{summary.verdict}`；record_status：`{summary.record_status}`；result_status：`{summary.result_status}`。",
        f"- main_result_eligible：`{str(summary.main_result_eligible).lower()}`。",
        f"- 一句话结论：`{summary.primary_failure_class}`；停止原因：{summary.verdict_reason or '<none>'}。",
        "",
        "### 1. 基本信息",
        "",
        "| 字段 | 值 |",
        "|---|---|",
        f"| Path | `{case.path}` |",
        f"| case_id | `{case.case_id}` |",
        f"| config_id | `{spec.config_id}` |",
        "| 运行入口 | `method.loop.run_agent_loop(nl, LoopConfig(...))` |",
        f"| LoopConfig 摘要 | `condition_id={summary.condition_id}`, `max_iterations={spec.max_iterations}`, `llm_max_retries={spec.llm_max_retries}`, `scenario_max_retries={spec.scenario_max_retries}`, `model_review_mode={spec.model_review_mode}`, `repair_review_mode={spec.repair_review_mode}` |",
        f"| Git commit | `{summary.git_commit}` |",
        f"| clean / diff / prompt snapshot | clean=`{summary.clean_commit_bound}`, dirty=`{summary.git_dirty}`, diff_hash=`{summary.git_diff_hash}`, prompt_hash=`{summary.prompt_snapshot_hash}` |",
        f"| provider/model 脱敏标识 | mode=`{summary.provider_mode}`, model=`{summary.provider_model_redacted}`, real_api=`{summary.real_llm_provider_api}` |",
        f"| source / paper | source=`{case.source_path or case.source_url}`, paper=`{case.paper_path or '<none>'}` |",
        f"| 样本筛选理由 | {case.selection_rationale or '<none>'} |",
        f"| 变量参与说明 | {case.variable_participation_note or '<none>'} |",
        f"| run_id | `{summary.run_id}` |",
        f"| final verdict/status | verdict=`{summary.verdict}`, record=`{summary.record_status}`, result=`{summary.result_status}` |",
        f"| main_result_eligible | `{str(summary.main_result_eligible).lower()}` |",
        f"| final.fcstm 来源 | `{_escape_md(json.dumps(summary.final_dsl_source, ensure_ascii=False, sort_keys=True))}` |",
        f"| FixLog next_action 序列 | `{_escape_md(_join_limited(summary.fix_log_next_actions, limit=12))}` |",
        f"| iteration exit_reason 序列 | `{_escape_md(_join_limited(summary.iteration_exit_reasons, limit=8))}` |",
        f"| token/cost/time | tokens=`{summary.token_usage}`, elapsed=`{summary.elapsed_seconds}s` |",
        f"| run record | [`{Path(summary.run_record_path).name}`](./{Path(summary.run_record_path).name}) |",
        "| summary/log/final DSL | [`summary.json`](./summary.json), [`checks.json`](./checks.json), [`reproducibility.json`](./reproducibility.json), [`flow_log.json`](./flow_log.json), [`fix_log.json`](./fix_log.json), [`final.fcstm`](./final.fcstm), [`stdout.txt`](./run_logs/stdout.txt), [`stderr.txt`](./run_logs/stderr.txt) |",
        "",
        "### 2. 输入 NL（多行原文）",
        "",
        "```text",
        case.nl,
        "```",
        "",
        "### 2.1 输入 NL 中文翻译",
        "",
        "```text",
        case.nl_zh,
        "```",
        "",
        "### 3. 最终产出的 FCSTM DSL",
        "",
        "```pyfcstm",
        final_dsl,
        "```",
        "",
        "### 4. 全流程真实摘要表",
        "",
        "| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |",
        "|---|---:|---:|---:|---|---|---|---|",
    ]
    for row in _stage_table_rows(record, summary):
        lines.append("| " + " | ".join(row) + " |")
    lines.extend(
        [
            "",
            "### 4.1 完整流程日志（stage/control-flow replay ledger）",
            "",
            "口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。",
            "",
            *_flow_log_lines(record),
            "",
            "### 5. Iteration / repair / review 摘要",
            "",
            "| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |",
            "|---:|---|---|---|---|---|---|---|---|",
        ]
    )
    for row in _iteration_table_rows(record):
        lines.append("| " + " | ".join(row) + " |")
    lines.extend(
        [
            "",
            "### 6. Scenario 明细与逐轮通过情况",
            "",
            *_scenario_report_lines(record),
            "",
            "### 7. Repair / blocking feedback 明细",
            "",
            *_repair_report_lines(record),
            "",
            "### 8. 尝试记录与成本",
            "",
            *_attempt_lines(record),
            "",
            "### 9. 最终停止状态与后续含义",
            "",
            f"- 停止状态：verdict=`{summary.verdict}`，record_status=`{summary.record_status}`。",
            f"- 主要原因分类：`{summary.primary_failure_class}`。",
            f"- required stages executed：`{len(summary.executed_stage_ids)}/{len(_required_stage_ids_for_summary(summary))}`，missing=`{', '.join(summary.missing_required_stage_ids) or '<none>'}`。",
            f"- repairs：`{summary.accepted_repair_count}/{summary.repair_count}` accepted；scenario_history=`{summary.scenario_history_count}`。",
            f"- 配置含义：`{spec.recommendation_role}`；{'该结果只作 exploratory/config evidence，不进入主结果。' if spec.exploratory else '该结果可用于评估默认入口本身。'}",
            "- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def render_exception_report(case: PrE1Case, spec: ConditionSpec, summary: PrE1RunSummary) -> str:
    return f"""## {case.path} / {case.case_id} / {spec.config_id} 真实运行异常

### 0. 准确边界与结论

- 本次调用 `method.loop.run_agent_loop` 未能写出 `AgentLoopRunRecord`。
- verdict：`{summary.verdict}`。
- reason：{summary.verdict_reason}
- stdout：[`stdout.txt`](./run_logs/stdout.txt)
- stderr：[`stderr.txt`](./run_logs/stderr.txt)
- reproducibility：[`reproducibility.json`](./reproducibility.json)
- clean / diff / prompt snapshot：clean=`{summary.clean_commit_bound}`, dirty=`{summary.git_dirty}`, diff_hash=`{summary.git_diff_hash}`, prompt_hash=`{summary.prompt_snapshot_hash}`

### 2. 输入 NL（多行原文）

```text
{case.nl}
```

### 2.1 输入 NL 中文翻译

```text
{case.nl_zh}
```
"""


def write_matrix_summary(summaries: Sequence[PrE1RunSummary], output_dir: str | Path) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    payload = [asdict(item) for item in summaries]
    (out / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "SUMMARY.md").write_text(render_matrix_summary(summaries), encoding="utf-8")
    (out / "pr_comment.md").write_text(render_pr_comment(summaries, output_dir=out), encoding="utf-8")


def render_matrix_summary(summaries: Sequence[PrE1RunSummary]) -> str:
    lines = [
        "# PR-E1 real agent-loop exploration summary",
        "",
        "本文件由 `python -m method.pr_e1_real_runs` 生成，用于汇总 PR-E1 真实运行证据。非 default 条件均为显式 exploratory condition，不应直接计入 Path1/Path2 主结果。",
        "",
        "## 0. 可复现性边界",
        "",
        *_reproducibility_observation_lines(summaries),
        "",
        "## 1. 运行矩阵总览",
        "",
        "| Path | case | config | verdict | record | clean | eligible | failure class | iter | repairs | scenarios | tokens | elapsed | report |",
        "|---|---|---|---|---|---:|---:|---|---:|---:|---:|---:|---:|---|",
    ]
    for s in summaries:
        lines.append(
            "| {path} | `{case}` | `{config}` | `{verdict}` | `{record}` | {clean} | {eligible} | `{failure}` | {iters} | {repairs} | {scenarios} | {tokens} | {elapsed:.1f}s | [{run_id}](./{run_id}/report.md) |".format(
                path=s.path,
                case=s.case_key,
                config=s.config_id,
                verdict=s.verdict,
                record=s.record_status,
                clean="✅" if s.clean_commit_bound else "❌",
                eligible="✅" if s.main_result_eligible else "❌",
                failure=s.primary_failure_class,
                iters=s.iteration_count,
                repairs=s.repair_count,
                scenarios=s.scenario_history_count,
                tokens=_escape_md(_token_display(s.token_usage)),
                elapsed=s.elapsed_seconds,
                run_id=s.run_id,
            )
        )
    lines.extend([
        "",
        "## 2. 初步配置结论",
        "",
        *_configuration_observation_lines(summaries),
        "",
        "## 3. 主要失败模式",
        "",
        *_failure_observation_lines(summaries),
        "",
        "## 4. Path1/Path2 样本筛选建议",
        "",
        *_sample_observation_lines(summaries),
        "",
        "| 维度 | 推荐纳入 | 降优先级 / 排除 |",
        "|---|---|---|",
        "| 状态机结构 | 有明确 states/events/transitions/modes/hierarchy，且 NL 能支持这些元素 | 只有流程叙述或连续优化公式，离散状态边界不清 |",
        "| 变量参与度 | 变量进入 guard/action/invariant/output decision，并存在事件或动作可更新变量值 | 变量只在背景中出现，或仅作为 guard 常量被读取但从不写入，即“吉祥物变量” |",
        "| 事件/触发 | 有外部事件、内部事件、故障/恢复、cut-in/out 等触发 | 纯连续控制或静态功率分配，缺少事件驱动逻辑 |",
        "| 论文证据 | `paper_content.txt` 可追溯支持 NL，必要图表可由 `paper.pdf` 核对 | 关键逻辑只在难解析图中，或抽取文本不足以复核 |",
        "| 复杂度 | 中等复杂度，足以展示层次/guard/action，但每轮可诊断 | 过小 toy case；或超大系统导致预算内无法形成有效诊断 |",
        "| Path1 需求 | 有 reference/signed behavior，适合和 ref model 比较 | gold/ref 过弱或人工标注不可复核 |",
        "| Path2 需求 | 能体现变量、guard、scenario、repair/review 的利用价值 | baseline 靠状态名即可猜对，或变量/guard 不影响运行 |",
        "",
        "筛选原则：先定义标准，再筛样本；被排除样本必须记录原因，不能为了结果好看事后 cherry-pick。",
        "",
        "## 5. 后续 reviewer 关注点",
        "",
        "- 是否已有足够 run record/report 证明 PR-E1 达成“实测 agent-loop 参数探索与问题闭环”的目标。",
        "- C/I 级问题只应指向学术可靠性、可复现性、run-record/secret/schema 污染或主结论越界；纯工程 polish 默认 M。",
        "- 若 reviewer 建议 micro-fix，必须不改变 SC/SD/SL stage graph，并用 paired rerun 对比。",
        "- 必须审查是否存在针对 ABS/CARA/Elevator/LNG 等具体样本的 lexical special-case、hard-coded hint、case_id 分支或 benchmark overfit；这类不具备普适性/学术解释力的优化应按 C/I 级处理。",
    ])
    return "\n".join(lines).rstrip() + "\n"


def render_pr_comment(summaries: Sequence[PrE1RunSummary], *, output_dir: str | Path = "runs/pr_e1_real_agent_loop") -> str:
    output_dir_text = _as_posix(output_dir)
    lines = [
        "## PR-E1 real-run evidence update",
        "",
        "身份：主 session / PR-E1 runner。",
        "",
        f"本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `{output_dir_text}/`。",
        "",
        "| Path | case | config | verdict | status | clean | eligible | failure class | tokens | report |",
        "|---|---|---|---|---|---:|---:|---|---:|---|",
    ]
    for s in summaries:
        lines.append(
            f"| {s.path} | `{s.case_key}` | `{s.config_id}` | `{s.verdict}` | `{s.record_status}` | {'✅' if s.clean_commit_bound else '❌'} | {'✅' if s.main_result_eligible else '❌'} | `{s.primary_failure_class}` | {_escape_md(_token_display(s.token_usage))} | `{output_dir_text}/{s.run_id}/report.md` |"
        )
    lines.extend(
        [
            "",
            "### 可复现性边界",
            "",
            *_reproducibility_observation_lines(summaries),
            "",
            "### 初步观察",
            "",
            *_configuration_observation_lines(summaries),
            "",
            "### 主要失败模式",
            "",
            *_failure_observation_lines(summaries),
            "",
            "### 样本筛选观察",
            "",
            *_sample_observation_lines(summaries),
            "",
            "### Reviewer 追加审查项：禁止样本特判 / benchmark overfit",
            "",
            "- 后续三路 reviewer 需显式检查 agent-loop / prompt / deterministic policy 是否包含针对 ABS、CARA、Elevator、LNG EMS 或本 PR 4 个样本的 lexical special-case、case_id 分支、hard-coded hint、结果导向参数。",
            "- 允许的优化必须是普适、可解释、可迁移的机制；例如通过 prompt 要求 LLM 区分外部输入与内部状态，而不是在代码中写样本专用词表。",
            "- 若发现样本特判影响 blocking/advisory、repair target、scenario oracle 或主结论归类，应至少按 I 级处理；若污染 main_result_eligible 或论文结论则按 C 级处理。",
            "",
            "### 4 例详细输入 / 输出 / artifact",
            "",
            *_per_run_comment_detail_lines(summaries, output_dir_text=output_dir_text),
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def _per_run_comment_detail_lines(summaries: Sequence[PrE1RunSummary], *, output_dir_text: str) -> list[str]:
    if not summaries:
        return ["- 尚无 per-run 详情。"]
    cases = {case.case_key: case for case in pr_e1_cases("all")}
    lines: list[str] = []
    for s in summaries:
        case = cases.get(s.case_key)
        final_dsl = _read_comment_artifact(s.final_dsl_path, max_chars=12000)
        report_path = f"{output_dir_text}/{s.run_id}/report.md"
        run_record_name = Path(s.run_record_path).name if s.run_record_path else "<none>"
        lines.extend(
            [
                f"<details><summary>{s.path} / {s.case_key} / {s.config_id} / {s.verdict}</summary>",
                "",
                "#### NL 输入（原文）",
                "",
                "```text",
                case.nl if case is not None else "<case metadata missing>",
                "```",
                "",
                "#### NL 输入中文翻译",
                "",
                "```text",
                case.nl_zh if case is not None else "<case metadata missing>",
                "```",
                "",
                "#### FCSTM 输出",
                "",
                "```pyfcstm",
                final_dsl,
                "```",
                "",
                "#### agent-loop 过程与日志路径",
                "",
                "| 项 | 值 |",
                "|---|---|",
                f"| verdict / status | `{s.verdict}` / `{s.record_status}` |",
                f"| failure class | `{s.primary_failure_class}` |",
                f"| executed stages | `{' -> '.join(s.executed_stage_ids)}` |",
                f"| iter / repairs / accepted / scenarios | `{s.iteration_count}` / `{s.repair_count}` / `{s.accepted_repair_count}` / `{s.scenario_history_count}` |",
                f"| token / elapsed | `{s.token_usage}` / `{s.elapsed_seconds}s` |",
                f"| full stage table | `{report_path}` §4 |",
                f"| run record | `{output_dir_text}/{s.run_id}/{run_record_name}` |",
                f"| logs | `{output_dir_text}/{s.run_id}/run_logs/stdout.txt`, `{output_dir_text}/{s.run_id}/run_logs/stderr.txt` |",
                f"| checks / repro | `{output_dir_text}/{s.run_id}/checks.json`, `{output_dir_text}/{s.run_id}/reproducibility.json` |",
                "",
                "#### 全流程摘要表（report §4 摘录）",
                "",
                _read_report_section(s.report_path, start="### 4. 全流程真实摘要表", end="### 5. Iteration / repair / review 摘要", max_chars=15000),
                "",
                "#### Scenario 逐轮通过矩阵（report §6.1 摘录）",
                "",
                _read_report_section(s.report_path, start="#### 6.1 Scenario pass/fail by iteration", end="#### 6.2 Scenario definitions", max_chars=5000),
                "",
                "#### Repair / blocking feedback 概览（report §7 摘录）",
                "",
                _read_report_section(s.report_path, start="### 7. Repair / blocking feedback 明细", end="<details><summary>Repair", max_chars=7000),
                "",
                f"> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `{report_path}` §7。",
                "",
                "</details>",
                "",
            ]
        )
    return lines


def _read_comment_artifact(path: str, *, max_chars: int) -> str:
    try:
        text = Path(path).read_text(encoding="utf-8")
    except Exception:
        return "<artifact not available>"
    if len(text) <= max_chars:
        return text.rstrip()
    return text[:max_chars].rstrip() + "\n... <truncated in PR comment; see artifact path>"


def _read_report_section(path: str, *, start: str, end: str, max_chars: int) -> str:
    try:
        text = Path(path).read_text(encoding="utf-8")
    except Exception:
        return "<report section not available>"
    start_index = text.find(start)
    if start_index < 0:
        return "<report section not found>"
    end_index = text.find(end, start_index + len(start))
    section = text[start_index : end_index if end_index >= 0 else len(text)].strip()
    if section.startswith(start):
        section = section[len(start) :].strip()
    if len(section) <= max_chars:
        return section
    return section[:max_chars].rstrip() + f"\n... <truncated {len(section) - max_chars} chars in PR comment; see report.md>"


def _configuration_observation_lines(summaries: Sequence[PrE1RunSummary]) -> list[str]:
    if not summaries:
        return ["- 尚无真实运行证据。"]
    by_config: dict[str, list[PrE1RunSummary]] = {}
    for s in summaries:
        by_config.setdefault(s.config_id, []).append(s)
    lines: list[str] = []
    for config_id in sorted(by_config):
        rows = by_config[config_id]
        successes = sum(1 for row in rows if row.verdict == "success")
        rejected = sum(1 for row in rows if row.record_status == "rejected")
        budget = sum(1 for row in rows if row.record_status == "budget_exhausted")
        total_tokens = _sum_numeric(row.token_usage.get("total_tokens") for row in rows)
        estimated_tokens = _sum_numeric(row.token_usage.get("estimated_total_tokens") for row in rows)
        if total_tokens is not None:
            token_text = f"total_tokens={total_tokens}"
        elif estimated_tokens is not None:
            token_text = f"estimated_total_tokens≈{estimated_tokens}（provider未返回stream usage，不当作真实token）"
        else:
            token_text = "token_usage=unknown"
        lines.append(
            f"- `{config_id}`：{successes}/{len(rows)} success，rejected={rejected}，budget_exhausted={budget}，{token_text}。"
        )
    max_iteration_values = {condition_specs()[s.config_id].max_iterations for s in summaries if s.config_id in condition_specs()}
    observed_multi_iter = any(s.iteration_count > 1 for s in summaries)
    if len(max_iteration_values) > 1 and not observed_multi_iter:
        lines.append("- Q1/max_iterations：当前所有样本均未观察到 `iteration_count > 1`，因此只能说明这些 run 在首轮 repair review 之前/之处失败；不能把它外推为“增加 `max_iterations` 无用”。")
    elif all(s.verdict != "success" for s in summaries):
        lines.append("- Q1/max_iterations：当前证据未产生 success；若 run 早停于 `rejected`，瓶颈更可能是 prompt/repair candidate quality 或样本变量语义，而不是单纯迭代预算。")
    if not any("SL-5" in s.executed_stage_ids for s in summaries):
        lines.append("- Q1/scenario-review 维度：当前矩阵尚未进入 SL-5/SD-6/SL-7/SL-10，因此 `scenario_max_retries`、`model_review_mode`、`repair_review_mode` 仍属于未回答问题。")
    eligible_count = sum(1 for s in summaries if s.main_result_eligible)
    lines.append(f"- 主结果候选：当前 {eligible_count}/{len(summaries)} run 可进入 main_result_eligible；其余只能作为 exploratory / infrastructure evidence。")
    return lines


def _reproducibility_observation_lines(summaries: Sequence[PrE1RunSummary]) -> list[str]:
    if not summaries:
        return ["- 尚无 run，因此没有可复现性证据。"]
    clean = sum(1 for s in summaries if s.clean_commit_bound)
    lines = [f"- clean commit 绑定：{clean}/{len(summaries)} run 的 `reproducibility.json` 记录 dirty=false。"]
    dirty_runs = [s.run_id for s in summaries if not s.clean_commit_bound]
    if dirty_runs:
        lines.append("- dirty / 不可确认 run 不应用作 paired causal conclusion，只能作为探索线索：" + ", ".join(f"`{run_id}`" for run_id in dirty_runs[:6]) + (" ..." if len(dirty_runs) > 6 else ""))
    hashes = sorted({s.prompt_snapshot_hash for s in summaries if s.prompt_snapshot_hash})
    lines.append(f"- prompt snapshot hash 种类：{len(hashes)}；用于确认同一轮 4 例是否共享同一 prompt/context 版本。")
    lines.append("- 每个 run 的 `reproducibility.json` 保存 git commit、dirty flag、diff hash、prompt file hash、runner command/config 与 source/paper path。")
    return lines


def _sample_observation_lines(summaries: Sequence[PrE1RunSummary]) -> list[str]:
    if not summaries:
        return ["- 尚无样本运行证据。"]
    by_case: dict[str, list[PrE1RunSummary]] = {}
    for s in summaries:
        by_case.setdefault(s.case_key, []).append(s)
    lines = [f"- 样本覆盖：{len(by_case)} 个 case，Path1={sum(1 for k in by_case if k.startswith('path1_'))}，Path2={sum(1 for k in by_case if k.startswith('path2_'))}。"]
    for case_key, rows in sorted(by_case.items()):
        classes = ", ".join(sorted({row.primary_failure_class for row in rows}))
        max_iter_seen = max((row.iteration_count for row in rows), default=0)
        lines.append(f"- `{case_key}`：失败/成功类别={classes or '<none>'}，最大 observed iteration_count={max_iter_seen}。")
    if any(s.primary_failure_class == "design_or_variable_dynamics" for s in summaries):
        lines.append("- 实证筛选更新：若论文变量主要是外部传感/环境输入，应在样本记录中明确“只读输入”身份；若模型需要内部状态变量，则必须有 NL-grounded write/action，否则容易被 SD-4 阻断。")
    if any(s.primary_failure_class == "grounding_or_required_element_loss" for s in summaries):
        lines.append("- 实证筛选更新：repair 能通过局部语法/语义但丢失 required grounded elements 的样本，应标为高风险，不应因为预算增大而视为质量提升。")
    return lines


def _failure_observation_lines(summaries: Sequence[PrE1RunSummary]) -> list[str]:
    if not summaries:
        return ["- 尚无失败模式证据。"]
    counts: dict[str, int] = {}
    for s in summaries:
        counts[s.primary_failure_class] = counts.get(s.primary_failure_class, 0) + 1
    lines = [f"- `{key}`：{value} run(s)。" for key, value in sorted(counts.items(), key=lambda item: (-item[1], item[0]))]
    if counts.get("design_or_variable_dynamics"):
        lines.append("- `design_or_variable_dynamics` 与变量只读不写、guard 变量永不变化等风险相关，需在样本筛选和 SL-9 prompt 中区分环境输入变量与内部状态变量。")
    if counts.get("grounding_or_required_element_loss"):
        lines.append("- `grounding_or_required_element_loss` 表示 repair 虽可能通过局部语法/语义检查，但丢失 NL-grounded required elements；这类结果不能因更高预算而算作改善。")
    if counts.get("semantic_or_topology") or counts.get("dsl_parse_or_grammar"):
        lines.append("- parse/semantic/topology 类问题说明 pyfcstm grammar 与层次路径约束仍需更强 prompt 约束或 repair context。")
    return lines


def _stage_table_rows(record: AgentLoopRunRecord, summary: PrE1RunSummary) -> list[list[str]]:
    rows: list[list[str]] = []
    stage_records = record.stage_records
    for idx, meta in enumerate(stage_records):
        if not isinstance(meta, dict):
            meta = asdict(meta)
        stage_id = str(meta.get("stage_id"))
        status = str(meta.get("status"))
        ok = bool(meta.get("ok"))
        rows.append(
            [
                f"`{stage_id}`",
                "是" if str(meta.get("stage_kind")) == "LLM" else "否",
                _iteration_for_stage(record, idx, stage_id),
                _status_icon(status, ok),
                _stage_feedback_summary(record, stage_id),
                _stage_action_summary(stage_id),
                _stage_dsl_delta(record, stage_id),
                "[`record`](./%s)" % Path(summary.run_record_path).name,
            ]
        )
    return rows


def _iteration_table_rows(record: AgentLoopRunRecord) -> list[list[str]]:
    if not record.iteration_records:
        return [["-", "<none>", "no", "<none>", "<none>", "<none>", "<none>", "no", "no iteration record"]]
    rows: list[list[str]] = []
    for item in record.iteration_records:
        if not isinstance(item, dict):
            continue
        selected = item.get("selected_feedback") if isinstance(item.get("selected_feedback"), dict) else None
        source_stage = selected.get("source_stage") if isinstance(selected, dict) else None
        source = selected.get("source") if isinstance(selected, dict) else None
        batch = item.get("fix_request_batch") if isinstance(item.get("fix_request_batch"), dict) else {}
        requests = batch.get("requests") if isinstance(batch, dict) else None
        batch_text = "<none>"
        if isinstance(requests, list):
            batch_text = f"{batch.get('batch_id') or '<batch>'} / n={len(requests)}"
        sl9 = item.get("sl9_decision") if isinstance(item.get("sl9_decision"), dict) else {}
        sl9_text = _sl9_decision_compact(sl9)
        local_evidence = item.get("local_check_evidence") if isinstance(item.get("local_check_evidence"), dict) else {}
        local_text = _local_check_compact(local_evidence)
        sl10 = item.get("sl10_repair_review") if isinstance(item.get("sl10_repair_review"), dict) else None
        repair_review = item.get("repair_review") if isinstance(item.get("repair_review"), dict) else None
        if sl10 is None and isinstance(repair_review, dict):
            delta = repair_review.get("delta_review")
            sl10 = delta if isinstance(delta, dict) else repair_review
        sl10_text = _sl10_review_compact(sl10 if isinstance(sl10, dict) else {})
        rows.append(
            [
                str(item.get("iteration", "-")),
                f"`{source_stage or source or '<none>'}`",
                "yes" if item.get("repair_stage_ids") else "no",
                _escape_md(_short_text(batch_text, 220)),
                _escape_md(_short_text(sl9_text, 220)),
                _escape_md(_short_text(local_text, 220)),
                _escape_md(_short_text(sl10_text, 220)),
                "yes" if item.get("accepted_candidate") else "no",
                str(item.get("exit_reason") or ""),
            ]
        )
    return rows


def _flow_log_lines(record: AgentLoopRunRecord) -> list[str]:
    logs = record.logs if isinstance(record.logs, list) else []
    if not logs:
        return ["- 本 run record 未记录流程日志；这通常表示旧格式记录或流程在日志初始化前异常退出。"]
    lines: list[str] = [
        "| # | ts | stage | iter | event | result / jump | DSL evidence |",
        "|---:|---|---|---:|---|---|---|",
    ]
    for index, item in enumerate(logs[:80], start=1):
        if not isinstance(item, dict):
            continue
        dsl_bits = []
        for key in ("dsl", "current_dsl", "old_dsl", "candidate_dsl", "final_dsl"):
            value = item.get(key)
            if isinstance(value, str) and value:
                dsl_bits.append(f"{key}:len={len(value)},hash={_short_hash_text(value)}")
        if item.get("candidate_dsl_hash") and not any(part.startswith("candidate_dsl:") for part in dsl_bits):
            dsl_bits.append(f"candidate_hash={item.get('candidate_dsl_hash')}")
        if item.get("current_dsl_hash") and not any(part.startswith("current_dsl:") for part in dsl_bits):
            dsl_bits.append(f"current_hash={item.get('current_dsl_hash')}")
        if item.get("final_dsl_hash") and not any(part.startswith("final_dsl:") for part in dsl_bits):
            dsl_bits.append(f"final_hash={item.get('final_dsl_hash')}")
        result_payload = {
            key: item.get(key)
            for key in (
                "ok",
                "status",
                "reason",
                "decision",
                "jump",
                "accepted",
                "selected_feedback",
                "request_count",
                "accepted_request_ids",
                "rejected_request_ids",
                "verdict",
            )
            if key in item
        }
        lines.append(
            "| {idx} | `{ts}` | `{stage}` | `{iteration}` | `{event}` | {result} | {dsl} |".format(
                idx=index,
                ts=_escape_md(str(item.get("ts") or "")),
                stage=_escape_md(str(item.get("stage_id") or "<control>")),
                iteration=_escape_md(str(item.get("iteration") if item.get("iteration") is not None else "-")),
                event=_escape_md(str(item.get("event") or "<none>")),
                result=_escape_md(_short_text(json.dumps(result_payload, ensure_ascii=False, sort_keys=True), 420)),
                dsl=_escape_md(_join_limited(dsl_bits, limit=5) or "<none>"),
            )
        )
    if len(logs) > 80:
        lines.append(f"- ……另有 `{len(logs) - 80}` 条流程日志见 [`flow_log.json`](./flow_log.json) / run record。")
    return lines


def _scenario_report_lines(record: AgentLoopRunRecord) -> list[str]:
    """Render human-readable scenarios and per-iteration pass/fail matrix."""

    scenarios = _latest_scenarios_from_record(record)
    sim_by_iteration = _sim_results_by_iteration(record)
    if not scenarios and not sim_by_iteration:
        return [
            "- 本 run 未生成或未执行 scenario；通常表示流程在 `SL-5` 之前因 provider/schema/parse/semantic/design 等问题退出。",
        ]

    lines: list[str] = [
        "#### 6.1 Scenario pass/fail by iteration",
        "",
        "口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。",
        "",
    ]
    iteration_ids = sorted(sim_by_iteration)
    scenario_names = _scenario_names_for_matrix(scenarios, sim_by_iteration)
    if iteration_ids and scenario_names:
        header = ["Scenario", "Intent"] + [f"Iter {idx + 1}" for idx in iteration_ids]
        lines.append("| " + " | ".join(header) + " |")
        lines.append("|" + "---|" * len(header))
        descriptions = {str(item.get("name", "")): str(item.get("description", "")) for item in scenarios if isinstance(item, dict)}
        for name in scenario_names:
            row = [f"`{_escape_md(name)}`", _escape_md(_short_text(descriptions.get(name, ""), 120))]
            for idx in iteration_ids:
                status = sim_by_iteration.get(idx, {}).get(name)
                row.append(_scenario_status_icon(status))
            lines.append("| " + " | ".join(row) + " |")
    else:
        lines.append("- 没有可形成矩阵的 SD-6 simulation 结果。")

    lines.extend(["", "#### 6.2 Scenario definitions", ""])
    if scenarios:
        for scenario in scenarios:
            lines.extend(_scenario_definition_lines(scenario))
    else:
        lines.append("- 有 simulation 结果，但 run record 中没有可展示的 SL-5 scenario 定义。")

    return lines


def _latest_scenarios_from_record(record: AgentLoopRunRecord) -> list[dict[str, Any]]:
    scenarios: list[dict[str, Any]] = []
    for interaction in record.llm_interactions:
        if not isinstance(interaction, dict) or interaction.get("stage_id") != "SL-5":
            continue
        parsed = interaction.get("parsed_output")
        if isinstance(parsed, dict) and isinstance(parsed.get("scenarios"), list):
            scenarios = [item for item in parsed["scenarios"] if isinstance(item, dict)]
    return scenarios


def _sim_results_by_iteration(record: AgentLoopRunRecord) -> dict[int, dict[str, str]]:
    result: dict[int, dict[str, str]] = {}
    feedback = record.deterministic_feedback if isinstance(record.deterministic_feedback, dict) else {}
    iterations = feedback.get("iterations", []) if isinstance(feedback, dict) else []
    if not isinstance(iterations, list):
        return result
    for fallback_index, item in enumerate(iterations):
        if not isinstance(item, dict):
            continue
        iteration = item.get("iteration", fallback_index)
        try:
            iteration_index = int(iteration)
        except (TypeError, ValueError):
            iteration_index = fallback_index
        sim = item.get("sim")
        if not isinstance(sim, dict):
            continue
        scenario_results = sim.get("scenario_results")
        if not isinstance(scenario_results, list):
            continue
        by_name: dict[str, str] = {}
        for scenario_result in scenario_results:
            if not isinstance(scenario_result, dict):
                continue
            name = str(scenario_result.get("name", ""))
            if name:
                by_name[name] = str(scenario_result.get("status", ""))
        result[iteration_index] = by_name
    return result


def _scenario_names_for_matrix(scenarios: list[dict[str, Any]], sim_by_iteration: dict[int, dict[str, str]]) -> list[str]:
    names: list[str] = []
    seen: set[str] = set()
    for scenario in scenarios:
        name = str(scenario.get("name", "")) if isinstance(scenario, dict) else ""
        if name and name not in seen:
            names.append(name)
            seen.add(name)
    for by_name in sim_by_iteration.values():
        for name in by_name:
            if name and name not in seen:
                names.append(name)
                seen.add(name)
    return names


def _scenario_status_icon(status: str | None) -> str:
    if status == "pass":
        return "✅"
    if status == "fail":
        return "❌"
    return "⚪"


def _scenario_definition_lines(scenario: dict[str, Any]) -> list[str]:
    name = str(scenario.get("name", "<unnamed>"))
    description = str(scenario.get("description", ""))
    initial_state = scenario.get("initial_state")
    initial_vars = scenario.get("initial_vars") if isinstance(scenario.get("initial_vars"), dict) else {}
    steps = scenario.get("steps") if isinstance(scenario.get("steps"), list) else []
    lines = [
        f"<details><summary>`{_escape_md(name)}` — {_escape_md(_short_text(description, 160))}</summary>",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| description | {_escape_md(description or '<none>')} |",
        f"| initial_state | `{_escape_md(str(initial_state)) if initial_state is not None else '<default-init>'}` |",
        f"| initial_vars | `{_escape_md(json.dumps(initial_vars, ensure_ascii=False, sort_keys=True))}` |",
        "",
        "| Step | before_cycles | events | expected_state | expected_vars |",
        "|---:|---:|---|---|---|",
    ]
    if not steps:
        lines.append("| - | - | - | - | - |")
    for index, step in enumerate(steps):
        if not isinstance(step, dict):
            continue
        events = step.get("events")
        expected_vars = step.get("expected_vars")
        lines.append(
            "| {idx} `{name}` | `{before}` | `{events}` | `{state}` | `{vars}` |".format(
                idx=index,
                name=_escape_md(str(step.get("name", ""))),
                before=_escape_md(str(step.get("before_cycles", 0))),
                events=_escape_md(json.dumps(events or [], ensure_ascii=False)),
                state=_escape_md(str(step.get("expected_state")) if step.get("expected_state") is not None else ""),
                vars=_escape_md(json.dumps(expected_vars or {}, ensure_ascii=False, sort_keys=True)),
            )
        )
    lines.extend(["", "</details>", ""])
    return lines


def _short_text(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + f"...<truncated {len(text) - limit} chars>"


def _escape_md(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def _repair_report_lines(record: AgentLoopRunRecord) -> list[str]:
    """Render each repair block with cause, requests, decisions, candidate, diff and review evidence."""

    repairs = [item for item in record.repair_history if isinstance(item, dict)]
    if not repairs:
        return [
            "- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。",
        ]

    lines: list[str] = [
        "口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。",
        "",
        "| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |",
        "|---:|---:|---:|---|---|---|---|---|",
    ]
    for index, item in enumerate(repairs, start=1):
        selected = item.get("selected_feedback") if isinstance(item.get("selected_feedback"), dict) else {}
        fix_plan = item.get("fix_plan") if isinstance(item.get("fix_plan"), dict) else {}
        sl10 = _sl10_review_dict(item)
        local = _local_check_dict(item)
        source = selected.get("source_stage") or selected.get("source") or fix_plan.get("source_stage") or "<none>"
        diagnostics = _diagnostic_list(selected, fix_plan)
        lines.append(
            "| {idx} | `{iteration}` | {accepted} | `{source}` | {diagnostics} | {sl9} | {review} | `{candidate_hash}` |".format(
                idx=index,
                iteration=item.get("iteration", "-"),
                accepted="✅" if item.get("accepted") is True else "❌",
                source=_escape_md(str(source)),
                diagnostics=_escape_md(_join_limited(diagnostics, limit=5)),
                sl9=_escape_md(_short_text(_sl9_decision_compact(_sl9_decision_dict(item)), 220)),
                review=_escape_md(_short_text(_sl10_and_local_compact(sl10, local), 260)),
                candidate_hash=_escape_md(str(item.get("candidate_dsl_hash") or "<none>")),
            )
        )

    lines.append("")
    for index, item in enumerate(repairs, start=1):
        lines.extend(_single_repair_detail_lines(index, item, repairs, record))
    lines.extend(_fix_log_ledger_lines(record))
    return lines

def _single_repair_detail_lines(
    index: int,
    item: dict[str, Any],
    repairs: Sequence[dict[str, Any]],
    record: AgentLoopRunRecord,
) -> list[str]:
    selected = item.get("selected_feedback") if isinstance(item.get("selected_feedback"), dict) else {}
    fix_plan = item.get("fix_plan") if isinstance(item.get("fix_plan"), dict) else {}
    rr = _repair_review_dict(item)
    sl10 = _sl10_review_dict(item)
    local_checks = _local_check_dict(item)
    candidate_dsl = str(item.get("candidate_dsl") or "")
    before_dsl = _before_dsl_for_repair(index - 1, item, repairs, record)
    diff_lines = _dsl_diff_lines(before_dsl, candidate_dsl)
    candidate_preview = _code_block_text(candidate_dsl, max_chars=9000)
    diagnostics = _diagnostic_list(selected, fix_plan)
    evidence_lines = _fix_plan_evidence_lines(fix_plan)
    hint_lines = _fix_plan_hint_lines(fix_plan)
    variable_role_lines = _variable_role_lines(selected)
    rr_lines = _repair_review_detail_lines(rr, sl10, local_checks)
    batch_lines = _fix_request_batch_lines(_fix_request_batch_dict(item))
    sl9_lines = _sl9_decision_lines(_sl9_decision_dict(item))
    before_hash = _escape_md(str(fix_plan.get("before_dsl_hash") or _repair_input_summary(item).get("old_dsl_hash") or "<unknown>"))
    candidate_hash = _escape_md(str(item.get("candidate_dsl_hash") or _repair_input_summary(item).get("candidate_dsl_hash") or "<unknown>"))
    source = selected.get("source_stage") or selected.get("source") or fix_plan.get("source_stage") or "<none>"
    problem_summary = str(fix_plan.get("problem_summary") or selected.get("source") or "<none>")

    lines = [
        f"<details><summary>Repair {index} / iteration `{item.get('iteration', '-')}` / source `{_escape_md(str(source))}` / accepted={'✅' if item.get('accepted') is True else '❌'}</summary>",
        "",
        "#### 为什么进入修复",
        "",
        f"- selected feedback source：`{_escape_md(str(source))}`；blocking=`{selected.get('blocking')}`；pre_scenario=`{selected.get('pre_scenario') or selected.get('is_pre_scenario')}`。",
        f"- problem_summary：{_escape_md(_short_text(problem_summary, 600))}",
        f"- diagnostic ids：`{_escape_md(_join_limited(diagnostics, limit=12))}`。",
        f"- before_dsl_hash：`{before_hash}`；candidate_dsl_hash：`{candidate_hash}`。",
        "",
        "#### 错误证据 / diagnostics",
        "",
    ]
    lines.extend(evidence_lines or ["- fix_plan 未记录结构化 evidence；请查看 run record 原文。"])
    if variable_role_lines:
        lines.extend(["", "#### 变量角色与上下文提示", ""])
        lines.extend(variable_role_lines)
    lines.extend(["", "#### SD-8 FixRequestBatch / 修改请求", ""])
    lines.extend(batch_lines or ["- 未记录 fix_request_batch；兼容旧 run record 时请查看 fix_plan。"])
    lines.extend(["", "#### SD-8 legacy fix plan / 修改建议", ""])
    lines.extend(hint_lines or ["- fix_plan 未记录 suggested_fix_hints / recommended_strategy。"])
    forbidden = fix_plan.get("forbidden_edits")
    preserve = fix_plan.get("required_preserve_element_ids")
    if isinstance(forbidden, list) and forbidden:
        lines.append(f"- forbidden_edits：`{_escape_md(_join_limited([str(x) for x in forbidden], limit=6))}`。")
    if isinstance(preserve, list) and preserve:
        lines.append(f"- required_preserve_element_ids：`{_escape_md(_join_limited([str(x) for x in preserve], limit=12))}`。")
    lines.extend(["", "#### SL-9 per-request 决策", ""])
    lines.extend(sl9_lines or ["- 未记录 SL-9 structured decisions；可能为旧 DSL-only 输出。"] )
    lines.extend(["", "#### SL-9 candidate / 最终修改执行方案", ""])
    if candidate_dsl:
        lines.extend(["```pyfcstm", candidate_preview, "```"])
    else:
        lines.append("- 本 repair 未记录 candidate_dsl。")
    lines.extend(["", "#### Candidate diff（before -> candidate）", ""])
    lines.extend(diff_lines)
    lines.extend(["", "#### SL-10 审查结果", ""])
    lines.extend(rr_lines)
    lines.extend(["", "</details>", ""])
    return lines


def _repair_review_dict(item: dict[str, Any]) -> dict[str, Any]:
    for key in ("repair_review", "sd10_repair_review"):
        value = item.get(key)
        if isinstance(value, dict):
            return value
    return {}


def _repair_input_summary(item: dict[str, Any]) -> dict[str, Any]:
    value = item.get("repair_review_input_summary")
    return value if isinstance(value, dict) else {}

def _fix_request_batch_dict(item: dict[str, Any]) -> dict[str, Any]:
    value = item.get("fix_request_batch")
    return value if isinstance(value, dict) else {}


def _sl9_decision_dict(item: dict[str, Any]) -> dict[str, Any]:
    value = item.get("sl9_decision")
    return value if isinstance(value, dict) else {}


def _sl10_review_dict(item: dict[str, Any]) -> dict[str, Any]:
    value = item.get("sl10_repair_review")
    if isinstance(value, dict):
        return value
    rr = item.get("repair_review")
    if isinstance(rr, dict):
        delta = rr.get("delta_review")
        if isinstance(delta, dict) and delta.get("legacy_field") == "sl10_repair_review":
            return delta
    return {}


def _local_check_dict(item: dict[str, Any]) -> dict[str, Any]:
    value = item.get("local_check_evidence")
    if isinstance(value, dict):
        return value
    sl10 = _sl10_review_dict(item)
    value = sl10.get("local_check_evidence")
    return value if isinstance(value, dict) else {}


def _fix_request_batch_lines(batch: dict[str, Any]) -> list[str]:
    if not batch:
        return []
    requests = batch.get("requests") if isinstance(batch.get("requests"), list) else []
    lines = [
        f"- batch_id：`{_escape_md(str(batch.get('batch_id') or '<none>'))}`；source_stage=`{_escape_md(str(batch.get('source_stage') or '<none>'))}`；legacy_plan_kind=`{_escape_md(str(batch.get('legacy_plan_kind') or '<none>'))}`；requests=`{len(requests)}`。"
    ]
    if requests:
        lines.extend(["", "| request_id | severity | hard | waiver | problem | evidence |", "|---|---|---:|---:|---|---|"])
        for req in requests[:10]:
            if not isinstance(req, dict):
                continue
            evidence = req.get("evidence") if isinstance(req.get("evidence"), list) else []
            ev_text = _join_limited([str((ev or {}).get("code") or (ev or {}).get("kind") or (ev or {}).get("instance_key") or ev) for ev in evidence if isinstance(ev, dict)], limit=3)
            lines.append(
                "| `{rid}` | `{sev}` | {hard} | {waiver} | {problem} | `{ev}` |".format(
                    rid=_escape_md(str(req.get("request_id") or "<none>")),
                    sev=_escape_md(str(req.get("severity") or "<none>")),
                    hard="✅" if req.get("hard_block") else "❌",
                    waiver="✅" if req.get("waiver_allowed") else "❌",
                    problem=_escape_md(_short_text(str(req.get("problem_summary") or ""), 220)),
                    ev=_escape_md(ev_text),
                )
            )
        if len(requests) > 10:
            lines.append(f"- ……另有 `{len(requests) - 10}` 个 request 见 run record。")
    return lines


def _sl9_decision_lines(decision: dict[str, Any]) -> list[str]:
    if not decision:
        return []
    decisions = decision.get("decisions") if isinstance(decision.get("decisions"), list) else []
    lines = [
        f"- accepted_request_ids：`{_escape_md(_join_limited([str(x) for x in decision.get('accepted_request_ids', [])], limit=12)) if isinstance(decision.get('accepted_request_ids'), list) else '<derived-from-table>'}`；candidate_len=`{len(str(decision.get('candidate_dsl') or ''))}`。"
    ]
    if decisions:
        lines.extend(["", "| request_id | decision | waiver | rework_locked | rationale / intent |", "|---|---|---:|---:|---|"])
        for row in decisions[:12]:
            if not isinstance(row, dict):
                continue
            intent = row.get("accepted_edit_intent") if isinstance(row.get("accepted_edit_intent"), list) else []
            text = str(row.get("rationale") or row.get("rejected_reason") or "")
            if intent:
                text += "；intent=" + _join_limited([str(x) for x in intent], limit=3)
            lines.append(
                "| `{rid}` | `{decision}` | {waiver} | {locked} | {text} |".format(
                    rid=_escape_md(str(row.get("request_id") or "<none>")),
                    decision=_escape_md(str(row.get("decision") or "<none>")),
                    waiver="✅" if row.get("waiver") else "❌",
                    locked="✅" if row.get("rework_locked") else "❌",
                    text=_escape_md(_short_text(text, 360)),
                )
            )
    rationale = decision.get("repair_rationale")
    if isinstance(rationale, list) and rationale:
        lines.append("- repair_rationale：" + "；".join(_escape_md(_short_text(str(x), 240)) for x in rationale[:5]))
    diff = decision.get("diff_summary")
    if isinstance(diff, dict) and diff:
        lines.append(f"- diff_summary：`{_escape_md(_short_text(json.dumps(diff, ensure_ascii=False, sort_keys=True), 700))}`。")
    return lines


def _sl9_decision_compact(decision: dict[str, Any]) -> str:
    if not decision:
        return "<none>"
    rows = decision.get("decisions") if isinstance(decision.get("decisions"), list) else []
    accepted = 0
    rejected = 0
    waived = 0
    if isinstance(rows, list):
        accepted = sum(1 for row in rows if isinstance(row, dict) and row.get("decision") == "accept")
        rejected = sum(1 for row in rows if isinstance(row, dict) and row.get("decision") == "reject")
        waived = sum(1 for row in rows if isinstance(row, dict) and row.get("waiver"))
    return f"accept={accepted}, reject={rejected}, waiver={waived}"


def _local_check_compact(local: dict[str, Any]) -> str:
    if not local:
        return "<none>"
    feedback = local.get("repair_review_feedback") if isinstance(local.get("repair_review_feedback"), dict) else {}
    meta = local.get("meta") if isinstance(local.get("meta"), dict) else {}
    if feedback:
        local_rej = feedback.get("local_rejection") if isinstance(feedback.get("local_rejection"), dict) else {}
        return "ok={ok}, target={target}, regression={regression}, drift={drift}, local_stage={stage}, reason={reason}".format(
            ok=feedback.get("ok"),
            target=feedback.get("target_resolved"),
            regression=feedback.get("regression_detected"),
            drift=feedback.get("drift_risk") or local_rej.get("drift_risk"),
            stage=local.get("legacy_local_check_stage_id") or meta.get("stage_id") or "<none>",
            reason=_short_text(str(local_rej.get("reason") or ""), 120),
        )
    return _short_text(json.dumps(local, ensure_ascii=False, sort_keys=True), 220)


def _sl10_review_compact(sl10: dict[str, Any]) -> str:
    if not sl10:
        return "<none>"
    return "decision={decision}, ok={ok}, target={target}, regression={regression}, drift={drift}, rework={rework}".format(
        decision=sl10.get("decision"),
        ok=sl10.get("ok"),
        target=sl10.get("target_resolved"),
        regression=sl10.get("regression_detected"),
        drift=sl10.get("drift_risk"),
        rework=_join_limited([str(x) for x in sl10.get("rework_instructions", [])], limit=2) if isinstance(sl10.get("rework_instructions"), list) else "<none>",
    )


def _sl10_and_local_compact(sl10: dict[str, Any], local: dict[str, Any]) -> str:
    parts = []
    if sl10:
        parts.append("SL-10 " + _sl10_review_compact(sl10))
    if local:
        parts.append("local " + _local_check_compact(local))
    return "; ".join(parts) or "<none>"


def _delta_review_dict(repair_review: dict[str, Any]) -> dict[str, Any] | None:
    value = repair_review.get("delta_review")
    return value if isinstance(value, dict) else None


def _diagnostic_list(selected: dict[str, Any], fix_plan: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for key in ("blocking_instance_keys", "diagnostic_codes"):
        raw = selected.get(key)
        if isinstance(raw, list):
            values.extend(str(item) for item in raw if item is not None)
    raw_plan = fix_plan.get("diagnostic_ids")
    if isinstance(raw_plan, list):
        values.extend(str(item) for item in raw_plan if item is not None)
    return _dedupe_keep_order(values)


def _fix_plan_evidence_lines(fix_plan: dict[str, Any]) -> list[str]:
    evidence = fix_plan.get("evidence")
    if not isinstance(evidence, list):
        return []
    lines: list[str] = []
    for index, item in enumerate(evidence[:8], start=1):
        if not isinstance(item, dict):
            continue
        code = item.get("code") or item.get("kind") or "<unknown>"
        instance = item.get("instance_key") or item.get("id") or ""
        message = item.get("message") or item.get("reason") or item.get("summary") or ""
        policy = item.get("policy_action") or item.get("pyfcstm_severity") or ""
        refs = item.get("refs")
        refs_text = json.dumps(refs, ensure_ascii=False, sort_keys=True) if isinstance(refs, dict) else ""
        lines.append(
            "- {idx}. `{code}` `{instance}` policy=`{policy}`：{message}{refs}".format(
                idx=index,
                code=_escape_md(str(code)),
                instance=_escape_md(str(instance)),
                policy=_escape_md(str(policy)),
                message=_escape_md(_short_text(str(message), 360)),
                refs=f"；refs=`{_escape_md(_short_text(refs_text, 300))}`" if refs_text else "",
            )
        )
    if len(evidence) > 8:
        lines.append(f"- ……另有 `{len(evidence) - 8}` 条 evidence 见 run record。")
    return lines


def _fix_plan_hint_lines(fix_plan: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    strategy = fix_plan.get("recommended_strategy")
    if isinstance(strategy, list) and strategy:
        lines.append("- recommended_strategy：" + "；".join(_escape_md(_short_text(str(item), 220)) for item in strategy[:6]))
    hints = fix_plan.get("suggested_fix_hints")
    if isinstance(hints, list):
        for index, hint in enumerate(hints[:6], start=1):
            if isinstance(hint, dict):
                summary = str(hint.get("summary") or hint.get("kind") or "")
                actions = hint.get("recommended_actions")
                action_text = _summarize_recommended_actions(actions)
                do_not = hint.get("do_not")
                do_not_text = _join_limited([str(x) for x in do_not], limit=3) if isinstance(do_not, list) else ""
                tail = []
                if action_text:
                    tail.append(f"actions={action_text}")
                if do_not_text:
                    tail.append(f"do_not={do_not_text}")
                lines.append(f"- hint {index}：{_escape_md(_short_text(summary, 300))}" + (f"；`{_escape_md('；'.join(tail))}`" if tail else ""))
            else:
                lines.append(f"- hint {index}：{_escape_md(_short_text(str(hint), 300))}")
    return lines


def _summarize_recommended_actions(actions: Any) -> str:
    if not isinstance(actions, list):
        return ""
    parts: list[str] = []
    for action in actions[:4]:
        if isinstance(action, dict):
            label = action.get("kind") or action.get("action") or action.get("summary") or action.get("description") or action
            parts.append(_short_text(str(label), 120))
        else:
            parts.append(_short_text(str(action), 120))
    return _join_limited(parts, limit=4)


def _variable_role_lines(selected: dict[str, Any]) -> list[str]:
    summary = selected.get("variable_role_summary")
    if not isinstance(summary, dict):
        return []
    lines = [
        f"- policy：{_escape_md(_short_text(str(summary.get('policy') or '<none>'), 500))}",
        f"- source：{_escape_md(str(summary.get('source') or '<none>'))}",
    ]
    variables = summary.get("variables")
    if isinstance(variables, dict) and variables:
        lines.extend(["", "| Variable | role_hint | nl_token_present | diagnostics |", "|---|---|---:|---|"])
        for name, meta in sorted(variables.items()):
            if isinstance(meta, dict):
                codes = meta.get("diagnostic_codes")
                code_text = _join_limited([str(x) for x in codes], limit=5) if isinstance(codes, list) else ""
                lines.append(
                    "| `{name}` | `{role}` | {present} | `{codes}` |".format(
                        name=_escape_md(str(name)),
                        role=_escape_md(str(meta.get("role_hint") or "<none>")),
                        present="✅" if meta.get("nl_token_present") else "❌",
                        codes=_escape_md(code_text),
                    )
                )
    return lines


def _repair_review_compact(repair_review: dict[str, Any], delta_review: dict[str, Any] | None) -> str:
    """Backward-compatible compact text for legacy callers."""

    sl10 = delta_review if isinstance(delta_review, dict) and delta_review.get("legacy_field") == "sl10_repair_review" else {}
    return _sl10_and_local_compact(sl10, {"repair_review_feedback": repair_review})


def _repair_review_detail_lines(
    repair_review: dict[str, Any],
    sl10_review: dict[str, Any] | None,
    local_check_evidence: dict[str, Any] | None,
) -> list[str]:
    if not repair_review and not sl10_review and not local_check_evidence:
        return ["- 未记录 repair_review / sl10_repair_review / local_check_evidence。"]
    lines: list[str] = []
    if sl10_review:
        lines.append(
            f"- SL-10 decision=`{sl10_review.get('decision')}`，ok=`{sl10_review.get('ok')}`，target_resolved=`{sl10_review.get('target_resolved')}`，regression_detected=`{sl10_review.get('regression_detected')}`，drift_risk=`{sl10_review.get('drift_risk')}`。"
        )
        meta = sl10_review.get("review_meta")
        if isinstance(meta, dict):
            lines.append(
                f"- SL-10 review_meta：schema=`{meta.get('parsed_schema_version')}`，failure_policy=`{meta.get('failure_policy')}`，replay_key=`{_escape_md(str(meta.get('replay_key') or '<none>'))}`。"
            )
        evidence = sl10_review.get("evidence")
        if isinstance(evidence, list) and evidence:
            for index, item in enumerate(evidence[:6], start=1):
                lines.append(f"  - SL-10 evidence {index}: `{_escape_md(_short_text(json.dumps(item, ensure_ascii=False, sort_keys=True), 700))}`")
        rework = sl10_review.get("rework_instructions")
        if isinstance(rework, list) and rework:
            lines.append("- SL-10 rework_instructions：" + "；".join(_escape_md(_short_text(str(x), 360)) for x in rework[:6]))
    else:
        lines.append("- SL-10：`<none>`（旧 record 或本 run 未进入 LLM repair review）。")

    local = local_check_evidence or {}
    if local:
        feedback = local.get("repair_review_feedback") if isinstance(local.get("repair_review_feedback"), dict) else {}
        lines.append(
            f"- local checks evidence：stage=`{local.get('legacy_local_check_stage_id') or local.get('stage_id')}`；note={_escape_md(_short_text(str(local.get('local_check_note') or '<none>'), 360))}。"
        )
        if feedback:
            lines.append(
                f"  - local ok=`{feedback.get('ok')}`，target_resolved=`{feedback.get('target_resolved')}`，regression_detected=`{feedback.get('regression_detected')}`，drift_risk=`{feedback.get('drift_risk')}`。"
            )
            local_rejection = feedback.get("local_rejection")
            if isinstance(local_rejection, dict):
                lines.append(
                    f"  - local_rejection：reason=`{_escape_md(str(local_rejection.get('reason') or '<none>'))}`，rejected_by_stage=`{local_rejection.get('rejected_by_stage')}`。"
                )
                evidence = local_rejection.get("evidence")
                if isinstance(evidence, list):
                    for index, item in enumerate(evidence[:6], start=1):
                        if isinstance(item, dict):
                            lines.append(f"    - local evidence {index}: `{_escape_md(str(item.get('kind') or '<unknown>'))}` {_escape_md(_short_text(json.dumps(item, ensure_ascii=False, sort_keys=True), 500))}")
    elif repair_review:
        lines.append(
            f"- legacy repair_review：ok=`{repair_review.get('ok')}`，target_resolved=`{repair_review.get('target_resolved')}`，regression_detected=`{repair_review.get('regression_detected')}`，drift_risk=`{repair_review.get('drift_risk')}`。"
        )
    return lines


def _fix_log_ledger_lines(record: AgentLoopRunRecord) -> list[str]:
    fix_log = record.fix_log if isinstance(record.fix_log, list) else []
    if not fix_log:
        return ["", "#### FixLog ledger", "", "- 本 run record 未记录 FixLog ledger（可能是旧格式或未进入 repair）。"]
    lines: list[str] = [
        "",
        "#### FixLog ledger",
        "",
        "口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。",
        "",
        "| # | iteration | phase | batch | decisions | next_action | candidate | notes |",
        "|---:|---:|---|---|---|---|---|---|",
    ]
    for index, entry in enumerate(fix_log[:30], start=1):
        if not isinstance(entry, dict):
            continue
        decisions = entry.get("decisions") if isinstance(entry.get("decisions"), list) else []
        accept = sum(1 for row in decisions if isinstance(row, dict) and row.get("decision") == "accept")
        reject = sum(1 for row in decisions if isinstance(row, dict) and row.get("decision") == "reject")
        notes = entry.get("notes") if isinstance(entry.get("notes"), list) else []
        lines.append(
            "| {idx} | `{iteration}` | `{phase}` | `{batch}` | accept={accept}, reject={reject} | `{next}` | `{candidate}` | {notes} |".format(
                idx=index,
                iteration=entry.get("iteration", "-"),
                phase=_escape_md(str(entry.get("phase") or "<none>")),
                batch=_escape_md(str(entry.get("batch_id") or "<none>")),
                accept=accept,
                reject=reject,
                next=_escape_md(str(entry.get("next_action") or "<none>")),
                candidate=_escape_md(str(entry.get("candidate_dsl_hash") or "<none>")),
                notes=_escape_md(_join_limited([str(x) for x in notes], limit=3)),
            )
        )
    if len(fix_log) > 30:
        lines.append(f"- ……另有 `{len(fix_log) - 30}` 条 FixLog entry 见 run record。")
    return lines


def _before_dsl_for_repair(
    zero_based_index: int,
    item: dict[str, Any],
    repairs: Sequence[dict[str, Any]],
    record: AgentLoopRunRecord,
) -> str | None:
    input_summary = _repair_input_summary(item)
    old_dsl = input_summary.get("old_dsl")
    if isinstance(old_dsl, str) and old_dsl:
        return old_dsl
    fix_plan = item.get("fix_plan") if isinstance(item.get("fix_plan"), dict) else {}
    wanted_hash = str(fix_plan.get("before_dsl_hash") or input_summary.get("old_dsl_hash") or "")
    hashed_before = _initial_or_current_dsl_for_hash(record, wanted_hash)
    if hashed_before:
        return hashed_before
    if zero_based_index > 0:
        previous_item = repairs[zero_based_index - 1]
        previous = previous_item.get("candidate_dsl")
        if previous_item.get("accepted") is not True:
            previous = None
        if isinstance(previous, str) and previous:
            return previous
    return _initial_or_current_dsl_for_hash(record, "")


def _initial_or_current_dsl_for_hash(record: AgentLoopRunRecord, wanted_hash: str) -> str | None:
    candidates: list[str] = []
    for interaction in record.llm_interactions:
        if not isinstance(interaction, dict):
            continue
        parsed = interaction.get("parsed_output")
        if isinstance(parsed, dict):
            for key in ("candidate_dsl", "dsl", "model_dsl", "repaired_dsl"):
                value = parsed.get(key)
                if isinstance(value, str) and value:
                    candidates.append(value)
    final_dsl = record.final_artifacts.get("final_dsl") if isinstance(record.final_artifacts, dict) else None
    if isinstance(final_dsl, str) and final_dsl:
        candidates.append(final_dsl)
    if wanted_hash:
        for text in candidates:
            if _hash_text(text) == wanted_hash:
                return text
    return candidates[0] if candidates else None


def _dsl_diff_lines(before_dsl: str | None, candidate_dsl: str) -> list[str]:
    if before_dsl and candidate_dsl:
        raw_lines = list(
            difflib.unified_diff(
                before_dsl.splitlines(),
                candidate_dsl.splitlines(),
                fromfile="before.fcstm",
                tofile="candidate.fcstm",
                lineterm="",
            )
        )
        if not raw_lines:
            return ["- before 与 candidate 文本完全一致；无 diff。"]
        truncated = raw_lines[:220]
        suffix = []
        if len(raw_lines) > len(truncated):
            suffix = [f"... <truncated {len(raw_lines) - len(truncated)} diff lines; see run record candidate_dsl>"]
        return ["```diff", *truncated, *suffix, "```"]
    if candidate_dsl:
        return [
            "- 完整 before DSL 文本不可恢复：run record 只保存了 before hash / compact summary；下面只能展示 candidate。若需要严格 before->after diff，应后续让 `repair_review_input_summary` 或 repair_history 落盘 `old_dsl`。",
            "```pyfcstm",
            _code_block_text(candidate_dsl, max_chars=9000),
            "```",
        ]
    return ["- 无 candidate DSL，因此无法生成 diff。"]


def _code_block_text(text: str, *, max_chars: int) -> str:
    stripped = text.rstrip()
    if len(stripped) <= max_chars:
        return stripped
    return stripped[:max_chars].rstrip() + f"\n... <truncated {len(stripped) - max_chars} chars; see run record>"


def _join_limited(values: Sequence[str], *, limit: int) -> str:
    cleaned = [value for value in values if value]
    head = cleaned[:limit]
    text = ", ".join(head)
    if len(cleaned) > limit:
        text += f", ... +{len(cleaned) - limit}"
    return text or "<none>"


def _dedupe_keep_order(values: Sequence[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            result.append(value)
            seen.add(value)
    return result


def _attempt_lines(record: AgentLoopRunRecord) -> list[str]:
    lines: list[str] = []
    if not record.llm_interactions:
        return ["- 无 LLM interaction 记录。"]
    for interaction in record.llm_interactions:
        if not isinstance(interaction, dict):
            continue
        usage = interaction.get("usage") if isinstance(interaction.get("usage"), dict) else {}
        attempts = interaction.get("attempts") if isinstance(interaction.get("attempts"), list) else []
        lines.append(
            f"- `{interaction.get('stage_id')}`：retry_count=`{interaction.get('retry_count')}`，schema_ok=`{interaction.get('schema_validation_ok')}`，usage=`{usage}`，attempts=`{len(attempts)}`。"
        )
        for attempt in attempts:
            if isinstance(attempt, dict):
                lines.append(
                    f"  - attempt {attempt.get('attempt_index')}: error_kind=`{attempt.get('error_kind')}`，model=`{attempt.get('model_id')}`。"
                )
    return lines


def _stage_feedback_summary(record: AgentLoopRunRecord, stage_id: str) -> str:
    if stage_id.startswith("SL-"):
        usage = [item.get("usage", {}) for item in record.llm_interactions if isinstance(item, dict) and item.get("stage_id") == stage_id]
        total = _sum_numeric(u.get("total_tokens") for u in usage if isinstance(u, dict))
        estimated = _sum_numeric(u.get("estimated_total_tokens") for u in usage if isinstance(u, dict))
        if total is not None:
            token_text = str(total)
        elif estimated is not None:
            token_text = f"~{estimated} est"
        else:
            token_text = "unknown"
        return f"LLM calls={len(usage)}, tokens={token_text}"
    if stage_id == "SD-2":
        return _det_feedback_ok(record, "parse")
    if stage_id == "SD-3":
        return _det_feedback_ok(record, "semantic")
    if stage_id == "SD-4":
        return _design_summary(record)
    if stage_id == "SD-6":
        return _det_feedback_ok(record, "sim")
    if stage_id == "SL-10":
        return _repair_review_summary(record)
    if stage_id == "SC-12":
        return str(record.final_artifacts.get("verdict_reason") or "")[:160]
    return "trace/control"


def _stage_action_summary(stage_id: str) -> str:
    mapping = {
        "SC-0": "初始化 run state",
        "SL-1": "生成初始 DSL 与 grounding seeds",
        "SD-2": "解析 pyfcstm DSL",
        "SD-3": "AST→state-machine semantic check",
        "SD-4": "设计健康与变量/guard 检查",
        "SL-5": "生成模型测试 scenario",
        "SD-5A": "检查 scenario coverage",
        "SC-5F": "冻结 scenario oracle",
        "SD-6": "执行 scenario simulation",
        "SL-7": "LLM model review",
        "SD-8": "生成 FixRequestBatch",
        "SL-9": "LLM per-request accept/reject + repair",
        "SL-10": "LLM repair review（输入 NL/FixLog/local evidence）",
        "SC-11": "接受/拒绝候选",
        "SC-12": "写 final verdict",
        "SC-13": "写审计 run record",
    }
    return mapping.get(stage_id, "stage execution")


def _stage_dsl_delta(record: AgentLoopRunRecord, stage_id: str) -> str:
    if stage_id == "SL-1":
        outputs = [item.get("parsed_output", {}) for item in record.llm_interactions if isinstance(item, dict) and item.get("stage_id") == stage_id]
        if outputs and isinstance(outputs[0], dict):
            dsl = outputs[0].get("candidate_dsl")
            if isinstance(dsl, str):
                return f"initial len={len(dsl)}"
    if stage_id == "SL-9":
        if record.repair_history:
            lengths = [len(str(item.get("candidate_dsl") or "")) for item in record.repair_history if isinstance(item, dict)]
            return "candidate len=" + ",".join(str(x) for x in lengths)
    return "无/见 record"


def _iteration_for_stage(record: AgentLoopRunRecord, stage_index: int, stage_id: str) -> str:
    for item in record.iteration_records:
        if not isinstance(item, dict):
            continue
        ids = list(item.get("stage_ids") or []) + list(item.get("repair_stage_ids") or [])
        if stage_id in ids:
            return str(item.get("iteration"))
    return "-"


def _det_feedback_ok(record: AgentLoopRunRecord, key: str) -> str:
    values: list[str] = []
    for item in record.deterministic_feedback.get("iterations", []) if isinstance(record.deterministic_feedback, dict) else []:
        if isinstance(item, dict) and isinstance(item.get(key), dict):
            fb = item[key]
            diag_count = len(fb.get("diagnostics") or []) if isinstance(fb.get("diagnostics"), list) else 0
            values.append(f"ok={fb.get('ok')}, diag={diag_count}")
    return "; ".join(values)[:180] or "<none>"


def _design_summary(record: AgentLoopRunRecord) -> str:
    parts: list[str] = []
    for item in record.deterministic_feedback.get("iterations", []) if isinstance(record.deterministic_feedback, dict) else []:
        if isinstance(item, dict) and isinstance(item.get("design"), dict):
            d = item["design"]
            parts.append(
                f"blocking={len(d.get('blocking_items') or [])}, advisory={len(d.get('advisory_items') or [])}, info={len(d.get('info_items') or [])}"
            )
    return "; ".join(parts)[:180] or "<none>"


def _token_display(usage: dict[str, Any]) -> str:
    available = usage.get("token_usage_available")
    total = usage.get("total_tokens")
    estimated = usage.get("estimated_total_tokens")
    prompt_chars = usage.get("prompt_chars")
    completion_chars = usage.get("completion_chars")
    if available is True and total is not None:
        return str(total)
    if estimated:
        return f"~{estimated} est (usage unavailable; chars={prompt_chars}/{completion_chars})"
    if total is not None:
        return str(total)
    return "unknown"


def _sum_numeric(values: Sequence[Any]) -> int | None:
    total = 0
    seen = False
    for value in values:
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            total += int(value)
            seen = True
    return total if seen else None


def _repair_review_summary(record: AgentLoopRunRecord) -> str:
    parts = []
    for item in record.repair_history:
        if isinstance(item, dict) and isinstance(item.get("repair_review"), dict):
            rr = item["repair_review"]
            parts.append(f"ok={rr.get('ok')}, target_resolved={rr.get('target_resolved')}, drift={rr.get('drift_risk')}")
    return "; ".join(parts)[:180] or "<none>"


def _status_icon(status: str, ok: bool) -> str:
    if ok and status == "ok":
        return "✅"
    if status == "skipped":
        return "⏭️"
    if status == "error":
        return "❌"
    return "⚠️"


def _token_usage(record: AgentLoopRunRecord) -> dict[str, Any]:
    usage: dict[str, Any] = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "estimated_prompt_tokens": 0,
        "estimated_completion_tokens": 0,
        "estimated_total_tokens": 0,
        "prompt_chars": 0,
        "completion_chars": 0,
        "n_calls": 0,
        "token_usage_available": True,
        "token_usage_unavailable_calls": 0,
    }
    for interaction in record.llm_interactions:
        if not isinstance(interaction, dict):
            continue
        stage_usage = interaction.get("usage")
        if isinstance(stage_usage, dict):
            usage["n_calls"] += 1
            usage_available = stage_usage.get("token_usage_available")
            if usage_available is None:
                usage_available = all(
                    isinstance(stage_usage.get(key), (int, float)) and not isinstance(stage_usage.get(key), bool)
                    for key in ("prompt_tokens", "completion_tokens", "total_tokens")
                )
            if usage_available:
                for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
                    value = stage_usage.get(key, 0)
                    if isinstance(value, (int, float)) and not isinstance(value, bool):
                        usage[key] += int(value)
            else:
                usage["token_usage_available"] = False
                usage["token_usage_unavailable_calls"] += 1
            for key in ("estimated_prompt_tokens", "estimated_completion_tokens", "estimated_total_tokens", "prompt_chars", "completion_chars"):
                value = stage_usage.get(key, 0)
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    usage[key] += int(value)
    if usage["token_usage_unavailable_calls"]:
        usage["prompt_tokens"] = None
        usage["completion_tokens"] = None
        usage["total_tokens"] = None
    return usage


def _executed_stage_ids(record: AgentLoopRunRecord) -> list[str]:
    ids: list[str] = []
    if isinstance(record.stage_graph, dict) and isinstance(record.stage_graph.get("executed"), list):
        ids.extend(str(item) for item in record.stage_graph["executed"])
    for meta in record.stage_records:
        stage_id = meta.get("stage_id") if isinstance(meta, dict) else getattr(meta, "stage_id", None)
        if stage_id and str(stage_id) not in ids:
            ids.append(str(stage_id))
    return ids


def _llm_stage_ids(record: AgentLoopRunRecord) -> list[str]:
    ids: list[str] = []
    for interaction in record.llm_interactions:
        if isinstance(interaction, dict) and interaction.get("stage_id"):
            ids.append(str(interaction["stage_id"]))
    return ids


def _record_public_text(record: AgentLoopRunRecord) -> str:
    return json.dumps(asdict(record), ensure_ascii=False, sort_keys=True, default=str)


def _contains_obvious_secret(text: str) -> bool:
    lowered = text.lower()
    if "authorization: bearer" in lowered:
        return True
    if re.search(r"\bsk-[A-Za-z0-9][A-Za-z0-9._-]{7,}", text):
        return True
    for key in REQUIRED_ENV_KEYS:
        value = os.environ.get(key)
        if value and len(value) >= 8 and value in text:
            return True
    return False


def _as_posix(path: str | Path) -> str:
    return Path(path).as_posix()


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    return str(value)


def _optional_bool(value: object) -> bool | None:
    if value is None:
        return None
    return bool(value)


def summaries_to_jsonable(summaries: Sequence[PrE1RunSummary]) -> list[dict[str, object]]:
    return [asdict(summary) for summary in summaries]


def load_existing_summaries(output_dir: str | Path) -> list[PrE1RunSummary]:
    path = Path(output_dir) / "summary.json"
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    fields = PrE1RunSummary.__dataclass_fields__
    normalized: list[PrE1RunSummary] = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        row: dict[str, object] = {}
        for key, info in fields.items():
            if key in item:
                row[key] = item[key]
            elif info.default is not MISSING:
                row[key] = info.default
            elif info.default_factory is not MISSING:  # type: ignore[comparison-overlap]
                row[key] = info.default_factory()  # type: ignore[misc]
        normalized.append(PrE1RunSummary(**row))
    return normalized


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run PR-E1 real agent-loop matrix and render reports.")
    parser.add_argument("--output-dir", default="runs/pr_e1_real_agent_loop")
    parser.add_argument("--case-set", default="mandatory", choices=["mandatory", "all", "e2-aligned", "mandatory+screening"])
    parser.add_argument("--condition-set", default="default,iter3,iter8")
    parser.add_argument("--case-keys", default="", help="Optional comma-separated subset of case_key values, e.g. path1_cara,path2_lng_ems.")
    parser.add_argument("--run-tag", default=None, help="Optional stable tag embedded into run_id for paired reruns.")
    parser.add_argument("--workers", type=int, default=1, help="Parallel run workers; default 1 to avoid provider rate limits.")
    parser.add_argument("--allow-missing-provider-env", action="store_true", help="Only for dry tests; real PR-E1 evidence requires provider env.")
    parser.add_argument("--append-existing", action="store_true", help="Append newly generated summaries to existing output summary.json.")
    args = parser.parse_args(argv)

    conditions = parse_csv_selection(args.condition_set, allowed=condition_specs().keys(), kind="condition")
    case_keys = parse_csv_selection(args.case_keys, allowed=[case.case_key for case in pr_e1_cases(args.case_set)], kind="case_key") if args.case_keys else None
    previous = load_existing_summaries(args.output_dir) if args.append_existing else []
    new_summaries = run_pr_e1_matrix(
        output_dir=args.output_dir,
        case_set=args.case_set,
        case_keys=case_keys,
        condition_set=conditions,
        require_provider_env=not args.allow_missing_provider_env,
        run_tag=args.run_tag,
        workers=args.workers,
    )
    if previous:
        write_matrix_summary([*previous, *new_summaries], args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
