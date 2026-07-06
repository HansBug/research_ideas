# A1-DT 19×3 全文审计汇总

本文件汇总 PR #135 中 19 篇 `survey_of_surveys` 论文的三路全文学术审计结果。每份审计报告均由对应 CLI agent 独立读取技能规则、文库规则、单篇 `bibtex.bib` / `metadata.json` / `paper_content.txt` / `review.md` 后生成。

## 1. 总体结论

57 份审计全部完成。三路审计的原始共同结论是：A1-DT 的基础证据降级纪律基本正确，但 19 篇 `review.md` 的维度树普遍存在“通用接口层过强、原文 schema 主树过弱”的问题。因此本轮返修必须把每篇论文的原文 RQ、抽取表、分类 schema、编码方案、统计表、roadmap / guideline stage、finding path 复原为主事实源；通用六叶接口只能作为跨论文投影，不得再作为原文树。

### 1.1 当前返修状态

本批次已经用于当前 PR 的结构化返修：19 篇 `review.md` 均已新增“原文 schema 主树（19×3 审计后返修）”“三路审计综合返修结论”“通用接口投影”和“返修后仍需 A2a 精核”，并回链三份审计报告。

需要特别说明：下表中的 `NEEDS FIX` 是三路 agent 对**返修前版本**给出的原始审计结论，不是当前工作区的最终状态。当前 PR 已处理这些原始 C/I 的共同根因：把原文 schema 主树抬升为单篇事实源，把六个通用 leaf 降级为跨论文投影，并保持 `schema_seed` / `not_verified` / `needs_manual_check` 的 A2a 接力边界。剩余的“逐页页码、表号、图号、supplementary、replication package 精核”按 PR body 和 GUIDE 口径留给 A2a，不作为本 PR-A1-DT 的合并阻塞项。

确定性门禁：

```bash
python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-19x3/check_structure.py
```

当前门禁期望通过：19 篇论文、57 份审计、三路审计回链、降级规则、中文审计附录表头和 SUMMARY 回链均存在。

## 2. 逐篇三路审计矩阵（返修前原始结论）

