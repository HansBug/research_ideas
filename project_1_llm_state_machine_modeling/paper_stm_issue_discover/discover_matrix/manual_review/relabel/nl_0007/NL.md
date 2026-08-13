<!-- RELABEL schema=paper1.relabel.nldoc.v1 nl_dir=nl_0007 -->
# NL 规约材料 · `nl_0007`

本文件由 [generate.py](../generate.py) 生成，**没有任何填写区** —— 它是只读材料。判读要填的东西全在同目录的 `<pair>.md` 里。

本页服务同目录的 **6** 份工作单：[`0007`](./0007.md)、[`0017`](./0017.md)、[`0027`](./0027.md)、[`0037`](./0037.md)、[`0047`](./0047.md)、[`0057`](./0057.md)。它们由**同一份 NL 规约**（sha8 `49854d04`）生成 6 个不同制品，所以 NL 侧材料只有一份，制品侧各不相同。

分段口径 `line_split`（按物理行切）：按物理行切分，与 pipeline 同口径，共 **3** 段（`NL-L001` … `NL-L003`）。台账里的「NL 第 N 句」与你要在工作单 §5 填的 `nl_evidence` 都按这套段 id 读。

## §1 译文纪律（先读这三段再看表）

**译文是给人判缺陷用的，不是给人读着舒服用的。** 它严格直译，不意译、不润色、不补原文没有的信息（含不补主语、不补量词、不补逻辑连接词）；状态名 / 事件名 / 变量名 / 守卫表达式一律**保留英文原样**，建模术语保留英文并在紧跟的括号里给中文。⚠️ 原文含糊的地方译文**照样含糊** —— 替它消歧就等于替你做了本轮要你自己做的判断。⚠️ 译文是**辅助**，判据仍以英文原文为准；两者不一致时以原文为准并请回报。

两种方括号标注的含义：`〔原文如此：…〕` 指**原文自身**有语法 / 拼写 / 数格错误，译文照直译并说明错在哪 —— 它不是译文的错，也不构成模型的缺陷；`〔译者存疑：…〕` 指**原文这里没说清**（谁是主语、并列项是「且」还是「或」、源状态是哪个），它直接决定判缺陷时这一句**能不能**用来说模型「违反」了什么。

口径与验收依据：[translations/TRANSLATION_SPEC.md](../translations/TRANSLATION_SPEC.md)；本份译文的原始 JSON：[translations/nl_0007.json](../translations/nl_0007.json)；装载与对拍：[nl_zh.py](../nl_zh.py)。

## §2 逐段：原文与中文严格翻译

| 段 id | 原文 | 中文严格翻译 |
| :-- | :-- | :-- |
| `NL-L001` | 1. There are three region in this diagram | 1. 本图中有三个 region（区）〔原文如此：region 未用复数，未写作 regions；句末缺句号〕 |
| `NL-L002` | 2. This sub-machine becomes active when a possible frontend collision, rear-end collision or collision with pedestrian is detected. | 2. 本 sub-machine（子机）在检测到一次可能的 frontend collision（前端碰撞）、rear-end collision（追尾碰撞）或 collision with pedestrian（与行人的碰撞）时变为 active（活动）。〔译者存疑：frontend 与并列的 rear-end 构词不对称，疑为 front-end 之误；此处照直译为「前端」，未按「前向／正面」消歧〕 |
| `NL-L003` | 3. The orthogonal regions of the active mode of collision avoidance allow for concurrent activation different of collision avoidance controls. | 3. collision avoidance（碰撞避免）的 active mode（活动模式）的 orthogonal regions（正交区）允许 concurrent activation（并发激活）different of（不同 的）collision avoidance controls（碰撞避免控制）。〔原文如此：`concurrent activation different of collision avoidance controls` 语序错乱，`different` 位置不当；译文按原语序直译，未作改正〕 |

## §3 逐段判读提示（该段约束了哪个元素 · 歧义点 · 边界外部分）

提示只陈述「原文这一句说了什么、没说什么」，不含任何裁决 —— 「所以模型应该怎样」是本轮要你自己填的，材料不替你填。

**提示里也不含任何关于被测制品的断言** —— 一份 NL 服务 6 个 pair，这一页是 6 份工作单共用的，讲制品的话必然对其中 5 份为假。因此「这个状态在不在」「这条边有没有」一律请自己到各份工作单的 §1.2（作者源，带行号）与 §4（按该 pair 现算的清单）核对，不要指望提示替你回答。2026-08-13 之前的旧版工作单**违反过这一条**，若你读过旧版，见 [README.md](../README.md) §十。

