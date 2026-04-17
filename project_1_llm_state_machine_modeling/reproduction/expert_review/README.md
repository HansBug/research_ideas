# Expert Review

`expert_review` 是一个面向状态机建模结果的专家评审模块。它接收：

1. `prompt`
2. `input_text`
3. `pred_output`
4. 可选 `ref_output`

然后输出结构化的 `ExpertReviewResult`，用于回答“这个预测模型是否覆盖需求、是否行为一致、是否引入了没有依据的额外结构，以及当前结论有多可靠”。

## 模块定位

这个目录当前已经不是早期那种“单大文件 heuristic reviewer”。`Phase 5/6` 之后，正式运行时已经稳定收敛到：

1. [`schemas/`](./schemas/)
2. [`prompts/`](./prompts/)
3. [`tools/`](./tools/)
4. [`agents/`](./agents/)
5. [`graph/`](./graph/)
6. [`compatibility/`](./compatibility/)

根层现在只保留对外入口、共享 schema、少量共享 helper，以及 benchmark 回放脚本，不再继续堆积长名字的大杂烩文件。

## 根层结构

当前根层文件职责如下：

| 路径 | 职责 |
|---|---|
| [__init__.py](./__init__.py) | 对外 Python API 导出：`ExpertReviewAgent`、`ExpertReviewRequest`、`ExpertReviewResult`、`review_artifacts()`、`review_model()` |
| [__main__.py](./__main__.py) | CLI 入口，支持 `python -m expert_review` |
| [agent.py](./agent.py) | 外部 agent 壳层，负责 provider 选择、LLM 初始化与 deterministic fallback |
| [schema.py](./schema.py) | 对外稳定 schema 与 JSON/flat-row 转换 |
| [inventory.py](./inventory.py) | 根层共享 inventory / requirement / artifact helper |
| [utils.py](./utils.py) | 根层共享环境解析、规范化与通用计算 helper |
| [benchmark.py](./benchmark.py) | 离线 benchmark replay 与评测汇总，不属于线上运行时主路径 |
| [batch.py](./batch.py) | batch screening 入口，负责批量执行、triage、导出与运行统计 |
| [test_review.py](./test_review.py) | 模块级最小回归测试 |
| [test_benchmark.py](./test_benchmark.py) | benchmark harness 的切片、coverage、LOFO 单测 |
| [test_batch.py](./test_batch.py) | batch triage / export / CLI 面的最小回归测试 |
| [GUIDE.md](./GUIDE.md) | 目录级维护规则 |
| [designs/README.md](./designs/README.md) | 设计与演化文档入口 |

本轮已经把根层长名字文件收敛为更短、更可读的命名：

1. `expert_review_agent.py` -> `agent.py`
2. `expert_review_schema.py` -> `schema.py`
3. `expert_review_self_iteration.py` -> `benchmark.py`
4. `expert_review_tools.py` -> `inventory.py`
5. `expert_review_utils.py` -> `utils.py`
6. `test_expert_review.py` -> `test_review.py`

历史 prompt / rubric 汇总文件也已经移到 [`legacy/`](./legacy/) 下，避免继续污染主路径。

## 真实运行时架构

### 入口层

外部调用通常只经过三层：

1. [`__init__.py`](./__init__.py)：导出稳定 API
2. [`compatibility/legacy_api.py`](./compatibility/legacy_api.py)：兼容历史调用名
3. [`agent.py`](./agent.py)：构造 `ExpertReviewAgent` 并决定 LLM / deterministic 路径

`agent.py` 的行为很简单：

1. 从 [`utils.py`](./utils.py) 读取 provider 环境变量
2. 按 `DEFAULT_PROVIDER_ORDER` 选择可用 provider
3. 如果 LLM 可用，则走 LLM-enhanced workflow
4. 如果 LLM 不可用或运行失败，则回退到 deterministic workflow

因此，外部接口兼容性和内部多智能体实现是分开的。对使用方来说，`review_artifacts()` / `review_model()` 不需要知道图内部怎么编排。

### 正式代码层

