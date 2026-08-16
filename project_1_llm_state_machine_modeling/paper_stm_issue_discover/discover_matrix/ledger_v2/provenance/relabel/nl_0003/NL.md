<!-- RELABEL schema=paper1.relabel.nldoc.v1 nl_dir=nl_0003 -->
# NL 规约材料 · `nl_0003`

本文件由 [generate.py](../generate.py) 生成，**没有任何填写区** —— 它是只读材料。判读要填的东西全在同目录的 `<pair>.md` 里。

本页服务同目录的 **6** 份工作单：[`0003`](./0003.md)、[`0012`](./0012.md)、[`0022`](./0022.md)、[`0032`](./0032.md)、[`0042`](./0042.md)、[`0052`](./0052.md)。它们由**同一份 NL 规约**（sha8 `9fe426ba`）生成 6 个不同制品，所以 NL 侧材料只有一份，制品侧各不相同。

分段口径 `line_split`（按物理行切）：按物理行切分，与 pipeline 同口径，共 **3** 段（`NL-L001` … `NL-L003`）。台账里的「NL 第 N 句」与你要在工作单 §5 填的 `nl_evidence` 都按这套段 id 读。

## §1 译文纪律（先读这三段再看表）

**译文是给人判缺陷用的，不是给人读着舒服用的。** 它严格直译，不意译、不润色、不补原文没有的信息（含不补主语、不补量词、不补逻辑连接词）；状态名 / 事件名 / 变量名 / 守卫表达式一律**保留英文原样**，建模术语保留英文并在紧跟的括号里给中文。⚠️ 原文含糊的地方译文**照样含糊** —— 替它消歧就等于替你做了本轮要你自己做的判断。⚠️ 译文是**辅助**，判据仍以英文原文为准；两者不一致时以原文为准并请回报。

两种方括号标注的含义：`〔原文如此：…〕` 指**原文自身**有语法 / 拼写 / 数格错误，译文照直译并说明错在哪 —— 它不是译文的错，也不构成模型的缺陷；`〔译者存疑：…〕` 指**原文这里没说清**（谁是主语、并列项是「且」还是「或」、源状态是哪个），它直接决定判缺陷时这一句**能不能**用来说模型「违反」了什么。

口径与验收依据：[translations/TRANSLATION_SPEC.md](../translations/TRANSLATION_SPEC.md)；本份译文的原始 JSON：[translations/nl_0003.json](../translations/nl_0003.json)；装载与对拍：[nl_zh.py](../nl_zh.py)。

## §2 逐段：原文与中文严格翻译

| 段 id | 原文 | 中文严格翻译 |
| :-- | :-- | :-- |
| `NL-L001` | 1. Once the device is powered on, the system enters the `Operate` state, and based on user actions, it transitions between `Idle`, `Accelerating or Cruising`, and `Braking` states. | 1. 一旦设备被上电，系统进入 `Operate` 状态（运行态），并基于用户动作，它在 `Idle`（空闲态）、`Accelerating or Cruising`（加速或巡航态）和 `Braking`（制动态）状态之间迁移。 |
| `NL-L002` | 2. The system can be turned on with the `start` signal and turned off with the `keyOff` signal. | 2. 系统可以通过 `start`（启动）信号开启，并通过 `keyOff`（钥匙关闭）信号关闭。 |
| `NL-L003` | 3. Within the `Operate` state, the system transitions between different substates depending on actions like accelerating, braking, or stopping. | 3. 在 `Operate` 状态内，系统在不同的子状态（substates）之间迁移，取决于诸如加速（accelerating）、制动（braking）或停止（stopping）的动作。〔译者存疑：原文中 accelerating、braking、stopping 三词未加反引号、未大写，其是否为具名事件无法由原文判定；本译文按普通动作名词译出，不指认任何具名事件，若判读者视其为事件名，须自行到 §1.3 逐行核对〕 |

## §3 逐段判读提示（该段约束了哪个元素 · 歧义点 · 边界外部分）

提示只陈述「原文这一句说了什么、没说什么」，不含任何裁决 —— 「所以模型应该怎样」是本轮要你自己填的，材料不替你填。

**提示里也不含任何关于被测制品的断言** —— 一份 NL 服务 6 个 pair，这一页是 6 份工作单共用的，讲制品的话必然对其中 5 份为假。因此「这个状态在不在」「这条边有没有」一律请自己到各份工作单的 §1.2（作者源，带行号）与 §4（按该 pair 现算的清单）核对，不要指望提示替你回答。2026-08-13 之前的旧版工作单**违反过这一条**，若你读过旧版，见 [README.md](../README.md) §十。

- `NL-L001`：该句要求了状态与迁移：设备上电后，系统进入 `Operate` 状态；根据用户动作，系统在 `Idle`、`Accelerating or Cruising`、`Braking` 状态之间迁移。原文未给出触发各迁移的具体用户动作，也未说明这三个状态与 `Operate` 状态的关系（本句未写明它们是否为 `Operate` 的子状态）。歧义点：`Once` 可理解为「每次上电后」或「首次上电后」；「用户动作」未指明具体动作。
- `NL-L002`：该句要求了两个信号（事件）：`start` 信号开启系统，`keyOff` 信号关闭系统。原文未说明开启、关闭分别对应系统处于哪个状态，也未说明关闭后系统进入哪个状态；未说明 `start` 信号与第 1 句的「上电」之间的关系。
- `NL-L003`：该句要求了子状态、迁移与事件：在 `Operate` 状态内，系统根据加速、制动、停止等动作，在不同的子状态之间迁移。原文未给出各子状态的名字，也未说明它们与第 1 句的 `Idle`、`Accelerating or Cruising`、`Braking` 是否对应；未给出哪个动作触发哪条迁移。

## §4 整份 NL 层面的观察（术语表 · 跨句反复出现的歧义 · 原文质量问题）

对象名对照表（英文原文 → 本份选定中文译名）：`Operate` → 运行态；`Idle` → 空闲态；`Accelerating or Cruising` → 加速或巡航态；`Braking` → 制动态；`start` → 启动；`keyOff` → 钥匙关闭；substates → 子状态；accelerating → 加速；braking → 制动；stopping → 停止。注意：第 3 句的 accelerating、braking、stopping 是动作名（小写、无反引号），与第 1 句的状态名 `Accelerating or Cruising`、`Braking`（带反引号）所指不同。正文约定：带反引号的标识符整串照抄，首次出现时其后括号内给中文译名；无反引号的对象名首次出现写作「中文（英文）」。术语：transition(s) → 迁移；state → 状态；signal → 信号；action(s) → 动作；device → 设备。反复出现的欠指定：第 1 句与第 3 句均未给出动作与迁移的一一对应；第 2 句未说明开启、关闭分别对应系统处于哪个状态，也未说明关闭后系统进入哪个状态；第 2 句未说明 `start` 信号与第 1 句「上电」的关系。原文质量问题：全篇未见语法或拼写错误；第 2 句的 `turned off` 前承前省略了 `can be`（正常省略，非错误）。

## §5 NL 原始字节（带物理行号）

```text
  1 | 1. Once the device is powered on, the system enters the `Operate` state, and based on user actions, it transitions between `Idle`, `Accelerating or Cruising`, and `Braking` states. 
  2 | 2. The system can be turned on with the `start` signal and turned off with the `keyOff` signal. 
  3 | 3. Within the `Operate` state, the system transitions between different substates depending on actions like accelerating, braking, or stopping.
```
