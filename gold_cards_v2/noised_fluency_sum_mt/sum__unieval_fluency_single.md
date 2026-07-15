# Gold Card v2 — Noised Fluency Test, CNN-DailyMail
## Metric: UniEval-Fluency (single-metric card)

> **Annotator instructions.** Do not open `sum_mt/reports/noised_fluency/evaluation/Noised_Fluency_SUM.pdf` while filling this in. Use only the score tables below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** Score range 0 (worst) to 1 (best).

**Task:** summarization
**Dataset:** CNN-DailyMail, 100 reference summaries (~3 sentences each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Test results:**

**Reference (gold) score:** 0.9197


#### Verb lemmatization (`flu-lemmatizeverb`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.8424 | 0.052 | -8.40% |
| 100% | 0.7760 | 0.102 | -15.62% |

#### Random word drop (`flu-randomworddrop`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.6612 | 0.061 | -28.10% |
| 10% | 0.5105 | 0.111 | -44.49% |
| 15% | 0.4055 | 0.163 | -55.91% |
| 20% | 0.3157 | 0.210 | -65.68% |
| 25% | 0.2231 | 0.260 | -75.74% |
| 30% | 0.1600 | 0.311 | -82.60% |
| 35% | 0.1390 | 0.361 | -84.89% |
| 40% | 0.1010 | 0.408 | -89.01% |
| 45% | 0.0803 | 0.461 | -91.27% |
| 50% | 0.0693 | 0.507 | -92.47% |

#### Punctuation noise (`flu-noisepunct`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.7031 | 0.052 | -23.55% |
| 100% | 0.5293 | 0.105 | -42.45% |

#### Sentence-middle swap (`flu-sentencemiddleswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 1 sentence(s) swapped | 0.6848 | 0.145 | -25.54% |
| 2 sentence(s) swapped | 0.4579 | 0.255 | -50.21% |
| 3 sentence(s) swapped | 0.2717 | 0.321 | -70.46% |

#### Preposition removal (`flu-removepreposition`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 40% | 0.7017 | 0.054 | -23.70% |
| 70% | 0.5573 | 0.093 | -39.41% |
| 100% | 0.4281 | 0.135 | -53.45% |

#### Stop-word removal (`flu-removestopwords`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.8073 | 0.044 | -12.22% |
| 20% | 0.7111 | 0.088 | -22.68% |
| 30% | 0.6239 | 0.130 | -32.15% |
| 40% | 0.5431 | 0.175 | -40.95% |
| 50% | 0.4677 | 0.219 | -49.15% |
| 60% | 0.4087 | 0.263 | -55.56% |

#### Local word swap (`flu-randomlocalswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.5132 | 0.056 | -44.20% |
| 15% | 0.2545 | 0.117 | -72.32% |
| 30% | 0.1058 | 0.169 | -88.49% |
| 60% | 0.0543 | 0.222 | -94.10% |

#### Truncate (remove suffix) (`flu-truncate`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.7406 | 0.114 | -19.47% |
| 20% | 0.7130 | 0.215 | -22.47% |
| 30% | 0.7155 | 0.312 | -22.20% |
| 40% | 0.6696 | 0.413 | -27.19% |
| 50% | 0.6601 | 0.515 | -28.23% |

#### Article removal (`flu-removearticle`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.9097 | 0.039 | -1.09% |
| 100% | 0.8985 | 0.081 | -2.30% |

#### Random token repetition (`flu-randomtokenrep`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.5833 | 0.061 | -36.57% |
| 10% | 0.4287 | 0.111 | -53.39% |
| 15% | 0.3033 | 0.163 | -67.02% |
| 20% | 0.2385 | 0.210 | -74.06% |
| 25% | 0.1857 | 0.260 | -79.80% |
| 30% | 0.1440 | 0.311 | -84.35% |
| 35% | 0.1171 | 0.361 | -87.26% |
| 40% | 0.0984 | 0.408 | -89.30% |
| 45% | 0.0870 | 0.461 | -90.54% |
| 50% | 0.0753 | 0.507 | -91.81% |

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
| Punctuation noise (`flu-noisepunct`) | Yes                 | No                   | moderate    |
| Sentence-middle swap (`flu-sentencemiddleswap`) | Yes                 | No                   | high        |
| Preposition removal (`flu-removepreposition`) | Yes                 | No                   | moderate    |
| Stop-word removal (`flu-removestopwords`) | Yes                 | No                   | moderate    |
| Local word swap (`flu-randomlocalswap`) | Yes                 | Yes                  | high        |
| Truncate (remove suffix) (`flu-truncate`) | No                  | No                   | moderate    |
| Article removal (`flu-removearticle`) | Yes                 | Yes                  | low         |
| Random token repetition (`flu-randomtokenrep`) | Yes                 | Yes                  | high        |

### 2. Recommendation

Yes iff *more than 7* of the 10 noise types have **both** a high change rate **and** a superlinear decrease, else No.

_Your answer (Yes/No):_ No
