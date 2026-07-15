# Gold Card v2 — Noised Fluency Test, CNN-DailyMail
## Metric: BARTScore-avg-f (single-metric card)

> **Annotator instructions.** Do not open `sum_mt/reports/noised_fluency/evaluation/Noised_Fluency_SUM.pdf` while filling this in. Use only the score tables below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** Log-likelihood; higher (closer to 0) = better. Reference values are negative.

**Task:** summarization
**Dataset:** CNN-DailyMail, 100 reference summaries (~3 sentences each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Test results:**

**Reference (gold) score:** -6.0636


#### Verb lemmatization (`flu-lemmatizeverb`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | -6.1397 | 0.052 | -1.26% |
| 100% | -6.2170 | 0.102 | -2.53% |

#### Random word drop (`flu-randomworddrop`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | -6.1591 | 0.061 | -1.57% |
| 10% | -6.2514 | 0.111 | -3.10% |
| 15% | -6.3393 | 0.163 | -4.55% |
| 20% | -6.4725 | 0.210 | -6.74% |
| 25% | -6.5831 | 0.260 | -8.57% |
| 30% | -6.7340 | 0.311 | -11.06% |
| 35% | -6.9000 | 0.361 | -13.79% |
| 40% | -7.1025 | 0.408 | -17.13% |
| 45% | -7.3047 | 0.461 | -20.47% |
| 50% | -7.5072 | 0.507 | -23.81% |

#### Punctuation noise (`flu-noisepunct`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | -6.1560 | 0.052 | -1.52% |
| 100% | -6.2633 | 0.105 | -3.29% |

#### Sentence-middle swap (`flu-sentencemiddleswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 1 sentence(s) swapped | -6.2111 | 0.145 | -2.43% |
| 2 sentence(s) swapped | -6.3653 | 0.255 | -4.97% |
| 3 sentence(s) swapped | -6.4977 | 0.321 | -7.16% |

#### Preposition removal (`flu-removepreposition`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 40% | -6.1745 | 0.054 | -1.83% |
| 70% | -6.2776 | 0.093 | -3.53% |
| 100% | -6.3932 | 0.135 | -5.44% |

#### Stop-word removal (`flu-removestopwords`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | -6.1210 | 0.044 | -0.95% |
| 20% | -6.1776 | 0.088 | -1.88% |
| 30% | -6.2515 | 0.130 | -3.10% |
| 40% | -6.3435 | 0.175 | -4.62% |
| 50% | -6.4407 | 0.219 | -6.22% |
| 60% | -6.5544 | 0.263 | -8.09% |

#### Local word swap (`flu-randomlocalswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | -6.3061 | 0.056 | -4.00% |
| 15% | -6.5639 | 0.117 | -8.25% |
| 30% | -6.7892 | 0.169 | -11.97% |
| 60% | -7.0103 | 0.222 | -15.61% |

#### Truncate (remove suffix) (`flu-truncate`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | -5.9843 | 0.114 | +1.31% |
| 20% | -5.9528 | 0.215 | +1.83% |
| 30% | -6.0093 | 0.312 | +0.90% |
| 40% | -6.1890 | 0.413 | -2.07% |
| 50% | -6.5007 | 0.515 | -7.21% |

#### Article removal (`flu-removearticle`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | -6.1174 | 0.039 | -0.89% |
| 100% | -6.1975 | 0.081 | -2.21% |

#### Random token repetition (`flu-randomtokenrep`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | -6.1719 | 0.061 | -1.79% |
| 10% | -6.2606 | 0.111 | -3.25% |
| 15% | -6.3589 | 0.163 | -4.87% |
| 20% | -6.4396 | 0.210 | -6.20% |
| 25% | -6.5301 | 0.260 | -7.69% |
| 30% | -6.6195 | 0.311 | -9.17% |
| 35% | -6.7143 | 0.361 | -10.73% |
| 40% | -6.7851 | 0.408 | -11.90% |
| 45% | -6.8614 | 0.461 | -13.16% |
| 50% | -6.9329 | 0.507 | -14.34% |

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
| Random word drop (`flu-randomworddrop`) | Yes                 | No                   | low         |
| Punctuation noise (`flu-noisepunct`) | Yes                 | Yes                  | low         |
| Sentence-middle swap (`flu-sentencemiddleswap`) | Yes                 | No                   | low         |
| Preposition removal (`flu-removepreposition`) | Yes                 | Yes                  | low         |
| Stop-word removal (`flu-removestopwords`) | Yes                 | No                   | low         |
| Local word swap (`flu-randomlocalswap`) | Yes                 | No                   | low         |
| Truncate (remove suffix) (`flu-truncate`) | No                  | No                   | low         |
| Article removal (`flu-removearticle`) | Yes                 | Yes                  | low         |
| Random token repetition (`flu-randomtokenrep`) | Yes                 | No                   | low         |

### 2. Recommendation

Yes iff *more than 7* of the 10 noise types have **both** a high change rate **and** a superlinear decrease, else No.

_Your answer (Yes/No):_ No
