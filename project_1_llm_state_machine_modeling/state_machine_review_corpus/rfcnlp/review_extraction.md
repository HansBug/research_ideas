# `rfcnlp` review extraction

## 1. 论文元信息

- **标题**：Automated Attack Synthesis by Extracting Finite State Machines from Protocol Specification Documents
- **作者**：Maria Leonor Pacheco, Max von Hippel, Ben Weintraub, Dan Goldwasser, Cristina Nita-Rotaru
- **年份 / Venue**：IEEE Symposium on Security and Privacy (S&P / Oakland) 2022, pp. 51-68
- **DOI / arXiv / URL**：[DOI: 10.1109/SP46214.2022.9833673](https://doi.org/10.1109/SP46214.2022.9833673) / [arXiv:2202.09470](https://arxiv.org/abs/2202.09470)
- **本篇 review 数据用途**：6 个 IETF 协议 RFC 的手工 XML grammar 标注 + ground-truth FSM；是 PSMBench 的源数据集之一（PSMBench 中 DCCP / TCP 复用本工作的 FSM 标注）。

## 2. review 数据获取方式

- **来源类型**：☑ 公开仓库（GitHub）
- **入口 URL**：[github.com/RFCNLP/RFCNLP](https://github.com/RFCNLP/RFCNLP)
- **本地落盘路径**：`state_machine_review_corpus/rfcnlp/`（仅 paper.pdf / paper_content.txt / bibtex.bib；标注数据需从 GitHub 二次拉取）
- **当前可访问性**：☑ GitHub org `RFCNLP` 已 web 验证（2 repos：`RFCNLP` 主项目 + `RFCNLP-korg`）；标注文件位于 `rfcs-annotated/`、`rfcs-annotated-tidied/`、`rfcs-bio/`、`rfcs-original/`、`rfcs-predicted/` 等目录
- **首次访问时间戳**：`2026-05-06 14:46`

## 3. reviewer 资质与人数

- **reviewer 资质**：🟢 domain experts（论文 line 144 / 240 / 858 多次强调"experts with domain knowledge"做标注；Purdue + Northeastern 两校 SE / security 研究者）
- **reviewer 总人数**：N（论文未单独披露具体人数，但 5 位作者中至少多人参与标注）
- **是否独立**：☑ 标注与验证由不同 author 协作完成
- **是否报告 inter-rater agreement**：⚪ 论文未显式报告 Cohen κ
- **annotation 强度**：6 个协议、每协议 1 个完整 RFC 文档；论文 Section IV.A 详述 BNF grammar + 4 类 annotation tags（state / event definition + state / event reference）

## 4. review 数据 schema

### 4.1 单条 review 的字段

按论文 Figure 2 (BNF grammar) + Section IV.A：

| 字段 | 类型 | 取值范围 | 备注 |
|---|---|---|---|
| `protocol` | string | 6 类（BGPv4 / DCCP / LTP / PPTP / SCTP / TCP） | IETF 协议 |
| `rfc_paragraph` | string | 原始 RFC 段落文本 | 输入 NL |
| `xml_annotation` | XML | `<def_state>` / `<def_event>` / `<error>` / 其它 5 tag | 论文 Section IV.A.2 定义的 5 类标签 |
| `bio_tag` | BIO encoding | per-token | 用于 NLP 模型训练 |
| `gold_fsm` | structured | 完整状态机 | 由 expert domain knowledge 构造（论文 line 858） |

### 4.2 数据规模

- 6 个完整 RFC 文档：BGPv4 / DCCP / LTP / PPTP / SCTP / TCP
- 标注总量：完整文档级 XML annotation
- 标签类别：4 类 definition tags + 5 类 state-machine logic tags（共 9 类）

### 4.3 评分聚合方式

- 论文不是 review-on-LLM-output；论文是 **数据驱动的 NLP 方法（zero-shot + 自监督）+ 人工 ground truth 评估**
- 公开的是：**xml 标注（多 reviewer 协作 + expert verification）+ 输出 FSM**
- benchmark 评估方式：F1 over 9 标签类别 + FSM-level transition accuracy

## 5. 对齐到 reviewer 统一 schema

| 本篇字段 | reviewer 系统统一字段 | 映射方式 |
|---|---|---|
| protocol | `paper_slug` / `case_id` | rfcnlp:::tcp / rfcnlp:::dccp / etc. |
| rfc_paragraph | `input_text` | 直接 |
| xml_annotation | `human_review_details_json` | 序列化为 JSON 保留 |
| gold_fsm | `ref_output_text` | FSM 序列化 |
| 9 类标签 F1 | `human_review_score` | component-level F1 口径 |

按用户最新口径（**状态机来源不限，人写也算**），RFCNLP 的 ground-truth FSM 是"domain expert 手工 XML 标注 + verified"——符合 H3。这是 PSMBench 的源数据集，已在 protocol state machine 领域有学术影响力。

## 6. 落盘与 parquet 化

- 本地数据路径：尚未克隆 RFCNLP/RFCNLP GitHub
- parquet schema 是否对齐：⚪ 待对齐
- parquet 行数：⚪ 待生成（预计：6 RFCs × 平均 ~80 paragraphs/RFC = ~500 行 paragraph-level / 或聚合到 transition-level ~200 行）
- 当前 reviewer benchmark 是否已能消费：⚪ 否，需 ETL

## 7. 状态

🟡 可整理：来源已确认可获取（GitHub repo 含完整标注文件目录）；schema 对齐与 ETL 工作未完成。

## 8. 后续动作

已完成：

- 论文 PDF 已落盘 + paper_content.txt 已提取
- bibtex.bib 已写（DOI + arXiv）
- GitHub repo 已 web 验证：[github.com/RFCNLP/RFCNLP](https://github.com/RFCNLP/RFCNLP)
- 6 协议的 XML / BIO / FSM 标注目录已识别（`rfcs-annotated-tidied/` 等）

待办：

- `git clone https://github.com/RFCNLP/RFCNLP` 到本地 `data/` 子目录（注意 Git LFS）
- 把 6 协议的 XML annotation 转换为 reviewer parquet schema
- 论文未显式报告 inter-rater κ → 在 review_extraction 中保留"⚪ 未报告"备注

阻塞：

- 无（仓库公开 + 文件结构清晰）

## 9. 更新日志

- `2026-05-06 14:48:00`：初版 review_extraction.md 入库；paper.pdf + paper_content.txt + bibtex.bib 已落盘；GitHub repo 二次克隆 + parquet 化 ETL 待办
