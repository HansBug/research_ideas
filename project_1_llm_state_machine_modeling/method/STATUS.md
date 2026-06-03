# `method/` 实现进度跟踪

> **branch**: `dev/method-agent-implementation`
> **目标**：完整实现 + 跑通 our agent loop + 给出引导 md + smoke 通过；merge 到 main 后 Path 1 / Path 2 各自 PR rebase main 拿到这部分。


## PR-E1 状态补充（issue #21，2026-06-03）

当前分支 PR-E1 在 PR-C/PR-D 默认入口基础上继续调整 repair 子架构与真实运行证据链：

- `LoopConfig()` 默认解析为 `experiment_default/full_staged_v1`，包含 full staged stage switches、feedback/budget/scenario/LLM/record/eligibility policy 与 condition hash。
- `method.loop.run_agent_loop()` 不再调用旧 A0-A4 implementation，也不再停留在 PR-A contract-only façade；默认执行 full staged runtime。
- 默认 `LoopConfig()` 使用 real-env LLM provider adapter；缺 provider 配置、provider retry exhaustion 或 schema invalid 会写出 run record 并以 `provider_error` / `invalid` 退出，不回退 fake。
- 旧实现移到 `method.legacy_loop.run_legacy_agent_loop()` / `LegacyLoopConfig`，并发 deprecation warning。
- planned stage graph 已更新为 `SC-0/SL-1/SD-2/SD-3/SD-4/SL-5/SD-5A/SC-5F/SD-6/SL-7/SD-8/SL-9/SL-10/SC-11/SC-12/SC-13`，每个 planned node 都有 `enabled/ran/status/skipped_reason` trace 字段。
- run record 记录 resolved config / environment / provider-model 脱敏标识 / stage_records / iteration_records / llm_interactions / deterministic_feedback / repair_history / fix_log / scenario_history / logs / final_artifacts / redaction_report。
- PR-E1 继续负责四例真实 agent-loop 重跑、NFRR v3 质量诊断与 reviewer 闭环；当前不声明模型质量已达到高可信主结果。


## PR-B2 状态补充（issue #21，2026-06-02）

PR-B2 交付真实/mock LLM stage execution units，但仍不切默认 full runtime：

- 新增/更新 `llm_stages.py`，封装 `SL-1/SL-5/SL-7/SL-9/SL-10` 的默认 provider adapter、schema/empty/provider retry 与 interaction record；旧 `SL-10B` 保留为 legacy/ablation。
- 默认真实 provider 通过 `method.gpt_client` 读取进程环境变量；单元测试使用 `MockLLMProvider`，不依赖真实 API。
- LLM retry 只处理 provider/network/schema-invalid/empty-output；deterministic feedback failure 不在 PR-B2 中 retry。
- `SL-9` repair prompt 保留 `suggested_fix` 作为 hint，不强制照抄，允许 LLM 基于 NL 与全局约束给出更合理修复。
- `SL-5` 的 `coverage_directive` 可由上游传入；coverage gap 如何触发 targeted retry 属于 PR-B1/PR-C runtime 责任，PR-B2 只保证 SL-5 可被再次调用且记录完整。
- interaction payload 记录 prompt、raw output、parsed output、usage、provider/model、attempts、retry error、schema validation、hash 与脱敏报告，为后续 Path1/Path2 实验可审计性服务。

## 整体阶段（v3 — 2026-05-26 D 拆分：sim 与 property generation 配对实现）

> **v2 → v3 修订依据**：用户 2026-05-26 反馈 — sim feedback 不依赖 property 就只能验证"不死锁 / 状态可达"这种通用 sanity，无法验证业务正确性；必须先有 property（提供 expected behavior oracle），sim 才能验证 model 行为是否符合 NL 需求。因此 sim 从 Phase D 中拆出，**与 property generation 在 Phase G 配对实现**。

