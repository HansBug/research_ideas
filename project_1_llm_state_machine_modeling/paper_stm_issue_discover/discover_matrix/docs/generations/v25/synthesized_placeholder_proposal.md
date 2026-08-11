# v25 提案：让「复合态无默认入口」变得可断言

## ⛔ 本提案已作废，改动已撤销（两份运行前 review 各自独立判「禁止开跑」）

两份 review 给出**互相独立、各自足以致命**的理由，两条我都接受：

### 代码正确性侧的致命理由：**极性反了**

`prompts.py:104` 逐字「Create confirmed issues only from **False** assertions」。而 reviewer 实测：

    initial_target(composite='…0047.CollisionAvoidanceSystem', child='…UnspecifiedInitial')  -> True
    initial_target(composite='…0047.…RearEnd',   child='…InvalidInitialtr_0005')             -> True state_declared('…UnspecifiedInitial', kind='any')                                        -> True

**True 的断言 = 已履行的义务 = 零 finding。** 我许可的形状按构造**不可能**成为发现。仓库每一处都写死极性（L27 / L34 / L46 / L551「That False is the finding.」），唯独我新写的那句丢掉极性并断言了相反的事。

真正可用的形状是 `initial_target(X, <NL 点名的状态>) is False` —— **它根本不需要把占位符写进绑定**，也不需要任何 prompt 许可。§六「不需要新谓词」只在这个负向形状下成立，与本提案的正向读法无关。

### 更糟：改动会翻掉两条**当前命中**的记录

`EIS-0035-01`（6/6）与 `EIS-0043-02`（5/6）所在 pair 都含占位符，且占位符挂在**同一个 composite** 上。许可等于告诉转换器可以把 `child=DoorShut`（False，命中）重绑为 `child=占位符`（True，零发现）。`capability.py:528-550` 把「frozen model 的已声明路径」列为合法来源，**没有确定性关卡拦得住**。

⛔ **而原 §五 预注册表里没有「已有命中丢失」这一行** —— 这个损失在我计划的读数里**不可见**，净效应会被错误归因（因为四条动机记录已按 §四 排除出能力度量）。

### 基础错误：改在了错误的阶段

`predicate_bindings` 是 **Requirement** 的字段，由 **Requirement Splitter** 产出（`schemas.py:207`「They give **the converter** the terms to bind」）。**我测的是 Splitter 的绑定，许可加在了 Converter 上**，而 `REQUIREMENT_SPLITTER_PROMPT` 一字未改。按原 §五 自己那一行「主体位仍为 0 → 位置问题」，**这个结果跑之前就静态可判**，那 66 格买不到信息。

### 与同 prompt 内两条无条件禁令直接冲突

| 行 | 阶段 | 逐字 |
| --: | :-- | :-- |
| 170 | Converter | Never acknowledge a contradiction … and then use a broader presence query that **evaluates True** |
| 180 | Reviewer | reject any script that … turns it into a **passing broad-presence assertion** … must evaluate **False** |
| 51 | Req Reviewer | **do not** ask the author to re-anchor those bindings to whatever the model already declares（点名 `containment` / `initial_target` / `cardinality`） |

许可只加进了 Converter，Reviewer 侧的拒绝规则原样保留 —— **听话的 converter 写出的东西，听话的 reviewer 必须拒。** 且 L51 明令禁止的正是我指示 converter 去做的那个 re-anchor。

📌 **这是本次会话第三次「断言某阶段被许可/禁止某事而未读相邻约束」**（前两次都在 L379 上）。三次的共同结构不是没查，是**查了、把事实写下来了、下一步推理时没有用它**。

### 公平性侧的致命理由：**C3 段是台账论证的去标识化改写**

reviewer 把台账 `0032-eis.md:21` 与我的新句逐项对上，**连情态动词都对上了**：

| 台账原文 | 我写的 prompt |
| :-- | :-- |
| 三个 Region 都是复合态却**没有初始伪态** | because a composite **declared none** |
| R4.5 投影**不得不**各合成一个 | the projection **had to synthesize** |
| **这是缺陷的机器证据** | **which is the finding** |

我删掉的只有 `UnspecifiedInitial` 与 pair 号 —— 正是 CLAUDE.md §3.5.-1 逐字描述的「不含任何台账标识符的『答案形状』」。原 §四 自评「不含期望缺陷、不含判定结论」**两条都假**。

⛔ **我的抽象化测试只按标识符扫描，而 §3.5.-1 明写这种扫描会失败。** 我读过那条规则、在提案里引用了它、然后用了它说会失败的方法。

### 留出集本身已污染，且留出这个装置对类级规则不适用

