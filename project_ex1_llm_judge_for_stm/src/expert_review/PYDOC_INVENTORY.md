# `expert_review/` Pydoc 写作 + 死代码清理盘点清单

> **时间**: 2026-05-09 14:50:00 起稿
> **任务**: 用户 W4.x 期间要求 (a) sync `README.md` + `GUIDE.md` 到代码现状；(b) 全部代码加**中文 RST 格式 pydoc**（module / class / func / meth 都要）；(c) 清理死代码
> **状态**: **盘点中**——本文件先列出全部待办项 + 优先级 + 工作量估算，**用户逐一过 / 标优先级后**再开始写
> **输入数据**: AST 全量扫描 64 个 Python 文件 + 死代码引用追溯

---

## 0. 总览

| 维度 | 数字 |
|---|---:|
| Python 文件总数 | **64** |
| Module-level docstring | ✗ 61  /  🇺🇸 3  /  🇨🇳 0 |
| Class + Function + Method | **439** items |
| → 缺 docstring | 424（**96.6%**）|
| → 英文 docstring | 15（3.4%）|
| → 中文 docstring | 0 |
| 总 LOC | 12,208 |

**结论**：基本上**全部从零开始写中文 pydoc**，工作量 ≈ 100% rewrite。

---

## A. 死代码清理候选

### A1. ⚠️ `legacy/` 整目录 — **完全死代码**（强烈建议删除）

| 文件 | 大小 | 内容 | 是否被 import |
|---|---:|---|:-:|
| `legacy/__init__.py` | 508 B | 仅 re-export `prompts.py` + `rubrics.py` 的 7 个符号 | ✗ |
| `legacy/prompts.py` | 13 KB | 旧版 5 维 dimension definitions、`AGENT_SYSTEM_PROMPT`、`render_request_prompt` 等 | ✗ |
| `legacy/rubrics.py` | 1.7 KB | `resolve_review_profile` 旧版 rubric 选择逻辑 | ✗ |

**核查**：`grep -rn "from .legacy\|import .*legacy" src/expert_review/` 仅返回 `legacy/` 自身的 self-import。**外部 0 引用**。

**建议**：`git rm -r src/expert_review/legacy/`（如怕历史丢失，可先 `git mv` 到 `_archive/`）。

- [ ] **A1 决策**：删除 / 移到 _archive / 保留？_______

### A2. `compatibility/` 目录 — **仍活跃但属遗留 shim**

| 文件 | 行数 | 用途 |
|---|---:|---|
| `compatibility/__init__.py` | 3 行 | re-export 3 个 legacy API |
| `compatibility/legacy_api.py` | 41 行 | `heuristic_expert_review`、`review_artifacts`、`review_model` —— 3 个旧 API 入口的薄封装 |

**引用情况**：
- `__main__.py:5` `from .compatibility import review_model`
- `__init__.py:1` `from .compatibility import ...`
- `batch.py:13` `from .compatibility import heuristic_expert_review`
- `test_review.py:9` `from .compatibility import heuristic_expert_review`

**建议**：保留但加 deprecation 注释；建议在 docstring 标注 "legacy entry point, prefer ExpertReviewAgent.review()"。

- [ ] **A2 决策**：保留+加 deprecation 注释 / 重构主代码消除依赖 / 全删并迁移？_______

### A3. ⚠️ `Disagreement Arbiter` 残留字符串

代码中 4 处残留（agent 已从 runtime.py L235 移除调用，但字符串还在）：

| 位置 | 内容 | 行动 |
|---|---|---|
| `graph/edges.py:18` | `FINAL_STAGE` 元组中保留 `"Disagreement Arbiter"` 字符串 | 删除 |
| `agents/orchestrator.py:23` | 同上 | 删除 |
| `agents/score_composer.py:551` | 注释残留 `"The arbiter also found dependency-sensitive..."` | 删除注释 |
| `graph/runtime.py:235-236` | 注释解释为什么删除 | 保留作 audit trail |

- [ ] **A3 决策**：清理 3 处字符串（保留 runtime.py 的 audit 注释）？_______

