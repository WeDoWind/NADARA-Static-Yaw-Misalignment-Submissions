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
| `TIER` | `TK`, where K is how many labelled turbines your method needed | `T0`, `T3`, `T4` |
| `x` | Submission number, starting at 0 — **counted separately per tier** | `0`, `1`, `2` |

| Tier | Labelled turbines used |
|---|---|
| `T0` | none — unsupervised or physics-based |
| `T1` / `T2` | one or two of the train turbines (PPP-12 / 13 / 14) |
| `T3` | all three train turbines |
| `T4` | the train turbines plus labels from the scored turbine itself |

Tiers rank by how much field measurement the method needs before it can be trusted
on a new turbine, so `T0` is the strongest claim and `T4` the weakest. `T4` is
penalised when the final winner is chosen, and is not yet open — the rules for
releasing scored-turbine labels are still being finalised. See the main
[README](../README.md#submitting).

The counter runs per tier, so `Results_42_T0_0.csv` and `Results_42_T3_0.csv` are
both valid first submissions and do not clash. Enter as many tiers as you like;
the leaderboard keeps your best entry in each tier rather than making them compete
with one another.

For the final private-test submission use `final` instead of a number:
`Results_42_T0_final.csv`.

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
