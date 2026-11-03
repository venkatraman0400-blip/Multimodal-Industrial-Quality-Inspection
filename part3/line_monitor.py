"""Daily production-line quality summary.

Usage:
    python line_monitor.py <input_folder>

Expected input:
    test_log.csv      unit_id, station, test_time, level_db, result
    station_mics.csv station, mic_model, installed_from, installed_to
    frames/           ST1.png, ST2.png, ... (640 x 480 grayscale)
"""
from pathlib import Path
import sys

import numpy as np
import pandas as pd
from PIL import Image

ALARM_RATE = 0.08
DARK_LIMIT = 0.35
ROI = {
    "ST1": (400, 180, 560, 300),
    "ST2": (420, 170, 580, 290),
    "ST3": (390, 190, 550, 310),
    "ST4": (410, 175, 570, 295),
}


def load_tests(folder):
    folder = Path(folder)
    log = pd.read_csv(folder / "test_log.csv")
    log["test_time"] = pd.to_datetime(log["test_time"])
    log["level_db"] = pd.to_numeric(log["level_db"], errors="coerce")
    missing = int(log["level_db"].isna().sum())
    return log, missing


def final_results(log):
    ordered = log.sort_values("test_time", kind="stable")
    return ordered.drop_duplicates("unit_id", keep="last").copy()


def attach_mics(tests, folder):
    folder = Path(folder)
    mics = pd.read_csv(
        folder / "station_mics.csv",
        parse_dates=["installed_from", "installed_to"],
    )
    source = tests.copy().reset_index(drop=True)
    source["_source_row"] = np.arange(len(source))
    joined = source.merge(mics, on="station", how="left")
    valid = (
        (joined["test_time"] >= joined["installed_from"])
        & (
            joined["installed_to"].isna()
            | (joined["test_time"] <= joined["installed_to"])
        )
    )
    matched = joined.loc[valid].copy()
    counts = matched["_source_row"].value_counts()
    unmatched_count = int(source["_source_row"].nunique() - counts.index.nunique())
    duplicated_count = int((counts > 1).sum())
    if unmatched_count:
        raise ValueError(
            f"No microphone installation record matched {unmatched_count} test(s)."
        )
    if duplicated_count:
        raise ValueError(
            f"{duplicated_count} test(s) matched multiple microphone records; "
            "check installation date boundaries."
        )
    return matched.drop(columns="_source_row")


def station_summary(tests):
    tests = tests.copy()
    tests["day"] = tests["test_time"].dt.date.astype(str)
    tests["is_ng"] = tests["result"].eq("NG")
    grouped = tests.groupby(["station", "day"], sort=True)
    out = pd.DataFrame({
        "units": grouped.size(),
        "ng": grouped["is_ng"].sum(),
        "mean_level_db": grouped["level_db"].mean(),
        "mic": grouped["mic_model"].first(),
    }).reset_index()
    out["ng_rate"] = out["ng"] / out["units"]
    out["alarm"] = np.where(out["ng_rate"] > ALARM_RATE, "ALARM", "-")
    return out


def camera_check(folder):
    folder = Path(folder)
    rows = []
    for station, (x0, y0, x1, y1) in ROI.items():
        image_path = folder / "frames" / f"{station}.png"
        frame = np.asarray(
            Image.open(image_path).convert("L"), dtype=float
        ) / 255.0
        patch = frame[y0:y1, x0:x1]
        brightness = float(patch.mean())
        status = "LOW" if brightness < DARK_LIMIT else "OK"
        rows.append((station, brightness, status))
    return rows


def main(folder):
    log, missing = load_tests(folder)
    tests = attach_mics(final_results(log), folder)
    summary = station_summary(tests)

    print(
        f"{'station':<8}{'day':<12}{'mic':<9}{'units':>6}"
        f"{'ng':>5}{'ng_rate':>9}{'mean_level_db':>15}  alarm"
    )
    for row in summary.itertuples():
        mean_level = (
            f"{row.mean_level_db:.1f}"
            if pd.notna(row.mean_level_db)
            else "NaN"
        )
        print(
            f"{row.station:<8}{row.day:<12}{row.mic:<9}"
            f"{row.units:>6}{row.ng:>5}{row.ng_rate:>9.3f}"
            f"{mean_level:>15}  {row.alarm}"
        )
    print(f"MISSING_LEVEL_READINGS {missing}")
    for station, brightness, status in camera_check(folder):
        print(f"CAMERA {station} brightness {brightness:.3f} {status}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python part3/line_monitor.py <input_folder>")
    main(sys.argv[1])
