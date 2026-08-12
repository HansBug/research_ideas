# 法规与标准台账（N1a · 法规标准族）

> ⭐ 本文件回答两个问题：**Q1** 功能安全标准里到底有没有约束「把需求文档 / 设计模型交给外部第三方处理」的条款；**Q2** 若没有，真正可引的成文依据在哪一族。⛔ 本文件只放证据与逐条判定，⛔ 结论汇总回 [SUMMARY.md](./SUMMARY.md)。

**核验状态口径**：`🟢 官方全文已核验`（引文来自官方或授权发行方的公开正文 / 免费 preview 正文范围内）/ `🟡 二手佐证`（注明出处）/ `🔴 付费墙未核验`（条款存在但正文不在免费范围）/ `⚪ 查无此条`。

⚠️ **关于 ISO / IEC preview 的证据等级说明**：ISO 与 IEC 通过授权发行方（iTeh Standards / SIST）发布**免费 preview PDF**，其中包含**完整目录、完整 Scope、以及正文前若干页的规范性条文**，页面带 `iTeh STANDARD PREVIEW` 水印且标注 ISO/IEC 版权。⭐ 本台账中凡标 🟢 的 ISO / IEC 引文，**均逐字取自这些 preview PDF 的正文范围**，并附 preview URL；⛔ 凡条文落在 preview 范围之外的（如 ISO 26262-8 的 5.4.3、Clause 11 正文），一律标 🔴，⛔ **不据记忆补写**。

---

## 0. 一句话结论

⛔ **Q1 = 无。** 在本轮覆盖的**九本**功能安全 / 软件保证标准中，**没有任何一条条款约束「把需求文档 / 设计模型 / 工作产品交给外部第三方处理」**；⭐ 其中 **IEC 61508-1:2010 §1.2 m) 用逐字条文把「安全策略与安全服务」明确排除出自身范围**，⭐ **ISO/SAE 21434:2021 §1 Scope 用逐字条文声明「本文件不规定与网络安全相关的具体技术或解决方案」**——⭐ 加上 **EN 50716:2023 Introduction 出现的、与 IEC 61508-1 §1.2 m) 措辞高度重合的同一句排除**——⭐ **三处彼此独立的自陈排除**把 Q1 的否定结论从「查不到」升级为「**这一族在设计上就不管这件事**」。⚠️ **ISO 26262 Part 8 的 DIA 机制确实是「责任划分」而非「数据驻留」**，⭐ 先验判断被逐字条文证实；⛔ 且 §5.1 c) 的目标恰恰是「identify the **work products to be exchanged**」——⛔ **它是共享制品的授权机制，不是禁止外发的依据**，⛔ 反向引用会被审稿人一击打穿。

⭐ **任务清单上的标准已全部覆盖**：⭐ IEC 61508-1、IEC 61508-3、ISO 26262-2、ISO 26262-6、ISO 26262-8、ISO/SAE 21434、IEC 62304、DO-178C / DO-330、EN 50128 / EN 50716，⭐ 另加 4 份邻接文件（⭐ ISO/IEC TR 5469、IEC 62443-4-1、IEC 81001-5-1、EU 2022/1645 Part-IS）。⚠️ ⛔ **但证据强度限定必须随结论带走**：⭐ 可断言的是「**clause 级 / annex 级**不存在保密条款」，⛔ **不能**断言深层编号里的单条要求也不存在（⭐ 详见 §1.9）。⭐ 邻接文件中有**三条正面命中**：① ⭐ **IEC 62443-4-1:2018 §5.9「SM-7: Development environment security」**（⭐ 顺着 IEC 61508-1 §1.2 k) 的 NOTE 5 官方指引找到，⭐ Scope 逐字锚定「industrial automation and control systems」的**开发者**，⛔ 条文 🔴，⭐ 见 §1.5b）；② ⭐ **IEC 81001-5-1:2021 §5.1.2「Development environment SECURITY」+ §4.1.5「SOFTWARE ITEMS from third-party suppliers」**（⛔ 条文 🔴，⭐ 见 §2.7e）；③ ⭐⭐ **EU 2022/1645（Part-IS）**（⭐ 2025-10-16 起适用，🟢 全文已核验，⭐ 见 §2.7c）——⭐ 其 **IS.D.OR.200(a)(13)** 是本台账中**唯一一条明文规定 confidentiality 义务的强制条文**。⚠️⚠️ ⛔ 另有一条**对本研究不利**的监管动向必须单独看：⭐ **EASA NPA 2025-07(A)** 逐字要求「**avoiding the double development and verification with AI tools**」，⛔ 直指 project_1→2/3 的闭环形态（⭐ 见 §2.7d）。

⭐ **Q2 = 有，⭐ 而且比预期强——⛔ 但没有一条能推出「必须私域部署」。** ⭐ **确实存在直接管到「把制品交给第三方处理」这个动作的成文条款**，⭐ 且可核验到条款级：⭐ 美国 **NIST SP 800-171 Rev 2 §3.1.20** 的 DISCUSSION 逐字点名 SaaS 云服务；⭐ **DFARS 252.204-7012 (a)** 的 `Technical information` 定义逐字包含 "specifications, standards… engineering data… data sets"，⭐ 即**需求文档与设计模型本身**；⭐ 欧盟 **VDA ISA2027** 逐字把 "AI tools (e.g., AI chatbots, AI agents)" 定义为受控外部 IT 服务；⭐ 中国**保密法第三十一条(三)**禁止用非涉密系统处理国家秘密。

⛔ **但这些条款的形态高度一致：⛔ 它们是「条件性允许 + 合规义务」，⛔ 不是「禁止」。** ⛔ 而且**三层论证强度必须分清**（详见 §0b）：(a)「不能用**未获授权的**商用 LLM 端点」**可立**；(b)「不能用任何第三方公有云 LLM」**仅涉密场景可立**；(c)「必须私域部署」⛔ **明确证伪**——⛔ 国防部自己在 GenAI.mil 上用 Gemini / Grok / ChatGPT 处理 CUI（IL5），⛔ Azure OpenAI 已达 IL6/Top Secret，⛔ 中国政务指引要求「充分利用互联网算力和模型资源」，⛔ 且涉密场景下**私域部署本身也不合规**。

⭐ **档位建议：B。** ⛔ 不是 A——⛔ A 要求「≥1 条成文、可引、且明确覆盖设计阶段制品交给第三方处理」**且** SE 文献里 ≥3 篇承重使用；⭐ 前半条**已满足**（⭐ NIST 3.1.20 / DFARS 7012 / VDA ISA2027 都够格），⛔ 但**后半条不在本路职责内**（⛔ 由 se_motivation_survey 一路判定），⛔ 且这些依据**都无法支撑论文实际想说的那句话（必须私域部署）**。⛔ 也不是 C——⛔ 依据确实存在且可引。⭐ **B 的含义在此处很具体：⭐ 可以写成 motivation，⛔ 但不得让任何 claim 依赖它，⛔ 且必须自陈证据等级与适用边界。**

⚠️⚠️ ⛔ **本路最重要的一条建议**：⛔ 与其把动机挂在法规上（⛔ 挂不住，⛔ 且反证遍地），⭐ 不如挂在**可复现性**上——⭐ hosted API 存在 provider drift，⛔ 而论文实验需要版本冻结与离线复现。⭐ 这条**不需要任何法规依据**，⭐ 与本仓库既有实践直接吻合，⭐ 且审稿人无法用「可是 Azure OpenAI 有 IL6」来反驳。

---

## 0b. ⭐⭐ 三层论证强度裁定（⭐ 本台账的核心产出）

⛔ **「必须私域部署」这句话必须拆成三层分别裁定，⛔ 混谈是本轮最容易犯、⛔ 也最致命的错误。**

| 层次 | 能否立住 | 依据与边界 |
| :-: | :-- | :-- |
| **(a) 不能用**未获相应授权的**公有商用 LLM 端点** | ✅ **能立住，⭐ 且有多条彼此独立的路径**（⭐ 命中任一即可）。⚠️ ⛔ **但措辞必须带「未获授权」限定**——⛔ 不能写成「公有云 SOTA 模型一律不能用」：⛔ OpenAI `ChatGPT Enterprise and API Platform` 已于 2026-01-09 取得 FedRAMP 20x Class C（≡ Moderate） | ① ⭐ **中国等保**（GB/T 22239-2019 §8.2.4.5 a) / §9.2.4.5 a)）：⭐ 三级及以上时「云服务客户数据」须存境内——⭐ **唯一不需要任何前置认定的路径**，⭐ 而工业控制系统定级三级极常见（🟡 需人工复核条款号）；② ⭐ **美国国防**（DFARS 252.204-7012 (b)(2)(ii)(D) + NIST 800-171 §3.1.20/§3.1.3）：⭐ CDI 须 FedRAMP Moderate 等效，⛔ 普通商用端点不满足（🟢）；③ ⭐ **美国出口管制**（ITAR §120.54(b)(1)(ii)、EAR §734.18(b)(ii)）：⭐ 加密安全港结构性不可满足（🟢）；④ ⭐ **欧盟汽车业**（VDA ISA 1.3.3 + 5.1.2 very high + ISA2027 6.1.1）：⭐ 审批 + 内容级加密 + 第三方审计（🟢）；⑤ ⭐ **中国保密**（保密法第二十九条第二款、第三十一条(三)）：⛔ 仅涉密场景（🟢） |
| **(b) 不能用任何第三方公有云 LLM（⭐ 含境内 / 含政府云）** | ⚠️ **仅在涉密场景立住，⛔ 普通商业场景立不住** | ✅ ⭐ 立得住：⭐ 中国保密法第三十一条(三)（⭐ 管**系统性质**而非地理位置）+ 军工保密资质管理办法第六条（⭐ 受托方须持证）。⛔ 立不住：⛔ 等保 §8.2.6.1 **明文容纳**第三方云服务商（⭐ 选型 + SLA + 保密协议）；⛔ 工信部办法第二十三条对委托处理要求的是**核验与签约**而非禁止；⛔ DFARS 的解是**用已授权政府云**；⛔ Anthropic 官方称 **ITAR 数据可经 Bedrock 处理** |
| **(c) 必须私域部署** | ❌ **立不住，⛔ 无任何成文依据** | ⛔ 没有任何一条现行法规或标准要求「私域部署」。🔻 ⛔ 反向证据更强：⛔ 中国政务指引（⭐ 比工业更敏感的场景）明确要求用「**已完成网信部门备案的模型产品和服务**」并「**充分利用互联网算力和模型资源**」；⛔ Azure OpenAI 已达 IL6 / Top Secret，⛔ Bedrock 已达 IL5；⛔ OpenAI 提供 ZDR + 区域驻留。⚠️⚠️ ⛔ **且存在一个反直觉的致命反例**：⛔ 若制品已定密为国家秘密，⛔ 企业自建的普通私有服务器**仍是「非涉密信息系统」**，⛔ 照样违反保密法第三十一条(三)——⛔ **涉密场景下「私域部署」本身也不合规**，⭐ 必须是经保密测评审查合格的涉密信息系统 |

