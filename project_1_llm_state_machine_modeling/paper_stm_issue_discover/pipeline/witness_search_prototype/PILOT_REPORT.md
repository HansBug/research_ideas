# Paper1 可执行见证发现方法：原型实验报告

## 1. 目标与结论

本轮要回答的不是“能否多找几个 L2”，而是“NL 契约 + 互补双 B discovery + 固定 proof compiler + 独立 D 裁决”能否在当前已实现的 L0/L1/L2 子集上产出真实运行的 W2，并在不读取台账和 X1v2 的运行时边界内形成可审计证据。当前结论是：方法骨架已经具备端到端可行性；最新 0029 v36 fresh 的 39 条 finding 全部具有 D/W/L，16 条 W2 全部真实执行，开发样例 strict accepted 为 8/8 且 8 条均 W2，成本为同模型 X1v2 的 `17.68×`。但该 pair 已深度参与方法开发、accepted report 尚未盲判、新双边 oracle 的自动触发仍有方差，而且 145 条逐条表达面审计尚未完成，因此不能声称完整表达面、整体显著超过 X1v2 或 precision 已改善。

当前唯一 baseline 是 X1v2 在 145 条第二版台账上的 `hit@1=59.8%`、`hit@all=47.9%`；L2 为 `43.6%/30.8%`，D2×L2 为 `40.2%/29.4%`。正式成功门保持为 overall `hit@1` 至少高 5pp 且 pair-clustered bootstrap 95% CI 下界大于 0，同时 overall `hit@all` 提升；分层结果和 precision 必须并列报告，不能用 D2×L2 的局部优势代替 overall 优势。baseline 事实源见 [X1V2_RESULTS.md](../../discover_matrix/ledger_v2/X1V2_RESULTS.md)，完整方法合同见 [METHOD_DESIGN.md](./METHOD_DESIGN.md)。

## 2. 方法与阶段

方法固定为三个 pair 级 LLM 角色。LLM-A 只读 numbered NL，抽取 initial、containment、direct transition、required state 和 required event scope 合同；LLM-B 在同一冻结输入上运行 `contract_structure_contrast` 与 `behavior_consequence` 两个互补分支，分别偏重契约/结构/跨边对照和可达性/响应/终止后果，开放候选取结构化并集；确定性 compiler 只按结构化 `EvidenceGoal` 与正式 ID 路由 source/FCSTM AST、guard SMT、topology 和 trace/BMC 后端并真实执行；LLM-C 最后按固定 8 条 finding 一批调用，但逐 facet 输出 D2/D1/D0。W 与 L 由执行结果和 proof relation 机械派生，LLM 不写 Python、不选 backend/template/predicate，也不输出 W/L。

运行时严禁对 NL、claim、label 或 identifier 使用关键词、substring、`and/or`、词干、编辑距离、embedding、suffix 或唯一候选补全做语义判断。确定性层只处理形式语法、AST、精确 ID、图、SMT、trace、hash、预算和逐字引用出处；逐字 quote span 只证明引用来自输入，不证明语义蕴含。非确定语义必须由具名 LLM 节点输出并保存 prompt、raw/structured output 与 usage；无法绑定时进入 rejected/unresolved 或 W1/W0，不得用字符串代理补答案。

同一纪律适用于 schema：自由文本 reason 的长度和措辞不是可完美判定的语义合同，不得触发 repair 或整格失败。0048-v4 的 LLM-B 首次输出在语义上可用，却因三个 reason 超过 320 字被 Pydantic 拒绝并额外消耗一次完整调用；当前原型已删除全部 semantic-grounding reason 的任意最大长度，并增加长文本无需 repair 的回归。后续成本统计必须把这种 schema 设计缺陷视为方法实现缺陷，而不能归因于模型“不听话”。

## 3. 运行设置与质量控制

真实 pilot 使用 `claude-opus-4-7` profile 和仓库 `utils.llm` 配置机制。成本只使用 `.llmconfig.yml` 中 input、output、cache read、cache write 四个 USD/M token 单价；同一 configured model 内比较方法与 X1v2 美元成本，单 pair 硬门为 25×，不要求跨模型可比，也不试图复现供应商峰谷、长上下文、TTL 等全部账单细节。每次运行保存 immutable stage record、LLM observation、compiled assertion、artifact/assertion hash、execution receipt、semantic-binding receipt v2、source causality certificate、D decision、四类 usage 与美元 eligibility。LLM receipt 以 hash chain 绑定真实 call、prompt、raw/parsed output、semantic/grounded plans、候选和 formal binding transforms；run-level audit 再与同一 record 对拍。formal scout 只输出 exact `FormalFact + OracleRule ID`，不解析 diagnostic message，规则是否适用于当前需求仍由 LLM-C/reference judge 裁决。

