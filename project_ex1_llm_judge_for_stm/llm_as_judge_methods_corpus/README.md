# `llm_as_judge_methods_corpus/` 论文集 README

## 1. 论文集定位

`project_ex1_llm_judge_for_stm/llm_as_judge_methods_corpus/` 是 project_ex1 下专门维护 **LLM-as-Judge 方法学论文** 的论文集工作区。

它的核心目标：把"用 LLM 评判其他 LLM/系统输出"这条研究线的关键方法学文献沉淀到一起，逐篇刻画其方法（method）、评审对象（judging object）、输入输出（I/O）、训练/Prompting 范式、局限性，作为 project_ex1 论文 §Related Work 的直接素材。

## 2. 与本项目其他论文集的关系

| 论文集 | 内容 | 用途 |
|---|---|---|
| **本论文集**（`llm_as_judge_methods_corpus/`）| LLM-as-Judge 方法学论文（G-Eval / MT-Bench / Prometheus / ...） | 作为 paper §Related Work 的方法学溯源 |
| **`state_machine_review_corpus/`**（同级）| 含 human STM review 的论文（PSMBench / TTool-AI / llms_emp / ...） | 作为 reviewer benchmark 的数据来源 |
| **`../project_1_llm_state_machine_modeling/baselines/`** | LLM 状态机生成方法 baseline（62 篇） | 作为 reviewer 评判**对象**的方法集合 |

**三个文库的角色**：
- **本论文集** = "怎么评" 的方法学
- **state_machine_review_corpus** = "评谁的人类 ground truth"
- **baselines** = "评的对象（被评制品的来源）"

## 3. 收录范围

### 3.1 收录条件（同时满足才算 🟢 直接可用）

1. **核心议题**：用 LLM 作为评判器（judge / evaluator / scorer / critic / grader），输出对某个候选输出的质量判断
2. **方法贡献**：有显式的 method 设计（不是只用 LLM 调用一下取分），含 prompting / training / aggregation 等任一层面的创新
3. **评测范式**：明确给出输入（被评对象 + 评判 protocol）/ 输出（score / judgement / preference / explanation）/ 与 human 的对齐方式

### 3.2 优先收录

1. **LLM-as-Judge 方法学经典**：G-Eval / MT-Bench / Prometheus / JudgeLM / Constitutional AI / Self-Consistency / Tian verbalized confidence ...
2. **结构化制品评估**：超出 generic dialog / summary / translation 的工作（包括 code review / spec review / model review / artifact eval ...）
3. **Calibration / Reliability 议题**：LLM judge 的偏差 / 一致性 / position bias / verbosity bias / 校准等
4. **Cross-domain transfer**：LLM judge 在专域（代码 / 法律 / 医疗 / SE artifact）的扩展

### 3.3 不收录

1. 纯文本生成的内容评测（如 dialog quality） 但**没有 method 创新**的论文
2. 只用 LLM 一次性评分（无 rubric 设计、无 calibration、无 inter-rater 处理）的论文
3. 评判对象是图像 / 多模态而非语言 artifact 的工作（除非方法可迁移到 STM）
4. 未公开（无 arXiv / 无可获取版本）的论文

## 4. 收录单论文目录约束

每篇论文目录至少包含：

1. `paper.pdf`（PDF 原文；若暂无可标 "PDF 待获取" 在 DESC.md 顶部）
2. `paper_content.txt`（用 `tools/pdf_extractor.py` 抽取；PDF 到位后才能产出）
3. `bibtex.bib`（论文引用）
4. `DESC.md`（单篇方法学分析，结构见 [DESC_GUIDE.md](./DESC_GUIDE.md)）

## 5. 工作流程

向本论文集添加新论文时：

1. 先读所属 [GUIDE.md](./GUIDE.md) 和 [SUMMARY.md](./SUMMARY.md)
2. 按 §3 判断该论文是否在收录范围
3. 创建 `<paper-slug>/` 目录
4. 放入 `paper.pdf` + `bibtex.bib`
5. 用 `python -m tools.pdf_extractor -i ... -o ...` 生成 `paper_content.txt`
6. 阅读全文后写 `DESC.md`（按 [DESC_GUIDE.md](./DESC_GUIDE.md)）
7. 回填到 [SUMMARY.md](./SUMMARY.md) 总账

## 6. 当前收录状态

详见 [SUMMARY.md](./SUMMARY.md)。当前收录 **7 篇方法学论文**（PDF 全部 ⏳ 待获取）：

1. G-Eval (Liu et al., EMNLP 2023)
2. MT-Bench / LLM-as-Judge (Zheng et al., NeurIPS 2023)
3. Constitutional AI (Bai et al., 2022)
4. Verbalized Confidence (Tian et al., 2023)
5. Self-Consistency (Wang et al., 2023)
6. Prometheus (Kim et al., 2024)
7. JudgeLM (Zhu et al., 2023)
