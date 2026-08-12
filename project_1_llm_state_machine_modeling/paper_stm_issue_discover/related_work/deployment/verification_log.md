# 一手核验记录

> ⭐ 本文件只放**主 session 亲自取原文核过**的条目，⛔ 不放 subagent 的转述。⭐ 层 3 的 C1 事实核验结果也并入这里。

## V1 · ⭐⭐ Zadenoori et al. 那句「2% 可接受」——⭐ 引文属实，⛔ 但**我们不能照抄**

**对象**：[arXiv:2510.21443](https://arxiv.org/abs/2510.21443)，*Large vs Small Language Models for Requirements Classification*（Zadenoori et al.），⛔ **arXiv preprint，v1，2025-10-24，作者自称 "preliminary study"，⛔ 无同行评审状态**。

⭐ **核验方式**：下载 PDF 全文并用 `tools/pdf_extractor` 提取（⚠️ **`abs` 页只有摘要，摘要里没有这句**——⛔ 只查 abs 页会误判成引文有误）。⭐ 原句在正文第 6 页：

> we argue that a loss of 2% can be considered acceptable, given the advantages of SLMs in data privacy and resource efficiency.

⭐ **这确实是「用私域部署把不利差距论证成可接受」的现成句式**，⛔ 但它成立依赖四个条件，⛔ **我们一个都不满足**：

| # | 它的条件 | ⛔ 我们的处境 |
| :-: | :-- | :-- |
| **1** | ⭐ 差距是 **2% F1** | ⛔ 我们是 **15.82pp** |
| **2** | ⭐⭐ 该差距 **not statistically significant**（⭐ 原文同段还自陈八个模型样本量小、⛔ 有 Type II error 风险） | ⛔ 我们的 15.82pp 约为代次内噪声底（极差 **2.04pp**）的 **8 倍**，⛔ 不在噪声内 |
| **3** | ⭐ 任务是**需求分类**，⭐ 且 SLM 在部分数据集的 recall 上**反超** | ⛔ 我们是生成型任务，⛔ 且无任何口径反超 |
| **4** | ⭐ 它比的是 **SLM vs LLM**（⭐ 同任务换模型） | ⛔ 我们的 15.82pp 是**方法 vs 朴素基线**（⛔ 同模型换方法） |

### ⛔⛔ 由第 4 条导出的结论：⭐ 两个比较不能混，⛔ 隐私论证只救得了其中一个

⭐ 这是本条核验最重要的产出：

| 比较 | 内容 | ⭐ 隐私论证能不能救 |
| :-- | :-- | :-- |
| **A** | ⛔ 我们的方法 **60.4%** vs 朴素基线 **76.2%**（⛔ Δ = −15.82pp，⛔ 同一批 SOTA 模型） | ⛔⛔ **救不了。** ⛔ 私域部署与「换了方法反而更差」无关，⛔ 这两件事在因果上不相接 |
| **B** | ⏳ 小模型 + 我们的方法 vs SOTA + 我们的方法（⛔ **未测，属 N1b**） | ⭐ **正好适用。** ⭐ 若差距落在噪声底内，⭐ 这就是一个干净的 model-substitutability parity claim，⭐ 且 Zadenoori 的句式**可以合法借用** |

⛔ **所以照抄那句话之前必须先问：你在给哪个比较找台阶。** ⭐ 给 B 找是合法的；⛔ 给 A 找是偷换——⛔ 它把「我们的方法造成的损失」伪装成「私域部署造成的损失」。

⚠️ ⛔ **而 B 目前一个数都没有**（⭐ N1b 硬依赖 M1）。⛔ 故本轮 N1a **不得**把这条句式写进任何结论性表述，⭐ 只能登记为「⭐ 若 N1b 落在噪声内则可用」的**条件性素材**。

⭐ **证据等级**：⭐ 引文 **M**（⭐ 一手 PDF 逐字）；⛔ 其学术分量 **弱**（⛔ preprint、⛔ 未评审、⛔ 作者自陈 preliminary、⛔ 八模型样本）。⛔ **可引作「他人也这么论证过」的先例，⛔ 不可引作权威依据。**

## V2 · ⭐⭐⭐ Abdulkarim et al. 的 crossover——⭐ 全部证实，⭐⭐ 且它把小模型路线从「退路」变成「⭐ 方法被预测生效的那个区间」

**对象**：[arXiv:2604.00275](https://arxiv.org/abs/2604.00275)，*Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models*，Abdulkarim / Boyd / Bridi / Tufenkjian / **Boqi Chen** / **Gunter Mussbacher**（McGill），⭐ **2026-03-31**。⛔ **arXiv preprint，⛔ 录用状态未核**。

⭐ **核验方式**：下载 PDF 全文提取，⭐ 逐字读 Table III–VI 与 RQ3 结论段。

### ⭐ 事实（⭐ 全部一手核过）

| 策略 | Claude 3.5 Sonnet $F_1$ | GPT-4o $F_1$ |
| :-- | --: | --: |
| **Single-Prompt Baseline** | ⭐ **0.7029**（⭐ 最高） | 0.5431 |
| Structure-Driven SMF | 0.5026 | 0.6260 |
| Event-Driven SMF | 0.3052 | 0.3735 |
| Hybrid Approach | 0.6336 | ⭐ **0.6559**（⭐ 最高） |

⭐ **crossover 干净且方向明确**：⭐ 在 Claude 3.5 Sonnet 上**朴素单提示打败全部三个多阶段框架**；⛔ 在 GPT-4o 上**多阶段反超**。⭐ 作者自己的解释逐字：

> while non-reasoning LLMs benefit from multi-step generation strategies, such strategies **may interfere with the inherent step-by-step reasoning process of reasoning LLMs**

### ⭐⭐⭐ 它对我们意味着什么

⭐ 我们主臂跑的是**真正的 reasoning 模型**（`gpt-5.5` / `claude-opus-4-7`），⛔ 而我们的方法是**多阶段流水线**。⭐⭐ **这篇论文恰好预测了我们观察到的方向**——⛔ 多阶段脚手架在强推理模型上会**干扰**而非帮助。⭐ 也就是说，⛔ 我们的 −15.82pp **不是孤立的实现失败**，⭐ 而是一个**同制品域已被记录的现象**。

⭐⭐ **由此，小模型路线的性质变了**：⛔ 它不是「打不过 SOTA 所以退到小模型」，⭐ 而是「**多阶段脚手架这类干预，其适用区间本来就是能力较弱的模型**」——⭐ 而这有同制品域的已发表证据。

### ⛔⛔ 但有五条限定，⛔ 一条都不能省

1. ⛔ **它是 preprint**，⛔ $n = 8$ 个建模问题、⛔ 只测 2 个模型。⛔ 证据基础薄。
2. ⛔⛔ **作者自陈污染了 crossover 的幅度**，⭐ 逐字：「the strict post-processor module for HTML tables **may suppress valid LLM outputs** that are not fully compliant, hence influencing the final result」。⭐⭐ **这正是本仓库 `CLAUDE.md` §11 那条纪律的外部案例**——⛔ 故**方向可信，⛔ 幅度不可信**。⭐⭐ 且它给我们一条**必须先做的自查**：⛔ **在把 −15.82pp 归因于「多阶段干扰」之前，必须先排除我们自己的契约门 / 致命门吃掉了正确产出。**
3. ⚠️ ⛔ **它的「reasoning vs non-reasoning」轴是自定义的**：⛔ 它把 **Claude 3.5 Sonnet 归为 reasoning-focused**，⛔ 而那并不是 o1 式的 test-time-compute 推理模型。⛔ 故这可能是**两个模型之间的个体差异**，⛔ 而非一条「推理/非推理」定律。⛔ **不得引作定律。**
4. ⚠️ **任务不同**：⭐ 它做的是状态机**生成**，⛔ 我们做的是状态机**缺陷发现**。⭐ **同制品、邻近任务**，⛔ **不是同任务**——⛔ 不得写成「同任务域」。
5. ⛔⛔ **它反过来也能伤我们**：⭐ 若「多阶段只在弱模型上有用」成立，⛔ 审稿人可以说「⛔ 那你的方法只对明年就会过时的弱模型有用」。⭐ 这条必须在 Q5 里有预答。

### ⛔ 它与仓库既有裁定的关系：⭐ 不是矛盾，⭐ 是一条必要的区分

⚠️ [`route_selection_and_v47_plan.md`](../../discover_matrix/docs/findings/route_selection_and_v47_plan.md) §一 写「⛔ 换弱模型只会让『想到该问什么』更差」，⭐ 依据是 Huang (ICLR 2024) 与 Stroebl 不可能性定理。⛔ **两处原文我都读过，⭐ 它们并不冲突**——⭐ 因为**干预类型不同**：

| 干预类型 | 机制 | ⭐ 对弱模型 |
| :-- | :-- | :-- |
| ⛔ **自我批判**（Huang / Stroebl / ⛔ 我们现在的 loop） | ⛔ 让模型判断自己的产出对不对 | ⛔ **更差**——⛔ 判断能力正是弱模型缺的 |
| ⭐ **多阶段分解**（Abdulkarim 的 SMF） | ⭐ 给模型一个子任务脚手架，⭐ 替它做规划 | ⭐ **更好**——⭐ 它补的正是弱模型缺的规划 |

⭐⭐ **而我们的方法两样都有。** ⭐ 仓库已实测：⛔ 自我批判那部分**吃掉 79% token 而净收益 ≈ 0**。⭐⭐ **所以合起来给出一个比任一单独证据都更硬的预测**：⛔ **砍掉自我批判环、⭐ 保留分解脚手架、⭐ 换到弱模型上跑**——⭐ 那正是文献预测本方法生效的区间。⭐ 这与 M1 已确立的设计原则一（⛔ 不要问「这写得对吗」，⭐ 要告诉它「还有这些没查」）**同向**。

⛔ **本条不推翻既有裁定**，⭐ 只给它补一条区分维度。⛔ 是否据此调整路线排序，⛔ 归 R1 / M1，⛔ 不在 N1a 权限内。

## V3 · ⛔⛔ Chou–Aydemir–Dalpiaz (REFSQ 2026)——⭐ 全部证实，⛔ 且比转述更狠，⭐ 但它埋着一个反向支点

**对象**：Chou, Aydemir, **Dalpiaz**, *A Comparative Study of Large and Small Language Models for Domain Model Extraction*, ⭐ **REFSQ 2026**, LNCS pp. 336–351, DOI [10.1007/978-3-032-21423-2_23](https://doi.org/10.1007/978-3-032-21423-2_23)。

⭐ **核验方式**：⛔ Springer 要鉴权（303 → idp），⭐ 改从 **Dalpiaz 个人主页自存版**取 PDF 全文（`papers/chou-ayde-dalp-26-refsq.pdf`）并提取，⭐ 逐字核摘要、§4.1 与结论段。

⚠️ ⛔ **先纠一处转述混淆**：⭐ REFSQ 2026 有**两篇**相关论文，⛔ 汇报措辞里被并成了一条——⭐ 本篇（Chou–Aydemir–Dalpiaz，**领域模型抽取**）与 ⭐ Mallya–Ferrari–Zadenoori–Dąbrowski 的 *From Online User Feedback to Requirements*（**用户反馈**，⭐ 那句「open, lightweight alternatives **to improve transparency and reproducibility**」出自后者）。⭐ [mde_re_venue_scan.md](./mde_re_venue_scan.md) 的**正文分得很清楚**，⛔ 混淆只在汇报层。

### ⛔ 事实（⭐ 逐字）

⭐ 摘要：「We compare **GPT-o1, Llama3-8B, and Qwen-14B** with the rule-based **Visual Narrator** using nine datasets … **GPT-o1 outperformed the smaller language models** and matched or exceeded Visual Narrator in most tasks. Small language models produced **competitive but less consistent** results, revealing efficiency–accuracy trade-offs.」

⭐ §4.1：「It is remarkable how, although the variants of VN are **from a decade ago**, they are still up-to-part (**if not better**) than the examined SLMs.」

⛔⛔ **统计部分转述里没有，⭐ 而它比措辞更硬**：⭐ Friedman 检验双指标均显著（⭐ validity $p = 0.0001246$、⭐ completeness $p = 0.003283$）；⭐ 事后 Nemenyi + Cohen's $d$ 确认 **GPT-o1 在 validity 上显著优于 Llama3-8B（$p = 0.0029$, $d = 2.343$）与 Qwen-14B（$p = 0.0056$, $d = 1.929$）**。⛔ **$d \approx 2$ 是极大效应量**，⛔ 不是边缘差异。

### ⛔ 对我们的威胁

⛔ 在**同一 venue 族、同一任务家族（需求文本 → 模型）、同一批小模型（⭐ 连 Qwen 都对上）**上，⛔ 已经有人做过统计检验，⛔ 结论是**小模型显著更差且效应量极大**，⛔ 且署名者是该子领域权威、⛔ 基线还是他自己的工具。⛔ **我们若主张平价，就是在直接反驳一篇 REFSQ 论文，⛔ 需要比它更强的证据——⛔ 而我们目前拿不出。**

### ⭐⭐ 但同一页埋着一个反向支点，⛔ 转述里漏了

⭐ 同一组检验里还有一句：⭐ GPT-o1 显著优于两个小模型，⛔ **但对 VN-P 不显著（$p = 0.3543$, $d = 0.842$）**。⭐⭐ **也就是说：⛔ 连 GPT-o1 都没能在统计上打赢一个十年前的规则式工具。**

⭐⭐ 这直接削弱**「裸覆盖率数字」这条轴本身的意义**——⛔ 而那恰恰是我们正在输的那条轴。⭐ 它给出的推论是：⛔ 在这个任务家族上，⛔ LLM 之间比覆盖率**未必是有意义的比较维度**，⭐ 差异化应当落到**产出形态**（⭐ 可求值断言、⭐ 可追溯证据链）上。

⭐ **另一条界限也要说清**：⛔ 它比的是**裸跑 vs 裸跑**（⭐ structured template prompting，⛔ 无方法层）。⭐ 我们要主张的是**小模型 + 方法 vs 小模型裸跑**——⭐ **那正是它没做的那个比较**。⛔ 故它**不证伪我们**，⭐ 但它**钉死了我们必须超过的基线**，⛔ 且必须在 Related Work 里正面处理，⛔ 躲不掉。

⭐ **证据等级 M**（⭐ 一手 PDF 逐字 + ⭐ 统计量原文）。

## V4 · ⛔⛔⛔ C2 提的两条新事实**全部证实**，⛔ 且它们合起来推翻本轮 §3.2 的推荐

### V4.1 ⛔ Abdulkarim 的 crossover **第二重污染**：⭐ 基线被多给了一个示例

⭐ 原文逐字（⭐ 一手 PDF，⭐ §Prompt settings）：

> We use a **2-shot** prompting strategy by selecting two examples from a pool of three state machines … for the single-prompt strategy we employ **3-shot** prompting

⛔⛔ **即：赢的那一方（单提示基线）拿了 3 个示例，⛔ 输的那一方（多阶段）只有 2 个。** ⭐ 这与作者自陈的「strict post-processor 可能压制合法输出」是**两重相互独立的污染**，⛔ 且**方向一致**——⛔ 两者都朝着「让多阶段看起来更差」的方向偏。⛔ **故 V2 里「⭐ 方向可信、⛔ 幅度不可信」这句话要再降一档：⛔ 连方向都只能算「⭐ 提示性」，⛔ 不能算证据。**

### V4.2 ⛔⛔⛔ VerIbmc 的逐模型消融：⭐ 我们准备搬进去的那一格，⛔ 收益已经归零

⭐ 数据（⭐ 已在 [small_model_papers.md](./small_model_papers.md) §4.6，⛔ 但**没有被提上 SUMMARY**）：

| Model | Basic | LLM-Only | Δ |
| :-- | --: | --: | --: |
| Llama-3.1-8B | 342 | 307 | **+35** |
| Qwen2.5-7B | 352 | 328 | +24 |
| GPT-OSS-20B | 424 | 409 | +15 |
| ⛔⛔ **Qwen2.5-32B** | 382 | 380 | ⛔ **+2** |
| GPT-OSS-120B | 431 | 428 | +3 |

⛔⛔ **`route_selection_and_v47_plan.md` 推荐的 `Qwen3.6-27B` 正落在这一档。** ⛔ 也就是说：⭐ 即使「脚手架在弱模型上生效」这条主张成立，⛔ **我们选的那个模型规模已经过了拐点**。

⚠️ ⛔ **但要纠正分册的一处措辞**：⭐ §4.6 标题写「**单调**衰减」，⛔ **数据并不单调**——⭐ 按 Basic 分排序是 342 → 352 → **382** → 424 → 431，⛔ 而 Δ 是 +35 → +24 → **+2** → **+15** → +3。⛔ **Qwen2.5-32B 是个反转点**：⛔ 它的绝对能力**低于** GPT-OSS-20B，⛔ 收益却**远小于**后者。

⭐⭐ **两种读法对我们都不利**：⛔ 若这是**能力律**，⛔ 那 30B 档已过拐点；⛔ 若这是 **Qwen 特有效应**，⛔ 那我们用的恰好是 Qwen。

⭐ **同一篇还给了本轮最该被抬到结论层的一条算术**（⛔ 分册 §4.6 已写，⛔ SUMMARY 漏了）：⭐ 设我们的方法在小模型上的增益为 $\Delta$、⭐ 小模型与云端 SOTA 的裸能力差为 $G$，⛔ 则 story 成立的**必要条件是 $\Delta \gtrsim G$**。⛔ VerIbmc 那个任务上 $\Delta_{\max} \approx 35$ 而 $G \approx 89$——⛔ **它做不到，⭐ 所以它老老实实用了「承认落后 + 绑定约束」而不是宣称打平。**

### ⛔ 合并推论

⛔ **本轮 §3.2 推荐的「换到弱模型上跑」，⛔ 在选型层面已被证据反对。** ⭐ C2 的处置建议成立且可执行：⭐ **加一条大开放权重臂**（⭐ 如 Qwen3.5-397B / DeepSeek / gpt-oss-120b）——⭐ 那是**分离「开放权重」与「小」的唯一手段**。⭐ 因为可复现性只推得出**开放权重**，⛔ 推不出**小**；⛔ 而同一厂商同时供 397B 与 27B，⛔ 连「必须用中国法域模型」都带不出「必须小」。
