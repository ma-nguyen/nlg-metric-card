# Gold Card v2 — Noised Fluency Test, CNN-DailyMail
## Metric: UniEval-Consistency (single-metric card)

> **Annotator instructions.** Do not open `sum_mt/reports/noised_fluency/evaluation/Noised_Fluency_SUM.pdf` while filling this in. Use only the score tables below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** Score range 0 (worst) to 1 (best).

**Task:** summarization
**Dataset:** CNN-DailyMail, 100 reference summaries (~3 sentences each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Test results:**

**Reference (gold) score:** 0.8599


#### Verb lemmatization (`flu-lemmatizeverb`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.8421 | 0.052 | -2.07% |
| 100% | 0.8232 | 0.102 | -4.26% |

#### Random word drop (`flu-randomworddrop`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.7639 | 0.061 | -11.16% |
| 10% | 0.6994 | 0.111 | -18.66% |
| 15% | 0.6483 | 0.163 | -24.60% |
| 20% | 0.5708 | 0.210 | -33.61% |
| 25% | 0.5313 | 0.260 | -38.22% |
| 30% | 0.4713 | 0.311 | -45.19% |
| 35% | 0.4237 | 0.361 | -50.72% |
| 40% | 0.3754 | 0.408 | -56.34% |
| 45% | 0.3486 | 0.461 | -59.45% |
| 50% | 0.3221 | 0.507 | -62.54% |

#### Punctuation noise (`flu-noisepunct`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.7982 | 0.052 | -7.17% |
| 100% | 0.7462 | 0.105 | -13.22% |

#### Sentence-middle swap (`flu-sentencemiddleswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 1 sentence(s) swapped | 0.7617 | 0.145 | -11.41% |
| 2 sentence(s) swapped | 0.6650 | 0.255 | -22.67% |
| 3 sentence(s) swapped | 0.5920 | 0.321 | -31.16% |

#### Preposition removal (`flu-removepreposition`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 40% | 0.8021 | 0.054 | -6.72% |
| 70% | 0.7632 | 0.093 | -11.24% |
| 100% | 0.7280 | 0.135 | -15.33% |

#### Stop-word removal (`flu-removestopwords`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.8335 | 0.044 | -3.06% |
| 20% | 0.8060 | 0.088 | -6.27% |
| 30% | 0.7831 | 0.130 | -8.93% |
| 40% | 0.7557 | 0.175 | -12.12% |
| 50% | 0.7323 | 0.219 | -14.84% |
| 60% | 0.7091 | 0.263 | -17.53% |

#### Local word swap (`flu-randomlocalswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.7312 | 0.056 | -14.96% |
| 15% | 0.6257 | 0.117 | -27.24% |
| 30% | 0.5360 | 0.169 | -37.66% |
| 60% | 0.4500 | 0.222 | -47.67% |

#### Truncate (remove suffix) (`flu-truncate`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.8106 | 0.114 | -5.73% |
| 20% | 0.8112 | 0.215 | -5.66% |
| 30% | 0.8059 | 0.312 | -6.28% |
| 40% | 0.7895 | 0.413 | -8.19% |
| 50% | 0.8121 | 0.515 | -5.56% |

#### Article removal (`flu-removearticle`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.8572 | 0.039 | -0.31% |
| 100% | 0.8537 | 0.081 | -0.72% |

#### Random token repetition (`flu-randomtokenrep`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.7962 | 0.061 | -7.40% |
| 10% | 0.7605 | 0.111 | -11.56% |
| 15% | 0.7206 | 0.163 | -16.20% |
| 20% | 0.7042 | 0.210 | -18.10% |
| 25% | 0.6807 | 0.260 | -20.83% |
| 30% | 0.6645 | 0.311 | -22.73% |
| 35% | 0.6462 | 0.361 | -24.85% |
| 40% | 0.6429 | 0.408 | -25.23% |
| 45% | 0.6271 | 0.461 | -27.07% |
| 50% | 0.6177 | 0.507 | -28.16% |

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
| Verb lemmatization (`flu-lemmatizeverb`) | Yes                 | Yes                  | low         |
| Random word drop (`flu-randomworddrop`) | Yes                 | No                   | high        |
| Punctuation noise (`flu-noisepunct`) | Yes                 | No                   | low         |
| Sentence-middle swap (`flu-sentencemiddleswap`) | Yes                 | No                   | moderate    |
| Preposition removal (`flu-removepreposition`) | Yes                 | No                   | low         |
| Stop-word removal (`flu-removestopwords`) | Yes                 | No                   | low         |
| Local word swap (`flu-randomlocalswap`) | Yes                 | No                   | moderate    |
| Truncate (remove suffix) (`flu-truncate`) | No                  | No                   | low         |
| Article removal (`flu-removearticle`) | Yes                 | Yes                  | low         |
| Random token repetition (`flu-randomtokenrep`) | Yes                 | No                   | moderate    |

### 2. Recommendation

Yes iff *more than 7* of the 10 noise types have **both** a high change rate **and** a superlinear decrease, else No.

_Your answer (Yes/No):_ No
