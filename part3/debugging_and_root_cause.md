# Debugging notes and root-cause investigation

## Issue 1 — Missing sound-level readings
- **Symptom:** blank or `--` values caused numeric processing to fail or rows to be lost.
- **Fix:** coerce sound-level values to numeric with invalid entries represented as NaN. Keep the test rows and report the missing-reading count.

## Issue 2 — Retests counted more than once
- **Symptom:** repeated tests for the same unit inflated station totals.
- **Fix:** stable-sort by test timestamp and retain the latest test per unit before station/day aggregation.

## Issue 3 — Incorrect microphone attribution
- **Symptom:** tests could be attributed to the wrong microphone when a station had multiple historical microphone records.
- **Root cause:** joining on station alone ignores installation dates.
- **Fix:** match each test timestamp to the microphone's installed_from / installed_to interval. Raise an error for unmatched tests or overlapping installation records rather than silently accepting incorrect attribution.

## Issue 4 — Camera ROI coordinates swapped
- **Symptom:** brightness values did not match the intended camera region.
- **Root cause:** NumPy image arrays use [row, column] indexing, equivalent to [y, x].
- **Fix:** slice the configured region as frame[y0:y1, x0:x1].

## Sensor-shift investigation

The supplied output shows ST3's NG rate at 3.3% on 12 October (MX-200) and 17.0% on 13 October (MX-350). Mean sound level rises from 62.2 dB to 65.1 dB, approximately +2.9 dB. Six of eight failed units retested at another station passed.

This is consistent with a possible microphone-related measurement shift, but does not prove it. The observation spans two days, microphone change and date change coincide, and the retest sample is small and potentially biased.

### Recommended next checks
1. Confirm microphone model, gain, sensitivity, mounting, distance, angle, cabling, and preamplifier settings.
2. Measure a known-good golden unit with both microphone configurations.
3. Retest a representative sample of flagged and unflagged units at an independently calibrated station.
4. Check ambient noise and process settings at the affected station.
5. If sensor baselines are updated, avoid learning them solely from potentially defective production units; prefer a golden reference and retain an independent alarm for extreme deviations.