真实主路径分成六层：

1. [`schemas/`](./schemas/)：内部 request / dossier / graph state / result 结构
2. [`prompts/`](./prompts/)：contract、policy、extraction、analysis、synthesis prompt 模板
3. [`tools/`](./tools/)：artifact probe、known-format lift、validation、policy library、merge 等辅助能力
4. [`agents/`](./agents/)：每个 agent 的决策逻辑、deterministic 规则和 LLM refinement
5. [`graph/`](./graph/)：阶段分组、节点封装、并行调度与最终运行时编排
6. [`compatibility/`](./compatibility/)：旧接口兼容层

这个分层的约束是：

1. 根层不再承载主业务逻辑
2. `benchmark.py` 不反向侵入真实运行时
3. agent 逻辑不靠历史超级文件中转
4. graph 负责编排，agents 负责能力，tools 负责复用 helper，schemas 负责数据结构

## 语义路由与跨语言约束

`Phase 11` 之后，runtime 对“怎么判定任务语义、证据制度、summary row 语义、review policy 和校准 profile”的要求又收紧了一层：

1. 不再允许用 prompt / input / label 上的裸字符串特判去直接决定 `task / regime / policy / score`
2. 这类判定默认先读结构化 `metadata`，再走语义分类器，失败时保守降级到 `unknown / generic / needs more evidence`
3. 仍允许保留 deterministic 逻辑的地方只限：
   - schema / field existence
   - JSON / XML / PlantUML / free-text 等格式解析
   - 显式 CLI 参数和用户结构化配置
4. `input / pred / ref / prompt / label` 不再假设同语种；当前主路径默认支持：
   - 中文、英文与混合文本
   - CJK 标识符状态/事件名
   - 不同语言 prompt 与结构化 metadata 混用

当前相关实现主要分布在：

1. [`semantic_router.py`](./semantic_router.py)：语义分类与 deterministic semantic fallback
2. [`agents/contract_router.py`](./agents/contract_router.py)：review contract 语义路由
3. [`agents/evidence_regime_estimator.py`](./agents/evidence_regime_estimator.py)：review surface / regime 语义判定
4. [`tools/policy_library.py`](./tools/policy_library.py)：summary row、target、diagram family 与 policy packet 语义归类
5. [`utils.py`](./utils.py)：Unicode 规范化、跨语言 token/term 归一化

## Agent 架构与流程

当前真实编排入口是 [`graph/runtime.py`](./graph/runtime.py) 的 `run_expert_review_workflow()`。

### 阶段总览

运行时按三段组织：

1. `preparation`
2. `analysis`
3. `finalization`

这三段由 [`graph/edges.py`](./graph/edges.py) 和 [`graph/subgraphs.py`](./graph/subgraphs.py) 固定。

### Stage 1: Preparation

该阶段先建立“怎么评”和“拿什么评”：

1. `Contract Router`
   - 只读 `prompt`
   - 解析任务契约、重点维度、严格度和注意事项
2. `Input Analyst`
   - 只读 `input_text`
   - 提取需求项、约束、可追踪证据
3. `Prediction Extractor`
   - 只读 `pred_output`
   - 将预测模型提升为 prediction dossier
4. `Reference Extractor`
   - 只读 `ref_output`
   - 将参考模型提升为 reference dossier
5. `Evidence Regime Estimator`
   - 基于 prompt / input / pred / ref 判断当前属于 `record_level`、`summary_level`、`protocol_only` 或其他 regime
6. `Review Policy Builder`
   - 组合 contract、regime、dossier，生成本轮 policy packet、维度定义与权重

这里的关键点是先把“证据制度”和“评分语义”定下来，再进入后续分析，而不是一上来就拿一个通用 rubric 生打。

### Stage 2: Analysis

该阶段并行完成三类主体分析：

1. `Traceability Agent`
   - 检查需求到预测元素的覆盖、缺失与支撑关系
2. `Equivalence and Difference Agent`
   - 在有参考模型时比较 prediction / reference 的语义等价、结构差异、harmful extras 和缺失项
