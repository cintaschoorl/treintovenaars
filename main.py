import csv
from code.classes.station import Station
from code.classes.connection import Connection
from code.classes.route import Route
from code.classes.railmap import Railmap


def load_stations(station_path, uid_path):
    """
    Reads stration and uid file paths, and
    creates a list of (22) Station instances for intercity stations.
    """
    # create dict for uid's
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
    return stations

def load_connections(connections_path):
    """
    Reads csv and creates list of the 56 possible connections with its traveltimes
    """
    connections = []
    with open(connections_path, 'r') as connect_f:
        connect_reader = csv.reader(connect_f)
        next(connect_reader)
        for row in connect_reader:
            station1, station2, travel_time = row
            connections.append(Connection(station1, station2, int(travel_time)))
            connections.append(Connection(station2, station1, int(travel_time)))
    return connections


if __name__ == "__main__":
    # file paths
    stations_path = "data/StationsHolland.csv"
    connections_path = "data/ConnectiesHolland.csv"
    uid_path = "data/uid.csv"

    stations = load_stations(stations_path, uid_path)

    connections = load_connections(connections_path)
    print(len(connections))

    # train_1 = Trajectory(connections, 55)
    # train_1.add_name('alk_zaa')
    # train_1.add_connection('Alkmaar', 'Hoorn')
    # train_1.add_connection('Hoorn', 'Zaandam')
    