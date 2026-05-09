# project_ex1 — 长线暂停 + 重构规划 + 未来路线（feedback / 强化学习）讨论

> **时间**：2026-05-09 15:19:23 起稿；2026-05-09 16:xx 二次完善（补"长线工作 + RL 方向 + 暂停投入但保留资产"口径）
> **形式**：W4.x 工作收口 + 暂停投入前的最终盘点 + 长线方向说明
> **状态**：本项目作为**长线工作**保留 —— 当前 PR 在说明状况后 merge 到 `main`，随后**优先回到 `project_1`**继续推进；ex1 的代码 / 数据 / 实验结论 / 文档**完整保留为长线资产**，**不再短期内继续投入新功能**，但**未来可重新激活**（最可能的两条路线见 §4：作为 `project_1` 的 feedback 源，或在强化学习场景下作为奖励信号 / critic）。本文件是这次暂停前的最后一份内部记录
> **关联文档**：
>
> 1. [2026-05-08-19-20-31-AI-讨论-project_ex1学术定位与相关工作综述.md](./2026-05-08-19-20-31-AI-讨论-project_ex1学术定位与相关工作综述.md) — 学术定位主稿（v4.3）
> 2. [2026-05-09-12-58-25-AI-讨论-prompt实现一致性待处理清单.md](./2026-05-09-12-58-25-AI-讨论-prompt实现一致性待处理清单.md) — I-1 ~ I-20 不一致清单 + Part II 代码事实档案

---

## 0. 摘要

本次讨论一次性沉淀以下四件事：

1. **现状盘点**：W4.x 完整收口后的代码状态（pydoc 100%、死代码清理、阶段口径冻结）与遗留待办（20 条 prompt-implementation 不一致 + 6 大目录散乱）；
2. **重构规划**：把 `src/` 当前混合状态（importable package + CLI 脚本 + 实验脚本 + 流程文档）拆成 6 大职责清晰的物理路径，并提供 9-commit TDD 增量执行计划，作为下一阶段重启时的施工说明书；
3. **未来路线**：与导师讨论后形成两条可能方向 ——
   - **路线 A（feedback）**：把 `LLM-as-Judge` 重新定位为 `LLM-as-feedback`，作为 `project_1` 迭代式状态机建模闭环里的反馈源；
   - **路线 B（强化学习）**：把 anchored rubric + sanity bound + 8 指标体系作为 RL 场景下的**奖励信号 / critic**，用于训练或微调下一代 STM 生成器；
4. **暂停投入与资产保留**：本项目的当前形态作为"独立 review 子系统"**告一段落**（不是"终结"，而是"暂停投入 + 资产保全"）。重构与方法重新落地的工作**不在本次合入前完成**；后续在 `project_1` 进展明朗、或 RL 路线有新需求时**择机重新激活**。

> **核心立场**：暂停 ≠ 放弃。本项目 W4.x 阶段已经形成稳定的方法学骨架（6 维 anchored rubric + 3-stage runtime + sanity bound + 8 指标）和可复用的实验数据 / 文献库，所有这些**都按"长线资产"标准保留**，不删、不下沉、不归档移除。

---

## 1. 现状盘点

### 1.1 已完成（W4.x 期间）

#### A. 工程层面

1. **3-stage runtime 已经稳定**：[src/expert_review/graph/runtime.py](../src/expert_review/graph/runtime.py)
   - `PREPARATION`：Contract Router → 并行三抽取（Input / Prediction / Reference Extractor）→ Evidence Regime Estimator → Review Policy Builder
   - `ANALYSIS`：并行三审（Traceability / Equivalence / Pragmatic Quality）→ Missing-Evidence Critic
   - `FINAL`：Score Composer（含 6 维 rubric LLM refinement）→ Final Synthesizer
   - W3 ablation 验证后 `Disagreement Arbiter` 已删除（ΔHAI=+0.1556 反向贡献），仅保留中文 audit 注释作为历史 trail
2. **死代码清理（W4.x Phase 0）**：
   - `legacy/` 目录整体删除（外部 0 引用）
   - `Disagreement Arbiter` 字符串残留在 4 个文件中清理完毕
   - 42/42 unit tests 全程绿
3. **中文 RST pydoc 全量补全（W4.x Phase 1-9）**：
   - 64 个 Python 文件，module / class / function / method 四级覆盖率 100%
   - module docstring 含 4 段标准结构（作用 / 设计思路 / 关键约束 / caveat）
   - 公共 API 配 `Examples::` 段，可被 `pytest --doctest-modules` 验证
   - 共计 **419 zh + 15 en items**（en 部分为外部 schema 兼容遗留，未触动）
4. **README + GUIDE 同步**：[src/expert_review/README.md](../src/expert_review/README.md)、[src/expert_review/GUIDE.md](../src/expert_review/GUIDE.md) 与当前代码状态一致；`Phase 7 ~ Phase 15` 阶段口径全部冻结
5. **benchmark harness 稳定**：`scope=phase7` / `scope=phase14` / `scope=phase15` 三套对比面落地，`validation + lockbox + LOFO + lockbox residual audit` 默认验收链固定

#### B. 方法学层面

1. **Anchored rubric 6 维 + 5+1 双轨聚合** 形成稳定方法学骨架（详见学术定位主稿 §3）
2. **3 道晋升门**（Q1 双轨 / Q2 evidence consistency / Q3 multi-rep stability）固定为评估口径
3. **Sanity bound 机制**（per-dim + per-(regime, dim) 非对称）作为 LLM refinement 与 deterministic estimate 之间的护栏
4. **PDS / HAI / RAS / SAS / CRAS / normalized_mae / Calib / Stability** 八指标体系闭环

