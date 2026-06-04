# NADARA Static Yaw Misalignment Challenge — Submissions

This is the official leaderboard repository for the NADARA Static Yaw Misalignment Challenge.

Participants submit predicted yaw misalignment angles for held-out 30-minute SCADA sessions. Submissions are scored against private ground truth on two leaderboards:

- **Model performance** — RMSE and MAE of the predicted yaw offset (degrees), regardless of method type.
- **Economic performance** — estimated fleet-scale annual energy savings if the method were deployed across Nadara's 2,000-turbine fleet, accounting for the practical deployability of the method.

Live leaderboard: **https://wedowind.github.io/NADARA-Static-Yaw-Misalignment-Submissions/**

## Submission tiers

Declare the tier that matches your method's deployment requirements:

| Tier | Code | What it needs at deployment | Turbines corrected in year 1 |
|---|---|---|---|
| Unsupervised | `U` | No labelled data | 2,000 (full fleet) |
| Calibrated | `C` + K | Labels from K reference turbines | 2,000 (full fleet) |
| Supervised | `S` | Fresh measurement per turbine | ~60 (Windfit throughput) |

## How to submit

Submissions are made by pull request. See **[docs/SUBMITTING.md](docs/SUBMITTING.md)** for full instructions.

In short:
1. Prepare your CSV file (see format below).
2. Open a PR adding it under `Submissions/`.
3. The automated format check runs immediately (no labels needed).
4. Once a maintainer merges your PR, scoring runs automatically and the leaderboard updates.

## Submission format

**Filename:** `Results_NN_TIER_x.csv`
- `NN` = your participant ID (assigned at registration)
- `TIER` = `U`, `S`, or `CK` where K is the number of reference turbines (e.g. `C5`)
- `x` = submission number (0, 1, 2, …)
- Final submission against private test: use `final` instead of a number

**Examples:** `Results_42_U_0.csv`, `Results_42_C5_1.csv`, `Results_42_S_final.csv`

**Content:**
```
session_id,yaw_misalignment_deg
validate-0,1.23
validate-1,-7.8
...
```
- Exactly **857 rows** (validate split) or **813 rows** (final / private test split)
- `session_id` must match the values in `submission_template.csv` (available on SwitchDrive)
- `yaw_misalignment_deg`: finite float, degrees
- Files are tracked with **Git LFS** (see [.gitattributes](.gitattributes))
- Submissions are **immutable** once merged — submit a new number to revise

## Sample submission

`Submissions/Results_99_U_0.csv` is a valid zero-prediction example you can use as a template.
