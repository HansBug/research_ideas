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

请把所有产物写入：`runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path2_lng_ems`

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
- case_key: `path2_lng_ems`
- path: `path2`
- case_id: `state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship`
- title: `Path2 LNG-ship EMS representative NL`
- NL source: `https://github.com/HansBug/research_ideas/issues/14#issuecomment-4598890799`
- paper_dir: `project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship`
- detected material files:
- `project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/bibtex.bib`
- `project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/STM.md`
- `project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/DESC.md`
- `project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/paper_content.txt`
- `project_1_llm_state_machine_modeling/sources/state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship/paper.pdf`
- selection rationale: Path2 EFSM 压力样本，变量、guard、12 个状态和非法状态明确；是否可作 Path2 主蓝本取决于 state-dependent mode memory。
- variable participation note: `PL/Ppv/Pw/SoC/eng*_Pmax` 是环境输入/容量边界。
- state/mode participation note: 原 NL 的 12 状态主要由瞬时需求/容量条件选择；需防止 state_mode_decorative。

# NL 原文

```text
The LNG-ship EMS manages a ship energy system with PVs, WECs, DGs, LNG, batteries, and time-varying ship loads, issuing cut-in and cut-out commands for generating units and loads. It controls power dispatch between generating units and load demand during changing time periods and operating conditions, dynamically switching states to maintain power balance as resources and demands vary. The FSM reads load demand PL, renewable contributions Ppv and Pw, battery state of charge SoC, and engine capacity bounds such as eng3_Pmax, then returns requested generator power, battery discharge or charging power, and spare power. The twelve finite states are selected by logical transition conditions over demand, generation, capacity, and SoC. When Ppv + Pw covers PL, the EMS serves all ship demand from RES and charges batteries while SoC is below 0.95, or treats residual renewable power as spare once SoC is at least 0.95. When Ppv + Pw is below PL, dispatch follows the stated priority: RES first, batteries when SoC is suitable, LNG before diesel units, and DG1/DG2 only as the last priority. Low-SoC branches add explicit charging margins, including Pgmax/5 in an LNG-covered case and Pd1max/10 in later diesel-generator cases. When PL = 0, RES production is sent to battery charging or to spare power according to SoC thresholds. The overload completion state is illegal: if extreme demand exceeds all RES and thermal resources, EMS activates all thermal generating units, covers the lack by battery discharge, and the state shall never occur in practice.
```

# NL 中文翻译/释义

```text
LNG 船 EMS 管理一个包含光伏、波浪能、柴油机、LNG、电池和随时间变化船舶负载的船舶能源系统，并向发电单元与负载发出切入/切出命令。它在变化的时段和运行条件下控制发电单元与负载需求之间的功率调度，随着资源和需求变化动态切换状态以保持功率平衡。FSM 读取负载需求 PL、可再生贡献 Ppv 和 Pw、电池荷电状态 SoC，以及 eng3_Pmax 等发动机容量边界，然后返回请求的发电机功率、电池放电或充电功率以及备用功率。十二个有限状态由需求、发电、容量和 SoC 上的逻辑转移条件选择。当 Ppv + Pw 覆盖 PL 时，EMS 用 RES 满足全部船舶需求，并在 SoC 低于 0.95 时给电池充电，或在 SoC 至少为 0.95 时把剩余可再生功率视为备用功率。当 Ppv + Pw 低于 PL 时，调度遵循优先级：RES 优先，SoC 合适时使用电池，LNG 先于柴油机，DG1/DG2 只作为最后优先级。低 SoC 分支加入明确充电裕量，包括 LNG 覆盖场景中的 Pgmax/5，以及后续柴油发电机场景中的 Pd1max/10。当 PL = 0 时，RES 产出根据 SoC 阈值送往电池充电或备用功率。过载完成状态是非法状态：若极端需求超过全部 RES 与热力资源，EMS 会激活全部热发电单元并用电池放电弥补缺口，该状态实践中不应发生。
```

请现在执行 PR-M3 codex exec skill 实验，并在最终回答中只给出：output_dir、status、final_model 路径、report 路径、metadata 路径、主要限制。
