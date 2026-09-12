# Calibration comparison: baseline iter8 arm A v3.9 prompt v13 45be62681

- run dirs: runs/paper1/judge-calibration-45be62681-v39A/baseline-r1, runs/paper1/judge-calibration-45be62681-v39A/baseline-r2, runs/paper1/judge-calibration-45be62681-v39A/baseline-r2-resume145104, runs/paper1/judge-calibration-45be62681-v39A/baseline-r3, runs/paper1/judge-calibration-45be62681-v39A/baseline-r3-resume150622, runs/paper1/judge-calibration-45be62681-v39A/baseline-r3-resume154414
- subset gold rows: 100; judged and matched: 100; missing: 0; judged outside subset: 0; failed pairs: 0

## Headline

- K/N/I agreement with gold: **56/100 = 56.0%** (frozen v3.2 judge on the same rows: 30/100 = 30.0%)
- defect-class exact agreement: 50/100 = 50.0%
- defect-class disagreements that are only D2<->D1: 17
- valid rate: gold 68/100 = 68.0%; new judge 69/100 = 69.0%; frozen judge 52/100 = 52.0%
- arbitrated reports: 67

## K/N/I matrix (rows = new judge, columns = gold)

| new_class \ gold_class | K | N | I | total |
| :-- | --: | --: | --: | --: |
| **K** | 31 | 10 | 6 | 47 |
| **N** | 3 | 9 | 10 | 22 |
| **I** | 5 | 10 | 16 | 31 |
| total | 39 | 29 | 32 | 100 |

## Defect-class matrix (rows = new judge, columns = gold)

| new_defect \ gold_defect | D2 | D1 | D0 | A0_FALSE_POSITIVE | A0_NOT_A_DEFECT_CLAIM | total |
| :-- | --: | --: | --: | --: | --: | --: |
| **D2** | 26 | 11 | 10 | 0 | 0 | 47 |
| **D1** | 6 | 9 | 5 | 1 | 0 | 21 |
| **D0** | 2 | 9 | 14 | 0 | 0 | 25 |
| **A0_FALSE_POSITIVE** | 2 | 3 | 1 | 1 | 0 | 7 |
| **A0_NOT_A_DEFECT_CLAIM** | 0 | 0 | 0 | 0 | 0 | 0 |
| total | 36 | 32 | 30 | 2 | 0 | 100 |

## Per stratum (stratum = frozen judge class -> gold class)

| stratum | n | class agree | defect agree | new class distribution |
| :-- | --: | --: | --: | :-- |
| `I->I` | 7 | 5/7 = 71.4% | 4/7 = 57.1% | I=5, K=2 |
| `I->K` | 20 | 16/20 = 80.0% | 12/20 = 60.0% | I=3, K=16, N=1 |
| `I->N` | 21 | 3/21 = 14.3% | 7/21 = 33.3% | I=8, K=10, N=3 |
| `K->K` | 15 | 13/15 = 86.7% | 12/15 = 80.0% | I=2, K=13 |
| `N->I` | 25 | 11/25 = 44.0% | 11/25 = 44.0% | I=11, K=4, N=10 |
| `N->K` | 4 | 2/4 = 50.0% | 2/4 = 50.0% | K=2, N=2 |
| `N->N` | 8 | 6/8 = 75.0% | 2/8 = 25.0% | I=2, N=6 |

## Disagreements by pair

0004=3, 0007=2, 0009=3, 0012=2, 0014=1, 0015=2, 0017=1, 0019=2, 0020=3, 0022=1, 0024=1, 0027=2, 0029=2, 0031=1, 0032=2, 0033=2, 0035=1, 0036=1, 0037=2, 0039=1, 0040=1, 0043=1, 0046=1, 0049=1, 0052=1, 0054=1, 0055=1, 0056=1, 0059=1

