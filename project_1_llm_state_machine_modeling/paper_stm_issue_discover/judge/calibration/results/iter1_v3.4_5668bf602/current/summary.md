# Calibration comparison: current iter1 v3.4 (5668bf602)

- run dirs: runs/paper1/judge-calibration-5668bf602/current-r1, runs/paper1/judge-calibration-5668bf602/current-r2, runs/paper1/judge-calibration-5668bf602/current-r3
- subset gold rows: 201; judged and matched: 201; missing: 0; judged outside subset: 0; failed pairs: 0

## Headline

- K/N/I agreement with gold: **132/201 = 65.7%** (frozen v3.2 judge on the same rows: 54/201 = 26.9%)
- defect-class exact agreement: 65/201 = 32.3%
- defect-class disagreements that are only D2<->D1: 18
- valid rate: gold 77/201 = 38.3%; new judge 89/201 = 44.3%; frozen judge 169/201 = 84.1%
- arbitrated reports: 193

## K/N/I matrix (rows = new judge, columns = gold)

| new_class \ gold_class | K | N | I | total |
| :-- | --: | --: | --: | --: |
| **K** | 35 | 1 | 5 | 41 |
| **N** | 2 | 12 | 34 | 48 |
| **I** | 16 | 11 | 85 | 112 |
| total | 53 | 24 | 124 | 201 |

## Defect-class matrix (rows = new judge, columns = gold)

| new_defect \ gold_defect | D2 | D1 | D0 | A0_FALSE_POSITIVE | A0_NOT_A_DEFECT_CLAIM | total |
| :-- | --: | --: | --: | --: | --: | --: |
| **D2** | 17 | 11 | 15 | 0 | 1 | 44 |
| **D1** | 7 | 15 | 20 | 0 | 3 | 45 |
| **D0** | 2 | 5 | 10 | 1 | 4 | 22 |
| **A0_FALSE_POSITIVE** | 9 | 11 | 17 | 5 | 29 | 71 |
| **A0_NOT_A_DEFECT_CLAIM** | 0 | 0 | 0 | 1 | 18 | 19 |
| total | 35 | 42 | 62 | 7 | 55 | 201 |

## Per stratum (stratum = frozen judge class -> gold class)

| stratum | n | class agree | defect agree | new class distribution |
| :-- | --: | --: | --: | :-- |
| `I->I` | 12 | 12/12 = 100.0% | 7/12 = 58.3% | I=12 |
| `I->K` | 8 | 5/8 = 62.5% | 3/8 = 37.5% | I=3, K=5 |
| `I->N` | 12 | 6/12 = 50.0% | 5/12 = 41.7% | I=6, N=6 |
| `K->I` | 1 | 0/1 = 0.0% | 0/1 = 0.0% | N=1 |
| `K->K/D1` | 8 | 5/8 = 62.5% | 3/8 = 37.5% | I=2, K=5, N=1 |
| `K->K/D2` | 22 | 14/22 = 63.6% | 10/22 = 45.5% | I=7, K=14, N=1 |
| `N->I/A0_FALSE_POSITIVE` | 1 | 1/1 = 100.0% | 1/1 = 100.0% | I=1 |
| `N->I/A0_NOT_A_DEFECT_CLAIM` | 50 | 47/50 = 94.0% | 16/50 = 32.0% | I=47, K=1, N=2 |
| `N->I/D0` | 60 | 25/60 = 41.7% | 9/60 = 15.0% | I=25, K=4, N=31 |
| `N->K` | 15 | 11/15 = 73.3% | 6/15 = 40.0% | I=4, K=11 |
| `N->N` | 12 | 6/12 = 50.0% | 5/12 = 41.7% | I=5, K=1, N=6 |

## Disagreements by pair

0000=1, 0003=3, 0004=4, 0006=1, 0009=1, 0010=1, 0012=2, 0014=4, 0016=3, 0019=1, 0020=1, 0029=3, 0032=3, 0033=2, 0034=2, 0036=1, 0039=4, 0040=1, 0043=4, 0044=4, 0045=1, 0049=6, 0052=3, 0053=3, 0054=4, 0055=2, 0056=1, 0057=1, 0059=2

