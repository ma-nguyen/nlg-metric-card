# Gold Card v2 — Noised Fluency Test, CNN-DailyMail
## Metric: BERTScore-f (single-metric card)

> **Annotator instructions.** Do not open `sum_mt/reports/noised_fluency/evaluation/Noised_Fluency_SUM.pdf` while filling this in. Use only the score tables below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** Score range 0 (worst) to 1 (best).

**Task:** summarization
**Dataset:** CNN-DailyMail, 100 reference summaries (~3 sentences each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Test results:**

**Reference (gold) score:** 0.2236


#### Verb lemmatization (`flu-lemmatizeverb`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.2093 | 0.052 | -6.42% |
| 100% | 0.1966 | 0.102 | -12.08% |

#### Random word drop (`flu-randomworddrop`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.1989 | 0.061 | -11.04% |
| 10% | 0.1822 | 0.111 | -18.55% |
| 15% | 0.1644 | 0.163 | -26.50% |
| 20% | 0.1462 | 0.210 | -34.62% |
| 25% | 0.1309 | 0.260 | -41.47% |
| 30% | 0.1151 | 0.311 | -48.53% |
| 35% | 0.0990 | 0.361 | -55.76% |
| 40% | 0.0824 | 0.408 | -63.15% |
| 45% | 0.0651 | 0.461 | -70.87% |
| 50% | 0.0540 | 0.507 | -75.84% |

#### Punctuation noise (`flu-noisepunct`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.2066 | 0.052 | -7.60% |
| 100% | 0.1872 | 0.105 | -16.30% |

#### Sentence-middle swap (`flu-sentencemiddleswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 1 sentence(s) swapped | 0.1966 | 0.145 | -12.09% |
| 2 sentence(s) swapped | 0.1717 | 0.255 | -23.21% |
| 3 sentence(s) swapped | 0.1520 | 0.321 | -32.04% |

#### Preposition removal (`flu-removepreposition`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 40% | 0.2056 | 0.054 | -8.07% |
| 70% | 0.1925 | 0.093 | -13.91% |
| 100% | 0.1787 | 0.135 | -20.11% |

#### Stop-word removal (`flu-removestopwords`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.2110 | 0.044 | -5.64% |
| 20% | 0.2004 | 0.088 | -10.40% |
| 30% | 0.1905 | 0.130 | -14.82% |
| 40% | 0.1807 | 0.175 | -19.18% |
| 50% | 0.1698 | 0.219 | -24.08% |
| 60% | 0.1595 | 0.263 | -28.69% |

#### Local word swap (`flu-randomlocalswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.1859 | 0.056 | -16.86% |
| 15% | 0.1474 | 0.117 | -34.10% |
| 30% | 0.1100 | 0.169 | -50.82% |
| 60% | 0.0731 | 0.222 | -67.33% |

#### Truncate (remove suffix) (`flu-truncate`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.2243 | 0.114 | +0.29% |
| 20% | 0.2268 | 0.215 | +1.41% |
| 30% | 0.2303 | 0.312 | +2.97% |
| 40% | 0.2311 | 0.413 | +3.34% |
| 50% | 0.2291 | 0.515 | +2.45% |

#### Article removal (`flu-removearticle`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.2151 | 0.039 | -3.81% |
| 100% | 0.2057 | 0.081 | -8.04% |

#### Random token repetition (`flu-randomtokenrep`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.2013 | 0.061 | -9.97% |
| 10% | 0.1834 | 0.111 | -17.99% |
| 15% | 0.1669 | 0.163 | -25.39% |
| 20% | 0.1516 | 0.210 | -32.22% |
| 25% | 0.1357 | 0.260 | -39.30% |
| 30% | 0.1220 | 0.311 | -45.44% |
| 35% | 0.1082 | 0.361 | -51.61% |
| 40% | 0.0957 | 0.408 | -57.20% |
| 45% | 0.0820 | 0.461 | -63.34% |
| 50% | 0.0691 | 0.507 | -69.11% |

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
| Random word drop (`flu-randomworddrop`) | Yes                 | No                   | high        |
| Punctuation noise (`flu-noisepunct`) | Yes                 | Yes                  | low         |
| Sentence-middle swap (`flu-sentencemiddleswap`) | Yes                 | No                   | moderate    |
| Preposition removal (`flu-removepreposition`) | Yes                 | No                   | low         |
| Stop-word removal (`flu-removestopwords`) | Yes                 | No                   | moderate    |
| Local word swap (`flu-randomlocalswap`) | Yes                 | No                   | high        |
| Truncate (remove suffix) (`flu-truncate`) | No                  | No                   | low         |
| Article removal (`flu-removearticle`) | Yes                 | Yes                  | low         |
| Random token repetition (`flu-randomtokenrep`) | Yes                 | Yes                  | high        |

### 2. Recommendation

Yes iff *more than 7* of the 10 noise types have **both** a high change rate **and** a superlinear decrease, else No.

_Your answer (Yes/No):_ No
