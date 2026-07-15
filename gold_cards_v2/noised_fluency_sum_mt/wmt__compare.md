# Gold Card v2 — Noised Fluency Test, WMT21 De-En
## Compare card across metrics

> **Annotator instructions.** Do not open `sum_mt/reports/noised_fluency/evaluation/Noised_Fluency_WMT.pdf` while filling this in. The single-metric tables you produce for `wmt__bart_score_wmt_single.md`, `wmt__bert_score_f_wmt_single.md`, `wmt__bleu_wmt_single.md`, `wmt__bleurt_wmt_single.md` are the per-metric ground truth — this card aggregates them. Save in place.

**Metrics compared:** BARTScore, BERTScore-f, BLEU, BLEURT
**Task:** machine translation
**Dataset:** WMT21 De-En, 1000 reference translations (~1 sentence each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Maximum absolute Δ% per (metric, noise type)** — drives the change-rate category. (Refer to the per-metric single cards for full per-variation tables.)

| Noise type | BARTScore max abs(Δ%) | BERTScore-f max abs(Δ%) | BLEU max abs(Δ%) | BLEURT max abs(Δ%) |
|---|---|---|---|---|
| Verb lemmatization (`flu-lemmatizeverb`) | 6.84% | 6.26% | 11.10% | 48.05% |
| Random word drop (`flu-randomworddrop`) | 108.06% | 74.18% | 83.54% | 401.28% |
| Punctuation noise (`flu-noisepunct`) | 11.25% | 8.21% | 13.75% | 20.78% |
| Sentence-middle swap (`flu-sentencemiddleswap`) | 23.73% | 28.80% | 21.15% | 122.89% |
| Preposition removal (`flu-removepreposition`) | 19.85% | 15.96% | 27.37% | 86.86% |
| Stop-word removal (`flu-removestopwords`) | 37.23% | 26.50% | 45.08% | 140.23% |
| Local word swap (`flu-randomlocalswap`) | 50.92% | 41.98% | 55.13% | 247.82% |
| Truncate (remove suffix) (`flu-truncate`) | 50.43% | 39.30% | 56.48% | 249.77% |
| Article removal (`flu-removearticle`) | 13.40% | 7.15% | 21.62% | 27.21% |
| Random token repetition (`flu-randomtokenrep`) | 41.81% | 38.22% | 48.53% | 207.64% |

---

## Your annotations

For each noise type, name the metric(s) that should be **recommended** for that noise type. A metric is recommended for a noise type iff it has *both* a `high` change rate *and* a `superlinear decrease` for that noise type, as you classified them in the corresponding single card. Multiple metrics may qualify for one noise type; if none qualify, write `none`.

| Noise type | Recommended metric(s) |
|---|-----------------------|
| Verb lemmatization | none                  |
| Random word drop | none                  |
| Punctuation noise | none                  |
| Sentence-middle swap | none                  |
| Preposition removal | none                  |
| Stop-word removal | none                  |
| Local word swap | none                  |
| Truncate (remove suffix) | none                  |
| Article removal | none                  |
| Random token repetition | none                  |
