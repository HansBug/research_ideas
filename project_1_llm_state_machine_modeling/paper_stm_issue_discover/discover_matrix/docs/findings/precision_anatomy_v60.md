# v60 precision 解剖：方法侧根因、确定性拦截规则与反事实预判（2026-09-04）

> 数据来源：[judge 第六轮配置的全量运行](../../../judge/calibration/results/full_v3.11_3a1ba5cf1/README.md)（v3.11，1271 + 512 条报告，0 格失败）与冻结的人工终稿 `final_results/v60_current_vs_x1v2_baseline`。本文只做诊断与反事实预判，⛔ 不改任何冻结数据；所有拦截规则若采用，必须作为方法的新版本（v61）在运行前登记，再走完整流程与人工裁定。

## 〇、定性

ours 的 precision 缺口是**方法侧**的：谓词在降低表示（closed model）上触发并用降低表示的词汇陈述事实。作者源措辞的 592 条报告 precision 89%（人工）/ 87.5%（judge），高于 baseline 的 81.4%；拉低整体的是三组派生表示报告（占全部报告 53%）。judge 不是主因：它把人工口径的 −4.3 pp 放大成 −12.2 pp，放大的部分全部落在派生措辞的报告上（人工透过措辞读源级关切，judge 按作者源原则字面执行）。

| 报告族 | n | 人工 K / N / I | judge K / N / I | precision 人工 / judge | 只靠它撑起的 hit@1 单位 |
| :-- | --: | :-- | :-- | --: | --: |
| 守卫载体（S5「X to Y omits its required guard」） | 308 | 62 / 160 / 86 | 35 / 140 / 133 | 72% / 57% | 11 |
| route token / trigger 槽位 | 68 | 32 / 0 / 36 | 20 / 15 / 33 | 47% / 51% | 9 |
| 其他派生措辞（closed model、运行时场景、inventory、carrier） | 303 | 163 / 34 / 106 | 133 / 44 / 126 | 65% / 58% | 43 |
| 作者源措辞 | 592 | 492 / 37 / 63 | 440 / 78 / 74 | 89% / 87.5% | — |

## 一、按谓词模板的精度表（ours 全部 1271 条）

| 谓词 / 标题模板 | n | 人工 K / N / I | 人工 precision | judge precision | 只靠它撑起的 hit@1 单位 |
| :-- | --: | :-- | --: | --: | --: |
| S5 守卫载体 `{src} to {tgt} omits its required guard` | 304 | 62 / 157 / 85 | 72% | 57% | 11 |
| `{event} may not leave the system in {tgt}`（R2 运行时委托） | 42 | 3 / 0 / 39 | **7%** | 2% | 0 |
| `{X} transition {A} -> {B} is absent`（transition_endpoints） | 46 | 14 / 0 / 32 | 30% | 30% | — |
| `Trigger set for {A} -> {B} uses …`（trigger_set） | 20 | 2 / 0 / 18 | 10% | 20% | 0 |
| `Initial transition … has a guard`（多为 route token） | 15 | 5 / 0 / 10 | 33% | — | — |
| `{owner} initial entry to {tgt} is conditional` | 20 | 19 / 0 / 1 | 95% | 75% | 0 |
| `Required operating scope {x} is unreachable from root` | 77 | 72 / 5 / 0 | 100% | 99% | 3 |
| `Initial transition … has a trigger` | 75 | 75 / 0 / 0 | 100% | 93% | 26 |
| `{state} is a source-certified reachable dead end` | 39 | 39 / 0 / 0 | 100% | 100% | 34 |
| `{scope} has declared but unreachable event consumers` | 43 | 39 / 4 / 0 | 100% | 98% | 1 |
| `{state} is a reachable leaf without outgoing transition` | 42 | 36 / 0 / 6 | 86% | 71% | 6 |
| `{var} has no data-side representation` | 24 | 18 / 4 / 2 | 92% | 100% | 3 |
| 其余（cardinality、lacks default entry、routes to、终止、层次等） | 524 | 365 / 61 / 98 | 81% | — | — |

结构性谓词（可达性、死端、初始触发、消费者可达、终止）precision 接近 100% 且撑起绝大部分 hit；拖累来自四个谓词。

