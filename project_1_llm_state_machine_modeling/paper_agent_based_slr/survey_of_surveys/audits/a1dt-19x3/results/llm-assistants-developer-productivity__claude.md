# llm-assistants-developer-productivity · claude 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：claude
- 是否读取 `$ai-research-writing-skill`：否。当前 session 在仓库容器内执行，`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md` 与 references 系列文件未被 mount/可见；审计仍按 reviewer-guidelines 与 reviewer-self-review 已知口径（对原文 schema 复原优先、不臆造字段、不把 roadmap/vision 写成完成型 finding）执行，并在本报告显式声明该限制。
- 是否读取 `$research-planning`：否，同上路径不可见；按 planning-prompts 已知口径（先复原原文 RQ→分类 schema→证据等级→候选 finding 路径，再判断是否过小）执行。
- 是否读取 `$oh-my-codex:autoresearch`：否，同上路径不可见；按 autoresearch 已知口径（抽取-验证-降级三段）执行。
- 是否完整阅读 `paper_content.txt`：是（覆盖 §1 Abstract/Intro、§2 Background、§3 Method 全部子节含 Table 1/2 与 §3.4 抽取字段、§4 RQ0 landscape 含 Table 3/4 与 Fig 2、§5 RQ1 含 Table 5/6/7、Fig 3/4/5 与 §5.3.1–5.3.4 instrument 细分、§6 RQ2 Benefits 8 主题 + Risks 5 主题 + Table 8/9 + Fig 6、§7 RQ3 SPACE Table 10 + Fig 7/8 + Table 11 quality metrics、§8 Discussion 含 Tetrad 4 象限 Fig 9 与 lessons learned，并扫读 §9 Threats 的 review methodology 与 primary evidence base 两组、§10 Conclusion 与 replication 声明）。
- 是否核对 `paper.pdf`：否；本轮以文本级审计为主，Table 1–11 / Fig 1–9 的精确页码与最终 ACM 版面留待 A2a 精核。

## 2. 原文真实结构复原

### 2.1 RQ / 目标 / 贡献声明

原文显式 4 个 RQ（§3 末尾 + 各结果章节起首）：

- RQ0 landscape：peer-reviewed studies 在 LLM-assistants × developer productivity 上的特征（年份、作者、venue、工具）。
- RQ1 methodology：methodological strategies / procedures / instruments。
- RQ2 impact：benefit / risk synthesis。
- RQ3 dimensions：哪些 productivity dimensions 被研究 + 如何映射到 SPACE。

贡献声明：39 篇 peer-reviewed primary studies、6 数据库检索 9 756 条、PRISMA-style flow、控制论文 + snowballing、Lenarduzzi 11-criterion QA、SPACE 维度映射 + Tetrad 解释、面向 practitioner / researcher 的 implications、open Zenodo replication package。

### 2.2 方法流程与显式 schema

原文方法链（§3.1–3.4）显式给出以下 schema / taxonomy / coding scheme，全部具有可枚举值：