3. `Pragmatic Quality Agent`
   - 检查清晰度、建模比例、噪声、可读性、命名与不必要复杂度

这里不是简单串行，而是 fan-out 并行分析，再在后面 fan-in 汇总。

### Stage 3: Finalization

该阶段负责 restraint、冲突裁决和输出合成：

1. `Missing-Evidence Critic`
   - 给 evidence discipline 上保险，抑制没有证据支撑的过度指控
2. `Disagreement Arbiter`
   - 在有参考模型时协调 traceability 与 equivalence 的潜在冲突
3. `Score Composer`
   - 组合六个正式维度的结果并得到整体分数与 issue 集
4. `Final Synthesizer`
   - 生成最终 `ExpertReviewResult`，补齐 overall reason、notes、evidence summary 和 confidence

当前正式维度为：

1. `notation_syntax`
2. `semantic_completeness`
3. `behavioral_consistency`
4. `requirement_traceability`
5. `pragmatic_clarity`
6. `evidence_discipline`

### Context Trimming 与并行方式

当前 runtime 不是把所有原始材料塞给每个 agent。它会显式记录每个 agent 的 `context_keys` 和 fan-out / fan-in 日志，控制：

1. 每个 agent 只看它需要的上下文
2. preparation 和 analysis 中可以并行的节点会并行执行
3. 最后统一在 finalization 阶段做收束

这也是 `Phase 5` 之后“多智能体 graph 主路径化”的实质，而不是只有几个函数改了名字。

## 执行方式

### Python API

最稳定的外部入口是：

1. `review_artifacts()`
2. `review_model()`
3. `ExpertReviewAgent().review()`

示例：

```python
from expert_review import review_artifacts

result = review_artifacts(
    prompt="Review the predicted state machine and focus on requirement coverage, behavioral consistency, and unsupported extras.",
    input_text=(
        "R1: login moves the system from Idle to Ready.\n"
        "R2: start moves the system from Ready to Printing.\n"
        "R3: paper jam suspends printing and allows resume."
    ),
    pred_output='{"machine_name":"Printer","states":[{"name":"Idle"},{"name":"Ready"},{"name":"Printing"},{"name":"Suspended"},{"name":"Maintenance"}],"transitions":[{"source":"Idle","target":"Ready","event":"login","guard":"","action":""},{"source":"Ready","target":"Printing","event":"start","guard":"","action":""},{"source":"Printing","target":"Suspended","event":"paperJam","guard":"","action":""},{"source":"Suspended","target":"Printing","event":"resume","guard":"","action":""},{"source":"Ready","target":"Maintenance","event":"selfCheck","guard":"","action":""}]}',
    ref_output='{"machine_name":"Printer","states":[{"name":"Idle"},{"name":"Ready"},{"name":"Printing"},{"name":"Suspended"}],"transitions":[{"source":"Idle","target":"Ready","event":"login","guard":"","action":""},{"source":"Ready","target":"Printing","event":"start","guard":"","action":""},{"source":"Printing","target":"Suspended","event":"paperJam","guard":"","action":""},{"source":"Suspended","target":"Printing","event":"resume","guard":"","action":""}]}',
)

print(result.overall_score)
print(result.overall_reason_text)
```

### CLI

[`__main__.py`](./__main__.py) 支持直接从命令行调用：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/reproduction \
python -m expert_review \
  --prompt "帮我评审这个状态机，重点看需求覆盖、行为一致性和无依据额外结构。" \
  --input "R1: 登录后进入 Ready。R2: start 触发 Printing。R3: jam 会进入 Suspended 并允许 resume。" \
  --pred-output '{"machine_name":"Printer","states":[{"name":"Idle"},{"name":"Ready"},{"name":"Printing"},{"name":"Suspended"},{"name":"Maintenance"}],"transitions":[{"source":"Idle","target":"Ready","event":"login","guard":"","action":""},{"source":"Ready","target":"Printing","event":"start","guard":"","action":""},{"source":"Printing","target":"Suspended","event":"paperJam","guard":"","action":""},{"source":"Suspended","target":"Printing","event":"resume","guard":"","action":""},{"source":"Ready","target":"Maintenance","event":"selfCheck","guard":"","action":""}]}' \
  --ref-output '{"machine_name":"Printer","states":[{"name":"Idle"},{"name":"Ready"},{"name":"Printing"},{"name":"Suspended"}],"transitions":[{"source":"Idle","target":"Ready","event":"login","guard":"","action":""},{"source":"Ready","target":"Printing","event":"start","guard":"","action":""},{"source":"Printing","target":"Suspended","event":"paperJam","guard":"","action":""},{"source":"Suspended","target":"Printing","event":"resume","guard":"","action":""}]}'