## 二、四条确定性拦截规则与反事实预判

> ⚠️ 本节的 G、R 两条在 §六 被**修正**：G 会误拦人工判 D1 的「条件以事件承载」报告并丢 6 个独占 hit 单位；R 以「文本含 token」为判据过宽，会拦掉 23 条 token 仅出现在引证里的有效报告。当前生效的规则包是 §六 的 P1–P5，本节保留为推导过程。

全部规则都能只看 v60 现有输出判定会拦哪条，⭐ 因此下面的数字是**预判**，不是估计。判定用 `where` 里的端点回到作者 PlantUML 找迁移标签（⛔ 不能用 `observed` 里的 `transition:line:NN`，那是降低表示的行号）。

### G. S5 守卫载体：只在作者标签为空或为布尔表达式时触发

产生点：`method/src/paper_stm_method/semantics/frontier.py` 的 `transition_guard_presence`（约 L3133–3262）。谓词看到 NL 侧备选带独立守卫、closed model 里该迁移 `guard=null` 就报「缺守卫」，⛔ 不看作者标签写的是什么。按作者标签分类：

| 作者标签 | n | 人工 K / N / I | 人工 I 的构成 | judge K / N / I | 处置 |
| :-- | --: | :-- | :-- | :-- | :-- |
| 事件名（`Door Closed`、`Approached/Decelerate`） | 118 | 19 / 44 / 55 | D0 55 | 7 / 20 / 91 | **拦截**：事件名标签实现了条件（载体纪律） |
| 方括号守卫（`Door Closed [time = 0]`） | 37 | 10 / 0 / 27 | NADC 26 | 6 / 15 / 16 | **拦截**：作者写了守卫，是降低表示把它丢了（同时是 lowering 的缺陷） |
| 布尔表达式（`intersection=true`、`dist_to_front<15 && …`） | 146 | 30 / 113 / 3 | D0 3 | 19 / 102 / 25 | 保留：条件写成标签文字而非守卫，人工 98% 判有效 |
| 无标签 | 3 | 3 / 0 / 0 | — | 3 / 0 / 0 | 保留：条件完全缺失，全是 K/D2 |

### R. 锚在编译器 route token 上的事实不发布

产生点：`pipeline/representation/src/paper_stm_representation/plantuml_source_lowering.py` 的 `route_code` 为跨作用域路由引入 `R45RouteToken`（登记为 `lowering_variable`，`canonical:compiler:route_token`）；inspection 事实 `INITIAL_ENTRY_CONDITIONAL` 随后把它当成初始进入的守卫，`owner_initial_entry`（约 L4722）与「Initial transition has a guard」据此发报。`observed` 或 `claim` 含 `R45RouteToken` 的 60 条：人工 K 25 / N 0 / I 35。人工留 K 的 25 条是透过措辞读到台账里的进入结构问题；只靠它们撑起的 hit 单位 5 个。

### S. R2「post-stimulus 委托运行时」的候选不发布未验证的假设

产生点：`state_after_stimulus`（约 L3377），`observed` 固定为「The exact post-stimulus state is delegated to a fresh native FCSTM runtime scenario」。42 条里人工有效 3 条、hit 贡献 0——它把一个待运行时验证的假设当成发现发出去了。规则：运行时场景没跑或没得出目标态不符，不发。

### T. trigger_set 比较不发布

「Trigger set for A -> B uses …」20 条里人工 NADC 18：比较的是 typed trigger 集合与 NL，差异来自降低表示的事件改名。规则：trigger_set 属性的差异报告在没有作者源级证据时不发。

### 反事实（人工口径 = 冻结终稿对同一批报告的判定；judge 口径 = 第六轮配置全量）

