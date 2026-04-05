# `ccf_history/` README

## 1. 路径定位

`ccf_history/` 用于存放 `CCF` 软件工程/系统软件/程序设计语言方向 `A/B/C` 类期刊会议的往年论文索引。

这里默认只存“元数据索引结果”，不直接存全文。

## 2. 推荐组织方式

后续默认按“**年份主目录**”组织，例如：

```text
ccf_history/
├── 2025/
│   └── README.md
├── 2024/
│   └── README.md
└── 2023/
    └── README.md
```

这样做的目的，是让每个年份目录直接代表“该年所有目标期刊会议的整体信息汇总”，便于从年度视角做横向观察和筛选。

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
2. 每个期刊/会议在该年的关键信息页。
3. 该期刊/会议在该年的论文名录。
4. 每篇论文的元数据、摘要/方向、`DOI`、官方页面与 `BibTeX`。
5. 对每篇论文的初步判定结果。
6. 对“哪些论文虽然在 `CCF` 大类里，但并不属于软件工程”的边界说明。
7. 对纳入软工语料的论文给出 `x.x.x` 级软工主路径。

## 4. 单个年份 `README.md` 的建议结构

每个年份目录下的 [README.md](./year_template/README.md) 默认建议包含：

1. 该年说明
2. 该年汇总统计
3. 该年覆盖 venue 列表
4. 每个 venue 一个独立 section

每个 venue section 默认应包含：

1. `venue` 基本信息
   - 缩写
   - 全称
   - `CCF` 等级
   - 类型
2. 该年的关键信息页面
   - 官方主页
   - `CFP`
   - 程序页 / proceedings / volume / issue 页
3. 论文名录表
   - 标题
   - 作者
   - 论文做什么的一句话
   - 一级总判定
   - 软工纳入判定
   - 软工主路径（`x.x.x`）
   - 软工次路径/标签
   - 判定依据（`X1/D1-D4`）
   - `DOI`
   - 官方落地页
   - 摘要或摘要简述
   - `BibTeX`
   - 初筛
   - `PDF` 跟进
4. 本 venue 在该年的简要观察

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
2. 年份目录下默认按 venue 分 section 统一维护，不要把同一年拆成很多零散碎文件。
3. 若需要给论文打 `方向标签`，默认先结合 [../CCF_SE_A_B_C.md](../CCF_SE_A_B_C.md) 建立 venue 级先验，再做一级总判定。
4. 再按 [../SOFTWARE_ENGINEERING_FIELD_TREE.md](../SOFTWARE_ENGINEERING_FIELD_TREE.md) 的 `X1 + D1-D4` 标准形成最小可追溯的判定依据。
5. 若论文跨域，则单独判断是否“软工主导”；只有最终落到 `软件工程` 时，才按 [../SOFTWARE_ENGINEERING_FIELD_TREE.md](../SOFTWARE_ENGINEERING_FIELD_TREE.md) 回填 `x.x.x` 级主路径。
6. 若扫论文时发现某类软工论文在现有 `x.x.x` 中没有自然落点，应先回到 [../SOFTWARE_ENGINEERING_FIELD_TREE.md](../SOFTWARE_ENGINEERING_FIELD_TREE.md) 扩树并同步说明，不要把论文硬塞进“最接近”的旧叶子。
7. 不要因为论文来自 `PL / systems / FM` venue 就自动将其视为软件工程论文。
8. 先做轻量筛选，再决定是否值得获取全文。
9. 可先从近 `3-5` 年开始建立年度页，再逐步回溯。
10. 每个年份页在正式加入新 venue 时，应同步更新该年的汇总统计。

## 8. 标准工作流

若任务是“完成某一年的 `CCF` 全量期刊会议论文名录”，默认按以下顺序执行：

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

6. 若发现会议边界、重名文件、官方页缺失等问题，优先修构建脚本并重跑。
7. 若回填时发现一批论文没有自然 `x.x.x` 落点，先扩 [../SOFTWARE_ENGINEERING_FIELD_TREE.md](../SOFTWARE_ENGINEERING_FIELD_TREE.md) 再更新分类脚本并重跑，不要为了赶进度把它们硬塞到旧路径。
8. 最后再回写 [../SUMMARY.md](../SUMMARY.md) 里的统计与更新日志。

补充约束：

1. `metadata/*.json` 与 `bib/*.bib` 默认视为脚本生成产物。
2. `_cache/` 是重跑加速缓存，应保留。
3. 后续若某些论文被选中进入全文阶段，再转入正式论文集路径处理 `paper.pdf / paper_content.txt / bibtex.bib`。
