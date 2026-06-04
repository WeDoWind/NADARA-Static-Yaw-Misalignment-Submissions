# Submissions

Add your results file here via a pull request. See [../docs/SUBMITTING.md](../docs/SUBMITTING.md) for full instructions.

- Filename: `Results_NN_TIER_x.csv` (e.g. `Results_42_U_0.csv`, `Results_42_C5_0.csv`)
- Header: `session_id,yaw_misalignment_deg`
- Exactly **857 rows** for the validate split, **813 rows** for the final test split
- Finite float predictions only — no NaN or empty values
- Files are tracked with **Git LFS** (see [../.gitattributes](../.gitattributes))
- Submissions are **immutable** once merged — add a new file to revise