- **检索**：6 数据库 × 3-segment query（AI/LLM 词 × developer/SE 词 × productivity 词）× 5 轮 query iteration × 17 control papers（Table 1 给出每库分母 ACM 4 044、IEEE 491、ScienceDirect 3 734、WoS 271、Scopus 836、Springer 380）。
- **筛选分母链**：9 756 → dedup −803 → 8 953 标题摘要 → 228 全文 → 39 入选 + snowballing 加 5 → QA 44 → final 39。每段都有 exclusion code（不研究 productivity / 顺带提及 / secondary / WIP / extended abstract / poster / tool demo / editorial / grey / book / thesis / workshop / <4p / 不可访问）。
- **QA**：Lenarduzzi 11 criteria（research-based / clear aims / context / design / recruitment / control / data collection / data analysis / researcher-participant / clarity / value），0–4 Likert，>50% 均分阈值，5 篇被 QA 排除（Table 2）。
- **抽取字段（§3.4 显式列出）**：study goals / tools / empirical strategy and design / tasks / settings / key results，并对每篇写 descriptive summary；之后做 3 轮 targeted thematic iteration（RQ1 / RQ2 / RQ3）。
- **RQ1 分类 schema**：① Strategy taxonomy = Stol & Fitzgerald 6 类（Field Study, Field Experiment, Experimental Simulation, Laboratory Experiment, Sample Study, Judgment Study；Table 5 + Fig 3）。② Procedure taxonomy = Glass-Vessey-Ramesh 5 类（Survey, User Experiment, Concept Implementation, Interview, Case Study；Table 6 + Fig 4 overlap）。③ Objective = Hartson 二分（formative / summative）。④ Analysis type 三分（quantitative / qualitative / mixed）。⑤ Data source × Instrument origin 2×2 矩阵 + 具体 instrument 清单（Table 7：Self-Reported × Designed-by-Authors 含 Surveys/Interviews/Open-ended feedback；Self-Reported × Validated 含 NASA-TLX/SPACE-Survey/TAM/Self-Efficacy/AAR-AI/Emotion Affect；Behavioral × Designed-by-Authors 含 Task Completion/Acceptance Rate/Interaction Logs/Time-to-Completion/Code Quality Metrics/Productivity Gain；Behavioral × Validated 含 TCQ/RBV）。⑥ 具体 metric 细分：Time-to-Completion 12/39 31%、Acceptance Rate 7、NASA-TLX 6、eye-tracking 1、TCQ-econometric 2。
- **RQ2 主题 schema**：Benefits 8 主题（Accelerate development / Minimize online code search / Automate trivial-repetitive tasks / Support knowledge acquisition / Support code-adjacent tasks / Reduce task initiation overhead / Improve code quality / Support debugging-troubleshooting；Table 8 + Fig 6 radar）。Risks 5 主题（Fail to meet requirements / Promote over-reliance and cognitive offloading / Limit code quality / Disrupt the flow / Reduce team collaboration；Table 9 + Fig 6 radar）。Code-quality 同时出现在 benefit + risk，被原文显式标为 contested。
- **RQ3 framework mapping**：SPACE 5 维 × 12 sub-dimension 显式枚举（Satisfaction = developer experience / self-efficacy / trust / cognitive load + 显式空 well-being；Performance = quality / impact；Activity = action-task counts；Communication = human-LLM / human-human；Efficiency = temporal efficiency / interruptions and flow / automation；Table 10）+ quality-metric 子表 13 项（Table 11：Passing Unit Tests / Functional Correctness / Code Smells / BLEU / Halstead / Cyclomatic / Translation Error Rate / Maintainability Index / Cognitive Complexity / Defect Density / Defect Rate / Technical Debt / Code Coverage）+ overlap intersection（Fig 8）。
- **Discussion lens**：McLuhan Tetrad 4 象限（Enhance / Reverse / Obsolesce / Retrieve；Fig 9）+ 三条 Lessons Learned + practitioner（5 类）+ researcher（3 方向）implications。
- **Validity**：threats 显式两层结构。Tier-1 review methodology 4 项（study selection bias / human-centered identification difficulty / bias-and-repeatability / classification rigor）；Tier-2 primary evidence base 3 项（formative-and-lab bias / methodological diversity / temporal relevance）。
- **Artifact**：Zenodo replication package 包含 study data / selection decisions / exclusion rationales / QA scores / control papers / query refinement / supplemental classification details。

### 2.3 从字段 / 统计观察到 finding / gap / recommendation 的形成方式

