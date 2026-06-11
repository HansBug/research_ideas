# Abstract v0：S0b 方向冻结版摘要草案

本文档是 **pre-result / direction-freeze draft**。它只冻结摘要应该讲什么、不应该讲什么，以及后续 S5 可使用的候选英文摘要。当前没有主实验结果、人工裁决结果或基线对比结果，因此本文件中的任何英文摘要都不得写成结果型提升 / 优越性措辞。

上游约束：[`DIRECTION.md`](./DIRECTION.md)、[`story/paper_story.md`](./story/paper_story.md)、[`story/terminology_policy.md`](./story/terminology_policy.md)、[`story/claim_evidence_map.md`](./story/claim_evidence_map.md)、[`baselines/SUMMARY.md`](./baselines/SUMMARY.md)。

## 1. 摘要必须表达的方向

摘要应表达以下四点：

1. 研究对象是**面向控制系统需求的 LLM 状态机建模**。
2. 关键动机是状态机工件不仅要“生成出来”，还要能被解析、诊断、仿真执行，并能在反馈下被结构化修复。
3. 本文研究的是确定性诊断、场景级仿真反馈、结构化修复决策和基线感知评估的组合是否能形成可评估闭环。
4. 结果型主张必须留到 G3/G5 后再补；当前只能写“研究 / 分析 / 评估 / 计划中的评估将区分……”这类方向性表述。

## 2. 摘要必须避免的方向

摘要不得使用以下写法或暗示：

- `first NL-to-STM` / `first LLM state-machine generation`
- `first feedback loop` / `first tool feedback` / `first trace repair`
- `new DSL` / `new modeling language` / `FCSTM`
- `we improve model quality` / `we outperform prior work` / `we achieve better performance`
- “prior work only draws diagrams” 或 “prior work lacks feedback”
- 把“形式化反馈 / 诊断”等同于完整形式化验证、模型检查或定理证明

`fcstm` / `pyfcstm` 不进入摘要。若后续投稿或制品说明需要披露，只能在方法实现、制品或附录中作为内部实现 / 制品说明。

## 3. 四个最接近工作对摘要的约束

摘要通常不适合逐名列出所有相关工作，但摘要措辞必须给四个最接近工作留出诚实空间，不能写出会被它们直接反驳的 novelty：

| 最接近工作 | 摘要层面的约束 |
|---|---|
| Structure/Event SMF | 不能暗示自然语言到 UML / 状态机生成尚无人覆盖；只能说本文研究可执行反馈 / 评估底座 |
| LLMs for EMP | 不能暗示行为模型反馈 / 再生成尚无人覆盖；只能说本文区分确定性诊断、场景仿真与修复决策的组合 |
| TTool-AI | 不能暗示工具反馈尚无人覆盖；只能说本文把诊断作为受控闭环中的反馈来源之一 |
| Designing FSMs | 不能暗示 oracle / 轨迹修复尚无人覆盖；只能说本文研究场景候选、确定性仿真执行和结构化修复决策 |

## 4. 候选英文标题

> Executable Feedback for LLM-Based State-Machine Modeling from Control-System Requirements

备选更保守标题：

> Studying Executable Feedback in LLM-Based State-Machine Modeling from Control-System Requirements

第二个标题更强调研究问题，适合在结果不够强或 reviewer 对贡献强度敏感时使用。

## 5. 候选英文摘要 v0

Lint anchor：本节候选摘要必须通过 “no first claim / no DSL naming / no result-level improvement” 人工检查；若 grep 命中禁词，只允许出现在本文件的禁止写法或自检说明中。

> Large language models can help translate natural-language requirements into behavioral models, but control-system state-machine artifacts must also be checkable, executable, and repairable under explicit feedback. This paper studies LLM-based state-machine modeling from control-system requirements under a machine-checkable and executable target representation. Rather than naming a new paper-level formalism or claiming a first generator, we use the representation as an implementation substrate for deterministic diagnostics, scenario-level simulation, and structured repair decisions. The planned evaluation separates closest-work positioning, frozen samples, human component adjudication, and ablations over diagnostic and simulation feedback sources. This pre-result draft states the intended scope and protocol; result-level claims will be added only after the experimental evidence gate is closed.

## 6. 候选英文摘要 v0：更短版本

> We study executable feedback for LLM-based state-machine modeling from control-system requirements. The work constrains generated artifacts to a machine-checkable and executable representation, so that deterministic diagnostics, scenario-level simulation, and structured repair decisions can be evaluated as feedback sources. The framing treats the implementation substrate as an artifact-level mechanism and avoids first-work claims that are contradicted by recent state-machine and behavior-model generation studies. The planned evaluation will use closest-work positioning, frozen samples, human component adjudication, and ablations before any result-level improvement claim is made.

## 7. 后续 S5 改写规则

1. 若 G3/G5 结果支持质量变化，只能补入具体、可追溯、带 caveat 的结果句；不得泛写 “significantly improves” 或 “outperforms prior work”。
2. 若基线近似只能覆盖 Structure/Event SMF 或 LLMs for EMP 的子集，摘要必须写明评估范围，不能暗示完整同 benchmark 比较。
3. 若消融不支持仿真反馈或修复决策的边际贡献，摘要必须降级为诊断 / 失败分析 / 协议贡献。
4. 若人工裁决一致性或样本规模不足，摘要必须避免主结果论断，把贡献收缩为 pilot / 协议 / 定性证据。
5. 若投稿出口更偏 SoSyM / ASEJ / REJ，摘要首句可分别强化建模质量、自动化工作流或需求到行为模型，但不得反向扭曲 S0a story。

## 8. 摘要自检清单

- [x] 是否明确标注 pre-result / direction-freeze？
- [x] 是否没有结果型提升 / 优越性措辞？
- [x] 是否没有把 `fcstm` / `pyfcstm` 写成摘要概念？
- [x] 是否没有首创 NL-to-STM / feedback / trace-repair 论断？
- [x] 是否能与 Structure/Event SMF、LLMs for EMP、TTool-AI、Designing FSMs 同时成立？
- [x] 是否把实验说成 planned / will use / to be evaluated，而不是 completed result？
