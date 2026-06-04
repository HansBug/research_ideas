# `method/` — Agent Loop 共同实现（two-path 共享基础）

> **位置**：`project_1_llm_state_machine_modeling/method/`
>
> **服务对象**：[`dev/path1-hard-comparison`](https://github.com/HansBug/research_ideas/pull/9) 与 [`dev/path2-differentiation`](https://github.com/HansBug/research_ideas/pull/10) 两路 sprint 共用的 agent loop 基础设施。本目录由 `dev/method-agent-implementation` branch 实现并合入 main，之后两路 PR rebase main 拿到这部分。
>
> **创建日期**：2026-05-26（sprint 共同基础阶段）


## 0. PR-C 默认入口语义（2026-06-02）

本目录当前处于 issue [#21](https://github.com/HansBug/research_ideas/issues/21) 的 PR-E1 阶段：

- `method.loop.run_agent_loop(nl, LoopConfig())` 已集成为 **canonical full staged runtime**，默认解析为 `experiment_default/full_staged_v1` 并调用 PR-B1 driver + PR-B2 real-env SL adapters。
- 默认入口不再返回 PR-A `contract_only` façade；缺少真实 provider 配置或 provider/schema retry 耗尽时，也会写出 `AgentLoopRunRecord` 并以 `provider_error` / `invalid` 等可审计 verdict 退出。
- fake / mock / replay / hot-start DSL 只能通过显式非默认 condition 或专用 smoke/replay 入口启用；默认 `LoopConfig()` 不允许 provider injection 或 `seed_dsl`，避免污染 Path1/Path2 主实验。
- `AgentLoopRunRecord` 会记录 resolved config、condition hash、environment、provider/model 脱敏标识、stage/iteration/repair/scenario/LLM trace、eligibility 与 `redaction_report`；非默认/weak oracle/provider error/schema invalid/write failure 均不得进入高可信主结果。
- 旧 A0-A4 loop 已迁移到 `method.legacy_loop.run_legacy_agent_loop()` / `LegacyLoopConfig`，调用时发 `DeprecationWarning`，只用于历史诊断与 baseline 对照。

默认 stage graph：

```text
SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SC-12 -> SC-13
```

PR-E1 后 repair 主链为 `SD-8 FixRequestBatch -> SL-9 per-request accept/reject + repair -> SL-10(NL + FixLog + local_check_evidence) -> SC-11 -> SD-2 full revalidation`。旧 `SD-10` local repair checks 仍作为 `SL-10` 的 `local_check_evidence` 运行，旧 `SL-10B` delta review 仅保留为 legacy/ablation 兼容，不再是默认主链 stage。

消融实验必须显式声明非默认 `condition_id` 与 `changed_factors`；任何关闭 stage、改 budget、改 oracle、禁用 review、切 fake/replay provider 的配置都不得污染 `LoopConfig()` 默认路径。


## 0.1 PR-B2 LLM stage execution units（2026-06-02）

PR-B2 在共享 contract 基础上新增 `llm_stages.py`，只交付 LLM stage / prompt / retry / interaction record 这一条线：

- `run_sl1_initial_modeling_llm(...)`：真实或 mock provider 执行 `SL-1`，解析 `candidate_dsl` 与 `grounding_seeds`。
- `run_sl5_scenario_generation_llm(...)`：执行 `SL-5`，解析 `TestScenario` 列表；`coverage_directive` 可作为输入，但 coverage gap 的触发与循环控制仍属于 PR-B1/PR-C runtime。
- `run_sl7_model_review_llm(...)`：执行 lightweight model review，并返回 typed `ModelReviewFeedback`。
- `run_sl9_repair_llm(...)`：执行 repair；prompt 必须携带 NL、`FixRequestBatch`、完整 `FixLog`、selected diagnostics、preserve list 与 scenario summary；每个 request 都要给出 accept/reject，`suggested_fix` 仅为参考 hint。
- `run_sl10_repair_review_llm(...)`：执行 PR-E1 默认 `SL-10` repair review；输入必须包含 NL、old/new DSL、FixRequestBatch、SL-9 decisions、完整 FixLog、diff 与 local deterministic check evidence，并返回 typed `SL10RepairReviewOutput`。
- `run_sl10b_delta_review_llm(...)`：legacy/ablation delta review 兼容入口，不再属于默认主链。

PR-B2/PR-E1 的 retry 只覆盖 LLM 层噪声：provider/network/schema-invalid/empty-output。parse、semantic、inspect、coverage、sim 与 local repair checks 等 deterministic failure 不在这里 retry，必须由 PR-B1/PR-C/PR-E1 top-down runtime 判定是否进入 repair、SL-10 rework 或下一轮完整验证。

所有 stage unit 均产出可写入 `AgentLoopRunRecord.llm_interactions` 的 interaction payload：prompt、raw output、parsed output、schema validation、usage、provider/model、attempts、retry error、prompt/input/raw hash 与 redaction report。默认真实 provider 仍只通过 `method.gpt_client` 读取进程环境变量，不直接读取 `.env` 文件。

## 1. 目录定位

本目录提供 NL → pyfcstm DSL 的 agent loop 完整实现，含：

1. **统一 LLM client** (`gpt_client.py`)：所有 LLM 调用走仓库根 `.env` 三件套 (`LLM_ENDPOINT` / `LLM_API_KEY` / `LLM_MODEL`)，OpenAI-compatible
2. **三个 LLM agent** (`agents/`)：SpecExtractor / Modeler / Repair
3. **四个 deterministic feedback source** (`feedback/`)：Parse / Semantic / Sim / Judge
4. **顶层 agent loop driver** (`loop.py`)：迭代 + gated cascade 反馈合并
5. **schema 定义** (`schema.py`)：FeedbackBundle / AgentLoopResult / LoopConfig 等 dataclass
6. **prompt 模板** (`prompts/`)：spec_extractor / modeler / repair 三套 prompt（全英文）
7. **组件抽取器** (`eval/component_extractor.py`)：从 Umple / pyfcstm DSL 抽出 7 类组件用于 Path 1 P/R/F1 评测
8. **smoke 测试** (`tests/test_smoke.py`)：端到端 1 条样本跑通 verify

## 2. LLM env 接入约束（**硬性要求**）

所有 LLM 调用统一走仓库根 `.env` 三件套：

```
LLM_ENDPOINT  — OpenAI-compatible proxy URL
LLM_API_KEY   — Bearer token
LLM_MODEL     — 主跑模型名（如 gpt-5.5）
```

**约束**：

1. 运行任何 method 脚本前必须先 shell `source .env`
2. **代码绝不直接读 `.env` 文件**，只读 `os.environ`
3. 切换模型只改 `.env` 的 `LLM_MODEL` 然后重新 `source .env`，**代码完全不动**
4. `method/gpt_client.py` 是仓库中**唯一**允许实例化 OpenAI-compatible client 的位置；所有 agent / baseline replication / judge adapter 都 inject 这个 client

## 3. pyfcstm 集成方式

`pyfcstm` 作为 **git submodule** pin 到 `main` 分支 commit `5f811a0f`（仓库根 `pyfcstm/`）。

```bash
# 初次 clone 时
git clone --recurse-submodules <repo>

# 或已 clone 后
git submodule update --init --recursive

# 安装到 venv（editable mode，submodule 升级时自动同步）
venv/bin/pip install -e ./pyfcstm
```

method 代码内一律以 `from pyfcstm.dsl import parse_with_grammar_entry` 等正常 import 使用。

## 4. 目录结构

```text
method/
├── README.md (本文件)
├── STATUS.md (sprint 进度跟踪)
├── __init__.py
├── gpt_client.py          统一 OpenAI-compatible LLM client (单一实例化入口)
├── llm_stages.py          PR-B2 SL stage provider adapter / retry / interaction record
├── schema.py              FeedbackBundle / AgentLoopResult / LoopConfig dataclass
├── loop.py                主 agent loop driver (run_agent_loop 入口)
├── agents/
│   ├── __init__.py
│   ├── spec_extractor.py  NL → JSON spec
│   ├── modeler.py         spec → pyfcstm DSL
│   └── repair.py          (current DSL, feedback) → new DSL
├── feedback/
│   ├── __init__.py
│   ├── parse.py           pyfcstm.dsl.parse_with_grammar_entry → ParseFeedback
│   ├── semantic.py        pyfcstm.model.parse_dsl_node_to_state_machine → SemanticFeedback
│   ├── sim.py             pyfcstm.simulate.SimulationRuntime → SimFeedback (+ reachability witness)
│   └── judge.py           ex1 ExpertReviewAgent adapter → JudgeFeedback
├── prompts/
│   ├── spec_extractor.txt
│   ├── modeler.txt
│   └── repair.txt
├── eval/
│   ├── __init__.py
│   └── component_extractor.py  Umple/pyfcstm 抽 7 类组件 (Path 1 用)
├── data/
│   └── (sprint 阶段填入数据准备脚本与 derived parquet)
└── tests/
    ├── __init__.py
    └── test_smoke.py      端到端单条样本 verify
```

## 5. 运行入口

### 5.1 Smoke test (Phase 0 末验证)

```bash
# 先 source .env
source .env

# 跑 smoke test (单条 sources/automatic-elevator-controller 跑通端到端 A4 loop)
venv/bin/python -m method.tests.test_smoke
```

### 5.2 Path 1 / Path 2 实验脚本入口

Path 1 / Path 2 各自的 `run_path1.py` / `run_path2.py` 在各自 branch 上实现，但都调本目录的 `method.loop.run_agent_loop` 作为唯一入口：

```python
from method.loop import LoopConfig, run_agent_loop

result = run_agent_loop(
    nl="...",
    config=LoopConfig(),  # experiment_default/full_staged_v1
)
```

历史 A0-A4 诊断入口必须显式调用 legacy module：

```python
from method.legacy_loop import LegacyLoopConfig, run_legacy_agent_loop

legacy_result = run_legacy_agent_loop(
    nl="...",
    config=LegacyLoopConfig(condition="A4", n_iter=3, feedback_sources=["parse", "semantic", "sim"]),
)
```

## 6. 新 session 接管入口

任何新 Claude / codex session 进入 `dev/method-agent-implementation` branch 后，按以下顺序读：

1. 本 [README.md](./README.md)（method/ 目录定位）
2. [STATUS.md](./STATUS.md)（当前 sprint 进度）
3. [../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md) — meta-level 路线规划与 §4.5 method core contribution
4. 两路 PR 共享的 §4.5 / PATH GUIDE §11 框架

## 7. 实现进度（参见 [STATUS.md](./STATUS.md)）

本目录由 `dev/method-agent-implementation` branch 分多阶段实现：

- Phase A：脚手架 + pyfcstm submodule + gpt_client + schema (本 commit)
- Phase B：三个 agent prompt + Python wrapper
- Phase C：四个 feedback source wrapper
- Phase D：loop.py 主驱动 + smoke test
- Phase E：组件抽取器 (eval/component_extractor.py)
- Phase F：跑通 + 文档收尾 + PR 准备 merge
