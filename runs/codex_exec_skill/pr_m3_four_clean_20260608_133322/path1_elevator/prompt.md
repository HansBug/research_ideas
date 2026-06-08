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

请把所有产物写入：`runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_elevator`

你只负责生成 producer-owned 产物；以下 runner-owned 文件由外部 harness 生成和回写，你不得创建、覆盖或修改：`prompt.md`、`command.redacted.txt`、`env.redacted.json`、`codex_events.jsonl`、`codex_stdout.log`、`codex_stderr.log`、`codex_transcript.redacted.md`、`run_manifest.json`、`forbidden_call_check.json`、`redaction_report.json`、`run_summary.md`。

必须至少生成以下 producer-owned 文件（缺一项都要在 report 中解释）：

```text
final_model.fcstm
report.md
metadata.json
actual_file_reads.json
tool_stage_check_ledger.json
repair_ledger.json
nfrr_report.json
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
| E6 final audit | 写 `report.md`、`metadata.json` 与 producer-owned ledgers；不要写 runner-owned audit files，外部 harness 会生成 `run_summary.md`、forbidden-call 与 redaction 结果。 |

# Case metadata

- run_label: `pr_m3_four_clean_20260608_133322`
- case_key: `path1_elevator`
- path: `path1`
- case_id: `automatic-elevator-controller`
- title: `Path1 automatic elevator controller`
- NL source: `project_1_llm_state_machine_modeling/eval/data/sources/automatic-elevator-controller/nl.md`
- paper_dir: `project_1_llm_state_machine_modeling/sources/automatic-elevator-controller`
- detected material files:
- `project_1_llm_state_machine_modeling/sources/automatic-elevator-controller/bibtex.bib`
- `project_1_llm_state_machine_modeling/sources/automatic-elevator-controller/STM.md`
- `project_1_llm_state_machine_modeling/sources/automatic-elevator-controller/DESC.md`
- `project_1_llm_state_machine_modeling/sources/automatic-elevator-controller/paper_content.txt`
- `project_1_llm_state_machine_modeling/sources/automatic-elevator-controller/paper.pdf`
- selection rationale: 楼层态、运动态、请求事件、到位传感事件与 reset 都明确，适合检验事件建模和 forced fallback。
- variable participation note: `PS*`/`S*`/`reset` 更适合按事件建模；`hbrg` 是纯输出动作。
- state/mode participation note: 楼层态和运动态直接承担 mode memory；请求/到位事件驱动状态迁移。

# NL 原文

```text
The automatic elevator controller is built as a finite-state machine whose state space combines floor states `F1`, `F2`, and `F3` with motion states `MU2`, `MU3`, `MD1`, and `MD2` for upward and downward travel.

In the normal workflow, the system starts from an ideal state on floor 1, chooses either the up or down branch according to floor requests, stops at the requested floor, and then immediately checks the next destination before deciding whether to continue moving.

The controller uses `PS1/PS2/PS3` as floor-request inputs and `S1/S2/S3` as sensing inputs for arrival. From `F1`, `PS2` triggers `MU2` and `PS3` triggers `MU3`. From `F2`, `PS3` triggers `MU3` and `PS1` triggers `MD1`. From `F3`, `PS1` triggers `MD1` and `PS2` triggers `MD2`. Arrival sensors complete motion transitions: `MU2 + S2 -> F2`, `MU3 + S3 -> F3`, `MD1 + S1 -> F1`, and `MD2 + S2 -> F2`.

The `hbrg` output distinguishes upward drive, downward drive, and stop conditions. A reset signal forces the controller back to floor 1 regardless of the outstanding request context.
```

# NL 中文翻译/释义

```text
自动电梯控制器被构建为有限状态机，其状态空间由楼层状态 `F1`、`F2`、`F3` 与上/下行运动状态 `MU2`、`MU3`、`MD1`、`MD2` 组合而成。

正常流程中，系统从 1 楼理想状态开始，根据楼层请求选择上行或下行分支，在请求楼层停止，然后立即检查下一目的地以决定是否继续移动。

控制器使用 `PS1/PS2/PS3` 作为楼层请求输入，使用 `S1/S2/S3` 作为到位传感输入。从 `F1`，`PS2` 触发 `MU2`，`PS3` 触发 `MU3`；从 `F2`，`PS3` 触发 `MU3`，`PS1` 触发 `MD1`；从 `F3`，`PS1` 触发 `MD1`，`PS2` 触发 `MD2`。到位传感器完成运动转移：`MU2 + S2 -> F2`，`MU3 + S3 -> F3`，`MD1 + S1 -> F1`，`MD2 + S2 -> F2`。

`hbrg` 输出区分上行驱动、下行驱动和停止状态。复位信号会无视当前请求上下文，强制控制器回到 1 楼。
```

请现在执行 PR-M3 codex exec skill 实验，并在最终回答中只给出：output_dir、status、final_model 路径、report 路径、metadata 路径、主要限制。
