你是 PR #135 的 `codex` 学术 reviewer。请只审计单篇论文 `ml4se-tertiary-study`，不要开启 sub-subagent，不要修改仓库文件，不要 push，不要 gh comment。

    你的任务是对该论文进行全文级学术审计，判断当前 `review.md` 中“维度树复原”是否完整、准确、可追溯，尤其检查树是否过小、是否把通用 6 个 leaf 接口误当成原文 schema、是否遗漏原文 RQ / extraction form / taxonomy / coding scheme / roadmap figure / evidence table / finding path / quality / validity / artifact 字段。

    必须使用并体现以下技能口径；你需要自行读取这些 SKILL.md / reference 文件后再审计：
    - `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/paper-story.md`
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`
- `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`
- `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`
- `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`

    必须读取以下文库级规则和 story：
    - `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/README.md`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/GUIDE.md`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/SUMMARY.md`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/patterns/pattern-field-schema.md`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/story/paper_story.md`

    必须读取该单篇的以下文件；`paper_content.txt` 必须尽可能全文阅读，不允许只看摘要或 grep 几个词：
    - `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/ml4se-tertiary-study/bibtex.bib`
    - `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/ml4se-tertiary-study/metadata.json`
    - `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/ml4se-tertiary-study/paper_content.txt`
    - `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/ml4se-tertiary-study/review.md`
    - 必要时核对 `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/ml4se-tertiary-study/paper.pdf` 的页码、图表或表格；如果无法视觉核对，必须说明。

    输出必须写入：`project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-19x3/results/ml4se-tertiary-study__codex.md`。请在最终回答中只简要说明写入路径和 C/I/M 摘要。

    审计报告必须使用中文，并包含以下结构：

    # ml4se-tertiary-study · codex 全文审计报告

    ## 1. 审计身份与输入
    - reviewer 身份：codex
    - 是否读取 `$ai-research-writing-skill`：是/否 + 读取路径
    - 是否读取 `$research-planning`：是/否 + 读取路径
    - 是否读取 `$oh-my-codex:autoresearch`：是/否 + 读取路径
    - 是否完整阅读 `paper_content.txt`：是/否 + 简述覆盖范围
    - 是否核对 `paper.pdf`：是/否 + 原因

    ## 2. 原文真实结构复原
    - 原文 RQ / 目标 / 贡献声明
    - 原文方法流程、检索 / 纳排 / 数据抽取 / 编码 / 统计 / finding 形成方式
    - 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric
    - 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

    ## 3. 当前 `review.md` 维度树审计
    | 检查项 | 结论 | 证据 / 理由 | 严重度 |
    |---|---|---|---|
    | 根节点是否准确 |  |  | C/I/M/通过 |
    | 主干分支是否覆盖原文 schema |  |  | C/I/M/通过 |
    | 叶子维度是否足够具体 |  |  | C/I/M/通过 |
    | 取值空间是否可执行 |  |  | C/I/M/通过 |
    | 关系边是否缺失 |  |  | C/I/M/通过 |
    | 统计用途 / 分母是否正确 |  |  | C/I/M/通过 |
    | 候选 finding 路径是否完整 |  |  | C/I/M/通过 |
    | A.1--A.4 证据链是否足够 |  |  | C/I/M/通过 |
    | 是否存在可能误导 A2a 的强主张 |  |  | C/I/M/通过 |

    ## 4. 建议维度树骨架
    给出你认为更忠实于原文的维度树，至少包含：根节点、主干分支、叶子维度、每个叶子的候选取值空间、是否可统计、缺失值语义、证据来源定位。若当前 review 已足够，请说明为什么。

    ## 5. 必须补充 / 修正清单
    | 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
    |---|---|---|---|---|

    ## 6. C/I/M 结论
    - C：直接破坏 Paper2 学术目标、证据链或后续 A2a/A2b 可靠性的问题。
    - I：会实质影响维度树可用性、原文 schema 复原、证据可审计性的问题。
    - M：不阻塞的清晰度或维护性建议。
    - 最终建议：READY / NEEDS FIX。

    审计原则：
    - 不允许为凑完整而臆造原文没有的字段。
    - 不允许把 roadmap / vision / proposal 写成完成型统计 finding。
    - 不允许把 `not_verified` 或泛定位证据升级成可统计结论。
    - 如果当前树只是通用接口而非原文 schema，必须指出并给出最小修复方案。
    - C/I 必须说明对 Paper2 学术目标或证据链的影响。
