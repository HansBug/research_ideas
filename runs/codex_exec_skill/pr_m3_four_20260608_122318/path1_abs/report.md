# PR-M3 Codex Exec Skill 实验报告：path1_abs

## Run identity

| 字段 | 值 |
|---|---|
| run_label | `pr_m3_four_20260608_122318` |
| case_key | `path1_abs` |
| case_id | `abs-fsm-brake-control` |
| path | `path1` |
| output_dir | `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_abs` |
| status | `success` |
| provider config seen | `{"model_provider": "airouter"}` |
| skill entry read | `project_1_llm_state_machine_modeling/method/agent_loop_skill/SKILL.md` -> `AGENT_LOOP_SKILL.md` |

## Input

NL source: `project_1_llm_state_machine_modeling/eval/data/sources/abs-fsm-brake-control/nl.md`

paper_dir: `project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control`

### NL 原文

```text
The paper implements the single-wheel ABS hydraulic regulator as a three-state FSM coupled with a PID-based slip controller. Wheel speed and vehicle speed are used to compute the slip ratio, and the PID output drives the Stateflow supervisor instead of sending commands directly to the hydraulic valves.

The FSM contains the states `increase`, `hold`, and `decrease`, where `increase` sets `k1=1, k2=0, n=0`, `hold` neutralizes both valves with `k1=0, k2=0, n=0`, and `decrease` sets `k1=0, k2=1, n=500` to release pressure.

The transition guards split the slip-error space into four bands: `increase -> hold` when `slp <= 0.01`, `hold -> increase` when `slp > 0.01`, `hold -> decrease` when `slp < -0.01`, and `decrease -> hold` when `slp >= -0.01`.

This gives a concrete discrete supervisor that maps slip-error thresholds to inlet-valve, return-valve, and pump actions while the continuous wheel-slip dynamics remain in the plant model.
```

### NL 中文翻译/释义

```text
论文把单轮 ABS 液压调节器实现为一个三状态 FSM，并与基于滑移率的 PID 控制器耦合。轮速与车速用于计算滑移率，PID 输出驱动 Stateflow 监督器，而不是直接发送液压阀命令。

FSM 包含 `increase`、`hold`、`decrease` 三个状态：`increase` 设置 `k1=1, k2=0, n=0`，`hold` 设置 `k1=0, k2=0, n=0`，`decrease` 设置 `k1=0, k2=1, n=500` 以释放压力。

转移 guard 把滑移误差空间分成四个区间：`increase -> hold` 当 `slp <= 0.01`，`hold -> increase` 当 `slp > 0.01`，`hold -> decrease` 当 `slp < -0.01`，`decrease -> hold` 当 `slp >= -0.01`。

这给出了一个具体的离散监督器，把滑移误差阈值映射为进油阀、回油阀与泵动作，而连续轮胎滑移动力学仍留在被控对象模型中。
```

## Actual reads

| 类型 | 路径 | 读取方式/范围 |
|---|---|---|
| skill_entry | `project_1_llm_state_machine_modeling/method/agent_loop_skill/SKILL.md` | full: sed -n 1,240p; file length 92 lines |
| skill_doc | `project_1_llm_state_machine_modeling/method/agent_loop_skill/e2e_ref_model_guide.md` | full by ranges: 1-260, 260-420, 420-500; file length 465 lines |
| skill_doc | `project_1_llm_state_machine_modeling/method/agent_loop_skill/tools.md` | full: sed -n 1,260p; file length 78 lines |
| skill_doc | `project_1_llm_state_machine_modeling/method/agent_loop_skill/prompts.md` | full: sed -n 1,260p; file length 57 lines |
| skill_doc | `project_1_llm_state_machine_modeling/method/agent_loop_skill/nfrr_evaluation_guide.md` | full by ranges: 1-320, 320-760, 760-980, 980-1040; file length 1014 lines |
| skill_doc | `project_1_llm_state_machine_modeling/method/agent_loop_skill/codex_exec_experiment_guide.md` | full: 1-360 plus 360-520 check; file length 81 lines |
| skill_doc | `project_1_llm_state_machine_modeling/method/agent_loop_skill/stages/README.md` | full: sed -n 1,260p; file length not separately needed |
| tool_doc | `project_1_llm_state_machine_modeling/method/prompts/_pyfcstm_grammar.md` | partial: 1-260, enough for declarations, states, transitions, actions |
| tool_test | `project_1_llm_state_machine_modeling/method/tests/stages/test_sd_tools.py` | partial: 1-260 |
| tool_schema | `project_1_llm_state_machine_modeling/method/schema.py` | partial: 1-260 and 740-875; class locations searched |
| tool_code | `project_1_llm_state_machine_modeling/method/stages/sd_tools.py` | partial: 1-220, 220-520, 520-820 |
| tool_code | `project_1_llm_state_machine_modeling/method/feedback/sim.py` | partial: full enough, 1-560 |
| tool_test | `project_1_llm_state_machine_modeling/method/tests/experiments/test_scenario_normalization.py` | partial: 1-260 |
| input_nl | `project_1_llm_state_machine_modeling/eval/data/sources/abs-fsm-brake-control/nl.md` | full: sed -n 1-220 |
| paper_meta | `project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control/bibtex.bib` | full: sed -n 1-220 |
| paper_derived | `project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control/STM.md` | full: sed -n 1-260 |
| paper_derived | `project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control/DESC.md` | full: sed -n 1-260 |
| paper_text | `project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control/paper_content.txt` | full/targeted: nl -ba 1-230 and 231-270; rg state/slp/PID terms; wc confirmed 261 lines |
| paper_pdf | `project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control/paper.pdf` | page 4 rendered with pdftoppm to /tmp/abs_page4.png and visually inspected |
| run_artifact | `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_abs/run_manifest.json` | partial: 1-220 |
| run_artifact | `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_abs/command.redacted.txt` | full: 1-200 |
| run_artifact | `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_abs/env.redacted.json` | full: 1-220 |

