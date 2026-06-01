# `method/` — Agent Loop 共同实现（two-path 共享基础）

> **位置**：`project_1_llm_state_machine_modeling/method/`
>
> **服务对象**：[`dev/path1-hard-comparison`](https://github.com/HansBug/research_ideas/pull/9) 与 [`dev/path2-differentiation`](https://github.com/HansBug/research_ideas/pull/10) 两路 sprint 共用的 agent loop 基础设施。本目录由 `dev/method-agent-implementation` branch 实现并合入 main，之后两路 PR rebase main 拿到这部分。
>
> **创建日期**：2026-05-26（sprint 共同基础阶段）

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

`pyfcstm` 作为 **git submodule** pin 到 `main` 分支 commit `693fcf57`（仓库根 `pyfcstm/`）。

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
from method.loop import run_agent_loop, LoopConfig

result = run_agent_loop(
    nl_input="...",
    config=LoopConfig(
        condition="A4",  # "A0" baseline / "A4" full agent loop
        n_iter=3,
        feedback_sources=["parse", "semantic", "sim"],  # judge adapter 尚未接入，需显式 opt-in
    ),
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
