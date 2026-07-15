# Gold Card v2 — Noised Fluency Test, WikiText-103
## Metric: GPT2-base-PPL (single-metric card)

> **Annotator instructions.** Do not open `wiki/reports/noised_fluency/evaluation/Noised_Fluency_WIKI.pdf` while filling this in. Use only the score tables below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** Higher GPT-PPL = lower quality.

**Task:** open-ended text generation
**Dataset:** WikiText-103, 1000 paragraphs (~256 tokens each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Test results:**

**Reference (gold) score:** 35.0607


#### Verb lemmatization (`flu-lemmatizeverb`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 45.0703 | 0.045 | +28.55% |
| 100% | 54.1623 | 0.090 | +54.48% |

#### Random word drop (`flu-randomworddrop`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 49.7052 | 0.053 | +41.77% |
| 10% | 67.7180 | 0.103 | +93.15% |
| 15% | 90.4285 | 0.153 | +157.92% |
| 20% | 118.2935 | 0.202 | +237.40% |
| 25% | 151.7249 | 0.252 | +332.75% |
| 30% | 193.4845 | 0.303 | +451.86% |
| 35% | 242.3474 | 0.353 | +591.22% |
| 40% | 298.8044 | 0.402 | +752.25% |
| 45% | 368.4505 | 0.453 | +950.89% |
| 50% | 449.3924 | 0.501 | +1181.76% |

#### Punctuation noise (`flu-noisepunct`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 47.1259 | 0.056 | +34.41% |
| 100% | 53.7629 | 0.111 | +53.34% |

#### Sentence-middle swap (`flu-sentencemiddleswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 1 sentence(s) swapped | 40.3362 | 0.072 | +15.05% |
| 2 sentence(s) swapped | 45.7827 | 0.134 | +30.58% |
| 3 sentence(s) swapped | 51.5131 | 0.191 | +46.93% |

#### Preposition removal (`flu-removepreposition`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 40% | 54.5072 | 0.057 | +55.47% |
| 70% | 75.0256 | 0.100 | +113.99% |
| 100% | 101.9704 | 0.142 | +190.84% |

#### Stop-word removal (`flu-removestopwords`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 48.1321 | 0.049 | +37.28% |
| 20% | 64.8395 | 0.097 | +84.94% |
| 30% | 85.9841 | 0.146 | +145.24% |
| 40% | 112.4323 | 0.194 | +220.68% |
| 50% | 145.3184 | 0.242 | +314.48% |
| 60% | 185.4190 | 0.290 | +428.85% |

#### Local word swap (`flu-randomlocalswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 62.1212 | 0.047 | +77.18% |
| 15% | 124.1443 | 0.109 | +254.08% |
| 30% | 217.7314 | 0.164 | +521.01% |
| 60% | 348.9352 | 0.216 | +895.23% |

#### Truncate (remove suffix) (`flu-truncate`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 37.0923 | 0.103 | +5.79% |
| 20% | 38.2839 | 0.203 | +9.19% |
| 30% | 39.7067 | 0.303 | +13.25% |
| 40% | 41.6693 | 0.403 | +18.85% |
| 50% | 44.4051 | 0.504 | +26.65% |

#### Article removal (`flu-removearticle`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 46.4985 | 0.053 | +32.62% |
| 100% | 58.5694 | 0.105 | +67.05% |

#### Random token repetition (`flu-randomtokenrep`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 44.1392 | 0.053 | +25.89% |
| 10% | 52.8325 | 0.103 | +50.69% |
| 15% | 61.1004 | 0.153 | +74.27% |
| 20% | 68.7757 | 0.202 | +96.16% |
| 25% | 75.4424 | 0.252 | +115.18% |
| 30% | 80.9751 | 0.303 | +130.96% |
| 35% | 85.5975 | 0.353 | +144.14% |
| 40% | 88.7074 | 0.402 | +153.01% |
| 45% | 91.1540 | 0.453 | +159.99% |
| 50% | 92.1514 | 0.501 | +162.83% |

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
| Verb lemmatization (`flu-lemmatizeverb`) | Yes                 | No                   | moderate    |
| Random word drop (`flu-randomworddrop`) | Yes                 | Yes                  | high        |
| Punctuation noise (`flu-noisepunct`) | Yes                 | No                   | moderate    |
| Sentence-middle swap (`flu-sentencemiddleswap`) | Yes                 | Yes                  | moderate    |
| Preposition removal (`flu-removepreposition`) | Yes                 | Yes                  | high        |
| Stop-word removal (`flu-removestopwords`) | Yes                 | Yes                  | high        |
| Local word swap (`flu-randomlocalswap`) | Yes                 | Yes                  | high        |
| Truncate (remove suffix) (`flu-truncate`) | Yes                 | Yes                  | moderate    |
| Article removal (`flu-removearticle`) | Yes                 | Yes                  | high        |
| Random token repetition (`flu-randomtokenrep`) | Yes                 | No                   | high        |

### 2. Recommendation

Yes iff *more than 7* of the 10 noise types have **both** a high change rate **and** a superlinear decrease, else No.

_Your answer (Yes/No):_ No
