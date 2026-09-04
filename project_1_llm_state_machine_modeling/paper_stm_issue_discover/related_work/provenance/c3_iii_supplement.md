# 已弃用的第三贡献补充留档

> 本文件属于旧三贡献路线的补充检索材料。它不构成当前 Paper1 的 C3、论文主张或引用闭合。当前来源审计在 [`predicate_provenance.md`](./predicate_provenance.md)。

> ⭐ **这份文件是 C-③ 措辞的最终依据。** ⛔ 它推翻了 [c3_differentiation.md](./c3_differentiation.md) 的原结论，⛔ **也推翻了 C3 覆盖审计给的那个替代写法**（四处错，其中一处严重）。
>
> **规模**：五条线，⭐ 入表 **89 篇**；⭐ 主执行者**亲自回一手来源逐字复核了 16 处承重引文**（⛔ 其中 1 处复核失败并已标明）。
>
> **档位标记**：⭐ 逐字引文与 `read_level` 为【实测】；⭐ 判定为【AI 建议·待确认】。

## ⛔⛔ 结论 1：「唯一空缺是 (iii)」是**被检索强度制造出来的假象**

⭐ **真相相反：(iii) 恰恰是被做得最多、最成熟的一维。**

| 社区 | 成熟度 | ⭐ 锚点是什么 |
| :-- | :-- | :-- |
| **SV-COMP witness 生态** | ⭐ 最成熟 —— 2025 年 **13 个 validator、2180 万次校验**，语法门 + **可反驳的**语义门，计分依赖确认 | 性质公式（LTL）+ 源码坐标，⭐ 输入用 **SHA-256** 钉住 |
| **SAT / SMT 证明** | ⭐ 最成熟 —— **多个独立、形式化验证的检查器**（Coq / ACL2 / CakeML / HOL4）；`cake_lpr` 把可信基收缩到**机器码** | 一个公式的一个全局判定 —— ⛔ 此处 (i)(ii) **不是缺席，是无意义** |
| **硬件 / 概率模型检查证书** | 成熟且在收紧 —— **HWMCC'24 起证书强制**；MDP 证书的检查器经 Isabelle 验证 | ⭐⭐ **状态机元素**：latch（状态变量）· MDP 状态 · μ-演算子公式 |
| **Datalog provenance** | 成熟且**工业规模可负担** —— 约 **1.27×** 开销 | 具名规则 ρ + 基态参数；⛔ **否定性发现无法自动生成记录** |
| **声明式静态分析**（CodeQL / Semgrep） | ⭐ 真正的工业常规 —— **出厂、带版本、可重跑的规则制品** + 快照数据库 | 规则 ID + 源码位置 / 数据流路径（Semgrep 另有 metavariable **绑定环境**） |
| **合规检查**（XCCDF + OVAL） | 成熟且**政府级部署逾十年** | 具名 OVAL 定义 + 配置项 |
| **演绎验证 session**（Why3 / GNATprove） | ⭐ **粒度最细 —— 逐条证明义务** | 目标 / VC + prover 名与版本 |
| **RV 认证式监控**（WhyMon / Explanator2） | 高端成熟 —— ⭐ **verdict 本身就是证明树**，Isabelle 抽取的检查器重判 | 公式 + 轨迹 + 变量赋值 |
| **测试竞赛**（Test-Comp / TestCov） | 成熟 —— ⭐ **生产者的主张从不被接受，只算 validator 的重跑** | 具名 FQL 覆盖准则 + 程序哈希 |
| ⛔ **主流 SAST**（ESLint / SpotBugs / Infer / Coverity / Clang SA） | ⛔ **不成熟** —— 具名规则有，可重算记录没有 | ⚠️ Infer 的语义载荷**全是 `description : string`**；Coverity 第三方"重算"只能是**再买一套工具** |
| ⛔ **传统 GSN / CAE assurance case** | ⛔ **不存在** | ⚠️ SACM 论文逐字：「evidence in assurance cases are described using natural language, and **there is no built-in facility that enables the traceability from evidence to the actual artefact**」 |

⭐⭐ **两条最值得写进论文的观察**：

1. ⭐ **XCCDF 证明瓶颈不在技术** —— ⛔ 严谨可重跑的检查标准早在 **2011** 年就大规模部署了；⭐ 从没建起来的是**那条通往需求的链**。
2. ⭐ **结构化程度与可检查性正交，⛔ 而领域优化了前者** —— ⚠️ Infer 有版本化 ATD schema 却全是字符串；⛔ **SARIF 是业界收敛点，却在规范层面「规定」rule ID 应当 `opaque`**（§3.49.3：`SHOULD be opaque`），⭐ 且全规范 grep `traceab*` 命中 **0** 次。

