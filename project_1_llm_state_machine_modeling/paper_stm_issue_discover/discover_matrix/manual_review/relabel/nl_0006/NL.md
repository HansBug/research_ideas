<!-- RELABEL schema=paper1.relabel.nldoc.v1 nl_dir=nl_0006 -->
# NL 规约材料 · `nl_0006`

⛔ 本文件由 [generate.py](../generate.py) 生成，**没有任何填写区** —— 它是只读材料。⭐ 判读要填的东西全在同目录的 `<pair>.md` 里。

⭐ 本页服务同目录的 **6** 份工作单：[`0006`](./0006.md)、[`0016`](./0016.md)、[`0026`](./0026.md)、[`0036`](./0036.md)、[`0046`](./0046.md)、[`0056`](./0056.md)。⭐ 它们由**同一份 NL 规约**（sha8 `a01c022f`）生成 6 个不同制品，⛔ 所以 NL 侧材料只有一份，⛔ 制品侧各不相同。

分段口径：`line_split`（按物理行切，与 pipeline 同口径），共 4 段。台账里的「NL 第 N 句」按这套编号读。

## §1 译文纪律（⛔ 先读这三段再看表）

⛔ **译文是给人判缺陷用的，⛔ 不是给人读着舒服用的。** 它严格直译，⛔ 不意译、⛔ 不润色、⛔ 不补原文没有的信息（⛔ 含不补主语、不补量词、不补逻辑连接词）；状态名 / 事件名 / 变量名 / 守卫表达式一律**保留英文原样**，建模术语保留英文并在紧跟的括号里给中文。⭐ 原文含糊的地方译文**照样含糊** —— ⛔ 替它消歧就等于替你做了本轮要你自己做的判断。⭐ 译文是**辅助**，⛔ 判据仍以英文原文为准；两者不一致时以原文为准并请回报。

⭐ 两种方括号标注的含义：`〔原文如此：…〕` 指**原文自身**有语法 / 拼写 / 数格错误，译文照直译并说明错在哪 —— ⛔ 它不是译文的错，⛔ 也不构成模型的缺陷；`〔译者存疑：…〕` 指**原文这里没说清**（谁是主语、并列项是「且」还是「或」、源状态是哪个），⭐ 它直接决定判缺陷时这一句**能不能**用来说模型「违反」了什么。

口径与验收依据：[translations/TRANSLATION_SPEC.md](../translations/TRANSLATION_SPEC.md)；本份译文的原始 JSON：[translations/nl_0006.json](../translations/nl_0006.json)；装载与对拍：[nl_zh.py](../nl_zh.py)。

## §2 逐段：原文与中文严格翻译

| 段 id | 原文 | 中文严格翻译 |
| :-- | :-- | :-- |
| `NL-L001` | 1 This state machine model describes the state transitions of a UAV swarm. | 1 本 state machine model（状态机模型）描述一个 UAV swarm（无人机集群）的 state transitions（状态迁移）。 |
| `NL-L002` | 2 Before the mission is completed, the UAV swarm continuously performs target search tasks, during which it operates within three different state areas. | 2 在 mission（任务）完成之前，UAV swarm（无人机集群）持续地执行 target search tasks（目标搜索任务），在此期间它在三个不同的 state areas（状态区域）之内运作。〔译者存疑：state areas 不是标准 UML 术语，此处按字面直译为“状态区域”，未译作 region（区）；原文所指究竟是 orthogonal region（正交区）、三个并列的状态、还是三组状态分区，无法从原文判定，故不消歧〕 |
| `NL-L003` | 3 When the UAV swarm is intercepted, it transitions to the formation adjustment state. | 3 当 UAV swarm（无人机集群）被拦截时，它迁移到 formation adjustment state（编队调整状态）。 |
| `NL-L004` | 4 During flight, if task assignment information is received, it enters the attack state. After completing the attack, the number of UAVs in the swarm decreases accordingly. | 4 在 flight（飞行）期间，如果收到 task assignment information（任务分配信息），它进入 attack state（攻击状态）。在完成 attack（攻击）之后，swarm（集群）中的 UAV（无人机）数量相应地减少。 |

## §3 逐段判读提示（该段约束了哪个元素 · 歧义点 · 边界外部分）

