# Calibration comparison: baseline iter6 v3.7 relation-first a7fe5b908

- run dirs: runs/paper1/judge-calibration-a7fe5b908-krelation/baseline-r1, runs/paper1/judge-calibration-a7fe5b908-krelation/baseline-r2, runs/paper1/judge-calibration-a7fe5b908-krelation/baseline-r3
- subset gold rows: 100; judged and matched: 100; missing: 0; judged outside subset: 0; failed pairs: 0

## Headline

- K/N/I agreement with gold: **58/100 = 58.0%** (frozen v3.2 judge on the same rows: 30/100 = 30.0%)
- defect-class exact agreement: 45/100 = 45.0%
- defect-class disagreements that are only D2<->D1: 18
- valid rate: gold 68/100 = 68.0%; new judge 72/100 = 72.0%; frozen judge 52/100 = 52.0%
- arbitrated reports: 69

## K/N/I matrix (rows = new judge, columns = gold)

| new_class \ gold_class | K | N | I | total |
| :-- | --: | --: | --: | --: |
| **K** | 32 | 6 | 2 | 40 |
| **N** | 4 | 12 | 16 | 32 |
| **I** | 3 | 11 | 14 | 28 |
| total | 39 | 29 | 32 | 100 |

## Defect-class matrix (rows = new judge, columns = gold)

| new_defect \ gold_defect | D2 | D1 | D0 | A0_FALSE_POSITIVE | A0_NOT_A_DEFECT_CLAIM | total |
| :-- | --: | --: | --: | --: | --: | --: |
| **D2** | 22 | 10 | 9 | 0 | 0 | 41 |
| **D1** | 8 | 11 | 8 | 1 | 0 | 28 |
| **D0** | 1 | 8 | 11 | 0 | 0 | 20 |
| **A0_FALSE_POSITIVE** | 5 | 3 | 2 | 1 | 0 | 11 |
| **A0_NOT_A_DEFECT_CLAIM** | 0 | 0 | 0 | 0 | 0 | 0 |
| total | 36 | 32 | 30 | 2 | 0 | 100 |

## Per stratum (stratum = frozen judge class -> gold class)

| stratum | n | class agree | defect agree | new class distribution |
| :-- | --: | --: | --: | :-- |
| `I->I` | 7 | 5/7 = 71.4% | 3/7 = 42.9% | I=5, K=1, N=1 |
| `I->K` | 20 | 18/20 = 90.0% | 10/20 = 50.0% | I=1, K=18, N=1 |
| `I->N` | 21 | 6/21 = 28.6% | 8/21 = 38.1% | I=9, K=6, N=6 |
| `K->K` | 15 | 13/15 = 86.7% | 10/15 = 66.7% | I=2, K=13 |
| `N->I` | 25 | 9/25 = 36.0% | 9/25 = 36.0% | I=9, K=1, N=15 |
| `N->K` | 4 | 1/4 = 25.0% | 2/4 = 50.0% | K=1, N=3 |
| `N->N` | 8 | 6/8 = 75.0% | 3/8 = 37.5% | I=2, N=6 |

## Disagreements by pair

0004=1, 0007=2, 0009=3, 0012=1, 0014=2, 0015=2, 0019=2, 0020=2, 0022=1, 0023=1, 0024=1, 0027=3, 0029=2, 0031=1, 0032=2, 0033=2, 0036=2, 0037=2, 0039=1, 0040=1, 0043=1, 0046=2, 0052=1, 0054=1, 0055=1, 0056=1, 0059=1