## 4. 开发性结果

四个 development pair `0004/0016/0046/0059` 的严格 post-hoc 初判共命中 12/15，即 80.0%；命中的 L0/L1/L2 各 4 条，D2/D1 为 9/3，12 条全部得到 source-attributable W2。X1v2 在同一小集合的六格 cell-wise `hit@1` 为 37/90，即 41.1%，方向差 +38.9pp；四个 run 平均成本为 X1v2 单格均值的 19.80 倍，最大 22.32 倍。该结果只说明表达能力和端到端机制值得进入 confirmatory 阶段，因为 pair 已影响 prompt/compiler、当前方法每 pair 只有一次运行且未经过环外 blind precision judge；逐条证据见 [METHOD_DESIGN.md](./METHOD_DESIGN.md) §7。

0048 是从未读取 NL、PlantUML、ledger 或 baseline 的 hash-selected pair。v1 在 LLM-B 后因“16 条 raw transition contract + 3 条 additional contract”错误复用有界 LLM schema 而崩溃，失败审计见 [failure.json](../../../../runs/paper1/witness-search/0048-v1-hash-selected-fresh-opus47/failure.json)。修复引入无损 `GroundedContractPlan`，并把 grounding 内部错误改为诊断降级；`16+3=19` 的不丢失回归已通过。v2 完整 record 见 [record.json](../../../../runs/paper1/witness-search/0048-v2-grounded-union-fresh-opus47/record.json)：形成 29 个 outcome、6 个 report，6 条全部 W2，D2/D1 各 3 条，L0/L1/L2 为 2/3/1，3 条进入 confirmed。

0048 在当前 145 条台账中没有条目，因此这次运行的 hit 分母为 0，不能贡献 recall 结论。更重要的负面证据是：LLM-B 已把 `Junction3` composite-initial 与 `Fork2 -> Terminate` 两个 raw contract 标成 plan artifact/错误源端，但旧 binding schema 仍要求给 formal binding，assembler 继续执行后分别得到 D2/W2 与 D1/W2。该结果证明“断言真实运行 + source 双证书 + D”仍不能挽救错误的规范前提。由此新增的结构化 `grounded/rejected/unresolved` resolution 让 LLM-B 可以否决 raw contract，assembler 只读枚举状态并停止编译，绝不解析 reason 文本。

0048 v2 的三个成功 provider attempt 记录了 53,139 token，即 24.58 倍；但 LLM-A 与 LLM-B 各有一次 schema-repair 首次尝试未暴露 usage，所以真实成本未知且可能超过 25 倍，run 按规则 `eligible=false`。它可以用于机制失败分析，不能进入成本或效果主结果。

最新 `0048-v6-receipt-v2-oracle-rule-fresh-opus47` 不 replay 旧 plan，恰好完成 3 次调用且无 schema repair，三次 usage 为 10,810、34,682、7,175，总计 52,667，即 24.36×；usage 完整、token gate 与 semantic provenance audit 均通过。它产出 5 条 finding，其中 `Fork2 ⊂ Join2` 为 D2/W2/L1、`Join2 -> Join1` 丢失 `sunny=true` condition 为 D2/W2/L1、`choice1` reachable deadlock 为 D2/W2/L2，另两条为 D0/W1。所有 LLM-grounded W2 receipt 都回指真实 LLM-B call 且 plan hash 闭合。LLM-A 这次没有生成旧 run 的 `Junction3` initial 错契约，所以只能记录“错误前提未进入执行层”，不能夸大为“LLM-B 成功拒绝”。0048 没有台账分母，v6 仍不支持 recall/precision 主张。

