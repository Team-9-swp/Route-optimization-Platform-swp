from typing import Any

from validator import validate_solution as _validate_solution


def validate_solution(instance: dict[str, Any], solution: dict[str, Any]) -> dict[str, Any]:
    """Validate a solution against an instance using the project's Validator.

    Returns a normalized dict that matches the ValidationResponse schema.
    """
    result = _validate_solution(instance, solution, quiet=True)
    violations = []
    for key, count in result["violations"].items():
        if count > 0:
            violations.append(f"{key}: {count}")

    passed = result["total_violations"] == 0
    return {
        "passed": passed,
        "objective_value": result["total_cost"] if passed else None,
        "violations": violations,
        "report": result,
    }
