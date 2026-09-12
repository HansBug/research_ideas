# Calibration comparison: current iter8 arm A v3.9 prompt v13 45be62681

- run dirs: runs/paper1/judge-calibration-45be62681-v39A/current-r1, runs/paper1/judge-calibration-45be62681-v39A/current-r1-resume155729, runs/paper1/judge-calibration-45be62681-v39A/current-r2, runs/paper1/judge-calibration-45be62681-v39A/current-r2-resume151040, runs/paper1/judge-calibration-45be62681-v39A/current-r2-resume154414, runs/paper1/judge-calibration-45be62681-v39A/current-r3, runs/paper1/judge-calibration-45be62681-v39A/current-r3-resume155654
- subset gold rows: 201; judged and matched: 201; missing: 0; judged outside subset: 0; failed pairs: 3

failures: runs/paper1/judge-calibration-45be62681-v39A/current-r1:0001, runs/paper1/judge-calibration-45be62681-v39A/current-r1:0010, runs/paper1/judge-calibration-45be62681-v39A/current-r3:0002

## Headline

- K/N/I agreement with gold: **142/201 = 70.6%** (frozen v3.2 judge on the same rows: 54/201 = 26.9%)
- defect-class exact agreement: 95/201 = 47.3%
- defect-class disagreements that are only D2<->D1: 14
- valid rate: gold 77/201 = 38.3%; new judge 82/201 = 40.8%; frozen judge 169/201 = 84.1%
- arbitrated reports: 201

## K/N/I matrix (rows = new judge, columns = gold)

| new_class \ gold_class | K | N | I | total |
| :-- | --: | --: | --: | --: |
| **K** | 42 | 4 | 12 | 58 |
| **N** | 0 | 6 | 18 | 24 |
| **I** | 11 | 14 | 94 | 119 |
| total | 53 | 24 | 124 | 201 |

## Defect-class matrix (rows = new judge, columns = gold)

| new_defect \ gold_defect | D2 | D1 | D0 | A0_FALSE_POSITIVE | A0_NOT_A_DEFECT_CLAIM | total |
| :-- | --: | --: | --: | --: | --: | --: |
| **D2** | 26 | 14 | 15 | 1 | 4 | 60 |
| **D1** | 0 | 10 | 5 | 0 | 4 | 19 |
| **D0** | 4 | 18 | 38 | 3 | 9 | 72 |
| **A0_FALSE_POSITIVE** | 4 | 0 | 4 | 2 | 19 | 29 |
| **A0_NOT_A_DEFECT_CLAIM** | 1 | 0 | 0 | 1 | 19 | 21 |
| total | 35 | 42 | 62 | 7 | 55 | 201 |

## Per stratum (stratum = frozen judge class -> gold class)

| stratum | n | class agree | defect agree | new class distribution |
| :-- | --: | --: | --: | :-- |
| `I->I` | 12 | 10/12 = 83.3% | 4/12 = 33.3% | I=10, K=2 |
| `I->K` | 8 | 7/8 = 87.5% | 4/8 = 50.0% | I=1, K=7 |
| `I->N` | 12 | 3/12 = 25.0% | 5/12 = 41.7% | I=7, K=2, N=3 |
| `K->I` | 1 | 0/1 = 0.0% | 0/1 = 0.0% | K=1 |
| `K->K/D1` | 8 | 8/8 = 100.0% | 2/8 = 25.0% | K=8 |
| `K->K/D2` | 22 | 16/22 = 72.7% | 15/22 = 68.2% | I=6, K=16 |
| `N->I/A0_FALSE_POSITIVE` | 1 | 0/1 = 0.0% | 0/1 = 0.0% | N=1 |
| `N->I/A0_NOT_A_DEFECT_CLAIM` | 50 | 43/50 = 86.0% | 17/50 = 34.0% | I=43, K=4, N=3 |
| `N->I/D0` | 60 | 41/60 = 68.3% | 38/60 = 63.3% | I=41, K=5, N=14 |
| `N->K` | 15 | 11/15 = 73.3% | 7/15 = 46.7% | I=4, K=11 |
| `N->N` | 12 | 3/12 = 25.0% | 3/12 = 25.0% | I=7, K=2, N=3 |

## Disagreements by pair

0001=1, 0002=1, 0003=2, 0006=1, 0007=1, 0009=2, 0010=1, 0011=1, 0012=2, 0014=2, 0016=1, 0020=2, 0021=2, 0029=3, 0032=3, 0033=3, 0034=1, 0035=1, 0036=1, 0037=1, 0039=4, 0040=2, 0044=1, 0046=2, 0049=9, 0050=1, 0052=2, 0053=1, 0054=1, 0055=1, 0056=1, 0059=2

