# 软件工程学术领域方向树（2025 基线版）

## 1. 文档定位

本文档是 `frontier_index/` 当前使用的软件工程领域分类基线。

它的用途不是做“2025 趋势报告”，而是为以下工作提供一套稳定、可执行、可维护的共同口径：

1. 判断一篇论文是否属于软件工程研究。
2. 为 `CCF` 年度索引与后续 `arXiv` 索引打方向标签。
3. 区分“软件工程论文”和“邻近但不属于软件工程主问题”的 `PL / systems / formal methods` 论文。
4. 为后续 `PDF` 获取、深读和正式文库迁移提供一致的前置分类。

因此，本文档是一份**工作型 taxonomy**，不是一个宣称“唯一正确”的学科本体。它首先服务于本仓库当前的前沿索引任务，尤其服务于 [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md)、[ccf_history/README.md](./ccf_history/README.md) 与 [ccf_history/2025/README.md](./ccf_history/2025/README.md) 这套索引体系。

## 2. 构建依据

这棵树不是凭直觉拍出来的，而是综合以下几类依据形成的：

1. **稳定知识骨架**
   - `SWEBOK v4.0a` 给出了 `18` 个知识域，其中第 `1-15` 章被视为软件工程知识域，第 `16-18` 章为基础知识域；它同时明确指出软件工程与计算机科学相关但不同，不应混为一谈。[R1]
2. **当前主流社区的问题划分**
   - `ICSE 2025 Research Track` 把研究范围明确整理为 `9` 个 area，包括 `AI for Software Engineering`、`Analytics`、`Architecture and Design`、`Dependability and Security`、`Evolution`、`Human and Social Aspects`、`Requirements and Modeling`、`Software Engineering for AI`、`Testing and Analysis`。[R2]
3. **稳定专门社区对关键子方向的强化**
   - `MSR` 强化了“挖掘软件仓库 / 软件分析学 / 数据驱动软件工程”的独立地位。[R3]
   - `ICST` 强化了“测试、验证、静态/动态分析、调试、修复、可靠性”的完整保证链条。[R4]
   - `REFSQ` 说明需求工程并不是 broad venue 下的一个零散主题，而是长期稳定、独立存在的核心分支。[R5]
   - `MODELS` 说明建模与模型驱动软件/系统工程具有持续稳定的独立社区。[R6]
   - `ICSA` 说明软件架构并不是“设计”中的一个小话题，而是成熟且独立的核心方向。[R7]
4. **过去与近期的大领域级路线图**
   - `FoSE 2000` 的《Software Engineering: A Roadmap》把软件工程明确理解为一个由多个研究专门化方向共同组成的学科整体，而不是单一技术线。[R8]
   - `The Future of Software Engineering`（2011）反映了软件工程已经从传统生命周期叙事扩展到架构、建模、验证、人因、工程化实践等多条成熟主线。[R9]
   - `SEI` 的 `2021` roadmap 进一步把 `AI-augmented software development`、`continuously evolving systems`、`socio-technical systems`、`AI-enabled systems` 与 `quantum systems` 提升为未来软件工程必须正视的方向。[R10]
5. **本仓库当前语料的现实覆盖检查**
   - 当前 [SUMMARY.md](./SUMMARY.md) 记录了 `2025` 年 `CCF` 索引的 `6301` 条论文元数据。
   - 从这些 venue 的类型分布和现有方向标签可以看出，若分类树缺少“需求/建模”“测试/验证/分析”“维护/演化”“经验/仓库挖掘”“AI for SE / SE for AI”“架构”“运行与持续工程”“质量属性与可信赖性”等主枝，就无法稳定覆盖当前已收录的软工论文类型。

## 3. 边界说明

### 3.1 什么算软件工程

在本仓库里，一篇论文应优先被视为软件工程论文，当且仅当它的**核心研究问题**明显落在以下问题之一：

1. 如何表达、获取、分析、管理和追踪软件需求。
2. 如何对软件或软件密集型系统进行建模、规格化、设计、架构化与构造。
3. 如何测试、分析、验证、监测、调试、修复和保证软件质量。
4. 如何维护、演化、部署、发布、运行和持续改进软件。
5. 如何以经验研究、度量、仓库挖掘、过程方法、人因与组织研究来理解和改进软件开发活动。
6. 如何工程化地开发 `AI` 支持的软件开发工具，或工程化地开发、验证、部署与治理带 `AI` 组件的软件系统。

