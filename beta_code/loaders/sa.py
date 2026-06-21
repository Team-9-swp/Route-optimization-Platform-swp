import math
import random
import time


class LoaderSA:
    """
    Simulated Annealing over loader routes with fixed vehicle times.
    Operators: relocate, swap, two_opt, merge.
    """

    def __init__(self, problem, evaluator, temp0=100, alpha=0.998,
                 max_iters=50000, time_budget=60.0):
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
