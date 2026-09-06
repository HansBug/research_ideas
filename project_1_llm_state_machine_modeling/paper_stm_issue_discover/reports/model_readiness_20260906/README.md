# E1 模型调研与推理接入证据

核验日期：2026-09-06。本文档组记录 Paper1 多模型实验的选型依据、官方资料、远程 H200 部署和有限兼容性 smoke。它不包含正式命中率、precision 或方法优越性结论；完整 baseline/ours 实验需要独立冻结协议与运行身份。研究范围来源为 [E1 合同](https://github.com/HansBug/research_ideas/pull/204)；施工状态以 GitHub 为准。

## 结论

商用讨论候选保留 `gpt-5.6-luna`，Gateway B 新增可访问的 `gemini-3.7-flash` 与 `gemini-3.8-flash` 原生 profile。两款 Gemini 已通过 `google-genai` adapter 的真实 pair `0001` method smoke；每款 1/1 method cell eligible、5/5 stage success、无 method/audit error，但只覆盖一个诊断 pair，不能据发现条数排名。严格 `responseJsonSchema` 与复杂 forced-tool canary 仍受网关限制，不能写成全面 schema 健康。`gemini-3.5-flash` 的旧渠道仍保留失败回执；Sonnet 5 与 Haiku 4.5 维持低优先级备选。完整结果见[商用报告](./2026-09-06-11-53-00-commercial-models.md)与[部署报告](./2026-09-06-11-53-00-serving-evidence.md)。

开放模型调查覆盖五款近期总参数 <100B 主候选及三款生态对照。实际部署的 Qwen3.8、Qwen3.6、Gemma4、Muse 均达到各自官方目标窗口约 0.9，包含 Qwen 的 1M/1.01M YaRN 扩展；四款在约 16K thinking 输入、16 worker 下均为 32/32。最小 method 路径中 Qwen3.8、Qwen3.6、Muse 完成，Gemma4 带 contract-completion 预算耗尽诊断落盘。Qwen3.8 是优先讨论对象，另一款在 Gemma4 和 Muse 之间权衡；证据见[开放模型报告](./2026-09-06-11-53-00-open-models.md)与[部署报告](./2026-09-06-11-53-00-serving-evidence.md)。这不是已冻结的 E2 名单。

## 证据入口

- [protocol.md](./protocol.md)：事前协议、context 0.9 边界、隐私和验收条件。
- [商用模型](./2026-09-06-11-53-00-commercial-models.md)：发布时间、价格、context/output、公开 benchmark 和可用性。
- [开放模型](./2026-09-06-11-53-00-open-models.md)：100B 以下候选、官方启动方式、许可证、benchmark 和选型。
- [近期 LLM4SE](./2026-09-06-11-53-00-llm4se-recent.md)：2026-03-06 至 2026-09-06 的 arXiv 样本和模型使用统计。
- [部署与负载](./2026-09-06-11-53-00-serving-evidence.md)：tunnel、并发、长上下文和 thinking 结果、失败记录与交接缺口。
- [evidence/manifest.json](./evidence/manifest.json)：脱敏归档的逐 member SHA-256 与 redaction 策略。
- [verify_evidence.py](./verify_evidence.py)：离线验证哈希，并从原始逐请求记录复算全部负载结果；不会调用 provider。
- [../../../talks/2026-09-05-导师-paper1多模型对照与谓词降幻觉.md](../../../talks/2026-09-05-导师-paper1多模型对照与谓词降幻觉.md)：导师讨论正式纪要。

## 选型原则

每个 backbone 在 E2 中应配对比较 `LLMx + FCSTM + 谓词` 与 `LLMx`。论文主张是方法提高不同模型在规定任务上的效果，不是击败最新模型。价格只用于工程可行性记录，不作为论文贡献。A1/A2 继续使用 Luna 单模型；E1 不启动 E2，也不启动伞 PR O2。

Muse 的推荐接入限定为已验证的 function/tool 路径；旧 JSON response-format 虽 schema 合法却有占位符，已单列内容失败。Gemma 的 method 预算耗尽、旧 Gemini 3.5 路由缺口、Claude timeout 类型和部分 workflow usage 缺失均保留。Gemini 3.7/3.8 的真实 method 成功只证明当前 native ToolStrategy 路径可运行，不能覆盖网关原生 JSON Schema 和所有强制工具场景。

## 证据等级

容量、API 和 workflow 分开判断：容量通过只表示对应负载成功；`completed_with_diagnostics` 不是无缺口完成；`failed_with_receipt` 不是成功；`untested` 不能写成已部署。所有 smoke 的 `formal_result_eligible=false`。原始 usage、stage receipts 和失败保留，公开包对 secret、端点、节点、用户名和私人路径脱敏；内嵌原始 run hash 不会因脱敏而伪造重签。`protocol.md` 是事前协议与后续用户约束记录，四份秒级命名报告是冻结的人类分析入口。
