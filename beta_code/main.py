#!/usr/bin/env python3
"""
Entry point: selects the best solver for the instance and runs the pipeline.

Usage:
    python -m beta_code.main --input instance.json --output solution.json --time-limit 900
"""

import argparse
import json
import sys

from solver import solve


def main():
    parser = argparse.ArgumentParser(
        description="CVRPTW+Loader solver — adaptive pipeline"
    )
    parser.add_argument("--input", default="instance.json")
    parser.add_argument("--output", default="solution.json")
    parser.add_argument("--time-limit", type=int, default=900, help="seconds")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--solver", default=None,
                        help="Force a specific solver (default: auto-select)")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    print(f"Orders: {len(data['orders'])}, Time limit: {args.time_limit}s, "
          f"Seed: {args.seed}")

    result = solve(data, time_limit=args.time_limit, seed=args.seed)

    if result is None:
        print("FAILED: no solution found.")
        sys.exit(1)

    with open(args.output, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\nSolution saved to {args.output}")


if __name__ == "__main__":
    main()
