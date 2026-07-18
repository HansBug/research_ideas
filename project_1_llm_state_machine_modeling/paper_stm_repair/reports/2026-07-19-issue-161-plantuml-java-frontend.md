# Issue #161：PlantUML Java source frontend 与 60 例人工验收报告

## 1. 结论先行

Issue #161 不是单一根因。

1. PlantUML `v1.2024.7` 的官方 SCXML exporter 确实有结构性信息损失，不能作为 statechart canonical AST。
2. 旧转换脚本又把这个有损产物当成语义真源，并继续做全局 short-ID 去重、endpoint lifting、first-child inference 和 blocked-edge 跳过，扩大了损失。
3. LLMS-EMP raw PlantUML 本身还包含非官方 `stm` 容器、无 owner lifecycle、无 initial composite、无标签 fan-out、显式 fork、时序/guard/effect 混合 label 等 source-level 问题。converter 不能替作者猜语义。

因此正确路线不是“换一个 SCXML parser”，而是：

```text
raw PlantUML
  -> Java 两遍 source frontend（canonical + raw span）
  -> PlantUML StateDiagram/Entity/Link 官方内部模型差分
  -> fail-closed FCSTM lowering
  -> pyfcstm parse/inspect/runtime
  -> 60 例逐例人工/LLM 阅读验收
```

当前最终工作副本结果：

| 指标 | 结果 |
|---|---:|
| Java source parse | `60/60` |
| raw 官方直接得到 `StateDiagram` | `33/60` |
| 仅用于差分的 normalization 后官方 `StateDiagram` | `60/60` |
| source states | `524` |
| source transitions | `754` |
| mapped transitions | `719` |
| explicitly blocked transitions | `35` |
| silently dropped transitions | `0` |
| root/nested final coverage | `36/36` |
| state-owned lifecycle coverage | `18/18` |
| FCSTM parse/inspect | `60/60` |
| `exact_r45_structure` | `19/60` |
| `blocked_unsupported` | `41/60` |

`41` 个 blocked case 不能进入 Discover input pool。这不是“41 个转换成功”，而是“41 个 raw source 暂时无法在当前 FCSTM 语义下无猜测执行，converter 已失败关闭并保留证据”。

## 2. 官方 SCXML 到底有什么问题

