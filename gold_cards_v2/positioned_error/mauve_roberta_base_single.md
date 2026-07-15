# Gold Card v2 — Positioned Error Test, WikiText-103
## Metric: MAUVE-RoBERTa-Base (single-metric card)

> **Annotator instructions.** Do not open `wiki/reports/positioned_error/evaluation/Positional_Error_Evaluation.pdf` while filling this in. Use only the score table below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** The Metric scores from 0 (Minimum) to 1 (Maximum)

**Task:** open-ended text generation
**Dataset:** WikiText-103, 1000 paragraphs (~256 tokens each)
**Perturbation:** 10 consecutive tokens at the beginning, middle, or end of each gold paragraph are either shuffled (shuffling-test) or replaced with random vocabulary tokens (random-test).

**Test results:**

| Variant                | Gold     | Perturbed | Δ (%)      |
|------------------------|----------|-----------|------------|
| Shuffling, Beginning   |   0.9621 |    0.9584 |     -0.39% |
| Shuffling, Middle      |   0.9621 |    0.9484 |     -1.43% |
| Shuffling, End         |   0.9621 |    0.5112 |    -46.87% |
| Random,    Beginning   |   0.9621 |    0.8939 |     -7.09% |
| Random,    Middle      |   0.9621 |    0.9113 |     -5.28% |
| Random,    End         |   0.9621 |    0.5097 |    -47.02% |

---

## Your annotations

### 1. Did a perturbed output score higher than the gold output? If yes, which one?

_Your answer:_ No


### 2. Were the scores similar for every location (beginning, middle, end)? Yes iff every individual location-score has |change| < 10%. Answer with `Yes` or `No` only -- no list.

_Your answer:_ No


### 3. Were the scores similar between the shuffling-test and the random-test? Yes iff every individual variant has |change| < 10%. Answer with `Yes` or `No` only -- no list.

_Your answer:_ No


### 4. **Strengths.** List every variation with high change rate or higher (≥70%).

_Your answer:_ None


### 5. **Weaknesses.** List every variation without high change rate or higher (<70%).

_Your answer:_ 
- Shuffling, Beginning
- Shuffling, Middle
- Shuffling, End
- Random, Beginning
- Random, Middle
- Random, End


### 6. **Recommendation.** Yes if the metric has more than 5 variants with ≥70% change, else No.

_Your answer:_ No


### 7. What needs improvement? (List positional variants where the metric did not reach a near-minimal score.)

_Your answer:_ 
- Shuffling, Beginning
- Shuffling, Middle
- Shuffling, End
- Random, Beginning
- Random, Middle
- Random, End



