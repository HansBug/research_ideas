# E2 微观决策画像：四个模型的可观测问题生成轨迹

> **材料性质**：E2 的派生审计报告，服务于导师讨论、论文结果解释和后续实验设计。报告描述模型在冻结任务协议下可观测的输出决策，不把 `reason`/`basis` 当作隐藏思维链，也不建立独立于 E2 裁定归档的结果口径。
>
> **核验日期**：2026-09-09。所有数值由本地微观审计 JSON 生成；该 JSON 不随本提交进入仓库，生成脚本为 [2026-09-09-e2-micro-decision-profiles.py](./2026-09-09-e2-micro-decision-profiles.py)。JSON 大小为 65,614,214 bytes，SHA-256 为 `69bb8cfae27204d384ea7cae05be333a327aa97cb9d26abfd1a456a2753f1bef`，供本地核验。

## 1. 研究问题

宏观的 hit、precision 和报告数量回答了“方法带来了多少变化”，但不能说明模型在候选生成、证据绑定、问题筛选和多轮重复之间如何作出不同选择。本报告回答三个描述性问题：

1. 四个模型更常从哪些状态机属性和问题方向提出候选？
2. 它们在 `reason`、`basis`、来源引用和可执行证据上的可观测承诺有何差异？
3. 同一输入重复运行时，哪些模型保持相同候选，哪些模型更常加入或删除候选？

核心结论是：模型差异表现为决策环节的组合，而不是一条“强弱”轴。Luna 更集中在迁移端点和目标错误，Sonnet 的候选属性更分散且对确定性事实依赖更明显，Qwen 扩大状态动作/效果类候选入口，Muse 在迁移、层级和动作之间保持较高重复稳定性。三款新增 backbone 的这些差异与 E2 宏观结果相互补充，但不能替代语义裁定。

## 2. 数据范围和可信边界

### 2.1 覆盖范围

机器归档包含四个模型、两条 arm、54 个输入 pair、3 个 round，共 1,296 个唯一 cell：

| 模型 | ours | baseline | 运行性质 | predicate 配置 |
| --- | ---: | ---: | --- | --- |
| GPT-5.6 Luna | 162 | 162 | v61 历史只读复用 | 19 条历史配置 |
| Claude Sonnet 5 | 162 | 162 | E2 新生成 | 12 条配置 |
| Qwen3.8-27B | 162 | 162 | E2 新生成，当前 serving 为 low | 12 条配置 |
| Muse Glimmer-30B | 162 | 162 | E2 新生成，当前 serving 为 high | 12 条配置 |
| **合计** | **648** | **648** |  |  |

Luna 的 `ours` 原始 method 记录来自 `v61_source_divergence_vs_x1v2_baseline`，baseline 来自 v60 的 X1v2 原始记录；三款新增模型的两条 arm 来自 `e2_20260907/raw/`。因此 Luna 只提供历史行为锚点，不属于本轮三款 backbone 的新增生成量。Luna 与其他模型的跨模型数值比较还受到 predicate 数量、运行日期、provider 路由和 serving 档位差异限制。

### 2.2 分母和字段边界

- **raw issue candidate**：`model_output.issues` 中模型直接提出的候选。全量为 Luna 778、Sonnet 754、Qwen 948、Muse 954。它是微观候选分母，不是去重后的缺陷数，也不等于最终发布报告数。
- **evidence record**：方法展开后的证据记录，可能由一个候选产生多个记录。它单独保留在 JSON 中，不能与 raw candidate 相加。
- **`reason`/`basis`**：候选模型实际输出的可见字段。它们反映输出中的解释和证据指向，不代表隐藏 chain-of-thought、内部 token 概率或未输出的思考过程。
- **D 决策**：`d_adjudication` 的 dossier 级记录。一个候选可能对应多个 obligation dossier，所以 `defeated/survives/unresolved` 的计数不能除以 raw candidate 数解释为候选比例。
- **baseline**：Luna X1v2 与三款 E2 baseline 只提供自由文本 issue（以及 Luna X1v2 的 `reason`）。没有与 ours 对齐的 typed `basis`、predicate、evidence 或阶段输出，因此 baseline 的微观对照只比较报告数量、`reason` 是否存在及其长度，不把缺失字段当作零。
- **judge**：所有 E2 语义裁定均由 Luna 完成。judge 的 `reason`/`basis` 不进入候选模型画像；Luna 的历史 judge 仅作为只读裁定快照附在 cell 上。

## 3. 微观画像框架

本报告不把多个维度压成总分，而是把模型行为拆成四个阶段。定义中的“候选”都以 `(property, locus_names, violation_direction)` 规范化键作为集合比较键；它是透明的字段键，不代表语义去重后的独立缺陷。本报告的候选广度记为 `B_c`，以区别于综合结果报告中“发布报告数 / cell”的宏观报告广度 `B_r`。

| 阶段 | 指标 | 计算 | 解释 |
| --- | --- | --- | --- |
| 探索 | 候选广度 `B_c` | raw candidates / 162 cells | 模型提出多少可定位候选 |
| 探索 | 属性/方向分布 | property、violation direction 的计数与占比 | 候选集中在哪类状态机后果 |
| 绑定 | source/locus/predicate rate | 有 `source_refs`、`locus_names`、`predicate_id` 的候选 / raw candidates | 输出是否把主张落到可定位对象或谓词 |
| 绑定 | evidence mix | `evidence_types` 的计数 | 采用来源、模型库存、迁移、可达性、执行等哪类依据 |
| 探索/绑定 | 分布熵 `H_property`、`H_direction`、`H_evidence` | 归一化 Shannon entropy | 候选属性、违反方向和证据类型是集中还是分散 |
| 选择 | `reason`/`basis` surface | 字符数、词项出现率 | 可见解释的长度和指向；不解释隐藏推理 |
| 选择 | D disposition | dossier 的 `defeated/survives/unresolved` | 后续反证处理轨迹；分母是 dossier，不是候选 |
| 重复 | pairwise Jaccard | 同 pair、同 round 的候选键集合交并比 | 两个模型对同一输入提出相同候选的程度 |
| 重复 | retained/added/dropped | 相邻 round 候选键的保留、加入、删除数 | 重复运行中候选集合如何变化 |

