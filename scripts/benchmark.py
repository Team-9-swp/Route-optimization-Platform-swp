import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from beta_code.pipeline.orchestrate import solve


def run_benchmark(instances_dir, report_path, time_limit, seed):
    instance_files = sorted(Path(instances_dir).glob("i*.json"))
    results = []
    for path in instance_files:
        with open(path) as f:
            instance = json.load(f)
        print(f"Running {path.name} ...")
        start = time.time()
        try:
            solution = solve(
                instance,
                time_limit=time_limit,
                seed=seed,
            )
        except Exception as exc:
            elapsed = time.time() - start
            results.append({
                "instance": path.name,
                "status": "ERROR",
                "objective_value": None,
                "runtime_s": round(elapsed, 2),
                "unserved_optional": None,
                "error": f"{type(exc).__name__}: {exc}",
            })
            continue

        elapsed = time.time() - start
        if solution is None:
            results.append({
                "instance": path.name,
                "status": "FAILED",
                "objective_value": None,
                "runtime_s": round(elapsed, 2),
                "unserved_optional": None,
            })
        else:
            objective_value = solution.get("objective_value")
            if objective_value is None:
                objective_value = solution.get("_cost")
            results.append({
                "instance": path.name,
                "status": "OK",
                "objective_value": round(objective_value, 2),
                "runtime_s": round(elapsed, 2),
                "unserved_optional": len(solution.get("unserved_optional", [])),
            })
    write_report(results, report_path, time_limit, seed)
    return results


def write_report(results, report_path, time_limit, seed):
    Path(report_path).parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Solver Benchmark Report",
        "",
        "- Solver: PyVRP + Nevergrad",
        f"- Time limit per instance: {time_limit}s",
        f"- Seed: {seed}",
        f"- Instances: {len(results)}",
        "",
        "| Instance | Status | Objective | Runtime (s) | Skipped optional |",
        "|---|---|---|---|---|",
    ]
    for r in results:
        lines.append(
            f"| {r['instance']} | {r['status']} | {r['objective_value']} | {r['runtime_s']} | {r['unserved_optional']} |"
        )
    Path(report_path).write_text("\n".join(lines), encoding="utf-8")
    print(f"Report written to {report_path}")


def main():
    parser = argparse.ArgumentParser(description="Run solver benchmark on competition instances.")
    parser.add_argument("--instances-dir", default="instances", help="Directory containing i*.json instances")
    parser.add_argument("--report-path", default="reports/week4/solver-benchmark.md", help="Output markdown report path")
    parser.add_argument("--time-limit", type=float, default=420, help="Solver time limit per instance in seconds")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    run_benchmark(args.instances_dir, args.report_path, args.time_limit, args.seed)


if __name__ == "__main__":
    main()
