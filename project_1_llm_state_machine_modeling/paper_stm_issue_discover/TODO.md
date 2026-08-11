# paper1（STM issue discover）待办总清单

> **这是本论文所有待办的唯一入口。** 每一项都是 `* [ ]` 复选框，做完打勾并注明在哪个 PR 完成。
>
> 建立于 2026-08-11，由一轮全目录踩点产出。踩点范围：`story/` 与 `outline`、
> 文献与 baseline 考据、`pipeline/` 与实验设计里的 repair 假设。
>
> **优先级口径**：
> - **P0** —— 不做会让论文的某条 claim 站不住，或会误导下一个动手的人
> - **P1** —— 论文成稿必须有，但不阻塞其它工作
> - **P2** —— 提升质量，可延后
> - **P3** —— 工程整洁，与论文结论无关

---

## A. 论文骨架与叙事

* [ ] **P0 · 重建 `story/` 的实质内容。** 当前是 placeholder（结构在、细节缺）。
  九节骨架、三条 contribution、4 个 RQ 的结构已立起来，要逐节填实。
  材料：`story/README.md` 的 TODO 区块、归档在 `archive/r8_discover_repair_story/` 的上一版
  （那一版内容质量不低，是在时间压力下赶的，可大量借鉴）。
* [ ] **P0 · 裁定 contribution 2 的 claim 形状。**
  导师原话是「现有 detection 方法报告错误，**缺少错误的上下文信息**」。
  ⚠️ 按字面写会被反驳——至少四个反例：模型检查的反例轨迹**就是**上下文；
  `automatic-debugging-support-for-uml-designs`(2000) 把状态图改动**反向映射回需求**；
  `rfseek-and-ye-shall-find`(2025) 给 **provenance**；
  `generating-annotated-behavior-models-from-end-user-scenarios`(2006) 自动生成状态不变式并附到节点上。
  建议收窄为「**需求侧锚定 + 可机械求值 + 可重放，三者不可兼得**」，
  但这**改变了 claim 的形状**，需人定。
* [ ] **P1 · 裁定 RQ 的数量与边界。** 当前 placeholder 按 4 个 RQ 立结构。
  ⚠️ RQ4「覆盖稳定性与能力归属」是否独立成 RQ，还是并入 RQ1 作子分析？
* [ ] **P1 · 「回归防护」这条贡献留不留。**
  `regression_guards` 是活字段、每格必写（smoke 里 16 条）、**零消费者**
  （全库只出现 2 次：`schemas.py:1143` 定义、`nodes.py:5703` 写入）。
  而 `README.md` 已把「为真的部分构成回归防护」写进 contribution 1。
  三选一：① 保留并标为「方法性质-未测」；② 保留并补一个消费者（ref 翻转率实验正好是它）；
  ③ 字段与那句话一起删。
* [ ] **P1 · 裁定 contribution 是两条还是三条。**
  BLUEPRINT 说三条（元模型 / 断言体系 / 证据链），归档版说两条，**都是 AI 归纳，从未被人裁定**。
  导师原话只支持「元模型与断言体系本身」+「缺上下文那条叙述」。
  ⚠️ **RQ 必须与 contribution 一一对应**，所以这条卡住「RQ 定稿」那条。
* [ ] **P1 · 九节骨架里没有独立的 Problem Formulation 节。**
  而导师定调要求建模对象边界在「**问题定义阶段**」给出——这个落点在九节里无处安放。
  要么加一节，要么明确它落在 §1 还是 §3。
* [ ] **P2 · 「覆盖」一词在本文有三个互不相同的含义**：
  构造覆盖性（断言由全覆盖需求条目转换而来）/ `hit@k` 缺陷覆盖率 / 元模型表达力覆盖。
  中文尚可靠上下文区分，**英文写作会撞车**，需一并给出三者的英文区分。
