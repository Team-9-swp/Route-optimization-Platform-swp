#!/usr/bin/env python3

from solver import solve as _solve
from solver import main as _main


def solve(instance, seed, time_budget=900, time_limit=None, max_restarts=None):
    return _solve(
        instance,
        time_limit=time_budget if time_limit is None else time_limit,
        seed=seed,
    )


def main():
    _main()


if __name__ == "__main__":
    main()
