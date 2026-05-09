# project_ex1_llm_judge_for_stm

> **计划外的 LLM-as-Judge 子系统**，从 [project_1](../project_1_llm_state_machine_modeling/) 拆出的独立项目，专注**针对状态机制品（State Machine artifacts）的 LLM-as-Judge 评审方法学**。
>
> `ex1` = "extra-1"，PhD 原计划没有，是实际工作中分化出来的独立子系统。
>
> **研究方向**：Software Engineering（SE）方向；目标产物为**方法学论文**（methodology paper）。详见 [discussions/2026-05-08-19-39-19-AI-讨论-SE视角下methodology-paper定位与LLM-as-Judge方法学详细综述.md](./discussions/2026-05-08-19-39-19-AI-讨论-SE视角下methodology-paper定位与LLM-as-Judge方法学详细综述.md) §0–§1。

## 一、项目定位

### 1.1 这个项目是什么

把"LLM 当审稿人评判 STM 制品质量"作为**一个独立研究问题**来对待，包括：

- **评审系统本身**（reviewer agent，rubric scoring，evidence locator，judgement derivation 等）
- **评审方法学**（LLM-as-Judge 在受限输出空间下的可靠性、calibration、self-consistency 设计、provider drift 影响）
- **基准构建**（从已发表论文的 human review 抽取作为 ground truth）
- **eval pipeline**（HAI/RAS/SAS/CRAS/PDS 等指标 + acceptance gates）

### 1.2 这个项目不是什么

- **不是 STM 生成方法本身**——那是 [project_1](../project_1_llm_state_machine_modeling/) 的 baselines/ 在管的 62 篇基线论文
- **不是 verification scenario generation**——那是 project_2
- **不是 model checking / repair**——那是 project_3 / project_4
- **不是 PhD 提案原计划研究内容**——是 review-quality 工作过程中分化出来的独立工程+方法学子系统

### 1.3 为什么拆出来独立