- `NL-L001`：约束元素：层次结构（region 的数量）。歧义①：`three region` 所指不明——既可读作 collision avoidance 这一 mode 内部的三个 orthogonal region，也可读作整张图顶层的三个 composite state；两种读法会导出完全不同的「区数量是否为三」的判定，判缺陷时不得单方面挑一种。歧义②：`this diagram` 指整张图还是本 sub-machine 所在的那一层，未指明。⛔ 边界外：若 `region` 按 UML 的 orthogonal region 理解，其并发语义落在本项目建模对象 M = (S, E, V, Tr, A) 之外，不得据本句把「未表达并发」判为方法应检出的缺陷，也不得反过来声称此处无并发问题。
- `NL-L002`：约束元素：一条进入本 sub-machine 的迁移及其触发事件（激活条件 = 检测到三类可能碰撞之一），并隐含三类碰撞检测事件的存在（frontend / rear-end / pedestrian）。歧义①：`This sub-machine` 指哪一个未指明——可指整张 collision-avoidance 子机图，也可指 collision avoidance 这一个状态。歧义②：`becomes active` 未说明激活后进入哪个 initial / 子状态，也未说明是否有 initial pseudostate（伪状态）。歧义③：三类碰撞是各自触发一条独立迁移，还是共同触发同一次激活（`or` 未澄清），未指明。歧义④：`a possible ... is detected` 只说「被检测到」，未说明检测由谁完成、是否为一个显式 event（事件）。
- `NL-L003`：约束元素：collision avoidance 这一 mode 内部的层次结构——它含有复数个 orthogonal region（正交区），并允许不同的 collision avoidance control 并发激活；⛔ 原文未说明区与 control 是否一一对应。歧义①：`the active mode of collision avoidance` 未说明是一个具体状态名还是描述性说法。歧义②：本句只说 regions 为复数，未给数量，与第 1 句的 `three` 是否同指不明。歧义③：语序错乱使 `different` 的辖域不定（不同的 activation？不同的 controls？）——见译文中的〔原文如此〕。⛔ 边界外：`orthogonal regions` 的并发语义与 `concurrent activation`（并发激活）整体落在本项目建模对象 M = (S, E, V, Tr, A) 之外（无时钟、无并发）。本句所要求的「多个 control 同时处于活动」无法在 M 中表达，因此不得把「未实现并发激活」记为方法未检出的缺陷。

## §4 整份 NL 层面的观察（术语表 · 跨句反复出现的歧义 · 原文质量问题）

【术语表（全份一致）】orthogonal region → orthogonal region（正交区）；sub-machine → sub-machine（子机）；active → active（活动）；concurrent activation → concurrent activation（并发激活）。状态／事件名一律不出现在本份 NL 中（NL 通篇为散文，未点名任何标识符），故第 2 句的 frontend / rear-end / pedestrian 三词按普通名词处理，保留英文并加中文，⛔ 不视为对任何具名碰撞状态的直接点名。

【反复出现的歧义】(a) 指代不明贯穿全份：第 1 句 `this diagram`、第 2 句 `This sub-machine`、第 3 句 `the active mode of collision avoidance` 三处都没有绑定到任何具名元素，使得「本 NL 到底在描述哪一层」始终不确定。(b) region 的数量口径不一致：第 1 句给出 `three`，第 3 句只说复数 `regions`，两者是否同指未说明。

【原文质量问题】(1) 第 1 句 `three region` 数格错误（应为 regions），且句末缺句号；(2) 第 1、2 句行尾各多出一个空格；(3) 第 3 句 `concurrent activation different of collision avoidance controls` 语序错乱，`different` 位置不当，疑本意为 `concurrent activation of different collision avoidance controls`（即：并发激活不同的碰撞避免控制）——但译文未替其改正；(4) 第 2 句 `frontend` 与并列的 `rear-end` 构词不对称，疑为 `front-end`；(5) 全份仅 46 词、三句，信息密度极低：只给了「有三个 region」「何时激活」「区内可并发」三条，对状态集、事件集、变量、迁移守卫、退出条件均无任何约束——判缺陷时大量元素属于「NL 未规定」，不能记为违反。

【⛔ 建模边界总提示】本份 NL 三句中有两句（第 1 句与第 3 句）整体或部分落在 M = (S, E, V, Tr, A) 之外：第 1 句的 region 计数若按 orthogonal region 读则涉及并发结构；第 3 句的 concurrent activation 明确要求并发语义。本项目不建模并发与时钟，这两处既不得记为「方法未检出」，也不得据此声称此处无并发缺陷。

## §5 NL 原始字节（带物理行号）

```text
  1 | 1. There are three region in this diagram 
  2 | 2. This sub-machine becomes active when a possible frontend collision, rear-end collision or collision with pedestrian is detected. 
  3 | 3. The orthogonal regions of the active mode of collision avoidance allow for concurrent activation different of collision avoidance controls.
```
