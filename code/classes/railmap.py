import csv
from code.classes.station import Station
from code.classes.connection import Connection

class Railmap():
    """
    The full route system with all trajectories
    """
    def __init__(self, ):
        self.trajectories = {}

    def load_all_files(self, station_path, uid_path, connections_path):
        """
        Reads station and uid file paths, and creates:
            1. a list of (22) Station instances for intercity stations
            2. a list of the (56) possible Connection instances and traveltimes
        """
        # 1
        uids = {}
        with open(uid_path, 'r') as uid_f:
            uid_reader = csv.reader(uid_f)
            next(uid_reader)  # Skip header
            for row in uid_reader:
                name, uid = row
                uids[name] = uid
        stations = []

        with open(station_path, 'r') as station_f:
            station_reader = csv.reader(station_f)
            next(station_reader)
            for row in station_reader:
                name, y, x = row
                uid = uids.get(name)
                stations.append(Station(name, float(y), float(x), uid))
        self.stations = stations

        # 2
        connections = []
        with open(connections_path, 'r') as connect_f:
            connect_reader = csv.reader(connect_f)
            next(connect_reader)
            for row in connect_reader:
                station1, station2, travel_time = row
                connections.append(Connection(station1, station2, int(travel_time)))
                connections.append(Connection(station2, station1, int(travel_time)))
        self.connections = connections

    def add_trajectory(self, train):
        """"Route aanroepen"""
        self.trajectories[train.id] = train


    def quality_K(self):
        #Compute fraction p of used connections
        self.p = 0.8 # example value -> needs to be computed!
        T = len(self.trajectories)
        Min = 0

        for values in self.trajectories.values():
            Min += values[1]

        # compute quality of the lines K
        return (self.p * 10000 - (T * 100 + Min))