* [ ] **P2 · fork/join 的写法定稿。** 已定：**不展开、不做 RQ**，在问题定义阶段给边界。
  ⚠️ 但 session 7de1b210 曾提过一个「四层 finding」方案（量化边界 11% / 不排除会高估 /
  机制同源 / 设计含义），且导师 08-08 原话说「恰恰可以在 RQ 中进行专门的分析，
  也是重要的 finding」。**当前决定与导师建议有张力**，成稿前确认一次。
  ⚠️ **而且那个方案的第 ② 层在 v46 下无法复现**：它的论据是「`0018` 的 `hit@1` 66.7%
  高于全量均值 53.9%」，但 `00x8` 系列**在 v46 里根本没跑**。要把它写成 finding
  就得重跑被排除的 6 个 pair，而那与「它们不在研究对象内」直接冲突。
  ⚠️ 另：该方案 ① 的「11%」单位不自洽——1/10 份需求 = 10%，6/54 pair = 11.1%，两者被混用。

## B. 领域考据（导师点名要重点展开）

* [ ] **P0 · 补齐 19 个谓词的领域出处。**
  实测：**只有 3 个**挂了 `provenance` 注释（`occupancy_after` / `stays_in` / `persists_until`），
  **16 个空白**。全库 15 条标注里 6 条不可引用——「形式语义中的预设」×2、
  「需求工程通则」、「需求可追溯性通则」、以及 **2 条指向本仓库自己的 `CLAUDE.md`**。
  而 `docs/protocol/method_provenance_policy.md` R1 要求出处必须是**可查证的外部文献、
  标准或工具规约**，为空则「补出处或从方法章节移除」。
* [ ] **P0 · 修 `method_provenance_policy.md` R1 自己的漏洞。**
  它的示例里就写了「`#: provenance: 需求工程通则 —— …`」这种不可查证的写法，
  难怪实际标注里出现了 4 条同类。规范自身要先自洽。
* [ ] **P1 · 建 19 行谓词→领域来源映射表。** 列：
  `谓词 | 族(S/B/P) | 归纳自哪类领域来源 | 具体文献/标准锚点 | 在 $M$ 上如何实例化 | 该来源类下未实例化的部分`。
  最后一列是 RQ1「表达力边界」的直接输入。
  候选来源类（**AI 凭记忆给出，必须自己核**）：Dwyer/Avrunin/Corbett ICSE 1999
  property specification patterns、Autili et al. TSE 2015、Konrad & Cheng ICSE 2005
  real-time patterns（⚠️ 整族未实例化，因 $M$ 无 $C$ 与 $Inv$）、OMG UML superstructure
  状态机约束、Egyed 一系 model consistency rules、IEC 61131-3 / 61499、ISO 26262。
* [ ] **P1 · 查 OMG PSSM（Precise Semantics of UML State Machines）。**
  它是 6 个仿真族谓词最正当的规范出处，**全库一次未提**。
* [ ] **P2 · 处理 4 个从未被激活的谓词。**
  `variable_declared` / `variable_delta_after` / `invariant` / `response_within`
  在实测中一次都没被用上（`response_within` 在 324 格里零生成）。
  补出处时这四个也要挂，否则审稿人会问「为什么词表里有它们」。
  ⚠️ 但**不要**据零使用就退役——见 D 组「查清 BMC 为什么用得少」。

## C. 文献与 baseline 考据

* [ ] **P0 · 决定 `baselines/` 是改口径还是分库。**
  它是为 **NL→STM 生成**建的，四条件里 `STM族输出` 要求输出是状态机，
  而 detection 的输出是 issue 报告——**天然被 gate 挡掉**。
  2327 篇的 arXiv 普查也是按这条轴筛的。91 篇里只有 **7 篇**仍直接相关，
  且**没有一篇的被检对象是状态机**。
  踩点倾向**分库**（现有字段体系全为生成侧设计），但这是结构决定，需人定。
* [ ] **P0 · 补检索：断言 / 契约 / 可执行规约。**
  `baselines/` 匹配 `assert|contract|ocl|invariant` 的目录数 **= 0**。
  contribution 1 是一套断言体系，而它的**整片 related work 在仓库里不存在**。
  ⚠️ **必须正面对照 OCL/USE/Epsilon(EVL) 与 Dwyer 的 property specification patterns，
  否则 C-I 会被质疑成「重造 OCL」。**
  关键词簇：`"OCL" + ("well-formedness" | "constraint checking")`、
  `"design by contract" + model`、`("executable specification" | "runtime verification") + statechart`、
  `("specification pattern" | "property specification language")`、
  `("assertion generation" | "invariant inference" | "specification mining")`。
