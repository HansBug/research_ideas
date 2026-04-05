# `CCF` 软件工程方向年度索引工作流

本文档说明如何使用 `tools/ccf_se_index_builder.py` 维护 `frontier_index/ccf_history/` 下的年度索引。

当前推荐流程已经拆成两步：

1. `ccf_se_index_builder.py` 负责基础元数据层。
2. `ccf_se_classifier.py` 负责启发式初判、人工复核覆盖、`x.x.x` 分类和年度页重渲染。

## 1. 目标

该工具用于生成：

1. 年度总 README
2. 每个 venue 的 `metadata` 数据文件
3. 每个 venue 的 `bib` 文件
4. 逐 venue 计数复核结果

当前默认服务于：

- `frontier_index/ccf_history/<year>/`

## 2. 运行方式

在仓库根目录执行：

```bash
python -m tools.ccf_se_index_builder --year 2025
```

完成基础构建后，再执行：

```bash
python -m tools.ccf_se_classifier --year 2025
```

如果需要输出到其他位置：

```bash
python -m tools.ccf_se_index_builder --year 2025 --target-dir frontier_index/ccf_history/2025
```

## 3. 生成结果

默认会在目标目录下生成：

1. `README.md`
2. `verification.json`
3. `metadata/*.json`
4. `bib/*.bib`
5. `_cache/`

其中：

1. `README.md`
   - 面向人工阅读。
2. `verification.json`
   - 记录逐 venue 的 `expected_total / actual_total`。
3. `metadata/*.json`
   - 保存每篇论文的结构化元数据、摘要、方向标签、官方页等。
4. `bib/*.bib`
   - 保存每个 venue 的完整 `BibTeX` 条目。
5. `_cache/`
   - 保存网络请求缓存，用于重复运行时加速和减小远端压力。
6. 后续分类补录字段
   - 例如 `macro_area`、`se_inclusion_decision`、`se_primary_path`、`se_secondary_paths`、`se_decision_basis`、`classification_source`、`manual_review_status`。
7. `manual_review/overrides.json`
   - 保存逐篇人工复核覆盖结果。

分类器运行完成后，`metadata/*.json` 里的每篇论文都应补齐：

1. `macro_area`
2. `se_inclusion_decision`
3. `cross_domain_flag`
4. `se_primary_path`
5. `se_primary_label`
6. `se_secondary_paths`
7. `se_decision_basis`
8. `classification_source`
9. `manual_review_status`

## 4. 标准工作流程

建议按以下顺序操作：

1. 先运行构建器生成当年的全量结果。
2. 检查 `verification.json` 是否全部为 `ok`。
3. 第一次运行分类器，先获得全量启发式初判结果。
4. 逐篇人工复核时，不要直接手改 `metadata/*.json`；应把最终裁决写入 `frontier_index/ccf_history/<year>/manual_review/overrides.json`。
5. 重新运行分类器，让人工复核覆盖脚本结果，并重渲染年度页。
6. 若某类论文没有自然 `x.x.x` 落点，应先扩 `frontier_index/SOFTWARE_ENGINEERING_FIELD_TREE.md`，再更新分类器规则并重跑，不要把论文硬塞进旧路径。
7. 若某些 venue 仍有边界或来源异常，再回到构建器中的特殊配置补规则。
8. 最后再人工抽查关键 venue 的 `README.md`、`metadata`、`bib`、`classification_source` 与 `manual_review_status` 是否一致。

## 5. 当前脚本的来源策略

脚本当前综合使用以下来源：

1. `DBLP`
   - venue 列表
   - 年度论文主数据
   - `BibTeX`
2. `OpenAlex`
   - 摘要与辅助方向信息
3. `DOI` 跳转
   - 官方落地页解析

当前默认分工如下：

1. 构建器负责生成**基础元数据层**。
2. 分类器负责启发式 `soft/non-soft` 初判、`x.x.x` 主路径建议、`X1/D1-D4` 依据和人工复核覆盖整合。

## 6. 维护约束

1. 若脚本对某些 conference 的主会 / companion / workshop 边界判断不稳，应优先补脚本特例，而不是手工改生成结果。
2. 若新增年份，优先复用该脚本，不要重新手工拼一整年的总表。
3. 若官方主页或 `CFP` 无法可靠自动获取，允许在生成结果中保留 `待补`，但主论文名录、`doi`、官方落地页、`BibTeX` 和计数复核必须优先保证。
4. 若 `CCF_SE_A_B_C.md` 扩展了列数或说明文字，构建器仍必须能稳定解析 venue 名录，不应把文档格式变化变成索引中断点。
5. 逐篇“最终属于什么类型”这件事，默认以人工复核覆盖文件为准；脚本规则只能降低人工成本，不能替代终判。