```

输出是 `ExpertReviewResult` 的 JSON。

### Deterministic Smoke

如果要确认 fallback 主路径是否正常，直接清空 provider key 后跑 CLI 即可：

```bash
AIROUTER_API_KEY= \
FINDCG_API_KEY= \
MIAOCG_API_KEY= \
PYTHONPATH=project_1_llm_state_machine_modeling/reproduction \
python -m expert_review \
  --prompt "Review this model." \
  --input "R1: login moves the system from Idle to Ready." \
  --pred-output '{"machine_name":"Demo","states":[{"name":"Idle"},{"name":"Ready"}],"transitions":[{"source":"Idle","target":"Ready","event":"login","guard":"","action":""}]}'
```

### Benchmark Replay

离线对齐评测入口在 [`benchmark.py`](./benchmark.py)。常用调用方式如下：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/reproduction python -m expert_review.benchmark --scope slice --llm-mode off
PYTHONPATH=project_1_llm_state_machine_modeling/reproduction python -m expert_review.benchmark --scope full --llm-mode off
PYTHONPATH=project_1_llm_state_machine_modeling/reproduction python -m expert_review.benchmark --scope split --split-name validation --llm-mode off
PYTHONPATH=project_1_llm_state_machine_modeling/reproduction \
python -m expert_review.benchmark \
  --scope phase7 \
  --llm-mode off \
  --rerun-count 0 \
  --output-markdown /tmp/expert_review_phase7_bundle.md \
  --output-json /tmp/expert_review_phase7_bundle.json
```

`benchmark.py` 的职责是：

1. 回放 double-green benchmark
2. 同时导出 `slice / full available / split / phase7 bundle` 四类评测口径
3. 计算 `HAI / RAS / SAS / PDS / normalized_mae / issue_f1 / ece` 以及 split / LOFO / error map
4. 暴露 coverage gaps、`component_level_review` schema 和后续 phase 要用的误差地图
5. 作为 phase 收尾和自我迭代的外环评测工具

它不参与 `review_artifacts()` 的线上主链路。

### Batch Screening

`Phase 10` 之后，离线批量筛选入口同时固定到 [`batch.py`](./batch.py)。

最小输入协议如下：

```json
[
  {
    "item_id": "demo:1",
    "prompt": "Review this model.",
    "input_text": "R1: login moves the system from Idle to Ready.",
    "pred_output": "{\"machine_name\":\"Demo\",\"states\":[{\"name\":\"Idle\"},{\"name\":\"Ready\"}],\"transitions\":[{\"source\":\"Idle\",\"target\":\"Ready\",\"event\":\"login\",\"guard\":\"\",\"action\":\"\"}]}",
    "ref_output": null,
    "metadata": {"family": "demo"}
  }
]
```

典型调用方式如下：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/reproduction \
python -m expert_review.batch \
  --input /tmp/expert_review_batch.json \
  --llm-mode off \
  --rerun-count 4 \
  --output-json /tmp/expert_review_batch_run.json \
  --output-jsonl /tmp/expert_review_batch_rows.jsonl \
  --output-csv /tmp/expert_review_batch_rows.csv
