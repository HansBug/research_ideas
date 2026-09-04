# Calibration comparison: baseline iter3 v3.6 (e5d5485be)

- run dirs: runs/paper1/judge-calibration-e5d5485be/baseline-r1, runs/paper1/judge-calibration-e5d5485be/baseline-r2, runs/paper1/judge-calibration-e5d5485be/baseline-r3
- subset gold rows: 100; judged and matched: 100; missing: 0; judged outside subset: 0; failed pairs: 0

## Headline

- K/N/I agreement with gold: **58/100 = 58.0%** (frozen v3.2 judge on the same rows: 30/100 = 30.0%)
- defect-class exact agreement: 49/100 = 49.0%
- defect-class disagreements that are only D2<->D1: 17
- valid rate: gold 68/100 = 68.0%; new judge 71/100 = 71.0%; frozen judge 52/100 = 52.0%
- arbitrated reports: 63

## K/N/I matrix (rows = new judge, columns = gold)

| new_class \ gold_class | K | N | I | total |
| :-- | --: | --: | --: | --: |
| **K** | 28 | 6 | 5 | 39 |
| **N** | 5 | 15 | 12 | 32 |
| **I** | 6 | 8 | 15 | 29 |
| total | 39 | 29 | 32 | 100 |

## Defect-class matrix (rows = new judge, columns = gold)

| new_defect \ gold_defect | D2 | D1 | D0 | A0_FALSE_POSITIVE | A0_NOT_A_DEFECT_CLAIM | total |
| :-- | --: | --: | --: | --: | --: | --: |
| **D2** | 25 | 11 | 10 | 1 | 0 | 47 |
| **D1** | 6 | 12 | 6 | 0 | 0 | 24 |
| **D0** | 1 | 6 | 11 | 0 | 0 | 18 |
| **A0_FALSE_POSITIVE** | 4 | 3 | 3 | 1 | 0 | 11 |
| **A0_NOT_A_DEFECT_CLAIM** | 0 | 0 | 0 | 0 | 0 | 0 |
| total | 36 | 32 | 30 | 2 | 0 | 100 |

## Per stratum (stratum = frozen judge class -> gold class)

| stratum | n | class agree | defect agree | new class distribution |
| :-- | --: | --: | --: | :-- |
| `I->I` | 7 | 6/7 = 85.7% | 4/7 = 57.1% | I=6, K=1 |
| `I->K` | 20 | 15/20 = 75.0% | 10/20 = 50.0% | I=4, K=15, N=1 |
| `I->N` | 21 | 8/21 = 38.1% | 10/21 = 47.6% | I=7, K=6, N=8 |
| `K->K` | 15 | 11/15 = 73.3% | 12/15 = 80.0% | I=2, K=11, N=2 |
| `N->I` | 25 | 9/25 = 36.0% | 8/25 = 32.0% | I=9, K=4, N=12 |
| `N->K` | 4 | 2/4 = 50.0% | 2/4 = 50.0% | K=2, N=2 |
| `N->N` | 8 | 7/8 = 87.5% | 3/8 = 37.5% | I=1, N=7 |

## Disagreements by pair

0000=1, 0004=3, 0007=2, 0009=3, 0012=1, 0014=1, 0015=2, 0019=2, 0020=3, 0022=1, 0024=1, 0027=2, 0029=2, 0031=1, 0032=2, 0033=1, 0036=1, 0037=3, 0039=1, 0043=1, 0046=2, 0049=1, 0054=1, 0055=1, 0056=1, 0057=1, 0059=1

