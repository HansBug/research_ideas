# PR-M3 codex exec skill 实验报告：path1_cara

## 1. Run identity

| 字段 | 值 |
|---|---|
| run_label | `pr_m3_four_clean_20260608_133322` |
| case_key | `path1_cara` |
| case_id | `cara-infusion-pump-formal-spec__01` |
| path | `path1` |
| 输出目录 | `runs/codex_exec_skill/2026-06-08-133322-pr39-pr-m3-codex-exec-skill-final-four-case-evidence/path1-cara-codex-exec-skill-completed` |
| skill 入口 | `project_1_llm_state_machine_modeling/method/agent_loop_skill/AGENT_LOOP_SKILL.md` |
| provider config 可见信息 | redacted command 中可见 `model_provider=airouter` |
| 状态 | `valid_candidate` |
| 禁止 runner | `forbidden_runner_used=false`；未使用顶层 loop runtime 或一键 staged runner |

本次运行作为 PR-M3 codex exec skill 标准实验入口执行。模型由本 agent 基于 repo-local skill、CARA 论文材料和底层 SD/SC 工具自主生成、检查、修复和评价；没有使用顶层 runtime 代生成模型。

## 2. Input

paper_dir:

```text
project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec
```

NL 原文：

```text
At run time, CARA coordinates the Caregiver Interface, Blood Pressure Monitor, Algorithm, and Pump Monitors around an infusion pump that moves fluid into the patient, while sensor readings are stored in a shared buffer for software access. The pump has manual and autocontrol modes. In manual mode, pump speed is set with the built-in switch and the caregiver sets a default flow rate directly on the pump for manual operation, while in autocontrol mode pump speed is set by a control voltage from an external source. The Algorithm component controls infusion rate and records infusion-related data in log files; patient blood pressure is used to compute the infusion rate, with higher pressure producing a lower flow rate. The Caregiver Interface lets the caregiver modify target blood pressure and initiate or terminate algorithmic pump control, and it also displays and sounds error messages. In the Mode_Control_Algorithm hierarchy, CARA has manual and autocontrol-related mode-control states plus an Ask_StartAC submode; within Ask_StartAC, the setpoint can be changed and pressing StartAC enters AutocontrolInit. During normal autocontrol, CARA controls flow rate only while there are no pump-operation complications. If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals, the caregiver removes the fault, and when CARA was controlling the pump the software releases control. As a cross-component fallback, CA_backManual or any of CB_backManual, CP_backManual, or CC_backManual causes CA_mode to become Manual, making manual operation the shared recovery target.
```

NL 中文翻译/释义：

```text
运行时，CARA 围绕一台向患者输液的输液泵协调 Caregiver Interface、Blood Pressure Monitor、Algorithm 与 Pump Monitors，传感器读数会写入共享缓冲区供软件访问。泵具有手动和自动控制两种模式。手动模式下，泵速由内置开关设置，护理人员直接在泵上设置默认流量；自动控制模式下，泵速由外部控制电压设置。Algorithm 组件控制输液速率并记录输液相关日志；患者血压用于计算输液速率，血压越高流量越低。Caregiver Interface 允许护理人员修改目标血压，并启动或终止算法泵控制，同时显示和发出错误消息。在 Mode_Control_Algorithm 层次中，CARA 具有手动与自动控制相关的模式控制状态以及 Ask_StartAC 子模式；在 Ask_StartAC 中可以修改设定点，按下 StartAC 会进入 AutocontrolInit。正常自动控制期间，只有没有泵操作并发症时 CARA 才控制流量。如果出现输液管堵塞等泵故障，泵会激活报警信号，护理人员排除故障；当 CARA 正在控制泵时，软件会释放控制。作为跨组件回退，CA_backManual 或 CB_backManual、CP_backManual、CC_backManual 中任一事件都会使 CA_mode 变为 Manual，使手动操作成为共享恢复目标。
```

## 3. Actual Reads

