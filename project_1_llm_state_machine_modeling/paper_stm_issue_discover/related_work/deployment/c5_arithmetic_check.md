# C5 · SUMMARY.md §12 事实与算术核验

> **核验对象**：[SUMMARY.md](./SUMMARY.md) §12（该节已随 2026-08-13 的 SUMMARY 重写移入 [revision_log.md](./revision_log.md)，原行号引用已失效）· **核验日期**：2026-08-13 · **核验人**：C5（事实与算术核验路）
>
> **本文件只查证，不评价结论好坏、不提改进建议。** 唯一例外是 P1-2 与 P1-3 两项，用户明确要求给出「合理区间与依据」和「漏项及其量级」，故那两节含定量替代值。
>
> **未读文件**：按任务约束，本轮未读同目录 `c1_fact_check.md` / `c2_rebuttal.md` / `c3_coverage.md`（无 `c4_*`）。凡与它们可能重叠的结论，本文件均独立取一手来源，不引用其结果。

## 0. 一句话结论

**两张表的 24 个算术格全部可复算、无一算错**，§12 的问题不在算术而在三处输入与一处时效：**(1) 「4-bit 下 8 卡节点能吃到 ~1164B，即当前最大的开放权重模型全部在内」是错的**——Kimi K3（2.8T）与 DeepSeek-V4-Pro（1.6T）两个官方开放权重模型分别是该上限的 2.4× 与 1.4×，且按原生量化体积都装不进 640 GB；**(2) `gpt-oss-120b` 的官方发布形态就是 MXFP4 原生量化**，故「BF16 234 GB」与「8-bit 117 GB」两格对应不到任何官方制品，而「4-bit 64 GB」这格恰好命中真实体积（实测 64.6 GB，误差 0.4%）但它不是我方要施加的量化、是唯一可得形态；**(3) §12.5 把 VerIbmc 的 +2 写成 `Qwen3.6-27B` 的实测值**，而该 +2 测的是 `Qwen2.5-32B`（§4.2 与 `small_model_papers.md` §4.6 均如此，§4.2 用的是「落在这一档」的类比措辞，§12.5 与 §7 第 2 行把类比升级成了实测归属）。**0.55 系数处在乐观边界但可辩护**（实测锚点 0.552–0.602，合理区间 **0.55–0.62**、中心 ~0.57）；**公式漏了框架预留、KV cache、激活与分片余量三类常驻项，合计吃掉标称容量的 10–15%**，把 640 GB / 4-bit 上限从 1164B 压到 **~990B**，也把 24 GB / BF16 从 12B 压到 **~11B**。**P2 的四条引用全部核对得上原文**，其中 §12.6 那条 YaRN 技术说法**本身成立**（`config.json` 逐字含 `original_max_position_embeddings: 4096`、`factor: 32.0`、`max_position_embeddings: 131072`），但「外推」是我方读法、OpenAI 自己的措辞是 "natively support context lengths of up to 128k"。

## 1. 确认错误

### 1.1 【最严重】「~1164B 即当前最大的开放权重模型全部在内」——不成立

§12.2 末句逐字：「8 卡节点在 4-bit 下能吃到 **~1164B 总参**，即**当前最大的开放权重模型全部在内**」。截至 2026-08-13，至少有两个官方开放权重模型超过这个上限：

