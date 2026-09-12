# Calibration comparison: current iter9 v3.10 prompt v14 5de564dad

- run dirs: runs/paper1/judge-calibration-5de564dad-v310/current-r1, runs/paper1/judge-calibration-5de564dad-v310/current-r2, runs/paper1/judge-calibration-5de564dad-v310/current-r3-resume181311
- subset gold rows: 201; judged and matched: 201; missing: 0; judged outside subset: 0; failed pairs: 0

## Headline

- K/N/I agreement with gold: **132/201 = 65.7%** (frozen v3.2 judge on the same rows: 54/201 = 26.9%)
- defect-class exact agreement: 81/201 = 40.3%
- defect-class disagreements that are only D2<->D1: 21
- valid rate: gold 77/201 = 38.3%; new judge 109/201 = 54.2%; frozen judge 169/201 = 84.1%
- arbitrated reports: 78

## K/N/I matrix (rows = new judge, columns = gold)

| new_class \ gold_class | K | N | I | total |
| :-- | --: | --: | --: | --: |
| **K** | 44 | 7 | 17 | 68 |
| **N** | 2 | 10 | 29 | 41 |
| **I** | 7 | 7 | 78 | 92 |
| total | 53 | 24 | 124 | 201 |

## Defect-class matrix (rows = new judge, columns = gold)

| new_defect \ gold_defect | D2 | D1 | D0 | A0_FALSE_POSITIVE | A0_NOT_A_DEFECT_CLAIM | total |
| :-- | --: | --: | --: | --: | --: | --: |
| **D2** | 24 | 18 | 19 | 0 | 5 | 66 |
| **D1** | 3 | 16 | 8 | 0 | 13 | 40 |
| **D0** | 4 | 7 | 28 | 3 | 6 | 48 |
| **A0_FALSE_POSITIVE** | 4 | 1 | 7 | 3 | 21 | 36 |
| **A0_NOT_A_DEFECT_CLAIM** | 0 | 0 | 0 | 1 | 10 | 11 |
| total | 35 | 42 | 62 | 7 | 55 | 201 |

## Per stratum (stratum = frozen judge class -> gold class)

| stratum | n | class agree | defect agree | new class distribution |
| :-- | --: | --: | --: | :-- |
| `I->I` | 12 | 9/12 = 75.0% | 5/12 = 41.7% | I=9, K=2, N=1 |
| `I->K` | 8 | 7/8 = 87.5% | 5/8 = 62.5% | I=1, K=7 |
| `I->N` | 12 | 5/12 = 41.7% | 7/12 = 58.3% | I=5, K=2, N=5 |
| `K->I` | 1 | 1/1 = 100.0% | 0/1 = 0.0% | I=1 |
| `K->K/D1` | 8 | 7/8 = 87.5% | 2/8 = 25.0% | I=1, K=7 |
| `K->K/D2` | 22 | 15/22 = 68.2% | 12/22 = 54.5% | I=5, K=15, N=2 |
| `N->I/A0_FALSE_POSITIVE` | 1 | 1/1 = 100.0% | 0/1 = 0.0% | I=1 |
| `N->I/A0_NOT_A_DEFECT_CLAIM` | 50 | 32/50 = 64.0% | 8/50 = 16.0% | I=32, K=6, N=12 |
| `N->I/D0` | 60 | 35/60 = 58.3% | 28/60 = 46.7% | I=35, K=9, N=16 |
| `N->K` | 15 | 15/15 = 100.0% | 9/15 = 60.0% | K=15 |
| `N->N` | 12 | 5/12 = 41.7% | 5/12 = 41.7% | I=2, K=5, N=5 |

## Disagreements by pair

0001=1, 0003=3, 0007=1, 0009=2, 0010=1, 0012=3, 0016=5, 0019=1, 0020=2, 0022=1, 0024=2, 0029=2, 0032=3, 0033=3, 0034=2, 0036=3, 0037=1, 0039=3, 0040=2, 0043=1, 0044=1, 0045=1, 0046=2, 0049=9, 0050=1, 0052=4, 0053=2, 0055=1, 0056=1, 0057=1, 0059=4

