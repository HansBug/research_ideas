# 方法谓词与出处政策

**状态：** 当前有效。**适用范围：** paper1 method、评测记录和论文叙事。唯一 registry 是 [predicate_registry.json](../../../method/src/paper_stm_method/resources/predicate_registry.json)。

## 冻结谓词与来源

`four-family-19-core.v1` 的 19 个公开原子谓词已有冻结 source-ID mapping。来源目录保存每个谓词的 `domain`、`formal`、`technical` 支持与边界，用于说明研究命题和限制论文声明。该 mapping 不等于外部书目、DOI、全文原句和语义一致性已经逐条闭合；论文引用状态以 [`related_work/provenance/predicate_provenance.md`](../../../related_work/provenance/predicate_provenance.md) 的 `TODO-CITATION` 审计为准。来源数量不表示总体普遍率，台账使用量不构成学术出处。

来源 metadata 与运行时执行严格正交：冻结 registry 为 19 个谓词保留 typed contract、compiled form 和 native backend；一次 finding 只有在合法 typed inputs、对应 soundness fragment、完整归因和终止 Boolean receipt 均满足时才可为 W2。bibliography 不参与 backend dispatch、W、D、publication、route 或实验分母。

FCSTM 一侧同样只有一个语义权威：`pyfcstm` 原生 parser/AST/StateMachine/topology/runtime/`.fbmcq`。`ModelIR` 只是从 native document 得到的 compatibility projection，保留 canonical path、owner、pseudo-state、lifecycle action、forced/combo provenance 和 span；不得用正则、逐行 parser、brace stack 或字符串切片重新解释 FCSTM DSL。method 可在 native object identity 上实现 route、事实投影和审计，但不能以这些算法替换 native truth。`fcstm_native_projection_audit` 要求 60/60 source load、54/54 frozen input closure、零 projection difference 和零未批准文本处理。

## W、D 与评测

- W2：当前制品的冻结谓词、精确合法 typed binding、native backend、完整 artifact attribution 和 terminal `true|false` receipt。
- W1：仍在 Paper1 声明模型与源语言范围内的精确语义问题没有合法完成的 predicate evaluation；失败只写入 execution audit。这里的 `out_of_fragment` 只指谓词类型化约定或可靠性片段未闭合，不包括全局范围外的语言或模型语义。
- W0：binding 不精确，作为 coverage gap。

completed false 仅在人工 D2/D1 裁定后发布；completed true 只保留 pass receipt。D2/D1/D0 与 A0 由人工对事实和义务完成裁定，method 不得生成、裁定或在 release issue 中声称自己的 `l_level`。Ledger L 与人工评测仅在独立 evaluation 层使用，不能进入 method prompt 或生产分支。

## Primary route 与保存重放

主 route 只使用当前 pair 的 typed contract、compatible predicate set、exact binding、当前制品与封闭模型。R1 只对 exact event/carrier、唯一 native cold entry 和唯一 direct unguarded carrier 构造 runtime scenario；R4 仅对 requirement 明示 `scenario=cold`、`window=cold_macrosteps=N`（`N <= 32`）构造 interval；V1 仅对完整 native same-choice guarded group、exact carrier 集和 requirement 独立有限 JSON `domain` 调用 `.fbmcq`。在已声明范围内缺少任一输入时留下精确 W1 和 `input_contract_missing`/`out_of_fragment`，不从 prose、guard、fixture、ledger 或答案补造；全局范围外的语言或模型语义按失败关闭隔离，不产生 Paper1 finding。

route A/B 必须是 provider-free，并以保存的最终 `predicate_id=null` W1 evidence 作为 cohort。当前有效 artifact ID 是 `1bf7555fdbb9661008fc1e14b0ae16be`（`evidence-discovery-15x1-primary-route-replay-78506646`）：88 条 cohort、0 provider 调用、0 Judge 调用。它不使用历史较宽的辅助 candidate 集，也不是 hit/precision/Judge 指标。

## 禁止事项

不得新增或改写 19 谓词，不得为 coverage 硬挂邻近谓词，不得将 timeout/error/invalid input 变成 violation，不得用 source trace 或答案构造 runtime input，也不得借 ledger expected、Judge relation 或 pair ID 驱动 route。变更 predicate 定义属于独立研究决策，不是本政策的日常维护。
