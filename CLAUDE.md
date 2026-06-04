# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此代码仓库中工作时提供指导。
`AGENTS.md` 是 `CLAUDE.md` 的软链接，本质上是同一个文件，不要重复修改两份。

## 仓库概述

这是一个专注于**基于大语言模型（LLM）的控制系统状态机建模与验证**的博士研究仓库。研究旨在构建一个覆盖"生成-验证-修复"全生命周期的自动化、迭代式闭环方法，系统性解决从非形式化需求到高可信度形式化模型的转化难题。

## 研究背景

本仓库包含博士论文的相关材料，涵盖四大研究主题：

1. **基于控制系统软件需求的LLM状态机结构化建模方法**
2. **基于模型元素的验证场景与待验证性质生成方法**
3. **基于验证剖面的状态机验证方法**
4. **面向已知缺陷的迭代式模型修复方法**

关键技术焦点：
- 时间自动机理论与时间约束
- 基于模型检查的形式化验证
- 安全性质、活性性质和时序逻辑（LTL/CTL）
- 带守卫条件的层次化状态机
- LLM能力与形式化方法的融合

## 仓库结构

- `phd_proposal/` - LaTeX格式的博士开题报告文档
  - `phd_proposal_report/` - 主开题报告
  - `phd_proposal_literature_review/` - 文献综述文档
- `project_1_llm_state_machine_modeling/` - 研究内容一：基于LLM的状态机结构化建模
- `project_2_verification_scenario_generation/` - 研究内容二：验证场景与性质生成
- `project_3_profile_based_verification/` - 研究内容三：基于验证剖面的状态机验证
- `project_4_iterative_model_repair/` - 研究内容四：迭代式模型修复
- `project_ex1_llm_judge_for_stm/` - **计划外项目（ex = extra/unplanned）**：针对状态机制品的 LLM-as-Judge 评审子系统，从 project_1 拆出独立。**边界**：本项目专注 reviewer 系统 + 评审方法学，不做 STM 生成（那是 project_1 的 baselines/）/ verification（那是 project_2/3）/ repair（project_4）。详见该目录下的 [README.md](./project_ex1_llm_judge_for_stm/README.md)。
- `talks/` - 与导师、同门、合作者等人类讨论的纪要工作区
- `llm_model_landscape/` - **根目录 LLM 模型现状微型文库**：长期维护 project_1 及后续研究常用 LLM / hosted API / 开放权重模型的发布时间、上下文窗口、最大输出、官方价格与来源链接；以 [README.md](./llm_model_landscape/README.md)、[GUIDE.md](./llm_model_landscape/GUIDE.md)、[SUMMARY.md](./llm_model_landscape/SUMMARY.md) 为入口，并用 [01-baseline-models.md](./llm_model_landscape/01-baseline-models.md)、[02-openai-models.md](./llm_model_landscape/02-openai-models.md)、[03-claude-models.md](./llm_model_landscape/03-claude-models.md)、[04-gemini-models.md](./llm_model_landscape/04-gemini-models.md)、[05-deepseek-models.md](./llm_model_landscape/05-deepseek-models.md)、[06-qwen-models.md](./llm_model_landscape/06-qwen-models.md)、[07-llama-models.md](./llm_model_landscape/07-llama-models.md)、[08-grok-models.md](./llm_model_landscape/08-grok-models.md)、[09-other-open-models.md](./llm_model_landscape/09-other-open-models.md) 维护完整表；所有模型表默认按发布时间从高到低排序，baseline 文献表按 year 从高到低排序。
- `ccf_venues/` - **根目录 CCF venue 情报库**：长期维护与本仓库四个 project 相关的 CCF 会议 / 期刊官方主页、CFP、important dates、论文名录、论文数量、年度状态与跨 venue 投稿时间线；以 [README.md](./ccf_venues/README.md)、[GUIDE.md](./ccf_venues/GUIDE.md)、[SUMMARY.md](./ccf_venues/SUMMARY.md)、[TIMELINE.md](./ccf_venues/TIMELINE.md)、[01-venue-scope.md](./ccf_venues/01-venue-scope.md) 为入口。
- `tools/` - Python工具集（详见下方"工具使用说明"）
  - `pdf_extractor.py` - PDF文本提取工具
  - `init_talk_workspace.py` - 讨论工作区初始化工具
- `TARGET.md` - 研究内容综合总结（中文）
- `requirements.txt` - 仓库工具与PPT工作流所需的Python依赖

**论文组织方式**：论文资料可以出现在仓库的任何路径下（如各个 `project` 目录、专题文献目录、baseline 目录等），但后续统一按“**论文集路径** + **单论文路径**”两级结构组织；单论文路径是基础单元，论文集路径是其上级汇总与操作入口（详见下方“论文文件管理规范”）。

**讨论纪要组织方式**：根目录 `talks/` 专门用于维护与人类讨论形成的纪要草稿与定稿，不按论文集结构管理；其具体规则见下方“讨论纪要工作区规范”。

**LLM 模型现状文库组织方式**：根目录 [llm_model_landscape/](./llm_model_landscape/) 是 LLM 模型现状微型文库，用于维护模型可用性、发布时间、context / max output、价格和官方来源。处理模型选型、baseline 模型矩阵、LLM 价格/上下文窗口更新、Qwen/Llama/Grok/DeepSeek/Gemini/GPT/Claude 等模型信息时，默认先读 [llm_model_landscape/README.md](./llm_model_landscape/README.md)，再读 [llm_model_landscape/GUIDE.md](./llm_model_landscape/GUIDE.md)，最后读 [llm_model_landscape/SUMMARY.md](./llm_model_landscape/SUMMARY.md) 获取统计结论与重点模型；需要完整表时跳转到各分册。所有正式模型表默认按**发布时间从高到低**排列，且必须使用可点击官方来源链接。

**CCF venue 情报库组织方式**：根目录 [ccf_venues/](./ccf_venues/) 是 CCF 会议 / 期刊情报库，用于维护官方主页、CFP、重要时间点、论文名录、论文数量、状态、核心人员情报与投稿时间线。处理 CCF venue、会议 deadline、期刊 special issue、2022 年以来年度主页、论文名录、核心人员情报或投稿规划时，默认先读 [ccf_venues/README.md](./ccf_venues/README.md)，再读 [ccf_venues/GUIDE.md](./ccf_venues/GUIDE.md)，再读 [ccf_venues/SUMMARY.md](./ccf_venues/SUMMARY.md) 和 [ccf_venues/TIMELINE.md](./ccf_venues/TIMELINE.md)，最后查 [ccf_venues/01-venue-scope.md](./ccf_venues/01-venue-scope.md) 确认 P0/P1/P2 范围。新增或修改任何 venue 年度 important date 后，必须同步更新 [ccf_venues/TIMELINE.md](./ccf_venues/TIMELINE.md) 的年度表格与 Mermaid Gantt；初始化 PR 阶段不得把待建 venue 写成已完成。

## 工具使用说明

### PDF文本提取工具（tools/pdf_extractor.py）

**重要：处理PDF文件时，优先使用此工具而非其他方法**

这是一个专门为本研究项目设计的PDF文本提取工具，支持两种提取模式：

#### 使用方法

```bash
# 文字模式（快速，适用于数字化PDF）
python -m tools.pdf_extractor -i document.pdf -o output.txt -m text

# OCR模式（适用于扫描版PDF）
python -m tools.pdf_extractor -i scanned.pdf -o output.txt -m ocr
```

#### 功能特点

- **文字模式（text）**：直接提取PDF中的文本内容，速度快，适用于电子版PDF
- **OCR模式（ocr）**：使用Tesseract OCR识别图像中的文字，支持中英文混合识别（`chi_sim+eng`），适用于扫描版PDF
- 自动按页码分隔内容（`--- Page N ---`）
- 输出UTF-8编码的文本文件

#### 重要提示

**如果使用文字模式提取的结果出现显著异常（如乱码、大量缺失内容、格式严重错乱等），请立即切换到OCR模式重新提取。**

某些PDF虽然看起来是电子版，但实际上是图片格式或使用了特殊编码，导致文字模式无法正确提取。此时OCR模式虽然较慢，但能获得更准确的结果。