0029 的双 B 收敛过程提供了更直接的架构证据。v34 replay 在候选隔离修复后得到 42 条 finding、16 条 accepted、10 条 confirmed，开发样例 strict accepted 为 8/8 且全部 W2，成本 `18.27×`；v35 完全 fresh 得到 46 条 finding、14 条 accepted、5 条 confirmed，成本 `17.27×`，但 cruise 错目标和稳定终止分别因缺少参照边与错误 claim 被 D0。v36 加入 `transition_target_consistency` 与稳定终止 D 纪律后完全 fresh，8 次调用均完成且 0 次 D schema repair，形成 39 条 finding、15 条 accepted facet、14 条 accepted report、6 条 confirmed report；全量为 `W2/W1=16/23`、`D2/D1/D0=6/12/21`、`L0/L1/L2=27/5/7`，成本 `$1.27404`、即 `17.68×`，semantic provenance audit 与 25×门均通过。post-hoc strict accepted 为 8/8 且全部 W2，其中 cruise 错目标为 D2/W2、稳定终止为 D1/W2；已知的 lane_change→FinishState 错误报告没有出现。T13 后端已在确切 0029 FCSTM fixture 上真实执行双边断言，但 v36 两个 B 分支都没有完整给出被测边、参照边和规范目标，所以这项自动 discovery 能力尚未稳定。

## 5. 当前支持与不支持的主张

当前证据支持：开放语义目标可以被固定 compiler 转成真实执行的 W2；source/FCSTM 双证书能区分作者源缺陷与 representation debt；D、W、L 可以逐 finding 独立生成；互补双 B 能在开发样例上同时保住 L0/L1/L2 的 strict accepted 8/8；完整 fresh 仍能保持在同模型 X1v2 的 17–18 倍成本；对 raw contract 的显式语义否决和逐候选隔离是控制 false positive 与防止证据丢失的必要组件。

当前证据不支持：整体 hit 已显著超过 X1v2、precision 已改善、L2 大部分已稳定发现、25 倍硬门在所有 pair 上都可满足、当前 D 可替代外部真值、19 个旧谓词足以覆盖开放世界问题，或当前 25 个 Goal relation 已经覆盖全部/大多数 145 条台账。尤其 12/15 来自 development data，0048 没有台账分母，所有 unmatched finding 仍需环外 blind semantic judge 按“同位置 + 同性质”或新缺陷有效性裁决；已知 expression gaps 与领域先行构建协议见 [EXPRESSION_SURFACE_AUDIT.md](./EXPRESSION_SURFACE_AUDIT.md)。

## 6. 正式实验设计

运行前冻结 prompt/compiler hash、pyfcstm commit、development pair、confirmatory remainder、matching protocol、budget policy 和 candidate/report clustering。主实验在完整 145 条台账上至少执行一个模型的三轮；每条输出 W/D/L/source-attribution/attempt count，分别报告 overall、L0/L1/L2、D×L、`hit@1/@3/@all`、precision、method-D/reference-D confusion、W2 fraction、mutation-surviving fraction、每个 external-valid issue 的 token、mean/p95/max cost 和 degraded grid。X1v2、budget-matched repeated-X1 与 mutation benchmark 必须并列，消融分别移除 NL contract、semantic grounding、mapping/inspect、formal execution、source gate 和 D adjudication。

confirmatory matching 必须在方法环外进行。判读包只给台账条目与匿名 report，不给方法臂、baseline 命中、prompt 规则来源或 method D；LLM/human judge 逐条判“同位置 + 同性质”，unmatched report 另判 reference D。runtime 不得导入 ledger/X1v2，文本相似度或字符串规则不得参与 matching。

## 7. 下一步

下一步先按领域与元模型来源建立 obligation taxonomy、补齐每个 Goal/template/backend 的 provenance，并完成不反向调优方法的 145 条逐条 feasibility audit；同时冻结 `grounded/rejected/unresolved`、receipt v2、OracleRule registry、prompt/compiler hash 和 development/confirmatory 划分。之后选择小型事前登记批次估计 semantic-veto precision/recall、schema-repair 率、overall/L0/L1/L2 hit 与 blind precision。若平均成本仍接近 25 倍，优先压缩重复的 discovery dossier 与 D dossier，而不是删除影响 overall recall 的 discovery lane。只有在表达面边界明确、小批次无内部崩格、usage 完整、W2 provenance 完整、overall 相对 X1v2 明显正向且 blind precision 可接受后，才进入完整 145 条正式运行。