```

当前 batch surface 提供：

1. `direct_pass / manual_review / high_risk_reject` 三桶 triage
2. `overall_score / confidence / evidence_discipline / unsupported_issue_count` 驱动的默认阈值策略
3. `json / jsonl / csv` 三种导出
4. `latency_p50 / latency_p95 / latency_max / retry_total / rerun_score_std / triage_flip_rate` 运行统计
5. deterministic 零成本口径和后续 `llm_mode='auto'` 的同构执行入口

## 当前状态

### Phase 10 结论

当前 `Phase 10` 已完成 batch screening 输入协议、triage 阈值、导出结构与 record-level 最后一轮门槛收口，并且已经确认：

1. `Milestone A` 已正式达成，当前 reviewer 可被表述为“可用于整体筛选”
2. 本轮提分主要落在 deterministic `record-level + batch surface`，`summary-level` 与 `protocol` 主口径没有被打坏
3. `unsupported_claim_rate`、`ece`、`summary_only_element_claim_rate` 与 `rerun_score_std` 同时受控，说明不是靠放松证据纪律或制造随机漂移换分
4. 当前系统仍不能宣称“可替代专家最终裁决”或“已在论文中充分证明 agent-based reviewer surrogate 成立”

当前 `Phase 10` 的 deterministic `full available benchmark` 收口快照为：

| 指标 | 当前值 |
|---|---:|
| `HAI` | `85.99` |
| `RAS` | `85.21` |
| `SAS` | `81.51` |
| `PDS` | `93.75` |
| `record normalized_mae` | `0.1228` |
| `summary normalized_mae` | `0.1044` |
| `record spearman_rho` | `0.8366` |
| `record pairwise_order_accuracy` | `0.7695` |
| `summary spearman_rho` | `0.7319` |
| `summary pairwise_order_accuracy` | `0.7286` |
| `issue_f1` | `0.9226` |
| `unsupported_claim_rate` | `0.0703` |
| `ece` | `0.1353` |
| `summary_only_element_claim_rate` | `0.0000` |
| `protocol_only_overclaim_rate` | `0.0000` |
| `rerun_score_std` | `0.0000` |

当前 benchmark coverage 也已经被明确写实：

1. 主评测 `record / summary / protocol` 分别是 `192 / 84 / 4` 行
2. deferred `component_level_review` 是 `512` 行、`16` 个 family、`8` 个 case
3. `record-level` 仍主要来自 `llms_emp`
4. `summary-level` 仍主要来自 `ttool-ai`
5. `protocol-only` 仍只有 `4` 个 paper family，必须保守解释泛化性

### Phase 11 入口

`Milestone A` 已完成，后续继续推进已经进入 `Phase 11+`，重点转为：

1. `Phase 11` 需要把 `512` 条 `component_level_review` 接入主评测，建立 `CRAS` 与逐组件对齐证据
2. `Phase 12` 需要补 judgement / reason / evidence reliability，避免只有分数对齐而缺少解释层证据
3. `Phase 13` 需要把验收从单次 full available benchmark 提升到 `validation + lockbox + LOFO`
4. `Phase 14-15` 需要补 deterministic / LLM-enabled 边界、成本与 ablation，形成论文级证据包
5. 当前 batch 结果虽然可用于整体筛选，但 `manual_review` 仍占大头，这和“高精度预筛器”定位一致，不应过度宣称自动化程度

相关结论见：

1. [GUIDE.md](./GUIDE.md)
2. [designs/README.md](./designs/README.md)
3. [designs/v1/README.md](./designs/v1/README.md)
4. [designs/v1/TODO.md](./designs/v1/TODO.md)
5. [designs/v1/V1_ALIGNMENT_REPORT.md](./designs/v1/V1_ALIGNMENT_REPORT.md)

## 推荐阅读顺序

1. 先读 [GUIDE.md](./GUIDE.md)
2. 再读本文件，理解目录结构与真实运行时
3. 再读 [designs/README.md](./designs/README.md)
4. 如果关注当前冻结判断与提分入口，读 [designs/v1/V1_ALIGNMENT_REPORT.md](./designs/v1/V1_ALIGNMENT_REPORT.md)
5. 如果要继续推进 phase，读 [designs/v1/TODO.md](./designs/v1/TODO.md)
