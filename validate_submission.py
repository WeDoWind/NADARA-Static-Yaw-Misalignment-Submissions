#!/usr/bin/env python3
"""Structural validation for a NADARA Yaw Misalignment challenge submission.

Runs in the PUBLIC repo's PR workflow — has NO access to ground-truth labels.
Only checks that the submission is well-formed; actual scoring happens after
merge, in the private evaluation repo.

Submission filename format:
  Results_NN_TIER_x.csv       (x = submission number)   → validate split
  Results_NN_TIER_final.csv   (final submission)         → private test split

TIER is one of:
  U           unsupervised (no labelled data at deployment time)
  CK          calibrated with K reference turbines (e.g. C5)
  S           fully supervised (per-turbine measurement required)

A valid submission:
  - filename matches the pattern above
  - has exactly the header:  session_id,yaw_misalignment_deg
  - has the correct number of rows for the split (857 validate / 813 test)
  - every session_id matches the expected prefix exactly once
  - yaw_misalignment_deg is a finite float on every row

Usage:
    python validate_submission.py Submissions/Results_42_U_0.csv
Exit 0 = valid, 1 = invalid.
"""

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

SPLITS = {
    "validate": {"prefix": "validate-", "n": 857},
    "test":     {"prefix": "test-",     "n": 813},
}

FILENAME_RE = re.compile(r"^Results_(\d+)_(U|S|C(\d+))_(\d+|final)\.csv$")


def split_for(suffix: str) -> str:
    return "test" if suffix == "final" else "validate"


def fail(msg: str) -> None:
    print(f"::error::{msg}", file=sys.stderr)


def validate(path: Path) -> list[str]:
    errors: list[str] = []

    m = FILENAME_RE.match(path.name)
    if not m:
        errors.append(
            f"Filename '{path.name}' must match "
            "Results_NN_(U|S|CK)_(NUM|final).csv  "
            "(NN=participant id, TIER=U/S/C5/etc., NUM=submission number)."
        )
        return errors

    cfg = SPLITS[split_for(m.group(4))]
    n, prefix = cfg["n"], cfg["prefix"]

    try:
        df = pd.read_csv(path, dtype={"session_id": str})
    except Exception as e:
        errors.append(f"Cannot parse CSV: {e}")
        return errors

    if list(df.columns) != ["session_id", "yaw_misalignment_deg"]:
        errors.append(
            f"Header must be exactly 'session_id,yaw_misalignment_deg'; "
            f"got {list(df.columns)}."
        )
        return errors

    if len(df) != n:
        errors.append(f"Expected {n:,} rows for this split; found {len(df):,}.")

    bad_ids = df[~df["session_id"].str.match(rf"^{re.escape(prefix)}\d+$")]
    if not bad_ids.empty:
        examples = bad_ids["session_id"].head(3).tolist()
        errors.append(
            f"{len(bad_ids)} session_id(s) don't match '{prefix}<N>' format "
            f"(e.g. {examples})."
        )

    if df["session_id"].duplicated().any():
        dups = df["session_id"][df["session_id"].duplicated()].unique()[:3].tolist()
        errors.append(f"Duplicate session_id(s): {dups}.")

    yaw = pd.to_numeric(df["yaw_misalignment_deg"], errors="coerce")
    n_bad = int(yaw.isna().sum())
    if n_bad:
        errors.append(f"{n_bad} yaw_misalignment_deg value(s) are empty or non-numeric.")
    if n_bad == 0:
        non_finite = ~np.isfinite(yaw.to_numpy(dtype=float))
        if non_finite.any():
            errors.append(
                f"{int(non_finite.sum())} yaw_misalignment_deg value(s) are NaN or infinite."
            )

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        fail("usage: validate_submission.py <Results_NN_TIER_x.csv>")
        return 1
    path = Path(sys.argv[1])
    if not path.exists():
        fail(f"File not found: {path}")
        return 1
    errors = validate(path)
    if errors:
        fail(f"{path.name} is INVALID:")
        for e in errors:
            fail(f"  - {e}")
        return 1
    print(f"OK: {path.name} is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
