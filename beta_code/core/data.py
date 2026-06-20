import math

from beta_code.utils.math_utils import round_mathematically


class ProblemData:
    """Stores instance data and pre-computes the distance matrix."""

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
                self.distance_matrix[i][j] = round_mathematically(
                    math.sqrt(dx * dx + dy * dy), 2
                )

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