### A4. `prompts/` 中**纯字符串文件**——是否需要 module docstring 保护？

`prompts/contract_router.py / equivalence.py / extraction.py / missing_evidence.py / quality_review.py / review_policy.py / synthesis.py / traceability.py` 等 8 个文件**只含 prompt 字符串常量**，无任何 class/func。仅 `prompts/rubric_dim_score.py` 有 4 个 def。

**建议**：这 8 个文件**只加 module docstring**（说明该 prompt 的用途、输入输出、被哪个 agent 使用），不需要单独 def docstring。

- [ ] **A4 决策**：8 个 prompts/ 字符串文件只加 module docstring 即可？_______

### A5. `test_*.py` 文件的 docstring 优先级

3 个测试文件：`test_batch.py / test_benchmark.py / test_review.py`，共 57 items。

**建议**：测试文件 **module docstring + 关键测试 class docstring 即可**，单个 test_xxx 函数可不写（Python 测试惯例）。

- [ ] **A5 决策**：tests 只写 module + class，跳过单个 test_func？_______

---

## B. README / GUIDE Sync 待办

### B1. `src/expert_review/README.md` (414 行) — sync 点

读已有 README 后发现以下与 [Part II 代码事实档案](../../discussions/2026-05-09-12-58-25-AI-讨论-prompt实现一致性待处理清单.md) 不一致或过时的点：

- [ ] **README §模块定位**：列了 5 个子目录（schemas / prompts / tools / agents / graph）但少了 `compatibility/ legacy/`——legacy 即将删除可保持不列；compatibility 应注明 deprecated
- [ ] **README §rubric 维度**：是否仍写"7 维 A-G"？（与 Part II §II-D 6 维不一致；待审核）
- [ ] **README §pipeline 阶段**：是否提到 4 阶段？（实际 3 阶段，与讨论稿 §I-18 同 issue）
- [ ] **README §metric 列表**：是否含已废弃的 HAI legacy 公式？需 sync 到 v2 公式
- [ ] **README §Disagreement Arbiter** 描述：需删除（已是死代码）
- [ ] **README §strict-llm 模式**：需澄清是 eval skip flag 而非全局 mode

### B2. `src/expert_review/GUIDE.md` (167 行) — sync 点

GUIDE.md 当前主要列 "1. 目录边界 / 2. 阅读入口"，需检查：

- [ ] **GUIDE §阅读入口**：是否仍指向已不存在的文件？
- [ ] **GUIDE §设计阶段**：phase 5/6/7+ 的标注是否齐？应加 W3 / W4 phase 注解
- [ ] **GUIDE §如何添加新 dim / 新 agent**：是否有？该有

### B3. 用户决策

- [ ] **B 决策**：先生成 README/GUIDE 改写 draft 给用户审，还是用户自己改？_______

---

## C. Pydoc 写作分阶段计划

### Phase 0: 死代码清理 (1-2 小时)

依据 §A 决策结果执行删除 / 注释清理。

### Phase 1 — 核心 schema + 入口（**最高优**，约 3-4 小时）

| 文件 | 行数 | items | 说明 |
|---|---:|---:|---|
| `__init__.py` | - | 0 | 仅加 module docstring，说明 expert_review 包入口 |
| `__main__.py` | - | 1 | CLI 入口 main 函数 |
| `agent.py` | - | 4 | **核心** ExpertReviewAgent class + review() method |
| `schema.py` | - | 17 | **核心** 全部 dataclass：Request / Result / DimensionResult / Evidence / Trace / Issue + judgement_from_score |
| `schemas/__init__.py` | - | 0 | 包入口 |
| `schemas/request.py` | - | 0 | ExpertReviewRequest（兼容） |
| `schemas/result.py` | - | 0 | ExpertReviewResult（兼容） |
| `schemas/dossiers.py` | - | 6 | InputDossier / ArtifactDossier / etc. |
| `schemas/graph_state.py` | - | 1 | ReviewGraphState dataclass |

**Phase 1 小计**：9 文件 / ~29 items + 9 module docstring = ~38 个 docstring

