# Gold Card v2 — Noised Fluency Test, WMT21 De-En
## Metric: BERTScore-f (single-metric card)

> **Annotator instructions.** Do not open `sum_mt/reports/noised_fluency/evaluation/Noised_Fluency_WMT.pdf` while filling this in. Use only the score tables below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** Score range 0 (worst) to 1 (best).

**Task:** machine translation
**Dataset:** WMT21 De-En, 1000 reference translations (~1 sentence each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Test results:**

**Reference (gold) score:** 0.6869


#### Verb lemmatization (`flu-lemmatizeverb`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.6645 | 0.041 | -3.27% |
| 100% | 0.6439 | 0.081 | -6.26% |

#### Random word drop (`flu-randomworddrop`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.6066 | 0.085 | -11.69% |
| 10% | 0.5622 | 0.131 | -18.16% |
| 15% | 0.5136 | 0.185 | -25.23% |
| 20% | 0.4713 | 0.229 | -31.40% |
| 25% | 0.4317 | 0.276 | -37.16% |
| 30% | 0.3788 | 0.333 | -44.85% |
| 35% | 0.3405 | 0.385 | -50.43% |
| 40% | 0.3016 | 0.428 | -56.10% |
| 45% | 0.2532 | 0.486 | -63.14% |
| 55% | 0.1774 | 0.584 | -74.18% |

#### Punctuation noise (`flu-noisepunct`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.6581 | 0.049 | -4.19% |
| 100% | 0.6306 | 0.099 | -8.21% |

#### Sentence-middle swap (`flu-sentencemiddleswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 1 sentence(s) swapped | 0.4891 | 0.474 | -28.80% |

#### Preposition removal (`flu-removepreposition`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 40% | 0.6436 | 0.058 | -6.32% |
| 70% | 0.6101 | 0.102 | -11.19% |
| 100% | 0.5773 | 0.145 | -15.96% |

#### Stop-word removal (`flu-removestopwords`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.6562 | 0.052 | -4.48% |
| 20% | 0.6241 | 0.104 | -9.14% |
| 30% | 0.5918 | 0.158 | -13.85% |
| 40% | 0.5611 | 0.212 | -18.32% |
| 50% | 0.5316 | 0.264 | -22.61% |
| 60% | 0.5049 | 0.316 | -26.50% |

#### Local word swap (`flu-randomlocalswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.5899 | 0.083 | -14.13% |
| 15% | 0.5194 | 0.138 | -24.39% |
| 30% | 0.4638 | 0.179 | -32.49% |
| 60% | 0.3986 | 0.224 | -41.98% |

#### Truncate (remove suffix) (`flu-truncate`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.6170 | 0.120 | -10.18% |
| 20% | 0.5624 | 0.241 | -18.13% |
| 30% | 0.5193 | 0.340 | -24.41% |
| 40% | 0.4767 | 0.442 | -30.61% |
| 50% | 0.4170 | 0.555 | -39.30% |

#### Article removal (`flu-removearticle`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.6620 | 0.062 | -3.64% |
| 100% | 0.6378 | 0.126 | -7.15% |

#### Random token repetition (`flu-randomtokenrep`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.6386 | 0.085 | -7.04% |
| 10% | 0.6133 | 0.131 | -10.72% |
| 15% | 0.5873 | 0.185 | -14.51% |
| 20% | 0.5663 | 0.229 | -17.56% |
| 25% | 0.5440 | 0.276 | -20.81% |
| 30% | 0.5199 | 0.333 | -24.31% |
| 35% | 0.4983 | 0.385 | -27.46% |
| 40% | 0.4818 | 0.428 | -29.86% |
| 45% | 0.4603 | 0.486 | -32.99% |
| 55% | 0.4244 | 0.584 | -38.22% |

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
| Preposition removal (`flu-removepreposition`) | Yes                 | No                   | low         |
| Stop-word removal (`flu-removestopwords`) | Yes                 | No                   | moderate    |
| Local word swap (`flu-randomlocalswap`) | Yes                 | No                   | moderate    |
| Truncate (remove suffix) (`flu-truncate`) | Yes                 | No                   | moderate    |
| Article removal (`flu-removearticle`) | Yes                 | No                   | low         |
| Random token repetition (`flu-randomtokenrep`) | Yes                 | No                   | moderate    |

### 2. Recommendation

Yes iff *more than 7* of the 10 noise types have **both** a high change rate **and** a superlinear decrease, else No.

_Your answer (Yes/No):_ No
