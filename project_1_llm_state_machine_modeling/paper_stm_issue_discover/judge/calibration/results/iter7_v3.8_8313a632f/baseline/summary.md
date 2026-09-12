# Calibration comparison: baseline iter7 v3.8 prompt v12 8313a632f

- run dirs: runs/paper1/judge-calibration-8313a632f-v38/baseline-r1, runs/paper1/judge-calibration-8313a632f-v38/baseline-r2, runs/paper1/judge-calibration-8313a632f-v38/baseline-r3
- subset gold rows: 100; judged and matched: 100; missing: 0; judged outside subset: 0; failed pairs: 0

## Headline

- K/N/I agreement with gold: **56/100 = 56.0%** (frozen v3.2 judge on the same rows: 30/100 = 30.0%)
- defect-class exact agreement: 48/100 = 48.0%
- defect-class disagreements that are only D2<->D1: 11
- valid rate: gold 68/100 = 68.0%; new judge 59/100 = 59.0%; frozen judge 52/100 = 52.0%
- arbitrated reports: 75

## K/N/I matrix (rows = new judge, columns = gold)

| new_class \ gold_class | K | N | I | total |
| :-- | --: | --: | --: | --: |
| **K** | 30 | 5 | 3 | 38 |
| **N** | 6 | 6 | 9 | 21 |
| **I** | 3 | 18 | 20 | 41 |
| total | 39 | 29 | 32 | 100 |

## Defect-class matrix (rows = new judge, columns = gold)

| new_defect \ gold_defect | D2 | D1 | D0 | A0_FALSE_POSITIVE | A0_NOT_A_DEFECT_CLAIM | total |
| :-- | --: | --: | --: | --: | --: | --: |
| **D2** | 25 | 9 | 7 | 1 | 0 | 42 |
| **D1** | 2 | 4 | 4 | 0 | 0 | 10 |
| **D0** | 3 | 16 | 18 | 0 | 0 | 37 |
| **A0_FALSE_POSITIVE** | 6 | 3 | 1 | 1 | 0 | 11 |
| **A0_NOT_A_DEFECT_CLAIM** | 0 | 0 | 0 | 0 | 0 | 0 |
| total | 36 | 32 | 30 | 2 | 0 | 100 |

## Per stratum (stratum = frozen judge class -> gold class)

| stratum | n | class agree | defect agree | new class distribution |
| :-- | --: | --: | --: | :-- |
| `I->I` | 7 | 6/7 = 85.7% | 5/7 = 71.4% | I=6, K=1 |
| `I->K` | 20 | 18/20 = 90.0% | 10/20 = 50.0% | I=1, K=18, N=1 |
| `I->N` | 21 | 2/21 = 9.5% | 4/21 = 19.0% | I=14, K=5, N=2 |
| `K->K` | 15 | 11/15 = 73.3% | 11/15 = 73.3% | I=2, K=11, N=2 |
| `N->I` | 25 | 14/25 = 56.0% | 14/25 = 56.0% | I=14, K=2, N=9 |
| `N->K` | 4 | 1/4 = 25.0% | 2/4 = 50.0% | K=1, N=3 |
| `N->N` | 8 | 4/8 = 50.0% | 2/8 = 25.0% | I=4, N=4 |

## Disagreements by pair

0004=3, 0007=2, 0009=3, 0012=2, 0014=1, 0015=2, 0017=1, 0019=2, 0020=3, 0022=2, 0023=1, 0024=1, 0027=3, 0029=2, 0031=1, 0032=2, 0033=2, 0036=1, 0037=2, 0039=1, 0040=1, 0043=1, 0046=1, 0049=1, 0055=1, 0057=1, 0059=1

