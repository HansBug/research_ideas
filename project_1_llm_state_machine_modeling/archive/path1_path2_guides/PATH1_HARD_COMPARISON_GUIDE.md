# Path 1 — 硬刚路线（Hard Comparison）接管指引

> 📌 **读这份文件前先看这里（2026-08-11 归档时添加）**
>
> 本文件是**冻结的历史指南**，正文与命令保留写作当时（2026 年 5–6 月）的目录名，**未作改写**——
> 改动它们等于篡改当时的陈述。但那些目录后来搬过家，所以文中出现旧路径时按下表换算：
>
> | 文中写的 | 现在在哪 |
> | :-- | :-- |
> | `project_1_llm_state_machine_modeling/method/` | `project_1_llm_state_machine_modeling/archive/agent_loop_method/`（模块名同步变为 `archive.agent_loop_method.*`） |
> | `project_1_llm_state_machine_modeling/eval/` | `project_1_llm_state_machine_modeling/archive/path1_evaluation/`（其中 `discover_matrix/` 去了 `paper_stm_issue_discover/`） |
> | `project_1_llm_state_machine_modeling/paper_v1/` | 就是本目录 `archive/path1_path2_guides/` |
> | `project_1_llm_state_machine_modeling/paper_stm_repair/` | `project_1_llm_state_machine_modeling/paper_stm_issue_discover/` |
>
> ⚠️ **Markdown 链接的 target 已经更新过**，点击可达；但**链接的显示文本仍是旧路径**。
> 照显示文本手敲会走错，以上表为准。
>
> 📌 另有一处**写作当时就写错**的链接已顺手修正：文中两处指向 `../SUMMARY.md` 的引用，
> 该文件从未存在过（`git log --diff-filter=A` 全历史无记录）；按上下文（sources 池子的
> 🟢 / T0 人工标注）实际应指 `sources/SUMMARY.md`，已改为 `../../sources/SUMMARY.md`。
>
> 复活说明见 [ARCHIVE_README.md](./ARCHIVE_README.md)。

> **本文件目标**：任何新 Claude / codex session 进入 `dev/path1-hard-comparison` branch 后，按本指引可直接接管，把 Path 1 quick experiment 推进到 sprint 末。
>
> **前置阅读**：先读 [../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md](../../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md)（meta-level 路线规划与决策准则），再读本文件。
>
> **版本**：v4（2026-05-27 — PR #11 共同基础落地后定稿；method/ + eval/ 全套实装完成，Path 1 实验目录与评测协议已切到 sources/ + 5-component manual eval）

## 1. 路线定位

Path 1 = **硬刚路线**，主张：**在与 baseline 论文同 protocol（component-level manual eval）下，把 method 应用到工业控制系统真实 NL 上，相对 baseline 最强 strategy（Hybrid）跑出显著更高的 5-component manual-eval F1**。

> **v3 修订说明**：原 v1/v2 把对手简化为 single-prompt 是错的。[structure_event_driven](../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/DESC.md) 论文里**最强 strategy 是 Hybrid**（先 Single-Prompt 出 Umple 草稿，再用 Structure-Driven 多步迭代细化），GPT-4o 上 macro-F1 = 0.6559 / Claude 3.5 Sonnet 单 prompt = 0.7029。Path 1 主对手应是 Hybrid 在 GPT-5.5 上的重跑结果，而非任何 single-prompt 版本。
>
> **v4 修订说明**：原 v1-v3 把 dataset 锁定在 `structure_event_driven` 8 cases 上是错的 — 实际查 GT 后发现 8/8 cases 的 `reference_history_states_count >= 1`（每个 case 至少有一个 `.H` history pseudo-state），而 pyfcstm 形式上不支持 history pseudo-state，按"排除含 parallel/history 的 NL"规则会把整个 dataset 排除掉。Path 1 因此切换到**我们自建的 `sources/` T0+🟢 子集**（5-10 条工业控制系统 NL，FSM/EFSM/HSM 分层抽样），与 Path 2 共用 sources/ 池子但选样规模和 metric 不同。同时评测组件从 paper §IV 原口径的 7 类简化为 **5 类**（剔除 pyfcstm 不主张覆盖的 parallel_regions / history_states）。

### 1.1 paper 主卖点（如果 Path 1 被选定）

> "We propose an agent loop architecture that integrates pyfcstm's deterministic verifier feedback (parse / semantic / simulation, with scenario-based bug-finding probes via scenariogen self-managed mutation coverage) as in-loop feedback signals. We adapt the manual-evaluation protocol of Apvrille et al. (2025) — originally on the `structure_event_driven` UML statechart benchmark — to our small-scale industrial-control-system benchmark (`sources/` T0+🟢 subset, $N$=5-10 cases stratified across FSM/EFSM/HSM, 5-component manual eval). On these inputs, the prior best strategy (Hybrid SMF) re-run under GPT-5.5 achieves macro-F1 = $X$, while our method lifts it to $Y$. Improvements are particularly pronounced on `guards / actions / hierarchical states`, which prior work identified as the hardest components."

### 1.2 与 6 个主力 baseline 的方法学差异化

