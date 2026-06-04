# How to submit

## 1. Prepare your file

Create a CSV with exactly two columns:

```
session_id,yaw_misalignment_deg
validate-0,1.23
validate-1,-7.8
...
```

- **857 rows** for the validate leaderboard (session_ids from `submission_template.csv`)
- **813 rows** for the final test (use `_final` suffix — see below)
- All values must be finite floats

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
`Results_42_U_final.csv`

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
