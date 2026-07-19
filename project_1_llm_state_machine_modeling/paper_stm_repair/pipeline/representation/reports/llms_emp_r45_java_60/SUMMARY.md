# LLMS-EMP Phase-II final 60 例 Java PlantUML -> FCSTM R4.5 复验

## 结论

- Java source frontend：`60/60`。
- raw PlantUML 官方直接接受：`59/60`；其余 `1` 条含非官方扩展/伪语法。
- Java official-validation normalization 后 `StateDiagram`：`60/60`。
- pinned PlantUML internal identity oracle：官方 behavior links `757`，source transitions `757`，差值 `+0`；note/presentation attachment 在 identity reconciliation 前过滤。
- source transition：`757`；FCSTM macro 映射 `757`，结构 blocked `0`，静默丢失 `0`。
- final boundary：`35/35`。
- opaque state body：`95/95`；均保存在 FCSTM display metadata 与 trace，不解释为 timing/guard/action。
- lifecycle action：`16/16` 结构保存；state-owned action 以 abstract hook 保留，ownerless action 仅保存在 metadata/trace，二者都不冒充已注册行为。
- PlantUML concurrent region：`29/29`；region separator：`20/20`，仅保留结构与顺序，不声称 FCSTM 已实现正交并发执行。
- 作者 workbook transport normalization：`6/6`；raw source、normalized source、规则与逐行 before/after 均进入 ledger。
- FCSTM parse/inspect：`60/60` / `60/60`。
- pyfcstm AST 独立反查：`60/60`。
- pinned PlantUML qualified identity：states `516/516`；transition endpoints `757/757`；state remap `24`；endpoint remap `37`。
- R4.5 structural preservation：`60/60`；structure blocked：`0/60`。
- FCSTM execution eligible：`0/60`；Discover eligible：`0/60`。

结构通过不等于行为等价。无/多/非法 initial、ownerless lifecycle、opaque state body、无标签 fan-out 与显式 fork 进入 `operational_debts`；转换器保留这些 source facts，但不推断 guard/effect/timing/concurrency。

60 例逐例人工/LLM 对读、官方源码逆向结论与真实 PlantUML/FCSTM 例子见 [Issue #161 技术报告](../../../../reports/2026-07-19-issue-161-plantuml-java-frontend.md)。

## 代表性样例

| case | structural verdict | states | transitions | mapped | blocked | final | lifecycle | raw official | normalized official |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| `0000` | `structure_preserved` | 5 | 6 | 6 | 0 | 0/0 | 0/0 | `state_diagram` | `state_diagram` |
| `0022` | `structure_preserved` | 5 | 10 | 10 | 0 | 1/1 | 0/0 | `state_diagram` | `state_diagram` |
| `0053` | `structure_preserved` | 7 | 4 | 4 | 0 | 0/0 | 0/0 | `state_diagram` | `state_diagram` |
| `0054` | `structure_preserved` | 7 | 8 | 8 | 0 | 0/0 | 4/4 | `state_diagram` | `state_diagram` |
| `0058` | `structure_preserved` | 24 | 22 | 22 | 0 | 1/1 | 0/0 | `not_state_diagram` | `state_diagram` |

## 机器证据入口

- `manifest.json`：版本、哈希、总计与 eligibility 口径。
- `comparison.jsonl`：60 例逐项摘要。
- `canonical/*.json`：Java source canonical + 官方 internal model 快照。
- `fcstm/*.fcstm`：60 个新 FCSTM STM0。
- `case_reports/*.json`：逐迁移 mapping、operational debt、name map 与 AST audit。
- `parse_inspect/*.json`：pyfcstm 结构化 inspect 输出。
