"""Solver registry — new solvers register here via VehicleSolver.__init_subclass__."""

from typing import Dict, Type

from beta_code.solvers.base import VehicleSolver

REGISTRY: Dict[str, Type[VehicleSolver]] = {}


def _auto_register():
    """Walk subclasses of VehicleSolver and register them by name."""
    for sub in VehicleSolver.__subclasses__():
        name = getattr(sub, "_solver_name", sub.__name__)
        REGISTRY[name] = sub


# Force registration at import time
_auto_register()


def get_solver(name: str) -> Type[VehicleSolver]:
    if name not in REGISTRY:
        raise KeyError(f"Unknown solver '{name}'. Available: {list(REGISTRY)}")
    return REGISTRY[name]
