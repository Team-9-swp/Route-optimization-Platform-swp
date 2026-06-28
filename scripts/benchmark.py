import json
import time
from pathlib import Path

from beta_code.pipeline.orchestrate import solve

INSTANCES_DIR = Path(__file__).parent.parent / "instances"
REPORT_PATH = Path(__file__).parent.parent / "reports" / "week4" / "solver-benchmark.md"
TIME_LIMIT = 420
SEED = 42


def run_benchmark():
    instance_files = sorted(INSTANCES_DIR.glob("i*.json"))
    results = []
    for path in instance_files:
        with open(path) as f:
            instance = json.load(f)
        print(f"Running {path.name} ...")
        start = time.time()
        solution = solve(instance, time_limit=TIME_LIMIT, seed=SEED)
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
            results.append({
                "instance": path.name,
                "status": "OK",
                "objective_value": solution.get("objective_value") or solution.get("_cost"),
                "runtime_s": round(elapsed, 2),
                "unserved_optional": len(solution.get("unserved_optional", [])),
            })
    return results


def write_report(results):
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Solver Benchmark Report",
        "",
        f"- Time limit per instance: {TIME_LIMIT}s",
        f"- Seed: {SEED}",
        f"- Instances: {len(results)}",
        "",
        "| Instance | Status | Objective | Runtime (s) | Skipped optional |",
        "|---|---|---|---|---|",
    ]
    for r in results:
        lines.append(
            f"| {r['instance']} | {r['status']} | {r['objective_value']} | {r['runtime_s']} | {r['unserved_optional']} |"
        )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report written to {REPORT_PATH}")


if __name__ == "__main__":
    results = run_benchmark()
    write_report(results)
