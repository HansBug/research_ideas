# Calibration comparison: current iter4 v3.7 (8d8452a6f)

- run dirs: runs/paper1/judge-calibration-8d8452a6f/current-r1, runs/paper1/judge-calibration-8d8452a6f/current-r2, runs/paper1/judge-calibration-8d8452a6f/current-r3
- subset gold rows: 201; judged and matched: 201; missing: 0; judged outside subset: 0; failed pairs: 0

## Headline

- K/N/I agreement with gold: **130/201 = 64.7%** (frozen v3.2 judge on the same rows: 54/201 = 26.9%)
- defect-class exact agreement: 89/201 = 44.3%
- defect-class disagreements that are only D2<->D1: 18
- valid rate: gold 77/201 = 38.3%; new judge 109/201 = 54.2%; frozen judge 169/201 = 84.1%
- arbitrated reports: 196

## K/N/I matrix (rows = new judge, columns = gold)

| new_class \ gold_class | K | N | I | total |
| :-- | --: | --: | --: | --: |
| **K** | 33 | 1 | 6 | 40 |
| **N** | 12 | 18 | 39 | 69 |
| **I** | 8 | 5 | 79 | 92 |
| total | 53 | 24 | 124 | 201 |

## Defect-class matrix (rows = new judge, columns = gold)

| new_defect \ gold_defect | D2 | D1 | D0 | A0_FALSE_POSITIVE | A0_NOT_A_DEFECT_CLAIM | total |
| :-- | --: | --: | --: | --: | --: | --: |
| **D2** | 23 | 14 | 14 | 0 | 2 | 53 |
| **D1** | 4 | 23 | 22 | 0 | 7 | 56 |
| **D0** | 5 | 5 | 22 | 3 | 6 | 41 |
| **A0_FALSE_POSITIVE** | 3 | 0 | 4 | 3 | 22 | 32 |
| **A0_NOT_A_DEFECT_CLAIM** | 0 | 0 | 0 | 1 | 18 | 19 |
| total | 35 | 42 | 62 | 7 | 55 | 201 |

## Per stratum (stratum = frozen judge class -> gold class)

| stratum | n | class agree | defect agree | new class distribution |
| :-- | --: | --: | --: | :-- |
| `I->I` | 12 | 12/12 = 100.0% | 7/12 = 58.3% | I=12 |
| `I->K` | 8 | 6/8 = 75.0% | 5/8 = 62.5% | I=1, K=6, N=1 |
| `I->N` | 12 | 8/12 = 66.7% | 8/12 = 66.7% | I=4, N=8 |
| `K->I` | 1 | 0/1 = 0.0% | 0/1 = 0.0% | N=1 |
| `K->K/D1` | 8 | 5/8 = 62.5% | 3/8 = 37.5% | K=5, N=3 |
| `K->K/D2` | 22 | 15/22 = 68.2% | 14/22 = 63.6% | I=4, K=15, N=3 |
| `N->I/A0_FALSE_POSITIVE` | 1 | 1/1 = 100.0% | 0/1 = 0.0% | I=1 |
| `N->I/A0_NOT_A_DEFECT_CLAIM` | 50 | 42/50 = 84.0% | 15/50 = 30.0% | I=42, K=1, N=7 |
| `N->I/D0` | 60 | 24/60 = 40.0% | 21/60 = 35.0% | I=24, K=5, N=31 |
| `N->K` | 15 | 7/15 = 46.7% | 8/15 = 53.3% | I=3, K=7, N=5 |
| `N->N` | 12 | 10/12 = 83.3% | 8/12 = 66.7% | I=1, K=1, N=10 |

## Disagreements by pair

0003=3, 0004=2, 0005=4, 0007=1, 0009=1, 0011=1, 0012=2, 0014=2, 0016=3, 0020=2, 0024=4, 0029=1, 0032=3, 0033=3, 0034=2, 0036=2, 0039=1, 0040=3, 0043=4, 0044=2, 0045=2, 0046=1, 0047=2, 0049=6, 0050=1, 0052=1, 0053=3, 0055=3, 0057=2, 0059=4

