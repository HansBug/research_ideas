# 机制层面的离线模拟：多读投票与置信度分流（迭代 3 与 4 的采样池）

迭代 3（`e5d5485be`）与迭代 4（`8d8452a6f`）的 validity 提示词相同，每条报告因此有最多 6 个同分布的独立采样（两轮 × 读数 1、读数 2、仲裁）。用 [scripts/simulate_aggregation.py](../scripts/simulate_aggregation.py) 在不新增 provider 调用的前提下模拟三类机制改动能把与人工的一致率推到哪里。有效结果的 relation 取任一轮判有效时的 relation，两轮都判无效时记 N；这是上界估计。

## 多数投票

| aggregation | current | baseline |
| :-- | :-- | :-- |
| run A final | 148/200 = 74.0% | 58/100 = 58.0% |
| run B final | 135/200 = 67.5% | 58/100 = 58.0% |
| run A majority(r1, r2, arbitration) else final | 148/200 = 74.0% | 58/100 = 58.0% |
| run B majority(r1, r2, arbitration) else final | 137/200 = 68.5% | 58/100 = 58.0% |
| pooled majority of 4 primaries else A final | 149/200 = 74.5% | 56/100 = 56.0% |
| pooled majority of up to 6 samples else A final | 150/200 = 75.0% | 58/100 = 58.0% |
| pooled majority of up to 6 on valid/invalid only | 148/200 = 74.0% | 59/100 = 59.0% |

## 上界

- oracle ceiling (current): any of up to 6 pooled samples equals gold: 167/200 = 83.5%
- oracle ceiling (baseline): any of up to 6 pooled samples equals gold: 69/100 = 69.0%

## 置信度分流（confident 列 = 该门通过的报告与人工的一致率；uncertain 列 = 未通过的）

| confidence gate | side | confident | uncertain | routed to human |
| :-- | :-- | :-- | :-- | :-- |
| run B readings agree on valid/invalid | current | 109/159 = 68.6% | 20/41 = 48.8% | 20% |
| run B readings agree on valid/invalid | baseline | 52/85 = 61.2% | 7/15 = 46.7% | 15% |
| run B readings agree on defect_class | current | 91/132 = 68.9% | 38/68 = 55.9% | 34% |
| run B readings agree on defect_class | baseline | 47/78 = 60.3% | 12/22 = 54.5% | 22% |
| 4 primaries unanimous on valid/invalid | current | 82/116 = 70.7% | 47/84 = 56.0% | 42% |
| 4 primaries unanimous on valid/invalid | baseline | 46/74 = 62.2% | 13/26 = 50.0% | 26% |
| both runs' finals give the same K/N/I | current | 113/144 = 78.5% | 16/56 = 28.6% | 28% |
| both runs' finals give the same K/N/I | baseline | 49/77 = 63.6% | 10/23 = 43.5% | 23% |

## 结论

1. 三读多数（run 内 r1、r2、仲裁）与单轮 final 一致率相同；把两轮最多 6 个采样合起来取多数，current 最高 75.0%、baseline 58–59%，与单轮持平。剩余分歧是逐条稳定的，不是随机抖动。
2. 6 个采样里「至少一个等于人工」也只有 current 82%、baseline 68%：即使能完美挑选采样，也到不了 85%。
3. 置信度分流不成立：judge 自身最一致的那部分报告（两轮 final 相同）与人工的一致率 current 78.5%、baseline 63.6%，仍低于门槛，而且要把 23–42% 的报告交给人工。
4. 因此在这份 gold 与这个子集上，85% 的登记门槛在提示词、采样聚合、置信度分流三条路径下都不可达；残余差异来自 D0↔D1 与 relation 边界上 gold 自身的不一致（见迭代 2、3 说明），只能通过统一 gold 口径解决，那超出本工作区的范围。