来自上游 [research_ideas#6](https://github.com/HansBug/research_ideas/pull/6) 的复盘结论：

1. **代码体量已过研究 sub-system 阈值**：`src/expert_review/` 3000+ 行核心库，多 agent 子模块（rubric_scorer / score_composer / final_synthesizer / fallback_llm 等）
2. **数据资产独立**：`state_machine_review_corpus/` 6 篇 LLM-as-Judge 相关文献文库 + ETL + benchmark + W0-W3 实验数据
3. **方法学独立**：[研究 PR #6 §16 final audit](https://github.com/HansBug/research_ideas/pull/6#issuecomment-4397759209) 揭示 LLM-as-Judge 在 provider drift 环境下的可复现性问题，这是独立于 STM modeling 的科学议题，**有可能成为独立论文方向**
4. **不解耦会牵一发动全身**：在 project_1 内迭代时每一次 reviewer 改动都要影响 project_1 的 baseline 评估口径

## 二、目录结构

```
project_ex1_llm_judge_for_stm/
├── README.md                    (本文件)
├── discussions/                 (学术讨论纪要：定位 / related work / 决策点)
│   ├── 2026-05-08-19-20-31-AI-讨论-project_ex1学术定位与相关工作综述_v1.md
│   └── 2026-05-08-19-39-19-AI-讨论-SE视角下methodology-paper定位与LLM-as-Judge方法学详细综述.md
├── experiments/                 (⚙️ 实验脚手架，原 state_machine_review_corpus/etl/，已迁出)
│   ├── run_ablation_config.py
│   ├── run_self_consistency_config.py
│   ├── analyze_default_verify_v4.py
│   ├── analyze_noise_floor.py
│   └── ...
├── llm_as_judge_methods_corpus/ (📚 LLM-as-Judge 方法学文献库，新建)
│   ├── README.md / SUMMARY.md / GUIDE.md / DESC_GUIDE.md
│   ├── g-eval/                  (G-Eval, Liu23 EMNLP)
│   ├── mt-bench/                (MT-Bench, Zheng23 NeurIPS)
│   ├── self-consistency/        (Self-Consistency, Wang23 ICLR)
│   ├── constitutional-ai/       (Constitutional AI, Bai22)
│   ├── tian-verbalized-confidence/ (Verbalized Confidence, Tian23 EMNLP)
│   ├── prometheus/              (Prometheus, Kim24 ICLR)
│   └── judgelm/                 (JudgeLM, Zhu23 arXiv)
├── src/                         (我们的正经代码，非"复现"包装)
│   ├── expert_review/           (核心 reviewer 库)
│   │   ├── agent.py             (ExpertReviewAgent 入口)
│   │   ├── benchmark.py         (eval pipeline + 各 metric 计算)
│   │   ├── fallback_llm.py      (FallbackLLMClient + chain logic)
│   │   ├── utils.py             (PROVIDER_CONFIGS / DEFAULT_PROVIDER_ORDER)
│   │   ├── agents/              (rubric_scorer / score_composer / final_synthesizer ...)
│   │   ├── prompts/             (rubric_dim_score with V1/V2/V3 paraphrase variants)
│   │   ├── designs/             (架构设计 / 历次 phase TODO)
│   │   ├── policy/              (deterministic post-transform policy)
│   │   ├── quality/             (review quality 度量)
│   │   ├── rubric/              (rubric 定义)
│   │   ├── schema/              (ExpertReviewRequest / ExpertReviewResult / DimensionResult 等)
│   │   ├── trace/               (trace 抽取)
│   │   └── ...
│   ├── run_expert_review.py     (single-shot CLI 入口)
│   ├── align_ttool_expert_review.py  (对齐 TTool-AI 输出做评分)
│   ├── tasks.py / config.py     (task 定义 + 配置)
│   └── REPRODUCTION_REPORT.md   (历史复现报告)
└── state_machine_review_corpus/ (📚 STM artifact 数据集 + benchmark；原 etl/ 已迁至 experiments/)
    ├── README.md / SUMMARY.md / GUIDE.md / REVIEW_GUIDE.md
    ├── hermes/ llms_emp/ psmbench/ rfcnlp/ ttool-ai/
    ├── structure-and-event-driven-frameworks-...
    └── out/                     (gitignored，eval reports + checkpoints + charts)
```

## 三、当前状态（继承自 PR #6 审计）

### 3.1 仍可信的结论

- **review-quality 7 维度框架**（A 覆盖 / B 准确 / C 具体 / D 证据 / E 校准 / F 可操作 / G 一致性）
- **架构判断**：reviewer 当前是 deterministic post-transform 主导，LLM 在 sanity bound 内做边缘修饰
- **iter_b 在 record regime 上有真实 calibration-vs-accuracy trade-off**（calib +5.7pp，但 ScoreAlign −4.5pp）
- **SC parallel pipeline ≡ standard pipeline**（除 score-derived judgement 外）
- **W2 confidence formula bug 已修复**（`clip(1-α·max_dim_std, 0.10, 0.99)` 与 benchmark.py 内 conf-阈值启发式不兼容）

### 3.2 已被推翻 / 不再可信

- 跨 milestone 的**绝对 HAI 数值**（W0 85.02 / W1 78.51 / W1.5 81.76 / W2 83.55）—— 全部不在同一 LLM 端条件下采集
- "+1.25 HAI / +1.85 HAI 改进"等叙事 —— 大都在 noise 内
- "通过 4/7 acceptance gates"类 single-shot gate-pass 计数

详见 [PR #6 §16 final audit](https://github.com/HansBug/research_ideas/pull/6#issuecomment-4397759209)。

### 3.3 Provider chain 现状

5 个 provider 已实现 fallback 链路（`src/expert_review/fallback_llm.py`）：

| 优先级 | provider | 状态 | 备注 |
|:-:|---|---|---|
| 1 | airouter | 🟡 当前环境 langchain stack hang | 历史 W0/W1/W1.5 主要使用 |
| 2 | deepghs | ✅ 健康 | 快速副选 |
| 3 | findcg | 🟡 余额不足 | 暂不可用 |
| 4 | miaocg | ✅ 健康 | W3 noise 实验主用 chain，**50 concurrent 容量** |
| 5 | api68886868 | 🔴 SSE 格式异常 | 不应使用 |

W3 noise 实验在 miaocg-first chain 下完成。

## 四、如何继续工作（暂时建议，待 EVAL_PROTOCOL 写定后正式确认）

### 4.1 在重启实验之前必做

1. **写定 `EVAL_PROTOCOL.md`**：
   - 锁定一条 canonical provider chain（建议 miaocg-first 因为稳定 + 50 concurrent）
   - 规定每个数值必须四元组 `(mean, σ, n_reps, provider+commit)`，禁单 single-shot
   - 改进 claim 必须 ≥ 3σ 才算真改进
   - lever 改 PR 必须配 baseline before/after 各 5 reps 对照
2. **noise floor 数据持久化**：把 W3 noise 实验的 `(provider, σ_metric)` 表单作为常驻数据，每个新实验对照它做显著性判定

### 4.2 暂不做的事

- **不要再发布 single-shot HAI 数字**作为 PR comment 主结论
- **不要在没固定 chain 的情况下发改进 claim**
- **不要继续在 PR #6 上 patch**（已 archive）

## 五、历史档案 + 引用

- **PR #6 archive**（W0-W3 全程）：[research_ideas#6](https://github.com/HansBug/research_ideas/pull/6)
  - **最终审计**：[#issuecomment-4397759209 §16](https://github.com/HansBug/research_ideas/pull/6#issuecomment-4397759209)
  - **W3 noise floor 数据**：见 PR #6 §13 + W3 实测分布
  - **W2 confidence bug 自查**：[issuecomment-4396913248](https://github.com/HansBug/research_ideas/pull/6#issuecomment-4396913248)

## 六、与 project_1 的边界

- **project_1**：研究 LLM 如何**生成**状态机；包含 baselines/（62 篇 STM-generation 论文文库）
- **project_ex1（本项目）**：研究 LLM 如何**评判**状态机；包含 state_machine_review_corpus/（6 篇 LLM-as-Judge 相关文献 + benchmark）

数据交叉点（保留为外部引用，不做 duplicate）：
- `project_1.../discussions/.../baseline_double_green_human_review_records.parquet` —— project_1 维护，本项目作为 benchmark 之一引用

## 七、关于命名

- `ex1` = extra-1 / unplanned-1 / 计划外的第 1 个项目
- `llm_judge` = LLM-as-Judge 的论文术语（Zheng et al., NeurIPS 2023）
- `for_stm` = 锁定对象：state machine artifacts

完整名意思即"针对状态机制品的 LLM-as-Judge 子系统"。
