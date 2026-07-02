# llm4se-systematic-review：A1-S1S8 四分栏提取

## 总体统计池裁决

裁决：**后续主统计池候选，但当前仅按 `schema_seed` 使用；A2a 完成页码、表图、ACM final 与 replication package 精核前，不进入最终定量统计或目标领域 finding。** 该文是 Kitchenham-style LLM4SE SLR，原文明确分析 2017-01 至 2024-01 的 395 篇 LLM4SE research papers，具备系统检索、纳排、QAC、snowballing、RQ-字段表与大量分布统计；但它的领域是 LLM4SE，不是 LLM4STM / 控制系统状态机 / formal verification × LLM，因此只能贡献“SE SLR 如何构造维度树、字段证据和候选 finding”的方法模式，不能把 LLM4SE 频次或路线图外推为本仓库目标领域结论。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | 摘要与 §2.1 声明回答 RQ1--RQ4：LLM、数据、优化/评价、SE tasks；§2 开头声明 follows Kitchenham et al. methodology。 | 复原为“LLM4SE 综合 SLR”的顶层任务树：RQ1 模型、RQ2 数据、RQ3 优化/评价、RQ4 SE 任务。 | **合格候选**：可作为 SLR 任务设定与 RQ-field contract 的统计池样本；不作为目标领域 evidence pool。 | 核对 ACM final 与本地 arXiv v6 在 RQ 表述、出版日期、页码上的差异。 |
| S2 语料收集与筛选 | Fig.1/§2.2--§2.4：QGS、6 个 SE venue、7 个数据库、218,765 初始候选、QAC 后 382、snowballing 补 13、最终 395；截止日 2024-01-31。 | 复原为完整分母链：manual search / automated search / filtering / QAC / snowballing；样本单位为一篇 LLM4SE research paper。 | **合格候选**：分母链足以进入后续统计池；当前只记录候选资格。 | PDF 视觉核验 Fig.1 数据库分项数；修正 `review.md` 中 ScienceDirect 62,290 与 Fig.1 65,290 的差异；确认 QGS 手工检索分母 4,618/图中阶段数。 |
| S3 原生维度树/样本编码对象 | Table 5 把 8 个 extracted data items 绑定 RQ；正文和附录按模型、数据、优化/评价、任务组织 395 篇。QAC3 要求 “not a secondary study”，但正文又称 systematic views/survey/review papers 会保留到质量评估阶段。 | 复原为 4 个 RQ 子树 + bibliographic/search meta 的维度森林；编码对象是 primary study / research paper，而非二次研究本身。 | **合格候选但带 caveat**：S3 可入统计池；secondary-study 纳排边界需标注。 | A2a 核验 QAC3 与 “retained systematic views/survey/review papers” 是否导致最终 395 中混入 secondary study；必要时在总账中加 “primary-study intended” 限定。 |
| S4 字段级证据 | Table 5 定义抽取字段；Appendix A--E / Tables 13--17 为 data type、input form、prompt、metric、SE task 等提供 study references；正文 footnote 给 replication package。 | 字段级证据链较强：字段合同 → 取值统计 → appendix reference list → replication package。 | **合格候选**：可作为 source-anchor / appendix-as-evidence 模式样本。 | 必须核验 replication package URL：paper text 为 `xinyi-hou/LLM4SE_SLR`，metadata abstract 为 `security-pride/LLM4SE_SLR`；核验 license、文件结构、与 ACM final 的 artifact 声明一致性。 |
| S5 维度模式演化 | §7 threats 称 RQ 与分类参考 DL4SE 等前序综述，并在每个 RQ 前阅读相关文献以预定义 categories；但原文未给 open coding、schema revision history、coder agreement 或 conflict log。 | 复原为“预定义分类 + full-text review 抽取”的模式演化，证据弱于字段结果本身。 | **降为中等资格**：可用于统计“是否报告 schema 来源/演化”的字段，但不能统计为已公开完整编码过程。 | 建议修正任何“字段审计过程充分公开”的强表述；A2a 查 replication package 是否有编码表、版本记录、冲突处理记录。 |
| S6 统计分析 | §2.5、§3--§6 与 Fig.2--10 / Tables 6--17 给出 N=395、154 peer-reviewed + 241 arXiv、年度分布、架构、数据源、输入形式、prompt、metric、SDLC/task/problem type 等统计。 | 复原为多个可计数字段叶：architecture、data_source、input_form、prompt、metric_by_problem_type、sdlc_phase、specific_task、problem_type。 | **合格候选**：适合后续统计池抽取字段分布；当前不得把 LLM4SE 数值外推为 LLM4STM 结论。 | 精核所有比例与分母：N=374 dataset、N=355 input form、task-instance vs paper count；ACM final 表图页码与 arXiv v6 是否一致。 |
| S7 候选 finding | §8 将统计观察组织为 challenges、opportunities 与 roadmap，例如 SE phase 覆盖不均、工业数据缺口、评价框架需求、domain-specific challenges。 | 复原为“统计观察 → challenge/opportunity/roadmap”的 finding 生成路径；Paper2 只迁移生成模式，不迁移 LLM4SE 领域结论。 | **模式合格，领域 finding 降级**：可入方法模式池；不得进入目标领域 final finding。 | 建议在后续汇总中持续保留“LLM4SE-only”边界；A2a 核验 §8 finding 是否均有前文统计支撑，避免 roadmap prose 直接升级。 |
| S8 研究者/作者质疑与裁决 | §7 reports search omission、study selection bias、empirical knowledge bias；两位 SE/LLM reviewers secondary review；QAC 与 replication package 作为缓解措施。 | 复原为质量控制 / threat 树：QGS、纳排、QAC、secondary review、replication package、threat mitigation；但缺字段级 coder agreement。 | **中等资格**：可统计“是否有 QA/threat/replication package”，但不能统计为强审计型研究。 | A2a 核验 reviewer 角色、是否独立双人抽取、是否存在 inter-rater agreement；若 replication package 不含审计记录，应维持 S8=中而非强。 |

## 建议降级 / 修正

- 保持 `review.md` 当前总体裁决：**主统计池候选 + `schema_seed`，A2a 前不进最终定量统计**。
- 明确修正/保留边界：replication package URL 存在 `xinyi-hou` vs `security-pride` 差异，ACM final 与本地 arXiv v6 差异未核验；二者不得作为已核验事实写入最终结论。
- 若后续汇总表需要压缩等级：建议 S1/S2/S4/S6 为强，S3/S7 为强但带边界 caveat，S5/S8 为中。
