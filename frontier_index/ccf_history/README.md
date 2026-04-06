# `ccf_history/` README

## 1. 路径定位

`ccf_history/` 用于存放当前 `CCF_SE_A_B_C.md` 保留的 `CCF` 软件工程高相关 venue 往年论文索引。

这里默认只存“元数据索引结果”，不直接存全文。

## 2. 推荐组织方式

后续默认按“**年份主目录**”组织，例如：

```text
ccf_history/
├── 2025/
│   ├── README.md
│   ├── verification.json
│   ├── metadata/
│   │   └── icse_conf_a.json
│   └── venues/
│       └── icse_conf_a.md
├── 2024/
│   ├── README.md
│   ├── verification.json
│   ├── metadata/
│   └── venues/
└── 2023/
    ├── README.md
    ├── verification.json
    ├── metadata/
    └── venues/
```

这样做的目的，是把“年度总览”和“逐 venue 论文名录”拆开：

1. `README.md` 负责年度总览、统计、规范口径和 venue 导航。
2. `venues/*.md` 负责单个 venue 的逐篇论文名录。
3. `metadata/*.json` 负责可重建、可回写的结构化保留载体。
4. `verification.json` 负责逐 venue 计数复核。

当前已建立的示例年份页：

1. [2025/README.md](./2025/README.md)
2. [year_template/README.md](./year_template/README.md)

若任务涉及“这篇论文到底算不算软件工程”“方向标签应该怎么打”，还应先读：

1. [../SOFTWARE_ENGINEERING_FIELD_TREE.md](../SOFTWARE_ENGINEERING_FIELD_TREE.md)
2. [../CCF_SE_A_B_C.md](../CCF_SE_A_B_C.md)

对于正式年度构建，默认优先使用：

1. [../../tools/ccf_se_index_builder.py](../../tools/ccf_se_index_builder.py)
2. [../../tools/ccf_se_index_workflow.md](../../tools/ccf_se_index_workflow.md)

## 3. 年份目录的职责

每个年份目录默认负责维护该年所有目标 venue 的信息汇总，重点包括：

1. 该年覆盖的期刊/会议清单。
2. 每个期刊/会议在该年的关键信息页与 venue 级先验。
3. 年度总页中的 venue 导航与链接。
4. `venues/*.md` 中按初筛优先级排序的逐篇论文名录。
5. 每篇论文的元数据、摘要/方向、`DOI`、官方页面与 `BibTeX`。
6. 对每篇论文的初步判定结果。
7. 对每篇论文的人工复核状态与判定来源说明。
8. 对混合 venue 中“哪些论文最终属于软件工程、哪些不属于”的边界说明。
9. 对纳入软工语料的论文给出 `x.x.x` 级软工主路径。

## 4. 单个年份 `README.md` 的建议结构

每个年份目录下的 [README.md](./year_template/README.md) 默认建议包含：

1. 该年说明
2. 该年汇总统计
3. 标准口径说明
4. 该年覆盖 venue 列表
5. 每个 venue 一个独立导航 section

每个 venue 导航 section 默认应包含：

1. `venue` 基本信息
   - 缩写
   - 全称
   - `CCF` 等级
   - 类型
   - `软工归属级别`
   - `氛围`
2. 该年的关键信息页面
   - 官方主页
   - `CFP`
   - 程序页 / proceedings / volume / issue 页
3. 指向对应 `venues/<venue>.md` 的论文名录页链接
4. 该 venue 在该年的统计概览
   - 一级总判定分布
   - 软工纳入判定分布
   - 初筛分布
5. 若需要表达 venue 跟踪优先级，直接使用 `氛围 A 🔥 / B 🟢 / C 🟡`；同档再结合 `软工归属级别`
6. 本 venue 在该年的简要观察

`venues/*.md` 默认负责真正的逐篇论文名录，至少应包含：

1. 文件导航
   - 年度总页
   - `verification.json`
   - 对应 `metadata/*.json`
2. `venue` 基本信息
3. 该年的关键信息页面
4. 该 venue 的年度统计
5. 逐篇论文名录表
6. 本 venue 年度观察

## 5. 关于“官方页面”的要求

你要求这里优先保存正式官方页面，这一点后续应作为硬约束执行：

1. 论文落地页优先使用：
   - `ACM DL`
   - `IEEE Xplore`
   - `Springer`
   - `Elsevier`
   - `USENIX`
   - 正式会议 proceedings 页
   - 正式期刊 article 页
2. 不应把下列页面当作主论文页：
   - `DBLP`
   - 普通引导页
   - 搜索结果页
   - 博客转载页
3. `DBLP` 可以作为辅助页保留，但不应替代主学术落地页。

表头可直接复用 [templates/metadata_index_template.md](../templates/metadata_index_template.md)。

## 6. 关于 `BibTeX` 的要求

后续每篇论文都应尽量补齐可直接引用的 `BibTeX`，至少包括：

1. `title`
2. `author`
3. `year`
4. `booktitle` 或 `journal`
5. `pages`（若可得）
6. `doi`
7. `url`

