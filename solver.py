import argparse
import json
import math
import random
import sys
import time
import warnings
import numpy as np
import nevergrad as ng
from pyvrp import (
    ProblemData as PyVRPProblemData,
    Client,
    Depot,
    VehicleType,
    solve as pyvrp_solve,
)
from pyvrp.stop import MaxRuntime

warnings.filterwarnings("ignore", category=UserWarning)


def clean_json_keys(obj):
    if isinstance(obj, dict):
        return {k.strip(): clean_json_keys(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_json_keys(elem) for elem in obj]
    return obj


def round_mathematically(value, decimals=2):
    if decimals == 0:
        return math.floor(value + 0.5)
    factor = 10**decimals
    return math.floor(value * factor + 0.5 * (1 if value >= 0 else -1)) / factor


class ProblemData:
    def __init__(self, raw_data):
        self.vehicle_capacity = raw_data["vehicle_capacity"]
        self.vehicle_speed = raw_data["vehicle_speed"]
        self.loader_speed = raw_data["loader_speed"]
        self.vehicle_shift_length = raw_data["vehicle_shift_size"]
        self.loader_shift_length = raw_data["loader_shift_size"]
        depot = raw_data["depot"]
        self.depot_x, self.depot_y = depot["x"], depot["y"]
        self.loading_time_at_depot = depot.get("load_time", 0.0)
        self.orders = raw_data["orders"]
        self.number_of_orders = len(self.orders)
        self.weights = raw_data["weights"]

        self.size = self.number_of_orders + 1

        self.order_by_idx = [None] + self.orders

        total_cells = self.size * self.size
        self.dist_flat = [0.0] * total_cells
        self.v_time_flat = [0.0] * total_cells
        self.l_time_flat = [0.0] * total_cells

        coords = [(self.depot_x, self.depot_y)] + [
            (o["x"], o["y"]) for o in self.orders
        ]

        for i in range(self.size):
            xi, yi = coords[i]
            idx_base = i * self.size
            for j in range(self.size):
                dx = xi - coords[j][0]
                dy = yi - coords[j][1]
                d = round_mathematically(math.sqrt(dx * dx + dy * dy), 2)

                cell = idx_base + j
                self.dist_flat[cell] = d
                self.v_time_flat[cell] = round_mathematically(d / self.vehicle_speed, 2)
                self.l_time_flat[cell] = round_mathematically(d / self.loader_speed, 2)

    def distance(self, a, b):
        return self.dist_flat[a * self.size + b]

    def v_time(self, a, b):
        return self.v_time_flat[a * self.size + b]

    def l_time(self, a, b):
        return self.l_time_flat[a * self.size + b]


class Solution:
    def __init__(self):
        self.vehicle_routes = []
        self.loader_routes = []
        self.unserved_optional = set()

    def copy(self):
        s = Solution()
        s.vehicle_routes = [list(r) for r in self.vehicle_routes]
        s.loader_routes = [list(r) for r in self.loader_routes]
        s.unserved_optional = set(self.unserved_optional)
        return s

    def number_of_vehicles_in_use(self):
        return sum(1 for r in self.vehicle_routes if len(r) > 2)

    def number_of_loaders_in_use(self):
        return sum(1 for r in self.loader_routes if r)


class Evaluator:
    def __init__(self, problem):
        self.problem = problem
        self.size = problem.size
        self.v_time_flat = problem.v_time_flat
        self.l_time_flat = problem.l_time_flat
        self.order_by_idx = problem.order_by_idx
        self.dist_flat = problem.dist_flat

    def is_vehicle_route_feasible(self, route):
        if len(route) <= 2:
            return True, [], 0.0

        v_tf = self.v_time_flat
        df = self.dist_flat
        obi = self.order_by_idx
        sz = self.size

        # Split route into trips at depot visits (0 markers)
        trips = []
        current_trip = [0]
        for n in route[1:]:
            current_trip.append(n)
            if n == 0:
                if len(current_trip) > 2:
                    trips.append(current_trip)
                current_trip = [0]
        if len(current_trip) > 1:
            trips.append(current_trip)

        if not trips:
            return False, [], 0.0

        all_start_times = []
        total_distance = 0.0
        shift_start = None
        shift_end = None

        for trip in trips:
            raw_arrival = {}
            current_time = 0.0

            for i in range(len(trip) - 1):
                f, t = trip[i], trip[i + 1]
                cell = f * sz + t
                current_time += v_tf[cell]
                total_distance += df[cell]
                if t != 0:
                    raw_arrival[t] = current_time
                    current_time += obi[t]["vehicle_service_time"]

            upper_bound = float("inf")
            for node in trip:
                if node == 0:
                    continue
                tw_start, tw_end = obi[node]["time_window"]
                ub = tw_end - raw_arrival[node]
                if ub < upper_bound:
                    upper_bound = ub
            if upper_bound < -1e-6:
                return False, [], 0.0

            departure = upper_bound if upper_bound > 0.0 else 0.0
            if shift_start is None:
                shift_start = departure

            trip_start_times = []
            current_time = departure

            for i in range(len(trip) - 1):
                f, t = trip[i], trip[i + 1]
                current_time += v_tf[f * sz + t]
                if t != 0:
                    tw_start, tw_end = obi[t]["time_window"]
                    actual = current_time if current_time > tw_start else tw_start
                    if actual > tw_end + 1e-6:
                        return False, [], 0.0
                    trip_start_times.append(round_mathematically(actual, 2))
                    current_time = actual + obi[t]["vehicle_service_time"]

            shift_end = current_time
            all_start_times.extend(trip_start_times)

            total_volume = sum(obi[n]["volume"] for n in trip if n != 0)
            if total_volume > self.problem.vehicle_capacity + 1e-6:
                return False, [], 0.0

        # NOTE: Uses > rather than >= to match PyVRP's internal tolerance.
        # Defensive post-check in the output section handles the boundary case.
        if round_mathematically(shift_end - shift_start, 2) > self.problem.vehicle_shift_length:
            return False, [], 0.0

        return True, all_start_times, total_distance

    def is_loader_route_feasible(self, route, vehicle_times):
        if not route:
            return True
        first = route[0]
        if first not in vehicle_times:
            return False

        l_tf = self.l_time_flat
        obi = self.order_by_idx
        sz = self.size

        t = vehicle_times[first] + obi[first]["loader_service_time"]
        for i in range(1, len(route)):
            prev, node = route[i - 1], route[i]
            t += l_tf[prev * sz + node]
            if node not in vehicle_times:
                return False
            if t > vehicle_times[node] + 1e-6:
                return False
            t = vehicle_times[node] + obi[node]["loader_service_time"]

        t += l_tf[route[-1] * sz + first]
        return t - vehicle_times[first] < self.problem.loader_shift_length - 1e-6

    def evaluate(self, solution):
        all_visited = [n for r in solution.vehicle_routes for n in r if n != 0]
        if len(all_visited) != len(set(all_visited)):
            return float("inf"), False, {}
        served = set(all_visited)
        obi = self.order_by_idx
        for o in self.problem.orders:
            if o["optional"] == 0 and o["id"] not in served:
                return float("inf"), False, {}

        vehicle_times = {}
        total_v_dist = 0.0

        for route in solution.vehicle_routes:
            if len(route) <= 2:
                continue
            ok, times, d = self.is_vehicle_route_feasible(route)
            if not ok:
                return float("inf"), False, {}
            total_v_dist += d
            idx = 0
            for n in route:
                if n != 0:
                    vehicle_times[n] = times[idx]
                    idx += 1

        total_l_work = 0.0
        loader_cnt = {o["id"]: 0 for o in self.problem.orders}
        for lr in solution.loader_routes:
            if not lr:
                continue
            for n in lr:
                loader_cnt[n] += 1
            if not self.is_loader_route_feasible(lr, vehicle_times):
                return float("inf"), False, {}
            total_l_work += obi[lr[0]]["loader_service_time"]

        if any(lr for lr in solution.loader_routes):
            for o in self.problem.orders:
                if (
                    o["id"] in served
                    and o["loader_cnt"] > 0
                    and loader_cnt[o["id"]] < o["loader_cnt"]
                ):
                    return float("inf"), False, {}

        used_v = solution.number_of_vehicles_in_use()
        used_l = solution.number_of_loaders_in_use()
        w = self.problem.weights
        cost = (
            used_v * w["vehicle_salary"]
            + total_v_dist * w["fuel_cost"]
            + used_l * w["loader_salary"]
            + total_l_work * w["loader_work"]
            + len(solution.unserved_optional) * w["optional_order_penalty"]
        )
        return cost, True, {"vehicle_times": vehicle_times}

    def extract_vehicle_times(self, solution):
        times = {}
        for route in solution.vehicle_routes:
            if len(route) <= 2:
                continue
            ok, start_times, _ = self.is_vehicle_route_feasible(route)
            if ok:
                idx = 0
                for n in route:
                    if n != 0:
                        times[n] = start_times[idx]
                        idx += 1
        return times


def solve_vehicles_pyvrp(
    problem, time_limit, penalty_scale=1.0, loader_penalty_weight=0.0, seed=None
):
    N = problem.number_of_orders
    coords = np.zeros((N + 1, 2))
    coords[0] = [problem.depot_x, problem.depot_y]
    for i, o in enumerate(problem.orders):
        coords[i + 1] = [o["x"], o["y"]]

    dist_mat = np.zeros((N + 1, N + 1))
    dur_mat = np.zeros((N + 1, N + 1))

    for i in range(N + 1):
        for j in range(N + 1):
            d = math.sqrt(
                (coords[i][0] - coords[j][0]) ** 2 + (coords[i][1] - coords[j][1]) ** 2
            )
            dist_mat[i, j] = round(d, 2)
            dur_mat[i, j] = round(d / problem.vehicle_speed, 2)
            if i > 0 and j > 0 and i != j:
                if (
                    problem.orders[i - 1]["loader_cnt"] > 0
                    and problem.orders[j - 1]["loader_cnt"] > 0
                ):
                    dur_mat[i, j] += (
                        (d / problem.loader_speed) - (d / problem.vehicle_speed)
                    ) * loader_penalty_weight

    SCALE = 100
    dist_mat_scaled = np.round(dist_mat * problem.weights["fuel_cost"] * SCALE).astype(
        np.int64
    )
    dur_mat_scaled = np.round(dur_mat * SCALE).astype(np.int64)

    penalty_val = problem.weights["optional_order_penalty"] * penalty_scale
    fc = problem.weights["fuel_cost"]
    vs = problem.weights["vehicle_salary"]

    clients = []
    for i, o in enumerate(problem.orders):
        if o["optional"] == 1:
            idx = i + 1
            nearest = min(dist_mat[idx][j] for j in range(N + 1) if j != idx)
            fuel_est = 2 * nearest * fc
            loader_est = 0.0
            if o["loader_cnt"] > 0:
                loader_est = (
                    (o["loader_service_time"] / problem.loader_shift_length) * problem.weights["loader_salary"]
                    + o["loader_service_time"] * problem.weights["loader_work"]
                )
            capacity_est = (o["volume"] / problem.vehicle_capacity) * vs * 0.5
            discount = fuel_est + loader_est + capacity_est
            if N <= 200:
                discount *= 0.5
            prize = max(1.0, penalty_val - discount)
        else:
            prize = 0.0
        clients.append(Client(x=float(o["x"]), y=float(o["y"]), delivery=[int(o["volume"])],
                              service_duration=int(o["vehicle_service_time"] * SCALE),
                              tw_early=int(o["time_window"][0] * SCALE), tw_late=int(o["time_window"][1] * SCALE),
                              prize=int(prize * SCALE), required=(o["optional"] == 0)))

    depots = [Depot(x=float(problem.depot_x), y=float(problem.depot_y))]
    vehicle_types = [
        VehicleType(
            num_available=N,
            capacity=[int(problem.vehicle_capacity)],
            shift_duration=int(problem.vehicle_shift_length * SCALE),
            fixed_cost=int(problem.weights["vehicle_salary"] * SCALE),
        )
    ]

    data = PyVRPProblemData(
        clients=clients,
        depots=depots,
        vehicle_types=vehicle_types,
        distance_matrices=[dist_mat_scaled],
        duration_matrices=[dur_mat_scaled],
    )

    result = pyvrp_solve(data, stop=MaxRuntime(time_limit), seed=seed)
    solution = Solution()
    if not result.is_feasible() or not result.best:
        return None

    for route in result.best.routes():
        pyvrp_route = [0] + list(route.visits()) + [0]
        if len(pyvrp_route) > 2:
            solution.vehicle_routes.append(pyvrp_route)

    served = set(n for r in solution.vehicle_routes for n in r)
    for o in problem.orders:
        if o["optional"] == 1 and o["id"] not in served:
            solution.unserved_optional.add(o["id"])
    return solution

def optimize_routes_multitrip(problem, evaluator, solution):
    """Post-processing: merge PyVRP routes by allowing vehicles to do multiple trips (depot reloads) within shift."""
    routes = [r for r in solution.vehicle_routes if len(r) > 2]
    if not routes:
        return solution

    merged = []
    used = [False] * len(routes)

    for i in range(len(routes)):
        if used[i]:
            continue
        current = list(routes[i])
        used[i] = True
        changed = True
        while changed:
            changed = False
            for j in range(i + 1, len(routes)):
                if used[j]:
                    continue
                other = list(routes[j][1:-1])  # orders without depot
                if not other:
                    continue
                candidate = current + other + [0]  # depot → orders → 0 → orders → 0
                ok, _, _ = evaluator.is_vehicle_route_feasible(candidate)
                if ok:
                    current = candidate
                    used[j] = True
                    changed = True
        merged.append(current)

    optional_unserved = set()
    served = set()
    for r in merged:
        served.update(n for n in r if n != 0)
    for o in problem.orders:
        if o["optional"] == 1 and o["id"] not in served:
            optional_unserved.add(o["id"])

    mandatory_missing = [o["id"] for o in problem.orders if o["optional"] == 0 and o["id"] not in served]
    if mandatory_missing:
        merged = [r for r in solution.vehicle_routes if len(r) > 2]
        optional_unserved = set(solution.unserved_optional)

    result = Solution()
    result.vehicle_routes = merged
    result.unserved_optional = optional_unserved
    return result


def assign_loaders_greedy(problem, evaluator, vehicle_times):
    demands = []
    obi = problem.order_by_idx
    for o in problem.orders:
        if o["loader_cnt"] > 0 and o["id"] in vehicle_times:
            for _ in range(o["loader_cnt"]):
                demands.append(
                    (o["id"], vehicle_times[o["id"]], o["loader_service_time"])
                )
    demands.sort(key=lambda x: (x[1], x[2]))
    loader_routes = []
    for order_id, _, _ in demands:
        placed, best_ri, best_pos, best_fs = False, -1, -1, float("inf")
        for ri, route in enumerate(loader_routes):
            if order_id in route:
                continue
            for pos in range(len(route) + 1):
                candidate = route[:pos] + [order_id] + route[pos:]
                if evaluator.is_loader_route_feasible(candidate, vehicle_times):
                    fs = obi[candidate[0]]["loader_service_time"]
                    if fs < best_fs:
                        best_fs, best_ri, best_pos = fs, ri, pos
                        break
        if best_ri >= 0:
            r = loader_routes[best_ri]
            loader_routes[best_ri] = r[:best_pos] + [order_id] + r[best_pos:]
            placed = True
        if not placed:
            loader_routes.append([order_id])
    return loader_routes


class LoaderSA:
    def __init__(
        self,
        problem,
        evaluator,
        temp0=100,
        alpha=0.995,
        max_iters=50000,
        time_budget=60.0,
    ):
        self.problem, self.evaluator = problem, evaluator
        self.temp0, self.alpha, self.max_iters, self.time_budget = (
            temp0,
            alpha,
            max_iters,
            time_budget,
        )

    def improve(self, solution, vehicle_times):
        best, current = solution.copy(), solution.copy()
        best_cost, ok, _ = self.evaluator.evaluate(best)
        if not ok:
            return best
        current_cost, temperature, start_time = best_cost, self.temp0, time.time()
        for _ in range(self.max_iters):
            if time.time() - start_time > self.time_budget:
                break
            neighbor = current.copy()
            op = random.choice(["relocate", "swap", "two_opt", "merge"])
            generated = getattr(self, f"_{op}")(neighbor, vehicle_times)
            if not generated:
                temperature *= self.alpha
                continue
            cost, valid, _ = self.evaluator.evaluate(neighbor)
            if not valid:
                temperature *= self.alpha
                continue
            delta = cost - current_cost
            if delta < 0 or random.random() < math.exp(-delta / (temperature + 1e-9)):
                current, current_cost = neighbor, cost
                if current_cost < best_cost:
                    best, best_cost = neighbor.copy(), current_cost
            temperature *= self.alpha
        return best

    def _relocate(self, sol, vt):
        if len(sol.loader_routes) < 1:
            return False
        ri = random.randrange(len(sol.loader_routes))
        if not sol.loader_routes[ri]:
            return False
        idx = random.randrange(len(sol.loader_routes[ri]))
        oid = sol.loader_routes[ri][idx]
        r_without = sol.loader_routes[ri][:idx] + sol.loader_routes[ri][idx + 1 :]
        for rj in random.sample(range(len(sol.loader_routes)), len(sol.loader_routes)):
            if rj == ri or oid in sol.loader_routes[rj]:
                continue
            pos = random.randrange(len(sol.loader_routes[rj]) + 1)
            cand = sol.loader_routes[rj][:pos] + [oid] + sol.loader_routes[rj][pos:]
            if self.evaluator.is_loader_route_feasible(cand, vt):
                new_r = [
                    r for k, r in enumerate(sol.loader_routes) if k != ri and k != rj
                ]
                if r_without:
                    new_r.append(r_without)
                new_r.append(cand)
                sol.loader_routes[:] = new_r
                return True
        return False

    def _swap(self, sol, vt):
        if len(sol.loader_routes) < 2:
            return False
        ri, rj = random.sample(range(len(sol.loader_routes)), 2)
        if not sol.loader_routes[ri] or not sol.loader_routes[rj]:
            return False
        i, j = random.randrange(len(sol.loader_routes[ri])), random.randrange(
            len(sol.loader_routes[rj])
        )
        oi, oj = sol.loader_routes[ri][i], sol.loader_routes[rj][j]
        if oi in sol.loader_routes[rj] or oj in sol.loader_routes[ri]:
            return False
        sol.loader_routes[ri][i], sol.loader_routes[rj][j] = oj, oi
        if not (
            self.evaluator.is_loader_route_feasible(sol.loader_routes[ri], vt)
            and self.evaluator.is_loader_route_feasible(sol.loader_routes[rj], vt)
        ):
            sol.loader_routes[ri][i], sol.loader_routes[rj][j] = oi, oj
            return False
        return True

    def _two_opt(self, sol, vt):
        if not sol.loader_routes:
            return False
        ri = random.randrange(len(sol.loader_routes))
        route = sol.loader_routes[ri]
        if len(route) < 3:
            return False
        i, j = random.randrange(len(route) - 1), random.randrange(1, len(route))
        if i >= j:
            i, j = j, i
        cand = route[:i] + route[i:j][::-1] + route[j:]
        if self.evaluator.is_loader_route_feasible(cand, vt):
            sol.loader_routes[ri] = cand
            return True
        return False

    def _merge(self, sol, vt):
        if len(sol.loader_routes) < 2:
            return False
        ri, rj = random.sample(range(len(sol.loader_routes)), 2)
        a, b = sol.loader_routes[ri], sol.loader_routes[rj]
        if set(a) & set(b):
            return False
        for merged in (a + b, b + a):
            if self.evaluator.is_loader_route_feasible(merged, vt):
                sol.loader_routes[:] = [
                    r for k, r in enumerate(sol.loader_routes) if k not in (ri, rj)
                ] + [merged]
                return True
        return False

def run_pipeline(problem, evaluator, params, time_limit, pyvrp_cap, seed=None, use_multitrip=False):
    solver_time = min(time_limit * params["pyvrp_time_frac"], pyvrp_cap)
    sa_time = max(time_limit - solver_time - 2.0, 10.0)

    sol = solve_vehicles_pyvrp(problem, solver_time, params["penalty_scale"], params["loader_penalty_weight"], seed=seed)
    if not sol or not sol.vehicle_routes:
        return None
    best_sol = sol

    if use_multitrip:
        best_sol = optimize_routes_multitrip(problem, evaluator, best_sol)

    vt = evaluator.extract_vehicle_times(best_sol)
    best_sol.loader_routes = assign_loaders_greedy(problem, evaluator, vt)

    loader_sa = LoaderSA(problem, evaluator, time_budget=sa_time)
    best_sol = loader_sa.improve(best_sol, vt)
    return best_sol


def solve(raw_data, time_limit=900, seed=42):
    random.seed(seed)

    data = clean_json_keys(raw_data)

    problem = ProblemData(data)
    evaluator = Evaluator(problem)
    N = problem.number_of_orders

    print(f"Orders: {N}, Time limit: {time_limit}s")

    best_cost, best_params, best_solution = float("inf"), None, None

    pyvrp_frac_bounds = (0.7, 1.05)
    pyvrp_cap = float("inf")

    if time_limit <= 60:
        ng_budget = 2
        print("Mode: Short Time Limit (Minimal Hyperparameter Tuning)")
    elif N <= 200:
        ng_budget = 10
        print("Mode: Small/Medium Instance (Hyperparameter Tuning)")
    else:
        ng_budget = 5
        print("Mode: Large Instance (Quick Sweep + Deep Convergence)")

    parametrization = ng.p.Dict(
        penalty_scale=ng.p.Scalar(lower=0.8, upper=2.0),
        pyvrp_time_frac=ng.p.Scalar(
            lower=pyvrp_frac_bounds[0], upper=pyvrp_frac_bounds[1]
        ),
        loader_penalty_weight=ng.p.Scalar(lower=0.0, upper=3.0),
    )

    optimizer = ng.optimizers.NGOpt(parametrization=parametrization, budget=ng_budget)
    eval_time = (time_limit * 0.4) / ng_budget

    def objective(params):
        nonlocal best_cost, best_params, best_solution
        sol = run_pipeline(problem, evaluator, params, eval_time, pyvrp_cap, seed=seed)
        if sol is None:
            return float("inf")

        cost, valid, _ = evaluator.evaluate(sol)
        if valid and cost < best_cost:
            best_cost, best_params, best_solution = cost, params, sol
            print(f"  [NG Sweep] Best: {cost:.2f} | Params: {params}")
        else:
            print(f"  [NG Sweep] Cur: {cost:.2f} | Params: {params}")
        return cost if valid else float("inf")

    print(f"Starting Nevergrad Warm-Up ({ng_budget} iterations)...")
    optimizer.minimize(objective)

    remaining_time = time_limit * 0.6
    print(f"\nStarting Deep Convergence Phase ({remaining_time:.0f}s, with multi-trip merge)...")

    final_sol = run_pipeline(problem, evaluator, best_params, remaining_time, pyvrp_cap, seed=seed, use_multitrip=True)

    if final_sol:
        final_cost, valid, _ = evaluator.evaluate(final_sol)
        if valid and final_cost < best_cost:
            best_solution, best_cost = final_sol, final_cost
            print(f"  [Deep Conv] Final Cost: {final_cost:.2f}")

    if best_solution is None:
        print("FAILED: No valid solution found.")
        return None

    vehicle_output, loader_output = [], []
    vid = 0
    for route in best_solution.vehicle_routes:
        if len(route) <= 2:
            continue
        ok, times, _ = evaluator.is_vehicle_route_feasible(route)
        if not ok:
            continue
        # Split multi-trip route into individual trips for output
        trips = []
        current = [0]
        for n in route[1:]:
            current.append(n)
            if n == 0 and len(current) > 2:
                trips.append(current)
                current = [0]
        if len(current) > 1:
            trips.append(current)

        time_idx = 0
        for trip in trips:
            route_ids = [n for n in trip if n != 0]
            trip_times = times[time_idx:time_idx + len(route_ids)]
            time_idx += len(route_ids)

            # Defensive shift check matching validator's exact formula
            vtf = evaluator.v_time_flat
            oi = evaluator.order_by_idx
            shift_limit = evaluator.problem.vehicle_shift_length
            sz = evaluator.size

            def _trip_shift_ok(trip_route, trip_tms):
                if not trip_route:
                    return True
                oids = [n for n in trip_route if n != 0]
                if not oids:
                    return True
                dep = trip_tms[0] - vtf[0 * sz + oids[0]]
                ret = trip_tms[-1] + vtf[oids[-1] * sz + 0] + oi[oids[-1]]["vehicle_service_time"]
                return ret - dep < shift_limit - 1e-6

            if not _trip_shift_ok(trip, trip_times):
                # Try splitting the trip to avoid shift violation
                split_idx = 1
                split_ok = False
                while split_idx < len(route_ids):
                    left_route = [0] + route_ids[:split_idx] + [0]
                    right_route = [0] + route_ids[split_idx:] + [0]
                    left_times = trip_times[:split_idx]
                    right_times = trip_times[split_idx:]
                    if _trip_shift_ok(left_route, left_times) and _trip_shift_ok(right_route, right_times):
                        vid += 1
                        vehicle_output.append({"id": vid, "route": left_route, "time": left_times})
                        vid += 1
                        vehicle_output.append({"id": vid, "route": right_route, "time": right_times})
                        split_ok = True
                        break
                    split_idx += 1
                if not split_ok:
                    continue
            else:
                vid += 1
                vehicle_output.append({"id": vid, "route": trip, "time": trip_times})
    for lid, route in enumerate(best_solution.loader_routes):
        if route:
            loader_output.append({"id": lid + 1, "route": route})

    result = {"vehicles": vehicle_output, "loaders": loader_output, "_cost": best_cost, "_evaluator": evaluator}
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="t1.json")
    parser.add_argument("--output", default="solution.json")
    parser.add_argument("--time-limit", type=int, default=900, help="seconds")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    with open(args.input) as f:
        raw_data = json.load(f)

    result = solve(raw_data, time_limit=args.time_limit, seed=args.seed)

    if result is None:
        print("FAILED: no solution found.")
        sys.exit(1)

    output = {k: v for k, v in result.items() if k not in ("_cost", "_evaluator")}
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nFinal Best Cost: {result['_cost']:.2f}")
    print(f"Solution saved to {args.output}")


if __name__ == "__main__":
    main()
