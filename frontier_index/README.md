# `frontier_index/` README

## 1. 路径定位

`frontier_index/` 是本仓库面向“前沿论文信息”的顶层索引入口。它当前不承担“正式全文文库”的职责，而是先承担一个更前置、更轻量的职责：

1. 维护 `CCF` 软件工程/系统软件/程序设计语言方向 `A/B/C` 类期刊会议的往年论文信息索引入口。
2. 维护近期 `arXiv` 上软件工程方向论文的滚动索引入口。
3. 先积累论文元数据、`BibTeX`、`DOI`、学术站落地页链接和初步判断结果，再决定哪些论文值得进一步获取 `PDF` 做深读。

换言之，这里是“前沿索引层”，不是“一上来就把全文都下载回来”的正式文库层。

## 2. 设立宗旨与期望收获

单独建立本路径，是为了把“前沿论文搜集与初筛”从“正式文库建设与全文精读”中拆开，避免后续工作一开始就陷入高成本全文处理。

这里期望持续沉淀的内容包括：

1. 各重点 venue 的稳定名录、方向边界和索引入口。
2. 按年份或按批次组织的论文元数据索引。
3. 对论文进行第一轮轻量筛查所需的基础信息：
   - 会议/期刊；
   - 年份；
   - 标题；
   - 作者；
   - 摘要；
   - `DOI`；
   - `BibTeX`；
   - 学术站落地页链接。
4. 面向后续正式读文献的候选优先级判断，例如：
   - 是否与形式化建模、状态机、验证、修复、需求工程、软件可靠性、运行时验证相关；
   - 是否明显涉及控制系统、嵌入式系统、`CPS`、时序约束或形式化方法；
   - 是否值得获取 `PDF` 并迁移到正式论文集继续深读。

## 3. 收录范围

本路径当前优先覆盖两类来源：

1. `CCF` 软件工程/系统软件/程序设计语言方向 `A/B/C` 类期刊会议的往年论文。
2. `arXiv` 上近期的软件工程方向论文，优先关注 `cs.SE`，并视需要补充和软件工程高度相关的交叉方向。

这里的“收录”当前默认指“收录索引信息”，不是“收录完整论文全文材料”。

### 3.1 当前优先关注的信息

后续每篇论文默认优先整理以下字段：

1. `title`
2. `authors`
3. `venue`
4. `year`
5. `type`（期刊 / 会议 / arXiv）
6. `rank`（如适用，记录 `CCF A/B/C`）
7. `macro_area`
8. `se_inclusion_decision`
9. `cross_domain_flag`
10. `se_primary_path`
11. `se_secondary_paths`
12. `se_decision_basis`
13. `abstract`
14. `keywords`（若来源页可得）
15. `doi`
16. `landing_url`
17. `dblp_url` 或其他学术索引页
18. `bibtex`
19. `initial_screening`
20. `pdf_followup`

其中 `landing_url` 指学术站落地页，而不是直接 `PDF` 下载链接。默认优先记录出版社页、`DBLP`、`OpenReview`、`arXiv abstract` 页、`ACM DL`、`IEEE Xplore`、`Springer`、`Elsevier` 等正式学术入口。

## 4. 不应在这里做的事情

以下工作当前不应直接作为本路径的主任务：

1. 不经过初筛，就批量下载大量 `PDF`。
2. 把这里做成“正式全文文库”或“paper.pdf` 仓库”。
3. 仅凭标题印象就写深入分析，跳过摘要和基础元数据。
4. 收录与软件工程/系统软件/程序设计语言主线明显无关的泛计算机论文。
5. 混入博客、新闻、宣传页或无稳定学术元信息的非正式材料。

## 5. 这里与正式文库的分工

后续默认采用两阶段流程：

1. **索引阶段**
   - 在本路径下整理元数据、`BibTeX`、`DOI`、学术落地页、摘要和初筛结论。
2. **深读阶段**
   - 只把经过初筛、确实值得投入的论文，进一步获取 `PDF`，再迁移或纳入到真正的论文集路径中，补 `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`desc.md` 等正式材料。

这个分层的目的，是先用低成本方式建立广覆盖前沿视野，再把阅读成本集中投到真正值得深读的部分。

## 6. 当前文件说明

本路径当前包含以下核心文档：

1. [README.md](./README.md)
   - 说明本路径的定位、边界、目标和后续使用方式。
2. [GUIDE.md](./GUIDE.md)
   - 规定后续如何维护索引、如何做初筛、如何控制“只积累元数据不急着下载全文”的工作流。
3. [SUMMARY.md](./SUMMARY.md)
   - 记录当前已经准备好的基础信息、后续待做事项和更新日志。
4. [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md)
   - 汇总 `CCF` 软件工程/系统软件/程序设计语言方向 `A/B/C` 类期刊会议名录、venue 主体归属、软工归属级别、主要方向与边界说明和索引入口。
5. [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md)
   - 给出当前 `frontier_index/` 使用的软件工程三级方向树、`X1 + D1-D4` 单篇软工判定标准、跨域处理规则，以及 `x.x.x` 主路径分类规则与典型例子总览。
   - 该树默认允许按覆盖需要继续扩叶，不以固定 `4` 叉结构为约束。
   - 后续扫论文时，如果发现某类软工论文没有自然落点，应先扩树再分类，禁止为了维持旧结构把论文硬塞进现有叶子。