#### C. 文档与材料层面

1. **学术定位主稿 v4.3**（[2026-05-08-19-20-31-AI-讨论-project_ex1学术定位与相关工作综述.md](./2026-05-08-19-20-31-AI-讨论-project_ex1学术定位与相关工作综述.md)）
   - §0~§14 完整结构，含 3 张 mermaid + 28 条参考文献 + 真实片段 case study
2. **LLM-as-Judge 文献库**：[llm_as_judge_methods_corpus/](../llm_as_judge_methods_corpus/)
   - 14 篇论文（7 通用 + 7 SE 相关），每篇配 `paper.pdf` / `paper_content.txt` / `bibtex.bib` / `DESC.md`
3. **STM 评估材料库**：[state_machine_review_corpus/](../state_machine_review_corpus/)
4. **不一致清单 v2 大扩充**（[2026-05-09-12-58-25-AI-讨论-prompt实现一致性待处理清单.md](./2026-05-09-12-58-25-AI-讨论-prompt实现一致性待处理清单.md)）
   - Part I：I-1 ~ I-20 共 20 条不一致 issue
   - Part II：II-A ~ II-L 代码架构事实档案

### 1.2 待办（按风险等级）

#### P0（致命，方法叙事必须修）

1. **I-7**：`k-rep / 3σ / noise floor` 完全未实现 —— 学术稿声称 multi-rep stability 实际只有 `_rerun_subset` 的 2-rep
2. **I-1**：`evidence_discipline` prompt-implementation 错配 —— LLM 从未看到 reviewer 的 V_1 输出，实际在做 self-prediction 而非 self-audit（用户在 v4.3 主稿中已选定 option C "5+1+derived" 路线，但代码尚未对齐）
3. **I-12**：Operability proxy 完全未实现 —— 主稿提到的"评估自动化代价"维度只有 placeholder

#### P1（重要，影响数据可信度）

4. **I-13**：score-to-label 双阈值系统 —— `judgement_from_score`（0.90/0.75/0.55/0.35）与 `_band_from_score`（0.85/0.65/0.45/0.25）共存，结论会因调用入口不同而差异
5. **I-15**：Score Composer mode-specific shaping 在 paper narrative 中被过度简化为"5+1 平均"，实际包含 summary_mode / protocol_mode / component_review_mode / record_level 四种 blend 路径
6. **I-2**：`vv_role_coverage` 是 `VV_ROLE_HINTS` 硬编码关键词匹配，不是 LLM 评估
7. **I-9**：Calibration 实际是 `Brier + ECE` 加权（0.55:0.45），不是单 ECE
8. **I-3 / I-4 / I-5 / I-6 / I-8 / I-10 / I-11 / I-14 / I-16 ~ I-20**：详见 [2026-05-09-12-58-25-AI-讨论-prompt实现一致性待处理清单.md](./2026-05-09-12-58-25-AI-讨论-prompt实现一致性待处理清单.md)

#### P2（结构层，影响协作效率）

9. **目录散乱**：详见 §2 重构规划

---

## 2. 重构规划（推迟到下次重新激活时执行）

### 2.1 现状散乱情况

按职责把当前文件分到 12 个域：

| 域 | 路径 | 当前问题 |
|----|------|----------|
| A. importable package | `src/expert_review/` | 内部结构良好，但根层混着 docs（PYDOC_INVENTORY.md / PYDOC_ITEMS.md / GUIDE.md / README.md） |
| B. CLI / 入口脚本 | `src/run_expert_review.py` / `src/align_ttool_expert_review.py` | 与 importable package **同级**，包内外混杂 |
| C. 复现配置 | `src/config.py` / `src/tasks.py` | 同样在 src/ 顶层 |
| D. 数据准备 / fixture | 散落在 `experiments/build_*` | 33 个脚本全部在仓库顶层 `experiments/` |
| E. 实验运行 | 同 D，混 `analyze_*` / `run_*` / `assemble_*` | 没有按"准备 / 运行 / 分析 / 汇报"分层 |
| F. 包级 docs | `src/expert_review/{README,GUIDE,PYDOC_*}.md` | 与代码同目录，文件类型混杂 |
| G. 流程 docs | 无独立位置 | 比如 `REPRODUCTION_REPORT.md` 在 src/ 顶层 |
| H. designs | `src/expert_review/designs/` | 设计文档跟代码混在一起 |
| I. 测试 | `src/expert_review/test_*.py`（3 文件） | 跟代码同目录，没有独立 `tests/` |
| J. discussions | `discussions/` | 状态良好 |
| K. corpus | `llm_as_judge_methods_corpus/` / `state_machine_review_corpus/` | 状态良好 |
| L. 项目入口 | 无 `pyproject.toml` / 无 `Makefile` | 没有顶层标准化入口 |

### 2.2 推荐的 6 域物理重构

