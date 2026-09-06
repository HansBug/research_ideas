# E1 模型调研与推理接入证据

核验日期：2026-09-06 至 2026-09-07。本文档组记录 Paper1 多模型实验的选型依据、官方资料、远程 H200 部署和有限兼容性 smoke。它不包含正式命中率、precision 或方法优越性结论；完整 baseline/ours 实验需要独立冻结协议与运行身份。研究范围来源为 [E1 合同](https://github.com/HansBug/research_ideas/pull/204)；施工状态以 GitHub 为准。

## 结论

用户优先组合为 **Luna + Sonnet 5 + Qwen3.8-27B + Muse Glimmer-30B**。Sonnet、Qwen 和修复后的 Muse 各有最终 profile 的 stream baseline 与 0019/0029/0049 method 证据；Sonnet 0029 保留正常证据降级，Muse 原结构耗尽已在 serving adapter 修复，最终三格 errors/audit errors 全 0。Luna 在此前六次 503 后，06:39 的最终 baseline 成功，但随后普通生成、原生同请求和共用 structured runtime 的四个请求仍返回 503，详见[Luna 路由复核](./2026-09-07-06-55-00-luna-route-recheck.md)。精确四款配置、逐格解释、失败和复现见[四模型交接证据](./2026-09-07-06-12-00-four-model-handoff.md)，不据单次成功声称渠道全面恢复。

两开放模型各自独立 conda、GPU 4-7，使用最大允许输出的剩余窗口模式，迁移后约 0.9 窗口和 16K/16-worker 均有证据；Muse 最新 serving 修复后再次通过 32/32 并发请求和 118375-token 输入 2/2。原生与扩展容量、高并发和完整 method 分开验收，不宣称 16 个最大窗口同时驻留。09-06 的五款近期 <100B 主候选、三款生态对照及旧环境实测仍见[开放模型报告](./2026-09-06-11-53-00-open-models.md)与[部署报告](./2026-09-06-11-53-00-serving-evidence.md)，其余候选后置。E2 正式协议与各模型实验档位仍需独立冻结。

## 证据入口

- [Luna 路由复核](./2026-09-07-06-55-00-luna-route-recheck.md)：最终 baseline 单次成功及后续四个 503，07:07 同配置追加复查仍 503；新旧包独立，[离线核验](./verify_luna_route_evidence.py)检查同 payload、wire 上限、provider 错误与终态。
- [四模型配置与交接证据](./2026-09-07-06-12-00-four-model-handoff.md)：最终 Muse 原生参数/字段顺序修复、九格逐阶段核对、四款 baseline 覆盖、Luna 渠道失败、Sonnet usage 更正、环境锁与启动/tunnel 步骤。
- [handoff manifest](./evidence/handoff_20260907/manifest.json) 与 [verify_handoff_evidence.py](./verify_handoff_evidence.py)：补充归档及离线复算；旧 stream 包保持冻结。
- [全候选公开 benchmark 与任务选型](./2026-09-07-04-30-00-candidate-benchmarks.md)：17 个已调查模型身份、20 个公开档位，AA v4.2 / LCR v1.1 与作者自报分表、结构化缺测、当前 low/default 与公开 max/xhigh 的差异。
- [protocol.md](./protocol.md)：事前协议、context 0.9 边界、隐私和验收条件。
- [09-07 最大输出与 stream 大格验收](./2026-09-07-03-36-18-stream-model-max-acceptance.md)：15 格、独立环境迁移负载、三层同请求、预算修复与商业替代建议。
- [evidence/stream_20260907/manifest.json](./evidence/stream_20260907/manifest.json) 与 [verify_stream_evidence.py](./verify_stream_evidence.py)：新旧 stream/诊断制品的脱敏归档、逐调用 wire、阶段回执及离线核验。
- [商用模型](./2026-09-06-11-53-00-commercial-models.md)：发布时间、价格、context/output、公开 benchmark 和可用性。
- [开放模型](./2026-09-06-11-53-00-open-models.md)：100B 以下候选、官方启动方式、许可证、benchmark 和选型。
- [近期 LLM4SE](./2026-09-06-11-53-00-llm4se-recent.md)：2026-03-06 至 2026-09-06 的 arXiv 样本和模型使用统计。
- [部署与负载](./2026-09-06-11-53-00-serving-evidence.md)：tunnel、并发、长上下文和 thinking 结果、失败记录与交接缺口。
- [evidence/manifest.json](./evidence/manifest.json)：脱敏归档的逐 member SHA-256 与 redaction 策略。
- [verify_evidence.py](./verify_evidence.py)：离线验证哈希，并从原始逐请求记录复算全部负载结果；不会调用 provider。
- [../../../talks/2026-09-05-导师-paper1多模型对照与谓词降幻觉.md](../../../talks/2026-09-05-导师-paper1多模型对照与谓词降幻觉.md)：导师讨论正式纪要。

## 选型原则

每个 backbone 在 E2 中应配对比较 `LLMx + FCSTM + 谓词` 与 `LLMx`。论文主张是方法提高不同模型在规定任务上的效果，不是击败最新模型。价格只用于工程可行性记录，不作为论文贡献。A1/A2 继续使用 Luna 单模型；E1 不启动 E2，也不启动伞 PR O2。

Muse 的推荐接入限定为 function/tool 路径；最终 required-tool serving 修复不覆盖旧 JSON response-format 占位符、D 结构错误和同请求远端反例。Claude timeout/客户端生命周期修复已有 stream 证据。Gemini 3.7/3.8 的 native ToolStrategy 成功不覆盖严格 JSON Schema/canary，09-07 Gemini 3.8 的 11 次网关 504 仍是可靠性限制，保留为备选资料；Haiku 也保留其 D 结构耗尽，不阻塞 Sonnet 方案。

## 证据等级

容量、API 和 workflow 分开判断：容量通过只表示对应负载成功；`completed_with_diagnostics` 不是无缺口完成；`failed_with_receipt` 不是成功；`untested` 不能写成已部署。所有 smoke 的 `formal_result_eligible=false`。原始 usage、stage receipts 和失败保留，公开包对 secret、端点、节点、用户名和私人路径脱敏；内嵌原始 run hash 不会因脱敏而伪造重签。`protocol.md` 是事前协议与后续用户约束记录，秒级命名报告分别保留对应配置的分析快照。
