# PR-M3 codex exec skill 实验报告: path1_abs

## 1. Run Identity

| 字段 | 值 |
|---|---|
| run_label | `pr_m3_four_clean_20260608_133322` |
| case_key | `path1_abs` |
| case_id | `abs-fsm-brake-control` |
| path | `path1` |
| title | Path1 ABS three-state brake supervisor |
| 输出目录 | `runs/codex_exec_skill/2026-06-08-133322-pr39-pr-m3-codex-exec-skill-final-four-case-evidence/path1-abs-codex-exec-skill-completed` |
| provider config seen | `model_provider=airouter`，仅来自脱敏 `run_manifest.json` / `command.redacted.txt` |
| status | `success` |
| 禁止runner | 未调用顶层agent-loop runtime、PR-D代表性runner、PR-E1真实运行runner或一键full staged runner |

## 2. Input

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

## 3. Actual Reads

| 类型 | 路径 | 用途 |
|---|---|---|
| skill entry | `project_1_llm_state_machine_modeling/method/agent_loop_skill/AGENT_LOOP_SKILL.md` | PR-M3入口、禁止项、stage顺序 |
| guide | `project_1_llm_state_machine_modeling/method/agent_loop_skill/e2e_ref_model_guide.md` | E0-E7、paper读取顺序、scenario provenance |
| guide | `project_1_llm_state_machine_modeling/method/agent_loop_skill/tools.md` | SD工具API |
| guide | `project_1_llm_state_machine_modeling/method/agent_loop_skill/prompts.md` | SL repair/review口径 |
| guide | `project_1_llm_state_machine_modeling/method/agent_loop_skill/nfrr_evaluation_guide.md` | NFRR v3评分与tier |
| guide | `project_1_llm_state_machine_modeling/method/agent_loop_skill/codex_exec_experiment_guide.md` | PR-M3 artifact和report要求 |
| tool API | `project_1_llm_state_machine_modeling/method/stages/api.py` | skill-facing facade |
| tool API | `project_1_llm_state_machine_modeling/method/stages/sd_tools.py` | SD-2/3/4/5A/SC-5F/SD-6实现 |
| schema/runtime | `project_1_llm_state_machine_modeling/method/schema.py`、`method/feedback/sim.py`、`method/feedback/parse.py` | scenario和反馈schema |
| examples | `project_1_llm_state_machine_modeling/method/tests/stages/test_sd_tools.py`、`method/tests/experiments/test_scenario_normalization.py` | 当前parser/sim语义确认 |
| input | `project_1_llm_state_machine_modeling/eval/data/sources/abs-fsm-brake-control/nl.md` | NL原文 |
| paper | `project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control/bibtex.bib` | 元信息 |
| paper | `project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control/STM.md` | 状态机整理、Figure 6摘录 |
| paper | `project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control/DESC.md` | 中文论文边界 |
| paper | `project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control/paper_content.txt` | PDF正文提取物 |
| runner-owned redacted | `command.redacted.txt`、`env.redacted.json`、`run_manifest.json`、`prompt.md` | 只读脱敏上下文，不修改 |

`paper.pdf` 被检测到但未直接打开；本次 `paper_content.txt`、`STM.md` 和 `DESC.md` 已能交叉确认 Figure 6 状态机和正文边界，未出现需要回看PDF原文的提取异常。

## 4. Grounding Summary

| 元素 | 证据 | 建模处理 |
|---|---|---|
| 三态 `increase/hold/decrease` | NL、STM摘录C、paper Figure 6说明 | exact state |
| `increase` action | NL、STM摘录C | enter: `k1=1; k2=0; n=0` |
| `hold` action | NL、STM摘录C | enter: `k1=0; k2=0; n=0` |
| `decrease` action | NL、STM摘录C | enter: `k1=0; k2=1; n=500` |
| 四条guard | NL、STM摘录C | exact guards |
| `slp` | NL-2/NL-5、paper_content Page 5 | external/PID/plant input |
| 连续动力学 | NL-5、paper正文 | out of FCSTM scope |
| `ABS` root state | pyfcstm结构需要 | synthetic wrapper，不是论文新增模式 |

## 5. Process Summary

