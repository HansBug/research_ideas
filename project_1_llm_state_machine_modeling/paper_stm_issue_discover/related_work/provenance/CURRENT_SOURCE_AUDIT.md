# 当前四族谓词来源审计

本文件是 `four-family-19-core.v1` 的 active 来源审计入口。机器目录见
[`current_source_catalog.json`](current_source_catalog.json)，注册表见
[`pipeline/evidence_discovery/predicate_registry.json`](../../pipeline/evidence_discovery/predicate_registry.json)。

## 先读结论

当前 19 个 ID 的来源已经可以回到具体文件；但“登记了来源”不等于“严格来源门通过”。
审计把三件事分开：

1. 文件是否存在、是否能回到可复核摘录；
2. 摘录是否真的提出当前谓词命题；
3. 摘录的模型边界是否与当前无时钟、无正交并发的 `M` 一致。

因此本轮结论是：结构族的基础事实、有限图可达的部分命题已经完成部分核验；守卫互斥、
共可达、轨迹行为和死锁等仍有 W1-only 或候选项。不能把 19 个谓词写成“19 条来源门
全部通过”，也不能把台账出场量写成学术证据。

## 状态含义

| 状态 | 含义 |
|---|---|
| `partial_pass` | 文件、摘录和边界已部分核对，只对记录的受限命题负责。 |
| `candidate` | 已找到相关档案，但仍需逐条摘录、独立来源或边界复核。 |
| `w1_only_*` | 当前不能给出 sound W2 证据；问题仍可提出，按 W1 计 `semantic_hit`。 |
| `rejected_for_scope` | 资料与当前模型边界不符，不能作为当前 W2 依据。 |

## 逐谓词审计

| ID | 当前状态 | 审计结论 |
|---|---|---|
| S1 | `partial_pass` | UML/领域资料支持封闭命名元素存在；不扩展到父子归属或基数。 |
| S2 | `partial_pass` | 支持迁移端点存在；不声称运行可行。 |
| S3 | `candidate` | 触发集合等同性需要逐条命题匹配。 |
| S4 | `partial_pass` | 支持动作与生命周期阶段的结构挂接。 |
| S5 | `candidate` | 守卫结构有依据，需求守卫精确等同仍待核。 |
| S6 | `candidate` | 效果挂接有候选依据，变量后值明确排除。 |
| G1 | `partial_pass` | 封闭图有限可达有依据；不等同运行时可行。 |
| G2 | `candidate` | 需要图完备化、终态和全称路径约定。 |
| G3 | `candidate` | 仅支持显式禁止节点/边的路径避免。 |
| G4 | `w1_only_pending_source` | 当前可用资料含并发/超界语义，不能升级 W2。 |
| R1 | `candidate` | 需要封闭场景和实际消费者回执。 |
| R2 | `candidate` | 只对声明轨迹窗口作到达判断。 |
| R3 | `w1_only_no_current_domain_source` | 当前没有足够的命题匹配领域来源。 |
| R4 | `candidate` | 只证明轨迹区间保持，不证明终止。 |
| V1 | `w1_only_pending_independent_rule` | UML 2.5.1 不要求守卫互斥，必须补独立规则来源。 |
| V2 | `candidate` | 守卫覆盖域的定义明确，闭合域证明待核。 |
| V3 | `w1_only_pending_bounded_semantics` | 无界 Response 不能直接替代有界步数 Response。 |
| V4 | `w1_only_parallel_sources_only` | 现有死锁资料依赖并发或超界语义。 |
| V5 | `candidate` | 不变式命题常见，但实例化和闭包条件待核。 |

## 受限准入

`S3` 的谓词级状态仍为 `candidate`，不得因此把一般的需求触发集合等同性升级为 W2。
唯一已审计的候选级例外是 `S3.uml_initial_outgoing_without_trigger.v1`：UML 2.5.1
14.5.6.7 / p.350 的 `Pseudostate::outgoing_from_initial` 明确规定初始顶点的出边不得有
trigger 或 guard。编译器只在一个精确 `[*]` 载体、要求集合为空且解析出的 trigger 集合非空时
使用该准入，并把引用、命题和边界写入计划与回执。它不覆盖 guard-only 缺陷、普通迁移的
trigger 等同性，亦不改变 `S3` 的全局 source gate。

## 三类来源的使用纪律

- `domain` 只说明真实控制系统中有相应检查命题，不能替代形式定义。
- `formal` 说明命题的数学/标准含义，不能自动证明当前后端实现正确。
- `technical` 只限定后端、回执、反例和边界，不能冒充领域普遍性。
- 任何来源若带 timed、parallel、hybrid 或其他超出 `M` 的语义，必须在引用处保留该
  限制；不能截掉限制后当作当前谓词出处。
- 来源审查未闭合的谓词仍可提出问题并输出 W1；W1 是合法 `semantic_hit`，不是失败。

## 维护门

新增或修改来源时，必须同时更新机器目录、人工审计表和注册表测试。没有独立来源、命题
匹配、边界审查、兼容性迁移和回归测试，不得新增谓词或修改定义。覆盖率压力不能绕过
这道门。
