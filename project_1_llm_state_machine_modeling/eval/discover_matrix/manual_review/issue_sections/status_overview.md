本轮把 60 对逐对人工复核的结果，收敛成一组彼此对得上的数字。下表每个数字都由脚本从逐行数据重算，并经 21 项交叉一致性检查（[reconcile_numbers.py](../reconcile_numbers.py)）全部通过——任何两个来源不一致都必须先解决再发布。

| 量 | 值 | 口径 |
| --- | ---: | --- |
| 逐对复核的差异总数 | **418** | 60 对全覆盖，五档：correct 77 / similar 127 / problem 132 / extra 31 / uncertain 51 |
| 计入问题（基线） | 154 | problem + extra − 范围外扣减 9 |
| **计入问题（主裁定后）** | **153** | 扣 `0013`#1（并发语义，见下）|
| **可入 E1（点值）** | **130** | 四个可归因层之和；词法分层只能给区间 66–144，本轮逐行判完收敛为点值 |
| 可用现有 19 谓词表述 | **123 / 153**（80%）| 独立复跑，只有返回 `False` 才计入 |
| 不可表述 | 30 | 按缺口族归类见下 |
| 落在 paper1 问题定义内 | **153 / 153**（100%）| `T0` + FSM/HSM/EFSM，不含时钟与正交并发 |

分层构成（决定 130 这个点值）：

| 层 | 条数 | 可入 | 判据 |
| --- | ---: | :-: | --- |
| `nl_named` | 70 | ✓ | NL 点名了那个缺失或错位的元素 |
| `wellformedness` | 36 | ✓ | 无需 oracle，仅凭生成模型自身即可判定 |
| `over_specification_benign` | 18 | ✗ | 生成方多出但写不出后果 |
| `nl_contradiction` | 13 | ✓ | 与 NL 的显式义务矛盾 |
| `over_specification` | 11 | ✓ | 生成方凭空多出**且**造成可断言的负面后果 |
| `reference_only` | 3 | ✗ | 只在参考、NL 未点名——不可归因于生成方 |
| `out_of_scope_concurrency` | 1 | ✗ | 主裁定移出范围 |
| `uncertain_stratum` | 1 | ✗ | 已审阅但搁置：当前谓词面给不出正面判定 |
| `over_specification_duplicate` | 1 | ✗ | 后果已被同 pair 的另一条承载，计入会双算 |
| **合计** | **154** | **130 可入** | |

逐行数据：[final_stratification.json](https://gist.github.com/HansBug/daa977482df22711e8e0d00fc80c406c#file-final_stratification-json)（154 行，每行带层、判据、断言与裁定来源）｜ 一致性检查明细：[reconcile.json](https://gist.github.com/HansBug/daa977482df22711e8e0d00fc80c406c#file-reconcile-json) ｜ 分层方法：[FINAL_STRATIFICATION.md](https://gist.github.com/HansBug/daa977482df22711e8e0d00fc80c406c#file-final_stratification-md)
