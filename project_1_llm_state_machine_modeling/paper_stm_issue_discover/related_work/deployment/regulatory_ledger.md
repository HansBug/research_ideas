# 法规与标准台账（N1a · 法规标准族）

> ⭐ 本文件回答两个问题：**Q1** 功能安全标准里到底有没有约束「把需求文档 / 设计模型交给外部第三方处理」的条款；**Q2** 若没有，真正可引的成文依据在哪一族。⛔ 本文件只放证据与逐条判定，⛔ 结论汇总回 [SUMMARY.md](./SUMMARY.md)。

**核验状态口径**：`🟢 官方全文已核验`（引文来自官方或授权发行方的公开正文 / 免费 preview 正文范围内）/ `🟡 二手佐证`（注明出处）/ `🔴 付费墙未核验`（条款存在但正文不在免费范围）/ `⚪ 查无此条`。

⚠️ **关于 ISO / IEC preview 的证据等级说明**：ISO 与 IEC 通过授权发行方（iTeh Standards / SIST）发布**免费 preview PDF**，其中包含**完整目录、完整 Scope、以及正文前若干页的规范性条文**，页面带 `iTeh STANDARD PREVIEW` 水印且标注 ISO/IEC 版权。⭐ 本台账中凡标 🟢 的 ISO / IEC 引文，**均逐字取自这些 preview PDF 的正文范围**，并附 preview URL；⛔ 凡条文落在 preview 范围之外的（如 ISO 26262-8 的 5.4.3、Clause 11 正文），一律标 🔴，⛔ **不据记忆补写**。

---

## 0. 一句话结论

⛔ **Q1 = 无。** 在本轮覆盖的六本功能安全标准中，**没有任何一条条款约束「把需求文档 / 设计模型 / 工作产品交给外部第三方处理」**；⭐ 其中 **IEC 61508-1:2010 §1.2 m) 用逐字条文把「安全策略与安全服务」明确排除出自身范围**，⭐ **ISO/SAE 21434:2021 §1 Scope 用逐字条文声明「本文件不规定与网络安全相关的具体技术或解决方案」**——⭐ 这两条把 Q1 的否定结论从「查不到」升级为「标准自己说了不管」。⚠️ **ISO 26262 Part 8 的 DIA 机制确实是「责任划分」而非「数据驻留」**，⭐ 先验判断被逐字条文证实；⛔ 且 §5.1 c) 的目标恰恰是「identify the **work products to be exchanged**」——⛔ **它是共享制品的授权机制，不是禁止外发的依据**，⛔ 反向引用会被审稿人一击打穿。

⭐ **Q2 = 有，但都带前置认定，且没有一条直接推出「必须私域部署」。** ⭐ 最强的一条落在**中国保密法族**与**美国国防供应链族**（详见 §2，以各分组 agent 回报为准）；⛔ 但**三层论证强度必须分清**：(a)「不能用境外 LLM API」**可立**；(b)「不能用任何第三方公有云 LLM」**需前置认定**；(c)「必须私域部署」⛔ **无法由任何成文依据直接推出**——⛔ 因为主流厂商已提供 ZDR / 区域驻留 / 政府云授权（见 §3.4），⛔ 它们在合规层面填掉了 (c) 的必要性。

⭐ **档位建议：B。** ⛔ 不是 A（Q1 全空，Q2 无一条覆盖「设计阶段制品交给第三方处理」这个动作本身），⛔ 也不是 C（依据确实存在，只是落在非功能安全族且带前置条件）。

---

## 1. Q1 · 功能安全标准（逐本）

### 1.1 总览表

| 标准 | 版本 | clause | 逐字原文（关键句） | 是否覆盖「制品外发」 | 来源 | 核验状态 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| IEC 61508-1 | Ed. 2.0, 2010-04 | §1.2 m) | "does not specify the requirements for the development, implementation, maintenance and/or operation of security policies or security services needed to meet a security policy that may be required by the E/E/PE safety-related system" | ⛔ **不覆盖（标准自陈排除）** | [preview PDF](https://cdn.standards.iteh.ai/samples/14795/b305f26083da4dcb915a95166796f773/IEC-61508-1-2010.pdf) | 🟢 |
| IEC 61508-1 | Ed. 2.0, 2010-04 | §1.2 l) | "does not cover the precautions that may be necessary to prevent unauthorized persons damaging, and/or otherwise adversely affecting, the functional safety of E/E/PE safety-related systems" | ⛔ 不覆盖 | 同上 | 🟢 |
| IEC 61508-1 | Ed. 2.0, 2010-04 | §1.2 k) | "requires malevolent and unauthorised actions to be considered during hazard and risk analysis. The scope of the analysis includes all relevant safety lifecycle phases" | ⛔ 不覆盖（对象是**产品**的危害分析，⛔ 不是开发制品的保密） | 同上 | 🟢 |
| IEC 61508-3 | Ed. 2.0, 2010-04 | 完整目录 Clause 1-8 + Annex A-G | 目录中**无**任何保密 / 数据保护 / 第三方数据处理条款 | ⛔ 不覆盖 | [preview PDF](https://cdn.standards.iteh.ai/samples/14797/4d43d90b5ea645fb998fd65139757ed2/IEC-61508-3-2010.pdf) | 🟢 |
| IEC 61508-3 | Ed. 2.0, 2010-04 | §7.4.4 | "Requirements for support tools, including programming languages"（标题，⛔ 正文在 preview 外） | ⭐ **工具钩子**（非保密） | 同上 | 🔴（标题 🟢） |
| ISO 26262-8 | 2018 | §1 Scope | 支持过程枚举共 12 项，⛔ **无**保密 / 信息安全 / 数据处理项 | ⛔ 不覆盖 | [preview PDF](https://cdn.standards.iteh.ai/samples/68390/8b6b8ddbf06b436e8ac60f72f63c17d9/ISO-26262-8-2018.pdf) | 🟢 |
| ISO 26262-8 | 2018 | §5.1 | "a) to define the interactions and dependencies between customers and suppliers for development activities; b) to describe the allocation of responsibilities; and c) to identify the work products to be exchanged for distributed developments" | ⛔ **不覆盖，且方向相反**（⛔ 它是**共享**制品的机制） | 同上 | 🟢 |
| ISO 26262-8 | 2018 | §5.2 NOTE 1 | "The Development Interface Agreement (DIA) aims to describe the **roles and responsibilities** between the customer and supplier." | ⛔ 不覆盖（⭐ **责任划分**，⛔ 非数据驻留） | 同上 | 🟢 |
| ISO 26262-8 | 2018 | §5.2 NOTE 2 | "This clause is not relevant for the procurement which do not place any responsibility for safety on the supplier" | ⛔ 不覆盖（⛔ LLM API 供方不承担安全责任 → **Clause 5 根本不适用**） | 同上 | 🟢 |
| ISO 26262-8 | 2018 | §5.4.2.1 + NOTE | 供方选择准则 = "capability to develop and, if applicable, produce items and elements of comparable complexity and ASIL"；NOTE 列 5 项准则，⛔ **无一项涉及保密或信息安全** | ⛔ 不覆盖 | 同上 | 🟢 |
| ISO 26262-8 | 2018 | Clause 11（11.4.1-11.4.9） | "Confidence in the use of software tools"（目录，⛔ 正文在 preview 外） | ⭐ **工具钩子**（非保密） | 同上 | 🔴（目录 🟢） |
| ISO 26262-6 | 2018 | §5.2 NOTE 2 | "Cybersecurity **can** also be considered when developing the embedded software of a particular item, see ISO 26262-2:2018, 5.4.2.3." | ⛔ 不覆盖（⛔ "can" = 非强制，⛔ 且指向**产品**网络安全） | [preview PDF](https://cdn.standards.iteh.ai/samples/68388/34205953cd2c4c5f947890009caa464e/ISO-26262-6-2018.pdf) | 🟢 |
| ISO 26262-2 | 2018 | Annex E（informative） | "Guidance on potential interaction of functional safety with cybersecurity" | ⛔ 不覆盖（⛔ **informative**，非规范性） | [preview PDF](https://cdn.standards.iteh.ai/samples/68384/a48c82d694274496bcb249700a63ac2f/ISO-26262-2-2018.pdf) | 🟢（目录） |
| ISO/SAE 21434 | 2021 | §1 Scope | "This document **does not prescribe specific technology or solutions** related to cybersecurity." | ⛔ **不覆盖（标准自陈排除）** | [preview PDF](https://cdn.standards.iteh.ai/samples/iso/iso-sae-21434-2021/d10b253f4fa94db482416f4fc608d83a/iso-sae-21434-2021.pdf) | 🟢 |
| ISO/SAE 21434 | 2021 | Clause 7（Introduction 描述） | "Clause 7 (Distributed cybersecurity activities) includes requirements for **assigning responsibilities** for cybersecurity activities between customer and supplier." | ⛔ 不覆盖（⭐ 与 26262 DIA 同构：**责任划分**） | 同上 | 🟢 |
| ISO/IEC TR 5469 | 2024 | §1 Scope 第三项 | "use of AI systems to **design and develop** safety related functions" | ⛔ 不覆盖保密，⭐ **但正面承认本文的使用场景** | [preview PDF](https://cdn.standards.iteh.ai/samples/81283/a480bab0b69c4335986c2b0de971308d/ISO-IEC-TR-5469-2024.pdf) | 🟢 |
| DO-178C / DO-330 | 2011 | — | 见 §1.6 | 见 §1.6 | 见 §1.6 | 见 §1.6 |
| EN 50128 / EN 50716 | 2011+A2:2020 / 2023 | — | 见 §1.7 | 见 §1.7 | 见 §1.7 | 见 §1.7 |
| IEC 62304 | 2006+A1:2015 | — | 见 §1.8 | 见 §1.8 | 见 §1.8 | 见 §1.8 |

### 1.2 IEC 61508（通用功能安全）· 结论：⛔ **明确排除，证据等级最高**

⭐ 这是 Q1 里**最干净的一条否定结论**，⛔ 因为它不是「查不到」，⛔ 而是标准在 Scope 里**逐字写明自己不管**。IEC 61508-1:2010 §1.2 用 a) 到 n) 逐项界定范围，⛔ 其中 l) 与 m) 两项连续排除了安全防护（security）相关内容：l) 排除「防止未授权人员损害功能安全的预防措施」，m) 排除「为满足安全策略所需的安全策略或安全服务的开发、实施、维护和/或运行要求」。⭐ k) 项确实要求「在危害与风险分析中考虑恶意与未授权行为」，⛔ **但其对象是被控设备（EUC）这个产品**，⛔ 不是开发过程中的工程文档；⭐ 且 NOTE 5 明确把这个主题外包给 ISO/IEC TR 19791 与 IEC 62443 系列。

