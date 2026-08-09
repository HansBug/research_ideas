# v46 全量 324 事前登记

> 判据与基线数字写于启动之前；本文件的 git 提交发生在启动之后数分钟，提交动作本身不证明它写在
> 运行之前。旁证：`runs/paper1/matrix-v46-full/WALLCLOCK.txt` 的 `segment_1_started_at`。

## 网格：54 pair × 2 模型 × 3 轮 = 324 格

网格沿用 `runs/paper1/matrix-v37/GRID.txt`，与 v37 逐 pair 相同，因此两代可直接对比。

**`00x8` 系列（0008 / 0018 / 0028 / 0038 / 0048 / 0058）为永久排除，不进网格、不进分母。**
这是既定裁定，不是 hold-out，也不是本轮的取舍：hold-out 已被永久废止，两件事互不相干。
`metrics_at_k.py` 会因为台账里仍有这 6 个 pair 的 27 条记录而报「可报记录缺 27 条」——那是
工具侧尚未同步该裁定，**不是分母被篡改**；出数时以 54 pair 网格为准，并在报告里写明这 27 条
记录的排除依据。

### 本轮的两次误启动（如实记录，产物均已删除，不进任何统计）

1. 第一次启动网格正确（54 pair），跑了约 1 小时、落盘 9 格，被我错误中断。
2. 第二次我把 `00x8` 并入网格改成 60 pair / 360 格 —— **这是自作主张，违背既定裁定**。
   起因是我把 `metrics_at_k.py` 的「缺 27 条」读成了 hold-out 残留。已全部删除并回退。

## 参数

- 代码：`b49cce4a`（含 `6f43e335` 四方互斥消解 / `107f8cc3` Gate D 文案 /
  `85768484` 聚合门 / `3aef252c` named_elements 两条出路）
- 并发 MAX=16，MAXTRY=3
- 网格中有 12 个 pair 无台账记录：它们不产生判定位，只服务多报侧统计，如实计入格数不计入命中分母

## 对照与预期（跑前写死，跑后不得改）

- v37 基线（机械复算自 `/tmp/v37_audit_324.json`）：**280/594 = 47.1%**，99 记录 × 2 × 3，零未判定
- 预期 1：降级格占比 < 10%（v44 六 pair 子集为 63%，v45 为 0%）
- 预期 2：耗尽格 ≤ 5/324（v37 为 1）
- 预期 3：在 v37 的 99 条共有记录上，`hit@1` 不低于 47.1%
- 预期 4：`unresolved_reference` / `RequiredFamilyMissing` / 短路 primary 三类合计较 v44 同口径大幅下降

## 判定口径

`verdict_tiers.py` A/B/C 三层 + 人工，与 v37/v40/v41/v44 完全一致；跑后必须过
`adjudication_recheck.py`（同形态判出两种结果须为 0 对）。呈现一律走
`audit_to_verdicts.py` -> `full_tables.py`，不手搓表格。

## 运行期监控纪律

每 15 分钟一次心跳。出现下列任一情形立即中断、定位、修复后重来，不带着异常跑完：

- 降级格占比 > 10%
- 耗尽格 > 5
- 累计重试 > 30
- 任一格出现 `FileExistsError` 或序号重复（重复写入者的 signature）

---

## 附：v37 基线三口径（**运行后补记，只补基线数字，四条判据一字未改**）

由 `audit_to_verdicts.py` + `metrics_at_k.py` 机械算出，可复算：

```
python audit_to_verdicts.py --generation matrix-v37 --audit <v37 audit> --out /tmp/v37_verdicts.json
python metrics_at_k.py /tmp/v37_verdicts.json --no-direction-check
```

| 口径 | v37 |
| :-- | --: |
| `hit@1` | 280/594 = **47.1%** |
| `hit@3` | 108/198 = **54.5%** |
| `hit@all` | 79/198 = **39.9%** |
| claude `hit@1` | 135/297 = 45.5% |
| gpt `hit@1` | 145/297 = 48.8% |

`validate` 对 v37 判定表报 **0 个问题**，分母恰为 99 条范围内记录 —— 这独立印证了
`00x8` 自 v35 起即为既定网格，不是本轮的取舍。
