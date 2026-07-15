# Gold Card v2 — Noised Fluency Test, CNN-DailyMail
## Metric: ROUGE-2 (single-metric card)

> **Annotator instructions.** Do not open `sum_mt/reports/noised_fluency/evaluation/Noised_Fluency_SUM.pdf` while filling this in. Use only the score tables below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** Score range 0 (worst) to 1 (best).

**Task:** summarization
**Dataset:** CNN-DailyMail, 100 reference summaries (~3 sentences each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Test results:**

**Reference (gold) score:** 0.1711


#### Verb lemmatization (`flu-lemmatizeverb`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.1692 | 0.052 | -1.17% |
| 100% | 0.1680 | 0.102 | -1.83% |

#### Random word drop (`flu-randomworddrop`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.1603 | 0.061 | -6.32% |
| 10% | 0.1530 | 0.111 | -10.63% |
| 15% | 0.1432 | 0.163 | -16.35% |
| 20% | 0.1381 | 0.210 | -19.34% |
| 25% | 0.1280 | 0.260 | -25.22% |
| 30% | 0.1176 | 0.311 | -31.26% |
| 35% | 0.1104 | 0.361 | -35.48% |
| 40% | 0.1009 | 0.408 | -41.06% |
| 45% | 0.0922 | 0.461 | -46.14% |
| 50% | 0.0862 | 0.507 | -49.63% |

#### Punctuation noise (`flu-noisepunct`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.1711 | 0.052 | +0.00% |
| 100% | 0.1711 | 0.105 | +0.00% |

#### Sentence-middle swap (`flu-sentencemiddleswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 1 sentence(s) swapped | 0.1673 | 0.145 | -2.22% |
| 2 sentence(s) swapped | 0.1624 | 0.255 | -5.14% |
| 3 sentence(s) swapped | 0.1590 | 0.321 | -7.08% |

#### Preposition removal (`flu-removepreposition`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 40% | 0.1635 | 0.054 | -4.49% |
| 70% | 0.1574 | 0.093 | -8.04% |
| 100% | 0.1499 | 0.135 | -12.39% |

#### Stop-word removal (`flu-removestopwords`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.1645 | 0.044 | -3.91% |
| 20% | 0.1585 | 0.088 | -7.41% |
| 30% | 0.1533 | 0.130 | -10.44% |
| 40% | 0.1454 | 0.175 | -15.05% |
| 50% | 0.1393 | 0.219 | -18.63% |
| 60% | 0.1341 | 0.263 | -21.62% |

#### Local word swap (`flu-randomlocalswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.1516 | 0.056 | -11.44% |
| 15% | 0.1262 | 0.117 | -26.23% |
| 30% | 0.1045 | 0.169 | -38.91% |
| 60% | 0.0871 | 0.222 | -49.08% |

#### Truncate (remove suffix) (`flu-truncate`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.1700 | 0.114 | -0.66% |
| 20% | 0.1712 | 0.215 | +0.04% |
| 30% | 0.1731 | 0.312 | +1.16% |
| 40% | 0.1717 | 0.413 | +0.31% |
| 50% | 0.1726 | 0.515 | +0.84% |

#### Article removal (`flu-removearticle`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.1600 | 0.039 | -6.53% |
| 100% | 0.1508 | 0.081 | -11.88% |

#### Random token repetition (`flu-randomtokenrep`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.1658 | 0.061 | -3.11% |
| 10% | 0.1616 | 0.111 | -5.55% |
| 15% | 0.1576 | 0.163 | -7.92% |
| 20% | 0.1540 | 0.210 | -10.03% |
| 25% | 0.1504 | 0.260 | -12.11% |
| 30% | 0.1469 | 0.311 | -14.19% |
| 35% | 0.1438 | 0.361 | -16.00% |
| 40% | 0.1409 | 0.408 | -17.67% |
| 45% | 0.1377 | 0.461 | -19.57% |
| 50% | 0.1351 | 0.507 | -21.06% |

---

## Your annotations

### 1. Sensitivity to the Perturbation

For each noise type, fill in three cells. Categorise the **change rate** by the *largest* `|Δ%|` observed across all variation levels for that noise type:

- `low`      iff `max(|Δ%|) ≤ 25`
- `moderate` iff `max(|Δ%|) ≤ 60`
- `high`     otherwise (especially when `≈ 100`)

`monotonous decrease` = score moves in the expected direction at every step as variation increases. `superlinear decrease` = the per-step `|Δ|` *grows* as variation grows. (Note: for `GPT2-base-PPL` higher = worse, so the expected direction is `score increases`. Apply the same definitions accordingly: monotonous = monotonous in the *correct* direction; the change-rate categories use `|Δ%|` and so don't need a sign flip.)

| Noise type | Monotonous decrease | Superlinear decrease | Change rate |
|---|---------------------|----------------------|-------------|
| Verb lemmatization (`flu-lemmatizeverb`) | Yes                 | No                   | low         |
| Random word drop (`flu-randomworddrop`) | Yes                 | No                   | moderate    |
| Punctuation noise (`flu-noisepunct`) | No                  | No                   | low         |
| Sentence-middle swap (`flu-sentencemiddleswap`) | Yes                 | No                   | low         |
| Preposition removal (`flu-removepreposition`) | Yes                 | No                   | low         |
| Stop-word removal (`flu-removestopwords`) | Yes                 | No                   | low         |
| Local word swap (`flu-randomlocalswap`) | Yes                 | No                   | moderate    |
| Truncate (remove suffix) (`flu-truncate`) | No                  | No                   | low         |
| Article removal (`flu-removearticle`) | Yes                 | Yes                  | low         |
| Random token repetition (`flu-randomtokenrep`) | Yes                 | No                   | low         |

### 2. Recommendation

Yes iff *more than 7* of the 10 noise types have **both** a high change rate **and** a superlinear decrease, else No.

_Your answer (Yes/No):_ No