| 类型 | 实际读取路径 | 用途 |
|---|---|---|
| skill | `project_1_llm_state_machine_modeling/method/agent_loop_skill/AGENT_LOOP_SKILL.md` | 确认 PR-M3/E2 边界、禁止项、stage 顺序 |
| skill guide | `project_1_llm_state_machine_modeling/method/agent_loop_skill/e2e_ref_model_guide.md` | 确认 NL+paper_dir 到 FCSTM 的 E0-E7 流程 |
| skill guide | `project_1_llm_state_machine_modeling/method/agent_loop_skill/tools.md` | 确认 SD/SC 工具入口 |
| skill guide | `project_1_llm_state_machine_modeling/method/agent_loop_skill/prompts.md` | 确认 SL prompt 和 repair 记录口径 |
| skill guide | `project_1_llm_state_machine_modeling/method/agent_loop_skill/nfrr_evaluation_guide.md` | 执行 NFRR v3 评价 |
| skill guide | `project_1_llm_state_machine_modeling/method/agent_loop_skill/codex_exec_experiment_guide.md` | 确认 PR-M3 artifact 和 report 要求 |
| stage guide | `project_1_llm_state_machine_modeling/method/agent_loop_skill/stages/README.md` | 确认 PR-E1 repair 主链 |
| API | `project_1_llm_state_machine_modeling/method/stages/api.py` | 确认 skill-facing facade |
| API | `project_1_llm_state_machine_modeling/method/schema.py` | 确认 StageContext、Scenario schema |
| API | `project_1_llm_state_machine_modeling/method/stages/sd_tools.py` | 确认 SD 工具行为和 warning policy |
| grammar | `project_1_llm_state_machine_modeling/method/prompts/_pyfcstm_grammar.md` | 确认当前 FCSTM 语法 |
| example | `project_1_llm_state_machine_modeling/method/EXAMPLES.md` | 参考 SD-6 scenario 习语 |
| paper | `project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/bibtex.bib` | 元信息 |
| paper | `project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/STM.md` | 主 evidence grounding |
| paper | `project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/DESC.md` | 范围与阅读路线 |
| paper | `project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper_content.txt` | 核对第 5、7、19 页相关段落 |
| redacted harness | `command.redacted.txt`、`env.redacted.json`、`run_manifest.json` | 只读取脱敏运行配置和 case 元数据 |

`paper.pdf` 被检测到但未直接打开。原因是 `paper_content.txt` 与 `STM.md` 的相关抽取段落一致且无明显乱码/缺失，不需要 PDF fallback。

## 4. Grounding 摘要

| 元素 | 证据 | 建模处理 |
|---|---|---|
| `Manual` / `Autocontrol` | `STM.md` 条目 1 摘录 A/C；`paper_content.txt` 第 247-250、1303-1323 行附近 | 作为核心模式状态 |
| `Ask_StartAC` | `STM.md` 条目 1 摘录 C；第 19 页 Mode_Control_Algorithm span | 作为可停止 leaf 状态；保留 setpoint 修改与 StartAC 触发 |
| `AutocontrolInit` | 同上 | 作为进入自动控制前的 transient state |
| `CA_mode` 回到 Manual | `STM.md` 摘录 B；`paper_content.txt` 第 536-537 行附近 | `CA/CB/CP/CC_backManual` forced transition 到 `Manual` |
| 泵故障、报警、释放控制 | `STM.md` 摘录 A/B；`paper_content.txt` 第 230-234、370-375 行附近 | `PumpFault` forced transition，entry 设置 alarm/message/release |
| 血压越高流量越低 | `paper_content.txt` 第 370-373 行附近 | 三档 `current_bp_level` 与 `flow_command` 离散抽象 |
| 传感器共享缓冲区 | `paper_content.txt` 第 239-245 行附近 | 用 `BP_Low/BP_Normal/BP_High` 事件模拟 buffer update |

合成抽象：`control_owned`、`flow_source`、`flow_command`、`current_bp_level`、`setpoint_change_count`、`log_count` 是为了可执行检查和输出观测引入的离散变量，不应被误认为论文原文直接定义的变量。

## 5. Process Table