```
project_ex1_llm_judge_for_stm/
├── pyproject.toml              # NEW：顶层标准化入口
├── README.md                   # 项目入口（保留）
├── AGENTS.md                   # 软链 → CLAUDE.md（保留）
│
├── src/                        # 仅放可导入 Python package
│   └── expert_review/
│       ├── agents/
│       ├── graph/
│       ├── prompts/
│       ├── schemas/
│       ├── tools/
│       ├── compatibility/
│       ├── benchmark/          # NEW：从 3127 行的 benchmark.py 拆出
│       │   ├── __init__.py
│       │   ├── harness.py      # _rerun_subset / scope dispatch
│       │   ├── metrics.py      # ScoreAlign / RAS / SAS / CRAS / PDS / HAI / Calib
│       │   └── splits.py       # family-aware greedy split
│       ├── batch.py
│       ├── inventory.py
│       ├── llm_telemetry.py
│       └── ...
│
├── tests/                      # 所有测试集中
│   ├── test_review.py
│   ├── test_benchmark.py
│   └── test_batch.py
│
├── reproduction/               # 复现链（CLI + 配置 + 数据准备 + 实验）
│   ├── README.md
│   ├── cli/
│   │   ├── run_expert_review.py
│   │   └── align_ttool_expert_review.py
│   ├── config/
│   │   ├── config.py
│   │   └── tasks.py
│   ├── data_prep/              # build_* 类脚本
│   └── experiments/            # analyze_* / run_* / assemble_*
│
├── docs/                       # 所有静态文档
│   ├── api/                    # 自动生成的 pydoc / sphinx 入口
│   ├── designs/                # 移自 src/expert_review/designs/
│   ├── reports/                # REPRODUCTION_REPORT.md 等
│   └── process/                # PYDOC_INVENTORY.md / PYDOC_ITEMS.md / GUIDE.md
│
├── discussions/                # 不动（保持现状）
├── llm_as_judge_methods_corpus/ # 不动
└── state_machine_review_corpus/ # 不动
```

### 2.3 6 个决策点（D1-D6）

> 当前**全部锁定为暂定推荐**，重构正式启动前由用户回看 + 复核。

| 决策 | 问题 | 暂定推荐 |
|------|------|----------|
| **D1** | `src/` 顶层 4 个 .py 怎么办？ | **方案 C**：移到 `reproduction/cli/` + `reproduction/config/` |
| **D2** | `benchmark.py`（3127 行）怎么办？ | **拆分**为 `benchmark/{harness, metrics, splits}.py` |
| **D3** | `src/expert_review/designs/` 怎么办？ | **移到 `docs/designs/`** |
| **D4** | `README.md` + `GUIDE.md` 怎么办？ | **留在 `src/expert_review/`**（包级 README 是 Python 社区习惯） |
| **D5** | 是否引入 lint / format 工具链？ | **引入 ruff + black**，写到 pyproject.toml |
| **D6** | `experiments/` 怎么处置？ | **整体迁入 `reproduction/experiments/`** |

### 2.4 9-commit TDD 增量执行计划

| Commit | 改动 | 检查点 |
|--------|------|--------|
| C1 | 新建 `pyproject.toml` + 顶层 `tests/` + 测试迁移 | `pytest tests/` 全绿 |
| C2 | `src/` 顶层 4 个 .py 移到 `reproduction/cli/` + `reproduction/config/` | CLI 入口可执行 |
| C3 | `experiments/` → `reproduction/experiments/` | 一致性脚本可跑 |
| C4 | `src/expert_review/designs/` → `docs/designs/`；包级 .md 移到 `docs/process/` | 链接有效 |
| C5 | `benchmark.py` 拆分阶段 1：`benchmark/harness.py` | 测试绿 |
| C6 | `benchmark.py` 拆分阶段 2：`benchmark/metrics.py` | 测试绿 |
| C7 | `benchmark.py` 拆分阶段 3：`benchmark/splits.py` + `__init__.py` re-export | 测试绿 |
| C8 | 引入 ruff + black + 修可发现的格式问题 | lint pass |
| C9 | 同步 README / GUIDE / discussions 引用 | 链接全部有效 |

> **重要**：**重构不在本归档前执行**，仅作为下一次启动时的施工说明书保留。

---

## 3. 完整 Mermaid 流程图

> 反映 `src/expert_review/graph/runtime.py` 当前真实运行结构（W4.x 收口版本），含已删除的 arbiter 历史标记、Score Composer 的 6 维 rubric 调用、fan-out/fan-in 模式与 ReviewGraphState 共享容器。

### 3.1 顶层调用链

```mermaid
flowchart LR
    subgraph EXTERNAL["外部入口"]
        REQ["ExpertReviewRequest<br/>(prompt + input_text<br/>+ pred_output + ref_output<br/>+ metadata)"]
        AGENT["ExpertReviewAgent<br/>.review()"]
        RES["ExpertReviewResult<br/>(overall_score + dimensions<br/>+ harmful_issues<br/>+ confidence + notes<br/>+ llm_usage_summary)"]
    end

    subgraph PKG["expert_review package"]
        WORKFLOW["run_expert_review_workflow()<br/>graph/runtime.py"]
        STATE["ReviewGraphState<br/>(共享 mutable 容器)"]
    end

    REQ --> AGENT
    AGENT --> WORKFLOW
    WORKFLOW <--> STATE
    WORKFLOW --> RES
```

### 3.2 3-stage langgraph 详细流程

