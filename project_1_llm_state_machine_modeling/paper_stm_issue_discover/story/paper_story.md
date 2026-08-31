# Paper1 叙事主线

## 问题

控制系统需求常以自然语言给出，状态机模型则以状态、迁移、guard、trigger 和 action 表达行为。由 LLM 生成的 PlantUML 模型可能在词面、结构或可执行行为上偏离需求。本文研究的不是生成新模型，也不是自动修复，而是给定 NL 与一份作者 PlantUML 状态机，发现其中可陈述且可审计的不一致，并说明发现依赖的证据形态。

研究对象是 `M = (S, E, V, Tr, A)` 片段。时钟、不变式、正交 region/并发、hybrid 和无界时序不在本研究可证明的范围内；被排除不意味着这些问题不存在。

## 方法

方法从受 hash 约束的输入闭包开始：NL、作者 PlantUML、canonical source IR、FCSTM、native/inspection facts、working contract 与 source trace 各自承担不同角色。方法先抽取 NL contract；只在固定条件满足时进行一次有界 contract completion；随后使用两个互补的 discovery-grounding lens 提出并定位候选。确定性 frontier、predicate routing、typed binding、compiler 和 backend 对可执行候选给出可复核证据。方法再作 D adjudication 和受限定向 correction，最后计算 W，并只发布 D2/D1 的 exact typed-deduplicated reports。

PlantUML -> FCSTM 是本方法为获得可执行分析能力而引入的内部 projection，不是领域任务天然提供的事实，也不默认与作者源行为等价。source-level finding 必须经过 source trace、ownership 和适用 capability contract。只存在于 lowered IR、compiler-owned element 或未闭合 runtime evidence 中的报告，不成立为作者模型缺陷；但它们仍是方法输出层面的 invalid cost，必须计入端到端 precision，并单独作为 method diagnostic 报告。当前 v60 的归因审计中，291 条 I 包括 D0=120、ordinary source-level FP=53 和 NADC=118；NADC 内有 compiler-owned artifact=38、projection/trace boundary=24、runtime/evidence closure=48、attribution-indeterminate=8。严格的 conversion-lowering-confirmed 数为 0，因此不能把 NADC 总量写成转换语义错误。

谓词体系依据相关状态机、形式化验证和执行语义文献归纳为四族 19 个谓词：Structure (6)、Topology (4)、Trajectory simulation (4) 和 Bounded verification (5)。在 v60 中，12 个不同的 predicate ID 产生过 terminal receipt，8 个不同的 predicate ID 出现在至少一条 report-bound finding 中。前者是 distinct-ID 执行统计，后者是 distinct-ID 的 report-bound presence，不能与 finding 数、W2 数或 hit 数混用。

W 描述方法发现的证据强度，D 描述方法内对问题主张的裁定，L 仅是 ledger 的层级分类。W2 需要准确制品上的合法可执行对象、typed input、backend terminal true/false 与完整 receipt；缺少这些条件的具体发现仍可能是 W1，无法具体定位的主张是 W0。四族 19 谓词服务于可执行证据，不是问题发现或发布的准入门。方法的公开 finding surface 只发布 D2/D1；独立评测归档仍保留全部 report 和 decision。本文的目标是发现并证实缺陷，不是证明模型对所有行为都正确；因此，来源约束下的明确违规证据或一个具体反例已经足够时，不再强行升级到轨迹仿真或 BMC。只有静态证据不足以处理 guard、时序、RTC、变量效果或全局终止语义时，才使用这些更强的后端。

独立 Semantic Judge 按冻结 issue #195 协议先判 report validity，再在冻结 validity certificate 约束下判 report 与 expected issue 的 relation。evaluation 独立汇总 FULL/PARTIAL/NONE、VALID_KNOWN/VALID_NOVEL/INVALID、hit、precision、W-on-hits、K/N/I、predicate usage 与成本。方法本身不读取评测裁定、Judge 输出或历史 report。

## 当前证据

当前实验证据来自 54 个 pair、3 个 round、145 条参考缺陷条目和 435 个 round-level evaluation units。按 v4 公平对照层，v60/current 的 overall FULL 为 310/435 = 71.26%，X1v2 baseline v3 为 227/435 = 52.18%；L2 FULL 分别为 105/117 = 89.74% 与 50/117 = 42.74%。current 输出 1271 条 report，baseline 输出 512 条，因此 I 的绝对条数不能当作独立缺陷数。report-level validity precision 为 current `980/1271 = 77.10%`、baseline `417/512 = 81.45%`，差异为 `-4.34 pp`。按 side-specific I rate 做描述性分解，D0 率差为 `-7.16 pp`，ordinary FP 率差为 `+2.22 pp`；NADC 在 current 侧为 `118/1271 = 9.28%`，但 baseline v3 未提供同构分类，不能把它写成可比的 `+9.28 pp` 成分。若为 bookkeeping 将缺失 baseline cell 机械记为 0，残差才是 `+9.28 pp`，这不构成跨臂因果或无 projection 反事实。净观察到的 I-rate 差为 `+4.34 pp`，全部 invalid report 都保留在 precision 分母中。完整指标、I 归因、D/A、K/N/I、W-on-hits、成本资格、raw/derived 制品与复算命令以 [最终归档](../final_results/v60_current_vs_x1v2_baseline/README.md)、[v4 中文正式报告](../final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_v4_cn.md) 和 [conversion attribution overlay](../final_results/v60_current_vs_x1v2_baseline/derived/conversion_attribution_v1/README.md) 为准。

这组结果描述的是冻结 ledger、输入闭包、issue #195 Judge、`gpt-5.6-luna` 和已声明 fragment 下的 coverage–precision operating point。它不能证明跨模型、跨台账或跨状态机语义片段的普遍效果，也不能把 X1v2 的 legacy Judge 数字与 current baseline 混用。由于两侧 report 数量和 baseline v3 的审阅构成不同，`-4.34 pp` 是当前协议下的观察值，不应被写成完全不受输出粒度影响的语义精度估计。

## 贡献的可写范围

本文可以描述一条从 NL/作者状态机到带定位和可执行证据的发现链路，描述冻结谓词体系在该链路中提供的可执行证据，以及描述与独立 Judge 和离线评测分离的审计边界。新颖性措辞必须由相关工作核实后再确定；当前文档不使用“首个”“首次”或跨域泛化表述。

历史 v46、v27-stream 与旧 X1v2 Judge 网格用于解释演进，不用于证明当前改进幅度。它们的 ledger、Judge、执行模型、轮数、发布边界或指标定义与 v60 不同，具体依据见 [实验历史索引](../archive/experiment_history/README.md)。
