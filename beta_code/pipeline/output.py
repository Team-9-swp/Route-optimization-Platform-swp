def format_solution_output(solution, evaluator):
    """Convert a Solution object into the output JSON dict."""

    vehicle_output = []
    for vid, route in enumerate(solution.vehicle_routes):
        if len(route) <= 2:
            continue
        ok, times, _ = evaluator.is_vehicle_route_feasible(route)
        if not ok:
            continue
        vehicle_output.append({"id": vid + 1, "route": route, "time": times})

    loader_output = []
    for lid, route in enumerate(solution.loader_routes):
        if not route:
            continue
        loader_output.append({"id": lid + 1, "route": route})

    return {"vehicles": vehicle_output, "loaders": loader_output}
