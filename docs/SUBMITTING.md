# How to submit

## 1. Prepare your file

Create a CSV with one row per turbine-day:

```
turbine_id,date,yaw_misalignment_deg,cluster
PPP_WTG17,2023-01-01,-8.1,0
PPP_WTG17,2023-01-02,-8.0,0
...
```

- **731 rows** — every turbine/date pair in the template for your round:
  `submission_template_validate.csv` for a numbered entry (PPP-17),
  `submission_template_final.csv` for `_final` (SSS-06)
- All values must be finite floats, within +/-90 degrees
- Predictions are asked for every day. Only days with a real label outside a
  transition window are scored; the rest are ignored, not penalised

`cluster` is the optional tie-breaker column: group days sharing a misalignment
state. Labels are arbitrary and only need to be consistent within a turbine. Fill
every row to enter, or leave the column empty to skip.

## 2. Name your file

```
Results_NN_TIER_x.csv
```

| Part | Meaning | Examples |
|---|---|---|
| `NN` | Your participant ID (from registration) | `42` |
| `TIER` | Method tier: `U`, `S`, or `CK` (K = reference turbines) | `U`, `S`, `C5` |
| `x` | Submission number, starting at 0 | `0`, `1`, `2` |

For the final private-test submission use `final` instead of a number:
`Results_42_U_final.csv`.

## 3. Open a pull request

1. Fork or branch this repo
2. Add your file under `Submissions/`
3. Open a PR — the automated format check runs immediately (no labels, no scoring yet)
4. A maintainer reviews and merges
5. Scoring runs automatically within a few minutes; the leaderboard updates

## Notes

- Files are stored via **Git LFS** — make sure LFS is installed (`git lfs install`)
- Once merged, a submission is **immutable** — add a new numbered file to revise
- The leaderboard shows your **best** submission per tier
- Ground truth is never exposed; scoring runs in a separate private repository