| 阶段 | 是否 LLM | 结果 | 做了什么 | 产物/证据 |
|---|---:|---|---|---|
| E0 skill discovery | 否 | pass | 读取 skill 入口和 5 个必读指南，确认禁止 full runner | `actual_file_reads.json` |
| E1 evidence grounding | 否 | pass | 从 NL、STM、DESC、paper_content 抽取状态、事件、变量和异常回退义务 | 本报告 §4、`nfrr_report.json` |
| E2 initial modeling | 是, 本 agent | v0 生成 | 生成 FCSTM DSL，使用 int 0/1 和整数档位，不使用 bool literal | repair ledger 中 v0 记录 |
| E3 deterministic checks v0 | 否 | SD-6 fail | SD-2/3/4 pass；SD-6 暴露 Wait 默认前缀和 Ask_StartAC event scope 问题 | `repair_ledger.json` |
| E4 repair | 是, 本 agent | accepted | 把 Ask_StartAC 改成 leaf，并把默认启动场景改为 Wait -> Manual 两步前缀 | `repair_ledger.json` |
| E3 deterministic checks v1 | 否 | pass with advisory | SD-2/3/4 pass，SD-6 5/5 pass，SD-5A mutation coverage advisory | `tool_stage_check_ledger.json` |
| E5 NFRR | 否 | T2 | 输出 claim、coverage、alignment、scenario、mutation、waiver、8 维分数 | `nfrr_report.json` |
| E6 final audit | 否 | pass | 写入 final model、report、metadata 与 ledgers | 本目录 producer-owned files |

## 6. Checks

| 检查 | 结果 | 摘要 |
|---|---|---|
| SD-2 parse | pass | `final_model.fcstm` 可解析 |
| SD-3 semantic | pass | AST 到 state-machine 构建通过 |
| SD-4 design | pass with advisory | blocking=0；advisory=18；info=2 |
| SD-5A scenario coverage | advisory gap | mutation coverage 有缺口，降低 DMR，不声明 T3 |
| SC-5F scenario freeze | pass | 5 个 scenario frozen |
| SD-6 simulation | pass | 5/5 场景通过 |

SD-4 advisories 主要来自 output/observability variables 不参与 guard，例如 `CA_mode`、`flow_command`、`pump_alarm`。这些变量由 NL/paper 明确支持，并通过 SD-6 expected_vars 检查，未作为 blocking 问题处理。

## 7. Repair Ledger 摘要

| request | decision | 修复 | local evidence | SL-10 式判断 |
|---|---|---|---|---|
| FR-001 | accept | 明确默认前缀：第一步进入 `Wait`，下一步无事件转入 `Manual` | SD-6 default scenario pass | pass，语义未漂移 |
| FR-002 | accept | 将 `Ask_StartAC` 从 composite+Prompting 改为 leaf，并直接承载 `ChangeSetpoint` 与 `StartAC` | SD-2/3/4 pass，Ask_StartAC scenario pass | pass，保留 NL 的 StartAC -> AutocontrolInit |
| SD-5A gap | waiver/limitation | 不伪造额外 mutation coverage | SD-5A advisory gap | 降低 DMR，限制 T3 claim |

## 8. NFRR 摘要

| 字段 | 值 |
|---|---|
| evidence_mode | `NL+paper` |
| scope_type | `full_NL_fragment` |
| obligation_independence | `single_self_assessment` |
| calibration_status | `uncalibrated_candidate_gate` |
| signed_reference | `false` |
| allowed_use_rule_id | `AU-3` |
| allowed_use | `reviewer_queue` |
| final_tier | `T2` |

| 维度 | 分数 | 依据 |
|---|---:|---|
| FE | 3 | SD-2/3 pass，SD-4 无 blocking，advisory 有说明 |
| NGF | 3 | 无 critical/major contradiction，主义务匹配 |
| REC | 3 | weighted recall 约 0.932，无 critical/major missing |
| GAS | 2 | BP 高低与 flow 方向有场景，连续边界未完整覆盖 |
| SCB | 3 | NL spans 已分类，scope 为 full_NL_fragment |
| AAT | 2 | 合成变量与 waiver 有 ledger，但只有 self review |
| BVS | 3 | 5 个 default-prefix obligation-anchored scenarios 全部 SD-6 pass |
| DMR | 1 | SD-5A mutation coverage gap 明显 |

准出判断：可进入 reviewer queue，但不是 signed reference，也不是 Ground Truth 级候选。

## 9. Final FCSTM

