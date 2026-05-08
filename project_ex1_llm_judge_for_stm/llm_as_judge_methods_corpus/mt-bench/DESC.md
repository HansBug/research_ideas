# MT-Bench / LLM-as-a-Judge — DESC

> ⚠️ **PDF 待获取**。本 DESC 基于 AI 训练知识写的初稿，正式 paper writing 前需读全文修订。

## 1. 论文元信息

- **标题**：Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena
- **作者**：Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, Ion Stoica
- **单位**：UC Berkeley + LMSYS
- **年份 / Venue**：**NeurIPS 2023 Datasets & Benchmarks Track**
- **arXiv / URL**：https://arxiv.org/abs/2306.05685
- **阅读状态**：Skim only
- **fingerprint**：80 multi-turn questions × 8 categories；strong model (GPT-4) judge ~80% agreement with human; identifies position bias / verbosity bias / self-enhancement bias

## 2. 一句话定位

> 提出 **MT-Bench**（80 道 multi-turn 任务问卷）+ **Chatbot Arena**（人类 pairwise 投票），系统化研究"用强 LLM（GPT-4）判 dialogue 质量"是否可行，**确认 LLM-as-Judge 与 human 的 agreement 可达 80%+**，但同时**揭示 3 类 LLM judge bias**（position / verbosity / self-enhancement）。

## 3. 评判对象（Judging Object）

- **类型**：LLM dialogue 输出（multi-turn instruction following / conversational quality）
- **典型 task**：80 questions × 8 categories（writing / roleplay / reasoning / math / coding / extraction / STEM / humanities）
- **与 STM artifact 的相似度**：⚪ unrelated（dialogue text vs 结构化模型）

## 4. 输入 / 输出（I/O）

| 项 | 内容 |
|---|---|
| **输入** | (1) Question (single-turn or multi-turn)；(2) 两个 candidate model 的 response（pairwise 模式）；(3) 评分指引 prompt（要求 LLM 比较 helpfulness / relevance / accuracy / depth / creativity / level of detail）|
| **输出** | (a) Pairwise: A wins / B wins / tie；(b) Pointwise: 1-10 score |

I/O schema：multi-turn dialogue 输入 → discrete preference 或 1-10 score。

## 5. Method 核心

| 维度 | 选择 |
|---|---|
| **Prompting / Training** | Pure prompting（GPT-4 as judge）|
| **rubric anchor** | 🟡 partial — 通用维度（helpfulness / accuracy / depth / detail / etc）但无 domain anchor |
| **CoT** | ✓（要求 judge 给出 reasoning 再给 verdict）|
| **多轮** | ✓ multi-turn（每个 question 包含 follow-up）|
| **聚合** | 单次 / 多次取多数 |
| **Bias correction** | ✓ position swap（A/B 顺序交换两次取一致）；prompted to "ignore length/style"（缓解 verbosity bias）|

**算法 sketch**（pairwise 模式）：

```
for each (question, response_A, response_B):
    verdict_1 = LLM_judge(question, A_first=True)
    verdict_2 = LLM_judge(question, A_first=False)
    if verdict_1 == verdict_2:
        final = verdict_1
    else:
        final = "tie"  # position bias detected
```

## 6. 评估方式 — 与 human 对齐协议

- **human reviewer**：MT-Bench 由 expert humans 评（约 6 人）；Chatbot Arena 由数千用户 pairwise 投票
- **评分尺度**：pairwise preference（A wins / B wins / tie）；MT-Bench pointwise 1-10
- **与方法对齐**：agreement rate（LLM judge vs human reference）
- **inter-rater agreement**：MT-Bench 报告 expert human pairwise agreement

**主要 metric**：
- LLM-judge vs human agreement rate（avg ~80%）
- Bias 量化（position swap consistency / length 偏好率）

## 7. 报告的 effect size + noise

- GPT-4 judge agreement with human ≈ 80%（与 expert human 之间的 agreement 80% 同水平）
- **是否多 seed**：✗ 未系统报告；只在某些实验上对比 GPT-4 vs GPT-3.5 vs Claude
- **是否有 noise floor 讨论**：🟡 部分（讨论 position bias 时报告 swap consistency 但不当 noise floor）
- **典型对比 baseline**：human pairwise / 其他 LLM judge（Claude / PaLM）

## 8. 局限性（按 project_ex1 4 维度）

| 维度 | 局限 |
|---|---|
| **L1 Noise floor** | 🟡 部分讨论了 position bias swap consistency，但**不是真正的 sample-level noise floor**（多次 judge same case 的 σ）|
| **L2 Provider drift** | ✗ 论文用 GPT-4-0314 / GPT-3.5-turbo specific date；这正是 W3 揭示的 "provider drift" 的 generic 体现，但论文未深究 |
| **L3 Rubric anchor** | 🟡 通用维度（helpfulness/accuracy/depth/...）但无 domain anchor；适用于 generic dialogue, 不适用于 SE artifact 这种 domain-heavy 评判对象 |
| **L4 STM 适配** | 🔴 dialogue vs STM 完全不是一个层次的 artifact；MT-Bench 的 multi-turn 思路不可直接迁移，但 **pairwise + position-swap** 可作为 STM artifact 比较的方法学借鉴 |

## 9. 对 project_ex1 的可借鉴性

### 9.1 借鉴

- **Pairwise comparison + position swap** —— project_ex1 之前的 S2-Q5 计划就是这个方向；MT-Bench 是直接 anchor
- **Bias 分类思维**：让我们意识到 LLM judge 不仅有 noise，还有 systematic bias（position / verbosity / self-enhancement）
- **Per-category granularity**：MT-Bench 8 categories 让我们看到 category-specific judge 行为差异 —— project_ex1 的 record/summary/component/protocol 4 regime 类似思路

### 9.2 不借鉴

- **80-question fixed benchmark**：MT-Bench 是 instruction-following 数据集，不是 SE artifact；project_ex1 用 PSMBench / TTool-AI / llms_emp 等专用数据集
- **Single-shot agreement number**：W3 实证显示这种 single-shot 比较不可信，需 5-rep 给 σ

### 9.3 对比 baseline

paper §Related Work 引用方式：

> "Zheng et al. [Zheng23] established that strong LLMs (GPT-4) can achieve ~80% agreement with human experts on dialogue quality judgment, while identifying position / verbosity / self-enhancement biases. We extend this line to **structured SE artifact (state machine) evaluation**, where (a) the judging object has explicit semantic structure that pairwise comparison alone cannot capture, requiring per-dim rubric scoring; (b) 我们 first 给出 LLM judge on SE artifact 的 systematic noise floor。"

## 10. 引用导出

```bibtex
@inproceedings{zheng2023judging,
  title={Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena},
  author={Zheng, Lianmin and Chiang, Wei-Lin and Sheng, Ying and Zhuang, Siyuan and Wu, Zhanghao and Zhuang, Yonghao and Lin, Zi and Li, Zhuohan and Li, Dacheng and Xing, Eric P. and Zhang, Hao and Gonzalez, Joseph E. and Stoica, Ion},
  booktitle={Advances in Neural Information Processing Systems},
  year={2023}
}
```