#### 依赖库

- 文字模式：`PyPDF2>=3.0.0`
- OCR模式：`pdf2image>=1.16.0`, `pytesseract>=0.3.10`, `Pillow>=10.0.0`

### Python环境设置

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 讨论工作区初始化工具（tools/init_talk_workspace.py）

当需要新建一次导师/同门/合作者讨论工作区时，优先使用此工具而不是手工搭目录：

```bash
python -m tools.init_talk_workspace 2026-04-14-导师-讨论主题
```

该工具会在 `talks/` 下初始化单次讨论子目录，默认包含：

1. `prep/` - 讨论前准备材料
2. `ppt/` - `PPT_GUIDE.md`、`generate_ppt.py`、`review/` 等 deck 工作区
3. `raw.md` - 会后原始碎片
4. `minutes.md` - 结构化纪要
5. `todo.md` - 后续动作

## 论文文件管理规范

论文资料统一按两级结构组织：

1. **单论文路径**：一个目录只对应一篇论文，是最小管理单元。
2. **论文集路径**：由多个单论文路径构成的上级目录，负责定义收录范围、检索口径、汇总方式和专项整理规则。

### 1. 两级结构定义

#### 1.1 单论文路径

单论文路径是“单篇论文原文 + 提取物 + 单篇分析结果”的承载目录。目录名应简洁、稳定、可读，通常使用标题关键词、系统名或工具名构成 slug，例如：

```
some_project/
└── related_work/
    └── some-paper/
        ├── paper.pdf
        ├── paper_content.txt
        ├── bibtex.bib
        ├── desc.md
        └── 其他单篇派生文件...
```

#### 1.2 论文集路径

论文集路径是多个单论文路径的上级目录。它不是“随手堆论文”的文件夹，而是一个带有明确目标、筛选标准、维护规则和 AI 工作指导的专题工作区，例如：

```
some_project/
└── some_collection/
    ├── README.md
    ├── SUMMARY.md
    ├── GUIDE.md
    ├── STM_GUIDE.md
    ├── paper-a/
    │   ├── paper.pdf
    │   ├── paper_content.txt
    │   ├── bibtex.bib
    │   └── STM.md
    └── paper-b/
        ├── paper.pdf
        ├── paper_content.txt
        ├── bibtex.bib
        └── STM.md
```

### 2. 论文集路径规范

#### 2.1 论文集的定义与作用

论文集是由多个单论文路径构成的专题化上级路径，用于围绕某一明确研究目的持续进行：

1. 文献检索与增量收录。
2. 论文筛选与范围控制。
3. 单篇论文提取物生产。
4. 跨论文汇总、归类、统计与观察沉淀。
5. 对后续 AI 工作进行稳定、可复用的过程约束。

论文集必须回答清楚以下问题：

1. 这个论文集是干什么的。
2. 它服务于整个博士研究中的哪一部分。
3. 期望从该论文集中获得什么类型的知识、证据、数据或素材。
4. 什么样的论文应该收录，什么样的论文不应该收录。
5. 后续 AI 在这个论文集中应当优先做什么、避免做什么。

#### 2.2 论文集必备文件

每个论文集路径下，原则上必须包含以下文件：

1. `README.md`
2. `SUMMARY.md`
3. `GUIDE.md`
4. 零个或多个专项 `XXXX_GUIDE.md`

如果当前目录已经存在具有同等职责的历史文件，允许暂时兼容历史命名；但新建论文集时，优先采用 `README.md / SUMMARY.md / GUIDE.md / XXXX_GUIDE.md` 这一统一命名。

### LLM 模型现状微型文库规范

根目录 [llm_model_landscape/](./llm_model_landscape/) 不按“单论文路径 + 论文集路径”展开，而是一个入口文件 + 稳定完整表分册的微型文库；内容分册统一使用 `01-xxx.md`、`02-xxx.md` 这类两位编号文件名，以便与 [llm_model_landscape/README.md](./llm_model_landscape/README.md)、[llm_model_landscape/GUIDE.md](./llm_model_landscape/GUIDE.md)、[llm_model_landscape/SUMMARY.md](./llm_model_landscape/SUMMARY.md) 区分。后续凡是涉及模型现状、模型价格、上下文窗口、最大输出、模型发布时间、API/开放权重可获取性、baseline 模型矩阵的工作，默认遵循以下规则：

1. 先读 [llm_model_landscape/README.md](./llm_model_landscape/README.md) 明确收录范围。
2. 再读 [llm_model_landscape/GUIDE.md](./llm_model_landscape/GUIDE.md) 明确来源优先级、价格口径、排序规则和一致性检查。
3. 以 [llm_model_landscape/SUMMARY.md](./llm_model_landscape/SUMMARY.md) 作为统计结论、重点模型与分册索引入口；完整表分别维护在 [01-baseline-models.md](./llm_model_landscape/01-baseline-models.md)、[02-openai-models.md](./llm_model_landscape/02-openai-models.md)、[03-claude-models.md](./llm_model_landscape/03-claude-models.md)、[04-gemini-models.md](./llm_model_landscape/04-gemini-models.md)、[05-deepseek-models.md](./llm_model_landscape/05-deepseek-models.md)、[06-qwen-models.md](./llm_model_landscape/06-qwen-models.md)、[07-llama-models.md](./llm_model_landscape/07-llama-models.md)、[08-grok-models.md](./llm_model_landscape/08-grok-models.md)、[09-other-open-models.md](./llm_model_landscape/09-other-open-models.md)。
4. issue/PR/comment 中的一次性调研若有长期价值，应先整合进对应完整表，再更新 [llm_model_landscape/SUMMARY.md](./llm_model_landscape/SUMMARY.md) 的统计结论或重点模型。
5. 所有正式模型表默认按**发布时间从高到低**排序；baseline 文献表按 year 从高到低排序；同一系列中 hosted API、开放权重、legacy/alias 必须区分。
6. 每条模型信息必须有可点击官方来源链接；没有官方来源的内容只能标为待核验，不能写成既定事实。
7. [AGENTS.md](./AGENTS.md) 是 [CLAUDE.md](./CLAUDE.md) 的软链接，更新这类仓库级引导时只修改 [CLAUDE.md](./CLAUDE.md)，不要重复编辑两份。

### CCF venue 情报库规范

根目录 [ccf_venues/](./ccf_venues/) 不按“单论文路径 + 论文集路径”展开，而是一个入口文件 + venue 子路径 + 年度 README + [TIMELINE.md](./ccf_venues/TIMELINE.md) 的情报库。后续凡是涉及 CCF 会议 / 期刊、年度主页、CFP、important dates、论文名录、论文数量、核心人员情报或投稿时间线的工作，默认遵循以下规则：

1. 先读 [ccf_venues/README.md](./ccf_venues/README.md) 明确定位与路径结构。
2. 再读 [ccf_venues/GUIDE.md](./ccf_venues/GUIDE.md) 明确来源优先级、时间格式、会议/期刊结构和 TIMELINE 同步规则。
3. 再读 [ccf_venues/SUMMARY.md](./ccf_venues/SUMMARY.md) 获取 P0/P1/P2 分批与当前完成状态。
4. 若任务涉及 deadline、投稿窗口或年度规划，必须读 [ccf_venues/TIMELINE.md](./ccf_venues/TIMELINE.md)，并在更新年度 important date 后同步维护其表格和 Mermaid Gantt。
5. 新增或更新 venue 时，根 README 年度汇总表、年度 README 和 [ccf_venues/TIMELINE.md](./ccf_venues/TIMELINE.md) 都必须直接挂核心 URL 的 Markdown 超链接；会议至少覆盖年度主页、CFP、Important Dates、submission system、program / accepted papers、proceedings、DBLP 年度页；期刊至少覆盖 author guidelines、submission system、special issue、volume / issue、online first、DBLP 年度页。
6. 新增或更新 venue 时，venue 根 README 必须维护“核心人员情报”：会议至少覆盖当前 / 未来年度 General Chair、Program / Research Track Chair、Steering Committee、强相关 track chair 与领域权威；期刊至少覆盖 Editor-in-Chief、Co-Editor-in-Chief、Associate / Area Editor-in-Chief、Managing Editor、Editorial Board leadership 和相关 special issue guest editor；每行必须有官方角色来源、研究方向、代表作 / 近年论文线索与本仓库 project 关系，期刊人员还必须保留 `核验等级 / 当前性`。
7. [ccf_venues/TIMELINE.md](./ccf_venues/TIMELINE.md) 按事件发生年份组织，不按会议 edition 年份强行归档；会议 edition 的投稿 ddl 若发生在前一年，应进入前一年章节，并在 Venue 字段保留 edition。
8. 所有更新日志表格必须按时间降序排列，最新记录置于最上方；新增日志时插入表格首行，不追加到末尾。
9. 再读 [ccf_venues/01-venue-scope.md](./ccf_venues/01-venue-scope.md) 确认目标 venue 是否属于当前批次。
10. 初始化 PR 阶段只交付骨架和执行计划，不得把待建 venue 或待核验年度写成已完成。