- 每个 RQ 末尾 Summary 把"分类频次 + 主导类别 + 争议 + gap"压成 3–5 行短结论（RQ0/1/2/3 Summary 显式存在于正文）。
- RQ2 → contested theme（code quality）→ Discussion Tetrad 解释 → recommendations。
- RQ3 → SPACE 覆盖统计 → Communication / Activity / well-being / team dynamics 显式 gap → researcher recommendation。
- Tetrad 4 象限把"测量层 SPACE"提升为"socio-technical 解释层"，并对应 practitioner 行动点。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 基本通过 | `[dim-llm-assistants-developer-productivity-root]` 锚定标题 + RQ 集合，与原文 §3 RQ 列表一致。 | 通过 |
| 主干分支是否覆盖原文 schema | 不完整 | 仅 5 个伞型分支 b1 综述范围 / b2 语料 / b3 主题 / b4 方法 / b5 评价+发现。RQ0 landscape（年份/作者/venue/工具）、framework-mapping 子树（SPACE 5×12）、Discussion lens 子树（Tetrad 4 象限）、threats 两层结构均未独立挂主干，被隐式塞进 b1/b3/b5。 | I |
| 叶子维度是否足够具体 | 不足 | 正式叶子只有 6 个通用接口（scope/corpus/taxonomy/method/evidence/finding）。原文 ≥12 个显式可枚举 schema（strategy 6 / procedure 5 / objective 2 / analysis-type 3 / data-source×instrument-origin 矩阵 / metric 细分 / benefit 8 / risk 5 / SPACE 5 / SPACE-sub 12 / quality-metric 13 / Tetrad 4 / QA 11 / threat-tier 2）未进入叶子层。 | I |
| 取值空间是否可执行 | 偏抽象 | 叶子表取值空间多写"自由文本 / 完整 SLR 数值链条 / 层级枚举"，未把原文已有的枚举值（如 Stol-Fitzgerald 6 值、Glass-Vessey-Ramesh 5 值、SPACE 5×12 已枚举值、QA 11 criteria、benefit 8 / risk 5 题名）落地。 | I |
| 关系边是否缺失 | 缺失 | 仅 2 条边（method↔evidence、taxonomy↔finding）。原文显式存在 study×SPACE-dim 映射边（Table 10）、strategy×procedure overlap 边（Fig 4）、strategy×instrument 边（Fig 5）、benefit/risk×支持证据强度边（Table 8/9 self-report vs measured）、SPACE×Tetrad 跨子树解释边、QA-score×study eligibility 边、threat×mitigation 边均未建模。 | I |
| 统计用途 / 分母是否正确 | 通过（保守正确） | 全部叶子标 `schema_seed` / `not_verified`，不直接进入 SUMMARY 定量统计，未越权升级。分母 39 / 9 756 等数字在 §2 narrative 已正确给出。 | 通过 |
| 候选 finding 路径是否完整 | 不完整 | finding 叶子只笼统说"统计观察 / discussion → 候选发现 → 研究者裁决"，未刻画原文 4 条显式 finding 路径：① RQ0 langscape→2024 占比 77% 的 temporal bias；② RQ1→time-to-completion 31% 主导 + acceptance rate caveat + cognitive load mixed；③ RQ2→code quality contested + Tetrad reverse；④ RQ3→Communication/Activity/well-being/team-dynamics gap。 | I |
| A.1–A.4 证据链是否足够 | 基本完成但偏弱 | A.1 三件套齐全；A.2 五条证据均 `not_verified`，但事实上 §2 narrative 已可定位到具体 Table/Figure（Table 1–11、Fig 2–9）、具体 §3.4/§5.3/§6/§7/§8.1/§9 章节、具体页 9–33；至少应升级为 `paper_text_local_verified` + "PDF 版面待 A2a 复核"两段式。A.4 visual-check 标 `needs_manual_check` 合理。 | M |
| 是否存在可能误导 A2a 的强主张 | 存在中等风险 | "一句话结论"称 tree-type = "RQ 驱动分类树" + "辅助 benefit-risk 评价树"。这遗漏了 framework-mapping（SPACE 5×12）子树与 Discussion lens（Tetrad 4 象限）子树。A2a 若按此 tree-type 聚类，会把本文与"只做 benefit/risk 主题分析的纯 SMS"误聚到一起，丢失它实际是"4-layer landscape→method→synthesis→framework+lens"完整 SLR+SMS 的事实。 | I |

