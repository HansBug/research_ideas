# `frontier_index/` SUMMARY

## 1. 当前整体状态

- 路径状态：`已初始化并进入可维护状态`
- 已建立核心文档：`10` 份
- 已建立正式论文索引批次：`1`
- 已收录具体论文条目：`5153`
- 已准备好的 `CCF` venue 名录：`57` 个
- 已准备好的 `arXiv` 入口：`1` 个主入口

## 2. 当前已完成的索引批次

### 2.1 `CCF 2025` 年度索引

1. 年度总页：
   - [ccf_history/2025/README.md](./ccf_history/2025/README.md)
2. 逐 venue 名录目录：
   - [ccf_history/2025/venues/](./ccf_history/2025/venues)
3. 逐 venue 复核文件：
   - [ccf_history/2025/verification.json](./ccf_history/2025/verification.json)
4. 结构化元数据目录：
   - [ccf_history/2025/metadata/](./ccf_history/2025/metadata)
5. `BibTeX` 与终判字段存储方式：
   - 已直接内嵌到 [ccf_history/2025/metadata/](./ccf_history/2025/metadata) 中，不再单独维护 `bib/` 或 `manual_review/` 目录

当前状态：

1. 覆盖 venue 数量：`57`
2. 期望条目数：`5153`
3. 实际条目数：`5153`
4. 复核结果：`57/57` 个 venue 全部 `ok`
5. `metadata` 文件数：`57`
6. 独立 `bib` 文件数：`0`
7. 独立人工复核覆盖目录：`0`

字段概况：

1. 缺 `doi` 条目：`0`
2. 缺官方落地页条目：`0`
3. 缺摘要条目：`1038`
   - 主要是 `OpenAlex` 未返回摘要或 publisher 元数据较薄的条目。
4. 自动初筛分布：
   - `🟢 优先跟进`：`1408`
   - `🟡 保留观察`：`2645`
   - `⚪ 暂不跟进`：`201`
   - `⏳ 待补信息`：`899`
5. 一级总判定分布：
   - `软件工程`：`3430`
   - `跨域/待判定`：`972`
   - `程序设计语言与形式化基础`：`510`
   - `系统软件`：`241`
6. 软工纳入判定分布：
   - `属于软件工程`：`3324`
   - `跨域但软工主导`：`106`
   - `不属于软件工程`：`1723`
7. 软工主路径覆盖：
   - `3430/3430` 条被纳入软工语料的论文都已回填 `se_primary_path`
8. 分类终判状态：
   - 当前年度页已改为区分 `classification_source` 与 `manual_review_status`
   - 当前 `5153` 条论文的终判字段已直接写回 `metadata/*.json`
   - `人工复核`：`5153`
   - `启发式初判`：`0`
   - 当前 `2025` 条目已全部固化为嵌入式人工终判，可视为保留范围内的逐篇人工终判完成

## 3. 当前已准备好的入口

### 3.1 `CCF` 方向入口

1. `CCF` 分类总入口：
   - <https://www.ccf.org.cn/Academic_Evaluation/By_category/>
2. `CCF` 软件工程/系统软件/程序设计语言分类页：
   - <https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/>
3. 本仓库内整理后的名录文档：
   - [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md)
4. `2026` 投稿日期与主页核查表：
   - [CCF_SE_2026_DEADLINES.md](./CCF_SE_2026_DEADLINES.md)

### 3.2 `arXiv` 方向入口

1. `arXiv cs.SE recent`：
   - <https://arxiv.org/list/cs.SE/recent>

### 3.3 Python 工具入口

1. 工具总入口：
   - [../tools/README.md](../tools/README.md)
2. `CCF` 年度索引工作流：
   - [../tools/ccf_se_index_workflow.md](../tools/ccf_se_index_workflow.md)
3. 年度索引生成脚本：
   - [../tools/ccf_se_index_builder.py](../tools/ccf_se_index_builder.py)
4. 年度软工分类脚本：
   - [../tools/ccf_se_classifier.py](../tools/ccf_se_classifier.py)

### 3.4 软件工程方向分类基线

1. 领域方向树与边界说明：
   - [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md)