#### 2.2.1 Markdown 链接规范

在 Markdown 文档中，只要是在**指引读者跳转到另一个已知 Markdown 文件**，默认都应使用**相对路径 Markdown 链接**，而不是只写文件名，也不要写绝对路径。

执行规则如下：

1. 同目录文件，写成如 `[GUIDE.md](./GUIDE.md)`。
2. 子目录文件，写成如 `[paper-a/STM.md](./paper-a/STM.md)`。
3. 上级目录文件，写成如 `[BASELINE.md](../BASELINE.md)`。
4. 只有在目标文件路径当前无法确定、它只是一个抽象占位名时，才允许继续用代码样式如 `` `XXXX_GUIDE.md` ``，不要伪造一个并不存在的链接。

这样做的目标是让人类读者在阅读仓库内文档时可以直接点击跳转，减少来回查找成本。

#### 2.2.2 Markdown 数学公式规范

当 Markdown 文档需要表达形式化定义、状态机元组、迁移规则、判定问题、复杂度或推导关系时，默认应使用 **GitHub 可正常渲染的 LaTeX 数学公式写法**。

执行规则如下：

1. **行内公式**统一使用 `$...$`
   - 例如：`timed automaton $M = (\Sigma, S, S_0, C, E)$`
2. **独立大块公式**统一使用单独成行的 `$$ ... $$`
   - 例如：

```markdown
$$
L(M') = \mathrm{Untime}(L(M))
$$
```

   - `$$` 与 `$$` 之间**必须刚好只有一行公式内容**，不要写成多行推导块，否则 GitHub 渲染容易异常。

3. 不要混用 `\(...\)`、`\[...\]`、截图公式或把公式塞进代码块来代替数学公式渲染。
4. **纯数学对象**不要用反引号包裹；例如集合、元组、关系、复杂度、公式推导应写成 `$L(M) \subseteq L(M')$`、`$O(n \log n)$`，而不是代码样式。
5. **代码标识**和**数学对象**要分开：
   - 工具名、文件名、目录名、命令行参数仍用反引号，如 `UPPAAL`、`desc.md`、`paper_content.txt`
   - 形式化对象、变量、谓词、约束、迁移关系用数学公式，如 `$x \le 2$`、`$\delta_1 \land \delta_2$`
6. 对 GitHub 数学渲染的兼容性要保守处理。默认避免使用以下容易出问题的宏或写法：
   - `\left` / `\right`
   - `\operatorname`
   - 多行 `$$ ... $$` 公式体
   - 其他未经验证的复杂排版宏
   - 推荐替代：
     - 花括号直接写 `\{` 与 `\}`
     - 自定义函数名优先写成 `\mathrm{fract}` 这类形式
     - 需要“或/且”时优先写 `\lor` / `\land`
7. 对理论性较强的单篇 `desc.md`、`GUIDE.md`、`SUMMARY.md`，若原文确有正式定义，优先至少保留：
   - 一个关键对象的公式定义
   - 一个关键构造、判定问题或复杂度结果的公式表达
8. 大块公式默认尽量短而稳，不为追求“像论文排版”而强行堆叠复杂 LaTeX；优先保证 GitHub 页面可读、可渲染、可维护。

#### 2.2.3 Markdown 表格与 emoji 列规范

当 Markdown 文档中的表格使用某一列专门承载 `状态`、`评估`、`分类`、`可获取性`、`优先级` 等 **emoji 口径** 时，默认必须遵循以下规则：

1. **emoji 列的单元格默认只写 emoji，不再重复写中文说明。**
   - 例如应写 `🟢`，而不是 `🟢 直接可用`
2. emoji 的中文释义应放在：
   - 表格前后的口径说明文字；或
   - 单独的 emoji 口径表中
3. 若该列按设计是**单值列**，默认每个单元格只放 **一个 emoji**。
4. 只有当论文集自己的 `GUIDE.md` 明确规定该列允许多值组合时，才允许写多个 emoji；否则一律按“一个单元格一个 emoji”执行。
5. 不要把“emoji + 中文解释”混写进正式总账表格单元格；这样会让表格冗长、口径不稳，也不利于后续统一维护。
6. 例外只允许出现在**单篇派生文件的短条目字段**中：若某个论文集的 `GUIDE.md` 明确要求 `desc.md` / `survey.md` 里的分类字段写成 `emoji + 中文全称`，可以按该要求执行；但这条例外**不适用于** `SUMMARY.md` 等正式总账表格。

换言之：**emoji 列负责紧凑编码，中文解释负责在列外统一定义。**

#### 2.2.4 Markdown 学术讨论 / 综述 / 文献引用与定义规范

当 Markdown 文档承担**学术讨论纪要 / 文献综述 / paper 写作起点**等正式职责（典型路径：`talks/.../minutes.md`、`discussions/*.md`、论文集 `SUMMARY.md` 中含跨文献综述部分、单篇 `DESC.md` 中含 §Related Work 引用句拟稿等），默认必须遵守以下规则：

##### A. 参考文献位置

1. **正式参考文献必须集中写在文档末尾的独立 §References / §参考文献 章节**，使用方括号编号 `[1] [2] [n]`。
2. 正文内引用统一使用 `[n]` 短形（不要在正文里整段重复 author + year + venue + URL）。
3. 编号原则：默认按**首次引用顺序** 编号；若文档分大类（如"Generic XX"、"SE-related XX"、"Foundational"），可在 §References 内分小节，但每条仍保留全局唯一编号。
4. §References 每条至少包含：编号、作者、年份、标题、Venue（含会议 / 期刊全称）、URL（arXiv / 出版页 / DOI 任一）。
5. 不要写"详见原文"这种空引用；每条必须给出可被点击或可被检索到的 URL / DOI。

##### B. 关键术语定义

讨论 / 综述类文档中**反复出现的核心术语**（如 LLM-as-Judge / rubric / noise floor / provider drift / state machine / Cohen $\kappa$ 等），默认应有一个**集中的"关键定义与术语"章节**（推荐放在 §背景 之后、§相关工作之前），并对每个术语标注：

1. **定义类型**：标注为 **"领域已有定义"** 或 **"本研究新造定义"**。
2. **领域已有定义** 必须给出参考文献（用 §References 中的编号 `[n]`）。若术语跨多家有不同口径，应说明本文使用哪一家口径。
3. **本研究新造定义** 必须说明：
   - **rationale**：为什么需要新造（既有定义不够 / 不准 / 不适用的具体原因）
   - **如何定义**：操作化的判定方式或公式
   - **与最近的既有概念的对照**：避免读者误以为是某个老概念
4. 若某术语**部分借用某既有定义但有改动**（混合情况），应同时给参考文献 + 改动说明。

##### C. 写作上的约束

1. 正文中**首次出现**的关键术语，应同时使用其**完整中英文 + 编号引用**（如 "LLM-as-Judge [1]"）；之后再次出现可省去 `[n]`。
2. 引用句拟稿（"paper §Related Work 引用方式拟稿"等）若直接放在 DESC.md / 讨论文档中，应保留方括号 `[Author25]` 或 `[n]` 占位，**不要把全文 author + year + venue 重复展开在正文**。
3. 跨文档引用（如讨论文档引用 corpus 中的 DESC.md）使用 §2.2.1 的 Markdown 相对路径链接 `[xxx](./relative/path.md)`，不替代 §References 的正式条目。
4. 若一份长讨论文档**确实没有正式 §References**（极短或纯内部记录），允许省略；但**只要文档中已经给出 `[n]` 短形引用**，就必须配套有末尾 §References。

