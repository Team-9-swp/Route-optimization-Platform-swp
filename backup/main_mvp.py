#!/usr/bin/env python3
import subprocess
import sys


def solve(instance, seed, time_budget=900, time_limit=None, max_restarts=None):
    from solver import solve as _solve
    return _solve(instance, time_limit=time_budget if time_limit is None else time_limit, seed=seed)


def main():
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    cmd = [sys.executable, "solver.py"] + args
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
