# `CCF` 软件工程高相关 venue 名录、软工归属判定与索引入口

## 1. 文档用途

本文档用于固定从 `CCF` “软件工程/系统软件/程序设计语言”方向中**筛选后保留**的 venue 子集，并给出三类后续工作所需的先验信息。

当前文库只保留同时满足下面两条的 venue：

1. `软工归属级别` 属于 `完全属于软工 / 大部分属于软工 / 部分属于软工`。
2. 与本博士研究的相关性氛围属于 `A 🔥 / B 🟢 / C 🟡`。

换言之，凡是不满足软工主体相关性，或只具有 `D` 档背景参考价值的 venue，当前都不进入本路径维护范围。

1. **venue 级主体归属**
   - 一个 venue 主要属于 `软件工程`、`系统软件`、`程序设计语言与形式化基础` 中的哪一类。
2. **venue 级软工归属级别**
   - 这个 venue 是否应默认按软工 venue 处理，还是应严格筛选后再纳入。
3. **与本博士研究的相关性氛围**
   - 这个 venue 对本仓库当前博士研究主线而言，是 `A 🔥 / B 🟢 / C 🟡` 中的哪一档，是否值得长期重点跟踪。

本文档不替代单篇论文级判定。后续真正做论文分类时，默认顺序是：

1. 先参考本文，得到 venue 级先验。
2. 再按 [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md) 的单篇论文标准做最终判定。
3. 最后给被纳入软工语料的论文分配 `x.x.x` 级主路径。

## 2. 整理依据

本文档的判断综合基于以下三类依据：

1. `CCF` 官方目录
   - `CCF` 分类总入口：<https://www.ccf.org.cn/Academic_Evaluation/By_category/>
   - `CCF` 软件工程/系统软件/程序设计语言分类页：<https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/>
2. 公开学术社区信息
   - 各 venue 的官方名称、社区定位、系列页、charter、scope 或社区稳定共识。
   - 其中与本仓库当前分类树直接相关的公开资料，已在 [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md) 中给出引用。
3. 本仓库当前语料
   - `frontier_index/ccf_history/2025/metadata/*.json` 中已整理的 `2025` 论文标题、摘要、自动标签与初筛结果。
   - 对已有 `2025` 数据的 venue，本表默认额外参考了其 `2025` 论文的主题分布，而不是只按 venue 名称拍脑袋。
4. 本仓库当前博士研究定位
   - [AGENTS.md](../AGENTS.md)、[TARGET.md](../TARGET.md)、[README.md](../README.md)
   - [project_1_llm_state_machine_modeling/README.md](../project_1_llm_state_machine_modeling/README.md)
   - [open_explore/README.md](../open_explore/README.md)、[open_explore/uppaal_tech/README.md](../open_explore/uppaal_tech/README.md)、[open_explore/uppaal_apps/README.md](../open_explore/uppaal_apps/README.md)
   - 开题报告与文献综述中关于 `LLM + 控制系统 + 状态机建模 + 验证剖面 + 形式化验证 + 反例驱动修复 + UPPAAL/timed automata` 的问题边界。

说明：

1. 本表的 `索引页` 统一保留 `DBLP` venue index 页，便于后续批量索引。
2. 本表的“软工归属级别”是**venue 级先验**，不是对单篇论文的最终裁决。
3. 不在本表中的 venue，默认不进入当前 `frontier_index/` 文库维护范围。
4. 本表中的“与本博士研究相关性（氛围）”也是 **venue 级先验**，服务于“先看哪些 venue 更值得优先跟踪”这一问题，不替代单篇论文终判。

## 3. 这个文档和单篇论文标准的关系

后续默认采用下面这套二层判定：

1. **venue 级先验**
   - 看本文的 `主体归属` 与 `软工归属级别`。
2. **单篇论文终判**
   - 看 [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md) 第 `3` 节的单篇论文标准。

换言之：

1. 本文回答“**这个 venue 默认怎么看**”。
2. 方向树文档回答“**这篇论文最终到底算不算软工**”。

## 4. `主体归属` 与 `软工归属级别` 的定义

### 4.1 `主体归属`

本文中的 `主体归属` 主要使用以下口径：

1. `软件工程`
2. `系统软件`
3. `程序设计语言与形式化基础`
4. `软件工程与系统建模交叉`
5. `信息系统工程与软件工程交叉`
6. `软件工程与服务系统工程交叉`
7. `形式化方法与软件工程交叉`
8. `软件工程与知识工程交叉`

### 4.2 `软工归属级别`