对**跨域论文**，这里采用“**软工主导就算软工**”的口径，而不是要求它必须是“纯软件工程”：

1. 只要论文的核心研究问题是软件工程问题，就应纳入软件工程。
2. 即使方法吸收了 `PL / FM / systems / AI` 技术，只要主要方法链条是在改进需求、建模、架构、测试、验证、维护、运维、过程或工程治理，就应纳入软件工程。
3. 如果主要评估证据也是软件工程证据，例如缺陷发现能力、测试效果、开发效率、维护性、可追踪性、可靠性改进、工程成本或开发者行为改进，也应优先按软件工程处理。

### 3.2 什么只是邻近学科

并不是 `CCF` 软件工程/系统软件/程序设计语言方向中的所有论文都属于软件工程。

以下类型通常**不应**仅因 venue 落在 `CCF` 列表中就被强行归入软件工程：

1. 纯编译优化、纯语言语义、纯类型理论、纯程序逻辑，而没有新的软件工程问题、工程流程或工程评价。
2. 纯系统机制、纯操作系统/网络/存储/体系结构实现，而没有软件工程上的构造、演化、测试、运维、质量或组织问题。
3. 纯硬件验证、纯电路验证、纯控制理论或纯数学理论工作。
4. 只是在软件工程序列会议发表，但论文并未从软件工程视角提出新 insight 的工作。

`ICSE 2025` 在 scope 中明确提醒：作者应判断论文是否为软件工程带来新的 insight；例如一个只聚焦硬件验证的形式化方法论文，就可能不在 `ICSE` 的软件工程范围内。[R2]  
这条判断对本仓库同样适用。

### 3.3 形式化方法、程序分析、PL、systems 在这里怎么处理

这里需要明确一个非常关键的口径：

1. **形式化方法不是自动等于软件工程**。
2. **程序分析不是自动等于软件工程**。
3. **PL / systems venue 不是自动等于软件工程**。

是否纳入本文方向树，取决于该论文是否在解决一个**软件工程问题**，例如：

1. 需求规格化与一致性分析。
2. 架构或设计分析。
3. 测试、验证、运行时监测、缺陷定位、程序修复。
4. 维护、演化、理解、配置、发布、运维。
5. 软件开发流程、团队协作、工程治理、经验评估。

换言之，**方法来源**可以是形式化方法、程序分析、机器学习、统计学或系统技术；但**分类主标签**优先看研究问题属于哪类软件工程活动。  
若论文是跨域的，但其核心研究问题和主要方法链条都明显是软件工程导向，则仍应算入软件工程，只是在次标签或备注中保留 `跨域` 标记。

### 3.4 与 `CCF` 大类页的关系

截至 **2026-04-05**，`CCF` 对应的官方页面标题是“**软件工程/系统软件/程序设计语言**”，而“**数据库/数据挖掘/内容检索**”是单独的另一页，不在本路径当前这个三分法之内。[R11]

这意味着后续面对本路径中的论文时，第一层总判定应优先落到下面四类之一：

1. `软件工程`
2. `系统软件`
3. `程序设计语言与形式化基础`
4. `跨域/待判定`

只有当总判定是 `软件工程` 时，才进入本文后续的软工方向树。  
如果总判定落在 `系统软件` 或 `程序设计语言与形式化基础`，应当**如实保留**这一判定，而不是强行塞进软工树。  
如果论文是跨域的，则需要再做一次“是否软工主导”的单独处理。

## 4. 软件工程学术方向 ASCII 树

下面给出当前推荐使用的方向树。

