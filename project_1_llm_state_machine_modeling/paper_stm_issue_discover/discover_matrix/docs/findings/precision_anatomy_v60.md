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
