# A3 Qwen / Muse：method-only 冻结归档

2026-09-10 按用户授权依次执行 Qwen、Muse，各相同 54 pair × 3 round。**本归档没有运行 judge，不包含 K/N/I、precision 或 hit 结果。** Sonnet/Luna 的既有 [完整归档](../a3_20260910/README.md) 保持不变。

| 模型 | 完成格 | 生成报告 | 最终发布 | true 拦截 | W0 coverage gap | 异常恢复 |
|---|---:|---:|---:|---:|---:|---:|
| Qwen3.8-27B | 162/162 | 379 | 358 | 4 | 17 | 1 |
| Muse Glimmer-30B | 162/162 | 509 | 495 | 2 | 12 | 0 |

每轮均为 54 格。Qwen 三轮发布数为 112/126/120，Muse 为 171/165/159。发布集合合计 853 条，均未作外部裁定；完成 method 不等于完成整个 A3 实验。具体来源、逐条生成到发布映射、轮次、usage 和资格见 [method-results.json](./method-results.json)。

生成和执行保持冻结 `direct-report`：NL + 作者 STM + inspection → 一次报告生成 → 注册谓词真实执行 → 确定性发布。prompt/schema hash 为 `8819378f31fd7f291e73324d1087e33e6a392103756bcab92093bfe50d889b9d`。两模型正常生成逻辑阶段各 162 次；计入节点内结构纠正后，实际 provider 调用分别为 181、164 次，结构校验失败事件分别为 20、2 次。全部 usage 都有输入/输出 token 计数，终态为 tool_calls，无输入截断；reasoning 明细未提供，汇总中的已观测和 0 不能解释为没有推理 token。开放模型费用未定价，不能把 runtime 的默认费用 0 当作免费。

Qwen `0002/r2` 原节点六轮结构纠正耗尽。首次回复已包含四条报告的全部字段，但每条拆为相邻两个互补字段块；事后恢复仅按精确字段分区合回，字段值和顺序不变，经原 schema 校验后重放真实执行与发布，新增 provider 调用为 0。原失败格和六轮审计全部保留，正式映射选用独立 `qwen/schema-recovered` 派生格。其余 Qwen 161 格和 Muse 全部 162 格正常完成；不按报告质量重采样。恢复规则及限制见 [协议](../../discover_matrix/docs/generations/a3_20260910/preregistered.md) 与 [恢复实现](../../discover_matrix/docs/generations/a3_20260910/recover_tool_envelope.py)。

模型服务位于远端 GPU 4–7，依次复用 Qwen、切换 Muse，均使用已有固定权重和独立 conda；客户端复用原生 method CLI。Qwen low、1M YaRN，Muse 模板默认 high、131072，两者均 stream、remaining_context、TP4，method 并发始终不超过 16。权重 revision、启动参数和环境见 [E1 复现附录](../../reports/model_readiness_20260906/2026-09-07-11-55-00-reproduction.md)。专用配置的公开字段见 [profiles.json](./profiles.json)；完整远端服务快照、环境、启动命令和各批 manifest 随原始记录保存。生成代码分别为 `327d43651`（Qwen）和 `93b094c03`（Muse），两提交间仅增加恢复工具、测试和异常记录，冻结方法 prompt/schema 未改。

## 原始证据与复算

- [full_source_manifest.json](./full_source_manifest.json)：324 个只读 Full 来源及哈希、冻结输入；运行前后全部核验一致。
- [raw_index.json](./raw_index.json)：1,933 个原始文件、350,598,676 字节，逐文件 SHA-256；仅排除锁文件。
- [redaction-report.json](./redaction-report.json)：已配置敏感值精确匹配扫描 0 命中。
- 原始记录独立存于 `/home/zhangshaoang/oo-projects/research_ideas-2/runs/paper1/a3_open_method_20260910`，不入 Git。fresh clone 可审阅公共计数和索引，完整复算须另取得该原始目录；索引不是原始内容的替代。

在仓库根运行以下纯标准库命令，不加载凭据、不访问 provider、不运行 judge：

```bash
P=project_1_llm_state_machine_modeling/paper_stm_issue_discover
python "$P/discover_matrix/docs/generations/a3_20260910/verify_open_method.py" \
  --root /home/zhangshaoang/oo-projects/research_ideas-2/runs/paper1/a3_open_method_20260910 \
  --archive "$P/final_results/a3_open_method_20260910"
```

该命令要求两个模型各 162 格、不重复不缺格、输入相同、单次生成身份、无新增候选或内部 D、执行到发布映射闭合、原始主张字段保留，并对拍公共结果及全部原始文件哈希。缺格、失败未恢复或文件损坏均失败，不将部分结果当作完整结果。
