# Gold Card v2 — Noised Fluency Test, TED Zh-En
## Metric: BARTScore (single-metric card)

> **Annotator instructions.** Do not open `sum_mt/reports/noised_fluency/evaluation/Noised_Fluency_TEDMT.pdf` while filling this in. Use only the score tables below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** Log-likelihood; higher (closer to 0) = better. Reference values are negative.

**Task:** machine translation
**Dataset:** TED Zh-En, 1000 reference translations (~1 sentence each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Test results:**

**Reference (gold) score:** -3.7343


#### Verb lemmatization (`flu-lemmatizeverb`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | -3.8256 | 0.034 | -2.45% |
| 100% | -3.9142 | 0.065 | -4.82% |

#### Random word drop (`flu-randomworddrop`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | -3.9563 | 0.056 | -5.95% |
| 10% | -4.1713 | 0.105 | -11.70% |
| 15% | -4.4134 | 0.156 | -18.19% |
| 20% | -4.6566 | 0.205 | -24.70% |
| 25% | -4.9251 | 0.254 | -31.89% |
| 30% | -5.2529 | 0.306 | -40.67% |
| 35% | -5.5718 | 0.356 | -49.21% |
| 40% | -5.9226 | 0.405 | -58.60% |
| 45% | -6.3162 | 0.456 | -69.14% |
| 55% | -7.0841 | 0.556 | -89.71% |

#### Punctuation noise (`flu-noisepunct`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | -4.0520 | 0.073 | -8.51% |
| 100% | -4.2991 | 0.145 | -15.13% |

#### Sentence-middle swap (`flu-sentencemiddleswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 1 sentence(s) swapped | -3.8569 | 0.073 | -3.28% |

#### Preposition removal (`flu-removepreposition`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 40% | -3.8919 | 0.041 | -4.22% |
| 70% | -4.0359 | 0.072 | -8.08% |
| 100% | -4.2035 | 0.104 | -12.56% |

#### Stop-word removal (`flu-removestopwords`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | -3.9436 | 0.069 | -5.60% |
| 20% | -4.1826 | 0.139 | -12.01% |
| 30% | -4.4449 | 0.208 | -19.03% |
| 40% | -4.7515 | 0.278 | -27.24% |
| 50% | -5.0826 | 0.346 | -36.11% |
| 60% | -5.4528 | 0.412 | -46.02% |

#### Local word swap (`flu-randomlocalswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | -4.1261 | 0.050 | -10.49% |
| 15% | -4.6411 | 0.111 | -24.28% |
| 30% | -5.1532 | 0.165 | -38.00% |
| 60% | -5.6243 | 0.217 | -50.61% |

#### Truncate (remove suffix) (`flu-truncate`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | -3.8427 | 0.105 | -2.90% |
| 20% | -4.0479 | 0.206 | -8.40% |
| 30% | -4.4133 | 0.305 | -18.18% |
| 40% | -4.9869 | 0.406 | -33.55% |
| 50% | -5.7788 | 0.508 | -54.75% |

#### Article removal (`flu-removearticle`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | -3.8691 | 0.040 | -3.61% |
| 100% | -4.0361 | 0.080 | -8.08% |

#### Random token repetition (`flu-randomtokenrep`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | -3.9210 | 0.056 | -5.00% |
| 10% | -4.1058 | 0.105 | -9.95% |
| 15% | -4.2948 | 0.156 | -15.01% |
| 20% | -4.4766 | 0.205 | -19.88% |
| 25% | -4.6429 | 0.254 | -24.33% |
| 30% | -4.8449 | 0.306 | -29.74% |
| 35% | -4.9993 | 0.356 | -33.88% |
| 40% | -5.1604 | 0.405 | -38.19% |
| 45% | -5.3488 | 0.456 | -43.24% |
| 55% | -5.6599 | 0.556 | -51.57% |

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
| Sentence-middle swap (`flu-sentencemiddleswap`) | Yes                 | No                   | low         |
| Preposition removal (`flu-removepreposition`) | Yes                 | No                   | low         |
| Stop-word removal (`flu-removestopwords`) | Yes                 | Yes                  | moderate    |
| Local word swap (`flu-randomlocalswap`) | Yes                 | No                   | moderate    |
| Truncate (remove suffix) (`flu-truncate`) | Yes                 | Yes                  | moderate    |
| Article removal (`flu-removearticle`) | Yes                 | Yes                  | low         |
| Random token repetition (`flu-randomtokenrep`) | Yes                 | No                   | moderate    |

### 2. Recommendation

Yes iff *more than 7* of the 10 noise types have **both** a high change rate **and** a superlinear decrease, else No.

_Your answer (Yes/No):_ No
