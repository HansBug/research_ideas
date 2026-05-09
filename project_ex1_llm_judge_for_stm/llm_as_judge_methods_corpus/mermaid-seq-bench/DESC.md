# MermaidSeqBench — DESC

## 1. 论文元信息

- **标题**：MermaidSeqBench: An Evaluation Benchmark for NL-to-Mermaid Sequence Diagram Generation
- **作者**：Basel Shbita, Farhan Ahmed, Chad DeLuca
- **单位**：IBM Research, San Jose CA
- **年份 / Venue**：**NeurIPS 2025 workshop**
- **arXiv / URL**：https://arxiv.org/abs/2511.14967
- **数据集**：https://huggingface.co/datasets/ibm-research/MermaidSeqBench
- **fingerprint**：与 MCeT 同一年的 sequence diagram 评估工作，但走的是 **benchmark + LLM-as-Judge with 6 fine-grained dimensions** 的路线

## 2. 一句话定位

> 把 sequence diagram（Mermaid 文本格式）的 LLM 评估**做成正式 benchmark**：132 sample（人验 + LLM 增广 + 规则展开），用 LLM-as-Judge 在 6 个 fine-grained 维度上打分。

## 3. 评判对象（Judging Object）

- **类型**：Mermaid 文本格式的 UML sequence diagram（LLM 生成）
- **典型 task**：NL prompt → Mermaid sequence diagram
- **与 STM artifact 的相似度**：✅ **同源** — 与 MCeT 同样针对 sequence diagram，但生成与评估都用 Mermaid 文本格式（更接近"DSL 文本化的 behavioral model"），与 STM 的 PlantUML / pyfcstm 文本化路线高度同构

## 4. 输入 / 输出（I/O）

| 项 | 内容 |
|---|---|
| **输入** | (1) NL prompt 描述系统行为；(2) Generated Mermaid sequence diagram；(3) 6 维度 rubric |
| **输出** | 6 维独立打分（0-1），可聚合为总分 |

## 5. Method 核心 — 6 维度 fine-grained metric

| 维度 | 评分内容 |
|---|---|
| **Syntax** | Mermaid 语法是否正确 |
| **Mermaid Only** | 是否只输出 Mermaid 而非混入其它格式 |
| **Logic** | 序列交互逻辑是否合理 |
| **Completeness** | 是否完整覆盖 NL prompt 中的交互 |
| **Activation Handling** | activate/deactivate bar 是否正确 |
| **Error & Status Tracking** | 错误情况与状态变化是否反映 |

| 维度 | 选择 |
|---|---|
| **Prompting / Training** | Pure prompting |
| **rubric anchor** | ✓ — 6 维 anchored；与我们 7 维 rubric 同思路 |
| **CoT** | partial |
| **多 LLM as evaluator** | ✓ — 多个 LLM judges 跑 benchmark |

## 6. 评估方式

- **human reviewer**：是 — 132 个 sample 的 hybrid methodology（human verified + LLM augmented + rule expanded）
- **metric**：判断 LLM judge 在每维度上对 reference 的 alignment

## 7. 报告的 effect size + noise

- 多个 SOTA LLM 在 benchmark 上有显著 capability gaps
- **是否多 seed**：✗
- **是否报告 noise floor**：✗（即使作为 benchmark 工作，也没引入 noise floor 协议）

## 8. 局限性（按 project_ex1 4 维度）

| 维度 | 局限 |
|---|---|
| **L1 Noise floor** | ✗ — 即使作为 benchmark paper 也未做 |
| **L2 Provider drift** | ✗ |
| **L3 Rubric anchor** | ✓ — 6 维 anchored，与我们 7 维同思路 |
| **L4 STM 适配** | ✅ **同源** — sequence diagram 与 STM 同为 UML behavioral model；6 维设计可作为我们 7 维 rubric 的对照 |

## 9. 对 project_ex1 的可借鉴性

### 9.1 借鉴

- **6 维 fine-grained anchored rubric** 是与我们 7 维 rubric 几乎并行的设计；可以做对照实验"6 维 vs 7 维"或借用其某些维度名义
- **Hybrid 数据集构造方法**（human verified + LLM augmented + rule expanded）：是 Path C human review 自补的可借鉴 pattern
- **Mermaid 文本格式作为 IO**：与我们 PlantUML / pyfcstm 文本化路线同构，加强了"behavioral model 文本化后做 LLM-as-Judge"的方法学共识

### 9.2 重要差异

- **MermaidSeqBench 是 benchmark paper，本研究是 methodology paper**：他们关注 LLM 生成能力 ranking，我们关注 evaluator 的 stability + drift；目的不重叠

### 9.3 §Related Work 引用句拟稿

> "Shbita et al. [Shbita25] proposed MermaidSeqBench, a 132-sample benchmark for NL-to-Mermaid sequence diagram generation that uses an LLM-as-Judge with six fine-grained dimensions (Syntax, Logic, Completeness, etc.). Together with MCeT [Ahmed25], MermaidSeqBench evidences that LLM-as-Judge for UML behavioral models is an active research area in 2025. Our work extends this evidence to state machines (which add transition guards / temporal semantics) and adds a noise-floor protocol that neither MermaidSeqBench nor MCeT addresses."

## 10. 引用导出

```bibtex
@inproceedings{shbita2025mermaidseqbench,
  title={MermaidSeqBench: An Evaluation Benchmark for NL-to-Mermaid Sequence Diagram Generation},
  author={Shbita, Basel and Ahmed, Farhan and DeLuca, Chad},
  booktitle={NeurIPS 2025 Workshop},
  year={2025}
}
```