| Phase | 内容 | 状态 |
| --- | --- | --- |
| **A** | 脚手架 + pyfcstm submodule + 目录骨架 + README + STATUS | ✅ 完成 |
| **B** | gpt_client.py 统一 LLM client + schema.py dataclass | ✅ 完成 (LLM endpoint ping 通) |
| **C** | single-prompt modeling 路径：spec_extractor / modeler / repair 三个 agent + prompt | ✅ 完成 (端到端 smoke 跑通) |
| **D (修订)** | **parse + semantic feedback wrappers**（2 个 property-independent deterministic feedback）<br>`feedback/parse.py`：包 `pyfcstm.dsl.parse_with_grammar_entry`，直接读取 `GrammarParseError.errors` 结构化字段抽 line/col/got/snippet<br>`feedback/semantic.py`：包 `pyfcstm.model.parse_dsl_node_to_state_machine(..., collect=True)`，按 `ModelDiagnostic.code` / `refs` 分类 (undefined_vars / missing_states / dangling_transitions / type_mismatches)，不再 regex 解析异常文案 | ✅ 完成并迁移到 pyfcstm v0.4.0 结构化诊断 (smoke verified：good DSL ok / parse_bad 给出 line+col+got+snippet / sem_bad 抽出多个 undefined_var) |
| **E** | loop.py 主驱动 + gated cascade 合并 + iter 控制 + **modeling_mode CLI flag (single_prompt vs multi_step)** + cascaded Repair（4 个 fix sub-prompt） + scenarios 冻结策略 + sim/judge optional 控制（ablation 用） | ✅ 完成（A2 跑通 3 NL examples + 2 个 inject-bug-recover trace；详见 [EXAMPLES.md §Phase E](./EXAMPLES.md#phase-e--agent-loop-driver-演示) ）|
| **F** | **Multi-step modeling 模块**（基于用户硕士论文 MTI 方法学）：拆 6 步 (identify_state → identify_event → identify_variable → identify_transition → identify_action → build_pyfcstm)；step 之间通过 JSON 上下文传递；每步 prompt 含统一 **7 段式骨架**（task / requirements / 上游 list / 本步任务 / domain knowledge / format / constraint / 起手占位） | ✅ 完成 (端到端 smoke：6 步流水 9850 tokens → pyfcstm DSL parse + sem 全通过；输出比 single-prompt 更紧凑，用 `! * -> Red :: Reset` 1 行代替 single-prompt 的 3 行；effect 自动移到 target state 的 enter action) |
| **G (修订 — 与 sim 配对，framing 校正)** | **Model test scenario generation + sim feedback 配对实现**：<br>**注意**：这里的 "scenario" / "property" 是 **model test case**（约定输入下的期望行为），**不是形式化验证的 LTL / CTL 性质**。框架对标 MTI 的 BDD scenario 三元组思路 — sim 是"用模型仿真代替代码运行的 testcase 执行环境"。<br><br>(1) test scenario generation 子模块（**v4.2 简化为 1 步**：NL + model elements → JSON scenarios；MTI 3 步对照保留为 future work）：<br>　• `agents/scenariogen/generate.py` + `prompts/scenariogen/generate_scenarios.txt`<br><br>(2) `feedback/sim.py`：把 scenario 喂给 `SimulationRuntime` — 用 initial_vars 做 hot-start（cycle 1 + 后续 mutate `runtime.vars`），按 events 跑 `cycle(events=...)` 含 cycles_between/extra_cycles 配置，对比 `runtime.current_state` / `runtime.vars` vs scenario expected，输出 SimFeedback（`scenario_violations` / `unreachable_states` / `safety_limit_hit` / runtime_error）<br><br>**核心 framing**：单靠 sim 跑空 cycle 只能 verify "不死锁 / 状态可达"；要 verify "model 行为是否符合 NL 需求"，必须有 "NL → scenario (expected behavior) → sim 执行验证" 的 oracle 链。这是**用模型仿真做 testcase 验证**而不是 model checking | ✅ 完成（3 NL examples + 3 buggy variants 全验证，详见 [EXAMPLES.md](./EXAMPLES.md)）|
| **H** | judge feedback (ex1 ExpertReviewAgent adapter) — rubric 5 维 semantic 评分 | 🔁 sprint 跳过（loop.py 已留 hook，Phase E v3 已落 `feedback_sources` 配置项；adapter 留作方向定后正式 paper 阶段补做）|
| **I** | Path 1 评测基础设施：5-component IR extractor + 双 LLM annotator + 中文 markdown 评审包 + audit-trail 汇总 | ✅ 完成（见 [`../eval/`](../eval/) — `extract/{umple,pyfcstm}.py` / `annotate/` / `review/` / `report.py` / `aggregate.py` / `demo/`；演习 67 rows × 26 列 audit-trail 跑通；评测协议见 [`../eval/PROTOCOL.md`](../eval/PROTOCOL.md)）|
| **J** | 端到端验收：single_prompt vs multi_step 对比跑、生成模型 + property 例子写进 README/STATUS、PR mark Ready for Review | sprint 末 Phase 6-7 由两个 path branch 各自完成 |

## Phase 依赖关系

```
A → B → C (single-prompt 已完成)
        │
        ├→ D (parse + sem) ─────────────┐
        │                               ├→ E (loop driver) ──→ J (验收, by path branch)
        ├→ F (multi-step modeling) ────┤      ↑
        │                               │      │
        ├→ G (property + sim 配对) ─────┤      │
        │                               │      │
        ├→ H (judge) ─[sprint 跳过]─────┘      │
        │                                      │
        └→ I (eval 评测基础设施，Path 1 用) ───┘
```

Phase D / F / G / H / I 之间无依赖，可以并行做。Phase E (loop driver) 把它们串起来。Phase H sprint 跳过（loop hook 已留）。Phase I 已实装为 [`../eval/`](../eval/) 整套 LLM-初审 + 人类签字 + audit-trail 评测基础设施（Path 1 主用，Path 2 可选作 audit-trail 抽查）。Phase J 由 path branch 各自完成。

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

## Phase G 验收证据（2026-05-26）

| 维度 | 数据 |
| --- | --- |
| Part A 真实 NL 例子 | 3 个 (traffic_light, microwave, elevator_3floor) — 详见 [EXAMPLES.md §Part A](./EXAMPLES.md#part-a--3-个-nl-控制系统真实端到端跑通) |
| Part A model 全 parse+sem | 3/3 ✅ |
| Part A sim scenario pass rate | traffic_light 2/7, microwave 4/7, **elevator 8/8** ✅ |
| 失败 scenarios 性质 | 绝大多数是 LLM scenario writer 的 cycle timing off-by-one bias（不是 model bug），是个有价值的 finding |
| Part B mutation detection | 3/3 buggy variants 都被 sim caught — 详见 [EXAMPLES.md §Part B](./EXAMPLES.md#part-b--mutation-detection验证-sim-检测-model-bug-的能力) |
| Part B mutation 覆盖维度 | state-mismatch / runtime_error / var-mismatch 3 类 |

## 历史 commit

| commit | 描述 |
| --- | --- |
| `6e...` | Phase A-C：脚手架 + pyfcstm submodule + 3 single-prompt agent + 端到端 smoke 跑通 |
| `2447ad8a` | Phase D 完成（parse + sem feedback wrappers 含 smoke 通过）+ STATUS v3（D 拆分 + Phase G framing 校正）|
| `f28c99b2` | Phase F multi-step MTI 端到端跑通 + 修 forced-effect grammar bug |
| `de67d131` | Phase G v3 完成（scenarios 重定位为 bug-finding probes + 6 mutation differential）|
| `1f26ff4c` | Phase E v1 完成（agent loop driver + cascaded Repair + ablation 支持） |
| `255c0af9` | Phase E v2（fix prompt context (a)+(c) + 共享 grammar reference） |
| `06536876` | Phase E v3（scenariogen 自管 cycle 一致性 + mutation self-validation） |
| `ff1e90ff` | Phase I 实装为 `eval/` 整套 LLM-初审 + 人类签字 + audit-trail 评测基础设施 |
| (待填，path branches) | Phase J 端到端验收 by Path 1 / Path 2 branch 各自完成 |

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

1. `pyfcstm` git submodule pin 到 main commit `5f811a0f`（pyfcstm v0.4.0 / Layer1+Layer2 diagnostics）
2. `method/` 目录骨架：`agents/` / `feedback/` / `prompts/` / `eval/` / `tests/` / `data/` + 各自 `__init__.py`
3. `method/README.md` 引导文档（目录定位 / LLM env 接入约束 / pyfcstm 集成方式 / 运行入口 / 接管入口）
4. `method/STATUS.md`（本文件）

## 下一步（PR #11 merge 后两路并行）

PR #11 已含全部 Phase A-G + E v3 + I 共同基础。merge 到 main 后：

1. **Path 1 branch** (`dev/path1-hard-comparison`)：rebase 到 main → 按 [`../paper_v1/PATH1_HARD_COMPARISON_GUIDE.md`](../paper_v1/PATH1_HARD_COMPARISON_GUIDE.md) 推进 sprint Phase 4（sources/ T0+🟢 选样 + Hybrid baseline 重跑 + agent loop 跑 + eval/ pipeline 评测）→ Phase 6 出 PATH1_REPORT.md
2. **Path 2 branch** (`dev/path2-differentiation`)：rebase 到 main → 按 [`../paper_v1/PATH2_DIFFERENTIATION_GUIDE.md`](../paper_v1/PATH2_DIFFERENTIATION_GUIDE.md) 推进 sprint Phase 5（sources/ T0+🟢 20 条分层 + 4-intrinsic + 可选 audit-trail 抽查）→ Phase 6 出 PATH2_REPORT.md
3. **决策合流**：sprint 末 Phase 6 由用户综合两路数据拍板方向

## 关键约束

- 所有 LLM 调用走 `method/gpt_client.py`，统一 OpenAI-compatible client
- 代码绝不直接读 `.env` 文件；运行前 shell `source .env` 把三件套加载到 `os.environ`
- pyfcstm 走 submodule (pin commit `5f811a0f`)，升级方式：在 submodule 内 `git fetch && git checkout <new-commit>` 后回到主仓 `git add pyfcstm && git commit`
- agent prompt **全英文**（paper 是英文 SE 论文，统一）

## 历史 commit

| commit | 描述 |
| --- | --- |
| (待填) | Phase A：脚手架 + pyfcstm submodule + README + STATUS |
