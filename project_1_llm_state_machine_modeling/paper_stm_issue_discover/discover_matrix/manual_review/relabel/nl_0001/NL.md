<!-- RELABEL schema=paper1.relabel.nldoc.v1 nl_dir=nl_0001 -->
# NL 规约材料 · `nl_0001`

⛔ 本文件由 [generate.py](../generate.py) 生成，**没有任何填写区** —— 它是只读材料。⭐ 判读要填的东西全在同目录的 `<pair>.md` 里。

⭐ 本页服务同目录的 **6** 份工作单：[`0001`](./0001.md)、[`0011`](./0011.md)、[`0021`](./0021.md)、[`0031`](./0031.md)、[`0041`](./0041.md)、[`0051`](./0051.md)。⭐ 它们由**同一份 NL 规约**（sha8 `abb20a21`）生成 6 个不同制品，⛔ 所以 NL 侧材料只有一份，⛔ 制品侧各不相同。

分段口径：`line_split`（按物理行切，与 pipeline 同口径），共 3 段。台账里的「NL 第 N 句」按这套编号读。

## §1 译文纪律（⛔ 先读这三段再看表）

⛔ **译文是给人判缺陷用的，⛔ 不是给人读着舒服用的。** 它严格直译，⛔ 不意译、⛔ 不润色、⛔ 不补原文没有的信息（⛔ 含不补主语、不补量词、不补逻辑连接词）；状态名 / 事件名 / 变量名 / 守卫表达式一律**保留英文原样**，建模术语保留英文并在紧跟的括号里给中文。⭐ 原文含糊的地方译文**照样含糊** —— ⛔ 替它消歧就等于替你做了本轮要你自己做的判断。⭐ 译文是**辅助**，⛔ 判据仍以英文原文为准；两者不一致时以原文为准并请回报。

⭐ 两种方括号标注的含义：`〔原文如此：…〕` 指**原文自身**有语法 / 拼写 / 数格错误，译文照直译并说明错在哪 —— ⛔ 它不是译文的错，⛔ 也不构成模型的缺陷；`〔译者存疑：…〕` 指**原文这里没说清**（谁是主语、并列项是「且」还是「或」、源状态是哪个），⭐ 它直接决定判缺陷时这一句**能不能**用来说模型「违反」了什么。

口径与验收依据：[translations/TRANSLATION_SPEC.md](../translations/TRANSLATION_SPEC.md)；本份译文的原始 JSON：[translations/nl_0001.json](../translations/nl_0001.json)；装载与对拍：[nl_zh.py](../nl_zh.py)。

## §2 逐段：原文与中文严格翻译

| 段 id | 原文 | 中文严格翻译 |
| :-- | :-- | :-- |
| `NL-L001` | 1 This state machine model represents the train's basic braking device, which serves as the final execution unit for train braking operations. | 1 本 state machine model（状态机模型）表示列车的 basic braking device（基础制动装置），其作为列车制动操作的最终执行单元。 |
| `NL-L002` | 2 When the basic braking device receives a brake signal, it transitions from the initial state to the braking state. If the signal transmission fails, it proceeds to the operational state. Once the signal feedback is sent, it returns to the initial state. | 2 当 basic braking device（基础制动装置）收到一个 brake signal（制动信号）时，它从 initial state（初始状态）迁移到 braking state（制动状态）。若 signal transmission（信号传输）失败，它前往 operational state（运行状态）〔译者存疑：operational 一词原文未加界定，此处按「运行」直译，无法确定其指「正常运行」「可操作」还是某种降级运行〕〔译者存疑：原文此处用 proceeds to，与前一分句的 transitions to、后一分句的 returns to 用词不同，无法确定三者是否都指同一种 transition（迁移），故一律按字面直译，不作统一〕。一旦 signal feedback（信号反馈）被发出，它返回 initial state（初始状态）。 |
| `NL-L003` | 3 After entering the braking state, the system transitions to the brake caliper clamping state. | 3 在进入 braking state（制动状态）之后，系统迁移到 brake caliper clamping state（闸片夹紧状态）。 |

## §3 逐段判读提示（该段约束了哪个元素 · 歧义点 · 边界外部分）

⛔ 提示只陈述「原文这一句说了什么、没说什么」，⛔ 不含任何裁决 —— ⭐ 「所以模型应该怎样」是本轮要你自己填的，⛔ 材料不替你填。

⚠️⚠️ **提示里也不含任何关于被测制品的断言** —— ⛔ 一份 NL 服务 6 个 pair，这一页是 6 份工作单共用的，⛔ 讲制品的话必然对其中 5 份为假。⭐ 因此「这个状态在不在」「这条边有没有」一律请自己到各份工作单的 §1.3（作者源，带行号）与 §4（按该 pair 现算的清单）核对，⛔ 不要指望提示替你回答。⚠️ 2026-08-13 之前的旧版工作单**违反过这一条**，若你读过旧版，见 [README.md](../README.md) §十。