⭐ IEC 61508-3（软件部分）的**完整目录**（Clause 1 Scope / 2 Normative references / 3 Definitions / 4 Conformance / 5 Documentation / 6 Additional requirements for management of safety-related software / 7 Software safety lifecycle requirements / 8 Functional safety assessment + Annex A-G）**不含任何保密、数据保护或第三方数据处理条款**。⭐ 在 preview 覆盖的 15 页（前言、引言、完整目录、完整 Scope）中，对 `security` / `confidential` / `third part` / `supplier` / `outsourc` 五个词做全文检索，**命中数为 0**。⚠️ 需诚实标注：preview 不覆盖全部正文，⛔ 因此这条只能表述为「**完整目录中无此类条款**」，⛔ 不能表述为「全文无此词」。

⭐ **工具钩子**：IEC 61508-3 §7.4.4「Requirements for support tools, including programming languages」与 Annex A Table A.3「Software design and development – support tools and programming language」是本标准处理「用工具开发安全相关软件」的落点；⭐ 61508-3 §1.1 c) 亦写明本部分「provides specific requirements applicable to support tools used to develop and configure a safety-related system」。⛔ 这些条款管的是**工具可信度**，⛔ 不管工具部署在哪里、数据发给谁。

### 1.3 ISO 26262（汽车功能安全）· 结论：⛔ **无，且 DIA 误读风险已证实**

⭐ **Part 8 的 Scope 枚举是本轮最有力的结构性证据**。ISO 26262-8:2018 §1 明确列出本部分规定的全部支持过程：`interfaces within distributed developments` / `overall management of safety requirements` / `configuration management` / `change management` / `verification` / `documentation management` / `confidence in the use of software tools` / `qualification of software components` / `evaluation of hardware elements` / `proven in use argument` / `interfacing an application that is out of scope of ISO 26262` / `integration of safety-related systems not developed according to ISO 26262`。⛔ **十二项里没有任何一项涉及保密、信息安全或数据处理。** ⭐ 由于 Part 8 正是 ISO 26262 系列中承载「支持过程」的那一部分，⛔ 若整个系列存在此类要求，⛔ 它只可能落在这里——⛔ 而它不在。

⚠️ **DIA 误读排查（任务点名的高风险项）· 结论：先验判断正确，且比预期更强。** ISO 26262-8:2018 §5.1 把 Clause 5 的目标逐字定为三项：a) 定义客户与供方在开发活动中的交互与依赖；b) 描述**责任的分配**；c) 识别分布式开发中**需要交换的工作产品**。⭐ §5.2 NOTE 1 再次逐字确认：「The Development Interface Agreement (DIA) aims to describe the **roles and responsibilities** between the customer and supplier.」⛔ **通篇没有任何关于数据存放地、传输限制或保密义务的表述。**

⛔ **更关键的是方向问题**：§5.1 c) 的目标是「**identify the work products to be exchanged**」——⛔ Clause 5 是一套**授权并规范化「把工作产品交给外部方」**的机制，⛔ 而不是禁止它的机制。⛔ 若论文把 DIA 引成「须与供方签订接口协议 → 故不得外发」，⛔ **不仅是误读，⛔ 而且是把一条方向相反的条款反向使用**，⛔ 任何熟悉 ISO 26262 的审稿人都会当场击穿。⛔ 本台账将此列为**禁止引用方式**。

⛔ **还有一层：Clause 5 对 LLM API 根本不适用。** §5.2 NOTE 2 逐字写明「This clause is not relevant for the procurement which do not place any responsibility for safety on the supplier」。⛔ 第三方 LLM API 供应商不承担任何功能安全责任，⛔ 因此它**不是 ISO 26262 意义上的 supplier**，⛔ Clause 5 整章不适用。

⭐ **供方选择准则也无保密项。** §5.4.2.1 规定供方选择准则「shall include an evaluation of the supplier's capability to develop and, if applicable, produce items and elements of comparable complexity and ASIL」，⭐ 其 NOTE 列举五项准则：供方质量管理体系证据、供方以往绩效与质量、供方投标中对功能安全能力的确认、依 ISO 26262-2:2018 6.4.12 的既往功能安全评估结果、整车厂各部门的推荐意见。⛔ **五项中无一项涉及信息安全、保密或数据处理能力。**

⭐ **网络安全在 ISO 26262 中的地位是「可选 + 外链」。** Part 6 §5.2 NOTE 2 逐字写「Cybersecurity **can** also be considered ... see ISO 26262-2:2018, 5.4.2.3」——⛔ 用的是 "can" 而非 "shall"；⭐ Part 2 的对应落点 Annex E 标题为「Guidance on potential interaction of functional safety with cybersecurity」，⛔ 且标注为 **informative**（资料性），⛔ 不具规范性效力。

⛔ **未直接核验项**：§5.4.3「Initiation and planning of distributed development」（DIA 内容清单，⛔ 二手来源称含 11 项要求）与 Clause 11「Confidence in the use of software tools」正文，⛔ 均落在 preview 范围之外，⛔ 标 🔴。⚠️ ⛔ 但即使这两处含未见内容，⛔ 也不改变 §1 Scope 的枚举结论——⛔ 因为 Scope 是对整个 Part 8 内容的穷举式声明。

### 1.4 ISO/SAE 21434（汽车网络安全）· 结论：⛔ **无，且标准自陈不规定技术方案**

⚠️ 任务判断「这本最可能命中」——⭐ **实测结果是不命中，⛔ 而且是被标准自己的 Scope 排除的。** ISO/SAE 21434:2021 §1 Scope 末句逐字写道：「This document **does not prescribe specific technology or solutions** related to cybersecurity.」⛔ 这一句直接切断了「因为 21434 所以必须私域部署」这条推理链——⛔ 私域部署正是一个「specific technology or solution」。

⭐ **对象错配是更根本的问题。** 21434 §1 Scope 界定其对象为「electrical and electronic (E/E) systems in road vehicles, including their components and interfaces」——⛔ 即**车上的产品**，⛔ 而不是 OEM 内部的工程文档。⛔ 换言之，21434 保护的是「车会不会被黑」，⛔ 不是「需求文档会不会外泄」。⛔ 这个错配对整个 Q1 族都成立，⛔ 是本轮最重要的结构性发现之一。