⛔ **给论文的落笔建议**：⭐ 把主张收缩到 **(a)**；⭐ **(b)** 必须加「涉密（军工/航天）分支」限定词；⛔ **(c) 放弃法规论证路径**，⭐ 改用**非法规论据**——⭐ 可控性、可审计性、**可复现性**（⭐ hosted API 存在 provider drift，⛔ 而论文实验需要版本冻结与离线复现）。⭐ 后者与本仓库既有实践直接吻合，⭐ 且**不需要任何法规依据**，⭐ 建议作为主论证。

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
| **IEC 62443-4-1** | 2018 | **§5.9** | `SM-7: Development environment security`（⭐ 目录标题；⛔ 条文付费墙） | ⭐ **唯一邻接命中**（⛔ 条文未核验） | [preview PDF](https://cdn.standards.iteh.ai/samples/21445/5d9b618cf732432b83b4e17e0e7b24cf/IEC-62443-4-1-2018.pdf) | 🟢 目录 / 🔴 条文 |
| IEC 62443-4-1 | 2018 | §1 Scope | "…process requirements for the secure development of **products used in industrial automation and control systems**… These requirements apply to the **developer and maintainer** of the product, but not to the integrator or user…" | ⭐ 域匹配度最高 | 同上 | 🟢 |
| DO-178C / DO-330 | 2011 | 完整目录 Sec 1-12 + Annex A/B | 目录中**无**任何 security / confidentiality / data protection 条款；⭐ FAA 对照文档 `security` 0 命中 | ⛔ 不覆盖 | [FAA Differences Tool](https://www.faa.gov/sites/faa.gov/files/aircraft/air_cert/design_approvals/air_software/differences_tool.pdf) | 🟡 |
| DO-178C | 2011 | §7.2.7 | `Archive, Retrieval, and Release`（⚠️ ⛔ **不是**「Protection against Unauthorized Changes」） | ⛔ 不覆盖（⭐ 完整性，⛔ 非保密性） | 同上 | 🟡 |
| DO-356A | 2018 | 官方描述 | "This document **does not provide guidelines concerning the structure of an individual organization or how the responsibilities for certification activities are divided.**" | ⛔ **明确不覆盖（自陈）** | [rtca.org/security](https://www.rtca.org/security/) | 🟢 |
| **EN 50716** | 2023 | **Introduction** | "This document **does not specify the requirements for the development, implementation, maintenance and/or operation of security policies or security services** needed to meet cybersecurity requirements…" | ⛔ **明确排除（第三处自陈）** | [NSAI 官方样张](https://i2.saiglobal.com/mpc2v/preview/1412600409546.pdf?sku=1348800_SAIG_NSAI_NSAI_3361513) | 🟢 |
| EN 50128 | 2011 | §1.8 | "This European Standard is **not intended to address commercial issues**. These should be addressed as an essential part of any contractual agreement." | ⛔ 不覆盖 | [SIST 官方样张](https://cdn.standards.iteh.ai/samples/20508/f059ecdf1111415dbf91a13af058154c/SIST-EN-50128-2011.pdf) | 🟢 |
| IEC 62304 | 2006 (+A1:2015) | 完整目录 Clause 1-9 | 目录中**无**任何保密 / 数据保护条款；⭐ Clause 8 只有 8.1/8.2/8.3，⛔ 无第四子条 | ⛔ 不覆盖 | [preview PDF](https://cdn.standards.iteh.ai/samples/11630/3af7c2dc38c8489781331a49a001b0ff/IEC-62304-2006.pdf) | 🟢 |
| IEC 62304 | 2006 | **Introduction** | "This standard **does not specify an organizational structure for the MANUFACTURER or which part of the organization is to perform which PROCESS, ACTIVITY, or TASK.**" | ⛔ **明确不覆盖（自陈免责）** | 同上 | 🟢 |
| **EU 2022/1645**（Part-IS） | 2022，⭐ **2025-10-16 起适用** | **IS.D.OR.200(a)(13)** | "…**protects the confidentiality of any information that the organisation may have received from other organisations**, according to its level of sensitivity." | ⭐⭐ **唯一明文 confidentiality 强制条文** | [CELEX:32022R1645](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R1645) | 🟢 |
| IEC 81001-5-1 | 2021 | **§5.1.2** | `Development environment SECURITY` | ⭐ 间接相关 | [IEC 官方 preview](https://webstore.iec.ch/en/iec_catalog/product/preview/?id=L3B1Yi9wZGYvcHJldmlldy9pbmZvX2llYzgxMDAxLTUtMXtlZDEuMH1iLnBkZg%3D%3D) | 🟢 标题 / 🔴 正文 |

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

### 1.5b IEC 62443-4-1:2018（工控产品安全开发生命周期）· ⭐⭐ **Q1 族唯一的邻接命中，且是顺着 61508 的官方指引找到的**

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

### 1.6 IEC 62304（医疗器械软件）· 结论：⛔ **无**

⭐ **本节由主 session 在并行分组未回报后亲自补做。** IEC 62304:2006 的**完整目录**（⭐ Clause 1 Scope / 2 Normative references / 3 Terms and definitions / 4 General requirements / 5 Software development PROCESS / 6 Software maintenance PROCESS / 7 Software RISK MANAGEMENT PROCESS / 8 Software configuration management PROCESS / 9 Software problem resolution PROCESS + Annexes）**不含任何保密、数据保护或第三方数据处理条款**。⭐ 在 preview 覆盖范围内对 `confidential` / `third part` / `outsourc` / `disclos` / `data protect` 五词检索，⭐ 唯一命中是术语定义中的 "that person or by a third party on that person's behalf"（⭐ 属 `manufacturer` 定义用语），⛔ **与数据外发无关**。

⭐ **工具 / 第三方钩子**：⭐ SOUP（Software of Unknown Provenance）机制位于 Clause 5.3（Software ARCHITECTURAL design）项下，⛔ 具体子条编号落在 preview 之外（🔴）。⚠️ ⛔ 但可确认的是：⭐ SOUP 机制的规制对象是**引入的第三方软件组件的已知缺陷与性能**，⛔ **不是把自己的数据交给第三方**——⛔ 二者方向相反，⛔ 不得混引。来源：[IEC 62304:2006 preview PDF](https://cdn.standards.iteh.ai/samples/11630/3af7c2dc38c8489781331a49a001b0ff/IEC-62304-2006.pdf)。

### 1.7 DO-178C / DO-330（航空）· 结论：⛔ **无**

⭐ **完整目录逐条核对**：DO-178C（2011-12-13）Section 1-12 + Annex A/B 中**无任何 section 标题涉及 security / confidentiality / data protection**。⭐ 对 FAA 官方 138 页《DO-178B/C Differences Tool》做机械检索：`security` **0**、`confidential` **0**、`cloud` **0**、`unauthorized` **0**、`third part` **0**、`disclos` **0**、`proprietar` **0**。来源：[FAA/AVS DO-178B/C Differences Tool](https://www.faa.gov/sites/faa.gov/files/aircraft/air_cert/design_approvals/air_software/differences_tool.pdf)（🟡 官方 FAA 文档复制 DO-178C 目录）。

⚠️⚠️ ⛔ **一处必须纠正的编号，⛔ 且它正是任务点名的那类误读**：⛔ **DO-178C §7.2.7 不是「Protection against Unauthorized Changes」，⭐ 而是「Archive, Retrieval, and Release」。** ⭐ Section 7.2 的完整子条为：`7.2.1 Configuration Identification` / `7.2.2 Baselines and Traceability` / `7.2.3 Problem Reporting, Tracking, and Corrective Action` / `7.2.4 Change Control` / `7.2.5 Change Review` / `7.2.6 Configuration Status Accounting` / `7.2.7 Archive, Retrieval, and Release`。⭐「protection against unauthorized changes」是 Table 7-1 的行标签，⭐ 指向 **§7.2.7.b(1)**（🟡 二手：[AdaCore DO-178C 变更说明 §4.1.2](https://www.adacore.com/uploads/books/DO178C-ED12C-Changes_and_Improvements-Sep2012.pdf)）。⛔ **注意措辞是 unauthorized *changes*（修改），⛔ 不是 disclosure（泄露）**——⛔ 它是**完整性**条款，⛔ 与保密无关。

⚠️ ⛔ **附一条方法论警告**：⛔ 核验过程中，⛔ 搜索引擎摘要**凭空编造**了「7.2.7 Protection / 7.2.8 Media Selection / 7.2.9 Release / 7.2.10 Data Retention」这一**并不存在**的条款结构来迎合提问。⛔ 这正是本仓库「机械代理只能定位不能裁定」的活体案例：⛔ **凡 DO 系条款号，⛔ 一律不得采信搜索摘要。**

⭐ **工具钩子（本节的正面价值）**：⭐ DO-178C **§12.2**（`12.2.1 Determining if Tool Qualification is Needed` / `12.2.2 Determining the Tool Qualification Level` / `12.2.3 Tool Qualification Process`）+ **Table 12-1**（TQL 矩阵）。⭐ §12.2.2 三准则逐字（🟡 两独立来源一致）：「a. Criteria 1: A tool whose output is part of the airborne software and thus could insert an error. b. Criteria 2: A tool that automates verification process(es) and thus could fail to detect an error… c. Criteria 3: A tool that, within the scope of its intended use, could fail to detect an error.」⛔ **三条准则只问「工具会不会引入或漏检错误」，⛔ 完全不问工具跑在哪、⛔ 数据发给谁。**

⭐ **DO-330** 官方摘要：「a tool is a computer program… used to help develop, transform, test, analyze, produce or modify another program… This document explains the process and objectives for qualifying tools.」（🟢 [my.rtca.org DO-330](https://my.rtca.org/productdetails?id=a1B36000001IcfkEAC)，⛔ 条文 🔴）。⭐ 对 DO-330 objective 逐条枚举表（Eclipse/Validas 41 页）扫 `cloud` / `confidential` / `third party` / `remote` / `premise` → **全 0 命中**。⚠️ ⛔ DO-330 §11.2.2 的 "Tool operational environment" 指的是**技术执行环境**（🟡 AdaCore 举例为 "upgrade of the workstation"），⛔ 判据是 equivalence，⛔ **不是 ownership 或 locality**——⛔ 不得误读为「部署位置」。

⭐ **DO-326A / ED-202A** 官方摘要：保护对象是「**intentional unauthorized electronic interaction to aircraft safety**」——⛔ 即**飞机**，⛔ 不是研发环境。⭐ **DO-356A** 更有一句自我免责（🟢 [rtca.org/security](https://www.rtca.org/security/)）：「This document **does not provide guidelines concerning the structure of an individual organization or how the responsibilities for certification activities are divided.** No such guidance should be inferred」。

### 1.8 EN 50128 / EN 50716（铁路）· 结论：⛔ **无，⭐ 且是第三处「标准自陈排除」**

⚠️ **版本事实（🟢 官方正文已核验）**：**EN 50716:2023**（2023-10-30，dop 2024-10-30，**dow 2026-10-30**）封面逐字：「Supersedes EN 50128:2011; EN 50128:2011/AC:2014; EN 50657:2017; EN 50128:2011/A1:2020; EN 50128:2011/A2:2020; EN 50657:2017/A1:2023」。⛔ **不得继续把 EN 50128 当作现行唯一标准。** ⭐ 新标准**刻意保留原章节编号**。

⭐⭐ **EN 50716:2023 Introduction 的逐字排除声明**（🟢 官方样张已核验）：

> "This document **does not specify the requirements for the development, implementation, maintenance and/or operation of security policies or security services** needed to meet cybersecurity requirements that may be needed by the safety-related system. Cyber attacks can affect not only the operation but also the functional safety of a system. For cybersecurity, appropriate standards should be applied."

⭐ **注意这句与 IEC 61508-1:2010 §1.2 m) 的措辞高度重合**——⭐ 这不是巧合，⛔ 而是功能安全标准族的**共同自我定位**：⛔ 它们**系统性地把 security 排除在自身范围之外**。⭐ 这使 Q1 的否定结论从「三本各自没有」上升为「**这一族在设计上就不管这件事**」，⭐ 是本台账可写进论文的最强结构性论断。

⭐ **EN 50128:2011 §1.8** 另有一句：「This European Standard is **not intended to address commercial issues**. These should be addressed as an essential part of any contractual agreement.」——⛔ 把商务与合同事项整体推给合同。

⭐ **工具钩子**：⭐ 两版**同号同名**的 **§6.7「Support tools and languages」** + **Table 1「Relation between tool class and applicable subclauses」**；⭐ 预存软件另见 §7.3.4.7 与 §6.5.4.16（⭐ §1.5 逐字：「for tools in **6.7** are fulfilled」）。⭐ 对 16 页官方样张（⭐ 封面 + 完整目录 + Foreword + Introduction + Clause 1 + Clause 2）扫 `confidential` / `data protection` / `third part` / `supplier` / `subcontract` / `proprietar` / `non-disclosure` / `privacy` → **0 命中**（⭐ `security` 仅命中上述**排除声明**）。来源：[SIST EN 50128:2011 preview](https://cdn.standards.iteh.ai/samples/20508/f059ecdf1111415dbf91a13af058154c/SIST-EN-50128-2011.pdf)、[NSAI I.S. EN 50716:2023 样张](https://i2.saiglobal.com/mpc2v/preview/1412600409546.pdf?sku=1348800_SAIG_NSAI_NSAI_3361513)。

### 1.9 ⚠️ Q1 覆盖边界的一条诚实限定（⛔ 必须随结论一起带走）

⛔ **所有免费 preview 只覆盖「封面 + 完整目录 + Scope + 部分定义 + 前若干页正文」。** ⭐ 因此可断言的是「**clause 级 / annex 级**不存在保密条款」；⛔ **不能**断言埋在 `5.1.x` / `6.5.4.x` 这类深层编号里的**单条要求**也不存在。⛔ 以下条文**均未直接核验**：DO-178C §7.2.7 正文、IEC 62304 SOUP 子条、IEC 81001-5-1 §5.1.2 正文、ISO 26262-8 §5.4.3、ISO/SAE 21434 Clause 7 正文。

## 2. Q2 · 其余各族（逐族）

### 2.1 出口管制 · 美国 ITAR / EAR · ⭐⭐⭐ **论证最锋利的一条（⛔ 适用面最窄）：⭐ 加密安全港在 LLM 推理场景下结构性不可满足**

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

⚠️⚠️ ⛔ **必须紧跟一条反向事实，⛔ 否则上面的论证会被一击打穿：⛔ 加密安全港不可满足 ≠ 第三方云不可用。**

⛔ 安全港只是**若干合规路径之一**。⛔ 另一条路径是让「release to a foreign person」这件事**根本不发生**——⭐ 即基础设施位于美国境内、⭐ 运维人员限于美国人。⭐ AWS GovCloud 正是这样的环境。⭐ 而 **Anthropic 官方支持页逐字写道：「ITAR data can only be processed in Claude via AWS Bedrock, which is IL5 accredited.」**（来源：[Anthropic Public Sector FAQs](https://support.claude.com/en/articles/13756069-public-sector-faqs)，🟢 已核验）——⛔ **即受 ITAR 管制的数据在合规环境下是可以交给第三方托管 LLM 处理的。**

⛔ **因此 §2.1 的正确净结论是**：⭐ ITAR / EAR **排除了普通商用 LLM 端点**（⛔ 因为既不满足加密安全港，⛔ 也无法保证不向外国人释放），⛔ **但没有排除第三方托管 LLM 服务本身**，⛔ **更推不出「必须私域部署」**。⭐ 加密安全港的存在反而说明立法者**原则上允许**把受控技术数据放到外部环境——⛔ 只要拿不到明文；⭐ 这也是机密计算 / 同态推理的立法空间。

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
| 禁止出口限制出口技术目录（商务部/科技部 2023 年第 57 号） | ⭐ **通用**软件类条目 | `083915X 计算机应用技术`、`086502X 计算机通用软件编制技术`（⭐ 巨型机 / 并行计算）、`086501X 信息处理技术`（⭐ 中文与少数民族语言处理、汉字识别、CAD 图纸档案管理、个性化推荐）、`206503X 基础软件安全增强技术` | ⛔ **不覆盖**：⭐ 机械复核「工业控制」0、「嵌入式」0、「状态机」0、「工业软件」0 —— ⛔ **无通用工业控制软件条目** | [目录全文 PDF](https://www.most.gov.cn/tztg/202312/W020231221620858841394.pdf) | 🟢 |
| ⭐ **同上，限制出口部分 序号 71，编号 `203912X` 无人机技术** | ⭐ **第 5 项** | "5.**无人机飞行控制系统（自主导航、路径及避障规划等相关的算法及软件）**" | ⭐⭐ **覆盖该细分领域**：⭐ 管制客体**正是控制系统的算法与软件** | 同上 | 🟢 |

⚠️ ⛔ **一处跨来源冲突已由主 session 亲自回原文裁定（依 §3.8）。** ⛔ 两路并行调研对同一份目录给出相反读数：⛔ 一路称「全文通读，⛔ 涉软条目均不覆盖」，⭐ 另一路称「序号 71 含无人机飞控软件」。⭐ 主 session 下载官方 PDF（30 页）并 `grep` 核对：⭐ **后者正确**。⭐ 第 71 条位于**限制出口部分**（⭐ 该部分自文本第 226 行起，⭐ 条目在第 952-965 行），⭐ 第 5 项逐字为「无人机飞行控制系统（自主导航、路径及避障规划等相关的算法及软件）」。⛔ **前一路的错误来自检索词选择**：⛔ 它只搜了「工业控制 / 嵌入式 / 状态机 / 工业软件」等通用词，⛔ 命中 0 即断言不存在，⛔ 而目录是按**领域**（无人机 / 航天 / 激光）而非按**技术形态**编排的。⭐ **准确表述应是**：⛔ 目录中**没有通用的工业控制软件条目**，⭐ **但存在以控制系统算法与软件为客体的领域性条目**。⛔ **不得沿用「目录里完全没有控制软件」这个说法。**
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

### 2.2b 数据出境 / 数据主权 · 中国部分 · 结论：⛔ **主轴是「不出境」，⛔ 不是「不出企业」**

⚠️ ⛔ **先纠三处条号错误（⛔ 任务描述与常见二手资料均沿用了旧条号，⛔ 论文若照抄会被当场抓住）**：

| 常见说法 | ⭐ 实际 |
| :-- | :-- |
| 《网络安全法》第三十七条（CIIO 境内存储） | ⛔ **已不是第三十七条。** ⭐ 网安法经 2025-10-28 修正、**2026-01-01 施行**，⭐ 境内存储条款现为**第三十九条**；⭐ 新第三十七条改为「采购网络产品服务的国家安全审查」 |
| 《保密法实施条例》国务院令第 788 号 | ⛔ 实为**国务院令第 786 号**（2024-07-10 公布，2024-09-01 施行） |
| 《武器装备科研生产单位保密资格审查认证管理办法》 | ⛔ 现行版本是**《武器装备科研生产单位保密资质管理办法》**（2025-07-01 施行），⭐「资格」已改「资质」，⭐ 三级改两级；⛔ 2016 年国保发〔2016〕15 号同时废止 |

| 法规 | 年份 | 条款 | 逐字原文（节录） | 触发前提 | 是否覆盖 | 来源 | 核验 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 数据安全法 | 2021 | 第三十一条 | 「关键信息基础设施的运营者…重要数据的出境安全管理，适用《中华人民共和国网络安全法》的规定；其他数据处理者…重要数据的出境安全管理办法，由国家网信部门会同国务院有关部门制定。」 | ⚠️ 须先被认定为**重要数据** + 行为构成**出境** | ⛔ 间接相关 | [cac.gov.cn](https://www.cac.gov.cn/2021-06/11/c_1624994566919140.htm) | 🟢 |
| 数据安全法 | 2021 | 第三十六条 | 「非经中华人民共和国主管机关批准，境内的组织、个人不得向外国司法或者执法机构提供存储于中华人民共和国境内的数据。」 | ⛔ 接收方须是**外国司法或执法机构** | ⛔ **不覆盖**（⛔ LLM 厂商不是司法执法机构）。⚠️ 可作「境外厂商受外国法域强制调取」的**风险论证**起点，⛔ 那是论证不是条款 | 同上 | 🟢 |
| 个人信息保护法 | 2021 | 第三十八 / 三十九 / 四十条 | 跨境提供个人信息的三条路径、单独同意、CIIO 境内存储 | ⛔ 文档须含**个人信息** | ⛔ **不覆盖**（⛔ 工程需求文档与状态机模型通常不含个人信息） | [npc.gov.cn](http://www.npc.gov.cn/npc/c2/c30834/202108/t20210820_313088.html) | 🟢 |
| 数据出境安全评估办法（网信办令第 11 号） | 2022 | 第四条 | 「数据处理者向境外提供数据，有下列情形之一的，应当…申报数据出境安全评估：（一）数据处理者向境外提供**重要数据**；…」 | ⚠️ 须先被认定为重要数据 | ⛔ 间接相关 | [cac.gov.cn](https://www.cac.gov.cn/2022-07/07/c_1658811536396503.htm) | 🟢 |
| **促进和规范数据跨境流动规定（网信办令第 16 号）** | 2024 | **第二条** | 「数据处理者应当按照相关规定识别、申报重要数据。**未被相关部门、地区告知或者公开发布为重要数据的，数据处理者不需要作为重要数据申报数据出境安全评估。**」 | 无 | 🔻 ⛔ **对本 story 最强的不利条款** | [cac.gov.cn](https://www.cac.gov.cn/2024-03/22/c_1712776611775634.htm) | 🟢 |
| 同上 | 2024 | **第三条** | 「国际贸易、跨境运输、**学术合作**、**跨国生产制造**和市场营销等活动中收集和产生的数据向境外提供，不包含个人信息或者重要数据的，**免予申报**数据出境安全评估…」 | 无 | 🔻 ⛔ **第二条不利条款**：⛔ 学术合作与跨国制造场景**明文豁免** | 同上 | 🟢 |
| 网络数据安全管理条例（国务院令第 790 号） | 2025-01-01 | 第三十七条 | 「…**但未被相关地区、部门告知或者公开发布为重要数据的，不需要将其作为重要数据申报数据出境安全评估**。」 | 重要数据认定 | ⛔ 间接（⛔ 再次重申豁免） | [国务院令转载](https://www.mee.gov.cn/zcwj/gwywj/202410/t20241003_1087417.shtml) | 🟢 |
| 同上 | 2025 | 第六十二条(四) | 「重要数据，是指特定领域、特定群体、特定区域或者达到一定精度和规模，一旦遭到篡改、破坏、泄露或者非法获取、非法利用，可能**直接**危害国家安全…的数据。」 | — | ⭐ 定义条款；⚠️ 注意「**直接**危害」这一限定 | 同上 | 🟢 |
| **网络安全法（2025 修正）** | ⭐ **2026-01-01 施行** | **第三十九条**（⛔ 原第三十七条） | 「关键信息基础设施的运营者在中华人民共和国境内运营中收集和产生的个人信息和重要数据应当在境内存储。因业务需要，确需向境外提供的，应当…进行安全评估…」 | ⚠️ 主体须是 **CIIO** | ⛔ 间接相关 | [cac.gov.cn 2025 修正版](https://www.cac.gov.cn/2025-12/29/c_1768735112911946.htm) | 🟢 |
| 工业和信息化领域数据安全管理办法（试行） | 2023 | 第八条 | 「…工业和信息化领域数据分类类别包括但不限于**研发数据**、生产运行数据、管理数据、运维数据、业务服务数据等。」 | — | ⭐ **明确把「研发数据」列为分类类别**，⭐ 是工程文档最容易挂上的钩子 | [gov.cn](https://www.gov.cn/zhengce/zhengceku/2022-12/14/content_5731918.htm) | 🟢 |
| 同上 | 2023 | 第二十一条 | 「…重要数据和核心数据，**法律、行政法规有境内存储要求的**，应当在境内存储，确需向境外提供的，应当依法依规进行数据出境安全评估。」 | ⛔ 双重前提：重要/核心数据 **且** 另有法规规定境内存储 | ⛔ 间接相关 | 同上 | 🟢 |
| 同上 | 2023 | 第二十三条 | 「工业和信息化领域数据处理者**委托他人开展数据处理活动的**，应当通过签订合同协议等方式，明确委托方与受托方的数据安全责任和义务。委托处理重要数据和核心数据的，应当对受托方的数据安全保护能力、资质进行核验。」 | ⭐ 委托处理（⭐ 调用第三方 LLM API 属此） | ⭐ **直接覆盖「委托第三方处理」这一动作**——⛔ 但要求的是**核验与签约**，⛔ **不是禁止** | 同上 | 🟢 |
| 汽车数据安全管理若干规定（试行） | 2021 | 第三条 | 重要数据枚举六项（⭐ 地理信息、车辆流量、充电网运行数据、车外视频图像、10 万人以上个人信息等） | — | ⛔ **不覆盖**：⛔ 枚举六项**全部是运行期数据**，⛔ 无一项是设计/需求文档 | [cac.gov.cn](https://www.cac.gov.cn/2021-08/20/c_1631049984897667.htm) | 🟢 |

### 2.3 中国保密法族 · ⭐⭐ **强制力最高，⛔ 覆盖面最窄，⛔ 且含一个反直觉结论**

⭐ **本节保密法四条（第二十九、三十、三十一、六十四条）由主 session 亲自 `curl` npc.gov.cn 官方全文抽取并逐字核对**（⛔ 依 §3.8）。⭐ 该法第六十五条确认「本法自 2024 年 5 月 1 日起施行」。

| 法规 | 年份 | 条款 | 逐字原文 | 触发前提 | 是否覆盖 | 来源 | 核验 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| **保守国家秘密法（2024 第二次修订）** | 2024-05-01 | **第二十九条** | 「禁止非法复制、记录、存储国家秘密。**禁止未按照国家保密规定和标准采取有效保密措施，在互联网及其他公共信息网络或者有线和无线通信中传递国家秘密。**禁止在私人交往和通信中涉及国家秘密。」 | ⚠️ 内容**必须已被依法定密为国家秘密** | ⭐ **直接覆盖** | [npc.gov.cn](http://www.npc.gov.cn/npc/c2/c30834/202402/t20240227_434859.html) | 🟢 |
| 同上 | 2024 | **第三十一条(三)** | 「…任何组织和个人不得有下列行为：…**（三）使用非涉密信息系统、非涉密信息设备存储或者处理国家秘密**；…」 | 同上 | ⭐⭐ **最硬的一条，⭐ 且它管的不是「出境」而是「系统性质」** | 同上 | 🟢 |
| 同上 | 2024 | 第三十条 | 「存储、处理国家秘密的计算机信息系统…按照涉密程度实行分级保护。涉密信息系统应当按照国家保密规定和标准规划、建设、运行、维护…经检查合格后，方可投入使用…」 | 同上 | ⭐ 直接覆盖 | 同上 | 🟢 |
| 同上 | 2024 | 第三十六条 | 「开展涉及国家秘密的数据处理活动…应当符合国家保密规定。…**防范数据汇聚、关联引发的泄密风险。**」 | 同上 | ⭐ 直接覆盖，⭐ 且「汇聚、关联引发泄密」正对应**把大量非密文档喂给同一模型**的场景 | 同上 | 🟢 |
| 同上 | 2024 | **第六十四条** | 「机关、单位对履行职能过程中产生或者获取的**不属于国家秘密但泄露后会造成一定不利影响的事项，适用工作秘密管理办法采取必要的保护措施。工作秘密管理办法另行规定。**」 | 主体须是**机关、单位** | ⚠️ ⛔ **关键中间层，⛔ 但目前是空转条款**——⛔《工作秘密管理办法》**尚未公布** | 同上 | 🟢 |
| 保密法实施条例（国务院令**第 786 号**） | 2024-09-01 | **第四十一条** | 「机关、单位应当加强对互联网使用的保密管理。机关、单位工作人员**使用智能终端产品等应当符合国家保密规定**，不得违反有关规定使用非涉密信息系统、信息设备存储、处理、传输国家秘密。」 | 机关、单位 + 国家秘密 | ⭐ 直接覆盖 | [gov.cn](https://www.gov.cn/zhengce/zhengceku/202407/content_6963934.htm) | 🟢 |
| 同上 | 2024 | 第三十三条 | 「涉密信息系统应当由国家保密行政管理部门设立或者授权的机构进行检测评估，并经设区的市级以上保密行政管理部门审查合格，方可投入使用。」 | 同上 | ⚠️ ⛔ **注意：⛔ 这要求的不是「私域部署」，⭐ 而是「经保密测评审查合格的涉密信息系统」** | 同上 | 🟢 |
| **武器装备科研生产单位保密资质管理办法** | ⭐ **2025-07-01 施行** | 第六条 | 「承担涉密武器装备科研生产任务的企业事业单位应当…取得相应等级的军工保密资质。涉密武器装备科研生产任务应当由具有相应等级的军工保密资质单位承担。**承包单位分包的涉密武器装备科研生产任务涉及国家秘密的，应当由具有相应等级的军工保密资质单位承担。**」 | 承担涉密武器装备任务 | ⭐ **间接但很强**：⭐ 意味着**受托处理方本身必须持证**——⛔ 境外 LLM 厂商永无可能持证 | [gjbmj.gov.cn](https://www.gjbmj.gov.cn/n1/2025/0604/c419767-40494024.html) | 🟢 |

⭐ **三分判定（⛔ 本次调研最容易出错处，⛔ 必须写清）**：⭐ **普通商用工程需求文档**（⭐ 民用汽车 ECU、电梯、微波炉、通用工控）→ **商业秘密**，⛔ 保密法**完全不适用**；⛔ 商业秘密受《反不正当竞争法》保护，⛔ 但那是**权利救济**而非**管制义务**，⛔ 它不禁止你把自己的商业秘密发给谁，⛔ **不能用它论证「不得外发」**。⭐ **机关、单位的非密敏感事项** → **工作秘密**（第六十四条），⛔ 但配套办法**至今未公布**，⛔ 只能作为「立法趋势」，⛔ 不能当现行禁令。⭐ **军工 / 航天 / 涉密武器装备任务下的需求与设计文档** → 依法定密后是**国家秘密**，⭐ 此时本族条款硬性适用。

⚠️⚠️ ⛔ **一个反直觉但必须写进论文的点：私域部署 ≠ 涉密合规。** ⛔ 若制品已被定密为国家秘密，⛔ 企业自建的**普通私有服务器仍然是「非涉密信息系统」**，⛔ 照样违反保密法第三十一条(三)。⭐ 涉密场景要求的是**经保密行政管理部门检测评估、设区的市级以上审查合格的涉密信息系统**（保密法第三十条、实施条例第三十三条），⛔ 这比「私域部署」严格得多，⛔ 且是完全不同的一套标准。⛔ **论文若写「因为涉密所以要私域部署」，⛔ 在保密专业读者眼里是外行话**——⭐ 正确表述是「涉密场景下**连私域部署都不够**，⭐ 必须是通过分级保护测评的涉密信息系统」。

### 2.4 中国网络安全等级保护 · ⭐ **对 (a) 层适用面最宽的一条，⛔ 但核验等级只有 🟡**

| 标准 | 年份 | 条款 | 逐字原文 | 触发前提 | 是否覆盖 | 核验 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| GB/T 22239-2019 | 2019 | **8.2.4.5 a)**（第三级） | 「应确保云服务客户数据、用户个人信息等**存储于中国境内**，如需出境应遵循国家相关规定；」 | ⭐ 定级第三级 + 采用云计算 | ⭐⭐ **直接覆盖**，⭐ 且「客户数据」**不限于个人信息或重要数据**——⭐ 是本轮对普通工程文档**唯一无需前置认定**的境内化要求 | 🟡 |
| GB/T 22239-2019 | 2019 | 8.2.1.1（第三级） | 「应保证云计算基础设施位于中国境内。」 | 同上 | ⭐ 直接覆盖 | 🟡 |
| GB/T 22239-2019 | 2019 | 8.2.7.1（第三级） | 「云计算平台的运维地点应位于中国境内，境外对境内云计算平台实施运维操作应遵循国家相关规定。」 | 同上 | ⭐ 直接覆盖 | 🟡 |
| GB/T 22239-2019 | 2019 | 9.2.1.1 / 9.2.4.5 a) / 9.2.7.1（第四级） | ⭐ 与第三级同义，逐字一致 | 定级第四级 | ⭐ 直接覆盖 | 🟡 |
| GB/T 22239-2019 | 2019 | **8.2.6.1 云服务商选择**（第三级） | 「a) 应选择安全合规的云服务商…；b) 应在服务水平协议中规定云服务的各项服务内容和具体技术指标；…d) 应在服务水平协议中规定服务合约到期时，完整提供云服务客户数据，并承诺相关数据在云计算平台上清除；e) 应与选定的云服务商签署保密协议，要求其不得泄露云服务客户数据。」 | 同上 | 🔻 ⛔ **对 (b)/(c) 层的致命反证**：⛔ 等保三级**明文预设并容纳使用第三方云服务商**，⭐ 路径是**选型 + SLA + 保密协议**，⛔ 不是禁止 | 🟡 |
| 网络安全等级保护条例 | — | — | — | — | ⚪ **查无此法**：⛔ 仅有 2018-06-27 公安部征求意见稿；⭐ 2025 年列入国务院立法工作计划「**预备制定**」，⛔ 至今未出台。⛔ **论文中不得引用为现行法规** | ⚪ |

⛔ **🟡 核验等级说明**：⭐ 官方免费预览入口在 [openstd.samr.gov.cn](https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=BAFB47E8874764186BDB7865E8344DAF)，⛔ 但为 JS 渲染页面，⛔ `curl` 不可取；⛔ 政府网站托管副本为**无文本层扫描件**，⛔ OCR 路径不通。⭐ 上表条文与条款号系从中科院合肥物质科学研究院托管的**可检索文本版 PDF** 逐字提取，⭐ 三级/四级两处相同条文交叉一致。⚠️ ⛔ **正式引用前必须人工在 openstd 官方预览页复核一次条款号。**

### 2.5 中国生成式 AI 专门法规 · ⚠️ **语义最直接命中，⛔ 但主体错位，⛔ 且含最强反向证据**

| 法规 | 年份 | 条款 | 逐字原文 | 触发前提 | 是否覆盖 | 来源 | 核验 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 生成式人工智能服务管理暂行办法 | 2023-08-15 | **第二条第三款** | 「行业组织、企业、教育和科研机构…研发、应用生成式人工智能技术，**未向境内公众提供生成式人工智能服务的，不适用本办法的规定。**」 | — | ⚠️ **双刃**：⭐ 企业私域部署**不受本办法约束**（⭐ 利于可行性论证），⛔ 但**这不构成「必须私域部署」的禁令** | [cac.gov.cn](https://www.cac.gov.cn/2023-07/13/c_1690898327029107.htm) | 🟢 |
| 同上 | 2023 | **第十一条** | 「提供者对使用者的输入信息和使用记录应当依法履行保护义务，不得收集非必要个人信息，不得非法留存**能够识别使用者身份的**输入信息和使用记录，不得非法向他人提供使用者的输入信息和使用记录。」 | — | 🔻 ⛔ **如实判定：不覆盖工程制品**。⛔ 义务主体是**提供者**不是用户；⛔ 保护对象限于「能够识别使用者身份的」输入信息与个人信息，⛔ **技术内容本身不在射程**。⛔ 把这条写成「禁止用户外发技术文档」是**误读** | 同上 | 🟢 |
| 同上 | 2023 | 第二十条 | 「对来源于中华人民共和国境外向境内提供生成式人工智能服务不符合法律、行政法规和本办法规定的，国家网信部门应当通知有关机构采取技术措施和其他必要措施予以处置。」 | 境外服务向境内提供 | ⭐ **间接但对 (a) 层有用**：⭐ 境外主流 LLM 服务在华**不具备合法提供服务的地位**。⚠️ ⛔ 但制裁对象是**服务提供方与网络接入**，⛔ 不是对企业用户设定「不得外发」义务 | 同上 | 🟢 |
| **政务领域人工智能大模型部署应用指引**（中央网信办、国家发展改革委，2025-10） | 2025 | 四、(四) 严格落实保密要求 | 「…严格落实『**涉密不上网、上网不涉密**』等保密纪律要求，采取加装保密『护栏』等措施，**防止国家秘密、工作秘密和敏感信息等输入非涉密人工智能大模型**，防范敏感数据汇聚、关联引发的泄密风险。…」 | ⚠️ ⛔ 适用主体是「**政务部门**」，⛔ 不是企业 | ⭐⭐ **本轮语义最直接命中的成文表述** | [cac.gov.cn](https://www.cac.gov.cn/2025-10/10/c_1761819469929310.htm) | 🟢 |
| 同上 | 2025 | 三、(一) 规范部署 | 「对于智能问答、辅助文书起草等通用性较强…的场景，**需采用市场上成熟，并已完成网信部门备案的模型产品和服务**。…在保障安全和不泄露国家秘密、工作秘密和敏感信息等的前提下，**充分利用互联网算力和模型资源**，开展政务领域人工智能大模型部署应用。」 | 同上 | 🔻🔻 ⛔ **对 (c) 层的最强不利证据**：⛔ 官方在**比工业更敏感**的政务场景，⭐ 明确要求用「已完成网信部门备案的市场化模型产品和服务」并「**充分利用互联网算力和模型资源**」，⛔ **恰恰不是「必须私域部署」** | 同上 | 🟢 |
| 保密宣传口径（国安部 / 各地保密部门 AI 保密提示） | 2024-2025 | — | 「不得将涉密文件、图片、音频、视频等信息，以拍照、输入、复制以及其他任何形式，部分或者全部使用生成式人工智能工具进行处理」 | 涉密信息 | 🟡 ⛔ **宣传材料，⛔ 非规范性文件**。⛔ 不得当作法规条款引用，⭐ 可作「监管态度」佐证 | [湖北省科技厅转载](https://kjt.hubei.gov.cn/kjdt/ztzl/kjaq/kjaqdxal/202504/t20250423_5626302.shtml) | 🟡 |
| 国资委 / 国防科工局禁止性通知 | — | — | — | — | ⚪ **未检索到**任何公开的「禁止向公有云上传敏感数据」通知。⭐ 国资委公开文件均为**推进类**。⛔ 若存在应为内部发文，⛔ **不可在论文中假定其存在** | [sasac.gov.cn](http://www.sasac.gov.cn/n2588025/n2643314/c32881575/content.html) | ⚪ |

### 2.6 国防供应链（美国 DFARS / NIST SP 800-171 / CMMC）· ⭐ **英文世界里唯一直接管到这个动作的一族，⛔ 但它是「条件性允许」而非「禁止」**

⭐ **本节的 DFARS 三条由主 session 亲自 `curl` acquisition.gov 全文抽取并逐字核对**（⛔ 非采信代理转述，⛔ 依仓库 §3.8 纪律）。⭐ 版本标记：条款标题为 `SAFEGUARDING COVERED DEFENSE INFORMATION AND CYBER INCIDENT REPORTING (MAY 2024)`，⭐ 页面标注 DFARS Change 05/07/2026。

| 文件 | 版本 | 条款 | 逐字原文 | 触发前提 | 是否覆盖 | 来源 | 核验状态 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| DFARS 252.204-7012 | MAY 2024 | (b)(2)(ii)(D) | "If the Contractor intends to use an **external cloud service provider to store, process, or transmit any covered defense information** in performance of this contract, the Contractor shall require and ensure that the cloud service provider meets **security requirements equivalent to those established by the Government for the Federal Risk and Authorization Management Program (FedRAMP) Moderate baseline**… and that the cloud service provider complies with requirements in paragraphs (c) through (g) of this clause…" | 合同含本条款 + 外发内容构成 CDI | ⭐⭐ **直接覆盖该动作**，⛔ **但形态是条件性允许** | [acquisition.gov](https://www.acquisition.gov/dfars/252.204-7012-safeguarding-covered-defense-information-and-cyber-incident-reporting.) | 🟢 |
| DFARS 252.204-7012 | MAY 2024 | (a) 定义 `Controlled technical information` | "technical information with **military or space application** that is subject to controls on the access, use, reproduction, modification, performance, display, release, disclosure, or dissemination. Controlled technical information would meet the criteria, if disseminated, for **distribution statements B through F** using the criteria set forth in DoD Instruction 5230.24… The term does not include information that is lawfully publicly available without restrictions." | — | ⭐ **关键**：⭐ 军用/航天控制系统的需求与设计数据通常落入此定义 | 同上 | 🟢 |
| DFARS 252.204-7012 | MAY 2024 | (a) 定义 `Covered defense information` | "unclassified controlled technical information or other information, as described in the Controlled Unclassified Information (CUI) Registry… that requires safeguarding or dissemination controls… and is— (1) Marked or otherwise identified in the contract… and provided to the contractor by or on behalf of DoD…; or (2) **Collected, developed, received, transmitted, used, or stored by or on behalf of the contractor** in support of the performance of the contract." | — | ⭐ **关键**：⭐ (2) 明确覆盖承包商**自己开发**的制品，⛔ 不限于政府交付物 | 同上 | 🟢 |
| DFARS 252.204-7012 | MAY 2024 | (b)(2)(i) | 非政府运营 IT 服务的承包商系统，⭐ 适用 NIST SP 800-171（⭐ 以招标发布时生效版为准，⛔ 或经 Contracting Officer 授权） | 同上 | ⭐ 间接相关（⭐ 引入 800-171 控制项） | 同上 | 🟢 |
| DFARS 252.204-7012 | MAY 2024 | (b)(1)(i) | 云计算服务落入 DFARS 252.239-7010《Cloud Computing Services》 | ⛔ 仅当系统是**为政府运营**的 IT 服务 | ⛔ 间接相关（⛔ 触发条件较窄） | 同上 | 🟢 |
| NIST SP 800-171 | Rev. 2 (2020) | **3.1.20** | "**Verify and control/limit connections to and use of external systems.**" ⭐ DISCUSSION: "External systems are systems or components of systems for which organizations typically have **no direct supervision and authority over the application of security requirements and controls** or the determination of the effectiveness of implemented controls…" | 系统需处理 CUI | ⭐ **直接覆盖**（⭐ 第三方 LLM API 即 external system） | [NIST SP 800-171r2 PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-171r2.pdf) | 🟢 |
| NIST SP 800-171 | Rev. 2 (2020) | **3.1.3** | "**Control the flow of CUI in accordance with approved authorizations.**" ⭐ DISCUSSION: "Information flow control regulates **where information can travel** within a system and between systems (versus who can access the information)…" | 同上 | ⭐ **直接覆盖**（⭐ 把制品送出组织边界即 CUI flow） | 同上 | 🟢 |
| NIST SP 800-171 | Rev. 2 | 3.1.20 DISCUSSION | "This requirement also addresses the use of external systems for the processing, storage, or transmission of CUI, **including accessing cloud services (e.g., infrastructure as a service, platform as a service, or software as a service) from organizational systems.**" | 同上 | ⭐⭐ **直接覆盖**：⭐ SaaS 明文点名，⭐ LLM API 即 SaaS | 同上 | 🟢 |
| NIST SP 800-171 | Rev. 2 | 3.1.3 DISCUSSION | "Flow control restrictions include the following: **keeping export-controlled information from being transmitted in the clear to the Internet**; … and limiting information transfers between organizations based on data structures and content." | 同上 | ⭐ 直接覆盖 | 同上 | 🟢 |
| NIST SP 800-171 | Rev. 2 | 3.1.22 + DISCUSSION | "Control CUI posted or processed on publicly accessible systems." ⭐ DISCUSSION: "This requirement addresses **systems that are controlled by the organization** and accessible to the public…" | 同上 | ⛔ **不覆盖第三方 LLM API**——⛔ 常被误引 | 同上 | 🟢 |
| NIST SP 800-171 | **Rev. 3 (2024-05)** | **03.01.20 a.** | "**Prohibit the use of external systems unless the systems are specifically authorized.**" | ⚠️ ⛔ **DoD 尚未采纳** | ⚠️ ⭐ **全部条款中唯一的「默认禁止」式表述**，⛔ 但对 DoD 承包商**当前不生效** | [NIST SP 800-171r3 PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-171r3.pdf) | 🟢 |
| 32 CFR 170.2（CMMC，IBR 条款） | 89 FR 83214 | — | "(9) SP 800-171… **Revision 2**, February 2020 (includes updates as of January 28, 2021), (NIST SP 800-171 R2); IBR approved for §§170.4(b) and 170.14(a) through (c)." | — | ⭐ **关键**：⭐ 确认 CMMC 锁定 **Rev 2** | [eCFR 32 CFR 170](https://www.ecfr.gov/current/title-32/subtitle-B/chapter-XX/part-170) | 🟢 |
| **DFARS 252.204-7021** | **NOV 2025**（90 FR 43575） | **(d)(2)** | "**Only process, store, or transmit FCI or CUI on contractor information systems that have a CMMC status at the CMMC level required in paragraph (d)(1) of this clause, or higher**" | 合同含 CMMC 条款 | ⭐⭐ **直接覆盖，⭐ 且这是本族最接近「禁止」的一条** | [eCFR 252.204-7021](https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7021) | 🟢 |
| CMMC, 32 CFR | **170.16(c)(2)** | — | "**An OSA may use a cloud environment to process, store, or transmit CUI**… under the following circumstances: (i) The CSP product or service offering is FedRAMP Authorized at the FedRAMP Moderate (or higher) baseline…; **or** (ii)… meets security requirements equivalent to those established by the FedRAMP Moderate (or higher) baseline." | Level 2 | ⛔ **条件性允许**（⚠️ 逐字 "**may use**"） | 同上 | 🟢 |
| CMMC, 32 CFR | 170.16(c)(3)(ii) / 170.19(c)(2) Table 4 | — | "The ESP services used to meet OSA requirements are **assessed within the scope of the OSA's assessment against all Level 2 security requirements**." | ⭐ 供方被判为 ESP 而非 CSP | ⭐ **直接覆盖，⭐ 门槛更高** | 同上 | 🟢 |
| 32 CFR 2002.14（CUI 本体） | current | (c)(1) | "Authorized holders must take reasonable precautions to guard against unauthorized disclosure of CUI. They must include the following measures…: (1) **Establish controlled environments in which to protect CUI from unauthorized access or disclosure**…" | — | ⛔ 间接（⛔「controlled environment」未定义为「私域」） | [eCFR 32 CFR 2002.14](https://www.ecfr.gov/current/title-32/subtitle-B/chapter-XX/part-2002/section-2002.14) | 🟢 |
| **NARA CUI Registry · Controlled Technical Information** | current | — | "…**Examples of technical information include research and engineering data, engineering drawings, and associated lists, specifications, standards, process sheets, manuals, technical reports, technical orders, catalog-item identifications, data sets, studies and analyses and related information, and computer software executable code and source code.**" ⭐ Banner: `CUI//SP-CTI` | — | ⭐⭐⭐ **本轮对「需求文档 / 设计模型属于受控信息」最直接的官方证据** | [archives.gov CUI Registry](https://www.archives.gov/cui/registry/category-detail/controlled-technical-info) | 🟢 |
| DFARS 252.204-7012 | MAY 2024 | (a) 定义 `Technical information` | "technical data or computer software, as those terms are defined in… DFARS 252.227-7013… **Examples of technical information include research and engineering data, engineering drawings, and associated lists, specifications, standards, process sheets, manuals, technical reports…, data sets, studies and analyses…, and computer software executable code and source code.**" | — | ⭐⭐⭐ **决定性**：⭐「需求文档 = specifications / standards」「设计模型 = engineering data / data sets」 | [acquisition.gov](https://www.acquisition.gov/dfars/252.204-7012-safeguarding-covered-defense-information-and-cyber-incident-reporting.) | 🟢 |
| NIST SP 800-53 | Rev. 5 | SA-9 | "a. Require that providers of external system services comply with organizational security and privacy requirements…" ⭐ DISCUSSION: "…**The responsibility for managing risks from the use of external system services remains with authorizing officials.**" | — | ⛔ 直接覆盖，⛔ 但同为**条件性** | [NIST SP 800-53r5](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf) | 🟢 |

⭐ **这是整份台账里唯一一条**逐字点名「把受控信息交给外部云服务处理」**这个具体动作的成文规范**，⭐ 且它是**免费公开全文、可核验到条款级**的。⭐ 论证链条完整：(1) 军用 / 航天控制系统的技术数据构成 `controlled technical information`；(2) 承包商**自己开发**的相关制品即构成 `covered defense information`（⭐ 定义 (2) 项）；(3) 一旦要把它交给外部云服务 store / process / transmit，⭐ 就触发 FedRAMP Moderate 等效要求 + (c)-(g) 的事故报告、恶意软件、介质保全、取证访问、损害评估等一整套义务。

⛔ **但必须钉死一件事：它是「条件性允许」，⛔ 不是「禁止」。** ⛔ 条文写的是 "**shall require and ensure that the cloud service provider meets** security requirements equivalent to… FedRAMP Moderate"——⛔ 即**满足即可用**。⛔ **不得把它引成「不得使用云服务」**，⛔ 这与 ISO 26262 DIA 是同一类误读。

⚠️⚠️ ⛔ **而且「满足」这个条件今天已被实际满足了——⛔ 这是对整条 story 最致命的一组反向事实**（🟢 官方来源已核验）：

| 事实 | 时间 | 来源 |
| :-- | :-- | :-- |
| ⭐ Azure OpenAI Service 获 **FedRAMP High** 授权（Azure Government），⭐ 并获 DISA 的 **DoD IL4 / IL5** 临时授权（⭐ 含 GPT-4o） | 2024-09 | [Azure Government DevBlog](https://devblogs.microsoft.com/azuregov/azure-openai-fedramp-high-for-government/) |
| ⭐ Azure OpenAI 进一步获授权至 **IL6 与 Top Secret**，⭐ 覆盖全部美国政府数据密级 | 2025 | [Azure Government DevBlog](https://devblogs.microsoft.com/azuregov/azure-openai-authorization/) |
| ⭐ Amazon Bedrock 上的 Claude 与 Llama 模型获 **FedRAMP High + DoD IL4/5**（AWS GovCloud） | 2025-05 | [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2025/05/amazon-bedrock-models-fedramp-high-dod-il-4-5-govcloud/) |
| ⭐ OpenAI GPT / GPT OSS / NVIDIA Nemotron 亦获 **FedRAMP High + IL4/5**（Bedrock GovCloud） | 2026-06 | [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/06/addl-bedrock-model-fedramp-il-5-govcloud/) |
| ⭐ **「ITAR data can only be processed in Claude via AWS Bedrock, which is IL5 accredited.」** | — | [Anthropic Public Sector FAQs](https://support.claude.com/en/articles/13756069-public-sector-faqs) |
| ⛔ 反面：**Claude Enterprise on AWS Marketplace 未获 FedRAMP 授权**；⭐ 有 FedRAMP 需求者须用 C4G 或经 Bedrock GovCloud / Vertex Assured Workloads 访问 | — | 同上 |

⛔⛔ **而最致命的一击来自国防部自己**（🟢 官方新闻稿已核验）：

| 事实 | 逐字原文 | 日期 | 来源 |
| :-- | :-- | :-- | :-- |
| ⛔ **DoD 自建 GenAI.mil 平台，⛔ 上面跑的是第三方商用前沿模型，⛔ 且认证处理 CUI** | "Security is paramount, and **all tools on GenAI.mil are certified for Controlled Unclassified Information (CUI) and Impact Level 5 (IL5)**, making them secure for operational use."；⭐ 首发为 "**Google Cloud's Gemini for Government**" | 2025-12-09 | [war.gov Release 4354916](https://www.war.gov/News/Releases/Release/Article/4354916/the-war-department-unleashes-ai-on-new-genaimil-platform/) |
| ⛔ 扩展至 xAI | "…allow all military and civilian personnel to use xAI's capabilities at Impact Level 5 (IL5), enabling the **secure handling of Controlled Unclassified Information (CUI)** in daily workflows." | 2025-12-22 | [war.gov Release 4366573](https://www.war.gov/News/Releases/Release/Article/4366573/the-war-department-to-expand-ai-arsenal-on-genaimil-with-xai/) |
| ⛔ 扩展至 OpenAI | "…a partnership with OpenAI to integrate ChatGPT into GenAI.mil… make OpenAI's advanced large language models readily available to all 3 million Department personnel." | 2026-02-09 | [war.gov Release 4401775](https://www.war.gov/News/Releases/Release/Article/4401775/genaimils-rapid-expansion-continues-with-openai-partnership/) |

⛔ **用国防供应链条款论证「必须私域部署」，⛔ 而国防部本身正在用第三方商用模型处理 CUI——⛔ 这是审稿人最容易找到、⛔ 也最难回应的反例。**

⭐ **主流端点的 FedRAMP 实况**（⭐ 取自 GSA FedRAMP Marketplace 服务端数据，🟢 已核验）：⭐ **Amazon Bedrock@GovCloud** = FedRAMP High + DoD IL2/IL4/IL5/IL6；⭐ **Azure OpenAI@Azure Government** = High + IL4/IL5WI（⚠️ `IL5WI` = Workload Isolation，⛔ 需额外配置，⛔ 且不在 US DoD Central/East 的原生 IL5 服务清单内）；⭐ **Vertex AI@Assured Workloads** = High + IL2/IL4/IL5；⚠️⚠️ ⭐ **OpenAI `ChatGPT Enterprise and API Platform` 已于 2026-01-09 取得 FedRAMP 20x Class C（≡ Moderate）认证**，⛔ 认证对象名称明确含 "API Platform"（[Marketplace FR2533155773](https://www.fedramp.gov/marketplace/products/FR2533155773/)）；⛔ **Anthropic 作为 CSP 在 605 个条目中零命中**（⭐ Claude 的合规路径是经 Bedrock GovCloud / Vertex，⛔ 而非自持授权）。

⛔ **净后果（⛔ 与直觉相反，⛔ 必须如实写）**：⭐ 这一族确实**直接管到了这个动作**，⛔ 但它给出的合规解是「**用已获授权的云上 LLM**」，⛔ **不是「自己部署」**。⛔ 且由于 OpenAI API Platform 已取得 Moderate 认证，⛔ **连「商用端点一律不合规」这句话都不再成立**——⭐ 准确表述只能是「**不能使用未取得 FedRAMP Moderate 授权或等效认定的端点**」（⭐ 例如直连 `api.anthropic.com`）。

⭐ **那这一族还能支撑什么？⭐ 四条经得起条款核对的替代论证**：

1. ⭐⭐ **(c)-(g) 义务是真正的实践卡点，⭐ 且独立于 FedRAMP 状态。** ⭐ 7012(b)(2)(ii)(D) 是**两个并列条件**：⭐ FedRAMP 等效 **and** CSP 须 comply with (c)-(g)——⭐ 72 小时向 dibnet.dod.mil 报告网络事件、向 DC3 提交恶意软件、保存镜像与包捕获、按需向 DoD 提供取证访问。⛔ **普通商用 ToS 不提供这些。** ⭐ 这条可引、可核，⛔ 且不依赖「禁止」措辞。
2. ⭐ **合规工程成本可量化。** 🟡 DoD CIO 的 FedRAMP Moderate Equivalency 备忘录要求 3PAO 出具 100% 合规的 BoE（SSP / SAP / SAR / CRM / 已闭环 POA&M），⛔ 不允许 3PAO 评估产生的 POA&M、⛔ 不允许自证；⭐ CMMC 170.19(c)(2)(ii) 要求 CSP 出具 CRM 并写进 SSP。
3. ⭐ **可选模型集被 region 与授权边界严重收窄**：⭐ 实际只有 `Bedrock@GovCloud` / `Azure OpenAI@Azure Gov` / `Vertex@Assured Workloads` 少数组合，⛔ 且政府 region 的模型版本通常**滞后于 commercial**。⭐ 这是「可用性与新鲜度」论证。
4. ⭐ **非 CSP 路径门槛更高**：⭐ 若供方被判为 ESP 而非 CSP，⭐ 须按**全部** Level 2 要求纳入 OSA 评估范围。

⚠️ ⛔ **两条必须写进论文的边界**：(1) ⛔ **触发前提是 DoD 合同 + CDI/CUI**——⛔ 若场景无 DoD nexus（⛔ 普通民用控制系统），⛔ 本族**完全不适用**，⛔ 其适用面比「工业场景」窄得多；(2) ⛔ **引用 Rev 3 的 03.01.20(a) 必须同时声明 Class Deviation 2024-O0013 使 Rev 2 仍为现行标准**（🟡 该 Deviation 为二手佐证，⛔ 官方 PDF 站点 curl 超时，⛔ 但与 32 CFR 170.2 的 IBR 🟢 相互印证），⛔ 否则构成误引，⛔ 且这恰是最容易被抓住的一处。

### 2.7 行业机制 · 欧盟汽车业 TISAX / VDA ISA · ⭐⭐ **唯一逐字点名 AI 工具的一条（⭐ 第一手 XLSX 逐格核验）**

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

### 2.7a 行业机制 · ISO/IEC 27001:2022 Annex A 5.23（⭐ ISA 1.3.3 的上游对标项）

⭐ VDA ISA 1.3.3 在其 XLSX 的对标列中指向 **ISO/IEC 27001:2022 Annex A 5.23**。⭐ 该控制项标题逐字为 **"Information security for use of cloud services"**，⭐ 是 2022 版**新增**控制项（⛔ 2013 版中不存在，⛔ 当时云服务归入供方关系章节）。🟡 其控制文本（要求就云服务的**获取、使用、管理与退出**建立符合组织信息安全要求的流程）**仅有二手来源**，⛔ 正文在 ISO 付费墙内，⛔ 标 🟡。⛔ 论文若引用，⛔ 只应引**标题与新增事实**，⛔ 不得逐字引控制文本。二手出处：[ISMS.online A.5.23](https://www.isms.online/iso-27001/annex-a-2022/5-23-information-security-use-of-cloud-services-2022/)、[Advisera](https://advisera.com/iso27001/control-5-23-information-security-for-use-of-cloud-services/)。

### 2.7b 行业机制 · UNECE R155 / R156 · 结论：⛔ **间接相关，⛔ 需跨一步不小的推理**

| 文件 | 年份 | 条款 | 逐字原文 | 是否覆盖 | 来源 | 核验状态 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| UN R155 | 2021 | §7.2.2.5 | "The vehicle manufacturer shall be required to demonstrate how their Cybersecurity Management System will manage dependencies that may exist with **contracted suppliers, service providers or manufacturer's sub-organizations**…" | ⛔ 间接相关 | [CELEX:42021X0387](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:42021X0387) | 🟢（⚠️ OJ 转载版） |
| UN R155 | 2021 | §5.1.1(a) / §7.3.2 | "Collect and verify the information required under this Regulation **through the supply chain**…" / "shall identify and manage… supplier-related risks" | ⛔ 间接相关 | 同上 | 🟢 |
| UN R155 | 2021 | Annex 5 Part A §4.3.1 | 威胁条目 "Extraction of copyright or proprietary software from vehicle systems (product piracy)" | ⛔ **不覆盖**（⛔ 针对**车上系统**被提取，⛔ 非开发期文档外发） | 同上 | 🟢 |
| UN R156 | 2021 | 全文 | 仅 §3.3 一句关于型式认证材料 know-how 保密 | ⛔ **不覆盖** | [CELEX:42021X0388](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:42021X0388) | 🟢 |

⚠️ `unece.org` 直连返回 **403**，⭐ 改用 EUR-Lex 转载的 OJ 版本（OJ L 82, 9.3.2021）；⛔ 该版本自带声明「Only the original UN/ECE texts have legal effect under international public law」，⛔ 引用时须标注。

### 2.7c 行业机制 · 欧盟航空 Part-IS · ⭐⭐ **航空侧唯一的正面命中，⭐ 且是强制性立法**

⭐ **本节四条由主 session 亲自 `curl` EUR-Lex 官方全文抽取并逐字核对**（⛔ 依 §3.8）。⭐ **Commission Delegated Regulation (EU) 2022/1645**（2022-07-14 通过，OJ L 248, 26.9.2022，⭐ **自 2025-10-16 起适用**）。

| 条款 | 逐字原文 | 触发前提 | 是否覆盖 | 核验 |
| :-- | :-- | :-- | :-- | :-- |
| **Part 21 新增 21.A.239A**（⭐ 由 2022/1645 插入 Reg. 748/2012） | "In addition to the design management system required by point 21.A.239, **the design organisation shall establish, implement and maintain an information security management system** in accordance with Commission Delegated Regulation (EU) 2022/1645 in order to ensure the proper management of information security risks **which may have an impact on aviation safety**." | ⭐ 持 DOA 的**设计组织** + ⚠️ **风险须可能影响航空安全** | ⭐ **间接相关（⭐ 强制性）** | 🟢 |
| Part 21 新增 21.A.139A | ⭐ 同一公式，⛔ 对象为**生产组织** | 持 POA 的生产组织 | ⭐ 间接相关 | 🟢 |
| **IS.D.OR.205(a)** | "The organisation shall identify all of its elements, which could be exposed to information security risks. That shall include: (1) the organisation's activities, facilities and resources, as well as **the services the organisation operates, provides, receives or maintains**; (2) the equipment, systems, **data and information** that contribute to the functioning of the elements listed in point (1)." | 同上 | ⭐⭐ **关键钩子**：⭐ "services the organisation **receives**" 足以涵盖外部托管模型 API | 🟢 |
| **IS.D.OR.200(a)(13)** | "…**protects the confidentiality of any information that the organisation may have received from other organisations**, according to its level of sensitivity." | 同上 | ⭐⭐ **本台账中唯一一条明文规定 confidentiality 义务的强制条文** | 🟢 |
| **IS.D.OR.235(a)** | "The organisation shall ensure that **when contracting any part of the activities referred to in point IS.D.OR.200 to other organisations, the contracted activities comply with the requirements of this Regulation and the contracted organisation works under its oversight.**" | 同上 | ⭐ 直接覆盖「外包给他方」 | 🟢 |

⚠️ ⛔ **限定必须写满，⛔ 否则是过度主张**：⛔ Part-IS 全程以「**with potential impact on aviation safety**」为闸门，⛔ **它不是通用的 IP 保密制度**；⛔ 且 IS.D.OR.200(a)(13) 保护的是「**从其他组织收到的**信息」，⛔ 不是组织自己的设计资料。⛔ 因此它能支撑的是「⭐ 航空设计组织须把外部 AI 服务纳入 ISMS 风险评估与合同监督」，⛔ **不是**「不得使用外部 AI 服务」。

### 2.7d ⚠️⚠️ 行业机制 · EASA NPA 2025-07(A) · ⛔ **一条直接约束本研究架构的监管动向**

⭐ **本条由主 session 亲自下载 EASA 官方 PDF 提取核对。** ⭐ EASA NPA 2025-07(A) 在说明 DS.AI 的范围排除时逐字写道：

> "Some exclusions from the scope of the DS have been identified, to avoid the risk of innovative AI technology contributing to any fatalities or uncontained environmental effect, to prevent the use of online learning techniques which are not compatible with the current approval frameworks, to limit the use of AI techniques (symbolic or hybrid-AI) that do not yet fall within the technical scope of this DS and **to ensure human oversight at development time when using generative AI techniques by avoiding the double development and verification with AI tools.**"

⭐ 同一文件另有一句（⭐ 关于覆盖面）：「While **generative AI tools and general-purpose models are not yet fully covered**, the current proposal creates a flexible foundation for adaptation as technology evolves.」来源：[EASA NPA 2025-07(A)](https://www.easa.europa.eu/en/downloads/142702/en)，🟢 已核验。

⛔⛔ **这条对本仓库的意义远超「私域部署」这个话题，⛔ 必须单独上报**：⛔ 它要求**避免用 AI 工具同时做开发与验证**（"avoiding the double development and verification with AI tools"），⛔ 而这正是 **project_1（LLM 建模）→ project_2/3（生成性质并验证）→ project_4（修复）** 这条闭环的形态。⚠️ ⛔ **必须同时说清它的性质与边界**：(1) ⛔ **NPA = Notice of Proposed Amendment，⭐ 是征求意见稿，⛔ 不是生效规章**；(2) ⛔ 适用域是**航空**，⛔ 不自动外推到汽车 / 轨交 / 医疗；(3) ⛔ 该句出现在**范围排除**的说明段，⛔ 不是一条编号要求。⭐ **但它是一条真实的监管方向信号**，⛔ 且**对我们不利**——⛔ 论文若要主张全自动闭环，⛔ 应当预先处理它，⛔ 而不是等审稿人提出。

### 2.7e 行业机制 · IEC 81001-5-1:2021（医疗健康软件安全生命周期）· ⭐ **医疗侧唯一命中**

| 条款 | 逐字原文（⭐ 目录标题） | 是否覆盖 | 核验 |
| :-- | :-- | :-- | :-- |
| **§5.1.2** | `Development environment SECURITY`（⭐ 位于 5.1 Software development planning 项下，⭐ p.21） | ⭐ **间接相关**：⭐ 医疗侧唯一直接命名「研发环境安全」的条款 | 🟢 标题 / 🔴 正文 |
| **§4.1.5** | `SOFTWARE ITEMS from third-party suppliers`（⭐ p.19） | ⭐ 间接相关 | 🟢 标题 / 🔴 正文 |
| §1 Scope | "This document defines the LIFE CYCLE requirements for development and maintenance of HEALTH SOFTWARE needed to support conformance to IEC 62443-4-1… by increasing the SECURITY of **SOFTWARE LIFE CYCLE PROCESSES themselves**." | ⭐ 间接相关（⭐ 注意「life cycle processes themselves」这一措辞） | 🟢 |

⭐ **与 §1.5b 的 IEC 62443-4-1 §5.9（SM-7 Development environment security）构成同一模式**：⭐ 医疗与工控两侧**各自**把「研发环境安全」立为规范性条款，⭐ 且 81001-5-1 明言其目的是支撑 IEC 62443-4-1 的符合性。⛔ **但两者的条文正文都在付费墙内未核验**，⛔ 不得据标题断言其内容禁止外发。

⚠️ **IEC 62304 Ed 2.0 状态纠错**（🟡 国家机构镜像，⛔ IEC 官方 dashboard 被 Cloudflare 拦截）：⛔ 项目仍处 **CD 阶段（stage 30.20）**，⛔ **尚未发布**。⛔ 若干厂商博客称「2026 年 FDIS / 发布」与此矛盾，⛔ **不可采信**。

### 2.8 商业秘密法（欧盟 TSD）· 结论：⭐ **法理最强，⛔ 但是推论，⛔ 无判例**

| 文件 | 年份 | 条款 | 逐字原文 | 是否覆盖 | 来源 | 核验状态 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| Directive (EU) 2016/943 | 2016 | Art. 2(1)(a)(b)(c) | "'trade secret' means information which meets **all** of the following requirements: (a) it is secret…; (b) it has commercial value because it is secret; (c) **it has been subject to reasonable steps under the circumstances, by the person lawfully in control of the information, to keep it secret**" | ⭐ **间接相关（⭐ 欧盟一族最强）** | [CELEX:32016L0943](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016L0943) | 🟢 |
| Directive (EU) 2016/943 | 2016 | Art. 4(3)(b) | "The use or disclosure of a trade secret shall be considered unlawful whenever carried out, without the consent of the trade secret holder, by a person who… (b) [is] in breach of a **confidentiality agreement or any other duty not to disclose** the trade secret" | ⭐ 间接相关（⛔ 无 NDA / DPA 时对方不负此义务） | 同上 | 🟢 |

⭐ **逻辑链**：⭐ 三要件是**累积**的（"meets **all**"）。⭐ 若设计制品满足 (a) 秘密性与 (b) 商业价值，⛔ 而组织在无 DPA / 无 NDA / 无零留存承诺的情况下把它明文送入公有云 LLM，⛔ 则对方不负 Art. 4(3)(b) 意义上的保密义务，⛔ 于是要件 (c) 可能被认定不成立——⛔ **商业秘密保护整体丧失**（⛔ 注意：不是被侵害，⛔ 是从一开始就不受保护）。

⛔ **必须如实标注两点**：(1) ⛔ **这是学理推论，⛔ 不是成文要求**——TSD 里没有任何一条写「向 AI 服务上传即丧失保护」；(2) ⚪ **欧盟侧无判例**——未找到任何 CJEU 或成员国判决把 Art. 2(1)(c) 适用于 AI chatbot 上传情形。🟡 检索到的唯一同形态判决是美国 *Trinidad v. OpenAI*（N.D. Cal., 2026-01，DTSA 项下），⛔ 事实形态特殊（⛔ 原告本人用 ChatGPT 创作了所主张的秘密），⛔ **不可作为欧盟依据**；🟡 另有二手报道称奥地利最高法院 4 Ob 165/16t 认为该要件只要求「合理努力」而非「成功保密」，⛔ 若属实**反而对强主张不利**。

⭐ **可写的安全表述**：Directive (EU) 2016/943 Art. 2(1)(c) 使商业秘密保护条件性地依赖于持有人所采取的保密措施；将设计制品送入不承担保密义务的公有 LLM 服务，会对该要件构成可争辩的削弱，⛔ 而这一风险目前**尚无欧盟判例予以确认**。

---

## 3. ⛔ 否定结果清单（查了但没有的）

⭐ **本节是本轮的高价值产出，⛔ 不是失败记录。** ⭐ 每条都写明「查了什么版本 / 查了哪些部分 / 用什么检索 / 结论为无」。

### 3.1 功能安全标准族 · ⛔ 全部为无

| 对象 | 查了什么 | 检索方式 | 结论 |
| :-- | :-- | :-- | :-- |
| IEC 61508-1:2010 | 完整 Scope §1.1-1.4 | 关键词 + 逐条读 a)-n) | ⛔ **明确排除**：§1.2 l)/m) 逐字排除安全防护措施与安全策略要求 |
| IEC 61508-3:2010 | 完整目录 Clause 1-8 + Annex A-G、完整 Scope §1.1 a)-j) | `grep` 五词 + 逐条读 | ⛔ **无**任何保密 / 数据保护 / 第三方数据处理条款；⛔ 五词命中 0 |
| ISO 26262-8:2018 | 完整目录 Clause 1-16 + Annex A、完整 Scope、Clause 5 全部 preview 正文 | `grep` 六词 + 逐条读 | ⛔ **无**；⭐ 支持过程枚举 12 项无一涉及；⭐ Clause 5 = 责任划分 |
| ISO 26262-6:2018 | 完整目录 + Introduction + §5.2 | `grep` 六词 | ⛔ **无**；⭐ 网络安全仅一处 "can" 级 NOTE |
| ISO 26262-2:2018 | 完整目录 + Introduction | `grep` 六词 | ⛔ **无**；⭐ 网络安全仅 Annex E（informative） |
| ISO/SAE 21434:2021 | Scope + Introduction 逐 Clause 说明 | 逐条读 | ⛔ **明确排除**：§1「不规定具体技术或解决方案」；⭐ Clause 7 = 责任划分 |
| ISO/IEC TR 5469:2024 | 完整目录 Clause 1-11 + Annex A-D、Scope | 逐条读 | ⛔ **无**数据驻留条款；⭐ 但 Scope 正面涵盖本文场景 |
| DO-178C / DO-330 | 完整目录 Sec 1-12 + Annex A/B | ⭐ FAA 138 页官方对照文档 `grep` 七词 | ⛔ **无**：⭐ 七词全部 0 命中；⚠️ ⛔ §7.2.7 实为 `Archive, Retrieval, and Release` |
| EN 50128 / EN 50716 | 完整目录 + Introduction + Clause 1-2 | ⭐ 官方样张 `grep` 八词 | ⛔ **无，⭐ 且显式排除**：⭐ EN 50716 Introduction 逐字排除 security policies / services |
| IEC 62304:2006 | 完整目录 Clause 1-9 | ⭐ 主 session 补做：`grep` 五词 + 逐条读目录 | ⛔ **无**（⭐ 唯一 `third party` 命中属 `manufacturer` 定义用语） |

### 3.2 Q2 各族 · ⛔ 明确的否定项

| 对象 | 结论 | 依据 |
| :-- | :-- | :-- |
| GDPR | ⛔ **不适用**（⛔ 前提不成立，⛔ 非成本高） | Art. 2(1) + Art. 4(1)：⛔ 工程制品无个人数据 |
| EU AI Act | ⛔ **不适用** | ⛔ 无任何条款规制输入数据保密性；⛔ 不落入 Art. 6 / Annex III |
| EU Data Act Ch. II 商业秘密条款 | ⛔ **场景错位** | ⛔ Art. 1(2)(a) 锁定 connected product 的 IoT 运行数据 |
| 中国《个人信息保护法》 | ⛔ **不适用** | ⛔ 工程制品通常不含个人信息 |
| 中国《汽车数据安全管理若干规定》 | ⛔ **不覆盖** | ⛔ 第三条枚举六项**全部是运行期数据**，⛔ 无一项是设计/需求文档 |
| 中国《生成式 AI 暂行办法》第十一条 | ⛔ **不覆盖工程制品** | ⛔ 义务主体是提供者；⛔ 保护对象限「能识别使用者身份的」输入与个人信息 |
| 中国《网络安全等级保护条例》 | ⚪ **查无此法** | ⛔ 仅 2018 征求意见稿；⛔ 2025 年仍为「预备制定」 |
| 中国《工作秘密管理办法》 | ⚪ **未公布** | ⛔ 保密法第六十四条授权制定，⛔ 至今空转 |
| 国资委 / 国防科工局「禁止向公有 LLM 上传敏感数据」通知 | ⚪ **公开渠道查无此文** | ⛔ 公开文件均为推进类；⛔ **不可假定内部发文存在** |
| 欧盟 / 成员国 DPA「禁止企业向公有 LLM 输入商业敏感数据」正式指引 | ⚪ **未找到** | ⛔ Garante 2023 令针对个人数据；⛔ EDPB 两份文件是 GDPR 风险方法学 |
| 「上传公有 LLM 即丧失商业秘密保护」的欧盟判例 | ⚪ **无** | ⛔ 唯一同形态判决在美国且事实特殊 |
| 中国禁止/限制出口技术目录中的**通用**工业控制软件条目 | ⛔ **无** | ⭐ 但存在**领域性**条目（⭐ 无人机飞控算法及软件），⛔ 见 §2.1b 的冲突裁定 |

### 3.3 ⛔ 三条明令禁止的引用方式（⛔ 每条都会被审稿人一击打穿）

1. ⛔ **不得**把 ISO 26262-8 Clause 5 / DIA 引成「须签接口协议 → 故不得外发」。⛔ §5.1 c) 的目标是「identify the **work products to be exchanged**」，⛔ 它是**共享机制**；⛔ 且 §5.2 NOTE 2 使其对不承担安全责任的 LLM 供方**根本不适用**。
2. ⛔ **不得**把 DFARS 252.204-7012 (b)(2)(ii)(D) 引成「不得使用云服务」。⛔ 条文是 "shall require and ensure that the cloud service provider **meets** security requirements equivalent to… FedRAMP Moderate"——⭐ **满足即可用**。
3. ⛔ **不得**把中国《出口管制法》第二条第二款「包括技术资料等数据」单独拎出来当作「工程文档受管制」的证据。⛔ 它只扩展**载体形态**，⛔ 不新增管制对象；⛔ 第四条明定「管制清单」是唯一开关。

⛔ **另加一条自查纪律**：⭐ 上述三条误读有共同结构——⛔ **把「规范如何做某事」的条款读成「禁止做某事」**。⭐ 引用任何一条依据前，⛔ 先问「它是在**授权并规范**这个动作，⛔ 还是在**禁止**这个动作」。

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

| 族 | 主入口（⭐ 均为免费公开全文） | 抓取方式 | 命中 |
| :-- | :-- | :-- | :-- |
| 美国出口管制 | `ecfr.gov` 官方 renderer API | `curl` + HTML 剥标签 + 定位条款 | ⭐ ITAR §120.54(a)(5)/(b)(1)(ii)/(b)(2)/(c)；⭐ EAR §734.18(a)(5)/(b)/(c) |
| 美国国防供应链 | `acquisition.gov`、`ecfr.gov`（32 CFR 170 / 48 CFR 252）、`nvlpubs.nist.gov`、`archives.gov`、`war.gov`、`fedramp.gov` | `curl` + 文本提取 | ⭐ DFARS 7012 (a)/(b)(1)/(b)(2)(i)/(b)(2)(ii)(D)、7021(d)(2)、7010；⭐ 800-171 R2 3.1.3/3.1.20/3.1.22 + R3 03.01.20；⭐ CMMC 170.2/170.16/170.19；⭐ CUI Registry CTI；⭐ 800-53 SA-9 |
| 中国 | `npc.gov.cn`、`gov.cn`、`cac.gov.cn`、`mofcom.gov.cn`、`most.gov.cn`、`gjbmj.gov.cn`、`moj.gov.cn` | `curl` + 多编码解码 + 条号定位；⭐ 目录 PDF 走 `pdf_extractor` | ⭐ 保密法 29/30/31/64；⭐ 数安法 21/31/36；⭐ 11 号令 4/5；⭐ 16 号令 2/3/7；⭐ 790 号令 37/62；⭐ 网安法 39；⭐ 出口管制法 2/4/12；⭐ 目录 203912X |
| 欧盟 | `eur-lex.europa.eu`（CELEX 全文 HTML） | 抓取 + 条款定位 | ⭐ GDPR 2/4/28/44-49；⭐ Data Act 32/23/4/5；⭐ AI Act 2/6/25/78；⭐ TSD 2(1)/4(3)(b)；⭐ UN R155/R156（OJ 转载） |
| TISAX / VDA ISA | `portal.enx.com` 官方 XLSX | ⭐ 下载 `isa6-en.xlsx` 与 `isa2027-en.xlsx`，⭐ 解 `sharedStrings.xml` 逐格比对 | ⭐ Glossary AI 词条；⭐ 1.3.3 / 5.1.2 / 5.3.4 / 6.1.1 / 6.1.2；⭐ Handbook 2.8 §4.3.3 |
| 厂商合规实况 | `openai.com`、`support.claude.com`、`aws.amazon.com`、`learn.microsoft.com`、`devblogs.microsoft.com`、`fedramp.gov/marketplace` | WebFetch / WebSearch + 官方页核对 | ⭐ ZDR / EU 驻留；⭐ Bedrock IL5；⭐ Azure OpenAI IL4/5WI/IL6；⭐ OpenAI 20x Class C |

⭐ **机械对拍范例**（⭐ TISAX AI 词条为 ISA2027 新增的证明）：⭐ 对两份官方 XLSX 的 `sharedStrings.xml` 全文件检索 `AI` / `artificial intelligence` / `machine learning` / `LLM`——⭐ `isa6-en.xlsx` **命中 0**，⭐ `isa2027-en.xlsx` **命中 1**（⭐ 即 Glossary `Cloud/external IT service` 词条）。

### 4.3 ⭐ 主 session 亲自复核的条款（⛔ 依仓库 §3.8 与「机械代理只能定位不能裁定」）

⛔ **凡承重结论所依赖的条文，⛔ 均不采信代理转述，⛔ 由主 session 重新抓原文逐字核对**：

| 条款 | 复核方式 | 结果 |
| :-- | :-- | :-- |
| EAR 15 CFR §734.18(a)(5)/(b) | `curl` eCFR API | ✅ 与转述一致 |
| ITAR 22 CFR §120.54(a)(5)/(b)(1)/(b)(2)/(c) | `curl` eCFR API | ✅ 一致；⚠️ ⛔ 但代理称定义在 `§120.55`——⛔ **实为 §120.54(b)(1)**，⛔ 已更正 |
| DFARS 252.204-7012 (a)/(b)(2)(ii)(D) | `curl` acquisition.gov | ✅ 一致 |
| NIST SP 800-171 Rev 2 §3.1.3 / §3.1.20 | ⭐ 下载官方 PDF 提取 | ✅ 一致 |
| 保密法（2024）第 29/30/31/64 条 | `curl` npc.gov.cn | ✅ 一致；⭐ 并确认第六十五条施行日期 |
| 中国禁止/限制出口技术目录 `203912X` | ⭐ 下载官方 PDF 提取 + `grep` | ⚠️ ⛔ **两代理结论相反，⭐ 已裁定**（⭐ 见 §2.1b） |
| Anthropic「ITAR data … via AWS Bedrock」 | WebFetch 官方支持页 | ✅ 一致；⛔ **推翻了本台账早先版本对 §2.1 的过强表述**，⛔ 已就地更正 |

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
| DO-178C §7.2.7 正文、DO-330 条文 | ⛔ RTCA 付费出版物 | 🔴，⭐ 目录与三准则有两处独立二手互证 🟡 |
| IEC 81001-5-1 §5.1.2 / §4.1.5 正文 | ⛔ 付费墙 | 🔴，⛔ **不得据标题断言其禁止外发** |
| EASA NPA 2025-07(A) | ⭐ 原文已核验，⛔ 但性质是**征求意见稿**非生效规章 | 🟢 原文 / ⚠️ ⛔ 引用须标明非规章地位 |
| IEC 62304 Ed 2.0 | ⭐ 仍处 CD 阶段（stage 30.20），⛔ 未发布 | 🟡（⛔ IEC dashboard 被 Cloudflare 拦截，⛔ 用国家机构镜像） |
| IEC 62304 SOUP 子条编号（5.3.x / 7.x / 8.x） | ⛔ preview 范围外 | 🔴，⛔ 仅确认 SOUP 位于 Clause 5.3 项下 |
| ISO 26262-8 §5.4.3（DIA 内容 11 项） | ⛔ preview 范围外 | 🔴 |
| ISO/SAE 21434 Clause 7 正文 + Annex C（CIA 内容） | ⛔ preview 范围外 | 🔴 |
| ISO/IEC TR 5469 §10.3.5 正文 | ⛔ preview 范围外 | 🔴 |
| IEC 62443-4-1 §5.9（SM-7）条文 | ⛔ 付费墙 | 🔴，⛔ 仅目录标题 🟢 |
| GB/T 22239-2019 全部条款号 | ⛔ openstd 官方预览为 JS 页面；⛔ 政府副本为无文本层扫描件；⛔ 本机无 OCR | 🟡，⚠️ ⛔ **正式引用前必须人工在 openstd 复核** |
| DoD CIO FedRAMP Moderate Equivalency 备忘录 | ⛔ Akamai WAF 403 | 🟡（⭐ 有 NDIA 公开简报佐证） |
| Class Deviation 2024-O0013 Rev.1 | ⛔ acq.osd.mil 超时 | 🟡（⭐ 与 32 CFR 170.2 的 IBR 🟢 互证） |
| DoDI 5230.24 / DoDI 5200.48 | ⛔ esd.whs.mil Akamai WAF 403 | 🔴，⭐ 其角色由 DFARS 7012(a) 与 NARA Registry 两处 🟢 互证 |
| 两用物项出口管制清单 700 余项具体条目 | ⛔ 仅核验「清单说明」第 1-6 页 | 🔴 |
| 2023 年目录中航空航天 / 轨道交通相关条目的穷举 | ⛔ 仅确认无人机飞控（`203912X`）一处形态 | 🔴 |
| 各行业「重要数据」具体目录 | ⛔ 须按工信 / 能源 / 交通分别查证 | 🔴 |
| ITAR §120.17 / EAR §734.15（release / deemed export 一般规则） | ⛔ 本轮未展开 | 🔴，⚠️ ⛔ §2.1 的「回落到一般规则评估」这一步**未逐条核验** |
| 各军种 CIO 生成式 AI 备忘录（Army 2024-06、DON） | ⛔ doncio.navy.mil 连接超时 | 🔴 |
| OpenAI ChatGPT Gov / trust center | ⛔ Cloudflare 403 | 🔴 |
| 中国《保密法》2010 版旧条号 | ⛔ 本轮未核验（⛔ 任务假设为第二十五条） | ⚪ |
