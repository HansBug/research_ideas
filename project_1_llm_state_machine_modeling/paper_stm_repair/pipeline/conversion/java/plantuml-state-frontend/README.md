# PlantUML state frontend

该目录是 LLMS-EMP PlantUML `STM_0` 转换的 Java 核心。它同时输出：

1. 两遍、scope-aware 的 source canonical；
2. 固定 PlantUML `1.2024.7` 内部 `StateDiagram -> Entity/Link` 快照。

SCXML 不再作为 PlantUML canonical 真源。Python 侧仅通过 `subprocess` 调用本工具并读取 JSON。

## 为什么不继续消费 SCXML

固定版本 `v1.2024.7` 的官方源码已经给出直接证据：

- [`ScxmlStateDiagramStandard`](https://github.com/plantuml/plantuml/blob/d2b2bcf1722b8705f7f01a556dc96751e7739f7d/src/net/sourceforge/plantuml/xmlsc/ScxmlStateDiagramStandard.java) 用 `entity.getName().replaceAll("\\*", "")` 生成 SCXML ID，没有保留 `Quark` qualified name；不同 scope 的同名 state 会碰撞。
- 同一 exporter 把 start/end circle 都输出成普通 `<state>`，并把整条 link label 写入一个 `event` 属性；它没有导出 final identity、guard/effect 拆分或 state bodier/lifecycle。
- [`StateDiagram`](https://github.com/plantuml/plantuml/blob/d2b2bcf1722b8705f7f01a556dc96751e7739f7d/src/net/sourceforge/plantuml/statediagram/StateDiagram.java) 内部仍保留 parent container、qualified `Quark`、`LeafType.CIRCLE_START/CIRCLE_END` 和 `Link`，明显比 SCXML 丰富。

因此 Java frontend 直接读取 raw source 建立 source span 与两遍 symbol table，同时调用官方 `SourceStringReader -> StateDiagram -> Entity/Link` 生成 differential snapshot。官方内部对象不是稳定公开 AST，也不保留所有 raw span；它只能验证“官方 parser 看到了什么”，不能替代 source canonical。

LLMS-EMP 还包含 `stm X {}`、bare lifecycle、`fork X` 等非官方/伪语法。`OfficialValidationNormalizer` 只生成一份可供官方 parser 差分的临时文本，不参与 canonical 或 FCSTM lowering，所有 normalization 都进入 JSON ledger。

```bash
make fetch
make compile
make run SOURCE=/abs/path/stm0.puml EXAMPLE_ID=llms_emp_stm_results_0000
```

若本机已有 jar：

```bash
make compile PLANTUML_JAR=/abs/path/plantuml-1.2024.7.jar
```

`verify` 会强制检查官方 jar SHA-256。升级 PlantUML 必须显式更新版本、哈希并重跑 60 例 differential contract。

## 输出边界

- transition label 原文完整保留为 opaque event，不猜 guard/effect/timing。
- 带 label 的 initial edge 使用 synthetic wait state，使事件可以跨 cycle 到达，而不要求 composite 在 `init_wait` 中悬空。
- nested final 使用 completion-hold lowering；root final 才真正终止模型。
- 无 initial composite、fan-out/concurrency、opaque state body 和 owner 不明 lifecycle 保留为 reason-coded operational debt，并在执行与 Discover 资格轴失败关闭；只有 source fact 无法进入 `.fcstm + trace` 时才形成 structural blocker。
- `structural_verdict` 只回答 source facts 是否被 FCSTM + trace 完整保存；`operational_status`、`fcstm_execution_eligible` 与 `discover_eligible` 独立裁决。结构通过不代表行为等价或可进入 Discover。