⛔ 提示只陈述「原文这一句说了什么、没说什么」，⛔ 不含任何裁决 —— ⭐ 「所以模型应该怎样」是本轮要你自己填的，⛔ 材料不替你填。

⚠️⚠️ **提示里也不含任何关于被测制品的断言** —— ⛔ 一份 NL 服务 6 个 pair，这一页是 6 份工作单共用的，⛔ 讲制品的话必然对其中 5 份为假。⭐ 因此「这个状态在不在」「这条边有没有」一律请自己到各份工作单的 §1.3（作者源，带行号）与 §4（按该 pair 现算的清单）核对，⛔ 不要指望提示替你回答。⚠️ 2026-08-13 之前的旧版工作单**违反过这一条**，若你读过旧版，见 [README.md](../README.md) §十。

- `NL-L001`：【约束元素】仅为全局性陈述，界定建模对象是一个 UAV swarm，未约束任何具体的状态、事件、变量或迁移。【歧义】“a UAV swarm”用不定冠词，未指明集群规模、成员数量，也未说明单机是否单独建模。【边界外】无。
- `NL-L002`：【约束元素】状态与层次。要求存在“目标搜索”这一持续进行的行为；并要求这段期间的运作发生在“三个不同的 state areas”之内，这是一条对状态划分 / 层次结构的数量约束（“三个”）。另外“Before the mission is completed”蕴含一个 mission 完成与否的条件，⛔ 但原文既未给出承载它的变量名（V），也未给出对应的事件名（E）。【歧义】①“during which”的先行词不明：可指“mission 完成之前的整段时间”，也可指“执行 target search tasks 的期间”，两种读法下“三个 state areas”的作用范围不同。②“three different state areas”所指不明——可能指 orthogonal region（正交区）、可能指三个并列的普通状态、也可能指三个状态分组；且原文未点名是哪三个，判缺陷时无法确定该与哪三个元素比对。③“target search tasks”用复数，但未说明是多个不同任务还是同一任务的多次执行。④未说明 mission 完成后会发生什么，既未给出后继状态也未提到 final state。【边界外】⛔ 本句有两处落在建模对象边界之外。其一，“continuously performs”表达的是持续性 / do-activity（状态内持续活动）语义，而本项目边界 M = (S, E, V, Tr, A) 不含时钟、不含持续活动，只能把“搜索”表示为一个状态的驻留，不能表示“不间断地执行”这一时序性质。其二，若“state areas”确指 orthogonal region（正交区），则其并发语义（多个区同时活跃）同样在边界之外，不得据此把“未能表达并发”判为缺陷。
- `NL-L003`：【约束元素】迁移（Tr）。触发条件为“UAV swarm 被拦截”，目标为 formation adjustment state。⛔ 原文只说了这一步，未规定它要由几条边实现。【模态】⚠️ 原文是一般现在时陈述句“it transitions to”，没有 can / will / must / continuously 中的任何一个；译文相应写作“它转移到”，未加“会 / 将 / 必须 / 可以”。⛔ 本句只规定“进入”，完全没有提及进入 formation adjustment state 之后能否离开、以及离开的条件与目标；判定“该状态是否应为吸收态”时，本句既不构成“必须能出来”的依据，也不构成“不能出来”的依据。【歧义】①未说明源状态：是任意状态下被拦截都成立，还是仅限于第 2 句所述的搜索期间。②“is intercepted”为被动语态，施动者未给出，也未说明拦截是外部事件还是可观测条件。③“the formation adjustment state”用小写散文写法，未说明它指的是一个复合状态整体，还是其内部的某个子状态。【边界外】无。
- `NL-L004`：【约束元素】迁移（Tr）＋变量（V）/ 动作（A）。前半句约束一条迁移：触发为收到 task assignment information，目标为 attack state。后半句要求“swarm 中的 UAV 数量”在攻击完成后减少，这需要一个表示无人机数量的变量及其更新动作，⛔ 而原文既没有给出该变量的名字，也没有给出减量的表达式。【歧义】①“During flight”未对应任何具名状态，无法判定它是一个独立状态、是所有状态的公共前置条件、还是纯背景描述。②“it enters”的先行词不明：句内最近的名词是 task assignment information，语义上更可能是第 3 句的 the UAV swarm。③“After completing the attack”未说明数量减少发生在何处——attack state 的内部动作、退出动作、迁移动作，还是后继状态的入口动作。④“decreases accordingly”未给出减少的数量、减少的依据或“accordingly”所相应的对象。⑤未说明攻击完成后转到哪个状态，⛔ 原文对「攻击之后」没有任何文字。【边界外】无（本句的数量减少属于 V 与 A，在 M = (S, E, V, Tr, A) 之内）。