⚠️ **Clause 编号纠错**：Clause 7 是 `Distributed cybersecurity activities`（分布式网络安全活动），⛔ **不是** TARA；⭐ TARA 方法在 **Clause 15**（`Threat analysis and risk assessment methods`）。⭐ 上述编号取自 21434 preview 的 Introduction 逐条目录说明，🟢 已核验。⭐ Introduction 对 Clause 7 的逐字描述为「includes requirements for **assigning responsibilities** for cybersecurity activities between customer and supplier」——⭐ 与 ISO 26262-8 Clause 5 完全同构：**责任划分，非数据驻留**。

⛔ **未直接核验项**：Clause 7 正文（含 CIA / Cybersecurity Interface Agreement 的具体要求）与 Annex C，⛔ 均在 preview 之外，⛔ 标 🔴。⚠️ ⛔ 二手来源（咨询公司博客）称 CIA 需约定「the information and work products to be shared」——⛔ 若属实，⛔ 则与 ISO 26262 DIA 同样是**共享机制**而非禁止机制，⛔ 但此点**未经官方原文核验**，⛔ 不得作为事实引用。

### 1.5 ISO/IEC TR 5469:2024（AI 与功能安全）· ⭐ **本轮意外收获，且对论文有正面价值**

⭐ 这份 TR 不在任务清单内，⭐ 但它是**整个 Q1 检索中与本文课题最贴合的一份国际标准文件**。ISO/IEC TR 5469:2024 §1 Scope 列出三类场景，⭐ **第三项逐字为「use of AI systems to design and develop safety related functions」**——⛔ 这正是本文的场景（用 LLM 参与安全相关状态机模型的构建与缺陷发现）。

⭐ **论文价值**：它提供了一条**权威、可引、且免费可核验**的依据，⛔ 用来支撑「把 AI 用于安全相关功能的设计与开发，是国际标准化组织已正式承认并正在制定保障方法的一类活动」。⛔ 这**不能**支撑「必须私域部署」，⭐ 但可以支撑论文引言里「为什么这件事需要可断言、可追溯的方法」——⭐ 而**可断言可追溯正是本文的真正卖点**（见 [README.md](./README.md) 对用户 2026-08-13 意见的记录）。⭐ 这比一条勉强的保密依据更贴合我们的实际主张。

⛔ **但它同样不含数据驻留条款**：完整目录（Clause 1-11 + Annex A-D）中最接近的是 §10.3.5「Protection of the data and parameters」，⛔ 从其所在章节（10.3「Increase the reliability of components containing AI technology」）判断，⛔ 它讨论的是**模型数据与参数的完整性/可靠性**，⛔ 而非「不得把输入数据发给第三方」。⛔ 正文在 preview 之外，⛔ 标 🔴，⛔ **不据标题推断内容**。

### 1.5b IEC 62443-4-1:2018（工控产品安全开发生命周期）· ⭐⭐ **本轮 Q1 族最强的一条，且是顺着 61508 的官方指引找到的**

⭐ **发现路径本身就是证据链**：IEC 61508-1:2010 §1.2 k) 的 NOTE 5 逐字写「Other IEC/ISO standards address this subject in depth; see ISO/IEC/TR 19791 and **IEC 62443 series**」——⭐ 即 IEC 61508 把安全防护主题**官方外包**给了 IEC 62443。⭐ 顺此线索命中 **IEC 62443-4-1:2018《Security for industrial automation and control systems — Part 4-1: Secure product development lifecycle requirements》**。

⭐ **域匹配度是全场最高的**：其 §1 Scope 逐字为「This part of IEC 62443 specifies process requirements for the secure development of **products used in industrial automation and control systems**」——⛔ 而本文的对象正是**控制系统**的状态机建模。⭐ Scope 亦逐字写明「These requirements apply to the **developer and maintainer** of the product, but not to the integrator or user of the product」——⭐ 即它约束的正是**我们这一方**（开发者），⛔ 而不是产品用户。

⭐ **命中的条款**（目录级 🟢 已核验，⛔ 条文级 🔴 付费墙）：

| 条款 | 标题（逐字） | 相关性 | 核验状态 |
| :-- | :-- | :-- | :-- |
| §5.9 | `SM-7: Development environment security` | ⭐⭐ **最相关**：⭐ 把「开发环境的安全」立为规范性过程要求 | 🟢 目录 / 🔴 条文 |
| §5.11 | `SM-9: Security requirements for externally provided components` | ⭐ 外部提供组件的安全要求 | 🟢 目录 / 🔴 条文 |
| §5.12 | `SM-10: Custom developed components from third-party suppliers` | ⭐ 第三方定制开发组件 | 🟢 目录 / 🔴 条文 |

⛔ **但必须诚实标注三点限制，⛔ 否则会重蹈 DIA 误读**：