这条规范的目标是让讨论稿可以**直接被 paper writing 复用**：定义清晰、引用可追溯、相关工作可比对，避免后续从讨论稿到论文稿大量重写。

#### 2.3 README.md 规范

`README.md` 是论文集的入口说明，主要负责“告诉人和 AI 这个论文集是什么、为什么存在、该怎么使用”。它必须面向后续自动化维护场景写清楚，不能只写成泛泛简介。

`README.md` 至少应包含以下内容：

1. **论文集定位**
   - 该论文集服务的研究主题、子任务或数据建设目标。
   - 在整个博士研究中的角色与边界。
2. **设立宗旨与期望收获**
   - 为什么需要单独建立这个论文集。
   - 希望从中沉淀什么类型的论文、提取物、统计或启发。
3. **收录范围**
   - 明确“需要什么样的论文”。
   - 明确“不要什么样的论文”。
   - 给出正例标准与反例标准，避免 AI 误收。
4. **纳入/排除判定标准**
   - 至少从研究对象、任务类型、证据形态、可提取性、与本研究相关性等维度给出标准。
   - 标准必须可执行，不能停留在抽象口号。
5. **本论文集下文件说明**
   - 逐一说明 `SUMMARY.md`、`GUIDE.md`、各专项 `XXXX_GUIDE.md` 分别负责什么。
   - 明确 AI 在开始工作前应按什么顺序阅读这些文件。
6. **单论文路径约束**
   - 说明本论文集下单论文目录至少要有哪些文件。
   - 说明本论文集特有的派生文件要求，例如 `desc.md`、`STM.md`、`notes.md`、`claims.md` 等。
7. **AI 工作入口提示**
   - 例如“先读 `README.md`，再读 `GUIDE.md`，再读 `SUMMARY.md`，最后进入具体论文目录”。
   - 需要明确写出推荐顺序和用途。

#### 2.4 SUMMARY.md 规范

`SUMMARY.md` 是论文集的总账与综合结果，不是可选文件。它用于记录当前论文集已经收录和整理到什么程度，并把对后续工作有指导价值的观察固定下来。

`SUMMARY.md` 至少应覆盖以下内容：

1. **论文集整体概况**
   - 当前收录数量。
   - 本轮新增数量。
   - 已完成的单篇派生物数量。
   - 尚未完成的条目数量。
2. **检索关键词簇分析**
   - 当前推荐关键词簇。
   - 已观察到的高命中特征。
   - 已观察到的低命中特征。
   - 检索倾向调整结论。
   - 该部分不是静态说明，必须随着实际收录结果持续修正。
   - 必须控制长度，避免无限制膨胀。
   - 默认要求：每个小节不超过 `10` 行，只保留当前最有指导意义的核心要点。
   - 维护方式应当是“整合更新”，而不是每轮机械追加旧观察。
   - 允许论文集在 `GUIDE.md` 中对该长度作二次 override，但若未明确 override，则一律按“每小节最多 10 行”执行。
3. **论文列表**
   - 必须包含指向各单论文路径的链接。
   - 每篇至少应包含：标题、年份、关键词、内容一句话简介、目录链接。
   - 只要是正式文献表格或正式论文总表，默认必须包含 `年份` 列。
   - 除非该论文集的 `GUIDE.md` 明确规定其他排序口径，否则正式文献表格默认按 `年份升序` 排列。
   - 如果该论文集的 `GUIDE.md` 另有要求，还应补充分类、领域、状态、条目数、备注、是否已完成某类提取等字段。
4. **初步归类或内部提取物整理**
   - 按 `GUIDE.md` 的要求，对论文进行初步分类、优先级划分、领域统计，或对单篇派生内容做汇总盘点。
   - 必要时应包含派生文件收获盘点、领域分布、状态口径、失败记录等。
5. **若收录综述/调查类文献，还应包含其引出的后续追踪线索**
   - 例如“由综述引出的待跟进原始文献”“survey 派生出的待补条目”“推荐下一轮优先追踪方向”等。
   - 目的不是把 survey 当成只读背景，而是把它转化成后续可执行的扩库入口。
6. **更新日志**
   - 记录每轮增量整理做了什么。
   - 记录本轮检索策略、侧重方向、主要收获和主要不足。
   - 时间字段默认必须统一使用 `yyyy-mm-dd hh:mm:ss`，保留到秒；若能从 `git log` 或其他可追溯记录恢复具体时间，则应优先回填完整时分秒，而不是只写日期。
7. **必要的失败与阻塞记录**
   - 若有下载失败、提取失败、质量异常、待补做条目等，必须有明确记录。

`SUMMARY.md` 还应满足以下维护要求：

1. **关键词簇分析要防止过拟合**
   - 不要把一轮偶然命中的细碎词堆满文档。
   - 只保留经过多篇论文验证、或对下一轮检索确实有方向价值的模式。
2. **关键词簇分析要防止信息爆炸**
   - 不是把所有搜索经验都记下来，而是压缩成“现在最值得继续试的方向”和“现在最应该回避的方向”。
3. **论文列表应是总账而不是临时便签**
   - 已正式收录的论文必须进入统一列表。
   - 不要为“本轮新增”反复创建一次性临时表，除非论文集自己的 `GUIDE.md` 明确要求。
4. **状态与统计要统一口径**
   - 统计数字必须与表格真实内容一致。
   - 状态标签、分类字段、领域字段、条目数字段在同一份 `SUMMARY.md` 内必须保持一致定义。
5. **失败记录要保留历史**
   - 下载失败、解析失败、提取失败、证据不足等情况都应记录。
   - 后续即使问题解决，历史失败记录也可保留，不要求回删。
6. **更新方式要稳定**
   - 正式论文列表原则上应在统一表格或统一清单中持续维护。
   - 不要因为每轮新增就重复新开一套临时结构，除非论文集自己的 `GUIDE.md` 明确要求。
7. **半成品也要如实入账**
   - 若论文已收录但目标派生文件尚未完成，应以 `⏳ 尚未提取` 或等价状态明确记录。
   - 不允许把“已经收录但未处理”的论文默默留在目录里而不写入总账。
8. **综述条目要承担引导职责**
   - 若某篇 `survey/review/mapping study` 已正式收录，则后续应尽量把它抽取出的代表原始文献、类别线索或后续扩库方向回写到 `SUMMARY.md`。
   - 不应把综述条目只当成“读完即止”的背景材料，而应把它转成下一轮可继续追踪的入口。
9. **年份与排序口径要稳定**
   - 正式文献表中的 `年份` 字段默认不得省略。
   - 除非论文集自己的 `GUIDE.md` 明确 override，否则正式文献表默认按 `年份升序` 排列。

若论文集需要对内部提取物进行盘点，推荐统一使用以下状态口径：

1. `🟢 直接可用`：可直接作为高质量研究素材、数据样本或证据来源。
2. `🟡 可整理`：有价值，但需要额外整理、补证或结构化加工。
3. `⚪ 未收获`：不满足目标，或无法形成可靠、可追溯的产物。
4. `⏳ 尚未提取`：论文已收录，但目标派生文件尚未完成。

`SUMMARY.md` 的核心要求是：它既要能让人一眼看到当前积累了什么，也要能让 AI 在下一轮工作时快速知道“该接着做什么”。

#### 2.5 GUIDE.md 规范

`GUIDE.md` 是论文集的 AI 自动工作指导文件，负责规定后续检索、筛选、整理、提取、汇总和回填时的技术标准与工作流程。它不是 README 的重复版，而是操作规范版。

`GUIDE.md` 至少应包含以下内容：

1. **论文集目标与任务边界**
   - 明确本论文集服务的具体任务。
   - 明确不属于该论文集目标的工作类型。