* [ ] **P1 · 补检索：错误定位与上下文 / 回归防护。**（服务 contribution 2）
  关键词簇：`("counterexample explanation" | "error explanation" | "fault localization") + model checking`、
  `("error report" | "diagnostic message") + ("usability" | "actionability")`、
  `("false positive" | "triage" | "review burden") + static analysis`、
  `("regression verification" | "proof reuse" | "incremental verification")`。
  ⚠️ 「**静态分析告警的复核成本与误报代价**」这一族是 contribution 2 最硬的实证证据来源，
  三个库里**一篇都没有**。价值高于再多找几篇 detection 方法论文。
* [ ] **P1 · 补检索：状态机上的 detection。**
  `baselines/` 里一篇都没有；`state_machine_types/`（679 篇）里有 **172 篇**命中
  model-check / verify / conform / diagnos / debug / test，但那个库按「形式主义地图」
  的轴写的，DESC 字段不记「输出带不带需求侧归因」。
* [ ] **P2 · 给 `state_machine_types/` 加一层 paper1 面向的派生视图。**
  逐条记录：能担哪些谓词 / 输出物形态（反例 trace / 布尔 / 状态集）/ **输出带不带需求侧上下文**。
  ⚠️ 但该库 README 明写「纯验证算法论文不应在这里扩张」——加视图前先定 owner。
  替代方案：只把最相关的 20–30 篇复制条目引用进 paper1 的 related work 工作区，不动原库。
* [ ] **P2 · 给 `corpora/repair_baselines/` 加 detection/repair 标注列。**
  24 篇里 **13 篇是 detection-bearing**，尤其 Egyed 那条线的四篇正是 contribution 2 的
  **靶子文献**。⛔ **不要整体移走**——移走等于把 Intro 的引文移走。
  ⚠️ 目录名带 `repair` 而论文不做 repair，改名要动 29 处链接，与标注列一起做。
* [ ] **P3 · 修 `reproduction/` 的死链。** 它的 README/GUIDE 仍引用 5 个已被拆去
  `project_ex1` 的路径（commit `67b4997a`）。

## D. 实验与测量

* [ ] **P0 · 补朴素基线。** 当前**没有任何外部对照**，60.4% 缺参照系。
  同两个执行模型、同 54 pair，不走八阶段循环，单提示直接列不符之处。
  ⚠️ **成本被低估过**：算力上确实小（324 次单提示 vs 3621 次多阶段），
  但它同样需要**一整轮 588 位判定**——那是本项目最贵的人工投入；
  且基线产出是自由文本、无断言，`verdict_tiers.py` 的 A/B 层大概率整体失效。
  跑之前必须先选定减负路径。
  ⚠️ **朴素基线 ≠ M0–M3 稻草人消融**：前者是**外部参照系**，后者是对手臂。
  M1/M2/M3 已被降为 future work，但基线不能跟着一起砍。
* [ ] **P0 · 交代台账的撰写时序。** 谁标的、什么时候标的、**是否在看过方法产出之后标的**、
  与命中判定是否同一人。⚠️ **若时序上晚于方法产出，60.4% 就不是覆盖率而是自相关。**
* [ ] **P1 · ref 翻转率实验。** 把为 pair X 生成的整套断言，拿去在同一份 NL 的**参考模型**上
  重新执行。预期：在错误模型上为 False 的断言应在参考模型上翻成 True。
  三个指标全部**零人工判定**：翻转率（判别效力）/ 残留 False / 参考侧误报。
  价值：`EIS-0029-05` 那条改判的理由逐字是「这条在参考模型上同样为 False——
  一个无法区分合规与不合规制品的断言不构成该缺陷的证据」，人工在 132 个位上发现 1 例，
  **这个检查能自动化到全部断言**。它同时是「回归防护」那条贡献的实证支撑。
  ⚠️ 引用该例时注意：「132 个位」是 **v35 口径**，不是 v46 的 588 位；
  引用前必须回 v46 裁定记录核对，且不要与报告 §3.3 那条 boundary-ruled 记录
  （`EIS-0043-02`）混谈。
  ⚠️ 「残留 False」这一格**二义**（断言写错 or 参考模型也有该问题），
  用作判别效力指标前必须先约定读法。
  ⚠️ **风险已重新定位**：参考模型**不是**阻塞——实测 `Experiment Results.xlsx / STM Results`
  第 D 列（表头 `PlantUML`）**60/60 行非空**，`source_meta.json` 的
  `source_cells.reference_plantuml` 直接给出单元格，`pairs.jsonl` 带 sha256 可校验；
  规范化后恰好 10 份、在用 9 份。**真正未测的是 PlantUML → DSL 的编译成功率**——
  而参考模型是人写的、写法分布与 LLM 生成的不同，且这条链已被证明有损（46.5%），
  **参考侧的编译损失会直接污染「残留 False」这个指标**。
