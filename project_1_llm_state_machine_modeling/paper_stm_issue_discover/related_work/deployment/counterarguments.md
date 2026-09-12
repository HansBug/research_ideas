# 反方与预答

> ⛔ **本文件是红队产出。** 它的职责是**把刀磨快**，不是让 story 好看。凡我们答不上来的，一律写在 §6，⛔ 不做修辞掩盖。
>
> **核验日期统一为 2026-08-13**（另注明者除外）。证据级别口径：**M** = 主 session 或 subagent 取到一手原文逐字核过 · **S** = 官方页面但返回为工具摘要 / 二手引述一手 · **I** = 只见于搜索摘要或二手文章，⛔ **标 I 的不得写成事实句**。
>
> 姊妹文件：[regulatory_ledger.md](./regulatory_ledger.md)（法规逐条台账）· [se_motivation_survey.md](./se_motivation_survey.md)（SE 文献动机论证）· [small_model_papers.md](./small_model_papers.md)（小模型 + 方法学补偿）· [verification_log.md](./verification_log.md)（一手核验记录）。⛔ 本文件不复制它们的内容，只在需要时引用并标注落点。

## 0. 一句话结论：这条 story 最致命的一刀是什么

⛔ **最致命的一刀不是「公有云已合规」，而是「动机层和贡献层之间没有因果连接」。**

把这条 story 拆成三段命题看：

| 段 | 命题 | 我们守得住吗 |
| :-: | :-- | :-- |
| **P1** | 某些工业场景**不能**把需求 / 设计模型送进公有云 LLM | **守得住，但只在窄条件下**（见 §1.2）。⛔ 不是「工业场景」普遍成立 |
| **P2** | P1 ⟹ **必须用小模型**（如 Qwen-32B） | ⛔ **守不住。** 这是纯逻辑跳跃，且它的补救前提与 P1 的成立条件**互相矛盾**（见 §5.1） |
| **P3** | P2 ⟹ **我们的方法有价值**（让小模型接近大模型 + 可断言可追溯） | ⛔ **守不住，且一个数都没有。** 已知的同向证据全指向反面 |

**三段里只有 P1 有一手依据，⛔ 而论文卖的是 P3。** ⛔ 审稿人只要打断 P1→P2 或 P2→P3 任意一环，整条 story 就断，**而 §1 的全部合规调研只加固 P1**。这就是为什么把主要力气花在「反驳 1 能不能守住」是**战略误判**：守住了也不通向结论。

⛔ **第二致命的一刀是内部的**：主臂 `hit@1` $\le$ **60.4%** 而朴素单提示基线 **76.2%**（$\Delta = -15.82$pp，同一批 SOTA 模型，见 [../../baseline_arm/docs/generations/x1v2/verdicts.md](../../baseline_arm/docs/generations/x1v2/verdicts.md)）。⛔ 也就是说：**在大模型上我们的方法都还没打赢什么都不做**，而 P3 要求它在小模型上把差距补回来。[verification_log.md](./verification_log.md) §V1 已裁定：**私域论证救不了这个差**——它是「同模型换方法」造成的，与部署形态在因果上不相接。

⚠️ **本文件之外的边界**：−15.82pp 的归因与修法属 M1 / v47，⛔ 不在 N1a 范围；本文件只负责说明**它使 §1 的全部战果贬值到什么程度**。

---

## 1. 反驳 1 · 「公有云早就合规了，所以『不得不本地部署』不成立」

> **审稿人的原话大概会是**：Azure OpenAI 已获 FedRAMP High 与 DoD IL2/IL4/IL5WI/IL6；AWS Bedrock 在 GovCloud 有 FedRAMP High + IL5；Google 的 Generative AI on Vertex 在 Assured Workloads 的 **ITAR** control package 内。受监管行业就是这么用的。你们的动机是伪的。

⛔ **先说结论：这一刀我们只能挡住一部分，而挡住的那部分恰好与我们要用的模型不匹配（见 §5.2）。**

### 1.1 各云的一手事实

下表每格都标了证据级别。⚠️ **两条术语陷阱先记住**：微软已把 Azure OpenAI 并入 "**Foundry Models sold by Azure**"（`content filters` 改名 Guardrails、`Azure AI Foundry` 改名 Microsoft Foundry）；Google 已把 Vertex AI 整体改名 "**Gemini Enterprise Agent Platform**"，文档域名从 `cloud.google.com/vertex-ai/...` 301 到 `docs.cloud.google.com/...`。⛔ 按旧名检索会漏页。

