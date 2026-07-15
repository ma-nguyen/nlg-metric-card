# Gold Card v2 — Noised Fluency Test, WikiText-103
## Compare card across metrics

> **Annotator instructions.** Do not open `wiki/reports/noised_fluency/evaluation/Noised_Fluency_WIKI.pdf` while filling this in. The single-metric tables you produced for `mauve_gpt2_single.md`, `mauve_roberta_single.md`, `mauve_roberta_large_single.md`, `gpt_ppl_single.md` are the per-metric ground truth — this card aggregates them. Save in place.

**Metrics compared:** MAUVE-GPT2-base, MAUVE-RoBERTa-base, MAUVE-RoBERTa-large, GPT2-base-PPL
**Task:** open-ended text generation
**Dataset:** WikiText-103
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Maximum absolute Δ% per (metric, noise type)** — drives the change-rate category. (Refer to the per-metric single cards for full per-variation tables.)

| Noise type | MAUVE-GPT2-base max abs(Δ%) | MAUVE-RoBERTa-base max abs(Δ%) | MAUVE-RoBERTa-large max abs(Δ%) | GPT2-base-PPL max abs(Δ%) |
|---|---|---|---|---|
| Verb lemmatization (`flu-lemmatizeverb`) | 47.78% | 35.53% | 74.87% | 54.48% |
| Random word drop (`flu-randomworddrop`) | 99.07% | 99.54% | 99.49% | 1181.76% |
| Punctuation noise (`flu-noisepunct`) | 99.38% | 97.33% | 99.05% | 53.34% |
| Sentence-middle swap (`flu-sentencemiddleswap`) | 66.70% | 35.96% | 89.11% | 46.93% |
| Preposition removal (`flu-removepreposition`) | 72.00% | 48.44% | 91.21% | 190.84% |
| Stop-word removal (`flu-removestopwords`) | 96.38% | 97.62% | 97.98% | 428.85% |
| Local word swap (`flu-randomlocalswap`) | 99.27% | 99.55% | 99.52% | 895.23% |
| Truncate (remove suffix) (`flu-truncate`) | 84.73% | 70.19% | 82.52% | 26.65% |
| Article removal (`flu-removearticle`) | 45.71% | 8.84% | 54.27% | 67.05% |
| Random token repetition (`flu-randomtokenrep`) | 98.99% | 99.50% | 99.52% | 162.83% |

---

## Your annotations

For each noise type, name the metric(s) that should be **recommended** for that noise type. A metric is recommended for a noise type iff it has *both* a `high` change rate *and* a `superlinear decrease` for that noise type, as you classified them in the corresponding single card. Multiple metrics may qualify for one noise type; if none qualify, write `none`.

| Noise type | Recommended metric(s)                                                   |
|---|-------------------------------------------------------------------------|
| Verb lemmatization | MAUVE-RoBERTa-large                                                     |
| Random word drop | MAUVE-GPT2-base, MAUVE-RoBERTa-base, MAUVE-RoBERTa-large, GPT2-base-PPL |
| Punctuation noise | MAUVE-GPT2-base, MAUVE-RoBERTa-base, MAUVE-RoBERTa-large                |
| Sentence-middle swap | none                                                                    |
| Preposition removal | MAUVE-GPT2-base, GPT2-base-PPL                                          |
| Stop-word removal | MAUVE-GPT2-base, MAUVE-RoBERTa-base, MAUVE-RoBERTa-large, GPT2-base-PPL |
| Local word swap | MAUVE-GPT2-base, MAUVE-RoBERTa-base, MAUVE-RoBERTa-large, GPT2-base-PPL |
| Truncate (remove suffix) | none                                                                    |
| Article removal | GPT2-base-PPL                                                     |
| Random token repetition | MAUVE-GPT2-base, MAUVE-RoBERTa-base, MAUVE-RoBERTa-large                                                     |
