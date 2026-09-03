# Calibration comparison: current iter7 v3.8 prompt v12 8313a632f

- run dirs: runs/paper1/judge-calibration-8313a632f-v38/current-r1, runs/paper1/judge-calibration-8313a632f-v38/current-r2, runs/paper1/judge-calibration-8313a632f-v38/current-r3
- subset gold rows: 201; judged and matched: 201; missing: 0; judged outside subset: 0; failed pairs: 0

## Headline

- K/N/I agreement with gold: **139/201 = 69.2%** (frozen v3.2 judge on the same rows: 54/201 = 26.9%)
- defect-class exact agreement: 78/201 = 38.8%
- defect-class disagreements that are only D2<->D1: 12
- valid rate: gold 77/201 = 38.3%; new judge 67/201 = 33.3%; frozen judge 169/201 = 84.1%
- arbitrated reports: 197

## K/N/I matrix (rows = new judge, columns = gold)

| new_class \ gold_class | K | N | I | total |
| :-- | --: | --: | --: | --: |
| **K** | 36 | 0 | 6 | 42 |
| **N** | 4 | 3 | 18 | 25 |
| **I** | 13 | 21 | 100 | 134 |
| total | 53 | 24 | 124 | 201 |

## Defect-class matrix (rows = new judge, columns = gold)

| new_defect \ gold_defect | D2 | D1 | D0 | A0_FALSE_POSITIVE | A0_NOT_A_DEFECT_CLAIM | total |
| :-- | --: | --: | --: | --: | --: | --: |
| **D2** | 23 | 12 | 14 | 0 | 2 | 51 |
| **D1** | 0 | 1 | 1 | 0 | 5 | 7 |
| **D0** | 9 | 29 | 36 | 2 | 16 | 92 |
| **A0_FALSE_POSITIVE** | 3 | 0 | 11 | 4 | 18 | 36 |
| **A0_NOT_A_DEFECT_CLAIM** | 0 | 0 | 0 | 1 | 14 | 15 |
| total | 35 | 42 | 62 | 7 | 55 | 201 |

## Per stratum (stratum = frozen judge class -> gold class)

| stratum | n | class agree | defect agree | new class distribution |
| :-- | --: | --: | --: | :-- |
| `I->I` | 12 | 10/12 = 83.3% | 6/12 = 50.0% | I=10, K=2 |
| `I->K` | 8 | 6/8 = 75.0% | 3/8 = 37.5% | I=2, K=6 |
| `I->N` | 12 | 1/12 = 8.3% | 1/12 = 8.3% | I=11, N=1 |
| `K->I` | 1 | 1/1 = 100.0% | 0/1 = 0.0% | I=1 |
| `K->K/D1` | 8 | 6/8 = 75.0% | 0/8 = 0.0% | I=1, K=6, N=1 |
| `K->K/D2` | 22 | 15/22 = 68.2% | 13/22 = 59.1% | I=5, K=15, N=2 |
| `N->I/A0_FALSE_POSITIVE` | 1 | 1/1 = 100.0% | 1/1 = 100.0% | I=1 |
| `N->I/A0_NOT_A_DEFECT_CLAIM` | 50 | 43/50 = 86.0% | 12/50 = 24.0% | I=43, N=7 |
| `N->I/D0` | 60 | 45/60 = 75.0% | 35/60 = 58.3% | I=45, K=4, N=11 |
| `N->K` | 15 | 9/15 = 60.0% | 7/15 = 46.7% | I=5, K=9, N=1 |
| `N->N` | 12 | 2/12 = 16.7% | 0/12 = 0.0% | I=10, N=2 |

## Disagreements by pair

0001=1, 0002=1, 0006=2, 0007=1, 0009=1, 0010=1, 0011=1, 0012=2, 0015=2, 0016=3, 0019=1, 0020=1, 0021=1, 0024=2, 0029=3, 0032=2, 0033=1, 0034=1, 0036=1, 0037=1, 0039=5, 0040=2, 0045=2, 0046=1, 0047=2, 0049=9, 0052=1, 0053=3, 0055=3, 0056=1, 0057=1, 0059=3