| 级别 | 含义 | 默认处理策略 |
|---|---|---|
| `完全属于软工` | venue 的官方定位、社区共识与近年论文主体都稳定落在 [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md) 的 `1.x-7.x` 主干，`X1` 型非软工主问题只占极少量 | 默认按软工 venue 处理 |
| `大部分属于软工` | venue 主体仍是软件工程，但会稳定混入少量建模、信息系统、服务系统或应用导向内容 | 默认纳入，少量邻近项复核 |
| `部分属于软工` | venue 是明显混合 venue，`D1/D2` 为软工的问题只是其中一部分重要分支 | 严格筛选，仅纳入满足单篇软工标准者 |

### 4.3 `典型软工路径` 如何理解

表格中的 `典型软工路径` 使用 [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md) 的 `x.x.x` 体系：

1. 对 `完全属于软工` 与 `大部分属于软工` 的 venue，给出其最常见的软工路径范围。
2. 对 `部分属于软工` 的 venue，给出“如果要纳入软工语料，通常会落到哪些路径”。

### 4.4 `主要方向与边界` 如何理解

下面各表中的“主要方向与边界”统一采用同一套口径：

1. 先写这个 venue 的**主体问题簇**是什么。
2. 再写它和软件工程方向树的**主要映射路径**。
3. 最后写清楚**边界在哪里**，也就是哪些内容通常不应被机械纳入软工。

换言之，本表不只回答“这个 venue 研究什么”，还回答“它里面哪些论文通常要进软工语料，哪些通常不要进”。

### 4.5 `与本博士研究相关性（氛围）` 如何理解

这里的“博士研究相关性”不是 venue 质量评级，而是**针对本仓库当前博士研究主题**的贴题程度分档。当前文库只保留下面三档：

| 氛围 | 含义 | 默认跟踪策略 |
|---|---|---|
| `A 🔥` | 与 `LLM + 需求/建模 + 状态机/形式化模型 + 性质生成 + 模型检查/运行时验证 + 反例驱动修复 + 控制系统/CPS/UPPAAL` 主线高度贴题 | 长期重点跟踪，默认优先扫 |
| `B 🟢` | 不一定直接命中主问题，但经常能提供关键方法链、验证链、评测链、建模链或 formal methods 邻近支撑 | 次优先跟踪，适合持续补链 |
| `C 🟡` | 以邻近问题为主，只有部分子题可能贴题 | 严格按子题筛选，不宜机械跟踪 |

### 4.6 `与本课题的关系` 如何理解

表格中的“与本课题的关系”统一采用短语式写法：

1. 直接说明它是通过哪条链路与博士研究发生关系的。
2. 优先点明它更接近哪一类问题：
   - 需求与规约生成
   - 状态机 / SysML / MDE 建模
   - 形式化验证 / 模型检查 / 运行时验证
   - 缺陷定位 / 修复 / 维护闭环
   - 控制系统 / CPS / 实时 / safety-critical 场景
   - `LLM for SE / AI for SE`
3. 若只是邻近支撑而不是直接主场，要明确写出“需严格筛选”“偶有贴题”“主要补方法链”等边界词。

## 5. A 类会议

