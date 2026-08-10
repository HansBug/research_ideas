# GUIDE.md — 本工作区的工作纪律

> 本文件约束后续 agent 在 `paper_stm_issue_discover/` 内怎么读、怎么改、怎么验收。
> 它不是 [README.md](./README.md) 的重复版——README 说「这篇论文是什么」，本文件说「怎么干活」。

## 1. 默认阅读顺序

1. [README.md](./README.md)：口径基准。这篇论文做什么、两条 contribution、建模对象边界、目录导航。
2. [STATUS.md](./STATUS.md)：已完成 / 未完成事实，以及当前不可声称的话。
3. 本文件：工作纪律。
4. 按任务分叉：
   - 写论文 → [story/README.md](./story/README.md)
   - 看结果、复算数字 → [discover_matrix/README.md](./discover_matrix/README.md)
   - 改方法 / 谓词 / 提示词 → 先读 [discover_matrix/docs/protocol/](./discover_matrix/docs/protocol/)，再动 [pipeline/feedback_loop/](./pipeline/feedback_loop/)
   - 查某个 pair 的原文 → [selected_seed_examples/](./selected_seed_examples/)

⛔ **施工流程状态**（PR 进度、review 状态、CI、子 PR 排期、commit 汇报）以 GitHub PR / issue
为准。本工作区**不维护**任何动态施工台账，见仓库根 [CLAUDE.md](../../CLAUDE.md) §9。

## 2. 事实源优先级

冲突时按此顺序裁定，上位覆盖下位：

| 级别 | 来源 | 管什么 |
| --: | :-- | :-- |
| 1 | 用户当前明确指令 | 一切 |
| 2 | 2026-08-07 / 08-08 导师定调 | 论文收窄、两条 contribution、RQ 设计原则、修复不展开。⚠️ 口头，原话摘录在 [README.md](./README.md) §2 |
| 3 | [discover_matrix/docs/protocol/](./discover_matrix/docs/protocol/) | 判定口径、方法出处口径、建模对象边界判据。**改它们等于改研究规则** |
| 4 | [../talks/2026-08-10-实验-v46全量矩阵双侧结论.md](../talks/2026-08-10-实验-v46全量矩阵双侧结论.md) | **全部实验数字的唯一来源** |
| 5 | [README.md](./README.md) / 本文件 / [STATUS.md](./STATUS.md) / [story/](./story/) | 口径、纪律、状态、叙事 |
| 6 | [../talks/](../talks/) 的更早导师记录、[reports/](./reports/)、[archive/](./archive/) | 历史背景。被后续记录覆盖的部分不得作为 active 依据 |

⚠️ 级别 3 与 4 的分工：口径文档说「怎么判」，报告说「判出来是多少」。
改了口径就必须说明它对已发布数字的影响；只改报告数字而不改口径，或反之，都是错的。

## 3. 论文口径纪律

### 3.1 硬约束

1. **本文只做发现，不做修复。** repair 另立后续论文。修复只在讨论一节**一小段**捎带提及，
   不展开、不承诺效果、不给数据。
2. **两条 contribution 的措辞以 [story/paper_story.md](./story/paper_story.md) §6 为准**，
   顺序不得调换：谓词逻辑元模型与断言体系 > 带上下文的发现。
3. **贡献不是「发现了多少问题」。** 覆盖率是支撑贡献的证据，不是贡献本身。
4. **谓词词表的由来一律表述为「从领域分析、真实文献与技术资料调研归纳而来，应用于 54 个案例，
   并据此指导 prompt 设计」。** ⛔ 不表述为「从这批 pair 归纳」；
   ⛔ 论文里不解释留出集——那个问题在本方法的论证结构里不出现。
5. **建模对象边界只在问题定义处出现一次，一句话带过。** 不展开辩护、不做成 RQ、不在后文重提。

### 3.2 ⛔ 已作废、不得回流的表述

多轮 Repair-Confirm、B-final、post-Confirm export、closure / regression audit 作为主线、
「loop + verification feedback 是 headline contribution」、Better STM / which STM is better、
`fcstm` / `pyfcstm` 作为贡献、ledger / audit 作为贡献、conversion gain。