| 论文 | codex 原始结论 | claude 原始结论 | deepseek 原始结论 | 当前返修主题 |
|---|---|---|---|---|
| `ai-native-se-roadmap` | [NEEDS FIX](./results/ai-native-se-roadmap__codex.md) | [NEEDS FIX](./results/ai-native-se-roadmap__claude.md) | [NEEDS FIX](./results/ai-native-se-roadmap__deepseek.md) | 修正技术栈候选取值错误；扩展原文候选叶子，不要只保留 5 个粗叶子；增加关系边表；主干分支扩到 6 条，区分 SE era / SE 2.0 critique / SE 3.0 principle / stack components / challenge & OQ / evidence base，并把 “action roadmap” 合并到 challenge.OQ.our_vision 而非独立 sibling；把已闭合枚举写入候选叶子的取值空间，而不是“开放文本 / 由 A2a 复核” |
| `app-reviews-slr-se` | [NEEDS FIX](./results/app-reviews-slr-se__codex.md) | [NEEDS FIX](./results/app-reviews-slr-se__claude.md) | [NEEDS FIX](./results/app-reviews-slr-se__deepseek.md) | 修正主干和叶子父子挂接；扩展原文 schema 叶子，不只保留 5 个候选 leaf；补全三套 classification schema 的取值空间；主干分支与 RQ 不对齐；叶子层是通用接口而非原文 schema |
| `da-silva-2011-six-years-slr` | [NEEDS FIX](./results/da-silva-2011-six-years-slr__codex.md) | [NEEDS FIX](./results/da-silva-2011-six-years-slr__claude.md) | [NEEDS FIX](./results/da-silva-2011-six-years-slr__deepseek.md) | 补完整 RQ 主轴；修正单位对象；展开原文 extraction form；把 6 叶通用接口降级为 "cross-paper schema seed 层"，并增加专门的 "原文 schema 叶子层"；补 QA1–QA4 子叶子并写明评分准则与四分位 |
| `devsecops-primary-dimensions` | [NEEDS FIX](./results/devsecops-primary-dimensions__codex.md) | [NEEDS FIX](./results/devsecops-primary-dimensions__claude.md) | [NEEDS FIX](./results/devsecops-primary-dimensions__deepseek.md) | 扩展正式原文维度树；将六个通用 leaf 降为 wrapper；补全 relation edge table；5 个 source-schema 候选叶子补"候选取值空间"枚举；新增 4 个 schema 主轴 b6–b9 |
| `formal-re-llm-roadmap` | [NEEDS FIX](./results/formal-re-llm-roadmap__codex.md) | [NEEDS FIX](./results/formal-re-llm-roadmap__claude.md) | [NEEDS FIX](./results/formal-re-llm-roadmap__deepseek.md) | 重建主树为“双向 roadmap”；将通用 6 leaf 从“原文叶子”降级为兼容接口；补全原文候选叶子；把 Roadmap A 5 个 action point 显式枚举为候选叶子取值空间；把 Roadmap B 7 个 action point 显式枚举为候选叶子取值空间 |
| `interactive-llm-systematic-mapping` | [NEEDS FIX](./results/interactive-llm-systematic-mapping__codex.md) | [NEEDS FIX](./results/interactive-llm-systematic-mapping__claude.md) | [NEEDS FIX](./results/interactive-llm-systematic-mapping__deepseek.md) | 重建 `维度树复原` 正式事实源；修正主干与叶子的父子错配；展开 Fig. 1 stage-level schema；维度树主表把 6 个通用接口当作主体叶子展示，导致原文已闭合枚举（6 阶段、3 agent、二元 coding 等）被掩埋；主干分支 b1/b2/b3 把 Fig.1 单一 mapping-process 骨架切成三条并列分支，破坏 Fig.1 三元配对 |
| `kitchenham-2009-slr-tertiary` | [NEEDS FIX](./results/kitchenham-2009-slr-tertiary__codex.md) | [NEEDS FIX](./results/kitchenham-2009-slr-tertiary__claude.md) | [NEEDS FIX](./results/kitchenham-2009-slr-tertiary__deepseek.md) | 补全原文 extraction form 叶子；补全 DARE quality rubric 与质量结果叶子；补 RQ → 字段 → 表 → finding 的关系边；主干层补齐"方法 / 抽取 / 编码"独立分支；把 4 项 DARE QA 写成可统计叶子 |
| `kitchenham-charters-2007-slr-guidelines` | [NEEDS FIX](./results/kitchenham-charters-2007-slr-guidelines__codex.md) | [NEEDS FIX](./results/kitchenham-charters-2007-slr-guidelines__claude.md) | [NEEDS FIX](./results/kitchenham-charters-2007-slr-guidelines__deepseek.md) | 扩展主干树，不再用 5 个粗分支代表全文 schema。；把“六个通用接口叶子”降为接口摘要，不计为原文叶子。；细化原文候选叶子映射。；主干分支重排；原文模式候选叶子表扩充 |
| `llm-assistants-developer-productivity` | [NEEDS FIX](./results/llm-assistants-developer-productivity__codex.md) | [NEEDS FIX](./results/llm-assistants-developer-productivity__claude.md) | [NEEDS FIX](./results/llm-assistants-developer-productivity__deepseek.md) | 将完整原文 schema 从历史草稿迁移进事实源维度树；修正候选原文叶子过粗问题；补充 QA / eligibility 分支；F1 修正一句话结论 tree-type；F2 主干分支扩到 ≥8 |
| `llm4se-systematic-review` | [NEEDS FIX](./results/llm4se-systematic-review__codex.md) | [NEEDS FIX](./results/llm4se-systematic-review__claude.md) | [NEEDS FIX](./results/llm4se-systematic-review__deepseek.md) | 将正式维度树从通用接口树升级为原文 schema 树；补全 Table 5 八项 extracted data items；把 QGS、纳排、QAC 质量 rubric 设为一等字段；主干分支重构为 RQ 同构；把原文五分类 / 四分类 / 三分类的封闭取值空间写入叶子 |
| `mde-ml-components-slr` | [NEEDS FIX](./results/mde-ml-components-slr__codex.md) | [NEEDS FIX](./results/mde-ml-components-slr__claude.md) | [NEEDS FIX](./results/mde-ml-components-slr__deepseek.md) | 把正式维度树主干改为原文 RQ/Fig.5 驱动，而不是 b1--b5 通用接口；扩充“原文模式候选叶子映射”；修复候选取值空间错误/过粗；把根名与一级分支锚定到 Fig. 5；把 §“原文模式候选叶子映射” 从 5 条扩充到至少覆盖 §2.3 列举的全部一阶字段 |
| `mdse-modelling-assistants-mapping` | [NEEDS FIX](./results/mdse-modelling-assistants-mapping__codex.md) | [NEEDS FIX](./results/mdse-modelling-assistants-mapping__claude.md) | [NEEDS FIX](./results/mdse-modelling-assistants-mapping__deepseek.md) | 扩展“原文模式候选叶子映射”；修正 strategy 取值空间；拆分 metric 与 user；主干分支需对齐原文 RQ 而非通用接口；RQ1 strategy 候选叶子取值必须复原 6 cluster + 13 Tool 子型 |
| `ml4se-tertiary-study` | [NEEDS FIX](./results/ml4se-tertiary-study__codex.md) | [NEEDS FIX](./results/ml4se-tertiary-study__claude.md) | [NEEDS FIX](./results/ml4se-tertiary-study__deepseek.md) | 把当前“tertiary 主题 / 挑战树”改为复合树；扩展原文候选叶子映射；补 DARE-4 quality rubric；删除/重命名 `leaf-ml4se-tertiary-study-orig-data-source`；补齐 3 个 RQ 显式叶子 |
| `petersen-2008-systematic-mapping` | [NEEDS FIX](./results/petersen-2008-systematic-mapping__codex.md) | [NEEDS FIX](./results/petersen-2008-systematic-mapping__claude.md) | [NEEDS FIX](./results/petersen-2008-systematic-mapping__deepseek.md) | 补原文 schema 复原，不只列五个粗粒度候选叶子；补 Table 5 comparative analysis schema；补关系边表；主干补 b6 Guidelines/Roadmap 分支；b5 拆分为 “gap identification + map–vs–review comparison” 或新增 `[b5-sr-coding]` 与 `[b5-comparison-dim]` 两个并列叶子 |
| `petersen-2015-mapping-guidelines-update` | [NEEDS FIX](./results/petersen-2015-mapping-guidelines-update__codex.md) | [NEEDS FIX](./results/petersen-2015-mapping-guidelines-update__claude.md) | [NEEDS FIX](./results/petersen-2015-mapping-guidelines-update__deepseek.md) | 把原文 RQ1--RQ4 作为维度树主干或至少作为主干映射层；展开 Table 3 extraction form 为叶子字段；将“原文模式候选叶子映射”从 5 个粗项拆成可执行 schema；主干分支错位：`b4 quality rubric` / `b5 topic-independent dimensions` 不是原文主干；6 个通用 leaf 与原文 schema 不对齐 |
| `re-agile-sms-2015` | [NEEDS FIX](./results/re-agile-sms-2015__codex.md) | [NEEDS FIX](./results/re-agile-sms-2015__claude.md) | [NEEDS FIX](./results/re-agile-sms-2015__deepseek.md) | 补 3 个显式 RQ；补原文 extraction form；补检索 / 纳排分母链；主干替换：用原文 schema 取代 6 通用接口；列出 B1–B6 / P1–P6 闭枚举 |
| `re-tertiary-study-2014` | [NEEDS FIX](./results/re-tertiary-study-2014__codex.md) | [NEEDS FIX](./results/re-tertiary-study-2014__claude.md) | [NEEDS FIX](./results/re-tertiary-study-2014__deepseek.md) | 修正根节点单位对象和分母；用原文 RQ 重建主干；扩展原文候选叶子表；重构根节点表述与主干分支；补齐 QA1–QA4 + qa-total 五叶子并冻结取值空间 |
| `requirements-quality-theory-roadmap` | [NEEDS FIX](./results/requirements-quality-theory-roadmap__codex.md) | [NEEDS FIX](./results/requirements-quality-theory-roadmap__claude.md) | [NEEDS FIX](./results/requirements-quality-theory-roadmap__deepseek.md) | 将正式维度树从通用五主干 / 六叶子改为原文 schema 树；展开 RQT 概念叶子和关系边；补充 extraction guideline / coding scheme；主干分支错位；缺失 RQT 11 concept 作为正式叶子 |
| `research-artifacts-secondary-studies` | [NEEDS FIX](./results/research-artifacts-secondary-studies__codex.md) | [NEEDS FIX](./results/research-artifacts-secondary-studies__claude.md) | [NEEDS FIX](./results/research-artifacts-secondary-studies__deepseek.md) | 把正式维度树从通用接口改为 RQ-driven artifact audit schema；修正单位对象；展开 Table 1 字段为一等叶子；主 `维度树结构` 用通用 6-leaf 接口替代原文 schema；主干分支 b2 "artifact type" 在原文不存在 |