- `NL-L001`：【约束元素】无。本句仅界定被建模对象（basic braking device，列车制动的最终执行单元）与建模范围，不约束任何 state（状态）、event（事件）、variable（变量）、transition（迁移）或层次结构。【歧义】无。【越界部分】无（本句不含时钟约束，也不含并发语义）。
- `NL-L002`：【约束元素】隐含三个 state（状态）：initial state、braking state、operational state；并约束三条 transition（迁移）：(a) initial state → braking state，触发条件为收到 brake signal；(b) 源状态未指明 → operational state，触发条件为 signal transmission 失败；(c) 源状态未指明 → initial state，触发条件为 signal feedback 已发出。【歧义】① 「If the signal transmission fails, it proceeds to the operational state」中的 it 未指明其当时所处的状态，源状态既可读作 initial state（与收到 brake signal 并列的另一条出边），也可读作 braking state（制动过程中传输失败），原文不足以在两种读法之间裁定，因此把源端取成其中任何一个都无法据本句判为违反。② 「Once the signal feedback is sent, it returns to the initial state」同样未指明源状态：按最近先行词读是 operational state，按上下文读也可能是 braking state，或两者皆是；原文既没有说只该有一条，也没有说两条都该有。③ 「the initial state」未区分它是 UML 的 initial pseudostate（初始伪状态）还是一个名为「初始」的 simple state（简单状态）；「returns to the initial state」暗示它是可被重新进入的实体状态，但原文并未明说。④ 未说明 receives a brake signal 与 signal transmission fails 是否互斥、是否针对同一次信号传输，也未说明二者同时成立时的优先级。⑤ 未说明 initial state 是否为整个状态机的启动状态；⛔ 原文没有任何文字规定顶层初始点指向何处。【越界部分】无（本句不含任何时间/时钟约束，也不含并发或 orthogonal region（正交区）语义）。
- `NL-L003`：【约束元素】隐含一个 state（状态）：brake caliper clamping state；并约束一条 transition（迁移）：braking state → brake caliper clamping state。【歧义】① 原文未给这条迁移任何 trigger（触发）或 guard（守卫）。「After entering the braking state, the system transitions to ...」可读作 completion transition（完成迁移，即进入 braking state 后自动离开），也可读作「此后在某个未言明的条件下迁移」；⛔ 原文没有给出任何事件名，因此凡出现在这条迁移上的具名触发都不是原文给的。② 若按 completion transition 读，braking state 将是瞬时状态，与第 2 句「signal feedback 发出后返回 initial state」若也适用于 braking state 会相互冲突；原文未排除这一冲突。③ 「the system」与第 1 句的「the basic braking device」是否指同一主体，原文未明说。④ 原文未说明进入 brake caliper clamping state 之后会发生什么，该状态是否为终态未定。【越界部分】无（本句不含时钟约束，也不含并发语义）。

## §4 整份 NL 层面的观察（术语表 · 跨句反复出现的歧义 · 原文质量问题）

【术语表 / 译法固定，全文一致】state machine model = state machine model（原文用语，保留英文原样）；basic braking device = basic braking device（基础制动装置）；brake signal = brake signal（制动信号）；signal transmission = signal transmission（信号传输）；signal feedback = signal feedback（信号反馈）；initial state = initial state（初始状态）；braking state = braking state（制动状态）；operational state = operational state（运行状态）；brake caliper clamping state = brake caliper clamping state（闸片夹紧状态）。【译法政策】原文中指代状态与事件的名词短语全部为小写散文形式（the initial state、a brake signal 等），并非驼峰式标识符写法，但它们正是状态名 / 事件名的直接来源；为使读者能逐条比对，一律保留英文原短语并在紧跟的括号内给出中文，不单独译成中文。轨道交通行业惯用译名（制动、缓解、闸片、夹紧）只出现在括号内的中文里，不用来替换英文短语本身。【原文质量】未发现语法、拼写或数格错误，因此全文 0 处〔原文如此〕。但存在两类系统性不精确：(1) 第 2 句的三条迁移中有两条未指明源状态（proceeds to the operational state / returns to the initial state），代词 it 一路指代 the basic braking device 而非某个具体状态，这是本份 NL 最主要的歧义来源；(2) 迁移动词在三处分别写作 transitions to / proceeds to / returns to，是否都指 Tr 中的同一类迁移，原文未统一。【主体指代漂移】第 1、2 句的主体是 the basic braking device，第 3 句改称 the system，原文未声明二者等同。【原文覆盖范围】原文三句只点到四个状态（initial / braking / operational / brake caliper clamping）与三个信号（brake signal / signal transmission / signal feedback）；⛔ 除此之外的任何状态、事件或概念在原文中都没有依据（⭐ 原文既没有点到「松钳 / 释放」一类概念，也没有给出任何状态名或事件名的标识符写法）。【触发词覆盖】⭐ 原文一共给出四条迁移：第 2 句的三条**各自都带一个触发词**（分别是 receives a brake signal、the signal transmission fails、the signal feedback is sent）；⛔ 而第 3 句那条（braking state → brake caliper clamping state）原文**没有给出任何触发词**，见该段 note 的歧义 ①。⭐ 这只是原文覆盖情况的说明，⛔ 不构成缺陷判定。【建模对象边界】全文不含任何时间/时钟约束、不变式或并发（orthogonal region）语义，整份 NL 均落在 M = (S, E, V, Tr, A) 边界之内；未出现变量（V）与动作（A）的约束。

## §5 NL 原始字节（带物理行号）

```text
  1 | 1 This state machine model represents the train's basic braking device, which serves as the final execution unit for train braking operations. 
  2 | 2 When the basic braking device receives a brake signal, it transitions from the initial state to the braking state. If the signal transmission fails, it proceeds to the operational state. Once the signal feedback is sent, it returns to the initial state. 
  3 | 3 After entering the braking state, the system transitions to the brake caliper clamping state.
```
