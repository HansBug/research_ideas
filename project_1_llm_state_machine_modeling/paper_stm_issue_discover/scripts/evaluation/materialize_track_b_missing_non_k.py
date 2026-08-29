"""Materialize the user-specified blind Track B additions.

The assessment table below is the only source of semantic decisions.  The
script reads only raw method records, the author-source closure, and ledger
items; relation expansion and digest calculation are deterministic.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
ARCHIVE = ROOT / (
    "project_1_llm_state_machine_modeling/paper_stm_issue_discover/"
    "final_results/v60_current_vs_x1v2_baseline"
)
RAW_ROOT = ARCHIVE / "raw/x1v2_baseline/method"
SOURCE_ROOT = ARCHIVE / "reference/x1v2_input_closure/pairs"
LEDGER_PATH = ARCHIVE / "reference/ledger.json"
OUTPUT = ARCHIVE / (
    "derived/manual_adjudication_v3_baseline_ni/proposals/"
    "track_b_0000_0019_missing_non_k.json"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def raw_record(pair: str, round_no: int) -> Path:
    matches = sorted(RAW_ROOT.glob(f"run{round_no}/{pair}-*/record.json"))
    if len(matches) != 1:
        raise RuntimeError(f"expected one raw record for {pair} r{round_no}, got {matches}")
    return matches[0]


def ref(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


# This table is manually authored from the report, NL, PlantUML, and ledger.
# It deliberately contains no inherited labels or reviewer conclusions.
MANUAL: dict[str, dict[str, Any]] = {
    "0000:r1:baseline_issue_2": {
        "pair": "0000", "round": 1, "index": 1,
        "d_tier": "D1", "validity": "VALID_KNOWN", "witness_level": "W1",
        "relations": {"EIS-0000-02": "FULL_MATCH"},
        "source_refs": ["pairs/0000/nl.txt:L1", "pairs/0000/plantuml.puml:L13"],
        "observed_source_fact_status": "SUPPORTED",
        "normative_violation_status": "AMBIGUOUS_READING",
        "defect_claim_status": "AUTHOR_SOURCE_DEFECT",
        "reason": "迁移标签确实把 Human Steering Cmd、Brake Pressed 和 in (AutoFinal) 压成一个自由文本标签，因而未把事件与状态条件分别表示。NL 原句本身没有标明逗号是析取还是合取；按合取读法，前两项可作触发、AutoFinal 可作状态限制，仍与源结构相容。因此事实和缺失的表达问题成立，但其规范违反的具体读法存在存活的第二解释，裁 D1。该缺口与 EIS-0000-02 是同一标签压缩问题。",
        "basis": "作者源 L13 只有一条从 AutonomousMode 到 HumanDrivingMode 的标签边，未出现三条独立边、结构守卫或从 AutoFinal 出发的边；NL L1 同时列出三项且没有逻辑分隔。替代读法不是 reviewer 犹豫，而是把同一标签解释为“转向且刹车且当前 AutoFinal”，与文本和结构均相容，所以不能裁 D2。",
        "alternative_reading": "把 Human Steering Cmd 与 Brake Pressed 读成合取触发，把 in (AutoFinal) 读成状态限制；该读法承认表示不清，但不要求把逗号解释为三个独立触发事件。",
        "relation_basis": {"EIS-0000-02": "同一条 L13 迁移把三项接管条件压为不可分解标签；该 expected 的核心是同一 author-source encoding defect。"},
    },
    "0002:r1:baseline_issue_3": {
        "pair": "0002", "round": 1, "index": 2,
        "d_tier": "D2", "validity": "VALID_KNOWN", "witness_level": "W1",
        "relations": {"EIS-0002-01": "FULL_MATCH", "EIS-0002-02": "FULL_MATCH", "EIS-0002-03": "FULL_MATCH"},
        "source_refs": ["pairs/0002/nl.txt:L2-L5", "pairs/0002/plantuml.puml:L4-L23"],
        "observed_source_fact_status": "SUPPORTED",
        "normative_violation_status": "ESTABLISHED",
        "defect_claim_status": "AUTHOR_SOURCE_DEFECT",
        "reason": "PumpControl 的唯一内部初始边在 L5 指向 InitialState；该名字不在 NL 的三个主子状态枚举中，且 InitialState 没有出边。于是模型既没有把首次落点设为 PumpState，也没有为 WaterState/MethaneState提供可达入口，并额外引入了枚举之外的状态。NL L2-L5 对三个名称和首次 PumpState 义务是明确的，作者源不存在可存活的设计解释，裁 D2。",
        "basis": "逐项对照 NL L2-L5 与 PlantUML L5、L7-L23：PumpState、WaterState、MethaneState均被声明但没有从 PumpControl 的唯一入口或其他边到达；InitialState只在 L5 出现且无后续边。该报告的承重主张同时覆盖错误初始目标、三主态不可达和额外 InitialState，分别与三个 expected 的核心事实重合。",
        "relation_basis": {
            "EIS-0002-01": "L5 的 InitialState 目标直接替代 NL L3 要求的 PumpState 初始落点。",
            "EIS-0002-02": "L7-L23 的三个主态没有任何可达入口，且 L5 的死端入口不能继续到达它们。",
            "EIS-0002-03": "InitialState 在 L5 被隐式引入，不属于 NL L2 明确枚举的三个主子状态。",
        },
    },
    "0002:r2:baseline_issue_1": {
        "pair": "0002", "round": 2, "index": 0,
        "d_tier": "D2", "validity": "VALID_KNOWN", "witness_level": "W1",
        "relations": {"EIS-0002-01": "FULL_MATCH"},
        "source_refs": ["pairs/0002/nl.txt:L3", "pairs/0002/plantuml.puml:L4-L8"],
        "observed_source_fact_status": "SUPPORTED",
        "normative_violation_status": "ESTABLISHED",
        "defect_claim_status": "AUTHOR_SOURCE_DEFECT",
        "reason": "PumpControl 的初始伪状态在 L5 进入 InitialState，而不是 NL L3 明确要求的 PumpState。InitialState 没有后续边，故该初始落点不能被解释为随后立即进入 PumpState。该报告只主张首次目标错误，事实和义务均由作者源直接核对，裁 D2。",
        "basis": "NL L3 给出确定的 first destination；PlantUML L5 给出唯一内部默认目标，L7 才声明 PumpState且没有到达它的边。该报告的最小修复意图是把初始边目标改为 PumpState，与 EIS-0002-01相同。",
        "relation_basis": {"EIS-0002-01": "相同的 L5 初始目标与 NL L3 首次进入 PumpState 义务。"},
    },
    "0019:r2:baseline_issue_4": {
        "pair": "0019", "round": 2, "index": 3,
        "d_tier": "D2", "validity": "VALID_KNOWN", "witness_level": "W1",
        "relations": {"EIS-0019-03": "FULL_MATCH"},
        "source_refs": ["pairs/0019/nl.txt:L7-L10", "pairs/0019/plantuml.puml:L23-L35"],
        "observed_source_fact_status": "SUPPORTED",
        "normative_violation_status": "ESTABLISHED",
        "defect_claim_status": "AUTHOR_SOURCE_DEFECT",
        "reason": "UrbanMode 的 exit_urban 目标边在 L30 之后，然而 exit_urban 没有写在 UrbanMode 块内；其到 FinishState 的边在 L35 也位于块外。NL L8 把 exit_urban 定义为 UrbanMode 的子状态，NL L10 又要求 UrbanMode 按 auto_finished=true 结束。作者源的作用域和完成路径均不满足该层级语义，裁 D2。",
        "basis": "PlantUML L23-L34 明确界定 UrbanMode 块，L30 的目标首次在该块内出现，L35 的完成边在块外；不存在把 exit_urban声明为 UrbanMode内部子态的显式结构。该层级错误与 EIS-0019-03 的模式完成源被收窄到出口态属于同一完成路径缺陷。",
        "relation_basis": {"EIS-0019-03": "UrbanMode 完成相关的出口态和 FinishState 边被放在模式外，导致 NL L10 的模式级完成语义被收窄/错层。"},
    },
    "0002:r3:baseline_issue_1": {
        "pair": "0002", "round": 3, "index": 0,
        "d_tier": "D2", "validity": "VALID_KNOWN", "witness_level": "W1",
        "relations": {"EIS-0002-01": "FULL_MATCH", "EIS-0002-02": "FULL_MATCH"},
        "source_refs": ["pairs/0002/nl.txt:L2-L5", "pairs/0002/plantuml.puml:L4-L23"],
        "observed_source_fact_status": "SUPPORTED",
        "normative_violation_status": "ESTABLISHED",
        "defect_claim_status": "AUTHOR_SOURCE_DEFECT",
        "reason": "作者源只有 PumpControl L5 的 InitialState 初始目标；L7-L23 的三个 NL 点名主态没有任何外部入口或从 InitialState 出发的边。故模型不能从 PumpControl 选择三个主态，也不能保证首先进入 PumpState。NL L2-L5 的可达性和首次进入要求均为明确义务，裁 D2。",
        "basis": "对作者源完整块体逐行检查：PumpState/WaterState/MethaneState分别在 L7、L14、L21声明，但唯一 PumpControl 初始边在 L5，InitialState没有出边。该报告的“全部三个主态不可达”与 EIS-0002-02同一事实，“未首先到 PumpState”与 EIS-0002-01同一事实。",
        "relation_basis": {
            "EIS-0002-01": "L5 的初始目标不是 NL L3 指定的 PumpState。",
            "EIS-0002-02": "L7、L14、L21 三个主态都没有可达入口，符合 NL L2-L5 的缺失可达性。",
        },
    },
    "0002:r3:baseline_issue_2": {
        "pair": "0002", "round": 3, "index": 1,
        "d_tier": "D2", "validity": "VALID_KNOWN", "witness_level": "W1",
        "relations": {"EIS-0002-01": "FULL_MATCH"},
        "source_refs": ["pairs/0002/nl.txt:L3", "pairs/0002/plantuml.puml:L5-L8"],
        "observed_source_fact_status": "SUPPORTED",
        "normative_violation_status": "ESTABLISHED",
        "defect_claim_status": "AUTHOR_SOURCE_DEFECT",
        "reason": "PumpControl 的 L5 初始目标是 InitialState，不是 NL L3 要求的 PumpState；InitialState没有后续出边。因此系统首次进入 PumpControl 后不能到达 PumpState。该主张是单一、明确的初始目标错误，裁 D2。",
        "basis": "NL L3 的 first transitions to PumpState 与 PlantUML L5 的唯一初始边逐字冲突；L7-L9 只定义 PumpState 的内部内容，没有任何目标为 PumpState 的边。",
        "relation_basis": {"EIS-0002-01": "同一 L5 初始目标错接 InitialState、未满足 NL L3 的 PumpState 首次落点。"},
    },
    "0004:r3:baseline_issue_5": {
        "pair": "0004", "round": 3, "index": 4,
        "d_tier": "D2", "validity": "VALID_KNOWN", "witness_level": "W1",
        "relations": {"EIS-0004-01": "FULL_MATCH"},
        "source_refs": ["pairs/0004/nl.txt:L1", "pairs/0004/plantuml.puml:L2-L8"],
        "observed_source_fact_status": "SUPPORTED",
        "normative_violation_status": "ESTABLISHED",
        "defect_claim_status": "AUTHOR_SOURCE_DEFECT",
        "reason": "作者源在根层 L2 将初始伪态指向 DoorsClosing，又在 DoorsClosing 块内 L5 用同名 DoorsClosing 作为内部初始目标。该内部目标不是一个明确的独立子态声明，按 PlantUML 名称解析会形成自嵌套/越界层级；因此顶层初始 DoorsClosing 与实际内部活动层级不再可唯一解释。NL L1 只要求从 DoorsClosing开始，不授权这一重复层级，裁 D2。",
        "basis": "逐行核对 PlantUML L2、L4-L6：重复名字出现在外部目标和内部初始目标，且没有另一命名或显式别名消除歧义。该事实与 EIS-0004-01 的同名复合态自初始目标完全重合。",
        "relation_basis": {"EIS-0004-01": "同一 DoorsClosing 块 L4-L6 的自引用初始目标和重复层级。"},
    },
    "0005:r3:baseline_issue_2": {
        "pair": "0005", "round": 3, "index": 1,
        "d_tier": "D2", "validity": "VALID_NOVEL", "witness_level": "W1",
        "relations": {},
        "source_refs": ["pairs/0005/nl.txt:L3-L4", "pairs/0005/plantuml.puml:L10-L16"],
        "observed_source_fact_status": "SUPPORTED",
        "normative_violation_status": "ESTABLISHED",
        "defect_claim_status": "AUTHOR_SOURCE_DEFECT",
        "reason": "DoorOpenWithItem 在作者源 L10-L16 被建成复合态，唯一初始目标是 NL 未提及的 DoorIdleWithItem；移除物品、关门和输入时间三条行为也从该额外子态发出。NL L3-L4把 DoorOpenWithItem作为直接可操作配置，没有要求一个会接管全部行为的中间子态，因此该额外层级是一个真实、可行动且未被 ledger expected 收录的结构问题，裁 D2并保留为 novel。",
        "basis": "NL L3明确从 DoorOpen 到 DoorOpenWithItem后处理 Item Removed，NL L4要求从 DoorOpenWithItem处理关门和时间输入；作者源 L11-L15却把三条出边的源统一改为 DoorIdleWithItem。最小修复是移除该中间层或把规范动作边接回 DoorOpenWithItem；这不是仅名称不同。",
        "relation_basis": {},
    },
    "0005:r3:baseline_issue_3": {
        "pair": "0005", "round": 3, "index": 2,
        "d_tier": "D2", "validity": "VALID_KNOWN", "witness_level": "W1",
        "relations": {"EIS-0005-02": "PARTIAL_MATCH"},
        "source_refs": ["pairs/0005/nl.txt:L4-L5", "pairs/0005/plantuml.puml:L18-L23"],
        "observed_source_fact_status": "SUPPORTED",
        "normative_violation_status": "ESTABLISHED",
        "defect_claim_status": "AUTHOR_SOURCE_DEFECT",
        "reason": "DoorShutWithItem 在 L18 被声明为复合态，L19 的唯一初始目标是 NL 未定义的 ItemInside；L21-L22 的规范动作随后从 ItemInside发出。NL L4-L5把 DoorShutWithItem作为直接配置并要求从该配置开门或输入时间，作者源插入了未授权中间活动层。该结构问题与 ledger 中同一微波炉模型的状态层级错置有关，但具体子态 ItemInside 不是 expected 描述的唯一实例，因此按 PARTIAL_MATCH。",
        "basis": "作者源 L18-L22 明确显示进入 DoorShutWithItem后先进入 ItemInside，且没有直接从 DoorShutWithItem承载两个规范行为。它与 EIS-0005-02共享层级错置的可审计后果和修复方向，但 expected 的 summary还涵盖其他前向引用造成的嵌套状态，故不把它升级为 FULL。",
        "relation_basis": {"EIS-0005-02": "同属 DoorOpenWithItem/DoorShutWithItem 复合层级错置，存在真实结构关系，但本报告的 ItemInside facet 不能唯一等同 expected 的全部前向引用实例。"},
    },
    "0005:r3:baseline_issue_8": {
        "pair": "0005", "round": 3, "index": 7,
        "d_tier": "D1", "validity": "VALID_KNOWN", "witness_level": "W1",
        "relations": {"EIS-0005-03": "FULL_MATCH"},
        "source_refs": ["pairs/0005/nl.txt:L6-L8", "pairs/0005/plantuml.puml:L33-L38"],
        "observed_source_fact_status": "SUPPORTED",
        "normative_violation_status": "AMBIGUOUS_READING",
        "defect_claim_status": "AUTHOR_SOURCE_DEFECT",
        "reason": "Cooking 的 Cancel 边在 L38 只改变状态到 ReadytoCook，没有写出取消或更新烹饪时间的动作。NL L6明确要求 Cancel 后取消或更新 cooking time，且 L5要求 ReadytoCook显示并更新该值，故缺失的数据动作与 EIS-0005-03同源。与此同时，规范也可能把回到 ReadytoCook抽象为由目标状态重新管理时间，作者源没有声明时间由本状态机内部持有；该替代读法仍存活，故裁 D1。",
        "basis": "NL L6-L8给出 Cancel、cooking time 与 Cooking 的关系；作者源 L33-L38无变量、effect或其它时间更新表示。直接读法支持缺失，抽象控制骨架读法可以把时间管理留给外部 HMI，二者均与现有文本相容，因此不是 D2。",
        "alternative_reading": "把 ReadytoCook解释为重新显示/管理外部维护的剩余时间，认为状态回转本身触发该管理；该读法不能证明作者源完整表达了动作，但足以使 D2 的唯一义务反驳不存活。",
        "relation_basis": {"EIS-0005-03": "同一 NL L5-L6 的 cooking-time 显示/取消/更新缺口；本报告具体落在 Cooking Cancel 分支。"},
    },
    "0012:r3:baseline_issue_1": {
        "pair": "0012", "round": 3, "index": 1,
        "d_tier": "D0", "validity": "INVALID", "witness_level": "W1",
        "relations": {},
        "source_refs": ["pairs/0012/nl.txt:L1-L3", "pairs/0012/plantuml.puml:L4-L9"],
        "observed_source_fact_status": "SUPPORTED",
        "normative_violation_status": "NOT_ESTABLISHED",
        "defect_claim_status": "AUTHOR_SOURCE_DEFECT_NOT_ESTABLISHED",
        "reason": "作者源确实只有 Idle -> AcceleratingOrCruising -> Braking -> Idle 三条内部边，但 NL L1-L3只要求根据用户动作在列出的子状态之间转换，并没有逐一规定从每个状态到每个其它状态的完整转移矩阵。报告把“没有 Idle 直接到 Braking”当成义务，却没有作者源或 NL 证据说明 stopping 必须绕过 AcceleratingOrCruising直接制动；因此事实（边不存在）成立，违反义务不成立，裁 D0并派生 INVALID。",
        "basis": "NL L3使用“actions like”举例而非穷举；PlantUML L6-L8提供一个可解释的动作链，且没有矛盾的状态/事件事实需要补一条 Idle->Braking边。D0而非A0，因为报告指出的边缺失是真实的，只是从该缺失不能推出规范缺陷。",
        "relation_basis": {},
    },
    "0015:r3:baseline_issue_2": {
        "pair": "0015", "round": 3, "index": 1,
        "d_tier": "D1", "validity": "VALID_NOVEL", "witness_level": "W1",
        "relations": {},
        "source_refs": ["pairs/0015/nl.txt:L7", "pairs/0015/plantuml.puml:L24-L30"],
        "observed_source_fact_status": "SUPPORTED",
        "normative_violation_status": "AMBIGUOUS_READING",
        "defect_claim_status": "AUTHOR_SOURCE_DEFECT",
        "reason": "作者源 L26 只表示 ReadytoCook 到 Cooking 的 Start 状态转换，没有 Start Timer effect 或其它计时动作。NL L7明确说进入 Cooking时 timer starts，故报告指出的表示缺口是可核对的；但也存在把进入 Cooking状态本身抽象为计时器启动、由外部计时器发出 Timer Expired 的称职读法。两读并立，裁 D1；本 pair 的 ledger expected只覆盖 cooking-time显示/更新，不覆盖该timer-start facet，因此全量 relation 为 NO_MATCH。",
        "basis": "NL L7将 Start 与 timer starts 同句绑定，PlantUML L24-L30只有状态和触发标签、无 effect。时间动作在本协议中属于可审计建模义务，但“状态进入即启动”仍是与控制骨架一致的替代解释，不能强行D2。",
        "alternative_reading": "把进入 Cooking 解释为 timer 已启动的抽象状态语义，Timer Expired作为外部事件；该读法保留了生命周期关系但没有显式动作。",
        "relation_basis": {},
    },
    "0015:r3:baseline_issue_3": {
        "pair": "0015", "round": 3, "index": 2,
        "d_tier": "D1", "validity": "VALID_NOVEL", "witness_level": "W1",
        "relations": {},
        "source_refs": ["pairs/0015/nl.txt:L8", "pairs/0015/plantuml.puml:L28-L30"],
        "observed_source_fact_status": "SUPPORTED",
        "normative_violation_status": "AMBIGUOUS_READING",
        "defect_claim_status": "AUTHOR_SOURCE_DEFECT",
        "reason": "作者源 L28 只有 Cooking 到 DoorOpenWithItem 的 Door Opened 边，没有 Stop Timer effect。NL L8明确要求开门停止计时器后转移，故直接读法发现了可定位缺口；但离开 Cooking状态也可以被解释为计时器停止的抽象状态生命周期，且源模型将 Timer Expired作为外部事件。两种解释与作者源相容，裁 D1；该具体 timer-stop facet不等同于 ledger 的 cooking-time显示/更新 expected。",
        "basis": "NL L8给出“opening the door stops the timer and ... transitions”，PlantUML L28-L30没有动作槽。报告的事实成立，但现有控制骨架可以把计时运行绑定到 Cooking占据、把离开视为停止，故不足以D2。",
        "alternative_reading": "把 Cooking 的状态占据定义为计时器运行，Door Opened离开该状态隐含停止；该解释不能提供显式 receipt，但与现有建模粒度一致。",
        "relation_basis": {},
    },
    "0019:r3:baseline_issue_1": {
        "pair": "0019", "round": 3, "index": 0,
        "d_tier": "D2", "validity": "VALID_KNOWN", "witness_level": "W1",
        "relations": {"EIS-0019-03": "FULL_MATCH"},
        "source_refs": ["pairs/0019/nl.txt:L3-L6", "pairs/0019/plantuml.puml:L10-L21"],
        "observed_source_fact_status": "SUPPORTED",
        "normative_violation_status": "ESTABLISHED",
        "defect_claim_status": "AUTHOR_SOURCE_DEFECT",
        "reason": "HighwayMode 的 cruise/lane_change 在 L16、L19 通过 dist_to_exit<2进入块外 ExitHighway，随后 L21 才由 auto_finished=true到 FinishState。NL L4-L6要求出口行为与 HighwayMode按 auto_finished完成分别表达；该中间状态和顺序把模式级完成条件收窄为先满足出口距离，且 ExitHighway不在 HighwayMode 内。作者源没有可存活的等价层级解释，裁 D2。",
        "basis": "PlantUML L10-L20闭合 HighwayMode，L21已在块外；NL L4-L6逐句区分出口距离与模式完成条件。最小修复是保留出口子状态在正确层级并补模式级完成边，正是 EIS-0019-03的核心。",
        "relation_basis": {"EIS-0019-03": "同一 HighwayMode完成源被收窄至 ExitHighway，且出口态被置于模式外，导致 NL L6模式级 auto_finished义务失真。"},
    },
    "0019:r3:baseline_issue_2": {
        "pair": "0019", "round": 3, "index": 1,
        "d_tier": "D2", "validity": "VALID_KNOWN", "witness_level": "W1",
        "relations": {"EIS-0019-03": "FULL_MATCH"},
        "source_refs": ["pairs/0019/nl.txt:L7-L10", "pairs/0019/plantuml.puml:L23-L35"],
        "observed_source_fact_status": "SUPPORTED",
        "normative_violation_status": "ESTABLISHED",
        "defect_claim_status": "AUTHOR_SOURCE_DEFECT",
        "reason": "UrbanMode块在 L23-L34结束，exit_urban 到 FinishState 的完成边在 L35位于块外；模型没有从 UrbanMode整体按 auto_finished=true结束的边。NL L8要求 exit_urban是UrbanMode内的出口子态，NL L10要求UrbanMode按完成条件退出，当前层级与路径均不符，裁 D2。该报告与 EIS-0019-03同一模式完成错层/收窄缺陷。",
        "basis": "逐行核对作者源 L23-L35：exit_urban首次作为目标出现在 UrbanMode内，但其完成边移到外层，且没有另一个 UrbanMode -> FinishState : auto_finished=true。",
        "relation_basis": {"EIS-0019-03": "同一 UrbanMode完成边被放在出口态外层，导致 auto_finished只在出口态被消费。"},
    },
    "0019:r3:baseline_issue_5": {
        "pair": "0019", "round": 3, "index": 4,
        "d_tier": "D2", "validity": "VALID_KNOWN", "witness_level": "W1",
        "relations": {"EIS-0019-03": "FULL_MATCH"},
        "source_refs": ["pairs/0019/nl.txt:L6-L10", "pairs/0019/plantuml.puml:L10-L39"],
        "observed_source_fact_status": "SUPPORTED",
        "normative_violation_status": "ESTABLISHED",
        "defect_claim_status": "AUTHOR_SOURCE_DEFECT",
        "reason": "作者源只在 L21 的 ExitHighway 和 L35 的 exit_urban 上消费 auto_finished=true；HighwayMode/UrbanMode整体以及其 enter、cruise、lane_change、straight、intersection状态没有对应模式级完成边。NL L6与L10明确把完成条件绑定到两个模式整体，因此该报告指出的是一个真实且可行动的完成闭合缺口，裁 D2。",
        "basis": "NL L6/L10的主语分别是 HighwayMode 与 UrbanMode，PlantUML L10-L39没有从两个复合模式整体发出的 auto_finished边，只有两个外部出口态边。该缺口与 EIS-0019-03的核心相同。",
        "relation_basis": {"EIS-0019-03": "同一 auto_finished消费点被错误收窄到 ExitHighway/exit_urban，而非两个模式整体。"},
    },
}

PREEXISTING = {
    "0007:r1:baseline_issue_1",
    "0009:r1:baseline_issue_6",
    "0019:r1:baseline_issue_2",
    "0019:r1:baseline_issue_3",
}


def all_raw_issues() -> dict[tuple[str, int, int], tuple[Path, dict[str, Any]]]:
    result: dict[tuple[str, int, int], tuple[Path, dict[str, Any]]] = {}
    for path in sorted(RAW_ROOT.glob("run*/[0-9][0-9][0-9][0-9]-*/record.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        pair = str(record["pair_id"])[-4:]
        round_no = int(record["round"])
        for index, issue in enumerate(record["parsed_output"]["issues"]):
            result[(pair, round_no, index)] = (path, issue)
    return result


def materialize_entry(key: str, assessment: dict[str, Any], raw_index: dict[tuple[str, int, int], tuple[Path, dict[str, Any]]], ledger_ids: list[str]) -> dict[str, Any]:
    pair, round_token, report_token = key.split(":")
    round_no = int(round_token[1:])
    report_index = int(report_token.rsplit("_", 1)[1]) - 1
    raw_path, issue = raw_index[(pair, round_no, report_index)]
    nl_path = SOURCE_ROOT / pair / "nl.txt"
    puml_path = SOURCE_ROOT / pair / "plantuml.puml"
    relation_map = assessment["relations"]
    relations = [
        {"ledger_id": ledger_id, "relation": relation_map.get(ledger_id, "NO_MATCH")}
        for ledger_id in ledger_ids
    ]
    full = [item["ledger_id"] for item in relations if item["relation"] == "FULL_MATCH"]
    partial = [item["ledger_id"] for item in relations if item["relation"] == "PARTIAL_MATCH"]
    no_match = [item["ledger_id"] for item in relations if item["relation"] == "NO_MATCH"]
    expected_validity = "VALID_KNOWN" if full or partial else assessment["validity"]
    if assessment["d_tier"] == "D0":
        expected_validity = "INVALID"
    evidence_digest = hashlib.sha256(
        (sha256(raw_path) + sha256(nl_path) + sha256(puml_path)).encode("ascii")
    ).hexdigest()
    return {
        "proposal_status": "PROPOSAL",
        "pair_id": pair,
        "round": round_no,
        "original_report_id": key,
        "finding_index": report_index,
        "raw_record_path": ref(raw_path),
        "raw_json_pointer": f"/parsed_output/issues/{report_index}",
        "raw_sha256": sha256(raw_path),
        "raw_fields": {"issue": issue.get("issue"), "where": issue.get("where"), "reason": issue.get("reason")},
        "author_source": {
            "nl_path": ref(nl_path), "nl_sha256": sha256(nl_path),
            "plantuml_path": ref(puml_path), "plantuml_sha256": sha256(puml_path),
        },
        "source_refs": assessment["source_refs"],
        "observed_source_fact_status": assessment["observed_source_fact_status"],
        "normative_violation_status": assessment["normative_violation_status"],
        "defect_claim_status": assessment["defect_claim_status"],
        "d_tier": assessment["d_tier"],
        "a0_reason": None,
        "validity": expected_validity,
        "witness_level": assessment["witness_level"],
        "relations": relations,
        "full_ledger_ids": full,
        "partial_ledger_ids": partial,
        "no_match_ledger_ids": no_match,
        "reason": assessment["reason"],
        "basis": assessment["basis"],
        "alternative_reading": assessment.get("alternative_reading"),
        "relation_basis": assessment["relation_basis"],
        "reviewer_id": "track_b_blind_raw_first",
        "review_mode": "PROPOSAL_ONLY",
        "human_confirmation": False,
        "evidence_digest": evidence_digest,
    }


def append_entries(existing: Any, additions: list[dict[str, Any]]) -> Any:
    if isinstance(existing, list):
        return existing + additions
    if not isinstance(existing, dict):
        raise TypeError("existing proposal must be a JSON array or object")
    for key in ("entries", "proposals", "reports"):
        if isinstance(existing.get(key), list):
            existing[key].extend(additions)
            return existing
    raise KeyError("could not find an entries/proposals/reports array")


def main() -> None:
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    ledger_ids = list(ledger["items"].keys())
    raw_index = all_raw_issues()
    existing = json.loads(OUTPUT.read_text(encoding="utf-8"))
    requested = set(MANUAL) | PREEXISTING
    if isinstance(existing, list):
        existing_entries = existing
        container = existing
    else:
        array_keys = [key for key in ("entries", "proposals", "reports") if isinstance(existing.get(key), list)]
        if len(array_keys) != 1:
            raise KeyError("could not find a unique entries/proposals/reports array")
        container = existing
        existing_entries = existing[array_keys[0]]
    # Keep only the exact user-supplied scope; this is structural filtering,
    # and does not inspect or use any prior decision content.
    retained = [entry for entry in existing_entries if entry.get("original_report_id") in PREEXISTING]
    existing_ids = {entry.get("original_report_id") for entry in retained}
    additions = [
        materialize_entry(key, assessment, raw_index, ledger_ids)
        for key, assessment in MANUAL.items()
        if key not in existing_ids
    ]
    retained.extend(additions)
    if isinstance(container, list):
        merged = retained
    else:
        array_key = next(key for key in ("entries", "proposals", "reports") if isinstance(container.get(key), list))
        container[array_key] = retained
        merged = container
    OUTPUT.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"retained": len(retained) - len(additions), "appended": len(additions), "removed_out_of_scope": len(existing_entries) - (len(retained) - len(additions)), "dense_relations": len(ledger_ids), "output": ref(OUTPUT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