```mermaid
flowchart TB
    START([开始])

    subgraph STAGE1["PREPARATION 阶段"]
        CR["Contract Router<br/>解析 prompt → contract"]
        FANOUT1["fan-out: preparation_fanout"]
        IA["Input Analyst<br/>需求 + grounding 抽取"]
        PE["Prediction Extractor<br/>预测制品 lift"]
        RE["Reference Extractor<br/>参考制品 lift"]
        ERE["Evidence Regime Estimator<br/>protocol_only / record_level<br/>/ summary_only / mixed_evidence"]
        RPB["Review Policy Builder<br/>policy_packet + 6 维 weight"]
    end

    subgraph STAGE2["ANALYSIS 阶段"]
        FANOUT2["fan-out: analysis_fanout"]
        TRACE["Traceability Agent<br/>需求 → 预测 link"]
        EQ["Equivalence Agent<br/>预测/参考 语义对比<br/>(仅 has_reference 时启用)"]
        PQ["Pragmatic Quality Agent<br/>务实质量 + proportionality"]
        FANIN1["fan-in"]
        MEC["Missing-Evidence Critic<br/>evidence discipline + confidence cap"]
        ARBITER["[已删除]<br/>Disagreement Arbiter<br/>(W3 ablation: ΔHAI=+0.1556)"]
    end

    subgraph STAGE3["FINAL 阶段"]
        SC["Score Composer<br/>6 维评分 + mode blend<br/>(summary/protocol/component/record_level)"]
        SCRUB["6× LLM rubric refine<br/>(rubric_llm_enabled)"]
        FS["Final Synthesizer<br/>结果装配（无新发现）"]
    end

    START --> CR
    CR --> FANOUT1
    FANOUT1 --> IA & PE & RE
    IA & PE & RE --> ERE
    ERE --> RPB

    RPB --> FANOUT2
    FANOUT2 --> TRACE & EQ & PQ
    TRACE & EQ & PQ --> FANIN1
    FANIN1 --> MEC
    MEC -.-> ARBITER

    MEC --> SC
    SC --> SCRUB
    SCRUB --> SC
    SC --> FS
    FS --> END([返回 ExpertReviewResult])

    style ARBITER fill:#fdd,stroke:#c00,stroke-dasharray: 5 5,color:#900
    style SCRUB fill:#ffd,stroke:#aa0
    style STAGE1 fill:#eef
    style STAGE2 fill:#efe
    style STAGE3 fill:#fee
```

### 3.3 Score Composer 内部 mode 分发（issue I-15 关键）

```mermaid
flowchart TB
    SC_IN["6 维 deterministic score<br/>(syntax / completeness / behavior /<br/>traceability / clarity / evidence)"]
    LLM_GATE{"rubric_llm_enabled?<br/>+ regime in iter_c_regimes?"}

    LLM_REFINE["6 次 llm_rubric_score 调用<br/>(每维独立 + 共享 extra_signals)"]

    MODE_GATE{"contract.review_mode"}

    SUMMARY_MODE["summary_mode<br/>blend with summary_score_hint<br/>+ public-row 上限 cap"]
    PROTOCOL_MODE["protocol_mode<br/>cap confidence + 弱化 element-level"]
    COMPONENT_MODE["component_review_mode<br/>引入 CRAS 加权<br/>+ structured TP/FP/FN evidence"]
    RECORD_MODE["record_level<br/>full alignment + 强 evidence 强 cap"]

    BLEND["mode 内 blend + sanity bound 护栏<br/>+ asymmetric per-(regime, dim) 校准"]
    OUT["dimension_results +<br/>harmful_issues + overall_score +<br/>confidence"]

    SC_IN --> LLM_GATE
    LLM_GATE -->|是| LLM_REFINE
    LLM_GATE -->|否| MODE_GATE
    LLM_REFINE --> MODE_GATE

    MODE_GATE --> SUMMARY_MODE & PROTOCOL_MODE & COMPONENT_MODE & RECORD_MODE
    SUMMARY_MODE & PROTOCOL_MODE & COMPONENT_MODE & RECORD_MODE --> BLEND
    BLEND --> OUT

    style LLM_REFINE fill:#ffd,stroke:#aa0
    style BLEND fill:#fed
```

### 3.4 LLM 失败回退链（FallbackLLMClient）

```mermaid
flowchart LR
    AGENT_CALL["Agent 调用<br/>(rubric / extractor /<br/>analyst / critic 等)"]
    FALLBACK["FallbackLLMClient.invoke()"]
    PRIMARY["主 provider 调用"]
    SUCCESS{"返回成功 +<br/>解析有效?"}
    PASS["llm_usage_summary 记录<br/>(success + latency + tokens)"]
    COOLDOWN["进入 cooldown 窗口<br/>(provider drift 防护)"]
    NEXT["下一个 provider<br/>(provider_order)"]
    DET["fallback to deterministic<br/>(silent fallback caveat I-4)"]
    USAGE["effective_llm_used = false<br/>(若所有 provider 都 fallback)"]

    AGENT_CALL --> FALLBACK
    FALLBACK --> PRIMARY
    PRIMARY --> SUCCESS
    SUCCESS -->|是| PASS
    SUCCESS -->|否| COOLDOWN
    COOLDOWN --> NEXT
    NEXT -->|还有 provider| FALLBACK
    NEXT -->|全部失败| DET
    DET --> USAGE

    style DET fill:#fdd,stroke:#c00
    style USAGE fill:#fdd,stroke:#c00
```

### 3.5 数据流（每 stage 输入 / 输出 → ReviewGraphState 字段）