如果还能拿到以下字段，也建议补齐：

1. `volume`
2. `number`
3. `publisher`
4. `abstract`
5. `keywords`

说明：

1. 标准 `BibTeX` 中通常不把 `abstract` 和 `keywords` 作为最核心引用字段，但在本路径中它们可作为扩展字段保留，以辅助后续初筛和方向判断。
2. 如果来源页无法直接提供完整 `BibTeX`，应综合出版社页、`Crossref` 和其他正式来源补齐到可引用程度。

## 7. 维护原则

1. 先补齐标题、作者、摘要、`DOI`、`BibTeX`、学术落地页。
2. 年份目录下默认按 `README.md + verification.json + metadata/*.json + venues/*.md` 统一维护，不要再额外拆出其他随意命名的零散文件。
3. 若需要给论文打 `方向标签`，默认先结合 [../CCF_SE_A_B_C.md](../CCF_SE_A_B_C.md) 建立 venue 级先验，再做一级总判定。
4. 再按 [../SOFTWARE_ENGINEERING_FIELD_TREE.md](../SOFTWARE_ENGINEERING_FIELD_TREE.md) 的 `X1 + D1-D4` 标准形成最小可追溯的判定依据。
5. 若论文跨域，则单独判断是否“软工主导”；只有最终落到 `软件工程` 时，才按 [../SOFTWARE_ENGINEERING_FIELD_TREE.md](../SOFTWARE_ENGINEERING_FIELD_TREE.md) 回填 `x.x.x` 级主路径。
6. 若扫论文时发现某类软工论文在现有 `x.x.x` 中没有自然落点，应先回到 [../SOFTWARE_ENGINEERING_FIELD_TREE.md](../SOFTWARE_ENGINEERING_FIELD_TREE.md) 扩树并同步说明，不要把论文硬塞进“最接近”的旧叶子。
7. 不要因为论文来自 `PL / systems / FM` venue 就自动将其视为软件工程论文。
8. 若任务要求逐篇终判，人工结论应直接写回 `metadata/*.json`；未写回的条目只能视为启发式初判。
9. venue 级先验默认统一使用 [../CCF_SE_A_B_C.md](../CCF_SE_A_B_C.md) 中的 `软工归属级别` 与 `氛围 A 🔥 / B 🟢 / C 🟡`，不要在年度页另造第二套 venue 分级。
10. 若需要表达 venue 跟踪先后顺序，默认先按 `氛围 A 🔥 / B 🟢 / C 🟡`，同档再参考 `完全属于软工 / 大部分属于软工 / 部分属于软工`，不要另造 `A/B/C/D` 跟踪制。
11. 逐篇论文层面默认沿用 `初筛 / pdf_followup` 字段，不再额外发明 `A/B/C/D` 第二套论文等级。
12. 先做轻量筛选，再决定是否值得获取全文。
13. 可先从近 `3-5` 年开始建立年度页，再逐步回溯。
14. 每个年份页在正式加入新 venue 时，应同步更新该年的汇总统计与 `venues/*.md`。

## 8. 标准工作流

若任务是“完成某一年的 `CCF` 保留子集论文名录”，默认按以下顺序执行：

1. 先确认 venue 范围以 [../CCF_SE_A_B_C.md](../CCF_SE_A_B_C.md) 为准。
2. 若任务同时涉及方向归类或软工边界判断，先读 [../CCF_SE_A_B_C.md](../CCF_SE_A_B_C.md) 与 [../SOFTWARE_ENGINEERING_FIELD_TREE.md](../SOFTWARE_ENGINEERING_FIELD_TREE.md)。
3. 在仓库根目录运行：

```bash
python -m tools.ccf_se_index_builder --year 2025
```

4. 检查 `frontier_index/ccf_history/2025/verification.json` 是否全部 `ok`。
5. 在仓库根目录继续运行：

```bash
python -m tools.ccf_se_classifier --year 2025
```

6. 若任务要求逐篇人工终判，把人工结论直接写回 `frontier_index/ccf_history/<year>/metadata/*.json`，再重跑分类器。
7. 若发现会议边界、重名文件、官方页缺失等问题，优先修构建脚本并重跑。
8. 若回填时发现一批论文没有自然 `x.x.x` 落点，先扩 [../SOFTWARE_ENGINEERING_FIELD_TREE.md](../SOFTWARE_ENGINEERING_FIELD_TREE.md) 再更新分类脚本并重跑，不要为了赶进度把它们硬塞到旧路径。
9. 最后再回写 [../SUMMARY.md](../SUMMARY.md) 里的统计与更新日志。

补充约束：

1. `metadata/*.json` 默认既是脚本生成产物，也是最终保留载体。
2. `venues/*.md` 默认是脚本生成的可重建产物，用于承载单个 venue 的逐篇名录。
3. 构建缓存位于仓库根目录 `.cache/ccf_se_index/<year>/`，不属于年度索引正式内容。
4. 后续若某些论文被选中进入全文阶段，再转入正式论文集路径处理 `paper.pdf / paper_content.txt / bibtex.bib`。
