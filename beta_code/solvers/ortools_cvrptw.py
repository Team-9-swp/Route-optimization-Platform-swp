import math

from ortools.constraint_solver import pywrapcp, routing_enums_pb2

from beta_code.solvers.base import VehicleSolver
from beta_code.core.solution import Solution


class ORToolsVehicleSolver(VehicleSolver):
    """OR-Tools CVRPTW solver respecting time windows, capacity, shift length."""

    _solver_name = "ortools"

    SCALE = 100

    def solve(self, time_limit: float, seed: int, **kwargs):
        strategy = kwargs.get(
            "strategy",
            routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION,
        )
        max_vehicles = self._estimate_max_vehicles()

        num_nodes = self.problem.number_of_orders + 1
        manager = pywrapcp.RoutingIndexManager(num_nodes, max_vehicles, 0)
        routing = pywrapcp.RoutingModel(manager)
        SC = self.SCALE

        # -- distance callback (for fuel cost) --
        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return int(self.problem.distance(from_node, to_node) * SC)

        routing.RegisterTransitCallback(distance_callback)

        # -- arc cost = fuel_cost × distance --
        fuel_cost_scaled = int(self.problem.weights["fuel_cost"] * SC)

        def cost_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return int(
                self.problem.distance(from_node, to_node) * fuel_cost_scaled / SC
            )

        routing.SetArcCostEvaluatorOfAllVehicles(
            routing.RegisterTransitCallback(cost_callback)
        )

        # -- Time dimension --
        def time_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            travel = self.problem.travel_time(
                from_node, to_node, self.problem.vehicle_speed
            )
            service = 0.0
            if from_node != 0:
                service = self.problem.order_by_id[from_node]["vehicle_service_time"]
            return int((travel + service) * SC)

        time_cb_id = routing.RegisterTransitCallback(time_callback)
        routing.AddDimension(
            time_cb_id,
            slack_max=86400 * SC,
            capacity=86400 * SC,
            fix_start_cumul_to_zero=False,
            name="Time",
        )
        time_dim = routing.GetDimensionOrDie("Time")

        for order in self.problem.orders:
            node_index = manager.NodeToIndex(order["id"])
            tw_start = int(order["time_window"][0] * SC)
            tw_end = int(order["time_window"][1] * SC)
            time_dim.CumulVar(node_index).SetRange(tw_start, tw_end)

        shift_scaled = int(self.problem.vehicle_shift_length * SC)
        for v in range(max_vehicles):
            time_dim.SetSpanUpperBoundForVehicle(shift_scaled, v)

        # -- Capacity dimension --
        def demand_callback(from_index):
            if from_index < 0:
                return 0
            from_node = manager.IndexToNode(from_index)
            if from_node == 0:
                return 0
            return int(self.problem.order_by_id[from_node]["volume"])

        demand_cb_id = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_cb_id,
            slack_max=0,
            vehicle_capacities=[int(self.problem.vehicle_capacity)] * max_vehicles,
            fix_start_cumul_to_zero=False,
            name="Capacity",
        )

        # -- Optional orders with penalty --
        penalty = int(self.problem.weights["optional_order_penalty"] * SC)
        for order in self.problem.orders:
            if order["optional"] == 1:
                node_index = manager.NodeToIndex(order["id"])
                routing.AddDisjunction([node_index], penalty)

        # -- Fixed cost per used vehicle --
        vehicle_salary_scaled = int(self.problem.weights["vehicle_salary"] * SC)
        for v in range(max_vehicles):
            routing.SetFixedCostOfVehicle(vehicle_salary_scaled, v)

        # -- Search parameters --
        search_params = pywrapcp.DefaultRoutingSearchParameters()
        search_params.first_solution_strategy = strategy
        search_params.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        search_params.time_limit.seconds = int(time_limit)
        search_params.log_search = False

        try:
            assignment = routing.SolveWithParameters(search_params)
        except Exception as e:
            print(f"  [OR-TOOLS EXCEPTION] {e}")
            return None

        if not assignment:
            print(
                f"  [OR-TOOLS] No solution in {time_limit:.0f}s "
                f"(max_vehicles={max_vehicles})"
            )
            return None

        # -- Extract solution --
        solution = Solution()
        for vehicle_id in range(max_vehicles):
            index = routing.Start(vehicle_id)
            route = []
            while not routing.IsEnd(index):
                node = manager.IndexToNode(index)
                route.append(node)
                index = assignment.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))
            if len(route) > 2:
                solution.vehicle_routes.append(route)

        served_order_ids = set()
        for route in solution.vehicle_routes:
            for node in route:
                if node != 0:
                    served_order_ids.add(node)
        for order in self.problem.orders:
            if order["optional"] == 1 and order["id"] not in served_order_ids:
                solution.unserved_optional.add(order["id"])

        return solution

    def _estimate_max_vehicles(self):
        total_mandatory_volume = sum(
            self.problem.order_by_id[oid]["volume"]
            for oid in self.problem.mandatory_order_ids
        )
        min_by_volume = math.ceil(
            total_mandatory_volume / self.problem.vehicle_capacity
        )
        return max(
            min_by_volume * 3,
            int(math.ceil(self.problem.number_of_orders / 3.5)),
            50,
        )
