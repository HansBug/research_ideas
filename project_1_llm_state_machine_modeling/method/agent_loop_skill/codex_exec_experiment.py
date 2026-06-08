"""Utilities for PR-M3 codex-exec skill experiment harness.

This module intentionally lives inside ``agent_loop_skill`` because PR-M3 lets
this skill path own the codex/CC experiment contract, prompt template, redaction
policy, and audit/report artifact shape.  Thin external runners may import these
helpers, but modeling semantics must remain in the skill/prompt used by the
mature agent rather than in the runner.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Mapping, Sequence

SKILL_ROOT = Path(__file__).resolve().parent
METHOD_ROOT = SKILL_ROOT.parent
PROJECT_ROOT = METHOD_ROOT.parent
REPO_ROOT = PROJECT_ROOT.parent

TRACKED_DEFAULT_CODEX_EXEC_CONFIG = "model_provider=airouter"
CODEX_EXEC_ENV_KEYS = (
    "CODEX_EXEC_DEFAULT_CONFIG",
    "CODEX_EXEC_EXTRA_CONFIG",
    "CODEX_EXEC_OVERRIDE_CONFIG",
)
COMMON_SECRET_KEY_HINTS = ("KEY", "TOKEN", "SECRET", "PASSWORD", "ENDPOINT")
SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("bearer_token", re.compile(r"Bearer\s+[A-Za-z0-9._~+\-/]{12,}=*", re.IGNORECASE)),
    ("sk_like_token", re.compile(r"\bsk-[A-Za-z0-9_\-]{12,}\b")),
    ("openai_project_key", re.compile(r"\bsk-proj-[A-Za-z0-9_\-]{12,}\b")),
)
FORBIDDEN_RUNNER_TERMS = (
    "method.loop.run_agent_loop",
    "run_agent_loop(",
    "method.pr_e1_real_runs",
    "method.pr_d_representative",
    "real_run_matrix.py --run",
)
REQUIRED_SKILL_DOCS = (
    "SKILL.md",
    "e2e_ref_model_guide.md",
    "tools.md",
    "prompts.md",
    "nfrr_evaluation_guide.md",
    "codex_exec_experiment_guide.md",
)

M3_AGENT_ARTIFACTS = (
    "final_model.fcstm",
    "report.md",
    "metadata.json",
    "actual_file_reads.json",
    "tool_stage_check_ledger.json",
    "repair_ledger.json",
    "nfrr_report.json",
    "run_summary.md",
)


@dataclass(frozen=True)
class CodexConfigEntry:
    key: str
    value: str
    source: str

    @property
    def cli_arg(self) -> str:
        return f"{self.key}={self.value}"



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

PATH1_CARA_NL = """At run time, CARA coordinates the Caregiver Interface, Blood Pressure Monitor, Algorithm, and Pump Monitors around an infusion pump that moves fluid into the patient, while sensor readings are stored in a shared buffer for software access. The pump has manual and autocontrol modes. In manual mode, pump speed is set with the built-in switch and the caregiver sets a default flow rate directly on the pump for manual operation, while in autocontrol mode pump speed is set by a control voltage from an external source. The Algorithm component controls infusion rate and records infusion-related data in log files; patient blood pressure is used to compute the infusion rate, with higher pressure producing a lower flow rate. The Caregiver Interface lets the caregiver modify target blood pressure and initiate or terminate algorithmic pump control, and it also displays and sounds error messages. In the Mode_Control_Algorithm hierarchy, CARA has manual and autocontrol-related mode-control states plus an Ask_StartAC submode; within Ask_StartAC, the setpoint can be changed and pressing StartAC enters AutocontrolInit. During normal autocontrol, CARA controls flow rate only while there are no pump-operation complications. If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals, the caregiver removes the fault, and when CARA was controlling the pump the software releases control. As a cross-component fallback, CA_backManual or any of CB_backManual, CP_backManual, or CC_backManual causes CA_mode to become Manual, making manual operation the shared recovery target."""

PATH1_CARA_NL_ZH = """运行时，CARA 围绕一台向患者输液的输液泵协调 Caregiver Interface、Blood Pressure Monitor、Algorithm 与 Pump Monitors，传感器读数会写入共享缓冲区供软件访问。泵具有手动和自动控制两种模式。手动模式下，泵速由内置开关设置，护理人员直接在泵上设置默认流量；自动控制模式下，泵速由外部控制电压设置。Algorithm 组件控制输液速率并记录输液相关日志；患者血压用于计算输液速率，血压越高流量越低。Caregiver Interface 允许护理人员修改目标血压，并启动或终止算法泵控制，同时显示和发出错误消息。在 Mode_Control_Algorithm 层次中，CARA 具有手动与自动控制相关的模式控制状态以及 Ask_StartAC 子模式；在 Ask_StartAC 中可以修改设定点，按下 StartAC 会进入 AutocontrolInit。正常自动控制期间，只有没有泵操作并发症时 CARA 才控制流量。如果出现输液管堵塞等泵故障，泵会激活报警信号，护理人员排除故障；当 CARA 正在控制泵时，软件会释放控制。作为跨组件回退，CA_backManual 或 CB_backManual、CP_backManual、CC_backManual 中任一事件都会使 CA_mode 变为 Manual，使手动操作成为共享恢复目标。"""

PATH2_LNG_EMS_NL = """The LNG-ship EMS manages a ship energy system with PVs, WECs, DGs, LNG, batteries, and time-varying ship loads, issuing cut-in and cut-out commands for generating units and loads. It controls power dispatch between generating units and load demand during changing time periods and operating conditions, dynamically switching states to maintain power balance as resources and demands vary. The FSM reads load demand PL, renewable contributions Ppv and Pw, battery state of charge SoC, and engine capacity bounds such as eng3_Pmax, then returns requested generator power, battery discharge or charging power, and spare power. The twelve finite states are selected by logical transition conditions over demand, generation, capacity, and SoC. When Ppv + Pw covers PL, the EMS serves all ship demand from RES and charges batteries while SoC is below 0.95, or treats residual renewable power as spare once SoC is at least 0.95. When Ppv + Pw is below PL, dispatch follows the stated priority: RES first, batteries when SoC is suitable, LNG before diesel units, and DG1/DG2 only as the last priority. Low-SoC branches add explicit charging margins, including Pgmax/5 in an LNG-covered case and Pd1max/10 in later diesel-generator cases. When PL = 0, RES production is sent to battery charging or to spare power according to SoC thresholds. The overload completion state is illegal: if extreme demand exceeds all RES and thermal resources, EMS activates all thermal generating units, covers the lack by battery discharge, and the state shall never occur in practice."""

PATH2_LNG_EMS_NL_ZH = """LNG 船 EMS 管理一个包含光伏、波浪能、柴油机、LNG、电池和随时间变化船舶负载的船舶能源系统，并向发电单元与负载发出切入/切出命令。它在变化的时段和运行条件下控制发电单元与负载需求之间的功率调度，随着资源和需求变化动态切换状态以保持功率平衡。FSM 读取负载需求 PL、可再生贡献 Ppv 和 Pw、电池荷电状态 SoC，以及 eng3_Pmax 等发动机容量边界，然后返回请求的发电机功率、电池放电或充电功率以及备用功率。十二个有限状态由需求、发电、容量和 SoC 上的逻辑转移条件选择。当 Ppv + Pw 覆盖 PL 时，EMS 用 RES 满足全部船舶需求，并在 SoC 低于 0.95 时给电池充电，或在 SoC 至少为 0.95 时把剩余可再生功率视为备用功率。当 Ppv + Pw 低于 PL 时，调度遵循优先级：RES 优先，SoC 合适时使用电池，LNG 先于柴油机，DG1/DG2 只作为最后优先级。低 SoC 分支加入明确充电裕量，包括 LNG 覆盖场景中的 Pgmax/5，以及后续柴油发电机场景中的 Pd1max/10。当 PL = 0 时，RES 产出根据 SoC 阈值送往电池充电或备用功率。过载完成状态是非法状态：若极端需求超过全部 RES 与热力资源，EMS 会激活全部热发电单元并用电池放电弥补缺口，该状态实践中不应发生。"""


@dataclass(frozen=True)
class CodexExecCase:
    case_key: str
    path: str
    case_id: str
    title: str
    nl: str
    nl_zh: str
    source_url: str
    source_path: str | None
    paper_path: str | None
    selection_rationale: str = ""
    variable_participation_note: str = ""
    state_mode_participation_note: str = ""




def codex_exec_cases(case_set: str = "all", case_keys: Sequence[str] | None = None) -> list[CodexExecCase]:
    """Return the four PR-M3 codex-exec evaluation cases without importing E1 runtime."""

    cases = [
        CodexExecCase(
            case_key="path1_abs",
            path="path1",
            case_id="abs-fsm-brake-control",
            title="Path1 ABS three-state brake supervisor",
            nl=PATH1_ABS_NL,
            nl_zh=PATH1_ABS_NL_ZH,
            source_url="project_1_llm_state_machine_modeling/eval/data/sources/abs-fsm-brake-control/nl.md",
            source_path="project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control",
            paper_path="project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control/paper.pdf",
            selection_rationale="三态、guard、state action 均明确，适合检验 parse/semantic/design/sim 是否能走到后段。",
            variable_participation_note="`slp` 是外部/plant 输入型 guard 变量；`k1/k2/n` 是状态动作输出。",
            state_mode_participation_note="三态本身承担阈值区间模式，状态进入动作决定阀/泵输出。",
        ),
        CodexExecCase(
            case_key="path1_elevator",
            path="path1",
            case_id="automatic-elevator-controller",
            title="Path1 automatic elevator controller",
            nl=PATH1_ELEVATOR_NL,
            nl_zh=PATH1_ELEVATOR_NL_ZH,
            source_url="project_1_llm_state_machine_modeling/eval/data/sources/automatic-elevator-controller/nl.md",
            source_path="project_1_llm_state_machine_modeling/sources/automatic-elevator-controller",
            paper_path="project_1_llm_state_machine_modeling/sources/automatic-elevator-controller/paper.pdf",
            selection_rationale="楼层态、运动态、请求事件、到位传感事件与 reset 都明确，适合检验事件建模和 forced fallback。",
            variable_participation_note="`PS*`/`S*`/`reset` 更适合按事件建模；`hbrg` 是纯输出动作。",
            state_mode_participation_note="楼层态和运动态直接承担 mode memory；请求/到位事件驱动状态迁移。",
        ),
        CodexExecCase(
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
            variable_participation_note="变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强。",
            state_mode_participation_note="Manual/Ask_StartAC/Autocontrol/PumpFault 状态承担模式记忆与故障恢复语义。",
        ),
        CodexExecCase(
            case_key="path2_lng_ems",
            path="path2",
            case_id="state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship",
            title="Path2 LNG-ship EMS representative NL",
            nl=PATH2_LNG_EMS_NL,
            nl_zh=PATH2_LNG_EMS_NL_ZH,
            source_url="https://github.com/HansBug/research_ideas/issues/14#issuecomment-4598890799",
            source_path="project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship",
            paper_path="project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/paper.pdf",
            selection_rationale="Path2 EFSM 压力样本，变量、guard、12 个状态和非法状态明确；是否可作 Path2 主蓝本取决于 state-dependent mode memory。",
            variable_participation_note="`PL/Ppv/Pw/SoC/eng*_Pmax` 是环境输入/容量边界。",
            state_mode_participation_note="原 NL 的 12 状态主要由瞬时需求/容量条件选择；需防止 state_mode_decorative。",
        ),
    ]
    if case_set == "mandatory":
        selected = [case for case in cases if case.case_key in {"path1_cara", "path2_lng_ems"}]
    elif case_set in {"all", "e2-aligned", "mandatory+screening"}:
        selected = cases
    else:
        raise ValueError("unknown case-set {!r}; allowed: mandatory, all, e2-aligned, mandatory+screening".format(case_set))
    if case_keys:
        allowed = {case.case_key for case in cases}
        unknown = [key for key in case_keys if key not in allowed]
        if unknown:
            raise ValueError("unknown case key(s): {}; allowed: {}".format(", ".join(unknown), ", ".join(sorted(allowed))))
        selected = [case for case in selected if case.case_key in set(case_keys)]
    return selected


@dataclass(frozen=True)
class CodexExecCommandPlan:
    command: list[str]
    command_redacted: list[str]
    config_entries: list[CodexConfigEntry]
    resolved_config: dict[str, str]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def relpath(path: Path, root: Path = REPO_ROOT) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_env_file(path: Path | None) -> dict[str, str]:
    """Parse a simple dotenv file without emitting raw values."""

    if path is None or not path.is_file():
        return {}
    env: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
            value = value[1:-1]
        env[key] = value
    return env


def _split_config_blob(blob: str | None) -> list[str]:
    if not blob:
        return []
    normalized = blob.replace("\n", " ").replace(",", " ").replace(";", " ")
    return [part for part in shlex.split(normalized) if part]


def _parse_config_entries(parts: Iterable[str], source: str) -> list[CodexConfigEntry]:
    entries: list[CodexConfigEntry] = []
    for part in parts:
        if "=" not in part:
            raise ValueError(f"invalid codex config entry {part!r}; expected key=value")
        key, value = part.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"invalid codex config entry {part!r}; empty key")
        entries.append(CodexConfigEntry(key=key, value=value.strip(), source=source))
    return entries


def resolve_codex_exec_config(
    *,
    file_env: Mapping[str, str] | None = None,
    process_env: Mapping[str, str] | None = None,
    cli_default_config: str | None = None,
    cli_extra_config: Sequence[str] = (),
    cli_override_config: Sequence[str] = (),
) -> list[CodexConfigEntry]:
    """Resolve ``codex exec -c`` entries with PR-M3 precedence.

    Precedence is tracked default -> loaded ``.env`` -> process env -> CLI
    default override -> extra -> override.  Duplicate keys are collapsed so that
    the final command and manifest expose the exact effective config.
    """

    file_env = file_env or {}
    process_env = process_env or os.environ
    entries: list[CodexConfigEntry] = _parse_config_entries(
        _split_config_blob(TRACKED_DEFAULT_CODEX_EXEC_CONFIG), "tracked-default"
    )
    if file_env.get("CODEX_EXEC_DEFAULT_CONFIG"):
        entries.extend(_parse_config_entries(_split_config_blob(file_env.get("CODEX_EXEC_DEFAULT_CONFIG")), ".env:CODEX_EXEC_DEFAULT_CONFIG"))
    if process_env.get("CODEX_EXEC_DEFAULT_CONFIG"):
        entries.extend(_parse_config_entries(_split_config_blob(process_env.get("CODEX_EXEC_DEFAULT_CONFIG")), "env:CODEX_EXEC_DEFAULT_CONFIG"))
    if cli_default_config:
        entries.extend(_parse_config_entries(_split_config_blob(cli_default_config), "cli:--codex-config"))

    for src, env_map, key in [
        (".env:CODEX_EXEC_EXTRA_CONFIG", file_env, "CODEX_EXEC_EXTRA_CONFIG"),
        ("env:CODEX_EXEC_EXTRA_CONFIG", process_env, "CODEX_EXEC_EXTRA_CONFIG"),
    ]:
        entries.extend(_parse_config_entries(_split_config_blob(env_map.get(key)), src))
    for item in cli_extra_config:
        entries.extend(_parse_config_entries(_split_config_blob(item), "cli:--codex-extra-config"))

    for src, env_map, key in [
        (".env:CODEX_EXEC_OVERRIDE_CONFIG", file_env, "CODEX_EXEC_OVERRIDE_CONFIG"),
        ("env:CODEX_EXEC_OVERRIDE_CONFIG", process_env, "CODEX_EXEC_OVERRIDE_CONFIG"),
    ]:
        entries.extend(_parse_config_entries(_split_config_blob(env_map.get(key)), src))
    for item in cli_override_config:
        entries.extend(_parse_config_entries(_split_config_blob(item), "cli:--codex-override-config"))

    collapsed: dict[str, CodexConfigEntry] = {}
    for entry in entries:
        collapsed[entry.key] = entry
    return list(collapsed.values())


def redact_value_for_key(key: str, value: str) -> str:
    upper = key.upper()
    if any(hint in upper for hint in COMMON_SECRET_KEY_HINTS):
        if key.startswith("CODEX_EXEC_"):
            return value
        if key in {"LLM_MODEL", "CODEX_BIN"}:
            return value
        return "<REDACTED>"
    return value


def secret_values_from_env(env: Mapping[str, str]) -> dict[str, str]:
    secrets: dict[str, str] = {}
    for key, value in env.items():
        if not value or len(value) < 6:
            continue
        upper = key.upper()
        if any(hint in upper for hint in COMMON_SECRET_KEY_HINTS) or value.startswith("sk-"):
            secrets[key] = value
    return secrets


def redact_text(text: str, secret_values: Mapping[str, str] | None = None) -> str:
    redacted = text
    for key, value in sorted((secret_values or {}).items(), key=lambda item: len(item[1]), reverse=True):
        if value:
            redacted = redacted.replace(value, f"<REDACTED:{key}>")
    for name, pattern in SECRET_PATTERNS:
        redacted = pattern.sub(f"<REDACTED:{name}>", redacted)
    return redacted


def redacted_env_snapshot(env: Mapping[str, str], file_env_keys: Iterable[str] = ()) -> dict[str, object]:
    interesting_prefixes = ("CODEX_EXEC_", "LLM_", "OPENAI_", "ANTHROPIC_", "CODEX_")
    payload: dict[str, object] = {
        "file_env_keys_loaded": sorted(set(file_env_keys)),
        "values": {},
    }
    values: dict[str, str] = {}
    for key in sorted(env):
        if key.startswith(interesting_prefixes):
            values[key] = redact_value_for_key(key, env[key])
    payload["values"] = values
    return payload


def skill_doc_hashes() -> dict[str, str | None]:
    return {name: sha256_file(SKILL_ROOT / name) for name in REQUIRED_SKILL_DOCS}


def existing_material_files(source_path: str | None) -> list[str]:
    if not source_path:
        return []
    base = REPO_ROOT / source_path
    candidates = ["bibtex.bib", "STM.md", "DESC.md", "desc.md", "paper_content.txt", "paper.pdf"]
    return [relpath(base / name) for name in candidates if (base / name).exists()]


def build_codex_prompt(case: CodexExecCase, run_dir: Path, run_label: str) -> str:
    paper_dir = case.source_path or "<none>"
    material_files = existing_material_files(case.source_path)
    material_bullets = "\n".join(f"- `{item}`" for item in material_files) or "- <none detected>"
    return f"""你是 PR-M3 的 codex exec skill 标准实验入口 runner。你的目标不是调用现成顶层 agent-loop，而是像成熟 coding agent 一样读取 repo-local skill/toolbox，自主完成 NL(+paper_dir) -> FCSTM 候选、检查、修复、NFRR 与完整审计报告。

