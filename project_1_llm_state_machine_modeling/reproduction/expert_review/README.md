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
| [test_review.py](./test_review.py) | 模块级最小回归测试 |
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

离线对齐评测入口在 [`benchmark.py`](./benchmark.py)。典型调用方式：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/reproduction \
python - <<'PY'
from expert_review.benchmark import run_benchmark_iteration

report = run_benchmark_iteration(llm_mode="off")
print(report["HAI"])
print(report["record_metrics"]["RAS"])
print(report["summary_metrics"]["SAS"])
print(report["protocol_metrics"]["PDS"])
PY
```

`benchmark.py` 的职责是：

1. 回放 double-green benchmark
2. 计算 `HAI / RAS / SAS / PDS / normalized_mae / issue_f1 / ece`
3. 作为 phase 收尾和自我迭代的外环评测工具

它不参与 `review_artifacts()` 的线上主链路。

## 当前状态

### Phase 6 结论

当前 `Phase 6` 已完成“冻结前核验与代码树收口”，并且已经确认：

1. 正式运行时主干稳定
2. 兼容边界已收敛
3. 根层长名字文件已完成整理
4. benchmark 指标与 `Phase 5 Round 0` 一致，没有观察到明显回退

当前 `Phase 6` 收口快照为：

| 指标 | 当前值 |
|---|---:|
| `HAI` | `78.68` |
| `RAS` | `74.87` |
| `SAS` | `75.02` |
| `PDS` | `93.75` |
| `normalized_mae` | `0.1751` |
| `issue_f1` | `0.8202` |
| `unsupported_claim_rate` | `0.1778` |
| `ece` | `0.5302` |

这说明 `Phase 6` 的收口没有带来明显退化，但也没有把当前版本推到可冻结状态。

### Phase 7 入口

后续继续提分已经明确进入 `Phase 7`，重点不再是清理目录，而是继续处理：

1. `record-level` partial-heavy 样例仍偏高分
2. `summary-level` 高分样例仍偏保守
3. `unsupported_claim_rate` 仍高
4. `ece` 仍高
5. `protocol-only` taxonomy 语言仍不够像真人 reviewer

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
