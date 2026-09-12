# Calibration comparison: current iter5 v3.7 majority-of-3 (bc8e60973)

- run dirs: runs/paper1/judge-calibration-bc8e60973-majority3/current-r1, runs/paper1/judge-calibration-bc8e60973-majority3/current-r2, runs/paper1/judge-calibration-bc8e60973-majority3/current-r3
- subset gold rows: 201; judged and matched: 197; missing: 4; judged outside subset: 0; failed pairs: 2

missing: 0009:r3:issue:0, 0009:r3:issue:21, 0057:r3:issue:0, 0057:r3:issue:3

failures: runs/paper1/judge-calibration-bc8e60973-majority3/current-r3:0057, runs/paper1/judge-calibration-bc8e60973-majority3/current-r3:0009

## Headline

- K/N/I agreement with gold: **136/197 = 69.0%** (frozen v3.2 judge on the same rows: 53/197 = 26.9%)
- defect-class exact agreement: 92/197 = 46.7%
- defect-class disagreements that are only D2<->D1: 12
- valid rate: gold 74/197 = 37.6%; new judge 99/197 = 50.3%; frozen judge 166/197 = 84.3%
- arbitrated reports: 16

## K/N/I matrix (rows = new judge, columns = gold)

| new_class \ gold_class | K | N | I | total |
| :-- | --: | --: | --: | --: |
| **K** | 33 | 2 | 6 | 41 |
| **N** | 8 | 18 | 32 | 58 |
| **I** | 9 | 4 | 85 | 98 |
| total | 50 | 24 | 123 | 197 |

## Defect-class matrix (rows = new judge, columns = gold)

| new_defect \ gold_defect | D2 | D1 | D0 | A0_FALSE_POSITIVE | A0_NOT_A_DEFECT_CLAIM | total |
| :-- | --: | --: | --: | --: | --: | --: |
| **D2** | 25 | 10 | 14 | 0 | 1 | 50 |
| **D1** | 2 | 24 | 9 | 0 | 14 | 49 |
| **D0** | 5 | 6 | 30 | 1 | 7 | 49 |
| **A0_FALSE_POSITIVE** | 2 | 0 | 9 | 5 | 24 | 40 |
| **A0_NOT_A_DEFECT_CLAIM** | 0 | 0 | 0 | 1 | 8 | 9 |
| total | 34 | 40 | 62 | 7 | 54 | 197 |

## Per stratum (stratum = frozen judge class -> gold class)

| stratum | n | class agree | defect agree | new class distribution |
| :-- | --: | --: | --: | :-- |
| `I->I` | 12 | 11/12 = 91.7% | 5/12 = 41.7% | I=11, K=1 |
| `I->K` | 7 | 5/7 = 71.4% | 5/7 = 71.4% | I=1, K=5, N=1 |
| `I->N` | 12 | 8/12 = 66.7% | 10/12 = 83.3% | I=2, K=2, N=8 |
| `K->I` | 1 | 0/1 = 0.0% | 0/1 = 0.0% | K=1 |
| `K->K/D1` | 7 | 5/7 = 71.4% | 2/7 = 28.6% | K=5, N=2 |
| `K->K/D2` | 22 | 14/22 = 63.6% | 14/22 = 63.6% | I=6, K=14, N=2 |
| `N->I/A0_FALSE_POSITIVE` | 1 | 1/1 = 100.0% | 1/1 = 100.0% | I=1 |
| `N->I/A0_NOT_A_DEFECT_CLAIM` | 49 | 35/49 = 71.4% | 7/49 = 14.3% | I=35, K=1, N=13 |
| `N->I/D0` | 60 | 38/60 = 63.3% | 30/60 = 50.0% | I=38, K=3, N=19 |
| `N->K` | 14 | 9/14 = 64.3% | 10/14 = 71.4% | I=2, K=9, N=3 |
| `N->N` | 12 | 10/12 = 83.3% | 8/12 = 66.7% | I=2, N=10 |

## Disagreements by pair

0000=1, 0001=1, 0003=2, 0007=1, 0009=1, 0010=1, 0012=3, 0014=2, 0016=5, 0020=1, 0021=1, 0029=1, 0032=2, 0034=2, 0035=1, 0036=3, 0037=1, 0039=1, 0040=2, 0044=2, 0045=3, 0046=1, 0047=1, 0049=6, 0050=1, 0052=4, 0053=3, 0054=1, 0055=3, 0059=4

