import sys
from pathlib import Path

_project_root = str(Path(__file__).resolve().parent.parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from solver import solve as _solve


def solve(problem_data, time_limit, seed):
    """Thin wrapper around the PyVRP + Nevergrad solver."""
    return _solve(problem_data, time_limit=time_limit, seed=seed)