## ⛔⛔ 结论 2：C3 给的替代写法**也有四处错，其中一处严重**

⚠️ C3 提议的写法是：

> ⭐ (iii) 在形式化验证与静态分析社区已有成熟实现，⛔ 但其锚点是**性质公式与代码位置**，**从不锚回自然语言需求原句**；⭐ (i)+(ii) 在需求追溯与模型一致性社区已有成熟实现，⛔ 但其链接项**不携带任何可独立重算的判据**。

⭐ **形状对，⛔ 四处具体说法错**：

| 半句 | 判定 | ⛔ 错在哪 |
| :-- | :-- | :-- |
| 「(iii) 在**形式化验证**社区已有成熟实现」 | ✅ **成立，且比它暗示的更强** | —— |
| 「在**静态分析**社区已有成熟实现」 | ⚠️ **只对一个子集成立** | ⭐ CodeQL / Semgrep / Soufflé / XCCDF+OVAL 成立（规则是**出厂可执行制品**）；⛔ ESLint / SpotBugs / PMD / Clang SA / Infer / Coverity **不成立**。⛔ 照抄这半句会**把一个分裂的现状说成统一的** |
| 「锚点是**性质公式与代码位置**」 | ⚠️ **少算了一类** | ⛔ 证书世界里 **(ii) 确实做到了**：Certifaiger 锚在 **latch**、MDP 定点证书是**按状态索引的向量**、certifying model checking 的证明原子直接提到状态与子公式、Simulink Model Advisor 的报告项锚在 **`SID` 模型元素**。⛔ **不能说 (iii) 从不锚模型元素** |
| 「**从不**锚回自然语言需求原句」 | ✅ **实质成立，⛔ 但「从不」要软化** | ⭐ 三个反例都**不真正推翻它**，⭐ 而是各自以不同方式说明**为什么做不到**（见下） |
| ⛔⛔ 「(i)+(ii) 社区的链接项**不携带任何可独立重算的判据**」 | ⛔⛔ **这半句现在是错的** | ⭐ **2020 年后的模型化 assurance case 工具恰恰就在做这件事**（见下） |

### ⛔⛔ 那处严重错误：**(i)+(ii) 侧已经有可重算判据了**

| 工作 | ⭐ 它做了什么 |
| :-- | :-- |
| ⭐⭐ **ACCESS**（JSS 2024, arXiv:2403.15236） | ⭐ 把 GSN 的 **Solution 节点挂上一段 EOL 查询**，对 **RoboChart 的具体迁移**逐字段断言（`Transition.all.selectOne(t\|t.name="t4")`，断言 guard 的算子与引用名），⭐ **点按钮即执行、返回布尔**。⭐ 论文自陈动机：「With traditional GSN approaches, references to external models/documents are informal and their evaluation is often **performed manually**」 |
| ⭐ **Wei et al.**（IEEE TCAD 2023） | ⭐ 把受限自然语言编译成**具名 EVL 约束**（`constraint rule_1`）对**状态机**执行 |
| ⭐ **FASTEN.Safe**（SAFECOMP 2020） | ⭐ 自动检查「the consistency of arguments with **system models**」并用外部验证工具兑现安全主张 |
| ⭐ **Isabelle/SACM**（FAC 2021） | ⭐ 整份 assurance case 由 **Isabelle 机器检查** |
| ⭐⭐ **Yan et al.**（arXiv:2602.03550, 2026） | ⭐ 自动生成具名断言 `A_Claim_ID` + 显式参数 + FDR/PRISM/Isabelle 出布尔；⭐ 模型一变即重跑并替换 evidence model |

⛔ **所以论文不能再说「那一侧没有可重算判据」。** ⭐ 准确的说法是：**那一侧已经有了可重算判据，⛔ 只是它的 (i) 端锚的不是原句** —— ⚠️ ACCESS 的 goal 是工程师依危害写的散文、CNL 由安全工程师直接撰写、Yan et al. 锚的是**人工改写后的** Kapture 模板。

## ⭐⭐ 结论 3：最强竞品是 **Yan et al. 2026**，⛔ 且它是**两路交叉确认**的

⭐ **`arXiv:2602.03550`（投 SoSyM 审稿中）**：三要素**全部 partial-to-yes**。

