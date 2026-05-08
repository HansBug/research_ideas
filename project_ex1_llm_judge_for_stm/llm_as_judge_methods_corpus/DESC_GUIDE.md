# LLM-as-Judge 方法学单篇 `DESC.md` 写作规范

## 0. 目标

每篇 `DESC.md` 是该论文的 **方法学单篇分析文件**，作为 paper writing 时 `§Related Work` / `§Background` / `§Comparison` 章节的直接素材。

写作以**软件工程方向**为视角：每一节都关心"这个方法对 SE artifact 评判可不可借鉴 / 怎么借鉴 / 局限是什么"。

## 1. 必备节段

### 1.1 论文元信息

- 标题（中英双语）/ 作者 / 单位 / 年份 / Venue / DOI / arXiv / URL
- 阅读状态（Skim / Section-read / Full-read）
- 主要图表 / 表格 / 公式 fingerprint（写 1-3 个让人一眼认出的信号）

### 1.2 一句话定位

> 用一句话回答："这篇是干嘛的？"

### 1.3 评判对象（Judging Object）

明确该方法评判的对象是什么类型的输出：

- 自由文本？dialog 回复？summary？translation？code？SE artifact（具体哪类）？
- **该评判对象与 STM artifact 的相似度**（粗判：strong / partial / unrelated）

### 1.4 输入 / 输出（I/O）

详细写：

- 输入：被评对象 + 参考 / oracle（如有）+ rubric / instruction
- 输出：score（连续 / 离散 / pairwise preference / explanation tuple）
- I/O schema 是否结构化

### 1.5 Method 核心

- Prompting / Training / RLAIF 哪类
- 是否有 rubric anchor（auto / pre-defined / none）
- 是否多步 CoT
- 是否有聚合（majority vote / median / weighted）
- 是否有 calibration 校正（position bias / verbosity / etc）

### 1.6 评估方式 — 与 human 对齐的协议

- human reviewer 资质 / 数量 / 训练
- 评分尺度（Likert / continuous / pairwise / pass-fail）
- inter-rater agreement 报告（κ / Spearman / pairwise % agreement）
- 与该方法对齐度（Pearson / Spearman / agreement rate）

### 1.7 报告的 effect size + noise

- 主要结果 metric（如 Spearman vs human, agreement %）
- 是否报告 σ / error bar
- 是否多 seed / 多次实验
- **是否有 noise floor 讨论**（绝大多数论文这条 = 无）

### 1.8 局限性（按 4 维度）

| 维度 | 该方法局限 |
|---|---|
| **L1 Noise floor** | 是否有 σ；W3 noise floor 视角下该方法是否仍 robust |
| **L2 Provider drift** | 是否报告 model checkpoint / API 时点；切换 provider 后稳定性 |
| **L3 Rubric anchor** | rubric 是否 anchor，谁定义，是否 SE-domain-aware |
| **L4 STM 适配** | 评判对象与 STM 的 gap，方法迁移到 STM 需要的 adaptation |

### 1.9 对 project_ex1 的可借鉴性

- **借鉴**：哪些设计可以直接 / 调整后用到 STM judge
- **不借鉴**：哪些设计在 STM artifact 上不适用 / 已失败
- **对比 baseline**：作为 §Related Work 的对比对象时，引用方式 / 比较口径

### 1.10 引用导出

- BibTeX key（与 `bibtex.bib` 一致）
- 论文 1-2 句直接引用（key argument 摘录）

## 2. 通用约束

1. 首次写 `DESC.md` 之前**必须**：
   - 读 `bibtex.bib`（核对元信息）
   - 读 `paper_content.txt`（全文，必要时回 PDF）
   - 不能只看 abstract 就写
2. 局限性章节**必须**写满 L1-L4 四维度，无信息时写 "未报告 / 待补"
3. 数学公式按仓库根 [CLAUDE.md](../../../CLAUDE.md) §2.2.2 规范（行内 `$...$`，块用 `$$ ... $$`）
4. 引用其他论文用相对路径 markdown link：`[mt-bench](../mt-bench/DESC.md)`
5. 写完后回填 [SUMMARY.md](./SUMMARY.md) 论文清单

## 3. 与 `state_machine_review_corpus/` 单篇文件的区别

| 文件 | 关心什么 |
|---|---|
| `state_machine_review_corpus/<slug>/review_extraction.md` | 该论文有哪些 review 数据可用作 reviewer benchmark 的 ground truth |
| **本文库** `llm_as_judge_methods_corpus/<slug>/DESC.md` | 该论文的**方法学**贡献是什么、可不可借鉴到 STM judge |

两者关心的角度完全不同 — review_extraction.md 关心"数据"，DESC.md 关心"方法"。
