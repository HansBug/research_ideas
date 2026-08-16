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
| `NL-L001` | 1. The system begins in the PumpControl state, from which it can transition to different substates based on specific conditions. | 1. 系统起始于泵控制状态（PumpControl state），从该状态可以转入不同的子状态（substates），基于特定条件。 |
| `NL-L002` | 2. Within the PumpControl state, there are three main substates: PumpState, WaterState, and MethaneState. | 2. 在泵控制状态内部，有三个主要的子状态：泵状态（PumpState）、水状态（WaterState）和甲烷状态（MethaneState）。 |
| `NL-L003` | 3. The system first transitions to the PumpState substate, where the pump is activated or controlled. | 3. 系统首先转入泵状态子状态，在该子状态中泵被激活或被控制。 〔译者存疑：原文 "first" 兼有「顺序上的首先」与「时间上的首次」两解；本译文取「首先」，中文无法同时保留这两种读法〕 |
| `NL-L004` | 4. The system can also transition to the WaterState substate, indicating that the pump is controlling or monitoring the water flow. | 4. 系统也可以转入水状态子状态，表明泵正在控制或监测水流。 |
| `NL-L005` | 5. Similarly, the system can transition to the MethaneState substate, indicating that the pump is controlling or monitoring the methane flow. | 5. 类似地，系统可以转入甲烷状态子状态，表明泵正在控制或监测甲烷流。 |

## §3 逐段判读提示（该段约束了哪个元素 · 歧义点 · 边界外部分）

提示只陈述「原文这一句说了什么、没说什么」，不含任何裁决 —— 「所以模型应该怎样」是本轮要你自己填的，材料不替你填。

**提示里也不含任何关于被测制品的断言** —— 一份 NL 服务 6 个 pair，这一页是 6 份工作单共用的，讲制品的话必然对其中 5 份为假。因此「这个状态在不在」「这条边有没有」一律请自己到各份工作单的 §1.2（作者源，带行号）与 §4（按该 pair 现算的清单）核对，不要指望提示替你回答。2026-08-13 之前的旧版工作单**违反过这一条**，若你读过旧版，见 [README.md](../README.md) §十。

- `NL-L001`：该句要求：系统的起始状态为泵控制状态（初始点）；系统可以从泵控制状态转入不同的子状态（迁移）。原文仅说这些迁移基于特定条件（specific conditions），未给出任何具体条件，也未给出转入各子状态各自的触发条件。
- `NL-L002`：该句要求在泵控制状态之内存在三个主要的子状态（层次与状态），并给出其名称：泵状态、水状态、甲烷状态。原文以 "main" 修饰这三个子状态，未明言是否还存在其他非主要的子状态。
- `NL-L003`：该句要求一条迁移：系统首先转入泵状态子状态，并说明在该子状态中泵被激活或被控制。原文的 "first" 未说明参照对象（是初始子状态，还是相对其他子状态的时间次序）；"or" 未明言激活与控制是二选一还是择一皆可；该句未给该迁移的触发条件与迁出状态。
- `NL-L004`：该句要求一条迁移：系统也可以转入水状态子状态，并说明泵正在控制或监测水流。该句未给该迁移的触发条件与迁出状态；"or" 未明言控制与监测是二选一还是择一皆可。
- `NL-L005`：该句要求一条迁移：系统可以转入甲烷状态子状态，并说明泵正在控制或监测甲烷流。该句未给该迁移的触发条件与迁出状态；"Similarly" 表明与前句（水状态）的情形类似，原文未明言类似具体指哪些方面；"or" 未明言控制与监测是二选一还是择一皆可。

## §4 整份 NL 层面的观察（术语表 · 跨句反复出现的歧义 · 原文质量问题）

对象名对照表（英文原文 → 选定中文译名）：system → 系统；pump → 泵；PumpControl state → 泵控制状态；substates / substate → 子状态；PumpState → 泵状态；WaterState → 水状态；MethaneState → 甲烷状态；water flow → 水流；methane flow → 甲烷流。术语与用词：transition / transitions（本份中均作动词）→ 转入；begins in → 起始于；based on → 基于；activated → 激活；controlling / controlled → 控制；monitoring → 监测；indicating that → 表明；Similarly → 类似地；main → 主要的。反复出现的歧义：① 全篇没有给出任何一条迁移的具体触发条件：第 1 句仅笼统说基于特定条件（specific conditions），第 3、4、5 句的迁移均未给触发条件与迁出状态；② 第 3 句的 "first" 未说明参照对象；③ 第 3、4、5 句的 "or"（activated or controlled / controlling or monitoring）未明言是二选一还是择一皆可；④ 第 2 句用 "main" 修饰三个子状态，未明言是否还存在其他非主要的子状态；⑤ 第 4、5 句以 "also"、"Similarly" 承接前文，暗示这些迁移与前述内容存在关联，原文未明言其具体关系。原文质量观察：全篇共 5 句；无拼写与语法错误；除句首编号外无阿拉伯数字，无守卫、比较式、赋值或带单位的量，也未点名任何事件或变量；情态动词 can 共出现 3 次（第 1、4、5 句）；pump 出现 3 次；substate（含复数 substates）出现 5 次；PumpControl、PumpState、WaterState、MethaneState 各出现 2 次。

## §5 NL 原始字节（带物理行号）

```text
  1 | 1. The system begins in the PumpControl state, from which it can transition to different substates based on specific conditions. 
  2 | 2. Within the PumpControl state, there are three main substates: PumpState, WaterState, and MethaneState. 
  3 | 3. The system first transitions to the PumpState substate, where the pump is activated or controlled. 
  4 | 4. The system can also transition to the WaterState substate, indicating that the pump is controlling or monitoring the water flow. 
  5 | 5. Similarly, the system can transition to the MethaneState substate, indicating that the pump is controlling or monitoring the methane flow.
```
