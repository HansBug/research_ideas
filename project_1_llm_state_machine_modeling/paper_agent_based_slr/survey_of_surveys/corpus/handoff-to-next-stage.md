# A2a → A2b 交接说明

## 1. A2b 可以直接使用的资产

| 资产 | 入口 | 说明 |
|---|---|---|
| 主候选 120 | [tables/core-corpus.csv](./tables/core-corpus.csv) | A2b 优先深读对象；其中 A1 13 篇已有正式 `review.md` / `evidence_chain.md`。 |
| 替补 40 | [tables/reserve-corpus.csv](./tables/reserve-corpus.csv) | 用于替换被 A2b 排除或全文无法取得的主候选。 |
| PDF 状态 | [tables/pdf-status.csv](./tables/pdf-status.csv) | 记录 69 篇已下载、91 篇待人工下载和失败类型。 |
| 人工下载 BibTeX | [manual-download-needed.bib](./manual-download-needed.bib) | 当前剩余 91 条，可继续导入 Zotero 后批量下载。 |
| 来源审计 | [source-audit.md](./source-audit.md) | 说明候选分母和快照口径。 |

## 2. A2b 优先级建议

1. 先处理已取得 PDF / 文本的 69 篇：其中 A1 已有 13 篇可校准 A2b 页码、表图和 supplementary 精核模板；其余 56 篇不得跳过全文审计，需从 `a2a_review_status = not_started` 开始。
2. 并行补剩余 P0 人工下载条目：主候选 + CCF-A 或与 LLM / 测试 / MDE / 证据链高度相关的论文。
3. 再处理 P1 主候选：补足 CCF-B、主题和综述类型分布；其中 `broken_pdf` 条目需重新下载干净 PDF。
4. 最后使用替补 40：仅在主候选被排除、全文不可得或类型误收时替换。

## 3. A2b 必须新增的证据

A2a 只提供候选与全文状态。A2b 若要把条目升级为可写作证据，必须补齐：

1. `review.md` 的全文深读结论。
2. `evidence_chain.md` 的页码、章节、原文短引和 claim map。
3. 维度树 / 维度森林与叶子取值空间。
4. 统计池资格裁决和排除理由。
5. 覆盖 / 饱和度判断。

## 4. 不得越级的事项

- 无 A2b 完整快照，不得冻结 A3 schema / stage contract。
- A2a 的 `core-corpus.csv` 不是最终统计分母。
- `manual-download-needed.bib` 中的条目不是排除条目。
- 边界池不能直接进入主统计池，除非 A2b 全文核验证明其满足系统化二次研究条件并显式升级。

## 5. 合流前复验

本 PR 合入伞 PR #101 前，需确认 GitHub `mergeStateStatus` 为 `CLEAN` 或已解释为只剩 CI / 上游同步等待；若 #101 先同步 `main`、rebase 或发生 sibling PR 合流，必须重新运行：

```bash
python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/scripts/build_corpus_tables.py
python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/scripts/validate_corpus.py
git diff --check
```

并确认 [raw/selection-seed.csv](./raw/selection-seed.csv)、[tables/core-corpus.csv](./tables/core-corpus.csv)、[tables/reserve-corpus.csv](./tables/reserve-corpus.csv)、[tables/boundary-pool.csv](./tables/boundary-pool.csv) 和人工下载清单没有被旧口径覆盖。
