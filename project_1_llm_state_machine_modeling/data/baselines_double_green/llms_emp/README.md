# `llms_emp/` — Generating SysML Behavior Models via LLMs (2025)

## 论文与上游引用

- **论文**：Wang et al., *Generating SysML Behavior Models via Large Language Models: an Empirical Study*, **Internetware 2025**, pp. 366-377. DOI: [10.1145/3755881.3755926](https://dl.acm.org/doi/10.1145/3755881.3755926)
- **baselines 单篇分析**：[`../../../baselines/llms_emp/`](../../../baselines/llms_emp/)
- **数据集公开入口**：[Google Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link)
- **可获取性**：🟢（直接公开）

## 任务

NL 需求 → PlantUML SysML 行为模型（STM / ACT / SD 三类）。

## 文件清单

| 文件 | 行数 | 列数 | 内容 |
|------|------|------|------|
| [`raw_samples.parquet`](./raw_samples.parquet) | 107 | 32 | 公开账本原始 107 行（含未筛选样本） |
| [`complete_samples.parquet`](./complete_samples.parquet) | 98 | 32 | 完整实验样本（同时含 input + output：38 STM / 21 ACT / 39 SD） |
| [`human_review.parquet`](./human_review.parquet) | 192 | 31 | 公开逐样本人评（input + ref + pred + 评分 + 论文摘录） |
| [`raw/`](./raw/) | — | — | 原始 ods/xlsx 等下载资源（**当前为空**，详见下文 §`原始资源现状`） |

## 关键字段

`complete_samples.parquet` 包含：

- `requirements_description`（输入 NL）
- `plantuml_code`（输出 PlantUML 代码）
- `diagram_type`（`stm` / `act` / `sd`）
- `output_metamodel`
- `basic_state_count` / `basic_transition_count` / `basic_hierarchical_state_count`（结构计数，用于切片）

`human_review.parquet` 包含：

- `input_text` / `ref_output_text` / `pred_output_text` 三元组
- `human_review_score` + `human_review_score_unit` + `human_review_summary`
- `paper_method_verbatim_excerpt`（论文原文评审协议摘录）

## 真实样本（一条）

火车基础制动装置 STM（5 状态 7 迁移）：

```
INPUT (requirements_description):
  This state machine model represents the train's basic braking device, which
  serves as the final execution unit for train braking operations. When the basic
  braking device receives a brake signal, it transitions from the initial state
  to the braking state. ...

OUTPUT (plantuml_code):
  @startuml
  [*] --> Initial_State
  Initial_State --> Braking_State : Signal_sent_successfully
  Initial_State --> Running_State : Signal_sending_failed
  Braking_State --> Brake_Caliper_Closed_State
  ...
  @enduml
```

## 原始资源现状（⚠️ P0 待补）

build 脚本 [`build_baseline_double_green_parquets.py`](../../../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/build_baseline_double_green_parquets.py) 当时把原始资源放在硬编码的 `/tmp/baseline_double_green/raw/llms_emp_gmodel/`，包含：

- `Dataset.xlsx` —— 数据集主账本（NL 需求 + PlantUML 输出）
- `Experiment Results.xlsx` —— 人工评审表

**当前 `/tmp` 已失效**，原始 xlsx 已不在本机。**当前 parquet 即真源**，下游无影响；但若要重新跑 build 脚本（修复 bug / 扩字段），需要先从 [Google Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link) 重新下载到 [`raw/`](./raw/)。

## 复用性建议

- ✅ **最适合做主样本级 NL→STM benchmark**：唯一一个 input/ref/pred/score 都齐的数据集
- ✅ 192 行人评直接可用于训练 / 评测 reviewer / LLM-as-judge
- ⚠️ PlantUML 元模型偏 SysML v1.6，跟时间自动机有 gap，需要做格式转换
- ⚠️ 缺时间约束语义（`after`/`every` 等都没编入）
