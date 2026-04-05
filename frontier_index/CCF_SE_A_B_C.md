# `CCF` 软件工程/系统软件/程序设计语言方向 `A/B/C` 名录与索引入口

## 1. 文档用途

本文档用于固定 `CCF` 软件工程/系统软件/程序设计语言方向的 `A/B/C` 类期刊会议名录，作为后续建立往年论文元数据索引的基础入口。

后续使用方式如下：

1. 先根据本文件确定 venue 范围。
2. 再按 venue 和年份去整理论文元数据。
3. 先做轻量初筛，再决定哪些论文值得获取 `PDF` 深读。

## 2. 整理依据

本文件主要依据以下入口整理：

1. `CCF` 官方分类总入口：
   - <https://www.ccf.org.cn/Academic_Evaluation/By_category/>
2. `CCF` 软件工程/系统软件/程序设计语言分类页：
   - <https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/>

说明：

1. 上述两个 `CCF` 页面是本文件的权威分类依据。
2. 各 venue 的索引入口这里统一记录为 `DBLP` venue index 页，这类链接通常也是 `CCF` 目录页中给出的可跳转索引入口。
3. 若后续 `CCF` 官方目录调整，以官方页为准，本文件需要同步修订。

## 3. 类别范围与主要方向

`CCF` 这里把“软件工程 / 系统软件 / 程序设计语言”合并为一个大类，因此它不是只包含传统窄义软件工程 venue，而是覆盖了三条彼此交叉的主线：

1. **软件工程**
   - 需求工程、建模、开发过程、自动化软件工程、测试、维护、演化、可靠性、经验软件工程等。
2. **系统软件**
   - 操作系统、中间件、服务计算、系统实现、性能分析、软件基础设施等。
3. **程序设计语言与形式化基础**
   - 编程语言、语义、类型系统、编译、程序分析、约束求解、抽象解释、形式化方法、模型检查等。

对于本博士研究，后续应优先关注其中更容易与“LLM + 状态机建模/验证/修复”接轨的子方向：

1. 形式化方法与模型检查
2. 需求工程
3. 软件测试与验证
4. 软件可靠性
5. 程序分析
6. 建模与模型驱动工程
7. 运行时验证
8. 与控制系统、实时系统、嵌入式系统、工业系统相关的软件工程工作

## 4. 后续索引时的优先读取建议

如果目标是尽快搭建一个对博士研究最有用的前沿索引，默认建议优先从以下 venue 簇开始：

1. 第一批优先
   - `ICSE`
   - `FSE`
   - `ASE`
   - `ISSTA`
   - `TSE`
   - `TOSEM`
   - `RE`
   - `ICSME`
   - `SANER`
   - `STVR`
2. 第二批优先
   - `FM`
   - `VMCAI`
   - `SPIN`
   - `ATVA`
   - `RV`
   - `ICST`
   - `MEMOCODE`
   - `MoDELS`
   - `CAiSE`
3. 谨慎按标题筛选后再跟进
   - `PLDI`
   - `POPL`
   - `TOPLAS`
   - `PACM PL`
   - `SOSP`
   - `OSDI`
   - `Middleware`
   - `HotOS`

最后一组 venue 并非不重要，而是它们更容易混入与当前博士研究主线关系较远的纯系统或纯语言工作，因此后续更适合依赖标题和摘要做严格初筛。

## 5. A 类会议

