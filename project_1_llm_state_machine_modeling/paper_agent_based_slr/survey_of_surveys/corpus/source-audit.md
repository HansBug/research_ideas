# A2a 来源审计

## 1. 来源快照

| 来源 | 本地文件 | 当前用途 | 备注 |
|---|---|---|---|
| issue #95 CCF-A/B 近年综述候选摸排 | [raw/candidates.csv](./raw/candidates.csv) | L0 全量候选账本输入 | 438 条；题名、摘要、venue、CCF、DOI、开放获取字段来自前序摸排。 |
| issue #95 全文获取审计 | [raw/fulltext-audit.csv](./raw/fulltext-audit.csv) | PDF 线索与失败类型审计输入 | 438 条；记录公开 PDF URL、历史下载状态、本地临时路径和结构分析状态；其中本地临时路径只作线索，不作为可复算事实源。 |
| Zotero PDF 导入审计 | [raw/zotero-import-2026-07-07.csv](./raw/zotero-import-2026-07-07.csv) / [raw/zotero-import-failed-2026-07-07.csv](./raw/zotero-import-failed-2026-07-07.csv) | 用户本地合法补齐 PDF 后的显式导入记录 | 54 篇成功导入并生成文本；2 篇附件损坏、内容错配或无法提取文本，继续留在人工下载清单。 |
| A2a 主候选选择种子 | [raw/selection-seed.csv](./raw/selection-seed.csv) | 主候选 120 的优先级种子 | 100 条；由前序候选摸排按 CCF 等级、年份、主题和综述类型分层得到，用于避免干净 clone 时依赖本机 `/tmp` 隐藏输入。 |
| A1 已合入文库 | [../papers/](../papers/) | 继承 13 篇入池候选与 6 篇边界 / 方法样本 | A1 的 `review.md` / `evidence_chain.md` 不被 A2a 覆盖。 |

## 2. 当前复算结果

| 表 | 数量 | 说明 |
|---|---:|---|
| [full-candidate-ledger.csv](./tables/full-candidate-ledger.csv) | 438 | 原始候选规范化后全量入账。 |
| [systematic-candidates.csv](./tables/systematic-candidates.csv) | 293 | 当前脚本按系统化信号识别的候选池，最终以脚本复算为准。 |
| [core-corpus.csv](./tables/core-corpus.csv) | 120 | 后续 A2b 优先处理。 |
| [reserve-corpus.csv](./tables/reserve-corpus.csv) | 40 | 替补 / 留出。 |
| [boundary-pool.csv](./tables/boundary-pool.csv) | 145 | 方法启发 / 边界条目。 |

## 3. 不确定性与审计限制

1. `title_zh_machine`、`abstract_zh_machine` 等字段是机器翻译或机器生成，只能辅助速读，不能作为最终论文证据。
2. RQ 字段在多数候选中仍为“待全文核验”，不得在 A2a 阶段写成已抽取研究问题。
3. CCF 大类 / 等级仍需在正式写作前回到 CCF 官方目录人工复核；本表沿用前序摸排工作口径。
4. 公开 PDF 临时路径来自前序 `/tmp` 快照；无论本机当前是否碰巧存在该路径，本 PR 都不得自动复制这些仓库外文件，也不得据此把条目计为已获取。只有仓库内真实存在的 `papers/<slug>/paper.pdf` 才是 `downloaded` 事实源。
5. `raw/` 中三个 CSV 已做换行符与行尾空白规范化，便于通过 `git diff --check`；该规范化不改变字段、行数、候选资格或任何元数据语义。
6. A2a 主候选优先级不得读取仓库外部 `/tmp` 文件；若要更改选择种子，必须先更新 [raw/selection-seed.csv](./raw/selection-seed.csv)，再复算 [tables/](./tables/)。
7. A2a PDF 获取状态不得读取仓库外部 `/tmp` 文件；若要把人工下载或本地 Zotero 找到的 PDF 纳入文库，必须显式复制到对应 `papers/<slug>/paper.pdf`，生成 `paper_content.txt`，再复算 [tables/pdf-status.csv](./tables/pdf-status.csv)。本轮采用 [../scripts/import_zotero_export_pdfs.py](../scripts/import_zotero_export_pdfs.py) 完成该步骤。

## 4. 复验命令

```bash
python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/scripts/build_corpus_tables.py
python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/scripts/validate_corpus.py
```
