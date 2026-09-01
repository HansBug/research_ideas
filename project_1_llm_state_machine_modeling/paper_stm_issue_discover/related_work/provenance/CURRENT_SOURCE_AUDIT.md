# 当前四族谓词来源审计

本文件记录冻结 registry 的学术 provenance 边界。当前可由证据支持的结论是：`four-family-19-core.v1` 的 S1--S6、G1--G4、R1--R4、V1--V5 均已完成 source-ID mapping、claim-support 和 boundary 对照；每个 ID 的来源与边界以 [current_source_catalog.json](current_source_catalog.json) 为机器真源。该结论不等于 19 个 predicate 的完整书目、DOI 或全文逐字核验。

`current_source_catalog.json` 的 schema 没有 authors/year/venue/bibliography/DOI/access-date
字段，且部分条目是仓库内技术或领域 artifact 而非外部论文。故本轮保留
`bibliography_and_full_text_metadata_gap`：缺失字段显式写为 null，不能从标题、路径或来源类型
推造书目。正式人工评测只使用 source mapping、具体 supports、boundary 和作者源证据；predicate
academic provenance 的这一限制会在报告和 manifest 中披露。

## 审计维度

每个来源 ID 都保留以下可复核信息：

- 文件落点和标题；
- `domain`、`formal`、`technical` 的来源类型；
- 对冻结谓词定义的支持说明；
- 不可越过的模型、语义和论文声明边界。

catalog 的来源记录只允许 `id/types/title/paths/supports/boundary` 六类字段；本审计只核对每条
冻结记录的 source-ID mapping、supports 和 boundary，不把这种核对扩展为书目、DOI、稳定链接
或全文逐字核验，也不设置或推导可靠性等级。

审计的作用是保持论文叙事、注册表定义和实现边界可追溯。它不产生 runtime status，不参与 W、D、publication、route、backend dispatch 或 predicate execution coverage。

## 运行时分工

| 维度 | 回答的问题 | 真源 |
|---|---|---|
| academic provenance | 为什么 19 个冻结谓词可用于论文方法 | registry + 本目录 |
| typed binding | 当前需求/模型是否形成精确合法输入 | method compiler/binder |
| execution | 当前 FCSTM 上是否真实终止得到 Boolean | native FCSTM backend / `.fbmcq` / runtime |
| W | 当前证据是否为 W2/W1/W0 | execution receipt + deterministic W state machine |
| Judge | report 与外置 expected 的独立关系 | 冻结 evaluation 路径 |

特别地，`completed`/`true` 与 `completed`/`false` 在其余 W2 条件闭合时都属于 W2；区别只在 publication。timeout、provider error、backend error、invalid input、unsupported backend 和 attribution failure 都是独立 execution failure，绝不能被解释为 violation。

## 维护纪律

来源维护不得改变谓词 ID、语义、typed contract 或 backend 的运行时解释。任何真正涉及冻结谓词定义变化的研究决定必须走独立变更流程和完整回归；普通来源文本更新只同步 catalog、引用与论文叙事，并保持上述运行时隔离。
