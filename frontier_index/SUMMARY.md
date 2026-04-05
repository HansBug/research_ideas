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

### 3.4 软件工程方向分类基线

1. 领域方向树与边界说明：
   - [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md)
2. 默认用途：
   - 用于判断一篇论文是否属于软件工程。
   - 用于先做 `软件工程 / 系统软件 / 程序设计语言与形式化基础 / 跨域待判定` 的一级总判定。
   - 用于给软工论文，以及跨域但软工主导的论文，分配主标签/次标签。

## 4. 当前已明确的工作原则

1. 本路径先做“元数据索引层”，不直接当全文文库使用。
2. `CCF` 年度索引优先通过脚本批量生成，并通过 `verification.json` 做逐 venue 复核。
3. 若发现 venue 边界、重名冲突、官方页回退等问题，应优先修脚本重跑，不手工补半成品。
4. 后续默认先整理元数据、`BibTeX`、`DOI`、摘要和学术落地页。
5. 后续若做方向归类，默认先做一级总判定；若论文跨域，则单独判断是否“软工主导”，只有最终落到 `软件工程` 时，才进入 [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md)。
6. 先做初筛，再决定哪些论文值得获取 `PDF`。
7. 只有真正值得深入阅读的论文，才应迁移到正式论文集路径继续处理。

## 5. 下一步建议

1. 基于 `2025` 年度索引，优先从 `🟢 优先跟进` 条目里挑选与形式化建模、验证、需求、修复更贴近的论文获取 `PDF`。
2. 对 `⏳ 待补信息` 且与你博士研究高度相关的条目，优先补摘要或 publisher 侧信息。
3. 若继续扩年份，直接复用：

```bash
python -m tools.ccf_se_index_builder --year 2024
```

4. 若进入全文阶段，再转用 `tools/pdf_extractor.py` 和正式论文集规范。

## 6. 更新日志

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
