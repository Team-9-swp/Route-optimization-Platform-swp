from app.validation import validate_solution


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
            {"id": 1, "route": [0, 1, 2, 0], "time": [5.0, 15.0]}
        ],
        "loaders": [],
    }


def test_validate_solution_returns_expected_shape():
    result = validate_solution(_minimal_instance(), _minimal_solution())
    assert isinstance(result["passed"], bool)
    assert "violations" in result
    assert "report" in result


def test_validate_solution_passes_valid_solution():
    result = validate_solution(_minimal_instance(), _minimal_solution())
    assert result["passed"] is True
    assert result["report"]["total_violations"] == 0
    assert result["objective_value"] is not None


def test_validate_solution_fails_missing_mandatory_order():
    instance = _minimal_instance()
    solution = {
        "vehicles": [{"id": 1, "route": [0, 1, 0], "time": [5.0]}],
        "loaders": [],
    }
    result = validate_solution(instance, solution)
    assert result["passed"] is False
    assert result["objective_value"] is None
    assert any("MandatoryUnscheduledOrders" in v for v in result["violations"])
