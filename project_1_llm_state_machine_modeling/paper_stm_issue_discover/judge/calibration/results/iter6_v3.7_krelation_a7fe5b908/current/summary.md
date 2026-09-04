# Calibration comparison: current iter6 v3.7 relation-first a7fe5b908

- run dirs: runs/paper1/judge-calibration-a7fe5b908-krelation/current-r1, runs/paper1/judge-calibration-a7fe5b908-krelation/current-r2, runs/paper1/judge-calibration-a7fe5b908-krelation/current-r3
- subset gold rows: 201; judged and matched: 200; missing: 1; judged outside subset: 0; failed pairs: 1

missing: 0047:r3:issue:5

failures: runs/paper1/judge-calibration-a7fe5b908-krelation/current-r3:0047

## Headline

- K/N/I agreement with gold: **136/200 = 68.0%** (frozen v3.2 judge on the same rows: 53/200 = 26.5%)
- defect-class exact agreement: 93/200 = 46.5%
- defect-class disagreements that are only D2<->D1: 19
- valid rate: gold 76/200 = 38.0%; new judge 116/200 = 58.0%; frozen judge 168/200 = 84.0%
- arbitrated reports: 193

## K/N/I matrix (rows = new judge, columns = gold)

| new_class \ gold_class | K | N | I | total |
| :-- | --: | --: | --: | --: |
| **K** | 41 | 1 | 12 | 54 |
| **N** | 7 | 19 | 36 | 62 |
| **I** | 4 | 4 | 76 | 84 |
| total | 52 | 24 | 124 | 200 |

## Defect-class matrix (rows = new judge, columns = gold)

| new_defect \ gold_defect | D2 | D1 | D0 | A0_FALSE_POSITIVE | A0_NOT_A_DEFECT_CLAIM | total |
| :-- | --: | --: | --: | --: | --: | --: |
| **D2** | 23 | 15 | 15 | 0 | 2 | 55 |
| **D1** | 4 | 22 | 17 | 0 | 11 | 54 |
| **D0** | 4 | 5 | 27 | 1 | 12 | 49 |
| **A0_FALSE_POSITIVE** | 3 | 0 | 3 | 5 | 14 | 25 |
| **A0_NOT_A_DEFECT_CLAIM** | 0 | 0 | 0 | 1 | 16 | 17 |
| total | 34 | 42 | 62 | 7 | 55 | 200 |

## Per stratum (stratum = frozen judge class -> gold class)

| stratum | n | class agree | defect agree | new class distribution |
| :-- | --: | --: | --: | :-- |
| `I->I` | 12 | 10/12 = 83.3% | 7/12 = 58.3% | I=10, K=2 |
| `I->K` | 8 | 7/8 = 87.5% | 4/8 = 50.0% | I=1, K=7 |
| `I->N` | 12 | 9/12 = 75.0% | 9/12 = 75.0% | I=3, N=9 |
| `K->I` | 1 | 1/1 = 100.0% | 0/1 = 0.0% | I=1 |
| `K->K/D1` | 8 | 7/8 = 87.5% | 2/8 = 25.0% | K=7, N=1 |
| `K->K/D2` | 21 | 18/21 = 85.7% | 13/21 = 61.9% | I=2, K=18, N=1 |
| `N->I/A0_FALSE_POSITIVE` | 1 | 1/1 = 100.0% | 1/1 = 100.0% | I=1 |
| `N->I/A0_NOT_A_DEFECT_CLAIM` | 50 | 35/50 = 70.0% | 13/50 = 26.0% | I=35, K=2, N=13 |
| `N->I/D0` | 60 | 29/60 = 48.3% | 27/60 = 45.0% | I=29, K=8, N=23 |
| `N->K` | 15 | 9/15 = 60.0% | 8/15 = 53.3% | I=1, K=9, N=5 |
| `N->N` | 12 | 10/12 = 83.3% | 9/12 = 75.0% | I=1, K=1, N=10 |

## Disagreements by pair

0003=2, 0005=4, 0009=1, 0010=1, 0012=2, 0014=3, 0016=3, 0020=2, 0022=1, 0029=1, 0032=3, 0033=2, 0034=2, 0036=3, 0037=1, 0039=1, 0040=2, 0044=2, 0045=2, 0046=1, 0049=7, 0050=1, 0052=2, 0053=3, 0054=1, 0055=3, 0056=2, 0057=3, 0059=3

