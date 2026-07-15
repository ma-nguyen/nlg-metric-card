# Gold Card v2 — Noised Fluency Test, CNN-DailyMail
## Metric: UniEval-Coherence (single-metric card)

> **Annotator instructions.** Do not open `sum_mt/reports/noised_fluency/evaluation/Noised_Fluency_SUM.pdf` while filling this in. Use only the score tables below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** Score range 0 (worst) to 1 (best).

**Task:** summarization
**Dataset:** CNN-DailyMail, 100 reference summaries (~3 sentences each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Test results:**

**Reference (gold) score:** 0.8976


#### Verb lemmatization (`flu-lemmatizeverb`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.8695 | 0.052 | -3.13% |
| 100% | 0.8481 | 0.102 | -5.50% |

#### Random word drop (`flu-randomworddrop`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.6514 | 0.061 | -27.43% |
| 10% | 0.5128 | 0.111 | -42.87% |
| 15% | 0.4180 | 0.163 | -53.43% |
| 20% | 0.3064 | 0.210 | -65.86% |
| 25% | 0.2601 | 0.260 | -71.02% |
| 30% | 0.2096 | 0.311 | -76.65% |
| 35% | 0.1578 | 0.361 | -82.42% |
| 40% | 0.1468 | 0.408 | -83.64% |
| 45% | 0.1237 | 0.461 | -86.22% |
| 50% | 0.0962 | 0.507 | -89.29% |

#### Punctuation noise (`flu-noisepunct`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.8267 | 0.052 | -7.89% |
| 100% | 0.7789 | 0.105 | -13.22% |

#### Sentence-middle swap (`flu-sentencemiddleswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 1 sentence(s) swapped | 0.5170 | 0.145 | -42.40% |
| 2 sentence(s) swapped | 0.3940 | 0.255 | -56.11% |
| 3 sentence(s) swapped | 0.3151 | 0.321 | -64.90% |

#### Preposition removal (`flu-removepreposition`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 40% | 0.7996 | 0.054 | -10.91% |
| 70% | 0.7366 | 0.093 | -17.94% |
| 100% | 0.6803 | 0.135 | -24.20% |

#### Stop-word removal (`flu-removestopwords`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.8473 | 0.044 | -5.59% |
| 20% | 0.8020 | 0.088 | -10.65% |
| 30% | 0.7565 | 0.130 | -15.71% |
| 40% | 0.7117 | 0.175 | -20.71% |
| 50% | 0.6729 | 0.219 | -25.03% |
| 60% | 0.6312 | 0.263 | -29.67% |

#### Local word swap (`flu-randomlocalswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.5653 | 0.056 | -37.01% |
| 15% | 0.3604 | 0.117 | -59.85% |
| 30% | 0.2601 | 0.169 | -71.02% |
| 60% | 0.1828 | 0.222 | -79.63% |

#### Truncate (remove suffix) (`flu-truncate`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.6606 | 0.114 | -26.40% |
| 20% | 0.5716 | 0.215 | -36.32% |
| 30% | 0.6037 | 0.312 | -32.74% |
| 40% | 0.5726 | 0.413 | -36.20% |
| 50% | 0.5753 | 0.515 | -35.91% |

#### Article removal (`flu-removearticle`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.8907 | 0.039 | -0.77% |
| 100% | 0.8841 | 0.081 | -1.49% |

#### Random token repetition (`flu-randomtokenrep`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.6573 | 0.061 | -26.77% |
| 10% | 0.5495 | 0.111 | -38.78% |
| 15% | 0.4608 | 0.163 | -48.66% |
| 20% | 0.4300 | 0.210 | -52.10% |
| 25% | 0.3866 | 0.260 | -56.93% |
| 30% | 0.3683 | 0.311 | -58.96% |
| 35% | 0.3529 | 0.361 | -60.68% |
| 40% | 0.3580 | 0.408 | -60.11% |
| 45% | 0.3556 | 0.461 | -60.38% |
| 50% | 0.3385 | 0.507 | -62.28% |

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
| Random word drop (`flu-randomworddrop`) | Yes                 | Yes                  | high        |
| Punctuation noise (`flu-noisepunct`) | Yes                 | No                   | low         |
| Sentence-middle swap (`flu-sentencemiddleswap`) | Yes                 | No                   | high        |
| Preposition removal (`flu-removepreposition`) | Yes                 | No                   | low         |
| Stop-word removal (`flu-removestopwords`) | Yes                 | No                   | moderate    |
| Local word swap (`flu-randomlocalswap`) | Yes                 | No                   | high        |
| Truncate (remove suffix) (`flu-truncate`) | No                  | No                   | moderate    |
| Article removal (`flu-removearticle`) | Yes                 | No                   | low         |
| Random token repetition (`flu-randomtokenrep`) | No                  | No                   | high        |

### 2. Recommendation

Yes iff *more than 7* of the 10 noise types have **both** a high change rate **and** a superlinear decrease, else No.

_Your answer (Yes/No):_ No