`B_c`、属性/方向分布、熵和解释字段描述“模型说了什么”；D、Jaccard 和 round transition 描述“候选在方法链中如何被处理”。E2 的 `K/N/I_rep`、strict precision 和 hit 仍以冻结 judge 归档为准。

### 3.1 公式、分母与统计程序

设模型 `m` 的 cell 数为 `C_m=162`，raw candidate 总数为 `C_raw,m`。候选级指标按 `C_raw,m` 作分母，cell 级指标按 `C_m` 作分母；D 阶段另有 dossier 分母。对任意候选字段 `f`（`source_refs`、`locus_names` 或 `predicate_id`），绑定率为：

```text
B_c(m) = C_raw,m / C_m
R_f(m) = #{candidate: f is present} / C_raw,m
R_term(m) = #{candidate: fixed term appears in reason/basis/strongest_rebuttal} / C_raw,m
L_f(m) = sum(length of non-null f text) / #{non-null f text}
```

`B_c` 反映每个 cell 的候选入口宽度；`R_f` 反映主张是否落到可定位对象或谓词；`R_term` 是固定词表的透明表面筛查，不是语义分类器；`L_f` 是字符长度均值，不是 token 数、延迟或推理成本。source/evidence 的计数还保留原始分子，因为一个候选可以包含多个 evidence type，不能把各类型计数相加后当成候选数。

对某个分布（属性、违反方向或证据类型），设第 `i` 类计数为 `n_i`，总数为 `N=Σ_i n_i`，只保留 `n_i>0` 的 `k` 个观测类别，`p_i=n_i/N`。报告使用归一化 Shannon entropy：

```text
H = -Σ_i p_i log2(p_i)
H_norm = H / log2(k),       0 <= H_norm <= 1
```

当 `N=0` 或 `k<=1` 时定义 `H_norm=0`。`H_norm` 越接近 0，表示该模型的候选集中在少数已出现类别；越接近 1，表示在已出现类别间更均匀。这里的归一化只在“已出现类别”内部进行，零计数类别不进入 `k`，因此熵必须与原始 counts 和支持集大小一起阅读，不能单独当作多样性总分。`H_property`、`H_direction` 和 `H_evidence` 分别在三种计数上计算。

`d_adjudication` 的三类 disposition 使用 dossier 作为分母：`q_d = count(disposition=d) / total dossiers`；一个候选可能展开为多个 dossier，所以不把 `q_d` 写成候选通过率。相似输入的候选集合记为 `A`、`B`，Jaccard 为：

```text
J(A,B) = |A ∩ B| / |A ∪ B|
```

其中集合元素是 `(property, locus_names, violation_direction)` 键；两集合都为空时约定为 1。相邻 round 的集合 `A_t`、`A_{t+1}` 则分别计算 `retained=|A_t∩A_{t+1}|`、`added=|A_{t+1}\A_t|`、`dropped=|A_t\A_{t+1}|`。这些量描述重复运行的重组，不代表正确性。

微观部分是对 162 个 cell 的全量描述统计：每个模型报告 counts、均值、中位数、范围和逐 cell 原件，不把 cell 或候选当作相互独立的总体样本，也不对 entropy/Jaccard 另报显著性。宏观 E2 的配对差值另按自然语言簇做描述性 cluster bootstrap：每次从 9 个簇有放回抽取 9 个簇，保留簇内全部 pair、round 和两条 arm，重复 10,000 次（`seed=20260907`），用重采样差值的 2.5% 和 97.5% 分位数形成区间。该区间反映结果对簇组成的敏感性，不把 972 个 cell 当作独立重复。

宏观结果与微观画像通过以下接口连接。对发布报告的冻结裁定，`K` 是 `VALID_KNOWN`，`N` 是有效但台账外的报告，`I_rep` 是 `INVALID`：

```text
P   = (K + N) / (K + N + I_rep)
P_s = #{validity != INVALID and d_tier in {D1, D2}} / (K + N + I_rep)
G   = P - P_s
hit@1   = #{expected-round with FULL VALID_KNOWN support} / 435
hit@3   = #{ledger item hit in at least one of 3 rounds} / 145
hit@all = #{ledger item hit in all 3 rounds} / 145
S       = hit@all / hit@3
E       = #{ours reports with W2 receipt} / #{ours reports}
ΔX      = X_ours - X_baseline
```

`P` 反映发布报告的普通有效性，`P_s` 把通过的报告进一步限制到 D1/D2 严格等级，`G` 反映普通有效性与严格等级之间的差距；`hit@1`、`hit@3`、`hit@all` 反映台账覆盖，`S` 反映已经命中的条目能否跨三轮保持，`E` 反映可执行证据回执的承诺。`ΔX` 只在同一模型的 paired baseline/ours 内解释。上述宏观指标来自冻结 Luna judge 与 expected 集合，本报告不以 raw candidate 重新计算或替换它们。

## 4. 全量微观统计

### 4.1 候选广度、可定位率和分布熵

| 模型 | raw candidates | `B_c` 每 cell | `reason` 均长 | `basis` 均长 | source ref | predicate bound | locus named | `H_property` | `H_direction` | `H_evidence` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Luna | 778 | 4.8025 | 248.61 | 184.12 | 92.0% | 30.2% | 100.0% | 0.7835 | 0.8130 | 0.8049 |
| Sonnet 5 | 754 | 4.6543 | 345.08 | 290.96 | 39.8% | 39.8% | 100.0% | 0.8338 | 0.8062 | 0.8037 |
| Qwen3.8-27B | 948 | 5.8519 | 351.61 | 319.97 | 82.1% | 35.1% | 100.0% | 0.8203 | 0.4972 | 0.7775 |
| Muse Glimmer-30B | 954 | 5.8889 | 173.26 | 213.92 | 97.4% | 36.7% | 100.0% | 0.7564 | 0.6146 | 0.8000 |