⚠️ 这些词可以出现，但**只允许在解释历史转向、或标注为已作废的语境**里出现。

### 3.3 RQ 纪律

每个 RQ 必须能回答「它验证哪条 contribution、扣住问题定义的哪个特征」。
⛔ 无归属的 RQ 不设；⛔ 无数据的 RQ 不写（当前已被排除的一条：回归防护面规模）。
不为了「多做一个实验」而增设 RQ，也不为了覆盖模型数量而堆执行模型——
导师明确「选择几个代表性的就可以了」。

## 4. 数字纪律

1. **每一个数字都回报告核对**，不从任何派生文件（含 story/、本文件、旧报告）转抄。
2. **覆盖率必须带 $\le$**，必须三口径（`hit@1` / `hit@3` / `hit@all`）同报，
   必须与算力代价同报。⛔ 不得写成点估计或区间估计。
3. **多报侧必须同时给两套分母**（条目 / 去重）。两套给出相反的主要矛盾，只报一套会把整改
   资源投错地方。⛔ 条目与去重的份额不可互换，引用时必须写清用的是哪一套。
4. **分母不同质的量不可相除**：逐格 issue 数与簇数、台账记录数与簇数，都不构成比率。
5. 跨代次比较必须**同分母**（同格集、同判据）。
6. 涉及台账的数字必须连带说明它的已知缺口——所有覆盖率都读作「在一个已知不完整的分母上的」。

## 5. 实验公平性纪律

以仓库根 [CLAUDE.md](../../CLAUDE.md) §3.5 系列为准，本地补三条落法：

1. **台账与参考模型不得进入运行时。** 只允许在图终止之后用于评测侧审计。
2. **泄漏审查必须覆盖运行期生成的文本**——门反馈、渲染说明、拒答文案。
   静态 grep 源码里的 prompt 常量抓不到它们，而它们恰恰只在相关样本上触发。
3. **每条规范性规则必须挂可查证的外部出处**（标准条款、工具规约、文献），
   写在源码注释里回答「它凭什么成立」；**引入动机写在提交记录里**回答「什么时候发现要加它」。
   两者不得互相冒充。见
   [discover_matrix/docs/protocol/method_provenance_policy.md](./discover_matrix/docs/protocol/method_provenance_policy.md)
   与 [discover_matrix/docs/protocol/rule_provenance.md](./discover_matrix/docs/protocol/rule_provenance.md)。

⚠️ **运行前 review 与运行后 review 分两段，职责不可互替**：前者查代码正确性与实验公平性，
不通过则**禁止开跑**；后者查数字可复算与因果归因，不通过则报告就地更正。

## 6. 术语纪律

术语裁定表在 [story/terminology_policy.md](./story/terminology_policy.md)。四组最易混的，
在此重复一遍，因为它们都实际发生过误读：

| 组 | 区分 |
| :-- | :-- |
| 作者 | **生成被评审模型的 LLM**；人类一律称「上游论文作者」 |
| 模型轴 | **生成方**（6 个，属语料，不控制）vs **执行方**（2 个，跑我们的方法） |
| 过度规定 | 台账归因层 `over_specification` = **被评审模型**多写了；多报侧「无需求依据」= **我们的断言**多要了。**方向相反** |
| 计数单位 | 逐格 issue / 簇（条目）/ 去重组，三层，分母不同质 |

## 7. 归属纪律

| 放哪 | 什么 |
| :-- | :-- |
| 本工作区内 | 与本论文直接绑定的一切：方法实现、语料、台账、实验、判定口径、报告、叙事 |
| project_1 顶层 | 只放**跨论文公共资产**（正式导师讨论文库、方法基础设施入口、评测审计入口） |
| GitHub PR / issue | 全部动态施工流程状态 |
| 仓库根情报库 | 模型价格 / 上下文窗口（[llm_model_landscape/](../../llm_model_landscape/)）、venue 与 deadline（[ccf_venues/](../../ccf_venues/)） |

