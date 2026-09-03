| run / side | K | N | I | report precision | hit@1 (rough) |
| :-- | --: | --: | --: | --: | --: |
| gold / current | 749 | 231 | 291 | 77.1% | 71.3% |
| gold / baseline | 312 | 105 | 95 | 81.4% | 52.2% |
| iter6 / current | 689 | 303 | 279 | 78.0% | 65.5% |
| iter6 / baseline | 288 | 108 | 116 | 77.3% | 48.2% |
| iter7 / current | 535 | 139 | 597 | 53.0% | 50.9% |
| iter7 / baseline | 252 | 101 | 159 | 68.9% | 42.1% |
| iter8A / current | 630 | 90 | 551 | 56.7% | 60.0% |
| iter8A / baseline | 306 | 83 | 123 | 76.0% | 51.2% |
| iter8B / current | 626 | 115 | 530 | 58.3% | 59.6% |
| iter8B / baseline | 295 | 108 | 108 | 78.8% | 49.4% |

| run | Δ hit@1 (ours − baseline) | Δ precision (ours − baseline) |
| :-- | --: | --: |
| gold | +19.1 pp | -4.3 pp |
| iter6 | +17.4 pp | +0.7 pp |
| iter7 | +8.8 pp | -15.9 pp |
| iter8A | +8.8 pp | -19.4 pp |
| iter8B | +10.2 pp | -20.5 pp |

hit@1 is scaled from the human hit@1 by projected K / human K; hit@3 and hit@all need the full-population run.