* [ ] **P1 · 表示债务的第二判定者盲判。** 46.5% 那一整块靠「人工回读作者源」认定，
  而该步不可机械复现、目前单人判定。抽 30 簇给第二人盲判、报一致率。
* [ ] **P1 · 命中形态的构成。** 四种等价形态中「蕴含更根本的原因」最宽。
  355 位按四形态拆开各多少？若相当比例靠最宽那一档，这个数的性质就变了。
* [ ] **P2 · 拒答文案回灌量的量化。** 同一机制在方法一节是设计优点、在上界一节是虚高成因，
  且尚未量化。从逐次调用记录里数：多少条已发布 issue 的断言是在收到拒答反馈之后才改成现在形状的。
* [ ] **P2 · 查清有界模型检查为什么用得这么少。** 只有 4 条记录用到、占命中 4.2%；
  3 个谓词里 `response_within` 零生成、`invariant` 台账零引用。
  三个候选原因**指向相反的行动**：① 建模边界不含不变式（那 `invariant` 该退役）；
  ② 语料确实少这类义务（那是语料问题）；③ 生成侧从未识别这类句式（那该补生成路径）。
  判别方法：人工通读 9 份需求，找出全部「响应性 / 持续性」义务，看两侧各表达了多少。
  ⛔ **在这件事做完之前，论文不得主张 BMC 必要，也不得据零使用就退役。**
* [ ] **P2 · 把命中位按「实际由哪一族断言支撑」重算。**
  当前族归属来自**台账侧标注**，而**产出侧 86.6% 的已发布断言是结构族**，两者不一致。
  ⚠️ **阻塞**：逐位判据是自由文本、无结构化 issue 引用，算不出来。
  要做需先改判定记录格式。
* [ ] **P2 · 循环各阶段的消融。** 八个阶段哪些必要？尤其两个审查阶段与静态预检——
  它们占算力大头却没有单独的收益证据。
* [ ] **P3 · 补齐 20 位缺逐位判据的判定。** 588 位中 568 位有判据、20 位无
  （15 位命中、5 位未命中），不可逐格复核。

## E. 口径与规范

* [ ] **P1 · 裁定 `wellformedness_attribution.md` 到底生效了没有。**
  它列在 `discover_matrix/README.md` 的「生效中」，但正文说「尚未改动任何已发布数字，
  一旦生效需同时更新 v22–v24」，又给「对 v25 的直接含义」——而当前是 v46。
  三种可能：早已生效且回填已做 / 早已生效但回填没做 / 被后续代次取代。
  ⚠️ 这条影响 `wellformedness` 层 48.1% 这个数字的口径归属。
* [ ] **P1 · 「一条 issue = 一个缺陷」的操作化定义要不要改。**
  代码里写的是「**一次模型编辑**能否同时解决」——`schemas.py:1008` 的
  `a single model edit resolves all of them`、`prompts.py:143` 的
  `would fixing that one place make both False results go away?`、`:151`。
  而 `docs/protocol/hit_criterion.md:60-62` **明令禁止**用同一句话当命中判据
  （理由：会误杀「合取项之一」与「蕴含更根本的原因」两种形态）。
  两者判的不是同一件事，不算矛盾，但**论文得解释为什么一处禁用一处依赖**。
  ⚠️ 现成的替代措辞就在 `hit_criterion.md:62`：「两者陈述的是不是同一处建模失误」。
  ⛔ 但改它属于**会影响模型行为的 prompt 改动**，按 `CLAUDE.md` §3.5.0
  必须先过运行前 review，不能算文档整理。
