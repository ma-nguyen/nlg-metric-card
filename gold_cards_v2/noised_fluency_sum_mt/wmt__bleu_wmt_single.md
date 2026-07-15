# Gold Card v2 — Noised Fluency Test, WMT21 De-En
## Metric: BLEU (single-metric card)

> **Annotator instructions.** Do not open `sum_mt/reports/noised_fluency/evaluation/Noised_Fluency_WMT.pdf` while filling this in. Use only the score tables below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** Reported on a 0–100 scale; higher = better.

**Task:** machine translation
**Dataset:** WMT21 De-En, 1000 reference translations (~1 sentence each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Test results:**

**Reference (gold) score:** 27.9476


#### Verb lemmatization (`flu-lemmatizeverb`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 26.4158 | 0.041 | -5.48% |
| 100% | 24.8463 | 0.081 | -11.10% |

#### Random word drop (`flu-randomworddrop`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 23.9003 | 0.085 | -14.48% |
| 10% | 21.4295 | 0.131 | -23.32% |
| 15% | 18.9729 | 0.185 | -32.11% |
| 20% | 16.9231 | 0.229 | -39.45% |
| 25% | 14.8111 | 0.276 | -47.00% |
| 30% | 12.4978 | 0.333 | -55.28% |
| 35% | 10.7499 | 0.385 | -61.54% |
| 40% | 9.3317 | 0.428 | -66.61% |
| 45% | 7.2957 | 0.486 | -73.90% |
| 55% | 4.5993 | 0.584 | -83.54% |

#### Punctuation noise (`flu-noisepunct`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 25.9734 | 0.049 | -7.06% |
| 100% | 24.1046 | 0.099 | -13.75% |

#### Sentence-middle swap (`flu-sentencemiddleswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 1 sentence(s) swapped | 22.0354 | 0.474 | -21.15% |

#### Preposition removal (`flu-removepreposition`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 40% | 24.9427 | 0.058 | -10.75% |
| 70% | 22.5950 | 0.102 | -19.15% |
| 100% | 20.2994 | 0.145 | -27.37% |

#### Stop-word removal (`flu-removestopwords`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 25.7299 | 0.052 | -7.94% |
| 20% | 23.4816 | 0.104 | -15.98% |
| 30% | 21.3088 | 0.158 | -23.75% |
| 40% | 19.1681 | 0.212 | -31.41% |
| 50% | 17.2269 | 0.264 | -38.36% |
| 60% | 15.3486 | 0.316 | -45.08% |

#### Local word swap (`flu-randomlocalswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 22.4189 | 0.083 | -19.78% |
| 15% | 18.2433 | 0.138 | -34.72% |
| 30% | 15.2085 | 0.179 | -45.58% |
| 60% | 12.5388 | 0.224 | -55.13% |

#### Truncate (remove suffix) (`flu-truncate`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 25.1682 | 0.120 | -9.95% |
| 20% | 22.2994 | 0.241 | -20.21% |
| 30% | 19.4082 | 0.340 | -30.56% |
| 40% | 16.1655 | 0.442 | -42.16% |
| 50% | 12.1621 | 0.555 | -56.48% |

#### Article removal (`flu-removearticle`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 25.1091 | 0.062 | -10.16% |
| 100% | 21.9040 | 0.126 | -21.62% |

#### Random token repetition (`flu-randomtokenrep`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 25.2643 | 0.085 | -9.60% |
| 10% | 23.7985 | 0.131 | -14.85% |
| 15% | 22.1806 | 0.185 | -20.63% |
| 20% | 20.9137 | 0.229 | -25.17% |
| 25% | 19.8791 | 0.276 | -28.87% |
| 30% | 18.5526 | 0.333 | -33.62% |
| 35% | 17.4893 | 0.385 | -37.42% |
| 40% | 16.7043 | 0.428 | -40.23% |
| 45% | 15.7703 | 0.486 | -43.57% |
| 55% | 14.3839 | 0.584 | -48.53% |

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
| Sentence-middle swap (`flu-sentencemiddleswap`) | Yes                 | No                   | low         |
| Preposition removal (`flu-removepreposition`) | Yes                 | No                   | moderate    |
| Stop-word removal (`flu-removestopwords`) | Yes                 | No                   | moderate    |
| Local word swap (`flu-randomlocalswap`) | Yes                 | No                   | moderate    |
| Truncate (remove suffix) (`flu-truncate`) | Yes                 | Yes                  | moderate    |
| Article removal (`flu-removearticle`) | Yes                 | Yes                  | low         |
| Random token repetition (`flu-randomtokenrep`) | Yes                 | No                   | moderate    |

### 2. Recommendation

Yes iff *more than 7* of the 10 noise types have **both** a high change rate **and** a superlinear decrease, else No.

_Your answer (Yes/No):_ No
