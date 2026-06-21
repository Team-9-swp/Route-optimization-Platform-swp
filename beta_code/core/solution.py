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
