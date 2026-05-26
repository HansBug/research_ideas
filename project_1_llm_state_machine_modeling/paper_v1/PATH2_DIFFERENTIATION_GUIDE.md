# Path 2 — 差异化路线（Differentiation）接管指引

> **本文件目标**：任何新 Claude / codex session 进入 `dev/path2-differentiation` branch 后，按本指引可直接接管，把 Path 2 quick experiment 推进到 sprint 末。
>
> **前置阅读**：先读 [../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md)（meta-level 路线规划与决策准则），再读本文件。
>
> **版本**：v3（2026-05-26 sprint 开工前定稿；v2→v3 主要加 §1.2 完整 6-baseline 对比表 + §1.3 学术合法性论证 + .env source 标准）

## 1. 路线定位

Path 2 = **差异化路线**，主张：**在真实控制系统语料上跑出 intrinsic metrics 显著 lift，paper 主打 reference-free evaluation + agent loop with externally grounded in-loop feedback**。

如果这条路最终被选定为正式 paper 方向，paper 主卖点将是：

> "We tackle NL-to-STM generation for real industrial control system requirements, where canonical reference STMs do not exist. Several recent works have already integrated in-loop feedback into LLM-based STM generation: rule-based grammar/semantics checks (llms_emp), JSON/syntax/constraint checks with TTool simulator (ttool-ai), and softPLC simulation with human-in-the-loop comments (IEC 61499). **However, no existing work integrates (i) parse + semantic + simulation + reachability witness as a unified deterministic verifier signal, (ii) LLM-as-judge as in-loop semantic feedback, and (iii) speculative validation from the runtime, all in a fully automated, no-human-in-the-loop pipeline targeting industrial control system NL.** We propose (a) an agent loop architecture with the above three components and (b) a reference-free intrinsic + judge evaluation protocol. On a 20-case T0 subset of [sources/](../sources/) (real industrial control NL from 9 domains), our method lifts the 5-metric mean from $X$ to $Y$, with the largest gains on `SimRate` (+$Z$pp) and `ReachabilityRate` (+$W$pp)."

### 1.1 与 6 个主力 baseline 的方法学差异化（v3 新增）

