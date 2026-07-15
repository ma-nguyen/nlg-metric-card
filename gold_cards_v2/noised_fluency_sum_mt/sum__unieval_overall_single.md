# Gold Card v2 — Noised Fluency Test, CNN-DailyMail
## Metric: UniEval-Overall (single-metric card)

> **Annotator instructions.** Do not open `sum_mt/reports/noised_fluency/evaluation/Noised_Fluency_SUM.pdf` while filling this in. Use only the score tables below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** Score range 0 (worst) to 1 (best).

**Task:** summarization
**Dataset:** CNN-DailyMail, 100 reference summaries (~3 sentences each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Test results:**

**Reference (gold) score:** 0.8646


#### Verb lemmatization (`flu-lemmatizeverb`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.8201 | 0.052 | -5.15% |
| 100% | 0.7856 | 0.102 | -9.13% |

#### Random word drop (`flu-randomworddrop`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.6334 | 0.061 | -26.74% |
| 10% | 0.5000 | 0.111 | -42.17% |
| 15% | 0.4170 | 0.163 | -51.77% |
| 20% | 0.3290 | 0.210 | -61.95% |
| 25% | 0.2732 | 0.260 | -68.40% |
| 30% | 0.2228 | 0.311 | -74.23% |
| 35% | 0.1888 | 0.361 | -78.16% |
| 40% | 0.1632 | 0.408 | -81.12% |
| 45% | 0.1429 | 0.461 | -83.47% |
| 50% | 0.1258 | 0.507 | -85.46% |

#### Punctuation noise (`flu-noisepunct`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.7440 | 0.052 | -13.95% |
| 100% | 0.6570 | 0.105 | -24.02% |

#### Sentence-middle swap (`flu-sentencemiddleswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 1 sentence(s) swapped | 0.5667 | 0.145 | -34.46% |
| 2 sentence(s) swapped | 0.4254 | 0.255 | -50.80% |
| 3 sentence(s) swapped | 0.3241 | 0.321 | -62.52% |

#### Preposition removal (`flu-removepreposition`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 40% | 0.7322 | 0.054 | -15.31% |
| 70% | 0.6457 | 0.093 | -25.32% |
| 100% | 0.5684 | 0.135 | -34.26% |

#### Stop-word removal (`flu-removestopwords`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.7957 | 0.044 | -7.97% |
| 20% | 0.7356 | 0.088 | -14.92% |
| 30% | 0.6788 | 0.130 | -21.49% |
| 40% | 0.6255 | 0.175 | -27.65% |
| 50% | 0.5760 | 0.219 | -33.38% |
| 60% | 0.5303 | 0.263 | -38.67% |

#### Local word swap (`flu-randomlocalswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.5322 | 0.056 | -38.45% |
| 15% | 0.3388 | 0.117 | -60.81% |
| 30% | 0.2350 | 0.169 | -72.81% |
| 60% | 0.1763 | 0.222 | -79.61% |

#### Truncate (remove suffix) (`flu-truncate`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.6726 | 0.114 | -22.20% |
| 20% | 0.6176 | 0.215 | -28.57% |
| 30% | 0.6438 | 0.312 | -25.54% |
| 40% | 0.6065 | 0.413 | -29.85% |
| 50% | 0.6104 | 0.515 | -29.40% |

#### Article removal (`flu-removearticle`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.8569 | 0.039 | -0.89% |
| 100% | 0.8500 | 0.081 | -1.69% |

#### Random token repetition (`flu-randomtokenrep`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.6294 | 0.061 | -27.20% |
| 10% | 0.5243 | 0.111 | -39.36% |
| 15% | 0.4333 | 0.163 | -49.88% |
| 20% | 0.3953 | 0.210 | -54.28% |
| 25% | 0.3556 | 0.260 | -58.87% |
| 30% | 0.3298 | 0.311 | -61.86% |
| 35% | 0.3110 | 0.361 | -64.03% |
| 40% | 0.3062 | 0.408 | -64.58% |
| 45% | 0.2971 | 0.461 | -65.64% |
| 50% | 0.2837 | 0.507 | -67.19% |

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
| Punctuation noise (`flu-noisepunct`) | Yes                 | No                   | low         |
| Sentence-middle swap (`flu-sentencemiddleswap`) | Yes                 | No                   | moderate    |
| Preposition removal (`flu-removepreposition`) | Yes                 | No                   | moderate    |
| Stop-word removal (`flu-removestopwords`) | Yes                 | No                   | moderate    |
| Local word swap (`flu-randomlocalswap`) | Yes                 | No                   | high        |
| Truncate (remove suffix) (`flu-truncate`) | No                  | No                   | moderate    |
| Article removal (`flu-removearticle`) | Yes                 | No                   | low         |
| Random token repetition (`flu-randomtokenrep`) | Yes                 | No                   | high        |

### 2. Recommendation

Yes iff *more than 7* of the 10 noise types have **both** a high change rate **and** a superlinear decrease, else No.

_Your answer (Yes/No):_ No
