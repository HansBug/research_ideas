# Calibration comparison: baseline iter1 v3.4 (5668bf602)

- run dirs: runs/paper1/judge-calibration-5668bf602/baseline-r1, runs/paper1/judge-calibration-5668bf602/baseline-r2, runs/paper1/judge-calibration-5668bf602/baseline-r3
- subset gold rows: 100; judged and matched: 100; missing: 0; judged outside subset: 0; failed pairs: 0

## Headline

- K/N/I agreement with gold: **46/100 = 46.0%** (frozen v3.2 judge on the same rows: 30/100 = 30.0%)
- defect-class exact agreement: 40/100 = 40.0%
- defect-class disagreements that are only D2<->D1: 15
- valid rate: gold 68/100 = 68.0%; new judge 67/100 = 67.0%; frozen judge 52/100 = 52.0%
- arbitrated reports: 72

## K/N/I matrix (rows = new judge, columns = gold)

| new_class \ gold_class | K | N | I | total |
| :-- | --: | --: | --: | --: |
| **K** | 24 | 6 | 3 | 33 |
| **N** | 5 | 11 | 18 | 34 |
| **I** | 10 | 12 | 11 | 33 |
| total | 39 | 29 | 32 | 100 |

## Defect-class matrix (rows = new judge, columns = gold)

| new_defect \ gold_defect | D2 | D1 | D0 | A0_FALSE_POSITIVE | A0_NOT_A_DEFECT_CLAIM | total |
| :-- | --: | --: | --: | --: | --: | --: |
| **D2** | 22 | 10 | 9 | 0 | 0 | 41 |
| **D1** | 5 | 9 | 12 | 0 | 0 | 26 |
| **D0** | 1 | 4 | 8 | 1 | 0 | 14 |
| **A0_FALSE_POSITIVE** | 8 | 9 | 1 | 1 | 0 | 19 |
| **A0_NOT_A_DEFECT_CLAIM** | 0 | 0 | 0 | 0 | 0 | 0 |
| total | 36 | 32 | 30 | 2 | 0 | 100 |

## Per stratum (stratum = frozen judge class -> gold class)

| stratum | n | class agree | defect agree | new class distribution |
| :-- | --: | --: | --: | :-- |
| `I->I` | 7 | 5/7 = 71.4% | 4/7 = 57.1% | I=5, K=1, N=1 |
| `I->K` | 20 | 12/20 = 60.0% | 7/20 = 35.0% | I=7, K=12, N=1 |
| `I->N` | 21 | 5/21 = 23.8% | 9/21 = 42.9% | I=10, K=6, N=5 |
| `K->K` | 15 | 10/15 = 66.7% | 11/15 = 73.3% | I=3, K=10, N=2 |
| `N->I` | 25 | 6/25 = 24.0% | 5/25 = 20.0% | I=6, K=2, N=17 |
| `N->K` | 4 | 2/4 = 50.0% | 2/4 = 50.0% | K=2, N=2 |
| `N->N` | 8 | 6/8 = 75.0% | 2/8 = 25.0% | I=2, N=6 |

## Disagreements by pair

0000=1, 0004=3, 0007=2, 0009=3, 0012=1, 0014=2, 0015=2, 0017=1, 0019=2, 0020=4, 0021=1, 0022=1, 0027=3, 0029=2, 0031=1, 0032=3, 0033=2, 0036=1, 0037=3, 0040=2, 0043=1, 0046=2, 0049=1, 0051=1, 0052=1, 0054=2, 0055=1, 0056=1, 0057=1, 0059=3