## §4 整份 NL 层面的观察（术语表 · 跨句反复出现的歧义 · 原文质量问题）

【术语与专名处理策略】(1) 领域专名 UAV / swarm / mission / flight 一律保留英文并在紧跟的括号中给出中文，原因有二：其一，原文的这些词会直接进入状态与标签的命名，保留英文便于逐条比对；其二，原文的 mission 与 task(s) 在中文里同样译作“任务”，若全部意译会把两个不同层级的概念合并，使第 2 句“mission 完成之前执行 target search tasks”的层级关系丢失。(2) 原文中以小写散文形式出现的名称（formation adjustment state、attack state、task assignment information），按建模术语处理：保留英文原样 + 括注中文，不改大小写、不加引号、⛔ 也不替换为任何驼峰标识符，以免把“原文写了什么”与“它被实现成什么”混为一谈。(3) state machine model、state transitions、state areas 按建模术语处理，保留英文 + 括注中文。【原文点名了什么】⛔ 本份 NL 通篇为小写散文，**没有**给出任何驼峰标识符、任何事件名、任何变量名：可与状态对应的只有 formation adjustment state 与 attack state 两处小写短语，可与事件对应的从句共四处：is intercepted、task assignment information is received、the mission is completed、completing the attack，⛔ 四处一律没有事件名。⭐ 逐条比对时须自行到 §1.3 去看实际写了哪些元素，⛔ 本观察不代为列举。【反复出现的歧义】(1) 代词 it 在第 2、3、4 句各出现 1 次、共 3 次，均需跨句回指才能确定先行词，其中第 4 句的 it 句内无先行词，最近名词为 task assignment information，回指关系最弱。(2) 全篇没有一处使用情态动词（无 can / will / must / should / may），四句全部是一般现在时陈述句，唯一的持续性标记是第 2 句的 continuously。因此原文对“进入某状态后能否离开”这一类问题始终保持沉默——第 3 句说了进入 formation adjustment state，但全篇没有任何文字规定它之后必须、可以或不能离开；译文严格保持了这一沉默，未补出任何出口语义。(3) 原文对状态的命名一律用小写散文短语（formation adjustment state / attack state），无法据此判定它对应的是复合状态还是其内部子状态。【原文质量】未发现语法、拼写或数格错误，故全篇无〔原文如此〕标注。但存在两处术语层面的不规范：其一，“state areas”不是 UML / 状态机领域的标准术语，无法确定其外延；其二，第 4 句的“During flight”引入了一个阶段名，⛔ 而原文其余部分从未再提及它，也没有把它与任何具名状态挂钩。另需注意行内格式：原文句子编号为“数字 + 一个空格”（1␣ 2␣ 3␣ 4␣），无点号；第 1、2、3 行行尾各有一个尾随空格，第 4 行无尾随空格且无行尾换行；第 4 段由两个英文句子组成，而第 1、2、3 段各只有一句。以上格式已在 en 字段中逐字节保留。【边界外统计】四句中有 1 句（第 2 句）部分落在建模对象边界 M = (S, E, V, Tr, A) 之外，涉及 continuously 的持续性语义，以及 state areas 若解作 orthogonal region（正交区）时的并发语义。第 1、3、4 句完全在边界之内。

## §5 NL 原始字节（带物理行号）

```text
  1 | 1 This state machine model describes the state transitions of a UAV swarm. 
  2 | 2 Before the mission is completed, the UAV swarm continuously performs target search tasks, during which it operates within three different state areas. 
  3 | 3 When the UAV swarm is intercepted, it transitions to the formation adjustment state. 
  4 | 4 During flight, if task assignment information is received, it enters the attack state. After completing the attack, the number of UAVs in the swarm decreases accordingly.
```
