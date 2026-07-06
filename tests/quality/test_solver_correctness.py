"""QRT-FC-01 — Solver functional correctness.

Verifies that the solver returns zero hard-constraint violations for
representative supported inputs (small instance, optional orders, loader
assignments).
"""

import json
from pathlib import Path

import pytest

from beta_code.pipeline.orchestrate import solve
from app.validation import validate_solution

pytestmark = [pytest.mark.qrt, pytest.mark.quality]

ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURE = ROOT / "test_cases" / "t1.json"


@pytest.fixture(scope="module")
def instance():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def solution(instance):
    """Solve once and reuse the result for all correctness checks."""
    sol = solve(instance, time_limit=60, seed=42)
    assert sol is not None, "Solver returned no solution"
    return sol


def test_qrt_fc_01_a_small_deterministic_instance(instance, solution):
    """A small reference instance must be solved without hard violations."""
    result = validate_solution(instance, solution)
    assert result["passed"] is True
    assert result["report"]["total_violations"] == 0


def test_qrt_fc_01_b_optional_orders(instance, solution):
    """Optional orders may be skipped, but mandatory orders must be feasible."""
    result = validate_solution(instance, solution)
    assert result["passed"] is True
    assert "unserved_optional" in solution

    optional_ids = {o["id"] for o in instance["orders"] if o.get("optional")}
    unserved = set(solution.get("unserved_optional", []))
    served_optional = optional_ids - unserved

    # Every served optional order must appear in a vehicle route.
    routed_orders = {
        order
        for route in solution.get("vehicles", [])
        for order in route.get("route", [])
        if order != 0
    }
    assert served_optional.issubset(routed_orders)


def test_qrt_fc_01_c_loader_assignment(instance, solution):
    """A loader-requiring instance must produce valid loader routes."""
    result = validate_solution(instance, solution)
    assert result["passed"] is True
    assert solution.get("loaders"), "Expected at least one loader route"

    loader_required = any(o.get("loader_cnt", 0) > 0 for o in instance["orders"])
    assert loader_required, "Fixture should require loader assignments"
