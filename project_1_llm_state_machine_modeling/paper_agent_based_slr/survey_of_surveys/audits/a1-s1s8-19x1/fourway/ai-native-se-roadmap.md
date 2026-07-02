# ai-native-se-roadmap：S1--S8 四分栏审计补充

## 总体统计池裁决

**裁决：不进入主统计池。** 该文是 vision / roadmap / proposal，不是 SLR、SMS、tertiary 或 guideline 检索研究。可作为 roadmap 边界锚点 / schema seed / 方法学启发，但不得把 117 条参考文献、3 个时代、5 个 stack component、5 个主挑战或 OQ1--OQ14 当作系统综述分母或最终 empirical finding。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | 摘要与 §1 明确提出 SE 3.0 vision、technology stack 与 challenge roadmap；§1 说明来源包括文献 survey、workshop、客户讨论、内部经验与 OPEA 互动。 | 对应 `vision / roadmap / proposal` 类型；不是 review-driven RQ 树，而是愿景—技术栈—挑战树。 | 否；只作边界锚点。 | 核对 publisher final 与 PDF 页码；确认原文没有隐藏 method / protocol 附录。 |
| S2 语料收集与筛选 | 只有“academic and gray literature surveys”等来源描述；没有数据库、检索式、纳排、去重、质量评价或筛选分母。 | 可登记为 `evidence.source_type` 开放枚举；不能复原系统语料链。 | 否；117 references 不是 SLR 分母。 | 复核参考文献列表总数、自引用 / companion work 标记；确认无 supplementary 检索协议。 |
| S3 原生维度树 / 样本编码对象 | §3 给出 5 层 SE 3.0 stack；§4 给出 5 个主挑战与 OQ1--OQ14；§4.6 是附加 OQ，不是第 6 个主挑战。 | 可复原为降级树：三时代 baseline + 五层 stack + challenge/OQ roadmap tree。 | 否；结构枚举可作 schema seed，不能作跨论文统计样本。 | 打开 PDF 核对 Fig. 1、Fig. 3、Fig. 4--7 的视觉结构、箭头、组件命名。 |
| S4 字段级证据 | §4 明确 challenge entry 包含 description、affects、open question、our vision；§4.1--§4.5 有 `Affects` 字段。 | 可复原 `challenge.template_field` 与 `rel.affects` 关系边；字段是 roadmap 字段，不是样本抽取表。 | 否；字段可迁移为候选抽取 schema，不进主统计。 | 精核每个 challenge 的 affects 值、OQ 编号、companion evidence 引用。 |
| S5 维度模式演化 | §3.6 curriculum recipe 提到 taxonomy、examples、evaluation rules、pilot testing、community contribution；但这是 FM.next 设想，不是本文 roadmap 形成过程。 | 只能作为“模式工程 / curriculum-as-asset”类比；原文没有报告开放编码、分类迭代或研究者裁决过程。 | 否；仅方法启发。 | 区分 InstructLab / curriculum learning 引文与作者自己的 roadmap 生成过程；避免误写成本文编码流程。 |
| S6 统计分析 | 原文有少量内部数量：3 个时代、5 个 stack component、5 个主挑战、14 个 OQ；也有 companion prototype 数字如 30%、50%、90%。 | 这些是 roadmap 内部枚举或 companion work 局部结果，不是综述 synthesis。 | 否；S6 应判为“不适用 / 弱”。 | 核对 companion works [28]、[98]、[114] 的发表状态、实验对象和外推限制。 |
| S7 候选 finding | 可启发 `limitation → stack component → OQ → vision` 的候选 finding 台账；但所有领域主张都是愿景性。 | 可迁移的是 finding ledger 结构，不是“SE 3.0 已成立”这类结论。 | 否；只能作候选启发，需后续研究者裁决。 | A2a 应为每条候选 finding 标注证据类型：vision-only、prototype、industry signal、peer-reviewed prior work。 |
| S8 研究者 / 作者质疑与裁决 | 原文没有 SLR 式多研究者筛选、编码分歧、一致性或 QA；仅有 caution、open questions 与结论中欢迎 opposing views。 | 可作为“缺少裁决日志”的反面样本，提醒 Paper2 保留人工质疑、override 与裁决链。 | 否；不支持质量控制统计。 | 复核是否存在独立 threats / limitation section；核对“only time will tell”等降级语句页码。 |

## 建议降级 / 修正

- 当前 `review.md` 中 S7 = 中略偏强。建议改为：`弱（结构启发）`，或写成 `中（仅 report-structure pattern，不代表 finding 证据强度）`。
- S3 = 中可以保留，因为 roadmap/challenge tree 可复原；但必须持续标注“降级树，不进主统计池”。
- S6 建议固定写作口径为：`不适用（主统计）/ 弱（内部枚举）`，避免内部数量被误读为综述统计。
