# 专家评审对齐报告

## 1. 范围

本文件记录了独立 [`expert_review`](../../README.md) agent 与 TTool-AI 基线数据集中真实人类专家评分之间的最终对齐实验。

对齐目标：

- 保持外部接口不变：`prompt`、`input`、`pred-output`、可选的 `ref-output`
- 保持评审流程以 LLM 为先
- 不在 agent 内部添加隐藏的、基于特定 baseline 的分派逻辑
- 使用已发布的人类评分，来源为 [`results.ods`](../../../data/raw/ttool-ai/results.ods)
- 在 [`alignment_reviews.parquet`](../../../results/ttool/expert_alignment/paper_rubric_v5/alignment_reviews.parquet) 和 [`alignment_summary.json`](../../../results/ttool/expert_alignment/paper_rubric_v5/alignment_summary.json) 中产出最终结构化结果

最终选定的 prompt 变体：

- `paper_rubric_v5`

最终版本中保留的 agent 侧关键改动：

- 针对 `airouter` JSON 响应的流式回退机制
- 使用紧凑的预计算上下文，而不是庞大的原始转储
- 从解析后的 artifact 载荷中精确提取状态/块名称
- 面向行为模型的通用语义锚定校准
- 面向类架构模型的通用架构锚定校准，以及 LLM/启发式稳定性混合
- 在 LLM JSON 格式错误或不可用时重试

## 2. 复现命令

完整对齐运行：

```bash
venv/bin/python project_1_llm_state_machine_modeling/reproduction/align_ttool_expert_review.py \
  --prompt-variant paper_rubric_v5
```

主要输出：

- 汇总：[`alignment_summary.json`](../../../results/ttool/expert_alignment/paper_rubric_v5/alignment_summary.json)
- 逐条表：[`alignment_reviews.parquet`](../../../results/ttool/expert_alignment/paper_rubric_v5/alignment_reviews.parquet)
- 每个样本缓存的请求/结果载荷：[`cache/`](../../../results/ttool/expert_alignment/paper_rubric_v5/cache/)

使用某个样本精确保存的请求进行复现回放的代表性命令：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/reproduction venv/bin/python - <<'PY'
import json
from pathlib import Path
from expert_review import review_artifacts

payload = json.loads(
    Path(
        "project_1_llm_state_machine_modeling/reproduction/results/ttool/"
        "expert_alignment/paper_rubric_v5/cache/automated_braking__System1__bd.json"
    ).read_text(encoding="utf-8")
)
request = payload["request"]
result = review_artifacts(
    prompt=request["prompt"],
    input_text=request["input_text"],
    pred_output=request["pred_output"],
    ref_output=request["ref_output"],
)
print({
    "overall_score_100": round(result.overall_score * 100, 4),
    "dimension_scores": {item.dimension_name: item.score for item in result.dimension_results},
    "notes": result.notes[:4],
})
PY
```

针对一个低分状态机案例的另一条回放命令：

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/reproduction venv/bin/python - <<'PY'
import json
from pathlib import Path
from expert_review import review_artifacts

payload = json.loads(
    Path(
        "project_1_llm_state_machine_modeling/reproduction/results/ttool/"
        "expert_alignment/paper_rubric_v5/cache/platooning__Platoon5__smd.json"
    ).read_text(encoding="utf-8")
)
request = payload["request"]
result = review_artifacts(
    prompt=request["prompt"],
    input_text=request["input_text"],
    pred_output=request["pred_output"],
    ref_output=request["ref_output"],
)
print({
    "overall_score_100": round(result.overall_score * 100, 4),
    "dimension_scores": {item.dimension_name: item.score for item in result.dimension_results},
    "notes": result.notes[:4],
})
PY
```

## 3. 最终指标

来自 [`alignment_summary.json`](../../../results/ttool/expert_alignment/paper_rubric_v5/alignment_summary.json)：

| 范围 | 评审数 | 人类均值 | 预测均值 | MAE | RMSE | Pearson | Spearman | 5分内占比 | 10分内占比 | 15分内占比 |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 总体 | 30 | 72.10 | 69.04 | 11.98 | 15.22 | 0.662 | 0.594 | 0.333 | 0.567 | 0.700 |
| bd | 15 | 81.20 | 78.27 | 13.04 | 16.21 | 0.523 | 0.287 | 0.333 | 0.400 | 0.600 |
| smd | 15 | 63.00 | 59.81 | 10.92 | 14.16 | 0.631 | 0.560 | 0.267 | 0.733 | 0.800 |

按案例计算的平均绝对误差：

| 案例ID | 平均绝对误差 |
|:--|--:|
| automated_braking | 9.56 |
| platooning | 12.49 |
| space_based_system | 13.89 |

解读：

- `automated_braking` 整体上是对齐效果最好的案例族。
- `smd` 现在明显优于更早的迭代，并且最终的 `MAE` 低于 `bd`。
- 目前最难的剩余案例族是 `space_based_system`，尤其是其中一些被高估的块图和一些被低估的高质量状态机。

## 4. 完整最终结果表

