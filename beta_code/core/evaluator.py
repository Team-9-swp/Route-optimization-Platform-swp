from beta_code.utils.math_utils import round_mathematically


class Evaluator:
    """Feasibility checks and cost evaluation — mirrors the official validator."""

    def __init__(self, problem):
        self.problem = problem

    def is_vehicle_route_feasible(self, route):
        if len(route) <= 2:
            return True, [], 0.0

        orders = [n for n in route if n != 0]

        pure = {}
        t = 0.0
        total_distance = 0.0
        for i in range(len(route) - 1):
            f, to_node = route[i], route[i + 1]
            travel = self.problem.travel_time(f, to_node, self.problem.vehicle_speed)
            t += travel
            total_distance += self.problem.distance(f, to_node)
            if to_node != 0:
                pure[to_node] = t
                t += self.problem.order_by_id[to_node]["vehicle_service_time"]

        upper_E = float("inf")
        for node in orders:
            tw_start, tw_end = self.problem.order_by_id[node]["time_window"]
            upper_E = min(upper_E, tw_end - pure[node])
        if upper_E < -1e-6:
            return False, [], 0.0
        E = max(0.0, upper_E)

        start_times = []
        t = E
        for i in range(len(route) - 1):
            f, to_node = route[i], route[i + 1]
            t += self.problem.travel_time(f, to_node, self.problem.vehicle_speed)
            if to_node != 0:
                tw_start, tw_end = self.problem.order_by_id[to_node]["time_window"]
                actual = max(t, tw_start)
                if actual > tw_end + 1e-6:
                    return False, [], 0.0
                start_times.append(round_mathematically(actual, 2))
                t = actual + self.problem.order_by_id[to_node]["vehicle_service_time"]

        if t - E > self.problem.vehicle_shift_length + 1e-6:
            return False, [], 0.0

        total_volume = sum(self.problem.order_by_id[node]["volume"] for node in orders)
        if total_volume > self.problem.vehicle_capacity + 1e-6:
            return False, [], 0.0

        return True, start_times, total_distance

    def is_loader_route_feasible(self, route, vehicle_times):
        if not route:
            return True
        first = route[0]
        if first not in vehicle_times:
            return False
        t = (
            vehicle_times[first]
            + self.problem.order_by_id[first]["loader_service_time"]
        )
        for i in range(1, len(route)):
            prev, node = route[i - 1], route[i]
            t += self.problem.travel_time(prev, node, self.problem.loader_speed)
            if node not in vehicle_times:
                return False
            if t > vehicle_times[node] + 1e-6:
                return False
            t = (
                vehicle_times[node]
                + self.problem.order_by_id[node]["loader_service_time"]
            )
        t += self.problem.travel_time(route[-1], first, self.problem.loader_speed)
        return t - vehicle_times[first] <= self.problem.loader_shift_length + 1e-6

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
            for node in route:
                if node != 0:
                    vehicle_times[node] = times[idx]
                    idx += 1

        total_l_work = 0.0
        loader_cnt = {order["id"]: 0 for order in self.problem.orders}
        for lr in solution.loader_routes:
            if not lr:
                continue
            for node in lr:
                loader_cnt[node] += 1
            if not self.is_loader_route_feasible(lr, vehicle_times):
                return float("inf"), False, {}
            total_l_work += self.problem.order_by_id[lr[0]]["loader_service_time"]

        has_loader_routes = any(lr for lr in solution.loader_routes)
        if has_loader_routes:
            for order in self.problem.orders:
                if order["id"] in served and order["loader_cnt"] > 0:
                    if loader_cnt[order["id"]] < order["loader_cnt"]:
                        return float("inf"), False, {}

        used_v = solution.number_of_vehicles_in_use()
        used_l = solution.number_of_loaders_in_use()
        cost = (
            used_v * self.problem.weights["vehicle_salary"]
            + total_v_dist * self.problem.weights["fuel_cost"]
            + used_l * self.problem.weights["loader_salary"]
            + total_l_work * self.problem.weights["loader_work"]
            + len(solution.unserved_optional)
            * self.problem.weights["optional_order_penalty"]
        )
        return (
            cost,
            True,
            {
                "used_vehicles": used_v,
                "vehicle_distance": total_v_dist,
                "used_loaders": used_l,
                "loader_work": total_l_work,
                "unserved_optional": len(solution.unserved_optional),
                "vehicle_times": vehicle_times,
            },
        )

    def extract_vehicle_times(self, solution):
        times = {}
        for route in solution.vehicle_routes:
            if len(route) <= 2:
                continue
            ok, start_times, _ = self.is_vehicle_route_feasible(route)
            if not ok:
                continue
            idx = 0
            for node in route:
                if node != 0:
                    times[node] = start_times[idx]
                    idx += 1
        return times