完整 6-baseline 对照表（与 [discussion §4.4](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md#44-6-个主力-baseline-方法学全景v3-新增) 同源，paper §2 related work 直接复用）：

| # | baseline | 任务 / 输出 | LLM | 方法核心 | prompt-eng | simulation 反馈 | formal verification 反馈 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [structure_event_driven](../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/DESC.md) (2026) | NL → UML statechart (Umple) | GPT-4o / Claude 3.5 Sonnet | 4 strategy: Single-Prompt / Structure-Driven / Event-Driven / Hybrid | 高（分步提示 + Hybrid 草稿迭代） | **无** | **无**（仅规则后处理 + 参考解比对） |
| 2 | [llms_emp](../baselines/llms_emp/DESC.md) (2025) | NL → SysML STM/ACT/SD (PlantUML) | GPT-4 / 4o / Kimi / Claude 3 Haiku / Llama3.1 / DeepSeek-v3 | **两阶段框架：提示生成 + 模型检查反馈修复** | 高（五段 prompt + RAG） | **低**（论文将 sim traces 视为未来反馈，**未真正接入**） | **中-**（PlantUML / SysML grammar / semantics / consistency **rule-based check**，不是完整 formal verification） |
| 3 | [LLM-based iterative refinement (IEC 61499)](../baselines/fsm-gen-iec-61499/DESC.md) (2025) | NL + I/O spec → FSM + IEC 61499 code | 未明确 | **迭代精化 + 仿真 + 代码生成** | 中（人类评论式增量修订） | **高**（EAE / softPLC 闭环仿真，**主反馈来源**） | 低-中（人工 / 可视化检查 + 计划接 formal，**未实装**） |
| 4 | [Automated Statechart (Automotive)](../baselines/req/DESC.md) (2025) | NL 产品功能需求 → Mermaid statechart | GPT-3.5 / 4 / 4o (微调) | NLP 特征提取 + 合成数据扩充 + 领域微调 | 中（prompt-completion 对 + 数据增广） | 低（Mermaid 渲染 + 专家评审） | **无** |
| 5 | [Llama3 Umple](../baselines/umple/DESC.md) (2025) | NL → Umple state machine | Llama 3 (8B) | Zero-shot / One-shot / RAG 提示策略对比 | 高（系统消息 + RAG 选例） | **中**（Umple 可执行性 / pass@k 检查） | **低**（依赖 Umple 编译 / 语义可执行性，非独立 formal proof） |
| 6 | [ttool-ai](../baselines/ttool-ai/DESC.md) (2024) | NL 系统规范 → SysML 块图 + 内部块图 + 状态机图 (AVATAR) | GPT-4 | **知识注入 + 自动反馈循环 + TTool 工具链** | 高（约束化 JSON 输出 + 自动反馈问答） | **中**（TTool simulator 观察行为，**评分支撑，非连续仿真闭环**） | **中-**（TTool 支持 model-checker，**反馈环主要检查 JSON / 语法 / 约束**，formal capability 是工具背景非主验证机制） |

### 1.2 6 个 baseline 的方法学局限性（Path 2 学术合法性来源）

**关键观察**：6 个 baseline 中，3 个已有 in-loop feedback（#2 llms_emp / #3 IEC 61499 / #6 ttool-ai）。"我们 first to do in-loop feedback" 不成立。但是：

1. **没有任何 baseline 同时做 5 路并列反馈**：parse + semantic + sim + reachability witness + LLM judge。llms_emp 只 a+b（grammar / semantics rule-based），ttool-ai 主要 a+b（JSON / syntax），IEC 61499 主要 c（simulation 但需人介入）。
2. **没有任何 baseline 做 reachability witness in loop**：pyfcstm `topology` 子包独有。witness 不只是 boolean "状态 X 不可达"，还含从 initial state 到达失败原因的具体 transition 链。
3. **没有任何 baseline 做 speculative validation from runtime**：pyfcstm `SimulationRuntime` 在 execute transition 前 speculatively validate，其他工具链不给。
4. **没有任何 baseline 做 fully automated control system NL-to-STM**：IEC 61499 是唯一做控制系统 + simulation feedback，但需要人类评论介入；其他 baseline 不做控制系统（家电 / domain model / 通用 reactive system / 系统级 spec）。
5. **没有任何 baseline 提出 reference-free evaluation protocol**：所有 baseline 都依赖 reference STM 做 F1 评测。控制系统真实场景下不存在 canonical reference STM（同一需求可对应多个等价 STM），ref-based F1 在 construct level 就不成立。

### 1.3 我们的 6 条核心创新点（paper §1 contributions 直接复用）

1. **In-loop multi-source deterministic verifier feedback**：parse + semantic + simulation + reachability witness 4 路并列接入 generation loop，覆盖 syntax / semantics / executability / coverage 4 个正交维度。
2. **Fully automated no-human-in-the-loop**：IEC 61499 需要人类评论介入；ttool-ai 评分含教师 rubric；我们 fully automated 跑完 $N=3$ 轮。
3. **Reachability witness as structured prompt input**：pyfcstm `topology` 提供，含具体不可达原因的 transition 链作为 LLM 修复输入。所有 baseline 都不做。
4. **Speculative validation from runtime**：pyfcstm `SimulationRuntime` 直接给，PlantUML / Umple / Mermaid / TTool 都不直接给。
5. **LLM-as-judge as in-loop semantic feedback (not standalone evaluator)**：借 [project_ex1](../../project_ex1_llm_judge_for_stm/) `ExpertReviewAgent` 作为 5 维 rubric semantic feedback，与 deterministic verifier 并列。所有 baseline 不把 LLM judge 用作 in-loop feedback。
6. **Reference-free intrinsic + judge evaluation protocol**：5 个 intrinsic 指标 + judge rubric，**这一条本身可作为独立 contribution 发表**，独立于具体 agent loop architecture。

### 1.4 与 Umple 的差异化（方向定后 paper §3 用）

完整 Umple rebuttal 口径见 [2026-04-14 讨论稿](../discussions/2026-04-14-23-03-54-AI-讨论-pyfcstm作为LLM建模论文目标形式的必要性与Umple-rebuttal口径.md) §7。Path 2 sprint 阶段**不主打 DSL 本身贡献**；与 Umple 的差异由 pyfcstm `SimulationRuntime` 的 speculative validation + `topology` 的 reachability witness 自然落地，不在 §2 related work 中正面 PK。

## 2. 接管前自检

进入 `dev/path2-differentiation` branch 后，按以下顺序验证 sprint 状态：

```bash
# 1. 确认 branch
git branch --show-current
# 应该输出: dev/path2-differentiation

# 2. 确认 method/ 共同基础已 fork 自 main
ls project_1_llm_state_machine_modeling/method/ 2>/dev/null
# 应该有: agents/ feedback/ loop.py schema.py prompts/ gpt_client.py

# 3. 确认 pyfcstm 已安装
python -c "from pyfcstm.dsl import parse_with_grammar_entry; print('ok')"
python -c "from pyfcstm.simulate import SimulationRuntime; print('ok')"

# 4. 确认 ex1 ExpertReviewAgent 可 import
python -c "import sys; sys.path.insert(0, 'project_ex1_llm_judge_for_stm/src'); from expert_review.agent import ExpertReviewAgent; print('ok')"

# 5. 确认 LLM env 三件套已 source 到当前 shell 环境变量
# 调用前必须先：source .env（仓库根，已 gitignore）
# 代码绝不直接读取 .env 文件本身，只读 os.environ
[ -n "$LLM_ENDPOINT" ] && [ -n "$LLM_API_KEY" ] && [ -n "$LLM_MODEL" ] && echo "env ok"
# 若 ok 不出现，shell 里跑：source .env  然后重试
# proxy 是 OpenAI-compatible，所有 vendor (GPT/Claude/Qwen/DeepSeek) 统一走这一个 endpoint
# 切换 model 只改 LLM_MODEL 环境变量，不动 client 代码

# 6. 查 sprint 进度
cat project_1_llm_state_machine_modeling/method/STATUS.md 2>/dev/null || echo "no STATUS yet"
```

若 1-5 任一不通过，**停下来**，先确认 main 上 Phase 0-3 是否已稳定 — Path 2 branch 不应当独立做共同基础。

## 3. 数据规则（T0 硬约束 + 3 桶分层）

### 3.1 T0 子集筛选

**T0 定义**：sources/ 样本的 STM.md §2 自然语言描述中**不含显式时间约束**。判定规则同 [PATH1 §3.1](./PATH1_HARD_COMPARISON_GUIDE.md#31-t0-子集筛选)，但应用于 sources/ STM.md §2 而非 baseline parquet。

实际 sources/ 池子里已经标过 T0/T1 标签（见 [sources/SUMMARY.md](../sources/SUMMARY.md) 与历史 PR #7），优先复用已有标签；标签不齐时按上述规则补判。

### 3.2 3 桶分层选样

| 桶 | 样本数 | 定义 |
| --- | --- | --- |
| `FSM-basic` | 6 | 状态数 $\le 10$、无层次、无并发的简单 reactive 控制器 |
| `EFSM-interlock` | 8 | 含变量更新 / 守卫 / 联锁条件的 EFSM，状态数中等 |
| `HSM-layered` | 6 | 含层次状态 / composite state / 子机的层次状态机 |

总计 20 条。从 sources/ 双 A T0 子集中按桶随机抽（seed 固定，可复现）。

### 3.3 选样落盘

筛完后落到：

```text
reproduction/data/derived/path2_t0_subset.parquet
```

schema：

```text
columns:
- source_dir: str  # sources/<dir-name>/
- nl_input: str  # 取 STM.md §2 整理后的自然语言描述
- stm_md_path: str  # 引用，方便 traceback
- bucket: str  # "FSM-basic" | "EFSM-interlock" | "HSM-layered"
- aa_t0_flag: str  # 双 A T0 标签（"AA-T0"）
- meta: dict  # {domain, n_states_estimate, has_hierarchy, ...}
```

## 4. method/ 共同基础调用方式

Phase 0-3 在 main 上稳定后，Path 2 sprint 跑两个 method 标签：

### 4.1 `A0_baseline` — Path 2 的对照 baseline

Path 2 主对手不是单独某个 baseline 论文的方法（详见 §1.1-§1.3 学术合法性论证），而是**展示我们在 reference-free intrinsic 上对 A0 single-prompt 的 lift**，作为 method efficacy 的内部对照。

```python
from method.loop import run_agent_loop, LoopConfig

result = run_agent_loop(
    nl_input=row["nl_input"],
    config=LoopConfig(
        condition="A0",  # single-prompt 直出 pyfcstm DSL，不接 feedback / repair
        n_iter=1,
        feedback_sources=[],
        # llm_model 默认 None；走 env LLM_MODEL
    ),
)
```

### 4.2 `A4_ours` — 我们的 full agent loop

调用 method/ 共同基础（与 Path 1 完全一致的接口）：

```python
from method.loop import run_agent_loop, LoopConfig
from method.schema import AgentLoopResult

result: AgentLoopResult = run_agent_loop(
    nl_input=row["nl_input"],
    config=LoopConfig(
        condition="A4",
        n_iter=3,
        feedback_sources=["parse", "semantic", "sim", "judge"],
        # llm_model 默认 None；走 env LLM_MODEL
    ),
)
```

Path 2 特有：**不需要 reference**，因此 LoopConfig 里 `reference_dsl=None`，evaluation 走 intrinsic 而非 component F1。

### 4.3 `method/gpt_client.py` 统一 LLM client（v3 新增 — 必须实现在 Phase 0）

所有 LLM 调用（spec / model / repair / judge / NL summary）**全部走这一个 client**。

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

切换模型（GPT-5.5 → GPT-5.4 → Claude → Qwen → DeepSeek）**只需要改 .env 的 LLM_MODEL 然后重新 source .env**，代码完全不动。

## 5. 实验脚本 `method/run_path2.py`

CLI 接口（Phase 5 开工时由 Path 2 branch 实现，本指引固定接口规范）：

```bash
# 先在 shell source 仓库根 .env 把三件套加载到环境变量
# 代码不会读 .env 文件本身，只读 os.environ
source .env

# 然后跑 run_path2（model 走 env LLM_MODEL，CLI 不需要传）
python -m method.run_path2 \
  --t0-subset reproduction/data/derived/path2_t0_subset.parquet \
  --methods A0_baseline,A4_ours \
  --n-iter 3 \
  --out reproduction/results/sprint_path2/predictions.parquet \
  --resume
```

method 字段映射（在 run_path2.py 内部分发）：

- `A0_baseline` → `method.loop.run_agent_loop(condition="A0", n_iter=1, feedback_sources=[])`
- `A4_ours` → `method.loop.run_agent_loop(condition="A4", n_iter=3, feedback_sources=["parse","semantic","sim","judge"])`

实现要点与 Path 1 一致（checkpoint + 失败容忍 + token tracking）。

## 6. 5 个 Intrinsic 指标定义与计算

### 6.1 `ParseRate`

$$\text{ParseRate} = \frac{|\{i : \texttt{parse\_with\_grammar\_entry}(\text{dsl}_i) \text{ succeeds}\}|}{N}$$

实现：捕获 `pyfcstm.dsl.parse_with_grammar_entry` 是否抛 grammar exception。

### 6.2 `SemValidRate`

$$\text{SemValidRate} = \frac{|\{i : \texttt{parse\_dsl\_node\_to\_state\_machine}(\text{ast}_i) \text{ succeeds}\}|}{N'}$$

实现：`pyfcstm.model.parse_dsl_node_to_state_machine` 是否抛 semantic exception（含 missing state / dangling transition / undefined var）。**分母 $N'$ 只算 Parse 通过的样本**（约束式定义），不要用所有 $N$。

### 6.3 `SimRate`

$$\text{SimRate} = \frac{|\{i : \texttt{SimulationRuntime}(\text{sm}_i).\texttt{run\_until\_stable}() \text{ completes a full cycle}\}|}{N''}$$

实现：跑 `SimulationRuntime` 一个完整 cycle，确认不触发 safety limit（1000 steps / 64 stack depth）。**分母 $N''$ 只算 SemValid 通过的样本**。

### 6.4 `ReachabilityRate`

对每个样本，定义状态可达性：

$$\text{ReachRate}_i = \frac{|\{s \in S_i : s \text{ is reachable from initial state}\}|}{|S_i|}$$

样本均值：

$$\text{ReachabilityRate} = \frac{1}{|N''|} \sum_{i \in N''} \text{ReachRate}_i$$

其中 $N''$ 是 SemValid 通过的样本集合。实现：调用 `pyfcstm.topology` 子包的 reachability API。

### 6.5 `JudgeScore`

调用 [project_ex1 ExpertReviewAgent](../../project_ex1_llm_judge_for_stm/src/expert_review/agent.py)，把 pyfcstm DSL 渲染回 NL summary 后送 judge，输出 rubric 5 维总分（0-1）。

$$\text{JudgeScore} = \frac{1}{N} \sum_{i=1}^{N} \text{rubric\_total}_i$$

**所有样本都参与**（含 parse 失败的样本，judge 直接打 0），因为 judge 的 input 是"DSL 文本"而非"可执行模型"。

## 7. 结果落盘 schema

### 7.1 `predictions.parquet`

```text
columns:
- case_id: str  # source_dir 的 slug
- source_dir: str
- bucket: str
- method: str  # "A0_baseline" | "A4_ours"
- model: str  # 实际跑的 LLM_MODEL 值
- final_dsl: str
- iter_traces: list[dict]
- token_usage: dict
- status: str
- intrinsic_scores: dict  # {parse_ok, sem_ok, sim_ok, reach_rate, judge_score}
- judge_evidence: dict  # 来自 ExpertReviewAgent 的 rubric 5 维 + evidence spans
```

### 7.2 `summary.json`

```json
{
  "path": "path2",
  "data": "sources_t0_20",
  "n_samples": 20,
  "n_per_bucket": {"FSM-basic": 6, "EFSM-interlock": 8, "HSM-layered": 6},
  "methods": {
    "A0_baseline": {
      "parse_rate": 0.XX,
      "sem_valid_rate": 0.XX,
      "sim_rate": 0.XX,
      "reachability_rate": 0.XX,
      "judge_score": 0.XX,
      "mean_5_metrics": 0.XX,
      "token_total": 12345
    },
    "A4_ours": {"... 同上 ...": null}
  },
  "per_bucket_lift": {"FSM-basic": {}, "EFSM-interlock": {}, "HSM-layered": {}},
  "intrinsic_lift_mean": 0.XX,
  "confounders": []
}
```

## 8. `PATH2_REPORT.md` 产出要求

sprint 末 Phase 6 必须产出，**Claude 整理不下结论**。最低字段：

1. **§1 实验配置**：sources/ T0 子集组成（3 桶分布）、LLM_MODEL 实际值、迭代轮数 $N$
2. **§2 主结果表**：A0_baseline vs A4_ours 的 5 个 intrinsic + JudgeScore + 5-metric mean
3. **§3 lift 分布**：按 3 桶（FSM / EFSM / HSM）拆分 lift，看哪类样本最吃 method 红利
4. **§4 每个样本 detail**：20 条样本各自的 intrinsic 5 维分数，便于 spot-check 异常样本
5. **§5 信号判定**：按 [discussion §4.1](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md) 的 S1/S2/S3/S4 把当前数据归类
6. **§6 confounders 列表**：API 失败 / 全轮 parse 失败 / judge 评分异常的样本
7. **§7 Claude 的方向建议 + rationale**：写明依据，不强推
8. **§8 后续 paper 工作量预估**：若选 Path 2，1-2 个月内要补的工作（手工标 10 条 reference / 扩 sources/ 到 60 条 / intrinsic-F1 Pearson calibration / 对照 llms_emp 两阶段 / 对照 ttool-ai 自动反馈 / cross-vendor 等）

## 9. 风险与回退（Path 2 特有）

| 风险 | 触发 | 回退 |
| --- | --- | --- |
| sources/ T0 双 A 子集 $< 20$ 条 | 池子不够选样 | 把 3 桶比例调整为实际可用样本的分层；不强行凑 20 条凑出来 |
| `SimulationRuntime` 缺 abstract handler 报错 | 大量样本 SimRate=0 | 用 no-op handler，sim 只检 reachability 不验业务逻辑（在 PATH2_REPORT §6 confounder 中披露） |
| `ExpertReviewAgent` 接入失败 | adapter schema breaking | 用简化 judge（单 prompt rubric scorer 走当前 LLM_MODEL），在 PATH2_REPORT 中标记 "JudgeScore_simplified" |
| Intrinsic lift 过低（5-metric mean $< 15$pp） | A4_ours 没比 A0_baseline 好多少 | 按 [discussion §4.1](../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md) S4 处理，在 PATH2_REPORT §7 给出"信号弱"判定，由用户综合判断 |
| `ParseRate` A0_baseline 已经很高（$\ge 0.9$） | 单 prompt 就足够，lift 空间小 | 这本身是有意义的发现（"agent loop 在 parse 上不显著，但 sim/reach 上仍显著"），不必回退；在 §3 lift 分布按指标细分讨论 |
| `LLM_API_KEY` / `LLM_ENDPOINT` 未 source | 跑实验时 KeyError on `os.environ["LLM_ENDPOINT"]` | shell 跑 `source .env` 后重新执行；这是 Phase 0 自检必须 verify 的 |

## 10. 完成度自检 checklist

sprint Phase 7 收口前用此 checklist 核验：

- [ ] `reproduction/data/derived/path2_t0_subset.parquet` 已落盘且 $= 20$ 条（或按风险表回退方案的实际数）
- [ ] `reproduction/results/sprint_path2/predictions.parquet` 已落盘，每条样本含 A0_baseline / A4_ours 两行
- [ ] `reproduction/results/sprint_path2/summary.json` 含 §7.2 全字段
- [ ] `paper_v1/PATH2_REPORT.md` 含 §8 全 8 节
- [ ] `method/STATUS.md` 更新 Path 2 进度行
- [ ] GitHub PR 已开（PR 描述含 PATH2_REPORT 关键数字摘要）
- [ ] Confounder 样本数 $\le$ 总样本数 30%

## 11. Method + Contribution 详述（paper writing 直接复用素材）

> 本节集中讲清楚 Path 2 视角下我们的 method 是什么、contribution 是什么；既给 sprint 末 PATH2_REPORT.md §7 (Claude 方向建议) 提供 anchored framing，也给方向定后正式 paper §1 contributions + §3 method 提供直接可复用的写作素材。

### 11.1 Method overview — Agent loop with externally-grounded in-loop feedback

```text
NL input (sources/ T0 case from real industrial control system paper)
      |
      v
  [SpecExtractor]   走 method/gpt_client.py (LLM_MODEL from env)
      |  out: structured spec JSON (states / events / vars / transitions / hierarchy)
      v
  [Modeler]         走 method/gpt_client.py
      |  out: pyfcstm DSL text (few-shot grounded by pyfcstm sample-test/)
      v
  current_model
      |
      +----+ Feedback Sources (gated cascade) +-----+
      |    |  ParseFeedback   (pyfcstm.dsl)         |
      |    |  SemanticFeedback (pyfcstm.model)      |
      |    |  SimFeedback     (pyfcstm.simulate    |
      |    |                   + topology witness)  |
      |    |  JudgeFeedback   (ex1 ExpertReviewAgent|
      |    |                   走 method/gpt_client) |
      |    +----+-------------------------------+   |
      |         |
      v         v
  feedback_bundle (JSON schema)
      |
      v
  [Repair]          走 method/gpt_client.py
      |  out: new pyfcstm DSL (按 feedback 具体错误指针定向修复)
      v
  next_model --> 回到 Feedback Sources, iterate N=3 rounds
      |
      v
  final_model (pyfcstm DSL) --> 进入 §6 5 个 intrinsic 指标计算 + JudgeScore
```

### 11.2 Method 各组件细节

#### 11.2.1 三个 LLM agent

1. **SpecExtractor**：NL → JSON spec
   - **设计目的**：把"自由文本"压成"结构化中间表示"，避免 Modeler 直接面对控制系统 NL 描述（含传感器 / 执行器 / 联锁 / 故障恢复等多重信息）时陷入语言细节歧义
   - **prompt 全英文**（paper 投稿英文，统一）
2. **Modeler**：spec → pyfcstm DSL 文本
   - few-shot 用 pyfcstm 仓库 `sample-test/` 2-3 个例子注入语法 grounding
3. **Repair**：(current DSL, feedback_bundle) → new DSL
   - **prompt 显式约束**："按 feedback 中的具体错误指针 (line/col/state/transition) 做定向修复，不要大改"

#### 11.2.2 四个 deterministic feedback sources（externally grounded）

| Source | pyfcstm 入口 | 输出 schema 核心字段 | 在 paper §3 method 里是哪一条 contribution |
| --- | --- | --- | --- |
| Parse | `pyfcstm.dsl.parse_with_grammar_entry` | `{ok, line, col, expected_tokens, got, snippet}` | C3 |
| Semantic | `pyfcstm.model.parse_dsl_node_to_state_machine` | `{ok, missing_states, dangling_transitions, undefined_vars, type_mismatches}` | C3 |
| Sim | `pyfcstm.simulate.SimulationRuntime` + `pyfcstm.topology` | `{ok, unreachable_states, deadlocks, witness_paths, safety_limit_hits}` | **C3 + C4 + C5** (sim + witness + speculative validation 都在这一路) |
| Judge | ex1 `ExpertReviewAgent` (走 method/gpt_client) | `{rubric_scores: {coverage, fidelity, structure, executability, safety}, evidence_spans, overall}` | C6 |

#### 11.2.3 Feedback 合并策略 + 迭代控制

- **gated cascade**：Parse 过 → Semantic 过 → Sim 过 → Judge
- **迭代上限 $N=3$**：feedback_bundle 为空时提前 break，标记 `status="converged_at_iter_X"`
- **不收敛回退**：3 轮仍有 feedback 不空时，取 iter_3 final_model 进评测，标 `status="not_converged"`

### 11.3 Contribution 详述（**Path 2 视角：method 为主 + 强化 pyfcstm → 控制系统价值论证**）

> **v4 修订（含 v4.1）**：原 v3 把 "Reference-free intrinsic + judge protocol" 与 "control system NL benchmark" 作 C1/C2 主 contribution，已撤销。v4.1 进一步根据用户反馈**删除原 C5 (Four-level event scoping + DSL-native module composition)**（理由：太侧重工程，不构成 paper-level method contribution），同时**新增 §11.3.0 三段论 framing 论证**（pyfcstm feature → LLM agent loop 能力 → 控制系统价值），把"为什么 pyfcstm 特性更贴合控制系统"这一论证链显式写清楚。

#### 11.3.0 pyfcstm feature → LLM 能力 → 控制系统价值（**Path 2 核心 framing**）

本子节回答：**为什么 pyfcstm 的差异化能力特别贴合控制系统 NL-to-STM 任务？只列特性不够 — 必须论证 pyfcstm feature 在 LLM agent loop 中给模型带来的具体能力，以及这些能力如何转化为控制系统场景的实际价值**。三段论：**pyfcstm feature → LLM agent capability → control system modeling value**。

##### 11.3.0.1 控制系统 NL-to-STM 与一般 reactive system 的 4 个本质区别

控制系统建模相对一般 reactive system（家电 / 办公设备 / 教学题）有 4 个本质区别：

1. **周期执行范式**：控制系统跑在 control cycle 上（PLC 扫描周期 / 嵌入式 superloop / ROS spin 周期），每个 cycle "读传感器 → 决策 → 写执行器"；状态机停在某个 mode 时**每个 tick 都要做事**（积分、滤波、监控、watchdog）。一般 reactive system 是事件驱动 — 状态机停下来等下次事件
2. **数值密集的守卫 / 效果**：控制系统 transition guard 含大量**复合数值条件**（温度阈值 / 距离阈值 / 流量约束 / 时序去抖 / 边沿检测）；effect 含 PID 计算 / 状态变量更新 / 累积量推进
3. **硬件解耦需求**：控制系统 STM 在生成阶段**无法决定 target deployment**（PC 仿真 / RTOS / PLC / 嵌入式 MCU / ROS 节点），必须符号占位 + 后期注入；不能在 DSL 里直接写宿主语言代码
4. **强 safety invariant + fault-recovery**：任何 mode 下都要 enforce 安全不变式（"温度 ≤ 最大值"、"距离 ≥ 最小值"、"流量 ∈ 允许区间"）；任何 mode 下 Error 事件触发都必须强制切到 fault-recovery 路径，**不能依赖具体 mode 内部的逻辑接收**

这 4 个本质区别决定了"通用 LLM-based STM 工具链（Umple / PlantUML / Mermaid / SysML / TTool）在控制系统场景下不胜任"的根本原因 — 不是工具链不能"画"控制系统状态机，而是**它们不在 generation loop 中暴露上述 4 类需求所需的 grounding signal**。

##### 11.3.0.2 三段论 mapping 表（4 行覆盖 4 条 method core）

下面 4 行对应 §11.3 中 C1-C4 四条 method core 各自的 **"(a) pyfcstm 给了什么 feature → (b) 这个 feature 在 LLM agent loop 中带来什么能力 → (c) 这个能力在控制系统场景的实际价值"** 论证链：

| pyfcstm feature | LLM agent loop 能力 | 控制系统场景价值 |
| --- | --- | --- |
| `SimulationRuntime` 内 deepcopy-snapshot speculative DFS validation + structured `SimulationRuntimeDfsError` (`pyfcstm/simulate/runtime.py:_validate_transition`) | agent 在每轮 repair 前能拿到"这条 transition 触发后该 mode 的子状态机能否 reach stable boundary"的 ground-truth 反馈，及具体 dead-end 模式（init 全失败 / pseudo 不停 / guard 互锁 / exit-vs-parent 循环） | 控制系统**多模式切换**（mode A → mode B）中"切过去后 mode B 子状态机无合法 init"这类 critical bug 在 generation 阶段就被识别，无需等到 deploy 后 runtime 死机；agent 拿到诊断后能定向修复 |
| `Expr` IR + `pyfcstm/solver/` Z3 集成（`expr_to_z3` / `execute_operations` / `solve`） | agent 在每轮 repair 前能拿到"这条 transition 的 guard 是否可达 (SAT)" / "effect 后变量空间是否满足下一 invariant" 的 SMT-grade 反馈，覆盖 22 个数学函数闭包 | 控制系统**数值密集 guard** (温度阈值、流量约束、传感器去抖、PID 计算后续条件) 可被符号求解；agent 能发现"这条 guard 在变量定义域内永不为真"或"effect 后违反 safety invariant"这类静态可证伪逻辑错误 |
| `>> during before/after` aspect actions (root→leaf→root cascade) + `!` forced transition (模型层递归展开到所有 descendant) | agent 可生成**跨所有叶子的 cross-cutting 行为**（监控、日志、安全断言）无需为每个 leaf 复制；可一行声明 fault-recovery escape 自动展开到所有适用子状态 | 控制系统**周期执行范式 + 强 safety invariant**：一行 `>> during after abstract AssertSafetyInvariant` 表达"任意 mode 下每周期都要检查安全上限"；**强 fault-recovery**：一行 `! * -> ErrorHandler :: Error` 表达"任意工作 mode 下 Error 都强制切到安全状态"；Umple 都需要在每一 mode level 手抄 |
| `enter abstract` / `during abstract` / `>> during before abstract` + `@abstract_handler` decorator + `ReadOnlyExecutionContext` (frozen) | agent 可在 generation 阶段产出**hardware-effector 占位符**不需要决定 deployment target；handler 在 runtime 反射注入，frozen context 防止 handler 修改 vars；两档错误处理（raise / log）把 handler 异常落到 structured field 供 agent 消费 | 控制系统**硬件解耦需求**：同一 STM 模型在 PC 仿真 / RTOS / 嵌入式 MCU 之间无修改部署；测试时 mock handler、deploy 时实硬件 handler；STM 模型保持"语义骨架"不动 |

##### 11.3.0.3 为什么 baseline 工具链（Umple / PlantUML / Mermaid / TTool / SysML）不胜任

不是这些工具不能"画"出控制系统状态机；问题在于它们**不能给 LLM agent loop 提供上述 4 行的 grounding signal**：

1. **Umple**：guard 是 host-language 代码片段，没有 language-independent IR → 无法 SMT 求解；no speculative validation → 死锁 / 不可达 transition 只在 codegen 后运行时暴露；no DSL-native aspect AOP → 控制系统 invariant 要手抄；no DSL-level abstract action → lifecycle hook 直接写宿主语言代码
2. **PlantUML / Mermaid**：纯渲染工具，**没有 runtime / simulation / verification 能力** — 在控制系统 LLM agent loop 中只是"画状态机的工具"，无 grounding signal
3. **ttool-ai**：有 JSON syntax check 但**没有 speculative validation**、**没有 Z3 solver**、**没有 aspect AOP**；TTool simulator 是 post-hoc 评分支撑，**不在 generation loop 内**
4. **IEC 61499 iterative refinement**：有 softPLC simulation 但**需要人类评论介入**驱动迭代；不是 fully automated
5. **SysML（标准而非工具）**：标准上有 statechart 表达力，但**没有特定 reference runtime 提供 in-loop grounding**

因此，**pyfcstm 在 LLM-based control system STM synthesis 任务中的不可替代性，不是"它有什么独家 feature"，而是"它把控制系统建模所需的 4 类 grounding signal（dead-end check / SMT 可达性 / cross-cutting + forced escape / hardware decoupling）全部做在了一个 fully-automated DSL toolchain 之内"**。这是 Path 2 paper 的 method core 的真正立论基础，也是 §11.3 下面 4 条 C1-C4 contribution 的统一 framing 锚点。

---

Path 2 视角下我们的 5 条 contribution（前 4 条 method core，第 5 条 evidence + enabling tooling）。**Path 2 与 Path 1 的差异**：method core (C1-C4) 是 paper-wide 一致的 4 条；但 Path 2 强化每条 method core 与控制系统具体场景的对应关系；evidence section 用 sources/ 真实工业控制系统 NL 而非家电 benchmark。

#### C1 — In-loop deterministic feedback via speculative validation（**method core**）

> "We integrate pyfcstm's cycle-based simulation runtime — featuring per-cycle deepcopy-snapshot speculative DFS validation bounded by 1000 steps, 64 stack frames, and structural-and-value signature pruning (`pyfcstm/simulate/runtime.py:_validate_transition`) — as a deterministic in-loop feedback source. The runtime rejects transitions whose downstream init / pseudo / parent-continuation chains cannot reach a stoppable boundary, and surfaces a structured `SimulationRuntimeDfsError` whose docstring enumerates pathological STM patterns."

**控制系统场景对应**：当 LLM 生成包含**多模式切换的控制器**时（如电梯模式切换、PLC 阶段控制、自动驾驶 supervisor mode 转换），speculative validation 能识别"某条 mode transition 触发后该 mode 的子状态机没有合法 init"这类病态。这对 Umple/PlantUML/Mermaid 这些**不在 runtime 层做 dead-end 检测**的工具链是无法替代的 grounding。

#### C2 — Language-independent expression IR enables symbolic reasoning without code generation（**method core，控制系统场景的关键 enabler**）

> "The DSL ships a unified `Expr` IR (`pyfcstm/model/expr.py`) supporting arithmetic / bitwise / logical / ternary / 22-function math closure required by state-machine guards and effects. The same IR is simultaneously (a) evaluable, (b) AST-round-trippable, (c) Z3-translatable via `pyfcstm/solver/expr.py:expr_to_z3`, and (d) renderable into 9 target languages. We exploit it to provide LLM agents with **guard SMT satisfiability** (`pyfcstm/solver/solve.py:solve`) and **symbolic effect propagation** (`pyfcstm/solver/operation.py:execute_operations`) as in-loop feedback — without ever leaving the DSL toolchain."

**控制系统场景对应**：控制系统状态机大量依赖**数值变量 + 复杂守卫条件**（温度阈值、距离阈值、流量约束、传感器去抖、PID 计算）。pyfcstm DSL 内可直接表达这类逻辑：

```fcstm
def int debounce_count = 0;
def float temp = 25.0;
def float threshold = 80.0;
state Wait {
    during {
        if [pressed >= 1] { debounce_count = debounce_count + 1; }
        else              { debounce_count = 0; }
    }
}
Wait -> Triggered : if [debounce_count >= 5 && abs(temp - target) < threshold] effect { debounce_count = 0; };
```

Z3-backed solver 让 agent loop 可以问"这条 transition 的 guard 是否可达？""effect 后变量空间满足下一 invariant 吗？" — Umple 的 host-language-bound guards 做不到。

#### C3 — DSL-native aspect AOP and forced fault paths align with control-system idioms（**method core，控制系统直接对应**）

> "We design our method around two pyfcstm DSL-level primitives that Umple, PlantUML, and Mermaid lack: (i) **aspect actions** `>> during before / after` cascading from root to leaf states at every cycle (`pyfcstm/model/model.py:iter_on_during_aspect_recursively`); and (ii) **forced transitions** `!` recursively expanded to every applicable descendant substate (`pyfcstm/model/model.py:_recursive_finish_states`)."

**控制系统场景对应**：

**Aspect actions** = 控制系统"每个周期都要做的事"的第一类原语：

```fcstm
state MotorControl {
    >> during before { tick = tick + 1; }              // 每周期递增 watchdog
    >> during after abstract AssertSafetyInvariant;    // 每周期注入 safety invariant 检查
    state Running { during { command_torque = kp * (target - position); } }
    state Stopped { during { command_torque = 0; } }
}
```

`>> during after` 在任意活跃叶子状态后都自动注入（root→leaf→root cascade），对应"任意 mode 下 invariant 都必须 hold"。Umple 要在每个叶子的 `do` 内手抄一遍。

**Forced transition** `!` = 控制系统"任何模式下 Error 触发必须切到 ErrorHandler"的一行 declarative encoding：

```fcstm
state Plant {
    ! * -> ErrorHandler :: Error;   // 任何子状态下 Error 都强制 escape
    state Idle;
    state Running { state Phase1; state Phase2; [*] -> Phase1; }
    state ErrorHandler { enter abstract NotifyOperator; }
}
```

Umple 需要手写每一层 escape 或借助 nested state 隐含规则（agent report §6.3）。

#### C4 — Abstract action + read-only context decouples symbolic STM from physical effectors（**method core，控制系统硬件解耦**）

> "Combining DSL-level abstract action declarations with Python-side `@abstract_handler` decorator and `ReadOnlyExecutionContext` (`pyfcstm/simulate/decorators.py` + `context.py`) lets the LLM synthesize STMs without committing to a deployment target."

**控制系统场景对应**：控制系统 STM 在生成阶段**不应该决定 deployment target**（PC 仿真 / RTOS / PLC / 嵌入式 MCU / ROS 节点）。pyfcstm 通过 DSL 级 abstract action 占位 + 反射式 handler 注入实现彻底解耦：

```fcstm
state CalibrationMode {
    enter { offset = 0; samples = 0; }
    enter abstract OpenValve;                          // hardware-specific, placeholder
    during { offset = offset + read_sensor(); samples = samples + 1; }
    exit { offset = offset / samples; }
    exit abstract CloseValve;                          // hardware-specific, placeholder
}
```

Python 侧：

```python
class HardwareHandlers:
    @abstract_handler('Plant.CalibrationMode.OpenValve')
    def open_valve(self, ctx):  # ctx is frozen ReadOnlyExecutionContext
        gpio.set_pin(VALVE_OUT, HIGH)
runtime.register_handlers_from_object(HardwareHandlers())
```

测试时 mock handler、部署时实硬件 handler — **STM 模型不变**。两档错误处理（`abstract_error_mode={raise, log}`）把 handler 异常落到 `error_info` / `abstract_handler_errors` 供 agent loop 消费。Umple 的 lifecycle hook 是 host-language-bound 代码，没有此抽象层（agent report §6.4 / §6.7）。

#### C5 — Empirical demonstration on real industrial control system NL + reference-free evaluation enabling tooling（**evidence + enabling tooling，NOT core contribution**）

> "We demonstrate the method on a 20-case T0 subset of [sources/](../sources/), spanning 9 real industrial control system domains. Since canonical reference STMs do not exist for real industrial requirements (the same NL can be modeled as multiple semantically-equivalent STMs), we develop a reference-free evaluation protocol combining five intrinsic metrics (`ParseRate`, `SemValidRate`, `SimRate`, `ReachabilityRate`) with an LLM-judge rubric score (`JudgeScore`). The protocol and benchmark are **enabling tooling** that makes the method's evaluation feasible in this domain, not the method itself."

**Path 2 关键 framing**：我们**不与 baseline 的家电/通用 reactive system/domain model 一般性方法竞争** — 我们只干 baseline 工具链干不了的事：在真实工业控制系统 NL 上做 fully-automated grounded synthesis。reference-free protocol + sources/ benchmark 是让 method core (C1-C4) **能在这个差异化领域被实验验证的 supporting infrastructure**。core contribution 是 method 本身（C1-C4，且每条都对应 §11.3.0 三段论 framing 论证的一行）。

### 11.4 paper §1 contributions 列表（Path 2 视角）

按 paper §1 排序，前 4 条都是 method core，每条都对应 pyfcstm 一个 control-system-specific 能力 + §11.3.0 三段论 framing 论证的一行：

| # | 类别 | contribution | 对应 pyfcstm feature | 控制系统场景价值 |
| --- | --- | --- | --- | --- |
| 1 | **method** | In-loop deterministic feedback via speculative validation | `SimulationRuntime` DFS validation + `SimulationRuntimeDfsError` | 多模式切换 dead-end 识别 |
| 2 | **method** | Language-independent expression IR enables symbolic reasoning | `Expr` IR + `solver/` Z3 集成 + 跨 9 语言渲染 | 复杂数值守卫 + Z3 可达性 + 跨部署目标 |
| 3 | **method** | DSL-native aspect AOP + forced fault paths | `>> during before/after` + `!` forced transition | per-tick invariant + 强制 fault-recovery escape |
| 4 | **method** | Abstract action + read-only context for effector-agnostic STM synthesis | `enter abstract` + `@abstract_handler` + `ReadOnlyExecutionContext` | 硬件解耦 + handler 反射注入 |
| 5 | **evidence + enabling** | 20-case industrial control system NL benchmark + reference-free intrinsic + judge protocol | — | sources/ 9 真实工业领域 |

> 完整 LaTeX 模板 + 引用 key 等 paper drafting 阶段再具体写。

### 11.5 与 6 个 baseline 的方法学定位（速查表，paper §2 related work 直接复用）

完整 6-baseline 对照表见 §1.1。下面是 Path 2 视角的精简表：

| baseline | 方法学共同点 | 与我们的关键区别 |
| --- | --- | --- |
| structure_event_driven (#1) | 多步 prompting | **无 in-loop feedback**；reference-based eval；家电而非控制系统 |
| llms_emp (#2) | 多步 + in-loop feedback | feedback 仅 rule-based grammar/semantics，**无 sim/reach/judge**；reference-based eval；混合领域非纯控制系统 |
| IEC 61499 (#3) | 控制系统 + sim feedback | **需要 human-in-the-loop comments**；输出 IEC 61499 code 而非 STM |
| Automated Statechart Auto (#4) | 控制系统 | **微调而非 prompt-based**；Volvo 内部数据 + reference-based eval |
| Llama3 Umple (#5) | Umple 可执行性 check | 小模型 (8B)；**无 control system 语义**；reference-based eval |
| ttool-ai (#6) | 自动反馈循环 | feedback 是 JSON/syntax/约束 + post-hoc TTool simulator；**无 reachability witness**；系统级 spec 而非单 STM |

**关键 framing 点**：Path 2 与 baseline 的差异不在"是否多步" / "是否有 in-loop feedback"（很多 baseline 都有），而在 **(i) 反馈源 grounding 强度（externally grounded multi-source vs internally grounded single-source）** + **(ii) 任务定位（reference-free industrial control system vs reference-based academic benchmark）**。这两个差异是 paper §1 contributions 的双锚点。
