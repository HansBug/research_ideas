# `frontier_index/` 操作规范

本文档用于固定 [README.md](./README.md)、[SUMMARY.md](./SUMMARY.md) 与本路径后续索引工作的统一维护方式。

## 1. 文档关系与使用顺序

`frontier_index/` 下的几个核心文档分工如下：

1. [README.md](./README.md)
   - 负责说明本路径为什么存在、收什么、不收什么，以及这里为什么只做“元数据索引层”。
2. [GUIDE.md](./GUIDE.md)
   - 负责规定后续如何做来源选择、元数据整理、初筛、去重和回填。
3. [SUMMARY.md](./SUMMARY.md)
   - 负责记录当前基础建设状态、已准备好的入口、下一步计划和更新日志。
4. [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md)
   - 负责固定 `CCF` 软件工程/系统软件/程序设计语言方向 `A/B/C` 期刊会议名录及索引入口。

推荐阅读顺序如下：

1. [README.md](./README.md)
2. [GUIDE.md](./GUIDE.md)
3. [SUMMARY.md](./SUMMARY.md)
4. 需要做 `CCF` venue 索引时，再读 [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md)

## 2. 目标与任务边界

本路径的目标是建立“前沿论文元数据索引 + 初筛决策层”，而不是直接建立全文论文库。

本路径应完成的事：

1. 固定重点来源和重点 venue 列表。
2. 为后续批量整理论文元数据建立统一字段口径。
3. 先完成轻量级初筛，减少后续全文获取与深读成本。
4. 形成“哪些论文值得进一步拿 `PDF`”的候选池。

本路径不应承担的事：

1. 不应把所有候选论文都变成 `paper.pdf` 目录。
2. 不应把深度单篇分析大量写在本路径。
3. 不应在这里替代正式论文集的 `paper_content.txt / desc.md` 工作。

## 3. 来源优先级

后续整理元数据时，默认按以下优先级取源：

1. **官方来源**
   - `CCF` 官方分类页；
   - 会议/期刊官网；
   - `arXiv` 官方页面；
   - 出版社正式论文页。
2. **学术索引来源**
   - `DBLP`；
   - `OpenReview`；
   - `Crossref`；
   - `Semantic Scholar` 等。
3. **补充来源**
   - 作者主页；
   - 实验室主页；
   - 官方 artifact / supplemental 页面。

默认要求如下：

1. 标题、作者、年份、venue 以官方页或稳定学术索引页为准。
2. `doi` 优先从出版社页或 `Crossref` 获取。
3. `BibTeX` 优先从 `DBLP`、出版社页或 `Crossref` 获取。
4. `landing_url` 必须优先记录学术落地页，而不是直接 PDF。
5. 如果同一论文存在多个可选链接，默认优先顺序为：
   - 出版社正式页；
   - `DBLP`；
   - `OpenReview`；
   - `arXiv abstract` 页；
   - 其他学术资料页。

## 4. 元数据字段标准

后续在本路径下新增论文索引时，单条论文记录默认至少应包含以下字段：

1. `title`
2. `authors`
3. `venue_abbr`
4. `venue_full`
5. `year`
6. `type`
7. `rank`
8. `abstract`
9. `keywords`
10. `doi`
11. `landing_url`
12. `dblp_url`
13. `bibtex`
14. `initial_screening`
15. `screening_reason`
16. `pdf_followup`
17. `notes`

其中状态字段默认使用以下口径：

1. `initial_screening`
   - `🟢 优先跟进`
   - `🟡 保留观察`
   - `⚪ 暂不跟进`
   - `⏳ 待补信息`
2. `pdf_followup`
   - `🟢 建议获取 PDF`
   - `🟡 可选获取`
   - `⚪ 暂不获取`
   - `⏳ 未判断`

## 5. 初筛标准

后续默认先做“轻量级初筛”，主要依据以下信息：

1. 会议/期刊本身的方向。
2. 论文年份。
3. 标题中的任务词。
4. 摘要中的对象、方法和问题设定。
5. 关键词中的形式化方法、软件工程、控制系统、模型、验证等线索。

### 5.1 优先跟进的典型信号

以下信号默认应提高优先级：

1. 论文明确涉及：
   - `formal methods`
   - `model checking`
   - `state machine`
   - `requirements engineering`
   - `runtime verification`
   - `software testing`
   - `software reliability`
   - `program analysis`
   - `model-driven engineering`
   - `repair`
   - `synthesis`
2. 论文对象与博士研究相关：
   - 控制系统；
   - 嵌入式系统；
   - 工业系统；
   - 安全关键系统；
   - `CPS`；
   - 时序/实时系统。
3. 论文标题或摘要明显包含：
   - `LLM`
   - `requirements`
   - `statechart`
   - `state machine`
   - `automata`
   - `timed`
   - `verification`
   - `repair`
   - `formal`
   - `specification`