### Phase 2 — graph/ pipeline 编排（约 2-3 小时）

| 文件 | items | 说明 |
|---|---:|---|
| `graph/__init__.py` | 0 | 包入口 |
| `graph/edges.py` | 0 | PREPARATION_STAGE / ANALYSIS_STAGE / FINAL_STAGE 常量（清理 arbiter 后） |
| `graph/subgraphs.py` | 1 | ordered_stage_groups |
| `graph/nodes.py` | 12 | 12 个 agent 节点封装 |
| `graph/runtime.py` | 3 | run_expert_review_workflow + 内部 helpers |

**Phase 2 小计**：5 文件 / 16 items + 5 module = 21

### Phase 3 — agents/（**最大块**，约 6-8 小时）

15 个 agent files + `__init__.py`：

| 文件 | items | 说明 |
|---|---:|---|
| `agents/__init__.py` | 0 | 包入口 |
| `agents/common.py` | 20 | tokenize / overlap_score / make_evidence_item / 等共享工具 |
| `agents/contract_router.py` | 2 | contract 路由 |
| `agents/input_analyst.py` | 3 | NL requirement 解析 |
| `agents/prediction_extractor.py` | 1 | pred artifact 解析 |
| `agents/reference_extractor.py` | 1 | ref artifact 解析 |
| `agents/evidence_regime_estimator.py` | 2 | regime 估计 |
| `agents/review_policy_builder.py` | 3 | policy_packet 构造 |
| `agents/traceability.py` | 4 | trace_results |
| `agents/equivalence.py` | 10 | equivalence_strength + contradictions（10 items 偏多，需细查）|
| `agents/pragmatic_quality.py` | 4 | quality_score_hint |
| `agents/missing_evidence_critic.py` | 3 | confidence_cap + warnings + vv_roles |
| `agents/orchestrator.py` | 3 | run_parallel + record_agent_context |
| `agents/rubric_scorer.py` | 5 | **核心** llm_rubric_score + sanity bound + RubricScore 🇺🇸→🇨🇳 |
| `agents/score_composer.py` | 9 | **最大** mode-specific blend + post-transform + overall_score 整形 |
| `agents/final_synthesizer.py` | 5 | judgement_anchor + strengths/weaknesses + synthesize_result |
| `agents/llm_helpers.py` | 4 | invoke_llm_json + record_llm_operation 🇺🇸→🇨🇳 |

**Phase 3 小计**：17 文件 / 79 items + 17 module = 96

### Phase 4 — prompts/（约 1-2 小时，多数仅 module docstring）

| 文件 | items | 说明 |
|---|---:|---|
| `prompts/__init__.py` | 0 | 包入口 |
| `prompts/contract_router.py` | 0 | 仅 prompt 字符串 |
| `prompts/extraction.py` | 0 | 同上 |
| `prompts/equivalence.py` | 0 | 同上 |
| `prompts/missing_evidence.py` | 0 | 同上 |
| `prompts/quality_review.py` | 0 | 同上 |
| `prompts/review_policy.py` | 0 | 同上 |
| `prompts/synthesis.py` | 0 | 同上 |
| `prompts/traceability.py` | 0 | 同上 |
| `prompts/rubric_dim_score.py` | 4 | **核心** _DIM_RUBRICS + build_rubric_prompt + DIM_SCORE_JSON_SCHEMA 🇺🇸→🇨🇳 |

**Phase 4 小计**：10 文件 / 4 items + 10 module = 14

### Phase 5 — tools/（约 3-4 小时）

| 文件 | items | 说明 |
|---|---:|---|
| `tools/__init__.py` | 0 | 包入口 |
| `tools/policy_library.py` | 19 | VV_ROLE_HINTS + build_review_policy + detect_vv_roles + 各 SemanticCategory |
| `tools/structured_extract.py` | 3 | extract_artifact_dossier |
| `tools/artifact_io.py` | 2 | I/O 工具 |
| `tools/artifact_probe.py` | 8 | format_guess + observability + element 探测 |
| `tools/dossier_merge.py` | 4 | dossier 合并 |
| `tools/known_format_lift.py` | 18 | PlantUML / SysML / FSM 等已知格式提升 |
| `tools/validation.py` | 4 | validate_result_shape + json_safe_report 等 |

