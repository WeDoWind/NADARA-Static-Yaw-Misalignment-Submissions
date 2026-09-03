# Submissions

Add your file here by pull request, named `Results_NN_TIER_x.csv`.

- Header: `turbine_id,date,yaw_misalignment_deg,cluster`
- Exactly **731 rows** — every turbine/date pair in the template for your round:
  `submission_template_validate.csv` for a numbered entry, `submission_template_final.csv` for `_final`
- `yaw_misalignment_deg`: finite float, within ±90 degrees
- `cluster`: optional tie-breaker. Fill every row to enter, or leave empty to skip
- Tracked with Git LFS (see [.gitattributes](../.gitattributes))
- Immutable once merged — submit a new number to revise

`Results_0_T0_0.csv` and `Results_0_T0_final.csv` are all-zero examples you can copy.
`TIER` is `TK` — K is how many labelled turbines your method needed (`T0` none, `T3`
all three train turbines, `T4` also the scored turbine). See the
[README](../README.md#submitting).

Check your file before opening the PR:

```bash
python ../validate_submission.py Results_42_T0_0.csv
```