`reason`/`basis` 均值是候选级字符数；它们不是 token 数，也不表示推理成本。Muse 的候选解释更短，Luna 的 source ref 率较高。Sonnet 的 source ref present 为 39.8%，但 `deterministic` 词项出现在 97.9% 的候选中；这表明“提到确定性检查”和“填写结构化 source_refs”是两个不同的表面行为。上述统计不能直接判定解释质量。

熵的组合给出一个不同于候选数量的视角：Sonnet 的属性熵最高（0.8338），说明其候选在已出现的属性类别间最分散；Luna 的方向熵最高（0.8130），而 Qwen 的方向熵最低（0.4972），后者与 `missing` 占 68.2% 相符，表示方向选择更集中；Muse 的属性熵最低（0.7564），与其迁移/动作/层级三类主导属性相符。四个模型的 evidence entropy 接近（0.7775--0.8049），所以不能据此宣称证据“更丰富”或“更好”；熵只描述分布形状，原始计数和绑定率仍是必要上下文。

### 4.2 属性分布

下表覆盖 JSON 中出现的全部属性键。空白表示该模型在 1,296 个 cell 的 raw candidate 中没有该属性。

| property | Luna | Sonnet | Qwen | Muse |
| --- | ---: | ---: | ---: | ---: |
| `initial_entry` | 163 | 163 | 134 | 151 |
| `transition_endpoints` | 190 | 129 | 114 | 259 |
| `state_action` | 99 | 57 | 202 | 164 |
| `termination` | 54 | 37 | 42 | 49 |
| `effect` | 47 | 45 | 143 | 88 |
| `reachability` | 34 | 62 | 73 | 2 |
| `event_consumer_coverage` | 34 | 71 | 66 | 36 |
| `containment` | 25 | 31 | 57 | 91 |
| `trigger_set` | 24 | 15 | 31 | 9 |
| `variable_delta` | 14 | 23 | 31 | 11 |
| `region_structure` | 14 | 11 | 14 | 12 |
| `guard` | 14 | 24 | 17 | 24 |
| `deadlock_freedom` | 11 | 13 | 5 | 0 |
| `state_retention` | 11 | 7 | 4 | 12 |
| `cardinality` | 10 | 2 | 1 | 17 |
| `element_declaration` | 7 | 4 | 5 | 14 |
| `event_consumption` | 4 | 6 | 0 | 13 |
| `guard_disjointness` | 3 | 52 | 9 | 1 |
| `behavior_occurrence` | 9 | 0 | 0 | 1 |
| `excess_behavior` | 0 | 2 | 0 | 0 |
| `other` | 7 | 0 | 0 | 0 |
| `state_after_stimulus` | 4 | 0 | 0 | 0 |

占比最高的属性组合给出四个清晰方向：Luna 的 `transition_endpoints`（24.4%）和 `initial_entry`（21.0%）；Sonnet 的 `initial_entry`（21.6%）、`transition_endpoints`（17.1%）和 `event_consumer_coverage`（9.4%）；Qwen 的 `state_action`（21.3%）和 `effect`（15.1%）；Muse 的 `transition_endpoints`（27.1%）、`state_action`（17.2%）和 `containment`（9.5%）。

### 4.3 违反方向分布

| violation direction | Luna | Sonnet | Qwen | Muse |
| --- | ---: | ---: | ---: | ---: |
| `missing` | 72 | 223 | 647 | 537 |
| `wrong_target` | 280 | 121 | 15 | 127 |
| `wrong_effect` | 101 | 75 | 61 | 98 |
| `wrong_scope` | 70 | 3 | 6 | 21 |
| `not_completed` | 57 | 37 | 42 | 49 |
| `unreachable` | 49 | 82 | 79 | 3 |
| `unconsumed` | 27 | 70 | 59 | 49 |
| `mismatched` | 33 | 16 | 21 | 23 |
| `wrong_guard` | 19 | 57 | 8 | 24 |
| `dead_end` | 18 | 16 | 5 | 2 |
| `not_retained` | 11 | 24 | 4 | 12 |
| `other` | 40 | 27 | 1 | 0 |
| `unsupported_expression` | 1 | 1 | 0 | 9 |
| `extra` | 0 | 2 | 0 | 0 |

Qwen 的 `missing` 占其候选的 68.2%，高于 Muse 的 56.3% 和 Sonnet 的 29.6%；Luna 则以 `wrong_target` 为主（36.0%）。Sonnet 的 `wrong_guard`、`unreachable` 和 `unconsumed` 比例较高，Muse 的 `wrong_target`、`wrong_effect` 和 `not_completed` 较集中。方向分布说明模型对同一类输入可能选择不同的错误表述粒度，不能把不同方向直接相加成“发现数”。

### 4.4 证据类型和解释词项

| 指标（候选级） | Luna | Sonnet | Qwen | Muse |
| --- | ---: | ---: | ---: | ---: |
| `natural_language` hint | 747 (96.0%) | 660 (87.5%) | 922 (97.3%) | 889 (93.2%) |
| `author_source` hint | 655 (84.2%) | 422 (56.0%) | 646 (68.1%) | 568 (59.5%) |
| `deterministic` hint | 376 (48.3%) | 738 (97.9%) | 759 (80.1%) | 847 (88.8%) |
| `execution` hint | 48 (6.2%) | 397 (52.7%) | 324 (34.2%) | 251 (26.3%) |
| `alternative_reading` hint | 0 | 165 (21.9%) | 121 (12.8%) | 1 (0.1%) |
| source identity evidence | 667 | 44 | 211 | 485 |
| closed model inventory | 364 | 532 | 730 | 574 |
| transition fact | 416 | 330 | 411 | 376 |
| reachability fact | 221 | 269 | 239 | 122 |
| action/effect evidence | 163 | 128 | 393 | 269 |

词项指标是透明的 term-presence triage，不是语义分类器。它们用于定位样本和提出假设：Sonnet 更常在 `reason/basis` 中显式提到确定性检查、执行和 alternative reading；Qwen、Muse 也大量提到 closed inventory；Luna 的候选输出更常保留 author-source 和 semantic comparison。完整 evidence type 计数、词项规则和每条候选文本都在 JSON 中保留。

