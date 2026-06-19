import json
import argparse
import logging
import numpy as np
import pandas as pd
from typing import Literal


class NAMES:
    ID = 'id'
    ROUTE = 'route'
    TIME = 'time'

    LOAD_SS = 'loader_shift_size'
    VEH_SS = 'vehicle_shift_size'
    LOAD_TIME = 'load_time'
    VEH_CAPACITY = 'vehicle_capacity'
    VEH_SPEED = 'vehicle_speed'
    LOAD_SPEED = 'loader_speed'

    TIME_WDW = 'time_window'
    VOLUME = 'volume'
    LOADER_CNT = 'loader_cnt'
    VEH_ST = 'vehicle_service_time'
    LOAD_ST = 'loader_service_time'
    OPTIONAL = 'optional'
    X = 'x'
    Y = 'y'
    X1 = X + '_1'
    Y1 = Y + '_1'
    X2 = X + '_2'
    Y2 = Y + '_2'

    OPTIONAL_PENALTY = 'optional_order_penalty'
    LOAD_SALARY = 'loader_salary'
    VEH_SALARY = 'vehicle_salary'
    VEH_FC = 'fuel_cost'
    LOAD_W = 'loader_work'


class OUTPUT:
    veh_saf = 'DepotStartAndFinish'
    veh_ss = 'VehicleShiftSize'
    veh_cap = 'VehicleCapacity'
    load_saf = 'LoaderStartAndFinish'
    load_ss = 'LoaderShiftSize'
    TW_VIOL = 'TimeWindowViolation'
    unsch_orders = 'MandatoryUnscheduledOrders'
    veh_route_seq = 'VehicleRouteSequence'
    load_route_seq = 'LoaderRouteSequence'
    invalid_orders = 'InvalidOrders'

    veh_fc = 'VehicleFuelCost'
    veh_shifts = 'VehicleShifts'
    load_shifts = 'LoaderShifts'
    load_wt = 'LoaderWorkTime'
    unsch_optional = 'OptionalUnscheduledOrders'


def strict_round(nums: pd.Series | float, accuracy: int = 0) -> pd.Series | float:
    if accuracy == 0:
        return np.floor(nums + 0.5)
    else:
        multiplier = 10 ** accuracy
        return np.floor(nums * multiplier + (0.5 * np.sign(nums))) / multiplier


RouteTypes = Literal['Vehicle', 'Loader']


