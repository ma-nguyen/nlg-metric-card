# Gold Card v2 — Noised Fluency Test, TED Zh-En
## Metric: BERTScore-f (single-metric card)

> **Annotator instructions.** Do not open `sum_mt/reports/noised_fluency/evaluation/Noised_Fluency_TEDMT.pdf` while filling this in. Use only the score tables below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** Score range 0 (worst) to 1 (best).

**Task:** machine translation
**Dataset:** TED Zh-En, 1000 reference translations (~1 sentence each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Test results:**

**Reference (gold) score:** 0.5452


#### Verb lemmatization (`flu-lemmatizeverb`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.5272 | 0.034 | -3.29% |
| 100% | 0.5110 | 0.065 | -6.26% |

#### Random word drop (`flu-randomworddrop`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.4937 | 0.056 | -9.45% |
| 10% | 0.4509 | 0.105 | -17.30% |
| 15% | 0.4040 | 0.156 | -25.89% |
| 20% | 0.3636 | 0.205 | -33.30% |
| 25% | 0.3215 | 0.254 | -41.03% |
| 30% | 0.2743 | 0.306 | -49.68% |
| 35% | 0.2353 | 0.356 | -56.83% |
| 40% | 0.1946 | 0.405 | -64.31% |
| 45% | 0.1537 | 0.456 | -71.81% |
| 55% | 0.0784 | 0.556 | -85.61% |

#### Punctuation noise (`flu-noisepunct`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.4911 | 0.073 | -9.91% |
| 100% | 0.4407 | 0.145 | -19.17% |

#### Sentence-middle swap (`flu-sentencemiddleswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 1 sentence(s) swapped | 0.5079 | 0.073 | -6.83% |

#### Preposition removal (`flu-removepreposition`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 40% | 0.5182 | 0.041 | -4.95% |
| 70% | 0.4990 | 0.072 | -8.47% |
| 100% | 0.4774 | 0.104 | -12.43% |

#### Stop-word removal (`flu-removestopwords`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.5065 | 0.069 | -7.10% |
| 20% | 0.4711 | 0.139 | -13.58% |
| 30% | 0.4355 | 0.208 | -20.12% |
| 40% | 0.3987 | 0.278 | -26.87% |
| 50% | 0.3622 | 0.346 | -33.56% |
| 60% | 0.3288 | 0.412 | -39.69% |

#### Local word swap (`flu-randomlocalswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.4733 | 0.050 | -13.17% |
| 15% | 0.3902 | 0.111 | -28.42% |
| 30% | 0.3112 | 0.165 | -42.92% |
| 60% | 0.2230 | 0.217 | -59.10% |

#### Truncate (remove suffix) (`flu-truncate`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.5130 | 0.105 | -5.90% |
| 20% | 0.4881 | 0.206 | -10.46% |
| 30% | 0.4640 | 0.305 | -14.89% |
| 40% | 0.4342 | 0.406 | -20.36% |
| 50% | 0.3993 | 0.508 | -26.75% |

#### Article removal (`flu-removearticle`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.5293 | 0.040 | -2.91% |
| 100% | 0.5133 | 0.080 | -5.84% |

#### Random token repetition (`flu-randomtokenrep`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.5042 | 0.056 | -7.51% |
| 10% | 0.4715 | 0.105 | -13.51% |
| 15% | 0.4391 | 0.156 | -19.45% |
| 20% | 0.4087 | 0.205 | -25.03% |
| 25% | 0.3781 | 0.254 | -30.65% |
| 30% | 0.3498 | 0.306 | -35.84% |
| 35% | 0.3238 | 0.356 | -40.60% |
| 40% | 0.2982 | 0.405 | -45.29% |
| 45% | 0.2745 | 0.456 | -49.66% |
| 55% | 0.2288 | 0.556 | -58.03% |

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
| Stop-word removal (`flu-removestopwords`) | Yes                 | No                   | moderate    |
| Local word swap (`flu-randomlocalswap`) | Yes                 | No                   | moderate    |
| Truncate (remove suffix) (`flu-truncate`) | Yes                 | No                   | moderate    |
| Article removal (`flu-removearticle`) | Yes                 | Yes                  | low         |
| Random token repetition (`flu-randomtokenrep`) | Yes                 | No                   | moderate    |

### 2. Recommendation

Yes iff *more than 7* of the 10 noise types have **both** a high change rate **and** a superlinear decrease, else No.

_Your answer (Yes/No):_ No
