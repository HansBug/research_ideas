<!-- RELABEL schema=paper1.relabel.nldoc.v1 nl_dir=nl_0001 -->
# NL 规约材料 · `nl_0001`

本文件由 [generate.py](../generate.py) 生成，**没有任何填写区** —— 它是只读材料。判读要填的东西全在同目录的 `<pair>.md` 里。

本页服务同目录的 **6** 份工作单：[`0001`](./0001.md)、[`0011`](./0011.md)、[`0021`](./0021.md)、[`0031`](./0031.md)、[`0041`](./0041.md)、[`0051`](./0051.md)。它们由**同一份 NL 规约**（sha8 `abb20a21`）生成 6 个不同制品，所以 NL 侧材料只有一份，制品侧各不相同。

分段口径 `line_split`（按物理行切）：按物理行切分，与 pipeline 同口径，共 **3** 段（`NL-L001` … `NL-L003`）。台账里的「NL 第 N 句」与你要在工作单 §5 填的 `nl_evidence` 都按这套段 id 读。

## §1 译文纪律（先读这三段再看表）

**译文是给人判缺陷用的，不是给人读着舒服用的。** 它严格直译，不意译、不润色、不补原文没有的信息（含不补主语、不补量词、不补逻辑连接词）；状态名 / 事件名 / 变量名 / 守卫表达式一律**保留英文原样**，建模术语保留英文并在紧跟的括号里给中文。⚠️ 原文含糊的地方译文**照样含糊** —— 替它消歧就等于替你做了本轮要你自己做的判断。⚠️ 译文是**辅助**，判据仍以英文原文为准；两者不一致时以原文为准并请回报。

两种方括号标注的含义：`〔原文如此：…〕` 指**原文自身**有语法 / 拼写 / 数格错误，译文照直译并说明错在哪 —— 它不是译文的错，也不构成模型的缺陷；`〔译者存疑：…〕` 指**原文这里没说清**（谁是主语、并列项是「且」还是「或」、源状态是哪个），它直接决定判缺陷时这一句**能不能**用来说模型「违反」了什么。

口径与验收依据：[translations/TRANSLATION_SPEC.md](../translations/TRANSLATION_SPEC.md)；本份译文的原始 JSON：[translations/nl_0001.json](../translations/nl_0001.json)；装载与对拍：[nl_zh.py](../nl_zh.py)。

## §2 逐段：原文与中文严格翻译

| 段 id | 原文 | 中文严格翻译 |
| :-- | :-- | :-- |
| `NL-L001` | 1 This state machine model represents the train's basic braking device, which serves as the final execution unit for train braking operations. | 1 本状态机模型表示列车的基础制动装置（basic braking device），其作为列车制动操作的最终执行单元。 |
| `NL-L002` | 2 When the basic braking device receives a brake signal, it transitions from the initial state to the braking state. If the signal transmission fails, it proceeds to the operational state. Once the signal feedback is sent, it returns to the initial state. | 2 当基础制动装置接收到制动信号（brake signal）时，它从初始状态（initial state）迁移到制动状态（braking state）。如果信号传输失败，它进入运行状态（operational state）。一旦信号反馈（signal feedback）被发出，它返回到初始状态。〔译者存疑：原文未对 operational 一词加以界定，此处按字面直译为「运行」；其究竟指「正常运行」、「可操作」还是某种降级运行，原文无法判定。〕〔译者存疑：原文此处用 proceeds to，与前一分句的 transitions to、后一分句的 returns to 用词不同；原文未说明三者是否同指一种 transition（迁移），无法判定，故一律按字面直译、不作统一。〕 |
| `NL-L003` | 3 After entering the braking state, the system transitions to the brake caliper clamping state. | 3 在进入制动状态后，系统迁移到制动钳夹紧状态（brake caliper clamping state）。 |

## §3 逐段判读提示（该段约束了哪个元素 · 歧义点 · 边界外部分）

提示只陈述「原文这一句说了什么、没说什么」，不含任何裁决 —— 「所以模型应该怎样」是本轮要你自己填的，材料不替你填。

**提示里也不含任何关于被测制品的断言** —— 一份 NL 服务 6 个 pair，这一页是 6 份工作单共用的，讲制品的话必然对其中 5 份为假。因此「这个状态在不在」「这条边有没有」一律请自己到各份工作单的 §1.2（作者源，带行号）与 §4（按该 pair 现算的清单）核对，不要指望提示替你回答。2026-08-13 之前的旧版工作单**违反过这一条**，若你读过旧版，见 [README.md](../README.md) §十。

- `NL-L001`：该句为描述性语句：点名 basic braking device（列车的基础制动装置）为其描述对象，并说明其职能是作为列车制动操作的最终执行单元；未对状态、迁移、事件、变量或初始点提出具体要求。
- `NL-L002`：该句对三个状态（initial state、braking state、operational state）与两个事件（收到 brake signal、发出 signal feedback）提出要求，并描述三条迁移：① 收到制动信号时从 initial state 迁到 braking state；② signal transmission 失败时进入 operational state；③ signal feedback 发出后返回 initial state。歧义点：① 「If the signal transmission fails」未明说 signal transmission 指哪个信号的传输（可读作 brake signal 的传输），它与「已收到 brake signal」如何并存原文未说明；② 后两条迁移的源状态均未指明：进入 operational state 的源状态、返回 initial state 的源状态都未说明（最自然的读法是从 operational state 返回）。
- `NL-L003`：该句要求状态 brake caliper clamping state 以及从 braking state 到该状态的迁移；原文未给该迁移的触发条件，只给了时机「进入制动状态后」。歧义点：主语由第 2 句的 it（指代 basic braking device）变为 the system，the system 是否仍指同一对象原文未说明。

## §4 整份 NL 层面的观察（术语表 · 跨句反复出现的歧义 · 原文质量问题）

对象名对照表（英文原文 → 本份选定的中文译名，全文一致）：

basic braking device → 基础制动装置

train → 列车

final execution unit → 最终执行单元

train braking operations → 列车制动操作

brake signal → 制动信号

initial state → 初始状态

braking state → 制动状态

signal transmission → 信号传输

operational state → 运行状态

signal feedback → 信号反馈

system → 系统

brake caliper clamping state → 制动钳夹紧状态

整份观察：

- 原文无语法、拼写或数格错误，未出现需加〔原文如此〕的情况。
- 反复出现的歧义：第 2 句三条迁移中，后两条的源状态未指明；「signal transmission」指哪个信号的传输未明说，且它与「已收到 brake signal」如何并存原文未说明。
- 原文质量：第 2 句用 it 指代 basic braking device，第 3 句改称 the system，二者是否同一对象原文未说明；第 3 句的迁移未给触发条件。
- initial state 仅作为具名状态充当迁移端点（第 2 句第 1 条迁移的源状态、第 3 条迁移的目标状态），原文未声明它在名称之外还有特殊地位。
- 全篇无形式表达式、无带单位数值、无显式时序或并发约束，无建模对象边界之外的内容。

## §5 NL 原始字节（带物理行号）

```text
  1 | 1 This state machine model represents the train's basic braking device, which serves as the final execution unit for train braking operations. 
  2 | 2 When the basic braking device receives a brake signal, it transitions from the initial state to the braking state. If the signal transmission fails, it proceeds to the operational state. Once the signal feedback is sent, it returns to the initial state. 
  3 | 3 After entering the braking state, the system transitions to the brake caliper clamping state.
```
