# Gold Card v2 — Noised Fluency Test, CNN-DailyMail
## Metric: ROUGE-L (single-metric card)

> **Annotator instructions.** Do not open `sum_mt/reports/noised_fluency/evaluation/Noised_Fluency_SUM.pdf` while filling this in. Use only the score tables below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** Score range 0 (worst) to 1 (best).

**Task:** summarization
**Dataset:** CNN-DailyMail, 100 reference summaries (~3 sentences each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Test results:**

**Reference (gold) score:** 0.2862


#### Verb lemmatization (`flu-lemmatizeverb`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.2849 | 0.052 | -0.45% |
| 100% | 0.2839 | 0.102 | -0.80% |

#### Random word drop (`flu-randomworddrop`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.2816 | 0.061 | -1.61% |
| 10% | 0.2803 | 0.111 | -2.07% |
| 15% | 0.2744 | 0.163 | -4.13% |
| 20% | 0.2710 | 0.210 | -5.31% |
| 25% | 0.2666 | 0.260 | -6.84% |
| 30% | 0.2621 | 0.311 | -8.43% |
| 35% | 0.2576 | 0.361 | -9.99% |
| 40% | 0.2512 | 0.408 | -12.21% |
| 45% | 0.2435 | 0.461 | -14.92% |
| 50% | 0.2368 | 0.507 | -17.26% |

#### Punctuation noise (`flu-noisepunct`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.2862 | 0.052 | +0.00% |
| 100% | 0.2862 | 0.105 | +0.00% |

#### Sentence-middle swap (`flu-sentencemiddleswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 1 sentence(s) swapped | 0.2766 | 0.145 | -3.34% |
| 2 sentence(s) swapped | 0.2670 | 0.255 | -6.69% |
| 3 sentence(s) swapped | 0.2589 | 0.321 | -9.53% |

#### Preposition removal (`flu-removepreposition`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 40% | 0.2827 | 0.054 | -1.22% |
| 70% | 0.2792 | 0.093 | -2.45% |
| 100% | 0.2742 | 0.135 | -4.18% |

#### Stop-word removal (`flu-removestopwords`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.2830 | 0.044 | -1.11% |
| 20% | 0.2810 | 0.088 | -1.80% |
| 30% | 0.2780 | 0.130 | -2.85% |
| 40% | 0.2758 | 0.175 | -3.64% |
| 50% | 0.2718 | 0.219 | -5.03% |
| 60% | 0.2682 | 0.263 | -6.27% |

#### Local word swap (`flu-randomlocalswap`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.2799 | 0.056 | -2.20% |
| 15% | 0.2727 | 0.117 | -4.73% |
| 30% | 0.2656 | 0.169 | -7.21% |
| 60% | 0.2568 | 0.222 | -10.29% |

#### Truncate (remove suffix) (`flu-truncate`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 10% | 0.2900 | 0.114 | +1.31% |
| 20% | 0.2954 | 0.215 | +3.22% |
| 30% | 0.2981 | 0.312 | +4.14% |
| 40% | 0.2998 | 0.413 | +4.74% |
| 50% | 0.3018 | 0.515 | +5.44% |

#### Article removal (`flu-removearticle`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 50% | 0.2795 | 0.039 | -2.33% |
| 100% | 0.2709 | 0.081 | -5.36% |

#### Random token repetition (`flu-randomtokenrep`)

| Variation | Score | edit_ratio | Δ vs gold |
|---|---|---|---|
| 5% | 0.2775 | 0.061 | -3.04% |
| 10% | 0.2717 | 0.111 | -5.05% |
| 15% | 0.2651 | 0.163 | -7.37% |
| 20% | 0.2594 | 0.210 | -9.37% |
| 25% | 0.2541 | 0.260 | -11.23% |
| 30% | 0.2480 | 0.311 | -13.35% |
| 35% | 0.2432 | 0.361 | -15.02% |
| 40% | 0.2388 | 0.408 | -16.55% |
| 45% | 0.2340 | 0.461 | -18.25% |
| 50% | 0.2291 | 0.507 | -19.95% |

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
| Random word drop (`flu-randomworddrop`) | Yes                 | No                   | low         |
| Punctuation noise (`flu-noisepunct`) | No                  | No                   | low         |
| Sentence-middle swap (`flu-sentencemiddleswap`) | Yes                 | No                   | low         |
| Preposition removal (`flu-removepreposition`) | Yes                 | Yes                  | low         |
| Stop-word removal (`flu-removestopwords`) | Yes                 | No                   | low         |
| Local word swap (`flu-randomlocalswap`) | Yes                 | No                   | low         |
| Truncate (remove suffix) (`flu-truncate`) | No                  | No                   | low         |
| Article removal (`flu-removearticle`) | Yes                 | Yes                  | low         |
| Random token repetition (`flu-randomtokenrep`) | Yes                 | No                   | low         |

### 2. Recommendation

Yes iff *more than 7* of the 10 noise types have **both** a high change rate **and** a superlinear decrease, else No.

_Your answer (Yes/No):_ No
