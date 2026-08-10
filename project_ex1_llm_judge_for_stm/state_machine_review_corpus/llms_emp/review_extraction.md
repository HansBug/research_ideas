# `llms_emp` review extraction

> 本篇方法分析见 [baselines/llms_emp/DESC.md](../../baselines/llms_emp/DESC.md)。

## 1. 论文元信息

- **标题**：Generating SysML Behavior Models via Large Language Models: an Empirical Study
- **中文标题**：基于大型语言模型的SysML行为模型生成：一项实证研究
- **作者**：Yuan Wang, Ning Ge, Jiangxi Liu, Zhilong Cao, Zheping Chen, Chunming Hu
- **单位**：Beihang University (北京航空航天大学), School of Software
- **年份 / Venue**：Internetware 2025（ACM, June 20-22, 2025, Trondheim, Norway）
- **DOI / arXiv / URL**：[ACM 10.1145/3755881.3755926](https://dl.acm.org/doi/10.1145/3755881.3755926)
- **本篇 review 数据用途**：当前 reviewer 系统 dataset 中 `sample_level_review` 类全部 192 行的来源；提供 SysML 行为模型（状态机图 / 活动图 / 序列图）的 sample-level human-rated 数据。

## 2. review 数据获取方式

- **来源类型**：☑ 公开仓库（Google Drive）
- **入口 URL**：[Google Drive 公开链接](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link)（论文脚注 1）
- **本地落盘路径**：`discussions/2026-04-15-01-03-52-AI-讨论-baselines双绿数据集下载解析与parquet化.assets/baseline_double_green_human_review_records.parquet`（`paper_slug == "llms_emp"`）
- **当前可访问性**：☑ 已下载 + 已 parquet 化
- **首次访问时间戳**：约 `2026-04-15 01:03:52`（baseline 双绿 parquet 化时）

## 3. reviewer 资质与人数

- **reviewer 总人数**：⚠️ **论文未交代评测阶段的人数**。论文只交代了数据集*构建*团队（§3.3：G_Search 5 人、G_Model 5 人，每人 >100 小时建模经验，共投入 524 人时），评测阶段（§4.7 的 $Acc_S$ 与 $F1$ 两项人工指标）由几人、按什么流程执行，全文未写
- **资质**：🟡 仅对构建团队有交代（SE 研究者），评测者资质未单独说明
- **是否独立**：⚠️ **未交代**。论文未描述评测阶段的独立评分与聚合机制，也未描述分歧消解流程
- **是否报告 inter-rater agreement**：☒ **否**。对 `paper_content.txt` 全文检索 `kappa` / `inter-rater` / `interrater` / `agreement` **零命中**。$Acc_S$（语义一致性）与 $F1$（按 grammar point 计）是人工计数指标，不是评分者间一致性指标——两者不可互换。论文 §4.2(4) 另明写 "we **assume** the reference model is semantically correct"，即参考模型的正确性是假设、未独立验证；§4.4 自认 "all validations must be performed manually, potentially limiting the comprehensiveness"

> 此处此前记作「☑ 是（含 reviewer 间一致性讨论）」，与原文冲突。该错误会污染 LLM-as-Judge 的 noise-floor 校准口径——把一个**没有**人类一致性基线的研究当成有基线的来对标。修正依据：`baselines/llms_emp/paper_content.txt` 全文检索，以及 §3.3 / §4.2 / §4.4 / §4.7 逐节核对。

## 4. review 数据 schema

### 4.1 单条 review 的字段

reviewer 系统的 parquet 中 `record_type == "sample_level_review"` 的 192 行：

| 字段 | 类型 | 取值范围 | 备注 |
|---|---|---|---|
| `review_record_id` | string | unique | |
| `case_id` / `case_name` | string | 来自 107 个 SysML 行为模型公开数据集 | |
| `diagram_type` | string | `stm` / `act` / `sd` | 状态机 / 活动 / 序列图 |
| `llm_name` | string | e.g. `GPT-4 / Claude / DeepSeek / Kimi` | |
| `review_target` | string | `generated_behavior_model` | sample 级 |
| `human_review_score` | float | 0-1 normalized | 综合评分 |
| `human_review_score_unit` | string | `normalized_quality` 或类似 | |
| `human_review_summary` | string | reviewer 文字说明 | |
| `human_review_details_json` | string | 多维评分细分（格式 / 语法 / 语义 / 需求一致） | |
| `pred_output_text` | string | LLM 生成的 PlantUML 文本 | |
| `paper_method_verbatim_excerpt` | string | 论文方法原文摘录 | |

### 4.2 数据规模

- artifact 总数：107 个 SysML 行为模型 → reviewer dataset 中保留 192 行（含多 LLM × 多策略组合）
- reviewer 总数：N（论文研究团队 SE 研究者）
- review 总条数：**192 行**（已聚合为单条 review_record_id）

### 4.3 评分聚合方式

- 论文是否提供原始评分表（每条独立）：🟡 部分（论文给出多维细分，但是否含逐 reviewer 原始评分需进一步核查）
- 论文公开的是聚合后的：☑ 是（多维细分但 reviewer-level 已聚合）
- 当前 corpus 持有的是哪一种：聚合后（已 parquet 化）

## 5. 对齐到 reviewer 统一 schema

| 本篇字段 | reviewer 系统统一字段 | 映射方式 |
|---|---|---|
| 综合评分（normalized） | `human_review_score`（0-1） | 直接 |
| 多维细分（格式 / 语法 / 语义 / 需求一致） | `human_review_details_json` | JSON 序列化保留 |
| LLM 名 + 策略 | `llm_name` / `strategy_name` | |
| diagram_type (stm / act / sd) | `diagram_type` | 保留分类 |

## 6. 落盘与 parquet 化

- 本地数据路径：`discussions/.../baseline_double_green_human_review_records.parquet`
- parquet schema 是否对齐到 `baseline_double_green_human_review_records` schema：☑ 是
- parquet 行数：**192** 行（占总 820 行的 23.4%）
- 当前 reviewer benchmark 是否已能消费：☑ 是

## 7. 状态

🟢 直接可用

## 8. 后续动作

已完成：

- Google Drive 公开数据已下载并 parquet 化
- reviewer benchmark 主路径已消费

待办：

- 检查论文 supplementary 是否含逐 reviewer 原始评分（当前持有的是聚合）
- 若需要，邮件联系 Yuan Wang / Ning Ge 团队拿原始评分表

阻塞：

- 无

## 9. 更新日志

- `2026-05-06 13:54:54`：初版 review_extraction.md 入库；数据沿用现有 parquet（baseline 双绿 2026-04-15）
