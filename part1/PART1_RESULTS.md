# Part 1 — Multimodal inspection classification

## Dataset
- 300 labelled training units; 100 unlabelled test units.
- Acoustic labels: 30 NG / 270 OK.
- Visual labels: 26 NG / 274 OK.
- Acoustic representation: 70 features.
- Visual representation: 8,114 features.

## Validation
The saved validation metrics use threshold 0.24 for acoustic and 0.10 for visual classification.

| Metric | Acoustic | Visual |
|---|---:|---:|
| Accuracy | 0.880 | 0.627 |
| Balanced accuracy | 0.742 | 0.721 |
| NG precision | 0.400 | 0.156 |
| NG recall | 0.571 | 0.833 |
| NG F1 | 0.471 | 0.263 |
| ROC-AUC | 0.874 | 0.737 |

Confusion matrices, rows and columns ordered as OK, NG:
- Acoustic: `[[62, 6], [3, 4]]`
- Visual: `[[42, 27], [1, 5]]`

The visual threshold catches five of six NG validation cases but flags 27 OK cases as NG. The small number of positive validation examples makes the estimates uncertain.

## Test prediction artifact
`results/predictions.csv` contains 100 unique test units. It stores both modality scores and labels and an OR-fused final label. Final thresholds recorded for the test artifact are 0.35 acoustic and 0.13 visual. These differ from the thresholds used for the validation table above.

Test labels are hidden; no test-set performance metric is available or claimed.
