# 软件工程学术领域方向树（2025 基线版）

## 1. 文档定位

本文档是 `frontier_index/` 当前使用的软件工程领域分类基线。

它不是一份“2025 热点趋势报告”，而是一份面向索引维护、论文筛查与后续深读规划的**工作型 taxonomy**。它主要解决四个问题：

1. 一篇论文到底属不属于软件工程领域。
2. 如果属于软件工程，它在软件工程内部应落到哪一条主路径。
3. 如果它同时跨了 `PL / systems / formal methods / AI`，到底应该算“非软工”，还是“跨域但软工主导”。
4. 在 `CCF` 的“软件工程/系统软件/程序设计语言”大类里，哪些论文应继续进入软工语料，哪些应被识别为非软工。

本文档与 [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md) 的关系如下：

1. 本文档负责**单篇论文级**的判定标准与软件工程内部路径树。
2. [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md) 负责**venue 级**的主体归属与“软工归属级别”先验。
3. 后续真正做论文分类时，默认是：
   - 先看 venue 级先验；
   - 再按本文的单篇论文标准做最终判定；
   - 最后再回填 `x.x.x` 级的软工主路径。

## 2. 构建依据

这棵树不是凭直觉拍出来的，而是综合以下几类依据形成的：

1. **稳定知识骨架**
   - `SWEBOK v4.0a` 给出了软件工程的稳定知识域框架，并明确软件工程与一般计算机科学相关但不同。[R1]
2. **当前主流社区的问题划分**
   - `ICSE 2025 Research Track` 把研究范围明确整理为 `9` 个 area，包括 `AI for Software Engineering`、`Analytics`、`Architecture and Design`、`Dependability and Security`、`Evolution`、`Human and Social Aspects`、`Requirements and Modeling`、`Software Engineering for AI`、`Testing and Analysis`。[R2]
3. **稳定专门社区对关键子方向的强化**
   - `MSR` 强化了仓库挖掘与软件分析学。[R3]
   - `ICST` 强化了测试、验证、确认与质量保证链条。[R4]
   - `REFSQ` 强化了需求工程的独立主枝地位。[R5]
   - `MODELS` 强化了建模与模型驱动工程。[R6]
   - `ICSA` 强化了软件架构的独立性。[R7]
4. **过去与近期的大领域级路线图**
   - `FoSE 2000` 的《Software Engineering: A Roadmap》把软件工程理解为一个由多个研究专门化方向构成的整体。[R8]
   - `The Future of Software Engineering`（2011）反映了架构、建模、验证、人因、工程化实践等主线的成熟化。[R9]
   - `Continuous software engineering: A roadmap and agenda`（2017）强化了持续工程、持续集成/交付与运行协同作为独立问题域的必要性。[R12]
   - `Collaboration in Software Engineering: A Roadmap`（2007）强化了协作、知识共享和社会技术协调是软件工程内部问题，而不是外围管理附属物。[R13]
   - `SEI` 的 `2021` roadmap 把 `AI-augmented software development`、`continuously evolving systems`、`socio-technical systems`、`AI-enabled systems`、`quantum systems` 提升为长期重要方向。[R10]
   - `Software Engineering for AI-Based Systems: A Survey`（2021）说明 `SE for AI` 已经形成可独立讨论的问题簇，而且其组织方式可以映射回 `SWEBOK` 知识域。[R14]
5. **本仓库当前语料的现实覆盖检查**
   - 当前 [SUMMARY.md](./SUMMARY.md) 记录了 `2025` 年 `CCF` 保留子集索引中的 `5153` 条论文元数据。
   - 当前 `2025` 元数据自动标签的前几类信号分别是：`建模/模型驱动 2026`、`测试与验证 1675`、`LLM/AI for SE 1335`、`可靠性/安全 1127`、`形式化方法 908`、`维护与演化 848`、`需求工程 742`、`经验软件工程 719`。
   - 这说明如果分类树缺少需求/建模、测试/分析/验证、维护/演化、经验研究/仓库挖掘、架构、过程/组织、人因、`AI for SE / SE for AI` 与运行时工程等主枝，就无法覆盖当前软工语料。

## 3. 边界说明与单篇论文判定标准

### 3.1 什么算软件工程

在本仓库里，一篇论文应优先被视为软件工程论文，当且仅当它的**核心研究问题**主要落在以下问题之一：

1. 如何表达、获取、分析、管理和追踪软件需求、规约与设计决策。
2. 如何对软件或软件密集型系统进行建模、规格化、架构化、设计与构造。
3. 如何测试、分析、验证、调试、修复、确认和保证软件质量与可信赖性。
4. 如何维护、演化、发布、部署、运行、观测和持续改进软件。
5. 如何以经验研究、度量、仓库挖掘、过程方法、人因与组织研究来理解和改进软件开发活动。
6. 如何工程化地开发 `AI` 支持的软件开发工具，或工程化地开发、验证、部署与治理带 `AI` 组件的软件系统。

这里的关键词不是“是否写了程序”，而是“是否在回答**软件工程活动**本身的问题”。

### 3.2 一级总类别先于软工细分

截至 **2026-04-05**，`CCF` 对应的官方页面标题是“**软件工程/系统软件/程序设计语言**”，而“**数据库/数据挖掘/内容检索**”是另一张单独的目录页，不属于本路径当前覆盖的大类。[R11]

因此，后续面对本路径中的论文时，第一层总判定默认先落到下面四类之一：

1. `软件工程`
2. `系统软件`
3. `程序设计语言与形式化基础`
4. `跨域/待判定`

只有当最终判定落到 `软件工程`，或“`跨域` 但软工主导”时，才继续进入本文后面的软件工程方向树。

### 3.3 软件工程对象清单

后续判断时，默认把下面这些对象视为典型的“软工对象”：

1. 需求、用户故事、需求文档、规约、属性、assurance case。
2. 模型、状态机、架构、设计、接口、配置、变体与产品线资产。
3. 代码库、提交历史、缺陷报告、补丁、测试用例、测试集、CI/CD 流水线。
4. 发布配置、依赖图、包生态、部署脚本、运行时监测数据、日志、告警、事故单。
5. 开发者、评审者、团队协作过程、软件组织与工程决策。
6. `AI` 系统的数据管线、模型版本、评测集、部署管线、运行时监测与治理工件。

如果论文的主要贡献对象不在这类工件、活动或工程决策上，就要非常谨慎地把它归入软件工程。

### 3.4 默认不算软件工程的情况

以下工作默认**不应**仅因 venue 落在 `CCF` 的该大类中，就被强行归入软件工程：

1. 纯编译优化、纯语言语义、纯类型理论、纯程序逻辑，而没有软件工程问题、工程流程或工程评价。
2. 纯操作系统/网络/存储/体系结构机制，而没有构造、维护、测试、运行、质量、组织或工程治理问题。
3. 纯硬件验证、纯电路验证、纯控制理论或纯数学理论工作。
4. 把代码仓库、程序或系统只当作实验对象，但论文真正回答的问题并不是软件工程问题。

`ICSE 2025` 的 scope 也明确强调：作者需要回答论文是否能为软件工程社区带来新的 insight；仅面向硬件验证的形式化方法论文就不一定落在软件工程范围内。[R2]

### 3.5 邻近学科和跨域论文怎么处理

这里需要明确四条硬口径：

1. **形式化方法不是自动等于软件工程。**
2. **程序分析不是自动等于软件工程。**
3. **PL / systems / AI / FM 论文并不因为用了“software”一词就自动属于软件工程。**
4. **只要核心问题确实是软工问题，且主要方法链条或评估证据是软工导向，就应纳入软件工程。**

因此，本仓库对跨域论文采用“**软工主导则纳入软工**”的规则：

