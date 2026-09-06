# 优先开放模型：独立环境最终验收

核验日期：2026-09-06。本文只记录 Qwen3.8-27B 与 Muse Glimmer 30B 从历史共享 serving 环境迁移到各自独立 conda 环境后的接入验收；不构成 E2 效果结果，也不改变 method、prompt、validator、eligibility 或 judge 口径。

## 环境与服务

两款模型分别使用独立环境和明确的环境解释器启动，均使用 SGLang 0.5.19、PyTorch 2.13.0、Transformers 5.12.1、FlashInfer 0.6.18；CUDA runtime、NVRTC、CUPTI 与 NVCC 已在各自环境内统一到 13.3 系列。conda base、系统 Python、系统 CUDA 和其他 GPU 未修改。

| 模型 | 服务身份 | TP / context | parser | 最终环境验收 |
|---|---|---:|---|---|
| Qwen3.8-27B | `qwen3.8-27b` | TP4 / 1,000,000 | `qwen3` + `qwen3_coder` | `/v1/models` 身份正确 |
| Muse Glimmer 30B | `muse-glimmer-30b` | TP4 / 131,072 | `muse` + `muse` | `/v1/models` 身份正确 |

服务只使用 GPU 0–3，GPU 4–7 未使用；验收结束后两款服务均已停止，GPU 0–7 均恢复为 0 MiB。

## 接入验收

根 `.llmconfig.yml` 的两个 profile 均可加载，`python -m utils.llm validate` 通过（主 registry 23 profiles）。两个 profile 的模型身份、context、max output 和 stream usage 配置如下：

| profile | model | context | max output | pricing |
|---|---|---:|---:|---|
| `e1-qwen38-27b` | `qwen3.8-27b` | 1,000,000 | 65,536 | 未配置，cost 不具资格 |
| `e1-muse30b` | `muse-glimmer-30b` | 131,072 | 32,768 | 未配置，cost 不具资格 |

两款均通过普通生成、function/tool 调用、流式 usage 和实际推理控制。Qwen 的低推理档通过 `reasoning_tokens` 回执核验；Muse 使用官方 high reasoning system instruction、`temperature=1.0`、`top_p=0.95`、`top_k=64`，并通过 reasoning usage 核验。Muse 仍只推荐已验证的 function/tool 路径，历史 JSON response-format 占位符缺陷保持记录。

## method 与并发

- Qwen method run `e2cd347fb8f84886b1c496675724046b`：pair `0001`、1 round，`1/1 method eligible`，0 errors，0 audit errors；5 个 method stage 均 success。为避开该模型长 structured 请求超过现有 30 秒 streaming 首字节边界，本次 method 使用 `--no-stream`；stream usage 已单独通过，首次 streaming timeout 也保留为诊断证据。
- Muse method run `2d2926079fef4ea5a7758d28ccbc8ab3`：pair `0001`、1 round，`1/1 method eligible`，0 errors，0 audit errors；contract、grounding、execution 和终态均正常，未运行 candidate judge。
- 新环境迁移后的 16-worker 短负载：Qwen `32/32`，输入仅 47–48 tokens 的普通生成，总用时约 7.26 s；Muse `32/32`，输入约 395 tokens 的简易 function/tool，总用时约 5.22 s。Qwen 这组不是工具请求；两组均不能替代约 16K thinking/tool 长输入并发。2026-09-07 逐请求复核修正了此前将两者都写成工具负载的错误。
- 两款历史 0.9 官方窗口与约 16K/16-worker 证据保留：Qwen 原生/YaRN 扩展和 Muse 原生窗口均已达到既定约 0.9 边界。独立环境迁移保留相同权重、TP、context 与 parser，但上述短请求不能证明迁移后的长输入承载情况；新旧环境证据需分开解释。

本轮没有运行 judge；A1/A2 与所有 judge 继续固定 Luna。这里证明的是两款独立环境的接入、短负载与 pair `0001`；大输入 pair `0029 / 0019 / 0049` 和迁移后长输入承载需单独给出证据，不能由本报告推导为已完成。商业模型配对和 E2 协议冻结仍按 E1 既定流程执行，E2/O2 本轮未启动。