### 4.5 D 阶段、调用阶段和修订

| 模型 | D defeated | D survives | D unresolved | contract extraction | contract completion | grounding | D adjudication | D correction |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Luna | 1,629 | 147 | 69 | 162 | 161 | 324 | 160 | 18 |
| Sonnet 5 | 1,330 | 427 | 137 | 162 | 162 | 324 | 162 | 133 |
| Qwen3.8-27B | 1,715 | 369 | 6 | 162 | 162 | 324 | 165 | 104 |
| Muse Glimmer-30B | 1,594 | 184 | 15 | 162 | 162 | 324 | 150 | 7 |

这里的 D 计数是 dossier 决策记录；Sonnet 的 correction 次数最多，和其较多的结构性诊断修订相符；Muse 的 correction 较少。该表不能单独推出“修订越多越差”，因为 dossier 数量和候选展开也不同。各阶段的 provider status、attempt、usage 和 finish reason 仍在每个 cell 的 `calls` 中逐调用保存。

### 4.6 同一输入的模型间一致性

Jaccard 使用同一 pair、同一 round 的 `(property, locus, direction)` 集合。它衡量候选集合重合，不衡量语义正确性。

| 模型对 | cell 数 | 平均 Jaccard | 中位数 | 范围 |
| --- | ---: | ---: | ---: | ---: |
| Luna–Sonnet | 162 | 0.0613 | 0.0000 | 0.0000–1.0000 |
| Luna–Qwen | 162 | 0.0307 | 0.0000 | 0.0000–1.0000 |
| Luna–Muse | 162 | 0.0493 | 0.0000 | 0.0000–1.0000 |
| Sonnet–Qwen | 162 | 0.0848 | 0.0000 | 0.0000–1.0000 |
| Sonnet–Muse | 162 | 0.0781 | 0.0000 | 0.0000–1.0000 |
| Qwen–Muse | 162 | 0.2704 | 0.1429 | 0.0000–1.0000 |

Qwen–Muse 的候选重合最高，但中位数仍只有 0.1429；这表明它们在若干输入上共享状态动作、效果或缺失类候选，整体仍保留明显的模型特异性。Luna 与其他模型的低重合受历史 predicate/运行配置差异影响，不能解释为能力差距。

### 4.7 重复 round 的候选变动

下表是每个模型在 108 个相邻 round pair 上的平均保留、加入和删除数；它们是候选集合的变化量。

| 模型 | 平均 retained | 平均 added | 平均 dropped | round 1→2 Jaccard（pair 均值/中位数） |
| --- | ---: | ---: | ---: | ---: |
| Luna | 0.889 | 2.824 | 2.963 | 0.170 / 0.000 |
| Sonnet 5 | 0.796 | 3.120 | 2.972 | 0.123 / 0.111 |
| Qwen3.8-27B | 1.954 | 2.250 | 2.463 | 0.429 / 0.270 |
| Muse Glimmer-30B | 2.028 | 1.870 | 2.083 | 0.462 / 0.400 |

Muse 和 Qwen 的重复候选保留更多，Muse 的新增/删除量最低；这与其在宏观结果中的较高 `round stability` 相容。Luna、Sonnet 的重复集合更易重组，说明它们的 coverage 不能只靠单轮候选数解释。

### 4.8 baseline 的有限表面对照

baseline 没有 ours 的 typed 字段，因此这里只列报告数量和自由文本 `reason`，不把数量差异解释为语义候选覆盖差异。

| 模型 | ours raw candidates | baseline issues | baseline 每 cell | baseline `reason` 均长（字符） | baseline `reason` 覆盖 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Luna（历史） | 778 | 512 | 3.1605 | 129.39 | 512/512 |
| Sonnet 5 | 754 | 715 | 4.4136 | 375.87 | 715/715 |
| Qwen3.8-27B | 948 | 455 | 2.8086 | 325.93 | 455/455 |
| Muse Glimmer-30B | 954 | 681 | 4.2037 | 301.10 | 681/681 |

这张表只说明两条 arm 的可见输出规模和文本长度。baseline 的自由文本没有 `property`、`violation_direction`、`basis` 或执行证据，不能据此计算与 ours 同口径的属性分布、证据绑定率或 D disposition。

## 5. 相似输入的人工抽样核对

为检查聚合统计是否对应真实输出，先前抽取了 pair `0002`、`0019`、`0029`、`0049` 的 round-1 结果，逐条阅读四模型的 `title/reason/basis`。这些 pair 是事先用于探索的固定样本，不据此挑选模型或结果；全量结论仍以 JSON 为准。

| pair | Luna | Sonnet 5 | Qwen3.8-27B | Muse Glimmer-30B |
| --- | --- | --- | --- | --- |
| `0002` PumpControl | 12 条；初始入口、动作、端点并列出现，常用 closed inventory 与有限初始事实 | 7 条；集中 PumpControl 初始入口、端点和可达性，`wrong_target` 较多 | 8 条；6 条 `missing`，围绕初始入口、PumpState 动作和事件消费 | 11 条；全为 `missing`，同时列出初始入口、端点和动作义务 |
| `0019` Autonomous/Collision | 8 条；初始入口、可达性、事件消费和终止并列 | 5 条；守卫互斥、不可达和事件消费较突出 | 5 条；4 条初始入口、1 条可达性 | 8 条；6 条初始入口、2 条终止 |
| `0029` Highway/Urban | 18 条；7 条层级范围，另有初始入口、事件消费和终止 | 8 条；守卫互斥、可达性和终止 | 21 条；包含、初始入口、守卫互斥和终止，候选最多 | 8 条；包含、初始入口和终止，候选较少 |
| `0049` FinishState | 7 条；初始入口、层级范围、事件消费、端点和终止 | 8 条；4 条终止，另有事件消费与可达性 | 8 条；端点和终止各 4 条 | 8 条；端点和终止各 4 条 |