2. **检索策略**
   - 推荐数据库、检索入口、关键词簇构造方式、扩词逻辑、去偏策略。
   - 如何根据已有高命中论文反推下一轮关键词。
   - 如何避免把检索资源浪费在低命中方向。
   - 如何在多个候选方向之间保持领域覆盖平衡，而不是只在少数高产方向无限膨胀。
   - 如何控制关键词簇分析的篇幅，避免记录过长、过细、过拟合。
   - 写 `GUIDE.md` 时，这一点必须明确强调为硬约束：关键词簇相关章节应采用“压缩式整合更新”，禁止写成逐轮机械追加的检索日志或关键词堆积清单。
3. **筛选标准**
   - 收录条件。
   - 降优先级条件。
   - 排除条件。
   - 去重规则。
4. **目录与文件标准**
   - 单论文目录需要包含哪些文件。
   - 每种派生文件如何生成、何时生成、何时允许暂缺。
5. **内容整理策略**
   - 单篇论文需要提取什么。
   - 什么内容值得进入单篇派生文件。
   - 什么内容只能记入 `SUMMARY.md` 而不进入单篇文件。
6. **SUMMARY.md 撰写规范**
   - 应有哪些章节。
   - 表格/字段口径如何统一。
   - 统计、状态、更新日志如何维护。
   - 哪些部分必须整合更新，哪些部分只允许增量追加。
7. **工作流程**
   - 一轮完整工作的推荐顺序。
   - 什么时候先补历史欠账，什么时候再扩新检索。
   - 什么时候必须回写 `SUMMARY.md`。
   - 一轮结束时应完成哪些一致性检查。
8. **质量与可追溯性要求**
   - 所有结论、条目、标签、统计、提取物都应有原文依据。
   - 如果证据不足，必须如实标明，而不是臆测补齐。
9. **与专项 GUIDE 的关系**
   - 如果存在 `STM_GUIDE.md` 等专项指导，应明确规定何时跳转、何时以专项 GUIDE 为准。

`GUIDE.md` 应当足够细，能直接约束 AI 的后续自动工作，而不是只给几条原则性建议。至少还应把以下事项说清楚：

1. **关键词簇更新规则**
   - 每轮是否允许新增关键词簇。
   - 新增后如何回写到 `SUMMARY.md`。
   - 哪些观察应整合替换，哪些信息不应长期保留。
   - 应明确默认动作是“合并、替换、删减旧项”，而不是持续累计旧 bullet；如果不特别强调这一点，后续 AI 很容易把 `SUMMARY.md` 写成不断膨胀的历史流水账。
2. **去重规则**
   - 优先按 DOI 去重。
   - DOI 缺失时按标准化标题去重。
   - 标题存在轻微差异时，再结合作者、年份、会议/期刊综合判断。
3. **失败跳过规则**
   - 最近刚失败过的候选是否需要暂缓重试。
   - 相隔多久才允许再次尝试。
4. **批量规模要求**
   - 每轮检索和筛查不应过小，避免只有极少量样本导致观察失真。
   - 若论文集有自己的批量阈值，应在 `GUIDE.md` 中明确写出。
5. **回填规则**
   - 论文目录完成到什么程度时必须回填 `SUMMARY.md`。
   - 对于半成品条目应如何如实记录。
6. **一致性检查规则**
   - 检查目录是否齐全。
   - 检查统计数字是否一致。
   - 检查状态与表格是否一致。
   - 检查关键词簇分析是否仍然简洁有效。

如果论文集自己的 `GUIDE.md` 没有给出更具体要求，则默认采用以下口径：

1. **关键词簇长度默认值**
   - `SUMMARY.md` 中“当前推荐关键词簇”“高命中特征”“低命中特征”“检索倾向调整”这类小节，默认每节最多 `10` 行。
   - 编写任何新 `GUIDE.md` 时，建议把这条写得更强：长度上限不是提醒，而是优先级很高的压缩约束；接近上限时，应先删减和整合旧内容，而不是放宽长度或继续简单累加。
2. **失败重试默认窗口**
   - 同一候选论文若在最近 `5` 天内已经明确记录失败，默认跳过，不重复尝试下载或解析。
   - 超过 `5` 天后可以重新尝试；若再次失败，则继续追加新的失败记录。
3. **批量规模默认下限**
   - 一轮实际筛查的候选论文数原则上不应少于 `20` 篇。
   - 一轮最终入库的论文数原则上不应少于 `10` 篇。
   - 若因领域过窄、开放获取受限、资料稀缺等客观原因无法达到，应在更新日志中说明。
4. **去重默认优先级**
   - 先按 DOI 去重。
   - 再按标准化标题去重。
   - 最后结合作者、年份、会议/期刊做人工判断。
5. **更新顺序默认值**
   - 先补历史欠账，再做新检索。
   - 先完成单论文目录必要文件，再统一回填 `SUMMARY.md`。
   - 回填后必须复核统计、一致性和状态口径。
6. **更新日志时间格式**
   - `SUMMARY.md` 及其他文库级更新日志中的时间默认统一使用 `yyyy-mm-dd hh:mm:ss`。
   - 若历史日志当前只剩日期，但可从 `git log` 或其他可追溯来源恢复具体时间，应优先补回完整时间。

#### 2.6 其他 `XXXX_GUIDE.md` 规范

当论文集存在某类稳定、重复、需要专项约束的派生工作时，应单独建立专项 GUIDE，例如：

1. `STM_GUIDE.md`：生成 `STM.md` 的专项规范。
2. `DATASET_GUIDE.md`：从单篇材料整理数据集条目的专项规范。
3. `PROPERTY_GUIDE.md`：提取待验证性质、场景或时序约束的专项规范。

专项 GUIDE 的作用是把某一种“单篇派生物”的目标、判定标准、章节结构、证据写法、未收获处理方式固定下来。`GUIDE.md` 必须对这些专项 GUIDE 给出明确指引，包括：

1. 哪些任务必须遵循哪个专项 GUIDE。
2. 当 `GUIDE.md` 与专项 GUIDE 发生冲突时，以谁为准。
3. 哪类论文必须生成该专项文件，哪类可以不生成。

### 3. 单论文路径规范

#### 3.1 基础文件

单论文路径默认至少应包含以下基础文件：

1. `paper.pdf`
2. `paper_content.txt`
3. `bibtex.bib`

说明如下：

1. **`paper.pdf`**
   - 保存论文 PDF 原文。
   - 文件名优先统一为 `paper.pdf`。
2. **`paper_content.txt`**
   - 必须使用 `tools/pdf_extractor.py` 从 PDF 自动提取。
   - 默认先用 `text` 模式；若结果明显异常，立即切换到 `ocr` 模式。
   ```bash
   python -m tools.pdf_extractor -i "path/to/paper/paper.pdf" -o "path/to/paper/paper_content.txt" -m text
   ```
3. **`bibtex.bib`**
   - 应尽可能完整，达到可直接用于学术写作的程度。
   - 至少尽量包含 `title`、`author`、`year`、`journal/booktitle`、`pages`、`doi`、`url` 等信息。

#### 3.2 论文集派生文件

除了基础文件外，单论文路径中还应根据所属论文集的 `GUIDE.md` 或专项 `XXXX_GUIDE.md` 生成派生文件，例如：

1. `desc.md`
2. `STM.md`
3. `notes.md`
4. `claims.md`
5. 其他专题分析文件

默认规则如下：

1. 如果该路径的工作目标是“单篇深度综述/相关工作分析”，则 `desc.md` 是核心派生文件。
2. 如果该路径属于某个论文集，并且该论文集的 `GUIDE.md`/专项 GUIDE 对派生文件另有明确要求，则以论文集规范为准。
3. 不得在没有阅读所属论文集 `README.md + GUIDE.md + SUMMARY.md` 的情况下，擅自假定该路径应该生成什么派生文件。

生成任何单篇派生文件前，默认必须先完成以下阅读动作：

1. **先读 `bibtex.bib`**
   - 用于确认标题、作者、年份、会议/期刊、DOI、链接等元信息。
   - 写 `desc.md`、`STM.md` 或其他派生文件时，不应跳过 BibTeX 而直接凭 PDF 首页目测填写元信息。