# 硬性边界

1. 必须读取并遵循 repo-local skill 入口：`project_1_llm_state_machine_modeling/method/agent_loop_skill/SKILL.md`（若 symlink 异常则读 `AGENT_LOOP_SKILL.md`）。
2. 必须读取：`e2e_ref_model_guide.md`、`tools.md`、`prompts.md`、`nfrr_evaluation_guide.md`、`codex_exec_experiment_guide.md`。
3. 禁止调用 `method.loop.run_agent_loop(...)`、PR-D representative runner、PR-E1 real-run runner 或任何一键 full staged runner；也不要用它们间接生成模型。
4. 允许使用 `method.stages.api` / `method.stages.sc_control` / `method.stages.sl_prompt_api` / SD deterministic tools / SL prompt generators / pyfcstm utilities / 仓库搜索与论文材料阅读。
5. 不得针对 ABS / CARA / Elevator / LNG 写 lexical special-case；所有 waiver、修复和上下文策略必须是可迁移规则。
6. 不要输出、写入或回显 raw API key、raw endpoint、Bearer token 或 `.env` secret。
7. 若 provider/network/CLI 故障导致无法完成，必须标记 invalid-run，不要伪造模型产物。

# 输出目录

请把所有产物写入：`{relpath(run_dir)}`