固定 jar：PlantUML `1.2024.7`，SHA-256 `e34c12bbe9944f1f338ca3d88c9b116b86300cc8e90b35c4086b825b5ae96d24`，对应官方 tag commit [`d2b2bcf1`](https://github.com/plantuml/plantuml/commit/d2b2bcf1722b8705f7f01a556dc96751e7739f7d)。

官方 [`ScxmlStateDiagramStandard`](https://github.com/plantuml/plantuml/blob/d2b2bcf1722b8705f7f01a556dc96751e7739f7d/src/net/sourceforge/plantuml/xmlsc/ScxmlStateDiagramStandard.java) 的实现直接证明：

1. `getId` 只取 `entity.getName()` 并删除 `*`，不使用 qualified `Quark`；不同 composite 内的 `InitialState` 会落到相同 short ID。
2. start/end circle 都走 `createState`，输出普通 `<state>`；final pseudo identity 没有独立 SCXML `<final>` 语义。
3. `addLink` 只取第一行 display label，整段写成 `event`；没有 guard/effect/timing grammar。
4. state `Bodier` 中的 entry/do/exit 与其他 body text 不进入行为输出；note 还会进入 entity/link 集合。

官方 [`StateDiagram`](https://github.com/plantuml/plantuml/blob/d2b2bcf1722b8705f7f01a556dc96751e7739f7d/src/net/sourceforge/plantuml/statediagram/StateDiagram.java) 本身更丰富：它保留 parent container、qualified `Quark`、`LeafType.CIRCLE_START/CIRCLE_END`、concurrent group 和 `Link`。这说明主要损失发生在 `StateDiagram -> SCXML` export，而不是 XML parser 读错。

但 `StateDiagram` 也不是公开稳定 AST：

- 没有本项目所需的完整 raw source span。
- parser 是顺序执行的；`0000` 在 `HumanDriving` 内先引用尚未声明的 `Autonomous` 时，官方内部模型会先创建 `HumanDriving.Autonomous`，后面的 root `state Autonomous` 又成为另一个实体。
- 27 个 raw case 含官方语法之外的 `stm`/bare lifecycle/fork 变体，不能直接得到 `StateDiagram`。

所以新 frontend 不把官方内部模型当唯一真源，而是把它作为版本固定的 differential evidence。case `0000` 的官方 scope disagreement、case `0019` 的 note attachment 都进入 canonical metadata，不能被隐藏。

## 3. 旧脚本为什么把问题放大了

SCXML 的损失本来应该触发 blocked；旧链路却继续做了以下近似：

- 用全局 short-ID 合并不同 scope 的 state。
- 把 leaf endpoint 提升到 composite boundary。
- composite 缺 initial 时选择第一个 child。
- 跨层 edge 无法渲染时跳过，但 partial FCSTM 仍可被下游消费。
- 把 end state 当普通 leaf，把 lifecycle/state body 当展示信息删除。
- 只用 parse/inspect 当 gate，没有 raw-to-FCSTM transition coverage 和 runtime probe。

因此 Issue #161 的正确判断是：官方 SCXML 路线确实不适合作 canonical；旧转换思路也有重大错误；raw corpus 还存在必须由 converter 明示的歧义。三者缺一不可。

## 4. 新实现

### 4.1 Java 核心

[Java frontend](../pipeline/conversion/java/plantuml-state-frontend/README.md) 负责：

- 两遍收集 `state` 关键字声明、alias、lexical scope、body 与 transition。
- 只把显式 `state`/alias 当跨 scope symbol anchor；普通 `State : body` 留在当前 scope。
- 输出 qualified state ID、parent、kind、initial/final boundary、raw label、lifecycle、body 与 `file:line`。
- 调用固定 PlantUML jar 的 `SourceStringReader -> StateDiagram -> Entity/Link` 生成官方差分快照。
- 记录 validation-only normalization，绝不拿 normalization 结果生成 canonical。

### 4.2 Python wrapper

Python 只做：

- jar 路径与 SHA-256 校验；
- `make compile`；
- `subprocess` 调用 Java；
- JSON 读取与 schema/版本检查；
- FCSTM lowering、pyfcstm parse/inspect/runtime 验证。

### 4.3 关键 lowering

- 带 event 的 initial：生成 stoppable `InitialWait*`，随后消费 opaque event 进入真实 child。
- leaf 跨层迁移：同一 raw event 贯穿 child exit、parent continuation 与 event-specific target entry，避免不同 deep target 按声明顺序坍缩。
- nested final：进入 `FinalWait*` completion-hold，允许外层 composite 后续再消费事件；root final 继续真正终止。
- lifecycle-only state：生成 `LifecycleActive` leaf，使 entry/do/exit wrapper 可运行。
- composite target 无合法 initial、multiple initial、unlabeled fan-out、explicit fork、opaque state body、owner 不明 lifecycle：reason-coded blocked。
- 所有 transition 必须是 mapped 或 blocked；两者之和必须等于 source transition 数。

## 5. 真实例子

### 5.1 `0000`：重复 short name 与跨层迁移

raw PlantUML 中 `HumanDriving.InitialState` 与 `Autonomous.InitialState` 是两个实体，且 initial label 本身有事件语义：

```plantuml
state HumanDriving {
    [*] --> InitialState : Power On
    InitialState --> Autonomous : Front Distance > 10
}
state Autonomous {
    [*] --> InitialState : Enter Autonomous
}
```

新 FCSTM 的关键片段：

```fcstm
state HumanDriving {
    state InitialWaittr_0002;
    [*] -> InitialWaittr_0002;
    InitialWaittr_0002 -> InitialState : /Power_On;
    InitialState -> [*] : /Front_Distance_10;
}
state Autonomous {
    state InitialWaittr_0006;
    [*] -> InitialWaittr_0006;
    InitialWaittr_0006 -> InitialState : /Enter_Autonomous;
}
HumanDriving -> Autonomous : /Front_Distance_10;
```

runtime probe 依次发送 `Power_On -> Front_Distance_10 -> Enter_Autonomous`，最终到达 `Autonomous.InitialState`。两个 `InitialState` 不再合并。

### 5.2 `0022`：final 不是普通 `end` state

```plantuml
PoweredOn --> [*]: keyOff
```

```fcstm
PoweredOn -> [*] : /keyOff;
```

runtime 后 `is_ended=true` 且 stack 为空；不再停在普通 `end` leaf。

### 5.3 `0054`：lifecycle-only state

```plantuml
Accelerating : entry/Accelerate
Approaching : do/Send
EmergencyStopping : do/Emergency Stop
```

```fcstm
state Accelerating {
    enter abstract Accelerate;
    state LifecycleActive;
    [*] -> LifecycleActive;
}
state Approaching {
    >> during before abstract Send;
    state LifecycleActive;
    [*] -> LifecycleActive;
}
```

4 条 state-owned lifecycle 全部可从 source map/inspect 找回。

### 5.4 `0053`：fan-out 不冒充 concurrency

```plantuml
PumpState --> WaterState
PumpState --> MethaneState
```

两条边均保留在 FCSTM，但 case 裁决为 `blocked_unsupported / R45.BLOCKED.ambiguous_unlabeled_fanout`。当前单 active-leaf runtime 无法证明这里是 nondeterminism、choice 还是 concurrency，因此禁止进入 Discover。

## 6. 60 例逐例人工/LLM 阅读总账

口径：`A` 表示 raw 结构在当前 R4.5 边界内可执行且无 blocker；`B` 表示 converter 已正确保留可证明部分并对其余部分失败关闭；`C` 表示仍有 converter defect。最终没有 `C`，但所有 `B` 都不能作为无损转换结果使用。

最终 leaf 复验绑定：converter commit 为 `577f33f95fc4cfe31f3f321399c167f50df3bd73`，`pyfcstm` gitlink/checkout 均为 `4ea23c9b153f47e5c4a2125d95b466eee6eed13e`，固定 PlantUML jar SHA-256 为 `e34c12bbe9944f1f338ca3d88c9b116b86300cc8e90b35c4086b825b5ae96d24`。本次主 session LLM 按 `0000` 至 `0059` 顺序读取每组完整 raw PlantUML、完整 FCSTM 与 blocker/mapping 摘要；submodule preflight 修复后重跑的 60 个 FCSTM 集合 SHA-256 为 `2eaf969bf34dcee811f6679b82c773a1ee8af4838fc63ab8f02389bb330bac88`，且 canonical/FCSTM 与逐组阅读版本 `60/60` bitwise identical。

| case | 结论 | 人工对读要点 |
|---|---|---|
| `0000` | B | 双 scope `InitialState`、三段事件路径与 initial wait 正确；三条 state body 保持 opaque blocker。 |
| `0001` | B | 6 条平面边一致；state description 未执行，blocked。 |
| `0002` | A | PumpControl 层次、initial 与 4 条事件边一致。 |
| `0003` | A | Operate composite 与 root start/keyOff 一致。 |
| `0004` | B | self-initial 非法，1 条 transition blocked；4 条 lifecycle 全保留。 |
| `0005` | B | 同名 state 按 scope 区分；1 条非法 self-initial 与 2 条无 initial composite 入口 blocked。 |
| `0006` | B | 12 条平面边一致；description/slash label 保持 opaque。 |
| `0007` | B | 三种 collision event 分别进入 Brake/Steer/Alert；nested final 可稳定；body/missing default initial blocked。 |
| `0008` | B | 27 条边与 TurnOff nested final 保留；无标签 fan-out 与时间/概率 label 不推断。 |
| `0009` | A | Highway/Urban 双层 scope、26 条边和独立 CollisionAvoidanceSystem 一致。 |
| `0010` | B | 8 条边一致；多条 state description/stereotype opaque。 |
| `0011` | B | 与 `0001` 同构；description blocked。 |
| `0012` | A | Off/Operate 层次与 7 条边一致。 |
| `0013` | A | 3 leaf、6 事件边及 root/composite initial 一致。 |
| `0014` | B | 缺 root initial，4 条 composite-target edge blocked；带 label initial 保留。 |
| `0015` | A | 六个 composite、重复 `State1`、22 条跨层 macro 均按 scope 对齐。 |
| `0016` | A | root initial event、Search/Formation/Attack 往返及 nested final 一致。 |
| `0017` | B | alias F/R/P、3 条 root final 正确；CA 无默认 initial，blocked。 |
| `0018` | B | 可证明的 13 条边保留；8 条无 initial composite entry blocked，fan-out/timing opaque。 |
| `0019` | B | 25 条行为边一致；note attachment 不进入行为；CollisionAvoidanceSystem 缺 initial。 |
| `0020` | B | nested child 回 HumanDriving 与 2 条 final 一致；state body opaque。 |
| `0021` | B | 6 条平面边一致；description blocked。 |
| `0022` | A | 9 条边一致；`keyOff` runtime 真终止。 |
| `0023` | B | 4 条边一致；4 条 state body opaque。 |
| `0024` | B | InMotion entry/exit 与 empty-label completion 保留；root bare exit owner 不明。 |
| `0025` | A | Microwave 16 条平面边逐条一致。 |
| `0026` | B | 5 条边与 root final 一致；state descriptions opaque。 |
| `0027` | B | 三条 initial fan-out 保留并阻塞；不固定声明顺序为语义。 |
| `0028` | B | 23 条平面边与 1 条 root final 保留；fork-like fan-out/timing body blocked。 |
| `0029` | B | root/nested `FinishState` scope保持；4 条无 initial composite entry blocked。 |
| `0030` | B | 两条 root initial 原样保留并阻塞；`/ [*]` 只作 opaque label。 |
| `0031` | B | 6 条平面边一致；description blocked。 |
| `0032` | B | 13 条 device edge 一致；state body opaque。 |
| `0033` | B | `stm` 仅作 model container；7 条边一致，body opaque。 |
| `0034` | B | directional arrow 不误判层级；5 lifecycle 与 2 final 保留；三路无标签 fan-out blocked。 |
| `0035` | B | 16 条 Microwave 边一致；6 个 body description opaque。 |
| `0036` | B | 7 条 UAV 边一致；description/slash label opaque。 |
| `0037` | B | bracket endpoint 还原；3 条 final 正确；description opaque。 |
| `0038` | B | 同名 nested state 不合并；8 条不稳定 composite entry blocked；self/multiple initial 明示。 |
| `0039` | B | nested final completion-hold 与 26 条边一致；两条 root initial blocked。 |
| `0040` | B | initial wait、Autonomous 子状态与 root final 一致；body opaque。 |
| `0041` | B | 6 条平面边一致；description blocked。 |
| `0042` | A | keyOff initial wait 与 Operate 6 条内部/外部边一致。 |
| `0043` | A | bracket label 作为完整 opaque event，4 条边一致。 |
| `0044` | B | inline lifecycle 可运行；InMotion 缺 initial，1 条 entry blocked；2 final 正确。 |
| `0045` | A | 各 composite 内同名 implicit state 按 lexical scope 保留；20 条边一致。 |
| `0046` | B | 6 条 UAV 边一致；state description/slash label opaque。 |
| `0047` | B | 三个 alias composite 与 3 final 一致；root initial 缺失。 |
| `0048` | B | 24 条 flat edge 与 2 final 保留；fan-out 与 timing body blocked。 |
| `0049` | A | 三个 lexical `FinishState`、29 条边与 root sibling system 一致。 |
| `0050` | A | literal `\\n` label、nested completion 与 3 final 一致。 |
| `0051` | B | 6 条平面边一致；description blocked。 |
| `0052` | A | Off/Operate 层次与 8 条边一致。 |
| `0053` | B | 两条无标签 PumpState fan-out 均保留，显式阻塞；body opaque。 |
| `0054` | A | 8 条边与 4 条 lifecycle 均可运行/可追溯。 |
| `0055` | A | 16 条 Microwave 平面边一致。 |
| `0056` | A | Search composite 循环、4 条 root transition 与 final 一致。 |
| `0057` | B | CA 三子 composite 保留；root initial 直接进入无 initial CA，逐迁移 blocked。 |
| `0058` | B | explicit alias body 回填正确；fork pseudo 明示；5 条 composite entry blocked，timing body opaque。 |
| `0059` | A | Highway/Urban/CollisionAvoidanceSystem 层次与 25 条边一致。 |

## 7. 验收与限制

通过项：

- Java compile 与固定 jar identity。
- Python wrapper 拒绝错误 jar。
- `60/60` source parse、FCSTM parse、inspect。
- `754 = 719 mapped + 35 blocked + 0 silent`。
- `36/36` final；`18/18` state-owned lifecycle。
- runtime 覆盖 `0000` initial/cross-scope、`0007` 三 deep target、nested final/outer termination、`0022` root termination、`0004/0054` lifecycle wrapper。
- 本节 60 行由 LLM 逐例读取 raw PlantUML 与最终 FCSTM 后形成，不是脚本自动生成的“人工验收”。

仍不支持：

- 把 opaque label 自动拆成 event/guard/effect/timing。
- orthogonal region / fork-join product-state lowering。
- 无 initial composite 的 child 推断。
- generic state body 的可执行语义。
- owner 不明的 bare lifecycle。

因此当前路线可以替代不可靠 SCXML canonical，但不能宣称 60 例均已无损转换。可进入后续实验的严格集合只有 `19` 例；其余 `41` 例需先修 raw source、扩展 FCSTM 语义或实现有证明义务的新 lowering。