| Stage | Agent | 输入字段 | 输出 state 字段 |
|-------|-------|----------|-----------------|
| PREP | Contract Router | `request.prompt` | `state.contract` |
| PREP | Input Analyst | `request.input_text` + `prompt` | `state.input_dossier` |
| PREP | Prediction Extractor | `request.pred_output` | `state.pred_dossier` |
| PREP | Reference Extractor | `request.ref_output` | `state.ref_dossier` |
| PREP | Evidence Regime Estimator | prompt + 三 dossier | `state.regime` |
| PREP | Review Policy Builder | contract + regime + 三 dossier | `state.policy_packet` + `state.dimensions` |
| ANALYSIS | Traceability Agent | input + pred dossier | `state.trace_results` |
| ANALYSIS | Equivalence Agent | input + pred + ref dossier | `state.equivalence_report` |
| ANALYSIS | Pragmatic Quality Agent | contract + regime + policy + input + pred | `state.quality_report` |
| ANALYSIS | Missing-Evidence Critic | 上述全部 | `state.evidence_critic` |
| FINAL | Score Composer | dimensions + 全部 dossier/report | `state.dimension_results` + `state.harmful_issues` + `state.overall_score` + `state.confidence` |
| FINAL | Final Synthesizer | request + 全部 state | `state.result` |

---

## 4. 未来路线（导师讨论后的两条候选 + 共同基础）

> **基本立场**：本项目作为**长线工作**保留。下面两条路线**互不排斥**，可以独立推进，也可以在合适时机合流。具体走哪条由 `project_1` 进展与外部需求决定，本文件不强行二选一。

### 4.A 路线 A — LLM-as-feedback：融入 project_1 迭代式建模

#### 4.A.1 重新定位

与导师本次讨论后形成的第一个关键洞察：

> **原 `LLM-as-Judge` 子系统可以重新定位为 `LLM-as-feedback`，融入 `project_1` 的迭代式状态机建模闭环。**

这一重新定位的核心论点是：

1. **同一套 reviewer 系统**既可以作为**评估器**（学术稿 §3 当前定位），也可以作为**反馈源**（提供 per-dim 分数 + structured evidence + actionable items）；
2. **`project_1` 本身是迭代式建模**：LLM 生成 STM → 评估 → 修复 → 再生成 → ……；
3. 当前的 reviewer 输出**完全可以作为下一轮 prompt 的"建设性 critique" 部分**，从而把"被动评估"变成"主动 feedback signal"。

#### 4.A.2 可能的架构骨架

```mermaid
flowchart LR
    subgraph PROJ1["project_1 — 迭代式 STM 建模"]
        REQ_NL["NL 需求"]
        GEN["LLM Generator<br/>(STM 生成)"]
        STM_K["STM_k<br/>(第 k 轮制品)"]
        DECIDE{"质量门<br/>(dim 分数 +<br/>evidence completeness)"}
        FINAL_STM["定稿 STM"]
        REFINE["LLM Refiner<br/>(基于 feedback 重写)"]
    end

    subgraph PROJ_EX1["project_ex1 — feedback 源"]
        REVIEWER["Reviewer Pipeline<br/>(3-stage × 12 agents)"]
        FEEDBACK["Structured Feedback<br/>per-dim score + evidence +<br/>actionable items + sanity bound 提示"]
    end

    REQ_NL --> GEN
    GEN --> STM_K
    STM_K --> REVIEWER
    REVIEWER --> FEEDBACK
    FEEDBACK --> DECIDE
    DECIDE -->|未通过| REFINE
    REFINE --> GEN
    DECIDE -->|通过| FINAL_STM

    style PROJ_EX1 fill:#eef,stroke:#446
    style FEEDBACK fill:#ffe,stroke:#aa0
```

#### 4.A.3 与原方法叙事的差异

| 维度 | 原 `LLM-as-Judge` | 新 `LLM-as-feedback` |
|------|-------------------|----------------------|
| 主要用户 | 评估者 / 论文 reviewer | `project_1` Generator + Refiner |
| 输出格式 | 数字分数 + evidence + 报告 | 结构化 critique + 可消化的 actionable list |
| 评估对象 | 静态 STM | 迭代轮次中的"当前最佳版本" |
| 使用频次 | 一次性最终评估 | 每轮 STM 生成后调用 |
| 与论文写作绑定 | 直接作为 §Method | 作为 `project_1` 的子组件 + ablation 维度 |
| Anchored rubric 的角色 | 评分锚点 | feedback 模板 + 引导 refine 方向 |

#### 4.A.4 对当前 ex1 工作的可重用性盘点

| 资产 | feedback 路线下的用途 |
|------|----------------------|
| 6 维 anchored rubric | **直接复用**为 feedback 模板 |
| 3-stage runtime | **直接复用**为 feedback 生成管线 |
| Score Composer mode 分发 | **降级简化**：feedback 不需要复杂的 score blend，可主要走 `record_level` mode |
| 8 指标体系 | **简化**：保留 PDS / RAS / Stability 作为 feedback 质量自检；HAI / SAS / CRAS 不再是主指标 |
| Sanity bound | **保留**作为 feedback 的可信区间标注 |
| LLM-as-Judge 文献库 | **拓展**为 LLM-as-feedback / iterative refinement / self-critique 文献库 |
| benchmark harness | **改造**为 closed-loop benchmark：评估"经过 N 轮 feedback 后的 STM 质量提升" |
| 20 条不一致清单 | 大部分仍然有效，**优先级会随 feedback 角色变化**（如 I-15 mode shaping 优先级降低，I-1 evidence_discipline 优先级升高） |

#### 4.A.5 后续在 project_1 中重启时的入口

1. 保留本项目作为**长线资产仓库**（package + corpus + discussions），不强制 read-only
2. 在 `project_1` 中新建 `feedback/` 子模块，**通过 `import expert_review` 复用**而不是 fork
3. 在 `project_1` 的迭代式 prompt 模板中，把 reviewer 输出作为**第二段 system context**（"以下是上一轮模型的 review 结论，请优先针对 ××× 进行修复"）
4. 增加一个 closed-loop benchmark：`HAI 单点 vs HAI@3rd-iter vs HAI@5th-iter`，验证 feedback 是否真的带来收敛

