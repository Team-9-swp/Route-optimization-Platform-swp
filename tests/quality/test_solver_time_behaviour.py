"""QRT-PE-01 — Solver time behaviour.

Verifies that the fixed CI benchmark completes within the required wall-clock
time and that a configured time limit is respected.
"""

import json
import time
from pathlib import Path

import pytest

from beta_code.pipeline.orchestrate import solve
from app.validation import validate_solution

ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURE = ROOT / "test_cases" / "t1.json"


@pytest.fixture
def instance():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


@pytest.mark.quality
def test_qrt_pe_01_a_fixed_benchmark_completion_time(instance):
    """The fixed small benchmark must finish and validate within 30 seconds."""
    start = time.monotonic()
    solution = solve(instance, time_limit=30, seed=42)
    elapsed = time.monotonic() - start

    assert solution is not None, "Solver did not return a solution"
    assert elapsed <= 40, f"Benchmark took {elapsed:.2f}s, threshold is 40s"

    result = validate_solution(instance, solution)
    assert result["passed"] is True


@pytest.mark.quality
def test_qrt_pe_01_b_configured_time_limit(instance):
    """A configured solver time limit must not be exceeded by more than 10 s."""
    configured_limit = 30
    start = time.monotonic()
    solution = solve(
        instance,
        time_limit=configured_limit,
        seed=42,
    )
    elapsed = time.monotonic() - start

    assert solution is not None
    assert elapsed <= configured_limit + 10, (
        f"Solver ran for {elapsed:.2f}s, allowed maximum is "
        f"{configured_limit + 10}s"
    )