| 规则 | 拦截 n（人工 K / N / I） | 剩余 n | 人工 K / N / I | **人工 precision** | judge precision | 人工 hit@1 下限 |
| :-- | :-- | --: | :-- | --: | --: | --: |
| 无 | — | 1271 | 749 / 231 / 291 | 77.1% | 71.2% | 71.3% |
| G | 155（29 / 44 / 82） | 1116 | 720 / 187 / 209 | 81.3% | 76.8% | 69.9%（≤6 单位） |
| R | 60（25 / 0 / 35） | 1211 | 724 / 231 / 256 | 78.9% | 72.4% | 70.1%（≤5） |
| S | 42（3 / 0 / 39） | 1229 | 746 / 231 / 252 | 79.5% | 73.6% | 71.3%（0） |
| T | 22（2 / 0 / 20） | 1249 | 747 / 231 / 271 | 78.3% | 72.1% | 71.3%（0） |
| G ∪ R | 215 | 1056 | 695 / 187 / 174 | 83.5% | 78.5% | 68.7%（≤11） |
| G ∪ R ∪ S | 257 | 1014 | 692 / 187 / 135 | 86.7% | 81.7% | 68.7% |
| **G ∪ R ∪ S ∪ T** | 279（59 / 44 / 176） | 992 | 690 / 187 / 115 | **88.4%** | **83.1%** | **≥ 68.7%**（≤11） |

四条规则互不重叠。baseline 人工 precision 81.4%、hit@1 52.2%：四条全上后 ours 的 precision 高出 baseline 7 pp，hit@1 差距下限 +16.5 pp（人工口径；judge 口径 hit 差距 +15.4 → 约 +13 到 +15，取决于 relation 粒度规则）。

## 三、不是确定性规则的部分

1. **`{X} transition A -> B is absent`（46 条，I 32）**：D0 21 是「NL 说该有一条迁移、作者用别的方式实现」的语义判断；FP 11 是作者在组合态边界写了那条迁移而谓词只查 closed model 的直接边。后者可以改成源级路径检查（确定性，但要改谓词实现）；前者不可确定性拦截。
2. **其他派生措辞（303 条）**：人工 K 163——发现是真的，但 `observed`/`basis` 用 closed model、inventory、runtime scenario 的词汇陈述。修法是渲染层：经 `source_trace` 把降低表示元素映射回作者 PlantUML 的行与标签再写 `observed`。对人工口径无影响（人工已透过措辞读），对 judge 口径能收回大部分 FP（judge FP 130 对人工 53）。
3. **relation 粒度**：ours 的 hit@1 在 judge 口径少 18 个单位是关系判定（同缺陷不同 facet 判 NO），不是方法问题，属 judge 规则。
4. **hit 的上限**：v60 人工 hit@1 71.3% 是方法覆盖的上限；四条规则只清 precision，不涨 hit。要把差距推到 +20 pp 需要覆盖侧改进（选题与断言构造，见 [v46_weakness_anatomy.md](./v46_weakness_anatomy.md) 的两处赤字）。

## 四、是否触及框架

G、S、T 是候选发布层的局部门（frontier 内三处），R 是一条溯源感知的过滤（编译器登记的 `lowering_variable` 已给出判据），方括号守卫被降低表示丢失还需要修 lowering 的标签解析。⛔ 这些都改变方法的产出，所以是新版本 v61，v60 冻结数字不动；不是八阶段循环的框架性重设计。渲染层改为作者源措辞是跨候选的中等改动，可与 v61 同批也可分批。

## 五、合规性

四条规则都以通用建模原则表述（事件名标签实现条件；编译器制品不参与归因；未验证假设不发布；typed 集合差异不是源级事实），对 baseline 不适用（它没有这些谓词），⭐ 必须在 v61 运行前写进事前登记；本文的反事实数字是从 v60 输出预判的期望值，v61 的真实数字以新运行与新裁定为准。

## 六、按谓词全表的系统性分析、表达债务排查与修正后的规则包 P1–P5

本节在 §一至§四之后补做三件事：把 ours 全部 1271 条按**谓词 × 性质 × 方向**列全表；系统排查「表达债务」（lowered 闭合模型的对象、行号与措辞泄入报告）；据此把 §二的四条规则修正为五条**发布层通用规则**，并给出逐条累积的精确反事实。口径同 §二：人工 = 冻结终稿对同一批报告的判定；judge = 第六轮配置全量（`full_v3.11_3a1ba5cf1`）。

### 6.1 谓词目录与实际发射

