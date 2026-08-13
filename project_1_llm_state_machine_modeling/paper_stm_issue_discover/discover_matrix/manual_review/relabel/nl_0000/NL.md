<!-- RELABEL schema=paper1.relabel.nldoc.v1 nl_dir=nl_0000 -->
# NL 规约材料 · `nl_0000`

⛔ 本文件由 [generate.py](../generate.py) 生成，**没有任何填写区** —— 它是只读材料。⭐ 判读要填的东西全在同目录的 `<pair>.md` 里。

⭐ 本页服务同目录的 **6** 份工作单：[`0000`](./0000.md)、[`0010`](./0010.md)、[`0020`](./0020.md)、[`0030`](./0030.md)、[`0040`](./0040.md)、[`0050`](./0050.md)。⭐ 它们由**同一份 NL 规约**（sha8 `f1c3dc88`）生成 6 个不同制品，⛔ 所以 NL 侧材料只有一份，⛔ 制品侧各不相同。

分段口径：`manual_override`（⭐ 该份规约的编号无法机器判定，分段来自 [corpora/nl_segmentation/overrides.json](../../../../corpora/nl_segmentation/overrides.json) 的人工标注），共 6 段。台账里的「NL 第 N 句」按这套编号读。

## §1 译文纪律（⛔ 先读这三段再看表）

⛔ **译文是给人判缺陷用的，⛔ 不是给人读着舒服用的。** 它严格直译，⛔ 不意译、⛔ 不润色、⛔ 不补原文没有的信息（⛔ 含不补主语、不补量词、不补逻辑连接词）；状态名 / 事件名 / 变量名 / 守卫表达式一律**保留英文原样**，建模术语保留英文并在紧跟的括号里给中文。⭐ 原文含糊的地方译文**照样含糊** —— ⛔ 替它消歧就等于替你做了本轮要你自己做的判断。⭐ 译文是**辅助**，⛔ 判据仍以英文原文为准；两者不一致时以原文为准并请回报。

⭐ 两种方括号标注的含义：`〔原文如此：…〕` 指**原文自身**有语法 / 拼写 / 数格错误，译文照直译并说明错在哪 —— ⛔ 它不是译文的错，⛔ 也不构成模型的缺陷；`〔译者存疑：…〕` 指**原文这里没说清**（谁是主语、并列项是「且」还是「或」、源状态是哪个），⭐ 它直接决定判缺陷时这一句**能不能**用来说模型「违反」了什么。

口径与验收依据：[translations/TRANSLATION_SPEC.md](../translations/TRANSLATION_SPEC.md)；本份译文的原始 JSON：[translations/nl_0000.json](../translations/nl_0000.json)；装载与对拍：[nl_zh.py](../nl_zh.py)。

## §2 逐段：原文与中文严格翻译

| 段 id | 原文 | 中文严格翻译 |
| :-- | :-- | :-- |
| `NL-M001` | 1 The human driving mode is represented by a simple state. | 1 human driving mode 由一个 simple state（简单状态）表示。 |
| `NL-M002` | 2 The autonomous mode has sub-states and is represented by a sub machine state. | 2 autonomous mode 拥有 sub-states（子状态）并由一个 sub machine state（子机状态）表示。 |
| `NL-M003` | 3. when power on, the system turn into human driving mode | 3. 当 power on 时，系统 turn into（转入）human driving mode〔原文如此：turn 与主语 the system 主谓不一致，应为 turns；句末无句号〕 |
| `NL-M004` | 4when front_distance > 10, auto transport to autonomous state | 4当 front_distance > 10 时，auto（自动）transport to（转运到）autonomous state〔原文如此：编号 4 与后接单词 when 之间无空格；transport 疑为 transit / transition 的误用；本段编号 4 与下一段编号 4 重复；句末无句号〕〔译者存疑：auto 既可读作副词 automatically 的缩写，也可读作 autonomous 的缩写而与其后的 autonomous state 重复指涉，原文无法判定〕 |
| `NL-M005` | 4. transit to human driving mode when receive human steering cmd, brake pressed, in (auto final) | 4. transit to（迁移到）human driving mode 当 receive（收到）human steering cmd, brake pressed, in (auto final) 时〔原文如此：when receive 后缺主语，应为 when (the system) receives 或改为被动式；本段编号 4 与上一段编号 4 重复，作者编号序列为 1,2,3,4,4,5，缺 6；句末无句号〕〔译者存疑：human steering cmd, brake pressed, in (auto final) 三项之间无任何连接词，无法判定是合取（and）、析取（or）还是顺序发生的并列列举〕 |
| `NL-M006` | 5 when power off, it will transit to final state | 5 当 power off 时，它 will transit to（将迁移到）final state〔原文如此：句末无句号，全份规格到此结束〕〔译者存疑：it 指代不明，可能指 the system，也可能指当时所处的状态，原文未说明〕 |

