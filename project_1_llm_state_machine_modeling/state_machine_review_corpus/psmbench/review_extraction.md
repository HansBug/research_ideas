# `psmbench` review extraction

## 1. 论文元信息

- **标题**：PSMBench: A Benchmark and Dataset for Evaluating LLMs on Extracting Protocol State Machines from RFC Specifications
- **作者**：Zilin Lin et al.
- **年份 / Venue**：NeurIPS 2025 Datasets and Benchmarks Track
- **DOI / arXiv / URL**：[OpenReview](https://openreview.net/forum?id=5HGBErIHuV)
- **本篇 review 数据用途**：提供 14 个网络协议的 RFC → Protocol State Machine 标注数据，含 cross-verified ground truth + κ 报告，可作为 reviewer 系统的多协议 cross-domain 评估材料。

## 2. review 数据获取方式

- **来源类型**：☑ 公开仓库（GitHub + HuggingFace）
- **入口 URL**：
  - GitHub: [Zilinlin/RFC_PSM_Benchmark](https://github.com/Zilinlin/RFC_PSM_Benchmark)
  - HuggingFace dataset: [zilinlin/RFC2PSM](https://huggingface.co/datasets/zilinlin/RFC2PSM)
- **本地落盘路径**：`state_machine_review_corpus/psmbench/`（仅 paper.pdf / paper_content.txt / bibtex.bib；review 标注数据需从 GitHub / HuggingFace 二次拉取）
- **当前可访问性**：☑ 已浏览未下载 review 数据；下次拉取需 `git clone` GitHub 仓库或 `datasets.load_dataset`
- **首次访问时间戳**：`2026-05-06 14:39`

## 3. reviewer 资质与人数

- **reviewer 总人数**：annotation 由 paper authors 中的 domain experts 进行；具体 N 论文未单独披露，但论文称"months of careful analysis and domain expertise"
- **资质**：🟢 domain experts / network protocol researchers
- **是否独立**：☑ 是（systematic annotation protocol：annotator A 提取 PSM → annotator B 审查并 mark revision points → 分歧 discussion 解决）
- **是否报告 inter-rater agreement**：☑ **是**（论文 line 217-219 明确报告：**κ = 0.82 for states / κ = 0.78 for transitions**，substantial agreement）

## 4. review 数据 schema

### 4.1 单条 review 的字段

| 字段 | 类型 | 取值范围 | 备注 |
|---|---|---|---|
| `protocol` | string | 14 类（BGP, DCCP, DHCP, FTP, IMAP, MQTT, NNTP, POP3, PPP, PPTP, RTSP, SIP, SMTP, TCP） | 网络协议 |
| `rfc_text_chunk` | string | 1,580 页 cleaned RFC 文本 | 输入 NL |
| `state` | string | 108 states 总计 | 标注节点 |
| `transition` | tuple (from, to, event, action) | 297 transitions 总计 | 标注边 |
| 内部 verification fields | — | annotator 1/2 一致性记录 | 用于 κ 计算 |

### 4.2 数据规模

- artifact 总数：14 个协议 × 1 个 ground-truth PSM
- 状态总数：108
- 迁移总数：297
- 输入文本：1,580 页 cleaned RFC
- 工作量：months of careful analysis per protocol；TCP / DCCP 直接复用 RFCNLP (Pacheco et al. 2022) 的标注

### 4.3 评分聚合方式

- 论文公开的是**单一 ground-truth**（cross-verified by two annotators 后的最终版本）+ pass-1/pass-2 一致性 κ
- HuggingFace dataset 提供机器可读的 PSM 标注 + RFC chunk pairs
- benchmark 评估方式：LLM 输出与 ground truth 的 fuzzy semantic matching → state F1 / transition F1

## 5. 对齐到 reviewer 统一 schema

| 本篇字段 | reviewer 系统统一字段 | 映射方式 |
|---|---|---|
| protocol | `case_id` / `paper_slug` | 视协议为 case 维度 |
| rfc_text_chunk | `input_text` | 直接 |
| ground-truth PSM (states + transitions) | `ref_output_text` | 序列化为文本 / JSON |
| 评估方式：fuzzy semantic state F1 / transition F1 | `human_review_score` (component F1) | 类似 structure-event-driven 的 component-level F1 口径 |
| reviewer agreement κ=0.82/0.78 | metadata `inter_rater_kappa` | 新增字段记录论文级 κ |

注：本数据集没有"对 LLM 输出的逐条 review 评分"——按用户最新口径（**状态机来源不限——人写也算**），论文提供的是**人写状态机 + 双人 cross-verified κ**，符合 H3。reviewer 系统消费时把"人写 PSM"作为参考，把"两位 reviewer 的 cross-verification κ"作为 dataset-level meta-evidence。

## 6. 落盘与 parquet 化

- 本地数据路径：尚未拉取（待办）
- parquet schema 是否对齐到 `baseline_double_green_human_review_records` schema：⚪ 待对齐（PSM 转 record 形式需要协议 → state/transition 展开）
- parquet 行数：⚪ 待生成（预计：14 协议 × 平均 ~21 transitions = ~300+ 行）
- 当前 reviewer benchmark 是否已能消费：⚪ 否，需 ETL 工作

## 7. 状态

🟡 可整理：来源已确认可获取，仓库与 dataset 都已 浏览验证；但抽取/对齐到 reviewer schema 尚未完成。

## 8. 后续动作

已完成：

- 论文与 abstract 已识别
- GitHub + HuggingFace 入口已 web 验证可访问
- 论文中 κ=0.82/0.78 已确认为论文显式报告
- paper.pdf + paper_content.txt + bibtex.bib 已落盘

待办：

- `git clone` GitHub 仓库到本地 `data/` 子目录
- ETL：把 14 协议的 PSM 标注展开为 reviewer parquet schema 的 record-level 行
- 对齐 `score scale / unit / review_target / diagram_type` 字段

阻塞：

- 无（数据完全公开）

## 9. 更新日志

- `2026-05-06 14:48:00`：初版 review_extraction.md 入库；paper.pdf + paper_content.txt + bibtex.bib 已落盘；review 数据本身（GitHub repo）尚未克隆，标 🟡 可整理