- 12 个留出 pair 中 `0019` / `0053` **被直接读过台账**（commit `3d0049c1` body 有据）。
- 原 §五 把 `0029` / `0043` 列为「非动机记录」，**两个都错** —— 门侧规则 `_omission_placeholder_only`（`e41ca47c`）的动机 body 写明是 `0029-claude`。**我只反向标注了 prompt 那一半动机，漏了它依赖的门侧那一半。**
- 更根本：留出处理的是**实例级**污染。C3 交出的是**整个缺陷类的检出规则**，在留出 pair 上命中的仍是「被告知」而非「被引导方法」。

### 运行时孪生体（早于 v25，但本改动的全部目的就是让它开始触发）

`nodes.py` 的 `_omission_placeholder_only` 写入的 rationale：

> "… **the placeholder is the omitted declaration**, not an unattributable artefact."

它经 `renderer.py:465` 的 `render_adjudicator_input` 整体序列化进裁决者 user input。**它只在这一缺陷类上触发，并把结论直接交给裁决者。** 此前休眠（主体位 0/4373），本改动会激活它 —— 故必须计入本次泄漏面，不能以「不是我引入的」豁免。

---

## ⚠️ 原 §二 的实测数字还有两处错，就地更正

| 我写的 | 实际 | 错因 |
| :-- | :-- | :-- |
| 占位符在需求绑定中出现 **3 次** | 去重后 **1 次 / 1026**，集中在 **1 个格** | 那 3 次是**同一条**绑定的三份累积状态快照。**结构化解析修掉了正则问题，没有修掉快照问题** —— 第 2 轮的错误换了结构化外衣重来一次 |
| 分母 **37 格** | **19 格**（`matrix-v24` 单版；37 对不上任何一个 universe） | —— |

⛔ **我在一个自陈教训是「先打印分母」的小节里写错了分母。** 且「模型会伸手去用」这个机制主张的证据是**单点观测**，不是 3 次尝试。

另有一处前置条件不成立（reviewer I3）：许可写「because a composite **declared none**」，但 `0047` 的 `InvalidInitialtr_*` 是**作者声明了入口、只是指到子域外**（`nodes.py:3527`「a stand-in for an initial target the author got **wrong**」）。原 §二 把 `UnspecifiedInitial` 与 `InvalidInitial*` 当同一类处理，**这一步也错了**。

---

## 两份 review 一致认可、应当保留的部分

1. **代理禁令从「synthetic root or completion holder」扩宽为「projection-synthesized element」是实质改进** —— 实测那次违规用的 `event_consumed(source=…)` 既非 root 也非 completion holder，**原句字面确实管不到它**。这一半可以单独重提，但需枚举类别（`FinalWait*` 等性质不同）。
2. **「绑定词表内的名字不是臆造」是干净的词表契约陈述**，不含结论。
3. 观测法定位（问题全部在断言生成之前）与「NL 是否点名绑定所需元素」这个两分**未被质疑**。

## 下一步的前置条件（两份 review 共同要求）

1. `docs/generations/v24/predicate_bottleneck.md` §四 已裁定：放开需求来源必须**同时**给出「工具已报的 vs 方法自推的」可执行区分，且能力主张只能记后者。**该裁定未做，v25 事实上选了路线 1 却没实现附带条件。**
2. 若要走「主体位」，形状必须写成**负向**（在缺陷模型上取 `False`）。
3. 改 **Splitter**，不是 Converter；且 **Reviewer 侧必须同步**。
4. 预注册必须加「已有命中丢失」这一行，并改为**类级**不可计入（所有 pair，含留出）。
5. 运行时 rationale 须改为只陈述归因状态与依据类型，不下「占位符就是作者遗漏」的判语。

---

📌 以下保留原文供追溯。**其中每一处「拟改动」「预注册」都已作废**，只有 §一 的观测与两分仍有效。

---

## 一、这条提案从何而来（不是猜的）

观测法（[docs/generations/v24/predicate_bottleneck.md](../v24/predicate_bottleneck.md) §十二）把 12 条 `wellformedness` 记录按四个流水线阶段逐条追踪，得到近乎完美的两分：**断言写进封存脚本的命中，没写的漏检。** 这排除了断言执行、attribution 门、判定三个环节 —— **全部问题在断言生成之前。**

随后逐条人工读 statement，找到区分命中与漏检的**不是**谓词、**不是**合成元素、而是：

> **NL 有没有点名该谓词的绑定所需要的那个元素。**

