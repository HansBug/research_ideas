# CodeJudge — DESC

## 1. 论文元信息

- **标题**：CodeJudge: Evaluating Code Generation with Large Language Models
- **作者**：Weixi Tong, Tianyi Zhang
- **单位**：Huazhong University of Science and Technology + Purdue University
- **年份 / Venue**：**EMNLP 2024**
- **arXiv / URL**：https://arxiv.org/abs/2410.02184
- **代码**：https://github.com/VichyTong/CodeJudge
- **阅读状态**：Skim（已读 abstract + intro + method 概述）
- **fingerprint**：LLM-as-Judge for code generation；提出"slow thinking"两条 prompting 路径——(a) analyze-and-summarize 与 (b) taxonomy-guided fault localization；test-case-free

## 2. 一句话定位

> 不依赖 test case，用 LLM 当 judge **直接评判 LLM 生成代码的语义正确性**；提出两条 slow-thinking 路径：先逐步分析再二元判定，或先用错误 taxonomy 做定位再加权打分。

## 3. 评判对象（Judging Object）

- **类型**：LLM 生成的源代码（Python / Java / C++ 等多语言）
- **典型 task**：HumanEval 类 NL → code 任务、CoNaLa、APPS、CodeContests
- **与 STM artifact 的相似度**：🟡 **partial** — 代码也是结构化、可执行 SE 制品，与 STM 同属"SE artifact"大类；但代码是文本流式可执行序列，STM 是图结构化迁移系统，结构语义差异大

## 4. 输入 / 输出（I/O）

| 项 | 内容 |
|---|---|
| **输入** | (1) NL task description（用户意图）；(2) Generated code（被评 candidate）；(3) （Method B）错误 taxonomy（论文给出 9 类常见 coding errors）|
| **输出** | (a) **Method A — Analysis + Summarization**：(step-by-step analysis text + binary correct/incorrect 判定)；(b) **Method B — Taxonomy-Guided**：(detected error types + per-type severity + 综合 0-100 correctness score) |

I/O schema：NL intent + code → CoT analysis → binary 或 graded score。

## 5. Method 核心

| 维度 | 选择 |
|---|---|
| **Prompting / Training** | **Pure prompting**（无 fine-tune；2024 年开始的 prompting-only 趋势之一） |
| **rubric anchor** | partial — Method B 用 9 类 error taxonomy，但 taxonomy 是论文作者凭经验列出，非领域专家广泛 anchor |
| **CoT** | ✓ — "slow thinking" 是核心卖点 |
| **聚合** | n/a（单 LLM 单次） |
| **Calibration** | ✗（论文未做） |
| **Bias correction** | ✗ |
| **多 LLM as evaluator** | ✓ — 实验 GPT-3.5 / GPT-4 / Mistral-7B / Llama-3-8B 4 个 |

## 6. 评估方式

- **human reviewer**：是 — 使用 CoNaLa 等数据集中含的人工标注作 ground truth
- **metric**：与 human judgment 的 Pearson / Spearman 相关系数；binary 准确率
- **inter-rater agreement**：依赖底层数据集的人评质量

## 7. 报告的 effect size + noise

- 与 SOTA GPT-3.5-based 方法相比，相关系数提升 12.1% – 41.8%
- Llama-3-8B + CodeJudge 方法 > GPT-3.5 + 旧方法
- Method A 在 binary 判定上达 80.56% 准确率（4 LLM 平均）
- **是否多 seed**：✗
- **是否有 noise floor 讨论**：✗

## 8. 局限性（按 project_ex1 4 维度）

| 维度 | 局限 |
|---|---|
| **L1 Noise floor** | ✗ 单次实验 |
| **L2 Provider drift** | ✗ 不讨论；实验跨 4 个 LLM 但未做时序 / 缓存 / 重复实验 |
| **L3 Rubric anchor** | partial — Method B 的 9 类 taxonomy 是论文作者构造，不是 SE 社区广泛接受的 review 维度 |
| **L4 STM 适配** | 🟡 — 思路完全可借鉴，但对象差异大；STM judge 不能套用 9 类 coding error，需要自己的 STM-specific error taxonomy |

## 9. 对 project_ex1 的可借鉴性

### 9.1 借鉴

- **Slow thinking** 思路：与我们 rubric_dim_score 的 "evidence first → score" CoT 形态高度一致，但 CodeJudge 的 Method B taxonomy 输入是闭环 schema 用法的更简版本
- **Test-case-free evaluation** 立场：与我们一致——SE artifact 不应只靠 oracle 评判
- **Multi-LLM evaluator 比较设计**：可作为 V4 多 provider 实验设计参考

### 9.2 不借鉴

- 9 类 error taxonomy 不能直接迁移到 STM；STM 错误类型（迁移漏掉、状态合并/拆分错误、不变式不满足等）与代码错误类型不同
- 单 seed 实验设计——我们已经做 5-rep，比 CodeJudge 的实验纪律更严格

### 9.3 对比 baseline

paper §Related Work 引用方式（拟稿）：

> "Tong & Zhang [Tong24] proposed CodeJudge, a test-case-free LLM-as-Judge for code generation that introduces two complementary 'slow thinking' prompting strategies. While CodeJudge demonstrates that prompting-only LLM judges can outperform automated metrics on code, it neither addresses evaluator stochasticity (single-seed) nor provider drift, and its taxonomy of 9 coding errors does not transfer to graph-structured artifacts such as state machines. Our work generalizes the test-case-free LLM-as-Judge paradigm to STM artifacts and adds a 5-replication noise-floor protocol."

## 10. 引用导出

```bibtex
@inproceedings{tong2024codejudge,
  title={CodeJudge: Evaluating Code Generation with Large Language Models},
  author={Tong, Weixi and Zhang, Tianyi},
  booktitle={Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing (EMNLP)},
  year={2024}
}
```
