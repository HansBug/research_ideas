# S2-Q1 Rubric Design — 6 Dim Form-Filling Score Rubrics

> **Spec source**：[Week 0 复命 PR comment](https://github.com/HansBug/research_ideas/pull/6#issuecomment-4387342325) §8 七条 acceptance gate；[review-quality-first 路线图](https://github.com/HansBug/research_ideas/pull/6#issuecomment-4386634782) §四。
>
> **核心设计目标**：把 `score_composer.py` lines 159-182 的 6 个 deterministic dim 公式替换为 LLM rubric-based scoring；保留 lines 184-213 的 summary_mode / protocol_mode / component_review_mode post-transforms（[ablation §C.5](https://github.com/HansBug/research_ideas/pull/6#issuecomment-4379802749) 已证它们贡献 +10.6 HAI）。
>
> **Sanity bound**：每个 dim 的 LLM 输出 score 必须在 deterministic 估计 ±0.20 内，否则 fallback 到 deterministic（防 LLM 在 record regime 给 ScoreAlign −19.30 那种暴跌）。

---

## 0. 共用约定

### 0.1 Score band（5 档，所有 dim 通用）

| Score | Label | 含义 |
|---:|---|---|
| 1.0 | excellent | 该 dim 维度上几乎无可挑剔，可以直接采用 |
| 0.7 | good | 主要要素正确，仅有少量可改进点 |
| 0.5 | acceptable | 关键缺陷已识别，artifact 需要修复后才能采用 |
| 0.3 | weak | 多个关键缺陷，artifact 不可用 |
| 0.0 | poor | 该 dim 完全失败（无法解析 / 完全偏离）|

允许中间值（0.2 / 0.4 / 0.6 / 0.8 / 0.9），但**LLM 必须能匹配到上述 5 档之一并给出 reason**。

### 0.2 LLM 输出 form-filling JSON schema

```json
{
  "dimension": "notation_syntax",
  "score": 0.7,
  "band": "good",
  "reason_anchor_id": "uml_anchor_2",      // 所选 anchor example 的 id（可选）
  "reason_text": "PlantUML structure is valid; one transition uses non-canonical naming.",
  "specific_defects": [                     // 0-3 条具体缺陷（用于 critique-first 信号）
    {"locator": "transition:line:7", "snippet": "->>>", "issue": "non-canonical arrow"}
  ],
  "confidence": 0.85                        // LLM 自报置信度
}
```

### 0.3 Sanity bound（防 LLM 暴跌或暴升）

| Dim | deterministic 估计参考 | sanity bound |
|---|---|---|
| `notation_syntax` | `format_guess + observability` heuristic | `[det − 0.20, det + 0.30]` |
| `semantic_completeness` | `0.18 + 0.78·trace_ratio − 0.08·harmful` | `[det − 0.20, det + 0.20]` |
| `behavioral_consistency` | `0.20 + 0.72·equivalence_strength − 0.12·contradictions` | `[det − 0.20, det + 0.20]` |
| `requirement_traceability` | `0.18 + 0.76·trace_ratio − 0.07·harmful` | `[det − 0.15, det + 0.15]`（更紧，因为 trace_ratio 是硬证据）|
| `pragmatic_clarity` | `quality_report.clarity_score_hint − 0.04·harmful` | `[det − 0.25, det + 0.25]` |
| `evidence_discipline` | `0.82 − evidence_critic.confidence_cap_penalty − 0.08·warnings` | `[det − 0.15, det + 0.15]` |

如果 LLM 输出超出 bound：取 bound 边界值 + 标 `sanity_clipped: true` 在 metadata。

### 0.4 Fallback 策略

LLM 调用失败 / 返回 invalid JSON / score 不在 [0,1] / 超出 sanity bound 太远（>2x bound）：→ fallback 到 deterministic 公式 + 标 `used_review_backend: rubric_fallback_deterministic`。

---

## 1. `notation_syntax` — 句法 / 记号合规性

### 1.1 这个 dim 评什么

prediction artifact 是否使用规范的状态机记号（PlantUML / SysML / TURTLEGMODELING / JSON FSM 等），是否能被对应工具解析，是否使用了非标准命名或语法错误。**重点是"能不能被工具吃下去"，不是语义对错**。

### 1.2 Rubric

| Score | 标准 |
|---:|---|
| 1.0 | 完全合规的 canonical 语法（PlantUML / SysML XML / 标准 JSON FSM），所有 element 命名规范，工具直接可解析 |
| 0.7 | 主要语法合规，少量非规范命名（如 `SYN_RECEIVED` 写成 `SYN-RECEIVED`）或冗余结构（如多余的 `state` 包裹）|
| 0.5 | 部分语法错误但人工可读（如 missing `@enduml`、transition 标签不规范），但状态/迁移仍可识别 |
| 0.3 | 多处语法问题导致工具难以解析（嵌套不闭合、关键字拼错、混用记号），需要重写大半 |
| 0.0 | 完全无法解析（不是状态机、是错误的代码 fragment、空字符串）|

### 1.3 Anchor examples

**Anchor uml_anchor_1 (score=1.0)**: 来自 `llms_emp::GPT-4` 高分 case，PlantUML 标准 act 图，所有 keyword 规范，工具可直接渲染。

**Anchor uml_anchor_2 (score=0.7)**: 来自 `psmbench::TCP::deepseek-reasoner`（human F1=0.883）：
```
@startuml
' initial: CLOSED
CLOSED --> SYN_SENT : cond active_open/send SYN
LISTEN --> SYN_RECEIVED : receive SYN/send SYN_ACK
SYN_SENT --> ESTABLISHED : receive SYN_ACK/send ACK
...
```
主体 PlantUML 合规，但 `cond active_open/` 语法在 PlantUML 不是标准 guard 写法（应该是 `[active_open]`）。

**Anchor protocol_anchor_3 (score=0.3)**: 来自 `psmbench::DCCP::mistral-small3.1`（human F1=0.000）：
```
@startuml
Received --> Acknowledged : receive DataChecksum/set CheckDataChecksum true
```
状态命名极不规范（`CheckDataChecksum true` 是 action 但写成 atom 名），关键状态缺失，难以作为 DCCP FSM 解析。

### 1.4 Common pitfalls

- ❌ **不要因为 prediction 本身没 bug 就给 1.0** — 规范命名 / 语法对工具可解析才能 1.0
- ❌ **不要因为格式好看就忽略 keyword 错误** — `cond X/` 不等于 `[X]`
- ✅ **当 reference 不存在时，仍可独立评 syntax**

---

## 2. `semantic_completeness` — 语义完备性

### 2.1 这个 dim 评什么

prediction 是否覆盖了 input requirement 中所有该建模的关键行为（matched 需求比例）+ 是否引入了 input 中没要求的额外行为（harmful_extras）。**重点是"没漏没多"**。

### 2.2 Rubric

| Score | 标准 |
|---:|---|
| 1.0 | matched_ratio ≥ 0.85，harmful_extras=0，所有需求点都有对应建模 |
| 0.7 | matched_ratio ≥ 0.65，harmful_extras ≤ 1，主要需求覆盖 |
| 0.5 | matched_ratio ≥ 0.40，关键需求点有缺失但**主流程可识别** |
| 0.3 | matched_ratio < 0.40，多数需求未建模 / 大量 harmful_extras |
| 0.0 | matched_ratio = 0，prediction 完全偏离 input 要求 |

### 2.3 Anchor examples

**Anchor uml_anchor_1 (score=1.0)**: `llms_emp::GPT-4`，act 图 5 个判断 + 2 个 print 都对应需求 1:1，无多余分支。

**Anchor protocol_anchor_2 (score=0.5)**: `psmbench::TCP::claude-3-7-sonnet`：覆盖 7/11 状态（CLOSED/LISTEN/SYN_SENT/SYN_RECEIVED/ESTABLISHED/CLOSE_WAIT/TIME_WAIT），缺 FIN_WAIT_1/FIN_WAIT_2/CLOSING/LAST_ACK 4 个。

**Anchor protocol_anchor_3 (score=0.0)**: `psmbench::SMTP::mistral-small3.1`：只有 3 个状态、F1=0；SMTP 应有 11+ 状态。

### 2.4 Common pitfalls

- ❌ **不要因为 input_text 薄就直接给低分** — 看 input 表达的需求量级，不是字数
- ❌ **harmful_extras 不等于额外细化** — 必须是 input 没说但 prediction 假设了的"无中生有"
- ✅ **trace_ratio 是先验信号** — score 应该 ≈ 0.18 + 0.78·trace_ratio ± rubric 调整

---

## 3. `behavioral_consistency` — 行为一致性

### 3.1 这个 dim 评什么

prediction 与 reference（如有）的**行为等价性**：哪怕结构不同，只要语义一致也算等价。重点检测 contradictions（明显矛盾）和 dependency_breaks（先后依赖错位）。

### 3.2 Rubric

| Score | 标准 |
|---:|---|
| 1.0 | equivalence_strength ≥ 0.85，无 contradictions，无 dependency_breaks |
| 0.7 | equivalence_strength ∈ [0.60, 0.85)，contradictions=0，主流程行为等价 |
| 0.5 | equivalence_strength ∈ [0.40, 0.60)，少量 contradictions，部分主流程缺失或顺序错 |
| 0.3 | contradictions ≥ 2 或主流程行为反向 |
| 0.0 | 完全不等价 / 无 reference 且 prediction 不自洽 |

### 3.3 Anchor examples

**Anchor uml_anchor_1 (score=1.0)**: `llms_emp::GPT-4o`：reference act 图 5 节点，prediction 与 reference 1:1 节点对应，无矛盾。

**Anchor protocol_anchor_2 (score=0.5)**: `psmbench::DCCP::deepseek-chat`：4 transitions，但缺 retransmission 路径，仅主连接握手 OK。

**Anchor uml_anchor_3 (score=0.3)**: `llms_emp::GPT-4o`（human F1=0.128）seq 图，多处 transition 反向（应该是 MES → WMS 但 prediction 给的是 WMS → MES）。

### 3.4 Common pitfalls

- ❌ **结构不一致 ≠ 行为不一致** — equivalence_strength 优先看语义不看 isomorphism
- ❌ **无 reference 时不要给 1.0** — 没有比较基准时 0.5 是上限
- ✅ **contradiction_count > 0 直接限制到 ≤ 0.5**

---

## 4. `requirement_traceability` — 需求可追溯性

### 4.1 这个 dim 评什么

input_text 中的每条需求是否能在 prediction 中找到对应 element / transition / action 锚定。**这是最严的一维**：trace_ratio 是硬证据，不能凭"看着像"给高分。

### 4.2 Rubric

| Score | 标准 |
|---:|---|
| 1.0 | 100% 需求都有 prediction 元素对应（matched，无 partial）|
| 0.7 | matched_ratio ≥ 0.70 + partial_ratio < 0.20 |
| 0.5 | matched_ratio ≥ 0.40，剩余主要是 partial（不是 missing）|
| 0.3 | matched_ratio < 0.40 或 missing_ratio > 0.50 |
| 0.0 | matched_ratio = 0（无任何需求成功 trace）|

### 4.3 Anchor examples

**Anchor uml_anchor_1 (score=1.0)**: `llms_emp::GPT-4` act 图，5 条需求全部 trace 到对应 plantuml 节点。

**Anchor protocol_anchor_2 (score=0.0)**: `psmbench::TCP::claude-3-7-sonnet`：input 给的是 RFC 章节摘要"Section 1. Purpose and Scope"，prediction 里没有任何元素对应章节标题；trace_ratio 必然是 0，**这是 input_text 上下文不足导致的，不是 prediction 错**。

**Anchor uml_anchor_3 (score=0.5)**: `ttool-ai::connected_device`：5 条需求中 2 条直接 match，1 条 partial（同一对象不同 attribute），2 条 missing（detection logic 缺失）。

### 4.4 Common pitfalls

- ❌ **不要凭直觉给分** — 这一维度的 score **必须**贴近 trace_ratio 的硬证据
- ❌ **input_text 太薄时给 0 不 fair** — 但仍是诚实评分；rubric 注释里要写"context_thin: true"
- ✅ **sanity bound 这一维设最紧**（±0.15）

---

## 5. `pragmatic_clarity` — 实用清晰度

### 5.1 这个 dim 评什么

prediction 作为给 SE / domain expert 阅读的工件，命名是否合理、结构是否易读、有无 generic placeholder（如 `state1`/`event_a`）、复杂度是否对应需求规模（不要 over-engineer 也不要 under-engineer）。

### 5.2 Rubric

| Score | 标准 |
|---:|---|
| 1.0 | 命名清晰 (语义明确)，结构与需求规模匹配，无 generic 占位 |
| 0.7 | 大部分命名好，少量 generic（如 1-2 个 `state_x`），整体易读 |
| 0.5 | 多处 generic 命名 / over-engineered（远超需求规模）/ under-engineered |
| 0.3 | 大量无意义命名 + 复杂度严重失配 |
| 0.0 | 全部 generic 或完全无法读 |

### 5.3 Anchor examples

**Anchor uml_anchor_1 (score=1.0)**: `ttool-ai::automated_braking` (human F1=0.85)：状态命名 `BrakeReady` / `Braking` / `BrakeReleased` 都是 domain term。

**Anchor protocol_anchor_2 (score=0.7)**: `psmbench::TCP::deepseek-reasoner`：协议状态名规范，但 transition 上的 action 用了 `set CheckDataChecksum true` 这种过度细节。

**Anchor uml_anchor_3 (score=0.3)**: 假设 case：5 个状态全部命名 `state0` / `state1` / ... — generic 占位泛滥。

### 5.4 Common pitfalls

- ❌ **不要因为生成了多就给低分** — 复杂度匹配需求即可
- ✅ **特别注意 generic_name_count**：每出现一个 `state_x` 类占位，−0.05

---

## 6. `evidence_discipline` — 证据纪律性

### 6.1 这个 dim 评什么

reviewer 自身的"克制"程度：是否有 prediction 之外的额外发明（unsupported claims）、reason_text 是否离 evidence 过远、是否在没 reference 时仍敢给 confident 高分。**这一维是 reviewer 给自己打分**。

### 6.2 Rubric

| Score | 标准 |
|---:|---|
| 1.0 | 所有 claim 都有 locator + snippet 对应；reason_text 完全基于 evidence；confidence 与 evidence 量匹配 |
| 0.7 | 主要 claim 有 evidence，少量 reason 偏离（< 20% claim 无 locator）|
| 0.5 | 部分 claim 缺 locator，reviewer 仍敢给 confident 高分 |
| 0.3 | 多数 claim 无 evidence support，reason 凭空发挥 |
| 0.0 | 完全无 evidence 链路 |

### 6.3 Anchor examples

**Anchor uml_anchor_1 (score=1.0)**: 所有 6 个 dim 的 issue 都有 `locator: prediction:relation:5` + 真实 snippet。

**Anchor protocol_anchor_2 (score=0.7)**: PSMBench TCP review 中，notation_syntax 给了 evidence，但 evidence_discipline 自身是 deterministic（这是当前 bug，rubric 该 dim 应该让 LLM 真自评）。

### 6.4 Common pitfalls

- ❌ **不要给自己打 1.0** — 即使全部 claim 都有 locator 也要看 confidence 是否合理
- ✅ **没 reference 时这一维度 ≤ 0.7**

---

## 7. Implementation outline（Day 3 实现入口）

```python
# agents/rubric_scorer.py (NEW)
def llm_rubric_score(
    dim_name: str,
    dim_def: DimensionDefinition,
    pred_dossier, ref_dossier, regime, policy_packet,
    trace_ratio: float, equivalence_strength: float,
    deterministic_estimate: float,
    llm_client,
) -> tuple[float, dict]:
    """Return (score, metadata)."""
    rubric = RUBRICS[dim_name]
    prompt = build_rubric_prompt(rubric, pred_dossier, ref_dossier, regime, ...)
    response = llm_client.complete_json(prompt, schema=DIM_SCORE_SCHEMA)
    score = response.get("score", deterministic_estimate)
    # Sanity bound
    bound = SANITY_BOUNDS[dim_name]
    lo = max(0.0, deterministic_estimate + bound[0])
    hi = min(1.0, deterministic_estimate + bound[1])
    if not lo <= score <= hi:
        # Out of bound — clip and flag
        score = max(lo, min(hi, score))
        response["sanity_clipped"] = True
    return score, response
```

```python
# agents/score_composer.py (PATCH at lines 159-182)
if policy_packet.get("rubric_llm_enabled", False) and llm_client:
    syntax_score, syntax_meta = llm_rubric_score("notation_syntax", ..., det_syntax_score, ...)
    completeness_score, ... = llm_rubric_score("semantic_completeness", ..., det_completeness, ...)
    # ... 6 dims
else:
    # Fallback to existing deterministic formulas (keep them as-is)
    syntax_score = ...  # current formula
```

`policy_packet["rubric_llm_enabled"]` 是 feature flag，A/B 测试用。

---

## 8. Acceptance gate（Week 1 验收对照 [Week 0 baseline](https://github.com/HansBug/research_ideas/pull/6#issuecomment-4387342325)）

| Gate | 当前 baseline | Week 1 目标 |
|---|---:|---|
| HAI new | 85.02 | **≥ 85.02**（不准退） |
| RAS | 83.71 | **≥ 80**（rubric 不许把 record 拖坍） |
| SAS | 71.77 | **≥ 71.77** 或 **summary ScoreAlign ≥ 60** |
| record ScoreAlign | 69.79 | **≥ 65**（不许出现 LLM-mode 那种 76→57 暴跌） |
| summary RankAlign | 59.40 | **≥ 65**（往 LLM-mode 已实测的 69.17 推进） |
| summary Spearman | 0.376 | **≥ 0.45** |
| 8 worst PSMBench LOFO ρ | 全 ≤ 0 | **至少 4/8 ρ ≥ 0** |
| critical_issue_recall | 0.94 | **≥ 0.90** |
| weighted_kappa | 0.69 | **≥ 0.65** |

**Hard fail**：若 HAI new < 84，rubric 设计回炉，不进入 Week 2。

---

## 9. 工作日历

| Day | 任务 |
|---:|---|
| 1（今天） | 完成本 RUBRIC_DESIGN.md（你正在读） |
| 2 | 6 个 dim 的 rubric prompt template + JSON schema 实现（`prompts/rubric_*.py`），收集 anchor examples 到 `RUBRIC_ANCHORS.md` |
| 3 | `agents/rubric_scorer.py` 实现 + 集成到 `score_composer.py` 的 feature flag |
| 4 | Micro ablation：5-row slice 跑 rubric vs det vs current LLM-mode |
| 5 | 修 bug + iterate（特别是 sanity bound 触发率） |
| 6 | 在 Week 0 同 slice (62 task) 上跑 rubric-LLM，对比 baseline |
| 7 | 在 combined 973 行的 LOFO 抽样上验证 8 worst family ρ；写 Week 1 复命 PR comment + push |

---

## 10. 风险与回退

| 风险 | 概率 | 回退方案 |
|---|:---:|---|
| LLM 输出 JSON 不合规 | 中 | 用 strict json schema validator，无效则 fallback deterministic |
| Sanity bound 触发率 > 30% | 中 | 调整 bound 范围或回炉 prompt |
| HAI 比 baseline 低 ≥ 2 分 | 中 | 不进 Week 2，分析具体哪个 dim 拖低 |
| LLM 延迟 > 200s/record | 低 | 选择性只对 summary regime 启用 rubric |
| Cost 爆表 | 低 | rubric 不带太多 anchor，prompt 控制在 1500 tokens 内 |