1. 如果论文的核心研究问题是软件工程问题，则纳入软件工程。
2. 如果论文同时跨了 `PL / systems / FM / AI`，但主要方法链条是在改进需求、建模、架构、测试、验证、修复、维护、运维、过程或工程治理，则仍纳入软件工程。
3. 如果论文的主要评估证据也是软件工程证据，例如缺陷发现能力、测试效果、维护性、开发效率、开发者行为、可靠性改进或工程成本改进，则优先按软件工程处理。
4. 如果论文主要回答的是语言理论、系统机制、硬件验证或数学求解问题，而软件只是实验载体，则不纳入软件工程。

### 3.6 单篇论文判定时必须检查的证据

后续判断“一篇论文到底算不算软工论文”时，默认至少检查下面这些证据，且顺序如下：

1. `title`
2. `abstract`
3. `keywords` 或官方主题词
4. `venue` 的官方 scope、call for papers、series page 或社区共识定位
5. 论文的 `introduction / problem statement / conclusion`
6. 若仍不清楚，再看 `method` 与 `evaluation`

默认禁止以下做法：

1. 只看 venue 名称就下结论。
2. 只看标题中的一个关键词就下结论。
3. 只因为论文用了形式化方法、静态分析、`LLM`、控制系统或云系统，就自动把它归到软件工程。

### 3.7 可执行、可检查的判定矩阵

后续默认按下面四个正向维度和一个排除门做检查。

| 维度 | 权重 | 要检查的问题 | 判为“是”的典型信号 |
|---|---:|---|---|
| `D1 核心研究问题` | `3` | 论文真正要解决的问题，是不是软件工程问题？ | 需求、建模、架构、测试、验证、调试、修复、维护、运维、过程、协作、经验研究、仓库挖掘、`AI for SE / SE for AI` |
| `D2 主贡献对象` | `2` | 论文主要改进的对象，是不是软件工程活动、工件或工程决策？ | 需求文档、模型、架构、代码库、测试集、缺陷、补丁、流水线、依赖图、开发流程、开发者协作 |
| `D3 主要方法链条` | `2` | 主要方法是不是软工方法，或明确作用于软工工件/活动？ | 需求分析、建模、架构评估、测试、程序理解、缺陷定位、程序修复、仓库挖掘、过程挖掘、开发者研究、MLOps/DevOps |
| `D4 主要评估证据` | `1` | 主要实验与评估是不是在评价软件工程效果？ | 缺陷发现率、测试覆盖、维护成本、开发效率、可靠性、开发者体验、工程质量、流程改进、部署效果 |
| `X1 排除门` | `-` | 论文的主要创新是不是明确属于非软工主问题？ | 新类型系统、新语义结果、新编译优化、纯系统吞吐/时延机制、纯硬件验证、纯数学求解 |

打分规则如下：

1. `是` 记满分。
2. `部分是` 记 `1` 分。
3. `否` 记 `0` 分。
4. `X1 = 是` 时，不直接自动排除，但会触发“必须额外证明其软工主导”的复核。

### 3.8 最终决策规则

默认按下面的规则落最终结论：

| 判定结果 | 默认规则 |
|---|---|
| `属于软件工程` | `X1 != 是`，且总分 `>= 6`，并且 `D1 >= 2`、`D2 >= 1` |
| `跨域但软工主导` | 总分在 `4-5`；或 `X1 = 是` 但 `D1 >= 2` 且 `D2 + D3 + D4 >= 3` |
| `不属于软件工程` | `D1 = 0` 且 `D2 = 0`；或 `X1 = 是` 且总分 `< 4` |
| `待判定` | 仅凭标题摘要无法稳定判断，或四个维度证据相互冲突 |

为了后续落表可执行，默认再把它压缩成下面这套检查顺序：

1. **先看 `X1`。**
   - 如果论文显然在回答类型系统、语言语义、编译优化、系统吞吐/延迟、硬件验证、纯求解问题，先暂记为“非软工候选”。
2. **再看 `D1` 和 `D2`。**
   - 只要核心研究问题和主贡献对象明显落在软件工程活动与工件上，就应显著倾向软工。
3. **对跨域论文，重点看 `D3` 和 `D4`。**
   - 尤其是当主要方法链条本身就是软工方法，或者主要评估证据是在测软工效果时，应按“跨域但软工主导”纳入。
4. **只要软件不是问题本身，而只是实验载体，就不要归进软工。**

### 3.9 一眼排除与一眼纳入规则

下面这些情况默认可以直接判为“非软工”：

1. 论文的核心创新是一个新类型系统、一个新语义结果、一个新编译优化，而评估也主要是性能、可证明性或理论性质。
2. 论文的核心创新是操作系统、网络、存储、调度、硬件协同等机制，而评估主要是吞吐、延迟、资源利用率。
3. 论文主要在证明某个逻辑系统、求解算法、定理证明流程，而没有把问题落到软件工程活动。
4. 论文只是在 `GitHub`、开源仓库或代码数据集上做实验，但研究问题不是软件工程问题。

下面这些情况默认要小心，不应因为它们用了邻近学科的方法就误判为“非软工”：

1. 用形式化方法做需求规格提取、规约一致性检查、软件验证、运行时监测。
2. 用程序分析做测试生成、缺陷定位、修复、程序理解、依赖治理、安全工程。
3. 用系统技术做发布工程、运维、可观测性、可靠性工程、依赖与供应链治理。
4. 用 `LLM/AI` 做代码生成、测试、需求分析、文档生成、开发者协作支持。
5. 面向 `CPS / 嵌入式 / 云 / Web / AI systems`，但论文真正解决的是建模、测试、验证、维护、运维或工程治理问题。

### 3.10 容易混淆的边界例子

| 论文类型 | 默认判定 | 原因 |
|---|---|---|
| 用静态分析优化编译器寄存器分配 | `不属于软件工程` | `D1` 是编译优化问题，评估也主要是性能 |
| 用静态分析生成测试输入并评估缺陷发现能力 | `属于软件工程` | 方法来自程序分析，但问题、对象和证据都落在测试 |
| 用模型检查验证硬件电路时序 | `不属于软件工程` | 形式化方法不自动等于软件工程，问题本体是硬件验证 |
| 用模型检查做软件需求规约一致性与运行时监测 | `属于软件工程` | 规约、验证与监测对象都是软工工件和活动 |
| 研究云平台调度算法的吞吐/时延改进 | `大多不属于软件工程` | 更像系统机制论文，除非显式回答发布、运维或治理问题 |
| 研究 CI/CD 回滚策略、发布闸门或依赖治理 | `属于软件工程` | 虽然使用系统技术，但问题本体是持续工程与运行治理 |

## 4. 软件工程学术方向 ASCII 树（三级路径版）

下面给出当前推荐使用的 `x.x.x` 级方向树。每个 `x.x.x` 叶子节点后面都附了典型论文问题/例子，用于后续实际分类定位。

