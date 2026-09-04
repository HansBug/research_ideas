# Paper1 结果处置清单

本清单只处置 v61（源–语义分歧审计与发布层规则包）与 X1v2 基线的规范指标（canonical metric），两臂的报告均由作者按同一协议人工裁定（大纲 §5.3）。每个标为 `included_in_main` 或 `included_in_appendix` 的指标，都已在[唯一论文大纲](./paper_outline.md)的相应段落解释；本清单不复制结果表，也不形成第二个结果真源。除另有注明外，规范来源指针为 `final_results/v61_source_divergence_vs_x1v2_baseline/derived/evaluate_rq3_output.txt` 与 `derived/evaluate_full_output.txt`，两者分别由 `discover_matrix/docs/generations/v61/evaluate_rq3.py` 与 `evaluate_full.py` 从归档的两臂裁定记录复算。v60 是前一代实现，其指标不再进入正文，其清单见本文件在提交 `1861969e7` 时的版本。成本按 2026-09-04 导师裁定不进论文。

| 指标组与冻结数值 | disposition | canonical source | 论文处理与限制 |
| --- | --- | --- | --- |
| 数据结构：9 个在用自然语言簇、每簇 6 个制品、54 pair、145 条 source-backed expected issues、3 rounds、435 round-level units | `included_in_main` | `discover_matrix/ledger_v2/ledger.json`；`discover_matrix/docs/protocol/nl_scope_rule.md` | 表 4 和第 5 节说明 54 不是独立描述数，435 是 145 条问题的三轮重复观测。 |
| 评测执行：两臂 903 / 512 条报告由作者按同一协议逐条人工裁定（两人独立裁定、分歧讨论至共识；relation-first 闭合；不报一致性系数） | `included_in_main` | 大纲 §5.2–§5.3；`discover_matrix/docs/protocol/`；v61 归档逐报告裁定记录 | §5.3 只写流程与闭合规则；§8 写非盲、同组作者的威胁。 |
| overall FULL `hit@1`：current `323/435=74.25%`，baseline `225/435=51.72%`；逐轮 113/98/112 对 75/71/79 | `included_in_main` | `derived/evaluate_rq3_output.txt` | 表 7 和 RQ1 主回答；只作本案例研究的描述性比较。 |
| L0/L1/L2 FULL `hit@1`：current `153/213=71.83%`、`73/105=69.52%`、`97/117=82.91%`；baseline `108/213=50.70%`、`72/105=68.57%`、`45/117=38.46%` | `included_in_main` | `derived/evaluate_rq3_output.txt`；L 取 `discover_matrix/ledger_v2/l_tier.json` | 表 7 分层行；L1 持平（条目层 10 赢 / 9 输 / 16 平）。 |
| overall FULL `hit@3` / `hit@all`：current `130/145=89.66%` / `82/145=56.55%`，baseline `105/145=72.41%` / `47/145=32.41%` | `included_in_main` | `derived/evaluate_rq3_output.txt` | 分母是 unique expected issues。 |
| L 分层 `hit@3` / `hit@all`：L0 `64/71`、`36/71` 对 `49/71`、`22/71`；L1 `30/35`、`18/35` 对 `31/35`、`18/35`；L2 `36/39=92.31%`、`28/39=71.79%` 对 `25/39=64.10%`、`7/39=17.95%` | `included_in_main` | `derived/evaluate_rq3_output.txt` | 表 7；39 是 L2 unique expected issues。 |
| supported coverage：round units current `355/435=81.6%`、baseline `257/435=59.1%`；unique IDs `135/145`、`117/145` | `included_in_appendix` | `derived/evaluate_rq3_output.txt` | 附录完整分层表；正文仅用于说明它不替代 PRIMARY FULL hit。 |
| reports：current `903`（5.6/格），baseline `512`（3.2/格）；current 含 32 条守卫模态聚合根（186 条成员）与 108 条携带 154 条折叠子主张的根报告 | `included_in_main` | `derived/evaluate_full_output.txt`；`derived/evaluate_rq3_output.txt` | 与 precision 同列，显示 coverage 增加伴随更多报告；折叠与聚合是发布层记账选择（§4.4、§7.2）。 |
| report validity precision：current `759/903=84.05%`，baseline `427/512=83.40%`，差 `+0.65 pp`；finding 级 `79.3%`（697）对 `81.1%`（449） | `included_in_main` | `derived/evaluate_full_output.txt` | §6.2 正文与表 8 / RQ2；这是报告级有效率，不是状态机语义真值率。 |
| K/N/I：current `561/198/144`，baseline `293/134/85`；K 中 D0 `81`、`24` | `included_in_main` | `derived/evaluate_rq3_output.txt` | RQ2；K 由 relation-first 闭合派生，不能把 K/N/I 当作缺陷类型。 |
| 命中来源分解（含子主张回执口径，分母 323）：分歧检查独占 `49`（L0/L1/L2 12/27/10）、谓词确认 W2 `137`（65/12/60）、谓词绑定未闭合 `36`（12/8/16）、纯语义 `101`（64/26/11） | `included_in_main` | `derived/evaluate_rq3_output.txt` | 表 7b、RQ1 第三问；回答「由谁承载」，不是因果归因。 |
| `pass` 回执 `573` 的谓词分布：S3 152、S2 150、S1 120、R2 78、R1 33、G4 15、S4 12、V4 7、R4 5、G1 1 | `included_in_main` | `derived/evaluate_rq3_output.txt` | §6.2 谓词的过滤作用；其精确率后果由 RQ5（`TODO-EXPERIMENT-02`）回答。 |
| 54 个制品规模：状态 5–20（中位 8）、迁移 5–70（中位 13.5）、守卫 0–14（中位 1）、复合态 1–7（中位 2）、深度 1–5（中位 2）；表 5b 按簇区间 | `included_in_main` | `discover_matrix/ledger_v2/provenance/corpus_structure.json`（排除 `00x8`） | §5.1 代表性段；与同类工作同量级、低于工业级。 |
| D2/D1/D0/A0：current `505/173/158/67`（FP 52、NADC 15），baseline `292/111/94/15`（FP 15、NADC 0） | `included_in_main` | `derived/evaluate_rq3_output.txt` | RQ2 的裁定组成。 |
| current I 组成：D0 且无关联 `77`、`FALSE_POSITIVE` `52`、NADC `15`；baseline `70`、`15`、不适用 | `included_in_main` | `derived/evaluate_rq3_output.txt`；`derived/per_predicate_and_ledger_report.txt` | 表 8；NADC 只报方法侧比率，不做跨臂比较，不重算校正精确率。 |
| D2/D1-only 敏感性：validity `678/903=75.08%` 对 `403/512=78.71%`；FULL `hit@1` `294/435` 对 `212/435`；`hit@3` `126` 对 `103`；`hit@all` `65` 对 `41` | `included_in_main` | `derived/evaluate_rq3_output.txt` | §6.2 保守口径；方向不变、精确率相对位置由持平变为低 3.6 pp。 |
| per-pair validity：current 平均 `80.6%`（min 0%：`0022` 6 条全无效；max 100%），baseline `84.1%`（min 33%） | `included_in_main` | `derived/evaluate_rq3_output.txt` | §6.2 一句话。 |
| N reports：current `198`（D2/D1 `114/84`）、baseline `134`（`79/55`） | `included_in_appendix` | `derived/evaluate_rq3_output.txt` | 跨轮、跨臂归并在 v61 上未重做，论文只报条数。 |
| W-on-hits：FULL 命中单元 `0/196/127`（根报告口径）与 `0/186/137`（含折叠子主张回执），L0/L1/L2 达 W2 `65/153`、`12/73`、`60/97`；报告级 `0/636/267`（分母 903）；baseline `0/225/0`，报告级 `1/511/0` | `included_in_main` | `derived/evaluate_rq3_output.txt` | 表 9；W 由程序按 §4.6 判定；发表层引文完整性审计未在 v61 上重做。 |
| 仅由分歧检查报告承载的 FULL 命中单元 `50`（L0 12 / L1 28 / L2 10）；分歧检查报告 `77` 条（K/N/I `59/4/14`） | `included_in_main` | `derived/evaluate_rq3_output.txt` | §6.3 解释 W2 份额；按构造 W1。 |
| receipt/binding 使用：terminal-receipt predicate IDs `12/19`（1114 条：`violation` 541、`pass` 573），`violation` IDs `9/19`，report-bound `8/19`（453 条报告），valid-bound `7/19`；W2 报告 × 谓词 S2 102、S3 66、V4 59、S5 22、G1 12、G2 3、S4 3 | `included_in_main` | `derived/evaluate_rq3_output.txt`；`derived/per_predicate_and_ledger_report.txt` | 表 9；distinct-ID usage，不是 defect coverage、边际贡献或 baseline 的等价零值。 |
| current method cost `$7.4903`（162 格全量，825 次阶段调用，含 `0045` r1 失败格）+ `$0.0616`（`0045` r1 重采样格）；baseline `$0.22523328` 为不完整小计 | `excluded_with_reason` | `raw/v61_current/method/summary.json`；`raw/v61_current_fill0045/summary.json` | 2026-09-04 导师裁定：成本节与价格数字不进论文，用量只留归档；提示工程质疑由两臂 prompt 结构并列图回应（§4.4）。 |
| 0045 第 1 轮：原格 `limit_exceeded: turns limit exceeded`（契约提取），重采样格替代 | `included_in_main` | `raw/v61_current/method/method/0045/round-1.json`；`raw/v61_current_fill0045/` | §8 威胁一句；两个记录都保留。 |
| 19 条谓词来源库存历史数 `313/310/454/361` | `excluded_with_reason` | `related_work/provenance/archive/legacy_20260821/SUMMARY.md` | 它们是来源库存/筛选规模，不是 prevalence 分母或本案例研究效果。 |
| v60 人工裁定指标（`310/435`、`77.10%`、W `0/142/168`、NADC 四路 overlay 等） | `excluded_with_reason` | `final_results/v60_current_vs_x1v2_baseline/` | 前一代实现；只作仪器校准参照与历史考据，不进正文；与 v61 的同仪器对照见 `discover_matrix/docs/generations/v61/analysis_and_options.md`。 |
| 显著性、总体效应和 population-level confidence interval | `excluded_with_reason` | 冻结设计与上述 canonical 输出 | 435 单元嵌套于 54 artifacts/9 NL clusters，且当前论文只报告描述性比较；不能按 IID 作推断。 |
| C1 inspect on/off 的 paired causal gain | `excluded_with_reason` | 冻结端到端比较与 `story/experiment_dependent_gates.json` | conversion、inspect、分歧检查与 C2 耦合；没有保持 conversion 不变的 paired switch 实验，不能从端到端差异识别任一组件的单独效应。 |
| 跨状态机语言效果、审查工时、生产率、安全认证或部署结果 | `excluded_with_reason` | `story/model_scope.md`；冻结 PlantUML 案例研究 | 本研究只实现并评测 PlantUML adapter，未运行跨语言或 human-outcome study。 |