### 5.2 降优先级或暂不跟进的典型信号

以下情况默认应降权：

1. 虽然 venue 在 `CCF` 名录里，但标题和摘要与当前博士研究主线明显偏离。
2. 主要是纯系统性能、纯网络基础设施或纯编译优化问题，与建模/验证/需求/修复关系较弱。
3. 只在软件工程 broad venue 中出现，但摘要没有形式化、建模、分析、验证、测试或可靠性线索。
4. 信息严重不全，短期内无法补齐摘要、`doi` 或基本落地页。

## 6. 去重与一致性规则

后续新增索引时，默认按以下顺序去重：

1. 先按 `doi` 去重。
2. `doi` 缺失时按标准化标题去重。
3. 标题存在轻微差异时，再结合作者、年份、venue 做人工判断。

一致性检查至少包括：

1. `venue_abbr` 与 `venue_full` 是否对应。
2. `rank` 是否与 [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md) 一致。
3. `landing_url` 是否为学术落地页而非裸 PDF。
4. `initial_screening` 与 `screening_reason` 是否匹配。
5. `pdf_followup` 是否与初筛结果一致。

## 7. 后续索引文件的建议组织方式

虽然当前还没有正式批量写入索引文件，但后续默认建议采用以下结构：

1. `CCF` 往年论文索引
   - 建议按 `year -> README.md` 组织。
   - 每个年份目录负责汇总该年所有目标 venue。
   - 目录内以 venue section 的方式统一维护，不再默认拆成“一个 venue 一个年份文件”。
2. `arXiv` 近期论文索引
   - 建议按时间窗口组织。
   - 例如：`2026-04.md`

单个索引文件中，默认优先采用 Markdown 表格维护；如果后续量级显著上升，再考虑在不破坏可读性的前提下补充结构化导出文件。

## 8. 一轮推荐工作流程

后续每一轮新增索引时，推荐按以下顺序进行：

1. 先选定来源批次
   - 某个 `CCF` 年份；
   - 或某个 `arXiv` 时间窗口。
2. 批量整理基础元数据
   - 标题、作者、摘要、`BibTeX`、`DOI`、落地页。
3. 批量做初筛
   - 不要看到一篇就立刻转入全文获取。
4. 回写筛选结果
   - 明确哪些是 `🟢`、哪些是 `🟡`、哪些是 `⚪`。
5. 最后才确定 `PDF` 跟进名单
   - 只把最值得深读的一部分推进到正式文库。

### 8.1 `CCF` 年份索引的固定展开方式

后续每个 `CCF` 年份目录下的 `README.md`，默认应按下面顺序展开：

1. 年份范围说明
2. 当年覆盖的 venue 清单
3. 每个 venue 一个独立 section

每个 venue section 默认至少包含：

1. venue 基本信息
   - 缩写
   - 全称
   - `CCF` 等级
   - 类型（会议 / 期刊）
2. 该 venue 在该年的关键信息页
   - 官方主页
   - `CFP` / `Call for Papers`
   - 程序页 / proceedings 页 / volume 页 / issue 页
   - 若有最佳论文、主题说明、重要时间线，也可补充
3. 论文名录表
   - 每篇论文都应尽量给出：
     - 标题
     - 作者
     - 论文主要内容一句话
     - `DOI`
     - 官方落地页
     - 摘要或摘要简述
     - 方向标签
     - `BibTeX`
     - 初筛结果
     - `PDF` 跟进建议

默认要求如下：

1. `官方落地页` 优先使用出版社或官方 proceedings 页：
   - `ACM DL`
   - `IEEE Xplore`
   - `Springer`
   - `Elsevier`
   - `USENIX`
   - 其他正式 publisher / society 页面
2. 不应优先使用：
   - `DBLP` 作为主落地页
   - 各种二次导航页
   - 博客式转发页
3. `BibTeX` 应尽量达到“可直接引用”的程度，至少应覆盖：
   - `title`
   - `author`
   - `year`
   - `booktitle` / `journal`
   - `pages`（若可得）
   - `doi`
   - `url`
4. 对会议论文，若能拿到 proceedings 页或 session 信息，可附在 venue section 的说明中。
5. 对期刊论文，若是按 volume / issue 汇总，优先记录该年的 volume / issue 入口页。

## 9. SUMMARY.md 维护要求

[SUMMARY.md](./SUMMARY.md) 主要用于记录本路径的“整体状态”，不是每条论文的明细总账。

后续维护时，默认应包含：

1. 当前已准备好的基础文档和入口。
2. 当前已纳入的来源范围。
3. 当前已正式建立的索引批次数量。
4. 当前已确定的高优先级跟进方向。
5. 更新日志。

`SUMMARY.md` 不应被写成机械堆积的检索流水账；每次更新都应做整合压缩，只保留对下一轮工作仍有指导价值的要点。