必须至少生成以下文件（缺一项都要在 report 中解释）：

```text
final_model.fcstm
report.md
metadata.json
actual_file_reads.json
tool_stage_check_ledger.json
repair_ledger.json
nfrr_report.json
forbidden_call_check.json
run_summary.md
```

`report.md` 必须中文为主、人类友好，不能只贴 final FCSTM；至少包含：输入 NL/NL_zh、实际读取文件、过程摘要表、检查/修复/NFRR 表、final FCSTM、质量风险和限制、是否可进入 reviewer queue。

`metadata.json` 必须是 JSON，至少包含：case_key、case_id、path、status、model_provider_config_seen、skill_entry_read、actual_file_reads、output_files、forbidden_runner_used=false、checks、nfrr、final_model_sha256、report_sha256。

# 建议执行流程

| 阶段 | 要求 |
|---|---|
| E0 skill discovery | 读取上述 skill docs，记录实际读取路径。 |
| E1 evidence grounding | 先从 NL 抽取 obligations，再读 paper_dir 中的 bibtex/STM/DESC/paper_content，记录 source span / synthetic abstraction。 |
| E2 initial modeling | 生成 pyfcstm/FCSTM DSL；parser 以当前 SD-2 为准，布尔语义用 int 0/1。 |
| E3 deterministic checks | 至少尝试 SD-2、SD-3、SD-4、SD-5A/SC-5F、SD-6；工具不可用也要记录命令和影响。 |
| E4 repair/waiver | 对 blocking 问题形成 FixRequestBatch/FixLog 风格 ledger，记录 request、accept/reject/waiver、diff、local evidence、SL-10式判断。 |
| E5 NFRR | 按 NFRR v3 输出 claim、NL coverage ledger、obligation ledger、scenario provenance ledger、waiver ledger、FE/NGF/REC/GAS/SCB/AAT/BVS/DMR、tier/cap/allowed_use。 |
| E6 final audit | 写 `report.md`、`metadata.json`、`run_summary.md`，检查 forbidden runner 和 secret redaction 风险。 |

