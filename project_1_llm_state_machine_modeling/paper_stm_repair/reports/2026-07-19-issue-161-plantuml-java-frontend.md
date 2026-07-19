# Issue #161：PlantUML 官方 SCXML、官方内部模型与 FCSTM 转换修复报告

## 1. 结论先行

这次问题不是二选一，而是三个问题叠加：

1. **PlantUML `1.2024.7` 官方 SCXML exporter 确实有结构性信息损失，不能作为状态图 canonical。** 它使用 short name 作为 ID，把 end circle 输出成普通 `<state>`，把整段 label 写成一个 `event`，并丢弃 state body/lifecycle。
2. **旧转换脚本的思路也有重大错误。** 它在有损 SCXML 上继续做 global short-ID 去重、endpoint lifting、first-child initial 推断和 blocked-edge skip，把“应失败关闭的证据不足”变成了可继续消费的 partial FCSTM。
3. **LLMS-EMP raw PlantUML 本身包含无法由 converter 唯一决定的行为语义。** multiple initial、无标签 fan-out、显式 fork、`after 2s`、`[x]`、`a / b`、bare lifecycle 等不能靠字符串形状自动决定是 event、guard、effect、timing 或 concurrency。

所以最终选择是：

- 放弃 `PlantUML -> SCXML -> canonical` 路线；
- 不放弃 PlantUML source；
- Java 两遍 source frontend 直接建立 scope-aware canonical；
- 固定版本的 PlantUML `StateDiagram/Entity/Link` 只作 differential evidence；
- Python 只通过 subprocess 调 Java，再执行 FCSTM lowering 和审计；
- 把结构保存、运行语义和下游 eligibility 拆成三个轴。

最终结果：

| 指标 | 结果 |
|---|---:|
| Java source parse | `60/60` |
| source states | `524` |
| source transitions | `754` |
| mapped transition macros | `754/754` |
| blocked / silent drop | `0 / 0` |
| final boundary | `36/36` |
| opaque body line | `96/96` |
| lifecycle source item | `19/19` |
| FCSTM parse / inspect | `60/60 / 60/60` |
| independent pyfcstm AST audit | `60/60` |
| structural preservation | `60/60` |
| FCSTM execution eligible | `0/60` |
| Discover eligible | `0/60` |

这里的 `60/60` 是 **FCSTM + mandatory trace bundle 的结构保真**，不是 `60/60 semantic equivalence`。`.fcstm` 单文件不包含 raw span、source braces 和 operational debt，不能脱离 case report 单独宣称可逆。

## 2. 官方 SCXML 为什么真的不可靠

固定版本：PlantUML `1.2024.7`，jar SHA-256：

```text
e34c12bbe9944f1f338ca3d88c9b116b86300cc8e90b35c4086b825b5ae96d24
```

