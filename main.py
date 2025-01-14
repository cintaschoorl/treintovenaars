import csv
from code.classes.station import Station
from code.classes.connection import Connection
from code.classes.trajectory import Trajectory
from code.classes.routemap import Routemap


def load_stations(filepath):
    stations = []
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            name, y, x = row
            stations.append(Station(name, float(y), float(x)))
    return stations

def load_connections(filepath): 
    connections = []
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            station1, station2, travel_time = row
            connections.append(Connection(station1, station2, int(travel_time)))
            connections.append(Connection(station2, station1, int(travel_time)))
    return connections


if __name__ == "__main__":
    # Inputbestanden
    stations_file = "data/StationsHolland.csv"
    connections_file = "data/ConnectiesHolland.csv"

    stations = load_stations(stations_file)

    connections = load_connections(connections_file)

    train_1 = Trajectory(connections, 55)
    train_1.add_name('alk_zaa')
    train_1.add_connection('Alkmaar', 'Hoorn')
    train_1.add_connection('Hoorn', 'Zaandam')
    
    # create dictionary with each trajectory and its duration
    # trajectories = {}
    # trajectories['train_1'] = (train_1.traject, train_1.duration)

    # lijntjes = Lines(trajectories)
    # lijntjes.fraction_p()
    # K = lijntjes.quality_K()
    # print(f"The quality of the lines K = {K}")
