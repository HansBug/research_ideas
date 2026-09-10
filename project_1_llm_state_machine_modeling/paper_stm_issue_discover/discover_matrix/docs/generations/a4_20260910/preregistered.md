# A4：冻结 Full 的最终报告判定重放

本协议按 2026-09-10 用户合同及[伞 PR #179 §4.7](https://github.com/HansBug/research_ideas/pull/179)登记。问题是：在 Full 已生成的候选条件下，隐藏谓词运行结果会怎样改变末端报告选择？本实验不估计端到端移除谓词机制的效果。最终报告判定对应代码中的内部 `d_adjudication`；它不是外部 Luna judge。

## 固定输入与唯一干预

每模型固定 54 pair × 3 round。Sonnet/Qwen/Muse 读取 E2 `cells.json` 的 ours 来源及 hash；Luna 读取 `luna_history.json` 对应 canonical v61 method，0045/r1 使用 `v61_current_fill0045`。judge 来源由同一 manifest 决定，其 `adapter_audit.source_hash` 必须匹配 method 原件。历史报告、裁定、提示词和输入不覆盖。

NL、STM、检查事实、契约、候选及顺序、来源、路由、绑定和计划全部冻结。输入加载只读取 hash 匹配的十二类制品；解析 FCSTM 恢复 ModelIR，但不重新计算 inspection/verify/SMT facts。旧文件路径可以重定位，内容 hash 必须完全一致。Luna 旧 G4/R4/V4 通过既有编号映射核对类型，实际序列化仍保留原编号；历史 S6 未完成布尔结果的记录只读恢复，不恢复其 backend，不改变已确认的十二种布尔谓词口径。

唯一实验干预是将所有候选的 method-visible execution receipt 替换为同一中性 unknown：清除旧终态、trace、counterexample、run metadata 和结果理由，保留候选、绑定、计划等独立于运行结果的输入。原 true 候选进入最终报告判定，不能直接判为缺陷；原 true→D0 的硬覆盖只能读到 unknown。独立语义拒绝和证据/发布纪律照常工作。原执行结果只在 evaluator 的独立来源记录中使用，不传入 method 或 residual judge。

只重新调用最终报告判定 LLM 及原有必要局部纠错，随后使用与 Full 共用的确定性校验、发布、去重、因果折叠和 guard 聚合。内部 D 的旧成功、旧拒绝和旧纠错均不复用。不调用契约提取、候选生成、候选准备或 backend；入口 guards 拒绝上游调用与后端尝试。完整候选数必须与 D 的 expected obligation ID 集合一致。

## 内容复用与核销

在同一模型、pair、round、冻结输入内，内容投影包含原 obligation/contract 身份、locus、源定位/引用、requirement quote、property/violation direction、expected/observed 以及实际发布的全部 facet/subclaim。集合排序和无意义空白归一；reason/basis、run ID、usage、W 与执行视图变化不改变内容身份，差异另存审计。新增、删除或合并的实质 facet、expected/observed 或方向变化不能复用。发布文字由冻结候选和既有确定性折叠产生；内部 D 只选择 disposition，不生成新的候选主张。

每个唯一最终报告按以下顺序核销一次：

1. 实际发布了原 true 候选的同一缺陷主张，直接记 `oracle_true_I`，优先于旧 Full 标签。一个混合折叠报告即使含多个 true facet 也只记一次 I；仅附带审计探针不算发布。候选 ID 相同但主张反向或无关不能套用。
2. 否则，确定性内容与 Full 等价时，复用原 validity/D/relations，显式重映射报告 ID。
3. 只有剩余无法匹配的报告进入原固定 Luna judge；不修改 prompt/schema/参数/裁定规则。残余可为零，但不强制为零。

原 false 不自动有效，原 unknown 不自动 I。消失的 Full 报告不进入 A4 分母，零报告格仍保留完成回执。oracle 与自动 judge 都不记为新增人工审阅。

## 运行身份与恢复

初始执行登记为先 Sonnet 162 格、再 Luna 162 格，Qwen/Muse 留后续；当时 method 最大 16 workers，residual judge 最大 8。2026-09-10 用户在开放模型调用前追加授权：本轮执行扩展至四模型各 162 格，共 648 格，judge 全局上限调整为 24 workers。该上限包含同渠道其他实验的 judge，不能为每个模型分别开 24。已有 8-worker 批次不为提速重启。method 仍最大 16 workers。

开放模型使用远端 GPU 4-7、各自独立 conda、固定权重和原已验参数；可先复用已驻留 Muse，再切换 Qwen。外部 judge 按 Sonnet、Luna、Qwen、Muse 分组推进，复用原同 pair/round 的 batch、双读、仲裁与失败恢复，不把残余报告强制拆成逐条请求。所有正式调用 stream，使用各 source backbone 对应 profile；沿用已核验模型输出上限，不设置小额 run override。Sonnet 按已有配置启用代理。范围扩展不改变屏蔽、内容等价、oracle 或指标定义，也不以 precision 必须下降作为验收条件。

运行 manifest 绑定来源清单、实现文件 hash、模型配置 hash、treatment 和 masked-input hash。每个 stage cache 另绑定 system/prompt/schema/参数，只有同命名空间已成功真实输出可以恢复；不读取 Full/A2 cache。失败尝试另存，恢复不重复成功末端调用。预选 smoke 为排序后 0000/r1，配置不变时归入对应 162 格。

脚本位于 `evaluation/src/paper_stm_evaluation/a4_{sources,replay,accounting,run}.py`。从仓库根运行，`P` 指论文目录；`INPUT` 指原冻结 representation 报告根，`OUT` 必须是独立本地 runs 路径：

```bash
export PYTHONPATH="$P/method/src:$P/evaluation/src:."
python -m paper_stm_evaluation.a4_sources --paper-root "$P"
python -m paper_stm_evaluation.a4_run freeze --paper-root "$P" \
  --output "$OUT" --model sonnet --profile claude-sonnet-5
python -m paper_stm_evaluation.a4_run run --paper-root "$P" \
  --output "$OUT" --input-root "$INPUT" --model sonnet \
  --profile claude-sonnet-5 --workers 16 --allow-live
python -m paper_stm_evaluation.a4_run verify --paper-root "$P" --output "$OUT"
```

`verify` 不调用 provider；它重新核验来源并从最终报告重建三路核销。完整退出还需全部残余裁定与结果分析，不以脚本退出码代替逐格检查。provider/schema 失败必须处理；语义 unresolved 和原校验机制的正常降级保留，不通过改语义规则制造发布。

四模型 CLI 使用同一入口：Luna 为 `--model luna --profile gpt-5.6-luna`，Qwen 为 `--model qwen --profile e1-qwen38-27b`，Muse 为 `--model muse --profile e1-muse30b`。各模型使用独立 `OUT`。开放模型的独立 conda、固定权重 revision、YaRN/Muse 启动参数和 tunnel 见 [E1 复现附录](../../../../reports/model_readiness_20260906/2026-09-07-11-55-00-reproduction.md)。共用服务端口时，先核验 `/v1/models` 与目标 profile 一致，不能同时向两个模型 profile 发请求。

2026-09-10 四模型实测共同执行文件 hash 为 `sha256:102adc2981f0a74cf8ee0359911f64062698759300fea1b9f6d57849d0ffe85f`。开放模型在既有商业模型任务运行期间通过同一 `freeze/execute_cell/verify` 函数的本地启动器运行，避免修改在途代码指纹；全部 648 格结束后，正式 CLI 仅扩展模型枚举，不变更重放逻辑。原运行 manifest 保留实测 commit 和文件 hash；新 clone 的新运行使用新 namespace，不把不同代码版本混作同一次恢复。

## 分析口径

主比较使用 Full 与 A4 双方全部三轮，而非挑选单轮。K、N、I 是最终唯一报告数：pooled precision = (K+N)/(K+N+I)；I/完成格衡量每格无效报告负担；K+N 衡量有效产出量。逐轮各 54 格单列同样指标，逐轮 precision 的均值与 pooled precision 区分。hit/expected coverage 从最终有效报告关系重新计算。

追踪原 true/false/unknown→D→拒绝/独立/折叠，区分 probe/nonprobe、贡献 true 候选数与唯一 oracle-I 报告数；展示 preserved/lost/new K/N/I、标签迁移、三路核销数、实际调用/缓存复用与耗时。precision 的变化须分解为新增 I、旧 I 消失和有效报告增减；不能把减少报告分母称作消除误报。需要区间时按 pair 将三轮成组，不把报告当独立样本。

Full 参考 K/N/I 为 Sonnet 536/183/104、Luna 561/198/144、Qwen 599/256/103、Muse 544/229/137。此前同率外推只是条件算术：Sonnet 约 +133 I/75.21%，Luna 约 +237 I/66.58%；nonprobe 情形约 +50 I/82.36%、+102 I/75.52%。这些不是实测、区间、保证或验收阈值。

原始 prompts/SSE 与大体量逐调用审计留本地受限归档；仓库交付稳定协议、必要脚本/测试、来源 hash、适量复算结果和中文报告。两模型结果不能代替追加授权后的四模型验收；四模型均须完成末端、残余裁定、离线复算与审查。A3 仍独立必需，不因本实验结果自动启动 O2。