冻结谓词目录共 **19 个**：S1–S6（结构：元素存在、迁移端点、触发器集合、状态动作、守卫、效果）、G1–G4（拓扑：可达、必达、禁止路径、根/标记）、R1–R4（轨迹：事件步、刺激后状态、行为窗口、状态保持）、V1–V5（有界验证：守卫互斥、死锁自由、步界、终止等）。发射侧（`frontier.py`）**只有 8 个谓词真正带 `predicate_id` 出现在报告里**：S2、S3、S4、S5、G1、G2、R2、V4；其余候选按 discovery-grounding 的规定「无法被目录表达则 `predicate_id=null`，不得静默丢弃」，共 **554 条**（43.6%）以无谓词候选发布。这 554 条整体人工 precision 87%，与结构谓词持平，说明无谓词候选不是弱点；弱点集中在下表的少数几行。

### 6.2 全表（n ≥ 10 的行；hit only = 该行独自撑起的 FULL 单位数；ids@3 = 该行三轮内至少命中一次的台账条目数）

| 谓词 / 性质:方向 | n | 人工 K/N/I | 人工 prec | judge prec | hit any | hit only | ids@3 | 代表标题 |
|:--|--:|--:|--:|--:|--:|--:|--:|:--|
| S5 / guard:missing | 304 | 62/157/85 | 72% | 57% | 23 | 11 | 13 | X to Y omits its required guard |
| G1 / reachability:unreachable | 105 | 98/7/0 | 100% | 99% | 52 | 4 | 23 | X operating scope is unreachable from root |
| S2 / transition_endpoints:wrong_target | 95 | 42/16/37 | 61% | 64% | 31 | 14 | 18 | transition X -> Y is absent |
| S3 / trigger_set:mismatched | 88 | 64/0/24 | 73% | 72% | 42 | 27 | 18 | trigger set for X -> Y uses Z |
| V4 / deadlock_freedom:dead_end | 85 | 79/0/6 | 93% | 86% | 63 | 43 | 25 | X is a source-certified reachable dead end |
| — / event_consumer_coverage:unconsumed | 56 | 50/6/0 | 100% | 96% | 34 | 1 | 18 | X has declared but unreachable event consumers |
| — / effect:wrong_effect | 55 | 42/6/7 | 87% | 91% | 23 | 8 | 12 | timer has no data-side representation |
| S5 / guard:wrong_guard | 33 | 6/3/24 | 27% | 33% | 3 | 0 | 2 | Initial transition transition:line:NN has a guard |
| R2 / state_after_stimulus:wrong_target | 32 | 0/0/32 | 0% | 3% | 0 | 0 | 0 | X may not leave the system in Y |
| S2 / initial_entry:missing | 31 | 25/0/6 | 81% | 71% | 26 | 2 | 12 | X lacks default entry to Y |
| — / initial_entry:missing | 29 | 28/0/1 | 97% | 79% | 23 | 1 | 15 | X initial entry to Y is conditional |
| — / containment:wrong_scope | 28 | 22/0/6 | 79% | 64% | 13 | 6 | 7 | X is outside required owner Y |
| — / state_action:wrong_effect | 27 | 18/7/2 | 93% | 56% | 13 | 3 | 12 | X lacks the required Y action |
| — / transition_endpoints:wrong_target | 27 | 13/1/13 | 52% | 52% | 10 | 6 | 9 | X activation is unreachable |
| S2 / initial_entry:wrong_target | 26 | 18/0/8 | 69% | 73% | 19 | 2 | 12 | — |
| — / state_action:other | 25 | 12/13/0 | 100% | 84% | 6 | 1 | 6 | X lacks the required pump action |
| — / initial_entry:wrong_target | 24 | 21/1/2 | 92% | 96% | 20 | 4 | 13 | X has a malformed owner-local initial target |
| — / termination:not_completed | 23 | 18/0/5 | 78% | 100% | 17 | 13 | 9 | termination target X does not terminate its scope |
| — / trigger_set:mismatched | 21 | 20/1/0 | 100% | 86% | 20 | 1 | 14 | Initial transition transition:line:NN has a trigger |
| — / cardinality:missing | 19 | 14/4/1 | 95% | 95% | 11 | 6 | 7 | X realizes 1, not 3, regions |
| — / cardinality:extra | 15 | 11/4/0 | 100% | 73% | 6 | 5 | 3 | X realizes 4, not 3, regions |
| — / region_structure:wrong_scope | 14 | 11/3/0 | 100% | 79% | 9 | 1 | 6 | region structure is not established |
| — / state_after_stimulus:wrong_target | 12 | 4/0/8 | 33% | 17% | 3 | 0 | 3 | X may not leave the system in Y |
| S2 / transition_endpoints:missing | 12 | 3/0/9 | 25% | 33% | 2 | 0 | 2 | transition X -> Y is absent |
| — / guard_disjointness:wrong_guard | 12 | 6/0/6 | 50% | 50% | 6 | 1 | 2 | X compete under the same selection conditions |
| — / event_consumer_coverage:unreachable | 11 | 10/1/0 | 100% | 100% | 3 | 0 | 2 | X response has no reachable consumer |
| — / variable_delta:wrong_effect | 11 | 8/0/3 | 73% | 100% | 7 | 4 | 4 | cooking time has no data-side representation |
| 其余 24 行（n < 10，合计 64） | 64 | 55/2/7 | 89% | — | — | — | — | 多为 100% 的小组 |
| **合计** | **1271** | **749/231/291** | **77.1%** | **71.2%** | **310** | — | **119** | |

