def assign_loaders_greedy(problem, evaluator, vehicle_times):
    """
    Build loader routes greedily:
      1. Create a demand entry per required loader, sorted by vehicle arrival time
      2. Insert each demand into the first feasible position in any existing route
      3. If no route accepts it, start a new loader route
    """
    demands = []
    for order in problem.orders:
        if order["loader_cnt"] > 0 and order["id"] in vehicle_times:
            for _ in range(order["loader_cnt"]):
                demands.append((
                    order["id"],
                    vehicle_times[order["id"]],
                    order["loader_service_time"],
                ))

    demands.sort(key=lambda x: (x[1], x[2]))

    loader_routes = []
    for order_id, _, _ in demands:
        placed = False
        best_route_index = -1
        best_position = -1
        best_first_service = float("inf")

        for ri, route in enumerate(loader_routes):
            if order_id in route:
                continue
            for pos in range(len(route) + 1):
                candidate = route[:pos] + [order_id] + route[pos:]
                if evaluator.is_loader_route_feasible(candidate, vehicle_times):
                    first_service = problem.order_by_id[candidate[0]]["loader_service_time"]
                    if first_service < best_first_service:
                        best_first_service = first_service
                        best_route_index = ri
                        best_position = pos
                    break

        if best_route_index >= 0:
            r = loader_routes[best_route_index]
            loader_routes[best_route_index] = r[:best_position] + [order_id] + r[best_position:]
            placed = True

        if not placed:
            loader_routes.append([order_id])

    return loader_routes