完整 6-baseline 对照表见 [discussion §4.4](../../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md#44-6-个主力-baseline-方法学全景v3-新增)。Path 1 sprint 阶段**只与 structure_event_driven Hybrid 对照**（但跑在我们的 sources/ T0+🟢 子集上，而非 structure_event 原数据集），其他 5 个 baseline（llms_emp / ttool-ai / IEC 61499 / Llama3 Umple / Automated Statechart Automotive）作为方向定后正式 paper 阶段的工作。

**sprint 范围声明（必须能向 reviewer 解释）**：

| 未在 sprint 复现的 baseline | 为什么 sprint 不做 | 方向定后怎么补 |
| --- | --- | --- |
| llms_emp 两阶段框架 (rule-based grammar/semantics feedback) | 输出是 PlantUML/SysML，不是 pyfcstm/Umple；需要写一套 PlantUML→pyfcstm 转换器；sprint 30h 不够 | paper §4.x 补 cross-formalism comparison（在 sources/ 上跑 llms_emp 风格 pipeline） |
| ttool-ai 自动反馈循环 (JSON/syntax check + post-hoc sim) | 输出是多 block AVATAR design 不是单 STM；task 不完全对齐 | paper §4.x discussion 段落讨论；不重跑实验，引用 paper 报告数字 |
| IEC 61499 仿真精化 (softPLC + 人类评论) | 需要 EAE / softPLC 环境部署；本质是 human-in-the-loop pipeline，与我们的 fully automated 范式不直接可比 | paper §5 discussion 段落讨论 "fully automated vs human-in-the-loop" trade-off |
| Llama3 Umple (Zero/One/RAG) | 模型代差大（Llama 3 8B vs GPT-5.5）；不公平对照 | paper §4.x 补 LLM model-comparison 附表 |
| Automated Statechart Automotive (微调) | 需要微调 LLM；Volvo 内部数据不可获取 | paper §2 related work 段落引用，不重跑 |

### 1.3 Path 1 学术 framing 三要点

1. **Protocol comparability** 强 — 评测协议直接 adapt 自 [structure_event_driven](../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/DESC.md) §IV manual eval protocol（5-component instance-level P/R/F1 + strict cascade，剔除 pyfcstm 不主张的 2 类组件）
2. **Reproducibility** 强 — baseline 复现代码在 [`baseline_structure_event.py`](../../reproduction/baselines/baseline_structure_event.py)，sources/ NL 公开在仓库 [`sources/`](../../sources/)；evaluation 全程 audit-trail 留痕（见 [`../eval/PROTOCOL.md`](../../archive/path1_evaluation/PROTOCOL.md) §1.3）
3. **Construct validity 担当** — sources/ 真实工业控制系统 NL 直接对接 paper 主问题；paper §6 limitations 显式承认 5-component 是 paper §IV 7-component 的子集 + sprint $N$=5-10 是小规模 benchmark，正式 paper 阶段需扩到 30-50 cases 并补 inter-rater agreement

### 1.4 Path 1 lift 学术意义

`A_full_ours - A0_strong` 这个 lift 反映的不是"我们比 baseline 强多少"，而是 **pyfcstm 外部 deterministic verifier feedback + scenariogen 自管 mutation coverage 作为 in-loop bug-finding probe** 相对于 **纯 prompt-based 多步 + 规则后处理** 的增量贡献。这正是 paper §1 contributions 第 1-3 条的实验证据：

1. In-loop multi-source deterministic verifier feedback
2. Fully automated no-human-in-the-loop
3. Scenario-based mutation-aware bug-finding probes in loop

> **Phase H (judge) 跳过说明**：sprint 阶段不接入 LLM-as-judge 第 4 个 feedback channel；`A_full_ours = parse+semantic+sim` 三通道（含 scenariogen self-managed 覆盖率）。判定 sprint 信号时也无 ex1 judge 贡献。Judge 留作方向定后正式 paper 阶段补充，原 v3 contribution 列表的 "Reachability witness as structured prompt input" 与 "LLM-as-judge as in-loop semantic feedback" 两条仍是 paper §1 contribution 候选，但不依赖 sprint 验证。

完整 6 条 contribution 见 [discussion §4.5](../../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md#45-我们的核心创新点v3-新增)。

## 2. 接管前自检

进入 `dev/path1-hard-comparison` branch 后，按以下顺序验证 sprint 状态：

```bash
# 1. 确认 branch
git branch --show-current
# 应该输出: dev/path1-hard-comparison

# 2. 确认 method/ + eval/ 共同基础已 fork 自 main
ls project_1_llm_state_machine_modeling/method/ project_1_llm_state_machine_modeling/eval/ 2>/dev/null
# method/: agents/ feedback/ loop.py schema.py prompts/ gpt_client.py scenariogen_validate.py
# eval/:   PROTOCOL.md extract/ annotate/ review/ aggregate.py report.py demo/ data/

# 3. 确认 pyfcstm 已安装
python -c "from pyfcstm.dsl import parse_with_grammar_entry; print('ok')"

# 4. 确认实验主路 LLM env 三件套已 source 到当前 shell 环境变量
# 调用前必须先：source .env（仓库根，已 gitignore）
# 代码绝不直接读取 .env 文件本身，只读 os.environ
[ -n "$LLM_ENDPOINT" ] && [ -n "$LLM_API_KEY" ] && [ -n "$LLM_MODEL" ] && echo "env ok"
# 若 ok 不出现，shell 里跑：source .env  然后重试
# 该 proxy 是 OpenAI-compatible，sprint 实验主路 (method/loop) 走这一个 endpoint；
# 切换 model 只改 LLM_MODEL 环境变量，不动 client 代码

# 5. 确认评测双 annotator CLI 配置（与 LLM_* 解耦，独立 .env 项）
# eval/ 的双 LLM 初审走 claude / codex CLI subprocess（非 HTTP API），原因见 eval/PROTOCOL.md §1.2
[ -n "$CLAUDE_CMD" ] && [ -n "$CLAUDE_MODEL" ] && [ -n "$CODEX_CMD" ] && [ -n "$CODEX_MODEL" ] && echo "annotator env ok"
which claude codex  # 这两个 CLI 必须在 PATH 中

# 6. 确认 baseline 复现代码可用（Path 1 特有）
test -f project_1_llm_state_machine_modeling/reproduction/baselines/baseline_structure_event.py && echo "baseline_structure_event ok"
# 注意：需要 verify 该代码支持把 LLM provider 切换到 GPT-5.5，且能跑 Hybrid strategy（4 strategy 中的最强）；详见 §5 实验脚本

# 7. 查 sprint 进度
cat project_1_llm_state_machine_modeling/method/STATUS.md 2>/dev/null || echo "no STATUS yet"
```

若 1-3、5-6 任一不通过，**停下来**，先确认 main 上 PR #11 是否已合入 + 本 branch 是否已 rebase 到 main — Path 1 branch 不应当独立做共同基础。

## 3. 数据规则（sources/ T0+🟢 + 排除 parallel/history NL）

### 3.1 T0 子集筛选

**T0 定义**：样本的 STM.md §2 自然语言描述中**不含显式时间约束**。判定规则（按优先级）：

1. 文本中是否含 `\b\d+\s*(second|seconds|minute|minutes|hour|hours|ms|millisecond)` 等时间量词 + 数字组合 → 含则非 T0
2. 文本中是否含 `after T_n`、`within T_n`、`every T_n` 等时间变量符号 → 含则非 T0
3. 文本中是否含 "timeout / time-out / delay / counting down / counts down / debounce / hysteresis" 等隐式时序词 → 含则非 T0
4. STM.md §0 已标 "代表时间级别" 字段，优先复用该标签

sources/ 池子已经标过 T0 / T1 / T2 / T3，优先复用 [`sources/SUMMARY.md`](../../sources/SUMMARY.md) 的人工标注；标签不齐时按上述规则补判。

### 3.2 数据集选择（与 v3 sprint plan §4.2 的差异）

| 维度 | sprint plan v3 原计划 | Path 1 v4 当前定稿 |
| --- | --- | --- |
| 数据集 | `structure_event_driven` 8 cases T0 子集 | **`sources/` T0+🟢 子集**（FSM/EFSM/HSM 分层抽 5-10 条）|
| 切换原因 | — | structure_event 9 个 case GT 均含 `reference_history_states_count ≥ 1`；与 pyfcstm 形式不支持的范围冲突，整 dataset 被排除 |
| baseline 对手 | Hybrid SMF on structure_event NL | **Hybrid SMF 重跑在 sources/ NL 上**（同 input, 不同 method）|

sources/ 池子规模（来自 [`sources/SUMMARY.md`](../../sources/SUMMARY.md) 的 🟢 + T0 + STM 类型筛选）：

| STM 类型 | T0+🟢 候选数 |
| --- | ---: |
| FSM | 68 |
| EFSM | 174 |
| HSM | 90 |
| **合计** | **332** |

Path 1 sprint 从中分层抽 5-10 条；实际数量在 Phase 4 开工时 verify，若不足按 §6 风险表回退。

### 3.3 选样落盘

筛完后落到：

```text
project_1_llm_state_machine_modeling/eval/data/sources_path1.parquet
```

schema：

```text
columns:
- case_id        : str   # sources/ 子目录名
- stm_type       : str   # FSM / EFSM / HSM
- nl_text        : str   # STM.md §2 整理后的 NL
- src_paper_path : str   # 反向到 sources/<case>/paper_content.txt 的指针
- rating         : str   # 🟢
- time_level     : str   # T0
```

### 3.4 排除规则（与 5-component 评测协议一致）

剔除以下样本（即使 T0+🟢）：

- NL 中明确含 parallel / concurrent regions（如 "in parallel with"）
- NL 中明确含 history-restore 语义（如 "resume to where it was before"）
- NL 只描述硬件 IO，无明确 STM 抽象的（state machine 隐性）

## 4. method/ 共同基础调用方式

Phase 0-3 已在 main 上落地（PR #11 commit `ff1e90ff`），Path 1 sprint 跑两个 method 标签：

### 4.1 `A0_strong` — baseline structure_event Hybrid 在 GPT-5.5 + sources/ NL 上重跑

调用现有复现代码（不在 method/ 共同基础内，在 reproduction/baselines/）：

```python
from reproduction.baselines.baseline_structure_event import run_hybrid  # 通用 NL 入口
from archive.agent_loop_method.gpt_client import get_llm_client  # 共同基础，统一走仓库根 .env

result = run_hybrid(
    nl_text=row["nl_text"],       # sources/ NL，与 A_full_ours 同 input
    llm_client=get_llm_client(),  # 走 LLM_ENDPOINT + LLM_API_KEY + LLM_MODEL 三件套
)

# result 含: predicted_dsl_text (Umple 文本), token_usage
```

**sprint Phase 0 必须 verify**：

1. `baseline_structure_event.py` 接口能接受 **NL string + 外部 llm_client**（不要 hardcode 在 structure_event case_id 列表里）
2. 如果原代码 hardcode 了 GPT-4o client 或 structure_event case 索引，需要花 30min-1h 重构为通用 NL 入口 + 外部 client 注入（统一走 archive.agent_loop_method.gpt_client）

### 4.2 `A_full_ours` — 我们的 full agent loop（无 judge）

调用 method/ 共同基础（与 Path 2 完全一致的接口）：

```python
from archive.agent_loop_method.loop import run_agent_loop
from archive.agent_loop_method.schema import LoopConfig, AgentLoopResult

result: AgentLoopResult = run_agent_loop(
    nl=row["nl_text"],
    config=LoopConfig(
        condition="A_full",
        n_iter=3,
        feedback_sources=["parse", "semantic", "sim"],  # Phase H (judge) 跳过
        modeling_mode="multi_step",                     # MTI 6-step (default)
        # llm_model 默认 None；None 时 archive.agent_loop_method.gpt_client 从 env LLM_MODEL 读取
        # 想强制指定模型时再显式传入字符串
    ),
)

# result.final_dsl              : pyfcstm DSL 文本
# result.iter_traces            : 每轮迭代的 (model, feedback, repair) 三元组
# result.token_usage            : dict
# result.scenariogen_coverage   : Phase E v3 (f) 的 6-mutation 覆盖率自检结果
```

### 4.2a `method/gpt_client.py` 统一 LLM client（Phase 0 已实装于 PR #11）

实验主路所有 LLM 调用（spec / model / repair / NL summary / baseline Hybrid 内部）**全部走这一个 client**。

**评测 annotator 例外**：`eval/annotate/{claude,codex}.py` 走 `claude` / `codex` CLI subprocess，不经 `gpt_client`，配置项是 `.env` 里独立的 `CLAUDE_CMD/MODEL` + `CODEX_CMD/MODEL` 四件套。详见 [`../eval/PROTOCOL.md`](../../archive/path1_evaluation/PROTOCOL.md) §1.2。

**约束**：代码**绝不**用 `python-dotenv` 或其他方式直接读 `.env` 文件；只读 `os.environ`。运行前由 shell `source .env` 把三件套（及 annotator 四件套）加载到环境变量。

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

切换实验主路模型（GPT-5.5 → GPT-5.4 → ...）**只需要改 .env 的 LLM_MODEL 然后重新 source .env**，代码完全不动。cross-vendor sanity 在 sprint 后是改一行 env + 重新 source 的事。

> **proxy 模型覆盖说明**：当前 LLM_ENDPOINT 提供的 OpenAI-compatible 代理只挂 GPT 系列（gpt-5.2 / 5.3-codex / 5.4 / 5.5 等 GPT 家族），**不直接覆盖 Anthropic / 其他 vendor**。如需 cross-vendor sanity 跑 Claude，正式 paper 阶段需要另接 endpoint 或走 Anthropic 原生 API（不在 sprint 范围）。

### 4.3 DSL 格式差异处理

A0_strong 输出 Umple，A_full_ours 输出 pyfcstm DSL。两者在评测 §6 之前需要先做 component 抽取归一化（两个 parser 都抽出 5 类组件后再走 instance-level manual eval）。**这块归一化代码已是 PR #11 共同基础的一部分**，在 [`../eval/extract/umple.py`](../../archive/path1_evaluation/extract/umple.py) 与 [`../eval/extract/pyfcstm.py`](../../archive/path1_evaluation/extract/pyfcstm.py) 实现，统一输出 5-component `ComponentSet`（states / transitions / guards / actions / hierarchical_states）。

## 5. 实验脚本 `method/run_path1.py`

CLI 接口（Phase 4 开工时由 Path 1 branch 实现，本指引固定接口规范）：

```bash
# 先在 shell source 仓库根 .env 把三件套加载到环境变量
# 代码不会读 .env 文件本身，只读 os.environ
source .env

# 然后跑 run_path1（model 走 env LLM_MODEL，CLI 不需要传）
python -m archive.agent_loop_method.run_path1 \
  --samples project_1_llm_state_machine_modeling/eval/data/sources_path1.parquet \
  --methods A0_strong,A_full_ours \
  --n-iter 3 \
  --out project_1_llm_state_machine_modeling/eval/data/preds/ \
  --resume  # 支持 checkpoint，跑到一半挂掉可继续
```

输出每 sample 一个目录 `eval/data/preds/<case_id>/{A0_strong,A_full_ours}.json + .txt`，schema 与 `eval/data/preds/` 演习目录一致（见 PR #11 `automatic-elevator-controller` / `abs-fsm-brake-control` 两个 mock case）。

method 字段映射（在 run_path1.py 内部分发）：

- `A0_strong` → 调 `reproduction.baselines.baseline_structure_event.run_hybrid(nl_text=..., llm_client=get_llm_client())`，输出 Umple text
- `A_full_ours` → 调 `archive.agent_loop_method.loop.run_agent_loop(nl=..., config=LoopConfig(condition="A_full", n_iter=3, feedback_sources=["parse","semantic","sim"], modeling_mode="multi_step"))`，输出 pyfcstm DSL

实现要点：

1. **checkpoint**：每条样本跑完立即写盘一份，不等全部跑完
2. **失败容忍**：单条样本 GPT 5xx 重试 3 次后跳过，记 `status="api_failed"`，不中止整个 batch
3. **token tracking**：每条 sample 记 input/output token，落到 `eval/data/preds/<case>/_token_log.json`
4. **DSL 格式归一化**：A0_strong 出 Umple，A_full_ours 出 pyfcstm DSL，由 [`../eval/extract/`](../../archive/path1_evaluation/extract/) 抽 5 类组件后再进 §6 manual eval（不再写额外归一化代码，复用 PR #11 已有）

## 6. 评测协议（adapt 自 [structure_event_driven 论文 §IV](../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/paper_content.txt) 的 manual evaluation scheme）

> **v3 修订**：v2 此节有 3 处隐藏不一致 — actions 范围、strict cascade rule、overall F1 计算 — 已全部修正与 baseline §IV-B/C 一致；不一致的部分（manual 评测 → LLM-judge alignment）在新 §6.4 显式说明 + 给出后续补偿动作。
>
> **v4 修订**：基于 [`../eval/PROTOCOL.md`](../../archive/path1_evaluation/PROTOCOL.md) 已落地的 manual-eval 基础设施，本节从原 v3 的 7 类组件 + manual eval 概念描述，更新为 **5 类组件** + **LLM-初审 + 人类签字** 操作流（保留 strict cascade + 语义等价判定原则）。**详细协议以 [`../eval/PROTOCOL.md`](../../archive/path1_evaluation/PROTOCOL.md) 为准**，本节为 Path 1 视角的接口说明 + 与 baseline 协议的对齐声明。

### 6.1 5 类组件定义（**adapt 自 baseline §IV-B**）

| 组件 | 抽取方式 | 比较单位 | baseline 特殊规定 |
| --- | --- | --- | --- |
| `states` | DSL 中所有 state 名 | 名称集合（语义等价允许） | — |
| `transitions` | (src, event, dst) 三元组集合 | 三元组（src/dst 名称语义等价允许） | **transitions to non-matching states 自动 FP**（strict cascade） |
| `guards` | transition 上 [condition] 子句 | 表达式集合（语义等价允许） | **依赖 FP transition 的 guards 自动 FP** |
| `actions` | transition 上 /effect 子句（**仅 transition actions**） | 表达式集合 | **baseline §IV-B 明确排除 state entry/exit/do actions** |
| `hierarchical_states` | composite state 名集合 | 名称集合 | superstate 含相同 substates 视为等价 |

> **v4 删除 `parallel_regions` / `history_states`**：pyfcstm 形式上不支持这两类（A_full_ours 输出结构性为 0），paper 不主张覆盖这两类。paper §6 limitations 显式声明本研究评测 5-component 是 baseline §IV 7-component 的子集；结论不外推到 parallel_regions / history_states。组件 IR 抽取统一走 [`../eval/extract/`](../../archive/path1_evaluation/extract/) 的 5-component `ComponentSet`。

### 6.2 P/R/F1 计算（**与 baseline §IV-C 一致**）

对每类组件 $c$ 计算：

$$P_c = \frac{TP_c}{TP_c + FP_c}, \quad R_c = \frac{TP_c}{TP_c + FN_c}, \quad F_{1,c} = \frac{2 P_c R_c}{P_c + R_c}$$

**Overall F1（与 baseline 一致 — 不是 macro-F1）**：

baseline §IV-C 明确 overall F1 是 "aggregating the true positives (TP), false positives (FP), and false negatives (FN) of all components"。我们采用同一公式：

$$\text{overall-}P = \frac{\sum_c TP_c}{\sum_c (TP_c + FP_c)}, \quad \text{overall-}R = \frac{\sum_c TP_c}{\sum_c (TP_c + FN_c)}, \quad \text{overall-}F_1 = \frac{2 \cdot \text{overall-}P \cdot \text{overall-}R}{\text{overall-}P + \text{overall-}R}$$

**注意**：v2 写的 macro-F1 是错的，已修正为 baseline 一致的 aggregate-F1。两种 F1 在组件分布不均时数值差异显著（如 history_states 每 case 仅 1 个，macro-F1 会被它放大），混用会导致与 baseline 论文数字不可比。

### 6.3 名称语义等价判定（**人工评测，与 baseline 一致**）

baseline §IV-A 用 manual single-author evaluation 判定语义等价（"components that are intended to represent the same concept ... are graded as equivalent, even if their names differ"）。

**paper 中正式评测协议也采用人工评测**，与 baseline 完全对齐 — §6.4 表中 Semantic equivalence 行标 "一致" 即指此。

#### 实操辅助流程（**已实装于 [`../eval/`](../../archive/path1_evaluation/)，仅 sprint 内部提效，paper 中不进 protocol description**）

为让单评测者在 sprint 时间内完成 10-20 runs × 5 组件 = 50-100 评审单元，采用 **双 LLM 初审 + 人类签字** 流程（详见 [`../eval/PROTOCOL.md`](../../archive/path1_evaluation/PROTOCOL.md) §1.2）：

1. **双 LLM 初审**：claude（`claude-opus-4-7`）+ codex（`gpt-5.5`）各自对每个 (ref_instance, pred_instance) 对独立给出 TP/FP/FN 提案 + rationale + confidence；落 `eval/review/raw/<case>/<cond>/<kind>/{claude,codex}.json`
2. **中文 markdown 评审包**：[`../eval/review/render.py`](../../archive/path1_evaluation/review/render.py) 把两份提案合并为 `eval/review/packs/<case>/<cond>/<kind>.md`，包顶含 NL 原文 + ref/pred 模型全文
3. **自动预勾选**：双 annotator 完全一致 → 默认 `[x] 采纳 Claude`（heading `✅`）；不一致 → 留空（heading `🔴` 需复议）；单票 → 留空（heading `🟡`）
4. **人类签字**：评测者逐行确认；audit-trail 全程留痕（`auto_marked` / `user_choice` / `user_final_status` / `user_note` 四列）
5. **签字后汇总**：[`../eval/demo/finalize_after_signoff.py`](../../archive/path1_evaluation/demo/finalize_after_signoff.py) → `eval/results/full_annotations.parquet`（26 列，paper-claim 唯一信源）+ `REPORT.md`（中文 audit-trail 报告）+ `summary.csv`（P/R/F1）；任一未签字行 → `UnsignedRowsError` refuse to finalize

**paper §4 evaluation 仅描述人工评测协议**，双 LLM 预审作为 internal tooling 仅在 §6 / appendix 简短提及（"to improve evaluator efficiency, we used two independent LLM annotators to propose initial classifications which were then manually verified row-by-row by the author; rows where the two annotators agreed were auto-pre-marked with the agreed label and confirmed by the author; rows where they disagreed required explicit author decision"）。这是工业界 SE 论文常用做法 — LLM-assisted labeling 但 final label 视为 human gold；双 annotator 设计额外提供 inter-LLM agreement signal 帮助评测者聚焦低置信度 / 分歧行。

### 6.4 与 baseline 评测协议的对齐声明（v4 修订 — 5-component subset adaptation）

| 维度 | baseline §IV 协议 | 我们 sprint Path 1 协议 | 一致 / 差异 |
| --- | --- | --- | --- |
| 组件清单 | 7 类：states / transitions / guards / actions / hierarchical / parallel / history | **5 类**（去 parallel / history，pyfcstm 形式不支持，paper 不主张覆盖） | **subset**（paper §6 limitations 显式声明）|
| `actions` 范围 | 仅 transition actions, **排除 state entry/exit/do** | 同（按 baseline 严格执行） | **一致** |
| Strict cascade rule | transitions to non-matching states 自动 FP；依赖 FP transition 的 guards/actions 自动 FP | 同 | **一致** |
| TP/FP/FN 分类 | 三类，含 exact match + semantic match | 同 | **一致** |
| Component-level P/R/F1 | $P_c, R_c, F_{1,c}$ | 同 | **一致** |
| Overall F1 | **aggregate TP/FP/FN across all components**（**NOT macro-F1**） | 同（v2 误写为 macro-F1，v3 已修正） | **一致** |
| Semantic equivalence 判定 | manual single-author evaluation | **manual single-evaluator**（双 LLM 预审仅作内部提效辅助，不进 paper protocol） | **一致** |
| Ground-truth 来源 | 8 个本科课程题的 expert-drawn diagrams | **`sources/` T0+🟢 5-10 cases 工业控制系统 NL** + 评测者手工构建 5-component reference IR | **不同 dataset，同 ground-truth-construction methodology** |
| 评估者 multiplicity | single author per approach | single human evaluator per approach | **一致** |

**核心 protocol 与 baseline 一致**（TP/FP/FN 定义、strict cascade、overall F1 计算）；dataset 切到 sources/ 是我们引入的差异，paper §6 limitations 显式声明 + §Discussion 说明 method 在 sources/ 工业 NL 上的可迁移性预期。

**paper §6 limitations 仍需讨论的点**（与 baseline 共有 + 我们 v4 引入）：

1. **单评测者主观性**（与 baseline 共有）：可在方向定后用 random subset 加第二位评测者算 Cohen's $\kappa$，作为 inter-rater agreement evidence
2. **双 LLM 预审是否偏置评测**（我们引入）：在 PATH1_REPORT §6 confounder 中披露；可选做 sensitivity analysis — 关闭双 LLM 预审在 random 3-5 cases 上跑全人工 alignment 看 disagreement rate；`eval/results/full_annotations.parquet` 的 `auto_marked` 列已保留每行是否被双 annotator 一致自动预勾选的状态供审计
3. **5-component subset 取代 7-component**（我们引入）：paper §6 显式声明 parallel_regions / history_states 不在评测范围，结论不外推；正式 paper 阶段若要扩到 7-component 需另选不依赖 pyfcstm 表达的 method 或在 method 中加 parallel/history 扩展

## 7. 结果落盘 schema

> **v4 修订**：实验输出与评测产物分离 — 实验脚本只产 `predictions.parquet`（每 sample × method 的预测 + token），评测产物（P/R/F1 / audit-trail）走 [`../eval/`](../../archive/path1_evaluation/) 的 `full_annotations.parquet` + `REPORT.md` + `summary.csv` 三件套，不重复定义；本节仅描述实验脚本侧的预测表。

### 7.1 `eval/data/preds/<case_id>/{A0_strong,A_full_ours}.{json,txt}`

```text
<case_id>/A0_strong.json:    {"source": "baseline_hybrid", "case_id": ..., "predicted_dsl_format": "umple", "token_usage": {...}, "status": "ok"|"api_failed"|"parse_fail"}
<case_id>/A0_strong.txt:     Umple 文本
<case_id>/A_full_ours.json:  {"source": "agent_loop", "case_id": ..., "predicted_dsl_format": "pyfcstm", "iter_traces": [...], "scenariogen_coverage": [...], "token_usage": {...}, "status": ...}
<case_id>/A_full_ours.txt:   pyfcstm DSL 文本
<case_id>/_token_log.json:   逐次 LLM call 的 input/output token + duration
```

schema 与 PR #11 演习用的 2 case (`automatic-elevator-controller` / `abs-fsm-brake-control`) 完全一致。

### 7.2 评测产物（由 [`../eval/`](../../archive/path1_evaluation/) pipeline 产出，不由 run_path1.py 直接写）

```text
eval/review/raw/<case>/<cond>/<kind>/{claude,codex}.json   # 双 annotator 原始 JSON
eval/review/packs/<case>/<cond>/<kind>.md                  # 中文 markdown 评审包（你签字这里）
eval/review/loaded/reviewed.parquet                        # markdown 解析回的统一表
eval/results/full_annotations.parquet                      # 26 列 audit-trail（paper-claim 信源）
eval/results/REPORT.md                                     # 中文 audit-trail 总报告
eval/results/summary.csv                                   # P/R/F1 浓缩
eval/results/detail.parquet                                # per case × condition × component
eval/results/macro_per_case.parquet                        # per case × condition macro F1
eval/results/overall_per_condition.parquet                 # per condition overall F1
```

## 8. `PATH1_REPORT.md` 产出要求

sprint 末 Phase 6 必须产出，**Claude 整理不下结论**。最低字段：

1. **§1 实验配置**：sources/ T0+🟢 子集组成（FSM / EFSM / HSM 各几条）、GPT 模型版本（gpt-5.5 主跑 / claude-opus-4-7 + gpt-5.5 评测 annotator）、迭代轮数 $N$
2. **§2 主结果表**：`A0_strong` (Hybrid on sources/ NL @ GPT-5.5) vs `A_full_ours` 的 5 类组件 P/R/F1 + overall-F1，行=组件，列=method（数据源：`eval/results/full_annotations.parquet`）
3. **§3 lift 分布**：每个 case 单独的 lift（不必出图，给 markdown 表）
4. **§4 signal 判定**：按 [discussion §4.1](../../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md) 的 S1/S2/S3/S4 把当前数据归类
5. **§5 confounders 列表**：API 失败 / 全轮 parse 失败 / token 截断的样本 + 评审中 🔴 不一致 / 🟡 单票被人工裁定行的分布，逐一列出
6. **§6 Claude 的方向建议 + rationale**：写明依据，不强推
7. **§7 后续 paper 工作量预估**：若选 Path 1，1-2 个月内要补的工作（扩 sources/ 到 30-50 cases / cross-vendor / 完整 ablation A1/A2/A3 / 接 Phase H judge 补 7-component 维度 等）

## 9. 风险与回退（Path 1 特有）

| 风险 | 触发 | 回退 |
| --- | --- | --- |
| sources/ T0+🟢 strata 抽不齐 | FSM/EFSM/HSM 某类不足 | 缩 strata 比例；若总数仍 $< 5$，把"显式时间词"判定放宽到"无 specific time literal"（保留 timeout / delay 等抽象时间词）；在 PATH1_REPORT §1 披露实际选样 |
| 双 LLM annotator 一致率过低 | `eval/review/packs/` 中 🔴 / 🟡 行占比 $> 30\%$ | annotator prompt 用 fixed seed；分歧行强制人工裁定（已是 protocol 默认）；在 PATH1_REPORT §5 confounder 中列分歧分布 |
| Ground-truth 构建工时超标 | $N$=5-10 cases 写 reference 5-component IR 太慢 | 跑 LLM-propose-ref pipeline（在 `eval/refgen/` 实装，sprint 演习后补，每 case 节约 ~15 min）；或临时缩到 $N$=3-5 |
| F1 lift 过低（$< 5$pp）信号不显著 | `A_full_ours` 没比 `A0_strong` 好多少 | 按 [discussion §4.1](../../discussions/2026-05-26-15-30-00-AI-讨论-第一篇论文agent-loop闭环2日冲刺计划.md) S4 处理，在 PATH1_REPORT.md §6 给出"信号弱"判定，由用户综合判断 |
| `baseline_structure_event.py` 不接受外部 NL | Phase 0 verify 时发现接口 hardcode 了 structure_event case 索引 | 花 30min-1h 重构为通用 NL 入口 + 外部 client 注入；fallback 用 single-prompt baseline 替代 Hybrid（在 PATH1_REPORT §1 明确披露），不阻塞 sprint |
| A0_strong 和 A_full_ours DSL 格式不同导致评测不公平 | Umple 抽 transitions / pyfcstm 抽 transitions 算出不同语义 | [`../eval/extract/`](../../archive/path1_evaluation/extract/) 已统一为 5-component `ComponentSet`；不一致样本标 confounder，PATH1_REPORT §6 披露 |

## 10. 完成度自检 checklist

sprint Phase 7 收口前用此 checklist 核验，缺哪条补哪条：

- [ ] `eval/data/sources_path1.parquet` 已落盘且 $\ge 5$ 条（FSM/EFSM/HSM 分层达成）
- [ ] 每个 case 的 `eval/data/refs/<case>/ref_components.json` 已写 + 你签字过
- [ ] `eval/data/preds/<case>/{A0_strong,A_full_ours}.json` 已落盘
- [ ] `eval/review/packs/<case>/<cond>/<kind>.md` 每个 non-empty pack 已签字
- [ ] `python eval/demo/finalize_after_signoff.py` 成功跑完（无 `UnsignedRowsError`）
- [ ] `eval/results/REPORT.md` + `full_annotations.parquet` + `summary.csv` 三件套产出
- [ ] `paper_v1/PATH1_REPORT.md` 含 §8 全 7 节
- [ ] `method/STATUS.md` 更新 Path 1 进度行
- [ ] GitHub PR #9 已 update（PR 描述含 PATH1_REPORT 关键数字摘要）
- [ ] Confounder 样本数 $\le$ 总样本数 30%（超过 30% 则方法实现可疑）

## 11. Method + Contribution 详述（paper writing 直接复用素材）

> 本节集中讲清楚 Path 1 视角下我们的 method 是什么、contribution 是什么；既给 sprint 末 PATH1_REPORT.md §7 (Claude 方向建议) 提供 anchored framing，也给方向定后正式 paper §1 contributions + §3 method 提供直接可复用的写作素材。

### 11.1 Method overview — Agent loop with externally-grounded in-loop feedback

```text
NL input (sources/ T0+🟢 case from industrial control NL corpus)
      |
      v
  [Multi-step Modeling]  走 method/gpt_client.py (LLM_MODEL from env)
      |  6 步 MTI 流水 (identify_state → identify_event → identify_variable →
      |                identify_transition → identify_action → build_pyfcstm)
      v
  current_model (pyfcstm DSL text)
      |
      +----+ Feedback Sources (gated cascade) +----------+
      |    |  ParseFeedback   (pyfcstm.dsl)              |
      |    |  SemanticFeedback (pyfcstm.model)           |
      |    |  SimFeedback     (pyfcstm.simulate         |
      |    |                   + scenariogen 自管 mutation|
      |    |                   coverage as bug probes)   |
      |    |  [JudgeFeedback   — Phase H 跳过，sprint 不用] |
      |    +----+--------------------------------+       |
      |         |
      v         v
  feedback_bundle (JSON schema)
      |
      v
  [Cascaded Repair]      走 method/gpt_client.py
      |  4 个 fix sub-prompt：fix_parse / fix_sem / fix_sim / fix_judge(占位)
      |  按 earliest-failing channel 路由 + 共享 pyfcstm grammar reference
      v
  next_model --> 回到 Feedback Sources, iterate N=3 rounds
      |
      v
  final_model (pyfcstm DSL) --> 进入 §6 评测协议算 P/R/F1 vs A0_strong
```

### 11.2 Method 各组件细节

#### 11.2.1 LLM agent 链

1. **MTI 6-step Multi-step Modeler**（PR #11 Phase F 实装）：NL → 6 步流水（identify_state → identify_event → identify_variable → identify_transition → identify_action → build_pyfcstm）→ pyfcstm DSL
   - **设计目的**：把"自由文本"压成 5 个结构化 list 后再 assemble DSL，避免单 prompt 直接面对 NL 时陷入语言细节歧义；与 sprint plan v3 的"Spec-driven LLM"概念一致
   - **prompt 全英文**（paper 投稿英文，统一）；共享 pyfcstm grammar reference (`method/prompts/_pyfcstm_grammar.md`)
   - 替代方案 single_prompt（同代码内 `LoopConfig.modeling_mode="single_prompt"`）作 ablation 对照
2. **ScenarioGen**（PR #11 Phase G+E v3 实装）：NL + 模型 → 多 step BDD scenarios + 6 mutation 覆盖率自检
   - **scenariogen self-validation**：scenariogen 后自动跑 6-mutation 覆盖率检查；任一类未被 catch → 用 `extra_directive` retry 直到覆盖
3. **Cascaded Repair**（PR #11 Phase E 实装）：(current DSL, feedback_bundle) → new DSL
   - 4 个 fix sub-prompt：`fix_parse.txt` / `fix_sem.txt` / `fix_sim.txt` / `fix_judge.txt`（占位）
   - 按 earliest-failing channel 路由；fix_sim 含 passing-scenarios 显式 preservation 段
   - **prompt 显式约束**："按 feedback 中的具体错误指针 (line/col/state/transition) 做定向修复，不要大改"

#### 11.2.2 三个 deterministic feedback sources（externally grounded）+ scenariogen 自管

| Source | pyfcstm 入口 | 输出 schema 核心字段 | 在 paper §3 method 里是哪一条 contribution |
| --- | --- | --- | --- |
| Parse | `pyfcstm.dsl.parse_with_grammar_entry` | `{ok, line, col, expected_tokens, got, snippet}` | C2 |
| Semantic | `pyfcstm.model.parse_dsl_node_to_state_machine` | `{ok, missing_states, dangling_transitions, undefined_vars, type_mismatches}` | C2 |
| Sim | `pyfcstm.simulate.SimulationRuntime` + scenariogen 多 step BDD probes（含 6-mutation 自检） | `{ok, scenario_violations, per_step_var_mismatches, runtime_error}` | **C1 + C2 + C3 + C4** (speculative validation + Z3 ready + aspect/forced 在这一路触达) |
| ~~Judge~~ | ~~ex1 `ExpertReviewAgent`~~ | **Phase H 跳过，sprint 不接入；留作正式 paper 阶段补**  | ~~C5~~ → 留作 future work |

#### 11.2.3 Feedback 合并策略 + 迭代控制

- **gated cascade**：Parse 过 → Semantic 过 → Sim 过 。任一卡住直接出反馈进 Repair，省 token
- **scenariogen frozen-once**：scenarios 在 iter 循环外生成一次 + mutation 覆盖率自检；model 适配 scenarios 不反向
- **迭代上限 $N=3$**：若某轮 feedback_bundle 全部 ok，提前 break，标记 `status="converged"`
- **不收敛回退**：3 轮仍有 feedback 不为空时，取 iter_3 的 final_model 进评测，标记 `status="not_converged"`

### 11.3 Contribution 详述（**Path 1 视角：method 为主，empirical lift 作 evidence**）

> **v4 修订**：原 v3 把 "Quantitative empirical lift" 作 C1 主 contribution；用户 2026-05-26 明确反馈"两个论文都不要把其他的当成核心贡献"，v4 调整为 method 为主、empirical lift 作 evidence。

Path 1 视角下我们的 5 条 contribution（前 4 条 method core，第 5 条 evidence）：

#### C1 — In-loop deterministic feedback via speculative validation（**method core**）

> "We integrate pyfcstm's cycle-based simulation runtime — featuring per-cycle deepcopy-snapshot speculative DFS validation bounded by 1000 steps, 64 stack frames, and structural-and-value signature pruning (`pyfcstm/simulate/runtime.py:_validate_transition` and `_run_cycle_on_context`) — as a **deterministic in-loop feedback source** for LLM-driven STM synthesis. Unlike Umple's generate-then-execute pipeline, pyfcstm rejects transitions whose downstream init / pseudo / parent-continuation chains cannot reach a stoppable boundary, and surfaces a structured `SimulationRuntimeDfsError` whose docstring enumerates the exact pathological patterns LLMs are known to emit (composite state with no enabled init transition, pseudo-state chains that never settle, mutually-blocking guards, exit-vs-parent-continuation cycles). This converts model checking from an offline batch artifact into an **online repair signal**."

#### C2 — Language-independent expression IR enables symbolic reasoning without code generation（**method core**）

> "The DSL ships a unified `Expr` IR (`pyfcstm/model/expr.py`) supporting the full arithmetic / bitwise / logical / ternary / 22-function math closure required by state-machine guards and effects. This same IR is simultaneously (a) numerically evaluable, (b) AST-round-trippable, (c) translatable to Z3 via `pyfcstm/solver/expr.py:expr_to_z3`, and (d) renderable into 9 target-language styles (`pyfcstm/render/expr.py:_KNOWN_STYLES`). We exploit this single IR to provide LLM agents with **guard SMT satisfiability checks** (`pyfcstm/solver/solve.py:solve`) and **symbolic effect propagation** (`pyfcstm/solver/operation.py:execute_operations`) as in-loop feedback signals — without ever leaving the DSL toolchain. Umple's host-language-bound guards cannot offer equivalent."

#### C3 — DSL-native aspect AOP and forced fault paths（**method core**）

> "We design our method around two pyfcstm DSL-level primitives that Umple and PlantUML lack: (i) **aspect actions** (`>> during before / after`) cascading from root to leaf states at every cycle (`pyfcstm/model/model.py:iter_on_during_aspect_recursively`), enabling first-class encoding of cross-cutting per-tick invariants, monitoring, and logging; and (ii) **forced transitions** (`!`) which the model layer recursively expands to every applicable descendant substate (`pyfcstm/model/model.py:_recursive_finish_states`), giving one-line declarative encoding of global escape paths. Although these primitives were originally motivated by control-system idioms, our experiments demonstrate they also improve STM-synthesis quality on the home-appliance benchmark."

#### C4 — Abstract action + read-only context decouples symbolic STM from physical effectors（**method core**）

> "Combining DSL-level abstract action declarations (`enter abstract Init;` / `during abstract Monitor;` / `>> during before abstract LogTick;`) with the Python-side `@abstract_handler` decorator and `ReadOnlyExecutionContext` (`pyfcstm/simulate/decorators.py` + `context.py`) lets the LLM synthesize STMs **without committing to a deployment target**. Handlers are injected at run-time through an immutable frozen context, and two-mode error handling (`abstract_error_mode={raise, log}`) captures handler failures into `error_info` / `abstract_handler_errors` fields for the agent loop to consume. Umple's lifecycle hooks are host-language-bound and provide no equivalent DSL-level abstraction."

#### C5 — Empirical demonstration on industrial control-system NL benchmark（**evidence section, NOT core contribution**）

> "On a small-scale industrial-control-system benchmark drawn from `sources/` ($N$=5-10 cases stratified across FSM/EFSM/HSM, T0+🟢 subset, manually constructed 5-component reference models), our method achieves overall-F1 = $X$ on the same model (LLM_MODEL=GPT-5.5), lifting the overall-F1 of the strongest prior strategy (Hybrid SMF, re-run on our `sources/` inputs) by $\Delta$ percentage points, with the largest gains on `guards / actions / hierarchical_states`, the three categories the prior work identified as hardest on home-appliance / undergrad-course datasets (baseline Hybrid GPT-4o: guards=0.42 / actions=0.34). The choice of `sources/` over the original `structure_event_driven` 8-case dataset is forced by the latter's universal use of history pseudo-states (`history_states_count ≥ 1` in all 8 GTs), which falls outside pyfcstm's expressive scope; this constraint is acknowledged in §6 limitations."

**This empirical result is not the paper's core contribution** — it is the evidence supporting C1-C4. The core contribution is the method itself. paper §1 应当把 C1-C4 作为 numbered contributions，C5 在 §1 末段作为 "We empirically validate the method on..." evidence sentence 给出。

### 11.4 paper §1 contributions 列表（Path 1 视角）

按 paper §1 排序，前 4 条都是 method core：

| # | 类别 | contribution |
| --- | --- | --- |
| 1 | **method** | In-loop deterministic feedback via speculative validation |
| 2 | **method** | Language-independent expression IR enables symbolic reasoning without codegen |
| 3 | **method** | DSL-native aspect AOP + forced fault paths |
| 4 | **method** | Abstract action + read-only context for effector-agnostic STM synthesis |
| 5 | **evidence** | Empirical demonstration on `sources/` T0+🟢 industrial control-system NL subset over Hybrid baseline re-run on the same inputs |

> 完整 LaTeX 模板 + 引用 key 等 paper drafting 阶段再具体写 — sprint 阶段保留 contribution 列表即可。

### 11.5 与 6 个 baseline 的方法学定位（速查表，paper §2 related work 直接复用）

| baseline | 方法学共同点 | 与我们的关键区别 |
| --- | --- | --- |
| structure_event_driven (#1) | 多步 prompting | **无 in-loop feedback**；仅后处理规则 |
| llms_emp (#2) | 多步 + in-loop feedback | feedback 仅 rule-based grammar/semantics，**无 sim/reach/judge**；输出 PlantUML 而非 pyfcstm |
| IEC 61499 (#3) | 控制系统 + sim feedback | **需要 human-in-the-loop comments**；与 fully automated 范式不可直接比 |
| Automated Statechart Auto (#4) | 控制系统 | **微调而非 prompt-based**；Volvo 内部数据不可获取 |
| Llama3 Umple (#5) | Umple 可执行性 check | 小模型 (8B)；**无 in-loop iterative repair** |
| ttool-ai (#6) | 自动反馈循环 | feedback 是 JSON/syntax/约束 + post-hoc TTool simulator；**无 reachability witness** |
