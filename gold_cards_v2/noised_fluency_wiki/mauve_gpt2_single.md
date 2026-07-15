# Gold Card v2 — Noised Fluency Test, WikiText-103
## Metric: MAUVE-GPT2-base (single-metric card)

> **Annotator instructions.** Do not open `wiki/reports/noised_fluency/evaluation/Noised_Fluency_WIKI.pdf` while filling this in. Use only the score tables below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** Score range 0 (worst) to 1 (best).

**Task:** open-ended text generation
**Dataset:** WikiText-103, 1000 paragraphs (~256 tokens each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Test results:**

**Reference (gold) score:** 0.9547


#### Verb lemmatization (`flu-lemmatizeverb`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.8560 | 0.045 | -10.34% |
| 100% | 0.4985 | 0.090 | -47.78% |

#### Random word drop (`flu-randomworddrop`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.6256 | 0.053 | -34.48% |
| 10% | 0.2672 | 0.103 | -72.02% |
| 15% | 0.0981 | 0.153 | -89.73% |
| 20% | 0.0476 | 0.202 | -95.01% |
| 25% | 0.0273 | 0.252 | -97.14% |
| 30% | 0.0189 | 0.303 | -98.02% |
| 35% | 0.0138 | 0.353 | -98.56% |
| 40% | 0.0108 | 0.402 | -98.87% |
| 45% | 0.0095 | 0.453 | -99.00% |
| 50% | 0.0089 | 0.501 | -99.07% |

#### Punctuation noise (`flu-noisepunct`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.0137 | 0.056 | -98.57% |
| 100% | 0.0059 | 0.111 | -99.38% |

#### Sentence-middle swap (`flu-sentencemiddleswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 1 sentence(s) swapped | 0.8351 | 0.072 | -12.53% |
| 2 sentence(s) swapped | 0.5283 | 0.134 | -44.67% |
| 3 sentence(s) swapped | 0.3180 | 0.191 | -66.70% |

#### Preposition removal (`flu-removepreposition`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 40% | 0.8309 | 0.057 | -12.97% |
| 70% | 0.5580 | 0.100 | -41.55% |
| 100% | 0.2673 | 0.142 | -72.00% |

#### Stop-word removal (`flu-removestopwords`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.8874 | 0.049 | -7.05% |
| 20% | 0.6370 | 0.097 | -33.28% |
| 30% | 0.3084 | 0.146 | -67.70% |
| 40% | 0.1398 | 0.194 | -85.36% |
| 50% | 0.0636 | 0.242 | -93.33% |
| 60% | 0.0346 | 0.290 | -96.38% |

#### Local word swap (`flu-randomlocalswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.2572 | 0.047 | -73.06% |
| 15% | 0.0263 | 0.109 | -97.24% |
| 30% | 0.0096 | 0.164 | -99.00% |
| 60% | 0.0069 | 0.216 | -99.27% |

#### Truncate (remove suffix) (`flu-truncate`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.1644 | 0.103 | -82.78% |
| 20% | 0.1707 | 0.203 | -82.12% |
| 30% | 0.1788 | 0.303 | -81.28% |
| 40% | 0.1623 | 0.403 | -83.00% |
| 50% | 0.1458 | 0.504 | -84.73% |

#### Article removal (`flu-removearticle`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.8495 | 0.053 | -11.02% |
| 100% | 0.5184 | 0.105 | -45.71% |

#### Random token repetition (`flu-randomtokenrep`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.6571 | 0.053 | -31.17% |
| 10% | 0.3207 | 0.103 | -66.41% |
| 15% | 0.1402 | 0.153 | -85.31% |
| 20% | 0.0703 | 0.202 | -92.64% |
| 25% | 0.0362 | 0.252 | -96.21% |
| 30% | 0.0228 | 0.303 | -97.61% |
| 35% | 0.0178 | 0.353 | -98.13% |
| 40% | 0.0132 | 0.402 | -98.61% |
| 45% | 0.0115 | 0.453 | -98.80% |
| 50% | 0.0097 | 0.501 | -98.99% |

---

## Your annotations

### 1. Sensitivity to the Perturbation

For each noise type, fill in three cells. Categorise the **change rate** by the *largest* `|Δ%|` observed across all variation levels for that noise type:

- `low`      iff `max(|Δ%|) ≤ 25`
- `moderate` iff `max(|Δ%|) ≤ 60`
- `high`     otherwise (especially when `≈ 100`)

`monotonous decrease` = score moves in the expected direction at every step as variation increases. `superlinear decrease` = the per-step `|Δ|` *grows* as variation grows. (Note: for `GPT2-base-PPL` higher = worse, so the expected direction is `score increases`. Apply the same definitions accordingly: monotonous = monotonous in the *correct* direction; the change-rate categories use `|Δ%|` and so don't need a sign flip.)

| Noise type | Monotonous decrease | Superlinear decrease | Change rate |
|---|-------|----------------------|------|
| Verb lemmatization (`flu-lemmatizeverb`) | Yes   | Yes                  | moderate |
| Random word drop (`flu-randomworddrop`) | Yes   | Yes                  | high |
| Punctuation noise (`flu-noisepunct`) | Yes   | Yes                  | high |
| Sentence-middle swap (`flu-sentencemiddleswap`) | Yes   | No                   | high |
| Preposition removal (`flu-removepreposition`) | Yes   | Yes                  | high |
| Stop-word removal (`flu-removestopwords`) | Yes   | Yes                  | high |
| Local word swap (`flu-randomlocalswap`) | Yes   | Yes                  | high |
| Truncate (remove suffix) (`flu-truncate`) | No    | No                   | high |
| Article removal (`flu-removearticle`) | Yes   | Yes                  | moderate |
| Random token repetition (`flu-randomtokenrep`) | Yes   | Yes                  | high |

### 2. Recommendation

Yes iff *more than 7* of the 10 noise types have **both** a high change rate **and** a superlinear decrease, else No.

_Your answer (Yes/No):_ Yes