## 2.1 当前结构性返修闭环

| 闭环对象 | 当前处理 | 是否阻塞本 PR |
|---|---|---|
| 通用接口误当原文 schema | 19 篇均新增“原文 schema 主树（19×3 审计后返修）”，并把通用接口改为“通用接口投影”。 | 否，已结构性处理。 |
| 叶子取值空间过粗 | 19 篇均在原文主树表中列出纸面取值空间种子、统计用途、缺失语义和 A2a 精核任务。 | 否；精确封闭枚举核验留给 A2a。 |
| 关系边与 finding path 不足 | 单篇保留关系边表 / 原文主树 / 候选发现链路，审计入口回链三份结果。 | 否；复杂关系的逐表精核留给 A2a。 |
| 弱证据误入统计 | GUIDE、SUMMARY、单篇 A.3 与结构门禁均要求 `not_verified` 不得进入当前 SUMMARY 定量统计或 final finding。 | 否，已作为硬规则冻结。 |
| 审计结果可追溯 | 新增 [TASKS.tsv](./TASKS.tsv)、[run_audit.py](./run_audit.py)、[check_structure.py](./check_structure.py)、57 份 prompt / log / result。 | 否，已可复验。 |


## 3. 本轮必须统一修复的跨论文问题

1. **原文 schema 主树缺失或过浅**：不能只用“范围 / 语料 / 分类 / 方法 / 证据 / finding”六个通用 leaf 充当原文维度树。
2. **RQ / 贡献声明到字段的映射不足**：每篇必须说明原文 RQ、guideline stage、roadmap action 或 taxonomy 如何转成主干节点。
3. **叶子取值空间不够可执行**：叶子必须写出原文枚举、层级枚举、数值分母、关系值或明确的自由文本理由。
4. **关系边缺失**：对统计表、taxonomy、模型、流程、finding path 中的横向关系必须显式建边。
5. **证据链粒度不足**：A1-DT 可继续使用 `not_verified` / `schema_seed`，但需要把 A2a 精核任务拆到具体页、表、图、附录或原文章节，而不是统一写“待精核”。

## 4. 返修策略

本轮返修不把 A1-DT 伪装成 A2a 精核完成品。所有新增原文 schema 节点仍默认 `schema_seed`，但必须让 A2a 接手时能直接看到“该核哪张表、哪个图、哪个 RQ、哪个取值空间、哪条关系边”。返修后每篇 `review.md` 应包含：

- 原文 schema 主树：作为单篇维度树事实真源。
- 跨论文通用接口映射：仅用于把原文树投影到 A1-M0--M6 和 SUMMARY。
- 三路审计回链：链接到本目录三份审计报告。
- A.3 新增返修结论：说明原文 schema 主树仍为 `schema_seed`，不得进入当前定量统计。
