# NADARA Static Yaw Misalignment Challenge — Submissions

Leaderboard repository. Predict the daily WindFit yaw misalignment value for a
turbine from its SCADA.

Live leaderboard: **https://wedowind.github.io/NADARA-Static-Yaw-Misalignment-Submissions/**

## Data

High-resolution SCADA (~12 s), 2023-01-01 to 2024-12-31, 16 turbines across two
anonymised sites. Available on SwitchDrive with a `metadata.croissant.json`
sidecar.

| File | Turbines | Labels |
|---|---|---|
| `train.parquet` | PPP-12, PPP-13, PPP-14 | yes, where WindFit measured |
| `validate.parquet` | PPP-17 | no — public leaderboard |
| `test.parquet` | SSS-06 | no — final round, scored once at the deadline |
| `context.parquet` | 11 others | no |

Test SCADA is published; only its labels are withheld. Use it freely for
unsupervised or transductive work.

`turbine_locations_PPP.csv` and `turbine_locations_SSS.csv` give the layout — one
file per site, since coordinates are relative to a different origin at each. Only
turbines whose SCADA ships are listed. `x_m` is easting, `y_m` northing; the layout
carries a constant scale factor applied to both axes, so distances stay
proportional and bearings between turbines are exact.

Signals: `Power`, `WindSpeed`, `WindDir`, `NacDir`, `PitchAngle`, `RotSpeed`,
`GenSpeed`. Vane angle is not supplied — derive it as `WindDir - NacDir`, wrapped
to ±180°.

`train.parquet` carries **every day**, labelled or not, so you can use the full two
years. `yaw_misalignment_deg` is null on unlabelled days.

Values are only present on change in the high-res stream: a null means "unchanged
since the last update", not "missing". Forward fill it.

## Submitting

By pull request, adding files under `Submissions/`. Format is checked immediately;
scoring runs when a maintainer merges.

**`Results_NN_TIER_x.csv`** — `NN` your participant ID, `TIER` one of `U`, `S`, or
`CK` (K reference turbines), `x` the submission number or `final` for the private
test.

```csv
turbine_id,date,yaw_misalignment_deg,cluster
PPP_WTG17,2023-01-01,-8.1,0
```

One row per turbine-day. **Each round has its own template**, so a leaderboard
entry never carries predictions for the held-out turbine:

| Round | Template | Turbine | Rows |
|---|---|---|---|
| numbered (`_0`, `_1`, …) | `submission_template_validate.csv` | PPP-17 | 731 |
| `_final` | `submission_template_final.csv` | SSS-06 | 731 |

Predictions are asked for every day; only days with a real label outside a
transition window are scored, and the rest are ignored rather than penalised.

**`cluster`** — optional tie-breaker, in the same file. Group the days that share a
misalignment state; the value does not matter, only which days belong together.
Labels are arbitrary and only have to be consistent within a turbine. We are not
telling you how many states there are — working that out is part of it.

Fill the column on every row to enter, or leave it empty to skip. A partly filled
column is rejected.

If you predict the value well, clustering is trivial — just bin your own
predictions. It is kept because it is reachable by routes the primary metric is
not: unsupervised methods that can tell a turbine's states apart without ever
calibrating them to degrees, and physics-based approaches that detect a change in
behaviour without pinning down its magnitude. Those are worth rewarding even when
the absolute number is out of reach.

`Submissions/Results_0_U_0.csv` is an all-zero example you can copy.

Submissions are immutable once merged; submit a new number to revise.

## Scoring

Ranked on **RMSE**, MAE alongside. Clustering breaks ties, scored per turbine with
the Adjusted Rand Index.

The tie-breaker is not decorative. Scored days are heavily autocorrelated — a run
of days at one misalignment level is effectively a single observation — so the
leaderboard resolves differences no finer than **±1.5 RMSE on validate and ±0.6 on
test**. The scorer prints that margin with every result. Submissions inside it are
tied, and the clustering score decides.

**Baselines.** A single constant scores RMSE 3.43 on the private test, which is
also what predicting that set's own mean would score. A result near 3.4 says
nothing about whether you have a model.

For clustering, the real states are contiguous in time, so cutting the calendar
into a few blocks scores ARI 0.53 / 0.65 with no SCADA read at all. **Do not use
calendar adjacency between scored days.** Rows ship shuffled, but dates are kept
because you need them to find the SCADA — so this is an honour-system rule.

## Things worth knowing about this data

- **Signals are rescaled for anonymity.** Power, wind speed, generator and rotor
  speed and pitch each carry an undisclosed constant factor, the same for every
  turbine. Relationships survive; absolute values and anything derived from them
  (power coefficient, tip-speed ratio) do not. Directions are unscaled.
- **Anemometer calibrations get changed.** This can put a step in a turbine's
  wind-speed-to-power relationship that has nothing to do with yaw. At least one
  turbine here has one.
- **Turbines genuinely see different wind.** Complex terrain, varying hub heights;
  persistent 10–15% offsets between turbines are real, not errors to remove.
- **Labels are smoothed.** The daily series behaves like a rolling estimate and
  drifts for about a week before each visible step. Those days are not scored.
- **The obvious method does not work out of the box.** An OpenOA-style
  power-versus-vane fit tracks a change *within* a turbine well, but ranks the
  three training turbines in the wrong order.

## Checking your file locally

```bash
python validate_submission.py Submissions/Results_42_U_0.csv
```
