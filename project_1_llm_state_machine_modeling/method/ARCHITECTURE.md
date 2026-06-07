# `method/` 架构与 LG-M1-A 基线

本文档是 LG-M1-A 的仓库内架构入口与 baseline 真源说明，服务于 LG-M1 后续维护性重构。LG-M1-A 只记录当前事实和后续目标边界，不迁移模块、不删除旧实现、不改变默认 runtime 语义、不运行真实 provider 四例。

相关入口：

- 上游 PR-langgraph：[PR #39](https://github.com/HansBug/research_ideas/pull/39)
- LG-M1 总计划：[PR #64](https://github.com/HansBug/research_ideas/pull/64)
- LG-M1-A 子 PR：[PR #66](https://github.com/HansBug/research_ideas/pull/66)
- 仓库内 baseline fixture：[tests/fixtures/lg_m1_a_baseline.json](./tests/fixtures/lg_m1_a_baseline.json)
- 表征测试：[tests/test_lg_m1_a_inventory_characterization.py](./tests/test_lg_m1_a_inventory_characterization.py)

## Current Facts

本节只记录 LG-M1-A 实现时的当前磁盘事实与可观察合约，不描述未来目标结构。后续 LG-M1-B..G 若改变这些事实，必须在对应子 PR 中说明原因、更新 baseline 或给出兼容证明。

### 基线捕获信息

- 捕获分支：`feature/project1-lg-m1-a-inventory-characterization`
- baseline source head：`8a5f7bfa9e93008a3b9eec4f7683b594aaee1de8`（LG-M1-A 空 PR head；fixture 还包含本 PR 新增 characterization test 后的 working-tree collection count，最终实现 commit 以 PR head 与实现 comment 为准，不在文件内伪造自引用 hash）
- baseline 真源：[`tests/fixtures/lg_m1_a_baseline.json`](./tests/fixtures/lg_m1_a_baseline.json)
- baseline 范围：inventory + characterization baseline；未读取 `.env`，未调用真实 provider，未生成新的论文主结果 evidence。
- pytest collection 基线：`382` tests collected，scope 为 `project_1_llm_state_machine_modeling/method/tests`。

### 当前顶层文件事实

`method/` 当前仍同时包含运行入口、实验入口、LangGraph runtime、legacy loop、stage helper、skill 文档和测试目录。LG-M1-A 不移动这些文件，只记录当前事实：

- 默认公开入口：[`loop.py`](./loop.py)
- 当前 LangGraph runtime 单文件入口：[`langgraph_runtime.py`](./langgraph_runtime.py)
- 当前 legacy loop：[`legacy_loop.py`](./legacy_loop.py)
- 当前 ablation / deterministic experiment 入口：[`pr2a_loop.py`](./pr2a_loop.py)（LG-M1-C2 后续处理）
- 当前真实 run matrix 功能入口：[`experiments/real_run_matrix.py`](./experiments/real_run_matrix.py)；legacy shim：[`pr_e1_real_runs.py`](./pr_e1_real_runs.py)
- 当前 representative cases 功能入口：[`experiments/representative_cases.py`](./experiments/representative_cases.py)；legacy shim：[`pr_d_representative.py`](./pr_d_representative.py)
- 当前 checkpoint / resume experiment 功能入口：[`experiments/checkpoint_resume.py`](./experiments/checkpoint_resume.py)；legacy shim：[`pr_lg_f1_resume_experiment.py`](./pr_lg_f1_resume_experiment.py)
- stage Python 模块目录：[`stages/`](./stages/)
- method tests 目录：[`tests/`](./tests/)

### Facade / re-export 当前事实

LG-M1-A 的 facade scan 记录当前所有 `method.langgraph_runtime` direct import、module alias import 与 alias attribute consumer。该 scan 的目的不是冻结私有 helper 的存在性，而是让 LG-M1-D1/D2/D3 在拆分 `langgraph_runtime.py` 时能审计已有 consumer surface。

关键事实：

- direct / module import entries：`61`
- alias attribute consumers：`27`
- 必须纳入 scan 的 re-export /入口路径：
  - [`__init__.py`](./__init__.py)
  - [`loop.py`](./loop.py)
  - [`staged_runtime.py`](./staged_runtime.py)
- 当前默认入口 [`loop.py`](./loop.py) 直接使用 `method.langgraph_runtime` 的 context assembly 与 `run_full_staged_langgraph_runtime`。

完整清单以 [`tests/fixtures/lg_m1_a_baseline.json`](./tests/fixtures/lg_m1_a_baseline.json) 的 `facade_reexport_scan` 为准。

### Stage API 当前事实

LG-M1-A 只盘点已存在的 `method.stages.*` Python-callable surface，不承诺尚未存在的 skill/toolbox API。当前 scan 覆盖 `17` 个 stage 模块，完整函数 / class / 常量清单见 fixture 的 `stage_api_scan`。

后续 LG-M1-B 若新增 `api.py`、`sc_control.py` 或 prompt-oriented Pythonic API，必须保证：

1. 不把当前不存在的 API 回填为“历史已有”。
2. 不改变 SC/SD/SL 语义、FixLog、NFRR / eligibility 或默认 provider 行为。
3. 保留可供 skill 直接调用的 Pythonic entrypoint。

### Legacy loop 当前事实

当前 active code 中 `method.legacy_loop` 的直接 import/use 主要集中在 [`tests/test_pr0_stage_contract.py`](./tests/test_pr0_stage_contract.py)，同时 [`loop.py`](./loop.py) 仅在错误信息中提及 legacy diagnostic path。

LG-M1-A 将 `test_pr0_stage_contract.py` 划分为：

- 总 test 数：`53`
- 直接依赖 `legacy_loop` 的 legacy-only test：`7`
- 不直接依赖 `legacy_loop` 的 stage/schema/contract test：`46`

这一区分是 LG-M1-C2 删除古老 legacy loop 的边界：C2 可以删除或迁移 legacy-only coverage，但不得默默丢失非 legacy stage/schema/contract coverage。

### Runtime identity 当前事实

LG-M1-A 的 runtime identity 真源来自已提交的 historical agent-loop gzip run record；该 record 只作为只读证据来源，LG-M1-A 不 replay provider、不读取 `.env`、不新增真实四例 evidence。

- 真源路径：[`../../runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4/pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4.agent_loop.json.gz`](../../runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4/pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4.agent_loop.json.gz)
- `environment.runner`：`method.langgraph_runtime.run_full_staged_langgraph_runtime`
- `environment.loop_entrypoint`：`method.loop.run_agent_loop`
- `environment.graph_runtime_backend`：`langgraph`
- `environment.graph_runtime_id`：`langgraph:pr-langgraph.stategraph.v1`
- `environment.node_edge_schema_version`：`pr-langgraph.stage-nodes.v1`
- `run_config.runtime_implementation`：`method.langgraph_runtime.run_full_staged_langgraph_runtime`
- `run_config.canonical_runtime_backend`：`langgraph`

完整字段见 fixture 的 `runtime_identity`。后续 LG-M1-D1/D2/D3 若调整物理模块位置，必须保持这些对外 identity / evidence 字段兼容，或在对应子 PR 中给出明确迁移与证据口径说明。

### Graph contract 当前事实

当前 graph contract baseline 来自 `build_langgraph_node_registry()`、`build_planned_stage_graph(LoopConfig())` 与 `graph_registry_consistency(...)` 的稳定字段。

- canonical hash：`sha256:38cd757393d04422de98bb60c6d0534833f1b97dd00ffc70062bd040610d6a45`
- registry runtime backend：`langgraph`
- opaque wrapper：`false`
- delegated monolithic runtime：`false`
- planned stage order 与 registry canonical stage sequence 一致。
- hash 排除：timestamp、绝对临时路径、dict insertion 偶然顺序、raw provider output、secret。

完整 registry dump、planned node / edge / stage order、schema/version metadata 与 consistency 结果见 fixture 的 `graph_contract`。

### Experiment / CLI 当前事实

LG-M1-A 对当前实验入口只做 import smoke 与 `--help` / argparse 层面的 no-provider baseline，不执行真实 provider run：

| 模块 | 当前 baseline | Provider 调用 |
| --- | --- | --- |
| `method.pr_e1_real_runs` | legacy shim import ok，`--help` exit 0 | 否 |
| `method.experiments.real_run_matrix` | 功能命名入口 import ok，`--help` exit 0 | 否 |
| `method.pr_lg_f1_resume_experiment` | legacy shim import ok，`--help` exit 0 | 否 |
| `method.experiments.checkpoint_resume` | 功能命名入口 import ok，`--help` exit 0 | 否 |
| `method.pr_d_representative` | legacy shim import ok，`--help` exit 0 | 否 |
| `method.experiments.representative_cases` | 功能命名入口 import ok，`--help` exit 0 | 否 |
| `method.pr2a_loop` | import ok，`python -m ... --help` exit 0；当前无 argparse usage 输出 | 否 |

LG-M1-C1 已完成前三组 current experiment entrypoint 的 old/new import / `--help` 双入口 baseline；LG-M1-C2 后续迁移 ablation 入口时，应继续以该 baseline 口径为锚点。

## Future Target Structure

本节只记录未来目标结构和负责子 PR，不代表当前已经实现。任何条目若未标注负责子 PR，均不得作为实现依据。

### `method/stages/` Pythonic API 目标 → LG-M1-B

LG-M1-B 负责在不改变 stage 语义的前提下，为 skill/toolbox 调用补齐更清晰的 Pythonic API。可能结构包括：

```text
method/stages/
├── api.py              # LG-M1-B：统一 stage callable facade
├── sc_control.py       # LG-M1-B：SC control helpers
└── ...                 # 现有 SD/SL helper 保持可追溯
```

### 当前实验入口迁移目标 → LG-M1-C1 / LG-M1-C2

LG-M1-C1/C2 负责把施工编号式实验入口迁往功能语义路径，同时保留必要 shim / old-new equivalence：

```text
method/experiments/
├── real_run_matrix.py            # LG-M1-C1：原 pr_e1_real_runs.py
├── checkpoint_resume.py          # LG-M1-C1：原 pr_lg_f1_resume_experiment.py
├── representative_cases.py       # LG-M1-C1：原 pr_d_representative.py
└── ablation/
    └── deterministic_loop.py     # LG-M1-C2：原 pr2a_loop.py
```

LG-M1-C1 implementation note：`method.pr_e1_real_runs`、`method.pr_lg_f1_resume_experiment` 与 `method.pr_d_representative` 现在是 compatibility shim；新代码和新文档应优先引用 `method.experiments.real_run_matrix`、`method.experiments.checkpoint_resume` 与 `method.experiments.representative_cases`。

### 古老 legacy loop 删除目标 → LG-M1-C2

LG-M1-C2 是唯一允许对古老 `legacy_loop.py` 做实质性删除 / 清理的子 PR。C2 必须先处理 LG-M1-A 记录的 legacy-only 与 non-legacy contract 区分，不能删除仍有学术价值的 stage/schema/contract 测试。

### LangGraph runtime 模块化目标 → LG-M1-D1 / LG-M1-D2 / LG-M1-D3

LG-M1-D1/D2/D3 负责把当前 `langgraph_runtime.py` 的大文件实现拆进 `method/langgraph/`，但必须保留 `method.langgraph_runtime` 作为 public physical facade：

```text
method/langgraph/
├── constants.py          # LG-M1-D1：schema/version/constants
├── state.py              # LG-M1-D1：graph state schema
├── registry.py           # LG-M1-D1：node/edge registry
├── checkpointing.py      # LG-M1-D2：checkpoint / resume support
├── instrumentation.py    # LG-M1-D2：operator log / stream / metadata
├── send_parallel.py      # LG-M1-D2：Send fan-out utilities
├── retry_timeout.py      # LG-M1-D2：retry / timeout envelope
├── nodes.py              # LG-M1-D3：top-level graph nodes
├── core.py               # LG-M1-D3：runtime assembly core
└── subgraphs/
    ├── validation.py     # LG-M1-D3
    ├── repair.py         # LG-M1-D3
    ├── waiver.py         # LG-M1-D3
    └── context_engineering.py  # LG-M1-D2/D3 boundary
```

### Tests mirror 目标 → LG-M1-E

LG-M1-E 负责把测试目录从当前 flat `test_pr*` 命名逐步整理为与 `method/` 子路径对应的镜像结构。LG-M1-A 新增的 [`tests/test_lg_m1_a_inventory_characterization.py`](./tests/test_lg_m1_a_inventory_characterization.py) 是功能语义命名起点，但不在本 PR 中重排整个测试树。

### 文档与 provenance 收口目标 → LG-M1-F

LG-M1-F 负责 README / ARCHITECTURE / EXAMPLES / STATUS / docstring provenance 的最终收口。LG-M1-A 只添加本文件与 README 入口链接，不做全文改写。

### 最终集成目标 → LG-M1-G

LG-M1-G 负责最终集成复核、CI / coverage / review closure 与必要四例真实 run。LG-M1-A 默认不跑四例；若后续实现触及默认 runtime、FixLog、operator log、eligibility 或 evidence 主字段，则按 #64 纪律升级。