2. **再读 `paper_content.txt`**
   - `paper_content.txt` 是单篇内容分析的默认主入口。
   - 如果文件不存在，应先基于 `paper.pdf` 生成，而不是直接只看 PDF 零散摘录后开始写派生文件。
3. **尽可能完整阅读 `paper_content.txt`**
   - 为了保证信息完整性，应尽量通读全文，而不是只做高度选择性的局部检索。
   - 至少应覆盖摘要、引言、方法、实验/案例、结论、相关工作/参考文献等关键部分；若任务涉及提取控制逻辑，还应重点覆盖系统描述、需求、设计、案例分析等部分。
4. **必要时回到 `paper.pdf` 核对**
   - 当 `paper_content.txt` 存在提取错误、图表缺失、公式断裂、版式歧义时，再回到 PDF 原文补证。

换言之，单篇派生文件的默认信息流应是：

`bibtex.bib` → `paper_content.txt`（尽量完整阅读）→ `paper.pdf`（必要时核对）→ 派生文件

不推荐的做法包括：

1. 只看标题、摘要或关键词就直接写 `desc.md`。
2. 只在 `paper_content.txt` 中搜索几个词命中后就跳过其余正文。
3. 不读取 `bibtex.bib`，直接凭 PDF 首页手动拼元信息。
4. 没有生成 `paper_content.txt` 就直接从 PDF 零散摘录内容。

#### 3.3 单篇 `desc.md` / `DESC.md` 的规范来源

仓库根级规范不再内嵌统一的 `desc.md` 长模板。

后续若需要生成、重写或审阅单篇 `desc.md` / `DESC.md`，应按以下顺序寻找约束来源：

1. 优先读取所属论文集的 `GUIDE.md`。
2. 若该论文集存在 `DESC_GUIDE.md` 或其他专项 GUIDE，再读取对应专项 GUIDE。
3. 若论文暂时不属于任何论文集，至少仍需遵守本文件 `3.2` 中的原文阅读顺序：`bibtex.bib -> paper_content.txt -> paper.pdf（必要时） -> 派生文件`。

默认原则如下：

1. 单篇分析必须基于原文与可追溯证据，不能臆测补齐。
2. 若论文涉及代码、仓库、数据集或 benchmark 获取方式，应在单篇分析中明确写出获取入口或说明“原文未提供”。
3. 若所属论文集已经定义了 `简报`、`重要的相关工作`、比较表字段或 emoji 评估口径，应完全以论文集规范为准，不再重复发明新结构。

### 4. 推荐工作流程

#### 4.1 新建论文集时

建议按以下步骤操作：

1. 先明确该论文集服务的研究目标、边界和期望收获。
2. 创建论文集目录。
3. 先写 `README.md`，把目标、范围、纳入/排除标准和文件说明讲清楚。
4. 再写 `GUIDE.md`，规定检索、筛选、整理、汇总和回写规则。
5. 如存在稳定的专项派生任务，再补 `XXXX_GUIDE.md`。
6. 初始化 `SUMMARY.md`，建立总账框架、字段口径和初始统计。
7. 最后再开始批量收录单论文目录。

#### 4.2 向论文集中新增单篇论文时

建议按以下步骤操作：

1. 先阅读该论文集的 `README.md`、`GUIDE.md`、`SUMMARY.md`，必要时再读专项 `XXXX_GUIDE.md`。
2. 根据论文集规则判断该论文是否应该收录。
3. 在论文集下创建新的单论文目录。
4. 放入 `paper.pdf`。
5. 完成 `bibtex.bib`。
6. 使用 `tools/pdf_extractor.py` 生成 `paper_content.txt`；若已存在，则先检查提取质量是否可用。
7. 在生成任何单篇派生文件前，先读取 `bibtex.bib` 确认元信息。
8. 以 `paper_content.txt` 作为主入口尽可能完整阅读论文正文，默认不应只抽读局部命中段落；必要时回到 `paper.pdf` 核对。
9. 按论文集要求生成对应的单篇派生文件，例如 `desc.md`、`STM.md` 等。
10. 最后统一更新 `SUMMARY.md`。
11. 必要时再更新仓库级综述文件，如 `TARGET.md`。

#### 4.3 处理独立单篇论文时

如果某篇论文暂时不属于任何论文集，建议按以下顺序执行：

1. 创建单论文目录。
2. 放入 `paper.pdf`。
3. 生成 `paper_content.txt`。
4. 完成 `bibtex.bib`。
5. 在生成派生文件前，先读取 `bibtex.bib`，再尽可能完整阅读 `paper_content.txt`，必要时回到 `paper.pdf` 核对。
6. 按需要生成 `desc.md` 或其他派生文件。

### 5. 阅读现有材料的推荐顺序

#### 5.1 阅读论文集时

当任务涉及一个已有论文集时，推荐按以下顺序阅读：

1. **先读 `README.md`**：理解这个论文集是什么、为什么存在、收什么、不收什么。
2. **再读 `GUIDE.md`**：理解后续检索、筛选、整理、汇总和回写的规则。
3. **再读 `SUMMARY.md`**：了解当前收录现状、关键词簇、分类、统计和历史进展。
4. **如有专项任务，再读相关 `XXXX_GUIDE.md`**：例如某个面向状态机提取、性质提取或数据集整理的专项 GUIDE。
5. **最后进入单论文目录**：先看该论文已有的派生文件，再回到 `paper_content.txt` 与 PDF。

#### 5.2 阅读单篇论文时

当需要了解一篇现存论文的内容时，应按以下顺序阅读：

1. **首先阅读单篇派生文件**：如 `desc.md`、`STM.md` 等，它们是结构化总结与整理结果。
2. **如需更多细节，再阅读 `paper_content.txt`**：这是从 PDF 提取的完整文本。
3. **必要时回到 `paper.pdf`**：用于核对图表、版式、公式和提取异常处。

但如果任务不是“了解已有整理结果”，而是“新生成或重写单篇派生文件”，则应改用以下优先级：

1. **先读 `bibtex.bib`**：锁定元信息。
2. **再读 `paper_content.txt`**：作为主要内容依据，且应尽量完整阅读。
3. **最后读 `paper.pdf`**：作为核对与补证材料。
4. **完成派生文件后，再回看已有派生文件**：只用于一致性检查或补充比较，不能反过来替代原文阅读。

这种顺序能够：

1. 快速把握核心内容和已有整理结果。
2. 避免在大量原始文本中迷失。
3. 根据需要逐步深入技术细节。
4. 节省重复阅读成本。

## 讨论纪要工作区规范

### 1. 路径定位

根目录 `talks/` 用于存放**我与导师、同门、合作者或其他人类对象的讨论纪要**。它服务的不是论文收录，而是把“讨论前准备 -> deck 准备与 review -> 会后原始碎片 -> AI 扩写 -> 人工纠偏 -> 纪要定稿”这条迭代链稳定下来。

该路径默认适合以下材料：

1. 会后凭记忆快速写下的原始片段。
2. 围绕研究方向、论文结构、实验设计、选题边界、推进节奏的讨论纪要。
3. 需要经过多轮补充、澄清和修订才能稳定下来的共识记录。

该路径默认不负责以下内容：

1. 单篇论文原文与派生分析。
2. 已可直接归档到某个 `project` 或论文集的正式研究产物。
3. 临时闲聊、无研究价值且无需追溯的聊天碎片。

### 2. 目录结构

`talks/` 下默认采用“**单次讨论一个子目录**”的方式组织，推荐结构如下：

```text
talks/
├── README.md
├── GUIDE.md
└── 2026-04-14-导师-状态机边界/
    ├── prep/
    │   ├── notes.md
    │   └── materials.md
    ├── ppt/
    │   ├── PPT_GUIDE.md
    │   ├── generate_ppt.py
    │   ├── deck.pptx
    │   ├── assets/
    │   ├── rendered/
    │   └── review/
    │       └── notes.md
    ├── raw.md
    ├── minutes.md
    └── todo.md
```

默认规则如下：

