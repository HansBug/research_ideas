# Calibration comparison: current iter8 arm B v3.9 prompt v13 45be62681

- run dirs: runs/paper1/judge-calibration-45be62681-v39B/current-r1, runs/paper1/judge-calibration-45be62681-v39B/current-r2, runs/paper1/judge-calibration-45be62681-v39B/current-r2-resume150740, runs/paper1/judge-calibration-45be62681-v39B/current-r2-resume154414, runs/paper1/judge-calibration-45be62681-v39B/current-r3, runs/paper1/judge-calibration-45be62681-v39B/current-r3-resume155654
- subset gold rows: 201; judged and matched: 201; missing: 0; judged outside subset: 0; failed pairs: 0

## Headline

- K/N/I agreement with gold: **144/201 = 71.6%** (frozen v3.2 judge on the same rows: 54/201 = 26.9%)
- defect-class exact agreement: 85/201 = 42.3%
- defect-class disagreements that are only D2<->D1: 12
- valid rate: gold 77/201 = 38.3%; new judge 73/201 = 36.3%; frozen judge 169/201 = 84.1%
- arbitrated reports: 91

## K/N/I matrix (rows = new judge, columns = gold)

| new_class \ gold_class | K | N | I | total |
| :-- | --: | --: | --: | --: |
| **K** | 36 | 6 | 9 | 51 |
| **N** | 1 | 7 | 14 | 22 |
| **I** | 16 | 11 | 101 | 128 |
| total | 53 | 24 | 124 | 201 |

## Defect-class matrix (rows = new judge, columns = gold)

| new_defect \ gold_defect | D2 | D1 | D0 | A0_FALSE_POSITIVE | A0_NOT_A_DEFECT_CLAIM | total |
| :-- | --: | --: | --: | --: | --: | --: |
| **D2** | 19 | 11 | 13 | 0 | 1 | 44 |
| **D1** | 1 | 13 | 5 | 0 | 1 | 20 |
| **D0** | 8 | 17 | 40 | 2 | 10 | 77 |
| **A0_FALSE_POSITIVE** | 7 | 1 | 4 | 4 | 34 | 50 |
| **A0_NOT_A_DEFECT_CLAIM** | 0 | 0 | 0 | 1 | 9 | 10 |
| total | 35 | 42 | 62 | 7 | 55 | 201 |

## Per stratum (stratum = frozen judge class -> gold class)

| stratum | n | class agree | defect agree | new class distribution |
| :-- | --: | --: | --: | :-- |
| `I->I` | 12 | 11/12 = 91.7% | 5/12 = 41.7% | I=11, K=1 |
| `I->K` | 8 | 6/8 = 75.0% | 2/8 = 25.0% | I=2, K=6 |
| `I->N` | 12 | 4/12 = 33.3% | 4/12 = 33.3% | I=7, K=1, N=4 |
| `K->I` | 1 | 0/1 = 0.0% | 0/1 = 0.0% | K=1 |
| `K->K/D1` | 8 | 6/8 = 75.0% | 3/8 = 37.5% | I=2, K=6 |
| `K->K/D2` | 22 | 15/22 = 68.2% | 14/22 = 63.6% | I=6, K=15, N=1 |
| `N->I/A0_FALSE_POSITIVE` | 1 | 1/1 = 100.0% | 1/1 = 100.0% | I=1 |
| `N->I/A0_NOT_A_DEFECT_CLAIM` | 50 | 48/50 = 96.0% | 9/50 = 18.0% | I=48, K=1, N=1 |
| `N->I/D0` | 60 | 41/60 = 68.3% | 38/60 = 63.3% | I=41, K=6, N=13 |
| `N->K` | 15 | 9/15 = 60.0% | 4/15 = 26.7% | I=6, K=9 |
| `N->N` | 12 | 3/12 = 25.0% | 5/12 = 41.7% | I=4, K=5, N=3 |

## Disagreements by pair

0000=1, 0002=1, 0003=3, 0004=1, 0005=1, 0006=1, 0007=1, 0009=1, 0010=1, 0011=1, 0012=2, 0014=2, 0016=1, 0019=1, 0020=1, 0029=2, 0032=2, 0033=2, 0034=1, 0036=1, 0037=1, 0039=4, 0040=3, 0043=2, 0044=1, 0045=1, 0046=1, 0049=7, 0052=2, 0053=3, 0055=2, 0056=1, 0059=2

