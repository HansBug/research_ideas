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
- 固定版本的 PlantUML `StateDiagram/Entity/Link` 作为 qualified state/transition identity oracle；
- Java raw parser 继续负责 raw span、body/lifecycle、region、normalization 与歧义证据；
- Python 只通过 subprocess 调 Java，再执行 FCSTM lowering 和审计；
- 把结构保存、运行语义和下游 eligibility 拆成三个轴。

最终结果：

| 指标 | 结果 |
|---|---:|
| Java source parse | `60/60` |
| Phase-II final pair pool | `60`（semantic `58` + Phase-I fallback `2`） |
| raw / normalized official StateDiagram | `59/60` / `60/60` |
| source / official identity states | `516/516` |
| source transitions / official endpoints | `757/757` |
| mapped transition macros | `757/757` |
| blocked / silent drop | `0 / 0` |
| state / endpoint identity remap | `24 / 37` |
| final boundary | `35/35` |
| opaque body line | `95/95` |
| lifecycle source item | `16/16` |
| FCSTM parse / inspect | `60/60 / 60/60` |
| independent pyfcstm AST audit | `60/60` |
| structural preservation | `60/60` |
| FCSTM execution eligible | `0/60` |
| legacy whole-model Discover eligible | `0/60` |
| attribution-scoped Discover input | `60/60` |
| source-static capability | `60/60 eligible_with_exclusions` |
| inspect diagnostic capability | `0/60` baseline eligible；逐条归为 `candidate_only` / `insufficient_evidence` / conversion artifact |
| simulation capability | `0/60` baseline eligible（runtime 无稳定 fired-transition ID，无法证明路径未经过 compiler macro） |
| transition-level runtime trace | `0/60`（runtime 无稳定 fired transition ID） |
| baseline Repair / main-result | `0/60`，均为 `not_run`，等待 confirmed issue binding 与真实 loop |

这里的 `60/60` 是 **FCSTM + mandatory working contract/trace bundle 的结构保真**，不是 `60/60 semantic equivalence`。`.fcstm` 单文件不包含 raw span、ownership、macro、capability 和 operational debt，不能脱离 sidecar 单独进入 Discover，也不能宣称可逆。

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

### 2.1 真实 `0054`：state body 与 lifecycle 不进入 SCXML

作者最终有效池中的 `0054` 明确包含四个 lifecycle item：

```plantuml
Accelerating : entry/Accelerate
Approaching : do/Send
EmergencyStopping : do/Emergency Stop
EmergencyStopping : do/Send Obstacle Detected
```

PlantUML SCXML exporter 只遍历 state/link 生成 `<state>` 与 `<transition>`，这四条 `Bodier` 内容没有进入行为输出。旧链路因而无法区分“源中没有 action”和“exporter 已丢 action”。新 frontend 直接从 raw source 提取 owner、kind、action text 与行号，并在 FCSTM 中保留 abstract hook：

```fcstm
state Accelerating {
    enter abstract Accelerate;
}
state EmergencyStopping {
    >> during before abstract EmergencyStop;
    >> during before abstract SendObstacleDetected;
}
```

这不是 XML parser 使用不当；信息在 `StateDiagram -> SCXML` export 前后已经不对称。

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

## 3. 官方内部对象为什么是 identity oracle，但不是完整稳定 AST