| 缩写 | 全称 | 主要方向 | 索引页 |
|---|---|---|---|
| `PLDI` | ACM SIGPLAN Conference on Programming Language Design and Implementation | 编程语言设计、编译、程序分析、运行时系统 | [DBLP](http://dblp.uni-trier.de/db/conf/pldi/) |
| `POPL` | ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages | 程序设计语言理论、语义、类型系统、形式化基础 | [DBLP](http://dblp.uni-trier.de/db/conf/popl/) |
| `FSE` | ACM International Conference on the Foundations of Software Engineering | 软件工程基础、开发工具、分析、测试、维护 | [DBLP](http://dblp.uni-trier.de/db/conf/sigsoft/) |
| `SOSP` | ACM Symposium on Operating Systems Principles | 操作系统原理、系统抽象、并发与分布式基础 | [DBLP](http://dblp.uni-trier.de/db/conf/sosp/) |
| `OOPSLA` | Conference on Object-Oriented Programming Systems, Languages,and Applications | 面向对象、程序设计语言、软件设计与运行时 | [DBLP](http://dblp.uni-trier.de/db/conf/oopsla/) |
| `ASE` | International Conference on Automated Software Engineering | 自动化软件工程、分析、测试、修复、生成 | [DBLP](http://dblp.uni-trier.de/db/conf/kbse/) |
| `ICSE` | International Conference on Software Engineering | 软件工程全生命周期、方法、工具与实证研究 | [DBLP](http://dblp.uni-trier.de/db/conf/icse/) |
| `ISSTA` | International Symposium on Software Testing and Analysis | 软件测试、程序分析、缺陷定位与验证 | [DBLP](http://dblp.uni-trier.de/db/conf/issta/) |
| `OSDI` | USENIX Symposium on Operating Systems Design and Implementation | 操作系统设计实现、系统基础设施、存储与云系统 | [DBLP](http://dblp.uni-trier.de/db/conf/osdi/) |
| `FM` | International Symposium on Formal Methods | 形式化建模、规格说明、验证与证明 | [DBLP](http://dblp.uni-trier.de/db/conf/fm/) |

## 6. A 类期刊

| 缩写 | 全称 | 主要方向 | 索引页 |
|---|---|---|---|
| `TOPLAS` | ACM Transactions on Programming Languages and Systems | 程序设计语言、编译、运行时与语言理论 | [DBLP](http://dblp.uni-trier.de/db/journals/toplas/) |
| `TOSEM` | ACM Transactions on Software Engineering and Methodology | 软件工程方法学、过程、建模、分析与工具 | [DBLP](http://dblp.uni-trier.de/db/journals/tosem/) |
| `TSE` | IEEE Transactions on Software Engineering | 软件工程主干期刊，覆盖需求、分析、测试、维护、实证等 | [DBLP](http://dblp.uni-trier.de/db/journals/tse/) |
| `TSC` | IEEE Transactions on Services Computing | 服务计算、服务系统工程、云与服务软件 | [DBLP](http://dblp.uni-trier.de/db/journals/tsc/) |

## 7. B 类会议

| 缩写 | 全称 | 主要方向 | 索引页 |
|---|---|---|---|
| `ECOOP` | European Conference on Object-Oriented Programming | 面向对象、语言设计、运行时与软件结构 | [DBLP](http://dblp.uni-trier.de/db/conf/ecoop/) |
| `ETAPS` | European Joint Conferences on Theory and Practice of Software | 软件理论、形式化方法、分析与验证 umbrella venue | [DBLP](http://dblp.uni-trier.de/db/conf/etaps/) |
| `ICPC` | IEEE International Conference on Program Comprehension | 程序理解、代码认知、维护与演化 | [DBLP](http://dblp.uni-trier.de/db/conf/iwpc/) |
| `RE` | IEEE International Requirements Engineering Conference | 需求工程、需求建模、规格与演化 | [DBLP](http://dblp.uni-trier.de/db/conf/re/) |
| `CAiSE` | International Conference on Advanced Information Systems Engineering | 信息系统工程、过程建模、建模方法 | [DBLP](http://dblp.uni-trier.de/db/conf/caise/) |
| `ICFP` | ACM SIGPLAN International Conference on Function Programming | 函数式编程、语言设计、类型系统 | [DBLP](http://dblp.uni-trier.de/db/conf/icfp/) |
| `LCTES` | ACM SIGPLAN/SIGBED International Conference on Languages, Compilers andTools for Embedded Systems | 嵌入式系统语言、编译与工具 | [DBLP](http://dblp.uni-trier.de/db/conf/lctrts/) |
| `MoDELS` | ACM/IEEE International Conference on Model Driven Engineering Languages and Systems | 模型驱动工程、建模语言、模型转换 | [DBLP](http://dblp.uni-trier.de/db/conf/models/) |
| `CP` | International Conference on Principles and Practice of Constraint Programming | 约束编程、求解、建模与搜索 | [DBLP](http://dblp.uni-trier.de/db/conf/cp/) |
| `ICSOC` | International Conference on Service Oriented Computing | 面向服务计算、服务系统建模与工程 | [DBLP](http://dblp.uni-trier.de/db/conf/icsoc/) |
| `SANER` | IEEE International Conference on Software Analysis, Evolution,and Reengineering | 软件分析、演化、逆向与重构 | [DBLP](http://dblp.uni-trier.de/db/conf/wcre/) |
| `ICSME` | International Conference on Software Maintenance and Evolution | 软件维护、演化、程序理解、技术债 | [DBLP](http://dblp.uni-trier.de/db/conf/icsm/) |
| `VMCAI` | International Conference on Verification,Model Checking, and Abstract Interpretation | 验证、模型检查、抽象解释、程序分析 | [DBLP](http://dblp.uni-trier.de/db/conf/vmcai/) |
| `ICWS` | IEEE International Conference on Web Services | Web 服务、服务组合、服务系统 | [DBLP](http://dblp.uni-trier.de/db/conf/icws/) |
| `Middleware` | International Middleware Conference | 中间件、分布式平台、系统软件基础设施 | [DBLP](http://dblp.uni-trier.de/db/conf/middleware/) |
| `SAS` | International Static Analysis Symposium | 静态分析、抽象解释、程序性质推断 | [DBLP](http://dblp.uni-trier.de/db/conf/sas/) |
| `ESEM` | International Symposium on Empirical Software Engineering and Measurement | 经验软件工程、测量、数据驱动软件研究 | [DBLP](http://dblp.uni-trier.de/db/conf/esem/) |
| `ISSRE` | IEEE International Symposium on Software Reliability Engineering | 软件可靠性、故障、容错与质量保障 | [DBLP](http://dblp.uni-trier.de/db/conf/issre/) |
| `HotOS` | USENIX Workshop on Hot Topics in Operating Systems | 操作系统前沿想法、系统设计新问题 | [DBLP](http://dblp.uni-trier.de/db/conf/hotos/) |
| `CC` | International Conference on Compiler Construction | 编译构造、程序变换、编译优化 | [DBLP](https://dblp.uni-trier.de/db/conf/cc/) |

## 8. B 类期刊

| 缩写 | 全称 | 主要方向 | 索引页 |
|---|---|---|---|
| `ASE` | Automated Software Engineering | 自动化软件工程、自动分析、自动修复、生成 | [DBLP](http://dblp.uni-trier.de/db/journals/ase/) |
| `ESE` | Empirical Software Engineering | 经验软件工程、数据分析、实证研究 | [DBLP](http://dblp.uni-trier.de/db/journals/ese/) |
| `IETS` | IET Software | 工程化软件方法、应用型软件工程 | [DBLP](https://dblp.uni-trier.de/db/journals/iet-sen) |
| `IST` | Information and Software Technology | 软件与信息系统方法、工具与评估 | [DBLP](http://dblp.uni-trier.de/db/journals/infsof/index.html) |
| `JFP` | Journal of Functional Programming | 函数式编程、语言理论与实现 | [DBLP](http://dblp.uni-trier.de/db/journals/jfp/) |
| `JSEP` | Journal of Software: Evolution and Process | 软件演化、软件过程、维护与持续工程 | [DBLP](http://dblp.uni-trier.de/db/journals/smr/) |
| `JSS` | Journal of Systems and Software | 系统与软件工程、方法、工具、评估 | [DBLP](http://dblp.uni-trier.de/db/journals/jss/) |
| `RE` | Requirements Engineering | 需求工程、规格、目标建模与变更管理 | [DBLP](http://dblp.uni-trier.de/db/journals/re/) |
| `SCP` | Science of Computer Programming | 程序设计、软件方法、形式化与实现 | [DBLP](http://dblp.uni-trier.de/db/journals/scp/) |
| `SoSyM` | Software and Systems Modeling | 软件与系统建模、模型驱动工程 | [DBLP](http://dblp.uni-trier.de/db/journals/sosym/) |
| `STVR` | Software Testing, Verification and Reliability | 软件测试、验证与可靠性 | [DBLP](http://dblp.uni-trier.de/db/journals/stvr/index.html) |
| `SPE` | Software: Practice and Experience | 软件实践、工程经验、系统实现与经验总结 | [DBLP](http://dblp.uni-trier.de/db/journals/spe/) |

说明：`JSEP` 这一行在可检索目录镜像中缩写留空，这里为了后续索引便利，采用常见缩写 `JSEP` 记之。

## 9. C 类会议

| 缩写 | 全称 | 主要方向 | 索引页 |
|---|---|---|---|
| `PEPM` | ACM SIGPLAN Workshop on Partial Evaluation and Program Manipulation | 偏求值、程序变换、元编程 | [DBLP](http://dblp.uni-trier.de/db/conf/pepm/) |
| `PASTE` | ACMSIGPLAN-SIGSOFT Workshop on Program Analysis for Software Tools and Engineering | 程序分析与软件工程工具 | [DBLP](http://dblp.uni-trier.de/db/conf/paste/) |
| `APLAS` | Asian Symposium on Programming Languages and Systems | 程序设计语言、语义、系统与验证 | [DBLP](http://dblp.uni-trier.de/db/conf/aplas/) |
| `APSEC` | Asia-Pacific Software Engineering Conference | 软件工程 broad venue，覆盖开发、分析、测试、维护 | [DBLP](http://dblp.uni-trier.de/db/conf/apsec/) |
| `EASE` | International Conference on Evaluation and Assessment in Software Engineering | 软件工程评估、实证、度量 | [DBLP](http://dblp.uni-trier.de/db/conf/ease/) |
| `ICECCS` | International Conference on Engineering of Complex Computer Systems | 复杂计算机系统工程、体系结构与形式化分析 | [DBLP](http://dblp.uni-trier.de/db/conf/iceccs/) |
| `ICST` | IEEE International Conference on Software Testing, Verification and Validation | 软件测试、验证、确认与质量保障 | [DBLP](http://dblp.uni-trier.de/db/conf/icst/) |
| `ISPASS` | IEEE International Symposium on Performance Analysis of Systems and Software | 系统与软件性能分析、测量与评估 | [DBLP](http://dblp.uni-trier.de/db/conf/ispass/) |
| `SCAM` | IEEE International Working Conference on Source Code Analysis and Manipulation | 源代码分析、理解、变换与重构 | [DBLP](http://dblp.uni-trier.de/db/conf/scam/) |
| `COMPSAC` | International Computer Software and Applications Conference | 计算机软件与应用、工程化系统开发 | [DBLP](http://dblp.uni-trier.de/db/conf/compsac/) |
| `ICFEM` | International Conference on Formal Engineering Methods | 形式化工程方法、规格、验证与建模 | [DBLP](http://dblp.uni-trier.de/db/conf/icfem/) |
| `SSE` | IEEE International Conference on Software Services Engineering | 软件服务工程、服务系统实现与治理 | [DBLP](http://dblp.uni-trier.de/db/conf/IEEEscc/) |
| `ICSSP` | International Conference on Software and System Process | 软件与系统过程、协作、流程改进 | [DBLP](http://dblp.uni-trier.de/db/conf/ispw/) |
| `SEKE` | International Conference on Software Engineering and Knowledge Engineering | 软件工程与知识工程交叉 | [DBLP](http://dblp.uni-trier.de/db/conf/seke/) |
| `QRS` | International Conference on Software Quality, Reliability and Security | 软件质量、可靠性与安全性 | [DBLP](https://dblp.uni-trier.de/db/conf/qrs) |
| `ICSR` | International Conference on Software Reuse | 软件复用、组件复用、可复用工程 | [DBLP](http://dblp.uni-trier.de/db/conf/icsr/) |
| `ICWE` | International Conference on Web Engineering | Web 工程、Web 系统设计与实现 | [DBLP](http://dblp.uni-trier.de/db/conf/icwe/) |
| `SPIN` | International Symposium on Model Checking of Software | 软件模型检查、验证与自动分析 | [DBLP](http://dblp.uni-trier.de/db/conf/spin/index.html) |
| `ATVA` | International Symposium on Automated Technology for Verification and Analysis | 自动化验证与分析、模型检查、形式化方法 | [DBLP](http://dblp.uni-trier.de/db/conf/atva/) |
| `LOPSTR` | International Symposium on Logic-based Program Synthesis and Transformation | 基于逻辑的程序综合与变换 | [DBLP](http://dblp.uni-trier.de/db/conf/lopstr/) |
| `TASE` | Theoretical Aspects of Software Engineering Conference | 软件工程理论、形式化分析与验证 | [DBLP](http://dblp.uni-trier.de/db/conf/tase/) |
| `MSR` | Mining Software Repositories | 软件仓库挖掘、演化分析、数据驱动 SE | [DBLP](http://dblp.uni-trier.de/db/conf/msr/) |
| `REFSQ` | Requirements Engineering: Foundation for Software Quality | 需求工程与软件质量 | [DBLP](http://dblp.uni-trier.de/db/conf/refsq/) |
| `WICSA` | Working IEEE/IFIP Conference on Software Architecture | 软件架构、体系结构设计与评估 | [DBLP](http://dblp.uni-trier.de/db/conf/wicsa/) |
| `Internetware` | Asia-Pacific Symposium on Internetware | Internetware、网络化软件与平台 | [DBLP](https://dblp.org/db/conf/internetware/index.html) |
| `RV` | International Conference on Runtime Verification | 运行时验证、监测、在线分析 | [DBLP](https://dblp.org/db/conf/rv/index.html) |
| `MEMOCODE` | International Conference on Formal Methods and Models for Co-Design | 协同设计的形式化方法与模型 | [DBLP](https://dblp.uni-trier.de/db/conf/memocode/) |

## 10. C 类期刊

| 缩写 | 全称 | 主要方向 | 索引页 |
|---|---|---|---|
| `CL` | Computer Languages, Systems and Structures | 程序设计语言、编译、软件工具与结构 | [DBLP](http://dblp.uni-trier.de/db/journals/cl/index.html) |
| `IJSEKE` | International Journal of Software Engineering and Knowledge Engineering | 软件工程与知识工程交叉 | [DBLP](http://dblp.uni-trier.de/db/journals/ijseke/index.html) |
| `STTT` | International Journal of Software Tools for Technology Transfer | 软件工具、验证工具与技术转移 | [DBLP](http://dblp.uni-trier.de/db/journals/sttt/) |
| `JLAMP` | Journal of Logical and Algebraic Methods in Programming | 逻辑与代数程序方法、语义与形式化 | [DBLP](https://dblp.uni-trier.de/db/journals/jlap/index.html) |
| `JWE` | Journal of Web Engineering | Web 工程、Web 系统设计实现 | [DBLP](http://dblp.uni-trier.de/db/journals/jwe/) |
| `SOCA` | Service Oriented Computing and Applications | 面向服务计算与应用 | [DBLP](http://dblp.uni-trier.de/db/journals/soca/) |
| `SQJ` | Software Quality Journal | 软件质量、质量评估与保障 | [DBLP](http://dblp.uni-trier.de/db/journals/sqj/) |
| `TPLP` | Theory and Practice of Logic Programming | 逻辑程序设计理论与实践 | [DBLP](http://dblp.uni-trier.de/db/journals/tplp/) |
| `PACM PL` | Proceedings of the ACM on Programming Languages | 程序设计语言前沿研究、语义、实现与工具 | [DBLP](https://dblp.org/db/journals/pacmpl/index.html) |

## 11. 后续落地索引时的建议

后续真正开始建往年论文索引时，默认建议：

1. 先从高相关 venue 开始，而不是机械地把全部 `82` 个 venue 同时铺开。
2. 每个 venue 先选近 `3-5` 年做试跑，再决定是否继续回溯更早年份。
3. 对 `SOSP / OSDI / Middleware / HotOS / PLDI / POPL / TOPLAS / PACM PL` 这类混合度较高的 venue，默认更依赖标题和摘要做严格筛选。
4. 对 `FM / VMCAI / SPIN / ATVA / RV / ICST / STVR / RE / MoDELS / CAiSE / MEMOCODE` 这类与当前博士研究更贴近的 venue，可以适当提高跟进优先级。
