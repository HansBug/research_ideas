# Calibration comparison: baseline iter9 v3.10 prompt v14 5de564dad

- run dirs: runs/paper1/judge-calibration-5de564dad-v310/baseline-r1, runs/paper1/judge-calibration-5de564dad-v310/baseline-r1-resume175628, runs/paper1/judge-calibration-5de564dad-v310/baseline-r2, runs/paper1/judge-calibration-5de564dad-v310/baseline-r3
- subset gold rows: 100; judged and matched: 100; missing: 0; judged outside subset: 0; failed pairs: 1

failures: runs/paper1/judge-calibration-5de564dad-v310/baseline-r1:0016

## Headline

- K/N/I agreement with gold: **58/100 = 58.0%** (frozen v3.2 judge on the same rows: 30/100 = 30.0%)
- defect-class exact agreement: 55/100 = 55.0%
- defect-class disagreements that are only D2<->D1: 16
- valid rate: gold 68/100 = 68.0%; new judge 82/100 = 82.0%; frozen judge 52/100 = 52.0%
- arbitrated reports: 31

## K/N/I matrix (rows = new judge, columns = gold)

| new_class \ gold_class | K | N | I | total |
| :-- | --: | --: | --: | --: |
| **K** | 37 | 13 | 8 | 58 |
| **N** | 1 | 10 | 13 | 24 |
| **I** | 1 | 6 | 11 | 18 |
| total | 39 | 29 | 32 | 100 |

## Defect-class matrix (rows = new judge, columns = gold)

| new_defect \ gold_defect | D2 | D1 | D0 | A0_FALSE_POSITIVE | A0_NOT_A_DEFECT_CLAIM | total |
| :-- | --: | --: | --: | --: | --: | --: |
| **D2** | 29 | 11 | 11 | 0 | 0 | 51 |
| **D1** | 5 | 15 | 9 | 1 | 0 | 30 |
| **D0** | 1 | 5 | 10 | 0 | 0 | 16 |
| **A0_FALSE_POSITIVE** | 1 | 1 | 0 | 1 | 0 | 3 |
| **A0_NOT_A_DEFECT_CLAIM** | 0 | 0 | 0 | 0 | 0 | 0 |
| total | 36 | 32 | 30 | 2 | 0 | 100 |

## Per stratum (stratum = frozen judge class -> gold class)

| stratum | n | class agree | defect agree | new class distribution |
| :-- | --: | --: | --: | :-- |
| `I->I` | 7 | 4/7 = 57.1% | 4/7 = 57.1% | I=4, K=2, N=1 |
| `I->K` | 20 | 20/20 = 100.0% | 13/20 = 65.0% | K=20 |
| `I->N` | 21 | 4/21 = 19.0% | 12/21 = 57.1% | I=5, K=12, N=4 |
| `K->K` | 15 | 14/15 = 93.3% | 13/15 = 86.7% | I=1, K=14 |
| `N->I` | 25 | 7/25 = 28.0% | 7/25 = 28.0% | I=7, K=6, N=12 |
| `N->K` | 4 | 3/4 = 75.0% | 2/4 = 50.0% | K=3, N=1 |
| `N->N` | 8 | 6/8 = 75.0% | 4/8 = 50.0% | I=1, K=1, N=6 |

## Disagreements by pair

0004=2, 0007=1, 0009=2, 0012=1, 0014=1, 0019=3, 0020=3, 0022=1, 0023=1, 0024=1, 0027=2, 0029=2, 0031=1, 0032=2, 0033=2, 0035=1, 0036=1, 0037=1, 0039=1, 0040=1, 0043=1, 0046=2, 0049=1, 0051=1, 0052=1, 0054=1, 0055=1, 0056=1, 0059=3