## §3 逐段判读提示（该段约束了哪个元素 · 歧义点 · 边界外部分）

⛔ 提示只陈述「原文这一句说了什么、没说什么」，⛔ 不含任何裁决 —— ⭐ 「所以模型应该怎样」是本轮要你自己填的，⛔ 材料不替你填。

⚠️⚠️ **提示里也不含任何关于被测制品的断言** —— ⛔ 一份 NL 服务 6 个 pair，这一页是 6 份工作单共用的，⛔ 讲制品的话必然对其中 5 份为假。⭐ 因此「这个状态在不在」「这条边有没有」一律请自己到各份工作单的 §1.3（作者源，带行号）与 §4（按该 pair 现算的清单）核对，⛔ 不要指望提示替你回答。⚠️ 2026-08-13 之前的旧版工作单**违反过这一条**，若你读过旧版，见 [README.md](../README.md) §十。

- `NL-M001`：约束「状态种类」：human driving mode 这一元素必须是 simple state（简单状态），按 UML 即不含任何 substate（子状态）、不含内部结构。歧义：原文用小写散文短语指代该状态，未给出标识符，「它对应哪一个具名状态」在 NL 层面没有答案，需判读者自行认定。本句未涉及任何迁移、事件或变量。
- `NL-M002`：约束「层次」与「状态种类」：autonomous mode 含有 sub-states（子状态），且其自身被表示为 sub machine state（子机状态）。歧义：(a) UML 中 sub machine state（子机状态，引用一个独立定义的状态机）与 composite state（复合状态，就地展开子结构）不是同一概念，原文未说明取哪一种；(b) 未列出任何具体 substate（子状态）的名字，也未给出数量，因此「有哪些子状态」在 NL 层面是不确定的；(c) 同上一段，autonomous mode 只是小写散文短语，非标识符。
- `NL-M003`：约束「迁移」：触发为 power on，目标为 human driving mode。歧义：(a) 未说明源——是从 initial pseudostate（初始伪状态）出发，还是从任意状态出发；(b) 未说明是「首次上电」还是「任意时刻上电」，⛔ 译文同样不作选择；(c) 未说明 power on 是 event（事件）、guard（守卫）还是外部条件。这三点直接决定「把它画成一条初始迁移」是否算违反本句。
- `NL-M004`：约束「迁移」与「变量」：守卫/条件为 front_distance > 10，目标为 autonomous state。front_distance 是本份 NL 中唯一显式出现的变量名，10 是唯一显式阈值。歧义：(a) 未说明源状态，是否必须从 human driving mode 出发原文没写；(b) autonomous state 与第 2 段的 autonomous mode 是否为同一元素，原文未作任何说明，⛔ 不得自行等同；(c) front_distance > 10 究竟充当 guard（守卫）还是 trigger（触发），原文未区分；(d) auto 的所指见译文中的存疑标注。
- `NL-M005`：约束「迁移」：目标为 human driving mode，触发/条件由三项内容构成：human steering cmd（收到人工转向指令）、brake pressed（刹车被踩下）、in (auto final)。歧义：(a) 三项之间缺连接词（见译文存疑），判缺陷时这一点决定「把三者压成同一条 label / 同一个事件名」是否算违反；(b) in (auto final) 形如 UML 的 in-state 条件（对所处状态的测试谓词），它指涉一个名为 auto final 的元素，而第 2 段虽声称 autonomous mode 有 sub-states，却未列举任何子状态名，此处是 auto final 在全份 NL 中首次且唯一一次出现；(c) 未说明源状态，也未说明该迁移是否只在 autonomous mode 内部有效。
- `NL-M006`：约束「迁移」与「状态」：存在一个 final state，power off 时迁移到它。歧义：(a) it 指代不明（见译文存疑）；(b) 未说明源——是任意状态皆可 power off，还是某个特定状态；(c) final state 究竟是 UML 的 final state（终态伪状态）还是一个名为 final state 的普通具名状态，原文未区分，这直接影响「用终态伪状态还是用一个具名状态」是否算违反；(d) 未说明它与第 5 段 in (auto final) 中的 auto final 是否同一元素。

## §4 整份 NL 层面的观察（术语表 · 跨句反复出现的歧义 · 原文质量问题）