1. 单次讨论目录名默认优先使用 `yyyy-mm-dd-对象-主题`。
2. 如果同一天有多次相近讨论，为避免冲突，可以扩展为 `yyyy-mm-dd-hh-mm-对象-主题`。
3. `对象` 应尽量稳定，如 `导师`、`组会`、`同门`、`合作者`。
4. `主题` 只保留短关键词，不要写成长句。

### 3. 单次讨论目录文件规范

单次讨论目录默认包含以下文件：

1. `prep/`
   - 讨论前准备材料目录。
   - 默认至少包含 `prep/notes.md` 与 `prep/materials.md`。
   - `prep/notes.md` 用于写本次要解决的问题、当前判断和想确认的点。
   - `prep/materials.md` 用于列出需要回看的论文、路径、图表或数据。
2. `ppt/`
   - 讨论配套 deck 工作区。
   - 默认维护 `PPT_GUIDE.md`、`generate_ppt.py`、`deck.pptx`、`assets/`、`rendered/`、`review/notes.md`。
   - 其中 `PPT_GUIDE.md` 是 deck 的上游真源，`generate_ppt.py` 是唯一生成入口。
3. `raw.md`
   - 原始输入文件。
   - 存放会后立即写下的记忆片段、关键词、半句、疑问和不完整判断。
   - 原则上保留原始表达，不应用 AI 扩写文本直接覆盖。
   - 若用户提供的是截图、拍照、便签、纸面草稿等“补充记忆”材料，默认优先视为**手写或非规整文本**，不要期待它适合常规 OCR。
   - 处理这类材料时，默认要求 **AI 亲自人工查看图片内容并完成人工 OCR/转录**，把可辨识碎片补入 `raw.md`；机器 OCR、外部识别工具或脚本只能作为辅助校对，不能代替人工判断。
   - 若字迹潦草、遮挡严重或局部无法确认，应显式标注“待确认”“字迹不清”或等价说明，保留不确定性，不要为了流畅擅自脑补成完整结论。
   - 除非用户明确要求进一步整理，否则这类补录默认只做“忠实转录与轻度归拢”，不提前扩写成 `minutes.md` 风格的结构化纪要。
4. `minutes.md`
   - 扩写后的结构化纪要。
   - 由 AI 基于 `raw.md` 和用户后续纠正反复重写，直到形成可用版本。
5. `todo.md`
   - 可选文件。
   - 当讨论直接产生了后续任务、待确认材料或行动项时再创建。

默认不要求 `SUMMARY.md`，因为 `talks/` 不是论文集，总账应保持轻量。

### 4. PPT 工作流与 `deck-workflow` skill 规则

当某次讨论需要准备 PPT 时，默认必须遵循以下规则：

1. 优先检查本地是否已安装 `deck-workflow` skill：`~/.codex/skills/deck-workflow/SKILL.md`。
2. 若未安装，使用以下命令安装，而不是临时绕开：
   ```bash
   python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
     --repo HansBug/deck-workflow-skill \
     --path deck-workflow
   ```
3. 安装后需要**重启 Codex** 才能在新会话中自动拾取该 skill。
4. 在本仓库里，`ppt/` 下**统一使用 Python 后端**，文件名固定为 `generate_ppt.py`，不要改成 `generate_ppt.js`。
5. Python 依赖统一安装到仓库已有环境里：若当前有激活的 conda 环境就用 conda；否则使用仓库根目录已有 `venv`。
6. 不要在 `talks/.../ppt/` 下再创建新的 `.venv`、`venv` 或局部 Python 环境。
7. `python-pptx`、`PyMuPDF`、`Pillow`、`pdf2image` 等依赖统一由仓库根目录 `requirements.txt` 管理。
8. `soffice`、`pdftoppm` 或字体等系统依赖若缺失，可以直接安装，不要为了规避安装而跳过 review 链。
9. deck 的默认生产链必须是：`PPT_GUIDE.md -> generate_ppt.py -> deck.pptx -> rendered/ -> review/notes.md -> 回写源文件 -> 重新生成`。

### 5. 编写与修订规则

处理 `talks/` 下材料时，默认遵循以下规则：