```text
Software Engineering
|-- 1. 需求、规格与建模
|   |-- 1.1 需求工程
|   |   |-- 1.1.1 需求获取与发现（访谈、用户反馈挖掘、需求抽取、用户故事）
|   |   |-- 1.1.2 需求分析、协商与优先级（goal modeling、冲突协调、优先级排序）
|   |   |-- 1.1.3 需求质量与歧义控制（歧义检测、完备性、需求一致性）
|   |   |-- 1.1.4 需求追踪、变更与演化（traceability、impact analysis、rationale）
|   |   `-- 1.1.5 需求知识复用与需求债务治理（requirements reuse、pattern libraries、requirements debt）
|   |-- 1.2 规格说明与形式化
|   |   |-- 1.2.1 形式化规约与契约（LTL/CTL、contracts、invariants、Alloy）
|   |   |-- 1.2.2 自然语言到规约/属性（NL2LTL、spec mining、property extraction）
|   |   |-- 1.2.3 规约质量与一致性（satisfiability、consistency、completeness）
|   |   `-- 1.2.4 合规与 assurance 规约（safety case、标准约束、compliance rules）
|   |-- 1.3 建模与模型驱动工程
|   |   |-- 1.3.1 建模语言与元模型（UML/SysML/DSL/metamodel）
|   |   |-- 1.3.2 模型转换、同步与协同（transformation、co-evolution、round-trip）
|   |   |-- 1.3.3 模型分析、仿真与验证（simulation、reachability、model checking）
|   |   |-- 1.3.4 基于模型的生成、测试与运行时支持（MBT、code generation、digital twins）
|   |   `-- 1.3.5 模型质量、仓库与治理（model quality、repository mining、model management）
|   `-- 1.4 变体管理与产品线
|       |-- 1.4.1 特征建模与配置（feature model、option dependency、product config）
|       |-- 1.4.2 产品线架构与资产复用（SPL、core asset、family architecture）
|       |-- 1.4.3 变体感知分析、测试与验证（family-based analysis/testing、config-aware checking）
|       `-- 1.4.4 可配置系统演化与依赖（option interaction、variability evolution）
|-- 2. 架构、设计与构造
|   |-- 2.1 软件架构
|   |   |-- 2.1.1 架构描述与恢复（ADL、architecture reconstruction、architecture documentation）
|   |   |-- 2.1.2 架构评估与推理（trade-off analysis、architecture debt、quality reasoning）
|   |   |-- 2.1.3 架构演化与重构（microservice extraction、decomposition、migration）
|   |   |-- 2.1.4 云/服务/平台架构（SOA、microservices、serverless topology、platform architecture）
|   |   `-- 2.1.5 架构知识、决策与不确定性管理（architecture decisions、ADRs、hypotheses engineering）
|   |-- 2.2 软件设计
|   |   |-- 2.2.1 设计原则、模式与反模式（patterns、anti-patterns、design heuristics）
|   |   |-- 2.2.2 模块化、依赖与解耦（coupling/cohesion、dependency structure、encapsulation）
|   |   |-- 2.2.3 API、接口与协议设计（API usability、versioning、protocol evolution）
|   |   `-- 2.2.4 技术债与设计质量（maintainability、design smell、debt repayment）
|   `-- 2.3 软件构造
|       |-- 2.3.1 代码生成、脚手架与 DSL 工程（code generators、low-code、language workbench）
|       |-- 2.3.2 构建工具链与开发环境（build system、IDE、toolchain、workspace automation）
|       |-- 2.3.3 组件、包与集成工程（component assembly、package engineering、integration）
|       `-- 2.3.4 协作式编码与开发支持（pair programming support、IDE assistant、review assistant）
|-- 3. 测试、分析、验证与修复
|   |-- 3.1 软件测试
|   |   |-- 3.1.1 测试生成与增强（test generation、test amplification、oracle generation）
|   |   |-- 3.1.2 回归测试与测试选择（regression testing、test prioritization、test selection）
|   |   |-- 3.1.3 模糊、搜索式、变异与性质驱动测试（fuzzing、SBST、mutation/metamorphic/property-based testing）
|   |   |-- 3.1.4 场景化测试（GUI/Web/mobile/CPS/AI system testing）
|   |   `-- 3.1.5 测试质量、脆弱性与测试资产维护（flaky tests、test debt、test suite maintenance）
|   |-- 3.2 程序分析
|   |   |-- 3.2.1 静态分析与抽象解释（dataflow、taint、abstract interpretation、type-based analysis）
|   |   |-- 3.2.2 动态与混合分析（instrumentation、trace analysis、hybrid analysis）
|   |   |-- 3.2.3 面向质量属性的分析（vulnerability analysis、reliability analysis、compliance analysis）
|   |   `-- 3.2.4 分析驱动的理解、重构与综合（analysis-guided refactoring、repair、synthesis）
|   |-- 3.3 验证与确认
|   |   |-- 3.3.1 面向软工问题的形式化验证（model checking、theorem proving、SMT-based verification）
|   |   |-- 3.3.2 运行时验证与运行时监测（runtime verification、monitor synthesis、online checking）
|   |   |-- 3.3.3 assurance、认证与合规验证（safety assurance、certification evidence、compliance verification）
|   |   `-- 3.3.4 基准、工具评测与可复现验证（benchmarks、tool competitions、reproducibility）
|   `-- 3.4 调试、定位与修复
|       |-- 3.4.1 调试、分诊与根因分析（debugging workflow、bug triage、root cause analysis）
|       |-- 3.4.2 缺陷定位、补丁生成与程序修复（fault localization、APR、patch generation）
|       |-- 3.4.3 补丁正确性与回归控制（patch validation、regression prevention、repair assessment）
|       `-- 3.4.4 恢复与自愈（error recovery、rollback、self-healing resolution）
|-- 4. 演化、交付与运行
|   |-- 4.1 维护与演化
|   |   |-- 4.1.1 缺陷修复与维护性修正（bug fixing、hotfix、backport）
|   |   |-- 4.1.2 重构、重模块化与代码清理（refactoring、remodularization、cleanup）
|   |   |-- 4.1.3 API、依赖与库演化（API evolution、dependency upgrade、library migration）
|   |   |-- 4.1.4 迁移、现代化与遗留系统更新（legacy modernization、cloud migration、language migration）
|   |   `-- 4.1.5 技术债、克隆与可维护性治理（technical debt、clone management、maintainability governance）
|   |-- 4.2 程序理解与逆向工程
|   |   |-- 4.2.1 代码搜索、导航与摘要（code search、navigation、summarization）
|   |   |-- 4.2.2 痕迹、文档与知识恢复（trace recovery、documentation mining、knowledge graph）
|   |   |-- 4.2.3 架构与代码库重建（system reconstruction、dependency recovery、architecture recovery）
|   |   |-- 4.2.4 克隆、相似性与理解支持（clone detection、similarity search、comprehension aid）
|   |   `-- 4.2.5 文档工程、解释与设计 rationale 恢复（documentation engineering、comment/doc evolution、rationale recovery）
|   |-- 4.3 发布、配置与持续工程
|   |   |-- 4.3.1 版本、配置与构建工程（version/config management、build reproducibility）
|   |   |-- 4.3.2 CI/CD 与发布工程（release engineering、continuous delivery、rollback pipeline）
|   |   |-- 4.3.3 流水线与基础设施自动化（pipeline engineering、IaC、DevOps automation）
|   |   `-- 4.3.4 依赖、供应链与包生态治理（package management、dependency governance、supply chain）
|   `-- 4.4 运维与运行
|       |-- 4.4.1 可观测性、日志与异常检测（observability、telemetry、log analytics、anomaly detection）
|       |-- 4.4.2 事故诊断、回滚与恢复（incident response、rollback、SRE diagnosis）
|       |-- 4.4.3 运行时重配置与自适应运维（autoscaling、runtime reconfiguration、adaptive operation）
|       `-- 4.4.4 持续 assurance 与运行时治理（runtime policy enforcement、continuous assurance、runtime governance）
|-- 5. 质量属性与可信赖性
|   |-- 5.1 可靠性、可用性与韧性
|   |   |-- 5.1.1 故障预测与失效分析（fault prediction、failure analysis、incident mining）
|   |   |-- 5.1.2 容错、韧性与恢复能力（fault tolerance、resilience engineering、graceful degradation）
|   |   |-- 5.1.3 发布可靠性与服务可用性（release reliability、availability analysis、SLO engineering）
|   |   |-- 5.1.4 可恢复性与连续运营（recoverability、business continuity、disaster response）
|   |   `-- 5.1.5 功能安全、危害分析与 safety assurance（functional safety、hazard analysis、safety case）
|   |-- 5.2 安全、隐私、公平与合规
|   |   |-- 5.2.1 安全开发与漏洞治理（secure SDLC、vulnerability management、patch management）
|   |   |-- 5.2.2 隐私工程与数据治理（privacy requirements、privacy compliance、data governance）
|   |   |-- 5.2.3 供应链安全与可追溯信任（SBOM、provenance、dependency trust）
|   |   `-- 5.2.4 公平性、问责与法规符合（fairness assurance、accountability、regulatory compliance）
|   |-- 5.3 性能、资源、能耗与可持续性
|   |   |-- 5.3.1 性能建模、基准与调优（benchmarking、profiling、performance diagnosis）
|   |   |-- 5.3.2 资源与成本优化（resource scheduling、capacity planning、cost optimization）
|   |   |-- 5.3.3 能耗与碳感知工程（energy-aware engineering、carbon-aware software）
|   |   `-- 5.3.4 扩展性、吞吐与时延保证（scalability engineering、latency assurance、throughput control）
|   `-- 5.4 可用性、可访问性与用户体验
|       |-- 5.4.1 面向开发者的可用性（API usability、tool usability、developer UX）
|       |-- 5.4.2 面向终端用户的可用性与可访问性（accessibility、inclusive UI、UX quality）
|       |-- 5.4.3 人本评估与交互质量（human-centered evaluation、usability study）
|       `-- 5.4.4 包容性软件工程（diversity support、developer accommodation、inclusive practice）
|-- 6. 过程、组织、人员与证据
|   |-- 6.1 软件过程与方法学
|   |   |-- 6.1.1 敏捷、精益与 DevOps 方法（agile、lean、DevOps、continuous improvement）
|   |   |-- 6.1.2 过程挖掘、符合性与改进（process mining、conformance checking、process improvement）
|   |   |-- 6.1.3 治理、合规与过程追踪（process traceability、governance、auditability）
|   |   `-- 6.1.4 社会技术协调与流程设计（coordination mechanism、workflow design、handoff）
|   |-- 6.2 项目管理与工程经济
|   |   |-- 6.2.1 估算、计划与排程（effort estimation、planning、scheduling）
|   |   |-- 6.2.2 风险、价值与优先级（risk management、value-driven engineering、prioritization）
|   |   |-- 6.2.3 成本、ROI 与生产率（cost modeling、ROI、productivity analysis）
|   |   `-- 6.2.4 组合治理与决策支持（portfolio management、decision support、governance analytics）
|   |-- 6.3 经验软件工程与证据综合
|   |   |-- 6.3.1 实验、案例研究与调查（experiment、case study、survey）
|   |   |-- 6.3.2 定性、混合方法与人类研究（qualitative coding、mixed methods、human study）
|   |   |-- 6.3.3 系统综述、mapping 与 meta-analysis（SLR、SMS、meta-analysis）
|   |   |-- 6.3.4 replication、benchmark 与开放科学（replication package、benchmarking、open science）
|   |   `-- 6.3.5 路线图、研究议程与领域回顾（roadmap、research agenda、retrospective）
|   |-- 6.4 挖掘软件仓库与软件分析学
|   |   |-- 6.4.1 代码、提交、issue 与 PR 挖掘（commit mining、issue mining、PR analytics）
|   |   |-- 6.4.2 团队、社区、评审与 CI 分析（code review analytics、team analytics、CI mining）
|   |   |-- 6.4.3 度量、预测与风险模型（defect prediction、risk modeling、software metrics）
|   |   `-- 6.4.4 生态、依赖与开源分析（ecosystem analysis、dependency analytics、OSS evolution）
|   `-- 6.5 人因、协作、社区与教育
|       |-- 6.5.1 开发者认知、生产力与福祉（cognition、productivity、wellbeing、ADHD/疲劳/压力）
|       |-- 6.5.2 协作、评审与知识共享（collaboration、code review、knowledge sharing）
|       |-- 6.5.3 开源社区、多样性与治理（OSS governance、community health、diversity）
|       `-- 6.5.4 教育、培训与入门支持（SE education、onboarding、training、curriculum）
|-- 7. 智能化软件工程与 AI 系统工程
|   |-- 7.1 AI for SE
|   |   |-- 7.1.1 代码生成、补全与变换（code generation、completion、transformation）
|   |   |-- 7.1.2 AI 支持的测试、分析与修复（AI-based testing、bug detection、APR）
|   |   |-- 7.1.3 AI 支持的需求、建模与文档（requirements summarization、model completion、doc generation）
|   |   |-- 7.1.4 AI 支持的架构、设计与工程决策（architecture/design assistance、decision support、planning）
|   |   `-- 7.1.5 人机协同开发与评估（pairing with LLM、human-AI workflow、trust/calibration）
|   |-- 7.2 SE for AI
|   |   |-- 7.2.1 数据、模型与管线工程（data pipeline、feature pipeline、model lifecycle）
|   |   |-- 7.2.2 AI 系统需求、建模与文档工程（requirements for AI systems、ML model cards、system modeling）
|   |   |-- 7.2.3 AI 测试、验证与监测（AI testing、robustness assurance、drift monitoring）
|   |   |-- 7.2.4 MLOps、部署与演化（MLOps、deployment pipeline、model rollback）
|   |   `-- 7.2.5 AI 系统治理、安全与合规（AI governance、safety case、regulatory assurance）
|   `-- 7.3 智能自治与自适应系统
|       |-- 7.3.1 自适应与反馈回路工程（MAPE-K、feedback loop、adaptive planning）
|       |-- 7.3.2 agent 软件工程（multi-agent workflows、agent orchestration、agent debugging）
|       |-- 7.3.3 自愈、自优化与自治运行（self-healing、self-optimization、autonomic operation）
|       `-- 7.3.4 自适应行为 assurance（adaptive assurance、runtime assurance、policy safety）
`-- 8. 应用与系统场景
    |-- 8.1 嵌入式、实时、IoT、CPS、机器人
    |   |-- 8.1.1 工业控制、汽车、航空与医疗软件（industrial control、avionics、medical device）
    |   |-- 8.1.2 机器人与自主系统（robot software、autonomous robotics、ROS engineering）
    |   |-- 8.1.3 IoT、边缘与数字孪生软件（IoT software、edge platform、digital twin engineering）
    |   `-- 8.1.4 安全关键认证场景（ISO 26262、DO-178C、certification-oriented assurance）
    |-- 8.2 Web、移动、云、服务与平台生态
    |   |-- 8.2.1 Web 与移动应用工程（web app engineering、mobile app evolution、GUI engineering）
    |   |-- 8.2.2 云原生、serverless 与平台工程（cloud-native、serverless、platform engineering）
    |   |-- 8.2.3 服务系统与 API 生态（service composition、API ecosystem、service governance）
    |   `-- 8.2.4 大规模分布式应用运行（distributed application operations、SRE at scale）
    |-- 8.3 安全关键、工业软件与系统之系统
    |   |-- 8.3.1 mission/safety critical 软件（mission critical、hazard analysis、formal assurance）
    |   |-- 8.3.2 企业级与业务关键软件（enterprise systems、business-critical workflows）
    |   |-- 8.3.3 系统之系统与互操作（system-of-systems、interoperability、integration assurance）
    |   `-- 8.3.4 受监管软件领域（regulated domains、auditability、compliance engineering）
    |-- 8.4 社会技术系统与开放生态
    |   |-- 8.4.1 开源软件生态（OSS ecosystem、community evolution、dependency commons）
    |   |-- 8.4.2 软件供应链与平台生态（supply chain ecosystem、package registry、platform governance）
    |   |-- 8.4.3 低代码、众包与终端用户开发（low-code engineering、citizen development、crowd engineering）
    |   `-- 8.4.4 政策、伦理与生态治理（software policy、ecosystem governance、ethical engineering）
    `-- 8.5 新型软件系统
        |-- 8.5.1 AI-enabled systems（AI-native software、copilot-enabled products、AI-heavy applications）
        |-- 8.5.2 quantum software engineering（quantum program engineering、testing、resource reasoning）
        |-- 8.5.3 大模型原生与 agentic 软件系统（LLM-native apps、agentic workflows、tool-using systems）
        |-- 8.5.4 异构与新型计算平台的软件工程（GPU/edge/classical-quantum orchestration）
        `-- 8.5.5 科学计算、数据密集与高性能软件工程（scientific software、HPC、data-intensive software）
