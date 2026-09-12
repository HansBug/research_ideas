# Calibration comparison: baseline iter2 v3.5 (8fd87c559)

- run dirs: runs/paper1/judge-calibration-8fd87c559/baseline-r1, runs/paper1/judge-calibration-8fd87c559/baseline-r2, runs/paper1/judge-calibration-8fd87c559/baseline-r3
- subset gold rows: 100; judged and matched: 100; missing: 0; judged outside subset: 0; failed pairs: 0

## Headline

- K/N/I agreement with gold: **56/100 = 56.0%** (frozen v3.2 judge on the same rows: 30/100 = 30.0%)
- defect-class exact agreement: 51/100 = 51.0%
- defect-class disagreements that are only D2<->D1: 12
- valid rate: gold 68/100 = 68.0%; new judge 64/100 = 64.0%; frozen judge 52/100 = 52.0%
- arbitrated reports: 68

## K/N/I matrix (rows = new judge, columns = gold)

| new_class \ gold_class | K | N | I | total |
| :-- | --: | --: | --: | --: |
| **K** | 28 | 4 | 2 | 34 |
| **N** | 4 | 12 | 14 | 30 |
| **I** | 7 | 13 | 16 | 36 |
| total | 39 | 29 | 32 | 100 |

## Defect-class matrix (rows = new judge, columns = gold)

| new_defect \ gold_defect | D2 | D1 | D0 | A0_FALSE_POSITIVE | A0_NOT_A_DEFECT_CLAIM | total |
| :-- | --: | --: | --: | --: | --: | --: |
| **D2** | 23 | 8 | 8 | 0 | 0 | 39 |
| **D1** | 4 | 13 | 7 | 1 | 0 | 25 |
| **D0** | 3 | 7 | 14 | 0 | 0 | 24 |
| **A0_FALSE_POSITIVE** | 6 | 4 | 1 | 1 | 0 | 12 |
| **A0_NOT_A_DEFECT_CLAIM** | 0 | 0 | 0 | 0 | 0 | 0 |
| total | 36 | 32 | 30 | 2 | 0 | 100 |

## Per stratum (stratum = frozen judge class -> gold class)

| stratum | n | class agree | defect agree | new class distribution |
| :-- | --: | --: | --: | :-- |
| `I->I` | 7 | 6/7 = 85.7% | 5/7 = 71.4% | I=6, N=1 |
| `I->K` | 20 | 14/20 = 70.0% | 10/20 = 50.0% | I=5, K=14, N=1 |
| `I->N` | 21 | 5/21 = 23.8% | 7/21 = 33.3% | I=12, K=4, N=5 |
| `K->K` | 15 | 12/15 = 80.0% | 12/15 = 80.0% | I=2, K=12, N=1 |
| `N->I` | 25 | 10/25 = 40.0% | 10/25 = 40.0% | I=10, K=2, N=13 |
| `N->K` | 4 | 2/4 = 50.0% | 2/4 = 50.0% | K=2, N=2 |
| `N->N` | 8 | 7/8 = 87.5% | 5/8 = 62.5% | I=1, N=7 |

## Disagreements by pair

0004=2, 0007=2, 0009=3, 0012=1, 0014=1, 0015=2, 0019=2, 0020=4, 0022=1, 0027=2, 0029=1, 0031=1, 0032=3, 0033=2, 0036=1, 0037=2, 0039=1, 0040=1, 0046=2, 0049=1, 0052=1, 0054=2, 0055=1, 0056=2, 0057=1, 0059=2

