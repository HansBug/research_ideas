# Paper1 叙事主线

## 问题

控制系统需求常以自然语言给出，状态机模型则以状态、迁移、guard、trigger 和 action 表达行为。由 LLM 生成的 PlantUML 模型可能在词面、结构或可执行行为上偏离需求。本文研究的不是生成新模型，也不是自动修复，而是给定 NL 与一份作者 PlantUML 状态机，发现其中可陈述且可审计的不一致，并说明发现依赖的证据形态。

研究对象是 `M = (S, E, V, Tr, A)` 片段。时钟、不变式、正交 region/并发、hybrid 和无界时序不在本研究可证明的范围内；被排除不意味着这些问题不存在。

## 方法

方法从受 hash 约束的输入闭包开始：NL、作者 PlantUML、canonical source IR、FCSTM、native/inspection facts、working contract 与 source trace 各自承担不同角色。方法先抽取 NL contract；只在固定条件满足时进行一次有界 contract completion；随后使用两个互补的 discovery-grounding lens 提出并定位候选。确定性 frontier、predicate routing、typed binding、compiler 和 backend 对可执行候选给出可复核证据。方法再作 D adjudication 和受限定向 correction，最后计算 W，并只发布 D2/D1 的 exact typed-deduplicated reports。

W 描述方法发现的证据强度，D 描述方法内对问题主张的裁定，L 仅是 ledger 的层级分类。W2 需要准确制品上的合法可执行对象、typed input、backend terminal true/false 与完整 receipt；缺少这些条件的具体发现仍可能是 W1，无法具体定位的主张是 W0。四族 19 谓词服务于可执行证据，不是问题发现或发布的准入门。

独立 Semantic Judge 按冻结 issue #195 协议先判 report validity，再在冻结 validity certificate 约束下判 report 与 expected issue 的 relation。evaluation 独立汇总 FULL/PARTIAL/NONE、VALID_KNOWN/VALID_NOVEL/INVALID、hit、precision、W-on-hits、K/N/I、predicate usage 与成本。方法本身不读取 ledger、expected answer、Judge 输出或历史 report。

## 当前证据

当前实验证据来自 54 个 pair、3 个 round、145 条 expected issue 和 435 条 round-level expected row。v60/current 的 overall FULL 为 306/435 = 70.34%，X1v2 baseline 为 211/435 = 48.51%；L2 FULL 分别为 104/117 = 88.89% 与 46/117 = 39.32%。完整指标、W 分布、成本资格、raw/derived 制品与复算命令以 [最终归档](../final_results/v60_current_vs_x1v2_baseline/README.md) 和 [中文正式报告](../final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_cn.md) 为准。

当前比较只支持冻结 ledger、输入闭包、issue #195 Judge、`gpt-5.6-luna` 和已声明 fragment 下的结论。它不能证明跨模型、跨台账或跨状态机语义片段的普遍效果，也不能把 X1v2 的 legacy Judge 数字与 current baseline 混用。

## 贡献的可写范围

本文可以描述一条从 NL/作者状态机到带定位和可执行证据的发现链路，描述冻结谓词体系在该链路中提供的可执行证据，以及描述与独立 Judge 和离线评测分离的审计边界。新颖性措辞必须由相关工作核实后再确定；当前文档不使用“首个”“首次”或跨域泛化表述。

历史 v46、v27-stream 与旧 X1v2 Judge 网格用于解释演进，不用于证明当前改进幅度。它们的 ledger、Judge、执行模型、轮数、发布边界或指标定义与 v60 不同，具体依据见 [实验历史索引](../archive/experiment_history/README.md)。