```

### 4.1 `1.x` 需求、规格与建模的 `x.x.x` 例子总览

| 二级方向 | `x.x.x` 叶节点与典型例子 |
|---|---|
| `1.1 需求工程` | `1.1.1` 从用户反馈、工单、访谈、论坛贴中抽取需求与用户故事；`1.1.2` 做需求优先级排序、目标冲突协调、利益相关者协商；`1.1.3` 检测需求歧义、缺失、矛盾和不可验证表述；`1.1.4` 建立需求到模型/测试/代码的追踪并做变更影响分析；`1.1.5` 研究需求复用、需求知识库、需求模式和需求技术债 |
| `1.2 规格说明与形式化` | `1.2.1` 编写或推导契约、时序属性、不变式、Alloy/LTL/CTL 规约；`1.2.2` 从自然语言需求或日志自动抽取形式化属性；`1.2.3` 检查规约一致性、可满足性和完备性；`1.2.4` 构建 safety case、compliance rule 和 assurance 规约 |
| `1.3 建模与模型驱动工程` | `1.3.1` 设计 `UML/SysML/DSL`、元模型与建模语言扩展；`1.3.2` 做模型转换、协同编辑、共演化与 round-trip engineering；`1.3.3` 用模型做仿真、可达性分析、模型检查与一致性分析；`1.3.4` 进行基于模型的代码生成、模型驱动测试、数字孪生与运行时支持；`1.3.5` 研究模型质量、模型仓库、模型资产治理和模型管理 |
| `1.4 变体管理与产品线` | `1.4.1` 建立 feature model、配置约束和产品派生规则；`1.4.2` 设计产品线架构和核心复用资产；`1.4.3` 做 config-aware analysis/testing 和 family-based verification；`1.4.4` 研究变体演化、选项交互、配置债务与可配置系统依赖治理 |

### 4.2 `2.x` 架构、设计与构造的 `x.x.x` 例子总览

| 二级方向 | `x.x.x` 叶节点与典型例子 |
|---|---|
| `2.1 软件架构` | `2.1.1` 做架构描述、文档生成、架构恢复和依赖重建；`2.1.2` 分析性能/可靠性/演化性 trade-off 与 architecture debt；`2.1.3` 研究单体拆分、微服务迁移、架构重构与演化治理；`2.1.4` 面向云、服务、平台、serverless 的拓扑与治理架构；`2.1.5` 研究架构决策、架构知识、架构 rationale 和架构不确定性管理 |
| `2.2 软件设计` | `2.2.1` 研究设计模式、反模式、设计启发式与设计质量；`2.2.2` 做模块化、依赖解耦、职责划分和耦合/内聚分析；`2.2.3` 关注 `API`、接口、协议、版本兼容与可用性设计；`2.2.4` 研究技术债、设计坏味道、可维护性与设计层面的债务偿还 |
| `2.3 软件构造` | `2.3.1` 做代码生成、低代码、脚手架与 `DSL` 工程；`2.3.2` 关注 build system、`IDE`、workspace、toolchain 与开发环境；`2.3.3` 研究组件装配、包管理、集成流水线与工程装配；`2.3.4` 关注协作编码、review assistant、pair programming support 与开发助手 |

### 4.3 `3.x` 测试、分析、验证与修复的 `x.x.x` 例子总览

| 二级方向 | `x.x.x` 叶节点与典型例子 |
|---|---|
| `3.1 软件测试` | `3.1.1` 自动生成测试用例、增强测试、生成 oracle；`3.1.2` 做回归测试选择、优先级排序和测试影响分析；`3.1.3` 研究 fuzzing、搜索式测试、性质驱动测试、变异测试与 metamorphic testing；`3.1.4` 面向 `GUI/Web/mobile/CPS/AI systems` 的场景化测试；`3.1.5` 研究 flaky tests、test debt、test smell 与测试资产维护 |
| `3.2 程序分析` | `3.2.1` 做静态分析、抽象解释、污点分析、数据流分析；`3.2.2` 做动态分析、插桩、trace 分析与静动态混合分析；`3.2.3` 面向安全、隐私、可靠性、合规等质量属性做专项分析；`3.2.4` 让分析结果驱动程序理解、重构、修复或代码综合 |
| `3.3 验证与确认` | `3.3.1` 用模型检查、定理证明、`SMT` 等验证软件规约与行为；`3.3.2` 做运行时验证、监测器合成、在线规则检查；`3.3.3` 构建安全认证、标准合规、assurance evidence 和 certification argument；`3.3.4` 构建验证 benchmark、工具竞赛、可复现验证流程 |
| `3.4 调试、定位与修复` | `3.4.1` 关注 bug triage、调试流程、根因定位和故障分诊；`3.4.2` 研究 fault localization、自动程序修复、补丁生成与建议；`3.4.3` 检查补丁正确性、回归风险与 repair quality；`3.4.4` 做 rollback、恢复、自愈决策和故障处置闭环 |

### 4.4 `4.x` 演化、交付与运行的 `x.x.x` 例子总览

| 二级方向 | `x.x.x` 叶节点与典型例子 |
|---|---|
| `4.1 维护与演化` | `4.1.1` 研究 bug fix、hotfix、backport 与维护性修正；`4.1.2` 做重构、remodularization、代码清理与结构重整；`4.1.3` 关注 `API` 演化、依赖升级、库迁移与版本兼容；`4.1.4` 研究遗留系统现代化、语言迁移、上云迁移与体系迁移；`4.1.5` 研究技术债、克隆债、维护性债务和长期治理 |
| `4.2 程序理解与逆向工程` | `4.2.1` 做代码搜索、导航、摘要和程序解释；`4.2.2` 进行 trace recovery、文档挖掘、知识图谱与知识恢复；`4.2.3` 重建架构、依赖关系和大型代码库结构；`4.2.4` 研究 clone detection、相似性搜索、理解支持与 code-to-code retrieval；`4.2.5` 研究开发者文档、注释、说明文本、设计 rationale 和解释生成/恢复 |
| `4.3 发布、配置与持续工程` | `4.3.1` 关注版本管理、配置管理、可复现构建与 build engineering；`4.3.2` 研究持续集成、持续交付、发布闸门与 rollback pipeline；`4.3.3` 研究流水线编排、`IaC`、基础设施自动化与 DevOps automation；`4.3.4` 关注依赖治理、包生态、供应链风险与 provenance 管理 |
| `4.4 运维与运行` | `4.4.1` 做可观测性、日志分析、遥测聚合和异常检测；`4.4.2` 关注事故诊断、根因定位、运行时回滚与恢复；`4.4.3` 研究 autoscaling、runtime reconfiguration 与自适应运维；`4.4.4` 研究运行时策略执行、continuous assurance 和 runtime governance |

### 4.5 `5.x` 质量属性与可信赖性的 `x.x.x` 例子总览

| 二级方向 | `x.x.x` 叶节点与典型例子 |
|---|---|
| `5.1 可靠性、可用性与韧性` | `5.1.1` 做故障预测、失效模式分析、incident mining；`5.1.2` 研究容错、韧性工程、优雅降级与恢复策略；`5.1.3` 分析发布可靠性、`SLO`、可用性与线上失效；`5.1.4` 关注 recoverability、业务连续性和灾难响应软件机制；`5.1.5` 研究功能安全、危害分析、safety case 与 safety assurance |
| `5.2 安全、隐私、公平与合规` | `5.2.1` 研究安全开发流程、漏洞治理、补丁管理；`5.2.2` 研究隐私需求、数据治理与隐私合规；`5.2.3` 关注 `SBOM`、依赖信任、来源证明和供应链安全；`5.2.4` 研究公平性、问责、审计与法规符合 |
| `5.3 性能、资源、能耗与可持续性` | `5.3.1` 做 profiling、benchmark、性能建模与性能诊断；`5.3.2` 做容量规划、资源调度、成本与资源优化；`5.3.3` 研究能耗、碳感知、绿色软件工程；`5.3.4` 研究扩展性、吞吐、时延保证与性能回归控制 |
| `5.4 可用性、可访问性与用户体验` | `5.4.1` 评估开发者向 `API/IDE/tool` 的可用性与开发体验；`5.4.2` 研究终端用户向可访问性、包容式界面与 `UX` 质量；`5.4.3` 做人本评估、交互质量实验与 usability study；`5.4.4` 研究多样性支持、包容性实践与特殊群体开发者支持 |

### 4.6 `6.x` 过程、组织、人员与证据的 `x.x.x` 例子总览

| 二级方向 | `x.x.x` 叶节点与典型例子 |
|---|---|
| `6.1 软件过程与方法学` | `6.1.1` 研究敏捷、精益、DevOps 与持续改进方法；`6.1.2` 做过程挖掘、过程符合性和流程改进；`6.1.3` 关注治理、审计、过程追踪与合规留痕；`6.1.4` 研究社会技术协调、handoff 与 workflow design |
| `6.2 项目管理与工程经济` | `6.2.1` 研究工作量估算、计划编制、排程与进度预测；`6.2.2` 做风险管理、价值驱动工程和需求优先级；`6.2.3` 关注成本模型、`ROI`、生产率与工程经济；`6.2.4` 研究组合治理、资源配置和决策支持分析 |
| `6.3 经验软件工程与证据综合` | `6.3.1` 做控制实验、案例研究、问卷和实地研究；`6.3.2` 做定性编码、混合方法与人类研究；`6.3.3` 进行系统综述、systematic mapping 与 meta-analysis；`6.3.4` 关注 replication、benchmark、artifact package、dataset/corpus 与开放科学；`6.3.5` 关注 roadmap、research agenda、retrospective、position/vision 类领域综合论文 |
| `6.4 挖掘软件仓库与软件分析学` | `6.4.1` 挖掘代码、提交、issue、PR 与 issue-resolution 链；`6.4.2` 研究代码评审、团队协作、CI 日志与社区行为；`6.4.3` 建立 defect prediction、风险模型和软件度量；`6.4.4` 研究生态演化、开源依赖、registry 与包生态分析 |
| `6.5 人因、协作、社区与教育` | `6.5.1` 研究开发者认知、生产力、压力、福祉与神经多样性；`6.5.2` 研究协作、评审、知识共享和沟通机制；`6.5.3` 研究开源社区治理、多样性、社区健康；`6.5.4` 研究软件工程教育、培训、onboarding 与 curriculum |

### 4.7 `7.x` 智能化软件工程与 AI 系统工程的 `x.x.x` 例子总览

| 二级方向 | `x.x.x` 叶节点与典型例子 |
|---|---|
| `7.1 AI for SE` | `7.1.1` 用 `LLM` 做代码生成、补全、翻译与重写；`7.1.2` 用 `AI` 做测试生成、缺陷检测、修复与程序分析；`7.1.3` 用 `AI` 做需求摘要、模型补全、文档生成与 trace 生成；`7.1.4` 用 `AI` 支持架构、设计、计划与工程决策；`7.1.5` 研究人机协同开发、信任校准、copilot workflow 与开发评估 |
| `7.2 SE for AI` | `7.2.1` 研究数据工程、特征/模型管线和模型生命周期；`7.2.2` 研究 `AI` 系统需求、建模、文档与接口契约；`7.2.3` 做 `AI` 测试、鲁棒性验证、漂移监测和安全评测；`7.2.4` 研究 `MLOps`、模型部署、灰度发布、回滚与持续演化；`7.2.5` 研究 `AI` 治理、合规、安全 case 与责任边界 |
| `7.3 智能自治与自适应系统` | `7.3.1` 做反馈回路、`MAPE-K`、适应性规划与自治控制；`7.3.2` 研究 agent workflow、工具编排、agent debugging 与多智能体工程；`7.3.3` 研究自愈、自优化和自治运行；`7.3.4` 研究 adaptive assurance、运行时安全策略和行为约束 |

### 4.8 `8.x` 应用与系统场景的 `x.x.x` 例子总览

| 二级方向 | `x.x.x` 叶节点与典型例子 |
|---|---|
| `8.1 嵌入式、实时、IoT、CPS、机器人` | `8.1.1` 面向工业控制、汽车、航电、医疗软件做建模/验证/测试；`8.1.2` 面向机器人与自主系统做软件架构、任务编排与 assurance；`8.1.3` 面向 IoT、边缘、数字孪生做平台工程与运行治理；`8.1.4` 面向 `ISO 26262`、`DO-178C` 等认证场景做证据工程 |
| `8.2 Web、移动、云、服务与平台生态` | `8.2.1` 研究 Web 与移动应用的设计、演化、测试与质量；`8.2.2` 研究云原生、serverless、平台工程与平台演化；`8.2.3` 研究服务组合、`API` 生态、服务治理与互操作；`8.2.4` 研究大规模分布式应用运行、`SRE` 和平台运维 |
| `8.3 安全关键、工业软件与系统之系统` | `8.3.1` 研究 mission/safety critical 软件的 hazard analysis 与 formal assurance；`8.3.2` 研究企业级、业务关键系统的软件工程方法；`8.3.3` 研究 system-of-systems、互操作与集成 assurance；`8.3.4` 研究受监管行业的软件审计、追责和合规工程 |
| `8.4 社会技术系统与开放生态` | `8.4.1` 研究开源生态、社区演化与公共依赖；`8.4.2` 研究软件供应链、registry、平台治理与生态安全；`8.4.3` 研究低代码、终端用户开发、众包式工程；`8.4.4` 研究软件政策、伦理与生态治理机制 |
| `8.5 新型软件系统` | `8.5.1` 研究 `AI-enabled` 产品与软件系统的工程问题；`8.5.2` 研究 quantum software engineering、量子程序测试和资源推理；`8.5.3` 研究大模型原生与 agentic 软件系统的工程化问题；`8.5.4` 研究 GPU/edge/classical-quantum 等异构平台上的软件工程问题；`8.5.5` 研究 scientific software、HPC、数据密集与实验计算软件的工程问题 |

### 4.9 覆盖复核结论

这里需要明确回答你关心的核心问题：**为什么之前很多二级方向下面都是 4 个叶子，这样到底能不能覆盖全部论文类型？**

结论是：

1. 之前的 `4` 叉结构更多是初版排版上的对称化结果，不应该被视为方法论约束。
2. 对后续论文分类服务而言，**叶子数量必须服从覆盖需求，而不是服从树形美观**。
3. 结合当前 `2025` 语料复核，均匀 `4` 叉会把若干稳定题型硬塞到不自然的位置，因此已经按需要扩成不等叉数。

这次复核主要基于两类证据：

1. **公开学术知识骨架**
   - `SWEBOK`、`ICSE 2025`、`MSR`、`ICST`、`REFSQ`、`MODELS`、`ICSA`、`SEI roadmap` 等来源给出稳定的大方向。
2. **本仓库 `2025` 语料的具体信号**
   - 当前 `6301` 条元数据中，高频主题包括 `建模/模型驱动`、`测试与验证`、`LLM/AI for SE`、`形式化方法`、`可靠性/安全`、`维护与演化`、`需求工程`、`经验软件工程`。
   - 同时还能稳定观察到若干在分类时经常需要单独落点的题型，例如：
     - `technical debt`：至少 `46` 条；
     - `traceability`：至少 `35` 条；
     - `code review`：至少 `63` 条；
     - `architecture decision`：已有显式论文；
     - `flaky tests / test debt`：已有显式论文；
     - `safety case`：已有显式论文；
     - `scientific software / HPC`：已有显式论文；
     - `AI` 辅助架构/设计、`SE for AI` 需求建模、agent 软件工程等也已在 `ICSE/FSE/ASE/ICSME/MSR` 等 venue 中出现。

因此，本次明确补出的稳定叶子包括：

1. `1.1.5` 需求知识复用与需求债务治理
2. `1.3.5` 模型质量、仓库与治理
3. `2.1.5` 架构知识、决策与不确定性管理
4. `3.1.5` 测试质量、脆弱性与测试资产维护
5. `4.1.5` 技术债、克隆与可维护性治理
6. `4.2.5` 文档工程、解释与设计 rationale 恢复
7. `5.1.5` 功能安全、危害分析与 safety assurance
8. `7.1.4-7.1.5` 中把 `AI` 支持的架构/设计与人机协同开发拆开
9. `7.2.2-7.2.5` 中把 `SE for AI` 的需求建模、测试验证、运维演化、治理合规拆开
10. `8.5.5` 科学计算、数据密集与高性能软件工程

后续默认采用下面这条硬规则：

1. 如果出现一批论文长期只能被“勉强塞进”某个叶子，而这个题型本身在问题对象、方法链条和评估证据上都已经稳定成形，就应继续扩出新的 `x.x.x` 叶子。
2. 不需要追求每个二级方向叶子数量相同。
3. 只要一级总类别与单篇软工判定规则不变，`x.x.x` 层允许持续增量细化。

### 4.10 分类树持续维护制度

为了让这棵树真正服务后续扫论文与批量分类，而不是变成僵硬目录，后续默认再执行下面几条制度：

1. 这棵树是**持续演化的工作树**，不是冻结 taxonomy。
2. 扫论文时，只要发现某类软工论文在现有 `x.x.x` 中没有自然落点，或者分类者只能靠“最像哪个旧叶子”来强行解释，就应把它视为扩树信号，而不是视为论文本身“必须服从旧树”。
3. 若一个候选新方向同时满足以下任一条件，就可以扩出新叶子：
   - 在当前批次或相邻批次中反复出现；
   - 在公开综述、社区 scope、CFP、专题 workshop 或多个 venue 中已表现为稳定题型；
   - 若继续沿用旧叶子，会混淆核心研究问题、主贡献对象、方法链条或评估证据。
4. 扩树时，优先在最合适的 `x.x` 下新增 `x.x.x`；如果现有二级方向本身也装不下，再考虑新增新的 `x.x` 分支。
5. 扩树后应同步：
   - 在本文 `4.x` 例子总览中补充新叶子与典型例子；
   - 在 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md) 中写明新规则或新覆盖范围；
   - 若该变化会影响 venue 级先验描述，再同步更新 [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md)。
6. 若树尚未更新完成，临时状态应记为“待扩树/待复核”，而不是先把论文硬塞到一个明显不自然的旧节点。
7. 禁止把“保持对称结构”“保持固定叶子数”或“兼容旧表头”当作拒绝扩树的理由。分类树应服从论文分布与可解释性，而不是反过来让论文迁就旧结构。

## 5. 这棵树如何实际用于论文分类

### 5.1 第 `0` 步：先做一级总判定

后续处理 `CCF` 这一路论文时，默认先做一级总判定：

| 一级总判定 | 何时使用 | 后续动作 |
|---|---|---|
| `软件工程` | 核心研究问题明确落在需求、建模、架构、测试、验证、维护、运维、过程、组织、经验研究、`AI for SE / SE for AI` 等软工活动 | 继续进入本文方向树 |
| `系统软件` | 核心研究问题是 OS、中间件、运行时平台、分布式系统、存储、网络、系统机制与性能 | 不进入本文方向树，单独保留为系统软件 |
| `程序设计语言与形式化基础` | 核心研究问题是语义、类型、编译、逻辑、约束求解、定理证明、纯程序分析 | 不进入本文方向树，单独保留为 `PL/FM` 邻近项 |
| `跨域/待判定` | 同时跨多个方向，或仅凭标题摘要无法稳定判断 | 再按第 `3.7` 节做“跨域但软工主导”判定 |

### 5.2 第 `1` 步：给软件工程论文分配一个 `x.x.x` 主路径

当且仅当论文最终被判为：

1. `属于软件工程`
2. `跨域但软工主导`

才进入 `x.x.x` 主路径分类。

默认规则如下：

1. 每篇软工论文**必须有且仅有一个主路径**。
2. 主路径优先看“它主要改进哪一种软件工程活动”，而不是看方法来源。
3. 路径尽量落到 `x.x.x`，不要只停在 `x.x`。

例如：

1. 用 `LLM` 生成测试用例的论文，主路径通常是 `7.1.2` 或 `3.1.1`，而不是笼统写成 `AI`。
2. 做需求歧义检测的论文，主路径通常是 `1.1.3` 或 `1.2.3`。
3. 做 CI/CD pipeline reengineering 的论文，主路径通常是 `4.3.2` 或 `4.3.3`。
4. 做开发者认知/协作研究的论文，主路径通常是 `6.5.x`。

### 5.3 第 `2` 步：再补辅助路径或辅助标签

主路径之外，允许再补 `1-3` 个辅助路径或辅助标签，用来表达横切维度：

1. 方法标签：`形式化方法`、`程序分析`、`经验研究`、`LLM/AI`。
2. 质量属性标签：`可靠性`、`安全/隐私`、`性能/能耗`、`合规`。
3. 场景标签：`CPS/嵌入式`、`云/服务`、`开源生态`、`移动/Web`、`AI systems`。
4. 运行阶段标签：`设计时`、`测试时`、`运行时`、`演化期`。

### 5.4 场景类节点如何使用

`8.x.x` 节点默认主要承担**场景定位**职责，而不是默认主路径。

例如：

1. 面向自动驾驶做测试生成，主路径通常仍应落在 `3.1.x`，`8.1.x` 作为辅助场景标签。
2. 面向云服务做故障诊断，主路径通常仍应落在 `4.4.2` 或 `5.1.1`，`8.2.x` 作为辅助场景标签。
3. 只有当论文的核心贡献就是“某一类系统的软件工程方法学”时，才考虑让 `8.x.x` 成为主路径。

### 5.5 推荐回填字段

后续在 `metadata` 或年表中，建议至少回填下面这些字段：

1. `macro_area`
   - `软件工程`
   - `系统软件`
   - `程序设计语言与形式化基础`
   - `跨域/待判定`
2. `se_inclusion_decision`
   - `属于软件工程`
   - `跨域但软工主导`
   - `不属于软件工程`
   - `待判定`
3. `cross_domain_flag`
   - `是` / `否`
4. `se_primary_path`
   - 例如：`4.1.2`
5. `se_secondary_paths`
   - 例如：`3.2.1;5.1.1;8.2.2`

## 6. 与当前 `CCF 2025` 索引的覆盖关系

结合 [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md)、[ccf_history/2025/README.md](./ccf_history/2025/README.md) 与现有 `2025` metadata，本文方向树应能覆盖 `CCF 2025` 索引里**属于软件工程的那部分论文类型**：

1. `ICSE / FSE / ASE / TSE / TOSEM`
   - 几乎覆盖 `1.x.x-7.x.x` 的完整软件工程主干。
2. `RE / REFSQ / Requirements Engineering`
   - 主要覆盖 `1.1.x / 1.2.x / 1.4.x`。
3. `MoDELS / SoSyM / CAiSE / WICSA`
   - 主要覆盖 `1.3.x / 2.1.x / 3.3.x / 8.x.x`。
4. `ISSTA / ICST / STVR / ISSRE / QRS / RV / SPIN / FM`
   - 主要覆盖 `3.x.x / 5.x.x`。
5. `ICSME / SANER / ICPC / JSEP / MSR`
   - 主要覆盖 `4.x.x / 6.4.x / 6.5.x`。
6. `ESEM / ESE / EASE`
   - 主要覆盖 `6.3.x / 6.4.x / 6.5.x`。
7. `ICWS / ICSOC / Internetware / TSC / SOCA`
   - 主要覆盖 `2.1.4 / 4.3.x / 4.4.x / 8.2.x`。
8. `PLDI / OOPSLA / FM / VMCAI / SCP / TSC`
   - 只有其中一部分论文会落入本文方向树；是否纳入，必须按第 `3.6-3.7` 节的单篇标准重新判断。

## 7. 过去与近期领域综述/roadmap 对本树的影响

下面这部分是基于 [R8]-[R14] 的综合推断，不是这些来源的原话复述。

### 7.1 从 `FoSE 2000` 到今天：软件工程一直不是单线学科

`FoSE 2000` 的《Software Engineering: A Roadmap》表明，软件工程从来就不是一条单一的“需求 -> 设计 -> 编码 -> 测试 -> 维护”流水线。[R8]  
它更像是：

1. 一组核心工程活动；
2. 一组横切质量属性；
3. 一组组织、方法、证据与社会技术问题。

因此，本文没有采用窄义生命周期树，而是把质量、组织、人因、证据与智能化方向提升为一级分支。

### 7.2 `SWEBOK` 提供的是稳定骨架，但不等于完整前沿视角

`SWEBOK v4.0a` 很适合做稳定骨架，因为它覆盖了需求、设计、架构、构造、测试、运维、维护、配置管理、过程、质量、专业实践与工程经济等知识域。[R1]

但如果只照抄 `SWEBOK`，会压扁以下现代社区已经显式成形的方向：

1. 仓库挖掘与软件分析学。
2. 人因与社会技术系统。
3. `AI for SE / SE for AI`。
4. `AI-enabled systems`、`quantum systems` 等新型软件系统工程问题。

所以本文把 `SWEBOK` 作为骨架，而不是最终目录。

### 7.3 `ICSE 2025` 的 area 设置说明社区已经显式接受新的主枝

`ICSE 2025` 至少做了两件非常关键的事情：[R2]

1. 把 `AI and Software Engineering` 显式拆成 `AI for SE` 与 `SE for AI`。
2. 把 `Architecture and Design` 独立命名，不再只是隐含在传统生命周期叙事里。

这正是本文把 `7.x.x` 和 `2.x.x` 显式提升为独立一级分支的直接原因。

### 7.4 `SEI 2021` 强化了“连续演化、社会技术、AI-enabled、量子”的必要性

`SEI 2021` 的 roadmap 把 `AI-Augmented Software Development`、`Assuring Continuously Evolving Systems`、`Engineering Socio-Technical Systems`、`Engineering AI-enabled Software Systems`、`Engineering Quantum Computing Systems` 都视为未来软件工程必须正视的问题。[R10]

这直接影响了本文的四个设计决定：

1. `4.x.x` 必须显式容纳“持续演化 + 持续 assurance”。
2. `6.x.x` 必须保留社会技术、人因与治理问题。
3. `7.x.x` 不能只是若干零散的 `AI` 标签。
4. `8.5.x` 必须为新型软件系统预留稳定位置。

### 7.5 `Continuous SE`、协作路线图与 `SE for AI` 共同解释了 `4.x.x / 6.x.x / 7.x.x`

这三类来源分别补了三块很重要的空白：

1. `Continuous software engineering: A roadmap and agenda` 说明持续集成、持续交付、部署与运维协同不只是工程实践口号，而是一个稳定研究方向。[R12]
2. `Collaboration in Software Engineering: A Roadmap` 说明协作、共享理解、设计 rationale 与社会技术协调是软件工程内部问题，因此 `6.5.x` 不能被删成“非技术杂项”。[R13]
3. `Software Engineering for AI-Based Systems: A Survey` 说明 `SE for AI` 已经形成围绕数据、质量、测试、部署、维护与治理的工程问题簇，因此 `7.2.x` 需要单独保留。[R14]

## 8. 参考文献

- `[R1]` Hironori Washizaki (ed.). *Guide to the Software Engineering Body of Knowledge (SWEBOK Guide), Version 4.0a*. IEEE Computer Society, 2025. <https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf>
- `[R2]` *ICSE 2025 Research Track*. The 47th International Conference on Software Engineering, research track call and area description. Accessed 2026-04-05. <https://conf.researchr.org/track/icse-2025/icse-2025-research-track>
- `[R3]` *MSR 2025*. Mining Software Repositories 2025 official homepage. Accessed 2026-04-05. <https://2025.msrconf.org/>
- `[R4]` *ICST 2025 Research Papers*. IEEE International Conference on Software Testing, Verification and Validation, call for papers. Accessed 2026-04-05. <https://conf.researchr.org/track/icst-2025/icst-2025-papers>
- `[R5]` *Charter of the International Working Conference on Requirements Engineering: Foundation for Software Quality (REFSQ)*. Version 3.1, updated 2025-04-08. Accessed 2026-04-05. <https://conf.researchr.org/info/refsq-2026/charter>
- `[R6]` *MODELS 2025*. ACM/IEEE International Conference on Model Driven Engineering Languages and Systems official homepage. Accessed 2026-04-05. <https://conf.researchr.org/home/models-2025>
- `[R7]` *ICSA Conference Series*. International Conference on Software Architecture series page. Accessed 2026-04-05. <https://conf.researchr.org/series/icsa>
- `[R8]` Anthony Finkelstein, Jeff Kramer. “Software Engineering: A Roadmap.” In *Proceedings of the Conference on the Future of Software Engineering*, ACM, 2000, pp. 3-24. DOI: <https://doi.org/10.1145/336512.336519>
- `[R9]` Sebastian Nanz (ed.). *The Future of Software Engineering*. Springer, Berlin Heidelberg, 2011. DOI: <https://doi.org/10.1007/978-3-642-15187-3>
- `[R10]` Anita Carleton. “Architecting the Future of Software Engineering: A Research and Development Roadmap.” *Carnegie Mellon University Software Engineering Institute Insights Blog*, 2021-07-12. <https://www.sei.cmu.edu/blog/architecting-the-future-of-software-engineering-a-research-and-development-roadmap/>
- `[R11]` 中国计算机学会. *中国计算机学会推荐国际学术刊物目录：软件工程/系统软件/程序设计语言*. Accessed 2026-04-05. <https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/>
- `[R12]` Brian Fitzgerald, Klaas-Jan Stol. “Continuous software engineering: A roadmap and agenda.” *Journal of Systems and Software*, 123:176-189, 2017. DOI: <https://doi.org/10.1016/j.jss.2015.06.063>
- `[R13]` Jim Whitehead. “Collaboration in Software Engineering: A Roadmap.” In *Future of Software Engineering 2007*, IEEE Computer Society, 2007, pp. 214-225. DOI: <https://doi.org/10.1109/FOSE.2007.4>
- `[R14]` Silverio Martínez-Fernández, Justus Bogner, Xavier Franch, Marc Oriol, Julien Siebert, Adam Trendowicz, Anna Maria Vollmer, Stefan Wagner. “Software Engineering for AI-Based Systems: A Survey.” arXiv:2105.01984, 2021. <https://arxiv.org/abs/2105.01984>