```text
Software Engineering
|-- 1. 需求、规格与建模
|   |-- 1.1 需求工程
|   |   |-- 需求获取、分析、协商、优先级
|   |   |-- 功能/非功能需求
|   |   |-- 需求管理、变更管理、反馈闭环
|   |   `-- 需求追踪、需求依赖、需求与架构对齐
|   |-- 1.2 规格说明与形式化
|   |   |-- 自然语言到形式化规格
|   |   |-- 约束、契约、属性、规约语言
|   |   `-- 规格一致性、完备性、可分析性
|   |-- 1.3 建模与模型驱动工程
|   |   |-- UML/SysML/状态机/时序模型
|   |   |-- MDE/MDD/数字孪生/领域建模
|   |   |-- 建模语言、建模工具、模型转换
|   |   `-- 模型驱动分析、生成与监测
|   `-- 1.4 变体管理与产品线
|       |-- 变体建模
|       `-- 软件产品线与可配置系统
|-- 2. 架构、设计与构造
|   |-- 2.1 软件架构
|   |   |-- 架构风格、微服务、SOA、云原生架构
|   |   |-- 架构恢复、架构重构、架构知识管理
|   |   `-- 组件化、可复用性、依赖结构
|   |-- 2.2 软件设计
|   |   |-- 设计原则、模式/反模式
|   |   |-- 模块化、复杂度、技术债
|   |   `-- API 设计与接口演化
|   `-- 2.3 软件构造
|       |-- 实现技术与开发环境
|       |-- 代码生成、脚手架、构造工具
|       `-- 复用、组件集成、构造自动化
|-- 3. 测试、分析、验证与修复
|   |-- 3.1 软件测试
|   |   |-- 测试设计、覆盖准则、测试生成
|   |   |-- 模糊测试、搜索式测试、符号执行
|   |   `-- GUI/移动/Web/嵌入式/AI 系统测试
|   |-- 3.2 程序分析
|   |   |-- 静态分析、动态分析、混合分析
|   |   |-- 污点分析、数据流/控制流分析
|   |   `-- 约束求解、程序综合（面向工程问题）
|   |-- 3.3 验证与确认
|   |   |-- 形式化验证、模型检查、定理证明
|   |   |-- 运行时验证、运行时监测
|   |   `-- V&V、确认、基准与可复现验证
|   `-- 3.4 调试、定位与修复
|       |-- 调试与故障定位
|       |-- 自动程序修复/补丁生成
|       `-- 错误恢复与自愈
|-- 4. 演化、交付与运行
|   |-- 4.1 维护与演化
|   |   |-- 缺陷修复、重构、回归影响
|   |   |-- API/依赖/库演化
|   |   `-- 遗留系统现代化
|   |-- 4.2 程序理解与逆向工程
|   |   |-- 代码理解、文档理解、痕迹恢复
|   |   `-- 逆向工程、程序理解支持工具
|   |-- 4.3 发布、配置与持续工程
|   |   |-- 配置管理、构建、打包、版本管理
|   |   |-- CI/CD、发布工程、DevOps、AIOps
|   |   `-- 依赖治理、供应链与软件生态
|   `-- 4.4 运维与运行
|       |-- 可观测性、日志、故障诊断
|       |-- 运行时配置、弹性伸缩、服务运维
|       `-- 事件响应、可靠运行、持续 reassurance
|-- 5. 质量属性与可信赖性
|   |-- 5.1 可靠性、可用性、安全性与韧性
|   |-- 5.2 安全、隐私、公平性与合规
|   |-- 5.3 性能、资源、能耗与可持续性
|   `-- 5.4 可用性、可访问性与用户体验
|-- 6. 过程、组织、人员与证据
|   |-- 6.1 软件过程与方法学
|   |   |-- 生命周期、敏捷、精益、持续交付
|   |   `-- 过程改进、方法组合、工程治理
|   |-- 6.2 项目管理与工程经济
|   |   |-- 成本、风险、估算、价值、优先级
|   |   `-- 治理、合规、策略与决策
|   |-- 6.3 经验软件工程与证据综合
|   |   |-- 实验、案例研究、调查、混合方法
|   |   |-- replication、benchmark、meta-analysis
|   |   `-- 证据等级、可复现性、工具评估
|   |-- 6.4 挖掘软件仓库与软件分析学
|   |   |-- 仓库挖掘、软件度量、可视化
|   |   |-- 开源生态、代码评审、CI 数据、遥测
|   |   `-- 数据驱动决策与预测软件工程
|   `-- 6.5 人因、协作、社区与教育
|       |-- 开发者生产力、认知、压力与体验
|       |-- 团队协作、全球软件开发、开源社区
|       `-- 软件工程教育与职业实践
|-- 7. 智能化软件工程与 AI 系统工程
|   |-- 7.1 AI for SE
|   |   |-- 代码生成、测试生成、缺陷检测、修复
|   |   |-- LLM/基础模型支持的软件开发
|   |   `-- 人机协同开发、prompt engineering for SE
|   |-- 7.2 SE for AI
|   |   |-- AI 模型/数据/管线工程
|   |   |-- AI 系统的需求、架构、测试、验证、部署
|   |   `-- AI 系统的质量、治理、监控与维护
|   `-- 7.3 智能自治与自适应系统
|       |-- 自愈系统、自治系统
|       `-- agentic software engineering
`-- 8. 应用与系统场景
    |-- 8.1 嵌入式、实时、IoT、CPS、机器人
    |-- 8.2 Web、移动、云、服务与平台生态
    |-- 8.3 安全关键、工业软件、系统之系统
    |-- 8.4 社会技术系统与大规模开放生态
    `-- 8.5 新型软件系统
        |-- AI-enabled systems
        `-- quantum software engineering
