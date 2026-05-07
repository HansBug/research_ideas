# `hermes` review extraction

## 1. 论文元信息

- **标题**：Hermes: Unlocking Security Analysis of Cellular Network Protocols by Synthesizing Finite State Machines from Natural Language Specifications
- **作者**：Abdullah Al-Ishtiaq, Sangmin Tu, Syed Rafiul Khandker, Mirza Masfiqur Rahman Akon, Syed Rafiul Hussain
- **年份 / Venue**：USENIX Security 2024
- **DOI / arXiv / URL**：[USENIX 24 page](https://www.usenix.org/conference/usenixsecurity24/presentation/al-ishtiaq) / [arXiv:2310.04381](https://arxiv.org/abs/2310.04381)
- **本篇 review 数据用途**：提供 4G NAS / 5G NAS / 5G RRC 三大 cellular 规范的专家手工标注 + ground-truth FSM，约 16,000 数据点；可作为 reviewer 系统的 cellular-domain 评估材料。

## 2. review 数据获取方式

- **来源类型**：☑ 公开仓库（GitHub）
- **入口 URL**：[github.com/SyNSec-den](https://github.com/SyNSec-den)（论文 line 176 明确给出此 anchor，具体 repo 名按主页找）
- **本地落盘路径**：`state_machine_review_corpus/hermes/`（仅 paper.pdf / paper_content.txt / bibtex.bib；review 标注数据需从 GitHub 二次拉取）
- **当前可访问性**：☑ 论文文字声称"will be available at https://github.com/SyNSec-den/"；GitHub org 主页可访问，具体 Hermes repo 待 clone 验证
- **首次访问时间戳**：`2026-05-06 14:44`

## 3. reviewer 资质与人数

- **reviewer 总人数**：**4 cellular systems researchers + 2 domain experts**（论文 line 954-955 明确）
- **资质**：🟢 cellular systems researchers（4 人，主标注） + 🟢 domain experts（2 人，verification）
- **是否独立**：☑ 是（标注 + 验证两阶段，由不同人完成）
- **是否报告 inter-rater agreement**：⚪ 论文未显式报告 Cohen κ；但有"verified by two domain experts"的 cross-verify 流程
- **annotation 工作量**：~2,800 person-hours

## 4. review 数据 schema

### 4.1 单条 review 的字段

按论文 Section 4.1 "Grammar and Annotated Dataset" + Figure 4：

| 字段 | 类型 | 取值范围 | 备注 |
|---|---|---|---|
| `specification` | string | 4G-NAS Release17 / 5G-NAS Release17 / 5G-RRC Release17 | 三大 cellular 规范 |
| `paragraph` / `sentence` | string | NL 段落 | 输入 NL 单元 |
| `annotation` | structured | 按论文 Figure 4 定义的 grammar tags | TCNL 文法标注（state / transition / condition / action） |
| `logical_form` | structured | 论文 Section 4.2 定义 | 中间逻辑形式 |
| `gold_FSM` | M_Gold (FSM) | 完整状态机 | manually constructed by prior works (line 1037) |

### 4.2 数据规模

- 三个完整规范文档：4G-NAS / 5G-NAS / 5G-RRC（Release 17）
- 标注 datapoints：~16,000
- 工作量：2,800 person-hours
- artifact 类型：paragraph-level grammar annotation + 完整 ground-truth Gold FSM

### 4.3 评分聚合方式

- 论文不是 review-on-LLM-output 模式；论文是 **manually annotated ground truth + LLM 输出与 ground truth 比较**（87.21% 准确率）
- ground truth FSM 公开（论文 line 176）
- benchmark 评估方式：transitions Jaccard / state F1 / overall accuracy

## 5. 对齐到 reviewer 统一 schema

| 本篇字段 | reviewer 系统统一字段 | 映射方式 |
|---|---|---|
| specification | `paper_slug` / `case_id` | hermes:::4g_nas / hermes:::5g_nas / hermes:::5g_rrc |
| paragraph | `input_text` | NL 段落 |
| annotation (grammar tags) | `human_review_details_json` | 序列化为 JSON 保留 |
| gold_FSM | `ref_output_text` | FSM 序列化（PlantUML / 自定义文本格式） |
| transition / state F1 | `human_review_score` | component-level F1 口径（与 structure-event-driven 一致） |

按用户最新口径（**状态机来源不限，含人写**），Hermes 的 ground-truth FSM 是"4 researcher 标注 + 2 expert verify 的人写状态机"——符合 H3 的"human expert review on 状态机 artifact"。

## 6. 落盘与 parquet 化

- 本地数据路径：[`./data/`](./data/)（`git clone --depth 1 https://github.com/SyNSec-den/hermes-spec-to-fsm.git data` 完成，2026-05-06 15:04）
- parquet schema 是否对齐：🟢 已对齐（34 列）
- parquet 行数：**3 行**（`case_aggregate_stat`，4G-NAS Release 16 / 5G-NAS Release 17 / 5G-RRC Release 17 spec-level paper-reported accuracy 0.8721）
- ETL 入口：[`../etl/build_protocol_fsm_records.py`](../etl/build_protocol_fsm_records.py)
- 输出文件：[`../etl/out/protocol_fsm_human_review_records.parquet`](../etl/out/protocol_fsm_human_review_records.parquet)
- 当前 reviewer benchmark 是否已能消费：🟢 是（`summarize_benchmark_coverage` 校验通过）

注：Hermes 论文本身的 NEUTREX 模型权重 gated 在 Google Drive，repo 内**仅包含 TCNL 标签 + 原始 spec txt 文件**；无 LLM/模型预测可用，因此每个 spec 只产生 1 行 spec-level 聚合行（不展开到 transition 级别）。

## 7. 状态

🟢 直接可用：数据已 clone、ETL 已完成（spec-level）、parquet 已对齐 schema、reviewer benchmark 已消费验证。

## 8. 后续动作

已完成：

- 论文 PDF 已落盘 + paper_content.txt 已用 pdf_extractor 提取
- bibtex.bib 已写
- review 数据来源（GitHub）已验证可访问
- reviewer 资质（4+2）+ 工作量（2,800 person-hours）+ 16,000 datapoints 已从论文证实

待办：

- 在 SyNSec-den GitHub org 找具体 Hermes 子 repo 并克隆
- 把 4G-NAS / 5G-NAS / 5G-RRC 标注转换为 reviewer parquet schema
- 确认 GitHub repo 是否包含 Cohen κ 或类似一致性数据，若无则保留"⚪ 未显式报告"

阻塞：

- 论文 line 176 的 anchor 是 org 级（github.com/SyNSec-den/），具体 repo 名需自行找；可能 paper 发表后才推送

## 9. 更新日志

- `2026-05-06 14:48:00`：初版 review_extraction.md 入库；paper.pdf + paper_content.txt + bibtex.bib 已落盘；review 数据本身（GitHub）尚未克隆，标 🟡 可整理
