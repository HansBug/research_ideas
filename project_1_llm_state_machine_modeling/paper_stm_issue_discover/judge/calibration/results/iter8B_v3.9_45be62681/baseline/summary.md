# Calibration comparison: baseline iter8 arm B v3.9 prompt v13 45be62681

- run dirs: runs/paper1/judge-calibration-45be62681-v39B/baseline-r1, runs/paper1/judge-calibration-45be62681-v39B/baseline-r2, runs/paper1/judge-calibration-45be62681-v39B/baseline-r2-resume145104, runs/paper1/judge-calibration-45be62681-v39B/baseline-r3, runs/paper1/judge-calibration-45be62681-v39B/baseline-r3-resume150423, runs/paper1/judge-calibration-45be62681-v39B/baseline-r3-resume154414
- subset gold rows: 100; judged and matched: 100; missing: 0; judged outside subset: 0; failed pairs: 1

failures: runs/paper1/judge-calibration-45be62681-v39B/baseline-r3:0002

## Headline

- K/N/I agreement with gold: **57/100 = 57.0%** (frozen v3.2 judge on the same rows: 30/100 = 30.0%)
- defect-class exact agreement: 50/100 = 50.0%
- defect-class disagreements that are only D2<->D1: 15
- valid rate: gold 68/100 = 68.0%; new judge 73/100 = 73.0%; frozen judge 52/100 = 52.0%
- arbitrated reports: 33

## K/N/I matrix (rows = new judge, columns = gold)

| new_class \ gold_class | K | N | I | total |
| :-- | --: | --: | --: | --: |
| **K** | 33 | 9 | 6 | 48 |
| **N** | 3 | 10 | 12 | 25 |
| **I** | 3 | 10 | 14 | 27 |
| total | 39 | 29 | 32 | 100 |

## Defect-class matrix (rows = new judge, columns = gold)

| new_defect \ gold_defect | D2 | D1 | D0 | A0_FALSE_POSITIVE | A0_NOT_A_DEFECT_CLAIM | total |
| :-- | --: | --: | --: | --: | --: | --: |
| **D2** | 28 | 11 | 13 | 1 | 0 | 53 |
| **D1** | 4 | 9 | 3 | 0 | 0 | 16 |
| **D0** | 1 | 10 | 12 | 0 | 0 | 23 |
| **A0_FALSE_POSITIVE** | 3 | 2 | 2 | 1 | 0 | 8 |
| **A0_NOT_A_DEFECT_CLAIM** | 0 | 0 | 0 | 0 | 0 | 0 |
| total | 36 | 32 | 30 | 2 | 0 | 100 |

## Per stratum (stratum = frozen judge class -> gold class)

| stratum | n | class agree | defect agree | new class distribution |
| :-- | --: | --: | --: | :-- |
| `I->I` | 7 | 5/7 = 71.4% | 4/7 = 57.1% | I=5, K=2 |
| `I->K` | 20 | 18/20 = 90.0% | 12/20 = 60.0% | I=1, K=18, N=1 |
| `I->N` | 21 | 4/21 = 19.0% | 6/21 = 28.6% | I=9, K=8, N=4 |
| `K->K` | 15 | 12/15 = 80.0% | 13/15 = 86.7% | I=2, K=12, N=1 |
| `N->I` | 25 | 9/25 = 36.0% | 9/25 = 36.0% | I=9, K=4, N=12 |
| `N->K` | 4 | 3/4 = 75.0% | 2/4 = 50.0% | K=3, N=1 |
| `N->N` | 8 | 6/8 = 75.0% | 4/8 = 50.0% | I=1, K=1, N=6 |

## Disagreements by pair

0000=1, 0003=1, 0004=2, 0007=2, 0009=3, 0012=1, 0014=1, 0017=1, 0019=2, 0020=3, 0022=1, 0023=1, 0027=2, 0029=2, 0031=1, 0032=2, 0033=2, 0036=1, 0037=3, 0039=1, 0040=1, 0041=1, 0043=1, 0046=1, 0049=1, 0051=1, 0052=1, 0054=1, 0055=1, 0056=1

