import multiprocessing as mp
import random
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from ortools.constraint_solver import routing_enums_pb2

from beta_code.core.data import ProblemData
from beta_code.core.evaluator import Evaluator
from beta_code.core.solution import Solution
from beta_code.loaders.greedy import assign_loaders_greedy
from beta_code.pipeline.output import format_solution_output
from beta_code.solvers.ortools_cvrptw import ORToolsVehicleSolver
from beta_code.utils.parallel import (
    _STRATEGIES,
    loader_sa_worker,
    ortools_worker,
)

SMALL_INSTANCE_LIMIT = 500


def solve(problem_data, time_limit, seed, skip_loader_refinement=False):
    """Full pipeline: vehicle routing → greedy loaders → optional Loader SA."""
    random.seed(seed)
    solve_start = time.time()

    print("Parsing problem data...")
    problem = ProblemData(problem_data)
    evaluator = Evaluator(problem)

    # ------------------------------------------------------------------
    # Phase 1: OR-Tools CVRPTW
    # ------------------------------------------------------------------
    or_tools_budget = max(time_limit * 0.5, 30)
    start_time = time.time()

    if problem.number_of_orders > SMALL_INSTANCE_LIMIT:
        solution = _run_large_instance(problem, evaluator, problem_data,
                                       or_tools_budget, seed, start_time)
    else:
        solution = _run_small_instance(problem, evaluator, problem_data,
                                       or_tools_budget, seed, start_time)

    if solution is None:
        return None

    # Phase 1b: GLS refinement
    solution = _refine_gls(problem, evaluator, solution,
                           or_tools_budget, start_time, seed)

    cost, _, details = evaluator.evaluate(solution)
    print(f"  Result: cost={cost:.2f}, v={details.get('used_vehicles', '?')}, "
          f"dist={details.get('vehicle_distance', 0):.1f}, "
          f"unserved_opt={details.get('unserved_optional', 0)}")

    # ------------------------------------------------------------------
    # Phase 2: Greedy loader assignment
    # ------------------------------------------------------------------
    print("\nPhase 2: Greedy loader assignment")
    vehicle_times = evaluator.extract_vehicle_times(solution)
    solution.loader_routes = assign_loaders_greedy(problem, evaluator, vehicle_times)

    cost, ok, details = evaluator.evaluate(solution)
    if not ok:
        print(f"  After loaders: INFEASIBLE (cost={cost:.2f})")
        print("  ERROR: greedy loader assignment produced infeasible solution.")
        return None
    print(f"  After loaders: cost={cost:.2f}, "
          f"v={details['used_vehicles']}, l={details['used_loaders']}")

    # ------------------------------------------------------------------
    # Phase 3: Loader SA refinement (parallel chains)
    # ------------------------------------------------------------------
    if skip_loader_refinement:
        print("\nPhase 3: Loader SA skipped (--skip-loader-refinement)")
    else:
        remaining = time_limit - (time.time() - start_time)
        ls_budget = max(remaining * 0.8, 10)
        n_chains = max(mp.cpu_count() // 2, 1)
        print(f"\nPhase 3: Loader SA ({n_chains} chains × {ls_budget:.0f}s budget)")

        base_solution = solution
        vehicle_times = evaluator.extract_vehicle_times(base_solution)
        loader_routes = [list(r) for r in base_solution.loader_routes]
        unserved_opt = list(base_solution.unserved_optional)
        veh_routes = [list(r) for r in base_solution.vehicle_routes]

        chain_results = []
        with ProcessPoolExecutor(max_workers=n_chains) as pool:
            futures = {
                pool.submit(
                    loader_sa_worker, problem_data, veh_routes, loader_routes,
                    unserved_opt, vehicle_times, ls_budget, seed + i,
                ): i
                for i in range(n_chains)
            }
            for fut in as_completed(futures):
                c, lr, uo = fut.result()
                chain_results.append((c, lr, uo))
                print(f"  Chain {futures[fut]}: cost={c:.2f}")

        chain_results.sort(key=lambda x: x[0])
        best_cost_loader, best_lr, best_uo = chain_results[0]
        solution = base_solution.copy()
        solution.loader_routes = [list(r) for r in best_lr]
        solution.unserved_optional = set(best_uo)

    cost, ok, details = evaluator.evaluate(solution)
    if not ok:
        print(f"  After loader stage: INFEASIBLE")
        cost = best_cost_loader if not skip_loader_refinement else cost
        print(f"\n  Final cost: {cost:.2f} (using best chain cost)")
    else:
        stage = "greedy loaders" if skip_loader_refinement else "Loader SA"
        print(f"  After {stage}: cost={cost:.2f}, "
              f"v={details['used_vehicles']}, l={details['used_loaders']}")
        print(f"\n  Final cost: {cost:.2f}")

    # ------------------------------------------------------------------
    # Output
    # ------------------------------------------------------------------
    elapsed = time.time() - solve_start
    print(f"\n  Elapsed: {elapsed:.1f}s")

    output = format_solution_output(solution, evaluator)
    output["_cost"] = cost
    return output


def _run_large_instance(problem, evaluator, problem_data,
                        or_tools_budget, seed, start_time):
    print(f"\nPhase 1: OR-Tools PCI + GLS ({or_tools_budget:.0f}s)")
    solver = ORToolsVehicleSolver(problem, evaluator)
    solution = solver.solve(
        time_limit=or_tools_budget,
        seed=seed,
        strategy=routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION,
    )
    if not solution or not solution.vehicle_routes:
        print("  OR-Tools failed - no feasible vehicle solution.")
        return None
    return solution


def _run_small_instance(problem, evaluator, problem_data,
                        or_tools_budget, seed, start_time):
    n_strategies = min(mp.cpu_count(), len(_STRATEGIES))
    init_budget = max(
        min(int(or_tools_budget * 0.20), max(60, problem.number_of_orders // 10)), 10
    )
    print(f"\nPhase 1a: Quick initial solutions ({n_strategies} strategies x {init_budget}s)")

    results = []
    with ProcessPoolExecutor(max_workers=n_strategies) as pool:
        futures = {
            pool.submit(ortools_worker, problem_data, init_budget, seed, s): s
            for s in _STRATEGIES[:n_strategies]
        }
        for fut in as_completed(futures):
            sname, routes, uo, c = fut.result()
            results.append((c if routes else float("inf"), sname, routes, uo))
            status = f"cost={c:.2f}" if c < float("inf") else "FAILED"
            print(f"  [{sname:35s}] {status}")

    results.sort(key=lambda x: x[0])
    best_cost, best_name, best_routes, best_uo = results[0]

    if not best_routes:
        fallback_budget = or_tools_budget - (time.time() - start_time)
        if fallback_budget > 30:
            print(f"  All strategies failed - PCI fallback ({fallback_budget:.0f}s)")
            solver = ORToolsVehicleSolver(problem, evaluator)
            fallback = solver.solve(
                time_limit=fallback_budget,
                seed=seed,
                strategy=routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION,
            )
            if fallback and fallback.vehicle_routes:
                print(f"  Fallback: cost={evaluator.evaluate(fallback)[0]:.2f}")
                return fallback
            else:
                print("  Fallback failed - no feasible solution.")
                return None
        else:
            print("  All strategies failed - no feasible solution.")
            return None

    solution = Solution()
    solution.vehicle_routes = [list(r) for r in best_routes]
    solution.unserved_optional = set(best_uo)
    return solution


def _refine_gls(problem, evaluator, solution, or_tools_budget, start_time, seed):
    refine_budget = or_tools_budget - (time.time() - start_time)
    if refine_budget > 10:
        print(f"Phase 1b: GLS refinement ({refine_budget:.0f}s)")
        solver = ORToolsVehicleSolver(problem, evaluator)
        refined = solver.solve(
            time_limit=refine_budget,
            seed=seed,
            strategy=routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION,
        )
        if refined and refined.vehicle_routes:
            cost_ref, _, _ = evaluator.evaluate(refined)
            cost_before, _, _ = evaluator.evaluate(solution)
            if cost_ref < cost_before:
                print(f"  Refined: {cost_before:.2f} -> {cost_ref:.2f}")
                return refined
            else:
                print(f"  GLS did not improve (stayed at {cost_before:.2f})")
    else:
        print("  Phase 1b skipped (no remaining budget)")
    return solution