**Phase 5 小计**：8 文件 / 58 items + 8 module = 66

### Phase 6 — utils + 顶层（约 1-2 小时）

| 文件 | items | 说明 |
|---|---:|---|
| `utils.py` | 12 | PROVIDER_CONFIGS / DEFAULT_PROVIDER_ORDER / resolve_api_env 等 |
| `inventory.py` | 19 | parse_requirement_items + dataset inventory |
| `llm_telemetry.py` | 10 | LLMUsageSummary / record_llm_operation |
| `semantic_router.py` | 9 | SemanticCategory + semantic_single_label / multi_label |
| `fallback_llm.py` | 13 | FallbackLLMClient 🇺🇸→🇨🇳 |

**Phase 6 小计**：5 文件 / 63 items + 5 module = 68

### Phase 7 — benchmark + batch（**最大文件**，约 5-6 小时）

| 文件 | items | 说明 |
|---|---:|---|
| `benchmark.py` | **109** | 最大文件，含全部 metric 公式 + checkpoint + rerun + report 渲染 |
| `batch.py` | 16 | 批量任务调度 |

**Phase 7 小计**：2 文件 / 125 items + 2 module = 127

### Phase 8 — tests（约 1-2 小时，按 §A5 决策）

| 文件 | items | 说明 |
|---|---:|---|
| `test_batch.py` | 4 | |
| `test_benchmark.py` | 22 | |
| `test_review.py` | 31 | |

**Phase 8 小计**：3 文件 / 57 items + 3 module = 60（如按 §A5 跳过单个 test func，则只剩 ~10 docstring）

### Phase 9 — compatibility（约 0.5 小时）

| 文件 | items | 说明 |
|---|---:|---|
| `compatibility/__init__.py` | 0 | |
| `compatibility/legacy_api.py` | 3 | 加 deprecation 注释 |

**Phase 9 小计**：2 文件 / 3 items + 2 module = 5

### 总工作量估算

| Phase | 文件 | items | 估时（小时）|
|---|---:|---:|---:|
| Phase 0 死代码 | - | - | 1-2 |
| Phase 1 schema + 入口 | 9 | 29 | 3-4 |
| Phase 2 graph | 5 | 16 | 2-3 |
| Phase 3 agents | 17 | 79 | 6-8 |
| Phase 4 prompts | 10 | 4 | 1-2 |
| Phase 5 tools | 8 | 58 | 3-4 |
| Phase 6 utils + 顶层 | 5 | 63 | 1-2 |
| Phase 7 benchmark | 2 | 125 | 5-6 |
| Phase 8 tests | 3 | 57 | 1-2 |
| Phase 9 compatibility | 2 | 3 | 0.5 |
| **总计** | **64** | **434** | **~25-35 小时** |

> 工作量很大。建议**分多次 commit**，每个 phase 一次。

---

## D. 完整文件 docstring 清单

> 状态符号：✗ 缺 / 🇺🇸 英文 / 🇨🇳 中文（目标）
> Cls = class，Fn = func，Mth = method，L = 行号

### Phase 1 — 核心 schema + 入口

#### `__init__.py`  module:✗
（仅加 module docstring）

#### `__main__.py`  module:✗
- [ ] ✗ `Fn ` `main` (L9)

#### `agent.py`  module:✗
- [ ] ✗ `Cls` `ExpertReviewAgent` (L19)
- [ ] ✗ `Mth` `ExpertReviewAgent.__init__` (L20)
- [ ] ✗ `Mth` `ExpertReviewAgent._build_llm` (L37)
- [ ] ✗ `Mth` `ExpertReviewAgent.review` (L58)