2. 默认用途：
   - 用于判断一篇论文是否属于软件工程。
   - 用于按 `X1 + D1-D4` 给出可追溯的单篇论文判定依据。
   - 用于先做 `软件工程 / 系统软件 / 程序设计语言与形式化基础 / 跨域待判定` 的一级总判定。
   - 用于给软工论文，以及跨域但软工主导的论文，分配 `x.x.x` 级主路径与辅助路径。
   - 用于把 `x.x.x` 叶节点和典型论文例子对齐，减少后续分类漂移。

### 3.5 `CCF` venue 级先验入口

1. venue 名录、主体归属与软工归属级别：
   - [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md)
2. 默认用途：
   - 先判断一个 venue 默认更像 `软件工程`、`系统软件` 还是 `程序设计语言与形式化基础`。
   - 先判断一个 venue 是 `完全属于软工`、`大部分属于软工` 还是 `部分属于软工`。
   - 若需要表达跟踪优先级，直接使用 `氛围 A 🔥 / B 🟢 / C 🟡`，同档再结合 `软工归属级别`。
   - 明确这个 venue 的“主要方向与边界”分别在哪里，避免把非软工部分机械塞进软工树。

## 4. 当前已明确的工作原则

1. 本路径先做“元数据索引层”，不直接当全文文库使用。
2. `CCF` 年度索引优先通过脚本批量生成，并通过 `verification.json` 做逐 venue 复核。
3. 若发现 venue 边界、重名冲突、官方页回退等问题，应优先修脚本重跑，不手工补半成品。
4. 后续默认先整理元数据、`BibTeX`、`DOI`、摘要和学术落地页。
5. 后续若做方向归类，默认先看 [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md) 的 venue 级先验，再做单篇终判。
6. venue 跟踪优先级统一直接复用 [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md) 中的 `氛围 A 🔥 / B 🟢 / C 🟡`；同档再参考 `完全属于软工 / 大部分属于软工 / 部分属于软工`，不再另造 `A/B/C/D`。
7. 若论文跨域，则单独判断是否“软工主导”；只有最终落到 `软件工程` 时，才进入 [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md)。
8. 对纳入软工语料的论文，默认回填 `软工纳入判定 + 软工主路径（x.x.x） + 软工次路径/标签 + 判定依据（X1/D1-D4）`。
9. 若后续扫论文时发现现有 `x.x.x` 没有自然覆盖某类稳定题型，应先扩 [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md)，不要把论文硬塞进最接近的旧节点。
10. `ccf_se_index_builder.py` 当前负责生成基础元数据层；`ccf_se_classifier.py` 负责启发式初判、保留已写回终判并重渲染年度页。
11. 若任务要求“逐篇真正所属类型”的终判，默认直接把终判字段写回 `metadata/*.json`，并保留 `classification_source / manual_review_status / manual_review_note` 作为可追溯证据。
12. 先做初筛，再决定哪些论文值得获取 `PDF`。
13. 只有真正值得深入阅读的论文，才应迁移到正式论文集路径继续处理。
14. 当前 `CCF` 文库已收缩为“软件工程高相关且值得持续跟踪”的保留子集，不再在本路径中保留被筛出的 venue 与其年度数据。

## 5. 下一步建议

1. 基于 `2025` 年度索引，优先从 `🟢 优先跟进` 条目里挑选与形式化建模、验证、需求、修复更贴近的论文获取 `PDF`。
2. 优先从已判为 `属于软件工程` 或 `跨域但软工主导` 的条目里，再按 `x.x.x` 主路径筛出与你博士研究最贴近的论文批次。
3. 若后续在扫新增论文时发现新稳定题型没有自然 `x.x.x` 落点，优先扩树并统一回填，不要先把论文硬塞进旧标签。
4. 对 `⏳ 待补信息` 且与你博士研究高度相关的条目，优先补摘要或 publisher 侧信息。
5. 若继续扩年份，直接复用：

```bash
python -m tools.ccf_se_index_builder --year 2024
```

6. 若进入全文阶段，再转用 `tools/pdf_extractor.py` 和正式论文集规范。
7. `2025` 年条目已经完成全量人工终判；若后续扩展到新年份，继续沿用“直接写回 `metadata/*.json` 终判字段并重跑分类器”的流程推进。

## 6. 更新日志

