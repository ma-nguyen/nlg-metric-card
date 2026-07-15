# Gold Card v2 — Noised Fluency Test, TED Zh-En
## Metric: BLEU (single-metric card)

> **Annotator instructions.** Do not open `sum_mt/reports/noised_fluency/evaluation/Noised_Fluency_TEDMT.pdf` while filling this in. Use only the score tables below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** Reported on a 0–100 scale; higher = better.

**Task:** machine translation
**Dataset:** TED Zh-En, 1000 reference translations (~1 sentence each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Test results:**

**Reference (gold) score:** 23.8190


#### Verb lemmatization (`flu-lemmatizeverb`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 22.9308 | 0.034 | -3.73% |
| 100% | 22.1092 | 0.065 | -7.18% |

#### Random word drop (`flu-randomworddrop`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 22.0297 | 0.056 | -7.51% |
| 10% | 20.4645 | 0.105 | -14.08% |
| 15% | 18.5157 | 0.156 | -22.26% |
| 20% | 16.3625 | 0.205 | -31.30% |
| 25% | 14.5756 | 0.254 | -38.81% |
| 30% | 12.5144 | 0.306 | -47.46% |
| 35% | 10.6952 | 0.356 | -55.10% |
| 40% | 8.8523 | 0.405 | -62.84% |
| 45% | 7.2367 | 0.456 | -69.62% |
| 55% | 4.4902 | 0.556 | -81.15% |

#### Punctuation noise (`flu-noisepunct`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 20.3014 | 0.073 | -14.77% |
| 100% | 16.7068 | 0.145 | -29.86% |

#### Sentence-middle swap (`flu-sentencemiddleswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 1 sentence(s) swapped | 22.6517 | 0.073 | -4.90% |

#### Preposition removal (`flu-removepreposition`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 40% | 22.7194 | 0.041 | -4.62% |
| 70% | 21.5701 | 0.072 | -9.44% |
| 100% | 20.4360 | 0.104 | -14.20% |

#### Stop-word removal (`flu-removestopwords`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 22.1469 | 0.069 | -7.02% |
| 20% | 20.1796 | 0.139 | -15.28% |
| 30% | 17.9839 | 0.208 | -24.50% |
| 40% | 15.4785 | 0.278 | -35.02% |
| 50% | 13.0321 | 0.346 | -45.29% |
| 60% | 10.8369 | 0.412 | -54.50% |

#### Local word swap (`flu-randomlocalswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 21.0533 | 0.050 | -11.61% |
| 15% | 17.4731 | 0.111 | -26.64% |
| 30% | 14.2524 | 0.165 | -40.16% |
| 60% | 10.7476 | 0.217 | -54.88% |

#### Truncate (remove suffix) (`flu-truncate`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 23.1514 | 0.105 | -2.80% |
| 20% | 20.9754 | 0.206 | -11.94% |
| 30% | 18.2386 | 0.305 | -23.43% |
| 40% | 14.7702 | 0.406 | -37.99% |
| 50% | 10.5364 | 0.508 | -55.76% |

#### Article removal (`flu-removearticle`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 22.2882 | 0.040 | -6.43% |
| 100% | 20.6209 | 0.080 | -13.43% |

#### Random token repetition (`flu-randomtokenrep`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 22.2166 | 0.056 | -6.73% |
| 10% | 20.9151 | 0.105 | -12.19% |
| 15% | 19.6746 | 0.156 | -17.40% |
| 20% | 18.5900 | 0.205 | -21.95% |
| 25% | 17.5995 | 0.254 | -26.11% |
| 30% | 16.5374 | 0.306 | -30.57% |
| 35% | 15.8269 | 0.356 | -33.55% |
| 40% | 14.9623 | 0.405 | -37.18% |
| 45% | 14.3604 | 0.456 | -39.71% |
| 55% | 13.1309 | 0.556 | -44.87% |

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
| Punctuation noise (`flu-noisepunct`) | Yes                 | Yes                  | moderate    |
| Sentence-middle swap (`flu-sentencemiddleswap`) | Yes                 | No                   | low         |
| Preposition removal (`flu-removepreposition`) | Yes                 | No                   | low         |
| Stop-word removal (`flu-removestopwords`) | Yes                 | No                   | moderate    |
| Local word swap (`flu-randomlocalswap`) | Yes                 | No                   | moderate    |
| Truncate (remove suffix) (`flu-truncate`) | Yes                 | Yes                  | moderate    |
| Article removal (`flu-removearticle`) | Yes                 | Yes                  | low         |
| Random token repetition (`flu-randomtokenrep`) | Yes                 | No                   | moderate    |

### 2. Recommendation

Yes iff *more than 7* of the 10 noise types have **both** a high change rate **and** a superlinear decrease, else No.

_Your answer (Yes/No):_ No
