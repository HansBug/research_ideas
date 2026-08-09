# v46 全量 324 事前登记

> 判据与基线数字写于 2026-08-09T16:40Z 启动之前（与启动命令同一次写入，先写后启）；
> 本文件的 git 提交发生在启动之后约数分钟，提交动作本身不证明它写在运行之前。
> 旁证：`runs/paper1/matrix-v46-full/WALLCLOCK.txt` 的 `segment_1_started_at` 与本文件 mtime 可比对。

```
v46 全量 324 事前登记
代码：3aef252c（含 6f43e335 四方互斥消解 / 107f8cc3 Gate D 文案 / 85768484 聚合门 /
      3aef252c named_elements 两条出路）
网格：54 pair × 2 模型 × 3 轮 = 324 格，MAX=16，MAXTRY=3
对照：v37 全量 324（同一 GRID.txt），基线 hit@1 280/594 = 47.1%
预期（跑前写死）：
 1. 降级格占比 < 10%（v44 六 pair 子集为 63%）
 2. 耗尽格 ≤ 5/324（v37 为 1）
 3. hit@1 不低于 v37 的 47.1%
 4. unresolved_reference / RequiredFamilyMissing / 短路 primary 三类合计较 v44 同口径大幅下降
判定：verdict_tiers A/B/C 三层 + 人工，口径与 v37/v40/v41/v44 完全一致；
      跑后必须过 adjudication_recheck（同形态判出两种结果须为 0 对）
```
