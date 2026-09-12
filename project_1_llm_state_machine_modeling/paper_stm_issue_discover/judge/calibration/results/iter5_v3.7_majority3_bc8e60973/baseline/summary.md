# Calibration comparison: baseline iter5 v3.7 majority-of-3 (bc8e60973)

- run dirs: runs/paper1/judge-calibration-bc8e60973-majority3/baseline-r1, runs/paper1/judge-calibration-bc8e60973-majority3/baseline-r2, runs/paper1/judge-calibration-bc8e60973-majority3/baseline-r3
- subset gold rows: 100; judged and matched: 99; missing: 1; judged outside subset: 0; failed pairs: 1

missing: 0053:r2:baseline_issue_3

failures: runs/paper1/judge-calibration-bc8e60973-majority3/baseline-r2:0053

## Headline

- K/N/I agreement with gold: **57/99 = 57.6%** (frozen v3.2 judge on the same rows: 30/99 = 30.3%)
- defect-class exact agreement: 53/99 = 53.5%
- defect-class disagreements that are only D2<->D1: 13
- valid rate: gold 67/99 = 67.7%; new judge 74/99 = 74.7%; frozen judge 52/99 = 52.5%
- arbitrated reports: 4

## K/N/I matrix (rows = new judge, columns = gold)

| new_class \ gold_class | K | N | I | total |
| :-- | --: | --: | --: | --: |
| **K** | 29 | 4 | 2 | 35 |
| **N** | 5 | 16 | 18 | 39 |
| **I** | 4 | 9 | 12 | 25 |
| total | 38 | 29 | 32 | 99 |

## Defect-class matrix (rows = new judge, columns = gold)

| new_defect \ gold_defect | D2 | D1 | D0 | A0_FALSE_POSITIVE | A0_NOT_A_DEFECT_CLAIM | total |
| :-- | --: | --: | --: | --: | --: | --: |
| **D2** | 25 | 10 | 11 | 1 | 0 | 47 |
| **D1** | 3 | 16 | 8 | 0 | 0 | 27 |
| **D0** | 3 | 4 | 11 | 0 | 0 | 18 |
| **A0_FALSE_POSITIVE** | 4 | 2 | 0 | 1 | 0 | 7 |
| **A0_NOT_A_DEFECT_CLAIM** | 0 | 0 | 0 | 0 | 0 | 0 |
| total | 35 | 32 | 30 | 2 | 0 | 99 |

## Per stratum (stratum = frozen judge class -> gold class)

| stratum | n | class agree | defect agree | new class distribution |
| :-- | --: | --: | --: | :-- |
| `I->I` | 7 | 3/7 = 42.9% | 3/7 = 42.9% | I=3, K=1, N=3 |
| `I->K` | 19 | 16/19 = 84.2% | 13/19 = 68.4% | I=2, K=16, N=1 |
| `I->N` | 21 | 9/21 = 42.9% | 11/21 = 52.4% | I=8, K=4, N=9 |
| `K->K` | 15 | 11/15 = 73.3% | 12/15 = 80.0% | I=2, K=11, N=2 |
| `N->I` | 25 | 9/25 = 36.0% | 9/25 = 36.0% | I=9, K=1, N=15 |
| `N->K` | 4 | 2/4 = 50.0% | 2/4 = 50.0% | K=2, N=2 |
| `N->N` | 8 | 7/8 = 87.5% | 3/8 = 37.5% | I=1, N=7 |

## Disagreements by pair

0004=2, 0007=2, 0009=3, 0012=1, 0014=2, 0015=2, 0017=1, 0019=2, 0020=3, 0022=1, 0024=1, 0027=2, 0031=1, 0032=2, 0033=2, 0035=1, 0036=1, 0037=3, 0039=1, 0043=1, 0046=1, 0051=1, 0054=1, 0055=1, 0056=1, 0057=1, 0059=2