1. 先读 [talks/README.md](./talks/README.md) 和 [talks/GUIDE.md](./talks/GUIDE.md)，再进入具体讨论目录。
2. 新建讨论时，优先先写 `prep/notes.md` 与 `prep/materials.md`，讨论后再写 `raw.md`。
3. 若需要讲解材料，先维护 `ppt/PPT_GUIDE.md`，再改 `ppt/generate_ppt.py`，不要直接把 `deck.pptx` 当唯一编辑入口。
4. AI 扩写 `minutes.md` 时，应把“用户明确说过的内容”和“为使语义完整做出的补全”区分开来。
5. 如果某个结论、表述顺序或动作项只来自模糊记忆，应明确写成“待确认”或“根据上下文推测”，不能把不确定内容写成既定事实。
6. 用户后续纠正优先级高于先前扩写版本；如两轮内容冲突，应重写 `minutes.md`，而不是机械并列堆积冲突版本。
7. `raw.md` 是原始记忆入口，除非用户明确要求整理原稿，否则不应把它改写成 polished 纪要。
8. 若讨论最终沉淀出明确的研究决策、任务拆分或对仓库已有材料的修订要求，应在 `minutes.md` 中写清楚落点路径或目标对象。
9. 若用户说的是“补充记忆”“把这张图里的内容补进去”“先记下来再说”这类低结构任务，默认目标文件应是 `raw.md`，并默认采用“人工看图转录优先、工具识别辅助、模糊处显式保留”的策略。
10. 若 `minutes.md` 或其他正式讨论稿涉及多篇文献引用、关键术语定义、§Related Work 拟稿等学术写作素材，必须遵守 [§2.2.4 Markdown 学术讨论 / 综述 / 文献引用与定义规范](#224-markdown-学术讨论--综述--文献引用与定义规范)：
    - 参考文献集中放文档末尾，正文用 `[n]` 短形
    - 关键术语单独章节集中定义，并标注是"领域已有定义（带参考文献）"还是"本研究新造（带 rationale + 操作化）"
    - 这条同样适用于各 `project_*` / `project_ex*` 下的 `discussions/*.md`，不局限于 `talks/`

### 6. 推荐阅读与工作顺序

当任务涉及 `talks/` 时，推荐顺序如下：

1. 先读 [talks/README.md](./talks/README.md)：理解这个工作区是干什么的。
2. 再读 [talks/GUIDE.md](./talks/GUIDE.md)：理解目录命名、文件职责和扩写边界。
3. 进入目标讨论目录，先读 `prep/notes.md` 与 `prep/materials.md`，理解讨论前上下文。
4. 若存在 `ppt/` 内容，再读 `ppt/PPT_GUIDE.md` 与 `ppt/review/notes.md`，判断 deck 当前状态。
5. 讨论后处理纪要时，先读 `raw.md`。
6. 若 `minutes.md` 已存在，再读 `minutes.md`，判断当前纪要与原始片段是否一致。
7. 必要时根据用户新补充的信息重写 `minutes.md`，并把待办拆到 `todo.md`。

## 核心技术概念

### 状态机形式化
- 状态机模型：`M = (S, E, V, Tr, A)` 其中 S=状态集合，E=事件集合，V=变量集合，Tr=迁移集合，A=动作集合
- 时间状态机：`TSM = (S, S₀, E, V, C, Tr, Inv, Act)` 包含时钟约束和不变式
- 验证剖面：`SP = ⟨(E₁, C₁, τ₁), (E₂, C₂, τ₂), ..., (Eₙ, Cₙ, τₙ)⟩`
- 性质模型：`Property = (Type, Scope, Predicate, TemporalConstraint)`

### 缺陷类型
- δ型：迁移守卫错误
- τ型：时间约束违反
- state型：状态缺失或冗余

### 相关工具与框架
- UPPAAL：时间自动机验证工具
- pyfcstm：状态机领域特定语言（https://github.com/HansBug/pyfcstm）
- UML/SysML：状态机建模标准

## LaTeX文档工作说明

博士开题报告文档结构：
- 主文件：`report.tex` 或 `review.tex`
- 内容文件位于 `content/` 子目录（章节、摘要、参考文献等）
- 参考文献：`refs.bib`
- 通过XeLaTeX支持中文

编辑LaTeX文件时，请保持与现有格式和引用风格的一致性。

## 语言说明

主要文档语言为**简体中文**。在此仓库中工作时：
- `TARGET.md` 包含完整的研究总结（中文）
- LaTeX文档使用中文
- 代码注释和工具帮助文本使用中文
- 添加文档时请保持中文以确保一致性

## Git 提交信息规范

当需要执行 `git commit` 时，默认使用中文提交说明，并采用如下格式：

```text
xxx(xxx): 中文标题

- 中文修改点 1
- 中文修改点 2
- 中文修改点 3
```

约束如下：

1. `xxx(xxx)` 中的 `type` 与 `scope` 必须使用英文小写。
2. `:` 后面的标题必须使用中文，简明概括本次提交的主要目的。
3. 提交正文默认使用多行 `- 中文说明` 的形式，逐条列出关键改动。
4. 若本次修改范围主要集中在某个论文集、专题或目录，`scope` 应优先使用该路径或专题的英文名，例如 `docs(uppaal)`、`data(open_explore)`、`fix(project_1)`。
5. 若确实只需要一行标题，也应优先遵守 `type(scope): 中文标题` 这一行格式，不要退化为全英文提交信息。

## GitHub PR 创建规范

当需要创建 GitHub PR 时，默认遵循以下规则：

1. PR 标题应与本轮改动目标一致，优先使用中文概括主要目的；若仓库当前已有稳定英文前缀习惯，可兼容，但正文仍默认使用中文。
2. PR 描述必须使用**中文详细概述**本轮：
   - 已经完成了什么；
   - 修改影响哪些目录、论文集、规则或产物；
   - 若当前工作尚未结束，还计划继续做什么；
   - 当前仍有哪些已知限制、待验证项或后续入口。
3. PR 不能只写一句话概述；默认应至少包含“已完成内容”和“后续计划/待补方向”两部分。
4. 创建 PR 时，若仓库存在 `.github/labels.yml` 或其他已知标签配置，应主动根据改动内容添加**合适的 label**，而不是留空。
5. 创建 PR 时，默认应根据**当前提交者身份**确定 assignee：
   - 先读取 `git config user.name` / `git config user.email`；
   - 再结合当前仓库远端、已知 GitHub 用户名或 CLI 登录身份，映射到最可能对应的 GitHub 账号；
   - 若能稳定确定该账号，则将其设为 assignee；
   - 若当前身份无法可靠映射到 GitHub 用户名，再说明原因，不要随意指定他人。
6. 若本轮改动明显仍处于持续推进中，PR 默认应考虑添加 `status:wip` 或等价状态标签。
7. 若本轮改动同时涉及规范更新、总账更新、结构调整等多种类型，label 应覆盖主要方面，但不应滥贴无关标签。

## 学术研究仓库 Review 口径规范

本仓库首先是博士研究仓库，不是生产级工程产品仓库。所有 code review、PR review、subagent review、CI 修复建议和主 session 汇总，都必须服务于**学术目标、实验可靠性、结论可复现性与研究证据链完整性**，不能反过来让纯工程洁癖牺牲研究推进节奏。

### 1. C/I/M 分级总原则

当 reviewer 要求按 `C/I/M`（critical / important / minor）分级时，默认采用以下口径：

1. **C / critical**：会直接破坏学术目标、实验结论、核心数据、可复现性或下游 Path 1 / Path 2 可靠性的严重问题。
2. **I / important**：虽不一定立刻导致完全失败，但会实质性影响功能正确性、实验可靠性、数据完整性、trace 可审计性、RepairReview/LLM review 判定可靠性，或可能使论文中的方法论结论站不住脚的问题。
3. **M / minor**：不影响上述学术目标与实验可靠性的工程改进建议，包括但不限于静态类型、LSP/pyright、style、命名、docstring、clean-code、轻微性能优化、局部重构、覆盖率锦上添花等。

换言之：**C/I 必须能说明它如何影响学术目标或实验可靠性；如果说不清楚，只能算 M 或 backlog。**

### 2. 工程性问题默认不阻塞

除非能给出严格可复现证据表明某个工程性问题会破坏预期功能、实验数据、运行记录、下游接入或学术结论，否则以下问题默认不得作为 C/I 阻塞：

1. `pyright` / LSP / 类型注解收窄问题。
2. `Literal` / `cast` / 类型 checker 不满意但运行时测试和对抗用例通过的问题。
3. 代码风格、命名、docstring、注释完整度、clean-code 偏好。
4. 非关键路径性能优化、缓存优化、重复计算优化。
5. 非核心覆盖率缺口，尤其是已经有功能测试、对抗测试或 smoke test 证明关键路径可靠时。
6. 可以后续 hardening 的局部工程韧性建议。

这些问题可以被记录为 M 级、follow-up issue 或 hardening backlog；但**不应该为了它们阻塞合并、牺牲研究节奏或打断 agent-loop / Path1 / Path2 的主线推进**。

### 3. 功能正确性也要以学术目标为锚

功能 bug 是否升级为 C/I，要看它是否会影响研究目标。例如：

1. 会导致 DSL parse / semantic / design / sim / repair-review 关键反馈错误，从而影响实验结论：可列 C/I。
2. 会导致 `AgentLoopRunRecord` 缺失关键证据，影响复盘、审计或论文证据链：可列 C/I。
3. 会导致 Path 1 / Path 2 数据集接入、grounding、scenario、trace 或指标统计失真：可列 C/I。
4. 只是局部 API 不够优雅、类型不够漂亮、实现不够生产级，但不影响上述结果：默认 M。

也就是说，功能正确性之所以重要，是因为它支撑学术实验与结论；review 时必须围绕这个目标判断严重性，而不是套用通用生产级软件的阻塞标准。

### 4. Reviewer 输出要求

后续 reviewer 在 PR comment 中提出 C/I 问题时，默认必须同时给出：

1. 该问题如何影响学术目标、实验可靠性、数据完整性、trace 可审计性或结论可复现性。
2. 严格可复现的最小例子、命令、测试片段或具体数据路径。
3. 期望行为与实际行为的差异。
4. 若只是工程 hardening 或生产级质量建议，应主动降级为 M，并明确“不阻塞”。

主 session 汇总 review 时，也应按上述口径复核 reviewer 的 C/I 分类；如果 reviewer 把纯工程性问题误列为 C/I，主 session 应当降级处理，而不是机械接受。

## GitHub CLI 身份一致性规范

当需要执行任何 `gh` 命令时，默认遵循以下硬性规则：

1. 在执行前，必须先确认**当前仓库的 git 身份**与**准备使用的 GitHub CLI 身份**一致。
2. `git 身份`至少应通过 `git config user.name` 与 `git config user.email` 确认；`gh 身份`至少应通过 `gh auth status`、当前活动账号以及仓库远端归属综合确认。
3. 只有当 `gh` 当前活动账号能够与当前仓库里用于 `commit / push / PR / comment / edit / assign / label` 的身份稳定对应时，才允许继续执行 `gh` 操作。
4. 若发现 `gh` 当前活动账号与当前仓库 git 身份不一致，必须先切换到一致的账号，再执行对应 `gh` 命令。
5. 若本机找不到与当前仓库 git 身份稳定对应的 GitHub CLI 账号，或无法可靠证明两者一致，则**不得执行任何 `gh` 操作**；此时应如实说明原因和阻塞点，而不是用其他账号代操作。
6. 这条规则适用于所有 `gh` 场景，包括但不限于：`pr view`、`pr create`、`pr edit`、`pr comment`、`issue comment`、`api` 直调、label / assignee / reviewer 修改等。

## 数据集信息

研究使用来自9个控制系统的101条功能安全需求数据集：
- 系统：BSN、CARA、Elevator、Microwave、PBA、Radar、Stopwatch、TCS、VHL
- 状态机模型包含5-27个状态、3-13个事件、1-12个变量、7-27个迁移
- 数据来源：公开数据集、工具案例、工业实践

## 外部参考

研究中提到的关键相关工作：
- TTool-AI（Apvrille & Sultan）：SysML块图和状态机生成
- UPPAAL：实时系统验证
- ISO 26262、IEC 61499：工业安全标准
