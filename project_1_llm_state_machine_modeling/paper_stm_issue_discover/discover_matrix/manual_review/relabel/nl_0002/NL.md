<!-- RELABEL schema=paper1.relabel.nldoc.v1 nl_dir=nl_0002 -->
# NL 规约材料 · `nl_0002`

本文件由 [generate.py](../generate.py) 生成，**没有任何填写区** —— 它是只读材料。判读要填的东西全在同目录的 `<pair>.md` 里。

本页服务同目录的 **6** 份工作单：[`0002`](./0002.md)、[`0013`](./0013.md)、[`0023`](./0023.md)、[`0033`](./0033.md)、[`0043`](./0043.md)、[`0053`](./0053.md)。它们由**同一份 NL 规约**（sha8 `a391765d`）生成 6 个不同制品，所以 NL 侧材料只有一份，制品侧各不相同。

分段口径 `line_split`（按物理行切）：按物理行切分，与 pipeline 同口径，共 **5** 段（`NL-L001` … `NL-L005`）。台账里的「NL 第 N 句」与你要在工作单 §5 填的 `nl_evidence` 都按这套段 id 读。

## §1 译文纪律（先读这三段再看表）

**译文是给人判缺陷用的，不是给人读着舒服用的。** 它严格直译，不意译、不润色、不补原文没有的信息（含不补主语、不补量词、不补逻辑连接词）；状态名 / 事件名 / 变量名 / 守卫表达式一律**保留英文原样**，建模术语保留英文并在紧跟的括号里给中文。⚠️ 原文含糊的地方译文**照样含糊** —— 替它消歧就等于替你做了本轮要你自己做的判断。⚠️ 译文是**辅助**，判据仍以英文原文为准；两者不一致时以原文为准并请回报。

两种方括号标注的含义：`〔原文如此：…〕` 指**原文自身**有语法 / 拼写 / 数格错误，译文照直译并说明错在哪 —— 它不是译文的错，也不构成模型的缺陷；`〔译者存疑：…〕` 指**原文这里没说清**（谁是主语、并列项是「且」还是「或」、源状态是哪个），它直接决定判缺陷时这一句**能不能**用来说模型「违反」了什么。

口径与验收依据：[translations/TRANSLATION_SPEC.md](../translations/TRANSLATION_SPEC.md)；本份译文的原始 JSON：[translations/nl_0002.json](../translations/nl_0002.json)；装载与对拍：[nl_zh.py](../nl_zh.py)。

## §2 逐段：原文与中文严格翻译

| 段 id | 原文 | 中文严格翻译 |
| :-- | :-- | :-- |
| `NL-L001` | 1. The system begins in the PumpControl state, from which it can transition to different substates based on specific conditions. | 1. 系统在 PumpControl 状态中开始，从该状态它可以基于特定条件迁移到不同的 substates（子状态）。 |
| `NL-L002` | 2. Within the PumpControl state, there are three main substates: PumpState, WaterState, and MethaneState. | 2. 在 PumpControl 状态内，有三个主要的 substates（子状态）：PumpState、WaterState 和 MethaneState。 |
| `NL-L003` | 3. The system first transitions to the PumpState substate, where the pump is activated or controlled. | 3. 系统首先迁移到 PumpState substate（子状态），在其中泵被激活或被控制。〔译者存疑：first 既可读作「（顺序上）首先」，也可读作「（时间上）首次」；此处译作「首先」，中文无法同时保留这两种读法〕 |
| `NL-L004` | 4. The system can also transition to the WaterState substate, indicating that the pump is controlling or monitoring the water flow. | 4. 系统也可以迁移到 WaterState substate（子状态），表明泵正在控制或监测水流。 |
| `NL-L005` | 5. Similarly, the system can transition to the MethaneState substate, indicating that the pump is controlling or monitoring the methane flow. | 5. 类似地，系统可以迁移到 MethaneState substate（子状态），表明泵正在控制或监测甲烷流。 |

## §3 逐段判读提示（该段约束了哪个元素 · 歧义点 · 边界外部分）

提示只陈述「原文这一句说了什么、没说什么」，不含任何裁决 —— 「所以模型应该怎样」是本轮要你自己填的，材料不替你填。

**提示里也不含任何关于被测制品的断言** —— 一份 NL 服务 6 个 pair，这一页是 6 份工作单共用的，讲制品的话必然对其中 5 份为假。因此「这个状态在不在」「这条边有没有」一律请自己到各份工作单的 §1.2（作者源，带行号）与 §4（按该 pair 现算的清单）核对，不要指望提示替你回答。2026-08-13 之前的旧版工作单**违反过这一条**，若你读过旧版，见 [README.md](../README.md) §十。