| 要素 | 判定 | 逐字证据 |
| :-- | :-- | :-- |
| **(i)** | `partial` | 「**systematically deriving formal assertions from natural language requirements using templates**」「**Backward traceability** links the requirement to its corresponding claim in the AC」 |
| **(ii)** | `yes` | 绑定 RoboChart 全限定 event / state（如 `sys::ctrl::Movement::flag.out`） |
| **(iii)** | `yes` | 具名断言 + 显式参数（`with constant`）+ FDR / PRISM / Isabelle 出布尔；「The identifier of the assertion, that is, `A_Claim_ID`, **is derived from the claim identifier** in the AC models, providing traceability between the assertion and the evidence」 |

⛔ **它掉出严格门槛只因两点**：① 需求被**人工改写**进 Kapture 模板（逐字自陈：「**Writing a requirement in Kapture is a manual activity.**」）—— ⭐ 锚的是**结构化需求**而非原句；② evidence model **不存**反例 / 见证轨迹 / 工具版本 / 模型哈希 —— ⛔ 第三方「独立重算」**缺料**。

⭐⭐ **值得注意：线 4 的 scout 在完全独立的检索路径上也命中了同一篇**，⭐ 并同样判其为「唯一三项全中者」。⛔ **这不是一路的偏好，是两路的交叉确认。**

## ⭐⭐⭐ 结论 4：跨全部五条线真正不变的那件事 —— ⭐ **建议直接用它作论文的 gap 陈述**

> ⭐ **可独立重算的判据早已成熟，需求追溯也早已成熟；⛔ 两者之间那一跳 —— 从自然语言需求到形式化判据 —— 在每一个社区里都是一次人的行为，且从未被机器检查过。**

⛔ **它有六处各自独立的自证**（⚠️ 全部逐字）：

| 出处 | 逐字自证 |
| :-- | :-- |
| **DO-178C 形式化方法补充**（经 Isabelle/SACM 转引） | 「Formal methods **cannot show** that derived requirements and the reason for their existence are correctly defined; **this should be achieved by review**.」 |
| **Isabelle/SACM** 的工程落法 | ⭐ 把这一跳做成**人写的 `justification element`** —— ⛔ 因为它不可形式化 |
| **Trusta**（SCP 2025） | 「This extraction is **subject to human review and correction**」 |
| **Yan et al.**（2026） | 「**Writing a requirement in Kapture is a manual activity.**」 |
| **Lahiri**（arXiv:2406.09757） | 「there is **no algorithmic way** of ensuring the correctness of the user-intent formalization for programs, expressed as a formal specification. This is because intent or requirement is expressed **informally** in natural language and the specification is a **formal** artefact.」 |
| **s(CASP)**（ICLP 2023 W） | 「Although this step **currently requires manual effort**…」 |

⛔⛔ **这同时定义了一条论文必须正面回答的问题**：⭐ 若把「每条报告项携带 (i)+(ii)+(iii)」作为贡献，**必须回答它凭什么让 NL→判据这一跳可信** —— ⛔ 否则审稿人会拿上面**任意一条**打回来。⚠️ **这不是检索出来的风险，⭐ 是这六处自证共同定义的领域立场。**

### ⭐ 一个方向出乎意料的负例（⛔ 比正例更该写进论文）

⭐ **SPARK / GNATprove**：在**追溯性要求最严苛**的 DO-178C 体制下，⛔ 它**不把 check 追到需求** —— ⭐ 而是**把形式契约直接升格为低层需求**（逐字：「one person can define the architecture and **low-level requirements (package specs)**」）。⛔ **链接的另一端根本不存在**，⭐ 故追溯是**定义性的而非记录性的**。

⚠️ 同理：DO-178C 下静态分析履行的是**编码标准符合性**目标 —— ⛔ 追的是**标准**而不是**需求**。

### ⚠️ 另一条方向性事实

⛔ **SV-COMP witness 1.0 曾是自动机表示，⭐ 2.0 主动放弃了自动机** —— ⚠️ **唯一有过自动机形状报告项的社区正在离开它**。

## ⛔ 结论 5：(i) 端**一个原句级实例都没找到**

⭐ 所有近似命中锚的都是：**编号需求**（Dordowsky 的 ACSL `behavior` 子句 · Isabelle/SACM 的 SFR1）· **标准条款**（OSCAL · MISRA · XCCDF）· **人工改写的结构化句**（FRETish · Kapture · CNL · Gherkin）。

⭐ **三个最接近的，各自以不同方式说明为什么做不到**：