- `2026-04-14 22:36:36`
  - 新增 [CCF_SE_2026_DEADLINES.md](./CCF_SE_2026_DEADLINES.md)，把 [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md) 当前保留的 `57` 个 `A/B/C` 软工相关 venue 全部补成一份 `2026` 投稿日期 / 主页核查表。
  - 执行口径明确收紧为“只认官方 `2026` 主页、`CFP`、important dates 或作者指南；官方没发就直接写 `未公布`；不按往年日期补空”。
  - 对 `ICSE/FSE/MSR/REFSQ` 等 conference-year 是 `2026`、但投稿窗口落在 `2025` 的 venue，保留官方真实日期，不做人为跨年平移。
  - 对期刊 venue，统一按“官方主页是否给出固定 `2026` 年度 `ddl`”回填；未见固定 `ddl` 的，只写“未见 `2026` 固定 `ddl`”，不伪造会务式时间线。

- `2026-04-06 16:40:38`
  - 统一 `CCF` 年度索引中的 venue 级归一化口径：以后只使用 `软工归属级别` 与 `氛围 A 🔥 / B 🟢 / C 🟡` 两列，不再保留任何独立 `A/B/C/D` 跟踪等级。
  - 把 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[ccf_history/README.md](./ccf_history/README.md)、[ccf_history/year_template/README.md](./ccf_history/year_template/README.md)、[../tools/README.md](../tools/README.md) 与 [../tools/ccf_se_index_workflow.md](../tools/ccf_se_index_workflow.md) 的说明统一到“年度总页 `README.md` + `venues/*.md` 单 venue 页”的结构。
  - 调整 [../tools/ccf_se_classifier.py](../tools/ccf_se_classifier.py) 的年度页说明，让生成页显式写清：venue 跟踪优先级直接看 `氛围`，同档再参考 `软工归属级别`；逐篇论文只沿用 `初筛 / PDF` 跟进排序。

- `2026-04-06 13:01:43`
  - 继续按“`2025` 终判依赖 LLM/人工逐篇复核，而不是依赖分类器启发式”的要求做 residual sweep，围绕剩余 false negative / false positive 边界条目补写人工终判字段。
  - 本轮新增 `34` 条 override 补丁，继续把 `compiler testing / fault localization / vulnerability detection / SLO monitoring / microservice self-adaptation / SE-focused review` 等条目恢复进软工，同时把 `battery optimization / blockchain consensus / federated learning optimization / theorem proving / SMT solver / compiler auto-tuning` 等非软工主问题条目移出。
  - 修正 [../tools/ccf_se_classifier.py](../tools/ccf_se_classifier.py) 的两个口径问题：补丁层优先级与人工终判计数统计保持一致。
  - 更新后 `2025` 年度统计为：`软件工程 3546`、`程序设计语言与形式化基础 1223`、`系统软件 520`、`跨域/待判定 1012`；软工纳入判定为 `属于软件工程 3410`、`跨域但软工主导 136`、`不属于软件工程 2755`。

- `2026-04-06 15:26:16`
  - 按“从文库中完全清掉 `D` 级与非目标 venue”的要求，把 `CCF` 侧范围收缩为 [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md) 当前保留的 `57` 个 software-engineering-oriented venue。
  - 同步删除 `2025` 年被筛出 venue 的 `metadata/*.json`、旧的独立 `BibTeX` 文件、外置人工终判批次文件以及年度目录内遗留缓存，并重算 [ccf_history/2025/verification.json](./ccf_history/2025/verification.json)。
  - 重跑 [../tools/ccf_se_classifier.py](../tools/ccf_se_classifier.py) 后，`2025` 年度页更新为：`5153` 条论文、`57` 个 venue、全部 `人工复核 / 已人工复核`。
  - 更新后 `2025` 年度统计为：`软件工程 3430`、`跨域/待判定 972`、`程序设计语言与形式化基础 510`、`系统软件 241`；软工纳入判定为 `属于软件工程 3324`、`跨域但软工主导 106`、`不属于软件工程 1723`。