读法：（1）拓扑与验证谓词（G1、V4）、事件消费覆盖、初始入口、终止，precision 93–100%，撑起绝大多数独占 hit；（2）S3 的 88 条里「Initial transition has a trigger」形态全对且独占 27 个单位，只有「uses」形态（≈22 条）是 lowering 改名造成的假不一致；（3）S2「transition is absent」61% 但独占 14 个单位，**不能删只能修**；（4）真正的洼地只有四处：S5 guard:missing（人工 I 85）、S5 guard:wrong_guard（I 24，全是 route token）、R2 全族（44 条，人工只认 4 条，hit 为 0）、S2 transition_endpoints 的 FP（11 条复合层已有该迁移）。

### 6.3 route token 属于哪个谓词

**不属于任何谓词。** `R45RouteToken` 是 PlantUML lowering（`plantuml_source_lowering.py` 的 `route_code`）为跨作用域路由保留的**编译器变量**（`canonical:compiler:route_token`，`object_type=lowering_variable`）。它出现在 60 条报告里，分两类：

| 类别 | n | 人工 K/N/I | 独占 hit | 处置 |
|:--|--:|--:|--:|:--|
| **主张的主语就是这个变量**：S5 guard:wrong_guard「Initial transition … has a guard」（33）+ 无谓词 owner_initial_entry「initial entry to X is conditional」中由 `INITIAL_ENTRY_CONDITIONAL` 诊断驱动的部分（4） | 37 | 11/0/26（A0 25） | 0 | 拦（P1） |
| **token 只出现在引证里**：effect / variable_delta / trigger_set / transition_endpoints 等报告把 lowered carrier 的 effect 列表原样引进 `observed` | 23 | 14/0/9 | 4 | 保留，只需按 6.4 回映射渲染 |

§二 的 R 规则以「文本含 token」为判据，会把第二类 23 条一起拦掉，丢 4 个独占单位（含 EIS-0006-02 三轮全中的一组）；本节改为 P1。

### 6.4 表达债务系统排查

以 `title + observed + expected + claim + where` 为文本，五类 lowered 标记在 1271 条中的分布：

| 标记 | n | 人工 K/N/I | 人工 prec | 独占 hit |
|:--|--:|--:|--:|--:|
| `R45RouteToken` | 60 | 25/0/35 | 41.7% | 5 |
| lowered 行号引用 `transition:line:NN` / `state:X:line:NN` | 775 | 440/174/161 | 79.2% | 142 |
| 「exact carrier / exact … alternative」措辞 | 370 | 105/157/108 | 70.8% | 14 |
| 「delegated to a fresh native FCSTM runtime」 | 42 | 3/0/39 | 7.1% | 0 |
| 编译器词汇（canonical / lowered / FCSTM / pseudo-state / closed model / derived） | 266 | 157/24/85 | 68.0% | 42 |
| **任一** | **925 (72.8%)** | 512/195/218 | 76.4% | 165 |
| 无（文本干净） | 346 | 237/36/73 | 78.9% | 59 |

