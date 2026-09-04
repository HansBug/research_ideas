# Calibration comparison: current iter3 v3.6 (e5d5485be)

- run dirs: runs/paper1/judge-calibration-e5d5485be/current-r1, runs/paper1/judge-calibration-e5d5485be/current-r2, runs/paper1/judge-calibration-e5d5485be/current-r3
- subset gold rows: 201; judged and matched: 200; missing: 1; judged outside subset: 0; failed pairs: 1

missing: 0027:r3:issue:1

failures: runs/paper1/judge-calibration-e5d5485be/current-r3:0027

## Headline

- K/N/I agreement with gold: **148/200 = 74.0%** (frozen v3.2 judge on the same rows: 53/200 = 26.5%)
- defect-class exact agreement: 105/200 = 52.5%
- defect-class disagreements that are only D2<->D1: 16
- valid rate: gold 76/200 = 38.0%; new judge 92/200 = 46.0%; frozen judge 168/200 = 84.0%
- arbitrated reports: 192

## K/N/I matrix (rows = new judge, columns = gold)

| new_class \ gold_class | K | N | I | total |
| :-- | --: | --: | --: | --: |
| **K** | 39 | 4 | 6 | 49 |
| **N** | 4 | 15 | 24 | 43 |
| **I** | 9 | 5 | 94 | 108 |
| total | 52 | 24 | 124 | 200 |

## Defect-class matrix (rows = new judge, columns = gold)

| new_defect \ gold_defect | D2 | D1 | D0 | A0_FALSE_POSITIVE | A0_NOT_A_DEFECT_CLAIM | total |
| :-- | --: | --: | --: | --: | --: | --: |
| **D2** | 24 | 14 | 11 | 0 | 0 | 49 |
| **D1** | 2 | 22 | 8 | 0 | 11 | 43 |
| **D0** | 6 | 6 | 37 | 2 | 8 | 59 |
| **A0_FALSE_POSITIVE** | 2 | 0 | 6 | 5 | 19 | 32 |
| **A0_NOT_A_DEFECT_CLAIM** | 0 | 0 | 0 | 0 | 17 | 17 |
| total | 34 | 42 | 62 | 7 | 55 | 200 |

## Per stratum (stratum = frozen judge class -> gold class)

| stratum | n | class agree | defect agree | new class distribution |
| :-- | --: | --: | --: | :-- |
| `I->I` | 12 | 12/12 = 100.0% | 6/12 = 50.0% | I=12 |
| `I->K` | 8 | 6/8 = 75.0% | 4/8 = 50.0% | I=2, K=6 |
| `I->N` | 12 | 7/12 = 58.3% | 9/12 = 75.0% | I=3, K=2, N=7 |
| `K->I` | 1 | 0/1 = 0.0% | 0/1 = 0.0% | N=1 |
| `K->K/D1` | 8 | 7/8 = 87.5% | 4/8 = 50.0% | I=1, K=7 |
| `K->K/D2` | 21 | 13/21 = 61.9% | 13/21 = 61.9% | I=6, K=13, N=2 |
| `N->I/A0_FALSE_POSITIVE` | 1 | 1/1 = 100.0% | 1/1 = 100.0% | I=1 |
| `N->I/A0_NOT_A_DEFECT_CLAIM` | 50 | 40/50 = 80.0% | 16/50 = 32.0% | I=40, K=2, N=8 |
| `N->I/D0` | 60 | 41/60 = 68.3% | 36/60 = 60.0% | I=41, K=4, N=15 |
| `N->K` | 15 | 13/15 = 86.7% | 11/15 = 73.3% | K=13, N=2 |
| `N->N` | 12 | 8/12 = 66.7% | 5/12 = 41.7% | I=2, K=2, N=8 |

## Disagreements by pair

0000=1, 0001=1, 0003=3, 0007=1, 0009=1, 0010=1, 0011=1, 0012=2, 0014=1, 0016=3, 0017=1, 0019=1, 0020=1, 0029=4, 0034=2, 0036=2, 0040=2, 0045=1, 0046=1, 0049=8, 0050=1, 0052=3, 0053=3, 0055=2, 0056=1, 0059=4

