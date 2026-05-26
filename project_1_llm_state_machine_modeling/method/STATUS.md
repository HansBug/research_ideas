# `method/` 实现进度跟踪

> **branch**: `dev/method-agent-implementation`
> **目标**：完整实现 + 跑通 our agent loop + 给出引导 md + smoke 通过；merge 到 main 后 Path 1 / Path 2 各自 PR rebase main 拿到这部分。

## 整体阶段

| Phase | 内容 | 状态 |
| --- | --- | --- |
| **A** | 脚手架 + pyfcstm submodule + 目录骨架 + README + STATUS | ✅ 完成 |
| **B** | gpt_client.py 统一 LLM client + schema.py dataclass | ✅ 完成 (LLM endpoint ping 通) |
| **C** | 三个 LLM agent + prompt 模板（spec_extractor / modeler / repair） | ✅ 完成 (端到端 smoke 跑通：NL → SpecJson → DSL → pyfcstm parse + sem OK) |
| **D** | 四个 feedback source wrapper（parse / semantic / sim / judge） | 未开工 |
| **E** | loop.py 主驱动 + gated cascade 合并 + iter 控制 | 未开工 |
| **F** | eval/component_extractor.py (Umple/pyfcstm 7 类组件抽取) | 未开工 |
| **G** | 端到端 smoke 跑通 + 文档收尾 + push branch + 创建 PR Ready | 未开工 |

## Phase A-C 完成里程碑

**端到端验证**（在 traffic light NL 上跑通，2026-05-26）：
- SpecExtractor (GPT-5.5) → 3 states / 1 events / 1 variables / 6 transitions
- Modeler (GPT-5.5) → 完整 pyfcstm DSL（含 `def int timer = 0;` + `state System { ... }` + 3 forced transitions `! X -> Red :: Reset` + 3 guard transitions `Red -> Green : if [timer >= 30] effect { timer = 0; };`）
- pyfcstm `parse_with_grammar_entry` ✓
- pyfcstm `parse_dsl_node_to_state_machine` ✓ → root state name / variables / state count 都对
- 总 token：5292（spec 3467 + model 1825）/ 单 sample

**Prompt 中所有 DSL example 已用 pyfcstm 真实验证**（user 2026-05-26 要求）：
- Elevator example (modeler.txt §Example) ✓
- local vs chain event scope example ✓
- guard-driven cycle example ✓
- forced transitions example ✓
- aspect + lifecycle + abstract example ✓
- pseudo state example ✓
- 6/6 verified pass

## 当前 commit 含

1. `pyfcstm` git submodule pin 到 main commit `693fcf57`（Merge PR #66 from HansBug/dev/vscode）
2. `method/` 目录骨架：`agents/` / `feedback/` / `prompts/` / `eval/` / `tests/` / `data/` + 各自 `__init__.py`
3. `method/README.md` 引导文档（目录定位 / LLM env 接入约束 / pyfcstm 集成方式 / 运行入口 / 接管入口）
4. `method/STATUS.md`（本文件）

## 下一步（Phase B）

1. 写 `method/gpt_client.py`：`get_llm_client()` + `get_default_model()` 走 `os.environ`，**绝不读 .env 文件**
2. 写 `method/schema.py`：核心 dataclass — `LoopConfig` / `AgentLoopResult` / `FeedbackBundle` / `ParseFeedback` / `SemanticFeedback` / `SimFeedback` / `JudgeFeedback` / `ModelArtifact`
3. Phase B smoke：可以 import 但不需要跑实际 LLM（实际 LLM 跑放在 Phase G）

## 关键约束

- 所有 LLM 调用走 `method/gpt_client.py`，统一 OpenAI-compatible client
- 代码绝不直接读 `.env` 文件；运行前 shell `source .env` 把三件套加载到 `os.environ`
- pyfcstm 走 submodule (pin commit `693fcf57`)，升级方式：在 submodule 内 `git fetch && git checkout <new-commit>` 后回到主仓 `git add pyfcstm && git commit`
- agent prompt **全英文**（paper 是英文 SE 论文，统一）

## 历史 commit

| commit | 描述 |
| --- | --- |
| (待填) | Phase A：脚手架 + pyfcstm submodule + README + STATUS |