# Case metadata

- run_label: `{run_label}`
- case_key: `{case.case_key}`
- path: `{case.path}`
- case_id: `{case.case_id}`
- title: `{case.title}`
- NL source: `{case.source_url}`
- paper_dir: `{paper_dir}`
- detected material files:
{material_bullets}
- selection rationale: {case.selection_rationale}
- variable participation note: {case.variable_participation_note}
- state/mode participation note: {case.state_mode_participation_note}

# NL 原文

```text
{case.nl}
```

# NL 中文翻译/释义

```text
{case.nl_zh}
```

请现在执行 PR-M3 codex exec skill 实验，并在最终回答中只给出：output_dir、status、final_model 路径、report 路径、metadata 路径、主要限制。
"""


def build_command_plan(
    *,
    codex_bin: str,
    repo_root: Path,
    last_message_path: Path,
    config_entries: Sequence[CodexConfigEntry],
) -> CodexExecCommandPlan:
    command = [
        codex_bin,
        "exec",
        "--json",
        "-C",
        str(repo_root),
        "--dangerously-bypass-approvals-and-sandbox",
        "--dangerously-bypass-hook-trust",
        "-o",
        str(last_message_path),
    ]
    for entry in config_entries:
        command.extend(["-c", entry.cli_arg])
    command.append("-")

    redacted_entries = [
        CodexConfigEntry(entry.key, redact_value_for_key(entry.key, entry.value), entry.source) for entry in config_entries
    ]
    command_redacted = [
        codex_bin,
        "exec",
        "--json",
        "-C",
        str(repo_root),
        "--dangerously-bypass-approvals-and-sandbox",
        "--dangerously-bypass-hook-trust",
        "-o",
        relpath(last_message_path),
    ]
    for entry in redacted_entries:
        command_redacted.extend(["-c", entry.cli_arg])
    command_redacted.append("-")
    return CodexExecCommandPlan(
        command=command,
        command_redacted=command_redacted,
        config_entries=list(config_entries),
        resolved_config={entry.key: entry.value for entry in config_entries},
    )


def git_metadata(repo_root: Path = REPO_ROOT) -> dict[str, object]:
    def _run(args: list[str]) -> str | None:
        try:
            return subprocess.check_output(args, cwd=repo_root, text=True, stderr=subprocess.DEVNULL).strip()
        except Exception:
            return None

    status = _run(["git", "status", "--short"])
    return {
        "branch": _run(["git", "rev-parse", "--abbrev-ref", "HEAD"]),
        "commit": _run(["git", "rev-parse", "HEAD"]),
        "dirty": bool(status),
        "status_short": status,
    }


def initial_manifest(
    *,
    case: CodexExecCase,
    run_dir: Path,
    command_plan: CodexExecCommandPlan,
    prompt: str,
    file_env_keys: Iterable[str],
) -> dict[str, object]:
    return {
        "schema_version": "pr-m3-codex-exec-skill-run-v1",
        "status": "started",
        "started_at": utc_now_iso(),
        "ended_at": None,
        "duration_seconds": None,
        "exit_code": None,
        "invalid_run_reason": None,
        "case": asdict(case),
        "run_dir": relpath(run_dir),
        "input_hashes": {
            "nl_sha256": sha256_text(case.nl),
            "nl_zh_sha256": sha256_text(case.nl_zh),
            "paper_pdf_sha256": sha256_file(REPO_ROOT / case.paper_path) if case.paper_path else None,
        },
        "material_files_detected": existing_material_files(case.source_path),
        "skill_doc_hashes": skill_doc_hashes(),
        "prompt_sha256": sha256_text(prompt),
        "command_redacted": command_plan.command_redacted,
        "resolved_config_redacted": {
            key: redact_value_for_key(key, value) for key, value in command_plan.resolved_config.items()
        },
        "config_sources": [asdict(entry) | {"value": redact_value_for_key(entry.key, entry.value)} for entry in command_plan.config_entries],
        "file_env_keys_loaded": sorted(set(file_env_keys)),
        "git": git_metadata(),
        "forbidden_runner_terms": list(FORBIDDEN_RUNNER_TERMS),
        "artifact_hashes": {},
        "redaction_status": "not_run",
    }


def update_manifest_after_run(
    manifest: dict[str, object], *, run_dir: Path, started_monotonic: float, exit_code: int, invalid_reason: str | None) -> dict[str, object]:
    import time

    manifest = dict(manifest)
    manifest["status"] = "invalid" if invalid_reason else ("completed" if exit_code == 0 else "failed")
    manifest["ended_at"] = utc_now_iso()
    manifest["duration_seconds"] = round(time.monotonic() - started_monotonic, 3)
    manifest["exit_code"] = exit_code
    manifest["invalid_run_reason"] = invalid_reason
    hashes: dict[str, str] = {}
    for path in sorted(run_dir.rglob("*")):
        if path.is_file():
            digest = sha256_file(path)
            if digest:
                hashes[relpath(path)] = digest
    manifest["artifact_hashes"] = hashes
    manifest["git_after"] = git_metadata()
    return manifest


def write_invalid_placeholders(run_dir: Path, *, reason: str) -> None:
    final_model = run_dir / "final_model.fcstm"
    if not final_model.exists():
        final_model.write_text("", encoding="utf-8")
    report = run_dir / "report.md"
    if not report.exists():
        report.write_text(
            "# PR-M3 codex exec run report\n\n"
            f"- status: `invalid-run`\n- reason: `{reason}`\n\n"
            "本文件由 runner 生成作为 invalid-run 占位；没有伪造模型产物。\n",
            encoding="utf-8",
        )
    metadata = run_dir / "metadata.json"
    if not metadata.exists():
        write_json(
            metadata,
            {
                "status": "invalid-run",
                "invalid_run_reason": reason,
                "forbidden_runner_used": None,
                "output_files": [relpath(final_model), relpath(report), relpath(metadata)],
            },
        )




def load_json_file(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {"value": data}
    except Exception as exc:
        return {"parse_error": repr(exc)}


def ensure_machine_audit_artifacts(run_dir: Path, manifest: Mapping[str, object]) -> dict[str, object]:
    """Create best-effort machine-audit ledgers if the mature agent omitted them.

    These files do not invent hidden reasoning.  They either preserve the
    producer-supplied JSON or record a harness-derived/``not_reported`` ledger so
    that reviewers can distinguish missing evidence from a silent pass.
    """

    metadata = load_json_file(run_dir / "metadata.json")
    generated_by_harness: list[str] = []

    def _write_if_missing(name: str, payload: dict[str, object]) -> None:
        path = run_dir / name
        if not path.exists():
            write_json(path, payload)
            generated_by_harness.append(name)

    case = manifest.get("case", {}) if isinstance(manifest.get("case"), dict) else {}
    material_files = manifest.get("material_files_detected") if isinstance(manifest.get("material_files_detected"), list) else []
    actual_reads = (
        metadata.get("actual_file_reads")
        or metadata.get("case_materials_read")
        or metadata.get("skill_documents_read")
        or metadata.get("required_docs_read")
    )
    _write_if_missing(
        "actual_file_reads.json",
        {
            "schema_version": "pr-m3-actual-file-reads-v1",
            "source": "harness_derived_from_metadata_or_prompt" if actual_reads else "harness_expected_not_confirmed",
            "skill_docs_required": list(REQUIRED_SKILL_DOCS),
            "producer_reported_reads": actual_reads or [],
            "material_files_detected": material_files,
            "paper_dir": case.get("source_path"),
            "audit_note": "Codex hidden reasoning is not reconstructed; this ledger records externally reported reads or expected inputs.",
        },
    )

    checks = metadata.get("checks") or metadata.get("deterministic_checks") or {}
    _write_if_missing(
        "tool_stage_check_ledger.json",
        {
            "schema_version": "pr-m3-tool-stage-check-ledger-v1",
            "source": "harness_derived_from_metadata" if checks else "not_reported_by_agent",
            "checks": checks,
            "required_minimum": ["SD-2", "SD-3", "SD-4", "SD-5A/SC-5F", "SD-6"],
            "audit_note": "If checks are empty, reviewers should treat this as evidence incompleteness, not as pass.",
        },
    )

    repair = metadata.get("repair_ledger") or metadata.get("fix_log") or metadata.get("repair") or []
    _write_if_missing(
        "repair_ledger.json",
        {
            "schema_version": "pr-m3-repair-ledger-v1",
            "source": "harness_derived_from_metadata" if repair else "not_reported_or_no_repair",
            "repair_ledger": repair,
            "required_fields": ["fix_request", "decision", "diff", "local_evidence", "sl10_style_review", "next_action"],
        },
    )

    nfrr = metadata.get("nfrr") or metadata.get("nfrr_report") or {}
    _write_if_missing(
        "nfrr_report.json",
        {
            "schema_version": "pr-m3-nfrr-report-v1",
            "source": "harness_derived_from_metadata" if nfrr else "not_reported_by_agent",
            "nfrr": nfrr,
            "required_snapshot": ["claim", "vector", "tier", "cap_reasons", "allowed_use"],
        },
    )

    completeness = {
        "schema_version": "pr-m3-artifact-completeness-v1",
        "required_agent_artifacts": list(M3_AGENT_ARTIFACTS),
        "present": {name: (run_dir / name).exists() for name in M3_AGENT_ARTIFACTS},
        "generated_by_harness": generated_by_harness,
    }
    write_json(run_dir / "checks" / "artifact_completeness.json", completeness)
    return completeness


def augment_metadata(run_dir: Path, manifest: Mapping[str, object]) -> None:
    metadata_path = run_dir / "metadata.json"
    payload: dict[str, object] = {}
    if metadata_path.exists():
        try:
            payload = json.loads(metadata_path.read_text(encoding="utf-8"))
        except Exception as exc:
            payload = {"metadata_parse_error": repr(exc)}
    payload.setdefault("status", manifest.get("status"))
    payload.setdefault("output_dir", relpath(run_dir))
    payload["runner_observed"] = {
        "schema_version": manifest.get("schema_version"),
        "exit_code": manifest.get("exit_code"),
        "invalid_run_reason": manifest.get("invalid_run_reason"),
        "duration_seconds": manifest.get("duration_seconds"),
        "resolved_config_redacted": manifest.get("resolved_config_redacted"),
        "run_manifest": relpath(run_dir / "run_manifest.json"),
    }
    payload.setdefault("final_model_sha256", sha256_file(run_dir / "final_model.fcstm"))
    payload.setdefault("report_sha256", sha256_file(run_dir / "report.md"))
    write_json(metadata_path, payload)


def write_forbidden_call_check(run_dir: Path) -> dict[str, object]:
    """Best-effort external-observable forbidden-call audit.

    We inspect command/tool-event looking lines, not the original prompt, because
    the prompt must mention the banned APIs as negative constraints.
    """

    event_file = run_dir / "codex_events.jsonl"
    stderr_file = run_dir / "codex_stderr.log"
    suspicious: list[str] = []
    tool_markers = ("exec", "tool_call", "command", "cmd", "/bin/bash", "python", "pytest")
    for file in [event_file, stderr_file]:
        if not file.exists():
            continue
        for idx, line in enumerate(file.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
            lower = line.lower()
            # The initial user prompt must mention forbidden APIs as negative
            # constraints.  Only command/tool-event shaped lines are evidence
            # for actual forbidden use, so prompt/user-message payloads are
            # excluded from this best-effort scan.
            if '"type":"user"' in lower or '"type":"user_message"' in lower or '"role":"user"' in lower:
                continue
            if not any(marker in lower for marker in tool_markers):
                continue
            if any(term in line for term in FORBIDDEN_RUNNER_TERMS):
                suspicious.append(f"{relpath(file)}:L{idx}:{line[:500]}")
    payload = {
        "forbidden_runner_used": bool(suspicious),
        "forbidden_terms": list(FORBIDDEN_RUNNER_TERMS),
        "suspicious_tool_lines": suspicious[:50],
        "scope_note": "Prompt/user-message mentions are excluded; this is an external tool-event scan.",
    }
    write_json(run_dir / "forbidden_call_check.json", payload)
    return payload


def write_transcript_redacted(run_dir: Path, secret_values: Mapping[str, str]) -> None:
    lines = ["# codex exec transcript (redacted)", ""]
    for name in ["codex_events.jsonl", "codex_stderr.log", "last_message.md"]:
        path = run_dir / name
        if not path.exists():
            continue
        lines.extend([f"## {name}", "", "```text"])
        text = path.read_text(encoding="utf-8", errors="replace")
        # Keep the artifact reviewable while avoiding pathological PR comments.
        if len(text) > 200_000:
            text = text[:200_000] + "\n... <truncated in transcript; see source artifact> ...\n"
        lines.append(redact_text(text, secret_values))
        lines.extend(["```", ""])
    (run_dir / "codex_transcript.redacted.md").write_text("\n".join(lines), encoding="utf-8")


def write_redaction_report(run_dir: Path, secret_values: Mapping[str, str]) -> dict[str, object]:
    leaks: list[dict[str, object]] = []
    pattern_hits: list[dict[str, object]] = []
    for path in sorted(run_dir.rglob("*")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for key, value in secret_values.items():
            if value and value in text:
                leaks.append({"path": relpath(path), "secret_key": key, "count": text.count(value)})
        for name, pattern in SECRET_PATTERNS:
            count = len(pattern.findall(text))
            if count:
                pattern_hits.append({"path": relpath(path), "pattern": name, "count": count})
    payload = {
        "ok": not leaks and not pattern_hits,
        "raw_secret_value_hits": leaks,
        "pattern_hits": pattern_hits,
        "scanned_file_count": sum(1 for path in run_dir.rglob("*") if path.is_file()),
        "policy": "PR-facing artifacts must not contain raw API keys, endpoints, Bearer tokens, or sk-like tokens.",
    }
    write_json(run_dir / "redaction_report.json", payload)
    return payload


def render_run_summary(run_dir: Path, manifest: Mapping[str, object], forbidden_check: Mapping[str, object], redaction_report: Mapping[str, object]) -> str:
    case = manifest.get("case", {}) if isinstance(manifest.get("case"), dict) else {}
    final_model_hash = sha256_file(run_dir / "final_model.fcstm")
    report_hash = sha256_file(run_dir / "report.md")
    metadata_path = run_dir / "metadata.json"
    metadata: dict[str, object] = {}
    if metadata_path.exists():
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except Exception:
            metadata = {}
    nfrr = metadata.get("nfrr", {}) if isinstance(metadata.get("nfrr"), dict) else {}
    checks = metadata.get("checks") or metadata.get("deterministic_checks") or {}
    lines = [
        "# PR-M3 codex exec run summary",
        "",
        f"- case_key: `{case.get('case_key', '<unknown>')}`",
        f"- case_id: `{case.get('case_id', '<unknown>')}`",
        f"- path: `{case.get('path', '<unknown>')}`",
        f"- status: `{manifest.get('status')}`",
        f"- invalid_run_reason: `{manifest.get('invalid_run_reason')}`",
        f"- duration_seconds: `{manifest.get('duration_seconds')}`",
        f"- final_model_sha256: `{final_model_hash}`",
        f"- report_sha256: `{report_hash}`",
        f"- forbidden_runner_used: `{forbidden_check.get('forbidden_runner_used')}`",
        f"- redaction_ok: `{redaction_report.get('ok')}`",
        "",
        "## Artifact paths",
        "",
        f"- manifest: `{relpath(run_dir / 'run_manifest.json')}`",
        f"- report: `{relpath(run_dir / 'report.md')}`",
        f"- final_model: `{relpath(run_dir / 'final_model.fcstm')}`",
        f"- metadata: `{relpath(metadata_path)}`",
        f"- codex_events: `{relpath(run_dir / 'codex_events.jsonl')}`",
        f"- transcript_redacted: `{relpath(run_dir / 'codex_transcript.redacted.md')}`",
        "",
        "## Checks / NFRR snapshot",
        "",
        "```json",
        json.dumps({"checks": checks, "nfrr": nfrr}, ensure_ascii=False, indent=2),
        "```",
        "",
    ]
    return "\n".join(lines)
