# 资源与复现实验资产 / ASSETS

更新时间：2026-06-10 13:08:00

状态口径：🟢 可直接访问；🟡 部分公开 / 可重建但不完整；🟠 未公开 / 仅论文内描述；🔒 受限私有资产 / 难以公开获取；❓ 入口存在但当前访问异常或未完成逐文件核验。

CCF 口径：🏆 CCF A；🥈 CCF B；🥉 CCF C；⚪ 非 CCF 推荐或不适用；❓ 未核验。

## 1. 资源总览

| 资源类型 | 状态 | URL / 路径 | 说明 |
|---|---|---|---|
| 论文 | 🟢 | [ACM DOI](https://dl.acm.org/doi/10.1145/3755881.3755926) / [本地 PDF](./paper.pdf) | ACM 论文页公开；本地已提取 `paper_content.txt`。 |
| 实验代码 | 🟠 | 未发现公开仓库 | 论文公开数据集，但未提供生成/修复 pipeline 源码。 |
| 实验结果细则 | 🟢 | [Google Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link) / [本地 human-review parquet](../../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/llms_emp_human_review.parquet) | Drive 文件夹入口可访问，但逐文件下载未在本轮重新逐一审计；本仓库已冻结公开 workbook 为 192 行 human-review parquet，SHA-256 `7b54b06ead32e0a5b6c6d4f2244d11a8e2439c64ad421f01a1b8a9175f16a427`。 |
| 数据集 / Benchmark | 🟢 | [Google Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link) / [complete samples parquet](../../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/llms_emp_complete_samples.parquet) / [raw samples parquet](../../discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/llms_emp_raw_samples.parquet) | 107 个 SysML 行为模型，含 36 activity、36 state machine、35 sequence diagrams；本地冻结 raw samples 107 行 SHA-256 `69e5123174f976bf7504eaa334e0670da22b2e0c67329c57539b3866dfe5b045`，complete samples 98 行 SHA-256 `d8c0dca59c650149c7c16e433fc54440fc72509c82d57676ca6238f2182fdf2e`。 |
| Artifact / 复现包 | 🟡 | [review_extraction](../../../project_ex1_llm_judge_for_stm/state_machine_review_corpus/llms_emp/review_extraction.md) | 数据和结果细则可用，代码不可用；本仓库已建立 reviewer 数据抽取与 parquet 化记录。 |

## 2. Venue 与 CCF

- **论文**：Generating SysML Behavior Models via Large Language Models: an Empirical Study
- **发表 / 版本**：Internetware 2025, ACM
- **CCF 口径**：🥉
- **论文入口**：[ACM DOI](https://dl.acm.org/doi/10.1145/3755881.3755926)

## 3. 实验代码核查

没有公开生成脚本或模型调用脚本。复现实验需要自行实现 prompt template、RAG、PlantUML/SysML 检查和 feedback regeneration。

## 4. 数据集 / Benchmark 核查

这是 9 篇五绿 direct baseline 中数据资产最强的一篇：公开 Drive 入口 + 本地 parquet 冻结，包含需求、PlantUML 行为模型、模型类别和基础结构统计。需注意本轮只能确认 Drive 文件夹入口可达，逐文件下载状态以本地冻结 parquet 为准。

## 5. 实验结果细则核查

公开 workbook 已在本仓库转换为 `llms_emp_human_review.parquet`、`llms_emp_complete_samples.parquet` 与 `llms_emp_raw_samples.parquet`，包含逐样本 STM/ACT/SD 结果、LLM 名、生成输出、人类评分和多维 hallucination 细节。公开的是数据与结果表，未发现公开生成 / 修复 pipeline 源码。

## 6. 对 Project 1 对比实验的可用性

优先作为 Project 1 对比实验数据源和 LLM-as-Judge 校准材料。可直接抽取 STM 子集，构造 `NL -> PlantUML/SysML STM` baseline 数据。

## 7. 风险与待复查

1. Google Drive 结构和权限可能漂移；正式实验应优先使用本地冻结 parquet，并记录来源日期、行数和 SHA-256。
2. 公开的是数据和结果表，不是完整代码。
3. CCF 🥉 按 CCF 推荐目录口径；官方网页可能受 WAF 影响，必要时用浏览器人工复核。