---

### 4.B 路线 B — 强化学习场景下的奖励信号 / critic

#### 4.B.1 重新定位

与导师本次讨论后形成的第二个关键洞察：

> **本项目沉淀的 anchored rubric + sanity bound + 8 指标体系，可以作为强化学习场景下的奖励信号或 critic，用来训练 / 微调下一代 STM 生成器。**

这一定位与"路线 A（feedback）"的本质差别在于：

1. **路线 A** 把 reviewer 当作**外部反馈管道**，模型本身不变，靠 prompt 迭代收敛；
2. **路线 B** 把 reviewer 当作**奖励函数**，**模型本身被反向更新**（PPO / DPO / GRPO / RLVR / RLAIF 等任一 RL fine-tune 范式都可以接入）。

#### 4.B.2 可能的接入位置（按 RL 框架习惯命名）

| RL 组件 | 在本项目里对应什么 | 备注 |
|---------|--------------------|------|
| **Reward** | `Score Composer` 输出的 `overall_score`（或 8 指标加权） | 6 维 anchored rubric 是天然的 multi-objective reward 构造器 |
| **Critic** | 6 维 deterministic estimate + LLM rubric refinement | 已经具备 `score + sanity_bound` 双输出，可直接当 critic 头 |
| **Verifier (RLVR)** | `Missing-Evidence Critic` + `Equivalence Agent` 的 deterministic 部分 | 这部分**不依赖 LLM**，可作为 RL 训练时**稳定的 verifier 信号源** |
| **Preference label (DPO/RLAIF)** | `judgement_from_score` 的 4 档离散标签 + per-dim score | 可批量生成 winner / loser pair |
| **Reward shaping** | `mode-specific blend`（issue I-15）+ asymmetric sanity bound | 已经天然带"局部偏置 + 渐进收敛"的 shaping 结构 |
| **Off-policy 数据** | 现有 benchmark harness 的 `phase7 / phase14 / phase15` 三套 scope + state_machine_review_corpus | 可直接作为 RL 训练初期的 cold-start 样本池 |

#### 4.B.3 与路线 A 的耦合关系

两条路线**可以独立推进**，也**可以分阶段合流**：

```mermaid
flowchart LR
    EX1["project_ex1<br/>(当前长线资产)"]

    A["路线 A: feedback<br/>(prompt-level 闭环)"]
    B["路线 B: RL reward / critic<br/>(模型权重级闭环)"]

    HYBRID["路线 A+B 合流<br/>(用 reviewer 同时做 prompt feedback 与 reward,<br/>训练时收紧权重, 推理时收紧上下文)"]

    EX1 --> A
    EX1 --> B
    A -.可选合流.-> HYBRID
    B -.可选合流.-> HYBRID

    style EX1 fill:#eef,stroke:#446
    style HYBRID fill:#fed,stroke:#c80,stroke-dasharray: 5 5
```

#### 4.B.4 路线 B 落地前需要先解决的依赖

1. **I-7 noise floor 必须实现**：RL 场景下 reward 的方差控制远比 paper 评估关键
2. **I-1 evidence_discipline 必须修复**：否则 reward 在 self-prediction 模式下会 reward-hack
3. **新增 reward 单调性测试**：构造刻意降级的 STM，确认 reward 单调下降；这是 RL 训练前的 sanity test
4. **Score Composer 的 mode 分发简化**：RL 场景下推荐主要用 `record_level`，避免 mode 切换带来 reward 震荡（同时也降低 issue I-15 的影响）

---

### 4.C 两条路线的共同基础

无论走 A、B 还是合流，下面这些**当前已经稳定**的资产都可以**直接复用**：

1. 6 维 anchored rubric（[src/expert_review/agents/rubric_scorer.py](../src/expert_review/agents/rubric_scorer.py)）
2. 3-stage runtime（[src/expert_review/graph/runtime.py](../src/expert_review/graph/runtime.py)）
3. Sanity bound 机制（[src/expert_review/agents/score_composer.py](../src/expert_review/agents/score_composer.py)）
4. 8 指标体系（[src/expert_review/benchmark.py](../src/expert_review/benchmark.py)）
5. state_machine_review_corpus（评估材料）
6. llm_as_judge_methods_corpus（14 篇文献，可拓展为 RL feedback / critic 文献）
7. 学术定位主稿 v4.3（方法叙事骨架）
8. I-1 ~ I-20 不一致清单（决定哪些 issue 在新路线下优先级会变化）

---

## 5. 暂停投入与资产保留计划

### 5.1 暂停投入的范围

本项目以 `dev/project_ex1_split` 分支为最后一次正式投入，合入 `main` 后**暂停新功能开发**，但**全部资产保留为长线资产**：

1. **代码**：维持 W4.x 收口版本（pydoc 100%、死代码已清、3-stage runtime 稳定），**不删、不下沉**
2. **文档**：维持当前 README / GUIDE / 设计文档 / 学术定位主稿 / 不一致清单 / 本暂停说明
3. **数据**：state_machine_review_corpus（评估材料）+ llm_as_judge_methods_corpus（14 篇文献库）**不动**
4. **实验产出 / 结论**：所有阶段产出的指标对比、ablation 结果、benchmark scope（`phase7 / phase14 / phase15`）**完整保留**
5. **重构**：**不执行**（仅以本文件 §2 的形式留下施工说明书）
6. **路线 B（RL）相关探索**：**不启动**（仅以本文件 §4.B 形式记录可能的接入位置）

