# Calibration comparison: current iter2 v3.5 (8fd87c559)

- run dirs: runs/paper1/judge-calibration-8fd87c559/current-r1, runs/paper1/judge-calibration-8fd87c559/current-r2, runs/paper1/judge-calibration-8fd87c559/current-r3
- subset gold rows: 201; judged and matched: 198; missing: 3; judged outside subset: 0; failed pairs: 1

missing: 0016:r1:issue:2, 0016:r1:issue:6, 0016:r1:issue:7

failures: runs/paper1/judge-calibration-8fd87c559/current-r1:0016

## Headline

- K/N/I agreement with gold: **125/198 = 63.1%** (frozen v3.2 judge on the same rows: 52/198 = 26.3%)
- defect-class exact agreement: 78/198 = 39.4%
- defect-class disagreements that are only D2<->D1: 14
- valid rate: gold 75/198 = 37.9%; new judge 87/198 = 43.9%; frozen judge 166/198 = 83.8%
- arbitrated reports: 193

## K/N/I matrix (rows = new judge, columns = gold)

| new_class \ gold_class | K | N | I | total |
| :-- | --: | --: | --: | --: |
| **K** | 28 | 3 | 8 | 39 |
| **N** | 6 | 12 | 30 | 48 |
| **I** | 17 | 9 | 85 | 111 |
| total | 51 | 24 | 123 | 198 |

## Defect-class matrix (rows = new judge, columns = gold)

| new_defect \ gold_defect | D2 | D1 | D0 | A0_FALSE_POSITIVE | A0_NOT_A_DEFECT_CLAIM | total |
| :-- | --: | --: | --: | --: | --: | --: |
| **D2** | 16 | 10 | 20 | 0 | 2 | 48 |
| **D1** | 4 | 19 | 8 | 1 | 7 | 39 |
| **D0** | 5 | 10 | 22 | 1 | 6 | 44 |
| **A0_FALSE_POSITIVE** | 8 | 2 | 10 | 4 | 23 | 47 |
| **A0_NOT_A_DEFECT_CLAIM** | 1 | 0 | 1 | 1 | 17 | 20 |
| total | 34 | 41 | 61 | 7 | 55 | 198 |

## Per stratum (stratum = frozen judge class -> gold class)

| stratum | n | class agree | defect agree | new class distribution |
| :-- | --: | --: | --: | :-- |
| `I->I` | 12 | 11/12 = 91.7% | 6/12 = 50.0% | I=11, K=1 |
| `I->K` | 8 | 7/8 = 87.5% | 5/8 = 62.5% | I=1, K=7 |
| `I->N` | 12 | 3/12 = 25.0% | 5/12 = 41.7% | I=7, K=2, N=3 |
| `K->I` | 1 | 1/1 = 100.0% | 0/1 = 0.0% | I=1 |
| `K->K/D1` | 7 | 5/7 = 71.4% | 2/7 = 28.6% | I=2, K=5 |
| `K->K/D2` | 21 | 10/21 = 47.6% | 10/21 = 47.6% | I=7, K=10, N=4 |
| `N->I/A0_FALSE_POSITIVE` | 1 | 1/1 = 100.0% | 1/1 = 100.0% | I=1 |
| `N->I/A0_NOT_A_DEFECT_CLAIM` | 50 | 41/50 = 82.0% | 15/50 = 30.0% | I=41, K=2, N=7 |
| `N->I/D0` | 59 | 31/59 = 52.5% | 21/59 = 35.6% | I=31, K=5, N=23 |
| `N->K` | 15 | 6/15 = 40.0% | 5/15 = 33.3% | I=7, K=6, N=2 |
| `N->N` | 12 | 9/12 = 75.0% | 8/12 = 66.7% | I=2, K=1, N=9 |

## Disagreements by pair

0002=1, 0003=3, 0004=3, 0007=2, 0009=2, 0010=1, 0011=1, 0012=3, 0014=2, 0016=2, 0017=1, 0020=2, 0021=1, 0024=2, 0029=2, 0032=3, 0033=1, 0034=2, 0036=1, 0039=2, 0040=3, 0043=3, 0044=4, 0045=2, 0046=1, 0049=10, 0050=1, 0052=2, 0053=3, 0055=2, 0056=3, 0059=2

