import json
import subprocess
import tempfile
from pathlib import Path

import pytest

from backup.validator import validate_solution, Validator


def _minimal_instance():
    return {
        "vehicle_capacity": 100,
        "vehicle_speed": 1,
        "loader_speed": 1,
        "vehicle_shift_size": 1000,
        "loader_shift_size": 1000,
        "depot": {"x": 0, "y": 0, "load_time": 0},
        "orders": [
            {
                "id": 1,
                "x": 3,
                "y": 4,
                "volume": 10,
                "time_window": [0, 100],
                "vehicle_service_time": 5,
                "loader_cnt": 0,
                "loader_service_time": 0,
                "optional": 0,
            },
            {
                "id": 2,
                "x": 6,
                "y": 8,
                "volume": 5,
                "time_window": [0, 100],
                "vehicle_service_time": 5,
                "loader_cnt": 0,
                "loader_service_time": 0,
                "optional": 0,
            },
        ],
        "weights": {
            "vehicle_salary": 1,
            "loader_salary": 1,
            "fuel_cost": 1,
            "loader_work": 1,
            "optional_order_penalty": 1,
        },
    }


def _minimal_solution():
    return {
        "vehicles": [
            {
                "id": 1,
                "route": [0, 1, 2, 0],
                "time": [5.0, 15.0],
            }
        ],
        "loaders": [],
    }


def test_validate_solution_passes_valid_solution():
    result = validate_solution(_minimal_instance(), _minimal_solution())
    assert result["total_violations"] == 0
    assert result["total_cost"] > 0


def test_validate_solution_fails_missing_mandatory_order():
    instance = _minimal_instance()
    solution = {
        "vehicles": [
            {
                "id": 1,
                "route": [0, 1, 0],
                "time": [5.0],
            }
        ],
        "loaders": [],
    }
    result = validate_solution(instance, solution)
    assert result["violations"]["MandatoryUnscheduledOrders"] == 1
    assert result["total_violations"] >= 1


def test_validator_class_from_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input.json"
        result_path = Path(tmpdir) / "result.json"
        input_path.write_text(json.dumps(_minimal_instance()))
        result_path.write_text(json.dumps(_minimal_solution()))

        validator = Validator(str(input_path), str(result_path))
        result = validator.validation()
        assert result["total_violations"] == 0


def test_validator_cli():
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input.json"
        result_path = Path(tmpdir) / "result.json"
        input_path.write_text(json.dumps(_minimal_instance()))
        result_path.write_text(json.dumps(_minimal_solution()))

        process = subprocess.run(
            [
                "python",
                "backup/validator.py",
                "--dir",
                str(tmpdir),
                "--input_file",
                "input",
                "--result_file",
                "result",
            ],
            capture_output=True,
            text=True,
        )
        assert process.returncode == 0
        assert "Total violations = 0" in process.stderr


@pytest.mark.slow
@pytest.mark.integration
def test_validator_on_t1_generated_solution():
    """Generate a solution with main_mvp and validate it."""
    from backup import main_mvp

    with open("test_cases/t1.json") as f:
        instance = json.load(f)

    solution = main_mvp.solve(instance, seed=42)
    assert solution is not None

    result = validate_solution(instance, solution)
    assert result["total_violations"] == 0
