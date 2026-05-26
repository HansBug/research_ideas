# Path 1 — 硬刚路线（Hard Comparison）接管指引

> **本文件目标**：任何新 Claude / codex session 进入 `dev/path1-hard-comparison` branch 后，按本指引可直接接管，把 Path 1 quick experiment 推进到 sprint 末。
>
> **前置阅读**：先读 [../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md)（meta-level 路线规划与决策准则），再读本文件。
>
> **版本**：v1（2026-05-26 sprint 开工前定稿）

## 1. 路线定位

Path 1 = **硬刚路线**，主张：**在公开 baseline 数据集上跑出比 baseline 论文最强 strategy（Hybrid）显著更高的 component-level F1**。

> **v3 修订说明**：原 v1/v2 把对手简化为 single-prompt 是错的。[structure_event_driven](../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/DESC.md) 论文里**最强 strategy 是 Hybrid**（先 Single-Prompt 出 Umple 草稿，再用 Structure-Driven 多步迭代细化），GPT-4o 上 macro-F1 = 0.6559 / Claude 3.5 Sonnet 单 prompt = 0.7029。Path 1 主对手应是 Hybrid 在 GPT-5.5 上的重跑结果，而非任何 single-prompt 版本。

### 1.1 paper 主卖点（如果 Path 1 被选定）

> "We propose an agent loop architecture that integrates pyfcstm's deterministic verifier feedback (parse / semantic / simulation / reachability witness) and LLM-as-judge as in-loop feedback signals. On the same T0 subset of the `structure_event_driven` benchmark where the prior **best** strategy (Hybrid SMF) achieves macro-F1 = $X$ on GPT-5.5, our method lifts the macro-F1 to $Y$. Improvements are particularly pronounced on `guards / actions / hierarchical states`, which prior work identified as the hardest components."

### 1.2 与 6 个主力 baseline 的方法学差异化