按谓词看债务占比：S5 100%、R2 100%、V4 99%、S3 95%、G1 82%；无谓词的事件消费覆盖只有 12%。

**代码层根因**：`frontier.py` 的全部 `observed` 都用 `transition.ref`（lowered 模型的行号）渲染；lowering 内部虽然保留了 `route_source_refs[transition_id] = raw_ref` 这样的回溯信息，但 **method 侧没有任何消费者**（`grep source_line|provenance|origin` 在 `method/src` 里只命中工具脚本），即**不存在作者源回映射层**。这是系统性缺口，不是个别模板的措辞问题。

但要区分两件事：（a）债务**本身**不压 precision——带 lowered 行号的 775 条 precision 79.2%，高于文本干净的 78.9%，142 个独占 hit 单位都在其中，人工基本读穿了行号；（b）压 precision 的是三种**特定**债务：主语是编译器变量（41.7%）、把未执行的委托判定当发现发布（7.1%）、lowering 丢失或改写了作者标签后再拿 lowered 事实去比对（S5 方括号守卫 37 条 A0 26、S3「uses」22 条 I 20）。所以修法分两层：回映射渲染解决可读性与 judge 的严格性问题；发布规则解决错误主张。

### 6.5 修正后的规则包 P1–P5：全是「发布层通用规则」，不针对任何谓词

不删谓词。19 个谓词是定义在 $M = (S, E, V, Tr, A)$ 上的闭合判定词表，每个都对应模型语义的一个可判定问题；本轮暴露的弱点都不在「问什么」，而在「谁有资格被问、拿什么证据问、答案算不算发现」。下面五条都能脱离具体样本独立成立，并且各有外部依据：

- **P1 主语必须是作者源元素。** 编译器为表示目的引入的变量、伪状态、路由守卫不属于被审模型（它们不在作者的 $M$ 里）；对它们的任何主张都不是关于模型的主张。依据：程序分析里「编译器引入的临时量不参与源级诊断」是通行做法；本方法自己的 canonical 注册表已经把它们标成 `lowering_variable`，只是发布层没查。
- **P2 只发布已执行判定的结论。** 谓词返回 unknown / delegated（R2 的「exact post-stimulus state is delegated to a fresh native FCSTM runtime scenario」）时，候选还是假设，不是证据；发布它等于把待验证项当成发现。依据：本仓库 §10 的降级纪律——未满足的义务记为 coverage gap，不得冒充结果。
- **P3 typed-set 比较必须在作者标签上做。** 触发器名、守卫文本经过 lowering 改名之后再比对，差异可能来自 lowering 而非模型；S3「uses」形态正是如此。规则：比对两侧都回映射到作者标签，只有作者标签层仍不一致才发布。
- **P4 lowering 必须保守：解析不了的标签成分不能当「缺失」。** PlantUML 迁移标签语法是 `event [guard] / effect`；当前 lowering 丢掉了方括号守卫，S5 随后把「作者写了守卫但 lowering 没带过来」报成「omits its required guard」。这是 lowering 的 bug，修 lowering 即可；作者标签里有方括号守卫的 37 条随之消失，其中 10 条 D2 应改以 guard:wrong_guard 形态重现（守卫存在但与要求不同）。
- **P5 S2 存在性判定必须在作者层的完整迁移集合上做。** 11 条 FP 是复合状态层已有该迁移、方法在展开后的子状态层没找到而报「absent」。规则：`transition_exists` 在作者源的迁移集合（含复合层）上判定。

它们都是**前置条件 / 健全性条款**，可以在看到任何样本之前从「作者源锚定」这一条方法立场推出来，不是对某个谓词或某个 pair 的特判。

### 6.6 累积反事实（每条规则独立可回放，按现有 v60 产出直接判定）

