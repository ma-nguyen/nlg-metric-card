# Gold Card v2 — Noised Fluency Test, WikiText-103
## Metric: MAUVE-RoBERTa-base (single-metric card)

> **Annotator instructions.** Do not open `wiki/reports/noised_fluency/evaluation/Noised_Fluency_WIKI.pdf` while filling this in. Use only the score tables below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** Score range 0 (worst) to 1 (best).

**Task:** open-ended text generation
**Dataset:** WikiText-103, 1000 paragraphs (~256 tokens each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Test results:**

**Reference (gold) score:** 0.9690


#### Verb lemmatization (`flu-lemmatizeverb`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.9376 | 0.045 | -3.23% |
| 100% | 0.6247 | 0.090 | -35.53% |

#### Random word drop (`flu-randomworddrop`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.9188 | 0.053 | -5.18% |
| 10% | 0.6335 | 0.103 | -34.62% |
| 15% | 0.1641 | 0.153 | -83.07% |
| 20% | 0.0289 | 0.202 | -97.01% |
| 25% | 0.0107 | 0.252 | -98.89% |
| 30% | 0.0069 | 0.303 | -99.29% |
| 35% | 0.0054 | 0.353 | -99.44% |
| 40% | 0.0049 | 0.402 | -99.50% |
| 45% | 0.0046 | 0.453 | -99.53% |
| 50% | 0.0045 | 0.501 | -99.54% |

#### Punctuation noise (`flu-noisepunct`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.3793 | 0.056 | -60.85% |
| 100% | 0.0258 | 0.111 | -97.33% |

#### Sentence-middle swap (`flu-sentencemiddleswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 1 sentence(s) swapped | 0.9503 | 0.072 | -1.92% |
| 2 sentence(s) swapped | 0.8763 | 0.134 | -9.56% |
| 3 sentence(s) swapped | 0.6205 | 0.191 | -35.96% |

#### Preposition removal (`flu-removepreposition`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 40% | 0.9403 | 0.057 | -2.96% |
| 70% | 0.8496 | 0.100 | -12.32% |
| 100% | 0.4996 | 0.142 | -48.44% |

#### Stop-word removal (`flu-removestopwords`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.9528 | 0.049 | -1.67% |
| 20% | 0.8663 | 0.097 | -10.59% |
| 30% | 0.5915 | 0.146 | -38.96% |
| 40% | 0.2168 | 0.194 | -77.62% |
| 50% | 0.0548 | 0.242 | -94.35% |
| 60% | 0.0231 | 0.290 | -97.62% |

#### Local word swap (`flu-randomlocalswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.8307 | 0.047 | -14.27% |
| 15% | 0.0318 | 0.109 | -96.72% |
| 30% | 0.0058 | 0.164 | -99.41% |
| 60% | 0.0043 | 0.216 | -99.55% |

#### Truncate (remove suffix) (`flu-truncate`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.7768 | 0.103 | -19.83% |
| 20% | 0.7119 | 0.203 | -26.53% |
| 30% | 0.6450 | 0.303 | -33.43% |
| 40% | 0.4706 | 0.403 | -51.44% |
| 50% | 0.2888 | 0.504 | -70.19% |

#### Article removal (`flu-removearticle`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.9569 | 0.053 | -1.24% |
| 100% | 0.8833 | 0.105 | -8.84% |

#### Random token repetition (`flu-randomtokenrep`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.9414 | 0.053 | -2.85% |
| 10% | 0.8230 | 0.103 | -15.07% |
| 15% | 0.4379 | 0.153 | -54.81% |
| 20% | 0.1282 | 0.202 | -86.77% |
| 25% | 0.0296 | 0.252 | -96.94% |
| 30% | 0.0125 | 0.303 | -98.71% |
| 35% | 0.0077 | 0.353 | -99.21% |
| 40% | 0.0062 | 0.402 | -99.36% |
| 45% | 0.0052 | 0.453 | -99.46% |
| 50% | 0.0049 | 0.501 | -99.50% |

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
| Verb lemmatization (`flu-lemmatizeverb`) | Yes                 | Yes                  | moderate    |
| Random word drop (`flu-randomworddrop`) | Yes                 | Yes                  | high        |
| Punctuation noise (`flu-noisepunct`) | Yes                 | Yes                  | high        |
| Sentence-middle swap (`flu-sentencemiddleswap`) | Yes                 | Yes                  | moderate    |
| Preposition removal (`flu-removepreposition`) | Yes                 | Yes                  | moderate    |
| Stop-word removal (`flu-removestopwords`) | Yes                 | Yes                  | high        |
| Local word swap (`flu-randomlocalswap`) | Yes                 | Yes                  | high        |
| Truncate (remove suffix) (`flu-truncate`) | Yes                 | No                   | high        |
| Article removal (`flu-removearticle`) | Yes                 | Yes                  | low         |
| Random token repetition (`flu-randomtokenrep`) | Yes                 | Yes                  | high        |

### 2. Recommendation

Yes iff *more than 7* of the 10 noise types have **both** a high change rate **and** a superlinear decrease, else No.

_Your answer (Yes/No):_ No
