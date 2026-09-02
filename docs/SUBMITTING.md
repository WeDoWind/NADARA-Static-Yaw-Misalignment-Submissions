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
  transition window are scored; the rest are ignored, not penalised.

## 2. Name your file

```
Results_NN_TIER_x.csv
```

| Part | Meaning | Examples |
|---|---|---|
| `NN` | Your participant ID (from registration) | `42` |
| `TIER` | Method tier: `U`, `S`, or `CK` (K = reference turbines) | `U`, `S`, `C5` |
| `x` | Submission number, starting at 0 — **counted separately per tier** | `0`, `1`, `2` |

The counter runs per tier, so `Results_42_U_0.csv` and `Results_42_S_0.csv` are
both valid first submissions and do not clash. Enter as many tiers as you like;
the leaderboard keeps your best entry in each tier rather than making them
compete with one another. `C3` and `C5` count as the same calibrated tier.

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