| 缩写 | 全称 | 主体归属 | 软工归属级别 | 主要方向与边界（按本仓库术语） | 典型软工路径 | 与本博士研究相关性（氛围） | 与本课题的关系 | 索引页 |
|---|---|---|---|---|---|---|---|---|
| `PLDI` | ACM SIGPLAN Conference on Programming Language Design and Implementation | 程序设计语言与形式化基础 | `部分属于软工` | 主体是语言设计、编译与程序分析；只有当问题落到测试/验证/修复/规约工程时，才稳定进入软工 | `1.2.x / 3.2.x / 3.3.x / 3.4.x` | `C 🟡` | 程序分析 / 软件验证 / repair 邻近但需严格筛选 | [DBLP](http://dblp.uni-trier.de/db/conf/pldi/) |
| `FSE` | ACM International Conference on the Foundations of Software Engineering | 软件工程 | `完全属于软工` | 软件工程 broad venue，`1.x-7.x` 全生命周期基本全覆盖；边界上只需复核极少数偏应用系统或纯形式化个案 | `1.x.x / 2.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x` | `A 🔥` | broad SE + `LLM/需求建模/测试验证/修复` 主线 | [DBLP](http://dblp.uni-trier.de/db/conf/sigsoft/) |
| `OOPSLA` | Conference on Object-Oriented Programming Systems, Languages, and Applications | 程序设计语言与形式化基础 | `部分属于软工` | 主体是语言、程序、运行时和软件结构；软工相关子集集中在设计、分析、重构与程序理解 | `2.2.x / 3.2.x / 3.4.x / 4.2.x` | `C 🟡` | 软件结构 / 程序分析 / 重构与验证偶发贴题 | [DBLP](http://dblp.uni-trier.de/db/conf/oopsla/) |
| `ASE` | International Conference on Automated Software Engineering | 软件工程 | `完全属于软工` | 主体是自动化软件工程，覆盖生成、分析、测试、验证、修复与工程决策自动化；边界上只需排除极少数纯 `PL/FM` 个案 | `1.x.x / 2.x.x / 3.x.x / 4.x.x / 7.1.x` | `A 🔥` | 自动化软件工程 / `LLM for SE` / 建模-验证-修复主场 | [DBLP](http://dblp.uni-trier.de/db/conf/kbse/) |
| `ICSE` | International Conference on Software Engineering | 软件工程 | `完全属于软工` | 软件工程主会，`1.x-7.x` 几乎全覆盖；邻近系统、`PL`、`AI` 内容也通常以软工问题为主轴组织 | `1.x.x / 2.x.x / 3.x.x / 4.x.x / 5.x.x / 6.x.x / 7.x.x` | `A 🔥` | broad SE 主会，需求-建模-验证-修复全链可见 | [DBLP](http://dblp.uni-trier.de/db/conf/icse/) |
| `ISSTA` | International Symposium on Software Testing and Analysis | 软件工程 | `完全属于软工` | 主体是测试、程序分析、验证、调试与修复；方法可来自 `PL/FM`，但问题本体稳定落在 `3.x` 软工链条 | `3.1.x / 3.2.x / 3.3.x / 3.4.x / 5.1.x / 5.2.x` | `A 🔥` | 测试分析 / 形式化验证 / 缺陷定位与修复主场 | [DBLP](http://dblp.uni-trier.de/db/conf/issta/) |
| `FM` | International Symposium on Formal Methods | 形式化方法与软件工程交叉 | `部分属于软工` | 主体是形式化建模、规约、验证与证明；只有当验证对象、工件和证据明确落在软件工程活动时才纳入软工 | `1.2.x / 1.3.x / 3.3.x / 8.1.x / 8.3.x` | `A 🔥` | 形式化方法 / timed automata / 工业与控制系统验证邻近 | [DBLP](http://dblp.uni-trier.de/db/conf/fm/) |

## 6. A 类期刊

| 缩写 | 全称 | 主体归属 | 软工归属级别 | 主要方向与边界（按本仓库术语） | 典型软工路径 | 与本博士研究相关性（氛围） | 与本课题的关系 | 索引页 |
|---|---|---|---|---|---|---|---|---|
| `TOSEM` | ACM Transactions on Software Engineering and Methodology | 软件工程 | `完全属于软工` | 软件工程方法学主干期刊，覆盖需求、建模、分析、测试、维护、过程与智能化软件工程 | `1.x.x / 2.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x` | `A 🔥` | 软件工程方法 / 需求建模 / 测试验证 / `AI for SE` | [DBLP](http://dblp.uni-trier.de/db/journals/tosem/) |
| `TSE` | IEEE Transactions on Software Engineering | 软件工程 | `完全属于软工` | 软件工程主干期刊，`1.x-7.x` 基本都可出现；邻近内容通常仍围绕软工对象和工程证据展开 | `1.x.x / 2.x.x / 3.x.x / 4.x.x / 5.x.x / 6.x.x / 7.x.x` | `A 🔥` | broad SE 主刊 / 建模验证修复与 `LLM` 子题持续出现 | [DBLP](http://dblp.uni-trier.de/db/journals/tse/) |
| `TSC` | IEEE Transactions on Services Computing | 软件工程与服务系统工程交叉 | `部分属于软工` | 主体是服务计算、云服务与服务系统；只有当问题落到服务设计、治理、持续工程、运行治理与质量保证时才纳入软工 | `2.1.4 / 4.3.x / 4.4.x / 5.3.x / 8.2.x` | `C 🟡` | 服务工作流 / 平台 orchestration 邻近，可补性质工程 | [DBLP](http://dblp.uni-trier.de/db/journals/tsc/) |

## 7. B 类会议

| 缩写 | 全称 | 主体归属 | 软工归属级别 | 主要方向与边界（按本仓库术语） | 典型软工路径 | 与本博士研究相关性（氛围） | 与本课题的关系 | 索引页 |
|---|---|---|---|---|---|---|---|---|
| `ECOOP` | European Conference on Object-Oriented Programming | 程序设计语言与形式化基础 | `部分属于软工` | 主体是面向对象程序设计、语言与运行时；软工相关子集多落在设计、结构分析、重构与程序理解 | `2.2.x / 3.2.x / 4.2.x` | `C 🟡` | `OO` 程序结构 / 分析与重构邻近 | [DBLP](http://dblp.uni-trier.de/db/conf/ecoop/) |
| `ICPC` | IEEE International Conference on Program Comprehension | 软件工程 | `完全属于软工` | 主体是程序理解、代码认知、逆向、维护与开发者理解支持；方法可来自检索或分析，但问题本体稳定是软工 | `4.2.x / 4.1.x / 6.5.1` | `B 🟢` | 程序理解 / 缺陷分析 / 修复解释与人因辅助 | [DBLP](http://dblp.uni-trier.de/db/conf/iwpc/) |
| `RE` | IEEE International Requirements Engineering Conference | 软件工程 | `完全属于软工` | 主体是需求工程全链条，包括获取、规格、质量、追踪、演化与决策；边界上只需排除极少数纯形式化理论个案 | `1.1.x / 1.2.x / 1.4.x / 6.1.x` | `A 🔥` | 需求工程 / 规约抽取 / 性质生成 / 需求到模型 | [DBLP](http://dblp.uni-trier.de/db/conf/re/) |
| `CAiSE` | International Conference on Advanced Information Systems Engineering | 信息系统工程与软件工程交叉 | `部分属于软工` | 主体是信息系统工程、企业建模、过程与方法工程；只有落在建模、架构、持续工程和系统化设计方法的部分稳定纳入软工 | `1.3.x / 2.1.x / 4.3.x / 8.3.x` | `B 🟢` | 信息系统与过程/模型工程，适合补需求-建模-规约链 | [DBLP](http://dblp.uni-trier.de/db/conf/caise/) |
| `MoDELS` | ACM/IEEE International Conference on Model Driven Engineering Languages and Systems | 软件工程与系统建模交叉 | `大部分属于软工` | 主体是建模语言、模型驱动工程、模型转换与模型分析；虽然会混入系统建模，但大多数内容可映射到 `1.3.x` 主干 | `1.3.x / 2.1.x / 3.3.x / 8.1.x` | `A 🔥` | 模型驱动 / 状态机-SysML / 形式化建模主场 | [DBLP](http://dblp.uni-trier.de/db/conf/models/) |
| `ICSOC` | International Conference on Service Oriented Computing | 软件工程与服务系统工程交叉 | `部分属于软工` | 主体是服务计算、服务组合、服务系统运行与治理；只有当问题落到服务设计、持续工程或质量治理时才纳入软工 | `2.1.4 / 4.3.x / 4.4.x / 8.2.3` | `C 🟡` | 服务组合 / 流程 / 性质与治理偶有贴题 | [DBLP](http://dblp.uni-trier.de/db/conf/icsoc/) |
| `SANER` | IEEE International Conference on Software Analysis, Evolution, and Reengineering | 软件工程 | `完全属于软工` | 主体是软件分析、演化、逆向、重构与程序理解，稳定落在 `3.x / 4.x` 软工链条 | `4.1.x / 4.2.x / 3.2.x / 3.4.x` | `B 🟢` | 代码分析 / 逆向 / 演化与 reengineering | [DBLP](http://dblp.uni-trier.de/db/conf/wcre/) |
| `ICSME` | International Conference on Software Maintenance and Evolution | 软件工程 | `完全属于软工` | 主体是维护、演化、重构、理解、技术债与维护过程；边界上只需复核极少数纯系统演化个案 | `4.1.x / 4.2.x / 4.3.x / 6.4.x` | `B 🟢` | 维护演化 / 修复 / 回归验证 / 工程闭环邻近 | [DBLP](http://dblp.uni-trier.de/db/conf/icsm/) |
| `VMCAI` | International Conference on Verification, Model Checking, and Abstract Interpretation | 形式化方法与软件工程交叉 | `部分属于软工` | 主体是验证、模型检查、抽象解释与程序分析；只有当验证对象和评估证据明确落在软件工程问题上时纳入软工 | `1.2.x / 3.2.x / 3.3.x / 5.1.x` | `A 🔥` | 程序验证 / 模型检查 / 抽象解释直接支撑验证框架 | [DBLP](http://dblp.uni-trier.de/db/conf/vmcai/) |
| `ICWS` | IEEE International Conference on Web Services | 软件工程与服务系统工程交叉 | `部分属于软工` | 主体是 Web 服务、服务组合和服务系统实现；只有服务设计、治理、质量和运行工程部分稳定纳入软工 | `2.1.4 / 4.4.x / 5.3.x / 8.2.3` | `C 🟡` | Web services / orchestration / 性质验证偶有贴题 | [DBLP](http://dblp.uni-trier.de/db/conf/icws/) |
| `ESEM` | International Symposium on Empirical Software Engineering and Measurement | 软件工程 | `完全属于软工` | 主体是经验软件工程、测量、实证方法与软件数据分析，稳定落在 `6.x` | `6.3.x / 6.4.x / 6.5.x / 4.1.x` | `B 🟢` | 实证方法 / 评测设计 / `LLM-SE` 实验口径重要 | [DBLP](http://dblp.uni-trier.de/db/conf/esem/) |
| `ISSRE` | IEEE International Symposium on Software Reliability Engineering | 软件工程 | `完全属于软工` | 主体是软件可靠性、故障、容错、质量保障与运行时可靠性工程，稳定落在 `3.x / 5.x / 4.4.x` | `3.1.x / 3.3.x / 5.1.x / 5.2.x / 4.4.x` | `A 🔥` | 可靠性 / assurance / 安全关键验证与缺陷检测很近 | [DBLP](http://dblp.uni-trier.de/db/conf/issre/) |

## 8. B 类期刊

| 缩写 | 全称 | 主体归属 | 软工归属级别 | 主要方向与边界（按本仓库术语） | 典型软工路径 | 与本博士研究相关性（氛围） | 与本课题的关系 | 索引页 |
|---|---|---|---|---|---|---|---|---|
| `ASE` | Automated Software Engineering | 软件工程 | `完全属于软工` | 主体是自动分析、自动生成、自动测试、自动验证和自动修复，稳定落在 `1.x-4.x / 7.1.x` | `1.x.x / 2.x.x / 3.x.x / 4.x.x / 7.1.x` | `A 🔥` | 自动化软件工程 / `LLM for SE` / 建模-验证-修复主场 | [DBLP](http://dblp.uni-trier.de/db/journals/ase/) |
| `ESE` | Empirical Software Engineering | 软件工程 | `完全属于软工` | 主体是经验软件工程、研究方法、数据分析与证据综合，稳定落在 `6.x` | `6.3.x / 6.4.x / 6.5.x / 4.1.x` | `B 🟢` | 实证研究 / 数据集 / benchmark / 人因与评测设计 | [DBLP](http://dblp.uni-trier.de/db/journals/ese/) |
| `IETS` | IET Software | 软件工程 | `大部分属于软工` | 主体是工程化软件方法、工具与应用型软件工程；少量应用系统实现或行业问题需要复核是否真正回答软工问题 | `1.x.x / 3.x.x / 4.x.x / 5.x.x` | `C 🟡` | broad SE 期刊，可筛少量建模/验证论文 | [DBLP](https://dblp.uni-trier.de/db/journals/iet-sen) |
| `IST` | Information and Software Technology | 软件工程 | `大部分属于软工` | 主体是软件与信息系统方法、工具、评估与实证；少量偏信息系统管理的条目需要严格复核 | `1.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x` | `B 🟢` | broad SE / 建模测试 / `AI4SE` 论文较常见 | [DBLP](http://dblp.uni-trier.de/db/journals/infsof/index.html) |
| `JSEP` | Journal of Software: Evolution and Process | 软件工程 | `完全属于软工` | 主体是软件演化、维护、持续工程与过程改进，稳定落在 `4.x / 6.x` | `4.1.x / 4.3.x / 6.1.x / 6.4.x` | `B 🟢` | 演化 / 过程 / 迭代闭环与工程实践邻近 | [DBLP](http://dblp.uni-trier.de/db/journals/smr/) |
| `JSS` | Journal of Systems and Software | 软件工程 | `大部分属于软工` | 主体仍是软件工程与软件密集型系统工程；少量系统实现或应用导向论文需要复核其是否以软工问题为主轴 | `2.x.x / 3.x.x / 4.x.x / 5.x.x / 8.x.x` | `B 🟢` | 系统与软件工程综合刊，常见建模/验证/CPS 个案 | [DBLP](http://dblp.uni-trier.de/db/journals/jss/) |
| `RE` | Requirements Engineering | 软件工程 | `完全属于软工` | 主体是需求获取、规格、质量、追踪、协商与变更管理，稳定落在 `1.1.x / 1.2.x / 1.4.x` | `1.1.x / 1.2.x / 1.4.x` | `A 🔥` | 需求工程 / 规约抽取 / 性质生成 / 需求到模型 | [DBLP](http://dblp.uni-trier.de/db/journals/re/) |
| `SCP` | Science of Computer Programming | 程序设计语言与形式化基础 | `部分属于软工` | 主体是程序设计、形式化方法与实现；只有面向软件方法、验证工程、程序分析和维护的问题才纳入软工 | `1.2.x / 3.2.x / 3.3.x / 4.1.x` | `B 🟢` | 软件程序与形式化/验证/程序分析交叉，贴题概率中高 | [DBLP](http://dblp.uni-trier.de/db/journals/scp/) |
| `SoSyM` | Software and Systems Modeling | 软件工程与系统建模交叉 | `大部分属于软工` | 主体是软件与系统建模、模型驱动工程与模型分析；会混入系统建模，但大多数内容可纳入 `1.3.x` 主干 | `1.3.x / 2.1.x / 3.3.x / 8.1.x` | `A 🔥` | 软件与系统建模 / DSL / 状态机与模型分析主场 | [DBLP](http://dblp.uni-trier.de/db/journals/sosym/) |
| `STVR` | Software Testing, Verification and Reliability | 软件工程 | `完全属于软工` | 主体是测试、验证、可靠性与质量保障，稳定落在 `3.x / 5.1.x` | `3.1.x / 3.3.x / 5.1.x` | `A 🔥` | 测试 / 验证 / 可靠性与 formal properties 非常贴题 | [DBLP](http://dblp.uni-trier.de/db/journals/stvr/index.html) |
| `SPE` | Software: Practice and Experience | 软件工程与系统软件交叉 | `部分属于软工` | 主体是软件实践、工程经验与系统实现；只有当论文真正回答构造、持续工程、运维或工程经验问题时才纳入软工 | `2.3.x / 4.3.x / 4.4.x / 6.3.x / 8.2.x` | `C 🟡` | 工程实践 / 系统实现为主，偶有 runtime/verification | [DBLP](http://dblp.uni-trier.de/db/journals/spe/) |

说明：`JSEP` 在可检索目录镜像中常以旧刊名路径维护，这里仍用常见缩写 `JSEP` 便于后续索引。

## 9. C 类会议

| 缩写 | 全称 | 主体归属 | 软工归属级别 | 主要方向与边界（按本仓库术语） | 典型软工路径 | 与本博士研究相关性（氛围） | 与本课题的关系 | 索引页 |
|---|---|---|---|---|---|---|---|---|
| `PASTE` | ACM SIGPLAN-SIGSOFT Workshop on Program Analysis for Software Tools and Engineering | 程序设计语言与形式化基础 | `部分属于软工` | 主体是程序分析与软件工具；只有当问题落到测试、调试、理解或工程工具链时稳定纳入软工 | `3.2.x / 3.4.x / 4.2.x` | `B 🟢` | 程序分析与软件工具工程，对验证/修复较近 | [DBLP](http://dblp.uni-trier.de/db/conf/paste/) |
| `APSEC` | Asia-Pacific Software Engineering Conference | 软件工程 | `大部分属于软工` | 软件工程 broad venue，覆盖开发、分析、测试、维护、实证与智能化软件工程；少量应用型系统论文需要复核 | `1.x.x / 2.x.x / 3.x.x / 4.x.x / 6.x.x / 7.x.x` | `B 🟢` | broad SE / 亚洲社区，`LLM-SE/测试/建模` 可见 | [DBLP](http://dblp.uni-trier.de/db/conf/apsec/) |
| `EASE` | International Conference on Evaluation and Assessment in Software Engineering | 软件工程 | `完全属于软工` | 主体是软件工程评估、测量、实证与证据方法，稳定落在 `6.x` | `6.3.x / 6.4.x / 6.5.x / 4.1.x` | `B 🟢` | 评测与实验设计 / benchmark / replication 有用 | [DBLP](http://dblp.uni-trier.de/db/conf/ease/) |
| `ICECCS` | International Conference on Engineering of Complex Computer Systems | 软件工程与系统建模交叉 | `部分属于软工` | 主体是复杂系统工程、架构与形式化分析；只有面向软件建模、系统工程方法和 assurance 的部分纳入软工 | `1.3.x / 2.1.x / 3.3.x / 8.3.x` | `B 🟢` | 复杂系统建模与验证 / safety-critical / CPS 邻近 | [DBLP](http://dblp.uni-trier.de/db/conf/iceccs/) |
| `ICST` | IEEE International Conference on Software Testing, Verification and Validation | 软件工程 | `完全属于软工` | 主体是软件测试、验证、确认与质量保证，稳定落在 `3.x`，并与 `5.x` 质量属性强交叉 | `3.1.x / 3.2.x / 3.3.x / 3.4.x / 5.1.x / 5.2.x` | `A 🔥` | 测试 / 形式化验证 / 缺陷检测与修复直接相关 | [DBLP](http://dblp.uni-trier.de/db/conf/icst/) |
| `SCAM` | IEEE International Working Conference on Source Code Analysis and Manipulation | 软件工程 | `大部分属于软工` | 主体是源代码分析、理解、变换与重构；少量偏纯程序变换的论文需要复核 | `3.2.x / 4.2.x / 4.1.x / 3.4.x` | `B 🟢` | 源码分析与变换 / 缺陷修复 / 程序理解邻近 | [DBLP](http://dblp.uni-trier.de/db/conf/scam/) |
| `COMPSAC` | International Computer Software and Applications Conference | 软件工程与系统软件交叉 | `部分属于软工` | 主体很宽，覆盖软件、平台与应用系统；只有明确回答软件工程质量、构造、维护或工程管理问题的部分纳入软工 | `2.x.x / 3.x.x / 4.x.x / 5.x.x / 8.x.x` | `C 🟡` | 覆盖过宽，需按建模/验证/`AI4SE` 子题筛选 | [DBLP](http://dblp.uni-trier.de/db/conf/compsac/) |
| `ICFEM` | International Conference on Formal Engineering Methods | 形式化方法与软件工程交叉 | `部分属于软工` | 主体是形式化工程方法、规约、验证与建模；当形式化对象和证据落到软件工程工件时纳入软工 | `1.2.x / 1.3.x / 3.3.x / 8.1.x / 8.3.x` | `A 🔥` | formal engineering / 规约建模 / 验证与证明 | [DBLP](http://dblp.uni-trier.de/db/conf/icfem/) |
| `SSE` | IEEE International Conference on Software Services Engineering | 软件工程与服务系统工程交叉 | `部分属于软工` | 主体是软件服务工程与服务系统实现；只有服务设计、发布、治理、质量和运行工程部分纳入软工 | `2.1.4 / 4.3.x / 4.4.x / 8.2.3` | `C 🟡` | 软件服务工程混合 | [DBLP](http://dblp.uni-trier.de/db/conf/IEEEscc/) |
| `ICSSP` | International Conference on Software and System Process | 软件工程 | `完全属于软工` | 主体是软件与系统过程、协作、流程改进、治理与过程证据，稳定落在 `6.1.x / 6.2.x / 6.5.x` | `6.1.x / 6.2.x / 6.5.x` | `C 🟡` | 软件过程 / 团队与流程，对主问题较间接 | [DBLP](http://dblp.uni-trier.de/db/conf/ispw/) |
| `SEKE` | International Conference on Software Engineering and Knowledge Engineering | 软件工程与知识工程交叉 | `部分属于软工` | 主体是软件工程与知识工程交叉；只有明确回答需求、设计、分析、测试或 `AI for SE` 问题的部分纳入软工 | `1.x.x / 2.x.x / 3.x.x / 7.1.x` | `C 🟡` | `SE + 知识工程` 混合，`AI/建模` 偶有贴题 | [DBLP](http://dblp.uni-trier.de/db/conf/seke/) |
| `QRS` | International Conference on Software Quality, Reliability and Security | 软件工程 | `完全属于软工` | 主体是软件质量、可靠性、安全与 assurance，稳定落在 `3.x / 5.x / 4.4.x` | `3.x.x / 5.1.x / 5.2.x / 4.4.x` | `A 🔥` | 质量 / 可靠性 / 安全 / assurance 与验证链很近 | [DBLP](https://dblp.uni-trier.de/db/conf/qrs) |
| `ICSR` | International Conference on Software Reuse | 软件工程 | `完全属于软工` | 主体是软件复用、组件复用、可复用资产与复用工程，稳定落在 `1.4.x / 2.3.x / 4.x` | `1.4.x / 2.3.x / 4.1.x / 4.3.x` | `C 🟡` | 复用 / 组件资产，可补模型资产与可复用工件 | [DBLP](http://dblp.uni-trier.de/db/conf/icsr/) |
| `SPIN` | International Symposium on Model Checking of Software | 形式化方法与软件工程交叉 | `部分属于软工` | 主体是软件模型检查、验证与自动分析；当问题落到软件规约、验证工程和 assurance 时纳入软工 | `1.2.x / 1.3.x / 3.3.x` | `A 🔥` | 软件模型检查 / state-based verification / `UPPAAL` 邻近 | [DBLP](http://dblp.uni-trier.de/db/conf/spin/index.html) |
| `TASE` | Theoretical Aspects of Software Engineering Conference | 形式化方法与软件工程交叉 | `部分属于软工` | 名称带软件工程，但主体常是形式化分析、验证和理论方法；只有问题本体明确是软件工程活动时纳入软工 | `1.2.x / 3.3.x / 5.1.x` | `B 🟢` | 软件工程名下的 formal verification / assurance 邻近 | [DBLP](http://dblp.uni-trier.de/db/conf/tase/) |
| `MSR` | Mining Software Repositories | 软件工程 | `完全属于软工` | 主体是软件仓库挖掘、演化分析、度量、开发者与社区分析，稳定落在 `6.4.x` 并与 `4.x / 6.5.x` 交叉 | `6.4.x / 6.3.x / 4.1.x / 6.5.x` | `B 🟢` | 仓库挖掘 / benchmark / `LLM-SE` 证据与数据建设有用 | [DBLP](http://dblp.uni-trier.de/db/conf/msr/) |
| `REFSQ` | Requirements Engineering: Foundation for Software Quality | 软件工程 | `完全属于软工` | 主体是需求工程与需求质量，稳定落在 `1.1.x / 1.2.x / 1.4.x` | `1.1.x / 1.2.x / 1.4.x` | `A 🔥` | 需求质量 / 需求规约 / 需求到性质非常贴题 | [DBLP](http://dblp.uni-trier.de/db/conf/refsq/) |
| `WICSA` | Working IEEE/IFIP Conference on Software Architecture | 软件工程 | `完全属于软工` | 主体是软件架构、架构设计、评估、恢复与演化，稳定落在 `2.1.x / 2.2.x / 4.1.x` | `2.1.x / 2.2.x / 4.1.x` | `B 🟢` | 软件架构 / 设计决策 / 模型结构与演化有用 | [DBLP](http://dblp.uni-trier.de/db/conf/wicsa/) |
| `Internetware` | Asia-Pacific Symposium on Internetware | 软件工程与服务系统工程交叉 | `大部分属于软工` | 主体是网络化软件、平台软件、Internetware 架构、发布与运行；会混入平台和服务系统内容，但大多数仍可纳入软工 | `2.1.4 / 4.3.x / 4.4.x / 8.2.x` | `C 🟡` | 平台 / 网络化软件 / 运行治理邻近 | [DBLP](https://dblp.org/db/conf/internetware/index.html) |
| `RV` | International Conference on Runtime Verification | 形式化方法与软件工程交叉 | `部分属于软工` | 主体是运行时验证、监测与在线分析；当对象是软件系统行为、运行治理与 assurance 时纳入软工 | `3.3.2 / 4.4.4 / 5.1.x` | `A 🔥` | 运行时验证 / 监测 / 时序性质 / 工具链直接邻近 | [DBLP](https://dblp.org/db/conf/rv/index.html) |

## 10. C 类期刊

| 缩写 | 全称 | 主体归属 | 软工归属级别 | 主要方向与边界（按本仓库术语） | 典型软工路径 | 与本博士研究相关性（氛围） | 与本课题的关系 | 索引页 |
|---|---|---|---|---|---|---|---|---|
| `IJSEKE` | International Journal of Software Engineering and Knowledge Engineering | 软件工程与知识工程交叉 | `大部分属于软工` | 主体是软件工程与知识工程交叉方法、工具和应用；少量纯知识表示或 `AI` 方法论文需要复核 | `1.x.x / 2.x.x / 3.x.x / 7.1.x` | `C 🟡` | `SE + 知识工程` 混合，`AI/建模` 可补链但不稳定 | [DBLP](http://dblp.uni-trier.de/db/journals/ijseke/index.html) |
| `STTT` | International Journal of Software Tools for Technology Transfer | 形式化方法与软件工程交叉 | `部分属于软工` | 主体是软件工具、验证工具与技术转移；只有面向软件分析、验证工程与工业软件 assurance 的部分纳入软工 | `3.2.x / 3.3.x / 5.1.x` | `A 🔥` | 验证工具 / formal methods tool transfer / `UPPAAL` 邻近 | [DBLP](http://dblp.uni-trier.de/db/journals/sttt/) |
| `SOCA` | Service Oriented Computing and Applications | 软件工程与服务系统工程交叉 | `部分属于软工` | 主体是服务计算与应用；只有服务设计、服务质量、运行治理和服务工程方法部分纳入软工 | `2.1.4 / 4.4.x / 8.2.3` | `C 🟡` | 服务计算与应用为主 | [DBLP](http://dblp.uni-trier.de/db/journals/soca/) |
| `SQJ` | Software Quality Journal | 软件工程 | `完全属于软工` | 主体是软件质量、质量评估、质量保障与度量，稳定落在 `5.x` 并与 `3.x / 6.3.x` 交叉 | `5.x.x / 3.x.x / 6.3.x` | `B 🟢` | 质量 / 度量 / assurance 视角可支撑验证评价 | [DBLP](http://dblp.uni-trier.de/db/journals/sqj/) |

## 11. 后续落地索引时的使用建议

后续真正开始建往年论文索引时，默认建议如下：

1. 对 `完全属于软工` 的 venue
   - 默认作为软工 venue 处理。
   - 单篇论文通常直接进入软工语料，但 broad venue 仍要做主路径细分。
2. 对 `大部分属于软工` 的 venue
   - 默认纳入软工索引。
   - 但需要警惕少量信息系统、服务系统、应用型系统实现或邻近形式化内容。
3. 对 `部分属于软工` 的 venue
   - 不要按 venue 名称机械纳入。
   - 必须按 [SOFTWARE_ENGINEERING_FIELD_TREE.md](./SOFTWARE_ENGINEERING_FIELD_TREE.md) 第 `3` 节的 `X1 + D1-D4` 单篇标准做最终判定，并保留判定依据。

对当前博士研究，如果目标是建立“与 `LLM + 状态机建模/验证/修复 + 控制系统/CPS + UPPAAL/timed automata` 最相关”的 venue 跟踪优先级，默认直接按上表中的 `A/B/C` 使用：

1. `A 🔥`
   - 作为长期重点跟踪 venue。
   - 默认优先扫新论文、新特刊和近年 `LLM/formal methods/modeling/testing/repair` 子题。
2. `B 🟢`
   - 作为第二梯队持续跟踪。
   - 重点补方法链、验证链、评测链、数据集链和 formal methods 邻近支撑。
3. `C 🟡`
   - 不要按 venue 名称机械跟。
   - 只在明确命中“需求到模型、状态机/模型驱动、性质生成、模型检查、运行时验证、缺陷修复、控制系统/CPS”子题时再纳入。