class Validator:
    def __init__(self, input_file_path, result_file_path):
        self._logger = logging.getLogger("Validator")
        self._logger.setLevel(0)
        self._logger.disabled = False

        self.orders = pd.DataFrame()
        self.weights = {}
        self.depot = {}
        self.params = {}

        self._read_input_data(input_file_path)

        self.vehicle_routes = pd.DataFrame()
        self.loader_routes = pd.DataFrame()

        self._read_result_data(result_file_path)

        self.violations = {
            OUTPUT.veh_route_seq: 0,
            OUTPUT.load_route_seq: 0,
            OUTPUT.invalid_orders: 0,
            OUTPUT.veh_saf: 0,
            OUTPUT.veh_ss: 0,
            OUTPUT.veh_cap: 0,
            OUTPUT.load_saf: 0,
            OUTPUT.load_ss: 0,
            OUTPUT.TW_VIOL: 0,
            OUTPUT.unsch_orders: 0,
        }

        self.costs = {
            OUTPUT.veh_fc: [0, self.weights[NAMES.VEH_FC], 0],
            OUTPUT.veh_shifts: [0, self.weights[NAMES.VEH_SALARY], 0],
            OUTPUT.load_shifts: [0, self.weights[NAMES.LOAD_SALARY], 0],
            OUTPUT.load_wt: [0, self.weights[NAMES.LOAD_W], 0],
            OUTPUT.unsch_optional: [0, self.weights[NAMES.OPTIONAL_PENALTY], 0],
        }

    @classmethod
    def from_dicts(cls, input_data: dict, result_data: dict):
        v = cls.__new__(cls)
        v._logger = logging.getLogger("Validator")
        v._logger.setLevel(0)
        v._logger.disabled = False

        v.orders = pd.concat([
            pd.DataFrame({
                NAMES.ID: [0],
                NAMES.X: [input_data["depot"][NAMES.X]],
                NAMES.Y: [input_data["depot"][NAMES.Y]],
                NAMES.TIME_WDW: [[0, 100000]],
                NAMES.VEH_ST: [input_data["depot"][NAMES.LOAD_TIME]],
                NAMES.VOLUME: [0],
            }),
            pd.DataFrame(input_data["orders"]),
        ], ignore_index=True).set_index(NAMES.ID, drop=False)
        v.orders.index.name = 'index'

        v.weights = input_data["weights"]
        v.depot = input_data["depot"]
        v.params = {
            k: v for k, v in input_data.items()
            if k not in ["orders", "weights", "depot"]
        }

        v.vehicle_routes = pd.DataFrame(result_data.get("vehicles", []), columns=[NAMES.ID, NAMES.ROUTE, NAMES.TIME])
        v.loader_routes = pd.DataFrame(result_data.get("loaders", []), columns=[NAMES.ID, NAMES.ROUTE])

        v.violations = {
            OUTPUT.veh_route_seq: 0,
            OUTPUT.load_route_seq: 0,
            OUTPUT.invalid_orders: 0,
            OUTPUT.veh_saf: 0,
            OUTPUT.veh_ss: 0,
            OUTPUT.veh_cap: 0,
            OUTPUT.load_saf: 0,
            OUTPUT.load_ss: 0,
            OUTPUT.TW_VIOL: 0,
            OUTPUT.unsch_orders: 0,
        }

        v.costs = {
            OUTPUT.veh_fc: [0, v.weights[NAMES.VEH_FC], 0],
            OUTPUT.veh_shifts: [0, v.weights[NAMES.VEH_SALARY], 0],
            OUTPUT.load_shifts: [0, v.weights[NAMES.LOAD_SALARY], 0],
            OUTPUT.load_wt: [0, v.weights[NAMES.LOAD_W], 0],
            OUTPUT.unsch_optional: [0, v.weights[NAMES.OPTIONAL_PENALTY], 0],
        }

        return v

    def _dist(self, point_id_1, point_id_2):
        return strict_round(np.linalg.norm(np.array(self.orders.loc[point_id_1, [NAMES.X, NAMES.Y]])
                                           - np.array(self.orders.loc[point_id_2, [NAMES.X, NAMES.Y]])), 2)

    def _dist_to_depot(self, point_id):
        return self._dist(point_id, 0)

    def _read_input_data(self, input_file_path) -> None:
        with open(input_file_path, "r") as input_file:
            input_data = json.load(input_file)
        self.orders = pd.concat([
            pd.DataFrame({
                NAMES.ID: [0],
                NAMES.X: [input_data["depot"][NAMES.X]],
                NAMES.Y: [input_data["depot"][NAMES.Y]],
                NAMES.TIME_WDW: [[0, 100000]],
                NAMES.VEH_ST: [input_data["depot"][NAMES.LOAD_TIME]],
                NAMES.VOLUME: [0],
            }),
            pd.DataFrame(input_data["orders"]),
        ], ignore_index=True).set_index(NAMES.ID, drop=False)
        self.orders.index.name = 'index'

        self.weights = input_data["weights"]
        self.depot = input_data["depot"]
        self.params = {
            k: v for k, v in input_data.items()
            if k not in ["orders", "weights", "depot"]
        }

    def _read_result_data(self, result_file_path) -> None:
        with open(result_file_path, "r") as result_file:
            result_data = json.load(result_file)

        self.vehicle_routes = pd.DataFrame(result_data.get("vehicles", []), columns=[NAMES.ID, NAMES.ROUTE, NAMES.TIME])
        self.loader_routes = pd.DataFrame(result_data.get("loaders", []), columns=[NAMES.ID, NAMES.ROUTE])

    def _proc_result_data(self):
        if not self.vehicle_routes.empty:
            self.vehicle_routes = (
                self.vehicle_routes
                .assign(**{
                    NAMES.TIME: lambda df: df.apply(
                        lambda row:
                        [strict_round(
                            row[NAMES.TIME][0] - strict_round(
                                self._dist_to_depot(row[NAMES.ROUTE][1]) / self.params[NAMES.VEH_SPEED], 2), 2)]
                        + row[NAMES.TIME]
                        + [strict_round(
                            row[NAMES.TIME][-1] + strict_round(
                                self._dist_to_depot(row[NAMES.ROUTE][-2]) / self.params[NAMES.VEH_SPEED], 2)
                            + self.orders.loc[row[NAMES.ROUTE][-2], NAMES.VEH_ST],
                            2)], axis=1),
                })
            )
        if not self.loader_routes.empty:
            veh_routes_orders = self.vehicle_routes[NAMES.ROUTE].sum() if not self.vehicle_routes.empty else []
            self.loader_routes = (
                self.loader_routes
                .assign(**{
                    NAMES.ROUTE: lambda df: df[NAMES.ROUTE].apply(lambda x: [_ for _ in x if _ in veh_routes_orders]),
                })
                .assign(route_len=lambda df: df[NAMES.ROUTE].apply(lambda x: len(x)))
                .query('route_len > 0')
                .drop(columns='route_len')
                .assign(**{
                    NAMES.ROUTE: lambda df: df.apply(lambda row: row[NAMES.ROUTE] + [row[NAMES.ROUTE][0]], axis=1),
                })
            )

    def _correct_orders_id(self, routes: pd.DataFrame, name: RouteTypes):
        assert name in ['Vehicle', 'Loader']

        invalid_id = (
            routes
            .explode(NAMES.ROUTE)
            .query(f"{NAMES.ROUTE} != 0")
            .assign(invalid=lambda df: ~(df[NAMES.ROUTE].isin(self.orders[NAMES.ID])))
            .query("invalid")
        )
        if not invalid_id.empty:
            self._logger.warning(f"\n{name} routes contains invalid orders:\n "
                                 + str(invalid_id[[NAMES.ID, NAMES.ROUTE]].drop_duplicates().groupby(NAMES.ID)
                                       .agg(**{"Invalid orders": pd.NamedAgg(NAMES.ROUTE, lambda x: list(x))})))
            self.violations[OUTPUT.invalid_orders] += invalid_id.shape[0]

            if name == 'Vehicle':
                self.vehicle_routes[NAMES.TIME] = self.vehicle_routes[[NAMES.TIME, NAMES.ROUTE]].apply(
                    lambda row: [row[NAMES.TIME][i] for i in range(len(row[NAMES.TIME]))
                                 if row[NAMES.ROUTE][i + 1] in self.orders.loc[:, NAMES.ID]],
                    axis=1
                )
                self.vehicle_routes[NAMES.ROUTE] = self.vehicle_routes[NAMES.ROUTE].apply(
                    lambda x: [_ for _ in x if _ in self.orders.loc[:, NAMES.ID]]
                )
            else:
                self.loader_routes[NAMES.ROUTE] = self.loader_routes[NAMES.ROUTE].apply(
                    lambda x: [_ for _ in x if _ in self.orders.loc[:, NAMES.ID]]
                )

    def _correct_start_time(self, routes: pd.DataFrame, name: RouteTypes):
        assert name in ['Vehicle', 'Loader']
        if routes.empty:
            return

        service_time_name = NAMES.VEH_ST if name == 'Vehicle' else NAMES.LOAD_ST
        speed = self.params[NAMES.VEH_SPEED] if name == "Vehicle" else self.params[NAMES.LOAD_SPEED]

        if name == 'Vehicle':
            points = (
                routes
                .assign(
                    point=routes[NAMES.ROUTE].apply(lambda x: x[:-1]),
                    next_point=routes[NAMES.ROUTE].apply(lambda x: x[1:]),
                    time=routes[NAMES.TIME].apply(lambda x: x[:-1]),
                    next_time=routes[NAMES.TIME].apply(lambda x: x[1:]),
                )
                .explode(['next_point', 'point', 'time', 'next_time'])
            )
        else:
            points = (
                routes
                .assign(
                    point=routes[NAMES.ROUTE].apply(lambda x: x[:-1]),
                    next_point=routes[NAMES.ROUTE].apply(lambda x: x[1:]),
                )
                .explode(['next_point', 'point'])
                .merge(self.vehicle_routes[[NAMES.ROUTE, NAMES.TIME]]
                       .explode([NAMES.ROUTE, NAMES.TIME])
                       .rename(columns={NAMES.ROUTE: 'point', NAMES.TIME: 'time'}),
                       on=['point'], how='left')
                .merge(self.vehicle_routes[[NAMES.ROUTE, NAMES.TIME]]
                       .explode([NAMES.ROUTE, NAMES.TIME])
                       .rename(columns={NAMES.ROUTE: 'next_point', NAMES.TIME: 'next_time'}),
                       on=['next_point'], how='left')
                .assign(
                    next_time=lambda df: df.apply(
                        lambda row: strict_round(
                            self.orders.loc[row['point'], NAMES.LOAD_ST] + row['time']
                            + strict_round(self._dist(row['point'], row['next_point']) / speed, 2), 2)
                        if row[NAMES.ROUTE][-1] == row['next_point'] else row['next_time'],
                        axis=1)
                )
            )

        points = (
            points
            .merge(self.orders[[NAMES.ID, NAMES.X, NAMES.Y, service_time_name, NAMES.TIME_WDW]]
                   .rename(columns={NAMES.ID: 'point_id'}),
                   left_on='point', right_on='point_id',
                   how='left')
            .merge(self.orders[[NAMES.ID, NAMES.X, NAMES.Y]]
                   .rename(columns={NAMES.ID: 'point_id'}),
                   left_on='next_point', right_on='point_id', how='left',
                   suffixes=('_1', '_2'))
        )
        if name == 'Vehicle':
            route_start_indices = points.groupby(NAMES.ID)['time'].idxmin()
            points.loc[route_start_indices, NAMES.VEH_ST] = 0

        points = (
            points
            .assign(
                travel_time=lambda df: strict_round(
                    strict_round(np.sqrt((df[NAMES.X1] - df[NAMES.X2]) ** 2 + (df[NAMES.Y1] - df[NAMES.Y2]) ** 2), 2)
                    / speed, 2),
                min_correct_time=lambda df: strict_round(df.time + df[service_time_name] + df.travel_time, 2),
                is_achievable=lambda df: df['min_correct_time'] <= df.next_time,
            )
        )
        if name == 'Vehicle':
            points = (
                points
                .assign(
                    in_window=lambda df: df.apply(
                        lambda row: row[NAMES.TIME_WDW][0] <= row['time'] <= row[NAMES.TIME_WDW][1], axis=1)
                )
            )
            not_in_window = points.query("not in_window")
            if not not_in_window.empty:
                self._logger.warning(f"\n{name} start times do not fall within the time windows:\n "
                                     + str(not_in_window[[NAMES.ID, 'point']].drop_duplicates().groupby(NAMES.ID)
                                           .agg(**{"Invalid orders": pd.NamedAgg('point', lambda x: list(x))}))
                                     )
                self.violations[OUTPUT.TW_VIOL] = not_in_window.shape[0]

        unachievable = points.query("not is_achievable")
        if not unachievable.empty:
            self._logger.warning(
                f"\n{name} incorrect times:\n "
                + str(unachievable
                      .assign(released=lambda df: df['time'] + df[service_time_name])
                      [[NAMES.ID, 'next_point', 'released', 'travel_time', 'min_correct_time', 'next_time']]
                      .rename(
                    columns={NAMES.ID: f'{name}_id', 'next_point': 'point',
                             'next_time': 'solution_time', })
                      .set_index(f'{name}_id')
                      .to_string()
                      )
            )
            viol_name = OUTPUT.veh_route_seq if name == 'Vehicle' else OUTPUT.load_route_seq
            self.violations[viol_name] = unachievable.shape[0]

        shift_max = self.params[(NAMES.VEH_SS if name == "Vehicle" else NAMES.LOAD_SS)]
        shift_length = (
            points
            .groupby(NAMES.ID)
            .agg({'time': 'first', 'next_time': 'last'})
            .assign(shift_time=lambda df: df['next_time'] - df['time'])
        )

        shift_length = (
            shift_length
            .query(f'shift_time >= {shift_max}')
        )
        if not shift_length.empty:
            self._logger.warning(f"\n{name} exceeding the shift duration: "
                                 + ', '.join([str(_) for _ in shift_length.index.astype(int).values])
                                 )
            self.violations[f'{name}{OUTPUT.load_ss[6:]}'] = shift_length.shape[0]

    def _correct_capacities(self, routes: pd.DataFrame):
        def route_to_circles(route: list):
            route = ['-' if i == 0 else i for i in route]
            circles = [[int(i) for i in group.split()] for group in ' '.join(map(str, route)).split('-') if group]
            return circles

        capacities = (
            routes
            .assign(
                circles=lambda df: df[NAMES.ROUTE].apply(route_to_circles),
                circles_num=lambda df: df.circles.apply(lambda x: list(range(len(x)))),
            )
            .explode(['circles', 'circles_num'])
            .explode('circles')
            .merge(self.orders[[NAMES.ID, NAMES.VOLUME]].rename(columns={NAMES.ID: 'circles'}),
                   on='circles', how='left')
            .groupby(NAMES.ID)
            .agg({NAMES.VOLUME: 'sum'})
            .query(f'{NAMES.VOLUME} > {self.params[NAMES.VEH_CAPACITY]}')
        )
        if not capacities.empty:
            self._logger.warning(f"\nVehicle with violation of capacity: "
                                 + ', '.join([str(_) for _ in capacities.index.values])
                                 )
            self.violations[OUTPUT.veh_cap] = capacities.shape[0]

    def _complete_order(self):
        orders = (
            self.orders
            .query(f'{NAMES.ID} != 0')
            .merge(self.vehicle_routes.explode([NAMES.ROUTE, NAMES.TIME])
                   .rename(columns={NAMES.ID: 'veh_id'}),
                   how='left', left_on=NAMES.ID, right_on=NAMES.ROUTE)
            .merge(self.loader_routes.explode([NAMES.ROUTE])
                   .rename(columns={NAMES.ID: 'loader_id'}),
                   how='left', left_on=NAMES.ID, right_on=NAMES.ROUTE)
        )

        complete = (
            orders
            .groupby([NAMES.ID, 'veh_id', NAMES.LOADER_CNT, NAMES.OPTIONAL], as_index=False, dropna=False)
            .agg({'loader_id': lambda x: sum(x.notna())})
            .assign(
                loaders_enought=lambda df: df[NAMES.LOADER_CNT] <= df['loader_id'],
                no_veh=lambda df: df['veh_id'].isna(),
                incomplete=lambda df: ~df['loaders_enought'] | df['no_veh']
            )
            .groupby([NAMES.ID, NAMES.OPTIONAL], as_index=False, dropna=False)
            .agg({"incomplete": lambda x: all(x)})
        )
        incomplete_obligatory = complete.query(f"{NAMES.OPTIONAL} == 0 and incomplete")
        if not incomplete_obligatory.empty:
            self._logger.warning(
                f"\nIncomplete obligatory orders: {', '.join(incomplete_obligatory[NAMES.ID].astype(str).values)}")
            self.violations[OUTPUT.unsch_orders] = incomplete_obligatory.shape[0]

        incomplete_optional = complete.query(f"{NAMES.OPTIONAL} == 1 and incomplete")
        if not incomplete_optional.empty:
            self._logger.warning(
                f"\nIncomplete optional orders: {', '.join(incomplete_optional[NAMES.ID].astype(str).values)}")
            self.costs[OUTPUT.unsch_optional][2] = incomplete_optional.shape[0]
            self.costs[OUTPUT.unsch_optional][0] = (self.costs[OUTPUT.unsch_optional][1]
                                                    * self.costs[OUTPUT.unsch_optional][2])

    def _start_and_finish(self):
        depot_start_and_finish = (
            self.vehicle_routes
            .assign(is_correct=lambda df: df[NAMES.ROUTE].apply(lambda x: x[0] == x[-1] == 0))
            .query('not is_correct')
        )
        if not depot_start_and_finish.empty:
            self._logger.warning(
                f"\nVehicle routes have to start and finish in depot. \n"
                f"Incorrect routes for {', '.join(depot_start_and_finish[NAMES.ID].astype(str).values)} vehicle")
            self.violations[OUTPUT.veh_saf] = depot_start_and_finish.shape[0]

        loader_start_and_finish = (
            self.loader_routes
            .assign(is_correct=lambda df: df[NAMES.ROUTE].apply(lambda x: x[0] == x[-1]))
            .query('not is_correct')
        )
        if not loader_start_and_finish.empty:
            self._logger.warning(
                f"\nLoader routes have to start and finish in same point. \n"
                f"Incorrect routes for {', '.join(loader_start_and_finish[NAMES.ID].astype(str).values)} vehicle")
            self.violations[OUTPUT.load_saf] = loader_start_and_finish.shape[0]

    def _route_dist_calc(self, routes: pd.DataFrame, name: RouteTypes) -> float:
        assert name in ['Vehicle', 'Loader']

        speed = self.params[NAMES.VEH_SPEED] if name == "Vehicle" else self.params[NAMES.LOAD_SPEED]
        dist_times = (
            routes
            .assign(
                point=routes[NAMES.ROUTE].apply(lambda x: x[:-1]),
                next_point=routes[NAMES.ROUTE].apply(lambda x: x[1:]),
            )
            .explode(['next_point', 'point'])
            .merge(self.orders[[NAMES.ID, NAMES.X, NAMES.Y]]
                   .rename(columns={NAMES.ID: 'point_id'}),
                   left_on='point', right_on='point_id',
                   how='left')
            .merge(self.orders[[NAMES.ID, NAMES.X, NAMES.Y]].rename(columns={NAMES.ID: 'point_id'}),
                   left_on='next_point', right_on='point_id', how='left',
                   suffixes=('_1', '_2'))
            .assign(
                travel_time=lambda df: strict_round(
                    strict_round(np.sqrt((df[NAMES.X1] - df[NAMES.X2]) ** 2 + (df[NAMES.Y1] - df[NAMES.Y2]) ** 2), 2)
                    / speed, 2)
            )
        )
        return strict_round(dist_times['travel_time'].sum(), 2)

    def _route_time_calc(self, routes: pd.DataFrame, name: RouteTypes) -> float:
        assert name in ['Vehicle', 'Loader']

        times = (
            routes
            .assign(
                start_point=routes[NAMES.ROUTE].apply(lambda x: x[0]),
                end_point=routes[NAMES.ROUTE].apply(lambda x: x[-1]),
            )
        )
        if name == 'Loader':
            times = (
                times
                .merge(
                    self.vehicle_routes[[NAMES.ROUTE, NAMES.TIME]].explode([NAMES.ROUTE, NAMES.TIME])
                    .rename(columns={NAMES.TIME: 'start_time'}),
                    how='left', left_on='start_point', right_on=NAMES.ROUTE
                )
                .merge(
                    self.vehicle_routes[[NAMES.ROUTE, NAMES.TIME]].explode([NAMES.ROUTE, NAMES.TIME])
                    .rename(columns={NAMES.TIME: 'end_time'}),
                    how='left', left_on='end_point', right_on=NAMES.ROUTE
                )
                .merge(self.orders[[NAMES.ID, NAMES.LOAD_ST]].rename(columns={NAMES.ID: 'end_point'}),
                       how='left', on='end_point')
                .assign(
                    end_time=lambda df: df['end_time'] + df[NAMES.LOAD_ST],
                )
            )
        else:
            times = times.assign(
                start_time=routes[NAMES.TIME].apply(lambda x: x[0]),
                end_time=routes[NAMES.TIME].apply(lambda x: x[-1]),
            )

        return strict_round((times['end_time'] - times['start_time']).sum(), 2)

    def _output(self):
        separator = '.'
        min_spacing = 3
        max_key_len = max([len(str(k)) for k in self.violations.keys()] + [len(str(k)) for k in self.costs.keys()])
        max_val_len = max(
            [len(str(k)) for k in self.violations.values()] + [len(str(k[0])) for k in self.costs.values()])

        common_len = max_key_len + min_spacing + max_val_len

        self._logger.warning('VIOLATIONS:')
        for key, value in self.violations.items():
            dots = separator.ljust(common_len - len(str(key)) - len(str(value)), '.')
            self._logger.warning(f"{key}{dots}{value}")
        self._logger.warning(f"Total violations = {sum(self.violations.values())}")

        self._logger.warning('\nCOSTS (weight X cost):')
        for key, value in self.costs.items():
            dots = separator.ljust(common_len - len(str(key)) - len(str(value[0])), '.')
            self._logger.warning(f"{key}{dots}{value[0]} ({value[1]} X {value[2]})")
        self._logger.warning(f"Total cost = {strict_round(sum([v[0] for v in self.costs.values()]), 2)}")

    def get_results(self):
        return {
            "violations": self.violations,
            "total_violations": sum(self.violations.values()),
            "costs": {k: v[0] for k, v in self.costs.items()},
            "total_cost": strict_round(sum([v[0] for v in self.costs.values()]), 2),
        }

    def validation(self):
        if not self.vehicle_routes[NAMES.ID].is_unique:
            self._logger.warning("Vehicle IDs is not unique. The IDs will be replaced with consecutive ones.")
            self.vehicle_routes[NAMES.ID] = np.arange(1, self.vehicle_routes.shape[0] + 1)

        if not self.vehicle_routes.explode(NAMES.ROUTE).query(f"{NAMES.ROUTE}!=0")[NAMES.ROUTE].is_unique:
            raise Exception("Orders in vehicle routes is not unique")

        if not self.loader_routes[NAMES.ID].is_unique:
            self._logger.warning("Loaders IDs is not unique. The IDs will be replaced with consecutive ones.")
            self.loader_routes[NAMES.ID] = np.arange(1, self.loader_routes.shape[0] + 1)

        self._correct_orders_id(self.vehicle_routes, name="Vehicle")
        self._correct_orders_id(self.loader_routes, name="Loader")

        self._proc_result_data()

        self._start_and_finish()

        self._correct_start_time(self.vehicle_routes, name="Vehicle")
        self._correct_start_time(self.loader_routes, name="Loader")

        self._correct_capacities(self.vehicle_routes)

        self._complete_order()

        self.costs[OUTPUT.veh_shifts][2] = self.vehicle_routes.shape[0]
        self.costs[OUTPUT.veh_shifts][0] = (self.costs[OUTPUT.veh_shifts][1] * self.costs[OUTPUT.veh_shifts][2])
        self.costs[OUTPUT.load_shifts][2] = self.loader_routes.shape[0]
        self.costs[OUTPUT.load_shifts][0] = (self.costs[OUTPUT.load_shifts][1] * self.costs[OUTPUT.load_shifts][2])

        self.costs[OUTPUT.veh_fc][2] = self._route_dist_calc(self.vehicle_routes, name="Vehicle")
        self.costs[OUTPUT.veh_fc][0] = strict_round(self.costs[OUTPUT.veh_fc][1] * self.costs[OUTPUT.veh_fc][2], 2)
        self.costs[OUTPUT.load_wt][2] = self._route_time_calc(self.loader_routes, name="Loader")
        self.costs[OUTPUT.load_wt][0] = strict_round(self.costs[OUTPUT.load_wt][1] * self.costs[OUTPUT.load_wt][2], 2)

        self._output()

        return self.get_results()


def validate_solution(input_data: dict, solution_dict: dict, quiet: bool = True) -> dict:
    v = Validator.from_dicts(input_data, solution_dict)
    if quiet:
        v._logger.disabled = True
    return v.validation()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default='../data', help="Validate data in dir (default 'data')")
    parser.add_argument("--input_file", type=str, default='input',
                        help="Name of instance input file (default 'input')")
    parser.add_argument("--result_file", type=str, default='result',
                        help="Name of instance result file (default 'result')")

    args = parser.parse_args()

    directory = args.dir
    input_file_name = args.input_file
    result_file_name = args.result_file

    input_file_path = f"{directory}/{input_file_name}.json"
    result_file_path = f"{directory}/{result_file_name}.json"
    Validator(input_file_path, result_file_path).validation()
