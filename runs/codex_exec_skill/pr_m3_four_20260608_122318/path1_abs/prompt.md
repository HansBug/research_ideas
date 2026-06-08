你是 PR-M3 的 codex exec skill 标准实验入口 runner。你的目标不是调用现成顶层 agent-loop，而是像成熟 coding agent 一样读取 repo-local skill/toolbox，自主完成 NL(+paper_dir) -> FCSTM 候选、检查、修复、NFRR 与完整审计报告。

# 硬性边界

1. 必须读取并遵循 repo-local skill 入口：`project_1_llm_state_machine_modeling/method/agent_loop_skill/SKILL.md`（若 symlink 异常则读 `AGENT_LOOP_SKILL.md`）。
2. 必须读取：`e2e_ref_model_guide.md`、`tools.md`、`prompts.md`、`nfrr_evaluation_guide.md`、`codex_exec_experiment_guide.md`。
3. 禁止调用 `method.loop.run_agent_loop(...)`、PR-D representative runner、PR-E1 real-run runner 或任何一键 full staged runner；也不要用它们间接生成模型。
4. 允许使用 `method.stages.api` / `method.stages.sc_control` / `method.stages.sl_prompt_api` / SD deterministic tools / SL prompt generators / pyfcstm utilities / 仓库搜索与论文材料阅读。
5. 不得针对 ABS / CARA / Elevator / LNG 写 lexical special-case；所有 waiver、修复和上下文策略必须是可迁移规则。
6. 不要输出、写入或回显 raw API key、raw endpoint、Bearer token 或 `.env` secret。
7. 若 provider/network/CLI 故障导致无法完成，必须标记 invalid-run，不要伪造模型产物。

# 输出目录

请把所有产物写入：`runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_abs`

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

- run_label: `pr_m3_four_20260608_122318`
- case_key: `path1_abs`
- path: `path1`
- case_id: `abs-fsm-brake-control`
- title: `Path1 ABS three-state brake supervisor`
- NL source: `project_1_llm_state_machine_modeling/eval/data/sources/abs-fsm-brake-control/nl.md`
- paper_dir: `project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control`
- detected material files:
- `project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control/bibtex.bib`
- `project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control/STM.md`
- `project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control/DESC.md`
- `project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control/paper_content.txt`
- `project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control/paper.pdf`
- selection rationale: 三态、guard、state action 均明确，适合检验 parse/semantic/design/sim 是否能走到后段。
- variable participation note: `slp` 是外部/plant 输入型 guard 变量；`k1/k2/n` 是状态动作输出。
- state/mode participation note: 三态本身承担阈值区间模式，状态进入动作决定阀/泵输出。

# NL 原文

```text
The paper implements the single-wheel ABS hydraulic regulator as a three-state FSM coupled with a PID-based slip controller. Wheel speed and vehicle speed are used to compute the slip ratio, and the PID output drives the Stateflow supervisor instead of sending commands directly to the hydraulic valves.

The FSM contains the states `increase`, `hold`, and `decrease`, where `increase` sets `k1=1, k2=0, n=0`, `hold` neutralizes both valves with `k1=0, k2=0, n=0`, and `decrease` sets `k1=0, k2=1, n=500` to release pressure.

The transition guards split the slip-error space into four bands: `increase -> hold` when `slp <= 0.01`, `hold -> increase` when `slp > 0.01`, `hold -> decrease` when `slp < -0.01`, and `decrease -> hold` when `slp >= -0.01`.

This gives a concrete discrete supervisor that maps slip-error thresholds to inlet-valve, return-valve, and pump actions while the continuous wheel-slip dynamics remain in the plant model.
```

# NL 中文翻译/释义

```text
论文把单轮 ABS 液压调节器实现为一个三状态 FSM，并与基于滑移率的 PID 控制器耦合。轮速与车速用于计算滑移率，PID 输出驱动 Stateflow 监督器，而不是直接发送液压阀命令。

FSM 包含 `increase`、`hold`、`decrease` 三个状态：`increase` 设置 `k1=1, k2=0, n=0`，`hold` 设置 `k1=0, k2=0, n=0`，`decrease` 设置 `k1=0, k2=1, n=500` 以释放压力。

转移 guard 把滑移误差空间分成四个区间：`increase -> hold` 当 `slp <= 0.01`，`hold -> increase` 当 `slp > 0.01`，`hold -> decrease` 当 `slp < -0.01`，`decrease -> hold` 当 `slp >= -0.01`。

这给出了一个具体的离散监督器，把滑移误差阈值映射为进油阀、回油阀与泵动作，而连续轮胎滑移动力学仍留在被控对象模型中。
```

请现在执行 PR-M3 codex exec skill 实验，并在最终回答中只给出：output_dir、status、final_model 路径、report 路径、metadata 路径、主要限制。
