# `2025/manual_review/` README

## 1. 路径定位

本目录用于维护 `CCF 2025` 年度条目的**逐篇人工复核终判**。

这里的职责不是重新保存整份年度元数据，而是只保存“哪些论文已经被人工确认，以及人工确认后的最终分类是什么”。

## 2. 与年度元数据的关系

默认流程如下：

1. [../../../../tools/ccf_se_index_builder.py](../../../../tools/ccf_se_index_builder.py) 先生成基础元数据。
2. [../../../../tools/ccf_se_classifier.py](../../../../tools/ccf_se_classifier.py) 先生成启发式初判。
3. 人工逐篇检查后，把最终裁决写入 [overrides.json](./overrides.json) 或 [batches/](./batches/) 下的批次文件。
4. 再次运行分类器，让人工复核覆盖脚本结果，并重写 [../README.md](../README.md)。

换言之，[../metadata/](../metadata) 中的分类字段是可重建产物；真正的人工终判入口在 [overrides.json](./overrides.json) 与 [batches/](./batches/)。

## 3. 人工复核的最低要求

每篇论文人工复核时，默认至少要检查：

1. 标题。
2. 摘要。
3. 官方学术落地页。
4. 若边界仍不清楚，再看正式 `PDF` 或可获得的完整正文。

复核时需要回答的核心问题：

1. 这篇论文一级总类别到底是 `软件工程`、`系统软件`、`程序设计语言与形式化基础` 还是 `跨域/待判定`。
2. 它是否真的属于软件工程，还是只是出现在 `TCSE_SS_PDL` 这一路 venue 里。
3. 若属于软件工程，主路径应落到哪个 `x.x.x`。
4. 若当前树没有自然落点，是否应该先扩 [../../../SOFTWARE_ENGINEERING_FIELD_TREE.md](../../../SOFTWARE_ENGINEERING_FIELD_TREE.md)。

## 4. 覆盖文件格式

[overrides.json](./overrides.json) 与 [batches/](./batches/) 下的单批次文件都使用如下结构：

```json
{
  "schema_version": 1,
  "year": 2025,
  "entries": [
    {
      "paper_key": "conf/icse/Example25",
      "doi": "10.0000/example",
      "title": "Example Paper",
      "macro_area": "软件工程",
      "se_inclusion_decision": "属于软件工程",
      "cross_domain_flag": "否",
      "se_primary_path": "6.3.1",
      "se_secondary_paths": [
        "6.5.1 开发者个体与认知",
        "5.4.3 人因评价与用户研究"
      ],
      "se_decision_basis": "人工复核：核心研究问题是软件开发者工作方式与支持策略，主要证据来自混合方法研究与调查。",
      "manual_review_note": "边界清晰，按经验软件工程纳入。",
      "manual_review_reviewer": "human",
      "manual_review_updated_at": "2026-04-06 01:30:00"
    }
  ]
}
```

字段要求如下：

1. `paper_key`
   - 推荐作为首选匹配键。
2. `doi`
   - 建议保留，便于双重核对。
3. `title`
   - 建议保留，便于人工阅读与兜底匹配。
4. `macro_area`
   - 必填。
5. `se_inclusion_decision`
   - 必填。
6. `cross_domain_flag`
   - 必填。
7. `se_primary_path`
   - 当且仅当论文属于软件工程或“跨域但软工主导”时填写。
8. `se_secondary_paths`
   - 建议填写 `1-3` 个辅助路径或标签。
9. `se_decision_basis`
   - 必填；这里建议写成真正的人工裁决依据，而不是仅重复脚本分数。
10. `manual_review_note`
   - 建议记录边界说明、争议点或复核备注。
11. `manual_review_reviewer`
   - 建议保留复核人标识。
12. `manual_review_updated_at`
   - 使用 `yyyy-mm-dd hh:mm:ss`。

## 5. 复核约束

1. 不要只因为论文来自 `ICSE / ASE / TOSEM / TSE` 就默认纳入软件工程。
2. 不要只因为论文来自 `PLDI / POPL / OOPSLA / FM / OSDI / SOSP` 就默认排除软件工程。
3. 判断时优先看核心研究问题、主贡献对象、方法链条和评估证据，而不是 venue 名称。
4. 若论文不属于软件工程，应把 `se_primary_path` 留空。
5. 若论文属于软件工程但找不到自然 `x.x.x`，先扩树，不要硬塞。
6. 调整分类器规则时，应该以这里已经积累的人工复核样本为依据，而不是反过来让脚本规则替代人工裁决。

## 6. 当前状态

1. 当前覆盖文件：[overrides.json](./overrides.json) / [batches/](./batches/)
2. `2025` 年度的全量人工终判当前实际保存在 [batches/](./batches/) 下的 `82` 个 venue 文件中；[overrides.json](./overrides.json) 当前保留为空占位文件，供后续零星补丁使用。
3. 若同一论文同时出现在 [batches/](./batches/) 与 [overrides.json](./overrides.json) 中，后者应视为更晚的人工补丁层，并优先覆盖前者。
4. 当前默认状态：已完成 `2025` 年 `6301` 条论文的逐篇人工终判。
5. [../README.md](../README.md) 中当前所有条目都应显示为 `人工复核 / 已人工复核`。