逆向 jar 与阅读官方源码后，PlantUML 的 [`StateDiagram`](https://github.com/plantuml/plantuml/blob/d2b2bcf1722b8705f7f01a556dc96751e7739f7d/src/net/sourceforge/plantuml/statediagram/StateDiagram.java) 确实比 SCXML 丰富：它保留 parent container、qualified `Quark`、`LeafType.CIRCLE_START/CIRCLE_END`、concurrent group、`Entity` 和 `Link`。

它是固定版本下回答“PlantUML 实际创建了哪个 entity、link 端点指向谁”的最强证据，因此当前实现以其 qualified identity 为准。但它仍不能单独承担完整 canonical：

- 这是内部实现对象，不是稳定公开 AST/API。
- PlantUML state syntax 没有一份可直接生成 parser 的完整官方形式文法；命令类按行匹配并直接修改 `StateDiagram`。
- 它不保留本研究需要的完整 raw source span 和 source-level ambiguity。
- 解析是顺序执行的，首次引用可能先创建 entity；这种结果必须被保留，而不能由 lexical parser 猜测覆盖。
- 当前 Phase-II final pool 有 `1/60` raw case 因 workbook doubled quote / trailing quote 不能直接成为 `StateDiagram`；6 条 transport normalization 后才达到 `60/60`。

因此“直接读官方源码”得到的正确设计不是反射/序列化全部私有字段，而是：

```text
raw source facts（span/body/lifecycle/region/normalization）
        +
pinned official Entity/Link identity oracle
        -> reconciled canonical（本项目稳定合同）
```

`0047` 是必要性最强的反例：三个 composite 都写了 `Idle/Braking/Clamping`，但 PlantUML `1.2024.7` 把后两组引用复用到 Frontend 首次创建的三个 entity。raw parser 初步得到 9 个状态，official identity 只有 7 个；reconciler 因此执行 2 个 state identity remap 和 6 个 endpoint remap。当前 FCSTM 忠实保留这一官方结果，并把 RearEnd/Pedestrian 的越界 initial 标成 invalid，而不是重新发明三套 lexical-local 状态。

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
- 调用固定 PlantUML `SourceStringReader -> StateDiagram -> Entity/Link`，以 qualified entity/link 身份校准 provisional source identity。
- 过滤 note/presentation attachment link；任何 behavior link/state 无法一一对齐即失败关闭。
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

- event-labeled initial 直接使用 FCSTM 原生带事件 initial edge；禁止再生成 `InitialWait*`，避免 helper 改变初态选择和层次结构。
- root final 直接发出 `X -> [*]`；nested final 使用 `FinalWait*` completion hold。
- leaf cross-scope transition 拆成 child exit、parent continuation、target entry，全部绑定同一 source transition ID。
- transition-specific deep entry 排在普通/default initial 与 `UnspecifiedInitial` 之前；source order和 duplicate occurrence不去重。
- missing initial 使用可见、可停止的 `UnspecifiedInitial`，绝不猜 child。
- invalid/non-direct initial 使用保留 raw target identity 的 surrogate。
- lifecycle 直接挂到原 leaf/composite 的 abstract hook；禁止再生成 `LifecycleActive` 子状态。这只证明结构位置和 action ID，不证明源动作行为已注册执行。
- generic state body 与 ownerless lifecycle 进入 display metadata + trace。
- multiple initial、unlabeled fan-out、explicit fork 的所有边都发出，但 case 保持 execution-ineligible。

## 6. 三轴裁决

旧 `exact / blocked` 一维口径无法区分“source fact 保存了”与“行为可证明”。当前同时保留 legacy whole-model gate 与逐能力合同：

```json
{
  "structural_verdict": "structure_preserved",
  "operational_status": "source_ambiguity_or_unsupported_semantics_preserved",
  "fcstm_execution_eligible": false,
  "discover_eligible": false,
  "working_bundle_usage_gate": "discover_input_with_capability_mask",
  "source_static_discovery": "eligible_with_exclusions",
  "inspect_diagnostics": "ineligible",
  "simulation": "ineligible",
  "transition_trace": "ineligible",
  "repair": "not_run",
  "main_result": "not_run"
}
```

结构 PASS 的必要条件：

- source state ID 与 trace ID Counter 完全相等，source state path 单射；
- output states 恰好等于 source-origin states、allowlisted synthetic states 和 root；
- `757` 个 source transition ID 逐个有非空 macro；
- authored FCSTM transition multiset 与 trace 完全相等，没有 untracked edge；
- AST endpoint、scope、event、forced、final hold 和 entry priority 可反查；
- `95` body、`16` lifecycle、35 final 与 6 条 source normalization 可从 canonical 重建；
- transition declaration order、multiple initial order、fan-out order和 placeholder priority受审计保护。

legacy whole-model 运行/Discover eligibility 仍另行判断。当前所有 60 例至少含一个 opaque transition label 或其他 debt，因此严格 whole-model 结果仍是 `0/60`。但这不再意味着整例只能废弃：`working_fcstm_contract.v2` 将 source-owned semantic roots、compiler-owned members 和 source-input normalization 分开，允许全部 60 例进入 source-static Discover；baseline inspect diagnostic、simulation、transition trace、Repair 和 main-result 一律 fail closed，不能仅因 parse/inspect 成功而获得 source-level 证据资格。

后续 #158 可以消费 60/60 working bundle，但必须遵守：

1. `FinalWait*`、`UnspecifiedInitial`、`InvalidInitial*`、`R45RouteToken` 和跨层 transition segments 均为 compiler-owned/protected；`InitialWait*` 与 `LifecycleActive` 被明确禁止；
2. compiler-only diagnostic 必须归为 `rejected_conversion_artifact`，不能成为 confirmed issue 或 Repair target；
3. macro member diagnostic 在有 NL/raw source/typed evidence 前只能 `candidate_only`；
4. source identity trace 只证明“FCSTM 逻辑 root 对应哪个 PlantUML source element”，所有 baseline entry 均 `behavioral_fidelity=not_assessed`、`closure_claim_allowed=false`；
5. source-input normalization 单独进入 `conversion_boundary`，不能混入 positive source trace；
6. confirmed issue 必须同时有 NL 或 raw-internal evidence、raw source fragment、positive source identity trace、capability-eligible typed evidence，并明确 `conversion_or_lowering_related=false`；
7. main-result conversion artifact 上限固定为 `0`。Discover candidates 可以暴露 conversion artifact，但必须在 Repair 前 fail closed。

这些规则不能只靠调用方自觉。正式 consumer 必须调用 `load_attribution_safe_working_bundle(evidence_dir, case_id)`，由 loader 重验 clean manifest、artifact inventory/hash、working contract、source trace、case report 与原始 pair，再通过 `discover_view()` 取得字段级 capability allowlist。裸 `.fcstm` 只能用于 parse/audit，不是合法 Discover 输入。source issue ledger 只有在 source refs 全部属于 positive-traced source-owned roots、typed evidence 对应 capability eligible 且 conversion boundary 为 false 时才形成 binding；本 PR baseline 的 binding 仍为 `repair_authorized=false`，因为 Repair patcher、Confirm adapter 与 final exporter 不在本 leaf PR 中实现。

## 7. 真实修复例子

### 7.1 `0005`：官方 first-created identity 不再被 lexical intuition 覆盖

PlantUML：

```plantuml
state DoorOpenWithItem {
    DoorIdleWithItem --> DoorShutWithItem : Close Door with Zero Time
    DoorIdleWithItem --> ReadytoCook : Enter Cooking Time
}
state DoorShutWithItem { ... }
state ReadytoCook { ... }
state Cooking { ... }
```

FCSTM：

```fcstm
state DoorOpenWithItem {
    state DoorShutWithItem { ... }
    state ReadytoCook {
        state Cooking { ... }
    }
    state DoorIdleWithItem;
}
```

后置 block 在视觉上像 root sibling，但官方 parser 已由前置 link 创建 nested entity；当前 state/transition ledger 记录所有 remap，19 条 source transition occurrence 全保留。转换器不再把自己更“直观”的 lexical 解释冒充 PlantUML 官方语义。

### 7.2 `0022`：final 恢复为真实终止

```plantuml
Operate --> [*] : keyOff
```

```fcstm
!Operate -> [*] : /keyOff;
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
}
state EmergencyStopping {
    >> during before abstract EmergencyStop;
    >> during before abstract SendObstacleDetected;
}
```

这证明 `4/4` lifecycle source item 有 owner/kind/text/raw span 和 inspect action ID，不证明 abstract action 已有注册行为。

### 7.4 `0058`：fork 与 timing 全保存，但不冒充可执行并发/时间语义

```plantuml
state fork1 <<fork>>
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

最终计数以 clean replay 后的全套测试输出为准。除正常路径外，audit 必须拒绝：

- state parent/path、display body 与 pseudo kind 漂移；
- source/trace endpoint 联合篡改；
- event binding 被换成另一事件；
- untracked extra edge；
- event-labeled initial 被错误拆成 helper state，或与原 initial source root 失去绑定；
- composite forced marker 丢失；
- nested final target/hold 被改写；
- cross-scope exit 从 `-> [*]` 改成内部 child；
- fail-closed placeholder 指向真实 child；
- multiple initial declaration order改变；
- transition-specific deep entry 被移动到 default initial 之后；
- source/synthetic state partition 或 mapping cardinality漂移。
- 已含 `MANUAL_REVIEW.md` 的冻结 evidence 目录被 batch runner 覆盖。
- 60 行人工账本中的 source/FCSTM SHA、三轴 verdict 或 FCSTM 集合哈希漂移。
- field ownership、positive-trace coverage、macro source binding 或 inventory digest 的自洽联合篡改。
- capability field allowlist 漂移，以及 Repair/Confirm/final-export/main-result 的提前准入。
- development-only evidence、裸 `.fcstm` consumer、compiler-owned confirmed/Repair target 和 attribution-ineligible typed evidence。
- 重复 semantic correspondence、`capability_excluded + preserved` 矛盾裁决、risk occurrence 绑定错误元素。

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

旧 v3 人工账本已因 working-contract、实现指纹和 review subject 更新而失效，不能继承。正式 v6 batch 制品（逐例 case report schema 为 v5）只能在实现提交后的 clean replay 生成；随后由主 session LLM 按 `0000 -> 0059` 重新完整读取 NL、PlantUML STM0、FCSTM STM0、working contract 与 source trace，并对每个 risk occurrence 按唯一 `obligation_id` 完成绑定同一 subject 的第二遍复核，不能用一条 risk-tag 总结覆盖多个 occurrence。

最终逐组三元组、人工账本、publication seal 和证据身份只能在 clean replay 与 60/60 主 session 重读完成后由本 PR 的 evidence commit 更新。开发 replay 即使机器 gate 全过，也必须显示 `development_only`，不得成为 READY 证据。

当前已在 clean detached worktree 完成绑定实现提交的 machine replay，得到 `60/60 structure_preserved`、`757/757` mapped transition、`0` silent drop、`1413` positive identity trace、`903` macro、`114` 个 protected route mapping 与 `0` sequential event replay debt。主 session 随后完成当前 review subject 下的 `60/60` 三元组重读、`120` 条独立语义对应和 `460` 个逐 occurrence obligation 复核，结果为 `60/60 pass`、`0` findings。新 [MANUAL_REVIEW.jsonl](../pipeline/representation/reports/llms_emp_r45_java_60/MANUAL_REVIEW.jsonl)、[PAIR_INDEX.md](../pipeline/representation/reports/llms_emp_r45_java_60/PAIR_INDEX.md) 与 [PUBLICATION_SEAL.json](../pipeline/representation/reports/llms_emp_r45_java_60/PUBLICATION_SEAL.json) 已绑定当前 manifest、working-contract set 与逐文件 hash；seal 状态为 `main_session_reviewed_ready_for_discover`、`evidence_eligible=true`。

## 10. 最终判断与后续边界

### 可以确认

1. SCXML 路线不适合继续承担 PlantUML statechart canonical。
2. 旧 converter 确实有重大设计错误，不能把责任全部推给官方工具。
3. Java source frontend + Python subprocess wrapper 是当前更可审计的路线。
4. pinned official `Entity/Link` 身份与 raw-source ledger 已共同进入 canonical；当前 v6 batch clean replay（v5 case report）、60 例主 session 重读与 publication seal 均已完成。旧账本 PASS 没有被继承，新 seal 只绑定当前实现和当前 review subject。

### 仍不能确认

1. opaque label 的 event/guard/effect/timing 解释。
2. multiple initial 是顺序优先、nondeterminism 还是并发。
3. unlabeled fan-out 的 choice/concurrency 语义。
4. PlantUML fork 在当前单 active-leaf FCSTM runtime 中的行为等价 lowering。
5. abstract lifecycle hook 的具体动作实现。

因此 paper1 采用非对称双投影合同，而不再追求通用双向无损：

```text
PlantUML STM0 -> attribution-safe FCSTM working bundle
validated post-Confirm semantic-root export bundle -> fresh canonical PlantUML STM_k
```

前向阶段允许 Discover 暴露 conversion candidate noise，但 `confirmed`、Repair target、Confirm accepted disposition 与 main-result issue 中的 conversion artifact 上限均为 `0`。operational debt 不再全局阻断 source-static Discover；它只关闭受影响的 inspect/simulation/transition/verification capability。后向阶段必须由未来独立的 post-Confirm semantic-root export bundle 生成完整、确定性的 PlantUML，不保留原 formatting 或最小 diff；compiler-owned scaffold 全部折叠，只导出 source-owned 与 issue-bound agent-created semantic roots。裸 `.fcstm` 和当前 baseline working bundle 都不能授权该操作。**该 post-Confirm contract 与 final exporter 当前尚未实现，capability 必须保持 `not_run`。**后续实现后仍必须重新经 pinned PlantUML frontend 解析并做 semantic-root audit，但这只是 final export 验证，不构成 `T_out(T_in(P)) = P` 的 round-trip 主张。
