<!-- RELABEL schema=paper1.relabel.nldoc.v1 nl_dir=nl_0006 -->
# NL 规约材料 · `nl_0006`

本文件由 [generate.py](../generate.py) 生成，**没有任何填写区** —— 它是只读材料。判读要填的东西全在同目录的 `<pair>.md` 里。

本页服务同目录的 **6** 份工作单：[`0006`](./0006.md)、[`0016`](./0016.md)、[`0026`](./0026.md)、[`0036`](./0036.md)、[`0046`](./0046.md)、[`0056`](./0056.md)。它们由**同一份 NL 规约**（sha8 `a01c022f`）生成 6 个不同制品，所以 NL 侧材料只有一份，制品侧各不相同。

分段口径 `line_split`（按物理行切）：按物理行切分，与 pipeline 同口径，共 **4** 段（`NL-L001` … `NL-L004`）。台账里的「NL 第 N 句」与你要在工作单 §5 填的 `nl_evidence` 都按这套段 id 读。

## §1 译文纪律（先读这三段再看表）

**译文是给人判缺陷用的，不是给人读着舒服用的。** 它严格直译，不意译、不润色、不补原文没有的信息（含不补主语、不补量词、不补逻辑连接词）；状态名 / 事件名 / 变量名 / 守卫表达式一律**保留英文原样**，建模术语保留英文并在紧跟的括号里给中文。⚠️ 原文含糊的地方译文**照样含糊** —— 替它消歧就等于替你做了本轮要你自己做的判断。⚠️ 译文是**辅助**，判据仍以英文原文为准；两者不一致时以原文为准并请回报。

两种方括号标注的含义：`〔原文如此：…〕` 指**原文自身**有语法 / 拼写 / 数格错误，译文照直译并说明错在哪 —— 它不是译文的错，也不构成模型的缺陷；`〔译者存疑：…〕` 指**原文这里没说清**（谁是主语、并列项是「且」还是「或」、源状态是哪个），它直接决定判缺陷时这一句**能不能**用来说模型「违反」了什么。

口径与验收依据：[translations/TRANSLATION_SPEC.md](../translations/TRANSLATION_SPEC.md)；本份译文的原始 JSON：[translations/nl_0006.json](../translations/nl_0006.json)；装载与对拍：[nl_zh.py](../nl_zh.py)。

## §2 逐段：原文与中文严格翻译

| 段 id | 原文 | 中文严格翻译 |
| :-- | :-- | :-- |
| `NL-L001` | 1 This state machine model describes the state transitions of a UAV swarm. | 1 本状态机模型描述一个无人机集群（UAV swarm）的状态迁移。 |
| `NL-L002` | 2 Before the mission is completed, the UAV swarm continuously performs target search tasks, during which it operates within three different state areas. | 2 在任务完成之前，无人机集群持续执行目标搜索任务（target search tasks），在此期间其运行于三个不同的状态区（state areas）内。〔译者存疑：state areas 不是标准 UML 术语，原文所指究竟是 orthogonal region（正交区）、三个并列的状态，还是三组状态分区，无法从原文判定，故按字面直译并括注原文，不作消歧。〕 |
| `NL-L003` | 3 When the UAV swarm is intercepted, it transitions to the formation adjustment state. | 3 当无人机集群被拦截时，其迁移到编队调整状态（formation adjustment state）。 |
| `NL-L004` | 4 During flight, if task assignment information is received, it enters the attack state. After completing the attack, the number of UAVs in the swarm decreases accordingly. | 4 飞行期间，如果任务分配信息（task assignment information）被接收到，其进入攻击状态（attack state）。在完成攻击之后，集群中无人机的数量相应减少。 |

## §3 逐段判读提示（该段约束了哪个元素 · 歧义点 · 边界外部分）

提示只陈述「原文这一句说了什么、没说什么」，不含任何裁决 —— 「所以模型应该怎样」是本轮要你自己填的，材料不替你填。

**提示里也不含任何关于被测制品的断言** —— 一份 NL 服务 6 个 pair，这一页是 6 份工作单共用的，讲制品的话必然对其中 5 份为假。因此「这个状态在不在」「这条边有没有」一律请自己到各份工作单的 §1.2（作者源，带行号）与 §4（按该 pair 现算的清单）核对，不要指望提示替你回答。2026-08-13 之前的旧版工作单**违反过这一条**，若你读过旧版，见 [README.md](../README.md) §十。

- `NL-L001`：元素类型：迁移。本句只概括说明描述对象为无人机集群的状态迁移，未给出任何具体状态名、事件或迁移条件。
- `NL-L002`：元素类型：状态（区）。原文要求：任务完成之前，无人机集群持续执行目标搜索任务，并在三个不同的状态区内运行。歧义点：①原文未列出三个状态区的名称，也未说明「不同」的含义及三个状态区之间的关系；②「任务完成」的判定条件与触发事件未给出；③「目标搜索任务」未说明其是否对应某一状态，也未说明其与三个状态区如何对应。边界外：「持续执行」「在此期间」含持续性时间语义，本项目建模对象不含时钟与时间约束。
- `NL-L003`：元素类型：状态、事件、迁移。本句给出迁移：无人机集群被拦截时转入编队调整状态，触发事件为「被拦截」。歧义点：①「被拦截」未说明由谁实施、以何种信号表示；②未给出转入编队调整状态的源状态；③未给出离开编队调整状态的条件。
- `NL-L004`：元素类型：状态、事件、迁移、变量。本句给出：收到任务分配信息时进入攻击状态（触发事件：任务分配信息被接收到）；完成攻击后，集群中无人机的数量相应减少（涉及变量：无人机数量）。歧义点：①未给出进入攻击状态的源状态；②「完成攻击」的判定条件未给出；③「相应减少（accordingly）」未说明按什么相应、减少多少；④「飞行期间」未说明「飞行」与各状态的关系。

## §4 整份 NL 层面的观察（术语表 · 跨句反复出现的歧义 · 原文质量问题）

对象名译名对照表（英文原文 → 中文译名，正文严格照此执行）：

- UAV swarm → 无人机集群；其后的 the UAV swarm、the swarm、UAVs 同指该对象，分别译作「无人机集群」「集群」「无人机」，不再括注英文
- state transitions → 状态迁移（通用术语，未括注英文）
- target search tasks → 目标搜索任务
- state areas → 状态区
- formation adjustment state → 编队调整状态
- task assignment information → 任务分配信息
- attack state → 攻击状态；the attack 译作「攻击」，指攻击这一行为，不再括注英文

反复出现的歧义与欠指定：

- 第 3、4 段各给出一个带触发条件的迁移（第 3 段：被拦截时转入编队调整状态；第 4 段：收到任务分配信息时进入攻击状态），两处均未给出源状态。
- 第 2 段「三个不同的状态区」未列出各区名称与相互关系；「任务完成」的判定条件未给出。
- 第 4 段「完成攻击」的判定条件、无人机数量「相应减少」的幅度均未给出。
- 全篇未出现形式表达式（比较式、赋值、带单位的量）。

原文质量问题：

- 四段均未见语法、拼写或数格错误，故无〔原文如此〕标注。

## §5 NL 原始字节（带物理行号）

```text
  1 | 1 This state machine model describes the state transitions of a UAV swarm. 
  2 | 2 Before the mission is completed, the UAV swarm continuously performs target search tasks, during which it operates within three different state areas. 
  3 | 3 When the UAV swarm is intercepted, it transitions to the formation adjustment state. 
  4 | 4 During flight, if task assignment information is received, it enters the attack state. After completing the attack, the number of UAVs in the swarm decreases accordingly.
```
