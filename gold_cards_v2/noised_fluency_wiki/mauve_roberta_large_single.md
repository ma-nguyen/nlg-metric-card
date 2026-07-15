# Gold Card v2 — Noised Fluency Test, WikiText-103
## Metric: MAUVE-RoBERTa-large (single-metric card)

> **Annotator instructions.** Do not open `wiki/reports/noised_fluency/evaluation/Noised_Fluency_WIKI.pdf` while filling this in. Use only the score tables below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** Score range 0 (worst) to 1 (best).

**Task:** open-ended text generation
**Dataset:** WikiText-103, 1000 paragraphs (~256 tokens each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Test results:**

**Reference (gold) score:** 0.9708


#### Verb lemmatization (`flu-lemmatizeverb`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.8646 | 0.045 | -10.94% |
| 100% | 0.2440 | 0.090 | -74.87% |

#### Random word drop (`flu-randomworddrop`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.7100 | 0.053 | -26.86% |
| 10% | 0.2314 | 0.103 | -76.16% |
| 15% | 0.0518 | 0.153 | -94.66% |
| 20% | 0.0215 | 0.202 | -97.79% |
| 25% | 0.0107 | 0.252 | -98.90% |
| 30% | 0.0074 | 0.303 | -99.24% |
| 35% | 0.0064 | 0.353 | -99.34% |
| 40% | 0.0060 | 0.402 | -99.38% |
| 45% | 0.0053 | 0.453 | -99.46% |
| 50% | 0.0049 | 0.501 | -99.49% |

#### Punctuation noise (`flu-noisepunct`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.0894 | 0.056 | -90.79% |
| 100% | 0.0092 | 0.111 | -99.05% |

#### Sentence-middle swap (`flu-sentencemiddleswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 1 sentence(s) swapped | 0.6930 | 0.072 | -28.61% |
| 2 sentence(s) swapped | 0.2923 | 0.134 | -69.89% |
| 3 sentence(s) swapped | 0.1057 | 0.191 | -89.11% |

#### Preposition removal (`flu-removepreposition`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 40% | 0.8680 | 0.057 | -10.58% |
| 70% | 0.4459 | 0.100 | -54.07% |
| 100% | 0.0853 | 0.142 | -91.21% |

#### Stop-word removal (`flu-removestopwords`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.9053 | 0.049 | -6.74% |
| 20% | 0.6007 | 0.097 | -38.12% |
| 30% | 0.1918 | 0.146 | -80.24% |
| 40% | 0.0595 | 0.194 | -93.87% |
| 50% | 0.0268 | 0.242 | -97.24% |
| 60% | 0.0196 | 0.290 | -97.98% |

#### Local word swap (`flu-randomlocalswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.3430 | 0.047 | -64.67% |
| 15% | 0.0122 | 0.109 | -98.74% |
| 30% | 0.0054 | 0.164 | -99.44% |
| 60% | 0.0047 | 0.216 | -99.52% |

#### Truncate (remove suffix) (`flu-truncate`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.7950 | 0.103 | -18.10% |
| 20% | 0.7009 | 0.203 | -27.79% |
| 30% | 0.5261 | 0.303 | -45.81% |
| 40% | 0.3488 | 0.403 | -64.07% |
| 50% | 0.1697 | 0.504 | -82.52% |

#### Article removal (`flu-removearticle`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.9103 | 0.053 | -6.23% |
| 100% | 0.4440 | 0.105 | -54.27% |

#### Random token repetition (`flu-randomtokenrep`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.7613 | 0.053 | -21.58% |
| 10% | 0.1862 | 0.103 | -80.81% |
| 15% | 0.0322 | 0.153 | -96.68% |
| 20% | 0.0109 | 0.202 | -98.88% |
| 25% | 0.0074 | 0.252 | -99.24% |
| 30% | 0.0059 | 0.303 | -99.39% |
| 35% | 0.0055 | 0.353 | -99.43% |
| 40% | 0.0050 | 0.402 | -99.49% |
| 45% | 0.0048 | 0.453 | -99.51% |
| 50% | 0.0046 | 0.501 | -99.52% |

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
| Verb lemmatization (`flu-lemmatizeverb`) | Yes                 | Yes                  | high        |
| Random word drop (`flu-randomworddrop`) | Yes                 | Yes                  | high        |
| Punctuation noise (`flu-noisepunct`) | Yes                 | Yes                  | high        |
| Sentence-middle swap (`flu-sentencemiddleswap`) | Yes                 | No                   | high        |
| Preposition removal (`flu-removepreposition`) | Yes                 | No                   | high        |
| Stop-word removal (`flu-removestopwords`) | Yes                 | Yes                  | high        |
| Local word swap (`flu-randomlocalswap`) | Yes                 | Yes                  | high        |
| Truncate (remove suffix) (`flu-truncate`) | Yes                 | No                   | high        |
| Article removal (`flu-removearticle`) | Yes                 | Yes                  | moderate    |
| Random token repetition (`flu-randomtokenrep`) | Yes                 | Yes                  | high        |

### 2. Recommendation

Yes iff *more than 7* of the 10 noise types have **both** a high change rate **and** a superlinear decrease, else No.

_Your answer (Yes/No):_ No
