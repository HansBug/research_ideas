# `method/` 架构与 LG-M1 current facts

本文档是 `project_1_llm_state_machine_modeling/method/` 的架构入口，用于说明当前功能命名、LangGraph 模块化、测试镜像与 historical provenance 的边界。若只想快速知道“现在该从哪里调用”，请先读 [README.md](./README.md) 的功能入口地图；若要追溯 LG-M1 的重构证据链，请继续阅读本文。

相关入口：

- 上游 PR-langgraph：[PR #39](https://github.com/HansBug/research_ideas/pull/39)
- LG-M1 总计划：[PR #64](https://github.com/HansBug/research_ideas/pull/64)
- LG-M1-A inventory 子 PR：[PR #66](https://github.com/HansBug/research_ideas/pull/66)
- LG-M1-B stage API 子 PR：[PR #68](https://github.com/HansBug/research_ideas/pull/68)
- LG-M1-C1 experiments entrypoints 子 PR：[PR #70](https://github.com/HansBug/research_ideas/pull/70)
- LG-M1-C2 ablation / legacy cleanup 子 PR：[PR #72](https://github.com/HansBug/research_ideas/pull/72)
- LG-M1-D1 foundation 子 PR：[PR #69](https://github.com/HansBug/research_ideas/pull/69)
- LG-M1-D2 instrumentation / checkpoint / context 子 PR：[PR #71](https://github.com/HansBug/research_ideas/pull/71)
- LG-M1-D3 nodes / subgraphs / core 子 PR：[PR #74](https://github.com/HansBug/research_ideas/pull/74)
- LG-M1-E tests mirror 子 PR：[PR #75](https://github.com/HansBug/research_ideas/pull/75)
- LG-M1-F docs / provenance 子 PR：[PR #76](https://github.com/HansBug/research_ideas/pull/76)
- LG-M1-A baseline fixture：[tests/fixtures/lg_m1_a_baseline.json](./tests/fixtures/lg_m1_a_baseline.json)
- LG-M1 characterization tests：[tests/crosscutting/test_lg_m1_inventory_characterization.py](./tests/crosscutting/test_lg_m1_inventory_characterization.py)

## 1. Current status summary

当前（LG-M1-F）事实如下：

| 维度 | 当前事实 | 证据 / 入口 |
|---|---|---|
| 默认完整 runtime | `method.loop.run_agent_loop(...)` 仍是 canonical public entry；默认 backend 为 LangGraph full staged runtime | [loop.py](./loop.py)、[langgraph_runtime.py](./langgraph_runtime.py)、[langgraph/core.py](./langgraph/core.py) |
| Stage API | 外部工具箱/skill 应优先调用 `method.stages.*` 的 Pythonic API；这些入口不读 `.env`、不调 provider、不调 full loop | [stages/api.py](./stages/api.py)、[stages/sc_control.py](./stages/sc_control.py)、[stages/sl_prompt_api.py](./stages/sl_prompt_api.py) |
| Experiment entrypoints | 新文档和新代码优先使用 `method.experiments.*` 功能命名入口 | [experiments/](./experiments/) |
| LangGraph physical layout | `method/langgraph/` 已承载 constants/state/registry/checkpointing/instrumentation/subgraphs/nodes/core/resume；`method.langgraph_runtime` 是 public compatibility facade | [langgraph/](./langgraph/)、[langgraph_runtime.py](./langgraph_runtime.py) |
| Tests mirror | `method/tests/` 已按功能域镜像迁移；root flat `test*.py` 已清空 | [tests/](./tests/) |
| 当前测试基线 | `412 tests collected`；full method tests `412 passed, 6 warnings` | LG-M1-E / [PR #75](https://github.com/HansBug/research_ideas/pull/75) 与 LG-M1-F gates |
| 当前 PR 边界 | LG-M1-F 只收口 docs/provenance/naming residue；不改 runtime、prompt、provider、FixLog、run record、eligibility 或真实 evidence | [PR #76](https://github.com/HansBug/research_ideas/pull/76) |
| 下一步 | LG-M1-G 在最终集成 head 上跑四例并做 #64 总复审 | [PR #64](https://github.com/HansBug/research_ideas/pull/64) |

## 2. Public entrypoint architecture

### 2.1 默认 agent-loop 入口

```text
method.loop.run_agent_loop(nl, LoopConfig())
```

该入口保持 Path1/Path2 主实验语义：默认 `experiment_default/full_staged_v1`、默认 LangGraph backend、默认真实 provider adapter（由进程环境变量提供），并写出完整 `AgentLoopRunRecord`。LG-M1 维护性重构不得改变默认 stage 顺序、FixLog、eligibility、provider/stream 纪律或 run-record canonical 字段。

默认 stage graph：

```text
SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SC-12 -> SC-13
```

默认 repair chain：

```text
SD-8 FixRequestBatch -> SL-9 per-request accept/reject + repair -> SL-10(NL + FixLog + local_check_evidence) -> SC-11 -> SD-2 full revalidation
```

### 2.2 Stage / skill API

LG-M1-B 后，skill/toolbox 不需要也不应该直接调用 full loop 来生成 ref model。稳定入口为：

- [stages/api.py](./stages/api.py)：SD/SL/SC stage callable facade 与 stage catalog。
- [stages/sc_control.py](./stages/sc_control.py)：control、stage order、summary helper。
- [stages/sl_prompt_api.py](./stages/sl_prompt_api.py)：`SL-*` prompt generator facade。
- [agent_loop_skill/AGENT_LOOP_SKILL.md](./agent_loop_skill/AGENT_LOOP_SKILL.md)：给 Codex / Claude Code 使用的 repo-local skill 文档。

这些入口的核心约束：不读 `.env`、不调真实 provider、不调用 `method.loop.run_agent_loop(...)` 作为一键 ref-model 生成器；外部 agent 应自行组合 prompt、LLM 调用、SD deterministic tools 与 NFRR/waiver evidence。

### 2.3 Experiment entrypoints 与 compatibility shim

| 功能 | 当前入口 | Compatibility shim | 新文档推荐 |
|---|---|---|---|
| real run matrix / 四例 evidence | [experiments/real_run_matrix.py](./experiments/real_run_matrix.py) | [pr_e1_real_runs.py](./pr_e1_real_runs.py) | 当前入口 |
| checkpoint / resume experiment | [experiments/checkpoint_resume.py](./experiments/checkpoint_resume.py) | [pr_lg_f1_resume_experiment.py](./pr_lg_f1_resume_experiment.py) | 当前入口 |
| representative cases | [experiments/representative_cases.py](./experiments/representative_cases.py) | [pr_d_representative.py](./pr_d_representative.py) | 当前入口 |
| deterministic ablation / replay | [experiments/ablation/deterministic_loop.py](./experiments/ablation/deterministic_loop.py) | [pr2a_loop.py](./pr2a_loop.py) | 当前入口 |

Shim 保留的理由是旧 PR comment reproduction path、历史脚本和 run-record provenance 可能仍引用这些模块。新代码不应把 shim 当作首选入口；删除 shim 需要另开兼容性评估 PR，不能在 F 阶段机械清理。

## 3. LangGraph module layout

LG-M1-D1/D2/D3 后的当前物理结构：

```text
method/langgraph/
├── constants.py                  # runtime / registry identity constants
├── state.py                      # graph state / compatibility state helpers
├── registry.py                   # node registry + consistency checker
├── checkpointing.py              # checkpoint serde / smoke helpers
├── resume.py                     # checkpoint/resume experiment support
├── core.py                       # graph assembly + full staged runtime core
├── nodes/
│   ├── sc.py                     # SC control nodes
│   ├── sd.py                     # SD deterministic nodes
│   └── sl.py                     # SL LLM/prompt nodes
├── subgraphs/
│   ├── context_engineering.py    # context assembly / budget / redaction helper
│   ├── validation.py             # validation subgraph
│   ├── repair.py                 # repair subgraph
│   └── waiver.py                 # waiver subgraph
└── instrumentation/
    ├── common.py
    ├── operator_stream.py
    ├── trace_export.py
    ├── tool_wrappers.py
    ├── retry_timeout.py
    ├── send_parallel.py
    └── store.py
```

[langgraph_runtime.py](./langgraph_runtime.py) 仍然是 public physical facade 与 historical run-record identity 的兼容入口。它可以 re-export 或包装下沉后的实现，但不得被重新膨胀为 monolithic implementation，也不得改变历史 evidence 中的 `environment.runner` / `runtime_implementation` 口径。

## 4. LG-M1 naming provenance

LG-M1-F 不要求把所有 `PR-*` / `LG-*` / `pr_*` 字符串清零。正确处理方式是分类：

| 类别 | 可保留示例 | 保留理由 | 后续策略 |
|---|---|---|---|
| schema/evidence identity | `LG-C1`、`LG-D1`、`LG-E2`、`LG-F1`、`pr-langgraph.stage-nodes.v1` | 已进入 run record、schema version、historical evidence 或 fixture；随意改名会破坏复现 | 保留，并在文档解释不是当前施工残留 |
| compatibility shim | `method.pr_e1_real_runs`、`method.pr_lg_f1_resume_experiment`、`method.pr_d_representative`、`method.pr2a_loop` | 支持旧命令、旧 PR comment reproduction path 与历史脚本 | 新文档优先功能入口；shim 标注 compatibility-only |
| historical PR provenance | `PR-B2`、`PR-C`、`PR-E1`、`PR-E2`、`issue #21`、`PR-3` | 解释 prompt、repair chain、skill、handoff smoke 的来源 | 正文压缩为 provenance；不要写成“当前阶段” |
| test function historical names | `test_pr_e1_*`、`test_lg_m1_*` | 改函数名对学术收益低且可能扰动 characterization baseline | 文件路径已功能化；函数名可保留为 M/backlog |
| frozen baseline fixture | 旧 flat test path、historical scan snapshot | 用于证明迁移前后 path normalization 与 coverage 未丢 | 保留在 fixture / characterization test，并明确 frozen baseline |
| stale misleading path | 旧 flat smoke/test path 作为当前运行命令 | 会误导新读者执行不存在或过时命令 | 必须修正为当前路径，或明确标为 historical evidence |

LG-M1-F 的 scan gate 应覆盖字母型 PR marker 与 hyphen/underscore LG marker，例如：

```bash
rg -n "test_pr|test_lg_m1|pr_[a-z0-9]|PR[-_][A-Za-z0-9][A-Za-z0-9_-]*|LG[-_][A-Za-z0-9][A-Za-z0-9_-]*|issue #|tests/test_" \
  project_1_llm_state_machine_modeling/method \
  -g "*.py" -g "*.md" -g "*.json"
```

验收口径是不要求零命中，但 stale misleading path 必须清零或被解释为 frozen baseline / historical evidence。

## 5. Tests mirror current facts

LG-M1-E 后测试树当前按功能域组织：

```text
method/tests/
├── stages/
├── langgraph/
├── experiments/
├── llm/
├── crosscutting/
├── handoff_smoke/
└── agent_loop_skill/
```

当前 docs/tests-only gate：

```bash
source venv/bin/activate
PYTHONPATH=project_1_llm_state_machine_modeling \
  python -m pytest --collect-only -q project_1_llm_state_machine_modeling/method/tests
PYTHONPATH=project_1_llm_state_machine_modeling \
  python -m pytest -q project_1_llm_state_machine_modeling/method/tests
```

旧 method tests flat path 只允许出现在 frozen baseline / path normalization test 中；不得作为当前运行命令或当前入口出现。

## 6. Historical baseline facts

LG-M1-A 捕获的 baseline 仍是重要 provenance，但它不是当前结构：

- 捕获分支：`feature/project1-lg-m1-a-inventory-characterization`
- baseline source head：`8a5f7bfa9e93008a3b9eec4f7683b594aaee1de8`
- baseline 真源：[tests/fixtures/lg_m1_a_baseline.json](./tests/fixtures/lg_m1_a_baseline.json)
- baseline 范围：inventory + characterization；未读取 `.env`，未调用真实 provider，未生成新的论文主结果 evidence。
- LG-M1-A 原始 collection：`382 tests collected`。
- LG-M1-A 曾记录的 facade scan、stage API scan、legacy loop test 分类、graph contract hash 与 runtime identity 均作为历史迁移锚点保留在 fixture 与 characterization tests 中。

后续子 PR 若改变 public identity、stage semantics、run record canonical 字段、FixLog、eligibility、provider policy 或 historical evidence 解释，必须给出等价性证明或按 #64 四例纪律升级验证。

## 7. LG-M1 sub PR completion map

| 子 PR | 状态 | 核心产物 | 四例策略 |
|---|---|---|---|
| LG-M1-A / [#66](https://github.com/HansBug/research_ideas/pull/66) | ✅ | inventory、ARCHITECTURE skeleton、baseline fixture、characterization tests | 未跑；baseline-only |
| LG-M1-B / [#68](https://github.com/HansBug/research_ideas/pull/68) | ✅ | `method.stages.*` Pythonic API、skill contract / health | 未跑；API/docs-only |
| LG-M1-C1 / [#70](https://github.com/HansBug/research_ideas/pull/70) | ✅ | experiments entrypoints 功能命名 + shim | 未跑；import/CLI equivalence |
| LG-M1-C2 / [#72](https://github.com/HansBug/research_ideas/pull/72) | ✅ | ablation 归位、古老 legacy active API 清理 | 已按用户 override 跑四例 |
| LG-M1-D1 / [#69](https://github.com/HansBug/research_ideas/pull/69) | ✅ | LangGraph constants/state/registry foundation | 未跑；foundation-only |
| LG-M1-D2 / [#71](https://github.com/HansBug/research_ideas/pull/71) | ✅ | instrumentation、checkpointing、context helper | 未跑；focused/historical gates |
| LG-M1-D3 / [#74](https://github.com/HansBug/research_ideas/pull/74) | ✅ | validation/repair/waiver subgraphs、SC/SD/SL nodes、core runtime、facade 收敛 | 已按计划跑四例 |
| LG-M1-E / [#75](https://github.com/HansBug/research_ideas/pull/75) | ✅ | tests mirror、collection gates、old path normalization | 未跑；tests-only |
| LG-M1-F / [#76](https://github.com/HansBug/research_ideas/pull/76) | 🚧 | docs/provenance/naming residue sweep | 不跑；docs/provenance-only |
| LG-M1-G | ⏳ | final integrated evidence、CI/coverage/review closure | 必须跑四例 |

> 表中 emoji 仅表示进度状态：✅ 已完成，🚧 进行中，⏳ 待开始。

## 8. Review / merge risk rules

1. 任何把 compatibility shim 写成当前首选入口的问题，若会误导实验复现，可列 I。
2. 任何删除或改名 schema/evidence identity 的问题，若会破坏 historical run record / fixture / paper evidence 可追溯性，可列 C/I。
3. 任何旧 flat test path 被写成当前命令，若命令不可执行或会误导新 session，可列 I。
4. 纯措辞、风格、函数名历史残留若不影响学术证据链，最高 M。
5. F 阶段不得 source `.env`、不得跑真实 provider、不得修改 `runs/` evidence；G 阶段必须在最终 integrated head 上跑四例。
