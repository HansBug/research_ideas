# 原型工程调试报告

## 1. 定位

本文件记录 witness-search 原型的工程调试结论，不承担方法来源、benchmark 分组或论文效果结论。方法的 obligation taxonomy、typed Evidence Program、D/W/L 定义、编译规则与发布策略必须由领域文献、UML 元模型、状态机测试、property-pattern、test-oracle 和 verification-witness 研究建立；任何真实 pair 只可用于验证实现是否符合已经定义的合同。

## 2. 已验证机制

当前调试记录已经证明以下工程链条能够运行：LLM 从 NL 生成结构化规范义务；另一 LLM 将义务绑定到 PlantUML 与带映射注释的 FCSTM 精确 ID；固定 compiler 生成 source/SMT/topology/pyfcstm Evidence Program；程序真实执行并保存 terminal verdict、artifact hash、assertion hash、observed values、path/cut/SCC/SMT model/trace 和工具版本；独立 D 节点为每条 finding 输出 D2/D1/D0；发布层机械派生 W2/W1/W0 与 L2/L1/L0，并保留 D0 与证据失败的降级记录。

调试还验证了两个必须分离的命题：FCSTM 上的真实 counterexample 只证明转换制品后果，作者源 issue 还需要独立 source-causality certificate；W2 只证明断言在声明片段内被真实执行并得到反例，不自动证明 NL obligation 绑定正确，因此仍需独立 D 裁决和环外 matching。

## 3. 已发现的实现风险

现有风险包括 structured output 过长、同一根因多 facet 重复发布、错误规范前提被真实执行、source certificate 与报告 claim 不一致、未决 binding 未完全 veto、semantic receipt 未闭合到真实 LLM call/hash chain、自由语义文本被不适当地放入 validator，以及 formal diagnostic 被误写成 NL obligation。它们都属于实现偏离或证据链缺陷，修复不得借助真实 pair 的答案，也不得使用关键词、字符串相似度、identifier 后缀或其他文本特判。

## 4. 调试纪律

每次调试只检查 schema、引用闭包、编译、执行、异常降级、D 覆盖、证书一致性、计价和 replay 等可机械验证的合同。若调试暴露疑似表达缺口，必须回到领域来源重新取证；只有能够给出领域义务、binding 角色、反例语义、soundness fragment 和预期 receipt 的能力才能进入方法。真实 pair 名称、台账条目、baseline miss 和预期答案不得进入 runtime prompt 或合成 worked example。

## 5. 效果结论边界

调试运行不能回答 overall hit、L0/L1/L2 hit、D×L hit、precision、false positive、W2 fraction 或相对 X1v2 显著性。上述问题统一由完整 54 pair、145 条台账上的 benchmark evaluation 回答；所有 pair 使用同一冻结方法版本与同一 matching 协议，不作数据集角色拆分。

## 6. 进入完整评测前的门

进入完整 benchmark 前必须完成领域义务来源账、typed obligation schema、relation-to-backend soundness table、单次整格 D、W2 receipt v2、未决 binding veto、source attribution gate、D0/W1/W0 降级、四类美元计价、prompt leakage test、合成 mutation test 和全链路 replay test。完整评测必须报告 overall 与各 D/L 分层、hit@1/@3/@all、precision、false positive、W2/W1/W0、source-attribution、degraded/unsupported grid、同模型美元倍率及相对 X1v2 的 pair-clustered uncertainty。
