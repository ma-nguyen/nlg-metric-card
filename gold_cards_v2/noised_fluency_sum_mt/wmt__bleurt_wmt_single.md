# Gold Card v2 — Noised Fluency Test, WMT21 De-En
## Metric: BLEURT (single-metric card)

> **Annotator instructions.** Do not open `sum_mt/reports/noised_fluency/evaluation/Noised_Fluency_WMT.pdf` while filling this in. Use only the score tables below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** Higher = better. Reference is on a small scale (~0–1) and may dip slightly negative; relative changes can therefore look large in % terms — judge change rate by absolute |Δ%| as defined in the rules.

**Task:** machine translation
**Dataset:** WMT21 De-En, 1000 reference translations (~1 sentence each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Test results:**

**Reference (gold) score:** 0.3166


#### Verb lemmatization (`flu-lemmatizeverb`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.2377 | 0.041 | -24.93% |
| 100% | 0.1645 | 0.081 | -48.05% |

#### Random word drop (`flu-randomworddrop`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.1041 | 0.085 | -67.13% |
| 10% | -0.0118 | 0.131 | -103.72% |
| 15% | -0.1446 | 0.185 | -145.67% |
| 20% | -0.2578 | 0.229 | -181.42% |
| 25% | -0.3702 | 0.276 | -216.94% |
| 30% | -0.4979 | 0.333 | -257.27% |
| 35% | -0.5983 | 0.385 | -288.99% |
| 40% | -0.6852 | 0.428 | -316.42% |
| 45% | -0.7895 | 0.486 | -349.37% |
| 55% | -0.9538 | 0.584 | -401.28% |

#### Punctuation noise (`flu-noisepunct`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.2819 | 0.049 | -10.96% |
| 100% | 0.2508 | 0.099 | -20.78% |

#### Sentence-middle swap (`flu-sentencemiddleswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 1 sentence(s) swapped | -0.0725 | 0.474 | -122.89% |

#### Preposition removal (`flu-removepreposition`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 40% | 0.2112 | 0.058 | -33.30% |
| 70% | 0.1275 | 0.102 | -59.72% |
| 100% | 0.0416 | 0.145 | -86.86% |

#### Stop-word removal (`flu-removestopwords`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.2456 | 0.052 | -22.44% |
| 20% | 0.1670 | 0.104 | -47.24% |
| 30% | 0.0878 | 0.158 | -72.27% |
| 40% | 0.0141 | 0.212 | -95.56% |
| 50% | -0.0592 | 0.264 | -118.70% |
| 60% | -0.1274 | 0.316 | -140.23% |

#### Local word swap (`flu-randomlocalswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.0349 | 0.083 | -88.97% |
| 15% | -0.1679 | 0.138 | -153.04% |
| 30% | -0.3174 | 0.179 | -200.26% |
| 60% | -0.4680 | 0.224 | -247.82% |

#### Truncate (remove suffix) (`flu-truncate`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.0816 | 0.120 | -74.24% |
| 20% | -0.0755 | 0.241 | -123.85% |
| 30% | -0.1881 | 0.340 | -159.43% |
| 40% | -0.3008 | 0.442 | -195.00% |
| 50% | -0.4742 | 0.555 | -249.77% |

#### Article removal (`flu-removearticle`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.2754 | 0.062 | -13.00% |
| 100% | 0.2304 | 0.126 | -27.21% |

#### Random token repetition (`flu-randomtokenrep`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.1851 | 0.085 | -41.55% |
| 10% | 0.1194 | 0.131 | -62.29% |
| 15% | 0.0484 | 0.185 | -84.72% |
| 20% | -0.0075 | 0.229 | -102.37% |
| 25% | -0.0666 | 0.276 | -121.03% |
| 30% | -0.1263 | 0.333 | -139.90% |
| 35% | -0.1728 | 0.385 | -154.57% |
| 40% | -0.2128 | 0.428 | -167.21% |
| 45% | -0.2630 | 0.486 | -183.08% |
| 55% | -0.3408 | 0.584 | -207.64% |

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
| Random word drop (`flu-randomworddrop`) | Yes                 | No                   | high        |
| Punctuation noise (`flu-noisepunct`) | Yes                 | No                   | low         |
| Sentence-middle swap (`flu-sentencemiddleswap`) | Yes                 | No                   | high        |
| Preposition removal (`flu-removepreposition`) | Yes                 | No                   | high        |
| Stop-word removal (`flu-removestopwords`) | Yes                 | No                   | high        |
| Local word swap (`flu-randomlocalswap`) | Yes                 | No                   | high        |
| Truncate (remove suffix) (`flu-truncate`) | Yes                 | No                   | high        |
| Article removal (`flu-removearticle`) | Yes                 | No                   | moderate    |
| Random token repetition (`flu-randomtokenrep`) | Yes                 | No                   | high        |

### 2. Recommendation

Yes iff *more than 7* of the 10 noise types have **both** a high change rate **and** a superlinear decrease, else No.

_Your answer (Yes/No):_ No
