# Calibration comparison: baseline iter4 v3.7 (8d8452a6f)

- run dirs: runs/paper1/judge-calibration-8d8452a6f/baseline-r1, runs/paper1/judge-calibration-8d8452a6f/baseline-r2, runs/paper1/judge-calibration-8d8452a6f/baseline-r3
- subset gold rows: 100; judged and matched: 100; missing: 0; judged outside subset: 0; failed pairs: 0

## Headline

- K/N/I agreement with gold: **59/100 = 59.0%** (frozen v3.2 judge on the same rows: 30/100 = 30.0%)
- defect-class exact agreement: 51/100 = 51.0%
- defect-class disagreements that are only D2<->D1: 15
- valid rate: gold 68/100 = 68.0%; new judge 68/100 = 68.0%; frozen judge 52/100 = 52.0%
- arbitrated reports: 65

## K/N/I matrix (rows = new judge, columns = gold)

| new_class \ gold_class | K | N | I | total |
| :-- | --: | --: | --: | --: |
| **K** | 30 | 3 | 3 | 36 |
| **N** | 6 | 13 | 13 | 32 |
| **I** | 3 | 13 | 16 | 32 |
| total | 39 | 29 | 32 | 100 |

## Defect-class matrix (rows = new judge, columns = gold)

| new_defect \ gold_defect | D2 | D1 | D0 | A0_FALSE_POSITIVE | A0_NOT_A_DEFECT_CLAIM | total |
| :-- | --: | --: | --: | --: | --: | --: |
| **D2** | 24 | 10 | 12 | 0 | 0 | 46 |
| **D1** | 5 | 13 | 4 | 0 | 0 | 22 |
| **D0** | 2 | 5 | 13 | 1 | 0 | 21 |
| **A0_FALSE_POSITIVE** | 5 | 4 | 1 | 1 | 0 | 11 |
| **A0_NOT_A_DEFECT_CLAIM** | 0 | 0 | 0 | 0 | 0 | 0 |
| total | 36 | 32 | 30 | 2 | 0 | 100 |

## Per stratum (stratum = frozen judge class -> gold class)

| stratum | n | class agree | defect agree | new class distribution |
| :-- | --: | --: | --: | :-- |
| `I->I` | 7 | 4/7 = 57.1% | 3/7 = 42.9% | I=4, K=2, N=1 |
| `I->K` | 20 | 18/20 = 90.0% | 13/20 = 65.0% | I=1, K=18, N=1 |
| `I->N` | 21 | 8/21 = 38.1% | 8/21 = 38.1% | I=10, K=3, N=8 |
| `K->K` | 15 | 11/15 = 73.3% | 11/15 = 73.3% | I=2, K=11, N=2 |
| `N->I` | 25 | 12/25 = 48.0% | 11/25 = 44.0% | I=12, K=1, N=12 |
| `N->K` | 4 | 1/4 = 25.0% | 3/4 = 75.0% | K=1, N=3 |
| `N->N` | 8 | 5/8 = 62.5% | 2/8 = 25.0% | I=3, N=5 |

## Disagreements by pair

0004=1, 0007=2, 0009=3, 0012=2, 0014=1, 0015=2, 0019=2, 0020=2, 0022=1, 0023=1, 0024=1, 0027=3, 0029=3, 0031=1, 0032=2, 0033=1, 0035=1, 0036=1, 0037=3, 0040=1, 0043=1, 0046=2, 0054=1, 0055=1, 0057=1, 0059=1

