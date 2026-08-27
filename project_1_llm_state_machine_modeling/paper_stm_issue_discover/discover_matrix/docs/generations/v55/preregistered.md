# v55 固定 15-pair hit 修复事前登记

> 本文件在本代次首次 live method 调用前随实现提交并推送。live run 的 immutable manifest 另行固定实际 source commit、run ID、prompt/schema hash、registry hash、输入 hash、selection preflight hash、成本与 worker 数；不得以本文件替代运行制品。

## 目的与范围

本代只检验 `evidence-discovery-typed-flow.v55-method-only` 对 exact contract、grounding、D 与 publication claim 完整性的通用修复。它不新增、删除、改名或重新定义 `four-family-19-core.v1` 的 19 个谓词，不改变冻结 Judge `05cf0da6`，不改变 W 的 `W0/W1/W2` 三档口径，也不将 bibliography status 接回任何运行时准入。

本轮不是 predicate usage 扩张实验。固定 planned predicate usage 为 12 个诊断谓词；12/15 为稳定合格，13/15 是非阻塞加分项。优化对象是冻结外置 Judge 下的 exact FULL hit 与 report claim 完整性，不能以 pass receipt、W2 总数或低频谓词出场替代。

## 固定输入与执行

- 固定 15 pair：`0001`、`0002`、`0004`、`0010`、`0012`、`0013`、`0023`、`0024`、`0029`、`0035`、`0046`、`0049`、`0053`、`0054`、`0056`。
- 只执行一次新的 15x1 live method；profile 为冻结 construction profile，`--workers 16`，所有 provider error 仅按既有协议原地重试受影响调用或 cell。
- 方法只读取当前 pair 的 NL、PlantUML、canonical source IR、pyfcstm-native FCSTM、inspect-equivalent facts 与 working contracts。不得读取 ledger expected、Judge、答案、其他 pair 或历史成功报告。
- 执行前必须生成新的 selection preflight 与 pyfcstm native projection audit；前者仅作 manifest provenance，后者必须达到 60/60 native source load、54/54 frozen input closure、零 parity difference 与零未批准文本处理。
- method artifact 冻结后，以冻结 `05cf0da6` 在独立路径完整 Judge；Judge 不参与 method 的 candidate、route、W、D 或 publication。

## 预先固定的机制检查

1. live primary contract extraction 的 atomic contract 数少于 numbered-NL segment 数时，至多执行一次 additive `contract_completion`；只接受 typed-new contract/group，canonical semantic key 去重，primary rows 永不覆盖。
2. 初始伪状态的 trigger/guard 领域不变量只由冻结 domain authority 提出，使用 exact native transition carrier 的 S3/S5 输入闭合；S2 endpoint pass 不能删除不同 property/role 的 exact candidate。
3. surviving `undercutting`/`rebutting` 必须引用当前 obligation 的 candidate/binding exact catalog；抽象“隐藏实现”不能单独压制已闭合 candidate。
4. report 必须保留 obligation、root locus/carrier、expected/actual carrier 或 member set、owner/source/target path、event/guard/effect/action role、minimal repair delta、reason 与 basis。粗粒度 predicate `true` 只证明该命题自身。

## 预先固定的验收与停止规则

| 指标 | 收敛门槛 | 目标 |
|---|---:|---:|
| method/Judge 完整性 | 15/15 terminal、60/60 expected 有结果 | 无 crash、无半成品 |
| overall FULL | 51/60 | 53--55/60 |
| L2 FULL | 不低于 23/24 | 24/24 |
| semantic precision | 90% | 不低于近期可比结果 |
| FULL-hit max-W2 | 60% | 保持或提高 |
| planned predicate usage | 12/15 | 13/15 |
| W/D/audit | 零假 W2、零 failure-as-violation | 每条完全闭合 |
| method cost | 尽量不超过 X1v2 的 35 倍 | 质量优先 |

固定 15x1 只运行一次。若结果在 49--50/60，但 exact claim 修复、L2、precision、W2/audit 与 12/15 usage 均稳定，且剩余缺口可审计地集中于高风险 closed-world 边界，则冻结 current 并进入既有 54x3 主线。若出现系统性 W/D 错误、unsafe binding、答案泄漏、Judge 口径变化、明显 precision 回退或易修复的通用 claim-loss 根因，则先做 provider-free stage-loss 修复，不重复同版本采样。
