import os as _os
import random

from ortools.constraint_solver import routing_enums_pb2

from beta_code.core.data import ProblemData
from beta_code.core.evaluator import Evaluator
from beta_code.core.solution import Solution
from beta_code.loaders.sa import LoaderSA

_STRATEGIES = [
    "PARALLEL_CHEAPEST_INSERTION",
    "PATH_CHEAPEST_ARC",
    "SAVINGS",
    "LOCAL_CHEAPEST_COST_INSERTION",
]


def _suppress_stderr():
    _os.dup2(_os.open(_os.devnull, _os.O_WRONLY), 2)


def ortools_worker(problem_data_dict, time_limit, seed, strategy_name):
    """Run OR-Tools with a specific first-solution strategy in a subprocess."""
    from beta_code.solvers.ortools_cvrptw import ORToolsVehicleSolver

    _suppress_stderr()
    _os.environ["GLOG_minloglevel"] = "3"

    random.seed(seed)
    problem = ProblemData(problem_data_dict)
    evaluator = Evaluator(problem)
    strategy_value = getattr(routing_enums_pb2.FirstSolutionStrategy, strategy_name)

    solver = ORToolsVehicleSolver(problem, evaluator)
    solution = solver.solve(time_limit, seed, strategy=strategy_value)

    if solution is None:
        return strategy_name, [], [], float("inf")
    cost, _, details = evaluator.evaluate(solution)
    vehicle_routes = [list(r) for r in solution.vehicle_routes]
    unserved_optional = list(solution.unserved_optional)
    return strategy_name, vehicle_routes, unserved_optional, cost


def loader_sa_worker(
    problem_data_dict,
    vehicle_routes,
    loader_routes,
    unserved_optional,
    vehicle_times,
    time_budget,
    seed,
):
    """Standalone Loader SA chain run in a subprocess."""
    _suppress_stderr()
    random.seed(seed)
    problem = ProblemData(problem_data_dict)
    evaluator = Evaluator(problem)
    solution = Solution()
    solution.vehicle_routes = vehicle_routes
    solution.loader_routes = loader_routes
    solution.unserved_optional = set(unserved_optional)

    loader_sa = LoaderSA(
        problem,
        evaluator,
        temp0=100,
        alpha=0.998,
        max_iters=100000,
        time_budget=time_budget,
    )
    improved = loader_sa.improve(solution, vehicle_times)

    cost, _, _ = evaluator.evaluate(improved)
    return cost, improved.loader_routes, list(improved.unserved_optional)
