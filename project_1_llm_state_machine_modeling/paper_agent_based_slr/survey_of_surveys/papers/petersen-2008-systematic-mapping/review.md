# Systematic Mapping Studies in Software Engineering

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Systematic Mapping Studies in Software Engineering |
| 年份 | 2008 |
| 类型 | systematic mapping study 方法论文 |
| 出版形态 | 会议 |
| 期刊/会议/预印本 | [EASE](https://conf.researchr.org/series/ease) |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | C |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| 来源等级 | EASE 2008 / BCS Electronic Workshops in Computing；正式 DOI 已核验；PDF 本轮未自动获取 |
| 阅读状态 | 全文不可得-待人工下载 |
| 证据等级 | 题摘级 / metadata-only；不得写方法细节为全文事实 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、DOI: <https://doi.org/10.14236/ewic/EASE2008.8> |
| 综述类型 | SMS 方法与示例 |
| SE 子领域 | 软件工程 mapping study 方法学 |
| A1 角色 | 用于压测 `manual-download-needed.bib`、metadata-only、不可获取 PDF 和“不假装已读全文”的失败路径。 |
| 是否目标证据池 | 否。 |
| schema 缺口 | 暴露 `全文不可得` 时只能记录候选 pattern，不能升级为已采纳字段。 |

## 2. 六类 pattern 抽取

| pattern | 当前状态 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 待全文核验；只能从题名推断与 SMS 相关。 | DOI metadata / title。 | 不可升级为已采纳。 | 无全文，不能采纳为 RQ 模式。 |
| dimension pattern | 待全文核验。 | DOI metadata / title。 | 只能记为候选。 | 无全文，不能采纳字段。 |
| finding pattern | 不可抽取。 | 无全文。 | 不可迁移。 | 无全文，不支撑 finding。 |
| evidence presentation pattern | 待全文核验。 | 无全文。 | 不可迁移。 | 无全文，不知道其证据呈现结构。 |
| validity / threat pattern | 待全文核验。 | 无全文。 | 不可迁移。 | 无全文，不知道 threat 章节。 |
| report structure pattern | 待全文核验。 | 无全文。 | 不可迁移。 | 无全文，不知道报告结构。 |

## 3. 对 PR-A1 schema 的启发

1. `阅读状态` 与 `证据等级` 必须阻止 metadata-only 条目进入已采纳 pattern。
2. `manual-download-needed.bib` 必须保存完整 BibTeX，便于后续人工补 PDF。
3. SUMMARY 中该条目只能计入候选池和失败路径验收，不得计入全文 dry-run 成功数量。

## 4. 待复核

- 需要人工下载正式 PDF 或通过图书馆访问。
- 全文补齐后应回填 `paper.pdf`、`paper_content.txt`，并重写本 review。

## 5. A1-M0--M6 脚手架元维度贡献

| A1-M 脚手架元维度 | 当前状态 | 采纳边界 |
|---|---|---|
| A1-M0 研究意图与综述元模型 | 题摘级可判断其为 systematic mapping 方法论文。 | 仅候选。 |
| A1-M1 语料收集与纳排 | PDF 未获取，不能核验 mapping process 细节。 | 不采纳。 |
| A1-M2 研究对象与主题语义 | 未读全文。 | 不采纳。 |
| A1-M3 方法 / 技术 / 干预 | 未读全文。 | 不采纳。 |
| A1-M4 评价、证据与复现资产 | 仅记录 DOI / 获取失败。 | 只用于 manual-download 失败路径。 |
| A1-M5 统计分析就绪 | 无全文字段。 | 不进入统计池。 |
| A1-M6 research finding 形成与裁决 | 无全文 findings。 | 不采纳。 |