来自 [`alignment_reviews.parquet`](../../../results/ttool/expert_alignment/paper_rubric_v5/alignment_reviews.parquet)：

| 案例ID            | 变体名         | artifact 类型  |   人类得分（百分制） |   预测得分（百分制） |   绝对误差 |
|:-------------------|:---------------|:----------------|---------------------:|---------------------:|-----------:|
| automated_braking  | System1        | bd              |                   85 |               87.5077 |     2.5077 |
| automated_braking  | System1        | smd             |                   65 |               56      |     9      |
| automated_braking  | System2        | bd              |                  100 |               83.2103 |    16.7897 |
| automated_braking  | System2        | smd             |                   45 |               73.8    |    28.8    |
| automated_braking  | System3        | bd              |                   95 |               86.0466 |     8.9534 |
| automated_braking  | System3        | smd             |                   30 |               38.2    |     8.2    |
| automated_braking  | System4        | bd              |                   45 |               41.6974 |     3.3026 |
| automated_braking  | System4        | smd             |                   30 |               39.6    |     9.6    |
| automated_braking  | System5        | bd              |                   90 |               90.4466 |     0.4466 |
| automated_braking  | System5        | smd             |                   70 |               62      |     8      |
| platooning         | Platoon1       | bd              |                  100 |               89.9    |    10.1    |
| platooning         | Platoon1       | smd             |                   85 |               70      |    15      |
| platooning         | Platoon2       | bd              |                   75 |               62      |    13      |
| platooning         | Platoon2       | smd             |                   75 |               72.2    |     2.8    |
| platooning         | Platoon3       | bd              |                   75 |               61      |    14      |
| platooning         | Platoon3       | smd             |                   65 |               56      |     9      |
| platooning         | Platoon4       | bd              |                   90 |               71.6211 |    18.3789 |
| platooning         | Platoon4       | smd             |                   70 |               73.6    |     3.6    |
| platooning         | Platoon5       | bd              |                   75 |               43      |    32      |
| platooning         | Platoon5       | smd             |                   40 |               47      |     7      |
| space_based_system | System1        | bd              |                   88 |               90.125  |     2.125  |
| space_based_system | System1        | smd             |                   70 |               70.8    |     0.8    |
| space_based_system | System2        | bd              |                   60 |               89.35   |    29.35   |
| space_based_system | System2        | smd             |                   75 |               57      |    18      |
| space_based_system | System3        | bd              |                   70 |               89.975  |    19.975  |
| space_based_system | System3        | smd             |                   65 |               56      |     9      |
| space_based_system | System4        | bd              |                   75 |               96.4    |    21.4    |
| space_based_system | System4        | smd             |                   70 |               68      |     2      |
| space_based_system | System5        | bd              |                   95 |               91.75   |     3.25   |
| space_based_system | System5        | smd             |                   90 |               57      |    33      |

## 5. 代表性示例

### 示例 A：接近人类评分的高质量块图

缓存样本：

- [`automated_braking__System1__bd.json`](../../../results/ttool/expert_alignment/paper_rubric_v5/cache/automated_braking__System1__bd.json)

人类与 agent：

- 人类专家：`85`
- Agent：`87.5077`

实际 agent 输出摘要：

```json
{
  "overall_score_100": 87.5077,
  "dimension_scores": {
    "notation_syntax": 0.75,
    "semantic_completeness": 0.65,
    "behavioral_consistency": 0.7,
    "requirement_traceability": 0.68,
    "pragmatic_clarity": 0.65
  },
  "notes": [
    "没有可用的参考输出，因此评分直接依据输入的架构和需求进行。",
    "评估优先考虑架构层面的充分性，但若要获得更高分，显式的安全、安全防护和时序需求仍然必须可追溯。",
    "由于模型包含许多由需求支撑的块名称和显式交互，因此应用了通用架构锚定加成。",
    "应用了架构稳定性混合：llm_weight=0.25，heuristic_weight=0.75。"
  ]
}
```

这为何是对齐的：

- agent 对核心 ECU → CSC → communication/broadcast 链条给予了较多加分。
- 它仍然因为缺少安全/隐私/时序架构而扣分，这与人类评审给出的非满分结果一致，而不是给出接近 100 的评分。

### 示例 B：接近人类评分的薄弱块图

缓存样本：

- [`automated_braking__System4__bd.json`](../../../results/ttool/expert_alignment/paper_rubric_v5/cache/automated_braking__System4__bd.json)

人类与 agent：

- 人类专家：`45`
- Agent：`41.6974`

实际 agent 输出摘要：

```json
{
  "overall_score_100": 41.6974,
  "dimension_scores": {
    "notation_syntax": 0.8,
    "semantic_completeness": 0.16,
    "behavioral_consistency": 0.12,
    "requirement_traceability": 0.27,
    "pragmatic_clarity": 0.32
  },
  "notes": [
    "没有可用的参考输出，因此评分直接基于输入描述和所请求的架构级评审任务。",
    "由于存在若干核心子系统，给予了高层架构层面的分数，但由于主要的交互链路在模型中实际上并未连通，因此进行了大幅扣分。",
    "由于模型包含许多块但几乎没有显式交互，因此应用了通用架构惩罚。",
    "应用了架构稳定性混合：llm_weight=0.75，heuristic_weight=0.25。"
  ]
}
```