## 4. 建议维度树骨架

下方为更忠实于原文的 8-主干、≥18-叶子骨架，所有取值空间均可在原文 Table 1–11 + Fig 2–9 + §3.1–9 中逐条锚定。当前 review.md 的骨架不够，应在 A2a 前补完或至少在"原文模式候选叶子映射"中显式列全。

```text
[root] LLM-Assistants on Developer Productivity (SLR + SMS, n=39)
├── B1 综述范围与 RQ
│   └── L1.1 单位对象 + RQ 集合（unit=primary peer-reviewed empirical study；RQ0–RQ3）
├── B2 检索与纳排
│   ├── L2.1 数据库 × 查询段（6 库 × 3 segment × 5 iteration；分母 9 756）
│   ├── L2.2 inclusion / exclusion 标准（13 排除编码 + 4 纳入条件）
│   ├── L2.3 PRISMA-style 分母链（9 756→8 953→228→39+5 snowball→QA→39）
│   └── L2.4 control papers（17 篇）+ snowballing 增量
├── B3 质量评价
│   ├── L3.1 QA framework + 11 criteria + 0–4 Likert + >50% 阈值
│   └── L3.2 QA 排除 5 / 44，score 分布
├── B4 数据抽取字段（§3.4 显式）
│   └── L4.1 raw extraction set = {study goals, tools, empirical strategy & design, tasks, settings, key results} + descriptive summary
├── B5 RQ0 Landscape schema
│   ├── L5.1 publication year（含 2014–2022=4、2024=77% temporal bias 锚点）
│   ├── L5.2 author distribution（154 作者 / 147 单篇）
│   ├── L5.3 venue focus（6 大类研究焦点 + 具体 venue list；Table 3）
│   └── L5.4 LLM tool（21 工具频次；Table 4）
├── B6 RQ1 Methodology schema
│   ├── L6.1 strategy taxonomy = Stol-Fitzgerald 6 值（Field Study/Field Experiment/Experimental Simulation/Lab Experiment/Sample Study/Judgment Study；Table 5）
│   ├── L6.2 procedure taxonomy = Glass-Vessey-Ramesh 5 值（Survey/User Experiment/Concept Implementation/Interview/Case Study；Table 6 + overlap Fig 4）
│   ├── L6.3 objective = Hartson 2 值（formative 59% / summative 41%）
│   ├── L6.4 analysis type 3 值（quantitative 13% / qualitative 21% / mixed 67%）
│   ├── L6.5 data-source × instrument-origin 2×2 矩阵 + instrument 清单（Table 7：surveys/interviews/open-ended/NASA-TLX/SPACE-Survey/TAM/Self-Efficacy/AAR-AI/Emotion Affect/Task Completion/Acceptance Rate/Interaction Logs/Time-to-Completion/Code Quality Metrics/Productivity Gain/TCQ/RBV）
│   └── L6.6 specific metric 细分（time-to-completion 31%、acceptance rate、NASA-TLX 6 dim、eye-tracking、econometric TCQ/RBV）
├── B7 RQ2 Impact synthesis schema
│   ├── L7.1 benefit theme = 8 值（Accelerate dev/Minimize online search/Automate trivial/Support knowledge acquisition/Support code-adjacent/Reduce task-initiation overhead/Improve code quality/Support debug-troubleshoot；Table 8 + Fig 6）
│   ├── L7.2 risk theme = 5 值（Fail to meet requirements/Promote over-reliance & cognitive offloading/Limit code quality/Disrupt flow/Reduce team collaboration；Table 9 + Fig 6）
│   └── L7.3 contested theme（code quality 同时出现在 L7.1 & L7.2，需 support_evidence / counter_evidence / boundary_condition 字段）
├── B8 RQ3 Framework mapping schema
│   ├── L8.1 SPACE dimension 5 值（S/P/A/C/E）+ coverage 统计（77/64/31/26/59%、多维 90%、≥3 维 44%、≥4 维 15%、最常组合 S-P-E）
│   ├── L8.2 SPACE sub-dimension 12 值（developer experience/self-efficacy/trust/cognitive load + 显式空 well-being / quality/impact / activity / human-LLM / human-human / temporal efficiency / interruptions & flow / automation；Table 10）
│   ├── L8.3 study×SPACE-dim 映射边（Table 10 39×5 矩阵 + Fig 8 intersection）
│   └── L8.4 quality metric 子表 13 值（Table 11）
├── B9 Discussion lens（McLuhan Tetrad）
│   ├── L9.1 4 象限值（Enhance/Reverse/Obsolesce/Retrieve；Fig 9）
│   ├── L9.2 Lessons Learned 3 条
│   ├── L9.3 practitioner implications 5 类（trust calibration / coder→reviewer / personal-team workflow / org adoption / ethics）
│   └── L9.4 researcher implications 3 方向（shared evaluation framework / multidim eval / confounding & replication）
└── B10 Validity & Artifact
    ├── L10.1 threat tier-1 review methodology 4 项
    ├── L10.2 threat tier-2 primary evidence base 3 项
    └── L10.3 replication package（Zenodo URL + study data + exclusion rationales + QA scores + control papers + query refinement）
```