## Evidence grounding

| 元素 | 证据 | 建模决定 |
|---|---|---|
| 初始状态与三态 | PDF 第 4 页 Figure 6；`STM.md` 摘录 C | `ABSBrakeSupervisor` 初始进入 `increase`，包含 `increase/hold/decrease` 三个状态 |
| 状态动作 | Figure 6 的 `du:`；`STM.md` 摘录 C | 用 pyfcstm `during` 表达 `k1/k2/n` 持续输出 |
| guard | Figure 6；NL 第四段 | 四条 guard 按阈值和方向原样建模 |
| 外部输入 | NL/Paper 说明 PID slip-error 输出驱动 FSM，连续动力学在 plant | `slp` 声明为 guard-only `float`，不伪造内部写入 |
| 输出变量 | `paper_content.txt` 第 137-139 行定义 K1/K2/n 为阀/泵信号 | `k1/k2/n` 用 `int` 输出，作为 scenario expected vars 检查 |

## Process table

| Stage | 是否 LLM | 结果 | 获取的信息/反馈 | DSL 修改 |
|---|---:|---|---|---|
| E0 Skill discovery | 否 | pass | 读取 skill 入口、E2/M3/NFRR/tool/prompt/stage 文档，确认禁止顶层 runner 与 SD 工具入口。 | 无 |
| E1 Evidence grounding | 否 | pass | 读取 NL、BibTeX、STM、DESC、paper_content，并视觉核对 PDF 第 4 页 Figure 6。 | 无 |
| E2 Initial modeling | 否 | pass | 生成三态 `ABSBrakeSupervisor`，使用 `float slp` 外部输入与 `int k1/k2/n` 输出。 | 新建 DSL |
| E3 Deterministic checks | 否 | pass | SD-2/SD-3/SD-4/SD-5A/SC-5F/SD-6 全部通过。 | 无 |
| E4 Repair/waiver | 否 | pass | 非 blocking 修订：`enter` 改为 `during` 以匹配 Stateflow `du:`；外部输入/输出 advisory 进入 waiver ledger。 | lifecycle action 修订 |
| E5 NFRR | 否 | pass | 输出 claim、NL coverage、obligation、alignment、scenario provenance、mutation、waiver、scores、tier。 | 无 |
| E6 Final audit | 否 | pass | forbidden runner=false；secret scan 未发现 raw key/endpoint/token 模式。 | 无 |

## Final FCSTM

- sha256: `2656aa5d8d2966fc924fc9b123603684d67ace3f139adbf90fe443ca0c8604ac`
- path: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_abs/final_model.fcstm`

```fcstm
def int k1 = 0;
def int k2 = 0;
def int n = 0;
def float slp = 0.0;

state ABSBrakeSupervisor {
    [*] -> increase;

    state increase {
        during { k1 = 1; k2 = 0; n = 0; }
    }

    state hold {
        during { k1 = 0; k2 = 0; n = 0; }
    }

    state decrease {
        during { k1 = 0; k2 = 1; n = 500; }
    }

    increase -> hold : if [slp <= 0.01];
    hold -> increase : if [slp > 0.01];
    hold -> decrease : if [slp < -0.01];
    decrease -> hold : if [slp >= -0.01];
}

