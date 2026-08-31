# Claim 与证据映射

| Claim | 可用证据 | 必须同时写出的边界 |
| --- | --- | --- |
| 方法能从 NL 与作者状态机产生可定位的发现及证据 | v60 method cell、stage receipt、source trace、publication artifact | 仅针对冻结输入闭包与当前方法合同；不等同于模型修复或完整需求覆盖 |
| 方法使用四族 19 个文献归纳谓词；v60 执行过 12 个 distinct predicate IDs，其中 8 个至少绑定到一条 report-bound finding | [predicate registry](../method/src/paper_stm_method/resources/predicate_registry.json)、[v60 method summary](../final_results/v60_current_vs_x1v2_baseline/raw/v60_current/method/summary.json)、[current v4 decisions](../final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v4_current_reaudit/current_report_decisions_v4.json)、[fair summary](../final_results/v60_current_vs_x1v2_baseline/derived/fair_comparison_v4/combined_summary_v4.json) | 12/19 是 terminal-receipt 的 distinct-ID 执行指标；8/19 是 report-bound distinct-ID presence；二者不表示缺陷类型覆盖、finding/W2 数或 hit 数；X1v2 predicate usage 为 N/A |
| 一部分发现具有可执行 W2 证据 | predicate registry、typed binding、compiler/backend terminal receipt、W audit | W2 只在精确制品、合法 typed input 和完整 receipt 都存在时成立；谓词不是发现准入门 |
| v60/current 在当前冻结比较中有 310/435 overall FULL | [v4 combined summary](../final_results/v60_current_vs_x1v2_baseline/derived/fair_comparison_v4/combined_summary_v4.json)、current v4 canonical decisions 与正式报告 | 分母为 435 expected-round units；D/A、relation、K/N/I 经过统一 source-first closure；不得改写成跨模型或跨 ledger 成效 |
| X1v2 baseline v3 在同一最终归档中为 227/435 overall FULL | [v4 combined summary](../final_results/v60_current_vs_x1v2_baseline/derived/fair_comparison_v4/combined_summary_v4.json)、baseline v3 canonical decisions 与正式报告 | baseline v3 冻结原有 K、重审原非 K；旧 Judge/网格数字只在 archive/history，不能进入本比较 |
| 两臂的 W-on-hits 可公平并列 | current expected-witness audit 与 baseline 512 finding 的双审 W audit | W 与谓词体系不绑定；baseline predicate usage 不适用，但 baseline W 适用；Judge 核验不使 baseline finding 成为 W2 |
| Judge、method 和 evaluation 的职责可审计 | 三个包的源码、资源、import boundary tests 与 release manifest | 这说明职责和输入输出隔离，不证明 Judge 没有测量误差 |

不得写成 claim 的内容包括：方法对所有状态机语义有效；冻结 ledger 是缺陷全集；某个执行模型普遍更优；当前谓词族的单独必要性已经被消融证明；或当前结果可与 v46/v27 直接相减。历史比较条件见 [实验历史索引](../archive/experiment_history/README.md)。