每个 L 叶子均可在原文显式表/图/章节锚定，取值空间在 A1-DT 阶段就可标 `enumerated_closed` 或 `enumerated_open_with_count`，不需要再降级为 `自由文本`。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| F1 修正一句话结论 tree-type | review.md §"一句话结论"+ `[clm-llm-assistants-developer-productivity-tree-type]` | 把 tree-type 改写为 "4-layer RQ-driven tree（landscape / methodology / impact synthesis / framework mapping）+ Tetrad discussion-lens 子树 + 两层 threats 子树"；保留 schema_seed 状态。 | §3 RQ 列表；§4–§7 各 RQ；§8.1 Tetrad；§9.1–9.2 threats | I |
| F2 主干分支扩到 ≥8 | review.md §"维度树结构" | 把 b1..b5 改为 B1–B10（见上方骨架），其中至少把 RQ0 landscape、RQ3 framework-mapping、Tetrad lens、Validity-Artifact 独立成主干。 | Table 3/4、Table 10/11、Fig 9、§9 | I |
| F3 把原文已枚举 schema 升级为正式叶子 | review.md §"叶子维度表" + §"原文模式候选叶子映射" | 增加叶子 L6.1 strategy（6 值）/ L6.2 procedure（5 值）/ L6.3 objective（2 值）/ L6.4 analysis-type（3 值）/ L6.5 data-source×instrument-origin（矩阵）/ L6.6 specific-metric / L7.1 benefit-theme（8 值）/ L7.2 risk-theme（5 值）/ L7.3 contested-theme / L8.1 SPACE-dim（5 值）/ L8.2 SPACE-sub-dim（12 值）/ L8.4 quality-metric（13 值）/ L9.1 Tetrad（4 值）/ L3.1 QA-criteria（11 值）/ L10.1+L10.2 threat-tier（4+3 值）。取值空间统一标 `enumerated_closed`。 | Tables 2/5/6/7/8/9/10/11；Figs 4/5/6/7/8/9 | I |
| F4 删除或重命名 5 个自造 bucket | review.md §"原文模式候选叶子映射" | 当前 5 个候选叶子（assistant-type / developer-task / productivity-outcome / evaluation-design / human-factor）并非原文显式抽取字段；应删除或重命名为 §3.4 实际字段 {study-goal / tool / strategy-design / task / setting / key-result}，避免 A2a 把自造 bucket 当成原文 schema。 | §3.4 抽取字段表述（line 405–407） | I |
| F5 关系边扩展 | review.md §"关系边表" | 至少补充：study×SPACE-dim 映射边（Table 10）、strategy×procedure overlap（Fig 4）、strategy×instrument-type（Fig 5）、benefit/risk×evidence-source-strength（Table 8/9 self-report vs measured）、SPACE×Tetrad 跨子树解释边、QA-score×study-inclusion 边、threat×mitigation 边。 | Tables 8/9/10；Figs 4/5；§9 | I |
| F6 候选 finding 路径具体化 | review.md §"统计与候选发现链路" + `[leaf-llm-assistants-developer-productivity-finding]` | 把 finding 路径写成 4 条具体 candidate path：①RQ0 temporal bias（77% 集中 2024）；②RQ1 instrument caveats（time-to-completion 主导、acceptance rate 单独使用风险、NASA-TLX cognitive-load mixed）；③RQ2 contested theme code-quality；④RQ3 gap（Communication/Activity/well-being/team-dynamics 覆盖低）。每条标 candidate 而非 final，并保留反证。 | §4 末尾 + §5 末尾 + §6.2.4 + §7 末尾 | I |
| F7 升级证据等级两段式 | review.md §A.2 EV-002 / EV-003 / EV-005 | 把 `not_verified` 拆为 `paper_text_local_verified`（已可锚定 Table 1–11、Fig 2–9、§3.4/§5.3/§6/§7/§8.1/§9）+ "PDF 版面待 A2a 复核"两段。避免后续读者误以为本文连文本级证据都未核验。 | review.md §2 narrative 已大量引用 Table/Fig/页码 | M |
| F8 在迁移边界中显式声明不可外推主题 | review.md §"可迁移与不可迁移边界" | 已声明不可迁移领域结论，建议加一行明确：SPACE / Tetrad 是 productivity-specific lens，Paper2 不应默认采纳为元模型，只能作为"framework-mapping 子树 + discussion-lens 子树"的方法学 pattern。 | §7 RQ3 + §8.1 Tetrad | M |

