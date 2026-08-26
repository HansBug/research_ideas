# 当前四族谓词来源审计

本文件记录冻结 registry 的学术 provenance 完整性。结论固定：`four-family-19-core.v1` 的 S1--S6、G1--G4、R1--R4、V1--V5 均具有完成的学术资格审查；每个 ID 的来源与边界以 [current_source_catalog.json](current_source_catalog.json) 为机器真源。

## 审计维度

每个来源 ID 都保留以下可复核信息：

- 文件落点和标题；
- `domain`、`formal`、`technical` 的来源类型；
- 对冻结谓词定义的支持说明；
- 不可越过的模型、语义和论文声明边界。

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