> **明确不做的事**：不删任何代码、不删任何 corpus、不删任何 discussion、不把 ex1 整个目录移到 archive/，也不在仓库结构上做任何"下沉"操作 —— 整个项目目录维持现状，作为可随时重新激活的资产。

### 5.2 暂停投入的执行方式

1. 提交本讨论文件（含本次"长线 + RL"完善）
2. 推送到远端 `dev/project_ex1_split`
3. 在 PR 评论中贴出**总结性 + 盘点性质**的 comment（草稿见 §5.3）
4. PR 合入 `main`
5. 本地 `git checkout main` 并同步远端最新
6. 后续工作切换到 `project_1`

### 5.3 PR 评论草稿（总结 + 盘点）

> **建议在 PR 上贴的中文说明（用户审定后发布）：**

```markdown
## 📌 PR 性质

本 PR 是 `project_ex1_llm_judge_for_stm` 的 **W4.x 收口 + 长线暂停投入** PR。

合入后**本子系统作为长线工作保留**，不再短期投入新功能；后续可能以
**LLM-as-feedback**（融入 project_1 迭代闭环）或 **RL 奖励信号 / critic**
（用于训练下一代 STM 生成器）形态重新激活。

详见 `project_ex1_llm_judge_for_stm/discussions/2026-05-09-15-19-23-AI-讨论-项目归档与重构规划与LLM-as-feedback路线.md`。

---

## ✅ 已完成（W4.x 阶段）

### 工程层面

- [x] 中文 RST pydoc 四级覆盖率 100%（module / class / function / method 共 **419 zh + 15 en items**）
- [x] `legacy/` 目录整体删除（外部 0 引用）+ `Disagreement Arbiter` 字符串残留清理
- [x] README + GUIDE 与代码状态对齐，Phase 7 ~ Phase 15 阶段口径全部冻结
- [x] 42/42 unit tests + 全量 doctest 通过（TDD 增量推进，每步 commit 都验证）
- [x] 3-stage runtime 稳定（PREPARATION / ANALYSIS / FINAL × 12 agents，已删除 1 个 dead arbiter）
- [x] benchmark harness 稳定（`scope=phase7 / phase14 / phase15` 三套对比面）

### 方法学层面

- [x] 6 维 anchored rubric + 5+1 双轨聚合
- [x] 3 道晋升门（Q1 双轨 / Q2 evidence consistency / Q3 multi-rep stability）
- [x] Sanity bound 机制（per-dim + per-(regime, dim) 非对称）
- [x] PDS / HAI / RAS / SAS / CRAS / normalized_mae / Calib / Stability 八指标体系闭环

### 文档与材料层面

- [x] 学术定位主稿 v4.3（含 3 张 mermaid + 28 条参考文献）
- [x] LLM-as-Judge 文献库 14 篇（7 通用 + 7 SE 相关）+ STM 评估材料库
- [x] I-1 ~ I-20 不一致清单 + 代码事实档案（II-A ~ II-L）
- [x] 长线暂停说明（本 PR 引入）+ 完整 mermaid（顶层调用链 + 3-stage langgraph + Score Composer mode 分发 + Fallback 链 + 数据流字段映射）

---

## ⏸ 故意未做（已规划但暂不执行）

- [ ] **20 条 prompt-implementation 不一致 issue 修复**（其中 P0 三条致命：I-1 evidence_discipline 错配 / I-7 noise floor 未实现 / I-12 Operability proxy 未实现）
- [ ] **6 大目录散乱的物理重构**（9-commit TDD 增量执行计划已规划，见暂停说明 §2）
- [ ] **`benchmark.py`（3127 行）拆分**为 `benchmark/{harness, metrics, splits}.py`
- [ ] **强化学习路线 B 的任何探索**（仅记录可能接入位置）

---

## 📊 资产保留清单（长线资产，不删不动）

| 类型 | 路径 | 说明 |
|------|------|------|
| 可导入 package | `src/expert_review/` | 64 个 .py，pydoc 100% |
| 单元测试 | `src/expert_review/test_{review,benchmark,batch}.py` | 42 cases |
| CLI / 实验脚本 | `src/{run,align}_*.py` + `experiments/` | 33 个 experiment 脚本完整保留 |
| 学术 corpus | `llm_as_judge_methods_corpus/` | 14 篇 paper.pdf + DESC.md |
| 评估 corpus | `state_machine_review_corpus/` | STM 评估材料 |
| Discussions | `discussions/` | 学术稿 v4.3 + 不一致清单 + 暂停说明 三份 |
| 设计文档 | `src/expert_review/designs/` | v0/v1 + V1_ALIGNMENT_REPORT |

---

## 🔮 未来重新激活的两条候选路线

1. **路线 A — LLM-as-feedback**：把 reviewer 输出作为 `project_1` 迭代建模的反馈信号，关闭"生成 → 评估 → 修复"闭环
2. **路线 B — RL 奖励 / critic**：把 6 维 anchored rubric + sanity bound + 8 指标作为 RL fine-tune 阶段的 reward / critic / verifier，反向更新模型权重

两条路线**互不排斥、可独立推进、可阶段合流**。具体走哪条由 `project_1` 进展与外部需求决定。

---

## 🛣 后续接力点

- **重启 ex1 / 重新进入重构**：先看暂停说明 §1.2（待办分级）+ §2（重构 9-commit 计划）
- **在 `project_1` 中作为 feedback 复用**：先看暂停说明 §4.A + `src/expert_review/__init__.py` 暴露的对外 API
- **走 RL 路线**：先看暂停说明 §4.B 的接入位置表 + 4.B.4 的依赖清单（I-7 / I-1 必须先修）

---

## ✋ 当前进度

- 当前 W4.x 工作完整结束
- 此 PR 合入后本地 checkout 回 `main`，**优先工作切换到 `project_1`**
```