## 6. C/I/M 结论

- **C（critical，破坏 Paper2 学术目标 / 证据链）**：0 项。所有叶子均标 `schema_seed` / `not_verified` 且未越权升级为定量统计；分母与排除链在 §2 narrative 中正确给出；root 与迁移边界未把领域结论冒充事实。
- **I（important，实质影响维度树可用性与 A2a 聚类正确性）**：6 项 = F1（tree-type 误归类）、F2（主干分支只 5 个）、F3（≥12 个原文显式 schema 未入正式叶子）、F4（5 个自造 bucket 冒充原文字段）、F5（关系边覆盖度严重不足）、F6（finding 路径未具体化）。这些问题若不修，A2a 会把本文 4-layer 完整 SLR+SMS 误聚为 "RQ + benefit-risk" 二层简化树，污染 Paper2 cross-paper taxonomy。
- **M（minor，清晰度 / 维护性）**：2 项 = F7（证据等级两段式）、F8（lens 迁移边界显式化）。
- **最终建议**：**NEEDS FIX**（先在本 PR 内修复 F1–F6 6 项 I 级问题；F7–F8 可延后到 A2a 或并入下一个清理 PR）。

### 审计自我审视（reviewer-self-review 口径）

- 是否臆造原文没有的字段？否；§4 骨架与 §5 F3 列出的所有叶子都对应到原文显式 Table / Figure / 章节，未引入新增构念。
- 是否把 roadmap / vision 写成 finding？否；F6 明确把 4 条 finding 都标 candidate。
- 是否把 `not_verified` 升级？否；F7 是把"局部已可锚定"显式拆为两段，不是单方面升级。
- 是否给出 I 级问题对 Paper2 的学术目标影响？是；F1–F6 均说明对 A2a taxonomy 聚类 / cross-paper finding path / 证据链审计性的直接影响。
- 已知局限：未访问 `$ai-research-writing-skill` / `$research-planning` / `$autoresearch` SKILL.md（路径不可见），仅按已知口径执行；未对 paper.pdf 做版面级人工核验，Table 1–11 / Fig 1–9 精确页码留待 A2a。
