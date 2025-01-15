import csv
from code.classes.station import Station
from code.classes.connection import Connection

class Railmap():
    """
    The full route system with all trajectories
    """
    def __init__(self, ):
        self.trajectories = {}

    def load_stations(self, station_path, uid_path, connections_path):
        """
        Reads station, connections and uid file paths, and creates:
            - stations: dict of stations, with a dict per station with 
              neighbouring connections and their travel time
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
        self.stations = {}
        with open(station_path, 'r') as station_f:
            station_reader = csv.reader(station_f)
            next(station_reader)
            for row in station_reader:
                name, y, x = row
                uid = uids.get(name)
                self.stations[name] = (Station(name, float(y), float(x), uid))

        # load connections and add neighbours
        with open(connections_path, 'r') as connect_f:
            connect_reader = csv.reader(connect_f)
            next(connect_reader)

            for row in connect_reader:
                station1_name, station2_name, travel_time = row
                station1 = self.stations.get(station1_name)
                station2 = self.stations.get(station2_name)
                if station1 and station2:
                    station1.add_neighbour(station2, int(travel_time))
                    station2.add_neighbour(station1, int(travel_time))
        

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
