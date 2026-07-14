import argparse
import json
import math
import os
import random
import sys
import time
import warnings
import numpy as np
import nevergrad as ng

warnings.filterwarnings("ignore", category=UserWarning)

try:
    from ortools.constraint_solver import routing_enums_pb2
    from ortools.constraint_solver import pywrapcp
    from ortools.sat.python import cp_model
    ORTOOLS_AVAILABLE = True
except ImportError:
    ORTOOLS_AVAILABLE = False

try:
    from pyvrp import (
        ProblemData as PyVRPProblemData,
        Client,
        Depot,
        VehicleType,
        solve as pyvrp_solve,
    )
    from pyvrp.stop import MaxRuntime
    PYVRP_AVAILABLE = True
except ImportError:
    PYVRP_AVAILABLE = False


def clean_json_keys(obj):
    if isinstance(obj, dict):
        return {k.strip(): clean_json_keys(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_json_keys(elem) for elem in obj]
    return obj


def round_mathematically(value, decimals=2):
    if decimals == 0:
        return math.floor(value + 0.5)
    factor = 10 ** decimals
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
                self.v_time_flat[cell] = round_mathematically(
                    d / self.vehicle_speed, 2
                )
                self.l_time_flat[cell] = round_mathematically(
                    d / self.loader_speed, 2
                )

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

    def _node_index(self, n):
        return 0 if n == -1 else n

    def is_vehicle_route_feasible(self, route, debug=False):
        if len(route) <= 2:
            return True, [], 0.0

        v_tf = self.v_time_flat
        df = self.dist_flat
        obi = self.order_by_idx
        sz = self.size

        trips = []
        current_trip = [0]
        for n in route[1:]:
            current_trip.append(n)
            if n in (0, -1):
                if len(current_trip) > 2:
                    trips.append(current_trip)
                current_trip = [0]
        if len(current_trip) > 1:
            trips.append(current_trip)

        if not trips:
            if debug:
                print(f"      [DEBUG] No trips found in route")
            return False, [], 0.0

        all_start_times = []
        total_distance = 0.0
        shift_start = None
        abs_time = 0.0

        for trip in trips:
            raw_arrival = {}
            current_time = 0.0

            for i in range(len(trip) - 1):
                f, t = trip[i], trip[i + 1]
                f_idx = self._node_index(f)
                t_idx = self._node_index(t)
                cell = f_idx * sz + t_idx
                current_time += v_tf[cell]
                total_distance += df[cell]
                if t not in (0, -1):
                    raw_arrival[t] = current_time
                    current_time += obi[t]["vehicle_service_time"]
                elif t == -1:
                    raw_arrival[t] = current_time
                    current_time += self.problem.loading_time_at_depot

            upper_bound = float("inf")
            for node in trip:
                if node in (0, -1):
                    continue
                tw_start, tw_end = obi[node]["time_window"]
                ub = tw_end - abs_time - raw_arrival[node]
                if ub < upper_bound:
                    upper_bound = ub
            if upper_bound < -1e-6:
                if debug:
                    tight_node = None
                    for node in trip:
                        if node in (0, -1):
                            continue
                        tw_s, tw_e = obi[node]["time_window"]
                        ra = raw_arrival[node]
                        ub_val = tw_e - abs_time - ra
                        if ub_val < -1e-6:
                            tight_node = node
                            break
                    print(f"      [DEBUG] Trip {trip}: upper_bound={upper_bound:.2f} < 0 (tight node={tight_node}, abs_time={abs_time:.2f})")

            departure = abs_time + max(0, upper_bound)
            if shift_start is None:
                shift_start = departure

            trip_start_times = []
            current_time = abs_time

            for i in range(len(trip) - 1):
                f, t = trip[i], trip[i + 1]
                f_idx = self._node_index(f)
                t_idx = self._node_index(t)
                current_time += v_tf[f_idx * sz + t_idx]
                if t not in (0, -1):
                    tw_start, tw_end = obi[t]["time_window"]
                    actual = current_time if current_time > tw_start else tw_start
                    if actual > tw_end + 0.5:
                        if debug:
                            print(f"      [DEBUG] TW violation at node {t}: actual={actual:.2f} > tw_end={tw_end}")
                        return False, [], 0.0
                    trip_start_times.append(round_mathematically(actual, 2))
                    current_time = actual + obi[t]["vehicle_service_time"]
                elif t == -1:
                    actual = current_time
                    trip_start_times.append(round_mathematically(actual, 2))
                    current_time = actual + self.problem.loading_time_at_depot

            abs_time = current_time
            all_start_times.extend(trip_start_times)

            total_volume = sum(
                obi[n]["volume"] for n in trip if n not in (0, -1)
            )
            if total_volume > self.problem.vehicle_capacity + 1e-6:
                if debug:
                    print(f"      [DEBUG] Capacity violation in trip {trip}: {total_volume} > {self.problem.vehicle_capacity}")
                return False, [], 0.0

        shift_used = round_mathematically(abs_time - shift_start, 2)
        if shift_used >= self.problem.vehicle_shift_length:
            if debug:
                print(f"      [DEBUG] Shift violation: {shift_used} >= {self.problem.vehicle_shift_length} (shift_start={shift_start:.2f}, abs_time={abs_time:.2f})")
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

    def evaluate(self, solution, debug=False):
        all_visited = [
            n for r in solution.vehicle_routes for n in r if n not in (0, -1)
        ]
        if len(all_visited) != len(set(all_visited)):
            if debug:
                print(f"    [DEBUG Evaluate] DUPLICATE orders in vehicle routes")
            return float("inf"), False, {}
        served = set(all_visited)
        obi = self.order_by_idx
        for o in self.problem.orders:
            if o["optional"] == 0 and o["id"] not in served:
                if debug:
                    print(f"    [DEBUG Evaluate] Mandatory order {o['id']} not served")
                return float("inf"), False, {}

        vehicle_times = {}
        total_v_dist = 0.0

        for route in solution.vehicle_routes:
            if len(route) <= 2:
                continue
            ok, times, d = self.is_vehicle_route_feasible(route, debug=debug)
            if not ok:
                if debug:
                    print(f"    [DEBUG Evaluate] Vehicle route infeasible: {route}")
                return float("inf"), False, {}
            total_v_dist += d
            idx = 0
            for n in route:
                if n not in (0, -1):
                    vehicle_times[n] = times[idx]
                    idx += 1
                elif n == -1:
                    idx += 1

        total_l_work = 0.0
        loader_cnt = {o["id"]: 0 for o in self.problem.orders}
        for lr in solution.loader_routes:
            if not lr:
                continue
            for n in lr:
                loader_cnt[n] += 1
            if not self.is_loader_route_feasible(lr, vehicle_times):
                if debug:
                    print(f"    [DEBUG Evaluate] Loader route infeasible: {lr}")
                    first = lr[0]
                    vt = vehicle_times.get(first, 'MISSING')
                    print(f"      First node {first}, vehicle_time={vt}")
                    for i in range(1, len(lr)):
                        prev, node = lr[i-1], lr[i]
                        vt_node = vehicle_times.get(node, 'MISSING')
                        print(f"      Node {node}, vehicle_time={vt_node}")
                return float("inf"), False, {}
            total_l_work += obi[lr[0]]["loader_service_time"]

        for o in self.problem.orders:
            if (
                o["id"] in served
                and o["loader_cnt"] > 0
                and loader_cnt[o["id"]] < o["loader_cnt"]
            ):
                if debug:
                    print(f"    [DEBUG Evaluate] Order {o['id']} needs {o['loader_cnt']} loader visits, got {loader_cnt[o['id']]}")
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
                    if n not in (0, -1):
                        times[n] = start_times[idx]
                        idx += 1
                    elif n == -1:
                        idx += 1
            else:
                trips = []
                ct = [0]
                for n in route[1:]:
                    ct.append(n)
                    if n in (0, -1):
                        if len(ct) > 2:
                            trips.append(ct)
                        ct = [0]
                if len(ct) > 1:
                    trips.append(ct)
                v_tf = self.v_time_flat
                sz = self.size
                base_time = 0.0
                obi = self.order_by_idx
                for trip in trips:
                    ends_with_reload = trip[-1] == -1
                    stripped = trip[:-1] + [0] if ends_with_reload else trip
                    trip_ok, rel_times, _ = self.is_vehicle_route_feasible(stripped)
                    if not trip_ok:
                        continue
                    idx = 0
                    for n in trip:
                        if n not in (0, -1):
                            times[n] = rel_times[idx] + base_time
                            idx += 1
                    served = [n for n in trip if n not in (0, -1)]
                    if served:
                        last_svc = served[-1]
                        last_arr = rel_times[len(served) - 1]
                        base_time = last_arr + obi[last_svc]["vehicle_service_time"]
                        base_time += v_tf[last_svc * sz + 0]
                    if ends_with_reload:
                        base_time += self.problem.loading_time_at_depot
        return times


def solve_vehicles_pyvrp(
    problem, time_limit, penalty_scale=1.0, loader_penalty_weight=0.0, seed=None
):
    if not PYVRP_AVAILABLE:
        return None

    N = problem.number_of_orders
    load_time = problem.loading_time_at_depot

    M = N + 2
    coords = [
        (problem.depot_x, problem.depot_y),
        (problem.depot_x, problem.depot_y),
    ]
    for o in problem.orders:
        coords.append((o["x"], o["y"]))

    dist_mat = np.zeros((M, M))
    dur_mat = np.zeros((M, M))

    for i in range(M):
        for j in range(M):
            d = math.sqrt(
                (coords[i][0] - coords[j][0]) ** 2
                + (coords[i][1] - coords[j][1]) ** 2
            )
            dist_mat[i, j] = round(d, 2)
            dur_mat[i, j] = round(d / problem.vehicle_speed, 2)

            if i >= 2 and j >= 2 and i != j:
                if (
                    problem.orders[i - 2]["loader_cnt"] > 0
                    and problem.orders[j - 2]["loader_cnt"] > 0
                ):
                    dur_mat[i, j] += (
                        (d / problem.loader_speed) - (d / problem.vehicle_speed)
                    ) * loader_penalty_weight

    SCALE = 100
    dist_mat_scaled = np.round(
        dist_mat * problem.weights["fuel_cost"] * SCALE
    ).astype(np.int64)
    dur_mat_scaled = np.round(dur_mat * SCALE).astype(np.int64)

    penalty_val = problem.weights["optional_order_penalty"] * penalty_scale
    fc = problem.weights["fuel_cost"]
    vs = problem.weights["vehicle_salary"]

    clients = []
    for i, o in enumerate(problem.orders):
        if o["optional"] == 1:
            idx = i + 2
            nearest = min(
                dist_mat[idx][j] for j in range(M) if j != idx
            )
            fuel_est = 2 * nearest * fc
            loader_est = 0.0
            if o["loader_cnt"] > 0:
                loader_est = (
                    o["loader_service_time"] / problem.loader_shift_length
                ) * problem.weights["loader_salary"] + o[
                    "loader_service_time"
                ] * problem.weights[
                    "loader_work"
                ]
            capacity_est = (o["volume"] / problem.vehicle_capacity) * vs * 0.5
            discount = fuel_est + loader_est + capacity_est
            if N <= 200:
                discount *= 0.5
            prize = max(1.0, penalty_val - discount)
        else:
            prize = 0.0
        clients.append(
            Client(
                x=float(o["x"]),
                y=float(o["y"]),
                delivery=[int(o["volume"])],
                service_duration=int(o["vehicle_service_time"] * SCALE),
                tw_early=int(o["time_window"][0] * SCALE),
                tw_late=int(o["time_window"][1] * SCALE),
                prize=int(prize * SCALE),
                required=(o["optional"] == 0),
            )
        )

    depots = [
        Depot(
            x=float(problem.depot_x),
            y=float(problem.depot_y),
            service_duration=0,
        ),
        Depot(
            x=float(problem.depot_x),
            y=float(problem.depot_y),
            service_duration=int(load_time * SCALE),
        ),
    ]

    vehicle_types = [
        VehicleType(
            num_available=N,
            capacity=[int(problem.vehicle_capacity)],
            shift_duration=int(problem.vehicle_shift_length * SCALE),
            fixed_cost=int(problem.weights["vehicle_salary"] * SCALE),
            start_depot=0,
            end_depot=0,
            reload_depots=[1],
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
        if not result.is_feasible():
            print(f"    [PyVRP] No feasible solution (time_limit={time_limit:.1f}s)")
        if result.is_feasible() and not result.best:
            print(f"    [PyVRP] Feasible but no best solution (time_limit={time_limit:.1f}s)")
        return None

    for route in result.best.routes():
        pyvrp_route = [0]
        for trip in route.trips():
            if len(pyvrp_route) > 1:
                pyvrp_route[-1] = -1
            for client_idx in trip.visits():
                order_id = client_idx - 1
                pyvrp_route.append(order_id)
            pyvrp_route.append(0)
        if len(pyvrp_route) > 2:
            solution.vehicle_routes.append(pyvrp_route)

    served = set(
        n for r in solution.vehicle_routes for n in r if n not in (0, -1)
    )
    for o in problem.orders:
        if o["optional"] == 1 and o["id"] not in served:
            solution.unserved_optional.add(o["id"])
    return solution


def solve_vehicles_ortools_routing(
    problem, time_limit, penalty_scale=1.0, loader_penalty_weight=0.0, seed=None
):
    if not ORTOOLS_AVAILABLE:
        return None

    N = problem.number_of_orders
    if N == 0:
        return Solution()

    COPIES = 2
    NUM_NODES = 1 + N * COPIES
    MAX_VEHICLES = max(N, 1)

    manager = pywrapcp.RoutingIndexManager(NUM_NODES, MAX_VEHICLES, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)

        def map_node(n):
            if n == 0:
                return 0
            return ((n - 1) % N) + 1

        i = map_node(from_node)
        j = map_node(to_node)
        d = problem.dist_flat[i * problem.size + j]
        penalty = 0.0
        if i >= 1 and j >= 1 and i != j:
            oi = problem.order_by_idx[i]
            oj = problem.order_by_idx[j]
            if oi["loader_cnt"] > 0 and oj["loader_cnt"] > 0:
                l_travel = d / problem.loader_speed
                v_travel = d / problem.vehicle_speed
                penalty = (l_travel - v_travel) * loader_penalty_weight
        return int((d + penalty) * 1000)

    transit_cb = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_cb)

    def time_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)

        def map_node(n):
            if n == 0:
                return 0
            return ((n - 1) % N) + 1

        i = map_node(from_node)
        j = map_node(to_node)

        travel = problem.v_time_flat[i * problem.size + j]
        service = 0
        if from_node != 0:
            service = problem.order_by_idx[i]["vehicle_service_time"]
        if to_node == 0 and from_node != 0:
            travel += problem.loading_time_at_depot

        return int((travel + service) * 1000)

    time_cb = routing.RegisterTransitCallback(time_callback)
    routing.AddDimension(
        time_cb,
        999999999,
        int(problem.vehicle_shift_length * 1000),
        False,
        "Time",
    )
    time_dim = routing.GetDimensionOrDie("Time")

    for copy in range(COPIES):
        base = 1 + copy * N
        for order_idx, o in enumerate(problem.orders):
            node = base + order_idx
            idx = manager.NodeToIndex(node)
            tw = o["time_window"]
            time_dim.CumulVar(idx).SetRange(
                int(tw[0] * 1000), int(tw[1] * 1000)
            )

    def demand_callback(from_index):
        node = manager.IndexToNode(from_index)
        if node == 0:
            return 0
        order_idx = (node - 1) % N
        return int(problem.orders[order_idx]["volume"])

    demand_cb = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_cb,
        0,
        [int(problem.vehicle_capacity)] * MAX_VEHICLES,
        True,
        "Capacity",
    )

    fc = problem.weights["fuel_cost"]
    vs = problem.weights["vehicle_salary"]
    for order_idx, o in enumerate(problem.orders):
        copies = [
            manager.NodeToIndex(1 + copy * N + order_idx)
            for copy in range(COPIES)
        ]
        if o["optional"] == 1:
            idx = order_idx + 1
            nearest = min(
                problem.dist_flat[idx * problem.size + j]
                for j in range(1, problem.size)
                if j != idx
            )
            fuel_est = 2 * nearest * fc
            loader_est = 0.0
            if o["loader_cnt"] > 0:
                loader_est = (
                    o["loader_service_time"] / problem.loader_shift_length
                ) * problem.weights["loader_salary"] + o[
                    "loader_service_time"
                ] * problem.weights[
                    "loader_work"
                ]
            capacity_est = (o["volume"] / problem.vehicle_capacity) * vs * 0.5
            discount = fuel_est + loader_est + capacity_est
            if N <= 200:
                discount *= 0.5
            prize = max(
                1.0,
                problem.weights["optional_order_penalty"] * penalty_scale
                - discount,
            )
            routing.AddDisjunction(copies, int(prize * 1000))
        else:
            routing.AddDisjunction(copies, 999999999)

    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_params.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_params.time_limit.FromSeconds(int(time_limit))
    search_params.log_search = False

    if seed is not None:
        search_params.random_seed = seed

    result = routing.SolveWithParameters(search_params)

    if not result:
        return None

    solution = Solution()
    for vehicle_id in range(MAX_VEHICLES):
        index = routing.Start(vehicle_id)
        route = []
        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            route.append(node)
            index = result.Value(routing.NextVar(index))

        pyvrp_route = [0]
        current_trip = []
        for node in route[1:]:
            if node == 0:
                if current_trip:
                    pyvrp_route.extend(current_trip)
                    pyvrp_route.append(0)
                    current_trip = []
            else:
                order_id = ((node - 1) % N) + 1
                current_trip.append(order_id)
        if current_trip:
            pyvrp_route.extend(current_trip)
            pyvrp_route.append(0)

        final_route = [0]
        for i, n in enumerate(pyvrp_route[1:-1], 1):
            if n == 0:
                final_route.append(-1)
            else:
                final_route.append(n)
        final_route.append(0)

        if len(final_route) > 2:
            solution.vehicle_routes.append(final_route)

    served = set(
        n for r in solution.vehicle_routes for n in r if n not in (0, -1)
    )
    for o in problem.orders:
        if o["optional"] == 1 and o["id"] not in served:
            solution.unserved_optional.add(o["id"])

    return solution


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
    loader_salary = problem.weights.get("loader_salary", 320)
    loader_routes = []
    for order_id, _, _ in demands:
        best_cost_impact = float("inf")
        best_ri, best_pos = -1, -1

        for ri, route in enumerate(loader_routes):
            if order_id in route:
                continue
            base_fs = obi[route[0]]["loader_service_time"]
            for pos in range(len(route) + 1):
                candidate = route[:pos] + [order_id] + route[pos:]
                if evaluator.is_loader_route_feasible(candidate, vehicle_times):
                    new_fs = obi[candidate[0]]["loader_service_time"]
                    work_delta = new_fs - base_fs
                    impact = work_delta
                    if impact < best_cost_impact:
                        best_cost_impact = impact
                        best_ri, best_pos = ri, pos

        new_route_cost = obi[order_id]["loader_service_time"] + loader_salary * 0.1
        if best_ri >= 0 and best_cost_impact <= new_route_cost:
            r = loader_routes[best_ri]
            loader_routes[best_ri] = (
                r[:best_pos] + [order_id] + r[best_pos:]
            )
        else:
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
        rng=None,
    ):
        self.problem, self.evaluator = problem, evaluator
        self.temp0, self.alpha, self.max_iters, self.time_budget = (
            temp0,
            alpha,
            max_iters,
            time_budget,
        )
        self.rng = rng if rng is not None else random

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
            op = self.rng.choice(["relocate", "swap", "two_opt", "merge"])
            generated = getattr(self, f"_{op}")(neighbor, vehicle_times)
            if not generated:
                temperature *= self.alpha
                continue
            cost, valid, _ = self.evaluator.evaluate(neighbor)
            if not valid:
                temperature *= self.alpha
                continue
            delta = cost - current_cost
            if delta < 0 or self.rng.random() < math.exp(
                -delta / (temperature + 1e-9)
            ):
                current, current_cost = neighbor, cost
                if current_cost < best_cost:
                    best, best_cost = neighbor.copy(), cost
            temperature *= self.alpha
        return best

    def _relocate(self, sol, vt):
        if len(sol.loader_routes) < 1:
            return False
        ri = self.rng.randrange(len(sol.loader_routes))
        if not sol.loader_routes[ri]:
            return False
        idx = self.rng.randrange(len(sol.loader_routes[ri]))
        oid = sol.loader_routes[ri][idx]
        r_without = (
            sol.loader_routes[ri][:idx] + sol.loader_routes[ri][idx + 1 :]
        )
        for rj in self.rng.sample(
            range(len(sol.loader_routes)), len(sol.loader_routes)
        ):
            if rj == ri or oid in sol.loader_routes[rj]:
                continue
            pos = self.rng.randrange(len(sol.loader_routes[rj]) + 1)
            cand = (
                sol.loader_routes[rj][:pos]
                + [oid]
                + sol.loader_routes[rj][pos:]
            )
            if self.evaluator.is_loader_route_feasible(cand, vt):
                new_r = [
                    r
                    for k, r in enumerate(sol.loader_routes)
                    if k != ri and k != rj
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
        ri, rj = self.rng.sample(range(len(sol.loader_routes)), 2)
        if not sol.loader_routes[ri] or not sol.loader_routes[rj]:
            return False
        i = self.rng.randrange(len(sol.loader_routes[ri]))
        j = self.rng.randrange(len(sol.loader_routes[rj]))
        oi, oj = sol.loader_routes[ri][i], sol.loader_routes[rj][j]
        if oi in sol.loader_routes[rj] or oj in sol.loader_routes[ri]:
            return False
        sol.loader_routes[ri][i], sol.loader_routes[rj][j] = oj, oi
        if not (
            self.evaluator.is_loader_route_feasible(sol.loader_routes[ri], vt)
            and self.evaluator.is_loader_route_feasible(
                sol.loader_routes[rj], vt
            )
        ):
            sol.loader_routes[ri][i], sol.loader_routes[rj][j] = oi, oj
            return False
        return True

    def _two_opt(self, sol, vt):
        if not sol.loader_routes:
            return False
        ri = self.rng.randrange(len(sol.loader_routes))
        route = sol.loader_routes[ri]
        if len(route) < 3:
            return False
        i = self.rng.randrange(len(route) - 1)
        j = self.rng.randrange(1, len(route))
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
        ri, rj = self.rng.sample(range(len(sol.loader_routes)), 2)
        a, b = sol.loader_routes[ri], sol.loader_routes[rj]
        if set(a) & set(b):
            return False
        for merged in (a + b, b + a):
            if self.evaluator.is_loader_route_feasible(merged, vt):
                sol.loader_routes[:] = [
                    r
                    for k, r in enumerate(sol.loader_routes)
                    if k not in (ri, rj)
                ] + [merged]
                return True
        return False


class JointLocalSearch:
    def __init__(self, problem, evaluator, time_budget=60.0, rng=None):
        self.problem = problem
        self.evaluator = evaluator
        self.time_budget = time_budget
        self.rng = rng if rng is not None else random.Random()

    def _get_trips(self, route):
        trips = []
        current = [0]
        for n in route[1:]:
            if n == 0:
                current.append(0)
                if len(current) > 2:
                    trips.append(current)
                current = [0]
            elif n == -1:
                current.append(-1)
                if len(current) > 2:
                    trips.append(current)
                current = [0]
            else:
                current.append(n)
        if len(current) > 1:
            if current[-1] != 0:
                current.append(0)
            trips.append(current)
        return trips

    def _trips_to_route(self, trips):
        if not trips:
            return []
        route = list(trips[0])
        for trip in trips[1:]:
            if route and route[-1] == 0:
                route[-1] = -1
            route.extend(trip[1:])
        return route

    def _clean_depots(self, route):
        cleaned = []
        for n in route:
            if n == 0 and cleaned and cleaned[-1] == 0:
                continue
            if n == -1 and cleaned and cleaned[-1] in (0, -1):
                continue
            cleaned.append(n)
        if cleaned and cleaned[0] not in (0, -1):
            cleaned.insert(0, 0)
        if cleaned and cleaned[-1] not in (0, -1):
            cleaned.append(0)
        return cleaned

    def improve(self, solution):
        best = solution.copy()
        best_cost, ok, _ = self.evaluator.evaluate(best)
        if not ok:
            best_cost = float("inf")

        current = best.copy()
        current_cost = best_cost
        start_time = time.time()
        iterations = 0
        no_improve = 0
        temp = 200.0
        alpha = 0.995
        ls_budget = max(0.4, min(2.0, self.time_budget * 0.005))
        total_ls_time = 0.0

        while time.time() - start_time < self.time_budget:
            iterations += 1
            neighbor = current.copy()

            op = self.rng.choice(
                [
                    "relocate", "swap", "two_opt",
                    "merge_trips", "split_trip", "resequence_trip",
                ]
            )
            if not getattr(self, f"_{op}")(neighbor):
                temp *= alpha
                continue

            vt = self.evaluator.extract_vehicle_times(neighbor)
            if not vt:
                temp *= alpha
                continue

            neighbor.loader_routes = assign_loaders_greedy(
                self.problem, self.evaluator, vt
            )

            cost, valid, info = self.evaluator.evaluate(neighbor)
            if not valid or cost == float("inf"):
                temp *= alpha
                continue

            if current_cost < float("inf") and cost >= current_cost * 1.20:
                temp *= alpha
                continue

            ls_start = time.time()
            sa = LoaderSA(
                self.problem,
                self.evaluator,
                temp0=50,
                alpha=0.99,
                max_iters=3000,
                time_budget=ls_budget,
                rng=self.rng,
            )
            neighbor = sa.improve(neighbor, vt)

            cost, valid, _ = self.evaluator.evaluate(neighbor)
            total_ls_time += time.time() - ls_start
            if not valid:
                temp *= alpha
                continue

            delta = cost - current_cost if current_cost < float("inf") else -1
            if delta <= 0 or self.rng.random() < math.exp(-delta / (temp + 1e-9)):
                current, current_cost = neighbor, cost
                if delta < 0:
                    no_improve = 0
                else:
                    no_improve += 1

                if cost < best_cost:
                    best, best_cost = neighbor.copy(), cost
                    no_improve = 0
                    print(
                        f"  [Joint LS] iter {iterations}, new best: {cost:.2f}"
                    )

            if no_improve > 50:
                frac = (time.time() - start_time) / self.time_budget
                if frac < 0.5:
                    current = best.copy()
                    current_cost = best_cost
                    no_improve = 0
                    temp = max(50.0, temp * 1.3)

            temp *= alpha

        return best

    def _relocate(self, sol):
        active = [
            (i, r) for i, r in enumerate(sol.vehicle_routes) if len(r) > 2
        ]
        if len(active) < 2:
            return False

        ri, route_i = self.rng.choice(active)
        orders_i = [(k, n) for k, n in enumerate(route_i) if n not in (0, -1)]
        if not orders_i:
            return False

        k, order = self.rng.choice(orders_i)
        new_route_i = self._clean_depots(route_i[:k] + route_i[k + 1 :])

        candidates = [(i, r) for i, r in active if i != ri]
        rj, route_j = self.rng.choice(candidates)

        for pos in range(1, len(route_j)):
            if route_j[pos] in (0, -1):
                continue
            candidate = route_j[:pos] + [order] + route_j[pos:]
            ok, _, _ = self.evaluator.is_vehicle_route_feasible(candidate)
            if ok:
                sol.vehicle_routes[ri] = (
                    new_route_i if len(new_route_i) > 2 else []
                )
                sol.vehicle_routes[rj] = candidate
                sol.vehicle_routes = [
                    r for r in sol.vehicle_routes if r and len(r) > 2
                ]
                return True
        return False

    def _swap(self, sol):
        active = [
            (i, r) for i, r in enumerate(sol.vehicle_routes) if len(r) > 2
        ]
        if len(active) < 2:
            return False

        (ri, route_i), (rj, route_j) = self.rng.sample(active, 2)
        orders_i = [k for k, n in enumerate(route_i) if n not in (0, -1)]
        orders_j = [k for k, n in enumerate(route_j) if n not in (0, -1)]
        if not orders_i or not orders_j:
            return False

        ki = self.rng.choice(orders_i)
        kj = self.rng.choice(orders_j)

        route_i[ki], route_j[kj] = route_j[kj], route_i[ki]
        ok_i, _, _ = self.evaluator.is_vehicle_route_feasible(route_i)
        ok_j, _, _ = self.evaluator.is_vehicle_route_feasible(route_j)

        if ok_i and ok_j:
            return True

        route_i[ki], route_j[kj] = route_j[kj], route_i[ki]
        return False

    def _two_opt(self, sol):
        active = [
            (i, r) for i, r in enumerate(sol.vehicle_routes) if len(r) > 2
        ]
        if not active:
            return False

        ri, route = self.rng.choice(active)
        trips = self._get_trips(route)
        if not trips:
            return False

        ti = self.rng.randrange(len(trips))
        trip = trips[ti]
        orders = [n for n in trip if n not in (0, -1)]
        if len(orders) < 3:
            return False

        i = self.rng.randrange(len(orders) - 1)
        j = self.rng.randrange(i + 1, len(orders))
        new_orders = orders[:i] + orders[i : j + 1][::-1] + orders[j + 1 :]
        new_trip = [0] + new_orders + [0]

        ok, _, _ = self.evaluator.is_vehicle_route_feasible(new_trip)
        if not ok:
            return False

        trips[ti] = new_trip
        sol.vehicle_routes[ri] = self._trips_to_route(trips)
        return True

    def _merge_trips(self, sol):
        active = [
            (i, r) for i, r in enumerate(sol.vehicle_routes) if len(r) > 2
        ]
        if len(active) < 2:
            return False

        (ri, route_i), (rj, route_j) = self.rng.sample(active, 2)
        trips_i = self._get_trips(route_i)
        trips_j = self._get_trips(route_j)
        if not trips_i or not trips_j:
            return False

        ti = self.rng.randrange(len(trips_i))
        tj = self.rng.randrange(len(trips_j))

        orders_i = [n for n in trips_i[ti] if n not in (0, -1)]
        orders_j = [n for n in trips_j[tj] if n not in (0, -1)]

        for merged in (
            [0] + orders_i + orders_j + [0],
            [0] + orders_j + orders_i + [0],
        ):
            ok, _, _ = self.evaluator.is_vehicle_route_feasible(merged)
            if ok:
                new_trips_i = [t for k, t in enumerate(trips_i) if k != ti]
                new_trips_j = [t for k, t in enumerate(trips_j) if k != tj]
                sol.vehicle_routes[ri] = (
                    self._trips_to_route(new_trips_i) if new_trips_i else []
                )
                sol.vehicle_routes[rj] = (
                    self._trips_to_route(new_trips_j) if new_trips_j else []
                )
                sol.vehicle_routes.append(merged)
                sol.vehicle_routes = [
                    r for r in sol.vehicle_routes if r and len(r) > 2
                ]
                return True
        return False

    def _split_trip(self, sol):
        active = [
            (i, r) for i, r in enumerate(sol.vehicle_routes) if len(r) > 2
        ]
        if not active:
            return False

        ri, route = self.rng.choice(active)
        trips = self._get_trips(route)
        if not trips:
            return False

        best_ti = max(range(len(trips)), key=lambda i: len(trips[i]))
        trip = trips[best_ti]
        orders = [n for n in trip if n not in (0, -1)]
        if len(orders) < 4:
            return False

        split_at = self.rng.randint(2, len(orders) - 2)
        t1 = [0] + orders[:split_at] + [0]
        t2 = [0] + orders[split_at:] + [0]

        ok1, _, _ = self.evaluator.is_vehicle_route_feasible(t1)
        ok2, _, _ = self.evaluator.is_vehicle_route_feasible(t2)
        if ok1 and ok2:
            trips[best_ti] = t1
            trips.insert(best_ti + 1, t2)
            sol.vehicle_routes[ri] = self._trips_to_route(trips)
            return True
        return False

    def _resequence_trip(self, sol):
        active = [
            (i, r) for i, r in enumerate(sol.vehicle_routes) if len(r) > 2
        ]
        if not active:
            return False

        ri, route = self.rng.choice(active)
        trips = self._get_trips(route)
        if not trips:
            return False

        ti = self.rng.randrange(len(trips))
        trip = trips[ti]
        orders = [n for n in trip if n not in (0, -1)]
        if len(orders) < 4:
            return False

        i = self.rng.randrange(len(orders) - 2)
        j = min(i + self.rng.randint(2, 4), len(orders))
        window = orders[i:j]
        self.rng.shuffle(window)
        new_orders = orders[:i] + window + orders[j:]
        new_trip = [0] + new_orders + [0]

        ok, _, _ = self.evaluator.is_vehicle_route_feasible(new_trip)
        if ok:
            trips[ti] = new_trip
            sol.vehicle_routes[ri] = self._trips_to_route(trips)
            return True
        return False


class OrtoolsCpsatClusterOptimizer:
    def __init__(self, problem, evaluator):
        self.problem = problem
        self.evaluator = evaluator

    def optimize(self, solution, cluster_orders, time_limit=3.0):
        if not ORTOOLS_AVAILABLE:
            return None

        cids = list(cluster_orders)
        n = len(cids)
        if n < 3 or n > 30:
            return None

        involved_v = set()
        involved_l = set()
        for ri, route in enumerate(solution.vehicle_routes):
            for node in route:
                if node in cids:
                    involved_v.add(ri)
        for li, route in enumerate(solution.loader_routes):
            for node in route:
                if node in cids:
                    involved_l.add(li)

        if len(involved_v) > 4:
            return None

        K = len(involved_v) + 1
        L = len(involved_l) + 2

        v_list = list(range(K))
        l_list = list(range(L))

        model = cp_model.CpModel()

        idx_of = {oid: i for i, oid in enumerate(cids)}
        orders_data = [self.problem.order_by_idx[oid] for oid in cids]

        assign_v = {}
        for i in range(n):
            assign_v[i] = model.NewIntVar(0, K - 1, f"v_{i}")

        pos_v = {}
        for i in range(n):
            for k in v_list:
                pos_v[(i, k)] = model.NewIntVar(0, n, f"pv_{i}_{k}")

        edge_v = {}
        for k in v_list:
            for i in range(n):
                for j in range(n):
                    if i != j:
                        edge_v[(k, i, j)] = model.NewBoolVar(
                            f"ev_{k}_{i}_{j}"
                        )

        av_vars = {}
        for k in v_list:
            for i in range(n):
                b = model.NewBoolVar(f"av_{i}_{k}")
                av_vars[(i, k)] = b
                model.Add(assign_v[i] == k).OnlyEnforceIf(b)
                model.Add(assign_v[i] != k).OnlyEnforceIf(b.Not())
                model.Add(
                    sum(edge_v[(k, j, i)] for j in range(n) if j != i) == b
                )
                model.Add(
                    sum(edge_v[(k, i, j)] for j in range(n) if j != i) == b
                )

        for k in v_list:
            for i in range(n):
                for j in range(n):
                    if i != j:
                        model.Add(
                            pos_v[(i, k)] + 1
                            <= pos_v[(j, k)]
                            + n * (1 - edge_v[(k, i, j)])
                        )

        t_v = {}
        for i, oid in enumerate(cids):
            o = orders_data[i]
            t_v[i] = model.NewIntVar(
                int(o["time_window"][0] * 100),
                int(o["time_window"][1] * 100),
                f"tv_{i}",
            )

        M_big = 999999
        for k in v_list:
            for i in range(n):
                for j in range(n):
                    if i != j:
                        oid_i, oid_j = cids[i], cids[j]
                        travel = int(
                            self.problem.v_time_flat[
                                oid_i * self.problem.size + oid_j
                            ]
                            * 100
                        )
                        service_i = int(
                            orders_data[i]["vehicle_service_time"] * 100
                        )
                        model.Add(
                            t_v[j]
                            >= t_v[i]
                            + service_i
                            + travel
                            - M_big * (1 - edge_v[(k, i, j)])
                        )

        for k in v_list:
            model.Add(
                sum(
                    int(orders_data[i]["volume"]) * av_vars[(i, k)]
                    for i in range(n)
                )
                <= int(self.problem.vehicle_capacity)
            )

        assign_l = {}
        for i in range(n):
            if orders_data[i]["loader_cnt"] > 0:
                assign_l[i] = []
                for _ in range(orders_data[i]["loader_cnt"]):
                    assign_l[i].append(
                        model.NewIntVar(0, L - 1, f"l_{i}_{_}")
                    )

        edge_l = {}
        for l in l_list:
            for i in range(n):
                for j in range(n):
                    if i != j:
                        edge_l[(l, i, j)] = model.NewBoolVar(
                            f"el_{l}_{i}_{j}"
                        )

        al_vars = {}
        aleq_vars = {}
        for l in l_list:
            for i in range(n):
                if orders_data[i]["loader_cnt"] == 0:
                    continue
                b = model.NewBoolVar(f"al_{l}_{i}")
                al_vars[(l, i)] = b
                eqs = []
                for idx, x in enumerate(assign_l[i]):
                    eq = model.NewBoolVar(f"aleq_{l}_{i}_{idx}")
                    aleq_vars[(l, i, idx)] = eq
                    model.Add(x == l).OnlyEnforceIf(eq)
                    model.Add(x != l).OnlyEnforceIf(eq.Not())
                    eqs.append(eq)
                model.AddMaxEquality(b, eqs)
                model.Add(
                    sum(
                        edge_l[(l, j, i)] for j in range(n) if j != i
                    )
                    == b
                )
                model.Add(
                    sum(
                        edge_l[(l, i, j)] for j in range(n) if j != i
                    )
                    == b
                )

        t_l = {}
        for i in range(n):
            if orders_data[i]["loader_cnt"] > 0:
                t_l[i] = model.NewIntVar(
                    0,
                    int(orders_data[i]["time_window"][1] * 100),
                    f"tl_{i}",
                )

        for i in range(n):
            if orders_data[i]["loader_cnt"] > 0:
                model.Add(t_l[i] <= t_v[i])

        for l in l_list:
            for i in range(n):
                for j in range(n):
                    if i != j:
                        if (
                            orders_data[i]["loader_cnt"] == 0
                            or orders_data[j]["loader_cnt"] == 0
                        ):
                            continue
                        travel = int(
                            self.problem.l_time_flat[
                                cids[i] * self.problem.size + cids[j]
                            ]
                            * 100
                        )
                        service_i = int(
                            orders_data[i]["loader_service_time"] * 100
                        )
                        model.Add(
                            t_l[j]
                            >= t_l[i]
                            + service_i
                            + travel
                            - M_big * (1 - edge_l[(l, i, j)])
                        )

        for l in l_list:
            for i in range(n):
                if orders_data[i]["loader_cnt"] == 0:
                    continue
                model.Add(
                    sum(aleq_vars[(l, i, idx)] for idx in range(len(assign_l[i]))) <= 8
                )

        obj_terms = []

        for k in v_list:
            used = model.NewBoolVar(f"used_v_{k}")
            model.AddMaxEquality(
                used, [av_vars[(i, k)] for i in range(n)]
            )
            obj_terms.append(
                used * int(self.problem.weights["vehicle_salary"])
            )

        for l in l_list:
            used = model.NewBoolVar(f"used_l_{l}")
            model.AddMaxEquality(
                used,
                [
                    al_vars[(l, i)]
                    for i in range(n)
                    if orders_data[i]["loader_cnt"] > 0
                ],
            )
            obj_terms.append(
                used * int(self.problem.weights["loader_salary"])
            )

        for k in v_list:
            for i in range(n):
                for j in range(n):
                    if i != j:
                        d = int(
                            self.problem.dist_flat[
                                cids[i] * self.problem.size + cids[j]
                            ]
                            * self.problem.weights["fuel_cost"]
                            * 100
                        )
                        obj_terms.append(edge_v[(k, i, j)] * d)

        lwf = self.problem.weights["loader_work"]
        for i in range(n):
            if orders_data[i]["loader_cnt"] > 0:
                sw = int(orders_data[i]["loader_service_time"] * lwf * 100)
                obj_terms.append(sw * orders_data[i]["loader_cnt"])

        model.Minimize(sum(obj_terms))

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = time_limit
        solver.parameters.num_search_workers = min(8, os.cpu_count() or 4)
        solver.parameters.log_search_progress = False
        solver.parameters.cp_model_presolve = True
        solver.parameters.linearization_level = 1

        status = solver.Solve(model)

        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return None

        new_sol = solution.copy()

        for ri in involved_v:
            new_sol.vehicle_routes[ri] = [
                n
                for n in new_sol.vehicle_routes[ri]
                if n not in cids and n not in (0, -1)
            ]
            if new_sol.vehicle_routes[ri]:
                if new_sol.vehicle_routes[ri][0] != 0:
                    new_sol.vehicle_routes[ri].insert(0, 0)
                if new_sol.vehicle_routes[ri][-1] != 0:
                    new_sol.vehicle_routes[ri].append(0)

        for k in v_list:
            orders_on_k = [
                i for i in range(n) if solver.Value(assign_v[i]) == k
            ]
            if not orders_on_k:
                continue
            orders_on_k.sort(key=lambda i: solver.Value(pos_v[(i, k)]))
            route = [0]
            for i in orders_on_k:
                route.append(cids[i])
            route.append(0)

            if k < len(involved_v):
                ri = list(involved_v)[k]
                existing = [
                    n
                    for n in new_sol.vehicle_routes[ri]
                    if n not in (0, -1)
                ]
                combined = [0] + existing + [cids[i] for i in orders_on_k] + [0]
                ok, _, _ = self.evaluator.is_vehicle_route_feasible(combined)
                if ok:
                    new_sol.vehicle_routes[ri] = combined
                else:
                    new_sol.vehicle_routes.append(route)
            else:
                new_sol.vehicle_routes.append(route)

        new_sol.vehicle_routes = [
            r for r in new_sol.vehicle_routes if r and len(r) > 2
        ]

        vt = self.evaluator.extract_vehicle_times(new_sol)
        if vt:
            new_sol.loader_routes = assign_loaders_greedy(
                self.problem, self.evaluator, vt
            )
            sa = LoaderSA(
                self.problem,
                self.evaluator,
                temp0=50,
                alpha=0.99,
                max_iters=3000,
                time_budget=2.0,
                rng=random.Random(42),
            )
            new_sol = sa.improve(new_sol, vt)

        cost, valid, _ = self.evaluator.evaluate(new_sol)
        if valid:
            return new_sol
        return None


def run_pipeline(
    problem, evaluator, params, time_limit, pyvrp_cap, seed=None,
    force_joint=True, force_cpsat=True
):
    base_time = time_limit
    solver_time = min(base_time * params["pyvrp_time_frac"] * 0.90, pyvrp_cap)

    remaining = max(base_time - solver_time - 2.0, 0)
    sa_time = remaining * 0.25
    joint_time = remaining * 0.40 if force_joint else 0.0
    cpsat_time = remaining * 0.25 if (force_cpsat and ORTOOLS_AVAILABLE) else 0.0

    print(f"  [Phase 1] PyVRP start (solver_time={solver_time:.1f}s, penalty_scale={params['penalty_scale']:.2f}, loader_penalty={params['loader_penalty_weight']:.2f})")
    sol = solve_vehicles_pyvrp(
        problem,
        solver_time,
        params["penalty_scale"],
        params["loader_penalty_weight"],
        seed=seed,
    )

    if not sol or not sol.vehicle_routes:
        print(f"  [Phase 1] PyVRP returned None — no vehicle routes found")
        return None
    else:
        n_routes = len(sol.vehicle_routes)
        served = set(n for r in sol.vehicle_routes for n in r if n not in (0, -1))
        print(f"  [Phase 1] PyVRP OK: {n_routes} routes, {len(served)} orders served, {len(sol.unserved_optional)} unserved optional")

    best_sol = sol
    vt = evaluator.extract_vehicle_times(best_sol)
    best_sol.loader_routes = assign_loaders_greedy(problem, evaluator, vt)

    init_cost, valid, _ = evaluator.evaluate(best_sol)
    print(f"  [Initial] Cost: {init_cost:.2f}, Vehicles: {best_sol.number_of_vehicles_in_use()}, Loaders: {best_sol.number_of_loaders_in_use()}")

    rng = random.Random(seed)
    if valid and sa_time > 3.0:
        loader_sa = LoaderSA(
            problem, evaluator, time_budget=sa_time, rng=rng
        )
        best_sol = loader_sa.improve(best_sol, vt)
        sa_cost, valid, _ = evaluator.evaluate(best_sol)
        if not valid:
            print(f"  [Loader SA] Infeasible — будет попытка Joint LS")
        else:
            print(f"  [Loader SA] Cost: {sa_cost:.2f}")

    if joint_time > 5.0:
        try:
            print(f"  Starting Joint Local Search ({joint_time:.0f}s)...")
            jls = JointLocalSearch(
                problem, evaluator, time_budget=joint_time, rng=rng
            )
            jls_sol = jls.improve(best_sol)
            jls_cost, jls_valid, _ = evaluator.evaluate(jls_sol)
            if jls_valid:
                best_sol = jls_sol
                init_cost = jls_cost
                valid = True
                print(f"  [Joint LS] Final Cost: {jls_cost:.2f}")
            else:
                print(f"  [Joint LS] Could not repair — solution still infeasible")
        except Exception as e:
            print(f"  Joint LS error: {e}")

    if not valid:
        print("  Pipeline could not produce a feasible solution")
        return None

    if cpsat_time > 5.0 and ORTOOLS_AVAILABLE:
        print(f"  Starting CP-SAT LNS ({cpsat_time:.0f}s)...")
        cpsat_opt = OrtoolsCpsatClusterOptimizer(problem, evaluator)
        start_cpsat = time.time()
        iterations = 0
        improvements = 0

        while time.time() - start_cpsat < cpsat_time:
            iterations += 1
            active = [
                (i, r)
                for i, r in enumerate(best_sol.vehicle_routes)
                if len(r) > 2
            ]
            if len(active) < 2:
                break

            num_routes = min(4, len(active))
            if iterations % 3 == 0 and len(active) >= 3:
                centroids = []
                for i, r in active:
                    xs = [problem.order_by_idx[n]["x"] for n in r if n not in (0, -1)]
                    ys = [problem.order_by_idx[n]["y"] for n in r if n not in (0, -1)]
                    if xs:
                        centroids.append((i, sum(xs) / len(xs), sum(ys) / len(ys)))
                if len(centroids) >= num_routes:
                    start = rng.choice(centroids)
                    centroids.sort(key=lambda c: (c[1] - start[1]) ** 2 + (c[2] - start[2]) ** 2)
                    samples = [(c[0], best_sol.vehicle_routes[c[0]]) for c in centroids[:num_routes]]
                else:
                    samples = rng.sample(active, num_routes)
            else:
                samples = rng.sample(active, num_routes)

            cluster_orders = set()
            loaders_in_cluster = 0
            for _, r in samples:
                for n in r:
                    if n not in (0, -1):
                        cluster_orders.add(n)
                        if problem.order_by_idx[n]["loader_cnt"] > 0:
                            loaders_in_cluster += 1

            if loaders_in_cluster < 2 and len(active) >= 3:
                loader_routes = [(i, r) for i, r in active
                                 if any(problem.order_by_idx[n]["loader_cnt"] > 0 for n in r if n not in (0, -1))]
                if loader_routes:
                    extra = rng.sample(loader_routes, min(1, len(loader_routes)))
                    for i, r in extra:
                        if i not in [s[0] for s in samples]:
                            samples.append((i, r))
                            for n in r:
                                if n not in (0, -1):
                                    cluster_orders.add(n)

            if len(cluster_orders) > 30:
                cluster_orders = set(rng.sample(list(cluster_orders), 30))
            elif len(cluster_orders) < 4:
                continue

            per_cluster_time = min(6.0, max(2.0, cpsat_time / max(iterations + 1, 8)))

            improved = cpsat_opt.optimize(
                best_sol, cluster_orders, time_limit=per_cluster_time
            )
            if improved:
                cost, valid, _ = evaluator.evaluate(improved)
                if valid:
                    current_best, _ = evaluator.evaluate(best_sol)
                    if cost < current_best:
                        best_sol = improved
                        improvements += 1
                        print(
                            f"    [CP-SAT LNS] iter {iterations}, new best: {cost:.2f} (#{improvements})"
                        )

        final_cost, _, _ = evaluator.evaluate(best_sol)
        print(f"  [CP-SAT LNS] Final Cost: {final_cost:.2f}, improvements: {improvements}")

    return best_sol

def solve(raw_data, time_limit=900, seed=42):
    random.seed(seed)
    np.random.seed(seed)

    data = clean_json_keys(raw_data)
    problem = ProblemData(data)
    evaluator = Evaluator(problem)
    N = problem.number_of_orders

    print(
        f"Orders: {N}, Time limit: {time_limit}s, CP-SAT LNS: {ORTOOLS_AVAILABLE}"
    )

    start_time = time.time()
    best_cost, best_params, best_solution = float("inf"), None, None
    warm_up_solutions = {}

    pyvrp_frac_bounds = (0.50, 0.80)
    pyvrp_cap = float("inf")

    if time_limit <= 60:
        ng_budget = 2
        print("Mode: Short Time Limit")
    elif N <= 200:
        ng_budget = 10
        print("Mode: Small/Medium Instance")
    else:
        ng_budget = 5
        print("Mode: Large Instance")

    parametrization = ng.p.Dict(
        penalty_scale=ng.p.Scalar(lower=0.8, upper=2.0),
        pyvrp_time_frac=ng.p.Scalar(
            lower=pyvrp_frac_bounds[0], upper=pyvrp_frac_bounds[1]
        ),
        loader_penalty_weight=ng.p.Scalar(lower=0.0, upper=1.0),
    )

    optimizer = ng.optimizers.NGOpt(
        parametrization=parametrization, budget=ng_budget
    )
    eval_time = (time_limit * 0.25) / ng_budget

    def objective(params):
        nonlocal best_cost, best_params, best_solution
        sol = run_pipeline(
            problem, evaluator, params,
            eval_time, pyvrp_cap, seed=seed,
            force_joint=True, force_cpsat=True,
        )
        if sol is None:
            return float("inf")

        cost, valid, _ = evaluator.evaluate(sol)
        if valid:
            param_key = (round(params["penalty_scale"], 2),
                        round(params["pyvrp_time_frac"], 2),
                        round(params["loader_penalty_weight"], 2))
            if param_key not in warm_up_solutions or cost < warm_up_solutions[param_key][0]:
                warm_up_solutions[param_key] = (cost, sol.copy())

            if cost < best_cost:
                best_cost, best_params, best_solution = cost, params, sol
                print(f"  [NG Sweep] Best: {cost:.2f} | Params: {params}")
            else:
                print(f"  [NG Sweep] Cur: {cost:.2f} | Params: {params}")
        return cost if valid else float("inf")

    print(f"Starting Nevergrad Warm-Up ({ng_budget} iterations)...")
    optimizer.minimize(objective)

    remaining_time = time_limit * 0.70

    if best_params is None:
        best_params = {"penalty_scale": 1.4, "pyvrp_time_frac": 0.6, "loader_penalty_weight": 0.0}
        print("  No valid warm-up params, using defaults")
    else:
        print(f"  Warm-up best: cost={best_cost:.2f}, params={best_params}, routes={len(best_solution.vehicle_routes) if best_solution else 0}")
        n_feasible = sum(1 for v in warm_up_solutions.values() if v[0] < float('inf'))
        print(f"  Warm-up summary: {len(warm_up_solutions)} param sets tried, {n_feasible} feasible solutions")

    elapsed_before_deep = time.time() - start_time
    remaining_time = max(0, remaining_time - elapsed_before_deep)
    print(f"\nStarting Deep Convergence ({remaining_time:.0f}s rem, elapsed={elapsed_before_deep:.0f}s)...")

    final_sol = None
    final_cost = float("inf")
    if remaining_time < 5.0:
        print(f"  [Deep Conv] Skipped — insufficient time remaining")
    else:
        final_sol = run_pipeline(
            problem, evaluator, best_params,
            remaining_time, pyvrp_cap, seed=seed,
            force_joint=True, force_cpsat=True,
        )

    if final_sol:
        final_cost, valid, _ = evaluator.evaluate(final_sol)
        if valid and final_cost < best_cost:
            best_solution, best_cost = final_sol, final_cost
            print(f"  [Deep Conv] Final Cost: {final_cost:.2f}")
        else:
            print(f"  [Deep Conv] Cost: {final_cost:.2f} (not better than warm-up {best_cost:.2f})")
    else:
        print(f"  [Deep Conv] Pipeline returned None")

    if final_cost > best_cost and best_solution is not None:
        print(f"  [Fallback] Using best warm-up solution: {best_cost:.2f}")

    if len(warm_up_solutions) > 1:
        sorted_sols = sorted(warm_up_solutions.items(), key=lambda x: x[1][0])
        for n_extra, (param_key, (cost, sol)) in enumerate(sorted_sols[1:3], 1):
            if cost >= best_cost * 1.02:
                continue
            rem = max(0, time_limit - (time.time() - start_time))
            extra_budget = min(time_limit * 0.05, rem)
            if extra_budget < 5.0:
                print(f"  [Extra #{n_extra}] Skipped — {time.time()-start_time:.0f}s elapsed, {extra_budget:.0f}s rem")
                continue
            print(f"  [Extra #{n_extra}] Trying warm-up params {param_key} (budget={extra_budget:.0f}s)...")
            extra_sol = run_pipeline(
                problem, evaluator,
                {"penalty_scale": param_key[0], "pyvrp_time_frac": param_key[1],
                 "loader_penalty_weight": param_key[2]},
                extra_budget, pyvrp_cap, seed=seed+1,
                force_joint=True, force_cpsat=True
            )
            if extra_sol:
                ec, ev, _ = evaluator.evaluate(extra_sol)
                if ev and ec < best_cost:
                    best_solution, best_cost = extra_sol, ec
                    print(f"  [Extra #{n_extra}] New best: {ec:.2f}")
                else:
                    print(f"  [Extra #{n_extra}] Cost: {ec:.2f} (not better than {best_cost:.2f})")
            else:
                print(f"  [Extra #{n_extra}] Pipeline returned None")

    rem = max(0, time_limit - (time.time() - start_time))
    if (best_params is None or best_params.get("loader_penalty_weight", 1.0) != 0.0) and rem >= 5.0:
        bonus_budget = min(time_limit * 0.35, rem)
        print(f"  [Bonus] Trying loader_penalty_weight=0.0 (budget={bonus_budget:.0f}s, {time.time()-start_time:.0f}s elapsed)...")
        bonus_params = {"penalty_scale": 1.4, "pyvrp_time_frac": 0.6, "loader_penalty_weight": 0.0}
        bonus_sol = run_pipeline(
            problem, evaluator, bonus_params,
            bonus_budget, pyvrp_cap, seed=seed,
            force_joint=True, force_cpsat=True
        )
        if bonus_sol:
            bc, bv, _ = evaluator.evaluate(bonus_sol)
            if bv and bc < best_cost:
                best_solution, best_cost = bonus_sol, bc
                print(f"  [Bonus] New best: {bc:.2f}")
            else:
                print(f"  [Bonus] Solution found but cost={bc:.2f} not better than {best_cost:.2f}")
        else:
            print(f"  [Bonus] Pipeline returned None")

    elapsed_total = time.time() - start_time
    if best_solution is None:
        print(f"FAILED: No valid solution found after {elapsed_total:.1f}s.")
        return None

    vehicle_output, loader_output = [], []
    vid = 0
    for route in best_solution.vehicle_routes:
        if len(route) <= 2:
            continue
        ok, times, _ = evaluator.is_vehicle_route_feasible(route)
        if not ok:
            continue
        trips = [route]

        time_idx = 0
        for trip in trips:
            node_ids = [0 if n == -1 else n for n in trip if n != 0]
            trip_times = times[time_idx : time_idx + len(node_ids)]
            time_idx += len(node_ids)

            vtf = evaluator.v_time_flat
            oi = evaluator.order_by_idx
            shift_limit = evaluator.problem.vehicle_shift_length
            sz = evaluator.size

            def _trip_shift_ok(trip_route, trip_tms):
                if not trip_route:
                    return True
                oids = [n for n in trip_route if n not in (0, -1)]
                if not oids:
                    return True
                dep = trip_tms[0] - vtf[0 * sz + oids[0]]
                ret = (
                    trip_tms[-1]
                    + vtf[oids[-1] * sz + 0]
                    + oi[oids[-1]]["vehicle_service_time"]
                )
                return ret - dep <= shift_limit + 1e-6

            if not _trip_shift_ok(trip, trip_times):
                pure_orders = [n for n in trip if n not in (0, -1)]
                split_idx = 1
                split_ok = False
                while split_idx < len(pure_orders):
                    left_orders = pure_orders[:split_idx]
                    right_orders = pure_orders[split_idx:]
                    left_route = [0] + left_orders + [0]
                    right_route = [0] + right_orders + [0]
                    left_times = trip_times[:split_idx]
                    right_times = trip_times[split_idx:]
                    if _trip_shift_ok(left_route, left_times) and _trip_shift_ok(
                        right_route, right_times
                    ):
                        vid += 1
                        vehicle_output.append(
                            {"id": vid, "route": left_route, "time": left_times}
                        )
                        vid += 1
                        vehicle_output.append(
                            {"id": vid, "route": right_route, "time": right_times}
                        )
                        split_ok = True
                        break
                    split_idx += 1
                if not split_ok:
                    continue
            else:
                vid += 1
                clean_route = [0 if n == -1 else n for n in trip]
                vehicle_output.append(
                    {"id": vid, "route": clean_route, "time": trip_times}
                )
    for lid, route in enumerate(best_solution.loader_routes):
        if route:
            loader_output.append({"id": lid + 1, "route": route})

    output_sol = Solution()
    output_sol.vehicle_routes = [v["route"] for v in vehicle_output]
    output_sol.loader_routes = [loader["route"] for loader in loader_output]
    output_sol.unserved_optional = set(best_solution.unserved_optional)
    output_cost, output_valid, _ = evaluator.evaluate(output_sol)
    if output_valid:
        best_cost = output_cost

    result = {
        "vehicles": vehicle_output,
        "loaders": loader_output,
        "unserved_optional": list(best_solution.unserved_optional),
        "_cost": best_cost,
        "_evaluator": evaluator,
    }
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