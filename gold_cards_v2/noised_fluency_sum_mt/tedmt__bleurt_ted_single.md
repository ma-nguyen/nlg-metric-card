# Gold Card v2 — Noised Fluency Test, TED Zh-En
## Metric: BLEURT (single-metric card)

> **Annotator instructions.** Do not open `sum_mt/reports/noised_fluency/evaluation/Noised_Fluency_TEDMT.pdf` while filling this in. Use only the score tables below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** Higher = better. Reference value is small in magnitude (close to zero, may be slightly negative); relative changes can therefore look very large in % terms — judge change rate by absolute |Δ%| as defined in the rules.

**Task:** machine translation
**Dataset:** TED Zh-En, 1000 reference translations (~1 sentence each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Test results:**

**Reference (gold) score:** -0.1043


#### Verb lemmatization (`flu-lemmatizeverb`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | -0.1564 | 0.034 | -49.93% |
| 100% | -0.2046 | 0.065 | -96.22% |

#### Random word drop (`flu-randomworddrop`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | -0.2134 | 0.056 | -104.62% |
| 10% | -0.3093 | 0.105 | -196.63% |
| 15% | -0.4145 | 0.156 | -297.49% |
| 20% | -0.4931 | 0.205 | -372.84% |
| 25% | -0.5912 | 0.254 | -466.92% |
| 30% | -0.6918 | 0.306 | -563.43% |
| 35% | -0.7673 | 0.356 | -635.82% |
| 40% | -0.8513 | 0.405 | -716.36% |
| 45% | -0.9238 | 0.456 | -785.84% |
| 55% | -1.0689 | 0.556 | -924.99% |

#### Punctuation noise (`flu-noisepunct`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | -0.1435 | 0.073 | -37.66% |
| 100% | -0.1742 | 0.145 | -67.05% |

#### Sentence-middle swap (`flu-sentencemiddleswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 1 sentence(s) swapped | -0.1556 | 0.073 | -49.19% |

#### Preposition removal (`flu-removepreposition`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 40% | -0.1672 | 0.041 | -60.34% |
| 70% | -0.2154 | 0.072 | -106.60% |
| 100% | -0.2748 | 0.104 | -163.50% |

#### Stop-word removal (`flu-removestopwords`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | -0.1873 | 0.069 | -79.65% |
| 20% | -0.2689 | 0.139 | -157.87% |
| 30% | -0.3562 | 0.208 | -241.55% |
| 40% | -0.4445 | 0.278 | -326.24% |
| 50% | -0.5246 | 0.346 | -403.11% |
| 60% | -0.5947 | 0.412 | -470.27% |

#### Local word swap (`flu-randomlocalswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | -0.2949 | 0.050 | -182.76% |
| 15% | -0.5090 | 0.111 | -388.13% |
| 30% | -0.6912 | 0.165 | -562.84% |
| 60% | -0.8326 | 0.217 | -698.42% |

#### Truncate (remove suffix) (`flu-truncate`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | -0.1586 | 0.105 | -52.08% |
| 20% | -0.1792 | 0.206 | -71.84% |
| 30% | -0.2121 | 0.305 | -103.39% |
| 40% | -0.2894 | 0.406 | -177.51% |
| 50% | -0.3568 | 0.508 | -242.18% |

#### Article removal (`flu-removearticle`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | -0.1321 | 0.040 | -26.63% |
| 100% | -0.1672 | 0.080 | -60.34% |

#### Random token repetition (`flu-randomtokenrep`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | -0.1909 | 0.056 | -83.10% |
| 10% | -0.2555 | 0.105 | -145.00% |
| 15% | -0.3165 | 0.156 | -203.51% |
| 20% | -0.3713 | 0.205 | -256.02% |
| 25% | -0.4259 | 0.254 | -308.37% |
| 30% | -0.4739 | 0.306 | -354.43% |
| 35% | -0.5264 | 0.356 | -404.77% |
| 40% | -0.5662 | 0.405 | -442.93% |
| 45% | -0.6116 | 0.456 | -486.50% |
| 55% | -0.6767 | 0.556 | -548.89% |

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
| Verb lemmatization (`flu-lemmatizeverb`) | Yes                 | No                   | high        |
| Random word drop (`flu-randomworddrop`) | Yes                 | No                   | high        |
| Punctuation noise (`flu-noisepunct`) | Yes                 | No                   | high        |
| Sentence-middle swap (`flu-sentencemiddleswap`) | Yes                 | No                   | moderate    |
| Preposition removal (`flu-removepreposition`) | Yes                 | No                   | high        |
| Stop-word removal (`flu-removestopwords`) | Yes                 | No                   | high        |
| Local word swap (`flu-randomlocalswap`) | Yes                 | No                   | high        |
| Truncate (remove suffix) (`flu-truncate`) | Yes                 | No                   | high        |
| Article removal (`flu-removearticle`) | Yes                 | Yes                  | high        |
| Random token repetition (`flu-randomtokenrep`) | Yes                 | No                   | high        |

### 2. Recommendation

Yes iff *more than 7* of the 10 noise types have **both** a high change rate **and** a superlinear decrease, else No.

_Your answer (Yes/No):_ No