#### `schema.py`  module:✗
- [ ] ✗ `Cls` `DimensionDefinition` (L11)
- [ ] ✗ `Cls` `EvidenceItem` (L23)
- [ ] ✗ `Cls` `TraceLink` (L31)
- [ ] ✗ `Cls` `ElementIssue` (L49)
- [ ] ✗ `Cls` `DimensionReviewResult` (L58)
- [ ] ✗ `Cls` `ExpertReviewRequest` (L72)
- [ ] ✗ `Cls` `ExpertReviewResult` (L81)
- [ ] ✗ `Mth` `ExpertReviewResult.to_dict` (L96)
- [ ] ✗ `Mth` `ExpertReviewResult.to_json` (L99)
- [ ] ✗ `Mth` `ExpertReviewResult.from_dict` (L102)
- [ ] ✗ `Fn ` `judgement_from_score` (L116)
- [ ] ✗ `Fn ` `_dim_to_dict` (L130)
- [ ] ✗ `Fn ` `_evidence_to_dict` (L150)
- [ ] ✗ `Fn ` `_trace_to_dict` (L160)
- [ ] ✗ `Fn ` `_issue_to_dict` (L170)
- [ ] ✗ `Fn ` `_dim_from_dict` (L180)
- [ ] ✗ `Fn ` `_safe_str` (L195)

#### `schemas/__init__.py`  module:✗
（仅加 module docstring）

#### `schemas/request.py`  module:✗
（仅加 module docstring + 1 个 dataclass class docstring 通过 `__init__.py` 暴露）

#### `schemas/result.py`  module:✗
（同上）

#### `schemas/dossiers.py`  module:✗
- [ ] ✗ `Cls` `ArtifactDossier` (...)
- [ ] ✗ `Cls` `ArtifactElement` (...)
- [ ] ✗ `Cls` `ArtifactRelation` (...)
- [ ] ✗ `Cls` `InputDossier` (...)
- [ ] ✗ `Cls` `EvidenceRegime` (...)
- [ ] ✗ `Cls` `等` (待 AST 详查)

#### `schemas/graph_state.py`  module:✗
- [ ] ✗ `Cls` `ReviewGraphState` (...)

### Phase 2 ~ Phase 9: 详细列表

> 因列表过长（共 ~600 行），完整 per-file checklist 见 `[/tmp/pydoc_items.txt](已生成)` 或下面 §D-EXT 单独文件 `PYDOC_ITEMS.md`（建议 split 出去）

---

## E. 写作规范（中文 RST 格式）

### Module-level docstring 模板

```python
"""模块标题（一行）

模块作用与设计思路（2-4 段，必须含）：

1. **作用**：本模块提供 XXX 功能；负责 X / Y / Z；典型调用方为 ZZZ。
2. **设计思路**：为何这样设计、与上下游模块的边界、核心抽象。
3. **关键约束 / 不变式**：例如必须先调用 X 才能调用 Y、单例性、线程安全性等。
4. （可选）历史变迁 / 已知 caveat：例如某 phase 引入、某 issue 跟踪中、某 fallback 逻辑。

参考：

- 总体方法论： :doc:`../../../discussions/2026-05-08-19-20-31-AI-讨论-project_ex1学术定位与相关工作综述`
- 实现 issue： :doc:`../../../discussions/2026-05-09-12-58-25-AI-讨论-prompt实现一致性待处理清单`
"""
```

### Class-level docstring 模板

```python
class ExpertReviewAgent:
    """Expert Review Agent — pipeline 主入口。

    本 class 装配 fallback LLM chain、调度 ``run_expert_review_workflow``
    并返回 :class:`ExpertReviewResult`。

    :ivar model_name: LLM model 名（如 ``gpt-4o-2024-08-06``）。
    :ivar provider_order: provider 优先级列表，由 ``DEFAULT_PROVIDER_ORDER`` 默认提供。
    :ivar temperature: 调用温度，默认 0。
    :ivar timeout: 单次调用上限秒数；同时受 ``PROVIDER_FALLBACK_TIMEOUT`` 约束。

    设计思路:
        1. 与 ``run_expert_review_workflow`` 解耦——本 class 只负责装配 + 调度
        2. fallback chain 由 ``fallback_llm.build_fallback_chain`` 构造，
           异常处理与 cooldown 在 chain 内部，不在本 class 暴露
        3. ``review()`` 方法是同步入口，未来可扩 ``review_async``
    """
```

