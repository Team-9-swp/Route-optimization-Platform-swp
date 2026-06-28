# Greedy Loader Stage Impact Analysis

## Setup

- Instances: `instances/i*.json` (10 official fixtures)
- Seed: `42`
- Solver time limit per instance: `60 s`
- Full pipeline: vehicle routing → greedy loaders → Loader SA refinement
- Greedy-only pipeline: vehicle routing → greedy loaders (Loader SA skipped)

## Results

| Instance | Full pipeline cost | Greedy-only cost | Difference (%) | Full runtime (s) | Greedy runtime (s) |
|---|---|---:|---:|---:|---:|
| i1.json | 13192.44 | 13457.44 | -1.97 | 40.25 | 29.27 |
| i2.json | 33268.56 | 33268.56 | 0.00 | 24.60 | 10.33 |
| i3.json | 22417.94 | 23287.94 | -3.88 | 54.17 | 29.35 |
| i4.json | 93706.58 | 96051.28 | -2.50 | 54.33 | 29.44 |
| i5.json | 37295.98 | 37599.73 | -0.81 | 54.34 | 29.60 |
| i6.json | 95431.67 | 92637.81 | +2.93 | 54.66 | 30.34 |
| i7.json | 241506.80 | 239186.78 | +0.96 | 54.95 | 30.52 |
| i8.json | 182919.09 | 185554.47 | -1.44 | 54.93 | 30.55 |
| i9.json | 501514.58 | 499709.30 | +0.36 | 55.17 | 30.71 |
| i10.json | 101572.95 | 102017.94 | -0.44 | 55.54 | 31.12 |

*Difference = ((full - greedy) / full) × 100. Positive value means the full pipeline is better (lower cost).*

## Observations

1. **Objective impact is small.** The Loader SA refinement changes the final objective by less than ±4 % on every instance and by less than ±1 % on five of ten instances.
2. **Loader SA is not universally better.** On `i6.json`, `i7.json`, and `i9.json` the greedy assignment already produced a lower-cost solution than the refined result. This is expected from a stochastic local-search phase that is seeded from the greedy solution.
3. **Runtime reduction is significant.** Skipping Loader SA saves roughly 20–25 seconds per instance (≈ 40 % of the full runtime), because the parallel SA chains are no longer executed.
4. **Quality/time trade-off.** For short time limits the greedy-only mode is attractive: it preserves feasibility, keeps skipped optional orders unchanged, and returns a result much faster.

## Conclusion

The greedy loader assignment is already a viable stand-alone stage. The optional `skip_loader_refinement` flag (added to `beta_code.pipeline.orchestrate.solve`) lets the operator choose between:

- **full pipeline** — slightly better average objective when compute budget allows;
- **greedy-only pipeline** — fast, deterministic-enough results when runtime matters.

For the Assignment 4 increment the flag is exposed through `scripts/benchmark.py --skip-loader-refinement` and can be wired into the API or runner later if the customer wants a fast mode.