1. ⛔ **条文未核验。** §5.9.1（Requirement）与 §5.9.2（Rationale and supplemental guidance）的正文落在付费墙内，⛔ preview 只暴露到前言、图表清单与部分术语定义。⛔ **不得写成「IEC 62443-4-1 要求不得把设计数据发给第三方」**——⛔ 这句话没有任何已核验依据。
2. 🟡 **二手描述指向的是完整性而非「禁止外发」。** 现有二手解读（[jtsec 培训材料](https://jtsec.es/files/IEC%2062443-4-1%20Practices%20&%20Requirementes.pdf)、[SecPortal](https://secportal.io/frameworks/iec-62443-4-1)）把 SM-7 的落地描述为「开发者工作站加固、源码仓库保护、构建服务器完整性」。⛔ 这更接近**防篡改**，⛔ 与 SM-6（File integrity）相邻的位置也支持这个读法。
3. ⛔ **它是「必须保护开发环境」，⛔ 不是「必须私域部署」。** ⭐ 能推出的最强命题是：「把设计制品送入一个不受控的外部服务，⭐ 属于 SM-7 项下必须被识别并处置的控制缺口」——⛔ 而「处置」的合规解可以是 ZDR 合同、可以是区域驻留、⛔ **也可以是私域部署，⛔ 但标准不指定哪一种**（⭐ 与 21434 §1「不规定具体技术或解决方案」同理）。

⭐ **对论文的正确用法**：可以引它来支撑「**控制系统产品的开发环境安全是一项成文的规范性要求**」这一背景句，⛔ 并自陈条文未核验；⛔ **不能**引它来支撑「必须私域部署」。⭐ 另注：修订版 `EN IEC 62443-4-1:2018/prAA:2026` 正在制定中，⭐ 目的之一是对齐欧盟 Cyber Resilience Act，⏳ 值得后续跟踪。

来源：[IEC 62443-4-1:2018 preview PDF](https://cdn.standards.iteh.ai/samples/21445/5d9b618cf732432b83b4e17e0e7b24cf/IEC-62443-4-1-2018.pdf)。

### 1.6 DO-178C / DO-330（航空）· ⏳ 待并入

⏳ 由并行分组核验中，⛔ 结果回报后并入。⚠️ ⛔ RTCA 文档为付费出版物，⛔ 预期多数条款只能标 🔴 或 🟡。⭐ 预设重点：DO-178C §7（Configuration Management）中的 protection 条款管的是**完整性/防篡改**而非**保密性**，⛔ 需逐条分清；⭐ DO-330 的 TQL 体系与 DO-178C §12.2 是**工具钩子**。

### 1.7 EN 50128 / EN 50716（铁路）· ⏳ 待并入

⏳ 由并行分组核验中，⛔ 结果回报后并入。⭐ 需确认 EN 50716:2023 取代 EN 50128 与 EN 50657 的生效/撤销日期。

### 1.8 IEC 62304（医疗器械软件）· ⏳ 待并入

⏳ 由并行分组核验中，⛔ 结果回报后并入。⭐ 预设重点：SOUP 机制管的是**已知缺陷与性能**，⛔ 不是数据保密，⛔ 需逐条分清。

---

## 2. Q2 · 其余各族（逐族）

### 2.1 出口管制 · 美国 ITAR / EAR · ⭐⭐⭐ **全台账最强的一条：⭐ 加密安全港在 LLM 推理场景下结构性不可满足**

⭐ **本节四条 eCFR 引文由主 session 亲自 `curl` eCFR 官方 API 抽取并逐字核对**（⛔ 非采信代理转述，⛔ 依仓库 §3.8 与「机械代理只能定位不能裁定」）。

| 法规 | 条款 | 逐字原文 | 是否覆盖 | 来源 | 核验状态 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| EAR, 15 CFR | §734.18(a)(5) | "Sending, taking, or storing 'technology' or 'software' that is: (i) Unclassified; (ii) Secured using 'end-to-end encryption;' (iii) Secured using cryptographic modules… compliant with… (FIPS 140-2) or its successors…; and (iv) Not intentionally stored in a country listed in Country Group D:5" ⭐ —— 属于 "activities that are **not** exports" | ⭐ **直接覆盖**（⭐ 安全港的构成要件） | [eCFR 15 CFR 734.18](https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C/part-734/section-734.18) | 🟢 |
| EAR, 15 CFR | **§734.18(b)** | "End-to-end encryption means (i) the provision of cryptographic protection of data such that the data is not in unencrypted form between an originator… and an intended recipient…, and **(ii) the means of decryption are not provided to any third party.** The originator and the recipient may be the same person." | ⭐⭐⭐ **直接覆盖，⛔ 且安全港不可满足** | 同上 | 🟢 |
| ITAR, 22 CFR | §120.54(a)(5) | "Sending, taking, or storing technical data that is: (i) Unclassified; (ii) Secured using end-to-end encryption; (iii) Secured using cryptographic modules… (FIPS 140-2)…; (iv) Not intentionally sent to a person in or stored in a country proscribed in §126.1…; and (v) Not sent from a country proscribed in §126.1" | ⭐ **直接覆盖** | [eCFR 22 CFR 120.54](https://www.ecfr.gov/current/title-22/chapter-I/subchapter-M/part-120/subpart-C/section-120.54) | 🟢 |
| ITAR, 22 CFR | **§120.54(b)(1)(ii)** | "The means of decryption are **not provided to any third party**." | ⭐⭐⭐ **直接覆盖，⛔ 且不可满足** | 同上 | 🟢 |
| ITAR, 22 CFR | **§120.54(b)(2)** | "The originator and the intended recipient may be the same person. **The intended recipient must be the originator, a U.S. person in the United States, or a person otherwise authorized to receive the technical data**, such as by a license or other approval pursuant to this subchapter." | ⭐⭐⭐ **直接覆盖，⛔ 且第三方 LLM 服务商不属任一类** | 同上 | 🟢 |
| ITAR / EAR | 22 CFR §120.54(c) / 15 CFR §734.18(c) | "The ability to access technical data in encrypted form that satisfies the criteria set forth in paragraph (a)(5)… does **not** constitute the release or export of such technical data." | ⭐ 直接覆盖（⭐ 反面确认：⛔ 不满足 (a)(5) 则无此豁免） | 同上 | 🟢 |

⭐⭐ **核心论证（⭐ 这是整份台账里唯一一条真正「直接管到这个动作、⭐ 且结论对我方有利」的成文依据）**：

1. ⭐ ITAR 与 EAR 都设了一个**加密安全港**：把受控技术数据加密后发送 / 存放于境外，⭐ **不构成出口**。
2. ⛔ **但两部法规对 "end-to-end encryption" 的定义都含同一个要件**：⭐ **"the means of decryption are not provided to any third party"**（EAR §734.18(b)(ii) 与 ITAR §120.54(b)(1)(ii) **措辞几乎完全一致**）。
3. ⛔ **第三方 LLM 服务商必须持有明文才能推理。** ⛔ 把制品送进公有云 LLM，⛔ 在**架构上**就等于把解密手段交给了第三方——⛔ **该要件结构性不可满足**，⛔ 不是「难满足」，⛔ 是**无法满足**。
4. ⛔ ITAR 还多叠一道：§120.54(b)(2) 要求收件人**必须是**发起人本人、美国境内的美国人、或经许可授权的人；⛔ 商用 LLM 服务商**不属任何一类**。
5. ⭐ **结论**：⭐ 对构成 ITAR `technical data` 或 EAR 管制 `technology` 的制品而言，⛔ **调用第三方 LLM API 无法援引加密安全港**；⛔ 此时该行为回落到一般的 release / deemed export 规则下评估（⭐ EAR §734.15、ITAR §120.17），⛔ 通常需要许可。

⛔ **但适用面必须自陈清楚，⛔ 否则会被一击打穿**：⛔ 上述结论**只对受管制物项成立**。⛔ 若制品是 **EAR99**（⛔ 绝大多数民用工业控制软件文档都是），⛔ 则根本不在管制范围内，⛔ 安全港的可满足性问题**不发生**。⛔ **不得把「ITAR/EAR 管制场景下不能用公有云 LLM」写成「工业场景下不能用公有云 LLM」。**

⚠️ **注意一个反向事实**：⭐ 加密安全港的存在本身说明立法者**允许**把受控技术数据放到境外云——⛔ 只要云商拿不到明文。⭐ 这正是机密计算 / 同态推理的立法空间；⛔ 也意味着**私域部署不是唯一合规解**，⛔ 只是当前唯一成熟的解。

### 2.1b 出口管制 · 中国 · 结论：⭐ **立法形态已涵盖，⛔ 但清单为空 → ⛔ 现行无义务**

| 法规 | 条款 | 逐字原文（关键片段） | 是否覆盖 | 来源 | 核验状态 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 出口管制法（2020） | 第二条第一款 | "国家对两用物项、军品、核以及其他与维护国家安全和利益、履行防扩散等国际义务相关的货物、技术、服务等物项…的出口管制，适用本法。" | ⛔ 不覆盖（⛔ 一般民用制品） | [商务部出口管制信息网](https://exportcontrol.mofcom.gov.cn/article/zcfg/gnzcfg/flfg/202111/226.html) | 🟢 |
| 出口管制法 | 第二条第二款 | "前款所称管制物项，**包括物项相关的技术资料等数据**。" | ⛔ 间接相关。⚠️ ⛔ **这一款只把管制物项的载体形态扩到数据，⛔ 不新增管制对象**——⛔ 单独拎出来当依据是误读 | 同上 | 🟢 |
| 出口管制法 | 第二条第三款（⭐ 中国版 deemed export） | "…是指国家对从中华人民共和国境内向境外转移管制物项，以及**中华人民共和国公民、法人和非法人组织向外国组织和个人提供管制物项**，采取禁止或者限制性措施。" | ⭐ 间接相关（⭐ 无形提供在射程内，⛔ 但宾语仍是「管制物项」） | 同上 | 🟢 |
| 出口管制法 | 第四条 | "国家实行统一的出口管制制度，**通过制定管制清单、名录或者目录…、实施出口许可等方式**进行管理。" | ⭐ **关键**：⛔ 管制的唯一开关是**清单** | 同上 | 🟢 |
| 出口管制法 | 第十二条第三款（catch-all） | "清单之外的货物、技术和服务，出口经营者**知道或者应当知道**，或者得到通知，可能存在以下风险的，应当申请许可：（一）危害国家安全和利益；（二）被用于…大规模杀伤性武器…；（三）被用于恐怖主义目的。" | ⛔ 间接相关（⛔ 需三类风险 + knowledge 要件） | 同上 | 🟢 |
| 两用物项出口管制条例（国务院令 792 号，2024-12-01） | 第二条第三款 | "…包括两用物项的贸易性出口及对外赠送、展览、合作、援助和**以其他方式进行的转移**…" | ⭐ 间接相关（⭐ deemed export 口径最宽处，⭐ 无形转移明文纳入） | [gov.cn 792 号令](https://www.gov.cn/zhengce/content/202410/content_6981399.htm) | 🟢 |
| ⭐ 两用物项出口管制清单（商务部等 2024 年第 51 号）§二（二）「关于技术的说明」 | 说明第 1、2 项 | "1．『技术』是指在产品的研发、生产或使用过程中所需的专门信息和知识…**对技术的出口管制不适用于公共领域信息、基础科学研究中的技术或普通专利申请所必需的知识。** 2．技术资料包括：蓝图、平面图、图表、**模型**、公式、**工程设计和技术规格**、手册与规程…" | ⚠️ ⭐ **形态命中、⛔ 对象不命中**（⭐ 见下） | [清单 PDF](https://picpolicy.mofcom.gov.cn/file/20241120/56691732080580306.pdf) | 🟢（⭐ 说明部分；⛔ 700 余项条目未逐条核验） |
| 禁止出口限制出口技术目录（商务部/科技部 2023 年第 57 号），⭐ **30 页全文逐条通读** | 涉软全部条目 | `083915X 计算机应用技术`、`086502X 计算机通用软件编制技术`（⭐ 巨型机 / 并行计算）、`086501X 信息处理技术`（⭐ 中文与少数民族语言处理、汉字识别、CAD 图纸档案管理、个性化推荐）、`206503X 基础软件安全增强技术` | ⛔ **不覆盖（⭐ 否定结论，⭐ 全文核验）**。⭐ 机械复核：「工业控制」0、「嵌入式」0、「需求」0、「状态机」0、「工业软件」0 | [目录全文 PDF](https://www.most.gov.cn/tztg/202312/W020231221620858841394.pdf) | 🟢 |
| 技术进出口管理条例（国务院令 331 号，⭐ 经 2011/2019/2020 三次修订） | **第五条** | "**国家准许技术的自由进出口**；但是，法律、行政法规另有规定的除外。" | ⛔ **不覆盖**（⭐ 默认自由原则） | [司法部国家行政法规库](http://xzfg.moj.gov.cn/front/law/detail?LawID=575) | 🟢 |
| 技术进出口管理条例 | 第二十八至三十条 | "第二十九条 属于禁止出口的技术，不得出口。第三十条 属于限制出口的技术，实行许可证管理；未经许可，不得出口。" | ⛔ 不覆盖（⛔ 完全绑定目录，⛔ 目录无条目） | 同上 | 🟢 |

⭐ **一处值得写进论文的形态吻合**：⭐ 两用物项清单对「技术资料」的定义**逐字包含「模型」与「工程设计和技术规格」**。⭐ 这说明中国立法者的技术资料概念**确实覆盖需求文档与状态机模型这类制品的形态**——⭐ **隔开我们的是「对象条件」（须为清单内物项研发/生产/使用所需），⛔ 不是「形态条件」。** ⭐ 这条有两个用处：(1) ⭐ 证明「工程制品是不是管制客体」在立法上**已有明确答案（⭐ 形态上是）**，⛔ 不是我们在过度解读；(2) ⭐ 给出一个**清晰的反转判据**——⭐ 若研究对象换成清单内受控装备（⭐ 航天、导弹、密码芯片）的设计模型，⭐ 判定立即反转为「覆盖」。⭐ 论文可用它精确划出适用边界。

⛔ **但中国这一族只能作为「立法趋势 / 客体形态已被涵盖」的注脚，⛔ 不能作为「现行合规义务」的依据。** ⛔ 三部出口管制法规都以**清单为唯一开关**，⛔ 而软件工程文档在任何清单上都找不到条目；⭐《技术进出口管理条例》第五条更确立「国家准许技术的自由进出口」的默认自由原则。⛔ **尤其不要**把《出口管制法》第二条第二款「包括技术资料等数据」单独拎出来当作「工程文档受管制」的证据——⛔ 那是脱离第一款限定的误读，⛔ 会被内行一眼看穿。

### 2.2 数据出境 / 数据主权 · 欧盟部分 · 结论：⛔ **GDPR 与 AI Act 均不适用，⭐ 仅 Data Act Art. 32 间接相关**

| 文件 | 年份 | 条款 | 逐字原文（关键片段） | 触发前提 | 是否覆盖「制品外发给第三方 LLM」 | 来源 | 核验状态 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| GDPR (EU) 2016/679 | 2016 | Art. 2(1) | "This Regulation applies to the processing of **personal data** wholly or partly by automated means…" | 处理对象须为个人数据 | ⛔ **不覆盖** | [CELEX:32016R0679](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679) | 🟢 |
| GDPR | 2016 | Art. 4(1) | "'personal data' means any information relating to an identified or identifiable natural person ('data subject')…" | 同上 | ⛔ **不覆盖** | 同上 | 🟢 |
| GDPR | 2016 | Art. 28(1) | "the controller shall use only processors providing sufficient guarantees to implement appropriate technical and organisational measures…" | ⛔ 仅当外发内容含个人数据 | ⛔ 间接相关（⛔ 前提不成立即不适用） | 同上 | 🟢 |
| GDPR | 2016 | Art. 44 | "Any transfer of **personal data**… to a third country or to an international organisation shall take place only if… the conditions laid down in this Chapter are complied with…" | 同上 + 跨境 | ⛔ 间接相关 | 同上 | 🟢 |
| Data Act (EU) 2023/2854 | 2023 | Art. 32(1) | "Providers of data processing services shall take all adequate technical, organisational and legal measures, including contracts, in order to **prevent international and third-country governmental access and transfer of non-personal data held in the Union** where such transfer or access would create a conflict with Union law…" | ⛔ 义务主体是 **provider**；⛔ 数据须 held in the Union | ⭐ **间接相关（欧盟数据族唯一可用的一条）** | [CELEX:32023R2854](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32023R2854) | 🟢 |
| Data Act | 2023 | Art. 32(2) | "Any decision or judgment of a third-country court… requiring a provider… to transfer or give access to non-personal data… shall be recognised or enforceable in any manner only if based on an international agreement, such as a mutual legal assistance treaty…" | 同上 | ⭐ 间接相关 | 同上 | 🟢 |
| Data Act | 2023 | Art. 4(6)/(7)/(8)、Art. 5(9)/(10) | 商业秘密在数据共享中的保全与拒绝共享权 | ⛔ **仅限 Chapter II**：connected product / related service 的 IoT 运行数据 | ⛔ **不覆盖（场景完全错位）** | 同上 | 🟢 |
| Data Act | 2023 | Art. 23 | "…to enable customers to switch to a data processing service… or to **on-premises ICT infrastructure**…" | 你是云客户 | ⛔ 不覆盖（⛔ 管锁定，⛔ 非保密）；⭐ 仅可作「立法承认迁回本地是正当选项」的软性佐证 | 同上 | 🟢 |
| AI Act (EU) 2024/1689 | 2024 | Art. 6(1)/(2) + Annex III | 高风险 = Annex I 立法覆盖产品的**安全部件**，或落入 Annex III 八类 | ⛔ 软件工程工具二者皆不属 | ⛔ **不覆盖** | [CELEX:32024R1689](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024R1689) | 🟢 |
| AI Act | 2024 | Art. 78(1)(a) | 委员会 / 市场监督机关 / 公告机构须尊重 "the intellectual property rights and confidential business information or trade secrets… **including source code**" | ⛔ 义务主体是**监管方** | ⛔ **不覆盖**（⛔ 约束监管者，⛔ 非 LLM 服务商） | 同上 | 🟢 |
| AI Act | 2024 | Art. 2(6)/(8) | 排除「专为科学研发唯一目的」开发投用的 AI 系统与上市前研发测试 | — | ⭐ **反向有用**：⭐ 我们自己的研究原型不受 AI Act 约束 | 同上 | 🟢 |
| Garante（意大利 DPA） | 2023 | Provv. 30/03/2023 [9870832] | 对 OpenAI 的临时限制令，⛔ 理由全部是 GDPR 项下个人数据问题（无告知、无法律依据、数据不准确、无年龄验证） | ⛔ 个人数据 | ⛔ **不覆盖** | [garanteprivacy.it 9870847](https://www.garanteprivacy.it/web/guest/home/docweb/-/docweb-display/docweb/9870847) | 🟢 |

⛔ **GDPR 必须放弃，⛔ 且理由要说清是「前提不成立」而非「成本高」。** Art. 2(1) 把整部条例锚定在个人数据上，Art. 4(1) 又把个人数据定义为「与已识别或可识别的自然人相关的任何信息」。⛔ 控制系统的功能安全需求、状态机模型、迁移守卫、时序约束里**没有自然人**，⛔ 因此 Chapter V（Art. 44-49）与 Art. 28 **根本不触发**。⚠️ 唯一窄例外：若文档元数据带工程师姓名 / 邮箱 / 工号 / 评审署名，⛔ 那部分构成个人数据——⛔ 但这是「文档附带的人名」问题，⛔ 拿它论证「必须私域部署 LLM」是偷换论题，⛔ 审稿人一句话就能反驳。

⛔ **AI Act 也必须放弃，⭐ 但这条否定结论有正面用途。** 全文**没有任何条款规制用户输入数据的保密性**；唯一的 confidentiality 条款 Art. 78 方向相反（约束监管方不得泄露被监管者的源码与商业秘密）。⭐ 可在论文里明确写「AI Act 未对工程制品外发施加约束，⭐ 故该风险须由其他机制承担」，⭐ 把读者导向商业秘密法与行业机制，⭐ 反而使论证更严密。

⭐ **Data Act Art. 32 是欧盟数据族唯一可留的一条**，⛔ 但必须写清它把缓解义务放在 **provider** 身上而非禁止 deployer 外发。⭐ 可用表述：欧盟已就非个人数据的第三国政府调取风险作出成文回应，⭐ 从立法层面确认「把非个人工业数据交给受第三国管辖的云服务」存在被承认的法律风险。适用日期 2025-09-12（Art. 50）。

### 2.3 国防供应链（美国 DFARS / NIST SP 800-171 / CMMC）· ⭐ **英文世界里唯一直接管到这个动作的一族，⛔ 但它是「条件性允许」而非「禁止」**

⭐ **本节的 DFARS 三条由主 session 亲自 `curl` acquisition.gov 全文抽取并逐字核对**（⛔ 非采信代理转述，⛔ 依仓库 §3.8 纪律）。⭐ 版本标记：条款标题为 `SAFEGUARDING COVERED DEFENSE INFORMATION AND CYBER INCIDENT REPORTING (MAY 2024)`，⭐ 页面标注 DFARS Change 05/07/2026。

| 文件 | 版本 | 条款 | 逐字原文 | 触发前提 | 是否覆盖 | 来源 | 核验状态 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| DFARS 252.204-7012 | MAY 2024 | (b)(2)(ii)(D) | "If the Contractor intends to use an **external cloud service provider to store, process, or transmit any covered defense information** in performance of this contract, the Contractor shall require and ensure that the cloud service provider meets **security requirements equivalent to those established by the Government for the Federal Risk and Authorization Management Program (FedRAMP) Moderate baseline**… and that the cloud service provider complies with requirements in paragraphs (c) through (g) of this clause…" | 合同含本条款 + 外发内容构成 CDI | ⭐⭐ **直接覆盖该动作**，⛔ **但形态是条件性允许** | [acquisition.gov](https://www.acquisition.gov/dfars/252.204-7012-safeguarding-covered-defense-information-and-cyber-incident-reporting.) | 🟢 |
| DFARS 252.204-7012 | MAY 2024 | (a) 定义 `Controlled technical information` | "technical information with **military or space application** that is subject to controls on the access, use, reproduction, modification, performance, display, release, disclosure, or dissemination. Controlled technical information would meet the criteria, if disseminated, for **distribution statements B through F** using the criteria set forth in DoD Instruction 5230.24… The term does not include information that is lawfully publicly available without restrictions." | — | ⭐ **关键**：⭐ 军用/航天控制系统的需求与设计数据通常落入此定义 | 同上 | 🟢 |
| DFARS 252.204-7012 | MAY 2024 | (a) 定义 `Covered defense information` | "unclassified controlled technical information or other information, as described in the Controlled Unclassified Information (CUI) Registry… that requires safeguarding or dissemination controls… and is— (1) Marked or otherwise identified in the contract… and provided to the contractor by or on behalf of DoD…; or (2) **Collected, developed, received, transmitted, used, or stored by or on behalf of the contractor** in support of the performance of the contract." | — | ⭐ **关键**：⭐ (2) 明确覆盖承包商**自己开发**的制品，⛔ 不限于政府交付物 | 同上 | 🟢 |
| DFARS 252.204-7012 | MAY 2024 | (b)(2)(i) | 非政府运营 IT 服务的承包商系统，⭐ 适用 NIST SP 800-171（⭐ 以招标发布时生效版为准，⛔ 或经 Contracting Officer 授权） | 同上 | ⭐ 间接相关（⭐ 引入 800-171 控制项） | 同上 | 🟢 |
| DFARS 252.204-7012 | MAY 2024 | (b)(1)(i) | 云计算服务落入 DFARS 252.239-7010《Cloud Computing Services》 | ⛔ 仅当系统是**为政府运营**的 IT 服务 | ⛔ 间接相关（⛔ 触发条件较窄） | 同上 | 🟢 |
| NIST SP 800-171 / CMMC(32 CFR 170) | — | — | ⏳ 由并行分组核验 | — | ⏳ | — | ⏳ |

⭐ **这是整份台账里唯一一条**逐字点名「把受控信息交给外部云服务处理」**这个具体动作的成文规范**，⭐ 且它是**免费公开全文、可核验到条款级**的。⭐ 论证链条完整：(1) 军用 / 航天控制系统的技术数据构成 `controlled technical information`；(2) 承包商**自己开发**的相关制品即构成 `covered defense information`（⭐ 定义 (2) 项）；(3) 一旦要把它交给外部云服务 store / process / transmit，⭐ 就触发 FedRAMP Moderate 等效要求 + (c)-(g) 的事故报告、恶意软件、介质保全、取证访问、损害评估等一整套义务。

⛔ **但必须钉死一件事：它是「条件性允许」，⛔ 不是「禁止」。** ⛔ 条文写的是 "**shall require and ensure that the cloud service provider meets** security requirements equivalent to… FedRAMP Moderate"——⛔ 即**满足即可用**。⛔ **不得把它引成「不得使用云服务」**，⛔ 这与 ISO 26262 DIA 是同一类误读。⚠️ 且由于主流云厂商的政府云版本已有 FedRAMP 授权（⏳ 具体授权状态由并行分组核验，⛔ 以 FedRAMP Marketplace 官方记录为准），⛔ **这条依据推不出「必须私域部署」**，⭐ 只能推出「不能用普通商用端点」。

### 2.4 行业机制 · 欧盟汽车业 TISAX / VDA ISA · ⭐⭐ **本轮 Q2 最强、且是第一手 XLSX 逐格核验**

⭐ **这是整份台账里唯一「直接覆盖」且**逐字点名 AI 工具**的成文依据。** ⭐ 它不是立法，⛔ 而是欧盟汽车供应链事实上的准入机制（TISAX label 是 OEM 采购的门槛）。

**版本事实（🟢 官方 XLSX 已下载逐格核验）**：⭐ 当前生效目录是 **VDA ISA 6.0.3**（文件 `isa6-en.xlsx`，ENX 下载页标注 2024-04-25，⚠️ 但文件内 Cover 版本戳写 `6.0.3 | 2023-04-12`，⛔ 两者不一致，⛔ 如实记录）；⭐ 新版 **ISA2027** 已于 **2026-07-01** 发布（`isa2027-en.xlsx`），⭐ 适用于 **2027-01-01 起下单**的评估。⛔ **不存在 ISA 6.1 / 6.2**——ENX 已放弃小数版本号，改为年份命名 + 年度发布。入口：[ENX downloads](https://portal.enx.com/en-US/TISAX/downloads/)。

| 文件 | 版本 | 控制项 | 逐字原文（关键片段） | 触发前提 | 是否覆盖 | 核验状态 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| VDA ISA2027 | 2026-07-01 | Glossary `Cloud/external IT service` | Examples: "**Cloud services, such as AI tools (e.g., AI chatbots, AI agents)**, hosting, web services such as anti-virus dashboards, SIEM services provided by external companies, etc." | 组织参加 TISAX 评估 | ⭐⭐ **直接覆盖** | 🟢 |
| VDA ISA2027 | 2026 | 1.3.3（must） | "External IT services are not used without explicit assessment and implementation of the information security requirements. The following aspects are considered: - Availability of a risk assessment of the external IT services, - Legal, regulatory, and contractual requirements. + The external IT services have been harmonized with the protection need of the processed information assets." | 同上 | ⭐ **直接覆盖** | 🟢 |
| VDA ISA2027 | 2026 | 1.3.3 Objective | "…**This is particularly common with IT services available online at little to no cost**, as users may be able to obtain these services without following proper approval processes that consider information security." | 同上 | ⭐ 直接覆盖 | 🟢 |
| VDA ISA2027 | 2026 | 6.1.1（very high，⭐ **本版新增**） | "The adequate level of information security should be demonstrated by a third party audit (**an adequate TISAX label or equivalent**) or an adequate supplier audit… If an audit was not conducted, a **risk-based decision must be made by the organization's management** to continue doing business with the supplier. A record of this decision exists. (C, I, A)" | 信息为 very high / strictly confidential | ⭐ **直接覆盖** | 🟢 |
| VDA ISA 6.0.3 / 2027 | — | 5.1.2（very high） | "Information is transported or transferred in **content-encrypted form**. (C)" | very high 保密需求信息的传输 | ⭐⭐ **直接覆盖（⭐ 最接近硬约束的一条）** | 🟢 |
| VDA ISA 6.0.3 / 2027 | — | 5.3.4（must） | "Effective segregation (e.g., segregation of customers) prevents access to own information by unauthorized users of other organizations." | 使用多租户外部 IT 服务 | ⭐ 直接覆盖 | 🟢 |
| VDA ISA 6.0.3 / 2027 | — | 6.1.2（must） | "Valid non-disclosure agreements are concluded **prior to** forwarding sensitive information." | 向组织外传递受保护信息 | ⭐ 直接覆盖 | 🟢 |
| VDA ISA 6.0.3 | 2023/2024 | Glossary 同词条 | "An external service is the processing of company information outside the audit scope. (e.g. external hosting, cloud service, web services such anti-virus dashboards on the web, SIEM services provided by external companies, etc.)" | — | ⭐ 直接覆盖，⛔ **但无 AI 字样** | 🟢 |
| TISAX Participant Handbook | 2.8, 2023-12-07 | §4.3.3.1 / §4.3.3.5 | "You can select the assessment objectives 'Info high' and 'Info very high' **only until 31 March 2024**." / "…'Confidential' and 'Strictly confidential' **from 1 April 2024**."；映射：Confidential → **AL 2**，Strictly confidential → **AL 3** | — | ⭐ 直接覆盖（⭐ 定义评估强度分级） | 🟢 |

⭐ **ISA2027 的 AI 新增是本轮最有价值的第一手发现，⭐ 且已做机械对拍。** 对两份官方 XLSX（含 `sharedStrings.xml` 原始 XML）做全文件检索：`isa6-en.xlsx` 中 `AI` / `artificial intelligence` / `machine learning` / `LLM` **命中 0 次**；`isa2027-en.xlsx` 中仅命中 1 次，⭐ 即上述 Glossary 词条。⭐ **这个改动的分量不在于新增一条 AI 规则，⭐ 而在于它把「AI 聊天机器人 / AI agent」以定义方式钉进 `Cloud/external IT service`，⭐ 于是所有针对外部 IT 服务的既有控制项（1.3.3、5.3.3、5.3.4、6.1.1、6.1.3）自动全部适用于 LLM API。** ⚠️ ⛔ 如实提醒：ENX 官方 ISA2027 新闻稿**通篇未提 AI**，⛔ 宣传重点是供应链安全与 Prototype Protection 重构；⛔ 此发现系从 XLSX 挖出，⛔ **引用时必须引 XLSX 本身，⛔ 不要引新闻稿**。

⚠️ **`Info High` / `Info Very High` 标签已于 2024-03-31 作废**，⛔ 现行为 `Confidential` / `Strictly confidential`；⛔ 任务描述与许多二手资料仍在用旧标签，⛔ 引用时须更正。

⛔ **但措辞必须收紧，⛔ 不能写成「禁止」。** ⛔ ISA 没有任何一条写「不得使用公有云 LLM」。⭐ 它写的是「必须评估、审批、文档化；very high 档需内容级加密传输 + 供应商第三方审计保证，⛔ 否则须管理层书面风险决策存档」。⭐ **诚实的论文表述应是**：

> 在欧盟汽车供应链中，将高保密等级的工程制品发送至公有云 LLM 服务并非被法律禁止，而是被行业合规机制施加了实质性的准入摩擦——外部 IT 服务须经显式风险评估与审批（VDA ISA 1.3.3），very high 保密需求的信息须以内容级加密形式传输（5.1.2），其服务供应商须具备第三方审计保证（ISA2027 6.1.1）。私域部署因此成为既有审批链下阻力最小的默认路径，而非法定义务。

⚠️ ⛔ **适用面收窄警告**：⭐ 该论证对**汽车供应链**成立（TISAX 是事实准入门槛），⛔ 对一般工业控制系统不成立。⛔ 若论文语料覆盖 BSN / Elevator / Microwave 这类非汽车系统，⛔ **不得把汽车业结论外推过去**。

### 2.4a 行业机制 · ISO/IEC 27001:2022 Annex A 5.23（⭐ ISA 1.3.3 的上游对标项）

⭐ VDA ISA 1.3.3 在其 XLSX 的对标列中指向 **ISO/IEC 27001:2022 Annex A 5.23**。⭐ 该控制项标题逐字为 **"Information security for use of cloud services"**，⭐ 是 2022 版**新增**控制项（⛔ 2013 版中不存在，⛔ 当时云服务归入供方关系章节）。🟡 其控制文本（要求就云服务的**获取、使用、管理与退出**建立符合组织信息安全要求的流程）**仅有二手来源**，⛔ 正文在 ISO 付费墙内，⛔ 标 🟡。⛔ 论文若引用，⛔ 只应引**标题与新增事实**，⛔ 不得逐字引控制文本。二手出处：[ISMS.online A.5.23](https://www.isms.online/iso-27001/annex-a-2022/5-23-information-security-use-of-cloud-services-2022/)、[Advisera](https://advisera.com/iso27001/control-5-23-information-security-for-use-of-cloud-services/)。

### 2.4b 行业机制 · UNECE R155 / R156 · 结论：⛔ **间接相关，⛔ 需跨一步不小的推理**

| 文件 | 年份 | 条款 | 逐字原文 | 是否覆盖 | 来源 | 核验状态 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| UN R155 | 2021 | §7.2.2.5 | "The vehicle manufacturer shall be required to demonstrate how their Cybersecurity Management System will manage dependencies that may exist with **contracted suppliers, service providers or manufacturer's sub-organizations**…" | ⛔ 间接相关 | [CELEX:42021X0387](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:42021X0387) | 🟢（⚠️ OJ 转载版） |
| UN R155 | 2021 | §5.1.1(a) / §7.3.2 | "Collect and verify the information required under this Regulation **through the supply chain**…" / "shall identify and manage… supplier-related risks" | ⛔ 间接相关 | 同上 | 🟢 |
| UN R155 | 2021 | Annex 5 Part A §4.3.1 | 威胁条目 "Extraction of copyright or proprietary software from vehicle systems (product piracy)" | ⛔ **不覆盖**（⛔ 针对**车上系统**被提取，⛔ 非开发期文档外发） | 同上 | 🟢 |
| UN R156 | 2021 | 全文 | 仅 §3.3 一句关于型式认证材料 know-how 保密 | ⛔ **不覆盖** | [CELEX:42021X0388](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:42021X0388) | 🟢 |

⚠️ `unece.org` 直连返回 **403**，⭐ 改用 EUR-Lex 转载的 OJ 版本（OJ L 82, 9.3.2021）；⛔ 该版本自带声明「Only the original UN/ECE texts have legal effect under international public law」，⛔ 引用时须标注。

### 2.5 商业秘密法（欧盟 TSD）· 结论：⭐ **法理最强，⛔ 但是推论，⛔ 无判例**

| 文件 | 年份 | 条款 | 逐字原文 | 是否覆盖 | 来源 | 核验状态 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Directive (EU) 2016/943 | 2016 | Art. 2(1)(a)(b)(c) | "'trade secret' means information which meets **all** of the following requirements: (a) it is secret…; (b) it has commercial value because it is secret; (c) **it has been subject to reasonable steps under the circumstances, by the person lawfully in control of the information, to keep it secret**" | ⭐ **间接相关（⭐ 欧盟一族最强）** | [CELEX:32016L0943](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016L0943) | 🟢 |
| Directive (EU) 2016/943 | 2016 | Art. 4(3)(b) | "The use or disclosure of a trade secret shall be considered unlawful whenever carried out, without the consent of the trade secret holder, by a person who… (b) [is] in breach of a **confidentiality agreement or any other duty not to disclose** the trade secret" | ⭐ 间接相关（⛔ 无 NDA / DPA 时对方不负此义务） | 同上 | 🟢 |

⭐ **逻辑链**：⭐ 三要件是**累积**的（"meets **all**"）。⭐ 若设计制品满足 (a) 秘密性与 (b) 商业价值，⛔ 而组织在无 DPA / 无 NDA / 无零留存承诺的情况下把它明文送入公有云 LLM，⛔ 则对方不负 Art. 4(3)(b) 意义上的保密义务，⛔ 于是要件 (c) 可能被认定不成立——⛔ **商业秘密保护整体丧失**（⛔ 注意：不是被侵害，⛔ 是从一开始就不受保护）。

⛔ **必须如实标注两点**：(1) ⛔ **这是学理推论，⛔ 不是成文要求**——TSD 里没有任何一条写「向 AI 服务上传即丧失保护」；(2) ⚪ **欧盟侧无判例**——未找到任何 CJEU 或成员国判决把 Art. 2(1)(c) 适用于 AI chatbot 上传情形。🟡 检索到的唯一同形态判决是美国 *Trinidad v. OpenAI*（N.D. Cal., 2026-01，DTSA 项下），⛔ 事实形态特殊（⛔ 原告本人用 ChatGPT 创作了所主张的秘密），⛔ **不可作为欧盟依据**；🟡 另有二手报道称奥地利最高法院 4 Ob 165/16t 认为该要件只要求「合理努力」而非「成功保密」，⛔ 若属实**反而对强主张不利**。

⭐ **可写的安全表述**：Directive (EU) 2016/943 Art. 2(1)(c) 使商业秘密保护条件性地依赖于持有人所采取的保密措施；将设计制品送入不承担保密义务的公有 LLM 服务，会对该要件构成可争辩的削弱，⛔ 而这一风险目前**尚无欧盟判例予以确认**。

---

## 3. ⛔ 否定结果清单（查了但没有的）

⏳ 待 Q2 回报后补全。⭐ Q1 部分已确立的否定项见 §1。

### 3.4 ⚠️ 反向证据：厂商侧合规能力已填掉「必须私域部署」的必要性

⛔ **这一节是本台账对论文最不利、但必须写进去的部分。** ⛔ 「必须私域部署」这个论断的隐含前提是「用第三方 LLM API 就等于失去数据控制」——⛔ 而这个前提在 2023 年之后**已不成立**：

| 事实 | 逐字/要点 | 来源 | 核验状态 |
| :-- | :-- | :-- | :-- |
| API 默认不用于训练 | OpenAI 声明默认不使用 API 平台的输入与输出训练或改进模型，⭐ 需显式 opt-in 才参与 | [openai.com/enterprise-privacy](https://openai.com/enterprise-privacy/) | 🟡（官方页，⛔ 未逐字锚定条款号） |
| 默认保留 30 天 | API 输入输出最多保留 30 天用于滥用监测，⭐ 之后删除（法律要求除外） | [platform 数据控制指南](https://developers.openai.com/api/docs/guides/your-data) | 🟡 |
| Zero Data Retention | ⭐ 合格客户可申请 ZDR，⛔ 启用后 `store` 参数恒为 false，⭐ 输入输出不落日志、不留存 | 同上 | 🟡 |
| 欧洲数据驻留 | ⭐ 可在 API dashboard 创建 Europe 区域 Project，⭐ 请求在区域内处理且 zero data retention | [openai.com 数据驻留公告](https://openai.com/index/introducing-data-residency-in-europe/) | 🟡 |

⛔ **对 story 的直接后果**：审稿人只需引用上面任意一条，⛔ 就能问「既然有 ZDR + 区域驻留 + 默认不训练，⛔ 为什么非得自建？」⛔ 论文**必须预先回答这个问题**，⛔ 否则动机层会被一击打穿。⭐ 可用的回答方向有三条，⛔ 但都不是「合规强制」：**(i) 合规**成本**而非合规**禁止**（ZDR 需逐案审批、需签附加条款、并非默认可得）；**(ii) 特定前置认定成立时**（国家秘密 / CUI / 重要数据）厂商侧措施不足以豁免（⭐ 此点须由 §2 的条款支撑）；**(iii) 成本与可复现性**（自建模型可版本冻结、可离线复现，⛔ 而 hosted API 存在 provider drift）。⭐ **第 (iii) 条与本仓库既有实践直接吻合，⛔ 且不需要任何法规依据**——⭐ 建议作为主论证。

### 3.5 🟡 产业先例（非成文依据，⛔ 证据等级低）

⭐ 三星 2023-05 因员工把源代码输入 ChatGPT 而临时禁用生成式 AI，⛔ 是被广泛引用的产业先例。⛔ **但它有三个硬伤，⛔ 引用时必须自陈**：(1) ⛔ 来源是新闻报道（Bloomberg 首发）而非成文规范，⛔ 属 🟡；(2) ⛔ 三星明确表示该禁令是**临时**措施，⛔ 并在研究「安全使用生成式 AI 的环境」；(3) ⛔ 事发于 2023 年 5 月，⛔ 早于 ZDR / 企业版数据控制普及，⛔ 时效性存疑。⛔ **不得把它写成「工业界普遍禁止」**，⛔ 只能写成「有企业曾因此临时限制」。来源：[Bloomberg](https://www.bloomberg.com/news/articles/2023-05-02/samsung-bans-chatgpt-and-other-generative-ai-use-by-staff-after-leak)、[TechCrunch](https://techcrunch.com/2023/05/02/samsung-bans-use-of-generative-ai-tools-like-chatgpt-after-april-internal-data-leak/)。

---

## 4. 检索过程（可复现）

### 4.1 Q1 检索链路

| 项 | 内容 |
| :-- | :-- |
| 时间窗 | 2026-08-13 |
| 主入口 | `iso.org` 目录页（⛔ **全部返回 HTTP 403**，⛔ 见 §5）；⭐ 改用 ISO / IEC 授权发行方 iTeh Standards 的免费 preview PDF（`cdn.standards.iteh.ai/samples/<id>/<hash>/<NAME>.pdf`） |
| 发现方式 | WebSearch 定位 preview URL → `curl` 下载 → `python -m tools.pdf_extractor -m text` 提取 → `grep` 检索 |
| 实际下载并提取的 preview | ISO 26262-2:2018、ISO 26262-4:2018、ISO 26262-6:2018、ISO 26262-8:2018、ISO/SAE 21434:2021、IEC 61508-1:2010、IEC 61508-3:2010、ISO/IEC TR 5469:2024（⭐ 共 8 份） |
| 检索关键词 | `confidential` / `proprietar` / `third part` / `data protect` / `security` / `disclos` / `supplier` / `outsourc` / `malevolent` / `unauthoris` / `cyber` |
| 命中数 | ⛔ 保密 / 数据外发方向：**0 条规范性条款**；⭐ 安全防护方向：IEC 61508-1 §1.2 k)/l)/m) 共 3 条，⛔ **均为排除性表述**；⭐ 工具钩子方向：ISO 26262-8 Clause 11、IEC 61508-3 §7.4.4 + Table A.3 |

⭐ **可复现命令**（以 ISO 26262-8 为例）：

```bash
curl -sSL -A "Mozilla/5.0" -o /tmp/iso26262-8.pdf \
  "https://cdn.standards.iteh.ai/samples/68390/8b6b8ddbf06b436e8ac60f72f63c17d9/ISO-26262-8-2018.pdf"
python -m tools.pdf_extractor -i /tmp/iso26262-8.pdf -o /tmp/iso26262-8.txt -m text
grep -ni "confidential\|proprietar\|third part\|data protect\|disclos" /tmp/iso26262-8.txt
```

### 4.2 Q2 检索链路

⏳ 待并行分组回报后补全。

---

## 5. 待核验项与访问受限记录

| 对象 | 问题 | 处理 |
| :-- | :-- | :-- |
| `www.iso.org/standard/*.html` | ⛔ **HTTP 403 Forbidden**（⛔ 多次尝试，⛔ 疑为 WAF / bot 拦截） | ⭐ 改用授权发行方 preview PDF；⛔ 按仓库规范，⛔ 记为「入口已定位 / 访问异常」，⛔ **不据此断言事实不存在** |
| `webstore.ansi.org/preview-pages/...` | ⛔ **HTTP 403**（⛔ 返回 HTML 而非 PDF） | ⛔ 放弃该入口 |
| ISO 26262-8:2018 §5.4.3 正文（DIA 内容清单） | ⛔ 落在 preview 范围外 | 🔴，⛔ 不据记忆补写 |
| ISO 26262-8:2018 Clause 11 正文（工具置信度 / TCL） | ⛔ 落在 preview 范围外 | 🔴，⛔ 仅目录标题 🟢 |
| ISO/SAE 21434:2021 Clause 7 正文与 Annex C（CIA 内容） | ⛔ 落在 preview 范围外 | 🔴，⛔ 仅 Introduction 的目录说明 🟢 |
| ISO/IEC TR 5469:2024 §10.3.5 正文 | ⛔ 落在 preview 范围外 | 🔴，⛔ **不据标题推断内容** |
| IEC 61508-3 全文词频 | ⛔ preview 仅 15 页 | ⛔ 结论只表述为「**完整目录**中无此类条款」，⛔ 不表述为「全文无此词」 |
| prEN IEC 61508-1:2025 | ⭐ 第三版制定中，⛔ 未核验其是否新增安全防护条款 | ⏳ 待核验 |
| DO-178C / DO-330 / EN 50128 / EN 50716 / IEC 62304 | ⏳ 并行核验中 | ⏳ |
| Q2 全族 | ⏳ 并行核验中 | ⏳ |