### Function / Method docstring 模板（RST 风格）

```python
def llm_rubric_score(
    dim_name: str,
    *,
    pred_summary: str,
    ref_summary: str | None,
    input_summary: str,
    regime_label: str,
    deterministic_estimate: float,
    extra_signals: dict[str, Any] | None = None,
    llm: Any = None,
    asymmetric_bounds: bool = False,
    differentiation_mode: bool = False,
    prompt_variant: str = "v1",
    temperature_override: float | None = None,
) -> RubricScore:
    """对单个 rubric 维度跑一次 LLM 评分。

    完整流程:
        1. 装配 prompt （ ``build_rubric_prompt`` ）
        2. 强 JSON schema 调用 LLM
        3. 三重 sanity 防线 (JSON 校验 → hard reject → soft clip)
        4. 失败时回退到 deterministic_estimate

    :param dim_name: 维度标识，必须在 ``SUPPORTED_DIMS`` 内
    :param pred_summary: 预测制品文本（已截断到 800 字符以内）
    :param ref_summary: 参考制品文本，可为 None
    :param input_summary: NL 需求文本
    :param regime_label: regime 标识，影响 sanity bound 选取
    :param deterministic_estimate: 启发式先验估计 (∈ [0, 1])，
        作为 sanity bound 的 anchor 中心
    :param extra_signals: 辅助信号 dict（trace_ratio / contradiction_count 等），
        会嵌入 prompt 让 LLM 参考
    :param llm: ChatOpenAI 实例；若 None 则直接返回 deterministic 兜底
    :param asymmetric_bounds: Iter-A flag — 启用按 (regime, dim) 不对称 sanity 边界
    :param differentiation_mode: Iter-B flag — 让 LLM 拒绝 default 到中线
    :param prompt_variant: ``"v1"`` / ``"v2"`` / ``"v3"`` paraphrase 变体
    :param temperature_override: 单次调用温度覆盖
    :return: :class:`RubricScore` dataclass，含 score、band、reason、
        confidence、sanity_clipped 等字段
    :rtype: RubricScore
    :raises ValueError: 当 ``dim_name`` 不在 ``SUPPORTED_DIMS`` 内

    .. note::
        本函数当前在 ``llm is None`` / JSON 异常 / score 越界 / hard reject
        4 种情况下**静默** fallback 到 deterministic estimate；与 strict-llm
        协议存在矛盾。详见 issue I-4。
    """
```

### 待用户决策的写作细节

- [ ] **E1 决策**：所有 module docstring 必须含 4 个段落（作用 / 设计思路 / 关键约束 / caveat），还是允许灵活？
- [ ] **E2 决策**：method docstring 是否每个 :param 都要写？私有 _ 开头的 method 是否简化？
- [ ] **E3 决策**：是否在每个 docstring 末尾加 `.. seealso::` 链回讨论稿 issue？
- [ ] **E4 决策**：dataclass `@dataclass` 是否需要每个字段都加 `:ivar:`？还是用 ``Attributes:`` Google 风格？

---

## F. 处理顺序（建议）

1. **先决 §A 死代码**（用户拍板 A1 删 legacy / A2 保留 compatibility / A3 清 arbiter 残留 / A4 prompts only-module / A5 tests 简化）
2. **执行 Phase 0 死代码清理**（git rm legacy/ + 清理 arbiter 字符串）
3. **决 §B README/GUIDE sync 范围**（用户口头说要改哪些点）
4. **执行 Phase 1 schema + 入口**（小但关键）
5. **决 §E 写作规范细节**
6. **逐步执行 Phase 2 ~ Phase 9**，每个 phase 单独 commit
7. **最后做 README/GUIDE sync**（依赖前面的 docstring，最后 sync 反而准确）

---

## G. 关于本文件的状态管理

- 每个 [ ] 处理完后改为 [x]
- §C 各 phase 完成后在标题加 ✅
- §A / §B 决策完成后把决议写到对应位置
- 全部完成后归档为 "process log"