6. [ccf_history/README.md](./ccf_history/README.md)
   - 规定后续 `CCF` 往年论文索引如何按“年份主目录”组织，并在每年内按 venue 分 section 汇总。
7. [arxiv_recent/README.md](./arxiv_recent/README.md)
   - 规定后续近期 `arXiv` 论文索引如何按时间窗口组织。
8. [templates/metadata_index_template.md](./templates/metadata_index_template.md)
   - 提供后续单批次索引可直接复用的元数据表头模板。
9. [../tools/README.md](../tools/README.md)
   - 汇总本仓库内与索引构建、全文提取相关的 Python 工具入口。
10. [../tools/ccf_se_index_workflow.md](../tools/ccf_se_index_workflow.md)
   - 规定 `CCF` 年度索引的标准批量构建、软工分类回填与复核流程。

推荐阅读顺序如下：

1. 先读 [README.md](./README.md)
2. 再读 [GUIDE.md](./GUIDE.md)
3. 再读 [SUMMARY.md](./SUMMARY.md)
4. 若任务涉及“哪些论文算软件工程、哪些只是系统软件或程序设计语言邻近项、单篇论文的可执行判定标准是什么”，先读 [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md)
5. 若要从 `CCF` 方向入手建索引，再读 [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md)，先建立 venue 级先验
6. 若要实际新建索引批次，再读 [ccf_history/README.md](./ccf_history/README.md) 或 [arxiv_recent/README.md](./arxiv_recent/README.md)
7. 若要批量构建 `CCF` 年度页，再读 [../tools/ccf_se_index_workflow.md](../tools/ccf_se_index_workflow.md)

## 7. 后续准备好的工作模式

后续在本路径下，默认按下面的顺序推进：

1. 先确定来源批次
   - `CCF` 某一年整体范围；
   - 或 `arXiv` 某个近期时间窗口。
2. 先做一级总判定
   - `软件工程`；
   - `系统软件`；
   - `程序设计语言与形式化基础`；
   - `跨域/待判定`。
3. 只整理元数据和基础证据
   - 标题、作者、摘要、`BibTeX`、`DOI`、学术链接。
4. 结合 [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md) 的 venue 级先验，再按 [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md) 的 `X1 + D1-D4` 标准做单篇最终判定。
5. 若论文最终被判为 `属于软件工程` 或 `跨域但软工主导`，再回填：
   - `软工纳入判定`
   - `软工主路径（x.x.x）`
   - `软工次路径/标签`
   - `软工判定依据（X1/D1-D4）`
6. 再做初步判定
   - 基于会议/期刊、年份、标题、摘要、关键词做轻量筛选。
7. 再选择容易关注、且与博士研究更相关的一部分
   - 再去获取 `PDF`。
8. 最后才进入正式文库建设
   - 做全文提取、单篇分析和更深入归档。

对于 `CCF` 年度索引，默认优先使用 Python 工具而不是手工拼整年总表：

```bash
python -m tools.ccf_se_index_builder --year 2025
```

基础元数据生成完成后，再运行：

```bash
python -m tools.ccf_se_classifier --year 2025
```

如需进入全文阶段，再转用 [../tools/pdf_extractor.py](../tools/pdf_extractor.py)。

## 8. AI 工作入口提示

后续 AI 在本路径下工作时，默认应遵守以下原则：

1. 先把本路径当成“索引层”，不要一上来就按正式论文库处理。
2. 优先补元数据和初筛结果，再考虑下载全文。
3. 若任务涉及 `CCF` 方向 venue 范围判断，优先参考 [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md)。
4. 若任务涉及“什么算软件工程”“非软工论文如何判出”“跨域论文怎么处理”“软工论文如何落到 `x.x.x` 路径”，优先参考 [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md)。
5. 方向归类时，先看 [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md) 的 venue 级先验，再做一级总判定和单篇终判。
6. 对纳入软工语料的论文，默认回填 `软工纳入判定 + 软工主路径（x.x.x） + 软工次路径/标签 + 软工判定依据（X1/D1-D4）`。
7. 若批量扫论文时发现现有 `x.x.x` 没有自然覆盖某一稳定题型，应先更新 [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md) 及相关说明，再回填分类，不要把论文硬塞到“最接近”的旧路径。
8. 若任务涉及批量索引新增，先读 [GUIDE.md](./GUIDE.md) 和 [SUMMARY.md](./SUMMARY.md)。
9. 若任务是构建某一年的 `CCF` 全量索引，先用 [../tools/ccf_se_index_builder.py](../tools/ccf_se_index_builder.py) 生成基础元数据，再用 [../tools/ccf_se_classifier.py](../tools/ccf_se_classifier.py) 回填软工判定与 `x.x.x` 路径，最后按 [../tools/ccf_se_index_workflow.md](../tools/ccf_se_index_workflow.md) 做复核。
10. 若后续某批论文已经明确要深读，再转入其他正式论文集路径，不要把全文阅读工作反压到本路径中。
