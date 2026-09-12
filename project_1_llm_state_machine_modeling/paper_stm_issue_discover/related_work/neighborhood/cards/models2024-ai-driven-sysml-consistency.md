# 卡片 · Sultan & Apvrille, MODELS 2024 —— AI-Driven Consistency of SysML Diagrams（TTool-AI 的跨视图一致性扩展）

⭐ **全文已通读**（⛔ 不是仅据摘要）。⚠️ ⛔ **ACM DL 对 CLI 是 Cloudflare 403**（⭐ `verify_assets` 逐字：`HTTP 403 · HTTPError 403`），⭐ **但作者预印本可直取** —— ⭐ [perso.telecom-paristech.fr/apvrille/docs/models2024_sultan.pdf](https://perso.telecom-paristech.fr/apvrille/docs/models2024_sultan.pdf)，⭐ `HTTP 200 · 1,235,760 B · PDF 1.5 · 11 页`，⭐ 已用 [`tools/pdf_extractor.py`](../../../../../tools/pdf_extractor.py) 提取（1373 行）。

⭐⭐ **本卡与 [sosym2026-state-machine-consistency.md](./sosym2026-state-machine-consistency.md) 是同一条线：⭐ 那篇是本篇的期刊扩展版，⭐ 本篇是前作，⛔ 且拿了 MODELS 2024 的 Distinguished Paper Award。**

⭐⭐⭐ **而本卡最大的产出不是抽卡本身，⭐ 而是它把那张卡的两条悬案结掉了：**

1. ⭐⭐ **那张卡 F §10 问「SoSyM Table 7 是不是就是 MODELS'24 的表」** → ⭐⭐ **答：⭐ 检出部分逐位相同，⛔ 纠正部分被下修了 1.5。**
2. ⭐⭐⭐ **那张卡 F §3 说 SoSyM 的 `87%` 四种口径都复算不出** → ⭐⭐⭐ **答：⛔ 那个 `87%` 是从本篇原样抄过去的陈旧数字。⭐ 在本篇它是对的（`60.5/69 = 87.68%`）。**

⭐ 详见下方「⭐⭐ 附答：两条 SoSyM 悬案」一节。

⚠️ **本卡开头先回答任务书的四问。**

---

## ⭐⭐ 第 1 问：「输出 token 上限导致不一致」原文怎么说的、有没有量化

### 逐字原文（⭐ 共两处）

**① 摘要（M，逐字）：**

> "Moreover, the integration of Large Language Models (LLMs) into Model Driven Engineering (MDE) introduces additional consistency challenges, **as LLM's limited output contexts requires the integration of responses.**"

**② §1 Introduction（M，逐字 —— ⭐ 这是完整的那一处）：**

> "Furthermore, il will become increasingly common to generate different system views from the same system specification using LLMs [3, 6]. New challenges then arise, due to the inherent limitations of these models, such as **their maximum token output (for instance, capped at 4,096 tokens for OpenAI's GPT-3.5 and 4). This limitation induces the generation of diagrams through multiple queries and answers. Due to the stochastic nature of LLMs, this multi-step generation introduces the risk of inconsistencies not only between different diagrams but also within different parts of the same diagram**, highlighting the need for adapted mechanisms to ensure diagram consistency [6]."

⚠️ ⛔ **原文拼写为 `il will become`，⭐ 应为 `it will become`。** ⭐ 逐字保留。

### ⛔⛔ **有没有量化 —— ⭐ 答：完全没有。⭐ 一个数字都没有。**

| 需要的东西 | ⭐ 有无 | ⭐ 证据 |
| :-- | :-: | :-- |
| ⭐ 「多少比例的不一致源于 token 上限」 | ⛔ **无** | ⭐ Table 4 只分 `Internal` / `External` / `Errors` 三列，⛔ **没有成因列、⛔ 没有归因分析** |
| ⭐ 「切分成几次查询」 | ⚠️ **正文未给，⛔ 但实现侧可推** | ⭐ 见下方「⭐ 切分机制」 |
| ⭐ 「不切分会怎样」的对照臂 | ⛔ **无** | ⛔ 全文无单次查询 vs 多次查询的对照 |
| ⭐ 「同一图内部的不一致」是否单独计数 | ⛔ **无** | ⚠️ ⭐ `Internal` 列**混装**了「图内自相矛盾」与「图不合规」两种东西，⛔ 论文不区分 |

⭐⭐ **裁定：⭐ 这是一条纯动机性论断（motivational claim），⛔ 不是实测结论。** ⭐ 它出现在摘要与引言，⛔ **在评估、结果、讨论三节里再也没有回来过** —— ⭐ 我已逐节确认（⛔ §5 Evaluation 无、⛔ §5.3 Results 无、⛔ §6 Discussion 只谈**输入** context 而非**输出** token）。

### ⭐ 切分机制 —— ⭐ 实现侧确实做了多次查询（M，⛔ 但是从代码与配套档读出的，⛔ 不是从正文）

⭐ **三条独立证据：**

1. ⭐ **论文脚注 9 点名的实现文件名本身就叫 slicing**（M，逐字脚注）：`https://gitlab.telecom-paris.fr/mbe-tools/TTool/-/blob/master/src/main/java/ai/AIBlockConnAttribWithSlicing.java` —— ⭐⭐ **`Block` ＋ `Conn` ＋ `Attrib` ＋ `WithSlicing`，⭐ 即 BD 的生成被切成「块 / 连接 / 属性」三段。**
2. ⭐ **配套 Zenodo 档的 README 逐字给出 UI 上的选项名**（M，⭐ 我方实取，⭐ 见 D 节）："select, to identify blocks: **'Identify system blocks (knowledge type #2 with slicing)** - Provide a system specification'"。
3. ⭐ **状态机是**另一次独立查询**（M，⭐ 同 README 逐字）："To identify state machines: select a block diagram, open the AI window […] select **'Identify state machines and attributes'** […] Once state machine have been computed, select 'apply response'. **You should now have both block and state machine diagrams.**"

⭐⭐ **所以「多次查询 → 不一致风险」这条链在实现上是真实存在的：⭐ BD 内部切三段、⭐ BD 与 SMD 分两次、⭐ UCD 与 BD 分两次。** ⛔ **但论文从未测量这条链贡献了多少不一致。**

### ⚠️⚠️ **对 M1 最要紧的一条：⛔ 这个缺陷来源可能已经蒸发了**

⭐ 论文钉的数字是 **4,096 output tokens**（⭐ GPT-3.5 / GPT-4，⭐ 2024 年）。⚠️ ⭐ 按本仓库 [llm_model_landscape/](../../../../../llm_model_landscape/) 的口径，⛔ **当代模型的 max output 已经不在这个量级**。⭐⭐ **所以任务书说的「那是我们目前完全没有跟踪的一类缺陷」需要修正为：**

⭐⭐ **它是一类**由生成方式引入**的缺陷，⛔ 不是一类**制品固有**的缺陷。⭐ 它的成因是「因为输出装不下所以拆成多次」，⛔ 而当输出装得下时它就不产生。⭐⭐ **对我们的含义是：**

1. ⭐ **我们的 discover 流水线确实有一个同构的风险点，⛔ 但不在输出长度上** —— ⭐ 我们的 `split_requirements` 把 NL 拆成多条原子需求、⭐ `convert_assertions` 逐条转断言，⭐ **这也是「多次生成 → 各次之间可能不自洽」的形状**（⭐ 例如两条需求选了互相矛盾的谓词、⭐ 或同一元素在两条断言里被指成不同名字）。⛔ **而我们目前确实没有任何跨断言一致性检查。**
2. ⛔ **但不要照抄它的归因（token 上限）** —— ⭐ 那个前提在我们这里不成立（⛔ 我们的拆分是**方法设计**决定的，⛔ 不是**上下文容量**逼出来的）。
3. ⭐⭐ **可搬的是「多次生成必须配一道跨次一致性门」这个结构，⛔ 不是「token 上限是缺陷来源」这个论断。**

---

## ⭐⭐ 第 2 问：形式化一致性规则有多少条、闭合吗、谁编的

### ⭐⭐ **25 条**（⭐ Table 1 的 10 ＋ Table 2 的 12 ＋ Table 3 的 3）

⚠️ ⭐ **与期刊版对比**：⭐ [sosym2026-state-machine-consistency.md](./sosym2026-state-machine-consistency.md) 是 **38 条**（⭐ 多了 SMD 内部 5 条 · UCD↔AVATAR 5 条 · SMD↔BD 4 条，⭐ 并把跨视图 3 条重编为 2 条）。⭐⭐ **即两年间从 25 条长到 38 条，⛔ 而 SMD 相关的 9 条全是期刊版才有的。**

### ⭐ Table 1 · UCD 内部一致性规则（10 条，⛔ 逐条抄，⭐ 含形式化表达与出处列）

| ID | 规则（⛔ 逐字） | ⭐ 形式化表达 | ⭐ 出处（⛔ 论文原表的 `Reference (when applicable)` 列） |
| :-- | :-- | :-- | :-- |
| **RU1** | There is at least one actor and one use case in the diagram | $V_A \neq \emptyset \land V_U \neq \emptyset$ | ⛔ **—** |
| **RU2** | Any link shall involve two actors/use cases existing in the diagram | $E \subset V^2$；⭐ 实现上强制 $\forall (v_1,v_2) \in E, \exists (v_3,v_4) \in V^2$ 使 $name_V(v_3)=name_V(v_1) \land name_V(v_4)=name_V(v_2)$ | ⛔ **—** |
| **RU3** | Each actor/use case shall have a name | $name_V$ 是全函数 | ⛔ **—** |
| **RU4** | Actor names shall start with a noun | $\forall v \in V_A, \exists i \in \mathbb{N}$ 使 $name_V(v)_i \in A^*_N$ | ⭐ **[13]** |
| **RU5** | Use case names shall start with a verb | $\forall v \in V_{U\overline{ext}}, \exists i \in \mathbb{N}$ 使 $name_V(v)_i \in A^*_V$（⭐ 带扩展点的另有双分量版） | ⭐ **Derives from [27] and [13]** |
| **RU6** | Any link between an actor and a use case shall be an association link | $type_E : E \cap V_U \times V_A \to \{associate\}$ | ⭐ **[13]** |
| **RU7** | ⚠️ Any link between two actors shall be an **specialization** link | $type_E : E \cap V_A^2 \to \{specialize\}$ | ⛔ **—** |
| **RU8** | Each actor shall be linked to at least one use case | $\forall \alpha \in V_A, \exists (u,\alpha) \in E$ | ⛔ **—** |
| **RU9** | At most one link shall exist between two given elements | $E$ 是反对称关系 | ⛔ **—** |
| **RU10** | Any link between two use cases shall be either a specialization, inclusion or extension link | $type_E : E \cap V_U^2 \to Types_E \setminus \{associate\}$ | ⭐ **Derives from [13]** |

⭐ **出处两条的全称**：⭐ **[13]** = Ibrahim, Ibrahim, Saringat, Mansor, Herawan, *On well-formedness rules for UML use case diagram*, WISM 2010, Springer, 432–439。⭐ **[27]** = Torre, Labiche, Genero, Elaasar, *A Systematic Identification of Consistency Rules for UML Diagrams*, JSS 144 (2018), 121–142。

⚠️⚠️ **`RU7` 在期刊版被改掉了**：⭐ 本篇 RU7 = 「两 actor 之间的连线**必须是** specialization」，⛔ 而 SoSyM 2026 的 RU7 = 「两 actor 之间**不得有**连线」（⭐ 见那张卡 B5）。⭐⭐ **本篇脚注 7 已经预告了这次改动（M，逐字）：** "Our implementation does not support the links between two actors. We therefore inject this rule to the LLM for RU7: $E \subset V_U \times (V_U \sqcup V_A)$." ⭐⭐ **即形式化规则允许 specialization，⛔ 而实现禁止，⛔ 于是喂给 LLM 的是禁止版。⭐ 期刊版把规则改成与实现一致。**

### ⭐ Table 2 · BD 内部一致性规则（12 条，⛔ 逐条抄）

| ID | 规则（⛔ 逐字） | ⭐ 形式化表达 |
| :-- | :-- | :-- |
| **RB1** | There is at least one block in a BD | $\mathcal{B} \neq \emptyset$ |
| **RB2** | Each block shall have a unique name | $\forall (B_1,B_2) \in \mathcal{B}^2, B_1 \neq B_2 \Rightarrow name_B(B_1) \neq name_B(B_2)$ |
| **RB3** | Each attribute shall have a unique name | ⭐ 同构，作用于 $A_B$ |
| **RB4** | Each method shall have a unique name | ⭐ 同构，作用于 $M_B$ |
| **RB5** | Each signal shall have a unique name | ⭐ 同构，作用于 $S_{iB} \sqcup S_{oB}$ |
| **RB6** | Attribute types shall be limited to either boolean or integer | $\forall B \in \mathcal{B}, type_A : A_B \to \{Bool, \mathbb{Z}, \mathbb{N}\}$ |
| **RB7** | In a method signature, parameters types shall be limited to either boolean or integer | ⭐ 方法由 $M_B \to \{(t_1,\ldots,t_n) \mid t_i \in Types_A\}$ 定型 |
| **RB8** | In a signal signature, parameters types shall be limited to either boolean or integer | ⭐ 信号由 $S_B \to \{(t_1,\ldots,t_n) \mid t_i \in Types_A\}$ 定型 |
| **RB9** | Signals shall be either **input** or **output** | $\forall B \in \mathcal{B}, S_B \subset InSign \sqcup OutSign$ |
| **RB10** | Any link shall involve two blocks existing in the diagram | $\mathcal{L} \subset \mathcal{B}^2$；⭐ TTool-AI 按名字比对强制 |
| **RB11** | Any link shall have a valid communication semantics | $\sigma : \mathcal{L} \to CommSemantics$ |
| **RB12** | Any connection shall involve two signals existing in the blocks involved in the connection | $\mathcal{C} \subseteq \mathcal{L} \times S_o \times S_i$，⭐ 且端口与信号须属同一 block |

⚠️ ⭐ **Table 2 没有出处列** —— ⛔ **12 条一条出处都没有**（⭐ 与 Table 1 不同，⭐ Table 1 至少有一列 `Reference (when applicable)`）。

⚠️ **`RB11` 也被实现收紧了**（M，脚注 10 逐字）："We enforce the following rule: $\sigma : \mathcal{L} \to \{(synchronous, unicast, private)\}$" —— ⭐ 即通信语义被钉死成单一取值，⛔ 而形式定义里 `CommSemantics` 是个含同步/异步 × 广播/单播 × 有损/无损 × 阻塞/非阻塞 × 公开/私有的大集合。

### ⭐ Table 3 · UCD↔BD 跨视图一致性规则（3 条，⛔ 逐条抄）

| ID | 规则（⛔ 逐字） | ⭐ 形式化表达 |
| :-- | :-- | :-- |
| **RC1** | No link shall exist between two environment blocks | ⚠️ $\langle B_1,B_2 \rangle \in \mathcal{L}$ s.t. $type_{B_1}=environment \land type_{B_2}=environment$（⛔ 见下方存疑） |
| **RC2** | Any environment block shall have at least one link with a system block | $\forall B \in \mathcal{B}$ s.t. $type_B=environment, \exists \langle B,\beta \rangle \in \mathcal{L}$ s.t. $type_\beta=system$ |
| **RC3** | Any environment block shall correspond to an actor defined in the UCD | ⭐ 给定 UCD $\langle (V,E), type_V, name_V, type_E \rangle$，$\forall B \in \mathcal{B}$ s.t. $type_B=environment, \exists v \in V_A$ s.t. $name_V(v)=name_B(B)$ |

⚠️ ⭐ **Table 3 也没有出处列。** ⭐ 论文自己说这三条**文献里没有**（M，§3.2.3 逐字）："Lastly, we have defined a set of consistency rules between UCDs and BDs. **To the best of our knowledge, such rules do not exist in the literature.**" ⭐ 并在 §2.1 用它当「规则法覆盖不全」的旁证。

⭐ **RC1 / RC2 的理由写在脚注里（M，逐字）**：⭐ 脚注 4 —— "An environment block is designed to encapsulate the environment rather than the system itself. […] It's important to note that **this rule can be system-specific or based on custom recommandations.**"；⭐ 脚注 5 —— "We assume that the system is already complex, so we usually assume that **modeling exchanges between environmental elements would lead to capture unnecessary relations**"。⭐⭐ **即作者自己标明这两条是方法学约定，⛔ 不是 UML/SysML 语义。**

### ⭐⭐ 闭合吗、谁编的

| 子字段 | 值 |
| :-- | :-- |
| ⭐ **是否闭合** | ⭐ **任一时刻闭合**（⭐ 25 条固定编号），⛔ **但论文明确声明会演化**（M，逐字："it is possible that some inconsistencies have not been captured in the rule definition process. **Therefore this list is set to evolve.**"）—— ⭐ 事实上两年后就变成 38 条了 |
| ⭐ **谁定的** | ⭐ **作者预编**，⛔ **三来源混合**（M，§3.2 逐字）："This rule list was developed through **(i) a literature review on SysML consistency rules, (ii) a literature review on the use of LLMs in UML/SysML modeling, and (iii) intensive testing of BDs and UCDs LLM-based generation.** These processes enabled us to identify **the inconsistencies most frequently introduced by LLMs**, incorporating feedback from the community as well as our own observations." |
| ⛔ **谁选（运行时）** | ⛔⛔ **按阶段硬编码，⛔ 与被检对象无关。⛔ LLM 不选** —— ⭐ 见下表 |
| ⭐ **定位** | ⭐ **专为 LLM 产出而设，⛔ 不求完备**（M，逐字）："the rules we propose below are **rules firstly designed for LLM-generated outputs rather than comprehensive consistency rules.**" ⭐ 并说明 TTool 自带 syntax checker 已覆盖文献里的常规规则，⛔ 故不重复 |

#### ⭐⭐ 三份硬编码名单（⛔ 逐条抄，⭐ 这是「谁选」这一格的实证）

| 阶段 | 干什么 | ⭐ 用到哪几条 |
| :-- | :-- | :-- |
| **U1** | ⭐ 注入 UCD 生成请求 | ⭐ `RU4` · `RU5` · ⛔ **`RU7` 的加强版** · `RU8` · ⛔ **`RU10` 的加强版**（⭐ 脚注 8：只支持 `include`，⭐ 故注入 $type_E : E \cap V_U^2 \to \{include\}$） |
| **U3** | ⭐ 语法 / 一致性检查（⭐ 失败则回 U1） | ⭐ `RU1` · `RU2` · `RU3` · `RU8` · `RU9` |
| **U5** | ⭐ 建构时强制（correct-by-construction） | ⭐ `RU1` · `RU2` · `RU3` · `RU6` · ⛔ `RU7` 加强版 · ⛔ `RU10` 加强版 |
| **B1/B2** | ⭐ 注入 BD 生成请求 | ⭐ `RB6` · `RB8` |
| **B3** | ⭐ 语法 / 一致性检查 | ⭐ `RB1` · `RB6` · `RB7` · `RB9` |
| **B5** | ⭐ 建构时强制 | ⭐ `RB3` · `RB5` · `RB6` · `RB7` · `RB10` · ⛔ `RB11` 加强版 · `RB12` |
| **C1** | ⚠️ **可选**注入跨视图请求 | ⭐ `RC1` · `RC2` · `RC3`（⭐ 以自然语言给出） |

⭐⭐ **注意三件事：**

1. ⛔ **`RU4` `RU5` 只在生成端注入，⛔ 从不在检查端验** —— ⭐ 即「actor 名以名词开头」「use case 名以动词开头」这两条**没有任何机械把关**，⛔ 全靠 LLM 听话。
2. ⛔ **`RB2` `RB4` `RB8` `RB9` 在建构强制名单里缺席** —— ⭐ `RB9`（信号必须是 input 或 output）只在 B3 检查、⛔ 不在 B5 强制。
3. ⭐⭐ **喂给 LLM 的规则是「实现收紧版」，⛔ 不是形式化规则本身**（⭐ `RU7` `RU10` `RB11` 三条）。⭐ **这是一个值得记住的做法：⭐ 规范层写通用规则、⛔ 运行层注入工具能力范围内的收紧版。**

### ⭐⭐ 出处分级 —— ⭐ 与我们 19 条谓词的直接对照

| 维度 | ⭐ 它（MODELS 2024，25 条） | ⭐ 期刊版（SoSyM 2026，38 条） | ⭐ 我们（19 条谓词） |
| :-- | :-- | :-- | :-- |
| 闭合性 | ⭐ 闭合（⛔ 声明会演化） | ⭐ 闭合（⛔ 自称 pragmatic subset） | ⭐ 闭合 |
| ⛔ **谁选** | ⛔ **三份硬编码名单** | ⛔ **三份硬编码名单** | ⭐⭐ **LLM 逐需求自动选** |
| ⭐ **有出处的条数** | ⛔⛔ **4 / 25 = 16%**（⭐ 只有 `RU4` `RU5` `RU6` `RU10`；⛔ Table 2 与 Table 3 **连出处列都没有**） | ⭐ **8 / 38 有文献或标准** ＋ 11 条记「元模型定义性」 | ⭐ **① 有领域证据 12 · ② 元模型定义性 6 · ③ 无外部依据 1** |
| ⭐ 出处形态 | ⛔ 一列 `Reference (when applicable)`，⛔ 只在 Table 1 上有 | ⭐ 每张表都有 `Reference […] or justification` 列 | ⭐ 三类分级 ＋ 逐条注释 |

⭐⭐⭐ **这一格的结论（⛔ 这是本卡对论文写作最有用的一条）：**

⭐⭐ **同一个团队，⭐ 两年之间把出处纪律从「4/25 且只覆盖一张表」补到「38/38 每条都有 justification 列」。** ⭐⭐ **即出处分级不是我们发明的怪癖，⛔ 而是这条线自己在演化中补上的东西 —— ⭐ 而它是在 CCF-B 期刊上补的。** ⭐ 我们的 `① 12 · ② 6 · ③ 1`（⛔ 只 1 条无外部依据 = 5.3%）**从一开始就比本篇（16% 有出处 = 84% 无出处）严得多**。

---

## ⭐⭐ 第 3 问：检测与纠正分别由谁做、有循环吗、裁决者是谁

### ⭐ B1 那张图的三段（⭐ Figure 1，⭐ 论文自己的阶段编号）

- ⭐ **段一：`U1–U5` 与 `B1–B5` 并行** —— ⭐ 各自生成一张图并守住**内部**一致性。
- ⭐ **段二：`C1–C3`** —— ⭐ 查**跨视图**一致性（⭐ 并捡漏 U3/B3 没抓到的内部不一致）。
- ⭐ **段三：回灌 `U1`/`B1` 纠正。**

### ⭐⭐ 逐阶段的执行者（⛔ 这是第 3 问的核心表）

| 阶段 | 干什么 | ⭐ 执行者 |
| :-- | :-- | :-- |
| **U1 / B1** | ⭐ 组请求 = NL 规约 ＋ 语法约束 ＋ 内部一致性规则 | ⭐ **确定性** |
| **U2 / B2** | ⭐ 生成图（⭐ JSON 回传） | ⭐ **LLM** |
| **U3 / B3** | ⭐ 语法 ＋ 一致性分析；⛔ **失败则重组请求回 U1** | ⭐⭐ **确定性**（⭐ 裁决者 #1） |
| **U4 / B4** | ⭐ 人看图：接受 / 要求改 / 重生成 | ⭐⭐ **人**（⭐ 裁决者 #2） |
| **U5 / B5** | ⭐ 画进 TTool GUI，⭐ 建构时强制一批规则 | ⭐ **确定性** |
| **C1** | ⭐ 两图导成精简文本 ＋ 输出格式约束 ＋（可选）跨视图规则 | ⭐ **确定性** |
| **C2** | ⭐⭐ **产出不一致清单（JSON）** | ⛔⛔ **LLM** |
| **C3** | ⭐⭐ **人挑哪些不一致要修 → 回灌 U1/B1** | ⭐⭐ **人**（⭐ 裁决者 #3） |

⭐⭐ **合计 11 个阶段 · ⛔ 只有 2 个是 LLM（`U2/B2` 生成、`C2` 检测）· ⭐ 6 个确定性 · ⭐ 3 个人。**

### ⭐⭐ **检测 = LLM；⛔ 纠正的「改哪些」= 人；⭐ 纠正的「怎么改」= LLM；⭐ 内部合规 = 确定性**

⭐ **逐字支撑：**

- ⭐ **检测（C2）是 LLM 做的**（M，逐字）："This request is sent to the LLM, which analyzes it and **produces a structured list (in json) of identified inconsistencies.** This can also include internal inconsistencies not detected in stages U3 and B3."
- ⭐⭐ **「改哪些」由人挑**（M，逐字）："With this list of inconsistencies, the process reverts to stages U1 and B1. Here, **the list of inconsistencies is (partially or totally) incorporated by the user** into the newly crafted requests."
- ⭐ **人还在循环里下别的指令**（M，逐字）："**Users play an integral role in this loop**, choosing which inconsistencies to tackle or guiding the diagram generation by imposing additional constraints, such as 'include at least 5 actors and 10 use cases'."
- ⭐ **误报在进纠正前被人先剔掉**（M，§5.3 逐字）："Inconsistencies incorrectly identified are cataloged in the 'Error' column; **they are excluded from the total inconsistency count and are not addressed during the correction phase.**"

### ⭐⭐ 循环与裁决者（⛔ 本轨最关键的一格）

⭐⭐ **有三个循环，⭐ 三个裁决者，⛔ 而 LLM 一个都不是。**

| 循环 | 裁决者 | ⭐ 类型 | 终止条件 | 最大轮数 |
| :-- | :-- | :-- | :-- | :-- |
| `U1→U2→U3→U1`（⭐ UCD 生成内环） | ⭐ `U3` 的语法 ＋ 一致性检查 | ⭐ **`parser / 编译器` ＋ `确定性规则`** | ⭐ 规则全过 / ⛔ 撞上限 | ⛔ **原文未提供** |
| `B1→B2→B3→B1`（⭐ BD 生成内环） | ⭐ `B3` 同上 | ⭐ **`parser / 编译器` ＋ `确定性规则`** | ⭐ 同上 | ⛔ **原文未提供** |
| `U4` / `B4` 接受门 | ⛔ **人** | ⭐ **`人`** | ⭐ 人叫停 | ⛔ 无 |
| `C1→C2→C3→U1/B1`（⭐ 检测-纠正外环） | ⛔ **人**（⭐ 挑条目、⭐ 剔误报） | ⭐ **`人`** | ⭐ 全部解决 / ⛔ 时限 / ⛔ 最大轮数 | ⛔ **原文未提供** |

⭐ **终止条件逐字（M，§4）：** "This iterative process concludes either **when all inconsistencies are resolved or when it reaches a predefined time limit or maximum number of iterations.**"

⚠️⚠️ ⭐ **注意：⭐ 论文说有 `maximum number of iterations`，⛔ 但没给数字。** ⭐⭐ **期刊版才给：⭐ SoSyM 2026 逐字 "caps the maximum number of iterations at **20**"，⛔ 并说 "this threshold was **never reached**"（⭐ 见那张卡 B4）。** ⭐ **本篇的对应数字应记「原文未提供」。**

⭐ **裁决者类型逐条对照 [EXTRACTION_SCHEMA.md](../EXTRACTION_SCHEMA.md) 的词表**：⛔ `LLM 自评` = **无**；⭐ `parser / 编译器` = **有**；⭐ `确定性规则` = **有**；⭐ `人` = **有（3 处）**；⛔ `sound oracle`（模型检查器 / SMT）= ⛔ **不在这条链上**（⚠️ ⭐ TTool 自带 SysML 直接模型检查 [5]，⛔ 但本文只在 §2.3 提，⛔ 不参与一致性循环）；⛔ `测试执行` = 无。

#### ⛔⛔ 有无报告循环的边际收益 —— ⭐ **没有，⛔ 一个逐轮数字都没有**

⛔ **本篇没有任何逐轮账**：⛔ 无「第 N 轮修好几条」、⛔ 无 token 曲线、⛔ 无成本曲线、⛔ 无轮数分布。

⭐ **能拿到的只有两条单例：**

1. ⭐ **内环唯一被记录的一次触发**（M，§5.1.2 逐字）：⭐ 初版 UCD 违反 `RU8`，⭐ 日志逐字为 "`−Actor "Azimuth_Thrusters" must be connected to at least one use case`" ＋ 同样一条 `Bow_Thrusters`。⭐ **一次反馈就修好**（逐字："These two internal inconsistencies were then addressed through the automated feedback mechanism. As a result, **the final version of the UCD adheres fully to the guidelines listed in Table 1.**"）。
2. ⛔⛔ **外环第 2 轮没跑**（M，§5.1.4 逐字）："We can observe that **not all inconsistencies were corrected.** For example, DPS block is still unrelated to other blocks. Nevertheless, the two primary categories of inconsistencies were addressed […] **Another iteration on inconsistencies (stages C1 to C3) could resolve these remaining issues.**"

⭐⭐ **S 级推论（⛔ 论文没这么写）：⭐ 当裁决者是确定性规则时，收敛发生在很少的轮数内 —— ⭐ 所以他们不觉得需要报边际收益曲线。** ⭐ 依据是上面第 1 条（一次即好）＋ 期刊版的「20 轮上限从未触及」。⚠️ ⭐ 这与我们 v46 的实测互补：⭐ 我们「第 3–5 轮零收益」的那 79% token 全花在**两个 LLM 自评 reviewer** 上，⛔ 而**确定性那条（`convert ⇄ precheck_and_seal`）在我们这里同样是 0 token 且性价比最高**。⭐ **又一次独立得到同一形状。**

⭐ **另有一条「确定性层吸收 LLM 错误」的自陈，⛔ 但未量化**（M，§6 逐字）：

> "the presence of an error in the list of detected inconsistencies does not necessarily means that this error will be introduced into the updated diagrams. Indeed, **the automated feedback loop of our framework, and the enforcement by design of several internal consistency rules, help eliminate errors introduced in the LLM generation process. However, we have not yet quantified this phenomenon**, but it would surely be interesting to evaluate it in the future."

⭐⭐ **这一条对 M1 很直接：⭐ 它主张「建构时强制 ＋ 确定性内环」能吃掉 LLM 的误报，⛔ 但自己承认没测。⭐⭐ 而我们有能力测这件事**（⭐ 我们的 `precheck_and_seal` 与契约门就在那个位置）—— ⛔ **这是一个别人留下的、我们可以填的空。**

---

## ⭐⭐ 第 4 问：跨视图一致性 vs 模型-需求一致性

⚠️⚠️ **任务书的术语陷阱警告成立，⛔ 但和 SoSyM 那张卡一样有一个非平凡例外 —— ⭐ 而本篇的例外证据比那张卡强得多。**

### ⭐ 判定的**对象与分类学**：⛔ 纯粹是多视图之间（＋单视图内部）

⭐ §5.3 逐字（M）：

> "We differentiate between **internal inconsistencies (within a single diagram)** and **external inconsistencies (between a block diagram and a use case diagram).**"

⭐ Table 4 的列就只有 `Internal` / `External` / `Errors` ＋ 纠正三列。⛔ **没有「模型 vs 需求」这一类，⛔ 也没有以 NL 规约为分母的任何统计。** ⭐ 全部 25 条规则（→ 第 2 问）也全是 diagram-内部 或 diagram-对-diagram，⛔ **一条都不涉及 NL。**

### ⭐⭐⭐ **但 NL 规约确实进了 prompt，⛔ 而且实际产出里就有 model-vs-NL 判定 —— ⭐ 本卡拿到了 3 条逐字实例**

⭐ **① 论文正文承认 NL 在请求里**（M，§5.1.3 逐字）：

> "Finally, the request sent to the AI engine contains **the constraints, the question, the system specification and the UCD and BD in textual format** added by the user."

⭐ **② 实现侧逐字印证**（M，⭐ 从 GitLab 实取的 `AIDiagramCoherencyWithFormalRules.java` 源码读的，⛔ 不是从论文推的）：

```java
private String[] QUESTION_IDENTIFY_INCOHERENCIES = {
  "From the provided specification and from the two SysML diagram given in textual format,"
  + "identify the incoherencies between the two diagrams. Do respect the JSON format, and\n"
  + "provide only JSON (no explanation before or after).\n"};
```

⭐ **③⭐⭐ 配套 Zenodo 档的 README 里，作者自己贴的真实输出含 3 条明确的 model-vs-NL 判定**（M，⭐ 逐字，⭐ 我方实取）：

> - "There is no actor or use case for ErrorCorrectionCode, which is a significant part of the system **as per the specification.**"
> - "There is no block representing the Watchdog's activity of checking if tasks are still responsive, which is a critical system function **as per the specification.**"
> - "There is no representation for the cancellation and recomputation of TM upon receiving another TC, **as described in the specification.**"

⭐ 同一份清单里还有两条是**领域判断**而非视图对比：⭐ "Use case 'Monitor_Safety_Data' is shown to be associated with RF_Receiver, **which is incorrect as monitoring is a ground station activity**"、⭐ "Block 'GroundStation' has attributes for temperature, batteryLevel, and fuelQuantity, **which are not its attributes but those of the space-based system**"。

⭐⭐⭐ **而且纠正 prompt 里也带着它们**（M，⭐ README 逐字给出的 correction 请求）：

```
Do correct the block diagram considering the following incoherencies:
...
3. There is no block representing the Watchdog's activity of checking if tasks are still
   responsive, which is a critical system function as per the specification
4. There is no representation for the cancellation and recomputation of TM upon receiving
   another TC, as described in the specification
```

⛔⛔ **这 3 条显然是「模型 vs 规约」，⛔ 不是「视图 vs 视图」。⛔ 但按 Table 4 的口径它们会被记成 `Internal`（⭐ 因为只涉及一张图），⛔ 而论文从不承认这一类的存在。**

### ⭐⭐ 第 4 问的裁定

| 维度 | ⭐ 它 | ⭐ 我们（v46） |
| :-- | :-- | :-- |
| ⭐ **问题定义** | ⛔ **多视图一致性**（UCD ↔ BD）＋ 单视图内部合规 | ⭐ **模型 vs 自然语言需求** |
| ⭐ 判定分母 | ⛔ **检出条数**（69）· ⛔ 图对 12 个 | ⭐ NL 需求台账条目（98 条能力分母） |
| ⭐ reference | ⛔ **另一张图**（⭐ UCD 与 BD 互为参照） | ⭐ **NL 文本** |
| ⚠️ NL 在不在 context 里 | ⭐ **在**（⭐ 正文 ＋ 源码双证） | ⭐ 在（⭐ 就是被比的对象） |
| ⛔ NL 算不算判定依据 | ⛔ **口径上不算**（⛔ 无 NL 分母、⛔ 无 NL 类别、⛔ 无 NL 真值），⚠️ ⭐ **但产出里事实上有** | ⭐ **就是全部依据** |
| ⭐ 有无 recall 分母 | ⛔ **无** | ⭐ 有 |

⛔⛔ **裁定：⭐ 与我们不是同一个问题。** ⚠️ ⭐ 术语陷阱确认成立 —— ⭐ 它的 `consistency` / `coherency` 指**多视图模型之间**（⭐ §2.1 脚注 1 逐字："In this paper, **we treat the terms consistency and coherence as synonymous.**"）。⛔ **不得把它当作 model-vs-NL 的先例或可比数字。**

⭐⭐ **但本卡比 SoSyM 那张卡多推进了一步：⭐⭐ 「LLM 拿到 NL 之后会自发产出 model-vs-NL 发现」这件事，⭐ 在本篇的配套档里有 3 条逐字实例 ＋ 进入了纠正 prompt。⭐⭐ 也就是说：⭐ 这条线**已经在无意中做了 model-vs-NL 检测**，⛔ 只是没有为它建分类学、没有建分母、没有建真值。⭐⭐ 那正好是我们在做的事 —— ⛔ 而这是一个可以在 Related Work 里写的、非常干净的差异化落点。**

⚠️ ⛔ **但按 [README.md](../README.md) §3 的防火墙，⭐ 这条要进论文必须先回 L1 重走门。⭐ 本卡只把它记为方法素材。**

---

## ⭐⭐ 附答：两条 SoSyM 悬案（⛔ 本卡的独立产出）

### ⭐⭐ 悬案一（那张卡 F §10）：SoSyM Table 7 是不是 MODELS'24 的表

⭐⭐ **答：⭐ 检出部分逐位相同，⛔ 纠正部分被下修了 1.5。**

| | ⭐ MODELS 2024（Table 4） | ⭐ SoSyM 2026（Table 7） | 差 |
| :-- | :-: | :-: | :-: |
| Internal 检出 | **36** | **36** | ⭐ 0 |
| External / Cross-view 检出 | **33** | **33** | ⭐ 0 |
| Errors | **6** | **6** | ⭐ 0 |
| ⭐ **Total 检出** | ⭐ **69** | ⭐ **69** | ⭐ **0** |
| Internal 纠正 | ⛔ **30** | ⛔ **28.5** | ⛔ **−1.5** |
| External 纠正 | **30.5** | **30.5** | ⭐ 0 |
| ⭐ **Total 纠正** | ⛔ **60.5 / 69** | ⛔ **59 / 69** | ⛔ **−1.5** |
| ⭐ **micro 纠正率** | ⛔ **87.68%** | ⛔ **85.51%** | ⛔ **−2.17pp** |

⭐ **下修发生在 DPS 系统的三格（⭐ 我方逐行对拍定位）：**

| 格 | ⭐ MODELS 2024 | ⭐ SoSyM 2026 |
| :-- | :-: | :-: |
| DPS · BD1 vs UCD2 · BD1 · Corr-Internal | **2** | ⛔ **1.5** |
| DPS · BD2 vs UCD1 · BD2 · Corr-Internal | **1**（⭐ 总 `1/1`） | ⛔ **0.5**（⭐ 总 `0.5/1`） |
| DPS · BD2 vs UCD2 · BD2 · Corr-Internal | **3**（⭐ 总 `3/3`） | ⛔ **2.5**（⭐ 总 `2.5/3`） |

⭐⭐ **即三格各扣 0.5 分，⭐ 合计 −1.5。⛔ 期刊版没有说明为什么重评。**

⭐ **我方对 MODELS 2024 Table 4 的独立复算全部通过 ✅**：⭐ 24 行逐行验 `Internal + External = Total`（⭐ `Errors` 不计入 `Total`）**24/24 通过**；⭐ 逐行验 `Corr-Int + Corr-Ext = Corr-Total 分子` 且 `分母 = Total`：**20/20 通过**（⭐ 4 行 `Total = 0` 的分母栏为 `—`）。⭐ 合计栏亦全部对上。

### ⭐⭐⭐ 悬案二（那张卡 F §3）：SoSyM 的 `87%` 复算不出

⭐⭐⭐ **答：⛔ 那是从本篇原样搬过去的陈旧数字。⭐ 在本篇它是正确的。**

⭐ **本篇 §5.3 逐字（M）：** "our approach enabled for **an automatic resolution of 87% of the inconsistencies on average**, demonstrating a slightly higher correction rate for external (cross-diagram) inconsistencies."

⭐ **本篇 §6 逐字（M）：** "the correction rate (**which varies between 50% and 100% per diagram, averaging at 87%**)"

⭐ **我方复算（⛔ 论文未列这些中间量）：**

| 口径 | ⭐ MODELS 2024 | ⭐ 对得上论文的 `87%` 吗 |
| :-- | :-: | :-: |
| ⭐ **micro（`60.5/69`）** | ⭐ **87.68%** | ⭐⭐ **对上 ✅** |
| ⭐ 逐图宏平均（20 行） | 89.78%（⭐ min **50%** · max **100%**） | ⛔ 数不对，⭐ **但区间逐字对上 ✅** |
| ⭐ 逐图对宏平均（12 对） | 86.96% | ⛔ 否 |
| ⭐ 逐系统宏平均（3 个） | 87.65% | ⚠️ 接近 |

⭐⭐ **所以本篇的 `87%` = micro（`60.5/69 = 87.68%`），⭐ 而 `50%–100%` 的区间 = 逐图宏平均的极值。⭐ 两句话各自都对。**

⭐⭐⭐ **而期刊版把三格分数下修后，micro 变成 `59/69 = 85.51%`，⭐ 它在 §6.1.1 更新成了 `85.5%`，⛔ 却漏改 §6.3 那句「averaging at 87%」与「50% to 100%」。** ⭐⭐ **这就是 SoSyM 那张卡「四种口径都算不出 87%」的原因 —— ⛔ 它是一个跨版本的陈旧数字，⛔ 不是一个未知口径。**

⭐ **两条其它自洽性核验（⛔ 本篇内部）：**

- ⭐ **`averaging 4 for BDs and 1.7 for UCDs` ✅** —— ⭐ 我方复算 BD 侧检出 **49**、`49/12 = 4.08`；UCD 侧 **20**、`20/12 = 1.67`。
- ⭐ **`slightly higher for external` ✅** —— ⭐ 我方复算 external `30.5/33 = 92.42%` vs internal `30/36 = 83.33%`。⚠️ ⭐ 「slightly」偏保守，⛔ 实际差 **9.1pp**。
- ⛔⛔ **`8%` vs `7%` 本篇内部冲突** —— ⭐ §5.3 逐字 "This represents **8%** of the detected inconsistencies, meaning that **92%** of detected inconsistencies were relevant"（⭐ `6/75 = 8.00%` ✅）；⛔ 而 §6 逐字 "This may decrease the rate of 'false positives' among the identified inconsistencies (**7%** in our evaluation)"。⭐ 我方复算：`6/75 = 8.00%` · `6/69 = 8.70%`，⛔ **两个都不是 7%。** ⛔ **登记为 F §2。**

---

## A. 元信息

| 字段 | 值 |
| :-- | :-- |
| `id` | `models2024-ai-driven-sysml-consistency` |
| `title` | ⭐ **AI-Driven Consistency of SysML Diagrams**（M，⭐ 与 ACM Reference Format 逐字一致） |
| 作者 | ⭐ **Bastien Sultan · Ludovic Apvrille**（M）—— ⭐ 同属 **LTCI, Télécom Paris, Institut Polytechnique de Paris**, Sophia-Antipolis, France |
| `year` | ⭐ **2024**（M，⭐ ACM Reference Format 逐字 "2024"；⭐ 会期 `2024-09-22`–`09-27`，⛔ 无 early-access 歧义） |
| `venue` | ⭐ **MODELS '24** = ACM/IEEE 27th International Conference on Model Driven Engineering Languages and Systems，⭐ Linz, Austria，⭐ 11 页，⭐ ISBN `979-8-4007-0504-5/24/09`。⭐ pages **149–159**（⚠️ ⭐ 页码来自检索结果，⛔ **预印本 PDF 上无页码**，⭐ 标 S） |
| ⭐ 奖项 | ⭐ **Distinguished Paper Award**（⚠️ **S** —— ⭐ 依据两条间接证据：⭐ ① 检索结果明写；⭐ ② [sosym2026-state-machine-consistency.md](./sosym2026-state-machine-consistency.md) F §10 记录作者主页上该文件名为 `models2024_sultan_distinguishedpaperaward.pdf`。⛔ **预印本正文内无奖项声明，⛔ 我未核 MODELS 2024 官方 award 页**） |
| `ccf` | ⭐ **B** —— ⭐ 本仓库 [ccf_venues/](../../../../../ccf_venues/) 有 [`conf-b-models`](../../../../../ccf_venues/conf-b-models/README.md) 建档，⭐ [01-venue-scope.md](../../../../../ccf_venues/01-venue-scope.md) 逐字标 `🥈` = CCF B（M） |
| `doi` | ⭐ [`10.1145/3640310.3674079`](https://doi.org/10.1145/3640310.3674079) —— ⭐ **已实际访问核验**（⭐ 论文首页 ACM Reference Format 逐字给出同一 DOI）。⚠️ ⛔ `verify_assets` 对 `doi.org` 得 **`HTTP 403 · HTTPError 403`**（⭐ ACM DL 的 Cloudflare），⛔ **非 DOI 不存在** |
| `arxiv` | ⛔ **无** |
| `url`（作者版全文） | ⭐ [perso.telecom-paristech.fr/apvrille/docs/models2024_sultan.pdf](https://perso.telecom-paristech.fr/apvrille/docs/models2024_sultan.pdf) —— ⭐ `HTTP 200 · application/pdf · 1,235,760 B` ✅ |
| `url`（复现包） | ⭐ [zenodo.org/doi/10.5281/zenodo.11936921](https://zenodo.org/doi/10.5281/zenodo.11936921) —— ⭐ **实取核验，⛔ 见 D 节** |
| `url`（实现） | ⭐ [gitlab.telecom-paris.fr/mbe-tools/TTool](https://gitlab.telecom-paris.fr/mbe-tools/TTool) —— ⭐ `HTTP 200` |
| `artifact_type` | ⚠️⚠️ **评测对象是 SysML **Use Case Diagram (UCD)** ＋ **Block Diagram (BD)****（⭐ TTool 的 AVATAR SysML profile）。⛔⛔ **State Machine Diagram (SMD) 由实现支持，⛔ 但不在本篇评测范围内** —— ⭐ 见下方 `boundary` 说明 |
| `task` | ⭐ **一致性检查（＝缺陷检测）＋ 纠正**，⭐ 附带 **生成**（⭐ UCD 生成是本篇新增功能；⭐ BD 生成复用 TTool-AI 前作 [3]） |
| `boundary` | ⚠️⚠️ **`邻域`（⛔ 但硬门 2 只部分满足 —— ⭐ 必读下方说明）** |

### ⚠️⚠️ `boundary` 与硬门 2 —— ⛔ **这一格必须诚实写：本篇的评测对象不是行为模型**

⭐ [README.md](../README.md) §2 的**硬门 2** 要求「行为类模型制品」，⭐ §2.1 的三档是：⭐ `界内` = FSM/HSM/EFSM/UML 状态机；⭐ `邻域` = 活动图 / 时序图 / BPMN / 协议状态机 / LTS；⭐ `界外` = 时间自动机 / 混成 / Petri / 进程代数 / 正交并发。

⛔⛔ **UCD 与 BD 一个都不在这三档里 —— ⭐ 因为它们根本不是行为模型：⭐ UCD 是功能/交互概览，⭐ BD 是结构（架构）视图。**

⭐ **所以准确状态是三层，⛔ 不要混：**

| 层 | 事实 | ⭐ 硬门 2 |
| :-- | :-- | :-: |
| ⛔ **① 本篇的评测** | ⛔ **只有 UCD ↔ BD**（⭐ Table 4 的 12 个图对全是 BD×UCD） | ⛔ **不满足** |
| ⭐ **② 本篇的框架 / 实现** | ⭐ **支持 SMD**（M，§7 逐字："**Currently, our implementation supports UCDs, BDs, and SMDs**"），⭐ 且 §6 明说 LLM 生成的 SMD 常有错（逐字："when generated by TTool-AI, **SMDs often contain errors detected by TTool-AI's syntax checker**"） | ⭐ **满足**（⛔ 但未评测） |
| ⭐ **③ 配套 Zenodo 档** | ⭐⭐ **含 SMD 的生成质量评分数据**（⭐ `results.ods` 有 `Grade SMD (/100)` 列 ＋ 人类对照，⭐ 见 D 节）—— ⛔ **但那属于前作 MODELSWARD 2024，⛔ 不属于本篇** | ⚠️ **间接** |
| ⭐ **④ 期刊扩展版** | ⭐⭐ **SMD 进了评测**（⭐ SoSyM 2026 有 `RS1–RS5` 内部规则 ＋ `RSB1–RSB4` SMD↔BD 规则） | ⭐ **满足** |

⭐⭐⭐ **裁定：⭐ 本卡标 `boundary = 邻域`，⭐ 依据是「框架层面（②）覆盖状态机」，⛔ 而不是「评测层面覆盖状态机」。** ⛔⛔ **在 [pipeline_forms.md](../pipeline_forms.md) 与 [SUMMARY.md](../SUMMARY.md) 里，本篇应当被当作「⭐ 流水线形态参照物」，⛔ 而不是「⭐ 制品同类」** —— ⭐ 即它的 B1/B4/B5/B7 各格可以进对照表，⛔ **但它的 C 节数字不得进任何「状态机上的效果」类统计。**

⚠️ ⭐ **另有一处与我们边界相关的界外成分**：⭐ BD 的 `CommSemantics` 含 `synchronous / asynchronous`、`broadcast / unicast`、`lossy / unlossy`、`blocking / non-blocking write` —— ⭐ 即**块间并发通信语义**，⛔ 按我们的边界属界外（⭐ 虽然不是单状态机内的正交区）。⭐ 不过 `RB11` 的实现版把它钉死成单一取值 `(synchronous, unicast, private)`，⛔ 所以实际用到的语义面很窄。

⛔⛔ **提醒：⭐ 若要把这篇搬进 L1/L2（⭐ 那两轨过边界门），⛔ 必须在「评测对象不是行为模型」这一点上先给出交代 —— ⭐ 它很可能过不了门。**

---

## B. LLM 应用形态

### B1 · 流水线阶段（⭐ Figure 1 的功能架构，⭐ 论文自己的编号）

```
┌── 段一：图生成 ＋ 内部一致性（⭐ UCD 与 BD 两条链并行）───────────────────┐
│ [人]      U1/B1 前：唯一的用户输入 = NL 系统规约                        │
│  → [确定性] U1  组请求 ＝ 规约 ＋ 语法约束 ＋ 内部一致性规则（RU4,RU5,RU7⁺,RU8,RU10⁺）│
│  → [LLM]   U2  生成 UCD（⭐ JSON 回传）                                 │
│  → [确定性] U3  语法 ＋ 一致性分析（RU1,RU2,RU3,RU8,RU9）── 不过则回 U1     │
│  → [人]    U4  人看图：接受 / 要求改 / 重生成（⭐ 回 U2）                  │
│  → [确定性] U5  画进 TTool GUI，⭐ 建构时强制（RU1,RU2,RU3,RU6,RU7⁺,RU10⁺）  │
│  ⭐ B1–B5 同构（⭐ B1 注入 RB6,RB8；B3 查 RB1,RB6,RB7,RB9；                │
│      B5 强制 RB3,RB5,RB6,RB7,RB10,RB11⁺,RB12）—— ⭐ B1–B5 是前作 [3] 已有  │
├── 段二：跨视图检测 ──────────────────────────────────────────────┤
│  → [确定性] C1  两图导成精简文本 ＋ 输出格式约束 ＋（可选）RC1–RC3          │
│  → [LLM]   C2  产出不一致清单（⛔ JSON，⛔ description 是自由文本）         │
├── 段三：纠正 ───────────────────────────────────────────────────┤
│  → [人]    C3  人挑哪些要修（⛔ 先剔掉 Errors）→ 回灌 U1 / B1              │
└─────────────────────────────────────────────────────────────┘
```

⭐⭐ **11 个阶段 · ⛔ 只有 2 个 LLM（`U2/B2` · `C2`）· ⭐ 6 个确定性 · ⭐ 3 个人。**

⚠️ ⭐ **注意 `U1`/`B1` 与 `C1` 的一个不对称：⭐ 生成端的规则注入是**必选**，⛔ 而跨视图检测端的规则注入是**可选** —— ⭐ 原因见 B3 的负面发现。

### B2 · 每次 LLM 调用的角色

| 环节 | 角色 |
| :-- | :-- |
| ⭐ `U2` 初次生成 | ⭐ **生成器**（NL 规约 → UCD） |
| ⭐ `B2` 初次生成 | ⭐ **生成器**（NL 规约 ＋ 已有 UCD → BD）—— ⭐ M，§4 逐字："It may also include analysis diagrams, **such as UCDs if they already exist.**" |
| ⭐ `U2`/`B2` 纠正复用 | ⭐ **修复者** —— ⚠️ ⛔ **同一个生成器换 prompt，⛔ 不是独立修复器**（M，§5.1.4 逐字："This correction relies on **the TTool-AI BD generation feature** [3] and on **the UCD generation feature** (a contribution of the paper)."） |
| ⭐ `C2` 跨视图检测 | ⭐ **评审者 / 检测器**（⛔ 自由文本 description） |
| ⛔ 裁决者 | ⛔ **LLM 从不担任** —— ⭐ 见 B4 |
| ⚠️ ⛔ **块类型分类** | ⛔⛔ **LLM 被迫兼任分类器 —— ⭐ 而这是一个未被承认的角色**，⭐ 见下方 |

#### ⚠️⚠️ **一个隐藏的 LLM 角色：⛔ 块类型（system vs environment）是 LLM 猜的**

⭐ **M，§6 逐字：**

> "the detection of inconsistencies related to these rules (concerning environment blocks) could be improved: currently, **the block type as defined in Definition 5 is not exported to the textual format generated by TTool from BDs. Therefore, the classification of system/environment blocks relies on the LLM's analysis, based on the provided UCD and specification.** Exporting it to the textual format would reduce the possible LLM's interpretation errors here."

⭐⭐⭐ **这一条很要紧：⭐ `RC1` / `RC2` / `RC3` **三条跨视图规则全部以 `type_B ∈ {system, environment}` 为前提**，⛔ 而这个属性**没有传给 LLM** —— ⛔ **于是三条规则是在一个由 LLM 自行推断的属性上被判定的。** ⛔ **即跨视图检测的那 33 条 `External` 结果，其判据本身带一层未测量的 LLM 推断误差。**

⚠️ ⭐ **而这个属性在 TTool 模型里是确定性可得的**（⭐ Definition 5 里 `type ∈ {system, environment}` 就是块描述的一个字段）—— ⛔ **只是导出格式没带它。⭐ 这是一个纯工程遗漏造成的方法学缺陷。**

⭐⭐ **对我们的直接教训：⭐ 检查一遍我们喂给 LLM 的模型文本表示，⛔ 有没有把某个我们已经确定性掌握的属性漏掉、⛔ 从而逼模型去猜。** ⭐ 这属于「确定性信息未下传」类缺陷，⛔ 症状是模型在一个本可免费获得的事实上出错。

### B3 · prompt 策略

| 策略 | 有无 | 证据 |
| :-- | :-: | :-- |
| ⭐ **规则以自然语言注入 prompt** | ⭐ **有** | ⭐ M，⭐ 论文称之为 "knowledge database injected in the consistency request"。⭐⭐ **源码逐字实取**（`AIDiagramCoherencyWithFormalRules.java`，⭐ 5353 B，`HTTP 200`）：`"#Respect: In a block diagram, the blocks representing actors as defined in the use-case diagram must bear identical names to their corresponding use cases.\n"` ＋ `"#Respect: In a block diagram, blocks representing actors from the use case diagram must not be connected together.\n"` ＋ ⚠️ `"#Repect: In a block diagram, a block representing an actor from the use case diagram must be interconnected with at least one block that doesn't represent an actor."`（⛔ **原文拼写 `#Repect`，⛔ 少一个 `s`**）＋ `"#Respect: Give any incoherency you can identify concerning the two provided diagrams"` |
| ⭐ **结构化输出约束**（⛔ prompt 层，⛔ 非受限解码） | ⭐ **有** | ⭐ M，⭐ 源码逐字：`"When you are asked to identify all the relevant incoherencies between two diagrams, return them as a JSON specification formatted as follows:{incoherencies: [{ \"diagram\" : \"diagram1 or diagram2\", \"description\": \"description of the incoherency\"}...]}"`；⭐ 正文 §5.1.3 给出同一段文本的截图版 |
| ⭐ **只要 JSON 不要解释** | ⭐ **有** | ⭐ M，⭐ 源码逐字："provide only JSON (no explanation before or after)." |
| ⭐ **解析 / 校验失败回灌** | ⭐ **有** | ⭐ M，§4 `U3` 逐字："If this analysis fails, then **a new request is forged from the results of the syntax analysis**, then the process goes back to stage (U1)." |
| ⭐ **精简自研文本格式**（⛔ 非 SysML v2） | ⭐ **有** | ⭐ M，§5.1.3 逐字："TTool is equipped to generate textual specifications of these diagrams in **SysML v2 format**. However, **this format's verbosity leads to extensive contexts, affecting both the cost and the quality of results.** To mitigate this, we have developed **a more concise textual format, based on element lists.**" ⭐ 样例逐字：`actors: User Propeller_Anerometer ...` / `Use cases: Define_PositionAndCourse ...` / `Connections: include(Activate_BowThrusters, Maintain_SetPositionAndCourse) ...` |
| ⭐ **切分生成**（slicing） | ⭐ **有** | ⭐ 见第 1 问「切分机制」三条证据 |
| ⛔ few-shot | ⛔ **无** | ⭐ 正文与源码都无（S） |
| ⛔ CoT | ⛔ **无** | ⭐ 无（S） |
| ⛔ self-consistency 投票 | ⛔ **无** | ⭐ 无（S） |
| ⛔ 工具调用 / function calling | ⛔ **无** | ⭐ 无（S） |
| ⛔ 多智能体辩论 | ⛔ **无** | ⭐ 无（S） |
| ⛔ 角色扮演 | ⛔ **无** | ⚠️ ⭐ 源码里的 prompt 无 "You are an expert..." 式角色设定（S） |

⭐ **prompt 是否公开** → ⭐ **公开（🟢）**，⭐ 见 D 节。⚠️ ⭐ 论文用四个脚注（6/9/11）逐一点名实现文件路径 —— ⭐ **这是一个很好的做法：⭐ 把 prompt 的权威版本指向源码而不是附录截图。**

### ⚠️⚠️ B3 附一条**对我们直接有用的负面发现**（⛔ 而且这是它的**首次**报告）

⭐ **M，§6 逐字：**

> "The management of rules outlined in Table 3 within the LLM-based consistency handling loop **was challenging.** Specifically, **when these rules are incorporated into the knowledge database injected in the consistency request (see Stage C1 of Figure 1), the LLM tends to exclusively focus on these rules, thus ignoring other consistency aspects.** To address this issue, we have introduced two separate features in TToolAI: one enabling users to evaluate consistency considering the embedded rules in the request, and the other allowing for consistency checks to be performed without these rules. As a result, **to achieve a comprehensive cross-view consistency evaluation, users are currently required to engage TToolAI sequentially in two different operations.** This may also be seen as an advantage since users of TTool can somehow customize the consistency rules they intend to address."

⭐⭐⭐ **这就是「把闭合词表塞进检测 prompt 会造成隧道视野」这条发现的**最早**一处报告（2024）。** ⭐ 期刊版（SoSyM 2026）把同一条重述并给出对策「跑两遍取并集」。

⚠️⚠️ ⭐ **计数纪律：⭐ MODELS 2024 与 SoSyM 2026 是**同一团队**，⛔ 算**一个**独立观察。⭐ 连同 [internetware2025-sysml-behavior-generation.md](./internetware2025-sysml-behavior-generation.md)（⭐ 北航团队，⭐ 逐字 "As rule complexity increases, **LLMs may lose focus on the original requirements**"）与我们自己（⭐ `occupancy_after` 的 `nl_cue` 把模型从 `edge_declared` 引开，⛔ 324 格里 `edge_declared` 被问 **0.0%**），⭐⭐ **合计三个独立团队、四处报告。⛔ 不要把 Télécom Paris 的两篇数成两票。**

⭐ **它的对策与我们的不同**：⭐ 它把「带规则 / 不带规则」做成两个功能让用户各跑一遍取并集；⛔ **我们成本已经 212.6×，⛔ 翻倍不可接受** —— ⭐ 我们的解是修 `nl_cue` 的措辞（⭐ 实测 0 → 4/6）。

### B4 · ⭐⭐ 循环与裁决者

⭐ **已在第 3 问完整回答，⭐ 此处只留摘要表。**

| 循环 | 裁决者 | ⭐ 类型 | 终止 | 最大轮数 | ⭐ 边际收益 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| `U1→U2→U3→U1` | ⭐ `U3` 语法 ＋ 规则检查 | ⭐ **`parser/编译器` ＋ `确定性规则`** | ⭐ 收敛 / 撞上限 | ⛔ **原文未提供** | ⛔ **未报**（⭐ 单例：一次即好） |
| `B1→B2→B3→B1` | ⭐ `B3` 同上 | ⭐ **`parser/编译器` ＋ `确定性规则`** | ⭐ 同上 | ⛔ **原文未提供** | ⛔ **未报** |
| `U4`/`B4` 接受门 | ⛔ **人** | ⭐ **`人`** | ⭐ 人叫停 | ⛔ 无 | ⛔ **未报** |
| `C1→C2→C3→U1/B1` | ⛔ **人** | ⭐ **`人`** | ⭐ 全解决 / 时限 / 最大轮数 | ⛔ **原文未提供** | ⛔⛔ **未报，⛔ 且第 2 轮没跑** |

⛔⛔ **`LLM 自评` = 无。⛔ `sound oracle` = 不在这条链上。**

### B5 · ⭐ 中间表示

⚠️ **两套，⭐ 一套闭合一套开放，⛔ 绝不能混谈。**

| | ⭐ ① 形式化规则目录 | ⛔ ② LLM 检测输出 |
| :-- | :-- | :-- |
| 有无 | ⭐ 有 | ⭐ 有（⛔ 但无结构） |
| 形态 | ⭐ **规则目录 / 缺陷类型学**（⭐ 25 条编号规则，⭐ 每条带形式化表达式） | ⛔ **自由文本 JSON**：`{"diagram": "diagram1 or diagram2", "description": <自由文本>}` |
| ⭐ **是否闭合** | ⭐⭐ **闭合**（⭐ 从固定 25 条里选；⛔ 声明会演化） | ⛔⛔ **完全开放** —— ⛔ 无类别字段、⛔ 无枚举、⛔ 无规则 ID 回指、⛔ description 随便写 |
| ⭐ **谁定的 / 谁选** | ⭐ **作者预编目录**（⭐ 三来源：文献综述 ×2 ＋ 大量实测）；⛔⛔ **按阶段硬编码挑选，⛔ 不是 LLM 选**（⭐ 三份名单见第 2 问） | ⛔ LLM 自由生成 |
| ⭐ 形式化基础 | ⭐⭐ **有 —— §3.1 给出 UCD 与 BD 的完整形式定义**（⭐ Definition 1–6：字母表与名字 · UCD 基本集 · UCD 4-元组 · BD 基本集 · 块描述 10-元组 · BD 6-元组） | ⛔ 无 |

⭐ **另有一个「LLM 实际产出的对象」与「形式定义要求的对象」之间的差集，⭐ 论文形式化写出来了（M，§3.2.1/§3.2.2）：** ⭐ LLM 产出的 UCD 是 $\langle (V,E), type_V, name_V, type_E \rangle$ 但 $E \subset Vertices^2$（⛔ 可引用图中不存在的顶点）、$name_V : Vertices \to A^*$（⛔ 全域而非仅 $V$）；⭐ LLM 产出的 BD 里 $\mathcal{L} \subset Blocks^2$、$\mathcal{C} \subset Blocks^2 \times Sign_{gen}^2$、⛔ **且 $name_X$ 不再是内射**（⛔ 即会重名）。⭐⭐ **这个「LLM 产物 vs 合法产物」的形式化差集是一个很干净的表述手法，⭐ 值得学。**

⭐⭐ **对照结论（⛔ 与我们 19 条谓词）：⛔⛔ 它对「闭合词表 ＋ LLM 自动选」这个组合给不出任何先例 —— ⭐ 又是一票**不算**。** ⚠️ ⭐ **连同 [sosym2026-state-machine-consistency.md](./sosym2026-state-machine-consistency.md) 与 [internetware2025-sysml-behavior-generation.md](./internetware2025-sysml-behavior-generation.md)，⛔ 本轨目前已有**三票**「闭合但人/规则/工具选」，⛔ **零票**「闭合且 LLM 选」。**

### B6 · 模型

⚠️⚠️ **这一格有一处论文内部不一致，⛔ 必须写清。**

| 用途 | 模型 | 证据 |
| :-- | :-- | :-- |
| ⭐ **框架声称的底层 LLM** | ⭐ **GPT-4-turbo ＋ GPT-4o** | ⭐ M，§4 逐字："Our framework is an extension of TTool-AI [3], **using OpenAI's GPT-4-turbo, and GPT-4o as underlying LLMs**" |
| ⛔ **评测里实际用于生成**（⭐ automotive braking ＋ space-based system 的全部图） | ⛔ **GPT-3.5** | ⭐ M，§5.2 逐字："**All diagrams of the automotive system and of the space-based system were generated using GPT 3.5**, and the diagrams of DPS were generated with GPT 4." |
| ⛔ 评测里实际用于生成（⭐ DPS 的图） | ⛔ **GPT-4** | ⭐ 同上 |
| ⭐ 检测（`C1–C3`，⭐ Table 4 全部数字） | ⛔ **GPT-4** | ⭐ M，§5.2 逐字："**GPT 4 was used to identify inconsistencies.**" |
| ⭐ 纠正 | ⛔ **GPT-4** | ⭐ M，§5.2 逐字："**GPT 4 was used to perform these diagram updates.**" |
| ⭐ 有无多模型对照 | ⛔⛔ **无** —— ⛔ 无同一任务的跨模型对比表 | ⭐ §7 把它列为 future work（逐字："**Integrating our implementation with other LLMs would also be beneficial for comparing performance and diversifying responses.**"） |
| ⭐ 工具版本 | ⭐ **TTool 3.0 beta, build 14731** | ⭐ M，§5.2 逐字："For these evaluations, **TTool version 3.0 beta, build: 14731**, was used." |
| ⛔ temperature / seed | ⛔ **原文未提供** | ⛔ 全文无 |

⚠️⚠️ **不一致点：⭐ §4 说框架用 GPT-4-turbo 与 GPT-4o，⛔ 而 §5.2 报告的评测只用了 GPT-3.5 与 GPT-4。⛔⛔ GPT-4o 在评测里一次都没出现。** ⛔ **登记为 F §3。**

⚠️⚠️ **X1 的代际折扣在这篇上要打得很重：⛔ Table 4 的 69 条数据里，⭐ 三分之二的系统（automotive braking ＋ space-based）的图是 **GPT-3.5** 生成的，⭐ 检测全部由 **GPT-4** 做。⛔⛔ 即这是 2023–2024 代的数字。** ⭐⭐ **反过来说：⭐ 期刊版用 **GPT-5.1** 复测时发现「连两跳路径都看不见」（⭐ 见 [sosym2026-state-machine-consistency.md](./sosym2026-state-machine-consistency.md) 首节）—— ⛔ **那说明这条线的核心缺陷不是代际能解决的**，⭐ 于是本篇的**结构性**结论仍然有效，⛔ 只有**绝对分数**要打折。

### B7 · ⭐ 确定性成分

| 环节 | 是什么 | ⭐ 在哪一段 |
| :-- | :-- | :-- |
| ⭐ **TTool syntax checker** | ⭐ SysML 图的语法检查器 —— ⭐⭐ **M，§3.2 逐字："TTool, the framework we rely on, incorporates a syntax checker for SysML diagrams. This feature enforces numerous consistency rules established in existing literature directly through syntax verification, eliminating the necessity for these rules to be replicated in our LLM-specific rule set."** | `U3` / `B3` |
| ⭐ **形式化规则检查器** | ⭐ 对生成结果算法化验 25 条中的一个子集（⭐ UCD 查 5 条 · BD 查 4 条） | `U3` / `B3` |
| ⭐⭐ **建构时强制**（correct-by-construction） | ⭐ 从 LLM 输出画图时**把一批规则做成不可违反** | `U5` / `B5` |
| ⭐ JSON 解析 | ⭐ LLM 回传的结构化响应解析 | `U2` / `B2` / `C2` |
| ⭐ 图导文本 | ⭐ TTool 自研精简文本格式（⛔ 不用 SysML v2，⭐ 因为太啰嗦） | `C1` |
| ⭐ 切分（slicing） | ⭐ BD 生成拆成「块 / 连接 / 属性」多次查询 | `B2` |
| ⛔ **模型检查器 / 求解器** | ⛔⛔ **没接进一致性循环** | ⚠️ ⭐ TTool 有 SysML 直接模型检查 [5]（⭐ §2.3 逐字："the formal semantics of SysML profiles enable **direct model-checking of SysML models** [5] without the need for intermediate formalisms"），⛔ **但本文不用它** |
| ⛔ **仿真器** | ⛔ 同上，⛔ 提到但不参与 | — |
| ⛔ **图算法 / 依赖图** | ⛔ **本篇无** | ⚠️ ⭐ 那是**期刊版**才加的（⭐ SoSyM 2026 的 `model2graph` ＋ Algorithm 1） |

⭐⭐⭐ **B7 这一格的核心发现（⛔ 也是本篇与期刊版最大的差别）：**

⭐⭐ **本篇的确定性成分全部集中在「生成端把关」（`U3`/`B3` 检查 ＋ `U5`/`B5` 建构强制），⛔ 检测端一点确定性都没有 —— ⭐ 跨视图检测 100% 由 LLM 做，⭐ 而裁决由人做。**

⚠️ ⭐ **两年后期刊版补的正是这一格**：⭐ SoSyM 2026 加了一条**完全不含 LLM 的确定性检测臂**（⭐ 依赖图 ＋ 图遍历），⭐ 并拿到 `0 误报 0 漏检`（⛔ `n = 3`）。⭐⭐ **即这条线自己的演化方向就是「给检测端加确定性底座」 —— ⭐ 而这正是 M1 第二条设计原则要动的地方。**

⭐⭐ **对我们的含义：⭐ 本篇是「检测端只有 LLM」的形态；⭐ 期刊版是「检测端 LLM ＋ 确定性双臂」的形态。⭐⭐ 我们是「求值端有 sound oracle、裁决端是 LLM」的形态 —— ⛔ 三种都不一样。⭐ 而这条线的演化告诉我们：⭐ 他们选的路是「加一条并列臂」，⛔ 不是「把裁决者换掉」。**

---

## C. 实验

| 字段 | 值 |
| :-- | :-- |
| `baseline` | ⛔⛔ **无。** ⛔ 无 rules-only 臂、⛔ 无 human 臂、⛔ 无其它 LLM 方法臂、⛔ 无跨模型臂。⚠️ ⭐ **连自家两臂互比都没有**（⭐ 那是期刊版才有的） |
| `dataset` | ⭐ **3 个系统 × (2 BD × 2 UCD) = 12 个图对**（⭐ Table 4 有 24 行 = 12 对 × 2 张图）。⭐ 系统来源：⭐ **automotive braking system** ＋ **space-based system**（M，§5.2 逐字："The two first systems are **use cases taken from two distinct European projects**"，⛔ **本篇未点名是哪两个项目** —— ⚠️ ⭐ 期刊版才点名 FP7 EVITA 与 H2020 SPARTA）· ⭐ **dynamic positioning system (DPS)**（⛔ 作者自撰规约） |
| ⭐ **分母怎么定的** | ⚠️⚠️ **分母是「检出的条数」而不是「应检出的条数」** —— ⛔ 即 **precision 分母，⛔ 无 recall 分母**。⭐ `Total = 69` 是**真不一致**的检出数，`Errors = 6` 单列且**从总数中剔除**（M，逐字："they are **excluded from the total inconsistency count** and are not addressed during the correction phase"） |
| ⭐ 缺陷从哪来 | ⭐⭐ **天然存在，⛔ 无人工播种** —— ⭐ 被检的 BD/UCD 本身就是 LLM（GPT-3.5/GPT-4）生成的，⭐ 不一致是生成的副产物 |
| `metrics` | ⭐ `Inconsistencies detected`（Internal / External / Errors / Total）＋ `Inconsistencies corrected`（Internal / External / Total 分数式）。⛔⛔ **无任何 `@k` 口径** —— ⛔ 每格只跑一次。⛔ **无时间、⛔ 无 token、⛔ 无成本** |
| ⭐ `judged_by` | ⛔⛔ **作者自己，⭐ 主观，⛔ 无第三方、⛔ 无标注者间一致性、⛔ 无 $\kappa$、⛔ 无一致率。** ⭐ 作者自己写在 §6（逐字）："Note also that **there is subjectivity in the classification of the detected inconsistencies** (determining their relevance to specific diagrams, identifying them as errors)." ⭐ 紧接着自我辩护（逐字）："However, until recently, **crossed-view consistency was mostly performed manually until now in TToolAI** (as in most UML/SysML toolkits)." |
| `human_baseline` | ⛔ **本篇无。** ⚠️⚠️ ⭐ **但配套 Zenodo 档里有一份**（⭐ `results.ods`，⭐ 覆盖 SMD，⛔ **属前作 MODELSWARD 2024**）—— ⭐ 见 D 节与 E §1 ④ |
| `runs` | ⛔⛔ **每格一次，⛔ 报单次，⛔ 无方差、⛔ 无重复采样。** ⛔ 全文未提 temperature、seed 或重复运行 |
| ⭐ `adverse_results` | ⭐ **处理得相当坦白** —— ⭐ 见下方专节 |

### ⭐ Table 4 逐格数字（⛔ 全表抄下，⭐ 已复算自洽 ✅）

| System | Test | Diagram | Internal | External | Errors | Total | Corr. Int. | Corr. Ext. | Corr. Total |
| :-- | :-- | :-- | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Automated braking | BD1 vs UCD1 | BD1 | 1 | 2 | 0 | 3 | 1 | 2 | 3/3 |
| | | UCD1 | 0 | 0 | 0 | 0 | 0 | 0 | — |
| | BD1 vs UCD2 | BD1 | 0 | 1 | 0 | 1 | 0 | 1 | 1/1 |
| | | UCD2 | 0 | 3 | 0 | 3 | 0 | 2 | 2/3 |
| | BD2 vs UCD1 | BD2 | 5 | 1 | 1 | 6 | 4 | 1 | 5/6 |
| | | UCD1 | 0 | 1 | 1 | 1 | 0 | 1 | 1/1 |
| | BD2 vs UCD2 | BD2 | 4 | 2 | 0 | 6 | 3 | 1 | 4/6 |
| | | UCD2 | 2 | 2 | 0 | 4 | 2 | 2 | 4/4 |
| Space-based system | BD1 vs UCD1 | BD1 | 3 | 6 | 0 | 9 | 3 | 5 | 8/9 |
| | | UCD1 | 0 | 0 | 0 | 0 | 0 | 0 | — |
| | BD1 vs UCD2 | BD1 | 4 | 1 | 0 | 5 | 3.5 | 1 | 4.5/5 |
| | | UCD2 | 3 | 1 | 0 | 4 | 2.5 | 1 | 3.5/4 |
| | BD2 vs UCD1 | BD2 | 2 | 2 | 0 | 4 | 1 | 2 | 3/4 |
| | | UCD1 | 1 | 1 | 1 | 2 | 1 | 1 | 2/2 |
| | BD2 vs UCD2 | BD2 | 1 | 4 | 0 | 5 | 1 | 4 | 5/5 |
| | | UCD2 | 0 | 2 | 0 | 2 | 0 | 2 | 2/2 |
| Dynamic positioning system | BD1 vs UCD1 | BD1 | 1 | 1 | 0 | 2 | 1 | 0 | 1/2 |
| | | UCD1 | 0 | 0 | 1 | 0 | 0 | 0 | — |
| | BD1 vs UCD2 | BD1 | 2 | 2 | 0 | 4 | ⭐ **2** | 1.5 | ⭐ **3.5/4** |
| | | UCD2 | 2 | 0 | 0 | 2 | 0 | 2 | 2/2 |
| | BD2 vs UCD1 | BD2 | 1 | 0 | 0 | 1 | ⭐ **1** | 0 | ⭐ **1/1** |
| | | UCD1 | 1 | 1 | 0 | 2 | 1 | 1 | 2/2 |
| | BD2 vs UCD2 | BD2 | 3 | 0 | 1 | 3 | ⭐ **3** | 0 | ⭐ **3/3** |
| | | UCD2 | 0 | 0 | 1 | 0 | 0 | 0 | — |
| ⭐ **Total** | | | **36** | **33** | **6** | **69** | ⭐ **30** | **30.5** | ⭐ **60.5/69** |

⭐ **加 ⭐ 标的四格就是期刊版下修的那三格所在**（→ 附答悬案一）。

⭐ **我方复算全部通过 ✅**：⭐ `Internal + External = Total` **24/24**；⭐ `Corr.Int + Corr.Ext = Corr.Total 分子` 且 `分母 = Total` **20/20**；⭐ 合计 `36 / 33 / 6 / 69 / 30 / 30.5 / 60.5` 全部对上；⭐ `60.5/69 = 87.68%` ↔ 论文 `87%` ✅；⭐ `6/75 = 8.00%` ↔ 论文 `8%` / `92%` ✅；⭐ BD 侧 **49**、`49/12 = 4.08` ↔ 论文 `averaging 4` ✅；⭐ UCD 侧 **20**、`20/12 = 1.67` ↔ 论文 `1.7` ✅；⭐ external `30.5/33 = 92.42%` > internal `30/36 = 83.33%` ↔ 论文 `slightly higher for external` ✅。

### ⭐ 那 `0.5` 半分 —— ⛔ **判定规则未落盘**

⛔ Table 4 里出现 `3.5` `2.5` `1.5` 三处半分（⭐ 全在 Space-based 与 DPS）。⛔ **全文无 `partial` / `half` / 打分细则。** ⛔ **而半分直接进了 `60.5/69 = 87%` 这个主结果。** ⚠️ ⭐ 与 [sosym2026-state-machine-consistency.md](./sosym2026-state-machine-consistency.md) F §4 是同一缺陷，⛔ **两版都没解释。**

### ⭐⭐ `adverse_results` 专节 —— ⭐ 它怎么写不利结果

⭐ **它把不利结果写在五个地方，⛔ 一个都没藏：**

1. ⭐ **正文明说误报存在并给出比例** —— ⭐ `Errors = 6`，⭐ 逐字 "**6 inconsistencies were erroneously identified—these are invalid incoherences, such as the erroneous assertion that two already connected blocks should be connected.**"
2. ⭐ **walkthrough 里主动展示一条误报** —— ⭐ §5.1.3 逐字："Additionally, the list included **another 'inconsistency' that seems irrelevant** (The block 'Controller' does not have a direct association with the 'User' or specific use cases as in [the use case] diagram)."
3. ⭐ **主动展示纠正失败** —— ⭐ §5.1.4 逐字："We can observe that **not all inconsistencies were corrected.** For example, DPS block is still unrelated to other blocks."
4. ⭐ **主动展示生成缺陷（拼写错）** —— ⭐ §5.1.2 逐字："However, it should be noted that **there is a misspelling in the actor representing the anemometer, incorrectly labeled as `Propeller_Anerometer`.**" ⭐⭐ **这条很妙：⭐ 它先在生成阶段承认拼错，⭐ 再在检测阶段展示 LLM 抓到了这个拼错 —— ⛔ 即用自己的缺陷当自己方法的示例。**
5. ⭐ **§6 Discussion 通篇是自我批评** —— ⭐ 五条改进方向全是自家缺陷：⛔ 规则注入造成隧道视野 · ⛔ 块类型没导出所以靠 LLM 猜 · ⛔ 跨视图规则没做成建构时强制 · ⛔ 自研文本格式非标准 · ⛔ 三个案例都太简单

⭐ **另有两条自我归因的方法论反省（⚠️ ⭐ 这两条对我们尤其有用）：**

- ⭐ **主动指出自家实验低估了自己**（M，逐字）："In our experiments, we integrated the entire list of detected inconsistencies (excluding those categorized as errors) into the message input in TToolAI for generating revised diagrams. **Adopting a strategy of addressing each inconsistency individually could potentially elevate the correction rate** […] LLMs tend indeed to produce more accurate results when their input is more concise: therefore, **providing the LLM with one inconsistency at a time would probably help it focus better and improve its performance.**"
- ⭐ **主动指出一个未量化的正面效应**（M，逐字）："the automated feedback loop of our framework […] help eliminate errors introduced in the LLM generation process. **However, we have not yet quantified this phenomenon**"

⭐⭐ **形态总结：⭐⭐ 「误报单列且展示样例 ＋ 纠正失败照实写 ＋ 生成缺陷当示例用 ＋ Discussion 通篇自我批评 ＋ 明说实验设计可能低估自己」。** ⚠️ ⭐ **但与 [internetware2025-sysml-behavior-generation.md](./internetware2025-sysml-behavior-generation.md) 相比它弱一档：⛔ 摘要里没有任何不利结果**（⭐ 摘要末句是 "highlighting its potential to significantly enhance consistency management in graphical modeling"，⛔ 纯正面）。⭐⭐ **期刊版才把 FP＋FN 写进摘要最后一句。⭐ 又是一条两年间演化的纪律。**

---

## D. 资产

⭐⭐ **本轮全部实取核验，⛔ 不只核 HTTP 200。**

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据 |
| :-- | :-: | :-- | :-- |
| ⭐ 论文全文 | ⭐ **🟢** | ⭐ [作者预印本 PDF](https://perso.telecom-paristech.fr/apvrille/docs/models2024_sultan.pdf) · [`10.1145/3640310.3674079`](https://doi.org/10.1145/3640310.3674079) | ⭐ **工具输出逐字**：`https://perso.telecom-paristech.fr/apvrille/docs/models2024_sultan.pdf` → `🟢 · HTTP 200 · application/pdf`（⭐ 实下 `1,235,760 B`，`PDF document, version 1.5`，⭐ 11 页，⭐ 已提取 1373 行）。⚠️ ⛔ **`https://doi.org/10.1145/3640310.3674079` → `🟠 · HTTP 403 · HTTPError 403`**（⭐ ACM DL 的 Cloudflare）。⭐ 版权页逐字 "©2024 **Copyright held by the owner/author(s)**"（⛔ 无 CC 许可声明，⛔ 与期刊版的 CC-BY 不同） |
| ⭐ **实验代码（框架）** | ⭐ **🟢** | [gitlab.telecom-paris.fr/mbe-tools/TTool](https://gitlab.telecom-paris.fr/mbe-tools/TTool) | ⭐ **工具输出逐字**：`🟢 · HTTP 200 · text/html; charset=utf-8`。⭐ 源码头逐字为 **CeCILL** 许可（`"Copyright or (C) or Copr. GET / ENST, Telecom-Paris, Ludovic Apvrille"`）。⚠️⚠️ ⛔ **GitLab 装了反爬（`go-away` / `anubis`）**：⭐ 裸 `curl` 对 raw 路径返回 **`HTTP 418`**（`<title>Checking you are not a bot</title>`，2917–2934 B）；⭐ 带浏览器 UA 时**部分**通过 |
| ⭐⭐ **prompt 是否公开** | ⚠️ **🟡** | ⭐ TTool 仓库 `src/main/java/ai/` | ⭐⭐ **公开且我实取到了一个，⛔ 但另三个被反爬拦住。** ⭐ 论文用脚注 6/9/11 逐一点名四个文件。⭐ **实取结果**：⭐ `AIDiagramCoherencyWithFormalRules.java` **`HTTP 200 · 5353 B` ✅**（⭐ B3 已逐字抄出其 `KNOWLEDGE_ON_JSON_FOR_INCOHERENCIES` 与 `QUESTION_IDENTIFY_INCOHERENCIES` 全文）；⛔ `AIUseCaseDiagram.java` · `AIBlockConnAttribWithSlicing.java` · `AIDiagramCoherency.java` 三者**均 `HTTP 418`**（⭐ 已重试 ＋ 加浏览器 UA ＋ 加延时，⛔ 仍被拦）。⭐⭐ **但这三个文件在 [sosym2026-state-machine-consistency.md](./sosym2026-state-machine-consistency.md) D 节已被实取过**（⭐ 该卡记 `AIUseCaseDiagram.java` 12343 B · `AIBlockConnAttribWithSlicing.java` 12520 B · `AIDiagramCoherency.java` 4673 B）—— ⭐ **所以「公开」这件事是坐实的，⛔ 本轮的失败是反爬而非缺失** |
| ⭐⭐ **复现包（Zenodo）** | ⭐ **🟢** | ⭐ [zenodo.org/doi/10.5281/zenodo.11936921](https://zenodo.org/doi/10.5281/zenodo.11936921) | ⭐ **工具输出逐字**：`🟢 · HTTP 200 · text/html`。⭐⭐ **我方实取完整元数据与内容**：⭐ concept DOI `10.5281/zenodo.11936921` → record **`11936922`**，⭐ title **`linuxisnotunix/ttool-ai: Models'24`**，⭐ license **`cc-by-4.0`**，⭐ created **`2024-06-17T11:45:06Z`**，⭐ 单文件 `linuxisnotunix/ttool-ai-1.zip` **`963,945 B`**，`md5:083b3902448fcc1727dec8debb713520`（⭐ **实下并复核 md5 逐位一致 ✅**）。⭐ 解包 **49 个文件 · 8,131,780 B**，⭐ 内含 git tree `3dbb937939dff1562653b015469d24d9322e7ac0`。⭐⭐ **是一个 GitHub-linked release 快照 —— ⭐ 有 DOI、有 license、有 md5，⭐ 这一点比期刊版强**（⛔ 期刊版**无** artifact DOI） |
| ⭐ NL 规约（3 个系统） | ⭐ **🟢** | ⭐ Zenodo 档 `incoherencies/specification_*.md` | ⭐ **实取逐字清单**：`specification_automatedbraking.md` **2,764 B** · `specification_dps.md` **1,247 B** · `specification_spacebasedsystem.md` **1,997 B**。⭐ 另有 `AutomatedBraking/automatedbraking.md`（2,764 B，⭐ 同内容）· `DPS/dps.md`（1,247 B）。⭐⭐ **三个系统的 NL 规约全在** |
| ⭐ TTool 模型（含判定结果） | ⚠️ **🟠** | ⭐ Zenodo 档 `incoherencies/*.xml` | ⭐ **实取逐字清单**：`incoherencies/automatedbraking.xml` **786,885 B** · `incoherencies/dps.xml` **436,865 B** · `incoherencies/spacebasedsystem.xml` **1,326,015 B** · `incoherencies/dps_forStepByStepIllustration.xml` **175,533 B**。⭐ README 逐字说明内容："Each file contains **2 block diagrams (BD) and 2 Use case diagrams (UCD)** automatically generated using the system specification. They also contain **the models corrected** thansk to the detection of incoherencies. **These incoherencies are given in the updated models.**" ⛔⛔ **判 🟠 的理由：⭐ 逐条判定内嵌在 TTool `.xml` 里，⛔ 需装 TTool 才能读，⛔ 无 CSV/JSON 逐条结果，⛔ 无 Table 4 的可下载原始表、⛔ 无那 6 条 `Errors` 的清单** |
| ⛔ Table 4 的可机读原始表 | ⛔ **⚪** | — | ⛔ **不存在。** ⭐ 我方已把 Zenodo 档 49 个文件逐一列出，⛔ **没有任何文件对应 Table 4**（⭐ 唯一的表格文件 `results.ods` 是前作的数据，⭐ 见下一行）。⛔ **与期刊版同一缺陷** |
| ⭐⭐ **人类对照数据（⛔ 属前作）** | ⭐ **🟢** | ⭐ Zenodo 档 `results.ods` | ⭐⭐⭐ **一个意外收获，⛔ 但归属必须写清。** ⭐ **实取**：`results.ods` **14,893 B**，⭐ 4 个工作表 `Platooning` / `Space-based system` / `Automated braking` / `Overall`。⭐ 列为 `Time BD (s)` · `Grade BD (/100)` · `Time SMD (s)` · `Grade SMD (/100)`，⭐ 每系统 5 次 TTool 运行 ＋ 一组学生数据。⭐ **`Overall` 逐字**：⭐ `TTool + AI` → BD `40 s / 81 分`、**SMD `178 s / 63 分`**（⭐ 标准差 `10 / 16 / 97 / 15`）；⭐ `Students` → BD `2700 s / 70 分`、**SMD `2700 s / 58 分`**（⭐ 标准差 `— / 26 / — / 32`）。⭐ 学生数 `13 + 15 + 13 = 41`。⭐ README 逐字定性："This quality is compared with one of the diagrams made by **master-level students after 21h of lectures ands labs**." ⛔⛔ **归属：⭐ 这是前作 MODELSWARD 2024 [3] 的数据，⛔ 不是本篇的** —— ⭐ 依据：⭐ ① 系统组合是 `Platooning + Space-based + Automated braking`（⛔ 本篇是 `Automated braking + Space-based + DPS`）；⭐ ② README 把它归到 "Model generation" 节，⛔ 与 "Incoherency detection and correction" 节分开；⭐ ③ 度量是生成质量评分，⛔ 与本篇的一致性检出无关 |
| ⭐ **LLM 真实输出样例** | ⭐ **🟢** | ⭐ Zenodo 档 `README.md` | ⭐ **实取**：`README.md` **6,860 B**，⭐ 含**一份完整的 7 条不一致 JSON 输出**（⭐ space-based system）＋ **一份完整的 5 条纠正 prompt**。⭐⭐ **这是第 4 问那 3 条 model-vs-NL 实例的来源。⭐ 且它是纯文本，⛔ 不是截图** —— ⛔ **这一点比论文正文强**（⭐ 正文的输出样例都是排版在 figure 里的） |
| ⚠️ 无关内容（⛔ 顺手记） | — | ⭐ Zenodo 档 `attacktrees/` · `platooning/` | ⚠️ ⭐ **档里混了别的论文的数据**：⭐ `attacktrees/` 有 3 个子系统共 14 个文件（⭐ 攻击树生成，⛔ 属另一条线）· `platooning/` 2 个文件。⛔ **且含 4 个 `.xml~` 编辑器备份与 1 个 `.~lock...#` 锁文件** —— ⭐ 即这是一个**共享的配套仓库快照**，⛔ 不是为本篇整理的最小复现包 |

### ⭐ 资产终裁（⛔ 机械判据之外的人工判断）

⭐⭐ **总体 🟢，⭐ 而且在一个关键维度上比它的期刊版更强：⛔⛔ 它有 artifact DOI（Zenodo，CC-BY-4.0，带 md5），⛔ 而期刊版没有。** ⭐ 三个系统的 NL 规约、真实 LLM 输出、纠正 prompt 都是纯文本可读。

⛔ **但三处扣分：**

1. ⛔⛔ **逐条判定结果被锁在 TTool `.xml` 里** —— ⛔ 不装 TTool 无法核 Table 4 的任何一行。⭐ **与期刊版完全相同的缺陷，⭐ 两年没改。**
2. ⛔ **论文用的 build 14731 在 GitLab 上定位不到** —— ⭐ 期刊版卡片已实测 `release 0`、⛔ 无 tag。⭐ **不过本篇有 Zenodo 快照兜底（git tree `3dbb937939`），⛔ 所以数据可定位，⛔ 只是代码不可定位。**
3. ⛔ **Zenodo 档不是最小复现包** —— ⛔ 混了攻击树与 platooning 的数据、⛔ 含编辑器备份与锁文件。⭐ 但这不影响可用性。

⚠️ ⭐ **本轮的 prompt 判 🟡 而非 🟢，⛔ 纯粹因为 GitLab 反爬拦掉了 3 个文件。⭐ 结合期刊版卡片的实取记录，⭐ 实质状态是 🟢** —— ⭐ 本卡按「本轮亲自核验到的」判 🟡 并注明。

---

## E. 对 M1 的意义

### 1. ⭐ 可取之处

| # | 可搬的设计决定 | ⭐ 证据强度 |
| :-: | :-- | :-- |
| **①** | ⭐⭐ **「建构时强制」（correct-by-construction）是一个我们没有的层次。** ⭐ 它在 `U5`/`B5` 把一批规则做成**不可违反** —— ⭐ 不是检查后打回，⛔ 而是从 LLM 输出构造制品时就把违规形态消掉（⭐ 例：属性类型未定义则默认建为 integer）。⭐⭐ **可直接搬的动作：⭐ 我们 `convert_assertions` 的 schema 违规目前走「拒绝 ＋ 回灌重试」，⛔ 而有一部分完全可以走「构造时归一化」** —— ⚠️ ⭐ 这正好呼应 [CLAUDE.md](../../../../../CLAUDE.md) §13 第 1 条的那个建议（⭐ 「改成**求值侧的确定性归一化**，⛔ 不要求任何人改任何东西」）。⭐⭐ **本篇是那条建议的一个已发表先例** | ⭐ **M**（⭐ 三份阶段名单逐条可数） |
| **②** | ⭐⭐ **喂给 LLM 的规则用「实现收紧版」，⛔ 而规范层保留通用版。** ⭐ `RU7` `RU10` `RB11` 三条都是这么做的（⭐ 脚注 7/8/10）。⭐⭐ **这是一个解决「规范该多通用 vs 运行时该多具体」的干净做法**：⭐ 论文里写通用规则（⭐ 可辩护、⭐ 可挂出处），⭐ 注入 prompt 时写工具能力内的收紧版（⭐ 可满足、⭐ 不会逼死模型）。⚠️ ⭐ 而这直接对上 [CLAUDE.md](../../../../../CLAUDE.md) §13 的第二层可满足性：⭐ **收紧到「被要求者确实做得到」的范围** | ⭐ **M**（⭐ 三条脚注逐字） |
| **③** | ⭐⭐ **「LLM 产物 vs 合法产物」的形式化差集写法。** ⭐ §3.2.1/§3.2.2 先给合法对象的形式定义，⭐ 再逐点写出 LLM 实际产出在哪些点上更弱（⛔ $E \subset Vertices^2$ 而非 $V^2$、⛔ $name_X$ 不再内射…）。⭐⭐ **这是一个把「为什么需要这些门」讲清楚的手法，⛔ 比列举错误样例更有说服力。⭐ 我们的 19 条谓词与契约门可以照这个结构重写动机段** | ⭐ **M** |
| **④** | ⭐⭐⭐ **配套档里有一份覆盖 SMD 的人类对照数据 —— ⭐ 这是 L1「外部可比数字 0 条」的一条线索。** ⭐ `results.ods` 的 `Overall`：⭐ TTool+AI 的 SMD `178 s / 63 分`，⭐ 学生的 SMD `2700 s / 58 分`（⭐ n = 41 学生，⭐ 21 小时课程后）。⭐⭐ **即：⭐ 一份**已发表**、⭐ 可下载、⭐ 带标准差、⭐ 针对**状态机制品**的人类基线。** ⚠️⚠️ **但三条限定必须一起带**：⛔ ① **它属前作 MODELSWARD 2024，⛔ 不属本篇**；⛔ ② 度量是**生成质量评分（0–100 rubric）**，⛔ 不是缺陷检出，⛔ **与我们的 `hit@k` 不可比**；⛔ ③ 评分 rubric 未公开。⭐⭐ **建议动作：⭐ 把 MODELSWARD 2024 [3] 单独抽一张卡，⭐ 专门核这份人类基线的 rubric 与可比性** | ⭐ **M**（⭐ 数字实取）· ⭐ 可比性判断 **I** |
| **⑤** | ⭐ **确定性裁决者的循环收敛得很快，快到不必报边际收益** —— ⭐ 内环唯一被记录的一次触发（`RU8` 违规）一次反馈即好；⭐ 期刊版补的「20 轮上限 never reached」印证。⭐ **这是我们「确定性那条 0 token 性价比最高、LLM 自评那两条零收益」的又一次独立外部印证** | ⭐ **S**（⭐ 从单例 ＋ 期刊版的上限陈述推出；⛔ 无逐轮曲线） |
| **⑥** | ⭐ **prompt 的权威版本指向源码，⛔ 不做附录截图。** ⭐ 论文用四个脚注逐一点名 `.java` 文件路径。⭐ 我们本来就在源码里，⭐ 这条只是印证做法可行且能过 CCF-B 的审 | ⭐ **M** |
| **⑦** | ⭐ **不利结果的写法**（→ C 节专节）：⭐ 误报单列并展示样例 ＋ 纠正失败照实写 ＋ **用自家生成的拼写错当自家检测方法的示例** ＋ 明说实验设计可能低估自己 | ⭐ **M** |

### 2. ⛔ 不可取 / 陷阱

| # | 陷阱 | ⚠️ 它踩没踩我们踩过的坑 |
| :-: | :-- | :-- |
| **①** | ⛔⛔⛔ **`Errors` 从分母里剔除，⛔ 且没有 recall 分母。** ⭐ 逐字 "they are **excluded from the total inconsistency count**"。⛔ 于是 `92% relevant` 的分母是 `69+6=75`，⛔ 而 `87%` 的分母是剔除后的 `69` —— ⛔⛔ **同一节里两个分母，⛔ 且不标注** | ⛔ **这正是本仓库 §3.5 第 4 条「评测口径迁就结果」的形态。** ⭐ 我们的 98 条能力分母 ＋ `hit@1/@3/@all` 三口径同报，⭐ 比它严格得多。⛔ **两版（本篇与期刊版）都有这个缺陷** |
| **②** | ⛔⛔ **判定全由作者自己做，⛔ 无第三方、⛔ 无 $\kappa$、⛔ 无一致率，⛔ 且作者自认 "subjectivity"** | ⛔ **「自证式验证」（§3.5 第 5 条）。** ⭐ 我们的人工判定同样是自判，⛔ 但判据先落盘、⭐ 逐位可复算 |
| **③** | ⛔⛔ **`n` 极小且无重复采样** —— ⭐ **12 个图对 · 3 个系统 · 每格跑一次**，⛔ 无 temperature/seed 记录、⛔ 无方差。⭐ 论文自己承认（逐字）："our evaluation relied on **three case studies involving relatively simple diagrams** and it would be interesting to assess our framework using more complex diagrams" | ⛔ 我们 324 格 × 3 轮 ＋ `@k` 三口径。⛔ **不要引用它的 `87%` / `92%` 当任何量级参照** |
| **④** | ⛔ **`0.5` 半分的判定规则未落盘** —— ⭐ Table 4 有 3 处半分，⛔ 全文无打分细则，⛔ 而半分直接进主结果 | ⛔ **判定规则未落盘的典型。⛔ 与期刊版同一缺陷，⛔ 两年未改** |
| **⑤** | ⚠️ **纠正阶段「哪些条目要修」由人挑，⛔ 且误报被人先剔掉** | ⛔ **所以 `87%` 的纠正率是「人已经把错的滤掉之后」的纠正率，⛔ 不是端到端自动率。⭐ 若我们要报修复率，⭐ 必须区分「端到端」与「人已过滤」两个口径** |
| **⑥** | ⛔⛔ **外环第 2 轮没跑** —— ⭐ 逐字 "**Another iteration** on inconsistencies (stages C1 to C3) **could resolve** these remaining issues"。⛔ **「could」是猜的，⛔ 没有数据** | ⚠️ ⭐ 我们有那条数据（⛔ 第 3–5 轮零收益），⛔ **而且方向相反。⭐ 别把它的「再跑一轮应该能好」当成先例信** |
| **⑦** | ⛔⛔ **把规则注进检测 prompt 会造成隧道视野** —— ⭐ 逐字 "the LLM tends to **exclusively focus on these rules, thus ignoring other consistency aspects**"。⛔ 对策是**跑两遍取并集** | ⭐⭐ **这是我们已踩过的坑的**最早**外部报告。⛔ 但它的对策对我们不适用 —— ⭐ 我们成本已 212.6×，⛔ 翻倍不可接受；⭐ 我们的解是修 `nl_cue`（⭐ 实测 0 → 4/6）。⚠️ ⭐ **注意它还把这个缺陷说成「也可以看作优点」（逐字 "This may also be seen as an advantage"）—— ⛔ 那是把工程妥协包装成功能，⛔ 不要学** |
| **⑧** | ⛔⛔⛔ **三条跨视图规则建立在一个 LLM 自己猜的属性上。** ⭐ `RC1`/`RC2`/`RC3` 全以 `type_B ∈ {system, environment}` 为前提，⛔ 而该字段**没有导出给 LLM** | ⛔⛔ **这是「确定性信息未下传，逼模型去猜」类缺陷 —— ⭐ 而它污染的正是本篇声称的新贡献（跨视图规则）那 33 条数据。⭐⭐ 直接教训：⭐ 我们要复查一遍喂给 LLM 的模型文本表示，⛔ 有没有把某个已确定性掌握的属性漏掉** |
| **⑨** | ⛔ **无跨模型对照，⛔ 且声称用的模型与实测用的模型不一致**（⭐ §4 说 GPT-4-turbo ＋ GPT-4o，⛔ §5.2 实际是 GPT-3.5 ＋ GPT-4，⛔ GPT-4o 一次未用） | ⛔ **引用它的任何数字都必须标模型代次。⭐ 我们 `gpt-5.5` × `claude-opus-4-7` 两模型对照，⭐ 这一点上我们更强** |
| **⑩** | ⛔ **LLM 输出无结构** —— ⛔ `{"diagram": ..., "description": <自由文本>}`，⛔ 无类别、⛔ 无规则 ID 回指、⛔ 无可机械求值的断言 | ⛔⛔ **所以它的「检出」永远需要人读。⭐ 这是我们相对它的结构性优势，⛔ 也意味着它的 `87%`/`92%` 与我们的任何数字都不可比** |

### 3. ⚠️ 与我们的关键差别（⛔ 为什么不能直接照搬）

| # | 差别 | ⛔ 为什么阻断照搬 |
| :-: | :-- | :-- |
| **①** | ⛔⛔⛔ **评测对象根本不是行为模型** —— ⭐ UCD 是功能概览、⭐ BD 是结构视图。⛔ **状态机在本篇里只出现在「实现支持」与「future work」两处** | ⛔⛔ **这是本卡与其它卡最大的不同：⭐ 它的 C 节数字**不能**进任何「状态机上的效果」类统计。⭐ 它只能当**流水线形态**参照物**（→ A 节 `boundary` 说明）。⛔ 若要搬进 L1/L2，⛔ 它很可能过不了边界门 |
| **②** | ⛔⛔ **问题不同：⭐ 它是多视图模型互比，⭐ 我们是模型 vs NL** | ⛔ 它的 reference 是**另一个形式化制品**（⭐ UCD 与 BD 互为参照）。⛔⛔ **我们的 reference 是自然语言 —— ⛔ 没有第二张图可以比。⭐ 我们能搬的只有架构形状，⛔ 不是它的判据** |
| **③** | ⛔ **中间表示的「谁选类」完全相反** | ⭐ 它：⛔ **三份硬编码名单**，⛔ 与被检对象无关。⭐ 我们：⭐ **LLM 逐需求自动选**。⛔⛔ **所以它对「闭合词表 ＋ LLM 自动选」这个组合给不出任何先例 —— ⭐ 本轨要数的那个组合，⛔ 这篇不算一票**（⚠️ ⛔ **已连续三票不算**） |
| **④** | ⛔⛔ **它的检测端一点确定性都没有** —— ⭐ 跨视图检测 100% 由 LLM 做，⭐ 裁决由人做，⛔ 无 sound oracle | ⭐⭐ **这决定了引用方向：⭐ 它是「检测端只有 LLM 时会怎样」的证据（⛔ 8% 误报 ＋ 未测漏检）。⭐⭐ 而这条线自己两年后补的正是「加一条确定性检测臂」 —— ⭐ 所以真正的先例在期刊版，⛔ 不在本篇。⭐ 本篇的价值是**演化的起点**，⛔ 不是可搬的终点** |
| **⑤** | ⛔ **它的「多次生成 → 不一致」归因于 token 上限，⛔ 而那个前提对当代模型已不成立** | ⭐⭐ **可搬的是「多次生成必须配一道跨次一致性门」这个结构，⛔ 不是「token 上限是缺陷来源」这个论断。⭐ 我们的 `split → convert` 逐条转换是同构风险点，⛔ 但成因是方法设计，⛔ 不是上下文容量**（→ 第 1 问末段） |

---

## F. 存疑与未核项

1. ⚠️⚠️ **`RC1` 的形式化表达疑似缺一个否定量词，⛔ 但我不能断言那是论文缺陷** —— ⭐ 规则文字是「No link shall exist between two environment blocks」，⛔ 而表达式抽出来是 `⟨B1,B2⟩ ∈ L s.t. typeB1=environment ∧ typeB2=environment`（⛔ 无 `∄` / `¬`）。⭐ **两个独立抽取器交叉验证**：⭐ PyPDF2 在 `⟨` 前留下一个未映射字节 `\x9a`；⭐ `pdftotext -layout` 在同一位置留下空白。⭐ 且全文 `∄` 与 `¬` 的出现次数都是 **0**，⛔ 而 `∀` 29 次、`∃` 13 次都抽到了。⭐⭐ **所以最可能的解释是 PDF 里有一个 `∄`（U+2204）两个抽取器都没能映射。⛔ 我未做像素级核对（⛔ 未渲染该页图像逐字比对），⛔ 因此不登记为论文缺陷。**
2. ⛔⛔ **`8%` vs `7%` 本篇内部冲突（⭐ 我方实测，⛔ 这是一条真实的数字缺陷）** —— ⭐ §5.3 逐字 `8%` 误报 / `92%` 相关（⭐ 我方复算 `6/75 = 8.00%` ✅）；⛔ §6 逐字 "(**7%** in our evaluation)"。⭐ 我方复算 `6/75 = 8.00%` · `6/69 = 8.70%`，⛔ **两个都不是 7%。** ⛔ **我不为它编一个能凑出 7% 的口径。**
3. ⚠️ **`GPT-4o` 在评测里一次都没用到，⛔ 但 §4 说框架用它** —— ⭐ §4 逐字 "using OpenAI's **GPT-4-turbo, and GPT-4o** as underlying LLMs"，⛔ 而 §5.2 的三句归属全是 GPT-3.5 / GPT-4。⛔ **未能确认 §4 那句是「实现支持」还是「评测使用」。**
4. ⚠️ **两个欧洲项目未点名** —— ⭐ §5.2 只说 "use cases taken from **two distinct European projects**"。⭐ [sosym2026-state-machine-consistency.md](./sosym2026-state-machine-consistency.md) C 节记为 **FP7 EVITA**（automotive braking）与 **H2020 SPARTA**（space-based），⛔ **但那是期刊版的信息，⛔ 本篇正文里没有。** ⛔ 未回期刊版原文核这一条。
5. ⚠️ **`0.5` 半分的判定规则未知** —— ⛔ 已 grep 全文 `partial` / `half` / `0.5` / `counted`，⛔ 无任何打分细则。⛔ **3 处半分直接进了主结果 `60.5/69`。**
6. ⚠️ **无法核 Table 4 的任何一行** —— ⛔ 逐条判定内嵌在 TTool `.xml`（175 KB–1.33 MB），⛔ 需装 **TTool 3.0 beta** 才能打开。⛔ **本卡未装 TTool，⛔ 所以 Table 4 只做了内部自洽复算（✅ 全通过）＋ 与期刊版的逐格对拍（✅ 已定位三格差异），⛔ 未做与原始制品的对拍。**
7. ⚠️ **`results.ods` 的评分 rubric 未知** —— ⭐ 它给了 `Grade BD (/100)` 与 `Grade SMD (/100)`，⛔ **但工作簿里没有评分细则，⛔ README 里也没有**（⛔ 只说 "compared with one of the diagrams made by master-level students after 21h of lectures ands labs"）。⛔⛔ **所以那份人类基线目前不可用于任何定量比较** —— ⭐ 需回前作 MODELSWARD 2024 [3] 找 rubric。⛔ **本卡未读那篇。**
8. ⚠️ **`platooning/` 与 `attacktrees/` 的归属未逐一确认** —— ⭐ 我按 README 的分节与 `results.ods` 的系统组合判断 `results.ods` ＋ `platooning/` ＋ 三个系统目录属前作、`incoherencies/` 属本篇。⛔ **这是我方推断（S），⛔ README 没有逐目录标明论文归属。**
9. ⚠️ **GitLab 反爬拦掉 3 个 prompt 文件** —— ⭐ 已试裸 `curl`（`HTTP 418`）· 浏览器 UA（⭐ 4 个里过了 1 个）· 加 2 秒延时重试（⛔ 仍 418）。⛔ **`AIUseCaseDiagram.java` · `AIBlockConnAttribWithSlicing.java` · `AIDiagramCoherency.java` 本轮未取到。** ⭐ 但期刊版卡片已实取过（⭐ 12343 / 12520 / 4673 B），⭐ **所以「公开」坐实，⛔ 只是本轮未亲自读到。**
10. ⚠️ **Distinguished Paper Award 未从官方页核实** —— ⭐ 两条间接证据（⭐ 检索结果 ＋ 作者主页文件名 `models2024_sultan_distinguishedpaperaward.pdf`），⛔ **预印本正文内无奖项声明，⛔ 我未访问 MODELS 2024 官方 award 页。**
11. ⚠️ **页码 149–159 未从原件核实** —— ⭐ 来自检索结果，⛔ **预印本 PDF 无页码**，⛔ ACM DL 被 403 拦。
12. ⚠️ **`Internal` 列混装两种东西，⛔ 而论文不区分** —— ⭐ 按定义 `Internal` = "within a single diagram"，⛔ 但从 Zenodo README 的真实输出看，⭐ 落到这一列的既有「图内自相矛盾」也有「图相对规约有缺失」（⭐ 那 3 条 `as per the specification`）。⛔ **我无法从 Table 4 反推每一列里各占多少** —— ⭐ 逐条判定锁在 `.xml` 里。⛔⛔ **所以「这篇实际做了多少 model-vs-NL 判定」这个数，⛔ 拿不到。**
13. ⚠️ **前作 MODELSWARD 2024 [3] 未读** —— ⭐ `B1–B5` 大部分来自那篇（M，§4 逐字："Stages B1 to B5 were already implemented in TTool-AI [3]"），⭐ 且那篇拿了 Best Paper Award（⭐ 据检索结果）。⭐ 全文入口：[doi.org/10.5220/0012320100003645](https://doi.org/10.5220/0012320100003645)。⛔ **本卡未读。** ⚠️⚠️ ⭐ **建议单独抽卡，⭐ 两个理由：⭐ ① 它有那份覆盖 SMD 的人类基线（⭐ 见 E §1 ④）；⭐ ② 它才是 BD 生成链（含 slicing）的原始出处。**
14. ⚠️ **同组另有一篇标题直指我们设计原则的工作未读** —— ⭐ B. Sultan, L. Apvrille, *Towards Safe LLM-Based Model Driven Engineering: when Syntax Checking and **Safety Formal Verification Join the Loop***, ERTS 2026（[hal.science/hal-05513959](https://hal.science/hal-05513959)）。⚠️⚠️ ⭐ **标题里 "Safety Formal Verification Join the Loop" 正是「把裁决者换成 sound oracle」。⛔ 本卡未读。** ⭐ [sosym2026-state-machine-consistency.md](./sosym2026-state-machine-consistency.md) F §11 也已标记为强烈建议单独抽卡 —— ⭐⭐ **本卡再次确认这个建议，⛔ 且认为它的优先级高于本篇。**