抽样文本呈现出与全量属性表相同的方向：Sonnet 会把同一结构后果拆成可达性、守卫和消费问题；Qwen 更常把一个状态机缺口扩展成多个 `missing`/动作/效果候选；Muse 的表述短，偏向端点和层级关系；Luna 的历史输出常将端点、范围和终止放在同一候选集合中。一个具体例子是 pair `0029`：Qwen 把 `AutonomousMode` 的层级、入口、守卫互斥和终止分别提出，Muse 主要保留层级和入口/终止，Sonnet 则突出两个相同守卫的互斥问题。它们面对相同 source STM 的差异属于决策粒度和属性选择差异，不能直接判定哪一种报告更正确。

为避免只看计数，下面保留 pair `0029`、round 1 的四条代表性原文摘录。它们来自各模型的完整 `issues`，用于核对 `reason` 与 `basis` 如何把同一份 Highway/Urban 状态机写成不同候选；摘录不是额外的语义裁定。

| 模型 | 候选键（property / direction） | `reason` 原文摘录 | `basis` 原文摘录 |
| --- | --- | --- | --- |
| Luna | `initial_entry / wrong_target` | “The exact HighwayMode initial edge reaches `enter_hwy` but carries guard `R45RouteToken == 5`...” | “NL3, source transition `tr_0005`, closed transition:line:24, and refuted initial-entry check...” |
| Sonnet 5 | `guard_disjointness / wrong_guard` | “exact cross-view comparison of source and closed transitions shows the same condition attached to both targets with no differentiator...” | “exact_source_inventory.transitions `tr_0006/tr_0007` (both event='dist_to_front<25 & extra_lane=true')...” |
| Qwen3.8-27B | `containment / missing` | “The contract requires containment of `InitialState` within `AutonomousMode`... the flat topology violates.” | “source_inventory rows for `AutonomousMode` (line 2) and `InitialState` (line 4); FCSTM states at lines 96 and 97...” |
| Muse Glimmer-30B | `containment / missing` | “Source inventory and closed-model hierarchy show no parent-child link between `AutonomousMode` and `InitialState`...” | “...`AutonomousMode` parent null, `InitialState` parent null... transition:line:105 `AutonomousMode->InitialState`” |

四条摘录对应四种可观察的选择：Luna 先检查 owner-local 初始入口及其 guard，Sonnet 先检查同一入口下的 guard 可区分性，Qwen 将自然语言中的“substate”展开为层级义务，Muse 也识别层级缺口但使用更短的依据链。它们说明 `reason/basis` 的差异来自候选属性和论证粒度，不能当作隐藏推理过程。

## 6. 四个模型的微观画像

### 6.1 GPT-5.6 Luna：端点和目标导向的历史锚点

Luna 的 raw candidate 主要集中在 `transition_endpoints`（190/778）和 `initial_entry`（163/778），`wrong_target` 占 36.0%。它的候选普遍带有 source identity 或 semantic comparison，且所有候选都命名了 locus。这个输出形态与 v61 的完整 method 设计一致：先把自然语言义务绑定到状态、迁移和触发事件，再围绕目标是否正确提出问题。

Luna 的重复候选保留少，round 1→2 的 pair Jaccard 均值为 0.170。宏观上，历史 Luna 的 baseline ordinary precision 已为 83.40%，完整方法的主要变化落在 coverage；微观上，候选集合的低重复表明 coverage 增益来自多轮扩展，而不是每轮复述同一组端点问题。这里的行为属于 19-predicate、v61 历史配置，不能外推到新连接或三款新模型。

### 6.2 Claude Sonnet 5：候选入口适中，选择性对外部约束敏感

Sonnet 的候选数最低（754），属性分布最分散，`initial_entry`、`transition_endpoints`、`event_consumer_coverage`、`reachability` 和 `guard_disjointness` 均有稳定占比。它的 `reason`/`basis` 平均长度最长，`deterministic`、`execution` 和 `alternative_reading` 词项出现率也最高。候选输出经常同时陈述 source inventory、可达性或执行结果，并明确写出一个有竞争力的替代解释。

Sonnet 的 `d_adjudication_correction` 为 133，高于其他模型；结合宏观结果中 ordinary precision 从 68.67% 升至 87.36%、strict precision 从 53.43% 升至 78.98%，可把它描述为“候选入口变化有限，外部证据约束改变了报告选择性”。这与它在 E2 中最大的 precision headroom 相符。证据只支持当前配置的描述，不支持“Claude 天生更容易幻觉”的模型家族结论。

### 6.3 Qwen3.8-27B：高探索量，偏状态动作和效果缺口

Qwen 的候选广度为 5.8519/cell，`state_action` 和 `effect` 合计 345 条，`missing` 占 68.2%。它同时保持较高的 source ref rate（82.1%）和低 D unresolved（6 条），说明候选扩张大多仍落在可定位、可核查的结构上。Qwen 的 `reason`/`basis` 也较长，但 alternative reading 低于 Sonnet，文本更常直接把自然语言要求映射成一个或多个缺失动作/效果。

宏观上 Qwen 的报告量和 hit 增长最大之一，普通 precision 从 81.10% 升至 89.25%。微观画像给出的机制假设是：方法提供了足够多的状态动作、效果和 closed inventory 锚点，使 Qwen 的探索倾向转化为可裁定候选。当前 serving 是 low，公开 AA xhigh 数字不能用于证明当前 low 达到相同能力。

### 6.4 Muse Glimmer-30B：迁移/层级取向和较强重复稳定性

Muse 的 `transition_endpoints`（259）、`state_action`（164）和 `containment`（91）占主导，`missing` 占 56.3%。它的 source ref rate 为 97.4%，`deterministic` hint 为 88.8%，但 `reason` 平均长度只有 173 字符，alternative reading 几乎不出现。输出更常用简短的契约、source inventory 和闭模型事实直接落到端点、层级或动作缺口。

Muse 的重复候选保留最多，round 1→2 Jaccard 均值/中位数为 0.462/0.400，且平均 added/dropped 最低。宏观上它的 ours round stability 为 70.97%，W2 share 为三款新增模型最高。两组观察相互支持“候选扩张适中、重复判断稳定、证据承诺较多”的任务内画像；它们仍然是描述性关联，不是因果证明。

