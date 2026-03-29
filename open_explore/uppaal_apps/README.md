# `uppaal_apps/` 论文集 README

## 1. 论文集定位

`open_explore/uppaal_apps/` 是面向 `UPPAAL` 应用与案例主线的专题论文集，用于系统沉淀基于 `UPPAAL` 的软件、系统、协议、控制器和工业验证工作。

它与同级的 [uppaal_tech/README.md](../uppaal_tech/README.md) 分工明确：

1. [uppaal_tech/README.md](../uppaal_tech/README.md)
   - 收 `UPPAAL` 本体技术。
2. [uppaal_apps/README.md](./README.md)
   - 收 `UPPAAL` 被用于解决具体问题、验证具体对象、支持具体工程场景的应用贡献。

## 2. 设立宗旨与期望收获

单独建立本论文集，是为了把“`UPPAAL` 技术本体”与“`UPPAAL` 被如何真正使用”拆开维护，避免两条主线互相稀释。

这里后续希望沉淀的内容主要包括：

1. 具有正式学术或工程贡献的 `UPPAAL` 应用论文。
2. 来自 `UPPAAL` 官方、核心团队或稳定学术脉络的案例工作。
3. 可复用的建模对象类型、验证目标类型、性质表达方式和案例组织模式。

## 3. 收录范围

本论文集优先收录以下条目：

1. 使用 `UPPAAL` 对具体协议、控制器、嵌入式系统、工业系统或软件系统做建模、验证、调度、测试或分析的正式论文。
2. `UPPAAL` 官方案例页、官方教程或官方文档中可追溯到正式论文或稳定技术报告的案例。
3. 在应用对象、建模方式、验证性质、结果分析上提供了足够细节，能为后续博士研究提供案例参考的工作。

本论文集不应收录以下条目：

1. 主贡献是 `UPPAAL` 本体算法、数据结构、抽象、引擎或工具工程的论文，这些应进入 [uppaal_tech/README.md](../uppaal_tech/README.md)。
2. 只是在 related work 里顺带提到 `UPPAAL`，没有真正形成案例贡献的论文。
3. 没有合法 PDF、没有可用正文提取物、无法支撑可靠整理的条目。

## 4. 纳入与排除判定标准

后续筛选时至少看五个维度：

1. 研究对象
   - 纳入：具体系统、协议、软件或工程场景。
   - 排除：工具本体技术。
2. 任务类型
   - 纳入：建模、验证、测试、调度、性能分析、工业验证落地。
   - 排除：纯算法或纯引擎论文。
3. 证据形态
   - 纳入：正文明确讲了对象、模型、性质和验证结果。
   - 排除：只有一句“我们用过 `UPPAAL`”。
4. 可提取性
   - 纳入：可获得 PDF 原文并生成 `paper_content.txt`。
   - 排除：无法稳定获取正文。
5. 与博士研究相关性
   - 纳入：能为状态机建模、性质构造、验证剖面或修复研究提供案例参照。
   - 降优先级：案例虽真实，但与控制系统/形式化验证关系较弱。

## 5. 本论文集下文件说明

本论文集默认包含以下核心文件：

1. [README.md](./README.md)
   - 入口说明与边界定义。
2. [GUIDE.md](./GUIDE.md)
   - AI 检索、筛选、回填和一致性检查规范。
3. [SUMMARY.md](./SUMMARY.md)
   - 当前总账、分类、条目清单、更新日志和失败记录。

推荐阅读顺序：

1. [README.md](./README.md)
2. [GUIDE.md](./GUIDE.md)
3. [SUMMARY.md](./SUMMARY.md)
4. 具体论文目录下的 `bibtex.bib`
5. 具体论文目录下的 `paper_content.txt`
6. 必要时核对 `paper.pdf`

## 6. 单论文路径约束

本论文集下每个单论文目录默认至少应包含：

1. `paper.pdf`
2. `paper_content.txt`
3. `bibtex.bib`

后续若开始做应用专题化整理，再额外补：

1. `desc.md`
2. 应用对象/性质/建模要点类笔记
3. 与博士研究任务的映射说明

## 7. AI 工作入口提示

进入本论文集时，默认按以下方式工作：

1. 先判断该条目是不是“应用主贡献”，若不是则转去 [uppaal_tech/README.md](../uppaal_tech/README.md)。
2. 再按 `README.md -> GUIDE.md -> SUMMARY.md` 的顺序理解现有口径。
3. 处理单篇论文时，仍按 `bibtex.bib -> paper_content.txt -> paper.pdf（必要时）` 的顺序工作。
4. 新条目入库后，必须同步回写 [SUMMARY.md](./SUMMARY.md)。