| 记录 | primary | NL 点名了绑定所需元素？ | 命中 |
| :-- | :-- | :-- | --: |
| `EIS-0035-01` | `initial_target` | ✅「starts in the **DoorShut** state」 | 6/6 |
| `EIS-0043-02` | `initial_target` | ✅「first transitions to the **PumpState**」 | 5/6 |
| `EIS-0032-01` | `initial_target` | ✗ 缺陷是三个 Region 都**没有**初始伪态 | 1/6 |
| `EIS-0047-02` | `initial_target` | ✗ **没有**初始子状态 | 0/6 |
| `EIS-0048-02` | `initial_target` | ✗ Join2 **无**初始子状态 | 0/6 |
| `EIS-0048-03` | `initial_target` | ✗ Fork2 **无**初始子状态 | 0/6 |

### ⚠️ 一个会让机械检查判错的陷阱

`0048-02` 的 NL **确实**点名了 `Join1`，`0048-03` 点名了 `Flash` —— 但它们是**迁移目标**，而缺陷需要的绑定是「Join2 / Fork2 的**默认子态**」。**一个「该元素名是否在 NL 中出现过」的检查会把这两条误判到命中侧。** 判据必须是「点名了**绑定位置上**的那个元素」，而非「点名了某个同名元素」。

## 二、机制：形状存在、模型会伸手，但只用被禁止的那一半

投影在复合态缺默认入口时会**合成**一个占位符（`UnspecifiedInitial` / `InvalidInitial*`）。

### 实测（分母：`0032`/`0047`/`0048` 三 pair 共 **37 格 / 1221 记录 / 4373 个 `predicate_bindings`**）

| 检查 | 结果 |
| :-- | :-- |
| 占位符在给 splitter 的词表里吗 | **在**（`0047` splitter prompt 中 16 次） |
| 需求绑定里出现占位符的次数 | **3 / 4373** |
| 这 3 次都在哪个绑定位 | **全部 `event_consumed(source=...)`** —— 即**代理**位 |
| 出现在**主体**位（`initial_target` 的 child、`state_declared` 的 subject） | **0 次** |
| 因此触发瞬时伪态拒答吗 | **0 次** —— 门从未参与 |

### `prompts.py` L77 里已有的禁令（这是关键，我起初没注意到）

> Do not use a **synthetic root or completion holder** as a source/target **proxy** unless the input explicitly names that scope.

**它禁的正是那 3 次尝试的形态（代理位）**，而且禁得对。它没说的是另一半：

| 用法 | 例 | L77 |
| :-- | :-- | :-- |
| **代理** —— 拿合成元素替代claim 真正关于的语义元素 | 「PumpState 不可达，那我改断言占位符」 | ⛔ 正确禁止 |
| **主体** —— 把它作为 claim 本身的对象 | 「X 的初始目标**就是**占位符 ⇒ 未声明默认入口」 | **未提及** |

📌 **模型的本能被正确拦下，而另一条路它不知道存在。** 4373 次里 0 次。

### ⚠️ 本节数字在一次调查里错了三轮，必须记录

| 轮 | 得数 | 错因 |
| --: | :-- | :-- |
| 1 | 「绑定 **0** 次」 | `glob.glob` **不做花括号展开**，`00{32,47,48}-*` 匹配到 **0 个目录** —— 空列表与「真的从未」输出完全相同 |
| 2 | 「**17** 次」 | 正则扫 JSON 文本，同一条绑定在多份累积状态快照里被重复计数 |
| 3 | 「**1** 条独立」 | 去重后只剩 1 条，但仅覆盖 6 个谓词、220 字符窗口 |
| **4（本节采用）** | **3 / 4373，全代理位** | 结构化解析 `predicate_bindings`，遍历全部谓词，**并打印分母** |

⛔ **第 1 轮的无效结果曾被我用来支持一次 src 改动，该改动已撤销。** 它躲过检查的原因很具体：**「0 次」是一个看起来有意义的结果**，且我在脚本里预先写好了「若为 0 说明模型从不尝试」的解读 ——空结果落进来时没有任何摩擦。

📌 **由此得到一条廉价判据：任何得出「0 / 从未 / 全部」的度量，先打印分母。**

### 被否证的另一个解释

~~合成元素本身区分命中与漏检~~ —— 指纹在命中侧 2/4、漏检侧 3/6，**几乎相同，不区分**。

## 三、拟改动（唯一一处）

**改 L77 那一句本身**，不新增第六处（遵守「一条策略只能有一个归属地」）。原句只禁「代理」用法而未提「主体」用法，补上这个区分：

原句：

> Do not use a synthetic root or completion holder as a source/target proxy unless the input explicitly names that scope.

改为：