### 6.5 跨层解释链：从候选入口到宏观后果

6.1–6.4 已经给出四个模型各自的局部观察。本节把这些观察按同一条链串起来，回答“模型先选择什么、证据如何改变筛选、这些选择怎样落到 precision/hit，重复运行又保留了什么”。分析覆盖 1,296 个 cell 和 3,434 条 raw issue candidate：Luna 778、Sonnet 754、Qwen 948、Muse 954。Luna 来自 v61 的 19-predicate 历史 method，后三款来自 12-predicate 新配置；本节比较配置下的行为组合，不建立统一模型排行榜。

#### 6.5.1 分析单位和观测顺序

同一输入经过以下可观测链：

```text
模型配置 + 固定输入
  -> 候选生成（B_c、H_property、H_direction）
  -> 证据绑定（source/locus/predicate、H_evidence）
  -> D 阶段反证与修订（D correction、disposition）
  -> 报告发布与 Luna 裁定（K/N/I_rep、P、P_s、hit）
  -> 跨 round 重现（J、retained/added/dropped、S）
```

链条中的指标各有固定职责，完整公式已在第 3 节给出。这里先固定阅读顺序：`B_c`、属性/方向熵描述候选入口；`R_f`、`H_evidence` 和词项率描述证据绑定；D disposition、`P`、`P_s`、`G` 描述反证后的发布选择；`hit` 和 `N_v` 描述语义后果；`J`、retained/added/dropped 和 `S` 描述重复保持。所有比例都使用各自声明的分母，不能跨层相除。

这条链描述数据的先后关系，不等同于已识别的独立因果图。四款配置的 ours 臂共享 FCSTM、inspection、predicate 和 backend，baseline 臂只提供原始输入；下文的前因、过程和后果是指标共变支持的任务内机制假设，A1/A2 才能进一步拆分组件贡献。

#### 6.5.2 先固定宏观终点

| 模型配置 | B baseline→ours | V baseline→ours | P / P_s baseline→ours | G baseline→ours (pp) | N_v baseline→ours | Δ hit@1 / @3 / @all (pp) | S baseline→ours |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Luna v61（19 predicates，历史） | 3.16→5.57 | 2.64→4.69 | 83.40→84.05% / 78.71→75.08% | 4.69→8.97 | 31.38→26.09% | +22.53 / +17.24 / +24.14 | 44.76→63.08% |
| Sonnet 5 | 4.41→5.08 | 3.03→4.44 | 68.67→87.36% / 53.43→78.98% | 15.24→8.38 | 30.75→25.45% | +11.49 / +8.28 / +14.48 | 43.64→56.56% |
| Qwen3.8-27B（low） | 2.81→5.91 | 2.28→5.28 | 81.10→89.25% / 74.51→81.52% | 6.59→7.72 | 33.06→29.94% | +19.77 / +20.69 / +19.31 | 55.79→64.80% |
| Muse Glimmer-30B（high） | 4.20→5.62 | 3.28→4.77 | 77.97→84.95% / 70.04→78.24% | 7.93→6.70 | 34.65→29.62% | +17.24 / +20.00 / +13.10 | 72.63→70.97% |

三款新增模型的报告量、有效报告量和两种 precision 同时上升。INVALID 比例分别从 31.33% 降到 12.64%（Sonnet）、从 18.90% 降到 10.75%（Qwen）、从 22.03% 降到 15.05%（Muse）。这说明在这些配置中，方法扩大了可报告候选，同时减少了无效发布。Luna 的 ordinary precision 只增加 0.65 pp，strict precision 下降 3.63 pp，但三种 hit 分别增加 22.53、17.24 和 24.14 pp。Luna 的结果主要承担历史 coverage 参照。

#### 6.5.3 向前追溯候选入口和证据

| 模型 | B_c | H_property | H_direction | H_evidence | source ref | predicate bound |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Luna（历史 v61） | 4.8025 | 0.7835 | 0.8130 | 0.8049 | 92.0% | 30.2% |
| Sonnet 5 | 4.6543 | 0.8338 | 0.8062 | 0.8037 | 39.8% | 39.8% |
| Qwen3.8-27B（low） | 5.8519 | 0.8203 | 0.4972 | 0.7775 | 82.1% | 35.1% |
| Muse Glimmer-30B（high） | 5.8889 | 0.7564 | 0.6146 | 0.8000 | 97.4% | 36.7% |

Qwen 和 Muse 的 `B_c` 最高，说明它们打开了更宽的候选入口。Qwen 的方向熵最低，`missing` 占 68.2%，入口扩张集中在状态动作和效果缺口。Muse 的属性熵最低，候选集中在迁移、动作和层级。Sonnet 的 `B_c` 最低但属性熵最高，候选较少却覆盖更多属性。source ref 从 Sonnet 的 39.8% 到 Muse 的 97.4% 变化很大，说明理由中的依据表述与结构化字段绑定是两个不同动作。

可见解释文本只能作表面补充：

| 模型 | reason / basis 均长（字符） | deterministic / execution / alternative reading 词项率 | round 1→2 J 均值 / 中位数 | 平均 retained / added / dropped |
| --- | ---: | ---: | ---: | ---: |
| Luna（历史 v61） | 248.61 / 184.12 | 48.3% / 6.2% / 0.0% | 0.170 / 0.000 | 0.889 / 2.824 / 2.963 |
| Sonnet 5 | 345.08 / 290.96 | 97.9% / 52.7% / 21.9% | 0.123 / 0.111 | 0.796 / 3.120 / 2.972 |
| Qwen3.8-27B（low） | 351.61 / 319.97 | 80.1% / 34.2% / 12.8% | 0.429 / 0.270 | 1.954 / 2.250 / 2.463 |
| Muse Glimmer-30B（high） | 173.26 / 213.92 | 88.8% / 26.3% / 0.1% | 0.462 / 0.400 | 2.028 / 1.870 / 2.083 |

长度是字符均值，词项率是固定词表的出现率，不能代表 hidden chain-of-thought、token 数或质量。J 衡量候选键集合重合，retained/added/dropped 衡量候选重组，均不构成质量分。

