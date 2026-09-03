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
| `validate.parquet` | PPP-17 | no, public leaderboard |
| `test.parquet` | SSS-06 | no, final round, scored once at the deadline |
| `context.parquet` | 11 others | no |

Test SCADA is published; only its labels are withheld. Use it freely for
unsupervised or transductive work. The evaluation of test data results will be
done at the end of the challenge.

`turbine_locations_PPP.csv` and `turbine_locations_SSS.csv` give the layout one
file per site. `x_m` is easting, `y_m` northing.

Signals: `Power`, `WindSpeed`, `WindDir`, `NacDir`, `PitchAngle`, `RotSpeed`,
`GenSpeed`. Vane angle can be derived as `WindDir - NacDir`, wrapped
to ±180°.

`train.parquet` carries **every day**, labelled or not, so you can use the full two
years. `yaw_misalignment_deg` is null on unlabelled days.

Values are only present on change in the high-res stream: a null means "unchanged
since the last update", not "missing". Forward fill it.

## Submitting

By pull request, adding files under `Submissions/`. Format is checked immediately;
scoring runs when a maintainer merges.

**`Results_NN_TIER_x.csv`** where `NN` is your participant ID, `TIER` has the form
`TK` (`K` being how many labelled wind turbines your method needed) and `x` is the
submission number, or `final` for the private test.

| Tier | Labelled turbines used | What it claims |
|---|---|---|
| `T0` | none | Unsupervised or physics-based: works with no labels anywhere |
| `T1` | one of PPP-12 / 13 / 14 | |
| `T2` | two of PPP-12 / 13 / 14 | |
| `T3` | all three train turbines | Transfers to a turbine it has never seen labelled |
| `T4` | the train turbines **plus** labels from the scored turbine itself | Few-shot calibration on the turbine being scored |

The tiers are ordered by how much field measurement the method needs before it can be
trusted on a new turbine. `T0` is the strongest claim — no campaign anywhere, so it
rolls out across a fleet immediately. `T4` is the weakest, because it needs a campaign
on **every** turbine you want to assess, which is the throughput problem this challenge
exists to solve. `T4` is therefore **penalised when choosing the final winner**.

Note this runs the opposite way to generalisation: `T0` is the hardest test of it and
`T4` the softest, since `T4` has already seen the answer on the turbine it is scored on.

Labels from the scored turbine (PPP-17 in the numbered rounds, SSS-06 in the final)
will be capped at **14 days**, roughly what one measurement campaign occupies. How
those days are released has not been settled yet — this section will be updated before
any of them are available, and until then no `T4` submission can be made.

The submission counter is **per tier**, so `Results_42_T0_0.csv` and
`Results_42_T3_0.csv` are both valid first submissions. Enter as many tiers as you
like. The board keeps your best in each, so a `T3` entry never hides your `T0` one.

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

**`cluster`** is the optional tie-breaker, in the same file. Group the days that
share a misalignment state.
The value does not matter, only which days belong together.
Labels are arbitrary and only have to be consistent within a turbine. We are not
telling you how many states there are: working that out is part of it.

Fill the column on every row to enter, or leave it empty to skip. A partly filled
column is rejected.

Skipping it scores **ARI 0.00**, and for ranking anything below zero counts as zero
too. So entering the tie-breaker can only help you: a grouping that lands at or
below chance leaves you exactly where declining it would have. Where a band ties at
zero, RMSE decides.

A below-chance score is still **reported** with its sign, because it tells you
something — ARI ignores what you name your clusters, so a negative value means the
grouping itself disagrees with the real states, not that the labels are inverted.

If you predict the value well, clustering is trivial: just bin your own
predictions. It is kept because it is reachable by routes the primary metric is
not: unsupervised methods that can tell a turbine's states apart without ever
calibrating them to degrees, and physics-based approaches that detect a change in
behaviour without pinning down its magnitude. Those are worth rewarding even when
the absolute number is out of reach.

`Submissions/Results_0_T0_0.csv` and `Results_0_T0_final.csv` are all-zero examples you
can copy, one per round.

Submissions are immutable once merged; submit a new number to revise.

## Scoring

Ranked on **RMSE**, MAE alongside. Clustering breaks ties, scored per turbine with
the Adjusted Rand Index.

The tie-breaker is not decorative. Scored days are heavily autocorrelated: a run of
days at one misalignment level is effectively a single observation, so the effective
sample size is the number of misalignment states, not the number of days. Most RMSE
differences are smaller than the noise.

Which differences are real is decided by a **paired bootstrap**. Whole states are
resampled, never individual days, and every submission is scored on the same
resampled draw — so the luck of a draw (an easy stretch pulled twice, a hard one
missed) lands on everyone at once and cancels when two submissions are compared.

Going down the RMSE order, a submission that is not provably better than the leader
of the band above it joins that band. Submissions sharing a **band** are statistically
tied on RMSE, and the clustering ARI decides their order. The board reports `band`
and `gap_vs_lead`: the RMSE margin you would need over your band's leader to be
provably ahead of it.

**Baselines.** The best single constant scores **RMSE 3.35 on the private test** and
**4.80 on validate**, and on the test it lands in the same band as the all-zero
example. The two are not separable. A test result near 3.4 says nothing about whether
you have a model. Note the two rounds are not comparable: a constant is a strong
baseline on the test turbine and a weak one on validate.

For clustering, the real states are contiguous in time, so cutting the calendar
into a few blocks scores ARI 0.53 / 0.65 with no SCADA read at all. **Do not use
calendar adjacency between scored days.** Rows ship shuffled, but dates are kept
because you need them to find the SCADA. **This is an honour-system rule.**

## Things worth knowing about this data

- **Signals are rescaled for anonymity.** Power, wind speed, generator and rotor
  speed and pitch each carry an undisclosed constant factor, the same for every
  turbine. Relationships survive; absolute values and anything derived from them
  (power coefficient, tip-speed ratio) do not. Directions are unscaled.
- **Anemometer calibrations get changed.** This can put a step in a turbine's
  wind-speed-to-power relationship that has nothing to do with yaw. At least one
  turbine here has one.
- **Turbines might genuinely see different wind.** Complex terrain, varying hub heights;
  persistent 10–15% offsets between turbines might be real.
- **Labels are smoothed.** The daily series behaves like a rolling estimate and
  drifts for about a week before each visible step. Those days are not scored.
- **The obvious method does not work out of the box.** An OpenOA-style
  power-versus-vane fit tracks a change *within* a turbine well, but ranks the
  three training turbines in the wrong order.
- **Check your sign before you submit.** A submission with the right magnitudes and
  the wrong sign scores worse than any constant while clustering perfectly — it is a
  solved problem thrown away on a convention. The board reports `bias` (mean predicted
  minus true); if yours is large and close in size to your MAE, suspect an inversion
  rather than a bad model.

## Checking your file locally

```bash
python validate_submission.py Submissions/Results_42_T0_0.csv
```
