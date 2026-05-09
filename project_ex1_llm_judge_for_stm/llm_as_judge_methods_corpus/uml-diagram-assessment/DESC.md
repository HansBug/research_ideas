# Toward Automated UML Diagram Assessment — DESC

## 1. 论文元信息

- **标题**：Toward Automated UML Diagram Assessment: Comparing LLM-Generated Scores with Teaching Assistants
- **作者**：Nacir Bouali, Marcus Gerhold, Tosif Ul Rehman, Faizan Ahmed
- **单位**：University of Twente
- **年份 / Venue**：CSEDU 2025（17th International Conference on Computer Supported Education，SCITEPRESS）
- **URL**：https://www.scitepress.org/Papers/2025/134819/134819.pdf
- **阅读状态**：Skim（已读 abstract + 部分 method）
- **fingerprint**：**首批针对 UML class diagram 的 LLM-as-Judge 实证**；用 92 个学生作业对比 LLM grader 与 TA grader，metrics 是 Pearson correlation 与 MAE

## 2. 一句话定位

> 在 software design 课程中用 **LLM 给 UML class diagram 打分**，与 3 位 TA 的人评对照；**GPT o1-mini 与 Claude Sonnet 与 TA 的 Pearson 相关性达 0.76+，MAE < 4 / 40 分**——证明 LLM grader 可达到 TA 水平的 UML 自动评估。

## 3. 评判对象（Judging Object）

- **类型**：UML class diagram（结构性 SE artifact，**非** behavioral model）
- **典型 task**：教学场景下评学生提交的 UML class diagram
- **与 STM artifact 的相似度**：🟡 **partial** — class diagram 也是 graph-structured UML artifact，与 state machine 同源（都是 UML），但 class diagram 是 structural model 而 STM 是 behavioral model；**两者评分 rubric 维度有显著差异**

## 4. 输入 / 输出（I/O）

| 项 | 内容 |
|---|---|
| **输入** | (1) Case study description + design constraints；(2) Student-submitted UML class diagram → 转成 textual description（pipeline 内做转换）；(3) Grading rubric + graded examples（few-shot）|
| **输出** | (a) Per-criterion score；(b) Total score（0-40 分制）|

I/O schema：(textualized diagram + rubric + examples) → LLM grading → numeric scores。

## 5. Method 核心

| 维度 | 选择 |
|---|---|
| **Prompting / Training** | **Pure prompting**（无 fine-tune） |
| **rubric anchor** | ✓ — 显式 grading rubric 作为输入；few-shot 提供 graded examples |
| **CoT** | partial（论文中是 standardized prompts；具体 CoT 程度需读全文确认） |
| **聚合** | n/a |
| **Calibration** | partial — 报告了 LLM 总分与子项之和不一致的问题（reviewer 自己发现的 bug） |
| **Bias correction** | ✗ |

## 6. 评估方式

- **human reviewer**：是 — 3 位 TA 用同一 rubric 评分
- **dataset size**：92 个学生提交
- **metric**：(a) LLM 与 TA 之间的 Pearson 相关系数；(b) MAE（Mean Absolute Error）
- **inter-rater agreement**：3 TA 之间的相关性也作为 baseline

## 7. 报告的 effect size + noise

- GPT o1-mini Pearson > 0.76，MAE < 4（满分 40）
- Claude Sonnet 类似水平
- Llama 性能弱于 GPT/Claude
- **GPT 与 Claude 之间的相关性高于它们各自与 TA 的相关性**——暗示 LLM 之间共享某些"机器视角"的偏置
- **是否多 seed**：✗
- **是否有 noise floor 讨论**：✗

## 8. 局限性（按 project_ex1 4 维度）

| 维度 | 局限 |
|---|---|
| **L1 Noise floor** | ✗ 单 seed |
| **L2 Provider drift** | ✗ 不讨论；3 个 LLM 跨 provider 但不分析时序 / 缓存 |
| **L3 Rubric anchor** | ✓ — **本文是少数显式 anchored rubric** 的 LLM grading 实证；rubric 由教学团队制定，不是 auto-generated |
| **L4 SE artifact** | 🟡 — class diagram 与 STM 同属 UML 但结构语义差异大；**直接借鉴 rubric 维度不可行**，但 anchored-rubric LLM grading 的方法论 可以借鉴 |

## 9. 对 project_ex1 的可借鉴性

### 9.1 借鉴

- **Anchored rubric + LLM grading 与人评对照** 是与我们方法学最相似的实验设计；其 Pearson > 0.76 / MAE < 4 是"LLM-as-Judge 在 UML 制品上可达 TA 水平"的实证支撑
- **Diagram → text 转换 pipeline** 思路：UML 视觉 artifact 输入 LLM 前都要文本化；STM 也面临类似问题（我们走 PlantUML / pyfcstm DSL 文本化路线，与 Bouali25 同思路）
- **3 LLM 跨 family 的对照设计**：可作为我们 multi-provider drift 实验的 reference
- **报告 LLM 总分与子项之和不一致** 的 finding：与我们 W2 confidence-formula bug 的 motivating example **同类型缺陷**——LLM 在多步打分时容易在汇总环节出 bug

### 9.2 不借鉴

- Class diagram rubric 维度（覆盖度 / 命名 / 关联多重性等）不能直接迁移到 STM
- 单 seed 实验

### 9.3 对比 baseline

paper §Related Work 引用方式（拟稿）：

> "Bouali et al. [Bouali25] demonstrated that LLM graders (GPT o1-mini, Claude Sonnet) achieve Pearson correlations above 0.76 with teaching assistants on UML class diagrams under an anchored grading rubric, providing the first empirical evidence that LLM-as-Judge can match human graders for UML artifacts. **Our work extends this evidence to UML behavioral models** — specifically state machines, which add transition guards / temporal semantics absent from class diagrams — and complements it with a multi-replication noise-floor protocol that Bouali et al. do not address."

## 10. 引用导出

```bibtex
@inproceedings{bouali2025uml,
  title={Toward Automated UML Diagram Assessment: Comparing LLM-Generated Scores with Teaching Assistants},
  author={Bouali, Nacir and Gerhold, Marcus and Rehman, Tosif Ul and Ahmed, Faizan},
  booktitle={Proceedings of the 17th International Conference on Computer Supported Education (CSEDU 2025)},
  year={2025},
  publisher={SCITEPRESS}
}
```