#### 6.5.4 反证筛选如何改变发布结果

`D correction` 是调用次数，不是独立候选数。下表把这一层与发布层的 precision 和台账外比例并列，便于判断候选扩张后有多少内容进入可裁定报告。

| 模型 | D correction calls | P / P_s ours | G baseline→ours (pp) | N_v baseline→ours | ours `E` (W2 share) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Luna（历史 v61） | 18 | 84.05% / 75.08% | 4.69→8.97 | 31.38→26.09% | 未在本表单列 |
| Sonnet 5 | 133 | 87.36% / 78.98% | 15.24→8.38 | 30.75→25.45% | 21.51% |
| Qwen3.8-27B（low） | 104 | 89.25% / 81.52% | 6.59→7.72 | 33.06→29.94% | 26.41% |
| Muse Glimmer-30B（high） | 7 | 84.95% / 78.24% | 7.93→6.70 | 34.65→29.62% | 30.88% |

#### 6.5.5 把四条配置内路径串起来

四个模型沿同一顺序阅读：先看 baseline 的起点，再看候选入口和证据绑定，接着看 D 阶段如何筛选，最后回到 precision、hit 和 S。这样每个结论都能对应链上的观测。

**Luna。** baseline ordinary precision 已为 83.40%，可提升空间较小。候选有 92.0% 带 source ref，方向熵为 0.8130；相邻 round 的 J 只有 0.170/0.000，候选主要在 `transition_endpoints` 和 `initial_entry` 间重组。结果是 precision 增加 0.65 pp，hit@1/@3/@all 增加 22.53/17.24/24.14 pp，S 从 44.76% 升至 63.08%。在 19-predicate v61 历史配置中，方法收益主要体现为多轮 coverage。

**Sonnet。** baseline precision 为 68.67%，strict gap 为 15.24 pp。候选数最低、属性熵最高，source ref 只有 39.8%，D correction 达 133 次，reason/basis 也最长。方法使报告密度由 4.41 增至 5.08，有效产出由 3.03 增至 4.44；普通/strict precision 增加 18.69/25.55 pp，strict gap 收窄到 8.38 pp。可观测链条指向“外部证据约束主要改变筛选和定级”，不能推广成 Claude 家族的固定倾向。

**Qwen。** baseline 报告密度为 2.81，有效产出为 2.28。`B_c=5.8519`，方向熵为 0.4972，`missing` 占 68.2%，source ref 为 82.1%，D correction 为 104 次。方法把报告密度提高到 5.91，有效产出提高到 5.28，hit@1/@3/@all 增加 19.77/20.69/19.31 pp，普通 precision 达到 89.25%。这支持“类型化谓词和可执行证据把高探索量导向可裁定候选”的任务内假设；方向集中本身提供的是选择倾向，不能直接当作正确性证据。当前 serving 为 low，公开 AA xhigh 数字不能替代本轮结果。

**Muse。** baseline S 为 72.63%，已有较高重复稳定性。`B_c=5.8889`，属性熵为 0.7564，source ref 为 97.4%，D correction 只有 7 次，round 1→2 J 为 0.462/0.400。候选集中在迁移、动作和层级，reason 较短而绑定率高。方法使 ordinary/strict precision 增加 6.97/8.20 pp，hit@1/@3/@all 增加 17.24/20.00/13.10 pp，ours S 为 70.97%。这组观测支持“候选扩张与重复保持可以并存”的任务内描述，稳定性不能直接换算成覆盖或通用能力。

#### 6.5.6 横向结论与边界

相同 pair/round 的候选 Jaccard 整体偏低，Qwen–Muse 均值 0.2704 最高，Luna–Qwen 仅 0.0307。人工复核 pair `0002`、`0019`、`0029` 和 `0049` 得到相同分化：Qwen 常把一个缺口拆成多个 `missing`、动作和效果候选；Muse 更常保留端点和层级；Sonnet 会加入可达性、守卫互斥和事件消费；Luna 更常把端点、范围和终止合并。差异发生在问题粒度和属性选择。

把四条路径合并后，得到四种任务内行为组合：Sonnet 的变化集中在证据筛选和严格定级；Qwen 集中在候选入口扩张和方向集中；Muse 集中在证据绑定和重复保持；Luna 集中在多轮 coverage 扩张。这个归纳把微观选择与宏观 precision、hit 和 S 接起来，仍属于描述性机制假设。baseline 没有 typed `basis/evidence`，只能做报告数量和自由文本 `reason` 的有限对照；Luna 的 19-predicate 历史结果也不能与后三款 12-predicate 配置合并为排行榜。

## 7. 与宏观 E2 结果的关系

微观统计和宏观结果可以放在同一条解释链上，但各自回答不同问题：

| 模型 | 微观主要变化 | 宏观对应现象 |
| --- | --- | --- |
| Luna | 端点/目标候选多，多轮保留少 | 历史方法收益主要体现为 coverage，precision headroom 小 |
| Sonnet | 候选广度变化小，确定性检查词项和 D correction 最多 | ordinary/strict precision 增益最大，strict gap 明显收窄 |
| Qwen | 状态动作/效果与 missing 候选大幅扩张，source ref 保持较高 | report breadth、accepted output 和 hit 增长明显，precision 仍上升 |
| Muse | 迁移/层级/动作候选集中，重复保留最高 | hit 和 precision 同时提升，round stability 最高 |

三款新增模型的报告量都增加，INVALID 比例同时下降。这个组合支持“FCSTM、inspection、typed predicates 和可执行证据共同改变候选筛选”的任务内解释。仅凭 E2 无法把收益拆成 predicate 定义、搜索引导和 backend 回执的独立因果贡献；A1/A2 才是相应的消融入口。

## 8. baseline 对照和方法学限制

baseline 的 `issue/reason/where` 能说明模型直接报告了什么，但缺少 ours 的 typed `property`、`violation_direction`、`source_refs`、`evidence_types`、predicate 和阶段回执。因此：