- `NL-L001`：约束元素：初始点 + 层次 + 迁移。要求（a）系统的起始位置是 PumpControl；（b）PumpControl 之下存在多个 substate（子状态）；（c）从 PumpControl 到这些 substate 的迁移受 specific conditions 约束。歧义：①「begins in」未说明是顶层初始伪状态直接指向 PumpControl，还是只描述运行起点，因此不能据本句断定顶层初始迁移的目标必须字面为 PumpControl；②「different substates」未列举具体是哪些，与第 2 句的三个是否为同一集合原文未明说；③「specific conditions」完全未给出内容，无法据此判定守卫缺失或守卫错误——相应迁移即使没有 guard（守卫），也只能记为「NL 未指定」，不得直接判违反。
- `NL-L002`：约束元素：层次 + 状态集合。要求 PumpControl 内含三个 main substate：PumpState、WaterState、MethaneState。歧义：「main」未定义，因此无法确定本句是否禁止 PumpControl 之下再存在其他非 main 的 substate；「PumpControl 之下出现了这三个之外的直接子状态」是否应判为多余，完全取决于这一处的读法，是判缺陷时的直接争议点。本句只约束 PumpControl 的直接子状态构成，未约束这三个 substate 各自的内部结构。
- `NL-L003`：约束元素：迁移 + 顺序。要求存在一条进入 PumpState 的迁移，且该迁移在顺序上或时间上居先。歧义：①first 的两种读法见句末存疑——若读作顺序，本句即主张 PumpState 先于 WaterState、MethaneState 被进入，这与把三者置于并列位置的写法有张力；②「activated or controlled」中的 or 是择一还是同义并举，原文未明；③本句未指明该迁移的源状态（PumpControl 自身、还是 PumpControl 内的某个起点）。⭐ 本句是否被满足，须自行到 §1.3 逐行核对「有没有一条以 PumpState 为目标的迁移」，⛔ 本提示不代为回答。
- `NL-L004`：约束元素：迁移。要求存在一条进入 WaterState 的迁移。歧义：①「can also」未给出任何条件，与第 1 句的 specific conditions 是否指同一组条件原文未明；②未说明该迁移的源状态是 PumpControl 自身、PumpState，还是 PumpControl 内某个未被点名的起点；③「the pump is controlling or monitoring the water flow」是对 WaterState 含义的说明性描述，未规定任何变量或动作，不足以据此要求存在对应的 V 或 A 元素。⭐ 与第 3 句同：本句是否被满足须自行到 §1.3 核对，⛔ 本提示不代为回答。
- `NL-L005`：约束元素：迁移。要求存在一条进入 MethaneState 的迁移；「Similarly」把本句与第 4 句置于同等地位，未引入新的条件或顺序约束。歧义与第 4 句相同：源状态未指明、条件未给出、「controlling or monitoring the methane flow」只是含义说明而非对变量或动作的规定。⭐ 与第 3、4 句同：本句是否被满足须自行到 §1.3 核对，⛔ 本提示不代为回答。

## §4 整份 NL 层面的观察（术语表 · 跨句反复出现的歧义 · 原文质量问题）

【术语表（全份一致）】substate → substate（子状态），英文单复数形式随原文（第 1、2 句为 substates，第 3、4、5 句为 substate）；state → 状态；transition to / transitions to → 迁移到；the pump → 泵；water flow → 水流；methane flow → 甲烷流。按 SPEC §4，substate 属于须保留英文并加中文括注的建模术语；state 与 transition 不在该清单内，故译为中文，但全份用词固定不变。

【原样保留的标识符】本份 NL 中出现且一律未翻译、未加引号、未改大小写的有 4 个：PumpControl、PumpState、WaterState、MethaneState。其中 PumpControl（复合状态）与 PumpState（其下的一个子状态）形近但是两个不同对象，全份译文未发生互换，判读时须严格区分。⛔ 本份 NL 只点了这 4 个标识符，此外**没有**给出任何事件名、变量名或其他状态名；凡不在此列的元素都不受本份 NL 任何一句约束。

【反复出现的歧义】①「何时切换」始终没说清：第 1 句只给出「based on specific conditions」这一空壳，第 3、4、5 句分别用 first / can also / Similarly 引入三个 substate，但三句都没有给出触发事件、守卫条件或源状态。因此 NL 既可读作「三者择一进入，条件待定」，也可读作「三者依次进入，PumpState 居首」。这份含糊已按 SPEC §2 原样保留，未在译文中替它消歧；判缺陷时不能任选一种读法后再宣称「违反」。②「main substates」的 main 未定义，⛔ 它直接决定 PumpControl 之下若出现第四个直接子状态算不算多余。

【建模对象边界提示（M = (S, E, V, Tr, A)，无时钟、无并发）】整份 NL 不含任何时间/时钟约束，也不含任何并发主张——first / also / similarly 是择一或顺序的措辞，不是 concurrent activation。⚠️ 因此若把 PumpState、WaterState、MethaneState 表达成三个 orthogonal region（正交区），其并发语义落在本项目边界之外，既不得记为「方法未检出的缺陷」，也不得反过来声称此处没有并发问题。⭐ 边界内可判读的是：本份 NL 主张了三条「进入 substate 的迁移」（第 3、4、5 句各一条），⛔ 它们是否存在须自行到 §1.3 核对。

【原文质量】未发现语法、拼写或数格错误，故本份 〔原文如此〕 标注为 0 处；未按 SPEC §5 无中生有地制造标注。格式上第 1 至 4 行行尾各有一个多余空格、第 5 行没有，此不一致已在 en 与 zh 中原样保留。句子编号 1. 至 5. 与原文逐字照抄。中文标点按中文体系处理（冒号「：」、顿号「、」、句号「。」），未逐字照搬英文半角标点，此为 SPEC §6「标点照抄」在跨语言时的唯一让步，特此声明。

## §5 NL 原始字节（带物理行号）

```text
  1 | 1. The system begins in the PumpControl state, from which it can transition to different substates based on specific conditions. 
  2 | 2. Within the PumpControl state, there are three main substates: PumpState, WaterState, and MethaneState. 
  3 | 3. The system first transitions to the PumpState substate, where the pump is activated or controlled. 
  4 | 4. The system can also transition to the WaterState substate, indicating that the pump is controlling or monitoring the water flow. 
  5 | 5. Similarly, the system can transition to the MethaneState substate, indicating that the pump is controlling or monitoring the methane flow.
```
