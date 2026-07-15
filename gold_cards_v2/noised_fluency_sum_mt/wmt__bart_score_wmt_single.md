# Gold Card v2 — Noised Fluency Test, WMT21 De-En
## Metric: BARTScore (single-metric card)

> **Annotator instructions.** Do not open `sum_mt/reports/noised_fluency/evaluation/Noised_Fluency_WMT.pdf` while filling this in. Use only the score tables below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** Log-likelihood; higher (closer to 0) = better. Reference values are negative.

**Task:** machine translation
**Dataset:** WMT21 De-En, 1000 reference translations (~1 sentence each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Test results:**

**Reference (gold) score:** -3.8115


#### Verb lemmatization (`flu-lemmatizeverb`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | -3.9420 | 0.041 | -3.42% |
| 100% | -4.0720 | 0.081 | -6.84% |

#### Random word drop (`flu-randomworddrop`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | -4.2614 | 0.085 | -11.80% |
| 10% | -4.4921 | 0.131 | -17.86% |
| 15% | -4.7854 | 0.185 | -25.55% |
| 20% | -5.0392 | 0.229 | -32.21% |
| 25% | -5.3038 | 0.276 | -39.15% |
| 30% | -5.7055 | 0.333 | -49.69% |
| 35% | -6.0443 | 0.385 | -58.58% |
| 40% | -6.3993 | 0.428 | -67.89% |
| 45% | -6.9040 | 0.486 | -81.14% |
| 55% | -7.9302 | 0.584 | -108.06% |

#### Punctuation noise (`flu-noisepunct`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | -4.0322 | 0.049 | -5.79% |
| 100% | -4.2403 | 0.099 | -11.25% |

#### Sentence-middle swap (`flu-sentencemiddleswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 1 sentence(s) swapped | -4.7161 | 0.474 | -23.73% |

#### Preposition removal (`flu-removepreposition`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 40% | -4.0954 | 0.058 | -7.45% |
| 70% | -4.3243 | 0.102 | -13.45% |
| 100% | -4.5679 | 0.145 | -19.85% |

#### Stop-word removal (`flu-removestopwords`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | -4.0151 | 0.052 | -5.34% |
| 20% | -4.2332 | 0.104 | -11.06% |
| 30% | -4.4635 | 0.158 | -17.11% |
| 40% | -4.7089 | 0.212 | -23.54% |
| 50% | -4.9592 | 0.264 | -30.11% |
| 60% | -5.2306 | 0.316 | -37.23% |

#### Local word swap (`flu-randomlocalswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | -4.4804 | 0.083 | -17.55% |
| 15% | -4.9548 | 0.138 | -30.00% |
| 30% | -5.3474 | 0.179 | -40.30% |
| 60% | -5.7525 | 0.224 | -50.92% |

#### Truncate (remove suffix) (`flu-truncate`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | -4.1542 | 0.120 | -8.99% |
| 20% | -4.4105 | 0.241 | -15.72% |
| 30% | -4.6621 | 0.340 | -22.32% |
| 40% | -5.0380 | 0.442 | -32.18% |
| 50% | -5.7337 | 0.555 | -50.43% |

#### Article removal (`flu-removearticle`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | -4.0574 | 0.062 | -6.45% |
| 100% | -4.3221 | 0.126 | -13.40% |

#### Random token repetition (`flu-randomtokenrep`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | -4.0856 | 0.085 | -7.19% |
| 10% | -4.2429 | 0.131 | -11.32% |
| 15% | -4.4034 | 0.185 | -15.53% |
| 20% | -4.5429 | 0.229 | -19.19% |
| 25% | -4.6767 | 0.276 | -22.70% |
| 30% | -4.8166 | 0.333 | -26.37% |
| 35% | -4.9554 | 0.385 | -30.01% |
| 40% | -5.0579 | 0.428 | -32.70% |
| 45% | -5.1941 | 0.486 | -36.27% |
| 55% | -5.4051 | 0.584 | -41.81% |

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
| Sentence-middle swap (`flu-sentencemiddleswap`) | Yes                 | No                   | low         |
| Preposition removal (`flu-removepreposition`) | Yes                 | No                   | low         |
| Stop-word removal (`flu-removestopwords`) | Yes                 | Yes                  | moderate    |
| Local word swap (`flu-randomlocalswap`) | Yes                 | No                   | moderate    |
| Truncate (remove suffix) (`flu-truncate`) | Yes                 | No                   | moderate    |
| Article removal (`flu-removearticle`) | Yes                 | Yes                  | low         |
| Random token repetition (`flu-randomtokenrep`) | Yes                 | No                   | moderate    |

### 2. Recommendation

Yes iff *more than 7* of the 10 noise types have **both** a high change rate **and** a superlinear decrease, else No.

_Your answer (Yes/No):_ No