```

## 5. 后续分类流程

### 5.1 第 `0` 步：先做一级总判定

后续处理 `CCF` 这一路论文时，默认先做一级总判定：

| 一级总判定 | 何时使用 | 后续动作 |
|---|---|---|
| `软件工程` | 论文核心问题落在需求、建模、架构、测试、验证、维护、运维、过程、经验研究、`AI for SE / SE for AI` 等软工活动 | 继续进入本文方向树 |
| `系统软件` | 核心问题是操作系统、中间件、服务基础设施、系统机制与系统实现 | 不进入本文方向树，单独保留为系统软件 |
| `程序设计语言与形式化基础` | 核心问题是语言设计、语义、类型、编译、逻辑、证明、约束求解等 | 不进入本文方向树，单独保留为 `PL/FM` 邻近项 |
| `跨域/待判定` | 同时跨多个方向，或仅凭标题摘要无法稳定判断 | 单独处理：若软工主导，则转入 `软件工程` 并加 `跨域` 次标签；若非软工主导，则保留为非软工或继续待判 |

只有一级总判定为 `软件工程` 时，才继续走下面的主标签/次标签流程。  
但对 `跨域/待判定` 条目，默认还要再问三个问题：

1. 核心研究问题是否是软件工程问题？
2. 主要方法链条是否主要作用于软件工程活动或软件工程工件？
3. 主要评估证据是否是在评估软件工程效果？

如果这三个问题中的前两个至少有一个明确为“是”，且第三个问题没有明显相反证据，通常就应按**跨域但软工主导**处理：  
把一级总判定落到 `软件工程`，同时在 `软工次标签` 或 `备注` 中保留 `跨域` 标记。

### 5.2 第 `1` 步：主标签优先看“研究问题”，不是看 venue

后续给论文打标签时，默认流程是：

1. 先判断它是否属于软件工程。
2. 再从上面的 `8` 个主枝中给它分配**一个主标签**。
3. 然后再补 `1-3` 个次标签。

例如：

1. 一篇“用 `LLM` 生成测试用例”的论文，主标签通常应落在 `7.1 AI for SE`，次标签可补 `3.1 软件测试`。
2. 一篇“自动驾驶系统中的感知模型测试与验证”论文，主标签通常应落在 `7.2 SE for AI` 或 `3.3 验证与确认`，次标签再补 `8.1 CPS/机器人/自动驾驶`。
3. 一篇“从 issue / PR / commit 中挖掘维护模式”的论文，主标签通常应落在 `6.4 挖掘软件仓库与软件分析学`，而不是简单标成“维护”。

### 5.3 第 `2` 步：次标签用于表达横切维度

推荐的次标签一般来自以下横切维度：

1. 方法：`形式化方法`、`程序分析`、`经验研究`、`机器学习/LLM`。
2. 质量属性：`可靠性`、`安全/隐私`、`性能/能耗`、`可持续性`。
3. 场景：`CPS/嵌入式`、`云/服务`、`开源生态`、`移动/Web`、`量子`。
4. 运行阶段：`设计时`、`测试时`、`运行时`、`演化期`。

### 5.4 默认不要把“应用场景”当主标签

`第 8 枝` 主要承担“场景标签”的职责。除非论文的核心问题就是“如何工程化某类系统”，否则它通常不应压过主活动标签。

例如：

1. “面向 `CPS` 的需求可追踪性方法”  
   主标签应是 `1.1 需求工程`，而不是 `8.1 CPS`。
2. “云服务系统的故障诊断与恢复”  
   主标签通常应是 `4.4 运维与运行` 或 `5.1 可靠性/韧性`，`8.2 云/服务` 作为场景次标签。

## 6. 主枝与经典知识域/现代社区口径的对应关系

| 本文主枝 | 主要吸收的稳定知识域 | 主要吸收的现代社区口径 |
|---|---|---|
| `1. 需求、规格与建模` | `SWEBOK` 的 `Requirements`、`Models and Methods` | `ICSE` 的 `Requirements and Modeling`，以及 `REFSQ`、`MODELS` |
| `2. 架构、设计与构造` | `Architecture`、`Design`、`Construction` | `ICSE` 的 `Architecture and Design`，以及 `ICSA` |
| `3. 测试、分析、验证与修复` | `Testing`、部分 `Quality/Security` | `ICSE` 的 `Testing and Analysis`、`Dependability and Security`，以及 `ICST` |
| `4. 演化、交付与运行` | `Maintenance`、`Configuration Management`、`Operations` | `ICSE` 的 `Evolution`，以及持续工程/DevOps 社区 |
| `5. 质量属性与可信赖性` | `Quality`、`Security` | `ICSE` 的 `Dependability and Security`，以及可靠性/安全/性能相关 venue |
| `6. 过程、组织、人员与证据` | `Process`、`Management`、`Economics`、`Professional Practice` | `ICSE` 的 `Human and Social Aspects`、`Analytics`，以及 `MSR/ESEM/EASE` |
| `7. 智能化软件工程与 AI 系统工程` | `SWEBOK` 中没有以同等显式方式独立成枝，但可从多个知识域吸收 | `ICSE 2025` 明确拆分出 `AI for SE` 与 `SE for AI` |
| `8. 应用与系统场景` | `SWEBOK` 说明不同系统类型会影响采用何种实践 | `SEI 2021` 明确强调 `AI-enabled systems`、`socio-technical systems`、`quantum systems` |

这个映射表说明：本文方向树**不是对 `SWEBOK` 的机械改写**，也**不是对 `ICSE 2025` 的机械抄录**。它是把“稳定骨架”和“现代社区显式关切”合并后的工作树。

## 7. 与当前 `CCF 2025` 索引的覆盖关系

结合 [CCF_SE_A_B_C.md](./CCF_SE_A_B_C.md)、[ccf_history/2025/README.md](./ccf_history/2025/README.md) 与 [SUMMARY.md](./SUMMARY.md)，当前这棵树应能覆盖 `CCF 2025` 索引里**属于软件工程的那部分论文类型**：

1. `ICSE / FSE / ASE / TSE / TOSEM`
   - 覆盖面最广，几乎横跨 `1-7` 全部主枝。
2. `RE / REFSQ`
   - 主要落在 `1.1 需求工程`，并与 `1.2 规格说明`、`1.4 追踪/依赖` 强相关。
3. `MODELS / CAiSE / SoSyM`
   - 主要落在 `1.3 建模与模型驱动工程`，并延伸到 `2. 架构与设计`。
4. `ISSTA / ICST / STVR / QRS / RV / FM / TASE`
   - 主要落在 `3. 测试、分析、验证与修复` 与 `5. 质量属性与可信赖性`。
5. `ICSME / SANER / ICPC / JSS / JSEP`
   - 主要落在 `4. 演化、交付与运行` 与 `6. 经验/组织/证据`。
6. `MSR / ESEM / EASE / PACMSE`
   - 主要落在 `6.4 挖掘软件仓库与软件分析学`、`6.3 经验软件工程与证据综合`。
7. `ICSA / WICSA / TSC / ICSOC / ICWS / Internetware`
   - 主要落在 `2. 架构、设计与构造`、`4. 运行与持续工程` 与 `8. 系统场景`。
8. `PLDI / POPL / OOPSLA / TOPLAS / PACMPL / SOSP / OSDI`
   - **只有其中一部分论文**会进入本文方向树；是否进入，取决于该论文是否把核心贡献落在需求、建模、架构、测试、验证、维护、过程、运维、经验研究、AI 工程化等软件工程问题上。

这也正是本文必须存在的原因：  
如果没有一棵显式的领域树，后续 AI 很容易把“落在 `CCF` 这个大类里”误当成“就是软件工程论文”。

## 8. 过去与近期领域综述/roadmap 对本树的影响

下面这部分是基于 [R8]-[R10] 的**综合推断**，不是这些来源的原话复述。

### 8.1 从 `FoSE 2000` 到今天：软件工程一直不是单线学科

`FoSE 2000` 的《Software Engineering: A Roadmap》把软件工程理解为一个由多条研究专门化方向构成的整体。[R8]  
这说明软件工程从一开始就不适合被压缩成单一“开发生命周期流程图”，而应该被看作：

1. 一组核心工程活动；
2. 一组横切质量属性；
3. 一组组织、方法、证据和社会技术议题。

因此，本文没有只做一棵“需求→设计→编码→测试→维护”的窄树，而是保留了质量、过程、人因、证据与智能化等横切主枝。

### 8.2 `SWEBOK` 提供的是稳定骨架，但不等于完整前沿视角

`SWEBOK v4.0a` 很适合提供稳定骨架，因为它覆盖了 `Requirements`、`Architecture`、`Design`、`Construction`、`Testing`、`Operations`、`Maintenance`、`Configuration Management`、`Management`、`Process`、`Models and Methods`、`Quality`、`Security`、`Professional Practice`、`Economics` 等知识域。[R1]

但如果只照抄 `SWEBOK`，会有两个问题：

1. `Analytics`、`MSR`、`Human and Social Aspects`、`AI for SE / SE for AI` 这些现代社区已经高度显式化的方向会被压扁。
2. 对 `AI-enabled systems`、`quantum systems`、大规模开放生态与社会技术系统的工程问题，表达力不足。

所以本文把 `SWEBOK` 作为主干，而不是作为最终目录。

### 8.3 `ICSE 2025` 的 area 设置说明社区已经显式接受新的主枝

`ICSE 2025` 今年明确做了两件很关键的事：[R2]

1. 把 `AI and Software Engineering` 拆成 `AI for SE` 与 `SE for AI`。
2. 新增并显式命名 `Architecture and Design`。

这说明当前主流软件工程社区已经不再满足于把这些方向塞在传统生命周期角落里。  
因此，本文把 `7. 智能化软件工程与 AI 系统工程` 设为一级主枝，而不是只把它当成若干零散关键词。

### 8.4 `SEI 2021` 说明“连续演化、社会技术、AI-enabled、量子”必须在树上有位置

`SEI 2021` 的 roadmap 关注 `AI-Augmented Software Development`、`Assuring Continuously Evolving Systems`、`Engineering Socio-Technical Systems`、`Engineering AI-enabled Software Systems`、`Engineering Quantum Computing Systems` 等方向。[R10]

这对本文方向树的直接影响是：

1. `4. 演化、交付与运行` 里必须显式容纳“持续演化 + 持续 reassurance”。
2. `6. 过程、组织、人员与证据` 里必须保留社会技术与人因主枝。
3. `7. 智能化软件工程与 AI 系统工程` 与 `8. 新型软件系统场景` 必须提升到一级节点。

## 9. 后续分类建议

后续在 `frontier_index/` 下做方向归类时，建议统一遵守以下规则：

1. **先判定一级总类别，再决定是否进入软工树。**
2. **每篇软件工程论文必须有且仅有一个主标签。**
3. **每篇软件工程论文可再补 `1-3` 个次标签。**
4. **跨域项需要单独处理；若软工主导，则按软件工程纳入，同时保留 `跨域` 标记。**
5. **主标签优先看研究问题，次标签再表达方法、质量属性与场景。**
6. **不要因为论文来自 `PL / systems / FM` venue 就自动判入软件工程。**
7. **不要因为论文来自 `ICSE / FSE / ASE` 等 broad venue 就自动认为与博士主线相关。**
8. **若主标签难以判断，优先问：这篇论文到底在改进哪一种软件工程活动，或在保证哪一种软件质量属性？**

## 10. 参考文献

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