| 服务 | 数据驻留 | 不用于训练 | 政府云 | 认证级别 | 中国大陆可得性 | 主要来源 | 级别 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-: |
| **Azure OpenAI**（Models sold by Azure） | 静态数据留在客户指定 geography；⛔ **推理位置由部署类型决定**：`Global` 可在任意 Azure region 处理、`DataZone` 限 US/EU/APAC、`Standard` 限单 region。微软可**不经通知**向 data zone 增加 region | 有承诺，⛔ **带条件**：逐字 "are NOT used to train any generative AI foundation models **without your permission or instruction**"；另有无条件句 "The models are stateless: no prompts or completions are stored in the model" | **Azure Government** 可用（`usgovarizona` / `usgovvirginia`），含 `gpt-5.1`（仅 Data Zone Standard）/ `gpt-4.1` / `o3-mini` / `gpt-4o`。⛔ Gov 上**不支持** fine-tuning、batch、Agents、Evaluation | Commercial：FedRAMP High ✅ + DoD IL2 ✅；Government：FedRAMP High ✅ + IL2/IL4/**IL5WI**/**IL6** ✅。⚠️ **`Microsoft Foundry portal` 只到 IL2**——portal 与模型服务授权级别不同 | ⛔ **不可用。** 五条独立否定证据收敛（`docs.azure.cn` 无 OpenAI 条目、定价页 404、Foundry sovereign clouds 只列 Azure Government）。**无任何官方明文否定句** | [data-privacy](https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/openai/data-privacy) · [deployment-types](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types) · [Gov models](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure-gov) · [FedRAMP scope](https://learn.microsoft.com/en-us/azure/azure-government/compliance/azure-services-in-fedramp-auditscope) · [Azure China](https://learn.microsoft.com/en-us/azure/china/concepts-service-availability) | **M** |
| **AWS Bedrock** | 默认单区域留在调用 region；⛔ **`global.` inference profile 路由到任意商用 region**，且逐字 "can route requests to AWS Regions that are **not manually enabled** in your AWS account"。geographic profile 亦自陈 "your input prompts and output results **might move outside of your source Region**" | 承诺方式是**排除法**（比正面条款更硬）：Service Terms §50.3 的「可用于改进服务」白名单**不含 Bedrock**。FAQ 逐字 "No. Users' inputs and model outputs are not shared with any model providers"。2026 年新增账户级 `data_retention_mode: none`（"Zero data retention"） | **GovCloud (US-West / US-East)** 均可用，含 FIPS 端点。⚠️ **「可用」≠「已授权」**：明文授权清单只有 All Titan / Claude Sonnet 4.5 / 3.7 / 3.5 v1 / 3 Haiku / Llama 3 8B / 70B | FedRAMP **Class C（原 Moderate，East/West）** ✅ + **Class D（原 High，GovCloud）** ✅；DoD **IL2 / IL4 / IL5 / IL6（AWS Secret Region）** 五列全 ✅。⚠️ `Bedrock Agentcore` 只有 IL2 | ⛔ **不可用。** 两条正面证据：中国区服务清单（2026-02-28 更新）ML 类目仅 5 项、无 Bedrock；官方 endpoints 页无 `cn-north-1` / `cn-northwest-1` | [FAQ](https://aws.amazon.com/bedrock/faqs/) · [Service Terms](https://aws.amazon.com/service-terms/) · [cross-region inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) · [GovCloud Bedrock](https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/govcloud-bedrock.html) · [FedRAMP scope](https://aws.amazon.com/compliance/services-in-scope/FedRAMP/) · [DoD SRG scope](https://aws.amazon.com/compliance/services-in-scope/DoD_CC_SRG/) · [中国区服务](https://www.amazonaws.cn/en/about-aws/regional-product-services/) | **M** |
| **Google Vertex AI**（Gemini Enterprise Agent Platform） | 静态驻留与端点无关；⛔ **ML processing 位置完全由端点决定**，**global endpoint 逐字「don't provide regional isolation or data residency guarantees」**。EU 端点**排除英国与瑞士**。**Interactions API 的 `store` 默认为 `true`** | 合同层 Service Specific Terms **§18 Training Restriction** 逐字："Google will not use Customer Data to train or fine-tune any AI/ML models without Customer's prior permission or instruction"。⛔ **但「不训练」≠「不留存」**：abuse monitoring 会 log prompt（可申请豁免）、Grounding with Search 存 3 天**且无法关闭**、Grounding with Maps 存 30 天**且无法关闭**、in-memory 缓存默认开启（24h TTL，可关）。**Pre-GA 不受 CDPA 与数据驻留条款覆盖** | **Assured Workloads** 的 FedRAMP High / Moderate / IL4 / IL5 / **ITAR** / EU Data Boundary 各 package 均含 `Generative AI on Vertex AI`。⛔ 前置条件是必须用 Assured Workloads + Assured/Enhanced Support | Google Cloud 持 FedRAMP **High P-ATO**（无独立 Moderate，靠继承）+ DISA **IL2 / IL4 / IL5** PA；`Generative AI on ...` 四列全 ✅。⚠️ **逐模型前置条件**：逐字 "Models not explicitly listed as supporting US multi-regions **don't meet DoD IL5 commitments**"。ITAR package 逐字含 "includes Gemini models **3.x or greater**" | ⛔ **不可用。** 41 个 region 无任何中国大陆站点（最近为 `asia-east1` 台湾、`asia-east2` 香港）；Gemini API 可用地区清单**含台湾、不含中国大陆与香港** | [Service Terms](https://cloud.google.com/terms/service-terms) · [data governance](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/data-governance) · [data residency](https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/data-residency) · [Assured Workloads 支持产品](https://docs.cloud.google.com/assured-workloads/docs/supported-products) · [ITAR](https://cloud.google.com/security/compliance/itar) · [FedRAMP/DoD scope](https://docs.cloud.google.com/architecture/security/fedramp-dod-compliance-scope) · [regions](https://docs.cloud.google.com/compute/docs/regions-zones) | **M** |

#### ⛔ 三条对我们**最不利**的事实，必须先自己说出来

1. ⛔ **「涉密不能上云」在 2026 年已经失效。** Azure OpenAI 已获 DISA **IL6**（SECRET 级）授权，且已进入 **Azure Government Top Secret**（按 ICD 503 运行）。⛔ 若论文写「classified 场景只能本地部署」，会被一击驳回。来源：微软 compliance scope 表（**M**，IL6 ✅ 一格）+ [Azure Gov devblog](https://devblogs.microsoft.com/azuregov/azure-openai-authorization/) 逐字 "authorized for workloads at **all U.S. Government data classification levels**"（**S**，厂商博客二手于 DISA 授权书）。
2. ⛔ **ITAR 有专门的云通道。** Google 的 Assured Workloads **ITAR** control package 明文含 `Generative AI on Gemini Enterprise Agent Platform`；AWS ITAR 页逐字 "AWS GovCloud (US) supports compliance with … ITAR"，且明确 "**There is no formal ITAR certification**"——⛔ ITAR 是 region 属性，不是逐服务认证，所以「Bedrock 不在 ITAR 清单里」这个说法本身就是错的（**根本不存在这样一份清单**）。
3. ⛔ **我们自己的实验跑在公有云上。** 主臂用 `gpt-5.5` / `claude-opus-4-7`。⛔ 一篇论证「工业场景不能用公有云」的论文，其全部实验配置在该论证下**不可部署**。这是 internal consistency 问题，审稿人会问，必须在论文里主动交代。

### 1.2 仍然不够用的具体条件（逐条给证据）

下表按**证据强度**排序。⛔ **只有「强」级可以承重**；⛔ 「弱」级单独写进 motivation 会被打回。

| # | 条件 | 为什么公有云在这里确实不够 | 一手依据 | 级别 |
| :-: | :-- | :-- | :-- | :-: |
| **① 最硬** | 数据构成**中国法下的国家秘密** | 《保守国家秘密法》（2024-02-27 修订，2024-05-01 施行）**第三十一条（三）**是**无条件禁止**，⛔ 无任何附条件豁免：逐字「**使用非涉密信息系统、非涉密信息设备存储或者处理国家秘密**」。公有云不是经检查合格的涉密信息系统 ⟹ **不存在任何合规配置**。配套：第二十九条禁止「在互联网及其他公共信息网络……中传递国家秘密」；第三十条要求涉密系统分级保护、经检查合格方可投用 | [npc.gov.cn 全文](http://www.npc.gov.cn/npc/c2/c30834/202402/t20240227_434859.html) | **M / 强** |
| **② ** | 中国境内 + 数据被认定为「**重要数据**」 | **所有放宽通道都以「不含重要数据」为前置**：《促进和规范数据跨境流动规定》（网信办令第16号，2024-03-22 施行）第三条豁免逐字限「**不包含个人信息或者重要数据的**」，第五条末款逐字「前款所称向境外提供的个人信息，**不包括重要数据**」。重要数据出境始终落在第七条的国家安全评估上。叠加《网络数据安全管理条例》（国令790号，2025-01-01 施行）第三十七条、《网安法》**现行第三十九条**（CIIO 境内存储）、《PIPL》第四十条 | [令16号](https://www.cac.gov.cn/2024-03/22/c_1712776611775634.htm) · [网安法 2025 修正](https://www.cac.gov.cn/2025-12/29/c_1768735112911946.htm) · [PIPL](http://www.npc.gov.cn/npc/c2/c30834/202108/t20210820_313088.html) | **M / 强** |
| **③** | **汽车行业** + 重要数据 | 《汽车数据安全管理若干规定（试行）》（五部门令第7号，2021-10-01 施行）**第十一条**逐字「**重要数据应当依法在境内存储**」；第三条第一项把「**军事管理区、国防科工单位**……的地理信息、人员流量、车辆流量」直接列为重要数据 | [cac.gov.cn](https://www.cac.gov.cn/2021-08/20/c_1631049984897667.htm) | **M / 强** |
| **④ 最贴题** | 需要 LLM **对受控技术数据做推理**（⛔ 而非仅存储 / 传输） | **这是本轮最锋利的技术—法律交点。** ITAR **22 CFR 120.54(b)(1)** 的加密豁免有两个构成要件：(i)「the data is **not in an unencrypted form**」+ (ii)「the means of decryption are **not provided to any third party**」。⛔ **LLM 推理在架构上必须在服务方侧把 prompt 解密成明文 token 才能计算** ⟹ 两个要件**同时**破裂 ⟹ 加密豁免通道**在推理场景关闭**（对纯加密存储 / 传输仍开着）。后果由 §120.56(a)(4) + §120.50(a)(6) 具体化：**解密动作本身构成 export**。EAR **15 CFR 734.18(b)** 定义同构，结论平移 | [22 CFR 120.54](https://www.ecfr.gov/current/title-22/chapter-I/subchapter-M/part-120/subpart-C/section-120.54) · [15 CFR 734.18](https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C/part-734/section-734.18)（⚠️ 经 eCFR 官方 API 取 XML；网页版对本环境 302 到 `unblock.federalregister.gov`） | **M / 强**（⚠️ 「推理必须明文」是**技术事实、非法条内容**，论文中必须与法条分开陈述） |
| **⑤** | 受控技术数据涉及**中国主体 / 中国境内存储** | ITAR §120.54(a)(5)(iv) 排除 §126.1 国家；§126.1(d)(1) Table 1 逐字含 **China**（policy of denial）。EAR §734.18(a)(5)(iv) 排除 Country Group D:5，Supplement 1 to Part 740 的 "China (PRC)" 行 D:5 列标 X。⟹ ⛔ **无任何云配置可解** | 同上 eCFR | **M / 强**（⚠️ 但见 §5.2：这条与用 Qwen **互斥**） |
| **⑥** | **军工保密资质**单位 | 《武器装备科研生产单位保密资质管理办法》（2025-07-01 施行）第十一条（五）：外资**直接投资为零**、间接不超 **20%**、实际控制人不得为外国投资者；（六）关键人员须中国国籍、无境外居留权。第六条：涉密任务及其分包须由有资质单位承担 | [国家保密局](https://www.gjbmj.gov.cn/n1/2025/0604/c419767-40494024.html) | **M / 强**（⚠️ 具体技术要求在第二十条「另行制定」的审查标准中，**未公开**，不可引条文级细节） |
| **⑦** | 美国 SECRET 及以上，⛔ **且主体非 DoD / 联邦承包商** | IL6 要求 dedicated cloud infrastructure、**closed self-contained environment connected only to SIPRNet**、与非联邦租户**物理隔离**、持密美国公民运维，且「IL6 CSOs **may only be provided by CSPs under contract to the DoD or a federal agency**」。**论证形状要反过来用**：⛔ IL6 的存在不是「云能干涉密」，而是「**涉密场景的准入条件本身等价于私域隔离环境**」，只是该环境可以由云商建 | [Microsoft Learn IL6 页](https://learn.microsoft.com/en-us/azure/compliance/offerings/offering-dod-il6) 对 SRG §5.2.2.4 / §5.1.1 / §5.6.2 的引述 | **S / 中**（⛔ **SRG 原文未取得**：`dl.dod.cyber.mil` 404、`rmf.org` 403、`disa.mil` 超时、`public.cyber.mil` 返回 JS 壳页。条款号与页码**待人工核验**） |
| **⑧** | 美国境内运维人员含外籍（**deemed export**） | EAR **15 CFR 734.13(a)(2)** 逐字「Releasing or otherwise transferring "technology" or source code … to a foreign person **in the United States** (a "deemed export")」；§734.15(a)(2) 含「**written exchanges** with a foreign person」。⟹ ⛔ 「数据不出美国国境」**不足够**；这正是通用商用云不够、而 GovCloud 的 "US Persons only" 才是必要条件的原因 | [15 CFR 734.13](https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C/part-734/section-734.13) | **M / 强** |

#### ⛔ 三条「看起来能用、实际不能用」的——⛔ 红队特别标出，防止我们自己踩

| ⛔ 别用 | ⛔ 为什么不能用 |
| :-- | :-- |
| ⛔ **《生成式人工智能服务管理暂行办法》第二十条** | ⛔ **它不支持我们想要的结论。** 该办法**第二条第三款**逐字把「行业组织、企业、教育和科研机构……**未向境内公众提供**生成式人工智能服务的」明确**排除在适用范围外**。第二十条约束的对象是**境外服务提供者向境内提供服务**，执行手段是通知有关机构采取技术措施（即阻断）。⟹ 它带来的是**可用性障碍**（叠加三大云 LLM 在大陆不可用这一既有事实），**不是对企业内部使用行为的禁令**。[原文](https://www.cac.gov.cn/2023-07/13/c_1690898327029107.htm)（**M**） |
| ⛔ **TISAX / VDA ISA 禁止用云** | ⛔ **本轮未找到任何公开可引证据，且反向证据成立。** TISAX Participant Handbook **§4.3.3.6** 明确不要求供应商持有同级 label、只要求企业自行风险评估；其举例说明**排除外部服务的依据来自企业自身信息处理政策、而非 TISAX 禁令**。更糟：**AWS 与 Microsoft 本身持有 TISAX AL3 标签**。另有结构性理由说明为什么找不到：TISAX 结果**仅通过 ENX 平台交换、不公开**——这本身只能写成 limitation，不能反过来当「存在该禁令」的证据。[Handbook](https://portal.enx.com/handbook/tisax-participant-handbook.html)（**M**） |
| ⛔ **「classified 系统必须 air-gapped」（美国侧）** | ⛔ **未找到通用成文强制。** 32 CFR 117.18（NISPOM）通篇是 risk-based approach + USG authorizing official 批准，通篇检索无 "air gap" / "physically isolated" 类强制表述。CNSSI 1253 正文未取得；NSA/NCDSMO "Raise the Bar" 非公开（须 Intelink-U）。**中国侧相反有明文**（条件 ①），论证重心应放在中国侧 |

#### 关于 IEC 62443 / NIST SP 800-82 的诚实口径

NIST SP 800-82r3（2023-09，[官方 PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r3.pdf)，**M**）确实建议 IT/OT 分离、DMZ 架构、并写有「**considering where physical separation may be required** as opposed to logical separation」；⛔ **但它是 guidance / recommendations，不是 regulation**——措辞是 "should consider" / "may consider"。⛔ **它不能用来证明「某类工业控制系统被法律要求网络隔离」**，只能证明「权威技术指南推荐禁止企业网与控制网直连」。IEC 62443-3-3:2013 范围确含 zones/conduits 与 security levels，**但全文付费（CHF 380）未取得**，不得引用任何条文编号或条文内容。

### 1.3 处置建议

**处置：接受并降档。**

| ⛔ 不能再写的 | 改成 |
| :-- | :-- |
| ⛔ 「工业场景**普遍**不能用公有云 LLM」 | 「**在三类可举证的条件下**（中国国家秘密 / 中国重要数据境内存储 / 需要对 ITAR-EAR 受控技术数据做**推理**），公有云路径要么被无条件禁止、要么其唯一合规形态本身即等价于隔离部署」 |
| ⛔ 「classified 不能上云」 | ⛔ **整句删除。** 改为条件 ⑦ 的反向论证：**IL6 的准入条件（专用基础设施 / 仅连 SIPRNet / 与非联邦租户物理隔离 / 持密美国公民运维 / CSP 须与 DoD 有合同）本身就是私域隔离的定义**，且对非美主体结构性不可得 |
| ⛔ 「ITAR 禁止上云」 | 改为**精确版**：ITAR/EAR 的加密豁免（22 CFR 120.54(a)(5) / 15 CFR 734.18(a)(5)）**在 LLM 推理场景不适用**，因为推理必须在服务方侧产生明文，破坏 "not in an unencrypted form" 与 "means of decryption are not provided to any third party" 两个构成要件。⚠️ **同时必须写清反面**：豁免不适用 **≠** 禁止上云——回落后的合规路径正是 GovCloud / Azure Government，**所以 ITAR 单独证明不了「必须私域」，只能证明「必须放弃通用公有云」** |
| ⛔ 用 TISAX / IEC 62443 / 美国 air-gap 做承重 | ⛔ **全部移入 Limitations 或删除。** 见 §1.2 三条「别用」 |

⚠️ **降档后必须同时接受的代价**：剩下最硬的三条（①②③⑥）**全在中国法域**。⛔ 这使 motivation 具有强地域性，而 ICSE / FSE / ASE 的审稿人多数不在该法域内。这条代价必须自己先说，不能等审稿人说。

---

## 2. 反驳 2 · 「为什么不微调 / 蒸馏？」

> 审稿人原话：私域部署框架下，工业界的自然做法是拿内部数据微调一个模型，⛔ 而不是套一个 prompt 流水线。

### 2.1 ⛔ 先说最不利的三条——⛔ 它们真实存在且很硬

| # | 证据 | ⛔ 为什么它疼 |
| :-: | :-- | :-- |
| **①** | **Hsieh et al., Distilling Step-by-Step!**（Findings of ACL 2023，[arXiv:2305.02301](https://arxiv.org/abs/2305.02301)，**M**）：**770M T5 只用 80% 数据即超过 540B PaLM 的 few-shot prompting**；ANLI 上 770M 超 540B（约 **700×** 小） | ⛔ **它正面否证「小模型必须靠 prompt 流水线才能接近大模型」**——它说的是靠蒸馏就能**超过** |
| **②** | **NL2TL**（EMNLP 2023，[arXiv:2305.07766](https://arxiv.org/abs/2305.07766)，**M**）：微调 **T5-large（770M）** 在三个域 **95.13 / 95.03 / 96.73%**，⛔ 而 **GPT-4 few-shot 端到端只有 77.7%** | ⛔ **杀伤力最大，因为它就在形式化生成侧。** 审稿人只需问：「NL→LTL 上 770M 微调完胜 GPT-4，你凭什么说 NL→状态机缺陷发现不适用微调？」 |
| **③** | **Shin et al.**（**MSR 2025**，[arXiv:2310.10508](https://arxiv.org/abs/2310.10508)，**M**）：GPT-4 三种 prompting vs **17 个微调模型**、3 个代码任务 —— GPT-4+prompting **不能稳定超过**微调模型，⛔ MBPP 上被微调模型高出 **28.3pp** | ⛔ **这是 SE 自己的会议**给出的结论。审稿人引这一篇即可说「你们领域的实证研究不支持 prompting 优于微调」 |

次级两条同样要备答：**SODA**（**FSE 2025**，[arXiv:2408.03680](https://arxiv.org/abs/2408.03680)，**M**）蒸馏后的 6.7B 平均 Pass@1 **超过 ChatGPT**；**LoRA Land**（[arXiv:2405.00732](https://arxiv.org/abs/2405.00732)，⚠️ Predibase technical report、**非同行评审**）310 个 QLoRA 模型平均超 GPT-4 **10 分**，⛔ 且 **25 个 Mistral-7B adapter 可共驻一张 80GB A100**——这条直接击中「私域部署成本」这个卖点。

### 2.2 我们能怎么答（四步，每步都有 M 级引用，且不需要补跑微调基线）

1. **该子领域的同行也不微调，且写明了理由。** [arXiv:2604.00275](https://arxiv.org/abs/2604.00275)（Abdulkarim et al., McGill, 2026-03-31；⛔ preprint，⛔ 录用状态未核）**逐字**："with larger LLMs (>1B parameters) this approach becomes harder and less common due to **training costs and lack of sufficient training data**"。这篇的任务与我们几乎重合（非结构化 NL 需求 → UML 状态机全自动生成，8 个系统 + 专家参考模型）。⟹ **「套 prompt 流水线」不是我们取巧，是 2026 年该子领域的主流做法。**（**M**，[verification_log.md](./verification_log.md) §V2 已一手复核）
2. **本任务的监督目标不唯一，⛔ 微调的前提不成立。** [arXiv:2404.06371](https://arxiv.org/abs/2404.06371)（Ferrari, Abualhaija, Arora）**明确拒绝使用单一 ground truth**，逐字两条理由："(a) more than one diagram exists that satisfies the same requirements"、"(b) existing ground truths are limited"；改测人类评审者间一致性，30 个模型交叉评审 **square-weighted Cohen $\kappa = 0.67$**。⟹ **没有唯一目标，就没有干净的监督信号。**（**M**）
3. **数据量落在「微调会掉点」的区间。** [arXiv:2409.03454](https://arxiv.org/abs/2409.03454)（Vieira et al.）在**一家软件行业公司的内部私域数据**上证明：Llama 3 8B Instruct 用 **1k / 2k 样本微调时性能比未微调 baseline 更差**，需到 207k 才大幅改善。而 RE 领域数据稀缺有系统性映射研究背书（[arXiv:2510.18787](https://arxiv.org/abs/2510.18787)，EASE，45 篇 primary studies / 62 数据集，逐字 "data scarcity remains a widely reported limitation"），公开需求语料的天花板是 PURE 的 **79 份文档 / 34,268 句且无标注**（[RE 2017, DOI 10.1109/RE.2017.29](https://doi.org/10.1109/RE.2017.29)）。⟹ **工业客户手上恰恰是 1k–2k 这个量级。**（**M**）
4. **微调还要付通用能力的账，而本任务需要通用推理。** [arXiv:2308.08747](https://arxiv.org/abs/2308.08747)（Luo et al.）在 1b–7b 范围**普遍观察到**遗忘，⛔ 且规模越大遗忘越严重。⚠️ **反例必须一起给**：[arXiv:2509.20758](https://arxiv.org/abs/2509.20758)（**ICLR 2026**）证明调小学习率即可大幅缓解——**但它自己逐字承认 "no method completely eliminates the trade-off"**，而工业私域没有逐任务调参找那个学习率的预算。（**M**）

### 2.3 ⛔ 必须主动承认的边界——⛔ 不写这句，整条会被 NL2TL 一篇打穿

⛔ **在目标唯一、可批量生成、评测确定的形式化翻译任务上（NL→LTL / STL / regex），微调 770M 级模型确实是更优路线**（[arXiv:2305.07766](https://arxiv.org/abs/2305.07766)、[arXiv:2206.01962](https://arxiv.org/abs/2206.01962)）。我们的任务与之不同**不在于「形式化」，而在于三点**：目标不唯一（$\kappa = 0.67$）· 判定需跨制品语义推理 · 没有可批量合成的标注。⛔ **这条区分必须在论文里显式写出来。**

**一条对我们有利的空缺**：本轮检索**未找到任何「需求 → UML/状态机（或需求 → 模型缺陷）」上的微调 vs prompting 头对头实证对比**（关键词见 [small_model_papers.md](./small_model_papers.md) 与本轮检索记录）。该基线在这个子领域**根本不存在**，⛔ 因此可以正当地列为 limitation + future work，⛔ 而不是必须补跑。

### 2.4 处置

**附引用理由驳回 + 部分移入 Limitations。** 驳回的部分是「微调是这里的自然做法」（用 §2.2 四步）；⛔ 移入 Limitations 的部分是「⛔ 我们没有跑微调对照」，并显式引 §2.3 的检索空缺说明该对照在子领域内无先例。

---

## 3. 反驳 3 · 移动靶（「小模型半年就被取代」）

**这一刀可以整个反手。** 本轮找到的材料**把「模型会过时」从我们的弱点变成了社区已承认的系统性问题，而开放权重模型正是被推荐的缓解手段**。

| # | 材料 | 逐字 / 数字 | 怎么用 |
| :-: | :-- | :-- | :-- |
| **①** | **Angermeir et al., ICSE 2026**（[arXiv:2510.25506](https://arxiv.org/abs/2510.25506)，DOI [10.1145/3744916.3773207](https://doi.org/10.1145/3744916.3773207)，**M**） | 85 篇 ICSE/ASE 2024 LLM 论文，18 篇看似可复现 → 实际可执行 **5** → **完全复现 0**。逐字："**The only factor directly linked to LLMs was the usage of deprecated models, an issue exclusive to commercial models.**" 另逐字："**the hurdles towards deprecation for open source models are higher**" | **主引文。** ⛔ 把它写成「领域现状」而非「我们的缺陷」，并据此把用开放权重模型说成**该文明确推荐的缓解手段** |
| **②** | **Williams et al., ICSE-NIER 2026**（[arXiv:2510.26538](https://arxiv.org/abs/2510.26538)，**M**） | 177 篇 ICSE 论文（2023–2025）：**136/177（76.8%）用开放模型**。逐字："replicability is hindered as these models are **frequently deprecated** when newer versions are released" | 用 76.8% 堵住「你为什么不用 GPT」 |
| **③** | **Sallou, Durieux & Panichella, ICSE-NIER 2024**（[arXiv:2312.08055](https://arxiv.org/abs/2312.08055)，pp. 102–106，DOI [10.1145/3639476.3639764](https://doi.org/10.1145/3639476.3639764)，**M**；用户点名的这篇**标题、作者、年份、venue 全部属实**） | 逐字："…notable changes in the output of OpenAI models have been observed … **potentially making the presented results obsolete**"。紧接一句更有用："distinguishing whether the improvements claimed in the new contribution are the result of **changes to the LLMs' models** or due to the **novelty of the contribution** becomes a complex task" | **第二句是归因论证**：⛔ 用会漂移的闭源模型使「方法贡献 vs 模型进步」无法区分 ⟹ 固定开放权重模型是**归因清晰性的前提**，不是妥协 |
| **④** | **Ouyang et al., ACM TOSEM 34(2) art.42**（DOI [10.1145/3697010](https://doi.org/10.1145/3697010)，[arXiv:2308.02828](https://arxiv.org/abs/2308.02828)，**M**；用户点名的这篇亦属实，⚠️ arXiv 初版题名不同，引用用 TOSEM 定名） | 829 个代码生成问题，零相同测试输出的任务比例 **75.76% / 51.00% / 47.56%**；逐字 "even the smallest temperature (i.e., temperature=0) could not guarantee the determinism"。其 §6.3 文献调查：76 篇中仅 **21.1%（16/76）** 在实验设计中考虑非确定性 | **为我们的 `hit@1 / hit@3 / hit@all` 多轮口径提供方法学正当性**，且这是**多数同行论文抵御不了的第三刀** |

⛔ **一条必须绕开的陷阱**：⛔ Chen, Zaharia & Zou（[arXiv:2307.09009](https://arxiv.org/abs/2307.09009)，HDSR 6(2) 2024）的「GPT-4 代码可执行率 52%→10%」**是 markdown 围栏造成的假象**——原文自陈 June 版本加了 ` ```python `，剥离非代码文本后（原文 Table 4）**六月为 70%、反而优于三月的 52%**。**Sallou et al. 引的正是未剥离的数字且未带 caveat**；照抄会被读过原文的审稿人抓住。若要引，改引「版本漂移会改变**输出形态**、进而使下游解析与评测口径失效」——对我们这种要解析结构化产物的工作，这个框法比性能退化更贴题。

另一条值得追的先例：[arXiv:2606.04739](https://arxiv.org/abs/2606.04739)（Kaniewski et al., Revisiting Vul-RAG）把原工作改造为**完全本地开放权重**运行并复现成功，⚠️ 搜索摘要称观察到约 **0.30 pairwise accuracy 的性能平台期，即便更新更强的模型也未突破**。⛔ **级别 I，未开原文**——若属实，它给出一个反刀 A 的强论点（**模型代际更新未带来实质提升**），但引用前必须自查。

### 3.1 处置

**附引用理由驳回。** 四层写法：① 承认并引社区共识（材料 ①③）· ② **把开放权重模型说成缓解手段而非妥协**（材料 ①②）——**Qwen-32B 可被任何人在任何时刻重新下载并精确重跑，⛔ GPT-5.5 不能** · ③ 引 Sallou 的归因论证（材料 ③）· ④ 显式限定主张的时效性，给精确 `模型@版本` + 日期 + 推理配置。

---

## 4. 反驳 4 · 泛化性（「换个模型还成立吗」）

### 4.1 社区惯例远比担心的宽松，且不存在「≥3 模型」硬要求

| 来源 | 结论 | 级别 |
| :-- | :-- | :-: |
| **Angermeir ICSE'26** | 逐字：「**In total, 43 of 85 articles compared multiple LLMs.**」⟹ ICSE/ASE 2024 的 LLM 论文里约**半数只用单一模型**。⚠️ **原文没有写出补数 42/85，那是推算**，引用时须写成「43 of 85 compared multiple LLMs，即约半数仅评测单一模型」 | **M** |
| **Baltes et al., 22 人，EMSE 已接收**（[arXiv:2508.15503](https://arxiv.org/abs/2508.15503) + 活体版 [llm-guidelines.org](https://llm-guidelines.org/)） | 八条 guideline 中唯一带数量含义的是 **G6**：「Researchers **should** include an open LLM as a baseline when using commercial models」⟹ 含义下限 = **2**，且是 `should` 不是 `must`。**我们本来就用开放权重模型，这条自动满足。** 官方定义逐字：`must` = requirement（通常是披露义务），`should` = desired practice。Advice for Reviewers 逐字：开放基线 "expected only when LLM use is central"，否则找 "a convincing argument for why it is impractical" | **M**（⚠️ G6 逐字核自官方配套站点；论文 PDF §5.6 未取到，定稿版措辞差异无法排除） |
| **ACM SIGSOFT Empirical Standards**（[标准索引](https://www2.sigsoft.org/EmpiricalStandards/docs/standards)） | ⛔ **没有 LLM/AI 专用 standard**。**反向弹药两条**：Data Science standard 把「'Needs more data' as a generic criticism **without a clear, justified reason**」列为 **illegitimate review comment**；General Standard 把「Setting **arbitrary minimum sample sizes** or other data requirements, based on neither power analysis nor theoretical saturation」列为 **invalid criticism** | **M** |
| **ICSE 2027 Research Track CFP** | 5 条评审标准全文**无任何模型数量条款** | **M** |

⚠️ **反向弹药要慎用、放最后**：⛔ 若审稿人给了理由（「你的核心主张是方法通用性，而通用性主张需要跨模型证据」），这两条**不适用**，硬顶反伤自己。

⛔ **一条纠正**：**Hou et al. TOSEM SLR**（395 篇，DOI [10.1145/3695988](https://doi.org/10.1145/3695988)）**没有**「每篇用几个模型」的分布统计——其 RQ1 做的是**模型分类**（按架构），⛔ 不是每篇的模型计数分布。**不要假设那句话存在。**（级别 **I**，只读了摘要页，全文 §RQ1 未核）

### 4.2 三种可用的写法（逐字范例）

| 招法 | 逐字范例 | 适用性 |
| :-- | :-- | :-- |
| **重新界定 aim** | **LIBRO, ICSE 2023**（[arXiv:2209.11515](https://arxiv.org/abs/2209.11515)）§VII 逐字：「**our aim is not to assess whether a specific instance of Codex has general intelligence about testing: our aim is to investigate the extent to which LLM architectures augmented with post-processing steps can be applied to the task**」。⚠️ 它**只用 Codex 一个模型**，且 external validity **完全没把模型数量列为威胁** | **对我们最适用**：我们的贡献是**谓词词表 + 契约门 + 修订循环这一方法结构**，⛔ 不是「Qwen-32B 有多强」 |
| **机制型 agnostic** | **FeatureSHAP**（[arXiv:2512.20328](https://arxiv.org/abs/2512.20328)）：agnostic 不靠模型数量，靠「operates **only on observable input–output behavior**」 | **若我们的框架只消费结构化输出、⛔ 不依赖模型内部信号**，可把 agnostic 论证成**接口性质**，模型数量只作补强，**2 个就够** |
| **一致性救援句** | [arXiv:2510.03029](https://arxiv.org/abs/2510.03029) §7.2 逐字：「…the results may not generalise across all generative coding models. **However, there are observations that are consistent on all LLMs that we studied. These observations should be able to generalise to other ML models.**」 | 把泛化损失**限定在跨模型不一致的结论上**，同时把跨模型一致的结论救出来 |
| **成本显式权衡** | **Yuan et al., ASE 2024**（[arXiv:2406.18181](https://arxiv.org/abs/2406.18181)）§4 逐字：「the current experiments … have spent **3,000 A100 GPU hours**, and our experimental design **balances conclusion generalizability and evaluation costs well**」 | 三步结构（选模准则 + 只声称 "to some degree" + **把算力成本写成显式权衡**）值得整段照搬 |
| **最短认账句（下限锚点）** | **Su & McMillan, EMSE**（[arXiv:2505.12118](https://arxiv.org/abs/2505.12118)）§3.9 逐字：「The threats to external validity are that different models might generate different results. We mitigate this threat by using two different commercial LLMs and two different open-souce LLMs.」（`open-souce` 为原文拼写错误） | **两句话在 EMSE 过审。** 用 2 个模型时这是下限锚点 |
| **规模跨度替代模型个数** | **HoarePrompt**（[arXiv:2503.19599](https://arxiv.org/abs/2503.19599)）§7 逐字：「models of diverse sizes (7B to 72B), including **Qwen-32B-Coder** … observed trends suggest broad applicability, **especially relevant given industry shifts toward proprietary small and mid-sized models**」 | **与我们处境高度相似**（同样用 Qwen-32B-Coder），且把模型选择反向说成**贴近实践** |

⛔ **反面教训**：**AutoProbe**（[arXiv:2510.02934](https://arxiv.org/abs/2510.02934)）用 6 个模型，⛔ 结果**自己否证了强版本主张**（Code Llama 上 F1 从 intra-model 0.77 掉到 cross-model 0.52，结论 "correctness-related representations remain **model-specific to some extent**"）。⟹ **若方法依赖模型内部表征或模型特有行为，多测模型反而会证伪 agnostic 主张。** 先想清楚主张哪一版 agnostic，再决定测几个。

### 4.3 ⛔ Wohlin 的坑

书目已核实：2012 版 Springer DOI [10.1007/978-3-642-29044-2](https://doi.org/10.1007/978-3-642-29044-2)；⛔ **DBLP 把 2024 版标为 `Second Edition`，⛔ 网上普遍把 2012 版称「第二版」是错的**——引 2012 版就只写 2012。**external validity 的逐字定义本轮未取到**（Springer 全线返回 WAF challenge），**现在不能写带引号的 Wohlin 定义句**；但按四分类组织章节结构并写 "based on Wohlin et al. 2012"（不加引号）已有 EMSE 先例。

### 4.4 处置

**附引用理由驳回。** 顺序：① 先按 LIBRO 招法重新界定 aim · ② 走机制型 agnostic · ③ threats 里用一致性救援句 + 规模跨度 + 成本显式权衡 · ④ 数字兜底（43/85）。⛔ **反向弹药（SIGSOFT invalid criticism）只在审稿人不给理由时用，⛔ 且放最后。**

---

## 5. 我们没想到的反驳

> ⛔ 本节是红队的主要价值所在。⛔ 下面 §5.1 和 §5.2 各自都能单独杀死这条 story，而 §1 的全部合规调研对它们**一点用都没有**。

### 5.1 ⛔ 刀 · 私域部署 ⟹ 小模型，⛔ 这个推理不成立，且它的补救前提与动机自相矛盾

⛔ **本地部署完全可以部署大模型，只要有卡。** 2026 年的开放权重模型早已覆盖到 SOTA 邻域（DeepSeek / Qwen / Llama / GLM 的旗舰档），⛔ 而这些同样可以私域部署。⟹ **「不能用公有云」推不出「必须用 32B」，只推得出「必须用开放权重」。**

要补上这一步，需要额外前提：**单卡预算 / 边缘设备 / 无 GPU 集群**。⛔ **而这个前提与 §1.2 里唯一守得住的那些场景直接矛盾**：

| §1.2 里守得住的场景 | ⛔ 它的 GPU 预算 |
| :-- | :-- |
| 中国国家秘密 / 军工保密资质单位 | ⛔ **国防科工单位买得起 GPU 集群。** 这恰恰是最不缺算力预算的一类主体 |
| 汽车行业重要数据 | ⛔ **主机厂同样买得起。** 一个 OEM 的年度 IT 预算远超几台 H100 |
| ITAR / DoD 承包商 | ⛔ **同上。** 且 §1.2 条件 ⑦ 的 IL6 环境本身就是重资产 |

⛔ **也就是说：动机越硬的场景，「必须用小模型」这个前提越站不住。** ⛔ 反过来，真正受单卡约束的场景（中小供应商、边缘设备、个人开发者）**恰恰不是**能举出成文合规约束的那些。

**我们的回答（诚实版）**：⛔ **我们答不上「必须小」。** 能答的只有**弱化版**：私域部署下模型规模是一个**可调的成本轴**，而**在该轴上向下走时方法学补偿是否能维持产出质量**，是一个独立于「必须」的经验问题。⛔ 这意味着 story 必须从「不得不用小模型」改写成「**若要在私域预算内向下调规模，方法学补偿能走多远**」——强度显著下降，但这是唯一诚实的形态。

**处置：接受并降档。**

### 5.2 ⛔ 刀 · Qwen 的来源国与我们守得住的动机场景**互斥**

⛔ 这不是「政治敏感」这种软问题，⛔ 而是**由我们自己引的法条导出的硬矛盾**：

| 动机场景 | ⛔ 用 Qwen 的后果 |
| :-- | :-- |
| **ITAR / EAR 受控技术数据**（§1.2 条件 ④⑤） | ⛔ **直接互斥。** 22 CFR §126.1(d)(1) Table 1 把 **China** 列为 policy of denial；EAR Country Group **D:5**（U.S. Arms Embargoed Countries）同样含 China (PRC)。一个论证「我们的方法服务于 ITAR 场景」而选用中国来源模型的论文，在该场景的实际读者眼里是**自相矛盾** |
| **美国 DoD IL4/IL5/IL6**（§1.2 条件 ⑦） | ⛔ 同上，且更严格（供应链审查、人员国籍限制） |
| **欧洲汽车 / TISAX**（⛔ 本就无证据，见 §1.2） | ⚠️ 虽无成文禁令，但欧美 OEM 对模型权重供应链的尽调（后门 / 数据投毒 / 出口管制）会构成实际阻力。**本轮未找到可引证据**，只能作为**未量化风险**记录，不得写成事实 |
| **中国国家秘密 / 重要数据 / 军工资质**（§1.2 条件 ①②③⑥） | **只有这一类与 Qwen 匹配。** ⛔ 但它同时是 §1.3 已指出的**强地域性代价** |

⛔ **结论很难看：我们守得住的动机里，只有中国法域这一支与我们要用的模型不冲突；⛔ 而 ICSE / FSE / ASE 的多数审稿人不在该法域内。**

⚠️ **另有一个内部矛盾**：论文的语料是 BSN / CARA / Elevator / Microwave / PBA / Radar / Stopwatch / TCS / VHL 这类**公开西方数据集**（见根 [CLAUDE.md](../../../../CLAUDE.md) §数据集信息）。⛔ 用公开数据集论证「数据不能出境」，本身就是 motivation 与 evaluation 的错配——**我们评测用的每一条数据都可以合法送进公有云。**

**处置：移入 Limitations，⛔ 且必须写透。** 具体：① 明写模型选型的地域适配边界 · ② 明写语料的公开性使 motivation 无法在评测中被检验 · ③ ⛔ **不得**在 ITAR / DoD 场景上做任何 claim。

### 5.3 ⛔ 刀 · 成本归一化后增益可能消失

⛔ 如果我们给小模型加了多轮 self-critique / 修订循环，⛔ 其**总推理成本可能超过大模型单轮**。审稿人会要求 **cost-normalized comparison**，而这个要求有强先例：**Baldur（FSE 2023，DOI [10.1145/3611643.3616243](https://doi.org/10.1145/3611643.3616243)）** —— 仓库自己的 [assertion_output_form_evidence.md](../assertion_output_form_evidence.md) 已登记其教训：**只抽掉诊断输出 → 按推理成本归一后，增益不再超过纯生成基线**。

更直接的同域证据在 [small_model_papers.md](./small_model_papers.md)：2026 年单测生成的复现研究发现**朴素提示胜过四条带执行反馈的流水线、⛔ 而调用量只有一半**。⛔ ⟹ **我们必须在报 `hit` 的同一张表里报 token / 墙钟 / 调用次数**，否则这一刀会在 rebuttal 阶段才被砍，那时补不了。

**处置：接受并降档**（把成本列写进主结果表，⛔ 不放 appendix）。

### 5.4 ⛔ 刀 · 若真那么涉密，正确答案可能是「不用 LLM」而不是「用本地 LLM」

⛔ 这一刀最尖锐，⛔ 因为它把我们的动机反过来用：**如果场景涉密到连公有云都不能碰，那么在涉密网络里引入一个不可解释、可能记忆输入、日志可能外泄的生成模型，本身就要过一轮审批**——而《保密法》第三十条要求涉密信息系统「**经检查合格后，方可投入使用，并定期开展风险评估**」。我们**无法证明**一个本地部署的 LLM 能通过该检查。

⚠️ 更糟的是：军工保密资质的**具体技术审查标准与评分标准**按该办法第二十条「**另行制定**」，⛔ **未公开**（见 [regulatory_ledger.md](./regulatory_ledger.md)）。⟹ **我们连「本地 LLM 能不能过审」这个问题都无法查证**，更别说论证。

**我们的回答**：⛔ **答不上。** 只能诚实写成 Limitations：本文论证的是「若该场景允许使用 LLM，则该 LLM 必须私域部署」——⛔ **前件的成立性不在本文论证范围内**。这是一个条件式动机，强度弱于无条件动机，必须自陈。

**处置：移入 Limitations。**

### 5.5 ⛔ 刀 · 「接近 / 相当」没有判据

⛔ 导师原话是「达到的效果能和最新的全量 llm 相当」。⛔ **「相当」是什么？** 90%？95%？统计不显著？没有事前登记的判据，事后无论结果如何都能被说成「相当」或「不相当」——这按仓库根 [CLAUDE.md](../../../../CLAUDE.md) §3.5 第 4 条属「评测口径迁就结果」，**C 级**。

[verification_log.md](./verification_log.md) §V1 已给出一个可借用的先例句式（Zadenoori et al. 的「2% 可接受」），⛔ **但同时裁定我们四个前置条件一个都不满足**，⛔ 且只能用于比较 **B**（小模型+我们的方法 vs SOTA+我们的方法），不能用于比较 **A**（我们的方法 vs 朴素基线）。

**处置：接受并降档 —— ⛔ 判据必须在跑之前写死并 push**（根 [CLAUDE.md](../../../../CLAUDE.md) §3.5.1）。建议形态：先测代次内噪声底，再把「相当」定义为「差值落在噪声底的 $k$ 倍内」，$k$ 事前定死。

### 5.6 ⛔ 刀 · 「工业场景」的举证责任

⛔ 我们**没有工业合作方、没有工业案例、语料是公开数据集**。⛔ 在 RE / SE 社区，声称工业动机而无工业证据是常见的被打点。**对照**：[small_model_papers.md](./small_model_papers.md) 记录的 MSR 2025 那篇（[arXiv:2503.17998](https://arxiv.org/abs/2503.17998)）用**问卷实证**支撑动机（46.2% 受访者所在公司限制外部服务器工具，保密 34.6%、成本 11.6%），**我们没有对应物**。

**处置：接受并降档 + 移入 Limitations。** 若时间允许，一份小规模从业者问卷是**性价比最高的补强**（⛔ 但那是新工作量，⛔ 不在 N1a 范围）。

### 5.7 ⛔ 刀 · 为什么是 **32B**、为什么是 **Qwen**

⛔ 需要理由，⛔ 而目前没有成文的。[route_selection_and_v47_plan.md](../../discover_matrix/docs/findings/route_selection_and_v47_plan.md) §1.2 已给出部分技术依据（`Qwen/Qwen3.6-27B` dense、单卡 BF16 **55.58 GB**、Apache-2.0；排除 `gpt-oss` 因其 128K 是从 4K base 做 32× YaRN 外推），这可以写成选型准则。**但它回答的是「在 30B 档里选谁」，不回答「为什么是 30B 档」**（⟸ §5.1 的同一个洞）。

⚠️ 另注：⛔ 导师给的口径是 "qianwen32b"，而当前推荐是 `Qwen3.6-27B`。**论文里不得写 "Qwen-32B" 而实际跑 27B**，这属版本披露问题（⟸ §4.1 Baltes G2）。

**处置：接受并降档**（把选型准则写清，⛔ 不假装「必须」）。

### 5.8 ⛔ 刀 · 私域部署的 TCO 可能高于 API

⛔ 若 motivation 掺入成本论证，⛔ 会被算账打回：一张 H100 的 TCO + 运维人力，对多数中小规模用量而言高于按 token 计费。更糟的是 **LoRA Land**（[arXiv:2405.00732](https://arxiv.org/abs/2405.00732)）的那个数字——**25 个 Mistral-7B adapter 可共驻一张 80GB A100**——它同时打击「私域成本」和「必须用 prompt 流水线」两个点。

**处置：附引用理由驳回 —— ⛔ 但驳回的方式是「不提成本」。** 若 motivation 是合规，⛔ 成本论证**不该出现**；一旦出现就要接受成本审查。两者混写是自找。

---

## 6. ⛔ 我们答不上来的（诚实清单）

> ⛔ 本节不做任何缓和。⛔ 每条都写清「答不上什么」与「要答上需要什么」。

| # | ⛔ 答不上来的 | ⛔ 要答上需要什么 |
| :-: | :-- | :-- |
| **1** | ⛔ **「私域部署 ⟹ 必须用小模型」** | ⛔ 需要一个与 §1.2 强条件**不矛盾**的算力约束场景。本轮**没找到**。且 §5.1 的表说明这两者在结构上倾向于互斥 |
| **2** | ⛔ **「小模型 + 我们的方法 ≈ 大模型」** | ⛔ **一个数都没有**（属 N1b，硬依赖 M1）。而已知同向证据全指向反面：主臂 −15.82pp、Stroebl et al. 的不可能性定理（[arXiv:2411.17501](https://arxiv.org/abs/2411.17501) 逐字 "no amount of inference scaling of weaker models can enable them to match the single-sample accuracy of a sufficiently strong model"，preprint）、以及 [small_model_papers.md](./small_model_papers.md) 记录的「模型裸能力差距（89 题）> 任何脚手架策略差距（最大 35 题）」 |
| **3** | ⛔ **「可断言可追溯」与「私域部署」之间的因果连接** | ⛔ **没有因果连接，这是两个独立卖点拼在一起。** 审稿人问「可断言可追溯跟私域部署有什么关系」时，诚实答案是「没关系」。绑得越紧越可疑 |
| **4** | ⛔ **「涉密网络里能不能引入 LLM」** | ⛔ 《保密法》第三十条要求经检查合格；军工审查标准**未公开**。无法查证，只能写成条件式动机（§5.4） |
| **5** | ⛔ **为什么我们自己的实验跑在公有云上** | ⛔ 可以交代（方法验证 vs 部署形态是两件事），但这是**辩解不是论证**。唯一硬解是真的在本地跑一遍，那就是 N1b |
| **6** | ⛔ **欧美汽车 / 航空甲方合同禁止用云的公开证据** | ⛔ **本轮未找到，且反向证据成立**（TISAX §4.3.3.6 + AWS/Microsoft 持 AL3）。结构性原因：TISAX 结果仅在 ENX 平台内交换、不公开。这只能写成 limitation，不能倒过来当证据 |
| **7** | ⛔ **「工业场景」的举证** | ⛔ 无工业合作方、无工业案例、语料全公开。需要一份从业者问卷或一个工业 case study |
| **8** | ⛔ **微调对照** | ⛔ 没跑。可用「该子领域无此对照先例」（§2.3）作为 limitation 的支撑，但那不是答案，是缓刑 |
| **9** | ⛔ **「相当」的判据** | ⛔ 未定义。必须在跑之前写死并 push（§5.5） |

**一句话**：⛔ **第 1、2、3 条是结构性的，⛔ 不是靠多查文献能补上的。** 它们要么需要新实验（N1b + M1），要么需要把 story 改写成更弱的形态。

---

## 7. 检索过程与核验状态

### 7.1 本轮做了什么

四路并行调研 + 主 session 综合：① Azure OpenAI 合规（一手 learn.microsoft.com / fedramp.gov）· ② AWS Bedrock + Google Vertex 合规（一手 docs.aws.amazon.com / docs.cloud.google.com / 各 services-in-scope 页）· ③ 微调 vs prompting 文献（arXiv / ACL Anthology / IEEE / ACM DL）· ④ SE threats-to-validity 惯例（arXiv / ACM DL / llm-guidelines.org / SIGSOFT Empirical Standards）· ⑤ 法规查证（cac.gov.cn / npc.gov.cn / gov.cn / eCFR API / ENX portal / NIST）。

⛔ **覆盖边界**（按伞 PR [#179](https://github.com/HansBug/research_ideas/pull/179) §4.2 第 8 条）：⛔ 这**不是** systematic review。检索是关键词驱动的机会性检索。凡本文件写「未见」「未找到」的，其有效范围仅限**本轮实际访问过的来源与关键词**，**不得**读成「据我们所知不存在」。

### 7.2 ⛔ 访问异常记录（⛔ 不得据此断言事实不存在）

| 目标 | 异常 | 处置 |
| :-- | :-- | :-- |
| `www.ecfr.gov` 网页版 | 302 → `unblock.federalregister.gov` | 改用 eCFR 官方 API 取 XML，成功；全部 CFR 引文出自此 |
| **DoD Cloud Computing SRG 原文** | `dl.dod.cyber.mil` 404 · `rmf.org` 403 · `disa.mil/.ashx` 超时 · `public.cyber.mil/dccs/` 返回 JS 壳页 | ⛔ §1.2 条件 ⑦ 的条款号与页码**退为 Microsoft Learn 引述**，待人工核验 |
| `marketplace.fedramp.gov` | ⛔ **整站已 301 到 `fedramp.gov/marketplace`**；旧路径 404；`api.fedramp.gov` TLS EOF | 改用 `fedramp.gov/marketplace/products/` |
| `web.archive.org` | ⛔ 本环境 WebFetch **直接拒绝** | ⛔ Azure abuse monitoring 的「30 天」历史表述**无法取证**，见 §7.3 |
| Springer（Wohlin / Runeson & Höst） | WAF challenge（3038B JS）+ IdP 鉴权重定向 | ⛔ **不能写带引号的 Wohlin 定义句** |
| IEC 62443-3-3:2013 | 付费墙 **CHF 380** | ⛔ 只引「标准存在 + 范围含 zones/conduits」，不引条文 |
| ACM DL（PEARC'25 k-shot 研究，[DOI 10.1145/3708035.3736091](https://dl.acm.org/doi/10.1145/3708035.3736091)） | **403** | ⛔ 其「ICL 全面落后微调」的结论**若成立对我们不利**，未核，**级别 I** |
| `azure.microsoft.com` products-by-region 表 | 内容截断（"Content truncated due to length"） | ⛔ 未能从权威页直读 China 列；结论改由五条其他一手证据收敛 |
| BMB17 / GJB 系列 · 军工审查标准 · VDA ISA 目录 · NSA "Raise the Bar" | ⛔ **不公开 / 需资质 / 需注册** | ⛔ 一律不引条文内容 |

### 7.3 ⛔ 本文件内所有 **I** 级与待核验项（⛔ 不得写成事实句）

1. ⛔ **Azure abuse monitoring 的保留期限。** 现行两页一手正文**均无天数**；⛔ 「30 天」仅见于 MS Q&A 引用的 2024-09 存档快照与支持人员口头答复（**I**）。**不要把 30 天写成当前官方承诺。**
2. ⛔ **FedRAMP Marketplace 的字段标签措辞**（"FedRAMP Certified" / "Class C" / "Class D"）。⛔ 两个条目页返回工具摘要而非原始 HTML，疑为 2026 站点改版新术语，**待人工打开确认**（**S**）。
3. ⛔ **Azure OpenAI 是否亦覆盖 FedRAMP Moderate。** ⛔ 微软 scope 表只有 High 与 DoD IL 列，**无 Moderate 列**，未找到一手明文。
4. ⛔ **FedRAMP Marketplace 与 Google 自家 scope 文档冲突**：⛔ Marketplace 的 GCP High 服务清单（111 项）**无** `Generative AI on ...`，而 Google scope 表 ✅ FedRAMP High。原因未定，不裁定。
5. ⛔ **Google 每模型的 US/EU multi-region 驻留矩阵**（勾选列在文本抽取中丢失）。⚠️ 这是 IL5 结论的**前置条件**（逐字 "Models not explicitly listed as supporting US multi-regions don't meet DoD IL5 commitments"），需人工看表。
6. ⛔ **AWS「cross-region inference 是否默认行为」**：⛔ 官方**未找到**「默认启用」的明文总述。能写的只有「选用 global inference profile 时会路由到全球任意商用 region，且可路由到账户未启用的 region」。
7. ⛔ **Google "EU Sovereign Controls" 品牌名下 Vertex 的覆盖范围**：⛔ `cloud.google.com/sovereign-cloud` 抓到的是营销页。EU 主权侧目前只有 Assured Workloads 的三个 EU Data Boundary package 作依据。
8. ⛔ **Hou et al. TOSEM SLR 中「每篇用几个模型」的分布统计**：⛔ **无证据，勿假设存在**（只读摘要页）。最可能藏着该分布的是 Williams et al. 的 [figshare 附录](https://figshare.com/s/903589cadfd84c50613f)（本轮未开）。
9. ⛔ **[arXiv:2606.04739](https://arxiv.org/abs/2606.04739) 的「0.30 平台期」**（**I**，未开原文）。⛔ 若属实是反刀 A 的强论点，引用前必须自查。
10. ⛔ **Microsoft Product Terms 的三条引用**来自工具摘要而非原始文本（**S**）；⛔ 「by using a Microsoft Generative AI Service, Customer agrees its data may be stored and processed outside of its tenant's geographic region」这句**一手页面未复现**，仅见二手评论文章，**不得作为原文引用**。
11. ⛔ **DPA 正文条款**：`aka.ms/dpa` 落地页只是下载索引，⛔ 条款在 .docx 内，未解析（当前版本 May 2026）。
12. ⛔ **Angermeir 的 "42/85"**：⛔ **原文只写 43 of 85 compared multiple LLMs**，补数是推算。
13. ⛔ **《网络数据安全管理条例》的 gov.cn 原页未定位**：⛔ 现用生态环境部转载中国政府网版本，引用前建议再核 gov.cn。
14. ⛔ **多篇 arXiv 预印本的正式发表状态未核**：[2510.03029](https://arxiv.org/abs/2510.03029) · [2503.19599](https://arxiv.org/abs/2503.19599) · [2512.20328](https://arxiv.org/abs/2512.20328) · [2604.00275](https://arxiv.org/abs/2604.00275) · [2411.17501](https://arxiv.org/abs/2411.17501)。

### 7.4 ⛔ 两条主动纠错（⛔ 我们自己容易踩的坑）

1. ⛔ **Chen, Zaharia & Zou 的 52%→10% 是 markdown 围栏假象**，剥离后六月 GPT-4 为 **70%**（优于三月 52%）。⛔ Sallou et al. 引了未剥离数字且未带 caveat。**照抄会被读过原文的审稿人抓住。**
2. ⛔ **Ouyang et al. 不能当反驳 4 的 threats 范例** —— ⛔ 其 §5 external validity **只谈数据集与度量工具，完全没提模型数量**。它是反驳 3 与多轮口径的引文，不是反驳 4 的。

### 7.5 ⛔ 处置汇总

| 反驳 | 处置 |
| :-- | :-- |
| **1 · 公有云已合规** | **接受并降档**（§1.3）。⛔ 删除三条不能用的表述，保留三类可举证条件，自陈强地域性代价 |
| **2 · 微调 / 蒸馏** | **附引用理由驳回**（§2.2 四步）**＋ 部分移入 Limitations**（⛔ 未跑微调对照） |
| **3 · 移动靶** | **附引用理由驳回**（§3.1）。可整个反手：开放权重是 ICSE'26 明确推荐的抗弃用手段 |
| **4 · 泛化性** | **附引用理由驳回**（§4.4）。43/85 + G6 只要求「商业模型时加一个开放基线」 |
| **5.1 · 私域⟹小模型** | **接受并降档**（⛔ story 必须改写成弱形态） |
| **5.2 · Qwen 来源国** | **移入 Limitations**，⛔ 且不得在 ITAR / DoD 场景上做任何 claim |
| **5.3 · 成本归一化** | **接受并降档**（成本列进主结果表） |
| **5.4 · 涉密网络能否用 LLM** | **移入 Limitations**（⛔ 条件式动机） |
| **5.5 · 「相当」无判据** | **接受并降档**（⛔ 判据跑前写死并 push） |
| **5.6 · 工业举证** | **接受并降档 + 移入 Limitations** |
| **5.7 · 为什么 32B / Qwen** | **接受并降档**（⛔ 写选型准则，不假装「必须」） |
| **5.8 · TCO** | **附引用理由驳回 —— ⛔ 方式是不提成本** |