⛔ **不得在本工作区新建** `progress.md`、`task-packets/`、`agent_provenance.md`
或任何充当 PR / issue 流程真源的文件。

⚠️ **已随 repair 一并搁置但文件仍在原地**的资产：
[experiment_design/issue_lifecycle/](./experiment_design/issue_lifecycle/)、
[experiment_design/source_trace/](./experiment_design/source_trace/)、
[evidence/ledgers/](./evidence/ledgers/)、[pipeline/agent_loop/](./pipeline/agent_loop/)。
它们只作历史背景与后续 repair 论文的迁移输入，**不得作为本文的方法或评价框架引用**。
本工作区内部的历史快照在 [archive/](./archive/)；已停用的旧路线（Path-1 评测链、旧 agent loop
基础设施）在 [../archive/](../archive/)，完整保留可复活，不参与本文任何结论。

## 8. 改动纪律

1. **改真源，不改派生物。** 判定表、统计表、gist bundle、报告表格多为脚本产出；
   改派生物会在下次重建时静默丢失。改完真源立刻重建并验证差异为零。
2. **文档大改必须在文末留一节「相对上一版改了什么、为什么」**，并把仍然有效的旧内容显式
   标为「保留 / 迁移」——重写不等于允许丢信息。
3. **结论更正一律就地改原件**，不另发更正件；原件内保留一节「相对上一版的改动」，
   只记改了什么、为什么，不复述错误结论。配套的 gist / bundle / 脚本产物必须同步更新。
4. 新增或修改任何 validator / 门之前，先回答两问：这条约束能否**只看字段值**唯一判定？
   被它拒绝的那一方**握不握有能改的那个字段**？两问答不上就不许加。
5. 新增一道会拒绝的门时，必须写出「满足本门且同时满足既有各门的一个具体形状」。

## 9. 验收清单

改完任何一份文档或代码后，逐条自查：

- [ ] 有没有引入 repair 口径（closure / regression / Repair-Confirm / B-final 作为主线）？
- [ ] 有没有把 loop、中间表示、ledger、audit 写成 contribution？
- [ ] 有没有把「发现了多少」写成贡献？
- [ ] 覆盖率是否带 $\le$、是否三口径同报、是否给了算力？
- [ ] 多报侧是否两套分母同报、是否写清用的是哪一套？
- [ ] 数字是否回 [../talks/2026-08-10-实验-v46全量矩阵双侧结论.md](../talks/2026-08-10-实验-v46全量矩阵双侧结论.md) 核对过，而不是从旧文件抄的？
- [ ] 「作者」「执行方 / 生成方」「过度规定」三组术语有没有混用？
- [ ] 建模对象边界是否只在问题定义处一句话带过，没有展开成辩护或 RQ？
- [ ] 新增的规范性规则是否挂了可查证的领域出处，而不是「某次运行暴露的问题」？
- [ ] 有没有把动态施工状态写进仓库文件？
- [ ] 文末是否留了「相对上一版改了什么、为什么」？
- [ ] Markdown 是否用相对路径链接、`$...$` 公式、emoji 列只放 emoji？

## 10. 静态检查

```bash
D=project_1_llm_state_machine_modeling/paper_stm_issue_discover

# 1. repair 口径回流（命中必须处于「已作废 / 历史 / 后续论文」语境）
rg -n "Repair-Confirm|B-final|post-Confirm|closure audit|regression audit|canonical source export|issue-grounded repair" \
  "$D"/README.md "$D"/GUIDE.md "$D"/STATUS.md "$D"/SUMMARY.md "$D"/story || true

# 2. 旧 headline contribution 回流
rg -n "Better STM|which STM is better|fcstm.*contribution|ledger.*contribution|conversion gain|headline contribution" \
  "$D"/README.md "$D"/GUIDE.md "$D"/STATUS.md "$D"/SUMMARY.md "$D"/story || true

# 3. 覆盖率写成点估计（命中处必须带 ≤ 或明确的上界说明）
rg -n "hit@1[^≤<]*=\s*60|60\.4%" "$D"/README.md "$D"/STATUS.md "$D"/SUMMARY.md "$D"/story || true

# 4. 多报侧只报一套分母（命中处必须同时出现条目与去重）
rg -n "46\.5%|54\.0%|24\.2%" "$D"/story "$D"/SUMMARY.md "$D"/STATUS.md || true

# 5. 误报率这类禁用读法
rg -n "误报率|false positive rate|precision\s*=" "$D"/story "$D"/SUMMARY.md "$D"/STATUS.md || true

# 6. 动态施工状态混入仓库文件
rg -n "ready to merge|等待 merge|本轮 CI|Codecov|subPR|sub PR" \
  "$D"/README.md "$D"/GUIDE.md "$D"/STATUS.md "$D"/SUMMARY.md "$D"/story || true
```