```fcstm
def int CA_mode = 0;
def int control_owned = 0;
def int flow_source = 0;
def int flow_command = 0;
def int current_bp_level = 1;
def int target_bp = 80;
def int setpoint_change_count = 0;
def int pump_fault = 0;
def int pump_alarm = 0;
def int error_message = 0;
def int log_count = 0;

state CARA_Mode_Control {
    event RequestAC;
    event ChangeSetpoint;
    event StartAC;
    event BP_Low;
    event BP_Normal;
    event BP_High;
    event PumpFault;
    event FaultRemoved;
    event TerminateAC;
    event CA_backManual;
    event CB_backManual;
    event CP_backManual;
    event CC_backManual;

    ! * -> PumpFault : /PumpFault;
    ! * -> Manual : /CA_backManual;
    ! * -> Manual : /CB_backManual;
    ! * -> Manual : /CP_backManual;
    ! * -> Manual : /CC_backManual;

    [*] -> Wait;

    state Wait;

    state Manual {
        enter {
            CA_mode = 0;
            control_owned = 0;
            flow_source = 0;
            flow_command = 0;
        }
    }

    state Ask_StartAC {
        enter {
            CA_mode = 1;
            flow_source = 0;
        }
    }

    state AutocontrolInit {
        enter {
            CA_mode = 2;
            control_owned = 1;
            flow_source = 1;
            pump_alarm = 0;
            error_message = 0;
        }
    }

    state Autocontrol {
        enter {
            CA_mode = 3;
            control_owned = 1;
            flow_source = 1;
        }
        during {
            log_count = log_count + 1;
            if [current_bp_level >= 2] {
                flow_command = 1;
            } else if [current_bp_level == 1] {
                flow_command = 2;
            } else {
                flow_command = 3;
            }
        }
    }

    state PumpFault {
        enter {
            pump_fault = 1;
            pump_alarm = 1;
            error_message = 1;
            control_owned = 0;
            flow_source = 0;
            CA_mode = 0;
        }
    }

    Wait -> Manual;
    Manual -> Ask_StartAC : /RequestAC;
    Ask_StartAC -> Ask_StartAC : /ChangeSetpoint effect {
        target_bp = target_bp + 5;
        setpoint_change_count = setpoint_change_count + 1;
    };
    Ask_StartAC -> AutocontrolInit : /StartAC;
    AutocontrolInit -> Autocontrol;
    Ask_StartAC -> Manual : /TerminateAC;
    AutocontrolInit -> Manual : /TerminateAC;
    Autocontrol -> Manual : /TerminateAC;
    Autocontrol -> Autocontrol : /BP_Low effect {
        current_bp_level = 0;
        flow_command = 3;
    };
    Autocontrol -> Autocontrol : /BP_Normal effect {
        current_bp_level = 1;
        flow_command = 2;
    };
    Autocontrol -> Autocontrol : /BP_High effect {
        current_bp_level = 2;
        flow_command = 1;
    };
    PumpFault -> Manual : /FaultRemoved effect {
        pump_fault = 0;
        pump_alarm = 0;
        error_message = 0;
    };
}
```

final_model_sha256:

```text
b48aa16eee2c0616f82f9706756377a508952aabd8447ad5652bd765448aa332
```

## 10. 质量风险和限制

1. 这是 `Mode_Control_Algorithm` 与泵故障回退的候选模型，不是完整 CARA 系统模型。
2. 血压和输液速率被离散化为三档整数，未建模连续控制公式和真实控制电压。
3. `Ask_StartAC` 为了 pyfcstm 可执行性建成 leaf state，而不是完整保留论文图中的嵌套子模式结构。
4. `paper_content.txt` 支持主证据，但没有直接打开 `paper.pdf` 核对图 11 的全部不可见 transition label。
5. SD-5A mutation coverage 仍有明显缺口，`DMR=1`。
6. NFRR 是单 agent 自评，没有独立 adjudication、人工签核或专家 signoff。

## 11. Reviewer Queue 判断

结论：可以进入 reviewer queue。

理由：模型达到 NFRR `T2`，SD-2/SD-3 通过，SD-4 无 unwaived blocking，至少一个且实际 5 个 counted main BVS scenario 通过 SD-6，无 critical contradiction、无 reachable test harness pollution。

限制：不得标为 signed reference 或 Ground Truth 级 ref model。进入 reviewer queue 后应优先复核 Ask_StartAC 层次结构、图 11 transition label、连续 BP/flow 抽象和 backManual forced transition 的事件作用域。