【本份 NL 的整体情况】

这是一份自动驾驶模式切换规格，共 6 条需求，全部挤在单个物理行内。分段不采用按行切分，而直接采用仓库对该份 NL 的人工分段标注（sha256 f1c3dc88… 的 6 段，NL-M001…NL-M006），切点取作者自己写下的六个编号标记的起始偏移；本文件逐段英文原文拼接可完整还原原文（已机械校验）。

【术语表：建模术语，保留英文 + 括号中文】

- simple state（简单状态）：出现于第 1 段
- sub-states / substate（子状态）：出现于第 2 段（原文写作带连字符的复数 sub-states）
- sub machine state（子机状态）：出现于第 2 段
- 以下术语只出现在 note 中，未出现于原文：composite state（复合状态）、guard（守卫）、trigger（触发）、initial pseudostate（初始伪状态）

【术语表：原文中指代状态机元素的英文串，一律原样保留、不译、不改大小写、不加引号】

- 状态指称：human driving mode、autonomous mode、autonomous state、auto final、final state
- 事件/条件指称：power on、power off、human steering cmd、brake pressed、in (auto final)
- 变量与守卫表达式：front_distance、front_distance > 10

⚠️ 注意：上面的状态指称与事件/条件指称在原文里全部是小写散文短语，不是标识符写法；只有 front_distance 一处采用下划线标识符写法。它们与具名标识符之间的对应关系本身就是判读者要做的判断，本译文不代为建立映射，也不统一大小写。

【反复出现的歧义（跨段）】

1. 六条需求中有四条（第 3、4、5、6 段）描述迁移，但没有一条写明源状态，只写了目标。「从哪来」在这份 NL 里系统性缺失，判定任何一条迁移的源是否画错时都缺少 NL 依据。
2. mode / state 两个词被混用：第 1、2、3、5 段用 mode，第 4、6 段用 state；第 5 段除 human driving mode 外还写了 in (auto final)，这是既不写 mode 也不写 state 的第三种写法。autonomous mode 与 autonomous state 是否同一元素、final state 与 auto final 是否有关，原文均无交代。⛔ 译文对每处均按原词保留，不作统一。
3. 触发与守卫不分：power on、power off、front_distance > 10、human steering cmd 等一律以「when …」引入，原文没有区分事件触发与布尔守卫。
4. 第 2 段声称 autonomous mode 有 sub-states 却从不列举；唯一疑似子状态名 auto final 要到第 5 段才以 in (auto final) 的形式出现。

【原文质量问题清单】

- 编号坏：1、2、4（4when 那条）、5 无点，3. 与 4.（transit 那条）有点；4 出现两次（4when… 与 4. transit…），作者编号序列为 1,2,3,4,4,5，缺 6。
- 4when 数字与单词之间无分隔符；同句内 > 10 说明裸数字也会作为数值出现。
- 句末标点不一致：第 1、2 段有句号，第 3、4、5、6 段均无。
- 语法错误 3 处：the system turn（主谓不一致）、when receive（缺主语）、transport 疑为 transit/transition 误用。
- 指代不明 1 处：第 6 段的 it。

【建模对象边界检查（M = (S, E, V, Tr, A)，无时钟、无并发）】

全份 NL 未出现任何时间约束（无秒级时限、无 after/timeout 措辞）、未出现任何 orthogonal region（正交区）、fork/join 或 concurrent activation 措辞。因此本份 NL 没有任何内容落在建模对象边界之外，六段 note 中均无边界外条目。

【译法与格式说明】

- 行首编号严格照抄：1 空格 / 2 空格 / 3. 空格 / 4 紧贴 when 无空格 / 4. 空格 / 5 空格。
- 原文句末无句号处，译文同样不补句号；原文内部逗号原样保留。
- 各段 en 末尾的段间空格（第 1—5 段各一个）是分段切点的产物，zh 字段未镜像该尾随空格，其余空格与标点均照抄。
- 未对任何一处歧义作消歧处理；凡需选择的地方一律以〔译者存疑〕保留。
- 〔原文如此〕共 4 处（第 3、4、5、6 段），〔译者存疑〕共 3 处（第 4、5、6 段）。

## §5 NL 原始字节（带物理行号）

```text
  1 | 1 The human driving mode is represented by a simple state. 2 The autonomous mode has sub-states and is represented by a sub machine state. 3. when power on, the system turn into human driving mode 4when front_distance > 10, auto transport to autonomous state 4. transit to human driving mode when receive human steering cmd, brake pressed, in (auto final) 5 when power off, it will transit to final state
```