⚠️ 第 3、4 两条是**提醒式**检查而非硬门：命中不等于错，但每一处命中都必须能立刻说出
「它带了上界标记 / 它两套分母同报」。说不出就是要改的。

## 11. 相对上一版改了什么、为什么

| 改动 | 为什么 |
| :-- | :-- |
| §2 事实源优先级从「按文件顺序列 10 条阅读路径」改为**六级带裁定顺序的表**，并明确口径文档与实验报告的分工 | 旧版的 10 条阅读清单里有 4 条指向 repair 期合同（Issue #152、issue_lifecycle、source_trace、asset map），且没有冲突裁定顺序 |
| 新增 §3 论文口径纪律（含 RQ 纪律）与 §4 数字纪律 | 旧版没有数字纪律；而实验已完成，最容易出错的地方从「claim 漂移」变成「数字写错」 |
| 新增 §5 实验公平性纪律的三条本地落法 | 旧版只有一句「工程洁癖默认 M」；泄漏审查、出处挂钩、两段 review 是 v22 以来实际付过代价的地方 |
| 新增 §6 术语纪律的四组易混术语 | 四组都实际发生过误读，尤其两个方向相反的「过度规定」 |
| 新增 §7 归属纪律与 §9 验收清单 | 旧版无归属纪律；验收清单把散落各处的 ⛔ 收成一张可逐条自查的表 |
| §10 静态检查从「查 Better STM / source-level 旧术语」改为查 repair 口径回流、点估计、单套分母、误报率、动态状态 | 旧检查项防的是两代前的风险；当前风险已换 |
| 删除 §2 旧 active 主线（一次 Discover + 多轮 Repair-Confirm + B-final + C 阶段 closure audit 的完整生命周期图） | paper1 收窄为 discover |
| 删除 §3 旧术语表（raw/source `STM_0`、candidate / confirmed issue、canonical source export、B-confirm、closure / regression audit） | 全部是 repair 期术语；仍有效的部分已迁入 [story/terminology_policy.md](./story/terminology_policy.md) |
| 删除 §4 资产使用纪律的 `active / update / archive / historical` 四态表 | 该表依赖 `evidence/ledgers/paper1_strategy_asset_map.md`，而那份资产地图本身已随 repair 搁置；仍需保留的信息（哪些资产不得作 active 引用）已改写进 §7 |
| 删除 §6 PR 施工纪律（empty PR、三路 review、C/I 清零） | 属跨仓库通用流程，已在仓库根 CLAUDE.md §4 与 §9 维护；本地重复一份会形成第二真源 |
| **保留并迁移**：C/I/M 分级口径（工程洁癖默认 M，只有影响学术目标 / 事实准确性 / 证据链 / 可复现性的才升级） | 仍然有效，且是本仓库的 review 基线；现由仓库根 CLAUDE.md「学术研究仓库 Review 口径规范」统一维护，本文件不再复制 |
| **保留并强化**：review 必须做真实 dry-run | 现以 §9 验收清单的形态落地——清单本身就是 dry-run 的判据 |
| **保留**：历史 R5.7 / Better STM 资产只能作 historical / superseded / calibration-only 引用 | 改写进 §7 的搁置资产提示 |