---

## 6. 接力点（下次重新激活时优先看这里）

> 不论是直接重启 ex1 自身、从 `project_1` 那侧反向复用、还是走 RL 路线，下面是**最快进入状态**的阅读路径。

### 6.1 直接重启 ex1（继续做评估子系统 / 修 P0 issue / 执行重构）

1. 先看本文件 §1.2（待办）+ §2（重构规划）
2. 再看 [I-1 ~ I-20 清单](./2026-05-09-12-58-25-AI-讨论-prompt实现一致性待处理清单.md) 的 P0 部分
3. 再看 [学术定位主稿 v4.3](./2026-05-08-19-20-31-AI-讨论-project_ex1学术定位与相关工作综述.md) §10 决策点
4. 最后看 [src/expert_review/README.md](../src/expert_review/README.md) + [GUIDE.md](../src/expert_review/GUIDE.md)

### 6.2 在 project_1 中作为 feedback 复用（路线 A）

1. 先看本文件 §4.A
2. 再看 [src/expert_review/__init__.py](../src/expert_review/__init__.py) 暴露的对外 API：
   - `ExpertReviewRequest` / `ExpertReviewResult` / `review_artifacts()` / `review_model()`
3. 再看 [src/expert_review/graph/runtime.py](../src/expert_review/graph/runtime.py) 的 `run_expert_review_workflow()` 与 §3.2 的 mermaid
4. 再看 `state_machine_review_corpus/` 里的 STM 评估材料（可作为初始 fixture）

### 6.3 在 RL 场景下作为 reward / critic 使用（路线 B）

1. 先看本文件 §4.B 全节
2. 再看 [src/expert_review/agents/score_composer.py](../src/expert_review/agents/score_composer.py) 的 6 维 score + sanity bound 输出结构
3. 再看 [src/expert_review/agents/missing_evidence_critic.py](../src/expert_review/agents/missing_evidence_critic.py) 与 [src/expert_review/agents/equivalence.py](../src/expert_review/agents/equivalence.py) 的 deterministic 部分（作为 RLVR verifier 候选）
4. 再看 [I-1 ~ I-20 清单](./2026-05-09-12-58-25-AI-讨论-prompt实现一致性待处理清单.md) 的 I-1 / I-7 / I-12（RL 路线启动前必须先修）
5. 最后看 [src/expert_review/benchmark.py](../src/expert_review/benchmark.py) 的 `phase14 / phase15` scope（作为 RL 训练初期 cold-start 数据池）

### 6.3 关键数据 / 文件索引

| 类型 | 路径 |
|------|------|
| 主入口 | [src/expert_review/agent.py](../src/expert_review/agent.py) |
| 主 runtime | [src/expert_review/graph/runtime.py](../src/expert_review/graph/runtime.py) |
| Score Composer | [src/expert_review/agents/score_composer.py](../src/expert_review/agents/score_composer.py) |
| benchmark | [src/expert_review/benchmark.py](../src/expert_review/benchmark.py) |
| schema | [src/expert_review/schema.py](../src/expert_review/schema.py) |
| 单元测试 | [src/expert_review/test_review.py](../src/expert_review/test_review.py)（39 KB）+ test_benchmark.py + test_batch.py |
| 学术稿 v4.3 | [discussions/2026-05-08-19-20-31-...综述.md](./2026-05-08-19-20-31-AI-讨论-project_ex1学术定位与相关工作综述.md) |
| 不一致清单 v2 | [discussions/2026-05-09-12-58-25-...清单.md](./2026-05-09-12-58-25-AI-讨论-prompt实现一致性待处理清单.md) |
| 本文件 | discussions/2026-05-09-15-19-23-...路线.md |

---

## 7. 备注与结束语

1. 本项目作为**独立 LLM-as-Judge 子系统**的当前形态在此**暂停投入**，但**作为长线工作保留**：代码 / 数据 / 实验结论 / 文献库 / 文档全部维持现状，不删不动
2. 6 维 anchored rubric + 3-stage runtime + sanity bound + 8 指标体系**已被验证可工作**，可以以以下任一形态进入下一阶段：
   - 作为 `project_1` 的 feedback 源（路线 A）
   - 作为 RL fine-tune 的 reward / critic / verifier（路线 B）
   - 作为独立 paper 投稿的方法学骨架（修完 P0 三条后启动）
3. 未完成的工程清理（重构 / I-1 ~ I-20）**不阻塞 project_1 的复用** —— 因为这些 issue 主要影响"作为独立 paper 提交"时的方法叙事一致性；**作为 feedback 源时大部分 issue 优先级会下降**；**作为 RL reward 时 I-1 / I-7 反而会上升为必须先修**
4. 后续 paper 若要发表 ex1 单独工作，建议先解决 P0 的 3 条（I-1 / I-7 / I-12），P1 的剩余 issue 可以按"已知局限"在 §Limitations 中诚实记录
5. **当前优先级**：暂停投入 → 合入 `main` → 切回 `project_1` 推进迭代式 STM 建模 → 如 `project_1` 进展需要 reviewer 反馈 / 训练信号，再回头按本文件 §4.A 或 §4.B 重新激活