对应官方 tag commit [`d2b2bcf1`](https://github.com/plantuml/plantuml/commit/d2b2bcf1722b8705f7f01a556dc96751e7739f7d)。官方 [`ScxmlStateDiagramStandard`](https://github.com/plantuml/plantuml/blob/d2b2bcf1722b8705f7f01a556dc96751e7739f7d/src/net/sourceforge/plantuml/xmlsc/ScxmlStateDiagramStandard.java) 的关键行为是：

1. `getId(entity)` 基于 `entity.getName().replaceAll("\\*", "")`，不使用 qualified `Quark` path。
2. start/end circle 都走普通 state 输出路径，没有 SCXML `<final>` 身份。
3. link display label 直接进入 `transition event="..."`，没有 guard/effect/timing grammar。
4. state `Bodier`、entry/do/exit 与 raw source span 不进入 SCXML 行为制品。

### 2.1 真实 `0000`：short ID 与 scope 信息坍缩

PlantUML 原文有两个不同 scope 的 `InitialState`：

```plantuml
state HumanDriving {
    [*] --> InitialState : Power On
    InitialState --> Autonomous : Front Distance > 10
}
state Autonomous {
    [*] --> InitialState : Enter Autonomous
    InitialState --> FinalState : Exit Autonomous
}
```

仓库归档的官方 SCXML 却只留下一个 `InitialState`，并把两组迁移挂到同一 state；`Autonomous` 还因 forward reference 被嵌入 `HumanDriving`：

```xml
<state id="HumanDriving">
  <state id="InitialState">
    <transition event="Front Distance &gt; 10" target="Autonomous"/>
    <transition event="Exit Autonomous" target="FinalState"/>
  </state>
  <state id="Autonomous">
    <state id="startAutonomous">
      <transition event="Enter Autonomous" target="InitialState"/>
    </state>
  </state>
</state>
```

新 FCSTM 使用 qualified source identity，两个 `InitialState` 保持独立：

```fcstm
state HumanDriving {
    state InitialState;
    state InitialWaittr_0002;
    [*] -> InitialWaittr_0002;
    InitialWaittr_0002 -> InitialState : /Power_On;
    InitialState -> [*] : /Front_Distance_10;
}
state Autonomous {
    state InitialState;
    state InitialWaittr_0006;
    [*] -> InitialWaittr_0006;
    InitialWaittr_0006 -> InitialState : /Enter_Autonomous;
}
HumanDriving -> Autonomous : /Front_Distance_10;
```

这不是 XML parser 使用不当；损失已经发生在官方 `StateDiagram -> SCXML` export 中。

### 2.2 真实 `0039`：final 变成普通 state，条件变成 event

PlantUML：

```plantuml
lane_change --> [*] : dist_to_exit<2
cruise --> [*] : dist_to_exit<2
```

官方 SCXML：

```xml
<state id="lane_change">
  <transition event="dist_to_exit&lt;2" target="endHighwayMode"/>
</state>
<state id="endHighwayMode"/>
```

这里同时发生两件事：`[*]` 的 final identity 被降成 ordinary state；看起来像 guard 的 `dist_to_exit<2` 被整体当作外部 event。新链路恢复 final boundary，但仍把 label 标为 opaque，不擅自认定它一定是 guard：

```fcstm
state FinalWaittr_0009 named "Completed final boundary: AutonomousMode.HighwayMode.lane_change";
lane_change -> FinalWaittr_0009 : /dist_to_exit_2;
```

## 3. 为什么不能直接把官方内部对象当稳定 AST

逆向 jar 与阅读官方源码后，PlantUML 的 [`StateDiagram`](https://github.com/plantuml/plantuml/blob/d2b2bcf1722b8705f7f01a556dc96751e7739f7d/src/net/sourceforge/plantuml/statediagram/StateDiagram.java) 确实比 SCXML 丰富：它保留 parent container、qualified `Quark`、`LeafType.CIRCLE_START/CIRCLE_END`、concurrent group、`Entity` 和 `Link`。

但它仍不适合作唯一 canonical：

- 这是内部实现对象，不是稳定公开 AST/API。
- PlantUML state syntax 没有一份可直接生成 parser 的完整官方形式文法；命令类按行匹配并直接修改 `StateDiagram`。
- 它不保留本研究需要的完整 raw source span 和 source-level ambiguity。
- 解析是顺序执行的。`0000` 中在 `HumanDriving` 内先引用尚未声明的 `Autonomous`，官方对象会先创建 nested entity；后面的 root declaration不能恢复原始意图。
- `27/60` raw case 含 `stm` container、bare lifecycle、fork 变体等官方 parser 不能直接接受的输入。

因此“直接读官方源码”得到的正确设计不是反射/序列化全部私有字段，而是：

```text
raw source canonical（本项目稳定合同）
        +
pinned official internal snapshot（差分证据）
```

官方 snapshot 用于回答“固定版本官方 parser 看到了什么”；source canonical 用于回答“raw 文本实际写了什么、在哪一行、属于哪个 lexical scope”。

## 4. 旧转换脚本的重大错误

官方 SCXML 有损本应触发 fail-closed；旧脚本却继续做近似：

1. 用 global short ID 合并不同 scope 的同名 state。
2. 为满足 FCSTM sibling endpoint，提升 leaf source/target 到 composite boundary。
3. composite 缺 initial 时选择第一个 child。
4. 无法合法 lowering 的 edge 只记 blocked 后跳过，partial FCSTM 仍可进入后续。
5. 把 final 当普通 dead-end leaf。
6. lifecycle/body 丢失后仍用 parse/inspect success 作为可信 gate。

Issue #161 旧审计发现的 `16` 条 dropped transition、`36` 条 final 失真和 scope collapse，主要就是这两层损失叠加产生的。现在 converter 不再使用 SCXML canonical，也不再把“可解析”当成“忠实”。

## 5. 新实现

### 5.1 Java 核心

路径：[plantuml-state-frontend](../pipeline/conversion/java/plantuml-state-frontend/README.md)

- 两遍收集 explicit state、alias、lexical scope、transition、body 和 lifecycle。
- 生成 qualified state ID、parent、kind、initial/final boundary、raw label 与 `file:line`。
- 保留 `declared_with_block`，即使某个 source block 在 FCSTM 运行投影中没有 child。
- 调用固定 PlantUML `SourceStringReader -> StateDiagram -> Entity/Link` 生成官方差分快照。
- validation-only normalization 不参与 canonical 或 lowering。
- 局部 `Makefile` 提供 `fetch / verify / compile / run / clean`。

### 5.2 Python wrapper

Python adapter 不重新解析 PlantUML：

1. 校验 PlantUML version/jar SHA。
2. 执行局部 `make compile`。
3. 用 `subprocess` 调 Java CLI。
4. 读取并校验 JSON schema。
5. 调用 FCSTM lowering、pyfcstm parse/inspect 与独立 AST audit。

### 5.3 FCSTM lowering

- event-labeled initial 使用 `InitialWait*`，避免进入 composite 时事件丢失。
- root final 直接发出 `X -> [*]`；nested final 使用 `FinalWait*` completion hold。
- leaf cross-scope transition 拆成 child exit、parent continuation、target entry，全部绑定同一 source transition ID。
- transition-specific deep entry 排在普通/default initial 与 `UnspecifiedInitial` 之前；source order和 duplicate occurrence不去重。
- missing initial 使用可见、可停止的 `UnspecifiedInitial`，绝不猜 child。
- invalid/non-direct initial 使用保留 raw target identity 的 surrogate。
- lifecycle 挂为 abstract hook；这只证明结构位置和 action ID，不证明源动作行为已注册执行。
- generic state body 与 ownerless lifecycle 进入 display metadata + trace。
- multiple initial、unlabeled fan-out、explicit fork 的所有边都发出，但 case 保持 execution-ineligible。

## 6. 三轴裁决

旧 `exact / blocked` 一维口径无法区分“source fact 保存了”与“行为可证明”。当前每例独立记录：

```json
{
  "structural_verdict": "structure_preserved",
  "operational_status": "source_ambiguity_or_unsupported_semantics_preserved",
  "fcstm_execution_eligible": false,
  "discover_eligible": false
}
```

结构 PASS 的必要条件：

- source state ID 与 trace ID Counter 完全相等，source state path 单射；
- output states 恰好等于 source-origin states、allowlisted synthetic states 和 root；
- `754` 个 source transition ID 逐个有非空 macro；
- authored FCSTM transition multiset 与 trace 完全相等，没有 untracked edge；
- AST endpoint、scope、event、forced、final hold 和 entry priority 可反查；
- `96` body、`19` lifecycle、36 final 与 orphan fact 可从 canonical 重建；
- transition declaration order、multiple initial order、fan-out order和 placeholder priority受审计保护。

运行/Discover eligibility 另行判断。当前所有 60 例至少含一个 opaque transition label 或其他 debt，因此严格结果是 `0/60`，不能把结构 PASS 直接投入 #158。

## 7. 真实修复例子

### 7.1 `0005`：missing initial 不再丢 incoming edge，也不猜 child

PlantUML：

```plantuml
state DoorOpen {
    DoorOpen --> DoorOpenWithItem : Place Item Inside
    state DoorOpenWithItem { }
}
DoorShutWithItem --> DoorOpenWithItem : Open Door
ReadytoCook --> DoorOpenWithItem : Open Door
Cooking --> DoorOpenWithItem : Open Door
```

FCSTM：

```fcstm
state DoorOpen {
    state UnspecifiedInitial;
    state DoorOpenWithItem;
    [*] -> DoorOpenWithItem : /Open_Door;
    [*] -> DoorOpenWithItem : /Open_Door;
    [*] -> DoorOpenWithItem : /Open_Door;
    ! * -> DoorOpenWithItem : /Place_Item_Inside;
    [*] -> UnspecifiedInitial;
}
```

三条 source occurrence 全保留，event-specific route 在 fallback 前；没有 `Open_Door` 时模型停在 `UnspecifiedInitial`。审计包含联合篡改负例：即使同时修改 FCSTM 和 trace，把 placeholder 指向真实 child，也会失败。

### 7.2 `0022`：final 恢复为真实终止

```plantuml
PoweredOn --> [*]: keyOff
```

```fcstm
PoweredOn -> [*] : /keyOff;
```

runtime probe 发送 `keyOff` 后 `is_ended=true` 且 stack 为空，不再停在 ordinary `end` leaf。

### 7.3 `0054`：lifecycle 保存，但不夸大执行能力

```plantuml
Accelerating : entry/Accelerate
Approaching : do/Send
EmergencyStopping : do/Emergency Stop
EmergencyStopping : do/Send Obstacle Detected
```

```fcstm
state Accelerating {
    enter abstract Accelerate;
    state LifecycleActive;
    [*] -> LifecycleActive;
}
state EmergencyStopping {
    >> during before abstract EmergencyStop;
    >> during before abstract SendObstacleDetected;
    state LifecycleActive;
    [*] -> LifecycleActive;
}
```

这证明 `4/4` lifecycle source item 有 owner/kind/text/raw span 和 inspect action ID，不证明 abstract action 已有注册行为。

### 7.4 `0058`：fork 与 timing 全保存，但不冒充可执行并发/时间语义

```plantuml
fork fork1
fork1 --> AutoFocus
fork1 --> DetLight
fork1 --> choice3
TurnOn_state : {max=2s, min=2s}
```

```fcstm
pseudo state fork1 named "fork1";
fork1 -> AutoFocus;
fork1 -> DetLight;
fork1 -> choice3;
state TurnOn_state named "TurnOn\n[PlantUML body] {max=2s, min=2s}";
```

三条 fork edge 与 timing body 都没有丢，但 FCSTM pseudo state 不是并发 product state，body 也不是 clock constraint。因此本例 `structural_verdict=structure_preserved`，同时保持 `fcstm_execution_eligible=false`。

## 8. 机器验证与对抗用例

最终 conversion + representation + readiness 套件：`111 passed`。除正常路径外，audit 必须拒绝：

- state parent/path、display body 与 pseudo kind 漂移；
- source/trace endpoint 联合篡改；
- event binding 被换成另一事件；
- untracked extra edge；
- event initial wait 与 main segment 断开；
- composite forced marker 丢失；
- nested final target/hold 被改写；
- cross-scope exit 从 `-> [*]` 改成内部 child；
- fail-closed placeholder 指向真实 child；
- multiple initial declaration order改变；
- transition-specific deep entry 被移动到 default initial 之后；
- source/synthetic state partition 或 mapping cardinality漂移。
- 已含 `MANUAL_REVIEW.md` 的冻结 evidence 目录被 batch runner 覆盖。
- 60 行人工账本中的 source/FCSTM SHA、三轴 verdict 或 FCSTM 集合哈希漂移。

constructed runtime 回归还直接验证：

```plantuml
state C {
    [*] --> Default
    state Default
    state Wanted
}
Outside --> C.Wanted : Go
```

发送 `Go` 后必须到 `C.Wanted`，不能先被 `Default` 抢占。

## 9. 60 组主 session 人工验收

最终制品冻结后，本轮主 session LLM 按 `0000 -> 0059` 读取了每一组完整、带行号的 PlantUML STM0 和完整 FCSTM STM0，并核对 hierarchy、initial/final、全部 transition、body/lifecycle、synthetic state 与 debt。随后又对 19 个高风险 case 做逐 transition macro 第二遍检查。

逐组完整 NL/PlantUML/FCSTM 三元组与原始文件见 [PAIR_INDEX.md](../pipeline/representation/reports/llms_emp_r45_java_60/PAIR_INDEX.md)；绑定 source/FCSTM SHA-256 的人工账本见 [MANUAL_REVIEW.md](../pipeline/representation/reports/llms_emp_r45_java_60/MANUAL_REVIEW.md)。结论为：

- 60 行均为结构 PASS；
- 无 state/transition/body/lifecycle/final 静默漏失；
- 没有任何一行被写成 semantic equivalence；
- `fcstm_execution_eligible=0/60`，`discover_eligible=0/60`。

证据身份：

- 实现提交：`393a1a71c3b959210aa429fbf552ddd0d6e46acc`
- 冻结证据提交：`0de936b2b5ac0c93c67d13314601b5666758f850`
- `tracked_worktree_dirty_before_run=false`
- FCSTM 集合 SHA-256：`591ff856f8a8985b1fcc1682d76193efeaea416be11ae84c64231abf00e17a82`
- pyfcstm：`4ea23c9b153f47e5c4a2125d95b466eee6eed13e`

## 10. 最终判断与后续边界

### 可以确认

1. SCXML 路线不适合继续承担 PlantUML statechart canonical。
2. 旧 converter 确实有重大设计错误，不能把责任全部推给官方工具。
3. Java source frontend + Python subprocess wrapper 是当前更可审计的路线。
4. 当前实现已把 60 例 source facts 结构性保存到 FCSTM + trace，并用 AST audit 与主 session 阅读双重验收。

### 仍不能确认

1. opaque label 的 event/guard/effect/timing 解释。
2. multiple initial 是顺序优先、nondeterminism 还是并发。
3. unlabeled fan-out 的 choice/concurrency 语义。
4. PlantUML fork 在当前单 active-leaf FCSTM runtime 中的行为等价 lowering。
5. abstract lifecycle hook 的具体动作实现。

因此后续有两条合理路线：

- 若 paper1 只需要忠实保存 source artifact，再由 Discover 识别 source ambiguity，则继续使用当前 canonical/trace，但只有 operational debt 闭合后才能进入实验。
- 若实验要求 60 例全部可执行等价，则必须先冻结受支持的 PlantUML label/fork/timing 子语言规范，或扩展 FCSTM 并发/时钟语义；不能再靠字符串猜测。
