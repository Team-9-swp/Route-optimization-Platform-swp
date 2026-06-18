import argparse
import json
import math
import random
import sys
import time

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
        self.depot_x = depot["x"]
        self.depot_y = depot["y"]
        self.loading_time_at_depot = depot.get("load_time", 0.0)

        self.orders = raw_data["orders"]
        self.number_of_orders = len(self.orders)
        self.weights = raw_data["weights"]

        self.locations = [(self.depot_x, self.depot_y)]
        for order in self.orders:
            self.locations.append((order["x"], order["y"]))

        size = self.number_of_orders + 1
        self.distance_matrix = [[0.0] * size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                dx = self.locations[i][0] - self.locations[j][0]
                dy = self.locations[i][1] - self.locations[j][1]
                self.distance_matrix[i][j] = round_mathematically(math.sqrt(dx * dx + dy * dy), 2)

        self.order_by_id = {order["id"]: order for order in self.orders}

        self.mandatory_order_ids = [
            order["id"] for order in self.orders if order["optional"] == 0
        ]
        self.optional_order_ids = [
            order["id"] for order in self.orders if order["optional"] == 1
        ]

    def distance(self, point_a, point_b):
        return self.distance_matrix[point_a][point_b]

    def travel_time(self, point_a, point_b, speed):
        return round_mathematically(self.distance(point_a, point_b) / speed, 2)

class Solution:
    def __init__(self):
        self.vehicle_routes = [] 
        self.loader_routes = [] 
        self.unserved_optional = set()

    def copy(self):
        new_solution = Solution()
        new_solution.vehicle_routes = [list(route) for route in self.vehicle_routes]
        new_solution.loader_routes = [list(route) for route in self.loader_routes]
        new_solution.unserved_optional = set(self.unserved_optional)
        return new_solution

    def get_all_served_order_ids(self):
        served = set()
        for route in self.vehicle_routes:
            for order_id in route:
                if order_id != 0:
                    served.add(order_id)
        return served

    def number_of_vehicles_in_use(self):
        return sum(1 for route in self.vehicle_routes if len(route) > 2)

    def number_of_loaders_in_use(self):
        return sum(1 for route in self.loader_routes if route)

class Evaluator:
    def __init__(self, problem):
        self.problem = problem

    def is_vehicle_route_feasible(self, route):
        if len(route) <= 2:
            return True, [], 0.0

        raw_arrival = {}
        current_time = 0.0
        total_distance = 0.0
        for i in range(len(route) - 1):
            from_node = route[i]
            to_node = route[i + 1]
            travel = self.problem.travel_time(from_node, to_node, self.problem.vehicle_speed)
            current_time += travel
            total_distance += self.problem.distance(from_node, to_node)
            if to_node != 0:
                raw_arrival[to_node] = current_time
                current_time += self.problem.order_by_id[to_node]["vehicle_service_time"]

        upper_bound = float("inf")
        for node in route:
            if node == 0:
                continue
            tw_start, tw_end = self.problem.order_by_id[node]["time_window"]
            upper_bound = min(upper_bound, tw_end - raw_arrival[node])

        if upper_bound < -1e-6:
            return False, [], 0.0

        departure_from_depot = max(0.0, upper_bound)

        start_times = []
        current_time = departure_from_depot
        for i in range(len(route) - 1):
            from_node = route[i]
            to_node = route[i + 1]
            current_time += self.problem.travel_time(from_node, to_node, self.problem.vehicle_speed)
            if to_node != 0:
                tw_start, tw_end = self.problem.order_by_id[to_node]["time_window"]
                actual_start = max(current_time, tw_start)
                if actual_start > tw_end + 1e-6:
                    return False, [], 0.0
                start_times.append(round_mathematically(actual_start, 2))
                current_time = actual_start + self.problem.order_by_id[to_node]["vehicle_service_time"]

        total_shift_time = current_time - departure_from_depot
        if total_shift_time > self.problem.vehicle_shift_length + 1e-6:
            return False, [], 0.0

        total_volume = sum(
            self.problem.order_by_id[node]["volume"] for node in route if node != 0
        )
        if total_volume > self.problem.vehicle_capacity + 1e-6:
            return False, [], 0.0

        return True, start_times, total_distance

    def is_loader_route_feasible(self, route, vehicle_arrival_times):
        if not route:
            return True

        first_order = route[0]
        if first_order not in vehicle_arrival_times:
            return False

        current_time = (
            vehicle_arrival_times[first_order]
            + self.problem.order_by_id[first_order]["loader_service_time"]
        )

        for i in range(1, len(route)):
            previous = route[i - 1]
            current_node = route[i]
            current_time += self.problem.travel_time(previous, current_node, self.problem.loader_speed)
            if current_node not in vehicle_arrival_times:
                return False
            if current_time > vehicle_arrival_times[current_node] + 1e-6:
                return False
            current_time = (
                vehicle_arrival_times[current_node]
                + self.problem.order_by_id[current_node]["loader_service_time"]
            )

        current_time += self.problem.travel_time(route[-1], first_order, self.problem.loader_speed)
        total_shift = current_time - vehicle_arrival_times[first_order]
        return total_shift <= self.problem.loader_shift_length + 1e-6

    def evaluate(self, solution):
        all_visited = []
        for route in solution.vehicle_routes:
            for node in route:
                if node != 0:
                    all_visited.append(node)
        if len(all_visited) != len(set(all_visited)):
            return float("inf"), False, {}

        served = set(all_visited)
        for order in self.problem.orders:
            if order["optional"] == 0 and order["id"] not in served:
                return float("inf"), False, {}

        vehicle_arrival_times = {}
        total_vehicle_distance = 0.0
        for route in solution.vehicle_routes:
            if len(route) <= 2:
                continue
            feasible, times, distance = self.is_vehicle_route_feasible(route)
            if not feasible:
                return float("inf"), False, {}
            total_vehicle_distance += distance
            time_index = 0
            for node in route:
                if node != 0:
                    vehicle_arrival_times[node] = times[time_index]
                    time_index += 1

        total_loader_work = 0.0
        loader_visit_count = {order["id"]: 0 for order in self.problem.orders}
        for loader_route in solution.loader_routes:
            if not loader_route:
                continue
            for node in loader_route:
                loader_visit_count[node] += 1
            if not self.is_loader_route_feasible(loader_route, vehicle_arrival_times):
                return float("inf"), False, {}
            total_loader_work += self.problem.order_by_id[loader_route[0]]["loader_service_time"]

        for order in self.problem.orders:
            if order["id"] in served and order["loader_cnt"] > 0:
                if loader_visit_count[order["id"]] < order["loader_cnt"]:
                    return float("inf"), False, {}

        used_vehicles = solution.number_of_vehicles_in_use()
        used_loaders = solution.number_of_loaders_in_use()

        cost = (
            used_vehicles * self.problem.weights["vehicle_salary"]
            + total_vehicle_distance * self.problem.weights["fuel_cost"]
            + used_loaders * self.problem.weights["loader_salary"]
            + total_loader_work * self.problem.weights["loader_work"]
            + len(solution.unserved_optional) * self.problem.weights["optional_order_penalty"]
        )

        details = {
            "used_vehicles": used_vehicles,
            "vehicle_distance": total_vehicle_distance,
            "used_loaders": used_loaders,
            "loader_work": total_loader_work,
            "unserved_optional": len(solution.unserved_optional),
            "vehicle_arrival_times": vehicle_arrival_times,
        }
        return cost, True, details

    def extract_vehicle_arrival_times(self, solution):
        times = {}
        for route in solution.vehicle_routes:
            if len(route) <= 2:
                continue
            feasible, start_times, _ = self.is_vehicle_route_feasible(route)
            if not feasible:
                continue
            idx = 0
            for node in route:
                if node != 0:
                    times[node] = start_times[idx]
                    idx += 1
        return times


class LoaderSA:
    def __init__(self, problem, evaluator, temp0=100, alpha=0.998,
                 max_iters=50000, time_budget=30.0):
        self.problem = problem
        self.evaluator = evaluator
        self.temp0 = temp0
        self.alpha = alpha
        self.max_iters = max_iters
        self.time_budget = time_budget

    def improve(self, solution, vehicle_times):
        best = solution.copy()
        best_cost, ok, _ = self.evaluator.evaluate(best)
        if not ok:
            return best

        current = solution.copy()
        current_cost = best_cost
        temperature = self.temp0
        start_time = time.time()

        for iteration in range(self.max_iters):
            if time.time() - start_time > self.time_budget:
                break

            neighbor = current.copy()
            operator = random.choice(["relocate", "swap", "two_opt", "merge"])
            generated = False

            if operator == "relocate":
                generated = self._relocate(neighbor, vehicle_times)
            elif operator == "swap":
                generated = self._swap(neighbor, vehicle_times)
            elif operator == "two_opt":
                generated = self._two_opt(neighbor, vehicle_times)
            elif operator == "merge":
                generated = self._merge(neighbor, vehicle_times)

            if not generated:
                temperature *= self.alpha
                continue

            cost, valid, _ = self.evaluator.evaluate(neighbor)
            if not valid:
                temperature *= self.alpha
                continue

            delta = cost - current_cost
            if delta < 0 or random.random() < math.exp(-delta / (temperature + 1e-9)):
                current = neighbor
                current_cost = cost
                if current_cost < best_cost:
                    best = neighbor.copy()
                    best_cost = current_cost

            temperature *= self.alpha

        return best

    def _relocate(self, solution, vehicle_times):
        if len(solution.loader_routes) < 1:
            return False
        ri = random.randrange(len(solution.loader_routes))
        if not solution.loader_routes[ri]:
            return False
        idx = random.randrange(len(solution.loader_routes[ri]))
        order_id = solution.loader_routes[ri][idx]

        route_without = solution.loader_routes[ri][:idx] + solution.loader_routes[ri][idx + 1:]

        candidates = list(range(len(solution.loader_routes)))
        random.shuffle(candidates)
        for rj in candidates:
            if rj == ri:
                continue
            route = solution.loader_routes[rj]
            if order_id in route:
                continue
            pos = random.randrange(len(route) + 1)
            candidate = route[:pos] + [order_id] + route[pos:]
            if self.evaluator.is_loader_route_feasible(candidate, vehicle_times):
                new_routes = []
                for k, r in enumerate(solution.loader_routes):
                    if k == ri and not route_without:
                        continue
                    if k == ri:
                        new_routes.append(route_without)
                    elif k == rj:
                        new_routes.append(candidate)
                    else:
                        new_routes.append(r)
                solution.loader_routes[:] = new_routes
                return True

        if route_without and self.evaluator.is_loader_route_feasible([order_id], vehicle_times):
            solution.loader_routes[ri] = route_without
            solution.loader_routes.append([order_id])
            return True

        return False

    def _swap(self, solution, vehicle_times):
        if len(solution.loader_routes) < 2:
            return False
        ri, rj = random.sample(range(len(solution.loader_routes)), 2)
        if not solution.loader_routes[ri] or not solution.loader_routes[rj]:
            return False
        i = random.randrange(len(solution.loader_routes[ri]))
        j = random.randrange(len(solution.loader_routes[rj]))
        oi = solution.loader_routes[ri][i]
        oj = solution.loader_routes[rj][j]
        if oi in solution.loader_routes[rj] or oj in solution.loader_routes[ri]:
            return False

        solution.loader_routes[ri][i], solution.loader_routes[rj][j] = oj, oi
        ok = (self.evaluator.is_loader_route_feasible(solution.loader_routes[ri], vehicle_times)
              and self.evaluator.is_loader_route_feasible(solution.loader_routes[rj], vehicle_times))
        if not ok:
            solution.loader_routes[ri][i], solution.loader_routes[rj][j] = oi, oj
            return False
        return True

    def _two_opt(self, solution, vehicle_times):
        if not solution.loader_routes:
            return False
        ri = random.randrange(len(solution.loader_routes))
        route = solution.loader_routes[ri]
        if len(route) < 3:
            return False
        i = random.randrange(len(route) - 1)
        j = random.randrange(i + 1, len(route))
        candidate = route[:i] + route[i:j + 1][::-1] + route[j + 1:]
        if self.evaluator.is_loader_route_feasible(candidate, vehicle_times):
            solution.loader_routes[ri] = candidate
            return True
        return False

    def _merge(self, solution, vehicle_times):
        if len(solution.loader_routes) < 2:
            return False
        ri, rj = random.sample(range(len(solution.loader_routes)), 2)
        a, b = solution.loader_routes[ri], solution.loader_routes[rj]
        if set(a) & set(b):
            return False
        for merged in (a + b, b + a):
            if self.evaluator.is_loader_route_feasible(merged, vehicle_times):
                new_routes = [r for k, r in enumerate(solution.loader_routes) if k not in (ri, rj)]
                new_routes.append(merged)
                solution.loader_routes[:] = new_routes
                return True
        return False

def build_vehicle_routes_greedy(problem, evaluator, order_sequence):
    solution = Solution()

    for order_id in order_sequence:
        best_cost = float("inf")
        best_action = None 

        for route_index, route in enumerate(solution.vehicle_routes):
            if len(route) <= 2:
                continue

            current_volume = sum(problem.order_by_id[n]["volume"] for n in route if n != 0)
            if current_volume + problem.order_by_id[order_id]["volume"] > problem.vehicle_capacity:
                continue

            for position in range(1, len(route)):
                candidate_route = route[:position] + [order_id] + route[position:]
                feasible, _, _ = evaluator.is_vehicle_route_feasible(candidate_route)
                if feasible:
                    extra_distance = (
                        problem.distance(route[position - 1], order_id)
                        + problem.distance(order_id, route[position])
                        - problem.distance(route[position - 1], route[position])
                    )
                    if extra_distance < best_cost:
                        best_cost = extra_distance
                        best_action = ("insert", route_index, position, candidate_route)

        new_route = [0, order_id, 0]
        feasible, _, _ = evaluator.is_vehicle_route_feasible(new_route)
        if feasible:
            cost_new = problem.distance(0, order_id) + problem.distance(order_id, 0)
            if cost_new < best_cost:
                best_cost = cost_new
                best_action = ("new", None, None, new_route)

        if best_action is None:
            solution.vehicle_routes.append([0, order_id, 0])
        elif best_action[0] == "new":
            solution.vehicle_routes.append(best_action[3])
        else:
            solution.vehicle_routes[best_action[1]] = best_action[3]

    return solution


def generate_order_sequences(problem, restart_index, seed):
    random.seed(restart_index * 7 + seed)
    all_ids = problem.mandatory_order_ids + problem.optional_order_ids
    random.shuffle(all_ids)
    all_ids.sort(key=lambda oid: problem.order_by_id[oid]["time_window"][1] + random.uniform(-5, 5))
    return all_ids


def apply_two_opt(problem, evaluator, routes):
    improved = True
    while improved:
        improved = False
        for route_index in range(len(routes)):
            route = routes[route_index]
            if len(route) <= 4:
                continue

            best_route = route
            best_distance = sum(
                problem.distance(route[k], route[k + 1]) for k in range(len(route) - 1)
            )

            for i in range(1, len(route) - 2):
                for j in range(i + 1, len(route) - 1):
                    candidate = route[:i] + route[i:j + 1][::-1] + route[j + 1:]
                    feasible, _, _ = evaluator.is_vehicle_route_feasible(candidate)
                    if feasible:
                        dist = sum(
                            problem.distance(candidate[k], candidate[k + 1])
                            for k in range(len(candidate) - 1)
                        )
                        if dist < best_distance - 1e-6:
                            best_route = candidate
                            best_distance = dist
                            improved = True

            routes[route_index] = best_route
    return routes


def apply_relocate(problem, evaluator, routes, max_passes=999999):
    improved = True
    passes_done = 0
    while improved and passes_done < max_passes:
        passes_done += 1
        improved = False

        for route_index in range(len(routes)):
            route = routes[route_index]
            if len(route) <= 3:
                continue

            for position in range(1, len(route) - 1):
                order_id = route[position]

                route_without_order = route[:position] + route[position + 1:]
                if len(route_without_order) > 2:
                    temp_routes = routes[:route_index] + [route_without_order] + routes[route_index + 1:]
                else:
                    temp_routes = routes[:route_index] + routes[route_index + 1:]

                for target_index in range(len(temp_routes)):
                    target_route = temp_routes[target_index]
                    if len(target_route) <= 2:
                        continue
                    current_volume = sum(problem.order_by_id[n]["volume"] for n in target_route if n != 0)
                    if current_volume + problem.order_by_id[order_id]["volume"] > problem.vehicle_capacity:
                        continue

                    for insert_pos in range(1, len(target_route)):
                        candidate = target_route[:insert_pos] + [order_id] + target_route[insert_pos:]
                        feasible, _, _ = evaluator.is_vehicle_route_feasible(candidate)
                        if feasible:
                            new_routes = temp_routes[:target_index] + [candidate] + temp_routes[target_index + 1:]
                            if len(new_routes) < len(routes):
                                routes = new_routes
                                improved = True
                                break
                    if improved:
                        break
                if improved:
                    break
            if improved:
                break
    return routes


def apply_swap(problem, evaluator, routes, max_passes=999999):
    improved = True
    passes_done = 0
    while improved and passes_done < max_passes:
        passes_done += 1
        improved = False

        for route_i in range(len(routes)):
            for route_j in range(route_i + 1, len(routes)):
                if len(routes[route_i]) <= 3 or len(routes[route_j]) <= 3:
                    continue

                for pos_i in range(1, len(routes[route_i]) - 1):
                    for pos_j in range(1, len(routes[route_j]) - 1):
                        new_route_i = routes[route_i][:pos_i] + [routes[route_j][pos_j]] + routes[route_i][pos_i + 1:]
                        new_route_j = routes[route_j][:pos_j] + [routes[route_i][pos_i]] + routes[route_j][pos_j + 1:]

                        vol_i = sum(problem.order_by_id[n]["volume"] for n in new_route_i if n != 0)
                        vol_j = sum(problem.order_by_id[n]["volume"] for n in new_route_j if n != 0)
                        if vol_i > problem.vehicle_capacity or vol_j > problem.vehicle_capacity:
                            continue

                        feasible_i, _, _ = evaluator.is_vehicle_route_feasible(new_route_i)
                        feasible_j, _, _ = evaluator.is_vehicle_route_feasible(new_route_j)
                        if feasible_i and feasible_j:
                            old_distance = (
                                sum(problem.distance(routes[route_i][k], routes[route_i][k + 1])
                                    for k in range(len(routes[route_i]) - 1))
                                + sum(problem.distance(routes[route_j][k], routes[route_j][k + 1])
                                      for k in range(len(routes[route_j]) - 1))
                            )
                            new_distance = (
                                sum(problem.distance(new_route_i[k], new_route_i[k + 1])
                                    for k in range(len(new_route_i) - 1))
                                + sum(problem.distance(new_route_j[k], new_route_j[k + 1])
                                      for k in range(len(new_route_j) - 1))
                            )
                            if new_distance < old_distance - 1e-6:
                                routes[route_i] = new_route_i
                                routes[route_j] = new_route_j
                                improved = True
                                break
                    if improved:
                        break
                if improved:
                    break
            if improved:
                break
    return routes


def assign_loaders_greedy(problem, evaluator, vehicle_arrival_times):
    demands = []
    for order in problem.orders:
        if order["loader_cnt"] > 0 and order["id"] in vehicle_arrival_times:
            for _ in range(order["loader_cnt"]):
                demands.append((
                    order["id"],
                    vehicle_arrival_times[order["id"]],
                    order["loader_service_time"],
                ))

    demands.sort(key=lambda x: (x[1], x[2]))

    loader_routes = []
    for order_id, _, _ in demands:
        placed = False
        best_route_index = -1
        best_position = -1
        best_start_service_time = float("inf")

        for route_index, route in enumerate(loader_routes):
            if order_id in route:
                continue
            for position in range(len(route) + 1):
                candidate = route[:position] + [order_id] + route[position:]
                if evaluator.is_loader_route_feasible(candidate, vehicle_arrival_times):
                    first_service = problem.order_by_id[candidate[0]]["loader_service_time"]
                    if first_service < best_start_service_time:
                        best_start_service_time = first_service
                        best_route_index = route_index
                        best_position = position
                    break  

        if best_route_index >= 0:
            route = loader_routes[best_route_index]
            loader_routes[best_route_index] = route[:best_position] + [order_id] + route[best_position:]
            placed = True

        if not placed:
            loader_routes.append([order_id])

    return loader_routes


def solve(problem_data, seed):
    """Run the full greedy + local search pipeline and return the solution JSON."""
    random.seed(seed)

    problem = ProblemData(problem_data)
    evaluator = Evaluator(problem)

    if problem.number_of_orders <= 200:
        number_of_restarts = 50
    elif problem.number_of_orders <= 500:
        number_of_restarts = 20
    else:
        number_of_restarts = 8

    print(f"Greedy construction ({number_of_restarts} restarts)")

    best_solution = None
    best_cost = float("inf")

    for restart in range(number_of_restarts):
        order_sequence = generate_order_sequences(problem, restart, seed)
        solution = build_vehicle_routes_greedy(problem, evaluator, order_sequence)
        solution.vehicle_routes = apply_two_opt(problem, evaluator, solution.vehicle_routes)

        vehicle_times = evaluator.extract_vehicle_arrival_times(solution)
        solution.loader_routes = assign_loaders_greedy(problem, evaluator, vehicle_times)

        cost, feasible, details = evaluator.evaluate(solution)
        if feasible and cost < best_cost:
            best_cost = cost
            best_solution = solution.copy()
            if restart % 5 == 0:
                print(f"  restart {restart}: cost={cost:.2f}, "
                      f"v={details['used_vehicles']}, l={details['used_loaders']}")

    if best_solution is None:
        print("No feasible solution found!")
        return None

    print("  Local search on best solution...")
    best_solution.vehicle_routes = apply_two_opt(problem, evaluator, best_solution.vehicle_routes)
    best_solution.vehicle_routes = apply_relocate(problem, evaluator, best_solution.vehicle_routes,
                                                   max_passes=2)
    best_solution.vehicle_routes = apply_swap(problem, evaluator, best_solution.vehicle_routes,
                                               max_passes=2)
    best_solution.vehicle_routes = apply_two_opt(problem, evaluator, best_solution.vehicle_routes)

    vehicle_times = evaluator.extract_vehicle_arrival_times(best_solution)
    best_solution.loader_routes = assign_loaders_greedy(problem, evaluator, vehicle_times)

    best_cost, feasible, details = evaluator.evaluate(best_solution)
    if feasible:
        print(f"  After local search: cost={best_cost:.2f}, "
              f"v={details['used_vehicles']}, l={details['used_loaders']}")

    print("  Loader SA improvement...")
    loader_sa = LoaderSA(problem, evaluator, temp0=100, alpha=0.998,
                         max_iters=50000, time_budget=30.0)
    best_solution = loader_sa.improve(best_solution, vehicle_times)

    best_cost, feasible, details = evaluator.evaluate(best_solution)
    if feasible:
        print(f"  After Loader SA: cost={best_cost:.2f}, "
              f"v={details['used_vehicles']}, l={details['used_loaders']}")
    else:
        print("  Loader SA produced infeasible solution, keeping previous.")

    _, _, evaluation_details = evaluator.evaluate(best_solution)
    all_vehicle_times = evaluation_details.get("vehicle_arrival_times", {})

    vehicle_output = []
    for vehicle_id, route in enumerate(best_solution.vehicle_routes):
        if len(route) <= 2:
            continue
        feasible, start_times, _ = evaluator.is_vehicle_route_feasible(route)
        if not feasible:
            continue
        vehicle_output.append({
            "id": vehicle_id + 1,
            "route": route,
            "time": start_times,
        })

    loader_output = []
    for loader_id, route in enumerate(best_solution.loader_routes):
        if not route:
            continue
        loader_output.append({
            "id": loader_id + 1,
            "route": route,
        })

    return {"vehicles": vehicle_output, "loaders": loader_output}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="instance.json")
    parser.add_argument("--output", default="solution.json")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    with open(args.input, "r") as file:
        data = json.load(file)

    print(f"Orders: {len(data['orders'])}, Seed: {args.seed}")

    start = time.time()
    result = solve(data, seed=args.seed)
    elapsed = time.time() - start

    if result is None:
        print("FAILED to find any feasible solution.")
        sys.exit(1)

    with open(args.output, "w") as file:
        json.dump(result, file, indent=2, ensure_ascii=False)

    print(f"\nTotal time: {elapsed:.1f}s")
    print(f"Solution saved to {args.output}")


if __name__ == "__main__":
    main()