| 工作 | ⭐ 它做到了什么 | ⛔ 为什么不算 |
| :-- | :-- | :-- |
| **Dordowsky**（F-IDE 2015） | 用**具名 ACSL `behavior` 子句**挂 DO-178C 低层需求 —— 逐字：「The behavior clause **can be named** as shown in the example which **facilitates traceability to higher level requirements**」 | ⛔ 那是**人维护的命名约定**，⛔ 不是任何格式里的字段；⛔ 指向**编号需求**而非某一句；⛔ 来自航电承包商而非该社区 |
| ⭐⭐ **Kern et al.**（COMPSAC 2019） | ⭐ **画出了完整的链**：UNECE 法规原句「The light shall be a flashing light flashing 90 ±30 times per minute」→ **Stateflow chart** → C 代码 → `static_assert` → 报告，用 OSLC/RDF 连接 | ⛔⛔ **结论自承**：「**Up to now, our implementation create linkages between code and static analysis results.**」—— ⭐ **提出了，没做成**，⛔ 且七年无后续实现。⚠️ 报告项锚在 C 行号，**从不锚 Stateflow 状态** |
| **OSCAL** Assessment Results | ⭐ 把真值绑到 **`statement-id`**（**句内指针** —— ⭐ 本调研见到的最佳 (i)） | ⛔ 回一手 metaschema 核实：`finding-target` 是「an **assessor's conclusions**」—— ⭐ **报告模型而非检查模型**；⛔ 且 control 由标准撰写，**永非项目自撰** |

## ⭐ 结论 6：本调研发现一个**空的方法论位置**

⛔ **未找到任何把「报告项的形态（report item schema）」本身当作一等研究对象的工作。** ⭐ 各社区都在造自己的记录格式（witness YAML · SARIF · OSCAL AR · `why3session.xml` · evidence model），⛔ 但**没有人做过跨社区的报告项形态比较**。

⭐ **若本论文想要一个方法论层面的次级贡献，这里是空的。**

## ⛔ 十条缺口（⭐ 逐条如实登记）

| # | 缺口 | 严重度 |
| --: | :-- | :-- |
| 1 | **JavaMOP / tracematches / LARVA 整簇缺席** —— 未取到可引正文 | ⚠️ 真实的洞 |
| 2 | ⭐ **Dawes & Reger, RV 2019**（`10.1007/978-3-030-32079-9_12`）—— ⭐ 据称能重建执行路径并定位**轨迹中第一条违例观察**，若属实是**见证子轨迹的命中**；⛔ 非 OA、唯一免费 PDF 是讲稿幻灯片 | ⛔ **最值得补的一条** |
| 3 | Aerial（TACAS 2017）· CRV 2015/2016 · Copilot 主论文 · CopilotVerifier（`arXiv:2607.01363`，已发现未读） | ⚠️ |
| 4 | **KeY 与 Isabelle proof terms** 被主动放弃（成本过高）—— ⛔ 故「演绎验证的证明对象能否作逐条报告记录」只由 Why3 / Frama-C / GNATprove 三家回答 | ⚠️ |
| 5 | ⛔ **Coverity 官方 checker reference 无法访问**（登录门）—— ⭐ 商业 SAST 的不可重算性只能**按闭源推定**，未获一手确证 | ⚠️ |
| 6 | ⛔ **ACM Artifact Badging 的逐字引文复核失败**（官网返回 754 字符 JS 壳）—— ⭐ 结论方向有其余证据支持，⛔ 但该引文**不可用** | ⭐ 已标注 |
| 7 | ⛔ **未做按年份的 venue 全扫** —— SAFECOMP / ISSC / SCSC / AAA 的历年目录没有逐年过一遍。⚠️ 安全论证社区二十年的会议论文里，⭐ 很可能还有把 evidence node 做成可重算判据的**早期工作**没被词簇捞到 | ⛔ 必补 |
| 8 | ⭐ **报告项形态本身是空的方法论位置**（见结论 6） | ⭐ 机会而非缺口 |
| 9 | ⛔ **未验证 Simulink Model Advisor 能否锚到 Stateflow 的 state / transition** —— ⭐ 只证到 block 与 signal。⚠️ 这条**直接关系到「状态机锚定报告项是否已有商业先例」** | ⛔ 必补 |
| 10 | ⛔⛔ **(i) 端一个原句级实例都没找到**（见结论 5） | ⭐ 这**本身就是结论**，⛔ 不是缺口 |

## 更新日志

| 时间 | 内容 |
| :-- | :-- |
| 2026-08-12 | 建立。五条线 89 篇入表，16 处承重引文经一手复核（1 处失败已标）。⛔ 推翻「唯一空缺是 (iii)」与 C3 给的替代写法（四处错，一处严重）；⭐ 给出跨五线不变的 gap 陈述与其六处独立自证。 |
