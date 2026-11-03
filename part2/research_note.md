# Research note: distinguishing sensor shift from a genuine defect surge

## Question
When a station's non-conformance (NG) rate rises after a sensor replacement, is the change caused by a real increase in product defects or by a shift in the measurement system?

## Proposed approach

1. Establish a baseline distribution for each station and sensor configuration using known-good reference units and recent production readings.
2. Track robust location and spread statistics (median, median absolute deviation, and selected quantiles) rather than relying only on the mean.
3. Compare the full score distribution before and after a sensor change. A broad shift affecting OK-like readings may indicate calibration or gain drift; a heavier upper tail may be more consistent with a subset of defective units.
4. Retest a sample of flagged units on an independent, calibrated station and record the paired outcomes.
5. Keep a sensor-installation history so each measurement is associated with the hardware active at its timestamp.

## Interpretation safeguards

A distribution shift is not proof of sensor drift. Product mix, process settings, environmental conditions, operator changes, and genuine defects can also change the observed distribution. Use golden-unit checks, matched retests, and controlled comparisons before recalibrating thresholds.

## Status
This document is a research direction and evaluation plan. It is not a validated model or an experimentally proven root-cause detector.
