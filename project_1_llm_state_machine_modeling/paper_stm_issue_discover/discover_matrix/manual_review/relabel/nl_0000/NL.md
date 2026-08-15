<!-- RELABEL schema=paper1.relabel.nldoc.v1 nl_dir=nl_0000 -->
# NL 规约材料 · `nl_0000`

本文件由 [generate.py](../generate.py) 生成，**没有任何填写区** —— 它是只读材料。判读要填的东西全在同目录的 `<pair>.md` 里。

本页服务同目录的 **6** 份工作单：[`0000`](./0000.md)、[`0010`](./0010.md)、[`0020`](./0020.md)、[`0030`](./0030.md)、[`0040`](./0040.md)、[`0050`](./0050.md)。它们由**同一份 NL 规约**（sha8 `f1c3dc88`）生成 6 个不同制品，所以 NL 侧材料只有一份，制品侧各不相同。

分段口径 `manual_override`（人工标注分段）：该份规约的编号无法机器判定，分段取自 [corpora/nl_segmentation/overrides.json](../../../../corpora/nl_segmentation/overrides.json) 的人工标注，共 **6** 段（`NL-M001` … `NL-M006`）。台账里的「NL 第 N 句」与你要在工作单 §5 填的 `nl_evidence` 都按这套段 id 读。

## §1 译文纪律（先读这三段再看表）

**译文是给人判缺陷用的，不是给人读着舒服用的。** 它严格直译，不意译、不润色、不补原文没有的信息（含不补主语、不补量词、不补逻辑连接词）；状态名 / 事件名 / 变量名 / 守卫表达式一律**保留英文原样**，建模术语保留英文并在紧跟的括号里给中文。⚠️ 原文含糊的地方译文**照样含糊** —— 替它消歧就等于替你做了本轮要你自己做的判断。⚠️ 译文是**辅助**，判据仍以英文原文为准；两者不一致时以原文为准并请回报。

两种方括号标注的含义：`〔原文如此：…〕` 指**原文自身**有语法 / 拼写 / 数格错误，译文照直译并说明错在哪 —— 它不是译文的错，也不构成模型的缺陷；`〔译者存疑：…〕` 指**原文这里没说清**（谁是主语、并列项是「且」还是「或」、源状态是哪个），它直接决定判缺陷时这一句**能不能**用来说模型「违反」了什么。

口径与验收依据：[translations/TRANSLATION_SPEC.md](../translations/TRANSLATION_SPEC.md)；本份译文的原始 JSON：[translations/nl_0000.json](../translations/nl_0000.json)；装载与对拍：[nl_zh.py](../nl_zh.py)。

## §2 逐段：原文与中文严格翻译

| 段 id | 原文 | 中文严格翻译 |
| :-- | :-- | :-- |
| `NL-M001` | 1 The human driving mode is represented by a simple state. | 1 人工驾驶模式（human driving mode）由一个简单状态（simple state）表示。 |
| `NL-M002` | 2 The autonomous mode has sub-states and is represented by a sub machine state. | 2 自动驾驶模式（autonomous mode）有子状态（sub-states）并由一个子机状态（sub machine state）表示。 |
| `NL-M003` | 3. when power on, the system turn into human driving mode | 3. 当上电时，系统转入人工驾驶模式〔原文如此：when power on 缺谓语（应为 when power is on）；turn 与主语 the system 主谓不一致（应为 turns）；句末无句号〕 |
| `NL-M004` | 4when front_distance > 10, auto transport to autonomous state | 4当 front_distance > 10 时，自动转运到自动驾驶态（autonomous state）〔原文如此：编号 4 与后接的 when 之间无空格；transport 疑为 transit / transition 之误；本段编号 4 与下一段编号 4 重复；句末无句号〕〔译者存疑：auto 既可读作副词 automatically 的缩写，也可读作 autonomous 的缩写而与其后的 autonomous state 重复指涉，原文无法判定〕 |
| `NL-M005` | 4. transit to human driving mode when receive human steering cmd, brake pressed, in (auto final) | 4. 转入人工驾驶模式，当接收到人工转向指令（human steering cmd），制动被踩下，处于 (auto final) 时〔原文如此：when receive 缺主语（应为 when receiving）；brake pressed 缺谓语（应为 when brake is pressed）；本段编号 4 与上一段编号 4 重复，作者编号序列为 1,2,3,4,4,5，缺 6；句末无句号〕〔译者存疑：auto final 含义不明，或指自动驾驶的某个最终阶段或状态〕〔译者存疑：human steering cmd, brake pressed, in (auto final) 三项之间无任何连接词，无法判定是合取（and）、析取（or）还是顺序发生的并列列举〕 |
| `NL-M006` | 5 when power off, it will transit to final state | 5 当断电时，它将转入终态（final state）〔原文如此：when power off 缺谓语（应为 when power is off）；句末无句号，全份规格到此结束〕〔译者存疑：it 指代不明，可能指 the system，也可能指当时所处的状态，原文未说明〕 |

