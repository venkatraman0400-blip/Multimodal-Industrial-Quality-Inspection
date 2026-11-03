# Multimodal Industrial Quality Inspection System

**Independent R&D project**  
Acoustic and visual defect classification, decision-level fusion, and production-line sensor-shift investigation.

## Project overview

This project explores an industrial quality-inspection workflow using two data modalities:

- **Acoustic inspection:** time-domain and spectral features, including RMS, zero-crossing rate, spectral descriptors, and MFCC statistics.
- **Visual inspection:** grayscale image processing and Histogram of Oriented Gradients (HOG) features.
- **Decision fusion:** OR-based fusion; a unit is flagged `NG` if either modality predicts `NG`.
- **Production monitoring:** latest-test handling, microphone installation-time matching, station/day summaries, alarm thresholds, and camera-region brightness checks.
- **Sensor-shift investigation:** examines whether a station-level alarm increase may be associated with a microphone change.

## Repository structure

```text
.
├── part1/
│   ├── notebooks/
│   │   ├── audio_defect_detection.ipynb
│   │   └── visual_defect_detection.ipynb
│   ├── PART1_RESULTS.md
│   └── results/
│       ├── predictions.csv
│       ├── least_confident_test_units.csv
│       ├── validation_metrics.csv
│       └── validation_metrics.json
├── part2/
│   └── research_note.md
├── part3/
│   ├── line_monitor.py
│   ├── debugging_and_root_cause.md
│   └── expected_output.txt
├── docs/
│   └── ai_assistance.md
└── requirements.txt
```

The large intermediate feature-cache CSV files are not committed to this repository. They can be regenerated from the original media inputs using the notebooks.

## Part 1 — Acoustic and visual defect detection

### Dataset and feature design

The supplied artifacts describe 300 labelled training units and 100 test units. Test labels are hidden.

| Modality | Features | Validation split |
|---|---:|---:|
| Acoustic | 70 | 225 train / 75 validation |
| Visual | 8,114 | 225 train / 75 validation |

### Saved validation metrics

The metrics below use the thresholds recorded in the validation artifact (acoustic 0.24; visual 0.10). They are not the final test-prediction thresholds.

| Metric | Acoustic | Visual |
|---|---:|---:|
| Accuracy | 0.880 | 0.627 |
| Balanced accuracy | 0.742 | 0.721 |
| NG precision | 0.400 | 0.156 |
| NG recall | 0.571 | 0.833 |
| NG F1 | 0.471 | 0.263 |
| ROC-AUC | 0.874 | 0.737 |

Confusion matrices (rows = actual [OK, NG], columns = predicted [OK, NG]):

- Acoustic: `[[62, 6], [3, 4]]`
- Visual: `[[42, 27], [1, 5]]`

**Interpretation:** the acoustic model has stronger ROC-AUC and accuracy in this validation split. The visual model detects 5 of 6 NG validation examples at its recorded threshold, but produces 27 false positives among OK examples. The positive validation sample is very small, so these results are uncertain and should not be treated as production performance.

### Test predictions

`part1/results/predictions.csv` contains 100 test-unit predictions, modality scores and labels, and the OR-fused final label. The recorded prediction thresholds are 0.35 (acoustic) and 0.13 (visual).

The test labels are unavailable. No test-set accuracy, precision, recall, F1, or ROC-AUC is claimed.

## Part 3 — Production-line monitoring

Run the monitor with:

```bash
python part3/line_monitor.py path/to/input_folder
```

The input folder must contain:

- `test_log.csv`
- `station_mics.csv`
- `frames/ST1.png`, `frames/ST2.png`, `frames/ST3.png`, and `frames/ST4.png`

The script treats blank and `--` sound-level readings as missing, retains the latest test per unit, matches microphone installation windows, aggregates station/day metrics, raises an alarm above an 8% NG rate, and checks configured camera ROIs.

The original Part 3 input CSVs and camera images are not included. `expected_output.txt` preserves the supplied output artifact; the script must be rerun against the original inputs for independent reproduction.

### Sensor-shift observation

The supplied summary shows ST3's NG rate rising from 3.3% on 12 October to 17.0% on 13 October, coinciding with a change from microphone MX-200 to MX-350. Mean sound level rises by approximately 2.9 dB. Six of eight failed units retested at another station passed.

This pattern is consistent with a possible measurement shift and false-alarm increase, but it is not conclusive: the observation spans only two days, the microphone change coincides with the date change, and the retest sample is small.

## Part 2 — Research direction

`part2/research_note.md` describes a proposed shift-versus-surge investigation using robust distribution movement and tail behaviour. It is a research hypothesis and evaluation plan, not a validated implementation.

## Setup

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

The notebooks expect the original audio and image datasets in a `part1_inspection/` directory. Those raw media files and labels are not bundled. Supply the original inputs before running feature extraction and model training.

## Reproducibility and limitations

- Metrics are transcribed from the supplied saved validation artifacts.
- Validation thresholds differ from the thresholds used for the saved test predictions.
- Held-out test labels are hidden; test performance cannot be evaluated.
- The validation set contains very few NG examples.
- The visual feature space (8,114 features) is high-dimensional relative to 225 training rows.
- Raw media, Part 3 source CSVs/images, and large intermediate feature caches are not included.
- AI assistance is disclosed in `docs/ai_assistance.md`.

## Technology

Python, NumPy, Pandas, librosa, scikit-learn, scikit-image, Matplotlib, Pillow, and Jupyter Notebook.
