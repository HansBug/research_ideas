# `frontier_index/` SUMMARY

## 1. 当前整体状态

- 路径状态：`已初始化`
- 已建立核心文档：`7` 份
- 已建立正式论文索引批次：`0`
- 已收录具体论文条目：`0`
- 已准备好的 `CCF` venue 名录：`82` 个
- 已准备好的 `arXiv` 入口：`1` 个主入口

## 2. 当前已准备好的入口

### 2.1 `CCF` 方向入口

1. `CCF` 分类总入口：
   - <https://www.ccf.org.cn/Academic_Evaluation/By_category/>
2. `CCF` 软件工程/系统软件/程序设计语言分类页：
   - <https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/>
3. 本仓库内整理后的名录文档：
   - [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md)

### 2.2 `arXiv` 方向入口

1. `arXiv cs.SE recent`：
   - <https://arxiv.org/list/cs.SE/recent>

## 3. 当前已明确的工作原则

1. 本路径先做“元数据索引层”，不直接当全文文库使用。
2. 后续默认先整理元数据、`BibTeX`、`DOI`、摘要和学术落地页。
3. 先做初筛，再决定哪些论文值得获取 `PDF`。
4. 只有真正值得深入阅读的论文，才应迁移到正式论文集路径继续处理。

## 4. 当前优先关注方向

当前建议优先从以下方向起步：

1. `ICSE / FSE / ASE / ISSTA / TSE / TOSEM`
   - 软件工程主干 venue，适合做第一批高价值往年索引。
2. `RE / ICSME / SANER / STVR / ESEM`
   - 与需求工程、维护演化、测试验证、经验软件工程更直接相关。
3. `FM / VMCAI / SPIN / ATVA / RV / ICST / MEMOCODE`
   - 与形式化方法、验证、模型检查、运行时验证更贴近。
4. `MoDELS / CAiSE`
   - 与建模、模型驱动工程、信息系统建模相关。
5. `arXiv cs.SE`
   - 用于滚动跟踪近期新论文，尤其是 `LLM for SE`、需求、验证、修复、分析等方向。

## 5. 下一步建议

1. 先选一个小批次开始试跑索引流程。
2. 建议优先从某一个年份开始，先做该年 `ICSE / ASE / FSE / TSE / TOSEM / RE` 的年度汇总页。
3. 同时建立一份 `arXiv cs.SE` 的近期批次索引，验证“按摘要先筛、再拿 PDF”的流程是否顺手。
4. 等第一轮索引形成稳定字段口径后，再决定是否补专门的模板文档或子目录结构。

## 6. 更新日志

- `2026-04-05 03:01:03`
  - 新建 `frontier_index/` 顶层路径。
  - 建立 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)。
  - 建立 [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md)，整理 `CCF` 软件工程/系统软件/程序设计语言方向 `A/B/C` 期刊会议名录、方向和索引入口。
  - 建立 [ccf_history/README.md](./ccf_history/README.md)、[arxiv_recent/README.md](./arxiv_recent/README.md) 与 [templates/metadata_index_template.md](./templates/metadata_index_template.md)，为后续批量索引准备目录和模板。