* [ ] **P2 · `unexpected_taxonomy.md` 的 `N-SPLIT` 判据去 repair 化。**
  `:348-350` 把「这条断言若被采纳去修，修出来的对不对」立为**唯一判据**，
  还专门排除了不依赖修复的替代判据。`:169-173` 的分叉表列名就是「拆开是不是正确修法」。
  ⚠️ 好消息：`:350` 已经把不依赖修复的等价理由写出来了——
  「把 AND 变成 OR，比现状更违反 NL」。所以改写是**纯措辞、不改任何判定结果**的。
* [ ] **P2 · `hit_criterion.md:86-88` 的一处 affirmative 用法。**
  「模型给的**修法**会把它一并搬走或删掉」——真正的判据是「严格超集且超出项是台账认定的
  正确元素」，改写掉「修法」二字不改结论。但它泄露了一个假设：**发布的 issue 里带有可供检视的修法**。

## F. 工程与结构

* [ ] **P2 · 决定 `pipeline/evaluation/` 的去留。**
  两份 v0 schema 是死的（`feedback_loop` 零 import），`source_issue_ledger.schema.json`
  必填 `downstream_repair_allowed`，且 schema 层强制「`confirmed` ⟺ 允许下游修」——
  这是「issue 分级按可修复性分」的最赤裸形态。
  ⚠️ **阻塞**：`pipeline/conversion/src/paper_stm_repair_conversion/evidence_integrity.py:17`
  把它列在 `IMPLEMENTATION_ROOTS` 里，其 SHA-256 汇总就是 60-pair 表示层证据的
  `generator_cli_sha256`。**移动或删除会改变一份已冻结证据的哈希。**
  先查：那个 `generator_cli_sha256` 有没有被写进已发布 gist / PR comment / publication seal？
* [ ] **P2 · 决定 `pipeline/agent_loop/` 是否归档。**（219 文件）
  ⚠️ 纠正一个常见误解：它**不含 repair**——没有 repair agent / prompt / stage，
  只是上一版单 Agent **discover**。
  支持归档：已被 `Makefile` 改名 `legacy-*`、被 import 门禁止、CI 不跑它。
  反对：当前 `assertions/` 五个文件的 docstring 都写着
  「ported from legacy agent_loop eval_env at commit …」，移动会切断 provenance 链。
  代价：`Makefile` 3 处路径常量、`test_import_boundaries.py:49` 的路径字面量断言、7 处文档。
  **CI 影响为零。** 倾向归档但优先级低。
* [ ] **P3 · 四个 Python 包名未改。**
  `paper_stm_repair_loop` / `_smoke` / `_conversion` / `_representation`。
  它们是包名不是目录名，约 150 处引用（含仓库根 `tests/utils/test_llm_model_factory.py`
  的负向断言）。另开一轮做。
* [ ] **P3 · `manual_review/eis_issue/*.md` 的死链。**
  `boundary.md` / `coverage.md` / `gate_detail.md` 里的 GitHub blob URL 含旧路径。
  它们是 `render_eis_issue.py` 的**派生物**——⛔ 改真源不改派生物，
  下次跑该生成器时一并覆盖。

---

## 已完成（2026-08-11 本轮）

* [x] PR 链从四层塌成一层，两个被自动 merged 的 PR 各留说明状况 + 指路 comment
* [x] `paper_stm_repair/` → `paper_stm_issue_discover/`，实验资产收归论文目录
* [x] 三条旧路线归档（旧 agent loop / Path-1 评测链 / Path-1&2 指南），各配复活导引
* [x] 43 份平铺 md 树化为 `protocol/` `judges/` `findings/` `generations/` 四类
* [x] 补建 2026-08-08 导师讨论正式记录；`talks/SUMMARY.md` 同步新定调
* [x] 重构后 e2e smoke 验证（`0000` × 双模型，输入哈希与搬迁前逐字节相同）
* [x] 更正 `CLAUDE.md` §5 与根 `README.md` 的 LLM 配置机制描述（真源是 `.llmconfig.yml` 不是 `.env`）
* [x] 修正 v46r 替换后遗留的旧分母数字（41.3/54.0/16.1/4.0）与两处事实错误
      （净增量 2 条、九个判定组全部回读作者源）
* [x] 修复重构造成的 82 条净增死链，净增归零
* [x] `story/` 与 `experiment_design/` 归档并留 placeholder（本清单即其产物）
