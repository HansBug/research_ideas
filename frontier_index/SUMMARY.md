# `frontier_index/` SUMMARY

## 1. 当前整体状态

- 路径状态：`已初始化并进入可维护状态`
- 已建立核心文档：`10` 份
- 已建立正式论文索引批次：`1`
- 已收录具体论文条目：`6301`
- 已准备好的 `CCF` venue 名录：`82` 个
- 已准备好的 `arXiv` 入口：`1` 个主入口

## 2. 当前已完成的索引批次

### 2.1 `CCF 2025` 年度索引

1. 年度总页：
   - [ccf_history/2025/README.md](./ccf_history/2025/README.md)
2. 逐 venue 复核文件：
   - [ccf_history/2025/verification.json](./ccf_history/2025/verification.json)
3. 结构化元数据目录：
   - [ccf_history/2025/metadata/](./ccf_history/2025/metadata)
4. `BibTeX` 目录：
   - [ccf_history/2025/bib/](./ccf_history/2025/bib)

当前状态：

1. 覆盖 venue 数量：`82`
2. 期望条目数：`6301`
3. 实际条目数：`6301`
4. 复核结果：`82/82` 个 venue 全部 `ok`
5. `metadata` 文件数：`82`
6. `bib` 文件数：`82`

字段概况：

1. 缺 `doi` 条目：`54`
   - 当前主要来自 `OSDI` 等无 DOI 或 DOI 不稳定的来源。
2. 缺官方落地页条目：`0`
3. 缺摘要条目：`1274`
   - 主要是 `OpenAlex` 未返回摘要或 publisher 元数据较薄的条目。
4. 自动初筛分布：
   - `🟢 优先跟进`：`1736`
   - `🟡 保留观察`：`3145`
   - `⚪ 暂不跟进`：`298`
   - `⏳ 待补信息`：`1122`
5. 一级总判定分布：
   - `软件工程`：`3444`
   - `程序设计语言与形式化基础`：`1233`
   - `跨域/待判定`：`1200`
   - `系统软件`：`424`
6. 软工纳入判定分布：
   - `属于软件工程`：`3292`
   - `跨域但软工主导`：`152`
   - `不属于软件工程`：`2857`
7. 软工主路径覆盖：
   - `3444/3444` 条被纳入软工语料的论文都已回填 `se_primary_path`

## 3. 当前已准备好的入口

### 3.1 `CCF` 方向入口

1. `CCF` 分类总入口：
   - <https://www.ccf.org.cn/Academic_Evaluation/By_category/>
2. `CCF` 软件工程/系统软件/程序设计语言分类页：
   - <https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/>
3. 本仓库内整理后的名录文档：
   - [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md)

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
   - 先判断一个 venue 是 `完全属于软工`、`大部分属于软工`、`部分属于软工`、`大部分不属于软工` 还是 `完全不属于软工`。
   - 明确这个 venue 的“主要方向与边界”分别在哪里，避免把非软工部分机械塞进软工树。

## 4. 当前已明确的工作原则

1. 本路径先做“元数据索引层”，不直接当全文文库使用。
2. `CCF` 年度索引优先通过脚本批量生成，并通过 `verification.json` 做逐 venue 复核。
3. 若发现 venue 边界、重名冲突、官方页回退等问题，应优先修脚本重跑，不手工补半成品。
4. 后续默认先整理元数据、`BibTeX`、`DOI`、摘要和学术落地页。
5. 后续若做方向归类，默认先看 [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md) 的 venue 级先验，再做单篇终判。
6. 若论文跨域，则单独判断是否“软工主导”；只有最终落到 `软件工程` 时，才进入 [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md)。
7. 对纳入软工语料的论文，默认回填 `软工纳入判定 + 软工主路径（x.x.x） + 软工次路径/标签 + 判定依据（X1/D1-D4）`。
8. 若后续扫论文时发现现有 `x.x.x` 没有自然覆盖某类稳定题型，应先扩 [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md)，不要把论文硬塞进最接近的旧节点。
9. `ccf_se_index_builder.py` 当前负责生成基础元数据层；`ccf_se_classifier.py` 负责软工终判、`x.x.x` 路径回填与年度页重渲染。
10. 先做初筛，再决定哪些论文值得获取 `PDF`。
11. 只有真正值得深入阅读的论文，才应迁移到正式论文集路径继续处理。

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

## 6. 更新日志

- `2026-04-06 00:49:29`
  - 重新跑通 [../tools/ccf_se_classifier.py](../tools/ccf_se_classifier.py)，把 `macro_area` 与最终 `se_inclusion_decision` 的口径收紧到一致，不再保留“一级总判定是软件工程、但最终又判为非软工”的冲突条目。
  - 最终确认 `2025` 年度 `6301` 条论文中，`3444` 条纳入软工语料且全部拥有 `se_primary_path`，其余条目落在 `程序设计语言与形式化基础 / 系统软件 / 跨域待判定`。

- `2026-04-06 00:38:29`
  - 新增 [../tools/ccf_se_classifier.py](../tools/ccf_se_classifier.py)，把 `2025` 年度 `6301` 条论文全部回填到 `macro_area / se_inclusion_decision / cross_domain_flag / se_primary_path / se_primary_label / se_secondary_paths / se_decision_basis`。
  - 重写 [ccf_history/2025/README.md](./ccf_history/2025/README.md)，把逐篇表格升级为“一级总判定 + 软工纳入判定 + `x.x.x` 主路径 + 判定依据”的版本。
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
  - 产出 [ccf_history/2025/README.md](./ccf_history/2025/README.md)、[ccf_history/2025/verification.json](./ccf_history/2025/verification.json)、`metadata/*.json`、`bib/*.bib`。
  - 修复并固化了官方页回退、同缩写 venue 文件冲突、proceedings 元条目误收、旧版 `DBLP` 链接兼容等规则。
  - 新增 [../tools/README.md](../tools/README.md)，并把 [../tools/ccf_se_index_builder.py](../tools/ccf_se_index_builder.py) 与 [../tools/ccf_se_index_workflow.md](../tools/ccf_se_index_workflow.md) 接入 `frontier_index` 文档入口。

- `2026-04-05 03:01:03`
  - 新建 `frontier_index/` 顶层路径。
  - 建立 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)。
  - 建立 [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md)，整理 `CCF` 软件工程/系统软件/程序设计语言方向 `A/B/C` 期刊会议名录、方向和索引入口。
  - 建立 [ccf_history/README.md](./ccf_history/README.md)、[arxiv_recent/README.md](./arxiv_recent/README.md) 与 [templates/metadata_index_template.md](./templates/metadata_index_template.md)，为后续批量索引准备目录和模板。
