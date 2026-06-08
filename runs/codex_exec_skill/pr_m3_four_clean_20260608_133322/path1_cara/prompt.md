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

请把所有产物写入：`runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_cara`

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
- case_key: `path1_cara`
- path: `path1`
- case_id: `cara-infusion-pump-formal-spec__01`
- title: `Path1 CARA representative NL`
- NL source: `https://github.com/HansBug/research_ideas/issues/14#issuecomment-4598890685`
- paper_dir: `project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`
- detected material files:
- `project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/bibtex.bib`
- `project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/STM.md`
- `project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/DESC.md`
- `project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper_content.txt`
- `project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf`
- selection rationale: issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。
- variable participation note: 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强。
- state/mode participation note: Manual/Ask_StartAC/Autocontrol/PumpFault 状态承担模式记忆与故障恢复语义。

# NL 原文

```text
At run time, CARA coordinates the Caregiver Interface, Blood Pressure Monitor, Algorithm, and Pump Monitors around an infusion pump that moves fluid into the patient, while sensor readings are stored in a shared buffer for software access. The pump has manual and autocontrol modes. In manual mode, pump speed is set with the built-in switch and the caregiver sets a default flow rate directly on the pump for manual operation, while in autocontrol mode pump speed is set by a control voltage from an external source. The Algorithm component controls infusion rate and records infusion-related data in log files; patient blood pressure is used to compute the infusion rate, with higher pressure producing a lower flow rate. The Caregiver Interface lets the caregiver modify target blood pressure and initiate or terminate algorithmic pump control, and it also displays and sounds error messages. In the Mode_Control_Algorithm hierarchy, CARA has manual and autocontrol-related mode-control states plus an Ask_StartAC submode; within Ask_StartAC, the setpoint can be changed and pressing StartAC enters AutocontrolInit. During normal autocontrol, CARA controls flow rate only while there are no pump-operation complications. If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals, the caregiver removes the fault, and when CARA was controlling the pump the software releases control. As a cross-component fallback, CA_backManual or any of CB_backManual, CP_backManual, or CC_backManual causes CA_mode to become Manual, making manual operation the shared recovery target.
```

# NL 中文翻译/释义

```text
运行时，CARA 围绕一台向患者输液的输液泵协调 Caregiver Interface、Blood Pressure Monitor、Algorithm 与 Pump Monitors，传感器读数会写入共享缓冲区供软件访问。泵具有手动和自动控制两种模式。手动模式下，泵速由内置开关设置，护理人员直接在泵上设置默认流量；自动控制模式下，泵速由外部控制电压设置。Algorithm 组件控制输液速率并记录输液相关日志；患者血压用于计算输液速率，血压越高流量越低。Caregiver Interface 允许护理人员修改目标血压，并启动或终止算法泵控制，同时显示和发出错误消息。在 Mode_Control_Algorithm 层次中，CARA 具有手动与自动控制相关的模式控制状态以及 Ask_StartAC 子模式；在 Ask_StartAC 中可以修改设定点，按下 StartAC 会进入 AutocontrolInit。正常自动控制期间，只有没有泵操作并发症时 CARA 才控制流量。如果出现输液管堵塞等泵故障，泵会激活报警信号，护理人员排除故障；当 CARA 正在控制泵时，软件会释放控制。作为跨组件回退，CA_backManual 或 CB_backManual、CP_backManual、CC_backManual 中任一事件都会使 CA_mode 变为 Manual，使手动操作成为共享恢复目标。
```

请现在执行 PR-M3 codex exec skill 实验，并在最终回答中只给出：output_dir、status、final_model 路径、report 路径、metadata 路径、主要限制。
