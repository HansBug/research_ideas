# LLMS-EMP 60 例 Java PlantUML -> FCSTM R4.5 复验

## 结论

- Java source frontend：`60/60`。
- raw PlantUML 官方直接接受：`33/60`；其余 `27` 条含非官方扩展/伪语法。
- Java official-validation normalization 后 `StateDiagram`：`60/60`。
- 官方 internal model links：`755`；source transitions：`754`。唯一 `+1` 来自 `0019` 的 note attachment，不是行为迁移。
- source transition：`754`；映射 `719`，显式 blocked `35`，静默丢失 `0`。
- final boundary：`36/36`。
- lifecycle action：state-owned `18/18`；另有 `1` 条 root-level owner ambiguity 被显式阻塞。
- FCSTM parse/inspect：`60/60` / `60/60`。
- R4.5 exact：`19/60`；blocked_unsupported：`41/60`。

`blocked_unsupported` 不表示 converter 静默失败。它表示 raw source 存在无/多 initial composite、无 owner lifecycle、opaque state body、无标签 fan-out、显式 fork，或无法合法进入 lexical scope 的 transition。所有项都保留 source span 与 reason code，禁止进入 Discover eligibility。

60 例逐例人工/LLM 对读、官方源码逆向结论与真实 PlantUML/FCSTM 例子见 [Issue #161 技术报告](../../../../reports/2026-07-19-issue-161-plantuml-java-frontend.md)。

## 代表性样例

| case | verdict | states | transitions | mapped | blocked | final | lifecycle | raw official | normalized official |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| `0000` | `blocked_unsupported` | 6 | 7 | 7 | 0 | 0/0 | 0/0 | `state_diagram` | `state_diagram` |
| `0022` | `exact_r45_structure` | 5 | 9 | 9 | 0 | 1/1 | 0/0 | `not_state_diagram` | `state_diagram` |
| `0053` | `blocked_unsupported` | 4 | 6 | 6 | 0 | 0/0 | 0/0 | `state_diagram` | `state_diagram` |
| `0054` | `exact_r45_structure` | 7 | 8 | 8 | 0 | 0/0 | 4/4 | `state_diagram` | `state_diagram` |
| `0058` | `blocked_unsupported` | 25 | 22 | 17 | 5 | 1/1 | 0/0 | `not_state_diagram` | `state_diagram` |

## 机器证据入口

- `manifest.json`：版本、哈希、总计与 eligibility 口径。
- `comparison.jsonl`：60 例逐项摘要。
- `canonical/*.json`：Java source canonical + 官方 internal model 快照。
- `fcstm/*.fcstm`：60 个新 FCSTM STM0。
- `case_reports/*.json`：逐迁移 mapping、blocker、name map 与 parse/inspect 指标。
- `parse_inspect/*.json`：pyfcstm 结构化 inspect 输出。
