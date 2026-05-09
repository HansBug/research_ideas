# Self-Consistency — DESC

> ⚠️ **PDF 待获取**。本 DESC 基于 AI 训练知识写的初稿。

## 1. 论文元信息

- **标题**：Self-Consistency Improves Chain of Thought Reasoning in Language Models
- **作者**：Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, Denny Zhou
- **单位**：Google Brain
- **年份 / Venue**：**ICLR 2023**
- **arXiv / URL**：https://arxiv.org/abs/2203.11171
- **阅读状态**：Skim only
- **fingerprint**：multi-sample CoT + majority vote on final answer；显著提升 GSM8K / SVAMP 等推理任务

## 2. 一句话定位

> 让 LLM 在 chain-of-thought reasoning 任务上**多次采样**（temperature > 0）→ 对**最终答案**做 majority vote，比 single-shot greedy 显著提升 reasoning 准确率。**严格说不是 LLM-as-Judge 方法，但被广泛挪用到 LLM-as-Judge 场景做 score 聚合**（这是我们 W2 Q3 的来源）。

## 3. 评判对象（Judging Object）

- **类型**：reasoning task 的最终 answer（不是 judge 别人，而是让 LLM 自己产出更可靠答案）
- **典型 task**：GSM8K（数学）/ SVAMP（数学）/ AQuA / StrategyQA / CommonsenseQA
- **与 STM artifact 的相似度**：⚪ unrelated（reasoning answer vs structured model）
- **被挪到 LLM-as-Judge 时**：sample 多次 score → median / majority

## 4. 输入 / 输出（I/O）

| 项 | 内容 |
|---|---|
| **输入** | (1) 同一 question；(2) CoT prompt；(3) sample N 次（典型 N=40，T=0.5-0.7）|
| **输出** | majority answer（频次最高的最终答案，忽略 reasoning chain 内容差异）|

I/O schema：1 question + N samples → 1 majority answer。

## 5. Method 核心

| 维度 | 选择 |
|---|---|
| **Prompting / Training** | Pure prompting（不动权重）|
| **rubric anchor** | n/a（不是 judge，不需要 rubric）|
| **CoT** | ✓（CoT 是必需的 — 若不 CoT 则 reasoning 路径不分散，sample 多次没意义）|
| **聚合** | **majority vote on final answer**（不是 reasoning chain，是结果）|
| **采样** | T=0.5-0.7，top-p=0.95，N=10-40 |

**算法 sketch**：

```
samples = [LLM(prompt, T=0.7) for _ in range(N)]
final_answers = [extract_final(s) for s in samples]
return Counter(final_answers).most_common(1)[0][0]
```

**关键假设**：reasoning paths 多模态（多条不同推理链 → 答案分散），但**正确答案是 attractor**（多条路径都收敛到同一答案）→ majority 即对。

## 6. 评估方式

- **数据集 ground truth**：GSM8K 等数学任务有标准答案
- **metric**：accuracy（最终答案对错）
- **noise floor**：每个 N 值跑多次取均值

## 7. 报告的 effect size + noise

- GSM8K：PaLM-540B greedy 56% → SC 74%（+18%）
- SVAMP：78% → 86%
- **是否多 seed**：✓（论文系统报告了多 seed 结果）
- **是否有 noise floor 讨论**：✓（论文讨论 N 增加时 saturation；典型 N=40）
- **关键发现**：N 越大效果越好但 saturate；T 太低则 sample 同样无意义

## 8. 局限性（按 project_ex1 4 维度）

| 维度 | 局限 |
|---|---|
| **L1 Noise floor** | ✓ SC 论文本身报告 noise floor，但 generic reasoning task；**SC 被挪用到 LLM-as-Judge 时这条无 free** |
| **L2 Provider drift** | n/a（论文 PaLM-540B 那个时代）|
| **L3 Rubric anchor** | n/a（不是 judge）|
| **L4 STM 适配** | 🔴 W2 §13.3 实证：**SC 假设在 rubric+iter_b 锁定输出空间下完全失效** —— sample variance ≈ 0，median 等同 single sample。**不应将 SC 直接迁移到 anchored-rubric LLM-as-Judge** |

## 9. 对 project_ex1 的可借鉴性

### 9.1 不借鉴 — 这是 W2 的重要负面结论

- **W2 Q3 实测**：在 rubric+iter_b 锁定下，N=3 sample 的 max_dim_std=0.0039（mean），median 与 any single sample 等价；SC confidence 公式 `1−α·max_dim_std` 直接塌到 0.99 触碰下游 confidence threshold heuristic 导致 trade-off 假象
- **W2 audit 结论**：SC 在结构化锁定输出空间上是 design failure，不应 publish 为 STM-judge 的 best practice

### 9.2 借鉴

- **Multi-sample 思维**作为 noise floor protocol 的灵感来源 —— 我们 5-rep noise floor design（V4）就是这条线的延续，**但聚合层面取消了 SC，改用 strict-llm 单 rep + 跨 rep mean ± std**
- **N saturate 实测**：W2 stage 1 三 source 等价（mean_max_dim_std 0.024-0.029）也印证了 N saturate

### 9.3 对比 baseline

paper §Related Work 引用方式：

> "Wang et al. [Wang23a] proposed Self-Consistency, which improves CoT reasoning by majority voting over multiple samples. **Subsequent LLM-as-Judge work (e.g. Liu23, Zheng23) attempted to apply this to score aggregation**. **However, our W2/W3 study shows that SC fails as a confidence-source in anchored-rubric LLM judging on STM artifacts: rubric form-filling locks the output space such that sample variance becomes uninformative**, while the SC-derived confidence formula `clip(1−α·max_dim_std, 0.10, 0.99)` interacts catastrophically with downstream confidence-thresholded metrics."

## 10. 引用导出

```bibtex
@inproceedings{wang2023self,
  title={Self-Consistency Improves Chain of Thought Reasoning in Language Models},
  author={Wang, Xuezhi and Wei, Jason and Schuurmans, Dale and Le, Quoc V. and Chi, Ed H. and Narang, Sharan and Chowdhery, Aakanksha and Zhou, Denny},
  booktitle={The Eleventh International Conference on Learning Representations (ICLR)},
  year={2023}
}
```
