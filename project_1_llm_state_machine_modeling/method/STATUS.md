# `method/` 实现进度跟踪

> **branch**: `dev/method-agent-implementation`
> **目标**：完整实现 + 跑通 our agent loop + 给出引导 md + smoke 通过；merge 到 main 后 Path 1 / Path 2 各自 PR rebase main 拿到这部分。

## 整体阶段（v3 — 2026-05-26 D 拆分：sim 与 property generation 配对实现）

> **v2 → v3 修订依据**：用户 2026-05-26 反馈 — sim feedback 不依赖 property 就只能验证"不死锁 / 状态可达"这种通用 sanity，无法验证业务正确性；必须先有 property（提供 expected behavior oracle），sim 才能验证 model 行为是否符合 NL 需求。因此 sim 从 Phase D 中拆出，**与 property generation 在 Phase G 配对实现**。

| Phase | 内容 | 状态 |
| --- | --- | --- |
| **A** | 脚手架 + pyfcstm submodule + 目录骨架 + README + STATUS | ✅ 完成 |
| **B** | gpt_client.py 统一 LLM client + schema.py dataclass | ✅ 完成 (LLM endpoint ping 通) |
| **C** | single-prompt modeling 路径：spec_extractor / modeler / repair 三个 agent + prompt | ✅ 完成 (端到端 smoke 跑通) |
| **D (修订)** | **parse + semantic feedback wrappers**（2 个 property-independent deterministic feedback）<br>`feedback/parse.py`：包 `pyfcstm.dsl.parse_with_grammar_entry`，从 `GrammarParseError.errors` 抽 line/col/got/snippet<br>`feedback/semantic.py`：包 `pyfcstm.model.parse_dsl_node_to_state_machine`，用 regex 从 SyntaxError message 分类 (undefined_vars / missing_states / dangling_transitions / type_mismatches) | ✅ 完成 (smoke verified：good DSL ok / parse_bad 给出 line+col+got+snippet / sem_bad 抽出 undefined_var) |
| **E** | loop.py 主驱动 + gated cascade 合并 + iter 控制 + **modeling_mode CLI flag (single_prompt vs multi_step)** | 未开工 |
| **F** | **Multi-step modeling 模块**（基于用户硕士论文 MTI 方法学）：拆 6 步 (identify_state → identify_event → identify_variable → identify_transition → identify_action → build_pyfcstm)；step 之间通过 JSON 上下文传递；每步 prompt 含统一 **7 段式骨架**（task / requirements / 上游 list / 本步任务 / domain knowledge / format / constraint / 起手占位） | 未开工 |
| **G (修订 — 与 sim 配对，framing 校正)** | **Model test scenario generation + sim feedback 配对实现**：<br>**注意**：这里的 "scenario" / "property" 是 **model test case**（约定输入下的期望行为），**不是形式化验证的 LTL / CTL 性质**。框架对标 MTI 的 BDD scenario 三元组思路 — sim 是"用模型仿真代替代码运行的 testcase 执行环境"。<br><br>(1) test scenario generation 子模块（3 步流水，对应 MTI 论文的 mapping → Gherkin → 三元组）：<br>　• `elements_mapping`：NL requirement → 涉及的 model 元素 (states / events / variables) 子集<br>　• `scenario_generation`：基于 mapping 生成 Gherkin (Given/When/Then) 人类可读场景，覆盖关键 transition + edge case<br>　• `structure_scenario`：Gherkin → 三元组 mini-DSL `[s-InitialState, e-Event1, e-Event2, ..., expected: s-FinalState, v-Var=Val]`（机器可执行）<br><br>(2) `feedback/sim.py`：把三元组 scenario 喂给 `SimulationRuntime` — 用 initial_state 做 hot start，按 event_sequence 跑 `cycle(events=...)`，对比 `runtime.current_state` / `runtime.vars` vs scenario 中的 expected_final_*，输出 SimFeedback（`scenario_violations` / `unreachable_states` / `deadlocks` / `safety_limit_hit` / `SimulationRuntimeDfsError`）<br><br>**核心 framing**：单靠 sim 跑空 cycle 只能 verify "不死锁 / 状态可达"；要 verify "model 行为是否符合 NL 需求"，必须有 "NL → scenario (expected behavior) → sim 执行验证" 的 oracle 链。这是**用模型仿真做 testcase 验证**而不是 model checking | 未开工 |
| **H** | judge feedback (ex1 ExpertReviewAgent adapter) — rubric 5 维 semantic 评分 | 未开工 |
| **I** | eval/component_extractor.py (Umple / pyfcstm 抽 7 类组件，Path 1 评测用) | 未开工 |
| **J** | 端到端验收：single_prompt vs multi_step 对比跑、生成模型 + property 例子写进 README/STATUS、PR mark Ready for Review | 未开工 |

## Phase 依赖关系

```
A → B → C (single-prompt 已完成)
        │
        ├→ D (parse + sem) ─────────────┐
        │                               ├→ E (loop driver) ──→ J (验收)
        ├→ F (multi-step modeling) ────┤      ↑
        │                               │      │
        ├→ G (property + sim 配对) ─────┤      │
        │                               │      │
        ├→ H (judge) ───────────────────┘      │
        │                                      │
        └→ I (eval extractor, Path 1 用) ──────┘
```

Phase D / F / G / H / I 之间无依赖，可以并行做。Phase E (loop driver) 把它们串起来。Phase J 验收。

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
