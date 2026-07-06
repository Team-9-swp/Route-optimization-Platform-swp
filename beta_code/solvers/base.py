from abc import ABC, abstractmethod

from beta_code.core.data import ProblemData
from beta_code.core.evaluator import Evaluator
from beta_code.core.solution import Solution


class VehicleSolver(ABC):
    """Abstract base for all vehicle routing solvers."""

    def __init__(self, problem: ProblemData, evaluator: Evaluator):
        self.problem = problem
        self.evaluator = evaluator

    @abstractmethod
    def solve(self, time_limit: float, seed: int, **kwargs) -> Solution: ...