- `2026-04-06 12:37:28`
  - 按“不要依赖 `ccf_se_classifier.py` 做 `2025` 终判”的要求，补做一轮以 `metadata` 原始题目/摘要为入口的 LLM 人工复核，重点回查路径明显不匹配的条目和被压成非软工的 false negatives。
  - 新增人工修正 `144` 条，其中 `57` 条用于清理 `1.2.3 / 6.4.1` 等误桶，`87` 条把明显属于软工的问题重新纳入软件工程主路径。
  - 同步改造 [../tools/ccf_se_classifier.py](../tools/ccf_se_classifier.py)：当年度条目已完成全量人工终判时，脚本不再依赖启发式分类结果，而是直接按终判结果回填与渲染。
  - 更新后 `2025` 年度统计为：`软件工程 3525`、`程序设计语言与形式化基础 1229`、`系统软件 521`、`跨域/待判定 1026`；软工纳入判定为 `属于软件工程 3410`、`跨域但软工主导 115`、`不属于软件工程 2776`。

- `2026-04-06 11:34:32`
  - 完成 `2025` 年度 `6301` 条论文的逐篇人工终判，并形成全量分 venue 终判批次。
  - 人工修正 `83` 条启发式误判，重点收紧了若干系统软件与 `PL/FM` 邻近条目，并补回 `ASE/ICSE/TOSEM/TSE/REFSQ` 中被误排除的软工条目。
  - 扩充 [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md)，新增 `6.3.5`“路线图、研究议程与领域回顾”，用于承接 roadmap / retrospective / research agenda 类软工论文。
  - 修订 [../tools/ccf_se_classifier.py](../tools/ccf_se_classifier.py) 的路径打分逻辑，过滤方向树中的过泛关键词，增强 `AI for SE` 子路径路由。

- `2026-04-06 01:32:51`
  - 把 [../tools/ccf_se_classifier.py](../tools/ccf_se_classifier.py) 改成“启发式初判 + 人工终判覆盖”的模式，新增 `classification_source / manual_review_status` 字段，并让年度页显示判定来源与人工复核状态。
  - 为 `2025` 年度建立逐篇人工复核写入口。
  - 先补入 `5` 条代表性人工复核样例，覆盖 `8` 个年度行项，并把典型 `AI for SE` 交叉样例收紧到 `跨域但软工主导 / 7.1.1`。
  - 同步更新 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[ccf_history/README.md](./ccf_history/README.md)、[../tools/README.md](../tools/README.md) 与 [../tools/ccf_se_index_workflow.md](../tools/ccf_se_index_workflow.md)，明确“脚本只做初判，终判以人工复核为准”。

- `2026-04-06 00:49:29`
  - 重新跑通 [../tools/ccf_se_classifier.py](../tools/ccf_se_classifier.py)，把 `macro_area` 与最终 `se_inclusion_decision` 的口径收紧到一致，不再保留“一级总判定是软件工程、但最终又判为非软工”的冲突条目。
  - 最终确认 `2025` 年度 `6301` 条论文中，`3525` 条纳入软工语料且全部拥有 `se_primary_path`，其余条目落在 `程序设计语言与形式化基础 / 系统软件 / 跨域待判定`。

- `2026-04-06 00:38:29`
  - 新增 [../tools/ccf_se_classifier.py](../tools/ccf_se_classifier.py)，把 `2025` 年度 `6301` 条论文全部回填到 `macro_area / se_inclusion_decision / cross_domain_flag / se_primary_path / se_primary_label / se_secondary_paths / se_decision_basis`。
  - 重写 [ccf_history/2025/README.md](./ccf_history/2025/README.md)，先把年度总页升级为“一级总判定 + 软工纳入判定 + `x.x.x` 主路径 + 判定依据”的分类版；后续又进一步拆分为“年度总页 + `venues/*.md` 单 venue 页”。
  - 同步更新 [../tools/README.md](../tools/README.md) 与 [../tools/ccf_se_index_workflow.md](../tools/ccf_se_index_workflow.md)，把标准流程固定为 `builder -> classifier`。