- baseline 可以用于报告数量、`reason` 覆盖率和字符长度的对照；
- baseline 不能用于与 ours 做同一属性分布、evidence mix 或 D disposition 的逐字段比较；
- baseline 的 `reason` 是自由文本，缺失 `basis` 不表示模型没有依据；
- 任何 baseline→ours 的 precision/hit 差值仍以 Luna judge 的冻结裁定为准，不能由 raw candidate 数重算。

四模型的 raw candidate 分布还受到 prompt、predicate 数、serving 档位、provider 路由和方法阶段 schema 的影响。Luna 的历史 19 predicates 尤其不能与三款 12-predicate 配置合成模型排行榜。报告不声称四款模型的隐藏推理已被读取，也不声称候选文本等于模型内部决策过程。

## 9. 近期 LLM4SE 文献对照

模型使用频数以 E1 的[近半年 LLM4SE 模型使用扫描](./model_readiness_20260906/2026-09-06-11-53-00-llm4se-recent.md)为准：该扫描覆盖 2026-03-06 至 2026-09-06 的 14 篇定向样本，按正文中的主要实验模型去重，明确声明不代表全部 LLM4SE 论文。下面列出其中与“多模型比较、过程轨迹或中间 artifact”最直接相关的 7 篇扩展对照；它们用于方法定位，不重新计算模型族频数。

| 工作 | 多模型/中间轨迹做法 | 对本报告的启示和边界 |
| --- | --- | --- |
| [SpecGPT](https://arxiv.org/abs/2510.14348)（2025-10-16） | 使用多个模型或 ensemble 比较最终规格生成质量，重点是最终指标 | 支持按同一任务协议比较 backbone；没有提供本报告粒度的 `reason/basis` 候选画像 |
| [MCeT](https://arxiv.org/abs/2508.00630)（2025-08-01） | 由多个检查视角生成并 cross-check 行为模型问题，报告最终 precision/recall 和人工评估 | 说明“生成视角 + 交叉核查”可拆开；其对象是 sequence diagram，未形成跨模型微观决策矩阵 |
| [LADEX](https://arxiv.org/abs/2509.03463)（2025-09-03） | 以多模型/多变体 critique 做受控消融，比较 correctness、completeness、调用量 | 支持把模型差异放在受控配置交互中；它不追踪每个 proposal 的属性/方向/证据承诺 |
| [Better Understanding, Better Fixes?](https://arxiv.org/abs/2609.04909)（2026-09-04） | 按模型和任务抽样中间 artifact，人工 open coding，研究错误如何影响修复 | 是最接近的先例：中间 artifact 必须有 codebook 和人工复核；本报告将 open coding 缩减为可复算的 typed 字段、透明词项和固定抽样 |
| [Two Truths and A Lie?](https://arxiv.org/abs/2609.03230)（2026-09-03） | 多模型、多轮重复任务，分析稳定的 error profile | 支持报告 round stability、retained/added/dropped；本报告进一步把稳定性绑定到候选键和模型属性 |
| [trajectory-judge](https://arxiv.org/abs/2609.00038)（2026-08-29） | 对 agent trajectory 做 step-level judge，强调终态不足以解释过程 | 支持保留阶段和逐调用边界；本报告不把 judge 的解释当作候选模型 rationale |
| [Beneath the Diff](https://arxiv.org/abs/2609.00077)（2026-08-31） | 对 proposal 按维度拆分、聚类并计算熵，分析不同模型的提议结构 | 提供“维度分布 + 多样性”分析方向；本报告使用 property/direction/evidence 分布和 Jaccard，避免用一个总分掩盖异质性 |

从这些工作可以归纳出三种常见模式：最终指标对照、受控的模型/流程消融、抽样的中间 artifact 编码。完整的逐调用 `reason/basis` 全量审计仍较少，尤其缺少“同一输入、同一候选键、跨模型和跨 round”的联合视图。E2 的数据允许做这类描述性分析，但不会把它写成模型内部思维可解释性或通用模型排名。

## 10. 论文可用结论与不可用结论

### 可以写

1. 在相同任务输入和冻结方法语义下，四个模型呈现不同的候选属性、违反方向、证据引用和重复稳定性组合。
2. Qwen 的探索量最高，Sonnet 的 D correction 次数最多且 precision gap 收窄最大，Muse 的重复候选稳定性最高，Luna 的历史方法收益主要体现在 coverage；这些判断都有候选级和 cell 级统计支持。
3. 三款新增模型的宏观 precision/hit 增益与微观候选扩张并存，说明方法改变了候选提出和筛选的组合，而非简单减少输出。

### 不能写

1. `reason/basis` 揭示了隐藏 chain-of-thought、真实思维过程或模型“内在信念”。
2. 某模型的候选数、Jaccard 或公开 benchmark 更高，所以它在本任务上整体更强。
3. E2 单独证明了仿真、形式化验证、谓词定义或 backend 的独立因果贡献。
4. Luna 的历史 19-predicate 画像与三款 12-predicate 新配置构成统一排行榜。
5. baseline 的 typed 字段缺失等于没有 reasoning，或把所有 `INVALID` 直接解释成一般 hallucination。

## 11. 复现和审计入口

从仓库根执行，脚本只读冻结 JSON，不调用 provider：

```bash
python project_1_llm_state_machine_modeling/paper_stm_issue_discover/reports/2026-09-09-e2-micro-decision-profiles.py
python -m json.tool project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/e2_20260907/micro_decision_profiles.json >/dev/null
```

数据入口保留四类内容：

- `cells`：每个模型、arm、pair、round 的来源 hash、阶段 trace、调用摘要、候选和 baseline issue；
- `aggregate_ours`：每模型全量与逐 round 属性、方向、证据、词项、D 和调用统计；
- `agreement`：六个模型对的同输入候选 Jaccard；
- `round_transitions`：相邻 round 的 retained/added/dropped。

E2 的语义结果和 precision 定义见 [E2 综合结果报告](./2026-09-08-e2-three-backbone-results.md)；历史 Luna 的裁定和可比性见 [E2 紧凑归档](../final_results/e2_20260907/README.md)。本报告的微观统计是派生观察层，不改变 E2 的 prompt、method、validator、eligibility、judge 协议或历史结果。