> Do not use a projection-synthesized element as a *proxy* -- standing in for a semantic element the claim is really about -- unless the input explicitly names that scope. Reporting such an element as the *subject* of the claim is a different act and is permitted: when the projection had to synthesize a default entry because a composite declared none, that synthesized entry is in `declared_model_vocabulary`, and binding a predicate to it states what the artifact actually does, which is the finding. Binding to a name the vocabulary lists is never fabrication; fabrication is introducing a name it does not list.

三点说明：

1. **不是放开禁令。** 代理禁令原样保留，且从「synthetic root or completion holder」**扩宽**为「projection-synthesized element」—— 实测那 3 次违规用的是 `event_consumed(source=...)`，既非 root 也非 completion holder，**原句字面管不到它**。
2. **新增的只是「主体位」这一条通路**，它在 4373 次绑定里从未被使用。
3. **无第六处。** 改动全在 L77 一句之内。

## 四、公平性自审（reviewer 会问的，先答）

### 抽象化测试

把措辞抽象后问「它表达的是通用建模原则还是这个样本的答案」：

- 它陈述的是**投影工具的一个行为**（缺默认入口时合成占位符）与**一条许可**（绑定词表内的名字不是臆造）。
- **不含**任何 pair 号、状态名、期望缺陷、期望真值、判定结论。
- 不告诉模型「哪里有缺陷」，只告诉它「这个形状是合法的」。

### 激活面（⚠️ 这是**误伤面**回测，不是通用性证据）

`.fcstm` 投影产物中含占位符指纹的 pair：**20 / 60（33%）**

| 分组 | pair | 数 |
| :-- | :-- | --: |
| 在矩阵 11 pair 内 | 0006 0029 0032 0035 0038 0043 0047 0048 | 8 |
| **矩阵外（留出）** | 0004 0014 0016 0017 0019 0028 0033 0044 0046 0053 0057 0058 | **12** |

按记忆纪律「回测证明不了通用性」：**上面的分布只说明这条规则不会只在一个 pair 上生效（误伤面/激活面可测），不能证明它通用。** 通用性只能由活体运行判定 —— 规则会改变模型后续行为，产出分布本就不同。

### ⛔ 按引入动机反向标注：这条规则的**动机是四条特定记录没被发现**

按记忆纪律「最可靠的判据是查引入动机」：本规则的引入动机确实是 `EIS-0032-01` / `EIS-0047-02` / `EIS-0048-02` / `EIS-0048-03` 漏检。

**因此这四条记录在 v25 上的结果不得计入发现能力。** 它们只能作为「方法 + 该样本共同演化」的观测。

**能力度量必须落在从未参与规则编写的 pair 上** —— 上表的 12 个留出 pair 提供了这个条件。这也意味着：**本条改动的能力主张要等全量 60-pair 实验才能兑现**，v25 的 11-pair 运行只能给出「规则是否产生行为变化、是否造成多报」这两个更弱的读数。

📌 **这一节不是免责声明，是这条改动的度量设计。** 若 reviewer 认为四条记录仍可计入，请给出理由 ——默认按不可计入执行。

## 五、预注册的判读条件（跑之前写死）

| 观察 | 判读 |
| :-- | :-- |
| **主体位**绑定次数从 0 变正，且四条动机记录命中上升 | **不作为能力证据**（动机已烧掉） |
| 多报（`fabricated` / `grounded-extra`）显著上升 | 规则**过宽**，需收窄或撤销 |
| **主体位**绑定次数仍为 0 | 规则**未生效**，是措辞或位置问题，不是能力问题 |
| **代理位**绑定次数上升（原为 3） | 扩宽后的代理禁令**反而失效**，净负面，须撤销 |
| 非动机记录（如 `0006` / `0029` / `0035` / `0038` / `0043`）出现新命中 | **弱正面信号**，仍需留出集确认 |
| 命中不变而修订轮数上升 | 规则制造了 reviewer 争议，净负面 |

## 六、与另外两处不可表达性的关系

这是**第三处**词表不可表达性发现，但**性质不同**：

| 发现 | 是否需要新谓词 |
| :-- | :-- |
| 事件粒度（[docs/protocol/fused_event_policy.md](../../protocol/fused_event_policy.md) §四） | **需要** `event_cardinality`，不属本代次 |
| join/junction 类型错配（`PAIR-G-REC-06`） | **需要**，台账已自陈 |
| **复合态无默认入口（本文件）** | **不需要** —— 形状已存在，缺的是许可 |

📌 前两处是能力上限问题，这一处是**已有能力未被使用**。这也是为什么它值得在本代次做。