- `2026-04-05 23:42:35`
  - 进一步把“分类树持续扩充”制度化：明确后续扫论文时，若现有 `x.x.x` 没有自然覆盖某类稳定题型，应先扩树再分类，禁止把论文硬塞到旧路径。
  - 同步更新 [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md)、[README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[ccf_history/README.md](./ccf_history/README.md) 与 [../CLAUDE.md](../CLAUDE.md)，把该规则落到执行入口与维护流程。

- `2026-04-05 21:50:18`
  - 继续扩展 [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md)，把 `x.x.x` 方向树补成“ASCII 树 + 二级方向下的 `x.x.x` 典型例子总览 + `X1/D1-D4` 可执行判定矩阵”的准综述版本。
  - 继续重写 [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md)，把 `82` 个 venue 的主要方向统一改写为“主体问题簇 + 软工边界”的同一套话语体系，并收紧了部分交叉 venue 的归属说明。
  - 同步更新 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[ccf_history/README.md](./ccf_history/README.md)、模板文件、[../tools/README.md](../tools/README.md)、[../tools/ccf_se_index_workflow.md](../tools/ccf_se_index_workflow.md) 与 [../CLAUDE.md](../CLAUDE.md)，把后续维护口径统一到 `一级总判定 + 软工纳入判定 + 软工主路径（x.x.x） + 判定依据（X1/D1-D4）`。
  - 修复 [../tools/ccf_se_index_builder.py](../tools/ccf_se_index_builder.py) 对 [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md) 表格扩列后的解析兼容性，避免后续重跑时 venue 名录读空。

- `2026-04-05 23:35:39`
  - 基于 `2025` 年度 `6301` 条元数据再次复核 [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md) 的覆盖性，确认“所有二级方向统一四个叶子”并不合理。
  - 按语料与公开学术资料补出若干稳定叶子，包括架构决策、测试债务/脆弱测试、技术债治理、文档与 rationale 恢复、功能安全、`AI` 支持架构设计、`SE for AI` 需求建模，以及 scientific/HPC 软件工程。
  - 在方向树文档中新增“覆盖复核结论”，明确后续分类树允许继续扩叶，不以对称结构为约束。

- `2026-04-05 21:10:45`
  - 把 [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md) 扩展为 `x.x.x` 级的软件工程三级方向树，并为每个叶子路径补充了典型论文问题/例子。
  - 在方向树文档中新增“单篇论文是否属于软件工程”的可执行、可检查判定标准。
  - 全面重写 [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md)，为 `82` 个 venue 增补主体归属、软工归属级别与典型软工路径。
  - 同步更新 `README/GUIDE/SUMMARY/ccf_history/README` 与模板文件，把后续回填口径统一为 `一级总判定 + 软工纳入判定 + 软工主路径（x.x.x）`。

- `2026-04-05 17:16:04`
  - 新增 [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md)，建立 `frontier_index/` 当前默认使用的软件工程学术方向树。
  - 把 `SWEBOK`、`ICSE 2025`、`MSR`、`ICST`、`REFSQ`、`MODELS`、`ICSA`、`FoSE 2000`、`SEI 2021` 与 `CCF` 官方大类页整合为一份面向索引维护的准综述型分类基线。
  - 更新 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[ccf_history/README.md](./ccf_history/README.md) 与模板文件，明确后续应先做 `软件工程 / 系统软件 / 程序设计语言与形式化基础 / 跨域待判定` 的一级总判定。

- `2026-04-05 16:46:25`
  - 完成 `CCF 2025` 年度索引全量生成。
  - 产出 [ccf_history/2025/README.md](./ccf_history/2025/README.md)、[ccf_history/2025/verification.json](./ccf_history/2025/verification.json)、`metadata/*.json`。
  - 修复并固化了官方页回退、同缩写 venue 文件冲突、proceedings 元条目误收、旧版 `DBLP` 链接兼容等规则。
  - 新增 [../tools/README.md](../tools/README.md)，并把 [../tools/ccf_se_index_builder.py](../tools/ccf_se_index_builder.py) 与 [../tools/ccf_se_index_workflow.md](../tools/ccf_se_index_workflow.md) 接入 `frontier_index` 文档入口。

- `2026-04-05 03:01:03`
  - 新建 `frontier_index/` 顶层路径。
  - 建立 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)。
  - 建立 [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md)，整理 `CCF` 软件工程/系统软件/程序设计语言方向 `A/B/C` 期刊会议名录、方向和索引入口。
  - 建立 [ccf_history/README.md](./ccf_history/README.md)、[arxiv_recent/README.md](./arxiv_recent/README.md) 与 [templates/metadata_index_template.md](./templates/metadata_index_template.md)，为后续批量索引准备目录和模板。
