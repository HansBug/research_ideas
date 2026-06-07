# `method/` current status

> **当前锚点（2026-06-08，LG-M1-F）**：本文件现在作为 `method/` 的状态总账与历史索引。新读者应优先读取 [README.md](./README.md) 与 [ARCHITECTURE.md](./ARCHITECTURE.md)，再把本文件用于确认当前 PR 阶段和历史 sprint provenance。
>
> **注意**：下方 “Historical sprint record” 保留 2026-05-26 至 PR-E1/PR-E2/PR-3 的早期记录，用于追溯 agent-loop 设计来源；其中的 `dev/method-agent-implementation`、PR #11、Phase A-J 等不再是当前 LG-M1 推荐入口或当前施工分支。

## 1. LG-M1 current overlay

| 子 PR | 状态 | 当前事实 | 验收 / 四例口径 |
|---|---|---|---|
| LG-M1-A / [PR #66](https://github.com/HansBug/research_ideas/pull/66) | ✅ | inventory、baseline fixture、characterization tests 已建立 | baseline-only，不跑四例 |
| LG-M1-B / [PR #68](https://github.com/HansBug/research_ideas/pull/68) | ✅ | `method.stages.api`、`method.stages.sc_control`、`method.stages.sl_prompt_api` 与 skill health 已落地 | API/docs-only，不跑四例 |
| LG-M1-C1 / [PR #70](https://github.com/HansBug/research_ideas/pull/70) | ✅ | `method.experiments.real_run_matrix`、`checkpoint_resume`、`representative_cases` 功能入口已落地，旧 `pr_*` shim 保留 | import/CLI equivalence，不跑四例 |
| LG-M1-C2 / [PR #72](https://github.com/HansBug/research_ideas/pull/72) | ✅ | `experiments/ablation/deterministic_loop.py` 已落地，古老 `legacy_loop` active API 已清理 | 已按用户 override 跑四例 |
| LG-M1-D1 / [PR #69](https://github.com/HansBug/research_ideas/pull/69) | ✅ | `method/langgraph/{constants,state,registry}.py` foundation 已落地 | foundation-only，不跑四例 |
| LG-M1-D2 / [PR #71](https://github.com/HansBug/research_ideas/pull/71) | ✅ | instrumentation、checkpointing、context helper 已下沉到 `method/langgraph/` | focused/historical gates，不跑四例 |
| LG-M1-D3 / [PR #74](https://github.com/HansBug/research_ideas/pull/74) | ✅ | validation/repair/waiver subgraphs、SC/SD/SL nodes、core runtime、facade 收敛已完成 | 已按计划跑四例 |
| LG-M1-E / [PR #75](https://github.com/HansBug/research_ideas/pull/75) | ✅ | `method/tests/` 已按功能域镜像迁移；root flat `test*.py` 清空 | `412 tests collected` / `412 passed, 6 warnings`；不跑四例 |
| LG-M1-F / [PR #76](https://github.com/HansBug/research_ideas/pull/76) | 🚧 | README / ARCHITECTURE / STATUS / skill / handoff docs provenance 收口 | docs/provenance scan + method tests；不跑四例 |
| LG-M1-G | ⏳ | 最终 integrated evidence、CI/coverage/comment、三路 review closure | 必须在最终 head 上跑四例 |

> 表中 emoji 仅表示进度状态：✅ 已完成，🚧 进行中，⏳ 待开始。

当前 method tests baseline：

```bash
source venv/bin/activate
PYTHONPATH=project_1_llm_state_machine_modeling \
  python -m pytest --collect-only -q project_1_llm_state_machine_modeling/method/tests
PYTHONPATH=project_1_llm_state_machine_modeling \
  python -m pytest -q project_1_llm_state_machine_modeling/method/tests
```

预期为 `412 tests collected`，full method tests 通过。LG-M1-F 不应 source `.env`、不应调用 provider、不得提交 `runs/` 真实 run artifact。

## 2. Current recommended entrypoints

| 用途 | 当前入口 | 不推荐作为新入口的历史路径 |
|---|---|---|
| 默认 full staged runtime | `method.loop.run_agent_loop(...)` | 旧 A0-A4 `method.legacy_loop` |
| Stage deterministic / control tools | `method.stages.api`、`method.stages.sc_control` | 直接抄旧 PR 命名 helper |
| SL prompt facade | `method.stages.sl_prompt_api` | 在 skill 中直接调用 full loop |
| Real run matrix | `method.experiments.real_run_matrix` | `method.pr_e1_real_runs` |
| Checkpoint / resume | `method.experiments.checkpoint_resume` | `method.pr_lg_f1_resume_experiment` |
| Representative cases | `method.experiments.representative_cases` | `method.pr_d_representative` |
| Deterministic ablation | `method.experiments.ablation.deterministic_loop` | `method.pr2a_loop` |
| LangGraph implementation | `method.langgraph.*` + `method.langgraph_runtime` facade | 把 `langgraph_runtime.py` 重新当作 monolith 编辑 |
| Tests | `method/tests/{stages,langgraph,experiments,llm,crosscutting,handoff_smoke,agent_loop_skill}` | 旧 method tests flat path |

## 3. Provenance handling rule

- `PR-*`、`issue #*`、`LG-*`、`pr_*` 可以作为 historical provenance / schema identity / compatibility shim 保留。
- 新文档、新代码、新测试路径应优先使用功能命名。
- 已写入 run record、schema version、historical fixture 的名称不得为了“去施工名”而机械改名。
- 旧 flat test path 若只存在于 [tests/crosscutting/test_lg_m1_inventory_characterization.py](./tests/crosscutting/test_lg_m1_inventory_characterization.py) 的 frozen path-normalization map 中，可保留；若作为当前命令出现，必须修正。

## 4. Historical sprint record（保留，不代表当前入口）

以下内容是早期 `method/` 共同基础 sprint 的历史记录，保留用于解释 agent-loop 的设计来源、prompt/stage 演化与早期验证证据。当前 LG-M1 维护性阶段不应把这些分支名、Phase 名或旧命令当作当前 recommended entrypoint。

### PR-E1 状态补充（issue #21，2026-06-03）

PR-E1 在 PR-C/PR-D 默认入口基础上调整 repair 子架构与真实运行证据链：

- `LoopConfig()` 默认解析为 `experiment_default/full_staged_v1`，包含 full staged stage switches、feedback/budget/scenario/LLM/record/eligibility policy 与 condition hash。
- `method.loop.run_agent_loop()` 不再调用旧 A0-A4 implementation，也不再停留在 PR-A contract-only façade；默认执行 full staged runtime。
- 默认 `LoopConfig()` 使用 real-env LLM provider adapter；缺 provider 配置、provider retry exhaustion 或 schema invalid 会写出 run record 并以 `provider_error` / `invalid` 退出，不回退 fake。
- planned stage graph 更新为 `SC-0/SL-1/SD-2/SD-3/SD-4/SL-5/SD-5A/SC-5F/SD-6/SL-7/SD-8/SL-9/SL-10/SC-11/SC-12/SC-13`。
- run record 记录 resolved config / environment / provider-model 脱敏标识 / stage_records / iteration_records / llm_interactions / deterministic_feedback / repair_history / fix_log / scenario_history / logs / final_artifacts / redaction_report。
- PR-E1 负责四例真实 agent-loop 重跑、NFRR v3 质量诊断与 reviewer 闭环；当时不声明模型质量已达到高可信主结果。

### PR-B2 状态补充（issue #21，2026-06-02）

PR-B2 交付真实/mock LLM stage execution units，但仍不切默认 full runtime：

- `llm_stages.py` 封装 `SL-1/SL-5/SL-7/SL-9/SL-10` 的默认 provider adapter、schema/empty/provider retry 与 interaction record；旧 `SL-10B` 保留为 legacy/ablation。
- 默认真实 provider 通过 `method.gpt_client` 读取进程环境变量；单元测试使用 `MockLLMProvider`，不依赖真实 API。
- LLM retry 只处理 provider/network/schema-invalid/empty-output；deterministic feedback failure 不在 PR-B2 中 retry。
- `SL-9` repair prompt 保留 `suggested_fix` 作为 hint，不强制照抄，允许 LLM 基于 NL 与全局约束给出更合理修复。
- interaction payload 记录 prompt、raw output、parsed output、usage、provider/model、attempts、retry error、schema validation、hash 与脱敏报告。

### 早期 Phase A-J 总览（2026-05-26 sprint）

| Phase | 历史内容 | 历史状态 |
|---|---|---|
| A | 脚手架 + pyfcstm submodule + 目录骨架 + README + STATUS | ✅ |
| B | `gpt_client.py` 统一 LLM client + `schema.py` dataclass | ✅ |
| C | single-prompt modeling：SpecExtractor / Modeler / Repair | ✅ |
| D | parse + semantic feedback wrappers | ✅ |
| E | loop.py 主驱动 + gated cascade + repair | ✅ |
| F | multi-step modeling 模块 | ✅ |
| G | model test scenario generation + sim feedback | ✅ |
| H | judge feedback adapter | sprint 跳过 |
| I | Path 1 评测基础设施 | ✅ |
| J | 端到端验收 | 由 path branch 承接 |

### 早期 sim / scenario framing

早期 Phase G 的核心结论是：单靠 sim 跑空 cycle 只能验证“不死锁 / 状态可达”；要验证“model 行为是否符合 NL 需求”，必须构造 `NL 需求 -> expected behavior scenario -> sim 执行验证` 的 oracle 链。该 framing 后续进入 `SD-6` / NFRR scenario provenance 的学术边界。

### 历史 commit 摘要

| commit / 阶段 | 描述 |
|---|---|
| `6e...` | Phase A-C：脚手架 + pyfcstm submodule + 3 single-prompt agent + 端到端 smoke 跑通 |
| `2447ad8a` | Phase D：parse + semantic feedback wrappers |
| `f28c99b2` | Phase F：multi-step MTI 端到端跑通 |
| `de67d131` | Phase G：scenarios 重定位为 bug-finding probes + mutation differential |
| `1f26ff4c` | Phase E v1：agent loop driver + cascaded Repair + ablation 支持 |
| `255c0af9` | Phase E v2：fix prompt context + grammar reference |
| `06536876` | Phase E v3：scenariogen 自管 cycle 一致性 + mutation self-validation |
| `ff1e90ff` | Phase I：`eval/` LLM 初审 + 人类签字 + audit-trail 评测基础设施 |
