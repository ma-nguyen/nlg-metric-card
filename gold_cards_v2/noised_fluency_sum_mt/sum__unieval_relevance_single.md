# Gold Card v2 — Noised Fluency Test, CNN-DailyMail
## Metric: UniEval-Relevance (single-metric card)

> **Annotator instructions.** Do not open `sum_mt/reports/noised_fluency/evaluation/Noised_Fluency_SUM.pdf` while filling this in. Use only the score tables below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** Score range 0 (worst) to 1 (best).

**Task:** summarization
**Dataset:** CNN-DailyMail, 100 reference summaries (~3 sentences each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Test results:**

**Reference (gold) score:** 0.7813


#### Verb lemmatization (`flu-lemmatizeverb`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.7265 | 0.052 | -7.02% |
| 100% | 0.6952 | 0.102 | -11.02% |

#### Random word drop (`flu-randomworddrop`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.4571 | 0.061 | -41.49% |
| 10% | 0.2773 | 0.111 | -64.50% |
| 15% | 0.1961 | 0.163 | -74.90% |
| 20% | 0.1231 | 0.210 | -84.24% |
| 25% | 0.0783 | 0.260 | -89.98% |
| 30% | 0.0502 | 0.311 | -93.58% |
| 35% | 0.0350 | 0.361 | -95.53% |
| 40% | 0.0297 | 0.408 | -96.20% |
| 45% | 0.0189 | 0.461 | -97.58% |
| 50% | 0.0155 | 0.507 | -98.02% |

#### Punctuation noise (`flu-noisepunct`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.6480 | 0.052 | -17.06% |
| 100% | 0.5735 | 0.105 | -26.60% |

#### Sentence-middle swap (`flu-sentencemiddleswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 1 sentence(s) swapped | 0.3033 | 0.145 | -61.18% |
| 2 sentence(s) swapped | 0.1847 | 0.255 | -76.36% |
| 3 sentence(s) swapped | 0.1176 | 0.321 | -84.95% |

#### Preposition removal (`flu-removepreposition`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 40% | 0.6254 | 0.054 | -19.95% |
| 70% | 0.5259 | 0.093 | -32.69% |
| 100% | 0.4370 | 0.135 | -44.06% |

#### Stop-word removal (`flu-removestopwords`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.6945 | 0.044 | -11.10% |
| 20% | 0.6234 | 0.088 | -20.21% |
| 30% | 0.5515 | 0.130 | -29.42% |
| 40% | 0.4917 | 0.175 | -37.07% |
| 50% | 0.4312 | 0.219 | -44.81% |
| 60% | 0.3720 | 0.263 | -52.39% |

#### Local word swap (`flu-randomlocalswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.3190 | 0.056 | -59.16% |
| 15% | 0.1148 | 0.117 | -85.31% |
| 30% | 0.0382 | 0.169 | -95.11% |
| 60% | 0.0181 | 0.222 | -97.68% |

#### Truncate (remove suffix) (`flu-truncate`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.4787 | 0.114 | -38.73% |
| 20% | 0.3744 | 0.215 | -52.08% |
| 30% | 0.4502 | 0.312 | -42.38% |
| 40% | 0.3944 | 0.413 | -49.53% |
| 50% | 0.3943 | 0.515 | -49.53% |

#### Article removal (`flu-removearticle`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.7700 | 0.039 | -1.44% |
| 100% | 0.7637 | 0.081 | -2.25% |

#### Random token repetition (`flu-randomtokenrep`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.4808 | 0.061 | -38.46% |
| 10% | 0.3586 | 0.111 | -54.11% |
| 15% | 0.2485 | 0.163 | -68.19% |
| 20% | 0.2084 | 0.210 | -73.33% |
| 25% | 0.1693 | 0.260 | -78.33% |
| 30% | 0.1422 | 0.311 | -81.79% |
| 35% | 0.1277 | 0.361 | -83.65% |
| 40% | 0.1255 | 0.408 | -83.94% |
| 45% | 0.1186 | 0.461 | -84.81% |
| 50% | 0.1033 | 0.507 | -86.78% |

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
| Punctuation noise (`flu-noisepunct`) | Yes                 | No                   | moderate    |
| Sentence-middle swap (`flu-sentencemiddleswap`) | Yes                 | No                   | high        |
| Preposition removal (`flu-removepreposition`) | Yes                 | No                   | moderate    |
| Stop-word removal (`flu-removestopwords`) | Yes                 | No                   | moderate    |
| Local word swap (`flu-randomlocalswap`) | Yes                 | Yes                  | high        |
| Truncate (remove suffix) (`flu-truncate`) | Yes                 | No                   | moderate    |
| Article removal (`flu-removearticle`) | Yes                 | No                   | low         |
| Random token repetition (`flu-randomtokenrep`) | Yes                 | No                   | high        |

### 2. Recommendation

Yes iff *more than 7* of the 10 noise types have **both** a high change rate **and** a superlinear decrease, else No.

_Your answer (Yes/No):_ No