## §3 逐段判读提示（该段约束了哪个元素 · 歧义点 · 边界外部分）

提示只陈述「原文这一句说了什么、没说什么」，不含任何裁决 —— 「所以模型应该怎样」是本轮要你自己填的，材料不替你填。

**提示里也不含任何关于被测制品的断言** —— 一份 NL 服务 6 个 pair，这一页是 6 份工作单共用的，讲制品的话必然对其中 5 份为假。因此「这个状态在不在」「这条边有没有」一律请自己到各份工作单的 §1.2（作者源，带行号）与 §4（按该 pair 现算的清单）核对，不要指望提示替你回答。2026-08-13 之前的旧版工作单**违反过这一条**，若你读过旧版，见 [README.md](../README.md) §十。

- `NL-M001`：该句对状态提出要求：人工驾驶模式须由一个简单状态表示。原文未说明该简单状态与其他状态的关系。
- `NL-M002`：该句对状态与层次提出要求：自动驾驶模式须有子状态，且须由一个子机状态表示。歧义：原文未说明子状态的数量与名称，也未说明子机状态与这些子状态之间的关系。
- `NL-M003`：该句对迁移提出要求：上电时系统转入人工驾驶模式。歧义：原文未说明是首次上电还是任意时刻上电，也未说明该迁移的来源状态。
- `NL-M004`：该句对迁移提出要求：转入自动驾驶态的迁移，其触发条件为 front_distance > 10。歧义：该句为省略句，未写明迁移的主体与来源状态；front_distance 的含义与单位原文未定义；autonomous state 与 autonomous mode 用词不同，原文未说明二者是否指同一对象。
- `NL-M005`：该句对迁移与事件提出要求：一条转入人工驾驶模式的迁移；原文列举其触发条件为接收到 human steering cmd、制动被踩下、处于 (auto final)。歧义：三个条件之间是与还是或的关系原文未说明；auto final 含义不明；主句无主语，为省略句。
- `NL-M006`：该句对迁移提出要求：断电时转入终态。歧义：原文用 it 指代而未点名；该迁移的来源状态未说明。

## §4 整份 NL 层面的观察（术语表 · 跨句反复出现的歧义 · 原文质量问题）

对象名对照表（英文原文 → 中文译名）：human driving mode → 人工驾驶模式；simple state → 简单状态；autonomous mode → 自动驾驶模式；sub-states → 子状态；sub machine state → 子机状态；autonomous state → 自动驾驶态；human steering cmd → 人工转向指令；final state → 终态；auto final → 含义不明，保留英文未译。术语：cmd 为 command 的缩写；power on / power off 译作上电 / 断电；brake 译作制动。反复出现的歧义：autonomous mode 与 autonomous state 原文用词不同，译文分别译作自动驾驶模式与自动驾驶态，未替原文合并，原文未说明二者是否为同一对象；front_distance 的含义与单位原文未定义。原文质量问题：句子编号不一致——4 出现两次；句点样式不一（1、2、5 无句点，3 与第二个 4 有句点，第一个 4 与 when 连写无空格）；多处语法错误已在各句译文末尾标注；(auto final) 含义不明。

## §5 NL 原始字节（带物理行号）

```text
  1 | 1 The human driving mode is represented by a simple state. 2 The autonomous mode has sub-states and is represented by a sub machine state. 3. when power on, the system turn into human driving mode 4when front_distance > 10, auto transport to autonomous state 4. transit to human driving mode when receive human steering cmd, brake pressed, in (auto final) 5 when power off, it will transit to final state
```