| Stage | 是否LLM | 轮次 | 结果 | 关键反馈 | 处理 |
|---|---:|---:|---|---|---|
| E0 skill discovery | 否 | 1 | pass | `SKILL.md`未列出，读取等价入口 `AGENT_LOOP_SKILL.md` | 记录actual reads |
| E1 grounding | 否 | 1 | pass | 论文/NL明确三态、动作、四条guard | 抽取obligations |
| E2 modeling | 否 | 1 | pass | 使用 `def int` / `def float`，不使用bool | 生成final DSL |
| SD-2 parse | 否 | 1 | pass | parser接受 | 无修改 |
| SD-3 semantic | 否 | 1 | pass | build成功 | 无修改 |
| SD-4 design | 否 | 1 | pass with advisory | `k1/k2/n`为output-only，`slp`为external input | waiver ledger |
| SD-5A/SD-6 | 否 | 1 | fail | 初版scenario少了默认init cycle | 修复scenario前缀 |
| SD-5A/SC-5F/SD-6 | 否 | 2 | pass | 4个scenario全部通过，oracle_weak=false | 冻结scenario证据 |
| NFRR | 否 | 1 | T2 | single self assessment cap | 可进reviewer queue |
| Final audit | 否 | 1 | pass | producer-owned文件齐全 | 写report/metadata |

## 6. Checks

| 检查 | 结果 | 说明 |
|---|---|---|
| SD-2 parse | pass | `final_model.fcstm` parse ok |
| SD-3 semantic | pass | build ok |
| SD-4 design | pass with advisory | 无blocking；advisory均有waiver |
| SD-5A coverage | pass | 修复后coverage_gap=false |
| SC-5F freeze | pass | `scenario-set-1bfac7d12d1d` |
| SD-6 sim | pass | 4/4 scenarios pass，oracle_weak=false |
| forbidden runner | pass | 未调用禁止runner |

## 7. Repair / Waiver

| 项 | 决策 | 依据 | 结果 |
|---|---|---|---|
| FR-001 scenario prefix | accept | 初版SD-6失败来自默认init cycle语义，不是DSL错误 | scenario修复，DSL不变 |
| `k1/k2/n` unreferenced | waiver | 论文把它们定义为阀/泵输出，不应为了消警删掉或放进guard | accepted |
| `slp` unwritten/read-only | waiver | slp来自PID/plant侧，FCSTM只读取guard | accepted |
| guard vars never change | waiver | 所有guard变量都是外部slp输入 | accepted |

## 8. NFRR Summary

| 字段 | 值 |
|---|---|
| evidence_mode | `NL+paper` |
| scope_type | `full_NL_fragment` |
| obligation_independence | `single_self_assessment` |
| scores | FE=3, NGF=3, REC=3, GAS=3, SCB=3, AAT=3, BVS=3, DMR=2 |
| tier_before_cap | `T3` |
| cap_reasons | `IND_SINGLE_SELF_ASSESSMENT`, `NO_HUMAN_SIGNOFF` |
| final_tier | `T2` |
| allowed_use | `reviewer_queue` |
| calibration_status | `uncalibrated_candidate_gate` |
| signed_reference | false |

4个主场景均为obligation-anchored oracle，未使用model-derived oracle。3个中间状态场景使用 `runtime_hotstart_surrogate`，均给出从默认初态可达的prefix witness和state snapshot justification，因此计入主BVS；这仍是当前SD-6 runtime限制下的近似执行证据，不等同于人工签核。

## 9. Final FCSTM

```fcstm
def int k1 = 0;
def int k2 = 0;
def int n = 0;
def float slp = 0.0;

state ABS {
    [*] -> increase;
    state increase { enter { k1 = 1; k2 = 0; n = 0; } }
    state hold { enter { k1 = 0; k2 = 0; n = 0; } }
    state decrease { enter { k1 = 0; k2 = 1; n = 500; } }
    increase -> hold : if [slp <= 0.01];
    hold -> increase : if [slp > 0.01];
    hold -> decrease : if [slp < -0.01];
    decrease -> hold : if [slp >= -0.01];
}
```

final_model_sha256: `2c0a3a5d240e75ed458fac0039a7b722979034909cf283d0306c6332e2681397`

## 10. Quality Risks and Limits

1. `slp` 是外部/PID/plant输入。FCSTM不模拟轮速、车速、滑移率计算或PID更新，因此下游仿真必须通过外部输入或环境层提供 `slp`。
2. `ABS` root state 是 pyfcstm wrapper，不是论文 Figure 6 中额外定义的模式。
3. SD-6 当前不支持step-level变量刷新；3个中间状态场景使用带reachable-prefix witness的 runtime hot-start surrogate。
4. 本次NFRR是 single self assessment，没有独立reviewer仲裁，也没有领域专家签核，因此只能到 `T2 reviewer_queue`，不能称为 signed reference 或 T3 paper-grounded candidate。

## 11. Reviewer Queue Decision

结论：可以进入 reviewer queue。理由是 final model 已覆盖输入NL的三态、三组动作、四条guard和外部输入边界，SD-2/3/4/5A/6均达到最低准出要求；但由于缺少独立仲裁和人工签核，不能作为最终ground truth发布。
