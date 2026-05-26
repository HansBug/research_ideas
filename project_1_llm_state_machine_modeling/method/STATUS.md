# `method/` 实现进度跟踪

> **branch**: `dev/method-agent-implementation`
> **目标**：完整实现 + 跑通 our agent loop + 给出引导 md + smoke 通过；merge 到 main 后 Path 1 / Path 2 各自 PR rebase main 拿到这部分。

## 整体阶段（v2 — 2026-05-26 加入 multi-step modeling + property generation）

| Phase | 内容 | 状态 |
| --- | --- | --- |
| **A** | 脚手架 + pyfcstm submodule + 目录骨架 + README + STATUS | ✅ 完成 |
| **B** | gpt_client.py 统一 LLM client + schema.py dataclass | ✅ 完成 (LLM endpoint ping 通) |
| **C** | single-prompt modeling 路径：spec_extractor / modeler / repair 三个 agent + prompt | ✅ 完成 (端到端 smoke 跑通：NL → SpecJson → DSL → pyfcstm parse + sem OK) |
| **D** | 四个 feedback source wrapper（parse / semantic / sim / judge） | 未开工 |
| **E** | loop.py 主驱动 + gated cascade 合并 + iter 控制 + **modeling 路径切换 (single-prompt vs multi-step) CLI flag** | 未开工 |
| **F (新增)** | **Multi-step modeling 模块**：基于用户硕士论文 MTI 方法学，拆 5 步 (identify_state → identify_event → identify_variable → identify_transition → identify_action → build_pyfcstm)；step 之间通过 JSON 上下文传递，每步 prompt 含统一的 task_description + step_prompt + domain_knowledge + format_description 结构 | 未开工 |
| **G (新增)** | **Property generation 模块**：基于已生成的 pyfcstm model 元素 (states / events / transitions / variables) 自动生成**待验证性质 / 测试场景**（Gherkin-like 或 event sequence + expected state/var），配合 pyfcstm `SimulationRuntime` sim 验证 — 性质提供 sim oracle (expected behavior)，sim 提供执行验证 | 未开工 |
| **H** | eval/component_extractor.py (Umple/pyfcstm 7 类组件抽取，Path 1 评测用) | 未开工 |
| **I** | 端到端 smoke (single-prompt vs multi-step 对比) + 验收 + 生成模型 vs baseline 对比例子写进 README/STATUS + 文档收尾 + PR Ready | 未开工 |

## 设计原则：modeling 路径作为 CLI 选项

`method/loop.py` 必须支持两条 modeling 路径切换（用 `LoopConfig.modeling_mode` 字段）：

| modeling_mode | 流程 | 用于 |
| --- | --- | --- |
| `"single_prompt"` | NL → SpecExtractor (1 步) → Modeler (1 步) → DSL | 当前 Phase C 已实现；对照组 |
| `"multi_step"` (新) | NL → 5 步 MTI (state / event / variable / transition / action) → build_pyfcstm → DSL | 基于 user 硕士论文方法学，Phase F 实现；主对照组 |

两种 modeling 路径共用同一套 feedback / repair / loop 机制（Phase D / E），保证 ablation 干净（仅 modeling 阶段差异）。

## 设计原则：待验证性质 + sim 联合工作流

Phase G 的待验证性质 generation 必须设计为可被 pyfcstm `SimulationRuntime` 消费的形式：

1. **性质 schema**：每条性质至少含 `(scenario_name, initial_state, event_sequence, expected_final_state_or_var_constraint)`
2. **生成方式**：从 model 已识别元素（state/event/var）出发，LLM 生成"覆盖关键 transition 的 scenario + expected outcome"
3. **配合 sim 验证**：把 event_sequence 喂给 `SimulationRuntime.cycle(events=...)`，看跑完后 `runtime.current_state` / `runtime.vars` 是否匹配 expected — 这就是 model defects 的来源信号

**核心 framing**：单靠 pyfcstm sim 跑空 cycle 只能 verify "不死锁 / 状态可达"；要 verify "model 行为是否符合 NL 需求"，必须有"NL 需求 → 期望行为 → sim 验证" 的 oracle 链。Phase G 就是补这条链。

## 历史 commit

| commit | 描述 |
| --- | --- |
| `6e...` | Phase A-C：脚手架 + pyfcstm submodule + 3 single-prompt agent + 端到端 smoke 跑通 |
| (待填) | Phase D-I |

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