完整 6-baseline 对照表见 [discussion §4.4](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md#44-6-个主力-baseline-方法学全景v3-新增)。Path 1 sprint 阶段**只与 structure_event_driven Hybrid 对照**，其他 5 个 baseline（llms_emp / ttool-ai / IEC 61499 / Llama3 Umple / Automated Statechart Automotive）作为方向定后正式 paper 阶段的工作。

**sprint 范围声明（必须能向 reviewer 解释）**：

| 未在 sprint 复现的 baseline | 为什么 sprint 不做 | 方向定后怎么补 |
| --- | --- | --- |
| llms_emp 两阶段框架 (rule-based grammar/semantics feedback) | 输出是 PlantUML/SysML，不是 pyfcstm/Umple；需要写一套 PlantUML→pyfcstm 转换器；sprint 30h 不够 | paper §4.x 补 cross-formalism comparison（在 sources/ 上跑 llms_emp 风格 pipeline） |
| ttool-ai 自动反馈循环 (JSON/syntax check + post-hoc sim) | 输出是多 block AVATAR design 不是单 STM；task 不完全对齐 | paper §4.x discussion 段落讨论；不重跑实验，引用 paper 报告数字 |
| IEC 61499 仿真精化 (softPLC + 人类评论) | 需要 EAE / softPLC 环境部署；本质是 human-in-the-loop pipeline，与我们的 fully automated 范式不直接可比 | paper §5 discussion 段落讨论 "fully automated vs human-in-the-loop" trade-off |
| Llama3 Umple (Zero/One/RAG) | 模型代差大（Llama 3 8B vs GPT-5.5）；不公平对照 | paper §4.x 补 LLM model-comparison 附表 |
| Automated Statechart Automotive (微调) | 需要微调 LLM；Volvo 内部数据不可获取 | paper §2 related work 段落引用，不重跑 |

### 1.3 Path 1 学术 framing 三要点

1. **Comparability** 强 — 直接对照 [structure_event_driven](../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/DESC.md) 的 7 类组件 P/R/F1 协议
2. **Reproducibility** 强 — baseline 数据集公开，且本仓库已有复现代码 [baseline_structure_event.py](../reproduction/baselines/baseline_structure_event.py)
3. **Construct validity 弱点** — 数据集多是家电 / 办公领域，paper §6 limitations 中显式承认 + §5 discussion 中说明 method 在 control system 上的可迁移性预期（即使 sprint 阶段没在 sources/ 上 evaluation）

### 1.4 Path 1 lift 学术意义

`A4_ours - A0_strong` 这个 lift 反映的不是"我们比 baseline 强多少"，而是 **pyfcstm 外部 deterministic verifier feedback + ex1 judge as in-loop feedback** 相对于 **纯 prompt-based 多步 + 规则后处理** 的增量贡献。这正是 paper §1 contributions 第 1-3 条的实验证据：

1. In-loop multi-source deterministic verifier feedback
2. Fully automated no-human-in-the-loop
3. Reachability witness as structured prompt input

完整 6 条 contribution 见 [discussion §4.5](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md#45-我们的核心创新点v3-新增)。

## 2. 接管前自检

进入 `dev/path1-hard-comparison` branch 后，按以下顺序验证 sprint 状态：

```bash
# 1. 确认 branch
git branch --show-current
# 应该输出: dev/path1-hard-comparison

# 2. 确认 method/ 共同基础已 fork 自 main
ls project_1_llm_state_machine_modeling/method/ 2>/dev/null
# 应该有: agents/ feedback/ loop.py schema.py prompts/ gpt_client.py

# 3. 确认 pyfcstm 已安装
python -c "from pyfcstm.dsl import parse_with_grammar_entry; print('ok')"

# 4. 确认 LLM env 三件套已 source 到当前 shell 环境变量
# 调用前必须先：source .env（仓库根，已 gitignore）
# 代码绝不直接读取 .env 文件本身，只读 os.environ
[ -n "$LLM_ENDPOINT" ] && [ -n "$LLM_API_KEY" ] && [ -n "$LLM_MODEL" ] && echo "env ok"
# 若 ok 不出现，shell 里跑：source .env  然后重试
# proxy 是 OpenAI-compatible，所有 vendor (GPT/Claude/Qwen/DeepSeek) 统一走这一个 endpoint
# 切换 model 只改 LLM_MODEL 环境变量，不动 client 代码

# 5. 确认 baseline 复现代码可用（Path 1 特有）
test -f project_1_llm_state_machine_modeling/reproduction/baselines/baseline_structure_event.py && echo "baseline_structure_event ok"
# 注意：需要 verify 该代码支持把 LLM provider 切换到 GPT-5.5，且能跑 Hybrid strategy（4 strategy 中的最强）；详见 §5 实验脚本

# 6. 查 sprint 进度
cat project_1_llm_state_machine_modeling/method/STATUS.md 2>/dev/null || echo "no STATUS yet"
```

若 1-3、5 任一不通过，**停下来**，先确认 main 上 Phase 0-3 是否已稳定 — Path 1 branch 不应当独立做共同基础。

## 3. 数据规则（T0 硬约束）

### 3.1 T0 子集筛选

**T0 定义**：样本的自然语言输入中**不含显式时间约束**。判定规则（按优先级）：

1. 文本中是否含 `\b\d+\s*(second|seconds|minute|minutes|hour|hours|ms|millisecond)` 等时间量词 + 数字组合 → 含则非 T0
2. 文本中是否含 `after T_n`、`within T_n`、`every T_n` 等时间变量符号 → 含则非 T0
3. 文本中是否含 "timeout / time-out / delay / counting down / counts down / debounce / hysteresis" 等隐式时序词 → 含则非 T0
4. 参考状态机模型本身是否有 `Timer / Clock / Tick / Periodic` 类组件 → 含则非 T0

筛选脚本（应放在 main 上的共同基础，调用方式）：

```python
from method.data import filter_t0
t0_indices = filter_t0(
    parquet_path="reproduction/data/derived/structure_event_driven_cases.parquet",
    text_col="description",
    reference_col="reference_solution",
)
```

### 3.2 数据集选择

| 来源 | 全量 | T0 子集预期 | 用途 |
| --- | --- | --- | --- |
| structure_event_driven | 8 cases | 3-5（dishwasher / chess clock / 等显式时间样本剔除） | 主对照 |
| llms_emp stm | 38 samples | 预估 15-25（time 词频 0.76% 较低） | 补量到 5-10 条 |

实际数量在 Phase 4 开工时 verify；若 T0 子集 < 5 条，按 §6 风险表回退。

### 3.3 选样落盘

筛完后落到：

```text
reproduction/data/derived/path1_t0_subset.parquet
```

schema：

```text
columns:
- source: str  # "structure_event" | "llms_emp"
- case_id: str
- nl_input: str  # T0 后的自然语言
- reference_solution: str  # Umple/PlantUML 文本
- reference_components: dict  # {states: [...], transitions: [...], guards: [...], ...}
```

## 4. method/ 共同基础调用方式

Phase 0-3 在 main 上稳定后，Path 1 sprint 跑两个 method 标签：

### 4.1 `A0_strong` — baseline structure_event Hybrid 在 GPT-5.5 上重跑

调用现有复现代码（不在 method/ 共同基础内，在 reproduction/baselines/）：

```python
from reproduction.baselines.baseline_structure_event import run_baseline
from method.gpt_client import get_llm_client  # 共同基础，统一走仓库根 .env

result = run_baseline(
    case=row,
    strategy="hybrid",            # baseline 论文 4 种 strategy 中最强
    llm_client=get_llm_client(),  # 走 LLM_ENDPOINT + LLM_API_KEY + LLM_MODEL 三件套
)

# result 含: predicted_dsl (Umple 文本), component_predictions (7 类组件), token_usage
```

**sprint Phase 0 必须 verify**：

1. `baseline_structure_event.py` 接口能接受外部传入的 `llm_client` 对象（OpenAI-compatible），不要 hardcode provider
2. 如果原代码 hardcode 了 GPT-4o client，需要花 30min-1h 重构为接收外部 client 注入（统一走 method.gpt_client）

### 4.2 `A4_ours` — 我们的 full agent loop

调用 method/ 共同基础（与 Path 2 完全一致的接口）：

```python
from method.loop import run_agent_loop, LoopConfig
from method.schema import AgentLoopResult

result: AgentLoopResult = run_agent_loop(
    nl_input=row["nl_input"],
    config=LoopConfig(
        condition="A4",  # method.loop 内部 condition 标签，与外部 A4_ours 对应
        n_iter=3,
        feedback_sources=["parse", "semantic", "sim", "judge"],
        # llm_model 默认 None；None 时 method.gpt_client 从 env LLM_MODEL 读取
        # 想强制指定模型时再显式传入字符串
    ),
)

# result.final_dsl   : pyfcstm DSL 文本
# result.iter_traces : 每轮迭代的 (model, feedback, repair) 三元组
# result.token_usage : dict
```

### 4.2a `method/gpt_client.py` 统一 LLM client（v3 新增 — 必须实现在 Phase 0）

所有 LLM 调用（spec / model / repair / judge / NL summary / baseline Hybrid 内部）**全部走这一个 client**。

**约束**：代码**绝不**用 `python-dotenv` 或其他方式直接读 `.env` 文件；只读 `os.environ`。运行前由 shell `source .env` 把三件套加载到环境变量。

```python
# method/gpt_client.py 骨架
import os
from openai import OpenAI

def get_llm_client():
    """从环境变量读三件套（运行前必须先 source 仓库根 .env）。
    proxy 是 OpenAI-compatible gateway，模型切换不动 client，只改 LLM_MODEL."""
    return OpenAI(
        base_url=os.environ["LLM_ENDPOINT"],  # KeyError if not sourced — fail loudly
        api_key=os.environ["LLM_API_KEY"],
    )

def get_default_model() -> str:
    return os.environ["LLM_MODEL"]  # 同样 fail loudly，不允许 silent fallback
```

切换模型（GPT-5.5 → GPT-5.4 → Claude → Qwen → DeepSeek）**只需要改 .env 的 LLM_MODEL 然后重新 source .env**，代码完全不动。cross-vendor sanity 在 sprint 后是改一行 env + 重新 source 的事。

### 4.3 DSL 格式差异处理

A0_strong 输出 Umple，A4_ours 输出 pyfcstm DSL。两者在评测 §6 之前需要先做 component 抽取归一化（两个 parser 都抽出 7 类组件后再算 P/R/F1）。**这块归一化代码也是 Phase 0-3 共同基础的一部分**，在 method/eval/component_extractor.py 实现，同时支持 Umple 和 pyfcstm 抽取。

## 5. 实验脚本 `method/run_path1.py`

CLI 接口（Phase 4 开工时由 Path 1 branch 实现，本指引固定接口规范）：

```bash
# 先在 shell source 仓库根 .env 把三件套加载到环境变量
# 代码不会读 .env 文件本身，只读 os.environ
source .env

# 然后跑 run_path1（model 走 env LLM_MODEL，CLI 不需要传）
python -m method.run_path1 \
  --t0-subset reproduction/data/derived/path1_t0_subset.parquet \
  --methods A0_strong,A4_ours \
  --n-iter 3 \
  --out reproduction/results/sprint_path1/predictions.parquet \
  --resume  # 支持 checkpoint，跑到一半挂掉可继续
```

method 字段映射（在 run_path1.py 内部分发）：

- `A0_strong` → 调 `reproduction.baselines.baseline_structure_event.run_baseline(strategy="hybrid", llm_provider="gpt-5.5")`
- `A4_ours` → 调 `method.loop.run_agent_loop(condition="A4", n_iter=3, feedback_sources=["parse","semantic","sim","judge"], llm_model="gpt-5.5")`

实现要点：

1. **checkpoint**：每条样本跑完立即写 parquet 一行，不等全部跑完
2. **失败容忍**：单条样本 GPT 5xx 重试 3 次后跳过，记 `status="api_failed"`，不中止整个 batch
3. **token tracking**：每条 sample 记 input/output token，落到 summary.json
4. **DSL 格式归一化**：A0_strong 出 Umple，A4_ours 出 pyfcstm DSL，由 method/eval/component_extractor.py 统一抽 7 类组件后再进 §6 评测

## 6. 评测协议（套 structure_event_driven 7 类组件）

### 6.1 7 类组件定义

| 组件 | 抽取方式 | 比较单位 |
| --- | --- | --- |
| `states` | DSL 中所有 state 名 | 名称集合（语义等价允许） |
| `transitions` | (src, event, dst) 三元组集合 | 三元组（src/dst 名称语义等价允许） |
| `guards` | transition 上 [condition] 子句 | 表达式集合（语义等价允许） |
| `actions` | transition / state 上 /effect 子句 | 表达式集合 |
| `hierarchical_states` | composite state 名集合 | 名称集合 |
| `parallel_regions` | parallel region 名集合 | 名称集合 |
| `history_states` | history pseudo-state 集合 | 名称集合 |

### 6.2 P/R/F1 计算

对每类组件 $c$ 计算：

$$P_c = \frac{TP_c}{TP_c + FP_c}, \quad R_c = \frac{TP_c}{TP_c + FN_c}, \quad F_{1,c} = \frac{2 P_c R_c}{P_c + R_c}$$

整体 macro-F1：

$$\text{macro-}F_1 = \frac{1}{|C|} \sum_{c \in C} F_{1,c}$$

其中 $|C| = 7$。

### 6.3 名称语义等价判定

由于 single ground truth 不存在，允许 LLM-judge 做一次性 alignment：

1. 把 prediction 的状态名 list 和 reference 的状态名 list 送 GPT-5.5
2. 让它输出 alignment dict：`{pred_name: ref_name or null}`
3. 用 alignment dict 标准化 prediction 名称后再算 TP/FP/FN

这一步只跑一次，alignment 结果固化在 `predictions.parquet` 的 `name_alignment` 列里，避免重复消耗 token。

## 7. 结果落盘 schema

### 7.1 `predictions.parquet`

```text
columns:
- case_id: str
- source: str
- method: str  # "A0_strong" (= structure_event Hybrid replicated) | "A4_ours" (= our full agent loop)
- model: str  # "gpt-5.5"
- output_dsl_format: str  # "umple" (A0_strong) | "pyfcstm" (A4_ours)
- final_dsl: str
- iter_traces: list[dict]  # 每轮 (model, feedback, repair) 三元组
- token_usage: dict
- status: str  # "ok" | "api_failed" | "parse_failed_all_iters"
- name_alignment: dict  # 7 类组件名称对齐
- component_scores: dict  # {states: {P, R, F1}, transitions: ..., ...}
- macro_f1: float
```

### 7.2 `summary.json`

```json
{
  "path": "path1",
  "data": "structure_event_t0 + llms_emp_stm_t0",
  "n_samples": 7,
  "conditions": {
    "A0_strong": {"macro_f1_mean": 0.XXX, "component_f1": {...}, "token_total": 12345},
    "A4_ours":   {"macro_f1_mean": 0.XXX, "component_f1": {...}, "token_total": 67890}
  },
  "f1_lift": 0.XXX,
  "confounders": [
    {"case_id": "...", "issue": "api_failed_after_3_retries"},
    {"case_id": "...", "issue": "parse_failed_all_iters"}
  ]
}
```

## 8. `PATH1_REPORT.md` 产出要求

sprint 末 Phase 6 必须产出，**Claude 整理不下结论**。最低字段：

1. **§1 实验配置**：T0 子集组成（多少条来自 structure_event / 多少条来自 llms_emp）、GPT 模型版本、迭代轮数 $N$
2. **§2 主结果表**：`A0_strong` (structure_event Hybrid on GPT-5.5) vs `A4_ours` 的 7 类组件 P/R/F1 + macro-F1，行=组件，列=method
3. **§3 lift 分布**：每个 case 单独的 lift 柱状图数据（不必出图，给 markdown 表）
4. **§4 信号判定**：按 [discussion §4.1](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md) 的 S1/S2/S3/S4 把当前数据归类
5. **§5 confounders 列表**：API 失败 / 全轮 parse 失败 / token 截断的样本，逐一列出
6. **§6 Claude 的方向建议 + rationale**：写明依据，不强推
7. **§7 后续 paper 工作量预估**：若选 Path 1，1-2 个月内要补的工作（扩 baseline 数据集 / cross-vendor / 完整 ablation A1/A2/A3 等）

## 9. 风险与回退（Path 1 特有）

| 风险 | 触发 | 回退 |
| --- | --- | --- |
| T0 子集 $< 5$ 条 | 筛完 structure_event + llms_emp stm 仍不足 | 扩 llms_emp 全 98 条中可类比 stm 任务的 T0 样本；若仍不足，把"显式时间词"判定放宽到"无 specific time literal"（保留 timeout / delay 等抽象时间词） |
| LLM-judge 名称 alignment 不稳定 | 同 prediction 跑两次 alignment 结果不一致 | alignment prompt 用 temperature=0 + seed；不一致则记为 confounder，在 PATH1_REPORT 中明确披露 |
| baseline reference 自身有歧义 | structure_event 的 reference Umple 含未在 NL 中出现的状态 | 在 component_scores 里把这类状态标 "reference_only"，从 R 的分母去掉但保留 F1 计算的 TP（保守口径） |
| F1 lift 过低（$< 5$pp）信号不显著 | A4_ours 没比 A0_strong 好多少 | 按 [discussion §4.1](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md) S4 处理，在 PATH1_REPORT.md §6 给出"信号弱"判定，由用户综合判断 |
| `baseline_structure_event.py` LLM provider 不支持 GPT-5.5 | Phase 0 verify 时报 unknown provider | 花 30min-1h 抽象 provider 接口，加 GPT-5.5 client；fallback 用 GPT-5.4 跑 A0_strong（在 PATH1_REPORT §1 实验配置中明确披露） |
| A0_strong 和 A4_ours DSL 格式不同导致评测不公平 | Umple 抽 transitions / pyfcstm 抽 transitions 算出不同语义 | method/eval/component_extractor.py 强制走相同 7 类组件 schema；不一致样本标 confounder，PATH1_REPORT §6 披露 |

## 10. 完成度自检 checklist

sprint Phase 7 收口前用此 checklist 核验，缺哪条补哪条：

- [ ] `reproduction/data/derived/path1_t0_subset.parquet` 已落盘且 $\ge 5$ 条
- [ ] `reproduction/results/sprint_path1/predictions.parquet` 已落盘，每条样本含 A0 / A4 两行
- [ ] `reproduction/results/sprint_path1/summary.json` 含 §7.2 全字段
- [ ] `paper_v1/PATH1_REPORT.md` 含 §8 全 7 节
- [ ] `method/STATUS.md` 更新 Path 1 进度行
- [ ] GitHub PR 已开（PR 描述含 PATH1_REPORT 关键数字摘要）
- [ ] Confounder 样本数 $\le$ 总样本数 30%（超过 30% 则方法实现可疑）