| 模型 | 官方总参 | 激活 | 原生权重形态 | 许可 | 相对 1164B |
| :-- | --: | --: | :-- | :-- | --: |
| [moonshotai/Kimi-K3](https://huggingface.co/moonshotai/Kimi-K3) | **2.8T** | 104B | MXFP4 权重 / MXFP8 激活（QAT） | `kimi-k3` | **2.40×** |
| [deepseek-ai/DeepSeek-V4-Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro) | **1.6T** | 49B | FP4（MoE 专家）+ FP8（其余） | MIT | **1.37×** |

且这两个不是「理论上要量化才装不下」——它们**已经是原生 4-bit 级形态**，所以没有进一步压缩的余量：Kimi K3 按 $2800 \times 0.55 \approx 1540$ GB、DeepSeek-V4-Pro 按 $1600 \times 0.55 \approx 880$ GB（实际更高，因为只有专家层是 FP4、其余是 FP8），两者都不是 640 GB 能装的。Kimi K3 官方卡逐字 "**Total Parameters** 2.8T" / "**Activated Parameters** 104B" / "MXFP4 weights / MXFP8 activations (quantization-aware training)"；DeepSeek-V4-Pro 官方卡逐字 "1.6T" / "49B" / "MoE expert parameters use FP4 precision; most other parameters use FP8"、许可 "License: mit"、上下文 "1M"。

**连带影响两处**：§12.4 的可发表形态句「真实私域部署包络允许 **~120B 到 671B**」与 §0 第 15 行「允许 120B–671B」，都把开放权重的实际上界写低了一个量级以上（671B → 至少 2.8T）。另外 §12.2 表中「DeepSeek 671B 级」这一行本身没错（V3/R1 确为 671B），但用它当「最大开放权重」的刻度已过时：DeepSeek 旗舰自 2026-04 起是 V4-Pro 1.6T。

### 1.2 `gpt-oss-120b` 的「BF16 234 GB」与「8-bit 117 GB」对应不到任何官方制品

[openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) 官方卡逐字："117B parameters with 5.1B active parameters"、"The models were post-trained with **MXFP4 quantization of the MoE weights**"、"All evals were performed with the same MXFP4 quantization"、模型 fits "into a single 80GB GPU (like NVIDIA H100 or AMD MI300X)"；页面 tag 为 `mxfp4` / "8-bit precision"，tensor types "BF16 · U8"。[config.json](https://huggingface.co/openai/gpt-oss-120b/raw/main/config.json) 逐字含 `quantization_config.quant_method = "mxfp4"`，`modules_to_not_convert` 列出 `model.layers.*.self_attn` / `model.layers.*.mlp.router` / `model.embed_tokens` / `lm_head`（即注意力与嵌入保持 BF16、只有专家层是 MXFP4）。[文件树](https://huggingface.co/openai/gpt-oss-120b/tree/main) 的 15 个 Transformers 格式 shard 合计 **约 64.6 GB**。

三条后果：**(a)** OpenAI 从未发布 BF16 检查点，`234 GB` 这格描述的是社区反量化产物，不是官方形态；`117 GB` 8-bit 这格同样无对应制品。**(b)** `64 GB` 这格与真实体积 64.6 GB 只差 0.4%，但它的性质是**唯一可得形态**而非我方施加的量化，§12.2 的行内注「64 GB → 单卡 80G 可容」在数值上等价于官方自述，语义上却把「原生」写成了「量化后」。**(c)** §12.3 部署难度列的「120B · 单卡 80G（**4-bit**）」这个括注同理，暗示需要一步量化，而官方形态本来就在 80 GB 内。

### 1.3 §12.5 把 VerIbmc 的 +2 归给了 `Qwen3.6-27B`

§12.5 逐字：「**不该用 `Qwen3.6-27B`**：**它在 VerIbmc 那一档只有 +2**」。按 §3.8 纪律，我逐字回读了三处原文：`small_model_papers.md` §4.6 的表把 +2 写在 **`Qwen2.5-32B`** 行（342/307 是 Llama-3.1-8B、382/380 才是 Qwen2.5-32B）；SUMMARY §4.2 的同一张表同样如此，且 §4.2 的措辞是「`route_selection_and_v47_plan.md` 推荐的 `Qwen3.6-27B` **正落在这一档**」——那是**类比**（同规模档位），不是实测归属。§12.5 把类比改写成了「它在……只有 +2」，即断言 VerIbmc 在 `Qwen3.6-27B` 上测出过 +2；VerIbmc 没有测过这个模型（它测的是 Qwen2.5 系与 GPT-OSS 系，见 [arXiv:2606.16886](https://arxiv.org/abs/2606.16886) 摘要 "five open-weight models (ranging from 7B to 120B parameters)"）。`Qwen2.5-32B` 与 `Qwen3.6-27B` 是不同世代、不同参数量（32B vs 28B）、不同形态（后者带视觉编码器）的两个模型。

**同病第二处**：§7 建议表第 2 行的依据栏写「VerIbmc（**27B 档** +2）」。VerIbmc 没有 27B 档，只有 32B 档。

**这一处必须与 §4.2 自己标出的限定一起看**：§4.2 逐字「⚠️ **衰减并不单调**（Qwen2.5-32B 是反转点，能力低于 GPT-OSS-20B 而收益远小于它）」，即 §4.2 明说 +2 这个低值可能是 **Qwen 系特有效应**而非规模律；§12.3 把同一批数据的列头写成「规模」并抹掉了模型身份，§12.5 又据此把 +2 落到另一个 Qwen 上。**按 §3.8 区分**：§12.3 与 §4.2 之间**不构成「两处说法相反」**（§12.3 从未声称单调，其四行数字 35/15/2/3 本身就含 2→3 的回升），登记为**限定丢失**；§12.5 与 §4.2 之间则是**实质不一致**，§4.2 的类比措辞在 §12.5 被升格为实测。

### 1.4 8-bit 系数 $b=1$ 偏低约 6%，且 DeepSeek 那一行缺了越界标注

实测锚点：[unsloth/DeepSeek-V3-GGUF](https://huggingface.co/unsloth/DeepSeek-V3-GGUF) 的 `Q8_0` 文件体积 **712 GB**，除以 671B 得 **1.061 B/参**（K-quant 的 scale 与保持高精度的 embed / lm_head 层所致）；DeepSeek 官方自己的原生 FP8 发布含 14B MTP 模块、HF 计数 685B，实际约 685 GB。所以 §12.2 表里「DeepSeek 671B 级 · 8-bit **671 GB**」低估了真实 8-bit 制品约 6%（712 GB），也低估了官方 FP8 形态（~685 GB）。

**连带的标注不一致**：671 GB 与 712 GB 都 **> 640 GB**，即 8 卡节点装不下；但该行没有任何标注，而同表 `Qwen3.5-397B-A17B` 的 BF16 行标了「→ 8 卡节点装不下」、8-bit 行标了「→ 单节点可」。同一张表对越界与不越界的标注口径不一致。

### 1.5 §12.6「4-bit 218 GB，需 3×80G」——3 卡装不下

实测：[mlx-community/Qwen3.5-397B-A17B-4bit](https://huggingface.co/mlx-community/Qwen3.5-397B-A17B-4bit/tree/main) 的 `main` 分支体积为 **224 GB**（46 个 shard，前 45 个可见合计约 221.3 GB，非权重文件不足 10 MB）。与 MLX 4-bit 的理论 4.5 bpw（4 bit + fp16 scale + fp16 bias / group 64）$= 0.5625$ B/参、按 HF 计数 403B 得 226.7 GB 相互印证。

两条算术：**(a)** §12 的 218 GB 比实测 224 GB 低 2.8%（原因是 §12 用 397B 而非 HF 计数 403B、且系数取 0.55 而非 MLX 实际 0.556–0.5625）。**(b)** 3×80 GB 的标称 240 GB，按 vLLM 默认 `--gpu-memory-utilization 0.92`（[engine args 文档](https://docs.vllm.ai/en/latest/configuration/engine_args.html) 逐字 "If unspecified, will use the default value of 0.92"）只有 **220.8 GB** 归 model executor，而权重实测就要 224 GB——**在任何 KV cache 之前就已经超了**。3 卡不成立，需 4 卡（或改用非默认配置 + 更激进的量化）。

## 2. 存疑未决

### 2.1 总参口径成立，但四行全部取了向下取整的营销数，偏差方向一致

§12.2 自述「各模型总参数量按官方模型卡口径」——这条**成立**，四个数都能在官方卡上找到逐字表述。但 HF 由 safetensors 索引自算的参数量全部更高，且**每一行都朝同一个方向偏**：

| 模型 | §12 用 | 官方卡逐字 | HF safetensors 计数 | 真实 BF16 体积 | §12 的 BF16 | 偏差 |
| :-- | --: | :-- | --: | --: | --: | --: |
| `Qwen3.6-27B` | 27B | "Number of Parameters: 27B" | **28B** | ~56 GB（仓库另记 55.58 GB） | 54 GB | **−2.8%** |
| `gpt-oss-120b` | 117B | "117B parameters with 5.1B active" | 117B | 无官方 BF16 | 234 GB | 见 §1.2 |
| `Qwen3.5-397B-A17B` | 397B | "397B in total and 17B activated" | **403B** | ~806 GB | 794 GB | **−1.5%** |
| DeepSeek 671B 级 | 671B | "671B total parameters with 37B activated for each token" | **685B**（含 14B MTP） | ~1370 GB | 1342 GB | **−2.0%** |

单条都在 3% 内、不构成错误，但**方向单一**：四条偏差全部让「装得下」更容易成立。叠加 0.55 系数的乐观边界（§4.1）与漏掉的常驻项（§4.2），三个独立的乐观偏差同向累积——这一点我只作事实登记，不作评价。

### 2.2 §12.6「正好落在最依赖长上下文保真度的区间」缺定量支撑

95,589 字符按 3–4 字符/token 的常用启发式约合 **24K–32K token**，即 gpt-oss-120b 131,072 窗口的 **18%–24%**，是 4K base 的 **6–8 倍**（不是 32 倍）。真实 token 数我**核不动**——需要用该模型 tokenizer 实跑一遍 splitter system prompt，本轮未做。故「正好落在最依赖长上下文保真度的区间」这句的定量依据待补。字符数 95,589 本身在仓库内可追溯且一致（`docs/generations/x1-split-intervention/preregistered.md` 第 250 行台账 `95589`、`v46_weakness_anatomy.md`、`route_selection_and_v47_plan.md` §二-B、`talks/2026-08-12-...` 两处，五处同值）。

### 2.3 「128K 是从 4K base 做 32× YaRN 外推」——config 层面成立，但「外推」是我方读法

**引文核对通过**（见 §3.4）。**技术说法本身也成立**：[config.json](https://huggingface.co/openai/gpt-oss-120b/raw/main/config.json) 逐字 `max_position_embeddings: 131072`、`rope_scaling: {"rope_type": "yarn", "factor": 32.0, "original_max_position_embeddings": 4096, "beta_fast": 32.0, "beta_slow": 1.0}`、另有 `initial_context_length: 4096`；$4096 \times 32 = 131072$ 精确闭合。

三点存疑：**(a)** OpenAI 自己的措辞是 "natively support context lengths of up to 128k"（[Introducing gpt-oss](https://openai.com/index/introducing-gpt-oss/)），官方材料**未**把它描述为推理期外推，也未公开长上下文阶段的训练细节；「外推」隐含的保真度贬义不是官方表述能支撑的。**(b)** 我未能核到官方对「是否在扩展窗口上做过训练」的正面陈述——本轮检索只看到官方仅说用了 RoPE + 128k 原生支持，细节要查模型卡论文 [arXiv:2508.10925](https://arxiv.org/abs/2508.10925)，**本轮未读该 PDF，核不动**。**(c)** 同一构造并非 gpt-oss 独有：检索结果显示 DeepSeek-V2 也是用 YaRN 把 4K 扩到 128K。该排除判据的区分力如何，超出本文件职责。

### 2.4 GLM-4.7 的 0.830 / GPT-5.4 的 0.825 在仓库内引用链未闭合

引文核对通过（见 §3.4）。但上游 [route_selection_and_v47_plan.md](../../discover_matrix/docs/findings/route_selection_and_v47_plan.md) §1.2 只写「结构化输出取值准确率开权重反超（GLM-4.7 **0.830** > GPT-5.4 0.825）」，**未给 benchmark 名、未给链接**，所以这两个数的一手来源在仓库内是断的，我**核不动**（不知道该去核哪个榜的哪个指标）。附带核到的 GLM-4.7 规模事实：官方 [zai-org/GLM-4.7](https://huggingface.co/zai-org/GLM-4.7) 为 **355B 总参 / 32B 激活**（HF 自算 358B），MIT，repo 约 717 GB，另有官方 FP8 检查点。

### 2.5 §12.5 的「~120B 级」与 §12.6 的候选清单在规模上不匹配

§12.5 上端臂定义为「**~120B 级开放权重**」，§12.6 给的三个待评估替代分别是：`Qwen3.5-397B-A17B`（397B，**3.3×**）· `GLM-4.7`（355B，**3.0×**）· `Kimi-K2`（[官方](https://huggingface.co/moonshotai/Kimi-K2-Instruct) 1T 总参 / 32B 激活、block-fp8 原生、128K 上下文，**8.5×**）。三者都不是「~120B 级」。§12.6 已自标「三者的上下文实现方式与单节点可容性均待核」，但没有提到与 §12.5 规模档位的落差。这是内部数字不匹配，**该改哪一边不由我裁定**。

### 2.6 VerIbmc 逐模型表我只能核到摘要级

[arXiv:2606.16886](https://arxiv.org/abs/2606.16886) 摘要独立印证了三个数：GPT-OSS-120B "solves **431** of **499** problems (86.4%)"（与 §4.6 表的 Basic 431 一致）、符号阶段单独可解 "**75** problems with no LLM call"（与 §4.6 的 Phase-1 75 题一致）、"adds **up to +35** additional problems for the weakest model"（与 +35 一致）。但摘要**没有**列出五个模型名，也没有 "Basic vs LLM-Only" 这个消融名（摘要给的对照是 CoT vs ToT），整张表需正文 PDF 才能逐格核。该项属 C1 已做范围，本轮**未重复**。另外摘要口径是 499 题（520 去掉 21 题不可避免溢出），§4.6 未写分母，若后续要引用命中率需带上 499。

### 2.7 「MoE 全部权重须常驻显存」是保守前提，方向对 §12 有利

§12.2 的公式前提逐字「**MoE 的全部权重须常驻显存，只有计算稀疏，故按总参而非激活参算**」——对 GPU 常驻的高吞吐服务成立，但**不普遍成立**：专家层可以卸载到主机内存（llama.cpp 的 expert offload、ktransformers 等）。同一份 [unsloth/DeepSeek-V3-GGUF](https://huggingface.co/unsloth/DeepSeek-V3-GGUF) 卡逐字说最小的 `Q2_K_XS` "should run ok in **~40GB of CPU / GPU VRAM** with automatic llama.cpp offloading"。即真实包络在这一维上比 §12 算的更宽松（代价是吞吐）。登记为事实，方向与 §12 的结论同向。

## 3. 已核无误

### 3.1 两张表的 24 个算术格全部可复算

**包络表**（$P_{\max} = C / b$）：

| 容量 | BF16 $b=2$ | 复算 | 8-bit $b=1$ | 复算 | 4-bit $b=0.55$ | 复算 |
| --: | --: | --: | --: | --: | --: | --: |
| 24 GB | ~12B | $24/2 = 12.00$ | ~24B | $24/1 = 24$ | ~44B | $24/0.55 = 43.64$ |
| 80 GB | ~40B | $80/2 = 40.00$ | ~80B | $80/1 = 80$ | ~145B | $80/0.55 = 145.45$ |
| 160 GB | ~80B | $160/2 = 80.00$ | ~160B | $160/1 = 160$ | ~291B | $160/0.55 = 290.91$ |
| 640 GB | ~320B | $640/2 = 320.00$ | ~640B | $640/1 = 640$ | ~1164B | $640/0.55 = 1163.64$ |

**实例表**（$\mathrm{VRAM} = P \times b$）：$27 \times 2 = 54$ ✓ · $27 \times 1 = 27$ ✓ · $27 \times 0.55 = 14.85 \to 15$ ✓ · $117 \times 2 = 234$ ✓ · $117 \times 1 = 117$ ✓ · $117 \times 0.55 = 64.35 \to 64$ ✓ 且 $64 < 80$ ✓ · $397 \times 2 = 794$ ✓ 且 $794 > 640$ ✓ · $397 \times 1 = 397 < 640$ ✓ · $397 \times 0.55 = 218.35 \to 218$ ✓ · $671 \times 2 = 1342$ ✓ · $671 \times 1 = 671$ ✓ · $671 \times 0.55 = 369.05 \to 369$ ✓ 且 $369 < 640$ ✓。§12.6 的 $218 / 80 = 2.73 \to 3$ 卡在标称口径下也算对（其失效原因是漏项，见 §1.5）。

$8 \times 80 = 640$ GB 亦正确。§12.2 那处自我更正也正确：$794 > 640$，所以「397B 在一台 8 卡机上 BF16 就能跑」确实是错的。

**结论：算术层零错误。** §1 的全部问题都出在输入值、系数、漏项与时效，不在四则运算。

### 3.2 四个模型的总参数量都能在官方卡上逐字对上

- `Qwen3.6-27B`：[官方卡](https://huggingface.co/Qwen/Qwen3.6-27B) 逐字 "Number of Parameters: **27B**"、"License: apache-2.0"、"Context Length: 262,144 natively and extensible up to 1,010,000 tokens"，架构为 dense（引文标题逐字 "Flagship-Level Coding in a **27B Dense** Model"），另附 Vision Encoder。**「27B dense」核对通过。**
- `gpt-oss-120b`：官方卡逐字 "**117B** parameters with **5.1B** active parameters"。**「117B（MoE 总参）」核对通过**（激活参数量与总参在 §12 中区分正确，未混用）。
- `Qwen3.5-397B-A17B`：[官方卡](https://huggingface.co/Qwen/Qwen3.5-397B-A17B) 逐字 "Number of Parameters: **397B in total and 17B activated**"、tensor type "BF16 · F32"、"Context Length: 262,144 natively"、apache-2.0。**「397B（激活 17B）」核对通过。**
- DeepSeek 671B 级：[deepseek-ai/DeepSeek-V3](https://huggingface.co/deepseek-ai/DeepSeek-V3) 逐字 "**671B** total parameters with **37B** activated for each token"，并逐字 "Since FP8 training is natively adopted in our framework, we only provide **FP8 weights**"。**「671B」核对通过**（附注：与 gpt-oss 同理，其 BF16 也不是官方发布形态，需用官方 `fp8_cast_bf16.py` 自行转换）。

**MoE 总参 vs 激活参未见混用**：§12 表头写「总参」、`Qwen3.5-397B-A17B` 行注明「激活 17B」、公式前提明写「按总参而非激活参算」，三处一致。

### 3.3 §12.3 的四个 Δ 与 `small_model_papers.md` §4.6 逐格一致

| §12.3 | §4.6 对应行 | Basic | LLM-Only | Δ | 一致 |
| :-- | :-- | --: | --: | --: | :-: |
| 8B +35 | Llama-3.1-8B | 342 | 307 | +35 | ✓ |
| 20B +15 | GPT-OSS-20B | 424 | 409 | +15 | ✓ |
| 32B +2 | Qwen2.5-32B | 382 | 380 | +2 | ✓ |
| 120B +3 | GPT-OSS-120B | 431 | 428 | +3 | ✓ |

$342-307=35$ · $424-409=15$ · $382-380=2$ · $431-428=3$，四个减法全对。§4.6 表里的 Qwen2.5-7B +24 一行在 §12.3 未列（$352-328=24$，该行本身算术也对）。

**两处限定在 §12.3 掉了**（登记为限定丢失，不是矛盾）：**(a)** §4.6 逐字「Llama 的 342 取自**三次运行的最好一次**（均值 336.0，σ=5.3），所以 +35 落在采样方差的**乐观端**」——按均值计 Δ 约为 $336.0 - 307 = +29$，而 §12.3 与 §12.5 都把 +35 当下端臂的头条数字。**(b)** §4.2 的「衰减并不单调」限定（详见 §1.3）。

### 3.4 P2 的三条引用全部对得上原文

三条都用 `grep -n` 定位后读了完整段落：

1. **55.58 GB 与出处** ✓：[route_selection_and_v47_plan.md](../../discover_matrix/docs/findings/route_selection_and_v47_plan.md) §1.2 逐字「推荐 `Qwen/Qwen3.6-27B`（dense，单卡 BF16 **55.58 GB**，Apache-2.0）」。数值、单位、精度、章节号全部一致，§12.2 标为 M 级也符合该文件的性质。附带一致性验算：$55.58 / 28 = 1.985$ B/参，与 HF 计数 28B 的 BF16 相符，即 55.58 GB 这个数自身是自洽的。
2. **gpt-oss 排除理由** ✓：同文件 §1.2 逐字「⛔ 排除 `gpt-oss`（128K 是从 4K base 做 32× YaRN 外推）」。§12.6 的引用「128K 是从 **4K base 做 32× YaRN 外推**」与原文逐字相符。技术说法本身的核验见 §2.3（config 层面成立，措辞层面有保留）。
3. **GLM-4.7 0.830 vs GPT-5.4 0.825** ✓：同文件 §1.2 逐字「**结构化输出取值准确率开权重反超**（GLM-4.7 **0.830** > GPT-5.4 0.825）」。§12.6 引作「结构化输出取值准确率反超 GPT-5.4，0.830 vs 0.825」，一致。该数的一手来源问题见 §2.4。

### 3.5 P3 内部一致性：逐条回原文后，无「两处说法相反」

按 §3.8 纪律，我把每一处候选指控的两端原文各自完整读了一遍再裁定：

| 候选指控 | 裁定 | 依据 |
| :-- | :-- | :-- |
| §12.3 讲规模律 vs §4.2 明写「衰减并不单调」 | **不存在**（不是相反陈述） | §12.3 从未写「单调」二字，且其自身四行 35/15/2/3 就含 2→3 回升；差别在 §4.2 标了⚠️限定而 §12.3 没带过去，属限定丢失 |
| §12.5「+2 是 `Qwen3.6-27B` 的」vs §4.2「Qwen2.5-32B 是 +2、`Qwen3.6-27B` 正落在这一档」 | **成立**（实质不一致） | 已登记为 §1.3；§4.2 是类比措辞，§12.5 与 §7 第 2 行升格为实测归属 |
| §5.1「Qwen3.5-397B / DeepSeek / gpt-oss-120b 在可复现性上与 27B 完全等价」vs §12 的两端选型 | **不存在** | 两处方向一致，§5.1 正是 §12.5 排除 27B 的前提之一 |
| §5.2「两端规模与其算术依据已在 §12.5 定下（下端 ~8–20B · 上端 ~120B 级）」vs §12.5 | **不存在**（一致） | 逐字相符；但 §5.2 一并继承了 §2.5 那处「120B 级 vs 候选清单」的规模落差 |
| §0 第 15 行「允许 120B–671B」vs §12.4「~120B 到 671B」 | **不存在**（一致） | 两处同值；但同一个上界都已过时，见 §1.1 |
| §7 第 2 行依据「VerIbmc（27B 档 +2）」vs §4.2 表 | **成立** | 同 §1.3，VerIbmc 无 27B 档 |

## 4. 公式漏项评估

### 4.1 0.55 这个系数：处在乐观边界但可辩护，合理区间 0.55–0.62

四个**实测**锚点（全部取制品自身体积除以总参，不是估算）：

| 量化方案 | 制品 | 体积 | 总参 | B/参 |
| :-- | :-- | --: | --: | --: |
| MXFP4 原生（专家层量化、注意力与嵌入保 BF16） | [openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b/tree/main) 15 shard | 64.6 GB | 117B | **0.552** |
| MLX 4-bit（4 bit + fp16 scale/bias per group 64 = 4.5 bpw） | [mlx-community/Qwen3.5-397B-A17B-4bit](https://huggingface.co/mlx-community/Qwen3.5-397B-A17B-4bit/tree/main) | 224 GB | 403B | **0.556** |
| llama.cpp `Q4_K_M`（文件体积） | [unsloth/DeepSeek-V3-GGUF](https://huggingface.co/unsloth/DeepSeek-V3-GGUF) | 377 GB | 671B | **0.562** |
| 同上，HF 硬件兼容口径（含运行时余量） | 同上 | 404 GB | 671B | **0.602** |

**评估**：0.55 略低于全部四个锚点，是**乐观边界**，但偏差在 0.4%–9% 之间，作为量级估算**可辩护**。**建议区间 0.55–0.62、中心取 0.57**：下界对应「只量化专家层、其余保 BF16」的原生 MXFP4（0.552），上界对应「K-quant + 高精度 embed/lm_head + 运行时余量」（0.602）。依据即上表四条；理论侧亦吻合——纯 MXFP4 是 4 bit + 每 32 值一个 8-bit 共享指数 $= 4.25$ bpw $= 0.531$ B/参，是不可能达到的地板，任何真实制品都要在此之上加 scale/zero-point 与高精度层。

**顺带一条同类问题**：8-bit 取 $b=1$ 同样偏低约 6%（实测 `Q8_0` 为 1.061，原生 FP8 含 BF16 norm/embed 约 1.02），已在 §1.4 登记。BF16 取 $b=2$ 则**精确**——`zai-org/GLM-4.7` 的 repo 717 GB 除以 HF 计数 358B 得 2.003，误差 0.15%（前提是用真实参数量，而 §12 用的是营销数，见 §2.1）。

**换成 0.57 后包络表的变化很小**：24 GB → 42B（原 44B）· 80 GB → 140B（145B）· 160 GB → 281B（291B）· 640 GB → 1123B（1164B）。**所以系数不是主要问题，漏项才是。**

### 4.2 漏项：三类必须常驻的开销，合计吃掉标称容量的 10–15%

公式 $\mathrm{VRAM} \approx P_{\text{total}} \times b$ **只算权重**。真实服务至少还有三类常驻项：

**(1) 框架预留（最大、最确定）。** vLLM 默认 `--gpu-memory-utilization` = **0.92**，[官方 engine args 文档](https://docs.vllm.ai/en/latest/configuration/engine_args.html) 逐字 "The fraction of GPU memory to be used for the **model executor**, which can range from 0 to 1"、"If unspecified, will use the default value of **0.92**"。即默认有 **8% 的标称容量根本不归 model executor**。在 640 GB 上是 **51 GB**，在 24 GB 上是 1.9 GB。这一项与模型无关、无法通过量化规避（只能手工调高，代价是 OOM 风险）。

**(2) KV cache（随上下文与并发线性增长）。** 用 gpt-oss-120b 自己的 config 值精确算一遍：`num_key_value_heads = 8`、`head_dim = 64`、`num_hidden_layers = 36`、`layer_types` 为 sliding(window 128) 与 full 交替、即 **18 个 full 层**。每 token 每 full 层 $2 \times 8 \times 64 \times 2\,\text{B} = 2$ KiB，$\times 18 = 36$ KiB/token；跑满 131,072 窗口时 $36\,\text{KiB} \times 131072 \approx 4.5$ GiB $\approx$ **4.8 GB 每序列**（18 个 sliding 层被 128 token 截断，合计仅 4.5 MiB，可忽略）。按我们自己的负载（splitter system prompt 95,589 字符 ≈ 24–32K token，见 §2.2）约 **0.9–1.2 GB 每序列**；8 路并发 **7–10 GB**。量级随架构变化很大：MLA（DeepSeek）与线性注意力混合（Qwen3.5/3.6 的 Gated DeltaNet 层不存 KV）显著更小，纯 MHA 显著更大。**整体量级：长上下文下 1–10 GB 每序列，乘并发数。**

**(3) 激活、CUDA graph 与通信缓冲。** prefill 工作区受 chunked-prefill 分块大小约束，量级 **0.5–4 GB**；CUDA graph 捕获缓冲与 NCCL 通信缓冲量级 **1–2 GB 每卡**，8 卡节点上即 **8–16 GB**。另有 MoE 专家并行分片不整除导致的最忙 rank 余量与显存碎片，无法给统一数值，但必须留。

**合计效应**：长上下文服务下可用于权重的预算约为标称的 **0.85–0.90**。取 0.88 可用率，并按 §4.1 的实测锚点把每参字节数改成 BF16 $b=2.00$ · 8-bit $b=1.03$ · 4-bit $b=0.57$，重算包络：

| 容量 | §12 的 BF16 | 重算 | §12 的 8-bit | 重算 | §12 的 4-bit | 重算 |
| --: | --: | --: | --: | --: | --: | --: |
| 24 GB | ~12B | **~11B** | ~24B | ~21B | ~44B | **~37B** |
| 80 GB | ~40B | ~35B | ~80B | ~68B | ~145B | ~124B |
| 160 GB | ~80B | ~70B | ~160B | ~137B | ~291B | ~247B |
| 640 GB | ~320B | ~282B | ~640B | ~547B | **~1164B** | **~988B** |

逐格复算：$24 \times 0.88 / 2 = 10.6$ · $24 \times 0.88 / 1.03 = 20.5$ · $24 \times 0.88 / 0.57 = 37.1$ · $80 \times 0.88 / 2 = 35.2$ · $80 \times 0.88 / 1.03 = 68.3$ · $80 \times 0.88 / 0.57 = 123.5$ · $160 \times 0.88 / 2 = 70.4$ · $160 \times 0.88 / 1.03 = 136.7$ · $160 \times 0.88 / 0.57 = 247.0$ · $640 \times 0.88 / 2 = 281.6$ · $640 \times 0.88 / 1.03 = 546.8$ · $640 \times 0.88 / 0.57 = 988.1$。

两处后果值得单列：**(a)** 640 GB / 4-bit 从 1164B 降到 **~988B**，于是连 Kimi-K2（1T）都刚好落在单节点之外——而 Kimi-K2 正是 §12.6 的候选之一。**(b)** 24 GB / BF16 从 12B 降到 **~11B**，且这还没扣 KV cache——扣掉一路 32K 上下文的 KV 后就落到 8–9B，与「消费卡 BF16 实际只跑得动 8B 级」这一常识吻合。

### 4.3 附带一条口径问题：「标准 8×80G 节点」已不是 2026 年的标准

$8 \times 80 = 640$ GB 算术正确，但它描述的是 H100 世代。按 NVIDIA 官方数据表，**DGX H200 的整机 GPU 显存是 1,128 GB**（$8 \times 141$），**HGX/DGX B200 是 1,440 GB**（$8 \times 180$）。按 §4.2 的重算口径（0.88 可用、$b=0.57$），B200 节点的 4-bit 权重上限约 **2,220B**——那能装下 DeepSeek-V4-Pro（1.6T），但仍装不下 Kimi K3（2.8T，原生形态约 1.5 TB）。这一项与 §1.1 相互作用：换更新的节点能把上限抬高，但抬不到「当前最大的开放权重模型全部在内」。

## 5. 核验方法与来源

### 5.1 本地核验命令（可复现）

```bash
cd /home/zhangshaoang/oo-projects/research_ideas/project_1_llm_state_machine_modeling/paper_stm_issue_discover
sed -n '244,332p' related_work/deployment/SUMMARY.md          # §12 全文
sed -n '94,175p'  related_work/deployment/SUMMARY.md          # §4.1–§7（P3 对照）
sed -n '1,40p'    discover_matrix/docs/findings/route_selection_and_v47_plan.md   # §1.2（P2.1/2.2/2.3）
sed -n '335,360p' related_work/deployment/small_model_papers.md                   # §4.6（P2.4）
grep -rn "95,589\|95589" --include=*.md .                     # 95,589 的五处一致性
grep -n "80G\|包络\|单节点\|397\|671\|120B\|27B\|1164\|gpt-oss" related_work/deployment/SUMMARY.md
```

### 5.2 官方来源（模型卡与 config）

| 事实 | 入口 | 核验结果 |
| :-- | :-- | :-- |
| `Qwen3.6-27B` 27B dense / apache-2.0 / 262K | [Qwen/Qwen3.6-27B](https://huggingface.co/Qwen/Qwen3.6-27B) | ✓，HF 计数 28B |
| `gpt-oss-120b` 117B / 5.1B active / MXFP4 原生 / 单卡 80G | [openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) | ✓，**原生量化**，无官方 BF16 |
| `gpt-oss-120b` 检查点体积 64.6 GB（15 shard） | [文件树](https://huggingface.co/openai/gpt-oss-120b/tree/main) | ✓（repo 全量 196 GB，含 `metal/`、`original/`） |
| `gpt-oss-120b` YaRN 4096×32=131072、`quant_method: mxfp4` | [config.json](https://huggingface.co/openai/gpt-oss-120b/raw/main/config.json) | ✓ 逐字 |
| `gpt-oss-120b` KV 结构（8 KV 头 / 64 dim / 36 层 / sliding 128 交替） | 同上 config.json | ✓ 逐字，用于 §4.2 计算 |
| `Qwen3.5-397B-A17B` 397B/17B / BF16 / 262K / apache-2.0 | [Qwen/Qwen3.5-397B-A17B](https://huggingface.co/Qwen/Qwen3.5-397B-A17B) | ✓，HF 计数 403B |
| DeepSeek-V3 671B/37B、仅提供 FP8 权重、HF 计数 685B | [deepseek-ai/DeepSeek-V3](https://huggingface.co/deepseek-ai/DeepSeek-V3) | ✓ 逐字 |
| **Kimi K3 2.8T / 104B / MXFP4 原生** | [moonshotai/Kimi-K3](https://huggingface.co/moonshotai/Kimi-K3) | ✓ 逐字（推翻 §12.2 末句） |
| **DeepSeek-V4-Pro 1.6T / 49B / FP4+FP8 / MIT / 1M** | [deepseek-ai/DeepSeek-V4-Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro) | ✓ 逐字（推翻 §12.2 末句） |
| Kimi-K2 1T / 32B / block-fp8 / 128K | [moonshotai/Kimi-K2-Instruct](https://huggingface.co/moonshotai/Kimi-K2-Instruct) | ✓ |
| GLM-4.7 355B/32B（HF 358B）/ MIT / repo 717 GB | [zai-org/GLM-4.7](https://huggingface.co/zai-org/GLM-4.7) | ✓ |
| MLX 4-bit 体积 224 GB（46 shard） | [mlx-community 文件树](https://huggingface.co/mlx-community/Qwen3.5-397B-A17B-4bit/tree/main) | ✓（社区量化，体积属该制品一手事实） |
| `Q4_K_M` 377 GB / `Q8_0` 712 GB / offload 40 GB | [unsloth/DeepSeek-V3-GGUF](https://huggingface.co/unsloth/DeepSeek-V3-GGUF) | ✓（社区量化） |
| vLLM `gpu_memory_utilization` 默认 0.92 | [vLLM engine args](https://docs.vllm.ai/en/latest/configuration/engine_args.html) | ✓ 逐字 |
| VerIbmc 431/499、75 题、+35 | [arXiv:2606.16886](https://arxiv.org/abs/2606.16886) | ✓ 摘要级；逐模型表需正文 |
| DGX H200 1,128 GB · HGX B200 1,440 GB | [NVIDIA H200](https://www.nvidia.com/en-us/data-center/h200/) · [DGX H200 数据表](https://resources.nvidia.com/en-us-dgx-systems/dgx-h200-datasheet) | ✓ |

### 5.3 明确核不动的三项

1. **splitter system prompt 的真实 token 数**：需用 gpt-oss tokenizer 实跑 95,589 字符，本轮未做；§2.2 的 24–32K 是按 3–4 字符/token 启发式估算，**不是实测**。
2. **gpt-oss 是否在扩展窗口上做过训练**：官方博客与模型卡只说 "natively support context lengths of up to 128k"，未公开长上下文训练阶段；细节要读 [arXiv:2508.10925](https://arxiv.org/abs/2508.10925) 全文，**本轮未读该 PDF**。
3. **GLM-4.7 0.830 / GPT-5.4 0.825 的一手来源**：上游文件未给 benchmark 名与链接，无法定位该去核哪个榜的哪个指标（见 §2.4）。

另有两项**部分核不动**：Kimi K3 与 DeepSeek-V4-Pro 的官方卡都**未显示 repo 总体积**，故 §1.1 里那两个「原生形态约 1.5 TB / 880 GB」是按参数量与声明精度推算的，**不是读到的文件体积**；VerIbmc 逐模型表只核到摘要（见 §2.6）。