```

## Checks

| Check | 结果 | 摘要 |
|---|---|---|
| SD-2 parse | pass | 无 parse error |
| SD-3 semantic | pass | semantic/build ok |
| SD-4 design | pass | blocking=0；advisory=17，均有外部输入或输出角色解释 |
| SD-5A coverage | pass | coverage_gap=false |
| SC-5F freeze | pass | scenario_set=abs-pr-m3-scenarios-v3 |
| SD-6 sim | pass | 5/5 scenarios pass |
| DMR targeted mutants | pass | 5/5 caught |
| Forbidden-call | pass | no forbidden runner invocation |

## Repair / waiver ledger

| 项 | 处理 | 依据 |
|---|---|---|
| `FR-001` | accept | `enter` 改为 `during`，贴合 Figure 6 `du:`；重跑 SD-2/3/4/6 通过 |
| `slp` read-only / guard vars never change | waiver/advisory accepted | `slp` 是外部 plant/PID 输入；添加内部写入会降低忠实度 |
| `k1/k2/n` unreferenced in guards | advisory accepted | 它们是阀门/泵输出，不应为了消警伪造进 guard |

## Scenario / NFRR evidence

### Scenario provenance

| 场景 | 覆盖义务 | provenance | runtime mode | SD-6 |
|---|---|---|---|---|
| S001 | O-001,O-002 | default_prefix | default_runtime | pass |
| S002 | O-002,O-003,O-005,O-009 | external_input_initial_vars | default_runtime | pass |
| S003 | O-002,O-003,O-006,O-009 | reachable_prefix | runtime_hotstart_surrogate | pass |
| S004 | O-003,O-004,O-007,O-009 | reachable_prefix | runtime_hotstart_surrogate | pass |
| S005 | O-003,O-004,O-008,O-009 | reachable_prefix | runtime_hotstart_surrogate | pass |

### Mutation evidence

| mutant | obligation | 变异 | caught |
|---|---|---|---:|
| M001 | O-005 | guard threshold/direction too strict: slp <= 0.01 replaced by slp < -0.01 | True |
| M002 | O-006 | wrong transition target: hold positive branch targets decrease | True |
| M003 | O-004 | wrong effect value: decrease n=500 replaced by n=0 | True |
| M004 | O-007 | guard direction flip: slp < -0.01 replaced by slp > -0.01 | True |
| M005 | O-003 | wrong effect value: hold k1=0 replaced by k1=1 | True |

### NFRR claim

| 字段 | 值 |
|---|---|
| evidence_mode | `NL+paper` |
| scope_type | `full_NL_fragment` |
| obligation_independence | `single_self_assessment` |
| signed_reference | `false` |
| calibration_status | `uncalibrated_candidate_gate` |
| tier_before_cap | `T3` |
| cap_reasons | `IND_SINGLE_SELF_ASSESSMENT`, `NO_HUMAN_SIGNOFF` |
| final_tier | `T2` |
| allowed_use_rule_id | `AU-3` |
| allowed_use | `reviewer_queue` |

### Scores

| Dimension | Score |
|---|---:|
| FE | 3 |
| NGF | 3 |
| REC | 3 |
| GAS | 3 |
| SCB | 3 |
| AAT | 3 |
| BVS | 3 |
| DMR | 2 |

## 质量风险和限制

1. 本报告是 single self-assessment，没有独立 reviewer、人工仲裁或领域专家签核，因此 final tier 被 cap 到 `T2`。
2. 模型只覆盖离散三态 ABS 液压监督器；PID 内部、车轮/车辆连续动力学、AMESim 液压模型和仿真曲线不在 FCSTM 范围内。
3. 当前 SD-6 不支持 step-level 外部输入刷新；中间态场景使用 `runtime_hotstart_surrogate`，但均给出从默认初态可达的 witness 和 `slp` 外部输入 ledger。
4. DMR 是 targeted mutation evidence，不是穷尽式形式证明。

## Reviewer queue 判断

可以进入 reviewer queue。理由：SD-2/3/4/5A/6 全通过，无 unwaived blocking，无 critical contradiction；5 个 obligation-anchored scenario 通过，5 个 targeted mutant 均被抓到。限制是缺少独立签核，不能称为 signed reference 或 final ground truth。
