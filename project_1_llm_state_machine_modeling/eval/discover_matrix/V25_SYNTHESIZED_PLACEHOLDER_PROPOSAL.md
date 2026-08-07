# v25 提案：让「复合态无默认入口」变得可断言

## 一、这条提案从何而来（不是猜的）

观测法（[PREDICATE_BOTTLENECK.md](./PREDICATE_BOTTLENECK.md) §十二）把 12 条 `wellformedness` 记录
按四个流水线阶段逐条追踪，得到近乎完美的两分：**断言写进封存脚本的命中，没写的漏检。** 这排除了断言
执行、attribution 门、判定三个环节 —— **全部问题在断言生成之前。**

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

`0048-02` 的 NL **确实**点名了 `Join1`，`0048-03` 点名了 `Flash` —— 但它们是**迁移目标**，而缺陷需要的
绑定是「Join2 / Fork2 的**默认子态**」。**一个「该元素名是否在 NL 中出现过」的检查会把这两条误判到
命中侧。** 判据必须是「点名了**绑定位置上**的那个元素」，而非「点名了某个同名元素」。

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

> Do not use a **synthetic root or completion holder** as a source/target **proxy** unless the input
> explicitly names that scope.

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

⛔ **第 1 轮的无效结果曾被我用来支持一次 src 改动，该改动已撤销。** 它躲过检查的原因很具体：
**「0 次」是一个看起来有意义的结果**，且我在脚本里预先写好了「若为 0 说明模型从不尝试」的解读 ——
空结果落进来时没有任何摩擦。

📌 **由此得到一条廉价判据：任何得出「0 / 从未 / 全部」的度量，先打印分母。**

### 被否证的另一个解释

~~合成元素本身区分命中与漏检~~ —— 指纹在命中侧 2/4、漏检侧 3/6，**几乎相同，不区分**。

## 三、拟改动（唯一一处）

**改 L77 那一句本身**，不新增第六处（遵守「一条策略只能有一个归属地」）。原句只禁「代理」用法而未提
「主体」用法，补上这个区分：

原句：

> Do not use a synthetic root or completion holder as a source/target proxy unless the input explicitly
> names that scope.

改为：

> Do not use a projection-synthesized element as a *proxy* -- standing in for a semantic element the
> claim is really about -- unless the input explicitly names that scope. Reporting such an element as
> the *subject* of the claim is a different act and is permitted: when the projection had to synthesize
> a default entry because a composite declared none, that synthesized entry is in
> `declared_model_vocabulary`, and binding a predicate to it states what the artifact actually does,
> which is the finding. Binding to a name the vocabulary lists is never fabrication; fabrication is
> introducing a name it does not list.

三点说明：

1. **不是放开禁令。** 代理禁令原样保留，且从「synthetic root or completion holder」**扩宽**为
   「projection-synthesized element」—— 实测那 3 次违规用的是 `event_consumed(source=...)`，
   既非 root 也非 completion holder，**原句字面管不到它**。
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

按记忆纪律「回测证明不了通用性」：**上面的分布只说明这条规则不会只在一个 pair 上生效（误伤面/激活面
可测），不能证明它通用。** 通用性只能由活体运行判定 —— 规则会改变模型后续行为，产出分布本就不同。

### ⛔ 按引入动机反向标注：这条规则的**动机是四条特定记录没被发现**

按记忆纪律「最可靠的判据是查引入动机」：本规则的引入动机确实是
`EIS-0032-01` / `EIS-0047-02` / `EIS-0048-02` / `EIS-0048-03` 漏检。

**因此这四条记录在 v25 上的结果不得计入发现能力。** 它们只能作为「方法 + 该样本共同演化」的观测。

**能力度量必须落在从未参与规则编写的 pair 上** —— 上表的 12 个留出 pair 提供了这个条件。这也意味着：
**本条改动的能力主张要等全量 60-pair 实验才能兑现**，v25 的 11-pair 运行只能给出「规则是否产生行为
变化、是否造成多报」这两个更弱的读数。

📌 **这一节不是免责声明，是这条改动的度量设计。** 若 reviewer 认为四条记录仍可计入，请给出理由 ——
默认按不可计入执行。

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
| 事件粒度（[FUSED_EVENT_POLICY.md](./FUSED_EVENT_POLICY.md) §四） | **需要** `event_cardinality`，不属本代次 |
| join/junction 类型错配（`PAIR-G-REC-06`） | **需要**，台账已自陈 |
| **复合态无默认入口（本文件）** | **不需要** —— 形状已存在，缺的是许可 |

📌 前两处是能力上限问题，这一处是**已有能力未被使用**。这也是为什么它值得在本代次做。
