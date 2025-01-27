import csv
from code.classes.station import Station
from code.classes.route import Route

class Railmap():
    """
    The full route system with all trajectories
    """
    def __init__(self):
        self.stations = []
        self.routes = {}

    def load_stations(self, station_path, uid_path, connections_path):
        """
        Reads station, connections and uid file paths, and creates:
            - stations: list of Station object, with for each station:
                - name: str
                - coordinates: (x, y)
                - neighbours: dict with neighbours and traveltimes as values
        """
        # load uid's into dictionary
        uids = {}
        with open(uid_path, 'r') as uid_f:
            uid_reader = csv.reader(uid_f)
            next(uid_reader)  # Skip header
            for row in uid_reader:
                name, uid = row
                uids[name] = uid

        # load the stations with coordinates and uid's
        name_for_station = {} # helper dict to find Station objects
        with open(station_path, 'r') as station_f:
            station_reader = csv.reader(station_f)
            next(station_reader)
            for row in station_reader:
                name, y, x = row
                uid = uids.get(name)
                if uid:
                    station = Station(name, float(y), float(x), uid)
                    self.stations.append(station)
                    name_for_station[name] = station

        # load connections and add neighbours
        with open(connections_path, 'r') as connect_f:
            connect_reader = csv.reader(connect_f)
            next(connect_reader)

            for row in connect_reader:
                station1_name, station2_name, travel_time = row
                station1 = name_for_station.get(station1_name)
                station2 = name_for_station.get(station2_name)
                if station1 and station2:
                    station1.add_neighbour(station2, int(travel_time))
                    station2.add_neighbour(station1, int(travel_time))


    def add_trajectory(self, train):
        """"Route aanroepen"""
        self.routes[train.id] = train


    def quality_K(self):
        # compute total connections
        total_connections = 0

        for station in self.stations:
            total_connections += len(station.neighbours)

        # ! hier moeten nog de unieke correcte connecties berekend worden!
        # dit is een versimpeling voor een werkend voorbeeld
        ridden_connections = set()
        total_time = 0
        total_routes = len(self.routes)

        for train_id, route in self.routes.items():
            for i in range(len(route.route) - 1):
                station1 = route.route[i]
                station2 = route.route[i + 1]

                # Add connection as a tuple (station1, station2) and its reverse
                ridden_connections.add((station1, station2))
                ridden_connections.add((station2, station1))

            # Sum the travel time of the route
            total_time += route.total_travel_time()


        #Compute fraction p of used connections
        p =  len(ridden_connections) / total_connections

        # computing the quality of the lines K
        return int(p * 10000 - (total_routes * 100 + total_time))