| 规则包（累积） | 本步拦下 n (K/N/I) | 剩余 n | 剩余人工 K/N/I | 人工 precision | judge precision | hit@1 | hit@3 | hit@all |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| v60 现状 | 0 | 1271 | 749/231/291 | 77.1% | 71.2% | 310/435 = 71.3% | 119/145 | 86/145 |
| P1 主语为编译器变量 | 37 (11/0/26) | 1234 | 738/231/265 | 78.5% | 72.3% | 310 = 71.3% | 119 | 86 |
| +P2 未执行判定不发布 | 44 (4/0/40) | 1190 | 734/231/225 | 81.1% | 74.7% | 310 = 71.3% | 119 | 86 |
| +P3 lowering 改名造成的触发器不一致 | 22 (2/0/20) | 1168 | 732/231/205 | 82.4% | 75.8% | 310 = 71.3% | 119 | 86 |
| +P4 lowering 丢失方括号守卫 | 37 (10/0/27) | 1131 | 722/231/178 | 84.3% | 76.4% | 310 = 71.3% | 119 | 86 |
| +P5 S2 复合层已有该迁移 | 11 (0/0/11) | 1120 | 722/231/167 | **85.1%** | **77.1%** | **310 = 71.3%** | **119** | **86** |
| （对照）再拦事件标签且守卫非同名的 S5 | 53 (11/1/41) | 1067 | 711/230/126 | 88.2% | 79.4% | 304 = 69.9% | 117 | 84 |
| （对照）再拦事件标签同名的 S5 | 65 (8/43/14) | 1002 | 703/187/112 | 88.8% | 83.4% | 304 = 69.9% | 117 | 84 |
| baseline（人工） | — | 512 | 312/105/95 | 81.4% | 83.4% | 227 = 52.2% | 106 | 46 |

P1–P5 合计拦 151 条，其中人工有效 27 条（全部 D2/D1 但**无一是独占 hit**），无效 124 条；三项 hit 指标**一个单位都不丢**。人工口径下 precision 差距从 −4.3 pp 变为 **+3.7 pp**，hit@1 差距维持 **+19.1 pp**。

两行对照解释了为什么 §二 的 G 规则被放弃：事件标签 118 条按「要求的守卫与作者事件是否同名」拆开后，**同名的 65 条人工判 43 条 D1**（条件以事件而非守卫承载，属模态缺陷），拦它们等于删有效报告；**不同名的 53 条**才是 D0 富集区（41/53），但这需要判断「事件是否蕴含该条件」，是语义问题，没有确定性判据。这 53 条留给生成端纪律与评审端条款，不进 validator（§11）。

### 6.7 剩余的 167 条无效报告在哪

按缺陷：D0 117、A0 50。按谓词：S5 guard:missing 58（上一段那 53 条为主）、S2 transition_exists 各形态 48（「absent」但 NL 备选以别的方式实现，D0）、无谓词 transition_endpoints 13、其余零散。这些都是「模型以另一种合法方式实现了需求」的判断，属评审端条款；确定性规则到 P5 为止。

### 6.8 hit 的杠杆在稳定性，不在覆盖

hit@1 = 各台账条目的命中轮数之和 / 435。当前 310 = 86 个 hit@all 条目 × 3 + 其余 33 个「至少中一轮」条目贡献的 52 / 99。若这 33 个不稳定条目全部稳定为三轮命中，hit@1 = 357/435 = **82.1%**，差距 +29.9 pp；而新增覆盖 26 个从未命中的条目每个最多 +0.7 pp。所以 +20 pp 的目标应从**候选发射的采样方差**（同一 pair 三轮发不同候选）下手，这是 v61 之后单独的方法议题，与本节的 precision 规则正交。

### 6.9 是否触及框架

P1、P3、P4 落在 lowering 与发布渲染层（加一个作者源回映射并在发射前查 canonical 注册表的 `object_type`）；P2 落在候选发射的证据门（谓词结果非 True/False 不发布）；P5 是 S2 求值器换分母。**谓词目录、契约结构、八阶段循环均不改。** 全部为确定性改动，可在 v60 产出上离线回放核对拦截集合与上表一致，再以 v61 事前登记后重跑。

### 相对上一版的改动

§二 的 G（事件标签一律免发）与 R（文本含 token 一律免发）被本节 P1、P4 取代；原因见 6.3 与 6.6 的对照行。原 §二 反事实表（88.4% / 68.7%）不再是推荐口径，保留为推导记录。
