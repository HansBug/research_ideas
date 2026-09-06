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
| `NL-L001` | 1. There are three region in this diagram | 1. 本图中有三个区（region）〔原文如此：region 未用复数；句末缺句号〕 |
| `NL-L002` | 2. This sub-machine becomes active when a possible frontend collision, rear-end collision or collision with pedestrian is detected. | 2. 此子机（sub-machine）在检测到可能的正面碰撞（frontend collision）、追尾碰撞（rear-end collision）或与行人的碰撞（collision with pedestrian）时变为活跃。〔原文如此：pedestrian 为单数可数名词，前缺冠词，应为 a pedestrian 或 pedestrians〕〔译者存疑：frontend 与并列的 rear-end 构词不对称，疑为 front-end 之误；译文按「正面碰撞」理解〕 |
| `NL-L003` | 3. The orthogonal regions of the active mode of collision avoidance allow for concurrent activation different of collision avoidance controls. | 3. 碰撞避免（collision avoidance）的活跃模式（active mode）的正交区（orthogonal regions）允许并发激活不同的碰撞避免控制。〔原文如此：different 与 of 词序颠倒，应为 activation of different；译文按更正后的语序（activation of different）译出，未在中文里保留原文的错乱语序〕 |

## §3 逐段判读提示（该段约束了哪个元素 · 歧义点 · 边界外部分）

提示只陈述「原文这一句说了什么、没说什么」，不含任何裁决 —— 「所以模型应该怎样」是本轮要你自己填的，材料不替你填。

**提示里也不含任何关于被测制品的断言** —— 一份 NL 服务 6 个 pair，这一页是 6 份工作单共用的，讲制品的话必然对其中 5 份为假。因此「这个状态在不在」「这条边有没有」一律请自己到各份工作单的 §1.2（作者源，带行号）与 §4（按该 pair 现算的清单）核对，不要指望提示替你回答。2026-08-13 之前的旧版工作单**违反过这一条**，若你读过旧版，见 [README.md](../README.md) §十。

- `NL-L001`：该句对图的层次提出要求：本图共有三个区；未说明各区的划分方式或内容，也未说明这三个区与第 2 句的子机有何关系。原文 region 未用复数。
- `NL-L002`：该句对迁移触发条件提出要求：当检测到可能的正面碰撞、追尾碰撞或与行人的碰撞时，子机变为活跃；三类碰撞的检测是并列的或关系。歧义：possible 在语法上只修饰 frontend collision，是否同样修饰后两类碰撞，原文未明示。原文未说明子机初始是否活跃，也未说明何时退出活跃。
- `NL-L003`：该句对层次与模式提出要求：碰撞避免的活跃模式包含正交区，正交区允许并发激活不同的碰撞避免控制。并发激活与正交区的并发语义均不在本项目建模对象（状态/事件/变量/迁移/动作）之内。原文未点名这些控制具体指什么、共有几种；原文 different 与 of 词序颠倒。

## §4 整份 NL 层面的观察（术语表 · 跨句反复出现的歧义 · 原文质量问题）

对象名对照表（英→中）：region→区；orthogonal region→正交区；sub-machine→子机；active mode→活跃模式；frontend collision→正面碰撞；rear-end collision→追尾碰撞；collision with pedestrian→与行人的碰撞；collision avoidance→碰撞避免；concurrent activation→并发激活。术语说明：orthogonal region 与 concurrent activation 为建模术语，其并发语义不在本项目建模对象之内。原文质量问题：第 1 句 region 未用复数；第 2 句 pedestrian 前缺冠词；第 3 句 different 与 of 词序颠倒（应为 activation of different）。歧义：第 2 句 possible 在语法上只修饰 frontend collision，是否修饰后两类碰撞未明示。全篇无形式表达式（无守卫、无赋值、无带单位的量）。格式：第 1、2 句行尾各多出一个空格（第 3 句无），⚠️ 尾随空格是全语料通例，非本份独有，故不在单句上标注。

## §5 NL 原始字节（带物理行号）

```text
  1 | 1. There are three region in this diagram 
  2 | 2. This sub-machine becomes active when a possible frontend collision, rear-end collision or collision with pedestrian is detected. 
  3 | 3. The orthogonal regions of the active mode of collision avoidance allow for concurrent activation different of collision avoidance controls.
```