这为何是对齐的：

- agent 并未因为只是存在若干块而过度扣分，但它对缺乏交互进行了强烈扣分。
- 这与该案例的人类评分模式非常接近。

### 示例 C：有一定剩余差距的优质状态机集合

缓存样本：

- [`platooning__Platoon1__smd.json`](../../../results/ttool/expert_alignment/paper_rubric_v5/cache/platooning__Platoon1__smd.json)

人类与 agent：

- 人类专家：`85`
- Agent：`70`

实际 agent 输出摘要：

```json
{
  "overall_score_100": 70.0,
  "dimension_scores": {
    "notation_syntax": 0.78,
    "semantic_completeness": 0.74,
    "behavioral_consistency": 0.68,
    "requirement_traceability": 0.73,
    "pragmatic_clarity": 0.57
  },
  "notes": [
    "没有可用的参考模型，因此评分仅针对输入需求进行。",
    "从表述来看，高级车队分裂功能似乎是可选的；它没有被视为导致缺失行为扣分的主要因素。",
    "由于模型包含许多领域特定的状态名称，且占位状态相对较少，因此应用了通用语义锚定加成。"
  ]
}
```

这为何只是部分对齐：

- agent 正确识别出这显然是一个强于平均水平的行为模型。
- 但它仍低于人类评分，因为它持续针对因果细节建模不足以及较弱的守卫/时序逻辑进行扣分。

### 示例 D：在最终修复后被拉低分数的低质量状态机集合

缓存样本：

- [`platooning__Platoon5__smd.json`](../../../results/ttool/expert_alignment/paper_rubric_v5/cache/platooning__Platoon5__smd.json)

人类与 agent：

- 人类专家：`40`
- Agent：`47`

实际 agent 输出摘要：

```json
{
  "overall_score_100": 47.0,
  "dimension_scores": {
    "notation_syntax": 0.79,
    "semantic_completeness": 0.41,
    "behavioral_consistency": 0.36,
    "requirement_traceability": 0.48,
    "pragmatic_clarity": 0.63
  },
  "notes": [
    "没有可用的参考模型，因此评分是基于文本需求进行的独立专家评审。",
    "时序细节未被视为语法问题，但它们的缺失仍然降低了完整性和可追溯性，因为这里明确要求了这些行为。"
  ]
}
```

这为何比早期迭代有所改进：

- 早期版本高估了这个案例，因为它们被受污染的伪状态提取误导了。
- 切换到精确的已解析状态名提取后，agent 将其视为一个浅层行为模型，而不是一个丰富的行为模型。

## 6. 哪些做法有效

- `airouter` 流式回退机制消除了空响应失败，并让以 LLM 为先的评审足够稳定，可反复运行。
- 紧凑的评审上下文避免了早先那种超大 prompt 的失败模式。
- 精确的状态/块名称提取修复了由通用文本抓取造成的错误语义加成。
- 通用行为模型校准提升了 `smd` 高分与低分之间的区分度。
- 通用架构校准加上 LLM/启发式混合，显著改善了 `bd` 的对齐效果，尤其是在明显较好和明显较弱的块图上。

## 7. 剩余差距

剩余误差最大的案例：

- `space_based_system / System5 / smd`：人类 `90`，agent `57`
- `space_based_system / System2 / bd`：人类 `60`，agent `89.35`
- `space_based_system / System4 / bd`：人类 `75`，agent `96.4`
- `platooning / Platoon5 / bd`：人类 `75`，agent `43`
- `automated_braking / System2 / smd`：人类 `45`，agent `73.8`

观察到的失效模式：

- 某些 `space_based_system` 块图即使在人类评分者更为保守的情况下，仍然会因为架构覆盖度而被过度奖励。
- 某些高质量的 `space_based_system` 状态机集合仍被低估，因为 agent 持续把缺失的细节行为证据看得比人类专家更重要。
- `automated_braking / System2 / smd` 仍然是一个持续存在的假阳性。

实际结论：

- 当前版本不再是一个会天真地普遍给出高分的评审器。
- 对于 `automated_braking`，它已经实现了较强对齐。
- 对于 `platooning`，它的对齐程度是合理的，但在行为侧仍残留一些保守性。
- 对于 `space_based_system`，它已经可用，但对齐程度还没有另外两个案例族那么紧。

## 8. 最终文件位置

- 最终汇总：[`alignment_summary.json`](../../../results/ttool/expert_alignment/paper_rubric_v5/alignment_summary.json)
- 最终逐条表：[`alignment_reviews.parquet`](../../../results/ttool/expert_alignment/paper_rubric_v5/alignment_reviews.parquet)
- 最终逐样本缓存：[`cache/`](../../../results/ttool/expert_alignment/paper_rubric_v5/cache/)
- 对齐运行器：[`align_ttool_expert_review.py`](../../../align_ttool_expert_review.py)
- 独立 agent：[`expert_review_agent.py`](../../expert_review_agent.py)
